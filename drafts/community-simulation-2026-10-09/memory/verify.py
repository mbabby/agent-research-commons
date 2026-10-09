"""Regression verification for correction v2; standard library only."""
import copy
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from experiment import run

root = Path(__file__).resolve().parent
fixture = json.loads((root / 'fixture.json').read_text())
saved = (root / 'results.json').read_bytes()
baseline = run(fixture)
assert (json.dumps(baseline, indent=2) + '\n').encode() == saved
# All 120 vendor permutations must retain exact eligible-set success.
for vendors in itertools.permutations(fixture['vendors']):
    probe = copy.deepcopy(fixture)
    probe['vendors'] = list(vendors)
    result = run(probe)
    assert all(t['scores'] == b['scores'] for t, b in zip(result['treatments'], baseline['treatments']))
# Oracle order is likewise irrelevant; missing expected membership is not.
probe = copy.deepcopy(fixture)
probe['oracle']['eligible'].reverse()
assert all(t['scores']['eligible_set_exact'] for t in run(probe)['treatments'])
probe['oracle']['eligible'] = ['B']
assert not any(t['scores']['eligible_set_exact'] for t in run(probe)['treatments'])
# Duplicate input IDs are invalid, not silently collapsed into a set.
for location in ('vendors', 'oracle'):
    probe = copy.deepcopy(fixture)
    if location == 'vendors':
        probe['vendors'].append(copy.deepcopy(probe['vendors'][0]))
    else:
        probe['oracle']['eligible'].append('B')
    try:
        run(probe)
    except ValueError as error:
        assert 'must be unique' in str(error)
    else:
        raise AssertionError('Duplicate IDs should be rejected')
print('PASS: baseline bytes unchanged; 120 vendor permutations; oracle reversal; wrong membership; duplicate rejection')
