#!/usr/bin/env python3
"""Bounded synthetic pending-operation recovery experiment; stdlib only."""
import argparse
import base64
import hashlib
import http.client
import http.server
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
from urllib.parse import urlsplit

SHA = 'f26b5522bbb20f2904d7534b879fa2896bdf1302'
CASES = ('safe-pending', 'unsafe-pending', 'safe-read-failed', 'safe-ambiguous-absence', 'safe-reconcile', 'safe-mismatched-receipt')


def save(path, value):
    with path.open('w') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def request(url, method='GET', body=None):
    u = urlsplit(url)
    assert u.hostname == '127.0.0.1', 'Only loopback permitted'
    c = http.client.HTTPConnection(u.hostname, u.port, timeout=5)
    try:
        c.request(method, u.path, json.dumps(body) if body is not None else None,
                  {'Content-Type': 'application/json'})
        r = c.getresponse()
        return r.status, json.loads(r.read())
    finally:
        c.close()


def client(args):
    out = Path(args.output)
    checkpoint = Path(os.environ['INFERNOSIM_CHECKPOINT_DIR']) / 'operation.json'
    pid = os.getpid()
    if not checkpoint.exists():
        code, op = request(args.provider + '/operations', 'POST', {'business_key': 'payment-1', 'key': 'original'})
        assert code == 202 and op['status'] == 'pending' and op['business_key'] == 'payment-1'
        save(checkpoint, op)
        save(out / 'checkpoint-copy.json', op)
        save(out / 'first-client.json', {'pid': pid, 'operation': op})
        # This one recorded HTTP exchange is an explicit crash barrier, not a
        # provider call. InfernoSIM kills this process before its response.
        proxy = urlsplit(os.environ['INFERNOSIM_PROXY_URL'])
        c = http.client.HTTPConnection(proxy.hostname, proxy.port, timeout=5)
        c.request('POST', 'http://barrier.test/tools', json.dumps(barrier_request()), {'Content-Type': 'application/json'})
        c.getresponse().read()
        raise RuntimeError('Crash boundary was not exercised')
    op = json.loads(checkpoint.read_text())
    code, observed = request(args.provider + '/operations/' + op['id'])
    decision = {'pid': pid, 'retained_handle': op['id'], 'first_status_code': code,
                'first_observation': observed, 'outcome': 'unknown', 'submitted_new': False}
    if args.case == 'unsafe-pending':
        code2, new = request(args.provider + '/operations', 'POST', {'business_key': 'payment-1', 'key': 'replacement'})
        assert code2 == 202
        decision.update(submitted_new=True, replacement=new['id'], outcome='unknown')
    elif args.case in ('safe-reconcile', 'safe-mismatched-receipt'):
        assert code == 200 and observed['status'] == 'pending'
        code2, completed = request(args.provider + '/operations/' + op['id'])
        assert code2 == 200 and completed['status'] == 'completed'
        matched = all(completed.get(k) == op[k] for k in ('id', 'business_key', 'idem_key'))
        decision.update(outcome='completed' if matched else 'unknown', terminal_observation=completed, receipt_matched=matched)
    save(out / 'decision.json', decision)


def barrier_request():
    return {'jsonrpc': '2.0', 'id': 'barrier', 'method': 'tools/call', 'params': {'name': 'checkpoint_barrier', 'arguments': {}}}


