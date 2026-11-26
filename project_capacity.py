"""Calculate capacity from live GitHub Projects fields, then write results back.

No backlog.json dependency. A capacity row has a title beginning [Capacity], one
assignee, an iteration, daily hours, and optional ISO dates/ranges for leave.
"""
import argparse
from datetime import date, datetime, timedelta, timezone
import json
import math
import os
from pathlib import Path
import urllib.request

from studyflow import sprint_capacity

INPUTS = {'Часов в день': 'NUMBER', 'Отпуск': 'TEXT'}
OUTPUTS = {'Доступно, ч': 'NUMBER', 'Запланировано, ч': 'NUMBER',
           'Перегрузка, ч': 'NUMBER', 'Расчёт загрузки': 'TEXT'}
FRAGMENT = '''fieldValues(first:100){nodes{
 ... on ProjectV2ItemFieldNumberValue {number field{... on ProjectV2Field{name}}}
 ... on ProjectV2ItemFieldTextValue {text field{... on ProjectV2Field{name}}}
 ... on ProjectV2ItemFieldSingleSelectValue {name field{... on ProjectV2SingleSelectField{name}}}
 ... on ProjectV2ItemFieldIterationValue {iterationId title startDate duration field{... on ProjectV2IterationField{name}}}
}} content{
 ... on Issue{id number title url closed assignees(first:100){nodes{login} pageInfo{hasNextPage}}}
 ... on DraftIssue{id title assignees(first:100){nodes{login} pageInfo{hasNextPage}}}
}'''


