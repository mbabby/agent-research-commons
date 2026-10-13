"""Recompute this bounded pilot from frozen inputs and attributed review; stdlib only."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ARMS = ['redo', 'report_only', 'locators', 'reproducible']

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(base, hashes):
    failed = [p for p, digest in hashes.items() if not (base / p).is_file() or sha(base / p) != digest]
    return {'ok': not failed, 'checked': len(hashes), 'failed': failed}

def elapsed(start, end):
    delta = (end['monotonic_ns'] - start['monotonic_ns']) / 1e9
    if delta < 0:
        raise ValueError('non-monotonic event interval')
    return delta

def ids_complete(rows, expected):
    return len(rows) == len(expected) and {r['id'] for r in rows} == set(expected)

def assessments(rows, errors, checked_errors):
    assessed = [r for r in rows if r.get('assessment') is not None]
    hits = [r['id'] for r in assessed if r['assessment'] == 'contradicted' and r['id'] in errors]
    false = [r['id'] for r in assessed if r['assessment'] == 'contradicted' and r['id'] not in errors]
    return {'true_positive_ids': hits, 'false_positive_ids': false,
            'unassessed': len(rows)-len(assessed),
            'report_error_denominator': len(errors), 'checked_error_denominator': len(checked_errors),
            'report_wide_detection_fraction': len(hits)/len(errors) if assessed else None,
            'checked_error_recall': len(hits)/len(checked_errors) if assessed and checked_errors else None,
            'note': 'Null redo assessment is not a failure; substantive correction belongs to semantic review. Unchecked report errors are unobserved, not checked false negatives.'}

def main():
    manifest = read(BASE/'manifest.json')
    integrity = {'frozen_materials': verify(BASE, manifest['files']),
                 'locked_runs': verify(BASE, read(BASE/'RUNS-LOCK.json')['files'])}
    if not all(v['ok'] for v in integrity.values()):
        raise ValueError(integrity)
    key = read(BASE/'hidden/answer-key.json')
    errors = {r['id'] for r in key if r['assessment']=='contradicted'}
    sources = read(BASE/'common/corpus.json')['sources']
    source_paths = {'common/'+s['path'] for s in sources}
    source_bytes = sum((BASE/p).stat().st_size for p in source_paths)
    disclosures = read(BASE/'performer-disclosures.json')
    grades_path = BASE/'review/semantic-grades.json'
    grades = read(grades_path) if grades_path.exists() else None
    timing = [json.loads(l) for l in (BASE/'author-timing.jsonl').read_text().splitlines()]
    phases = []
    for a,z in zip(timing,timing[1:]):
        phases.append({'phase':a.get('to',a.get('phase')), 'start':a['at'], 'end':z['at'],
                       'seconds':(datetime.datetime.fromisoformat(z['at'])-datetime.datetime.fromisoformat(a['at'])).total_seconds()})
    durations={p['phase']:p['seconds'] for p in phases}
    C=durations['instruction_setup']+durations['common_corpus_questions_candidate_hidden_labels']
    H=durations['protocol_prompts_common_measurement_QA']+durations['pre_run_corrections_and_freeze']
    R=durations['report_only_packaging'];L=durations['locators_packaging'];X=durations['reproducible_package_script_packaging']
    prep={'redo':0,'report_only':C+H+R,'locators':C+H+R+L,'reproducible':C+H+R+L+X}
    output={}
    for arm in ARMS:
        run=BASE/'runs'/arm
        events=[json.loads(l) for l in (run/'events.jsonl').read_text().splitlines()]
        assert all(a['monotonic_ns'] <= z['monotonic_ns'] for a,z in zip(events,events[1:]))
        start=next(e for e in events if e['event']=='start')
        sample=next(e for e in events if e['event']=='checkpoint')
        end=next(e for e in events if e['event']=='end')
        reads=[dict(e,relative_path=e['path'].split('/'+BASE.name+'/')[-1]) for e in events if e['event']=='file_read']
        for e in reads:
            assert sha(BASE/e['relative_path'])==e['sha256']
        sr=[e for e in reads if e['relative_path'] in source_paths]
        counts=collections.Counter(e['relative_path'] for e in sr)
        internal=2 if arm=='reproducible' else 0
        evidence={}
        for stage,event,expected in [('sample',sample,manifest['sample_ids']),('full',end,manifest['all_ids'])]:
            path=run/(stage+'.json'); rows=read(path)['answers']; assert sha(path)==event['sha256']
            assert ids_complete(rows,expected)
            quote_checks=[]
            for row in rows:
                assert set(row)=={'id','answer','evidence','uncertainty','assessment'}
                assert row['assessment'] in ([None,'supported','contradicted'] if arm=='redo' else ['supported','contradicted'])
                for item in row['evidence']:
                    lines=(BASE/'common'/item['path']).read_text().splitlines()
                    lo,hi=item['start_line'],item['end_line']
                    quote_checks.append(1<=lo<=hi<=len(lines) and bool(item['quote']) and item['quote'] in '\n'.join(lines[lo-1:hi]))
            semantic=None
            if grades is not None:
                entries=grades['arms'][arm][stage]
                assert set(entries)==set(expected)
                semantic={'answer_correct':sum(entries[i]['answer_correct'] for i in expected),
                          'evidence_correct':sum(entries[i]['evidence_correct'] for i in expected),
                          'joint_correct':sum(entries[i]['answer_correct'] and entries[i]['evidence_correct'] for i in expected),
                          'denominator':len(expected),'source':'review/semantic-grades.json'}
            evidence[stage]={'items':len(rows),'schema_complete':True,'all_quotes_lexically_match':all(quote_checks),
                             'semantic_review':semantic,'assessments':assessments(rows,errors,errors & set(expected))}
        full_seconds=elapsed(start,end)
        output[arm]={'start_utc':start['at'],'sample_utc':sample['at'],'end_utc':end['at'],
            'seconds':{'start_to_sample':elapsed(start,sample),'sample_to_full':elapsed(sample,end),'start_to_full':full_seconds},
            'outer_tool_calls_reported':disclosures['outer_tool_calls'][arm],
            'within_20_tools_reported':disclosures['outer_tool_calls'][arm]<=20,
            'within_720_seconds_observed':full_seconds<=720,
            'reads':{'all_helper_file_reads':len(reads),'all_helper_bytes':sum(e['bytes'] for e in reads),
                     'source_helper_reads':len(sr),'source_helper_bytes':sum(e['bytes'] for e in sr),
                     'per_source_helper_reads':dict(counts),'repeat_source_helper_reads':sum(max(0,n-1) for n in counts.values()),
                     'repeat_source_helper_bytes':sum(max(0,n-1)*(BASE/p).stat().st_size for p,n in counts.items()),
                     'script_internal_source_reads':internal,'script_internal_source_bytes':source_bytes if internal else 0,
                     'script_internal_other_reads':['common/corpus.json','arms/reproducible/locators.json'] if internal else [],
                     'script_internal_other_bytes':sum((BASE/p).stat().st_size for p in ['common/corpus.json','arms/reproducible/locators.json']) if internal else 0,
                     'note':'Internal script I/O reconstructed from inspected frozen code plus actual execution receipt, not per-read instrumented. Bytes are file I/O volumes, not tokens or cognition.'},
            'outputs':evidence,
            'cost_seconds':{'reader_only':full_seconds,'primary_conservative_total':full_seconds+prep[arm],
                            'sensitivity_including_explicit_wait':full_seconds+prep[arm]+(durations['pre_run_review_wait'] if arm!='redo' else 0),
                            'sensitivity_excluding_H':full_seconds+(prep[arm]-H if arm!='redo' else 0)}}
    receipt=read(BASE/'runs/reproducible/execution-receipt.json')
    assert receipt['exit_code']==0
    assert receipt['stdout_sha256']==sha(BASE/'runs/reproducible/execution.stdout')
    assert receipt['source_sha256']=={s['path']:s['sha256'] for s in sources}
    re=[json.loads(l) for l in (BASE/'runs/reproducible/events.jsonl').read_text().splitlines()]
    cmd_start=next(e for e in re if e['event']=='command_start');cmd_end=next(e for e in re if e['event']=='command_end')
    assert cmd_end['command']==receipt['command']==cmd_start['command']
    assert cmd_end['monotonic_ns']<next(e for e in re if e['event']=='checkpoint')['monotonic_ns']
    result={'status':'independent_semantic_review_available' if grades else 'semantic_review_pending',
       'integrity':integrity,'preregistration_url':read(BASE/'dispatch.json')['preregistration_url'],
       'arms':output,'execution':{'receipt':receipt,'seconds':elapsed(cmd_start,cmd_end),'before_sample':True,'stdout_bytes':(BASE/'runs/reproducible/execution.stdout').stat().st_size,
          'excerpt_text_bytes':sum(len(e['text'].encode()) for e in read(BASE/'runs/reproducible/execution.stdout')['excerpts'])},
       'preparation':{'phases':phases,'full_session_elapsed_seconds':sum(durations.values()),
          'explicit_review_wait_seconds':durations['pre_run_review_wait'],'C':C,'H':H,'R':R,'L':L,'X':X,
          'conservative_preparation_charges':prep,
          'interpretation':'Redo zero preparation charge means reader-only operational comparator, not zero experiment setup. C inseparably includes experimental questions/key and candidate authoring. H exclusion is sensitivity, not true net cost. Full elapsed includes explicit wait; waiting is separately visible and excluded only from per-format preparation allocation.'},
       'review_overhead':{'known_measured_intervals':[{'start':'2026-10-13T02:41:49Z','end':'2026-10-13T02:42:04Z','seconds':15},
          {'start':'2026-10-13T02:45:17Z','end':'2026-10-13T02:47:38Z','seconds':141},
          {'start':'2026-10-13T02:49:16Z','end':'2026-10-13T02:49:26Z','seconds':10},
          {'start':'2026-10-13T02:51:36Z','end':'2026-10-13T02:54:18Z','seconds':162}],
          'sources':['review/design-audit.md','review/results-audit.md'],'note':'Intervals overlap author/session wall time; do not sum as calendar duration. Closing prose, postrun review, coordinator administration and publication are separate, incompletely measured overhead.'},
       'semantic_review_provenance':{'path':'review/semantic-grades.json','sha256':sha(grades_path)} if grades else None,
       'telemetry':{'model_identifier':None,'input_tokens':None,'output_tokens':None,'billed_usd':None},
       'limitations':['One run per workflow, same operator, no randomization or causal/population claim.',
        'Sessions overlapped after fixed dispatch order; resource/concurrency effects are uncontrolled.',
        'Sample timing is four-output checkpoint; sources/extraction can expose all twelve beforehand.',
        'Read logs are cooperative, not OS tracing. Protocol deviation: promised transcript tool-count audit could not be completed; 7/8/5/8 are self-reported counts, not independently verified. Ledger events are not equivalent outer tool counts.',
        'Historical project/prior-study creation is unmeasured sunk input. Round 1 remains intact.',
        'Author analysis and independent semantic review occur after frozen preparation and are separate overhead.']}
    (BASE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'full_seconds':{a:output[a]['seconds']['start_to_full'] for a in ARMS}},indent=2))

if __name__=='__main__':
    main()
