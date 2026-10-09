#!/usr/bin/env python3
"""Deterministic synthetic approval race; Python stdlib, no network or money."""
import json
from pathlib import Path

DESIGNS = ('approval_only', 'reread_before_write', 'source_conditional_write')
SCHEDULES = ('unchanged', 'before_approval', 'after_approval', 'after_read_before_write')


def run(design, schedule):
    state = {'version': 1, 'disputed': False, 'executed': False}
    trace = []

    def event(name, **details):
        trace.append({'step': len(trace) + 1, 'event': name,
                      'source': dict(state), **details})

    def dispute():
        state['disputed'] = True
        state['version'] += 1
        event('external_dispute')

    captured = dict(state)
    event('capture_for_approval', captured_version=captured['version'])
    if schedule == 'before_approval':
        dispute()
    approved = not captured['disputed'] and not captured['executed']
    event('approve_captured_snapshot', approved=approved,
          approved_version=captured['version'])
    if schedule == 'after_approval':
        dispute()
    last_read = dict(state) if design != 'approval_only' else captured
    event('final_read' if design != 'approval_only' else 'reuse_captured_snapshot',
          observed_version=last_read['version'])
    if schedule == 'after_read_before_write':
        dispute()
    client_allows = approved and (design == 'approval_only' or (
        last_read['version'] == captured['version'] and
        not last_read['disputed'] and not last_read['executed']))
    event('client_decision', allow=client_allows)
    # Oracle observes truth immediately before write/skip, never authorizes it.
    valid = (approved and state['version'] == captured['version'] and
             not state['disputed'] and not state['executed'])
    committed = False
    if client_allows:
        # The check and mutation below are ONE source transaction: no scheduler
        # yield or external event can occur between them in this mock.
        source_allows = design != 'source_conditional_write' or (
            state['version'] == captured['version'] and
            not state['disputed'] and not state['executed'])
        if source_allows:
            state['executed'] = True
            state['version'] += 1
            committed = True
        event('source_commit' if committed else 'source_reject',
              expected_version=captured['version'], valid_at_boundary=valid,
              atomic_conditional=(design == 'source_conditional_write'))
    else:
        event('client_skip', valid_at_boundary=valid)
    outcome = ('valid_commit' if valid else 'invalid_commit') if committed else (
        'valid_incorrectly_blocked' if valid else 'invalid_blocked')
    return {'design': design, 'schedule': schedule, 'outcome': outcome,
            'committed': committed, 'valid_at_boundary': valid, 'trace': trace}


def main():
    cases = [run(d, s) for d in DESIGNS for s in SCHEDULES]
    # Declared analytical expectations, checked against actual transitions.
    expected_invalid = {'approval_only': 3, 'reread_before_write': 1,
                        'source_conditional_write': 0}
    counts = {}
    for design in DESIGNS:
        subset = [c for c in cases if c['design'] == design]
        counts[design] = {outcome: sum(c['outcome'] == outcome for c in subset)
                          for outcome in ('valid_commit', 'invalid_commit',
                                          'invalid_blocked', 'valid_incorrectly_blocked')}
        assert counts[design]['invalid_commit'] == expected_invalid[design]
        assert counts[design]['valid_commit'] == 1
        assert counts[design]['valid_incorrectly_blocked'] == 0
        assert subset[0]['schedule'] == 'unchanged' and subset[0]['committed']
    results = {'status': 'unreviewed_simulation_draft', 'logical_session': 'sim-approval',
               'case_count': len(cases), 'counts': counts, 'cases': cases}
    output = Path(__file__).with_name('results.json')
    output.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'case_count': len(cases), 'counts': counts}, indent=2))


if __name__ == '__main__':
    main()
