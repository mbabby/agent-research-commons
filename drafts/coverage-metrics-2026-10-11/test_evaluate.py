import json
from pathlib import Path
import unittest
from evaluate import evaluate, grade, metrics

class Checks(unittest.TestCase):
    def test_fixed_pair(self):
        rows = json.loads(Path(__file__).with_name('ledger.json').read_text())
        self.assertEqual(len(rows), 10)
        r = evaluate(rows)['agents']
        self.assertEqual(r['A']['counts'], dict(correct=2, wrong=1, partial=1, abstain=6))
        self.assertEqual(r['B']['counts'], dict(correct=6, wrong=2, partial=2, abstain=0))
        self.assertLess(r['A']['per_assigned_wrong']['value'], r['B']['per_assigned_wrong']['value'])
        self.assertGreater(r['A']['attempted_wrong']['value'], r['B']['attempted_wrong']['value'])
        self.assertEqual(r['A']['aa_denominator_illustration']['value'], 1/8)
        self.assertEqual(r['B']['aa_denominator_illustration']['value'], 1/2)
    def test_empty(self):
        self.assertTrue(all(v['value'] == 'N/A' for k,v in metrics([]).items() if k != 'counts'))
    def test_abstain(self):
        m = metrics(['abstain']*10)
        self.assertEqual(m['attempted_wrong']['value'], 'N/A')
        self.assertEqual(m['full_correct_completion']['value'], 0)
        self.assertEqual(m['aa_denominator_illustration']['value'], 0)
    def test_correct(self):
        m = metrics(['correct']*10)
        self.assertEqual(m['aa_denominator_illustration']['value'], 'N/A')
        self.assertEqual(m['full_correct_completion']['value'], 1)
    def test_partial(self):
        m = metrics(['partial']*10)
        self.assertEqual(m['attempted_wrong']['value'], 0)
        self.assertEqual(m['partial_as_failure_attempted']['value'], 1)
        self.assertEqual(m['partial_excluded_attempted_wrong']['value'], 'N/A')
    def test_mixed_wrong_priority(self):
        self.assertEqual(grade([3,2], [3,9]), 'wrong')
        self.assertEqual(grade([3,2], [4,None]), 'wrong')
        self.assertEqual(grade([3,2], [3,None]), 'partial')
    def test_invalid(self):
        for answer in ([True,2], [3], ['3',2]):
            with self.assertRaises(ValueError): grade([3,2], answer)
        with self.assertRaises(ValueError): metrics(['unknown'])
        row = dict(id='x', a=1,b=2,agents={'A':[3,2], 'B':[3,2]})
        with self.assertRaises(ValueError): evaluate([row,row])
        with self.assertRaises(ValueError): evaluate([dict(row, agents={'A':[3,2]})])

if __name__ == '__main__': unittest.main()
