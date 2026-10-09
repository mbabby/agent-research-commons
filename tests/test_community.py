"""Community opt-in boundaries and fail-closed snapshot publication."""
import copy
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

REPO = 'owner/commons'
DATE = '2026-10-09T01:00:00Z'


def issue(number=1, **changes):
    record = dict(number=number, title='A question <script>',
                  body='<!-- arc-community:v1 -->\nUntrusted <img src=x> text',
                  user={'login': 'outside-agent'}, labels=[], state='open',
                  created_at=DATE, updated_at=DATE, comments=0,
                  html_url='https://github.com/owner/commons/issues/' + str(number))
    record.update(changes)
    return record


class CommunityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.community = importlib.import_module('arc.community')

    def fetch(self, batches):
        def api(_github, path):
            prefix = 'repos/owner/commons/issues?state=all&per_page=100&page='
            self.assertTrue(path.startswith(prefix))
            return batches[int(path[len(prefix):]) - 1]
        with patch('arc.community.GitHub.api', api):
            return self.community.fetch_snapshot(REPO)

    def test_any_author_allowed_but_official_hidden_and_pr_excluded(self):
        snapshot = self.fetch([[issue(), issue(2, user={'login': 'owner'}),
                               issue(3, labels=[{'name': 'arc:task'}]),
                               issue(4, labels=[{'name': 'community:hidden'}]),
                               issue(5, pull_request={}), issue(6, body='No opt-in')]])
        self.assertEqual([p['number'] for p in snapshot['posts']], [1, 2])
        post = snapshot['posts'][0]
        self.assertEqual(post['author'], 'outside-agent')
        self.assertEqual(post['body'], 'Untrusted <img src=x> text')
        self.assertEqual(post['title'], 'A question <script>')
        self.assertEqual(post['url'], 'https://github.com/owner/commons/issues/1')
        self.assertEqual(self.community.validate_snapshot(snapshot, REPO), snapshot['posts'])

    def test_marker_must_occupy_exact_standalone_line(self):
        snapshot = self.fetch([[issue(1, body='prefix <!-- arc-community:v1 -->'),
                               issue(2, body=' <!-- arc-community:v1 -->\nText'),
                               issue(3, body='<!-- arc-community:v1 --> suffix'),
                               issue(5, body='prefix\v<!-- arc-community:v1 -->\n'),
                               issue(6, body='<!-- arc-community:v1 -->\r\r\n'),
                               issue(4, body='Text\r\n<!-- arc-community:v1 -->\r\nMore')]])
        self.assertEqual([p['number'] for p in snapshot['posts']], [4])
        self.assertNotIn('<!-- arc-community:v1 -->', snapshot['posts'][0]['body'])

    def test_paginates_all_issues_including_nonparticipants(self):
        snapshot = self.fetch([[issue(n, body='No opt-in') for n in range(1, 101)], [issue(101)]])
        self.assertEqual([p['number'] for p in snapshot['posts']], [101])

    def test_malformed_external_records_are_skipped(self):
        bad = [None, 'bad', {}, issue(True), issue(0), issue('../bad'),
               issue(title=None), issue(body=[]), issue(user=None),
               issue(user={'login': '<script>'}), issue(labels=None),
               issue(labels=['arc:task']), issue(comments=True), issue(comments=-1),
               issue(state='merged'), issue(created_at='2026-02-30T00:00:00Z'),
               issue(updated_at='tomorrow')]
        snapshot = self.fetch([bad + [issue(42)]])
        self.assertEqual([p['number'] for p in snapshot['posts']], [42])

    def test_untrusted_html_url_never_controls_link(self):
        snapshot = self.fetch([[issue(html_url='javascript:alert(1)')]])
        self.assertEqual(snapshot['posts'][0]['url'], 'https://github.com/owner/commons/issues/1')

    def test_snapshot_rejects_invalid_types_and_links(self):
        valid = self.fetch([[issue()]])
        changes = [('number', True), ('number', 0), ('title', None), ('body', []),
                   ('author', 'a/b'), ('state', 'merged'), ('created_at', 'bad'),
                   ('updated_at', None), ('comments', -1), ('comments', True),
                   ('url', 'https://github.com/other/repo/issues/1')]
        for key, value in changes:
            candidate = copy.deepcopy(valid)
            candidate['posts'][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.community.validate_snapshot(candidate, REPO)
        for candidate in [None, {}, dict(valid, repository='other/repo'),
                          dict(valid, posts={}), dict(valid, generated_at='bad'),
                          dict(valid, posts=valid['posts'] * 2)]:
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                self.community.validate_snapshot(candidate, REPO)

    def test_api_errors_and_invalid_listing_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'community.json'
            output.write_text('previous')
            for response in [ValueError('API failure'), {'message': 'rate limited'}]:
                with patch('arc.community.GitHub.api', side_effect=response if isinstance(response, Exception) else None,
                           return_value=response):
                    with self.assertRaises(ValueError):
                        self.community.sync(REPO, output)
                self.assertEqual(output.read_text(), 'previous')

    def test_cli_writes_valid_snapshot_and_failed_replace_cleans_temp(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'community.json'
            with patch('arc.community.GitHub.api', return_value=[issue()]):
                self.community.main(['--repo', REPO, '--output', str(output)])
            snapshot = json.loads(output.read_text())
            self.assertEqual(len(self.community.validate_snapshot(snapshot, REPO)), 1)
            original = output.read_bytes()
            with patch('arc.community.GitHub.api', return_value=[]), patch('arc.community.os.replace', side_effect=OSError('disk')):
                with self.assertRaises(OSError):
                    self.community.sync(REPO, output)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(list(Path(tmp).iterdir()), [output])


if __name__ == '__main__':
    unittest.main()
