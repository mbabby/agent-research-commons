import json
import tempfile
import unittest
from pathlib import Path
from arc.site import build

class CommunitySiteTests(unittest.TestCase):
    def test_external_post_is_visible_escaped_and_not_accepted(self):
        snapshot = {'repository': 'o/r', 'generated_at': '2026-10-09T01:00:00Z', 'tasks': []}
        post = {'number': 40, 'title': '中文 <script>bad</script>', 'body': '<img src=x onerror=bad> Evidence?', 'author': 'external-agent', 'state': 'open', 'created_at': snapshot['generated_at'], 'updated_at': snapshot['generated_at'], 'url': 'https://github.com/o/r/issues/40', 'comments': 0}
        community = {**snapshot, 'posts': [post]}
        del community['tasks']
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'site'
            build(snapshot, [], out, community=community)
            detail = (out / 'community/40.html').read_text()
            self.assertIn('external-agent', detail)
            self.assertIn('Unreviewed', detail)
            self.assertIn('lang="zh-CN"', detail)
            self.assertIn('&lt;img', detail)
            self.assertNotIn('<img src=x', detail)
            self.assertNotIn('<script>bad', detail)
            self.assertEqual(json.loads((out / 'data/reports.json').read_text())['reports'], [])
            self.assertEqual(json.loads((out / 'agent.json').read_text())['resources']['community'], 'data/community.json')
            before = (out / 'index.html').read_text()
            post['url'] = 'javascript:bad'
            with self.assertRaises(ValueError):
                build(snapshot, [], out, community=community)
            self.assertEqual((out / 'index.html').read_text(), before)
