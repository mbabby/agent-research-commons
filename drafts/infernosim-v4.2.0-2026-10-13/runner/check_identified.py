import json, os, pathlib, shutil, sqlite3, subprocess, sys
state=pathlib.Path(os.environ['INFERNOSIM_STATE_DIR'])
root=pathlib.Path(os.environ['EVIDENCE_DIR']); root.mkdir(parents=True,exist_ok=True)
out=root/os.environ['INFERNOSIM_CASE_ID'];out.mkdir(exist_ok=False)
with sqlite3.connect('file:'+str(state/'application.sqlite')+'?mode=ro',uri=True) as con:
    with sqlite3.connect(str(out/'application.sqlite')) as target: con.backup(target)
    tables={t:con.execute('SELECT * FROM '+t).fetchall() for t in ['account','outbox','idempotency','reservations']}
(out/'tables.json').write_text(json.dumps(tables,indent=2)+'\n')
shutil.copyfile(state/'application.jsonl',out/'application.jsonl')
p=subprocess.run(['/usr/bin/python3','/tmp/arc-inferno-source-20261013/examples/concurrencylab/app.py','--scenario','retry','--check'],capture_output=True)
(out/'check.stdout').write_bytes(p.stdout); (out/'check.stderr').write_bytes(p.stderr); (out/'check.exit').write_text(str(p.returncode)+'\n')
sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr);sys.exit(p.returncode)
