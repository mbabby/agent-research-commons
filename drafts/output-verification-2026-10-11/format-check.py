"""Format-only baseline; does not read or judge source content or requirements."""
import json
import sys
import time
from pathlib import Path

def valid(case, sources):
    if set(case) != {'case_id', 'request', 'required_information', 'output'}:
        return False
    if not all(isinstance(case[k], str) and case[k] for k in ('case_id','request')):
        return False
    if not isinstance(case['required_information'], list) or not case['required_information'] or not all(isinstance(x,str) and x for x in case['required_information']):
        return False
    if not isinstance(case['output'],dict) or set(case['output']) != {'claims'}:
        return False
    claims=case['output']['claims']
    if not isinstance(claims,list) or not claims:
        return False
    ids=set()
    for claim in claims:
        if not isinstance(claim,dict) or set(claim) != {'id','text','citations'}:
            return False
        if not all(isinstance(claim[k],str) and claim[k] for k in ('id','text')) or claim['id'] in ids:
            return False
        ids.add(claim['id'])
        if not isinstance(claim['citations'],list) or not claim['citations']:
            return False
        for cite in claim['citations']:
            if not isinstance(cite,dict) or set(cite) != {'source_id','start_line','end_line'}:
                return False
            if cite['source_id'] not in sources:
                return False
            a,b=cite['start_line'],cite['end_line']
            if type(a) is not int or type(b) is not int or not 1 <= a <= b <= sources[cite['source_id']]['lines']:
                return False
    return True

if __name__ == '__main__':
    started=time.perf_counter()
    packet=Path(sys.argv[1]); data=json.loads((packet/'cases.json').read_text()); sources=json.loads((packet/'sources.json').read_text())['sources']
    assert data['schema_version']==1
    assert len({c['case_id'] for c in data['cases']})==len(data['cases'])
    rows=[{'case_id':c['case_id'],'verdict':'pass' if valid(c,sources) else 'flag','findings':[]} for c in data['cases']]
    print(json.dumps({'method':'format_only','elapsed_seconds':time.perf_counter()-started,'cases':rows},indent=2))
