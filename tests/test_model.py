import unittest
from arc.model import transition, validate_task

def task():
    return dict(number=1,title='Question',question='Why?',scope='Scope',exclusions=[],as_of='2026-10-09',deliverable='Report',acceptance=['Evidence'],parent=None,status='open',agent_id=None,coordinator='host',attempt=0,updated_at='2026-10-09',history=[])
class ModelTests(unittest.TestCase):
    def test_lifecycle_and_idempotency(self):
        t=transition(task(),'assign','host','a',agent_id='researcher')
        self.assertEqual(transition(t,'assign','host','a',agent_id='researcher'),t)
        with self.assertRaises(ValueError): transition(t,'assign','host','b',agent_id='other')
        t=transition(t,'start','researcher','s',attempt=1)
        t=transition(t,'submit','researcher','u',attempt=1,artifact_url='https://github.com/o/r/pull/1')
        with self.assertRaises(ValueError): transition(t,'review','researcher','r',attempt=1,verdict='pass',notes='ok')
        t=transition(t,'review','reviewer','r',attempt=1,verdict='changes_requested',notes='fix')
        t=transition(t,'submit','researcher','u2',attempt=1,artifact_url='https://github.com/o/r/pull/1')
        t=transition(t,'review','reviewer','r2',attempt=1,verdict='pass',notes='ok')
        t=transition(t,'complete','host','c',attempt=1,merged_url='https://github.com/o/r/pull/1',review_operation_id='r2')
        self.assertEqual(t['status'],'completed')
    def test_stale_and_authority(self):
        t=transition(task(),'assign','host','a',agent_id='one')
        with self.assertRaises(ValueError): transition(t,'release','other','x',attempt=1)
        t=transition(t,'release','host','l',attempt=1)
        t=transition(t,'assign','host','a2',agent_id='two',attempt=1)
        with self.assertRaises(ValueError): transition(t,'start','two','s',attempt=1)
        t['status']='bogus'
        with self.assertRaises(ValueError): validate_task(t)
    def test_evidence(self):
        t=transition(task(),'assign','host','a',agent_id='one')
        t=transition(t,'start','one','s',attempt=1)
        with self.assertRaises(ValueError): transition(t,'submit','one','u',attempt=1,artifact_url='javascript:bad')

class ReportTests(unittest.TestCase):
    def fixture(self):
        t=transition(task(),'assign','host','a',agent_id='researcher')
        t=transition(t,'start','researcher','s',attempt=1)
        t=transition(t,'submit','researcher','u',attempt=1,artifact_url='https://github.com/o/r/pull/1')
        t=transition(t,'review','reviewer','r',attempt=1,verdict='pass',notes='ok')
        t=transition(t,'complete','host','c',attempt=1,merged_url='https://github.com/o/r/pull/1',review_operation_id='r')
        report=dict(slug='example',title='Title',summary='Summary',task_number=1,agent_id='researcher',attempt=1,as_of='2026-10-09',published_at='2026-10-09',claims=[dict(id='c1',kind='fact',text='Evidence',source_ids=['s1'])],sources=[dict(id='s1',title='Primary',url='https://example.org',accessed_at='2026-10-09',published_at=None,supports=['c1'],note='')],unknowns=[],method='Read sources',limitations=[],review=dict(agent_id='reviewer',notes='ok',review_url='https://github.com/o/r/issues/1#issuecomment-1'),acceptance_url='https://github.com/o/r/pull/1',revision=1)
        return t,report
    def test_valid_report_and_evidence(self):
        from arc.model import validate_report
        t,r=self.fixture(); validate_report(r,[t])
        r['claims'][0]['source_ids']=[]
        with self.assertRaises(ValueError): validate_report(r,[t])
    def test_unsafe_slug_and_unrelated_record(self):
        from arc.model import validate_report
        t,r=self.fixture(); r['slug']='../escape'
        with self.assertRaises(ValueError): validate_report(r,[t])
        r['slug']='safe'; r['review']['review_url']='https://github.com/other/repo/issues/1'
        with self.assertRaises(ValueError): validate_report(r,[t])
    def test_history_authority(self):
        t=transition(task(),'assign','host','a',agent_id='researcher')
        t['history'][0]['actor']='attacker'
        with self.assertRaises(ValueError): validate_task(t)
