"""Core rules for an educational material catalogue and sprint planning."""
from datetime import date, timedelta


def latest_materials(materials, limit=6):
    if limit < 0:
        raise ValueError('limit must not be negative')
    return sorted(materials, key=lambda x: (x['published'], x['id']), reverse=True)[:limit]


def recently_viewed(materials, history):
    index = {item['id']: item for item in materials}
    seen, result = set(), []
    for material_id in reversed(history):
        if material_id in index and material_id not in seen:
            result.append(index[material_id])
            seen.add(material_id)
    return result


def sprint_capacity(start, end, hours_per_day=1, days_off=()):
    if end < start or hours_per_day < 0:
        raise ValueError('invalid sprint interval or daily capacity')
    excluded = set(days_off)
    return sum(hours_per_day for offset in range((end-start).days+1)
               if (day := start+timedelta(days=offset)).weekday() < 5 and day not in excluded)


def capacity_summary(tasks, available_hours):
    if available_hours < 0:
        raise ValueError('negative capacity')
    planned = sum(task['remaining_hours'] for task in tasks if task['level'] == 'Task')
    return {'available': available_hours, 'planned': planned,
            'overload': max(0, planned-available_hours)}


def unresolved_dependencies(items):
    by_id = {item['id']: item for item in items}
    problems = []
    for item in items:
        for dependency_id in item.get('depends_on', []):
            dependency = by_id.get(dependency_id)
            if dependency is None or dependency['end'] > item['start']:
                problems.append((item['id'], dependency_id))
    return problems
