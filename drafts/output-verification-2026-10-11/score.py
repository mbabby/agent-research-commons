"""Recompute preregistered case scores from hash-locked artifacts, stdlib only."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LOCKS={
 'SHA256SUMS':'3831fc244a2ee9045b9230ae0cd8ed32849fe77ed325094de804f74da51c9961',
 'results/format-only.json':'01801bb9567a2e186513aa2c96c397bba1a1bf9e9d776e5134557b7062bd168f',
 'results/source-check.json':'e6cc5c4bb91bb74d407c844487255e1e9c1e61a3492d40ae16b355dac60f49ff',
 'results/independent-review.json':'422889613089bc692cdc302c9cfeb0c94e2c3beea045bba2fbe5b8e5a0daba83',
}
def read(path): return json.loads((ROOT/path).read_text())
def ratio(n,d): return n/d if d else None

def score(gold, result):
    counts=dict(TP=0,FN=0,FP=0,TN=0,U_positive=0,U_negative=0)
    rows=[]; deviations=[]; predictions={}
    for p in result.get('cases',[]):
        cid=p.get('case_id')
        predictions.setdefault(cid,[]).append(p)
    if set(predictions)-set(gold): deviations.append('Unknown prediction IDs present')
    for cid,answer in gold.items():
        found=predictions.get(cid,[])
        verdict=found[0].get('verdict') if len(found)==1 else None
        if verdict not in ('flag','pass','uncertain'):
            deviations.append(f'{cid}: missing, duplicate or invalid verdict treated as unresolved')
            verdict='uncertain'
        pos=answer['defective']
        bucket=('TP' if pos else 'FP') if verdict=='flag' else ('FN' if pos else 'TN') if verdict=='pass' else ('U_positive' if pos else 'U_negative')
        counts[bucket]+=1
        rows.append({'case_id':cid,'gold_label':answer['label'],'verdict':verdict,'outcome':bucket,'expected_defect':answer['expected_defect'],'reference':answer['reference'],'findings':found[0].get('findings',[]) if len(found)==1 else []})
    c=counts
    return {'method':result['method'],'counts':c,'denominators':{'all':12,'positive':9,'negative':3,'per_defect_class':3},'rates':{'FPR':ratio(c['FP'],3),'FNR':ratio(c['FN'],9),'sensitivity':ratio(c['TP'],9),'specificity':ratio(c['TN'],3),'precision':ratio(c['TP'],c['TP']+c['FP']),'unresolved_or_missed':ratio(c['FN']+c['U_positive'],9),'coverage':ratio(12-c['U_positive']-c['U_negative'],12)},'per_class_detection':{label:{'TP':sum(r['gold_label']==label and r['outcome']=='TP' for r in rows),'denominator':3} for label in ('numeric','unsupported_citation','omission')},'protocol_deviations':deviations,'runtime':result.get('runtime',{'elapsed_seconds':result.get('elapsed_seconds')}),'cases':rows}

def main():
    for path,expected in LOCKS.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected: raise ValueError('Locked hash mismatch: '+path)
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,path=line.split('  ',1)
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected: raise ValueError('Design hash mismatch: '+path)
    key={a['case_id']:a for a in read('sealed/answer-key.json')['cases']}
    order=[c['case_id'] for c in read('packet/cases.json')['cases']]
    gold={cid:key[cid] for cid in order}
    assert len(gold)==12 and sum(a['defective'] for a in gold.values())==9
    assert all(sum(a['label']==label for a in gold.values())==3 for label in ('numeric','unsupported_citation','omission','clean'))
    results=[score(gold,read(path)) for path in LOCKS if path.startswith('results/')]
    output={'scope':'Descriptive scores for these 12 synthetic cases only; null precision means N/A. Supported-hit diagnosis is a separate independent audit.','locks':LOCKS,'conditions':results}
    (ROOT/'results/scores.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    lines=['# Full case results','','Pass/flag are predictions, not official acceptance. Expected defect and source locator were fixed before runs.','','| Case | Gold class | Format | Claim-by-claim | Independent review | Fixed defect/reference |','|---|---|---|---|---|---|']
    for i,cid in enumerate(order):
        a=gold[cid]; values=[x['cases'][i]['verdict'] for x in results]
        desc=(a['expected_defect'] or 'Clean control')+' ('+a['reference']+')'
        lines.append('| '+' | '.join([cid,a['label']]+values+[desc.replace('|','\\|')])+' |')
    lines += ['','Full unmodified findings and runtime records: [source check](source-check.json), [independent review](independent-review.json), [format](format-only.json). [Machine-readable scores](scores.json) preserve each finding and outcome.']
    (ROOT/'results/case-table.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({r['method']:{'counts':r['counts'],'rates':r['rates'],'protocol_deviations':r['protocol_deviations']} for r in results},indent=2))
if __name__=='__main__': main()
