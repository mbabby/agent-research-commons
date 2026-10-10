import json
from pathlib import Path
import unittest
import experiment

FIXTURES = json.loads(Path(__file__).with_name('fixtures.json').read_text())

class OnlineTests(unittest.TestCase):
    def test_frozen_metrics(self):
        for case in FIXTURES['cases']:
            for policy in ('one_shot','online'):
                with self.subTest(case=case['id'],policy=policy):
                    result=experiment.run(case,policy,FIXTURES['deadline'])
                    self.assertIsInstance(result,dict,'Online interpreter is not implemented')
                    self.assertEqual(result['metrics'],case['expected'][policy])

    def case(self, name):
        return next(c for c in FIXTURES['cases'] if c['id'] == name)

    def test_delayed_receipt_not_visible_early(self):
        provider = experiment.Provider(self.case('receipt_at_2'))
        provider.advance(0)
        self.assertEqual(provider.read()['status'], 'unknown')
        with self.assertRaises(ValueError):
            provider.advance(2)
        provider.advance(1)
        self.assertEqual(provider.read()['status'], 'unknown')
        provider.advance(2)
        self.assertEqual(provider.read()['status'], 'succeeded')

    def test_future_delay_cannot_change_initial_decision(self):
        early = experiment.run(self.case('receipt_at_2'), 'online', 4)
        late = experiment.run(self.case('receipt_after_deadline'), 'online', 4)
        self.assertEqual(early['decisions'][0], late['decisions'][0])
        self.assertEqual(late['last_tick'], 4)
        self.assertEqual(late['metrics']['unresolved'], 1)
        self.assertTrue(all(item['tick'] <= 4 for item in late['provider_trace']))

    def test_authorization_transitions_stop_dependent_actions(self):
        read = experiment.run(self.case('read_withdrawn'), 'online', 4)
        self.assertEqual(read['last_tick'], 1)
        self.assertEqual([e['tick'] for e in read['provider_trace'] if e['event'] == 'read'], [0])
        write = experiment.run(self.case('mutation_withdrawn'), 'online', 4)
        self.assertEqual(write['metrics']['reads'], 5)
        self.assertEqual(write['metrics']['retry_submissions'], 0)

    def test_expiry_boundary_and_receipt_scope(self):
        context = {'tick': 3, 'mutation_authorized': True, 'read_authorized': True,
                   'deduplication_contract': True, 'key_expires_at': 3}
        self.assertEqual(experiment.decide(context, {'status': 'unknown'}, False, 'online'), 'wait')
        context['tick'] = 2
        self.assertEqual(experiment.decide(context, {'status': 'unknown'}, False, 'online'), 'retry')
        bad = dict(experiment.SCOPE, account='wrong', status='succeeded')
        self.assertNotEqual(experiment.decide(context, bad, False, 'online'), 'resolve')

    def test_negative_controls_are_detected(self):
        controls = experiment.negative_controls(FIXTURES)
        self.assertEqual({c['detected_violation'] for c in controls},
                         {'duplicates', 'unauthorized_effects', 'unauthorized_read_attempts'})

if __name__=='__main__':
    unittest.main()
