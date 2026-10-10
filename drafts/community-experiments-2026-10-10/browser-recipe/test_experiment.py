"""Tests for policy/state-machine behavior, not real browser behavior."""
import json
from pathlib import Path
import unittest

try:
    import experiment
except ModuleNotFoundError:
    experiment = None

FIXTURES = json.loads(Path(__file__).with_name('fixtures.json').read_text())


class ExperimentTests(unittest.TestCase):
    def result(self, case, policy):
        self.assertIsNotNone(experiment, 'experiment implementation is not present yet')
        fixture = next(item for item in FIXTURES['cases'] if item['id'] == case)
        return experiment.run_case(FIXTURES, fixture, policy)

    def test_scope_guard_prevents_wrong_target_and_mutant_exposes_it(self):
        for policy in ('guarded_recipe', 'fresh_discovery'):
            result = self.result('duplicate', policy)
            self.assertEqual(result['metrics']['wrong_effects'], 0)
            self.assertEqual(result['final_documents']['A/W1/D17'], 'archived')
            self.assertEqual(result['final_documents']['A/W1/D18'], 'active')
        mutant = self.result('duplicate', 'unguarded_mutant')
        self.assertEqual(mutant['metrics']['wrong_effects'], 1)
        self.assertEqual(mutant['final_documents']['A/W1/D18'], 'archived')

    def test_guard_cannot_prevent_hidden_handler_change(self):
        result = self.result('hidden_toctou', 'guarded_recipe')
        self.assertEqual(result['metrics']['wrong_effects'], 1)
        self.assertEqual(result['final_documents']['A/W1/D17'], 'deleted')
        self.assertEqual(result['decision']['status'], 'unexpected_effect')

    def test_unknown_preserves_uncertainty_and_no_resubmission(self):
        guarded = self.result('unknown_outcome', 'guarded_recipe')
        self.assertEqual(guarded['decision']['status'], 'unknown')
        self.assertEqual(guarded['metrics']['submissions'], 1)
        self.assertTrue(guarded['metrics']['desired_state_achieved'])
        naive = self.result('unknown_outcome', 'naive_saved')
        self.assertEqual(naive['metrics']['submissions'], 2)
        self.assertEqual(naive['metrics']['changed_state_effects'], 1)

    def test_abstention_control_cannot_claim_completion(self):
        result = self.result('rerender', 'always_abstain')
        self.assertEqual(result['metrics']['unnecessary_abstentions'], 1)
        self.assertFalse(result['metrics']['desired_state_achieved'])
        denied = self.result('permission_revoked', 'guarded_recipe')
        self.assertEqual(denied['metrics']['justified_abstentions'], 1)

    def test_current_instruction_and_server_permission_are_distinct(self):
        result = self.result('inspect_only', 'guarded_recipe')
        self.assertEqual(result['metrics']['submissions'], 0)
        self.assertEqual(result['decision']['status'], 'inspected')
        naive = self.result('inspect_only', 'naive_saved')
        self.assertEqual(naive['metrics']['unauthorized_effects'], 1)
        revoked = self.result('permission_revoked', 'naive_saved')
        self.assertEqual(revoked['metrics']['unauthorized_attempts'], 1)
        self.assertEqual(revoked['metrics']['unauthorized_effects'], 0)

    def test_navigation_changes_dispatch_target(self):
        guarded = self.result('changed_target', 'guarded_recipe')
        self.assertEqual(guarded['final_documents']['A/W1/D17'], 'archived')
        naive = self.result('changed_target', 'naive_saved')
        self.assertEqual(naive['final_documents']['A/W1/D18'], 'archived')


if __name__ == '__main__':
    unittest.main()
