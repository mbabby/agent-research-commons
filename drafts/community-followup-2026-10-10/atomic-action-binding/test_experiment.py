"""Behavior tests for the hypothetical server model, not a deployed API."""
import json
from pathlib import Path
import unittest

try:
    import experiment
except ModuleNotFoundError:
    experiment = None

FIXTURES = json.loads(Path(__file__).with_name('fixtures.json').read_text())


class AtomicBindingTests(unittest.TestCase):
    def run_case(self, case, policy):
        self.assertIsNotNone(experiment, 'experiment implementation is not present yet')
        fixture = next(f for f in FIXTURES['cases'] if f['id'] == case)
        return experiment.run_case(FIXTURES, fixture, policy)

    def test_atomic_binding_stops_target_race_bypass_exposes_wrong_effect(self):
        atomic = self.run_case('between_target', 'atomic_scoped')
        self.assertEqual(atomic['metrics']['conflicts'], 1)
        self.assertEqual(atomic['metrics']['changed_state_effects'], 0)
        bypass = self.run_case('between_target', 'bypass_compare')
        self.assertEqual(bypass['metrics']['wrong_effects'], 1)
        self.assertEqual(bypass['final_documents']['A/W1/D18'], 'archived')

    def test_version_only_change_is_not_laundered_as_correct_action(self):
        atomic = self.run_case('between_version', 'atomic_scoped')
        self.assertEqual(atomic['metrics']['conflicts'], 1)
        baseline = self.run_case('between_version', 'precheck_only')
        self.assertEqual(baseline['metrics']['stale_version_effects'], 1)
        self.assertEqual(baseline['metrics']['wrong_effects'], 1)
        self.assertTrue(baseline['metrics']['desired_state_achieved'])
        self.assertFalse(baseline['metrics']['known_correct_completion'])

    def test_global_version_overrejects_unrelated_change(self):
        scoped = self.run_case('between_unrelated', 'atomic_scoped')
        global_bound = self.run_case('between_unrelated', 'atomic_global')
        self.assertTrue(scoped['metrics']['known_correct_completion'])
        self.assertEqual(global_bound['metrics']['unnecessary_rejections'], 1)
        self.assertEqual(global_bound['metrics']['conflicts'], 1)

    def test_revocation_before_commit_denies_even_baseline(self):
        for policy in ('precheck_only', 'atomic_scoped', 'bypass_compare'):
            result = self.run_case('between_revocation', policy)
            self.assertEqual(result['metrics']['authorization_rejections'], 1)
            self.assertEqual(result['metrics']['changed_state_effects'], 0)

    def test_postcommit_change_does_not_retroactively_revoke_action(self):
        result = self.run_case('after_commit_change', 'atomic_scoped')
        self.assertTrue(result['metrics']['known_correct_completion'])
        self.assertEqual(result['metrics']['wrong_effects'], 0)
        self.assertFalse(result['final_world']['permission'])
        self.assertEqual(result['final_documents']['A/W1/D17'], 'archived')

    def test_response_loss_is_unknown_after_one_valid_effect(self):
        result = self.run_case('lost_response_after_commit', 'atomic_scoped')
        self.assertEqual(result['metrics']['unknown_outcomes'], 1)
        self.assertEqual(result['metrics']['changed_state_effects'], 1)
        self.assertTrue(result['metrics']['desired_state_achieved'])
        self.assertFalse(result['metrics']['known_correct_completion'])
        self.assertEqual(result['metrics']['submissions'], 1)

    def test_all_reject_control_exposes_incomplete_normal_case(self):
        normal = self.run_case('unchanged', 'atomic_scoped')
        reject = self.run_case('unchanged', 'all_reject')
        self.assertTrue(normal['metrics']['known_correct_completion'])
        self.assertEqual(reject['metrics']['unnecessary_rejections'], 1)
        self.assertEqual(reject['metrics']['wrong_effects'], 0)
        self.assertFalse(reject['metrics']['desired_state_achieved'])

    def test_each_binding_field_matters_without_relying_on_version_difference(self):
        self.assertIsNotNone(experiment, 'experiment implementation is not present yet')
        for field, value in (('origin', 'https://other.invalid'), ('account', 'B'),
                             ('workspace', 'W2'), ('target', 'D18'), ('effect', 'delete')):
            world = experiment.World(FIXTURES['base'], {'events': []}, 'atomic_scoped')
            observed = world.call('observe')
            expected = dict(observed)
            expected[field] = value
            response = world.call('submit', expected)
            self.assertEqual(response['status'], 'conflict', field)
            self.assertFalse(world.ledger, field)


if __name__ == '__main__':
    unittest.main()
