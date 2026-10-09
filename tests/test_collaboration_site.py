import json
import tempfile
import unittest
from pathlib import Path
from arc.site import build

STAMP = '2026-10-09T04:00:00Z'
VERSION = 'a' * 40
ARTIFACT = 'https://github.com/external/research/tree/' + VERSION

def post(number, record=None, author='external-agent', body='中文 <script>unsafe</script>'):
    if record is not None:
        body = '<!-- arc-record:v1 -->\n```json\n' + json.dumps(record) + '\n```\n' + body
    return dict(number=number, title='Evidence question', body=body, author=author,
                state='open', created_at=STAMP, updated_at=STAMP,
                url='https://github.com/o/r/issues/' + str(number), comments=0)

class CollaborationSiteTests(unittest.TestCase):
    def render(self, posts):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        out = Path(tmp.name) / 'site'
        build(dict(repository='o/r', generated_at=STAMP, tasks=[]), [], out,
              community=dict(repository='o/r', generated_at=STAMP, posts=posts))
        return out

    def test_empty_discovery_and_legacy_prose(self):
        out = self.render([post(1)])
        manifest = json.loads((out / 'agent.json').read_text())
        for key in ('collaboration', 'help_needed', 'contribution_history', 'collaboration_guide'):
            self.assertTrue((out / manifest['resources'][key]).exists())
        self.assertIn('No current help requests', (out / 'community/needs.html').read_text())
        self.assertIn('No linked evidence histories', (out / 'community/history.html').read_text())
        self.assertIn('&lt;script&gt;', (out / 'community/1.html').read_text())
        self.assertIn('community/needs.html', (out / 'index.html').read_text())

    def test_scoped_evidence_version_and_same_account_disclosure(self):
        question = post(27, dict(kind='question', needs=['evidence', 'review']))
        contribution = post(40, dict(kind='contribution', question=27, artifact_url='https://github.com/external/research/tree/' + VERSION, artifact_version=VERSION, supersedes=None))
        checks = {key: dict(verdict='not_checked', evidence='') for key in ('reproducibility', 'data', 'method', 'conclusion')}
        checks['method'] = dict(verdict='concerns', evidence='Missing comparator')
        review = post(41, dict(kind='review', contribution=40, artifact_url=ARTIFACT, artifact_version=VERSION, affiliation='different_operator', checks=checks))
        reuse = post(42, dict(kind='reuse', contribution=40, artifact_url=ARTIFACT, artifact_version=VERSION, outcome='Found a regression', evidence_url='https://github.com/external/research/issues/7'), author='reader')
        out = self.render([question, contribution, review, reuse])
        detail = (out / 'community/40.html').read_text()
        for text in ('Reproducibility', 'Data', 'Method', 'Conclusion', 'Missing comparator', VERSION, 'Same-account', 'rel="noreferrer nofollow"'):
            self.assertIn(text, detail)
        self.assertNotIn('<script>unsafe', detail)
        self.assertIn('community-review.md', detail)
        self.assertIn('42.html', (out / 'community/history.html').read_text())
        self.assertIn('40.html', (out / 'community/27.html').read_text())
        self.assertNotIn('arc-record:v1', detail)

    def test_invalid_metadata_remains_visible_without_history_credit(self):
        out = self.render([post(7, dict(kind='reuse', contribution=99, artifact_url=ARTIFACT, artifact_version=VERSION, outcome='Claim', evidence_url='https://github.com/o/r/issues/1')),
                           post(8, dict(kind='question', needs=['invented']))])
        self.assertIn('Record warning', (out / 'community/7.html').read_text())
        self.assertIn('arc-record:v1', (out / 'community/8.html').read_text())
        self.assertNotIn('7.html', (out / 'community/history.html').read_text())

    def test_superseded_version_does_not_inherit_reviews_and_links_resolve(self):
        from test_site import Links
        q = post(27, dict(kind='question', needs=['review']))
        c = post(40, dict(kind='contribution', question=27, artifact_url='https://github.com/external/research/tree/' + VERSION, artifact_version=VERSION, supersedes=None))
        checks = {key: dict(verdict='supported', evidence='Observed fixture output') for key in ('reproducibility', 'data', 'method', 'conclusion')}
        r = post(41, dict(kind='review', contribution=40, artifact_url=ARTIFACT, artifact_version=VERSION, affiliation='unknown', checks=checks), author='reviewer')
        new = post(43, dict(kind='contribution', question=27, artifact_url='https://github.com/external/research/commit/' + 'b'*40, artifact_version='b'*40, supersedes=40))
        out = self.render([q, c, r, new])
        self.assertIn('Superseded by', (out / 'community/40.html').read_text())
        updated = (out / 'community/43.html').read_text()
        self.assertIn('No scoped reviews for this exact contribution version', updated)
        self.assertNotIn('Observed fixture output', updated)
        for page in out.rglob('*.html'):
            parser = Links(); parser.feed(page.read_text())
            for link in parser.local:
                self.assertTrue((page.parent / link).exists(), (page, link))

    def test_withdrawn_contribution_removes_linked_review_from_history(self):
        checks = {key: dict(verdict='not_checked', evidence='') for key in ('reproducibility', 'data', 'method', 'conclusion')}
        out = self.render([post(27, dict(kind='question', needs=[])),
                           post(41, dict(kind='review', contribution=40, artifact_url=ARTIFACT, artifact_version=VERSION, affiliation='unknown', checks=checks), author='reviewer')])
        self.assertIn('Record warning', (out / 'community/41.html').read_text())
        self.assertNotIn('41.html', (out / 'community/history.html').read_text())
        self.assertNotIn('41.html', (out / 'community/27.html').read_text())

    def test_exported_community_documents_have_resolvable_markdown_links(self):
        import re
        out = self.render([])
        for name in ('community-policy.md', 'collaboration-guide.md', 'skill.md'):
            for target in re.findall(r'\]\(([^)]+)\)', (out / name).read_text()):
                if not target.startswith(('http:', 'https:', '#', 'mailto:')):
                    path = target.split('#')[0].split('?')[0]
                    self.assertTrue((out / path).is_file(), (name, target))

    def test_context_actions_prefill_real_links_without_invented_evidence(self):
        from html.parser import HTMLParser
        from urllib.parse import urlsplit, parse_qs
        class Actions(HTMLParser):
            def __init__(self):
                super().__init__(); self.queries = []
            def handle_starttag(self, tag, attrs):
                href = dict(attrs).get('href', '')
                if '/issues/new?' in href:
                    self.queries.append(parse_qs(urlsplit(href).query))
        out = self.render([post(71, dict(kind='question', needs=['review'])),
                           post(85, dict(kind='contribution', question=71, artifact_url='https://github.com/external/research/tree/' + VERSION, artifact_version=VERSION, supersedes=None))])
        actions = Actions(); actions.feed((out / 'community/85.html').read_text())
        def record(kind):
            query = next(q for q in actions.queries if q.get('template') == ['community-' + kind + '.md'])
            body = query['body'][0]
            self.assertIn('<!-- arc-community:v1 -->', body)
            return json.loads(body.split('```json\n')[1].split('\n```')[0])
        review = record('review')
        self.assertEqual(review['contribution'], 85)
        self.assertEqual(review['artifact_version'], VERSION)
        self.assertEqual(review['artifact_url'], ARTIFACT)
        self.assertEqual(review['affiliation'], 'unknown')
        self.assertEqual(set(review['checks']), {'reproducibility', 'data', 'method', 'conclusion'})
        self.assertTrue(all(c == dict(verdict='not_checked', evidence='') for c in review['checks'].values()))
        self.assertEqual(record('reuse')['contribution'], 85)
        self.assertEqual(record('reuse')['artifact_url'], ARTIFACT)
        correction = record('contribution')
        self.assertEqual(correction['question'], 71)
        self.assertEqual(correction['supersedes'], 85)
        self.assertNotEqual(correction['artifact_version'], VERSION)
        actions = Actions(); actions.feed((out / 'community/71.html').read_text())
        for query in actions.queries:
            if query.get('template') in (['community-intent.md'], ['community-contribution.md']):
                body = json.loads(query['body'][0].split('```json\n')[1].split('\n```')[0])
                self.assertEqual(body['question'], 71)

    def test_changed_artifact_url_same_version_does_not_inherit_feedback(self):
        checks = {key: dict(verdict='supported', evidence='Old path evidence') for key in ('reproducibility', 'data', 'method', 'conclusion')}
        out = self.render([post(27, dict(kind='question', needs=['review'])),
                           post(40, dict(kind='contribution', question=27, artifact_url=ARTIFACT + '/different-file', artifact_version=VERSION, supersedes=None)),
                           post(41, dict(kind='review', contribution=40, artifact_url=ARTIFACT, artifact_version=VERSION, affiliation='unknown', checks=checks), author='reviewer'),
                           post(42, dict(kind='reuse', contribution=40, artifact_url=ARTIFACT, artifact_version=VERSION, outcome='Old URL outcome', evidence_url='https://github.com/o/r/issues/7'), author='reader')])
        detail = (out / 'community/40.html').read_text()
        self.assertIn('No scoped reviews for this exact contribution version', detail)
        self.assertNotIn('Old path evidence', detail)
        self.assertNotIn('Old URL outcome', detail)
        self.assertNotIn('41.html', (out / 'community/history.html').read_text())
        self.assertNotIn('42.html', (out / 'community/history.html').read_text())

    def test_unpaired_json_surrogate_is_a_warning_not_a_deployment_failure(self):
        intent = dict(kind='intent', question=27, scope=chr(0xD800), expires_at='2026-10-16T00:00:00Z')
        candidate = post(28, intent)
        candidate['body'].encode('utf-8')  # Raw JSON escape is harmless ASCII.
        out = self.render([post(27, dict(kind='question', needs=['evidence'])), candidate])
        self.assertIn('Record warning', (out / 'community/28.html').read_text())
        self.assertIn('arc-record:v1', (out / 'community/28.html').read_text())
        graph = json.loads((out / 'data/collaboration.json').read_text())
        self.assertFalse(next(r for r in graph['records'] if r['issue'] == 28)['valid'])
