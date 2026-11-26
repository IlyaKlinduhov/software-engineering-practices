import copy
from datetime import date
import json
from pathlib import Path
import tempfile
import unittest

from project_capacity import calculate, leave_dates, synchronize


def item(id_, title, level=None, hours=None, owners=('alice',), iteration='s2', **extra):
    values = {'Итерация': {'iterationId': iteration, 'title': 'Sprint 2',
                         'startDate': '2026-11-16', 'duration': 17}}
    if level:
        values['Уровень'] = {'name': level}
    if hours is not None:
        values['Осталось, ч'] = {'number': hours}
    values.update(extra)
    return {'id': id_, 'isArchived': False,
            'content': {'title': title, 'closed': False, 'assignees': {
                'nodes': [{'login': x} for x in owners], 'pageInfo': {'hasNextPage': False}}},
            'fieldValues': {'nodes': [dict(v, field={'name': k}) for k, v in values.items()]}}


def fixture():
    return [item('capacity', '[Capacity] alice', **{'Часов в день': {'number': 1},
                'Отпуск': {'text': '2026-11-23..2026-11-27'}}),
            item('task4', 'Page', 'Task', 8), item('task5', 'Query', 'Task', 3)]


class CapacityTests(unittest.TestCase):
    def test_real_example_and_changed_estimate(self):
        data = fixture()
        r = calculate(data)[0]
        self.assertEqual((r['available'], r['planned'], r['overload']), (8, 11, 3))
        data[1] = item('task4', 'Page', 'Task', 5)
        r = calculate(data)[0]
        self.assertEqual((r['planned'], r['overload']), (8, 0))

    def test_availability_and_dates_are_inputs(self):
        data = fixture()
        data[0] = item('capacity', '[Capacity] alice', **{'Часов в день': {'number': 2}})
        self.assertEqual(calculate(data)[0]['available'], 26)
        data[0]['fieldValues']['nodes'][0]['duration'] = 5
        self.assertEqual(calculate(data)[0]['available'], 10)

    def test_only_open_tasks_for_same_assignee_and_iteration(self):
        data = fixture()+[item('pbi', 'Parent', 'PBI', 999),
                          item('other', 'Other sprint', 'Task', 999, iteration='s3'),
                          item('bob', 'Bob', 'Task', 999, owners=('bob',))]
        archived = item('archive', 'Archived', 'Task', 999)
        archived['isArchived'] = True
        closed = item('closed', 'Closed', 'Task', 999)
        closed['content']['closed'] = True
        done = item('done', 'Done', 'Task', 999, Status={'name': 'Done'})
        self.assertEqual(calculate(data+[archived, closed, done])[0]['planned'], 11)

    def test_zero_is_valid_but_missing_negative_and_ambiguous_are_errors(self):
        for bad in (None, -1, float('inf')):
            data = fixture()
            data[1] = item('task4', 'Page', 'Task', bad)
            self.assertIn('error', calculate(data)[0])
        data = fixture()
        data[1] = item('task4', 'Page', 'Task', 0)
        self.assertEqual(calculate(data)[0]['planned'], 3)
        data[1] = item('task4', 'Page', 'Task', 8, owners=('alice', 'bob'))
        self.assertIn('error', calculate(data)[0])

    def test_leave_ranges_overlap_weekend_and_invalid_ranges(self):
        self.assertEqual(len(leave_dates('2026-11-23..2026-11-27,2026-11-25')), 5)
        data = fixture()
        data[0] = item('capacity', '[Capacity] alice', **{'Часов в день': {'number': 1},
                     'Отпуск': {'text': '2026-11-21..2026-11-22'}})
        self.assertEqual(calculate(data)[0]['available'], 13)
        with self.assertRaises(ValueError):
            leave_dates('2026-11-27..2026-11-23')

    def test_duplicate_capacity_rows_are_both_invalid(self):
        data = fixture()
        duplicate = copy.deepcopy(data[0])
        duplicate['id'] = 'duplicate'
        data.append(duplicate)
        self.assertTrue(all('error' in r for r in calculate(data)))

    def test_invalid_input_clears_old_results_instead_of_leaving_stale_numbers(self):
        class FakeAPI:
            def __init__(self):
                self.updated, self.cleared = [], []
            def project(self, *args):
                from project_capacity import INPUTS, OUTPUTS
                return {'id': 'p', 'url': 'https://github.com/example', 'fields': {
                    'pageInfo': {'hasNextPage': False},
                    'nodes': [{'id': k, 'name': k, 'dataType': v} for k, v in {**INPUTS, **OUTPUTS}.items()]}}
            def items(self, *args):
                data = fixture()
                data[1] = item('task4', 'Page', 'Task')
                data[0]['fieldValues']['nodes'].append({'field': {'name': 'Перегрузка, ч'}, 'number': 0})
                return data
            def set_field(self, *args):
                self.updated.append(args)
            def clear_field(self, *args):
                self.cleared.append(args)
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'result.json'
            with self.assertRaises(ValueError):
                synchronize(api, 'alice', 1, output)
            self.assertIn('error', json.loads(output.read_text(encoding='utf-8'))['results'][0])
        self.assertEqual(api.cleared, [('p', 'capacity', 'Перегрузка, ч')])
        self.assertIn('ОШИБКА', api.updated[0][-1]['text'])


if __name__ == '__main__':
    unittest.main()
