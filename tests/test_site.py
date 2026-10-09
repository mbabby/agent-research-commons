import json
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser
from arc.site import build

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.local = []
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value and not value.startswith(('http:', 'https:', '#', 'mailto:', 'data:')):
                self.local.append(value.split('#')[0].split('?')[0])

class SiteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'site'
        self.snapshot = {'generated_at': '2026-10-09T04:00:00Z', 'repository': 'mbabby/agent-research-commons', 'tasks': []}
    def test_empty_site_has_working_relative_links_and_machine_entry(self):
        build(self.snapshot, [], self.out)
        for page in self.out.rglob('*.html'):
            parser = Links(); parser.feed(page.read_text())
            for link in parser.local:
                self.assertTrue((page.parent / link).exists(), (page, link))
                self.assertFalse(link.startswith('/'))
        data = json.loads((self.out / 'agent.json').read_text())
        self.assertEqual(data['resources']['tasks'], 'data/tasks.json')
        self.assertIn('暂无', (self.out / 'tasks/index.html').read_text())
        self.assertTrue((self.out / 'guide.md').exists())
    def test_agents_can_discover_inactive_rules_and_matching_download(self):
        # Catches missing discovery, broken export links and accidental activation.
        build(self.snapshot, [], self.out)
        entry = json.loads((self.out / 'agent.json').read_text())
        self.assertIn('rules', entry['resources'])
        index_path = self.out / entry['resources']['rules']
        index = json.loads(index_path.read_text())
        self.assertEqual(index['status'], 'draft')
        self.assertIsNone(index['effective_at'])
        document = index['versions'][0]
        html_text = (index_path.parent / document['html']).read_text()
        markdown = (index_path.parent / document['markdown']).read_text()
        for section in document['sections']:
            for paragraph in section['paragraphs']:
                from html import escape
                self.assertIn(escape(paragraph, quote=True), html_text)
                self.assertIn(paragraph, markdown)
        self.assertIn('repository owner', entry['write_access'])
        self.assertTrue((self.out / 'guide.md').is_file())

    def test_active_rules_cannot_replace_previous_site(self):
        from arc.site import ROOT
        build(self.snapshot, [], self.out)
        before = (self.out / 'rules/index.json').read_text()
        document = json.loads((ROOT / 'docs/governance.json').read_text())
        candidate = Path(self.tmp.name) / 'candidate.json'
        for update in ({'status': 'active'}, {'effective_at': '2026-10-09'}):
            with self.subTest(update=update):
                candidate.write_text(json.dumps({**document, **update}))
                with self.assertRaises(ValueError):
                    build(self.snapshot, [], self.out, governance_path=candidate)
                self.assertEqual((self.out / 'rules/index.json').read_text(), before)

    def test_philosophy_is_discoverable_and_exports_preserve_principles(self):
        build(self.snapshot, [], self.out)
        entry = json.loads((self.out / 'agent.json').read_text())
        self.assertIn('philosophy', entry['resources'])
        index_path = self.out / entry['resources']['philosophy']
        document = json.loads(index_path.read_text())
        page = (index_path.parent / document['html']).read_text()
        markdown = (index_path.parent / document['markdown']).read_text()
        from html import escape
        for section in document['sections']:
            for paragraph in section['paragraphs']:
                self.assertIn(escape(paragraph, quote=True), page)
                self.assertIn(paragraph, markdown)
        self.assertIn('repository owner', entry['write_access'])
        rules = json.loads((self.out / entry['resources']['rules']).read_text())
        self.assertEqual(rules['status'], 'draft')
        self.assertIsNone(rules['effective_at'])

    def test_invalid_snapshot_leaves_previous_site_intact(self):
        build(self.snapshot, [], self.out)
        before = (self.out / 'index.html').read_text()
        with self.assertRaises(ValueError):
            build({**self.snapshot, 'tasks': [{'number': 1, 'status': 'invented'}]}, [], self.out)
        self.assertEqual((self.out / 'index.html').read_text(), before)
    def test_snapshot_repository_cannot_inject_html_or_urls(self):
        with self.assertRaises(ValueError):
            build({**self.snapshot, 'repository': 'evil/../<script>'}, [], self.out)
    def test_missing_generation_time_fails_instead_of_looking_current(self):
        snapshot = dict(self.snapshot); del snapshot['generated_at']
        with self.assertRaises(ValueError):
            build(snapshot, [], self.out)

    def test_report_links_resolve_and_task_prose_is_escaped(self):
        from test_model import ReportTests
        task, report = ReportTests().fixture()
        task['title'] = '<script>alert(1)</script>'
        task['exclusions'] = ['Private data']
        snapshot = {**self.snapshot, 'repository': 'o/r', 'tasks': [task]}
        build(snapshot, [report], self.out)
        detail = (self.out / 'tasks/1.html').read_text()
        self.assertNotIn('<script>alert(1)</script>', detail)
        self.assertIn('&lt;script&gt;', detail)
        self.assertNotIn("[&#x27;Private data&#x27;]", detail)
        for page in self.out.rglob('*.html'):
            parser = Links(); parser.feed(page.read_text())
            for link in parser.local:
                self.assertTrue((page.parent / link).exists(), (page, link))
        self.assertIn('## 来源', (self.out / 'reports/example.md').read_text())

    def test_unaccepted_report_cannot_replace_published_site(self):
        from test_model import ReportTests, task
        _, report = ReportTests().fixture()
        build(self.snapshot, [], self.out)
        before = (self.out / 'index.html').read_text()
        with self.assertRaises(ValueError):
            build({**self.snapshot, 'tasks': [task()]}, [report], self.out)
        self.assertEqual((self.out / 'index.html').read_text(), before)

    def test_reserved_report_slug_cannot_overwrite_library(self):
        from test_model import ReportTests
        task, report = ReportTests().fixture()
        report['slug'] = 'index'
        with self.assertRaises(ValueError):
            build({**self.snapshot, 'repository': 'o/r', 'tasks': [task]}, [report], self.out)

    def test_public_skill_document_links_resolve_inside_site(self):
        import re
        build(self.snapshot, [], self.out)
        for target in re.findall(r'\]\(([^)]+)\)', (self.out / 'skill.md').read_text()):
            if not target.startswith(('http:', 'https:')):
                self.assertTrue((self.out / target).is_file(), target)

if __name__ == '__main__':
    unittest.main()
