import json
import unittest
from pathlib import Path
from experiment import simulate

ROOT = Path(__file__).parent
FIXTURES = json.loads((ROOT / 'fixtures.json').read_text())

class FrozenCases(unittest.TestCase):
    def test_frozen_expected_metrics(self):
        for case in FIXTURES['cases']:
            for policy in ('blind', 'evidence'):
                with self.subTest(case=case['id'], policy=policy):
                    result = simulate(case, policy)
                    self.assertIsInstance(result, dict, 'Simulator must produce measured metrics')
                    for key, expected in case['expected'][policy].items():
                        self.assertEqual(result['metrics'][key], expected, key)
                    self.assertEqual(result['metrics']['false_success'], 0)

if __name__ == '__main__':
    unittest.main()
