import importlib.util
import pathlib
import tempfile
import unittest
import hashlib

HERE = pathlib.Path(__file__).resolve().parent

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((HERE / 'analyze.py').exists(), 'analysis implementation not created')
        spec = importlib.util.spec_from_file_location('analysis', HERE / 'analyze.py')
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_monotonic_duration_ignores_reversed_utc(self):
        self.assertEqual(self.m.elapsed({'monotonic_ns': 10, 'at': 'later'},
                                       {'monotonic_ns': 2000000010, 'at': 'earlier'}), 2)

    def test_integrity_rejects_modified_source(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'source'
            p.write_text('original')
            hashes = {'source': hashlib.sha256(p.read_bytes()).hexdigest()}
            self.assertTrue(self.m.verify(pathlib.Path(d), hashes)['ok'])
            p.write_text('changed')
            self.assertFalse(self.m.verify(pathlib.Path(d), hashes)['ok'])

    def test_redo_null_is_not_failed_detection(self):
        score = self.m.assessments([{'id':'q03','assessment':None}], {'q03'}, {'q03'})
        self.assertIsNone(score['report_wide_detection_fraction'])
        self.assertEqual(score['unassessed'], 1)

    def test_sample_detection_uses_four_report_errors(self):
        score = self.m.assessments([{'id':'q03','assessment':'contradicted'}],
                                  {'q03','q06','q09','q12'}, {'q03'})
        self.assertEqual(score['report_wide_detection_fraction'], .25)
        self.assertEqual(score['checked_error_recall'], 1)

    def test_duplicate_ids_not_complete(self):
        rows = [{'id':'q01'}, {'id':'q01'}]
        self.assertFalse(self.m.ids_complete(rows, ['q01','q02']))

if __name__ == '__main__':
    unittest.main()
