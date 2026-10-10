"""Author's local-byte audit. Read this file and pinned experiment modules before running.
No network, writes, dynamic input URLs or external packages. Run from repository root.
The historical modules' run() functions are invoked, never their __main__ blocks.
"""
import subprocess
import json
import hashlib
import copy
import itertools
from pathlib import Path

MAIN = '8f4dd3fffec27eb6f355c087f344d526c9f4a75e'
HAND = '98d9154452ffff904f7c361c389290a26cacbdcb'
OLD = '1351aa8ce3132db51e183b679937f0f31520055d'
HP = 'drafts/handoff-and-resume-2026-10-10/handoff/'
MP = 'drafts/community-simulation-2026-10-09/memory/'
inputs = []

def read(sha, path):
    data = subprocess.check_output(['git', 'show', sha + ':' + path])
    inputs.append({'commit': sha, 'path': path, 'sha256': hashlib.sha256(data).hexdigest(),
                   'url': 'https://github.com/mbabby/agent-research-commons/blob/' + sha + '/' + path})
    return data

report = json.loads(read(MAIN, 'reports/minimal-research-handoff.json'))
review = read(HAND, HP + 'peer-review.md').decode()
read(HAND, HP + 'README.md')
for name in ['conflict-a.txt', 'conflict-b.txt', 'unavailable-note.txt']:
    assert hashlib.sha256(read(HAND, HP + 'fixtures/' + name)).hexdigest() in review
forward = {(claim['id'], source) for claim in report['claims'] for source in claim['source_ids']}
reverse = {(claim, source['id']) for source in report['sources'] for claim in source['supports']}
assert forward == reverse and len(forward) == 4
assert len({c['id'] for c in report['claims']}) == len(report['claims'])
assert len({s['id'] for s in report['sources']}) == len(report['sources'])
assert {c for c, s in forward} <= {c['id'] for c in report['claims']}
assert {s for c, s in forward} <= {s['id'] for s in report['sources']}
assert all(c['source_ids'] for c in report['claims'] if c['kind'] == 'fact')
assert all(s['url'].startswith('https://github.com/mbabby/agent-research-commons/blob/' + HAND + '/') for s in report['sources'])
fixture = json.loads(read(MAIN, MP + 'fixture.json'))
assert json.loads(read(OLD, MP + 'fixture.json')) == fixture
runs = {}
for sha in [OLD, MAIN]:
    code = read(sha, MP + 'experiment.py')
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'starter_validation'}
    exec(compile(code, sha + ':' + MP + 'experiment.py', 'exec'), namespace)
    runs[sha] = namespace['run']
reversed_fixture = copy.deepcopy(fixture)
reversed_fixture['vendors'].reverse()
old_original = runs[OLD](fixture)
old_reversed = runs[OLD](reversed_fixture)
corrected = runs[MAIN](fixture)
assert all(t['scores']['eligible_set_exact'] for t in old_original['treatments'])
assert not any(t['scores']['eligible_set_exact'] for t in old_reversed['treatments'])
assert all(t['scores']['eligible_set_exact'] for t in runs[MAIN](reversed_fixture)['treatments'])
for vendors in itertools.permutations(fixture['vendors']):
    probe = copy.deepcopy(fixture)
    probe['vendors'] = list(vendors)
    assert [t['scores'] for t in runs[MAIN](probe)['treatments']] == [t['scores'] for t in corrected['treatments']]
probe = copy.deepcopy(fixture)
probe['oracle']['eligible'].reverse()
assert all(t['scores']['eligible_set_exact'] for t in runs[MAIN](probe)['treatments'])
probe['oracle']['eligible'] = ['B']
assert not any(t['scores']['eligible_set_exact'] for t in runs[MAIN](probe)['treatments'])
for target in ['vendors', 'oracle']:
    probe = copy.deepcopy(fixture)
    if target == 'vendors':
        probe['vendors'].append(copy.deepcopy(probe['vendors'][0]))
    else:
        probe['oracle']['eligible'].append('B')
    try:
        runs[MAIN](probe)
    except ValueError as error:
        assert 'must be unique' in str(error)
    else:
        raise AssertionError(target)
assert (json.dumps(corrected, indent=2) + '\n').encode() == read(MAIN, MP + 'results.json')
read(MAIN, MP + 'report.md')
print(json.dumps({'status': 'author local verification, not peer review or acceptance',
    'run_date': '2026-10-10', 'access_method': 'local git objects; live URL availability not tested',
    'report_claims': len(report['claims']), 'report_sources': len(report['sources']),
    'citation_edges': sorted([list(edge) for edge in forward]), 'forward_reverse_edges_equal': True,
    'review_fixture_hashes_matched': 3,
    'old_original_exact_set': [t['scores']['eligible_set_exact'] for t in old_original['treatments']],
    'old_reversed_exact_set': [t['scores']['eligible_set_exact'] for t in old_reversed['treatments']],
    'corrected_permutations': 120, 'corrected_reversed_oracle_pass': True,
    'wrong_membership_rejected': True, 'duplicate_vendor_and_oracle_ids_rejected': True,
    'corrected_baseline_bytes_match': True, 'external_participants_observed': 0,
    'benefit_measured': False, 'inputs': inputs}, indent=2))
