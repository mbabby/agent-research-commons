import json
import tempfile
import unittest
from pathlib import Path
from arc.site import build

STAMP = '2026-10-10T00:00:00Z'
SHA = 'a' * 40
URL = 'https://github.com/other/research/tree/' + SHA

def post(n, record, state='open'):
    return dict(number=n, title='Question 中文', body='<!-- arc-record:v1 -->\n```json\n' + json.dumps(record) + '\n```\nUntrusted <script> content 中文', author='contributor', state=state, created_at=STAMP, updated_at=STAMP, url='https://github.com/o/r/issues/' + str(n), comments=2)

class OpportunityTests(unittest.TestCase):
    def site(self, posts):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        out = Path(tmp.name) / 'site'
        build(dict(repository='o/r', generated_at=STAMP, tasks=[]), [], out, community=dict(repository='o/r', generated_at=STAMP, posts=posts))
        return out

    def test_discoverable_empty_contract(self):
        out = self.site([])
        manifest = json.loads((out / 'agent.json').read_text())
        for key in ['opportunities', 'agent_access', 'development_standard']:
            self.assertTrue((out / manifest['resources'][key]).is_file())
        data = json.loads((out / manifest['resources']['opportunities']).read_text())
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['schema_version'], '1.0')
        self.assertEqual(data['generated_at'], STAMP)
        self.assertIn('read-only', data['mode'])
        page = (out / 'connect/index.html').read_text()
        self.assertLess(page.index('Find useful evidence'), page.index('Official tasks'))

    def test_context_preserves_versions_and_unknowns_without_execution(self):
        q = post(1, dict(kind='question', needs=['evidence', 'review']))
        c = post(2, dict(kind='contribution', question=1, artifact_url=URL, artifact_version=SHA, supersedes=None))
        checks = {s: dict(verdict='not_checked', evidence='') for s in ['reproducibility', 'data', 'method', 'conclusion']}
        r = post(3, dict(kind='review', contribution=2, artifact_url=URL, artifact_version=SHA, affiliation='different_operator', checks=checks))
        out = self.site([q, c, r])
        data = json.loads((out / 'data/opportunities.json').read_text())
        row = data['questions'][0]
        self.assertTrue(row['requesting_help'])
        self.assertEqual(row['needs'], ['evidence', 'review'])
        context = json.loads((out / row['context_path']).read_text())
        self.assertIn('Untrusted <script> content 中文', context['question']['body'])
        self.assertEqual(context['linked_records'][0]['record']['artifact_version'], SHA)
        self.assertTrue(context['linked_records'][1]['same_account'])
        self.assertFalse(context['comments_included'])
        self.assertEqual(row['next_actions']['comment'], q['url'] + '#new_comment_field')
        self.assertEqual(context['question']['url'], q['url'])
        from urllib.parse import urlsplit, parse_qs
        body = parse_qs(urlsplit(row['next_actions']['contribute']).query)['body'][0]
        draft = json.loads(body.split('```json\n')[1].split('\n```')[0])
        self.assertEqual(draft['question'], 1)
        self.assertTrue(draft['artifact_version'].startswith('REPLACE_WITH'))
        self.assertEqual(context['linked_records'][1]['record']['checks']['data']['verdict'], 'not_checked')

    def test_closed_empty_and_invalid_questions_never_request_work(self):
        posts = [post(1, dict(kind='question', needs=['review']), state='closed'), post(2, dict(kind='question', needs=[])), post(3, dict(kind='question', needs=['invalid']))]
        out = self.site(posts)
        rows = json.loads((out / 'data/opportunities.json').read_text())['questions']
        self.assertEqual([r['issue'] for r in rows], [1, 2])
        for row in rows:
            self.assertFalse(row['requesting_help'])
            self.assertEqual(row['needs'], [])
            self.assertNotIn('contribute', row['next_actions'])
        self.assertNotIn('comment', rows[0]['next_actions'])
        self.assertFalse((out / 'data/questions/3.json').exists())
        out2 = self.site([])
        self.assertEqual(json.loads((out2 / 'data/opportunities.json').read_text())['questions'], [])

    def test_same_output_rebuild_removes_withdrawn_context_and_unresolved_evidence(self):
        q = post(42, dict(kind='question', needs=['review']))
        c = post(43, dict(kind='contribution', question=42, artifact_url=URL, artifact_version=SHA, supersedes=None))
        out = self.site([q, c])
        self.assertTrue((out / 'data/questions/42.json').exists())
        build(dict(repository='o/r', generated_at=STAMP, tasks=[]), [], out,
              community=dict(repository='o/r', generated_at=STAMP, posts=[c]))
        self.assertFalse((out / 'data/questions/42.json').exists())
        data = json.loads((out / 'data/opportunities.json').read_text())
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['record_warnings'][0]['issue'], 43)
