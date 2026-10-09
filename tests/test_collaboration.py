import copy
import json
import unittest
from arc import collaboration

V = '0123456789abcdef0123456789abcdef01234567'
NOW = '2026-10-09T00:00:00Z'

def post(n, record, author='external', state='open'):
    return dict(number=n, author=author, state=state,
                body='Chinese prose 中文\n<!-- arc-record:v1 -->\n```json\n' + json.dumps(record) + '\n```\nTail <script>')

def question():
    return dict(kind='question', needs=['evidence', 'review'])

def contribution(**extra):
    return dict(kind='contribution', question=1, artifact_url='https://github.com/external/private/tree/'+V,
                artifact_version=V, supersedes=None, **extra)

def review(target=3, version=V):
    return dict(kind='review', contribution=target, artifact_version=version, artifact_url='https://github.com/external/private/tree/'+V, affiliation='different_operator',
                checks={k:dict(verdict='supported', evidence='Observed output') for k in ['reproducibility','data','method','conclusion']})

class CollaborationTests(unittest.TestCase):
    def test_all_kinds_graph_and_nonexclusive_intents(self):
        posts=[post(1,question()), post(2,dict(kind='intent',question=1,scope='Reproduce',expires_at='2026-10-10T00:00:00Z')),
               post(3,contribution()),post(4,review()),post(5,dict(kind='reuse',contribution=3,artifact_version=V,artifact_url='https://github.com/external/private/tree/'+V,outcome='Found regression',evidence_url='https://example.com/evidence')),
               post(6,dict(kind='intent',question=1,scope='Independent reproduction',expires_at='2026-10-11T00:00:00Z'))]
        original=copy.deepcopy(posts)
        result=collaboration.derive(list(reversed(posts)),NOW)
        self.assertEqual(result['timelines'],{'1':[1,2,3,4,5,6]})
        self.assertEqual(result['needs'],[dict(question=1,need='evidence',intents=[2,6]),dict(question=1,need='review',intents=[2,6])])
        self.assertTrue(result['records'][3]['same_account'])
        self.assertEqual(result['profiles'],[dict(author='external',contributions=[3],reviews=[4],reuse=[5])])
        self.assertEqual(posts,original)

    def test_malformed_metadata_stays_visible_and_warns(self):
        bodies=['<!-- arc-record:v1 -->\n```json\n{"kind":"question","kind":"question","needs":[]}\n```',
                '<!-- arc-record:v1 -->\n```json\n{"kind":"question","needs":[],"extra":1}\n```',
                '<!-- arc-record:v1 -->\n```json\n{"kind":"other"}\n```',
                '<!-- arc-record:v1 -->\n```json\nNaN\n```',
                '<!-- arc-record:v1 -->\n```json\n{"kind":"question","needs":[]}\n```\n<!-- arc-record:v1 -->']
        for body in bodies:
            with self.subTest(body=body):
                p=post(1,question()); p['body']=body
                result=collaboration.derive([p],NOW)
                self.assertFalse(result['records'][0]['valid'])
                self.assertEqual(result['records'][0]['kind'],'invalid')
                self.assertEqual(result['records'][0]['record'],{})
                self.assertLess(len(result['warnings'][0]['error']),160)
                self.assertEqual(collaboration.display_body(body),body)

    def test_display_removes_only_valid_block_and_preserves_unsafe_prose(self):
        self.assertEqual(collaboration.display_body(post(1,question())['body']),'Chinese prose 中文\nTail <script>')
        self.assertEqual(collaboration.derive([dict(number=9,author='x',state='open',body='legacy')],NOW)['records'],[])

    def test_invalid_authority_versions_targets_and_urls(self):
        for change in [dict(artifact_version='a'*40),dict(artifact_url='https://github.com/x/y/tree/'+V+'?secret=x'),dict(artifact_url='https://x@github.com/x/y/tree/'+V),dict(question=True),dict(supersedes=3)]:
            c=contribution(); c.update(change)
            result=collaboration.derive([post(1,question()),post(3,c)],NOW)
            self.assertFalse(result['records'][-1]['valid'])
        for target,version in [(1,V),(99,V),(3,'a'*40)]:
            self.assertFalse(collaboration.derive([post(1,question()),post(3,contribution()),post(4,review(target,version))],NOW)['records'][-1]['valid'])

    def test_supersession_preserves_versions_without_inherited_review(self):
        c=contribution(); c['supersedes']=3
        posts=[post(1,question()),post(3,contribution()),post(4,review()),post(5,c)]
        result=collaboration.derive(posts,NOW)
        self.assertEqual(result['profiles'][0]['contributions'],[3,5])
        self.assertEqual(result['records'][2]['record']['contribution'],3)
        posts[-1]['author']='other'
        self.assertFalse(collaboration.derive(posts,NOW)['records'][-1]['valid'])
        posts[-1]['author']='external'; posts.append(post(7,question())); c['question']=7; posts[-2]=post(5,c)
        self.assertFalse(next(r for r in collaboration.derive(posts,NOW)['records'] if r['issue']==5)['valid'])

    def test_expiry_closed_question_and_withdrawn_target(self):
        intent=dict(kind='intent',question=1,scope='Check',expires_at=NOW)
        result=collaboration.derive([post(1,question()),post(2,intent)],NOW)
        self.assertFalse(result['records'][1]['active'])
        self.assertEqual(result['needs'][0]['intents'],[])
        result=collaboration.derive([post(1,question(),state='closed'),post(3,contribution()),post(4,review())],NOW)
        self.assertEqual(result['needs'],[])
        result=collaboration.derive([post(1,question()),post(4,review())],NOW)
        self.assertFalse(result['records'][-1]['valid'])
        self.assertEqual(result['profiles'],[])

    def test_reuse_links_and_other_account_disclosure(self):
        reuse=dict(kind='reuse',contribution=3,artifact_version=V,artifact_url='https://github.com/external/private/tree/'+V,outcome='Found regression',evidence_url='https://example.com/evidence')
        posts=[post(1,question()),post(3,contribution()),post(4,review(),author='reviewer'),post(5,reuse,author='user')]
        result=collaboration.derive(posts,NOW)
        self.assertFalse(result['records'][2]['same_account'])
        self.assertFalse(result['records'][3]['same_account'])
        for url in ['http://example.com/evidence','https://user:password@example.com/evidence','https://example.com:invalid/path']:
            reuse['evidence_url']=url
            self.assertFalse(collaboration.derive([post(1,question()),post(3,contribution()),post(5,reuse)],NOW)['records'][-1]['valid'])

    def test_closed_and_missing_question_intents_are_not_active(self):
        intent=dict(kind='intent',question=1,scope='Check',expires_at='2026-10-10T00:00:00Z')
        result=collaboration.derive([post(1,question()),post(2,intent,state='closed')],NOW)
        self.assertTrue(result['records'][1]['valid'])
        self.assertFalse(result['records'][1]['active'])
        self.assertFalse(collaboration.derive([post(2,intent)],NOW)['records'][0]['valid'])

    def test_later_json_evidence_is_preserved_and_empty_url_delimiters_invalid(self):
        p=post(1,question()); p['body'] += '\n```json\n{}\n```'
        self.assertTrue(collaboration.derive([p],NOW)['records'][0]['valid'])
        self.assertEqual(collaboration.display_body(p['body']), 'Chinese prose 中文\nTail <script>\n```json\n{}\n```')
        for suffix in ['?', '#']:
            c=contribution(); c['artifact_url'] += suffix
            self.assertFalse(collaboration.derive([post(1,question()),post(3,c)],NOW)['records'][-1]['valid'])

    def test_untrusted_wrong_types_are_bounded_diagnostics(self):
        for field,value in [('needs',[{}]),('needs',None)]:
            q=question(); q[field]=value
            result=collaboration.derive([post(1,q)],NOW)
            self.assertFalse(result['records'][0]['valid'])
            self.assertLess(len(result['warnings'][0]['error']),160)
        r=review(); r['checks']['data']['verdict']={'untrusted':'object'}
        self.assertFalse(collaboration.derive([post(1,question()),post(3,contribution()),post(4,r)],NOW)['records'][-1]['valid'])

    def test_fixed_artifact_paths_cannot_normalize_away_revision(self):
        paths = [
            '/o/r/tree/' + V + '/../main',
            '/o/r/tree/' + V + '/%2e%2E/main',
            '/o/r/tree/' + V + '/.%2e/main',
            '/o/r/tree/' + V + '/%252e%252e/main',
            '/o/r/tree/' + V + '/x%2f..%2f../main',
            '/o/r/tree/' + V + '/x%5c..%5c../main',
            '/%6f/r/tree/' + V,
            '/o/%72/tree/' + V,
            '/o/r:/tree/' + V,
        ]
        for path in paths:
            with self.subTest(path=path):
                c=contribution(); c['artifact_url']='https://github.com'+path
                result=collaboration.derive([post(1,question()),post(3,c)],NOW)
                self.assertFalse(result['records'][-1]['valid'])
                self.assertEqual(result['profiles'],[])
        c=contribution(); c['artifact_url']='https://github.com/o/research-fixtures/blob/'+V+'/results/observed%20output.json'
        self.assertTrue(collaboration.derive([post(1,question()),post(3,c)],NOW)['records'][-1]['valid'])

    def test_artifact_url_change_invalidates_review_and_reuse_at_same_sha(self):
        reuse=dict(kind='reuse',contribution=3,artifact_version=V,
                   artifact_url='https://github.com/external/private/tree/'+V,
                   outcome='Found regression',evidence_url='https://example.com/evidence')
        c=contribution(); c['artifact_url']='https://github.com/external/other/tree/'+V
        result=collaboration.derive([post(1,question()),post(3,c),post(4,review()),post(5,reuse)],NOW)
        self.assertFalse(result['records'][2]['valid'])
        self.assertFalse(result['records'][3]['valid'])
        self.assertEqual(result['profiles'][0]['reviews'],[])
        c['artifact_url']='https://github.com/external/private/tree/'+V+'/different-path'
        self.assertFalse(collaboration.derive([post(1,question()),post(3,c),post(4,review())],NOW)['records'][-1]['valid'])

    def test_unpaired_surrogate_metadata_is_rejected_before_publication(self):
        for location in ['scope', 'key', 'nested']:
            body='<!-- arc-record:v1 -->\n```json\n'
            if location=='scope':
                body += '{"kind":"intent","question":1,"scope":"\\ud800","expires_at":"2026-10-10T00:00:00Z"}'
            elif location=='key':
                body += '{"kind":"question","needs":[],"\\udfff":"x"}'
            else:
                body += '{"kind":"question","needs":[{"x":"\\udc00"}]}'
            body += '\n```'
            p=post(2,question()); p['body']=body
            result=collaboration.derive([post(1,question()),p],NOW)
            self.assertFalse(result['records'][-1]['valid'])
            self.assertEqual(collaboration.display_body(body),body)
            self.assertLess(len(result['warnings'][-1]['error']),160)
            json.dumps(result,ensure_ascii=False).encode('utf-8')
        intent=dict(kind='intent',question=1,scope='Reproduce 😀',expires_at='2026-10-10T00:00:00Z')
        result=collaboration.derive([post(1,question()),post(2,intent)],NOW)
        self.assertTrue(result['records'][-1]['valid'])
        self.assertEqual(result['records'][-1]['record']['scope'],'Reproduce 😀')
        json.dumps(result,ensure_ascii=False).encode('utf-8')

    def test_review_checks_and_https_reuse_are_strict(self):
        mutations=[lambda r:r['checks']['data'].update(evidence=''),lambda r:r['checks'].pop('method'),lambda r:r.update(affiliation='verified')]
        for mutate in mutations:
            r=review(); mutate(r)
            self.assertFalse(collaboration.derive([post(1,question()),post(3,contribution()),post(4,r)],NOW)['records'][-1]['valid'])
        r=review(); r['checks']['data']=dict(verdict='not_checked',evidence='')
        self.assertTrue(collaboration.derive([post(1,question()),post(3,contribution()),post(4,r)],NOW)['records'][-1]['valid'])

if __name__=='__main__': unittest.main()