class GitHub:
    def __init__(self, token):
        self.token = token

    def query(self, query, **variables):
        request = urllib.request.Request('https://api.github.com/graphql',
            data=json.dumps({'query': query, 'variables': variables}).encode(),
            headers={'Authorization': f'Bearer {self.token}', 'User-Agent': 'StudyFlow-capacity',
                     'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
        if result.get('errors'):
            raise RuntimeError(json.dumps(result['errors'], ensure_ascii=False))
        return result['data']

    def project(self, owner, number):
        return self.query('''query($owner:String!,$number:Int!){user(login:$owner){projectV2(number:$number){
          id title url fields(first:100){nodes{
           ... on ProjectV2Field{id name dataType}
           ... on ProjectV2SingleSelectField{id name dataType}
           ... on ProjectV2IterationField{id name dataType}
          } pageInfo{hasNextPage}}
        }}}''', owner=owner, number=number)['user']['projectV2']

    def items(self, project_id):
        result, cursor = [], None
        while True:
            page = self.query('''query($id:ID!,$cursor:String){node(id:$id){... on ProjectV2{
              items(first:100,after:$cursor){nodes{id isArchived ''' + FRAGMENT + '''}
              pageInfo{hasNextPage endCursor}}}}}''', id=project_id, cursor=cursor)['node']['items']
            result.extend(page['nodes'])
            if not page['pageInfo']['hasNextPage']:
                return result
            cursor = page['pageInfo']['endCursor']

    def set_field(self, project_id, item_id, field_id, value):
        self.query('''mutation($project:ID!,$item:ID!,$field:ID!,$value:ProjectV2FieldValue!){
          updateProjectV2ItemFieldValue(input:{projectId:$project,itemId:$item,fieldId:$field,value:$value}){
            projectV2Item{id}}}''', project=project_id, item=item_id, field=field_id, value=value)

    def clear_field(self, project_id, item_id, field_id):
        self.query('''mutation($project:ID!,$item:ID!,$field:ID!){
          clearProjectV2ItemFieldValue(input:{projectId:$project,itemId:$item,fieldId:$field}){
            projectV2Item{id}}}''', project=project_id, item=item_id, field=field_id)


def fields(item):
    values = {}
    for value in item['fieldValues']['nodes']:
        if value.get('field', {}).get('name'):
            values[value['field']['name']] = value
    return values


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f'{label}: требуется неотрицательное число')
    return value


def leave_dates(text):
    days = set()
    for part in text.replace('\n', ',').split(','):
        if not part.strip():
            continue
        bounds = part.strip().split('..')
        if len(bounds) > 2:
            raise ValueError('Отпуск: формат YYYY-MM-DD..YYYY-MM-DD, даты через запятую')
        start, end = date.fromisoformat(bounds[0]), date.fromisoformat(bounds[-1])
        if end < start or (end-start).days > 3660:
            raise ValueError('Отпуск: некорректный диапазон')
        days.update(start+timedelta(days=i) for i in range((end-start).days+1))
    return days


def assignees(item):
    content = item.get('content') or {}
    connection = content.get('assignees', {})
    if connection.get('pageInfo', {}).get('hasNextPage'):
        raise ValueError('Более 100 исполнителей: расчёт остановлен')
    return [person['login'] for person in connection.get('nodes', [])]


def calculate(items):
    active = [i for i in items if not i['isArchived'] and i.get('content')]
    rows = [i for i in active if i['content']['title'].startswith('[Capacity]')]
    if not rows:
        raise ValueError('В Projects отсутствует строка [Capacity]')
    results, keys = [], set()
    for row in rows:
        result = {'item_id': row['id'], 'title': row['content']['title']}
        try:
            f = fields(row)
            owners = assignees(row)
            if len(owners) != 1:
                raise ValueError('У строки [Capacity] должен быть ровно один исполнитель')
            iteration = f.get('Итерация', {})
            if not iteration.get('iterationId'):
                raise ValueError('Не задана Итерация')
            key = (owners[0], iteration['iterationId'])
            if key in keys:
                raise ValueError('Повторная строка ёмкости для исполнителя и итерации')
            keys.add(key)
            daily = number(f.get('Часов в день', {}).get('number'), 'Часов в день')
            start = date.fromisoformat(iteration['startDate'])
            end = start+timedelta(days=iteration['duration']-1)
            available = sprint_capacity(start, end, daily, leave_dates(f.get('Отпуск', {}).get('text', '')))
            tasks, planned = [], 0
            for item in active:
                values = fields(item)
                if values.get('Уровень', {}).get('name') != 'Task':
                    continue
                if values.get('Итерация', {}).get('iterationId') != key[1]:
                    continue
                if item['content'].get('closed') or values.get('Status', {}).get('name') == 'Done':
                    continue
                assigned = assignees(item)
                if owners[0] not in assigned:
                    continue
                if len(assigned) != 1:
                    raise ValueError(f"{item['content']['title']}: нужен один исполнитель для однозначного учёта часов")
                hours = number(values.get('Осталось, ч', {}).get('number'), item['content']['title'])
                planned += hours
                tasks.append({'title': item['content']['title'], 'hours': hours,
                              'url': item['content'].get('url')})
            overload = max(0, planned-available)
            result.update(assignee=owners[0], iteration=iteration['title'], available=available,
                          planned=planned, overload=overload, tasks=tasks)
        except (ValueError, KeyError) as exc:
            result['error'] = str(exc)
        results.append(result)
    # Duplicates invalidate both rows, never leave the first one looking valid.
    for result in results:
        if 'assignee' in result and any(r.get('error', '').startswith('Повторная строка') for r in results):
            matching = [r for r in rows if assignees(r) == [result['assignee']]
                        and fields(r).get('Итерация', {}).get('title') == result['iteration']]
            if len(matching) > 1:
                result['error'] = 'Повторная строка ёмкости для исполнителя и итерации'
    return results


def synchronize(api, owner, number_, output, dry_run=False):
    project = api.project(owner, number_)
    if project['fields']['pageInfo']['hasNextPage']:
        raise ValueError('Более 100 полей: требуется расширить пагинацию полей')
    definitions = {f['name']: f for f in project['fields']['nodes']}
    for name, kind in {**INPUTS, **OUTPUTS}.items():
        if definitions.get(name, {}).get('dataType') != kind:
            raise ValueError(f'Не задано поле {name} типа {kind}')
    items = api.items(project['id'])
    results = calculate(items)
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    run_url = os.environ.get('GITHUB_SERVER_URL', 'https://github.com')+'/'+os.environ.get('GITHUB_REPOSITORY', '')+'/actions/runs/'+os.environ.get('GITHUB_RUN_ID', '')
    for result in results:
        updates = {}
        if 'error' in result:
            updates['Расчёт загрузки'] = {'text': f"ОШИБКА: {result['error']} | {now}"}
        else:
            updates = {name: {'number': result[key]} for name, key in
                       [('Доступно, ч', 'available'), ('Запланировано, ч', 'planned'), ('Перегрузка, ч', 'overload')]}
            state = 'ПЕРЕГРУЗКА' if result['overload'] else 'В пределах доступности'
            updates['Расчёт загрузки'] = {'text': f'{state} | {now} | {run_url}'}
        existing = fields(next(i for i in items if i['id'] == result['item_id']))
        if not dry_run:
            if 'error' in result:
                for name in ('Доступно, ч', 'Запланировано, ч', 'Перегрузка, ч'):
                    if name in existing:
                        api.clear_field(project['id'], result['item_id'], definitions[name]['id'])
            for name, value in updates.items():
                if any(existing.get(name, {}).get(k) != v for k, v in value.items()):
                    api.set_field(project['id'], result['item_id'], definitions[name]['id'], value)
    report = {'project': project['url'], 'calculated_at': now, 'run': run_url,
              'dry_run': dry_run, 'results': results}
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = ['## Загрузка из GitHub Projects', '', '| Исполнитель | Итерация | Доступно | План | Перегрузка |',
               '|---|---|---:|---:|---:|']
    for r in results:
        if 'error' in r:
            summary.append(f"\nОшибка: {r['title']}: {r['error']}")
        else:
            summary.append(f"| {r['assignee']} | {r['iteration']} | {r['available']} | {r['planned']} | {r['overload']} |")
    text = '\n'.join(summary)+'\n'
    print(text)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
            stream.write(text)
    if any('error' in r for r in results):
        raise ValueError('Неверные исходные данные. Устаревшие итоги очищены; см. Расчёт загрузки.')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--owner', default='IlyaKlinduhov')
    parser.add_argument('--project', type=int, default=1)
    parser.add_argument('--output', default='project-capacity.json')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    synchronize(GitHub(os.environ['PROJECTS_TOKEN']), args.owner, args.project, args.output, args.dry_run)
