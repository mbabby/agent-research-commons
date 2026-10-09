import contextlib
import io
import json
import subprocess
import unittest
from unittest.mock import patch
from arc.cli import main
from arc.github import GitHub, body
from test_model import task

class CLITests(unittest.TestCase):
    def issue(self,t=None,author='owner'):
        return dict(number=1,user={'login':author},labels=[{'name':'arc:task'},{'name':'keep'},{'name':'status:open'}],body=body(t or task()))
    def test_transport_and_owner_filter(self):
        response=subprocess.CompletedProcess([],0,json.dumps([self.issue(),self.issue(author='attacker')]),'')
        with patch('subprocess.run',return_value=response) as run:
            self.assertEqual(len(GitHub('owner/repo').tasks()),1)
            self.assertEqual(run.call_args.args[0][0:2],['gh','api'])
    def test_api_failure_cli(self):
        response=subprocess.CompletedProcess([],1,'','secret credentials')
        err=io.StringIO()
        with patch('subprocess.run',return_value=response), contextlib.redirect_stderr(err):
            self.assertEqual(main(['--repo','owner/repo','list']),1)
        self.assertNotIn('secret',err.getvalue())
    def test_malformed_official_fails(self):
        issue=self.issue(); issue['body']='bad'
        with patch.object(GitHub,'api',return_value=[issue]):
            with self.assertRaises(ValueError): GitHub('owner/repo').tasks()
    def test_assign_patch_preserves_labels(self):
        responses=[self.issue(),{}]
        out=io.StringIO()
        with patch.object(GitHub,'api',side_effect=responses) as api, contextlib.redirect_stdout(out):
            self.assertEqual(main(['--repo','owner/repo','assign','1','--agent','a','--actor','host','--attempt','0','--operation-id','a']),0)
            self.assertEqual(api.call_args.args[2]['labels'],['arc:task','keep','status:assigned'])
        self.assertEqual(json.loads(out.getvalue())['attempt'],1)
    def test_merged_verification(self):
        with patch.object(GitHub,'api',return_value={'merged':False}):
            with self.assertRaises(ValueError): GitHub('owner/repo').verify_merged('https://github.com/owner/repo/pull/2')
        with self.assertRaises(ValueError): GitHub('owner/repo').verify_merged('https://github.com/other/repo/pull/2')
    def test_tampered_state_rejected(self):
        t=task(); t['status']='completed'
        with self.assertRaises(ValueError): GitHub('owner/repo').parse(self.issue(t))
    def test_markdown_round_trip(self):
        t=task(); t['question']='Explain ```python print(1) ```'
        issue=self.issue(t); pass
        self.assertEqual(GitHub('owner/repo').parse(issue),t)
    def test_status_labels_conflict(self):
        issue=self.issue(); issue['labels'] += [{'name':'status:open'},{'name':'status:assigned'}]
        with self.assertRaises(ValueError): GitHub('owner/repo').parse(issue)
    def test_sync_verifies_completion(self):
        from test_model import ReportTests
        t,_=ReportTests().fixture()
        issue=self.issue(t); issue['labels'][-1]['name']='status:completed'
        github=GitHub('o/r',owner='owner')
        with patch.object(github,'api',side_effect=[[issue],{'merged':False}]):
            with self.assertRaises(ValueError): github.tasks()
        with patch.object(github,'api',side_effect=[[issue],{'merged':True,'merged_at':'2026-10-09'}]) as api:
            self.assertEqual(github.tasks()[0]['status'],'completed')
            self.assertEqual(api.call_args.args[0],'repos/o/r/pulls/1')
        for url in ('https://example.org/no-pr','https://github.com/other/repo/pull/1'):
            for event in t['history']:
                if event['action']=='submit': event['artifact_url']=url
                if event['action']=='complete': event['merged_url']=url
            issue['body']=body(t)
            with patch.object(github,'api',return_value=[issue]):
                with self.assertRaises(ValueError): github.tasks()
