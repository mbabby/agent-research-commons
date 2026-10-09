"""Run with python3 -m arc.cli."""
import argparse
import json
import os
import sys
from .github import GitHub, body
from .model import now, transition, validate_task

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',default='mbabby/agent-research-commons'); p.add_argument('--owner',help='Allowed official issue author login')
    commands=p.add_subparsers(dest='command',required=True)
    commands.add_parser('list')
    show=commands.add_parser('show'); show.add_argument('number',type=int)
    create=commands.add_parser('create'); create.add_argument('--file',required=True); create.add_argument('--operation-id',required=True)
    sync=commands.add_parser('sync'); sync.add_argument('--output',required=True)
    for name in ('assign','start','submit','review','complete','block','release','cancel'):
        sub=commands.add_parser(name); sub.add_argument('number',type=int); sub.add_argument('--actor',required=True); sub.add_argument('--operation-id',required=True); sub.add_argument('--attempt',required=True,type=int)
        if name=='assign': sub.add_argument('--agent',required=True)
        if name=='submit': sub.add_argument('--artifact-url',required=True)
        if name=='review': sub.add_argument('--verdict',choices=['pass','changes_requested'],required=True); sub.add_argument('--notes',required=True)
        if name=='complete': sub.add_argument('--merged-url',required=True); sub.add_argument('--review-operation-id',required=True)
    return p

def run(args):
    github=GitHub(args.repo,args.owner); command=args.command
    if command=='list': return github.tasks()
    if command=='show': return github.get_task(args.number)
    if command=='sync':
        snapshot=dict(generated_at=now(),repository=args.repo,tasks=github.tasks())
        temporary=args.output+'.tmp'
        with open(temporary,'w',encoding='utf-8') as out: json.dump(snapshot,out,ensure_ascii=False,indent=2); out.write('\n')
        os.replace(temporary,args.output); return snapshot
    if command=='create':
        with open(args.file,encoding='utf-8') as source: task=json.load(source)
        validate_task(task)
        if task['status']!='open' or task['attempt']!=0 or task['agent_id'] is not None or task['history']: raise ValueError('New task must be open with empty history')
        for existing in github.tasks():
            for event in existing['history']:
                if event['operation_id']==args.operation_id:
                    if event['action']!='create': raise ValueError('Operation ID conflict')
                    for key in ('title','question','scope','exclusions','as_of','deliverable','acceptance','parent','coordinator'):
                        if existing[key]!=task[key]: raise ValueError('Create operation ID conflict')
                    return existing
        user=github.api('user')
        if user.get('login')!=github.owner: raise ValueError('Creation requires configured official issue author')
        task['number']=0
        task['updated_at']=now(); task['history']=[dict(action='create',actor=task['coordinator'],operation_id=args.operation_id,at=task['updated_at'],attempt=0)]
        issue=github.api('repos/'+args.repo+'/issues','POST',dict(title=task['title'],body=body(task),labels=['arc:task','status:open']))
        task['number']=issue['number']; github.update(task,issue); return task
    issue=github.get_issue(args.number); task=github.parse(issue)
    fields={'attempt':args.attempt}
    for key in ('artifact_url','verdict','notes','merged_url','review_operation_id'):
        if hasattr(args,key): fields[key]=getattr(args,key)
    if command=='assign': fields['agent_id']=args.agent
    updated=transition(task,command,args.actor,args.operation_id,**fields)
    if command=='complete': github.verify_merged(args.merged_url)
    if updated!=task: github.update(updated,issue)
    return updated

def main(argv=None):
    args=parser().parse_args(argv)
    try: print(json.dumps(run(args),ensure_ascii=False,indent=2)); return 0
    except (ValueError,OSError,KeyError,TypeError) as error:
        print('arc: '+str(error),file=sys.stderr); return 1
if __name__=='__main__': sys.exit(main())
