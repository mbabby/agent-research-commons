import copy
import unittest
import calculator as c

class AccountingChecks(unittest.TestCase):
    def test_fixed_arithmetic(self):
        for accounting, utilization, rate, expected in [
            ('marginal', .5, 0, [.4, 12, 6.2]),
            ('marginal', .5, 20, [20.4, 17, 16.2]),
            ('marginal', .5, 60, [60.4, 27, 36.2]),
            ('amortized', .1, 0, [20.4, 12, 16.2]),
            ('amortized', .5, 0, [4.4, 12, 8.2])]:
            got = c.compare(c.load(), accounting, utilization, .2, rate)
            self.assertTrue(got['comparable'])
            for result, total in zip(got['modes'], expected):
                self.assertAlmostEqual(result['total'], total)
                self.assertEqual(result['accepted'], 3)
                self.assertAlmostEqual(result['per_accepted'], total / 3)
    def test_zero_and_unknown(self):
        data = c.load()
        for row in data['modes'][0]['attempts']:
            row['accepted'] = False
        self.assertIsNone(c.compare(data)['modes'][0]['per_accepted'])
        data = c.load()
        data['modes'][0]['attempts'][0]['energy_kwh'] = None
        result = c.compare(data)
        self.assertIsNone(result['modes'][0]['total'])
        self.assertIsNone(result['ranking'])
    def test_quality_mismatch(self):
        data = c.load()
        data['modes'][0]['rubric'] = 'easier'
        self.assertFalse(c.compare(data)['comparable'])
        data = c.load()
        data['modes'][0]['attempts'][0]['task'] = 'other'
        self.assertFalse(c.compare(data)['comparable'])
    def test_invalid(self):
        for utilization in [0, -1, 1.1]:
            with self.assertRaises(ValueError): c.compare(c.load(), utilization=utilization)
        data = c.load()
        data['modes'][0]['attempts'][0]['api_cost'] = -1
        with self.assertRaises(ValueError): c.compare(data)
