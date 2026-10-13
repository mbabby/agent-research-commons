"""Focused denominator/schema tests for the standalone pilot analysis."""
import unittest
from analyze import score, source_reads

class DetectionScoreTests(unittest.TestCase):
    def setUp(self):
        self.labels = {f'C{i:02}': i in (3, 6, 10, 12) for i in range(1, 13)}

    def test_sample_keeps_full_error_denominator(self):
        s = score([{'id': f'C{i:02}', 'answer': 'contradicted' if i in (3,10) else 'supported'} for i in (2,3,8,10)], self.labels)
        self.assertEqual((s['tp'], s['fn_report_wide'], s['unchecked']), (2,2,8))
        self.assertEqual(s['recall_report_wide'], .5)
        self.assertEqual(s['recall_checked_only'], 1)
        self.assertEqual(s['correct_denominator_checked_only'], 2)

    def test_false_positive_unresolved_and_wrong_validation(self):
        s = score([{'id':'C01','verdict':'contradicted'}, {'id':'C03','verdict':'supported'}, {'id':'C06','verdict':'unresolved'}], self.labels)
        self.assertEqual((s['fp'], s['fn_report_wide'], s['unresolved_checked'], s['wrong_validations']), (1,4,1,1))
        self.assertEqual(s['false_positive_rate_report_wide'], 1/8)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            score([{'id':'C01','answer':'supported'}]*2, self.labels)

    def test_report_only_raw_file_bytes_schema(self):
        m = {'command_read_event_ledger': [{'reads': [
            {'path': '/arm/corpus/docs/community.md', 'raw_file_bytes': 4634},
            {'path': '/arm/corpus/docs/agent-value.md', 'raw_file_bytes': 4394}]}]}
        got = source_reads(m)
        self.assertEqual((got['source_file_read_events'], got['distinct_source_file_bytes'], got['repeated_source_file_read_bytes']), (2, 9028, 0))

    def test_full_all_detected(self):
        s = score([{'id':cid,'verdict':'contradicted' if error else 'supported'} for cid,error in self.labels.items()], self.labels)
        self.assertEqual((s['tp'],s['fn_report_wide'],s['fp'],s['unchecked']), (4,0,0,0))

if __name__ == '__main__':
    unittest.main()
