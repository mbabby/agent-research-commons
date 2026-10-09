"""GitHub transport via gh, with owner-filtered authoritative issue bodies."""
import json
import re
import subprocess
from urllib.parse import urlparse
from .model import validate_task
MARKER='<!-- arc-task:v1 -->'
def body(task):
    return task['question']+'\n\n'+MARKER+'\n```json\n'+json.dumps(task,ensure_ascii=False,indent=2)+'\n```\n'
class GitHub:
    def __init__(self,repo,owner=None):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo): raise ValueError('Invalid repository')
        self.repo=repo; self.owner=owner or repo.split('/')[0]
    def api(self,path,method='GET',data=None):
        args=['gh','api',path,'--method',method]
        if data is not None: args+=['--input','-']
        result=subprocess.run(args,input=json.dumps(data) if data is not None else None,text=True,capture_output=True)
        if result.returncode: raise ValueError('GitHub API request failed')
        try: return json.loads(result.stdout)
        except json.JSONDecodeError: raise ValueError('Invalid GitHub response')
    def official(self,issue):
        return 'pull_request' not in issue and issue.get('user',{}).get('login')==self.owner and any(l.get('name')=='arc:task' for l in issue.get('labels',[]))
    def parse(self, issue):
        # A closing fence must occupy its own line. Backticks inside JSON
        # strings are normal research prose and must not terminate the record.
        pattern = re.escape(MARKER) + r'\s*```json[^\S\n]*\n([\s\S]*?)^```[^\S\n]*(?:\n|$)'
        matches = re.findall(pattern, issue.get('body') or '', re.MULTILINE)
        if len(matches) != 1:
            raise ValueError('Malformed official task body')
        try:
            task = json.loads(matches[0])
        except json.JSONDecodeError:
            raise ValueError('Malformed task JSON')
        validate_task(task)
        if (task['number'] == 0 and task['status'] == 'open'
                and len(task['history']) == 1
                and task['history'][0]['action'] == 'create'):
            task['number'] = issue['number']
        if task['number'] != issue['number']:
            raise ValueError('Issue number mismatch')
        status_labels = [label['name'] for label in issue.get('labels', [])
                         if label['name'].startswith('status:')]
        if status_labels != ['status:' + task['status']]:
            raise ValueError('Issue status labels disagree with task')
        if task['status'] == 'completed':
            completion = next(event for event in reversed(task['history'])
                              if event['action'] == 'complete')
            self.verify_merged(completion['merged_url'])
        return task
    def issues(self):
        result=[]; page=1
        while True:
            batch=self.api('repos/'+self.repo+'/issues?state=all&per_page=100&page='+str(page))
            if not isinstance(batch,list): raise ValueError('Invalid issue listing')
            result.extend(i for i in batch if self.official(i))
            if len(batch)<100: return result
            page+=1
    def tasks(self): return [self.parse(i) for i in self.issues()]
    def get_issue(self,number):
        issue=self.api('repos/'+self.repo+'/issues/'+str(number))
        if not self.official(issue): raise ValueError('Not an official owner-authored task')
        return issue
    def get_task(self,number): return self.parse(self.get_issue(number))
    def update(self,task,issue):
        labels=[l['name'] for l in issue['labels'] if not l['name'].startswith('status:')]
        labels.append('status:'+task['status'])
        self.api('repos/'+self.repo+'/issues/'+str(task['number']),'PATCH',{'body':body(task),'labels':labels})
    def verify_merged(self,url):
        parsed=urlparse(url)
        match=re.fullmatch('/'+re.escape(self.repo)+r'/pull/([1-9][0-9]*)',parsed.path)
        if parsed.scheme!='https' or parsed.netloc!='github.com' or not match: raise ValueError('Merged PR must belong to this repository')
        pr=self.api('repos/'+self.repo+'/pulls/'+match.group(1))
        if not pr.get('merged') or not pr.get('merged_at'): raise ValueError('PR has not been merged')
