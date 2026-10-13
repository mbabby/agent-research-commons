"""Read raw SQLite before runner cleanup; persist backup; invoke upstream check unchanged."""
import json, os, pathlib, sqlite3, subprocess, sys, uuid
state = pathlib.Path(os.environ['INFERNOSIM_STATE_DIR'])
out = pathlib.Path(os.environ['CHECKER_EVIDENCE']) / str(uuid.uuid4())
out.mkdir(parents=True)
with sqlite3.connect('file:' + str(state / 'application.sqlite') + '?mode=ro', uri=True) as db:
    data = {table: db.execute('SELECT * FROM ' + table).fetchall() for table in ('outbox','idempotency','account','reservations')}
    with sqlite3.connect(out / 'application.sqlite') as saved:
        db.backup(saved)
data['case_id'] = os.environ.get('INFERNOSIM_CASE_ID')
(out / 'raw-sql.json').write_text(json.dumps(data, indent=2))
(out / 'application.jsonl').write_bytes((state / 'application.jsonl').read_bytes())
result = subprocess.run([sys.executable, '${SOURCE_ROOT}/examples/concurrencylab/app.py', '--scenario', 'retry', '--check'], capture_output=True)
(out / 'upstream-check.json').write_bytes(result.stdout)
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
raise SystemExit(result.returncode)
