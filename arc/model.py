"""Validated task state transitions and publication evidence."""
import copy
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

STATUSES = {'open','assigned','in_progress','in_review','changes_requested','completed','blocked','cancelled'}
TASK_FIELDS = {'number','title','question','scope','exclusions','as_of','deliverable','acceptance','parent','status','agent_id','coordinator','attempt','updated_at','history'}
def now():
    return datetime.now(timezone.utc).isoformat()
def require(condition, message):
    if not condition: raise ValueError(message)
def link(value, https=False):
    p=urlparse(value if isinstance(value,str) else '')
    require(p.scheme in ({'https'} if https else {'http','https'}) and bool(p.hostname) and not p.username, 'Invalid evidence URL')
def validate_task(task, _replay=True):
    require(isinstance(task,dict) and TASK_FIELDS <= task.keys(), 'Missing task fields')
    require(task['status'] in STATUSES,'Invalid status')
    require(task['history'] or task['status']=='open' and task['attempt']==0 and task['agent_id'] is None,'State requires history')
    require(type(task['number']) is int and task['number'] >= 0,'Invalid number')
    require(type(task['attempt']) is int and task['attempt'] >= 0,'Invalid attempt')
    require(task['parent'] is None or type(task['parent']) is int,'Invalid parent')
    for key in ('title','question','scope','as_of','deliverable','coordinator','updated_at'):
        require(isinstance(task[key],str) and task[key].strip(),'Invalid '+key)
    require(task['agent_id'] is None or isinstance(task['agent_id'],str) and bool(task['agent_id']),'Invalid agent')
    require(isinstance(task['exclusions'],list) and isinstance(task['acceptance'],list),'Invalid scope criteria')
    require(isinstance(task['history'],list),'Invalid history')
    seen=set()
    for event in task['history']:
        require(isinstance(event,dict) and {'action','actor','operation_id','at','attempt'} <= event.keys(),'Invalid event')
        require(event['operation_id'] not in seen,'Duplicate operation')
        seen.add(event['operation_id'])
        require(type(event['attempt']) is int and 0 <= event['attempt'] <= task['attempt'],'Invalid event attempt')
        for key in ('action','actor','operation_id','at'): require(isinstance(event[key],str) and event[key],'Invalid event '+key)
        for key in ('artifact_url','merged_url'):
            if key in event: link(event[key],True)
    if _replay and task['history']:
        initial=copy.deepcopy(task)
        initial.update(status='open',agent_id=None,attempt=0,history=[])
        for event in task['history']:
            if event['action']=='create':
                require(not initial['history'] and event['actor']==task['coordinator'] and event['attempt']==0,'Invalid creation event')
                initial['history'].append(copy.deepcopy(event)); continue
            fields={k:v for k,v in event.items() if k not in {'action','actor','operation_id','at','attempt'}}
            fields['attempt']=initial['attempt']
            initial=transition(initial,event['action'],event['actor'],event['operation_id'],**fields)
            require(initial['attempt']==event['attempt'],'History attempt mismatch')
            initial['history'][-1]=copy.deepcopy(event)
        require(all(initial[k]==task[k] for k in ('status','agent_id','attempt')),'Task state disagrees with history')

