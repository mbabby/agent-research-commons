"""Small explicit event logger. Not an OS tracer or tamper-proof telemetry."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

out = pathlib.Path(sys.argv[1]).resolve()
action = sys.argv[2]
out.mkdir(parents=True, exist_ok=True)
log = out / 'events.jsonl'
def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def emit(event):
    event['at'] = stamp()
    # Python 3.9/macOS monotonic_ns can use a per-process epoch.
    event['monotonic_ns'] = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    with log.open('a') as stream:
        stream.write(json.dumps(event) + '\n')
    print(json.dumps(event))
if action == 'start':
    if log.exists():
        raise SystemExit('Refusing to restart an existing measurement')
    emit({'event': 'start'})
elif action == 'read':
    for name in sys.argv[3:]:
        path = pathlib.Path(name).resolve()
        data = path.read_bytes()
        emit({'event': 'file_read', 'path': str(path), 'bytes': len(data),
              'sha256': hashlib.sha256(data).hexdigest()})
        print('FILE ' + str(path) + '\n' + data.decode())
elif action == 'run':
    command = sys.argv[3:]
    emit({'event': 'command_start', 'command': command})
    result = subprocess.run(command, capture_output=True, text=True)
    (out / 'execution.stdout').write_text(result.stdout)
    (out / 'execution.stderr').write_text(result.stderr)
    receipt = {'command': command, 'exit_code': result.returncode,
               'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest(),
               'finished_at': stamp()}
    try:
        receipt['source_sha256'] = json.loads(result.stdout)['source_sha256']
    except (ValueError, KeyError, TypeError):
        receipt['source_sha256'] = None
    (out / 'execution-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    emit(dict(receipt, event='command_end'))
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
elif action in ('checkpoint', 'end'):
    name = sys.argv[3]
    path = out / (name + '.json')
    data = path.read_bytes()
    json.loads(data)
    emit({'event': action, 'artifact': path.name, 'bytes': len(data),
          'sha256': hashlib.sha256(data).hexdigest()})
else:
    raise SystemExit('Use start, read PATH..., run COMMAND..., checkpoint NAME or end NAME')
