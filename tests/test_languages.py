import copy
import json
import tempfile
import unittest
from pathlib import Path
from arc.site import build

class LanguageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.out = self.root / 'site'
        from test_model import ReportTests
        self.task, self.report = ReportTests().fixture()
        self.task.update(title='中文研究 <script>bad</script>', question='如何核查证据？')
        self.snapshot = {'generated_at':'2026-10-09T04:00:00Z','repository':'o/r','tasks':[self.task]}

    def test_english_interface_accepts_untranslated_chinese(self):
        build(self.snapshot, [self.report], self.out)
        page = (self.out/'tasks/1.html').read_text()
        self.assertIn('<html lang="en">', page)
        self.assertIn('Research tasks', page)
        self.assertIn('Chinese', page)
        self.assertIn('lang="zh-CN"', page)
        self.assertIn('如何核查证据？', page)
        self.assertNotIn('<script>bad</script>', page)
        self.assertEqual(json.loads((self.out/'data/tasks.original.json').read_text())['tasks'][0], self.task)

    def test_translation_has_readable_original_and_stale_translation_falls_back(self):
        keys = ('title','question','scope','exclusions','deliverable','acceptance')
        source = {k:self.task[k] for k in keys}
        translated = {**source, 'title':'Chinese research', 'question':'How can evidence be checked?'}
        path = self.root/'translations/tasks/1.json'; path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'source':source,'translation':translated}))
        build(self.snapshot,[self.report],self.out,translations_path=self.root/'translations')
        page = (self.out/'tasks/1.html').read_text()
        self.assertIn('Chinese research',page)
        self.assertIn('English translation',page)
        self.assertIn('1.original.html',page)
        original = (self.out/'tasks/1.original.html').read_text()
        self.assertIn('如何核查证据？',original)
        self.assertNotIn('<script>bad</script>',original)
        self.task['question'] = '更新后的问题'
        build(self.snapshot,[self.report],self.out,translations_path=self.root/'translations')
        page = (self.out/'tasks/1.html').read_text()
        self.assertIn('更新后的问题',page)
        self.assertNotIn('How can evidence be checked?',page)
        self.assertNotIn('<strong>English translation',page)

    def test_translation_cannot_rewrite_evidence_or_acceptance(self):
        translated = copy.deepcopy(self.report)
        translated['acceptance_url'] = 'https://github.com/o/r/pull/999'
        path = self.root/'translations/reports/example.json'; path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'source':self.report,'translation':translated}))
        with self.assertRaises(ValueError):
            build(self.snapshot,[self.report],self.out,translations_path=self.root/'translations')

    def test_protocol_translation_falls_back_when_source_changes(self):
        from arc import languages
        import hashlib
        source = self.root/'protocol.md'; source.write_text('原始协议')
        english = self.root/'protocol.en.md'; english.write_text('English protocol')
        metadata = self.root/'protocol-source.json'
        metadata.write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}))
        text, translated = languages.guide_translation(source, english, metadata)
        self.assertTrue(translated)
        self.assertIn('English protocol', text)
        self.assertIn('English translation', text)
        self.assertIn('guide.original.md', text)
        source.write_text('修改后的协议')
        text, translated = languages.guide_translation(source, english, metadata)
        self.assertFalse(translated)
        self.assertIn('修改后的协议', text)
        self.assertNotIn('English protocol', text)

    def test_original_document_exports_link_to_original_formats(self):
        build(self.snapshot, [self.report], self.out)
        for directory, stem in (('rules','rules'),('philosophy','philosophy')):
            index = json.loads((self.out/directory/'index.original.json').read_text())
            record = index['versions'][0] if directory == 'rules' else index
            self.assertEqual(record['html'], 'index.original.html')
            self.assertEqual(record['markdown'], stem + '.original.md')
            page = (self.out/directory/record['html']).read_text()
            self.assertIn('lang="zh-CN"', page)

if __name__ == '__main__':
    unittest.main()
