#!/usr/bin/env python3
"""Read captured artifacts and query the provider DB; no fixture imports."""
import argparse
import json
from pathlib import Path
import sqlite3


def check(root):
    case = root.name
    results = json.loads((root/'reports/infernosim-agent-results.json').read_text())
    assert len(results) == 1
    report = results[0]
    assert report['passed'] and not report.get('invalid_run', False)
    assert report['process']['restarted'] and report['process']['exit_code'] == 0 and not report['process']['timed_out']
    assert report['restart_after_call'] == 1
    assert report['simulator']['expected'] == report['simulator']['observed'] == 1
    assert report['simulator']['agent']['calls'][0]['tool'] == 'checkpoint_barrier'
    first = json.loads((root / 'first-client.json').read_text())
    cp = json.loads((root / 'checkpoint-copy.json').read_text())
    dec = json.loads((root / 'decision.json').read_text())
    with sqlite3.connect('file:' + str(root / 'provider.sqlite') + '?mode=ro', uri=True) as con:
        ops = con.execute('SELECT id,business_key,idem_key,status FROM operations ORDER BY id').fetchall()
        effects = con.execute('SELECT operation_id,business_key FROM effects ORDER BY operation_id').fetchall()
        events = [(seq, kind, json.loads(detail)) for seq, kind, detail in con.execute('SELECT seq,kind,detail FROM events ORDER BY seq')]
    assert first['pid'] != dec['pid'], 'not distinct client PIDs'
    assert first['operation'] == cp, 'checkpoint copy inconsistent'
    assert cp['id'] == dec['retained_handle'] == ops[0][0], 'original identity lost'
    assert (cp['business_key'], cp['idem_key']) == ops[0][1:3], 'receipt identity does not match provider row'
    reads = [e for e in events if e[1] == 'status_read']
    assert reads and reads[0][2]['id'] == cp['id'] and reads[0][2]['actual_status'] == 'pending'
    assert dec['first_observation'] == reads[0][2]['response']
    assert dec['first_status_code'] == reads[0][2]['response_code']
    submits = [e for e in events if e[1] == 'submit']
    assert len(submits) == len(ops), 'unexpected duplicate POST or missing admission'
    assert all(o[3] == 'completed' for o in ops), 'future effects still pending'
    assert sorted(e[0] for e in effects) == sorted(o[0] for o in ops), 'drain incomplete'
    assert {o[1] for o in ops} == {'payment-1'}
    unsafe = case == 'unsafe-pending'
    assert len(ops) == len(effects) == (2 if unsafe else 1)
    assert dec['submitted_new'] is unsafe
    if unsafe:
        assert len({o[2] for o in ops}) == 2, 'replacement retained old identity'
        assert dec['replacement'] != cp['id']
    assert dec['outcome'] == ('completed' if case == 'safe-reconcile' else 'unknown')
    assert reads[0][2]['response_code'] == {'safe-read-failed':503, 'safe-ambiguous-absence':404}.get(case, 200)
    if case in ('safe-reconcile', 'safe-mismatched-receipt'):
        assert len(reads) == 2 and reads[1][2]['actual_status'] == 'completed'
        assert dec['terminal_observation'] == reads[1][2]['response']
        matched = all(dec['terminal_observation'].get(k) == cp[k] for k in ('id','business_key','idem_key'))
        assert matched == dec['receipt_matched'] == (case == 'safe-reconcile')
    else:
        stopped = next(e[0] for e in events if e[1] == 'client_runner_stopped')
        assert all(e[0] > stopped for e in events if e[1] == 'effect_committed'), 'effect committed before selected drain'
    return {'case':case,'first_pid':first['pid'],'resumed_pid':dec['pid'],'retained_handle':cp['id'], 'outcome':dec['outcome'], 'operations':len(ops), 'final_effects':len(effects), 'checks':'pass'}

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('root',type=Path); a=p.parse_args()
    results=[check(d) for d in sorted(a.root.iterdir()) if (d/'provider.sqlite').exists()]
    assert {r['case'] for r in results} == {'safe-pending','unsafe-pending','safe-read-failed','safe-ambiguous-absence','safe-reconcile','safe-mismatched-receipt'}, 'missing/extra case evidence'
    print(json.dumps(results,indent=2))
