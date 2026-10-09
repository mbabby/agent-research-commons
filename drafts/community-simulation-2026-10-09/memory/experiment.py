"""Deterministic information-preservation fixture; no model or network calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def apply_events(events):
    current, sources, reasons = {}, {}, {}
    for event in events:
        for key, value in event['set'].items():
            current[key] = value
            sources[key] = event['id']
            reasons[key] = event['reason']
    return current, sources, reasons


def representations(fixture):
    events = [event for session in fixture['sessions'] for event in session['events']]
    current, sources, _ = apply_events(events)
    # The summary rule overwrites values after every session, deliberately dropping history.
    summary = {}
    for session in fixture['sessions']:
        for event in session['events']:
            summary.update(event['set'])
    return {
        'transcript_replay': {'events': events},
        'current_state_plus_history': {'current': current, 'sources': sources, 'events': events},
        'rolling_summary_values_only': {'current': summary},
    }


def recover(name, context):
    if name == 'transcript_replay':
        return apply_events(context['events'])
    current = context['current']
    sources = context.get('sources', {})
    history = {event['id']: event for event in context.get('events', [])}
    reasons = {key: history[source]['reason'] for key, source in sources.items()}
    return current, sources, reasons


def run(fixture):
    oracle = fixture['oracle']  # Used only for scoring, never passed to recovery.
    treatments = []
    for name, context in representations(fixture).items():
        current, sources, reasons = recover(name, context)
        decisions = [{
            'vendor': vendor['id'],
            'eligible': vendor['price'] <= current['max_price'] and vendor['region'] == current['region'],
            'price_pass': vendor['price'] <= current['max_price'],
            'region_pass': vendor['region'] == current['region'],
        } for vendor in fixture['vendors']]
        eligible = [row['vendor'] for row in decisions if row['eligible']]
        treatments.append({
            'name': name, 'context': context,
            'answer': {'current': current, 'sources': sources, 'reasons': reasons, 'decisions': decisions},
            'scores': {
                'current_constraints_correct': sum(current.get(k) == v for k, v in oracle['current'].items()),
                'current_constraints_total': len(oracle['current']),
                'stale_constraints_used': sum(current.get(k) in values for k, values in oracle['stale_values'].items()),
                'attributions_correct': sum(sources.get(k) == v for k, v in oracle['sources'].items()),
                'reasons_correct': sum(reasons.get(k) == v for k, v in oracle['reasons'].items()),
                'eligible_set_exact': eligible == oracle['eligible'],
            },
        })
    return {'kind': 'deterministic synthetic information-preservation check', 'model': None,
            'token_measurement': None, 'cost_measurement': None, 'treatments': treatments}


if __name__ == '__main__':
    fixture = json.loads((ROOT / 'fixture.json').read_text())
    result = run(fixture)
    # Sanity checks validate fixture execution, not independent scientific review.
    assert len(fixture['sessions']) == 3 and len(fixture['vendors']) == 5
    assert [len(s['events']) for s in fixture['sessions']] == [1, 1, 1]
    assert all(t['scores']['eligible_set_exact'] for t in result['treatments'])
    assert [t['scores']['attributions_correct'] for t in result['treatments']] == [2, 2, 0]
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    for treatment in result['treatments']:
        print(treatment['name'], json.dumps(treatment['scores'], sort_keys=True))
