"""Synthetic accounting only. Python 3.9+, no network or dependencies."""
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ('energy_kwh', 'api_cost', 'occupied_hours', 'review_hours', 'repair_hours', 'maintenance_hours')

def load():
    return json.loads((ROOT / 'synthetic-ledger.json').read_text())

def compare(data, accounting='marginal', utilization=.5, electricity=.2, human_rate=0):
    if accounting not in ('marginal', 'amortized'):
        raise ValueError('unknown accounting basis')
    if not 0 < utilization <= 1:
        raise ValueError('utilization must be in (0,1]')
    for value in (electricity, human_rate):
        if value is not None and (not math.isfinite(value) or value < 0):
            raise ValueError('rates must be finite and nonnegative or null')
    modes, signatures = [], []
    for mode in data['modes']:
        sums = {}
        for field in FIELDS:
            values = [row[field] for row in mode['attempts']]
            if any(v is not None and (not math.isfinite(v) or v < 0) for v in values):
                raise ValueError('resources must be finite and nonnegative or null')
            sums[field] = None if None in values else sum(values)
        accepted_ids = sorted({r['task'] for r in mode['attempts'] if r['accepted']})
        signatures.append((mode['rubric'], sorted({r['task'] for r in mode['attempts']}), accepted_ids))
        energy = None if sums['energy_kwh'] is None or electricity is None else sums['energy_kwh'] * electricity
        hours = [sums[f] for f in ('review_hours', 'repair_hours', 'maintenance_hours')]
        human = None if None in hours or human_rate is None else sum(hours) * human_rate
        hardware = 0 if accounting == 'marginal' else (
            None if sums['occupied_hours'] is None else 1200 / (3 * 2000 * utilization) * sums['occupied_hours'])
        parts = {'electricity': energy, 'api': sums['api_cost'], 'human': human, 'hardware': hardware}
        total = None if None in parts.values() else sum(parts.values())
        modes.append({'mode': mode['name'], 'attempts': len(mode['attempts']), 'accepted': len(accepted_ids),
                      'parts': parts, 'total': total,
                      'per_accepted': total / len(accepted_ids) if total is not None and accepted_ids else None})
    comparable = bool(signatures) and all(s == signatures[0] for s in signatures)
    ranking = None
    if comparable and all(m['per_accepted'] is not None for m in modes):
        ranking = [m['mode'] for m in sorted(modes, key=lambda m: m['per_accepted'])]
    return {'synthetic': True, 'accounting': accounting, 'utilization': utilization,
            'electricity_per_kwh': electricity, 'human_hourly_rate': human_rate,
            'comparable': comparable, 'comparison_basis': 'assumed identical rubric, workload and accepted task IDs',
            'ranking': ranking, 'modes': modes}

if __name__ == '__main__':
    results = [compare(load(), basis, u, e, h) for basis, u, e, h in itertools.product(
        ('marginal', 'amortized'), (.1, .5, 1), (.1, .2, .5), (0, 20, 60))]
    print(json.dumps({'status': 'synthetic arithmetic; not observed savings', 'scenarios': results}, indent=2))