def run(args):
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    for d in ('home', 'tmp', 'incident'):
        (out / d).mkdir()
    db = out / 'provider.sqlite'
    with sqlite3.connect(db) as con:
        con.executescript('''CREATE TABLE operations(id TEXT PRIMARY KEY, business_key TEXT NOT NULL, idem_key TEXT UNIQUE NOT NULL, status TEXT NOT NULL);
        CREATE TABLE effects(operation_id TEXT PRIMARY KEY, business_key TEXT NOT NULL);
        CREATE TABLE events(seq INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, detail TEXT NOT NULL);''')

    def event(con, kind, detail):
        con.execute('INSERT INTO events(kind, detail) VALUES (?,?)', (kind, json.dumps(detail, sort_keys=True)))

    def drain(con, reason):
        rows = con.execute("SELECT id,business_key FROM operations WHERE status='pending' ORDER BY id").fetchall()
        for handle, key in rows:
            con.execute('INSERT INTO effects VALUES (?,?)', (handle, key))
            con.execute("UPDATE operations SET status='completed' WHERE id=?", (handle,))
            event(con, 'effect_committed', {'id': handle, 'reason': reason})

    class Provider(http.server.BaseHTTPRequestHandler):
        def log_message(self, *unused):
            pass

        def reply(self, status, body):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            assert self.path == '/operations'
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            with sqlite3.connect(db) as con:
                row = con.execute('SELECT id,status FROM operations WHERE idem_key=?', (body['key'],)).fetchone()
                if row is None:
                    handle = 'op-' + str(con.execute('SELECT COUNT(*) FROM operations').fetchone()[0] + 1)
                    row = (handle, 'pending')
                    con.execute('INSERT INTO operations VALUES (?,?,?,?)', (handle, body['business_key'], body['key'], 'pending'))
                event(con, 'submit', dict(body, id=row[0], status=row[1]))
            self.reply(202, {'id': row[0], 'status': row[1], 'business_key': body['business_key'], 'idem_key': body['key']})

        def do_GET(self):
            handle = self.path.rsplit('/', 1)[-1]
            with sqlite3.connect(db) as con:
                row = con.execute('SELECT status,business_key,idem_key FROM operations WHERE id=?', (handle,)).fetchone()
                assert row is not None
                code, body = 200, {'id': handle, 'status': row[0], 'business_key': row[1], 'idem_key': row[2]}
                if args.case == 'safe-read-failed':
                    code, body = 503, {'error': 'read unavailable'}
                if args.case == 'safe-ambiguous-absence':
                    code, body = 404, {'error': 'visibility lag; absence is not authoritative'}
                if args.case == 'safe-mismatched-receipt' and row[0] == 'completed':
                    body['id'] = 'op-unrelated'
                event(con, 'status_read', {'id': handle, 'actual_status': row[0], 'response_code': code, 'response': body})
                # First read remains pending; deterministic logical scheduler
                # completes after its observation, before the next read.
                if args.case in ('safe-reconcile', 'safe-mismatched-receipt') and row[0] == 'pending':
                    drain(con, 'after_first_pending_observation')
            self.reply(code, body)

    server = http.server.HTTPServer(('127.0.0.1', 0), Provider)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    incident = out / 'incident'
    response = {'jsonrpc': '2.0', 'id': 'barrier', 'result': {'ok': True}}
    evt = {'id': 'barrier', 'type': 'OutboundCall', 'method': 'POST', 'url': 'http://barrier.test/tools', 'status': 200,
           'bodyB64': base64.b64encode(json.dumps(barrier_request()).encode()).decode(), 'responseCaptured': True,
           'responseHeaders': {'Content-Type': ['application/json']}, 'responseBodyB64': base64.b64encode(json.dumps(response).encode()).decode()}
    save(incident / 'incident.json', {'schema_version': 1})
    (incident / 'inbound.log').write_text('')
    (incident / 'outbound.log').write_text(json.dumps(evt) + '\n')
    save(incident / 'replay.yaml', {'agent': {'enabled': True, 'adapters': {'mcp': True}, 'limits': {'max_calls': 4},
          'assertions': [{'id': 'recorded-only', 'type': 'no_unexpected_calls'}]}})
    argv = [str(Path(args.binary).resolve()), 'agent', 'run', str(incident), '--case', 'baseline', '--seed', '7140',
            '--restart-after-call', '1', '--report-dir', str(out / 'reports'), '--', sys.executable, str(Path(__file__).resolve()),
            'client', '--case', args.case, '--output', str(out), '--provider', 'http://127.0.0.1:' + str(server.server_port)]
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(out / 'home'), 'TMPDIR': str(out / 'tmp')}
    save(out / 'command.json', {'argv': argv, 'environment': env, 'source_sha_expected': SHA,
         'binary_sha256': hashlib.sha256(Path(args.binary).read_bytes()).hexdigest()})
    try:
        with (out / 'stdout').open('wb') as stdout, (out / 'stderr').open('wb') as stderr:
            proc = subprocess.run(argv, env=env, stdout=stdout, stderr=stderr, timeout=30)
        save(out / 'exit.json', {'returncode': proc.returncode})
        with sqlite3.connect(db) as con:
            event(con, 'client_runner_stopped', {'returncode': proc.returncode})
            before = {'operations': con.execute('SELECT * FROM operations ORDER BY id').fetchall(), 'effects': con.execute('SELECT * FROM effects ORDER BY operation_id').fetchall()}
            save(out / 'before-drain.json', before)
            drain(con, 'after_client_runner_stopped')
            event(con, 'drain_complete', {'pending': con.execute("SELECT COUNT(*) FROM operations WHERE status='pending'").fetchone()[0]})
        with sqlite3.connect(db) as con:
            save(out / 'after-drain.json', {t: con.execute('SELECT * FROM ' + t).fetchall() for t in ('operations', 'effects', 'events')})
        if proc.returncode:
            raise SystemExit(proc.returncode)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=('run', 'client'))
    p.add_argument('--case', choices=CASES, required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--binary')
    p.add_argument('--provider')
    a = p.parse_args()
    (run if a.action == 'run' else client)(a)
