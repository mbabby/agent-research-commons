#!/usr/bin/env python3
"""Run six fixed deterministic cases, preserving failures and exact provenance."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

CASES = ('safe-pending', 'unsafe-pending', 'safe-read-failed',
         'safe-ambiguous-absence', 'safe-reconcile', 'safe-mismatched-receipt')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', type=Path, required=True)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    fixture, binary, root = (p.resolve() for p in (args.fixture, args.binary, args.output))
    root.mkdir(parents=True, exist_ok=False)
    fingerprint = digest(fixture)
    metadata = {'fixture_sha256': fingerprint, 'binary_sha256': digest(binary),
                'python': sys.version, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'cases': [], 'note': 'Six selected deterministic cases; not independent statistical samples.'}
    for case in CASES:
        assert digest(fixture) == fingerprint, 'Fixture changed during campaign'
        argv = [sys.executable, str(fixture), 'run', '--case', case,
                '--binary', str(binary), '--output', str(root / case)]
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45,
                              env={'PATH': '/usr/bin:/bin', 'HOME': str(root), 'TMPDIR': '/tmp'})
        (root / (case + '.stdout')).write_bytes(proc.stdout)
        (root / (case + '.stderr')).write_bytes(proc.stderr)
        metadata['cases'].append({'case': case, 'argv': argv, 'exit': proc.returncode, 'started_utc': start})
        print(case, proc.returncode, flush=True)
    metadata['final_fixture_sha256'] = digest(fixture)
    (root/'campaign.json').write_text(json.dumps(metadata, indent=2)+'\n')
    assert metadata['final_fixture_sha256'] == fingerprint
    assert all(c['exit'] == 0 for c in metadata['cases'])

if __name__ == '__main__':
    main()
