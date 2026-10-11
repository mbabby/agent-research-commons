import unittest
from summarize import summarize


class SummaryTests(unittest.TestCase):
    def test_all_correct_has_undefined_noncorrect_rate(self):
        result = summarize(['C'] * 8)
        self.assertTrue(result['locally_usable'])
        self.assertEqual(result['rates']['C/N']['value'], 1)
        self.assertIsNone(result['rates']['W/(W+P+A)']['value'])

    def test_no_attempts_and_wrong_prevent_gate(self):
        result = summarize(['A'] * 8)
        self.assertIsNone(result['rates']['W/T']['value'])
        self.assertFalse(result['locally_usable'])
        self.assertFalse(summarize(['W'] + ['C'] * 7)['locally_usable'])

    def test_critical_partial_fails_even_with_seven_correct(self):
        labels = ['C'] * 8
        labels[4] = 'P'
        self.assertFalse(summarize(labels)['locally_usable'])
        labels[4], labels[7] = 'C', 'P'
        self.assertTrue(summarize(labels)['locally_usable'])

    def test_invalid_or_incomplete_labels_rejected(self):
        for labels in ([], ['C'] * 7, ['C'] * 7 + ['unknown']):
            with self.assertRaises(ValueError):
                summarize(labels)


if __name__ == '__main__':
    unittest.main()