def transition(task, action, actor, operation_id, **fields):
    validate_task(task, _replay=False)
    require(isinstance(actor,str) and bool(actor) and isinstance(operation_id,str) and bool(operation_id),'Actor and operation ID required')
    for event in task['history']:
        if event['operation_id']==operation_id:
            require(event['action']==action and event['actor']==actor and all(event.get(k)==v for k,v in fields.items() if k!='attempt') and ('attempt' not in fields or fields['attempt']==event['attempt'] or action=='assign' and fields['attempt']==event['attempt']-1),'Operation ID conflict')
            return copy.deepcopy(task)
    require(action in {'assign','start','submit','review','complete','block','release','cancel'},'Invalid action')
    require(fields.get('attempt',task['attempt'])==task['attempt'],'Stale attempt')
    t=copy.deepcopy(task); status=t['status']; coordinator=actor==t['coordinator']; researcher=actor==t['agent_id']
    if action=='assign':
        require(coordinator and status=='open','Assignment requires coordinator and open task')
        require(isinstance(fields.get('agent_id'),str) and fields['agent_id'],'Agent required')
        t['agent_id']=fields['agent_id']; t['attempt']+=1; t['status']='assigned'
    elif action=='start':
        require(researcher and status=='assigned','Start requires assigned researcher'); t['status']='in_progress'
    elif action=='submit':
        require(researcher and status in {'in_progress','changes_requested'},'Submission requires active researcher')
        link(fields.get('artifact_url'),True); t['status']='in_review'
    elif action=='review':
        require(not researcher and status=='in_review','Independent review required')
        require(fields.get('verdict') in {'pass','changes_requested'} and isinstance(fields.get('notes'),str) and fields['notes'].strip(),'Review verdict and notes required')
        t['status']='in_review' if fields['verdict']=='pass' else 'changes_requested'
    elif action=='complete':
        require(coordinator and status=='in_review','Completion requires coordinator and passed review')
        link(fields.get('merged_url'),True)
        reviews=[e for e in t['history'] if e['action']=='review' and e['attempt']==t['attempt']]
        require(reviews and reviews[-1].get('verdict')=='pass' and reviews[-1]['operation_id']==fields.get('review_operation_id'),'Passing review reference required'); t['status']='completed'
    elif action=='release':
        require((coordinator or researcher) and status not in {'open','completed','cancelled'},'Release unauthorized')
        t['status']='open'; t['agent_id']=None
    elif action=='block':
        require((coordinator or researcher) and status in {'assigned','in_progress','changes_requested'},'Block unauthorized'); t['status']='blocked'
    elif action=='cancel':
        require(coordinator and status not in {'completed','cancelled'},'Cancel unauthorized'); t['status']='cancelled'
    t['updated_at']=now()
    event=dict(fields,action=action,actor=actor,operation_id=operation_id,at=t['updated_at'],attempt=t['attempt'])
    t['history'].append(event); validate_task(t, _replay=False); return t

def validate_report(report, tasks):
    required={'slug','title','summary','task_number','agent_id','attempt','as_of','published_at','claims','sources','unknowns','method','limitations','review','acceptance_url','revision'}
    require(isinstance(report,dict) and required <= report.keys(),'Missing report fields')
    require(isinstance(report['slug'],str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',report['slug']),'Unsafe slug')
    for key in ('title','summary','agent_id','as_of','published_at','method'): require(isinstance(report[key],str) and report[key].strip(),'Invalid report '+key)
    for key in ('unknowns','limitations'): require(isinstance(report[key],list) and all(isinstance(x,str) for x in report[key]),'Invalid '+key)
    require(type(report['revision']) is int and report['revision'] > 0,'Invalid revision')
    matches=[t for t in tasks if t['number']==report['task_number']]; require(len(matches)==1,'Unknown task')
    task=matches[0]; validate_task(task)
    require(task['status']=='completed' and task['agent_id']==report['agent_id'] and task['attempt']==report['attempt'],'Report task mismatch')
    reviews=[e for e in task['history'] if e['action']=='review' and e['attempt']==task['attempt'] and e.get('verdict')=='pass']
    review=report['review']; require(isinstance(review,dict) and {'agent_id','notes','review_url'}<=review.keys() and reviews and review['agent_id']==reviews[-1]['actor'],'Review mismatch')
    completions=[e for e in task['history'] if e['action']=='complete']; require(completions,'Missing completion')
    merged=urlparse(completions[-1]['merged_url']); repository='/'.join(merged.path.split('/')[:3])
    for value in (review['review_url'],report['acceptance_url']):
        link(value); p=urlparse(value)
        require(p.hostname=='github.com' and re.fullmatch(re.escape(repository)+r'/(issues|pull)/[1-9][0-9]*',p.path),'Unrelated review or acceptance record')
    require(isinstance(report['sources'],list) and isinstance(report['claims'],list),'Invalid evidence arrays')
    sources={}; claims={}
    for source in report['sources']:
        require(isinstance(source,dict) and {'id','title','url','accessed_at','published_at','supports','note'} <= source.keys(),'Invalid source')
        require(isinstance(source['id'],str) and source['id'] and source['id'] not in sources,'Duplicate source'); link(source['url']); sources[source['id']]=source
        require(isinstance(source['supports'],list),'Invalid source support')
    for claim in report['claims']:
        require(isinstance(claim,dict) and {'id','kind','text','source_ids'} <= claim.keys(),'Invalid claim')
        require(isinstance(claim['id'],str) and claim['id'] and claim['id'] not in claims,'Duplicate claim')
        require(claim['kind'] in {'fact','inference'} and isinstance(claim['text'],str) and claim['text'].strip(),'Invalid claim kind/text')
        require(isinstance(claim['source_ids'],list) and all(s in sources for s in claim['source_ids']),'Unknown source')
        require(claim['kind']!='fact' or bool(claim['source_ids']),'Fact lacks source'); claims[claim['id']]=claim
    for source in sources.values(): require(all(c in claims for c in source['supports']),'Unknown supported claim')
