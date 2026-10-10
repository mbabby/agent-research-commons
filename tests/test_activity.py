import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from arc import site

STAMP = '2026-10-10T01:00:00Z'


def issue(number=1, **changes):
    return dict(number=number, title='<script>question</script>', body='<!-- arc-community:v1 -->\nQuestion', labels=[], user={'login': 'other'}, **changes)


def comment(number=1, ident=101, **changes):
    value = dict(id=ident, issue_url='https://api.github.com/repos/o/r/issues/' + str(number), html_url='https://github.com/o/r/issues/{}#issuecomment-{}'.format(number, ident), user={'login': 'reader'}, updated_at=STAMP, body='NEVER EXPORT COMMENT BODY')
    value.update(changes)
    return value


class ActivityTests(unittest.TestCase):
    def fetch(self, comments, issues):
        from arc.activity import fetch_snapshot
        def api(path):
            if '/issues/comments?' in path:
                self.assertIn('sort=updated&direction=desc&per_page=100&page=1', path)
                return comments
            return issues[int(path.rsplit('/', 1)[1])]
        with patch('arc.activity.GitHub.api', side_effect=api):
            return fetch_snapshot('o/r')

    def test_only_eligible_metadata_with_exact_comment_links(self):
        issues = {n: issue(n) for n in range(1, 7)}
        issues[2]['body'] = 'withdrawn'
        issues[3]['labels'] = [{'name': 'community:hidden'}]
        issues[4]['pull_request'] = {}
        issues[5].update(labels=[{'name': 'arc:task'}], user={'login': 'o'})
        issues[6]['labels'] = [{'name': 'arc:task'}]
        result = self.fetch([comment(n, 100+n) for n in issues], issues)
        self.assertEqual([r['issue'] for r in result['comments']], [5, 1])
        self.assertEqual(result['comments'][0]['kind'], 'official_task')
        self.assertEqual(result['comments'][0]['url'], 'https://github.com/o/r/issues/5#issuecomment-105')
        self.assertNotIn('NEVER EXPORT', json.dumps(result))
        self.assertEqual(result['coverage'], {'limit': 100, 'scanned': 6, 'order': 'updated_desc'})

    def test_network_failure_preserves_previous_file(self):
        from arc.activity import sync
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'activity.json'; path.write_text('previous')
            with patch('arc.activity.GitHub.api', side_effect=ValueError('unavailable')):
                with self.assertRaises(ValueError):
                    sync('o/r', path)
            self.assertEqual(path.read_text(), 'previous')

    def test_invalid_urls_dates_ids_and_unexpected_fields_fail_closed(self):
        from arc.activity import validate_snapshot
        valid = self.fetch([comment()], {1: issue()})
        for field, value in [('url', 'javascript:alert(1)'), ('id', True), ('updated_at', '2026-02-30T00:00:00Z'), ('author', '<img>'), ('body', 'secret')]:
            bad = copy.deepcopy(valid); bad['comments'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_snapshot(bad, 'o/r')
        with self.assertRaises(ValueError):
            self.fetch([comment(html_url='https://evil.test')], {1: issue()})

    def test_malformed_issue_number_cannot_qualify(self):
        wrong = issue(); wrong['number'] = True
        with self.assertRaises(ValueError):
            self.fetch([comment()], {1: wrong})

    def test_metadata_sort_is_update_order_and_bad_build_preserves_site(self):
        activity = self.fetch([comment(1, 102, updated_at='2026-10-09T01:00:00Z'), comment(1, 101)], {1: issue()})
        self.assertEqual([r['id'] for r in activity['comments']], [101, 102])
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'site'
            snapshot = dict(repository='o/r', generated_at=STAMP, tasks=[])
            site.build(snapshot, [], out, activity=activity)
            previous = (out / 'community/recent.html').read_text()
            activity['comments'][0]['url'] += '/malicious'
            with self.assertRaises(ValueError):
                site.build(snapshot, [], out, activity=activity)
            self.assertEqual((out / 'community/recent.html').read_text(), previous)

    def test_page_and_manifest_and_explicit_offline_unavailable(self):
        snapshot = dict(repository='o/r', generated_at=STAMP, tasks=[])
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'site'
            site.build(snapshot, [], out)
            self.assertTrue((out / 'community/recent.html').exists(), 'legacy builds need an explicit unavailable page')
            self.assertIn('unavailable', (out / 'community/recent.html').read_text())
            activity = self.fetch([comment()], {1: issue()})
            site.build(snapshot, [], out, activity=activity)
            page = (out / 'community/recent.html').read_text()
            self.assertIn('&lt;script&gt;question&lt;/script&gt;', page)
            self.assertIn('#issuecomment-101', page)
            self.assertIn('bounded', page)
            self.assertNotIn('NEVER EXPORT', page)
            manifest = json.loads((out / 'agent.json').read_text())
            self.assertEqual(manifest['resources']['activity'], 'data/activity.json')
            for relative in ['community/index.html', 'connect/index.html']:
                self.assertIn('recent.html', (out / relative).read_text())
            activity['comments'] = []; activity['coverage']['scanned'] = 0
            site.build(snapshot, [], out, activity=activity)
            self.assertIn('No eligible comments', (out / 'community/recent.html').read_text())


if __name__ == '__main__':
    unittest.main()
