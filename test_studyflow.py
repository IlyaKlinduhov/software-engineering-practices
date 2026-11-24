import json
import unittest
from datetime import date, timedelta
from pathlib import Path
from studyflow import latest_materials, recently_viewed, sprint_capacity, capacity_summary, unresolved_dependencies

ROOT = Path(__file__).parent


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.materials = json.loads((ROOT/'materials.json').read_text(encoding='utf-8'))

    def test_newest_material_first_and_limit(self):
        result = latest_materials(list(reversed(self.materials)), 2)
        self.assertEqual([x['id'] for x in result], [6, 5])

    def test_recent_history_deduplicates_and_ignores_deleted(self):
        result = recently_viewed(self.materials, [1, 3, 1, 999])
        self.assertEqual([x['id'] for x in result], [1, 3])

    def test_empty_catalogue_and_zero_limit(self):
        self.assertEqual(latest_materials([], 5), [])
        self.assertEqual(latest_materials(self.materials, 0), [])


class PlanningTests(unittest.TestCase):
    def test_capacity_excludes_weekends_and_five_day_vacation(self):
        start, end = date(2026, 11, 16), date(2026, 12, 2)
        vacation = [date(2026, 11, 23)+timedelta(days=i) for i in range(5)]
        self.assertEqual(sprint_capacity(start, end, 1, vacation), 8)

    def test_overload_counts_tasks_only(self):
        items = json.loads((ROOT/'backlog.json').read_text(encoding='utf-8'))
        self.assertEqual(capacity_summary(items, 8), {'available': 8, 'planned': 11, 'overload': 3})

    def test_invalid_capacity_rejected(self):
        with self.assertRaises(ValueError):
            sprint_capacity(date(2026, 12, 2), date(2026, 11, 16))

    def test_dependency_conflict_detected_and_resolved(self):
        original = [{'id': 8, 'start': '2026-12-14', 'end': '2027-01-01'},
                    {'id': 10, 'start': '2026-11-24', 'end': '2026-12-04', 'depends_on': [8]}]
        self.assertEqual(unresolved_dependencies(original), [(10, 8)])
        corrected = json.loads((ROOT/'backlog.json').read_text(encoding='utf-8'))[7:]
        self.assertEqual(unresolved_dependencies(corrected), [])


if __name__ == '__main__':
    unittest.main()
