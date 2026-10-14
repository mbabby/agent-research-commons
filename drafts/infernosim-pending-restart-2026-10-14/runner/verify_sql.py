#!/usr/bin/env python3
"""Runner cross-review: read-only SQL, exported snapshots, and event ordering."""
import json
from pathlib import Path
import sqlite3
import sys

def verify(root):
    output = []
    for case in sorted(root.iterdir()):
        if not (case/'provider.sqlite').exists():
            continue
        with sqlite3.connect('file:'+str(case/'provider.sqlite')+'?mode=ro', uri=True) as con:
            assert con.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
            raw = {t: [list(row) for row in con.execute('SELECT * FROM '+t)]
                   for t in ('operations','effects','events')}
        assert raw == json.loads((case/'after-drain.json').read_text())
        before = json.loads((case/'before-drain.json').read_text())
        cp = json.loads((case/'checkpoint-copy.json').read_text())
        dec = json.loads((case/'decision.json').read_text())
        first = json.loads((case/'first-client.json').read_text())
        result = json.loads((case/'reports/infernosim-agent-results.json').read_text())[0]
        assert result['process']['restarted'] and first['pid'] != dec['pid']
        assert cp == first['operation'] and cp['status'] == 'pending'
        assert (cp['id'], cp['business_key'], cp['idem_key']) == tuple(raw['operations'][0][:3])
        assert dec['retained_handle'] == cp['id']
        events = [(seq,kind,json.loads(detail)) for seq,kind,detail in raw['events']]
        reads = [(seq,e) for seq,kind,e in events if kind == 'status_read']
        commits = [(seq,e) for seq,kind,e in events if kind == 'effect_committed']
        stop = next(seq for seq,kind,e in events if kind == 'client_runner_stopped')
        assert reads[0][1]['id'] == cp['id'] and reads[0][1]['actual_status'] == 'pending'
        assert all(o[3]=='completed' for o in raw['operations'])
        assert sorted(e[0] for e in raw['effects']) == sorted(o[0] for o in raw['operations'])
        reconcile = case.name in ('safe-reconcile', 'safe-mismatched-receipt')
        if not reconcile:
            assert not before['effects'] and all(o[3]=='pending' for o in before['operations'])
            assert all(seq>stop for seq,e in commits)
        else:
            assert reads[0][0]<commits[0][0]<reads[1][0]<stop
            assert len(before['effects']) == 1
        expected = 2 if case.name=='unsafe-pending' else 1
        assert len(raw['effects']) == expected
        assert dec['outcome'] == ('completed' if case.name=='safe-reconcile' else 'unknown')
        output.append({'case':case.name, 'sqlite_integrity':'ok','snapshot_equals_sql':True,
                       'effect_count':len(raw['effects']), 'effects_before_stop':sum(seq<stop for seq,e in commits),
                       'effects_after_stop':sum(seq>stop for seq,e in commits),
                       'initial_pending':True,'identity_preserved':True, 'raw_infernosim_pass':result['passed'],
                       'no_duplicate_business_effect':len(raw['effects'])==1})
    assert len(output)==6
    return output

if __name__=='__main__':
    print(json.dumps(verify(Path(sys.argv[1]).resolve()),indent=2))
