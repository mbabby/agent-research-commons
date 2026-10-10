import copy
import json
import unittest
import experiment as e


class ExperimentTests(unittest.TestCase):
    def test_saved_results_match_fresh_execution_before_regeneration(self):
        saved = json.loads((e.ROOT / "results.json").read_text())
        self.assertEqual(saved["results"], [e.run(case) for case in e.CASES])

    def test_matrix_observations_match_declared_expectations(self):
        for case in e.CASES:
            with self.subTest(case=case['id']):
                result = e.run(case)
                self.assertEqual(result['observed'], case['expected'])

    def test_unguarded_unit_mix_changes_actual_ledger(self):
        case = next(c for c in e.CASES if c['id'] == 'unsafe-tool-mix')
        result = e.run(case)
        self.assertEqual(result['ledger_after']['charged_cents'], 125000)
        self.assertEqual(result['trace'][-1]['implementation'], 't2')

    def test_rejected_resume_preserves_existing_effect(self):
        case = next(c for c in e.CASES if c['id'] == 'new-on-old-checkpoint')
        result = e.run(case)
        self.assertEqual(result['ledger_after'], result['ledger_before'])
        self.assertEqual(result['ledger_after']['reserved_items'], 1)
        self.assertFalse(any(t['stage'] == 'tool' for t in result['trace']))

    def test_migration_converts_units_without_mutating_source(self):
        source = copy.deepcopy(e.CHECKPOINTS['old'])
        migrated = e.migrate(source)
        self.assertEqual(migrated['amount'], '12.50')
        self.assertEqual(source, e.CHECKPOINTS['old'])

    def test_trace_records_executed_versions_not_just_requested_bundle(self):
        case = next(c for c in e.CASES if c['id'] == 'compatible-tool')
        trace = e.run(case)['trace']
        self.assertEqual([t['stage'] for t in trace], ['checkpoint', 'prompt', 'schema', 'tool'])
        self.assertEqual(trace[-1]['implementation'], 't1b')

    def test_compensation_is_separate_from_deployment_selection(self):
        ledger = {'reserved_items': 1, 'charged_cents': 1250}
        before = copy.deepcopy(ledger)
        e.select_deployment('old')
        self.assertEqual(ledger, before)
        e.compensate(ledger)
        self.assertEqual(ledger, {'reserved_items': 0, 'charged_cents': 0})
