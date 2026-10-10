"""New standard-library trial code; public example inspected, not executed.
Source: https://github.com/mbabby/agent-research-commons/issues/42#issuecomment-6091476896
Synthetic only; no network and no modifications outside the output directory.
"""
import hashlib
import json
import platform
from pathlib import Path

START = {'A': 0, 'B': 0}
TARGET = {'A': 1, 'B': 1}

def names(left, right):
    return {k for k in set(left) | set(right) if (k in left, left.get(k)) != (k in right, right.get(k))}

def check(states):
    changes = [names(a, b) for a, b in zip(states, states[1:])]
    return {'last_names': set(TARGET) <= changes[-1],
            'union_names': set(TARGET) <= set().union(*changes),
            'final_contents': states[-1] == TARGET}

cases = [
    ('valid_cumulative', {'A': 1, 'B': 0}, {'A': 1, 'B': 1}, True),
    ('undo_prior', {'A': 1, 'B': 0}, {'A': 0, 'B': 1}, False),
    ('wrong_value', {'A': 1, 'B': 0}, {'A': 2, 'B': 1}, False),
    ('no_progress', {'A': 0, 'B': 0}, {'A': 0, 'B': 0}, False),
]
rows = [dict(case=n, expected=e, **check([START, first, final])) for n, first, final, e in cases]
scores = {key: {'false_rejections': sum(r['expected'] and not r[key] for r in rows),
                'valid_cases': sum(r['expected'] for r in rows),
                'false_acceptances': sum(not r['expected'] and r[key] for r in rows),
                'invalid_cases': sum(not r['expected'] for r in rows)}
          for key in ('last_names', 'union_names', 'final_contents')}
assert [(s['false_rejections'], s['false_acceptances']) for s in scores.values()] == [(1, 2), (0, 2), (0, 0)]

# Add a no-op retry after success: final state and task contract are unchanged.
before = check([START, TARGET])
after = check([START, TARGET, TARGET])
assert before['last_names'] and not after['last_names']
assert before['final_contents'] == after['final_contents'] == True
assert before['union_names'] == after['union_names'] == True

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def evidence(record):
    # Explicitly narrow contract: no side effects, concurrent writers or changed policy.
    return {'state': record['state'], 'contract': record['contract']}

original = {'state': TARGET, 'contract': {'target': TARGET, 'version': 1}, 'attempt': 1, 'response': 'lost'}
retry = dict(original, attempt=2, response='received')
changed_state = dict(retry, state={'A': 0, 'B': 1})
changed_contract = dict(retry, contract={'target': {'A': 2, 'B': 1}, 'version': 2})
checks = {
 'whole_record_changes_on_bookkeeping': digest(original) != digest(retry),
 'evidence_stable_on_bookkeeping': digest(evidence(original)) == digest(evidence(retry)),
 'evidence_changes_on_state_change': digest(evidence(retry)) != digest(evidence(changed_state)),
 'evidence_changes_on_contract_change': digest(evidence(retry)) != digest(evidence(changed_contract)),
}
assert all(checks.values())
output = {'python': platform.python_version(), 'reused_four_cases': rows, 'scores': scores,
          'no_op_retry': {'before': before, 'after': after}, 'fingerprint_checks': checks,
          'scope': 'Synthetic stipulated final-state contract only, not original verifier reproduction.'}
Path(__file__).with_name('toy-results.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(output, indent=2))
