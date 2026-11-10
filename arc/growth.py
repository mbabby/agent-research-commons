"""Private, evidence-led outreach bookkeeping. Never sends or scrapes."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from urllib.parse import urlsplit, urlunsplit
from uuid import uuid4
from zoneinfo import ZoneInfo


class Blocked(ValueError):
    """A safety or evidence precondition is unmet."""


def stamp(value=None):
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if not isinstance(value, str):
        raise Blocked('Timestamp must be an ISO string with a timezone')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise Blocked('Timestamp requires a timezone')
    return parsed.astimezone(timezone.utc).isoformat()


def url(value):
    parsed = urlsplit(value.strip())
    if parsed.scheme not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password:
        raise Blocked('A public HTTP(S) source URL without credentials is required')
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip('/'), parsed.query, parsed.fragment))


def endpoint(channel, value):
    value = value.strip()
    if channel in ('email', 'gmail'):
        if value.count('@') != 1 or any(c.isspace() for c in value) or not all(value.split('@')):
            raise Blocked('Invalid email address')
        return 'email', value.lower()
    if not channel.strip() or not value:
        raise Blocked('Channel and address are required')
    return channel.strip().lower(), url(value)


def provider_key(value):
    if not isinstance(value, str) or len(value.split(':', 2)) != 3 or not all(value.split(':', 2)):
        raise Blocked('Provider ID must be scoped as provider:account:message-id')
    return value


def required(data, *keys):
    for key in keys:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise Blocked('Missing nonempty field: ' + key)


SCHEMA = '''
CREATE TABLE IF NOT EXISTS people(id TEXT PRIMARY KEY, name TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS identities(identity TEXT PRIMARY KEY, person TEXT NOT NULL REFERENCES people(id));
CREATE TABLE IF NOT EXISTS endpoints(id TEXT PRIMARY KEY, person TEXT NOT NULL REFERENCES people(id), channel TEXT NOT NULL, address TEXT NOT NULL, contact_source TEXT NOT NULL, relevance_source TEXT NOT NULL, relevance TEXT NOT NULL, verified_at TEXT NOT NULL, UNIQUE(channel,address));
CREATE TABLE IF NOT EXISTS reviews(person TEXT PRIMARY KEY REFERENCES people(id), payload TEXT NOT NULL, reviewed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS attempts(id TEXT PRIMARY KEY, person TEXT NOT NULL REFERENCES people(id), endpoint TEXT NOT NULL REFERENCES endpoints(id), kind TEXT NOT NULL CHECK(kind IN ('first','followup')), state TEXT NOT NULL CHECK(state IN ('reserved','unknown','sent','accepted','failed','denied','cancelled')), reserved_at TEXT NOT NULL, sent_at TEXT, provider_id TEXT UNIQUE, evidence TEXT, draft TEXT NOT NULL);
CREATE UNIQUE INDEX IF NOT EXISTS active_attempt ON attempts(person) WHERE state IN ('reserved','unknown');
CREATE TABLE IF NOT EXISTS durable_reservations(attempt TEXT PRIMARY KEY REFERENCES attempts(id), at TEXT NOT NULL, evidence TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS result_log(id TEXT PRIMARY KEY, attempt TEXT NOT NULL REFERENCES attempts(id), state TEXT NOT NULL, at TEXT NOT NULL, provider_id TEXT, evidence TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY, person TEXT NOT NULL REFERENCES people(id), attempt TEXT REFERENCES attempts(id), kind TEXT NOT NULL, at TEXT NOT NULL, evidence TEXT NOT NULL, UNIQUE(person,kind,evidence));
CREATE TABLE IF NOT EXISTS suppressions(person TEXT PRIMARY KEY REFERENCES people(id), at TEXT NOT NULL, evidence TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS caps(channel TEXT PRIMARY KEY, daily_limit INTEGER NOT NULL CHECK(daily_limit >= 0), evidence TEXT NOT NULL, checked_at TEXT NOT NULL);
PRAGMA user_version=1;
'''
TABLES = ('people', 'identities', 'endpoints', 'reviews', 'attempts', 'durable_reservations', 'result_log', 'events', 'suppressions', 'caps')


class Ledger:
    def __init__(self, path, now=None):
        self.path = Path(path)
        if self.path.is_symlink():
            raise Blocked('Ledger path must not be a symbolic link')
        if self.path.exists() and self.path.stat().st_mode & 0o077:
            raise Blocked('Existing ledger is not owner-only; use a private copy with mode 0600')
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # The ledger belongs outside a checkout. Restrict files from first creation.
        old_mask = os.umask(0o077)
        try:
            self.db = sqlite3.connect(str(self.path), timeout=15, isolation_level=None)
            self.db.execute('PRAGMA foreign_keys=ON')
            self.db.executescript(SCHEMA)
        finally:
            os.umask(old_mask)
        self.db.row_factory = sqlite3.Row
        self.now = stamp(now)
        self.dt = datetime.fromisoformat(self.now)

    def close(self):
        self.db.close()

    @contextmanager
    def transaction(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            yield
        except Exception:
            self.db.rollback()
            raise
        else:
            self.db.commit()

    def fresh(self, timestamp, days):
        dt = datetime.fromisoformat(stamp(timestamp))
        if not self.dt - timedelta(days=days) <= dt <= self.dt:
            raise Blocked('Evidence is stale or dated in the future')

    def person(self, person):
        if not self.db.execute('SELECT 1 FROM people WHERE id=?', (person,)).fetchone():
            raise Blocked('Unknown person')

    def add(self, data):
        required(data, 'identity', 'name', 'channel', 'address', 'contact_source', 'relevance_source', 'relevance', 'verified_at')
        aliases = {url(data['identity'])} | {url(item) for item in data.get('aliases', [])}
        channel, address = endpoint(data['channel'], data['address'])
        verified = stamp(data['verified_at'])
        if datetime.fromisoformat(verified) > self.dt:
            raise Blocked('Source verification cannot be in the future')
        contact, source = url(data['contact_source']), url(data['relevance_source'])
        with self.transaction():
            known = set()
            for alias in aliases:
                row = self.db.execute('SELECT person FROM identities WHERE identity=?', (alias,)).fetchone()
                if row:
                    known.add(row['person'])
            row = self.db.execute('SELECT person FROM endpoints WHERE channel=? AND address=?', (channel, address)).fetchone()
            if row:
                known.add(row['person'])
            if len(known) > 1:
                raise Blocked('Identity collision: investigate before merging or sending')
            person = next(iter(known)) if known else str(uuid4())
            self.db.execute('INSERT OR IGNORE INTO people VALUES(?,?,?)', (person, data['name'], self.now))
            for alias in aliases:
                self.db.execute('INSERT OR IGNORE INTO identities VALUES(?,?)', (alias, person))
            self.db.execute('INSERT INTO endpoints VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(channel,address) DO UPDATE SET contact_source=excluded.contact_source,relevance_source=excluded.relevance_source,relevance=excluded.relevance,verified_at=excluded.verified_at', (str(uuid4()), person, channel, address, contact, source, data['relevance'], verified))
            ep = self.db.execute('SELECT id FROM endpoints WHERE channel=? AND address=?', (channel, address)).fetchone()['id']
        return {'person': person, 'endpoint': ep, 'deduplicated': bool(known)}

    def review(self, person, data):
        self.person(person)
        required(data, 'subject', 'body', 'personalization', 'ask', 'opt_out_text', 'sender_identity', 'history_evidence', 'policy_evidence', 'backup_evidence')
        for key in ('history_checked_at', 'policy_checked_at', 'backup_verified_at'):
            self.fresh(data.get(key), 1)
        if data['opt_out_text'] not in data['body'] or data['sender_identity'] not in data['body']:
            raise Blocked('Draft must include the declared sender identity and refusal route')
        if not isinstance(data.get('followup_allowed', False), bool):
            raise Blocked('followup_allowed must be boolean')
        with self.transaction():
            self.db.execute('INSERT INTO reviews VALUES(?,?,?) ON CONFLICT(person) DO UPDATE SET payload=excluded.payload,reviewed_at=excluded.reviewed_at', (person, json.dumps(data, ensure_ascii=False), self.now))
        return {'person': person, 'reviewed_at': self.now}

    def cap(self, channel, limit, evidence):
        if limit < 0 or not evidence.strip():
            raise Blocked('Cap must be nonnegative and justified by verified evidence')
        channel = 'email' if channel == 'gmail' else channel.lower()
        self.db.execute('INSERT INTO caps VALUES(?,?,?,?) ON CONFLICT(channel) DO UPDATE SET daily_limit=excluded.daily_limit,evidence=excluded.evidence,checked_at=excluded.checked_at', (channel, limit, evidence, self.now))
        return {'channel': channel, 'daily_limit': limit}

    def _eligible(self, person, endpoint_id, kind, tz):
        self.person(person)
        ep = self.db.execute('SELECT * FROM endpoints WHERE id=? AND person=?', (endpoint_id, person)).fetchone()
        if ep is None:
            raise Blocked('Endpoint does not belong to this person')
        if self.db.execute('SELECT 1 FROM suppressions WHERE person=?', (person,)).fetchone():
            raise Blocked('Creator is suppressed across all channels')
        if self.db.execute("SELECT 1 FROM events WHERE person=? AND kind IN ('reply','bounced')", (person,)).fetchone():
            raise Blocked('Reply or bounce stops the cold sequence')
        prior = self.db.execute('SELECT * FROM attempts WHERE person=?', (person,)).fetchall()
        if any(a['state'] == 'denied' for a in prior):
            raise Blocked('Policy-denied attempt requires authorization resolution; no automatic retry')
        if any(a['state'] in ('reserved', 'unknown') for a in prior):
            raise Blocked('Unresolved attempt: check provider outcome before any resend')
        firsts = [a for a in prior if a['state'] in ('sent', 'accepted') and a['kind'] == 'first']
        if kind == 'first' and firsts:
            raise Blocked('Already contacted: first touch cannot be repeated on another channel')
        row = self.db.execute('SELECT payload FROM reviews WHERE person=?', (person,)).fetchone()
        if row is None:
            raise Blocked('Personalization and safety review required')
        review = json.loads(row['payload'])
        for key in ('history_checked_at', 'policy_checked_at', 'backup_verified_at'):
            self.fresh(review.get(key), 1)
        self.fresh(ep['verified_at'], 14)
        if kind == 'followup':
            if not firsts or not review.get('followup_allowed'):
                raise Blocked('Follow-up lacks first send or explicit authorization')
            first_at = min(datetime.fromisoformat(a['sent_at']) for a in firsts)
            if self.dt - first_at < timedelta(days=7):
                raise Blocked('Follow-up must wait at least seven days')
            if any(a['kind'] == 'followup' and a['state'] in ('sent', 'accepted') for a in prior):
                raise Blocked('At most one follow-up is allowed')
        self._check_capacity(ep['channel'])
        return dict(ep), review

    def _check_capacity(self, channel, existing_reservation=0):
        cap = self.db.execute('SELECT * FROM caps WHERE channel=?', (channel,)).fetchone()
        if cap is None:
            raise Blocked('No verified channel capacity; default cap is zero')
        self.fresh(cap['checked_at'], 1)
        attempts = self.db.execute("SELECT a.* FROM attempts a JOIN endpoints e ON e.id=a.endpoint WHERE e.channel=? AND a.state IN ('reserved','unknown','sent','accepted')", (channel,)).fetchall()
        # Unknown/reserved operations consume capacity until resolved, including older days.
        used = sum(a['state'] in ('reserved','unknown') or datetime.fromisoformat(a['sent_at']) >= self.dt - timedelta(hours=24) for a in attempts)
        if used >= cap['daily_limit'] + existing_reservation:
            raise Blocked('Verified channel daily capacity is exhausted')

    def reserve(self, person, endpoint_id, kind='first', tz='UTC'):
        if kind not in ('first', 'followup'):
            raise Blocked('Unknown attempt kind')
        with self.transaction():
            ep, review = self._eligible(person, endpoint_id, kind, tz)
            attempt = str(uuid4())
            self.db.execute('INSERT INTO attempts VALUES(?,?,?,?,?,?,NULL,NULL,NULL,?)', (attempt, person, endpoint_id, kind, 'reserved', self.now, json.dumps(review, ensure_ascii=False)))
        return {'attempt': attempt, 'person': person, 'state': 'reserved', 'warning': 'DO NOT SEND YET. Export this reservation to durable private storage, verify it, then run confirm-checkpoint.'}

    def confirm_checkpoint(self, attempt, evidence):
        if not evidence.strip():
            raise Blocked('Durable checkpoint receipt containing this reservation is required')
        with self.transaction():
            row = self.db.execute('SELECT * FROM attempts WHERE id=?', (attempt,)).fetchone()
            if row is None or row['state'] != 'reserved':
                raise Blocked('Only an unresolved reservation can be prepared for sending')
            if self.db.execute('SELECT 1 FROM suppressions WHERE person=?', (row['person'],)).fetchone() or self.db.execute("SELECT 1 FROM events WHERE person=? AND kind IN ('reply','bounced')", (row['person'],)).fetchone():
                raise Blocked('Suppression or response stops this send')
            review = json.loads(row['draft'])
            for key in ('history_checked_at', 'policy_checked_at', 'backup_verified_at'):
                self.fresh(review.get(key), 1)
            ep = self.db.execute('SELECT * FROM endpoints WHERE id=?', (row['endpoint'],)).fetchone()
            self.fresh(ep['verified_at'], 14)
            self._check_capacity(ep['channel'], existing_reservation=1)
            self.db.execute('INSERT OR REPLACE INTO durable_reservations VALUES(?,?,?)', (attempt, self.now, evidence))
        return {'attempt': attempt, 'person': row['person'], 'channel': ep['channel'], 'address': ep['address'], 'subject': review['subject'], 'body': review['body'], 'warning': 'This command did not send. Verify current provider history and suppression immediately before the authorized external action. Never retry an uncertain send.'}

    def result(self, attempt, state, evidence, provider_id=None, at=None):
        if state not in ('sent', 'accepted', 'unknown', 'failed', 'denied') or not evidence.strip():
            raise Blocked('Result requires a valid state and evidence')
        when = stamp(at or self.now)
        if datetime.fromisoformat(when) > self.dt:
            raise Blocked('Result cannot be in the future')
        if state == 'sent':
            provider_key(provider_id)
        with self.transaction():
            row = self.db.execute('SELECT * FROM attempts WHERE id=?', (attempt,)).fetchone()
            if row is None:
                raise Blocked('Unknown attempt')
            if state == 'accepted':
                channel = self.db.execute('SELECT channel FROM endpoints WHERE id=?', (row['endpoint'],)).fetchone()[0]
                if channel != 'contact_form':
                    raise Blocked('accepted without a provider ID is only valid for contact_form receipts')
            if row['state'] == state and row['evidence'] == evidence and row['provider_id'] == provider_id:
                return {'attempt': attempt, 'state': state, 'unchanged': True}
            if state in ('sent', 'accepted') and at is None and (row['state'] != 'reserved' or datetime.fromisoformat(row['reserved_at']).date() != self.dt.date()):
                raise Blocked('Reconciled or historical send requires actual provider send time via --at')
            if row['state'] == 'denied' and state not in ('sent', 'accepted'):
                raise Blocked('Policy denial cannot be cleared to permit an automatic retry')
            if row['state'] not in ('reserved', 'unknown', 'cancelled', 'denied'):
                raise Blocked('Resolved result cannot be overwritten; retain and correct evidence')
            if datetime.fromisoformat(when) < datetime.fromisoformat(row['reserved_at']) and not attempt.startswith('legacy-'):
                raise Blocked('Result predates reservation')
            # A late confirmation after cancellation must still be recorded truthfully.
            self.db.execute('INSERT INTO result_log VALUES(?,?,?,?,?,?)', (str(uuid4()), attempt, state, when, provider_id, evidence))
            self.db.execute('UPDATE attempts SET state=?,sent_at=?,provider_id=?,evidence=? WHERE id=?', (state, when if state in ('sent', 'accepted') else None, provider_id, evidence, attempt))
        return {'attempt': attempt, 'state': state}

    def event(self, person, kind, evidence, attempt=None, at=None):
        self.person(person)
        if kind not in ('delivered', 'bounced', 'reply', 'participation', 'reuse') or not evidence.strip():
            raise Blocked('Outcome requires a supported kind and evidence')
        when = stamp(at or self.now)
        if datetime.fromisoformat(when) > self.dt:
            raise Blocked('Event cannot be in the future')
        if attempt:
            row = self.db.execute('SELECT person,state,sent_at FROM attempts WHERE id=?', (attempt,)).fetchone()
            if row is None or row['person'] != person or row['state'] not in ('sent', 'accepted'):
                raise Blocked('Outcome attempt must be a confirmed send for this person')
            if when < row['sent_at']:
                raise Blocked('Outcome predates send')
        if kind in ('delivered', 'bounced', 'reply') and not attempt:
            raise Blocked('Delivery, bounce and reply need an attributable attempt')
        with self.transaction():
            self.db.execute('INSERT OR IGNORE INTO events VALUES(?,?,?,?,?,?)', (str(uuid4()), person, attempt, kind, when, evidence))
            if kind in ('reply', 'bounced'):
                self.db.execute("UPDATE attempts SET state='cancelled' WHERE person=? AND state='reserved'", (person,))
        return {'person': person, 'kind': kind}

    def suppress(self, person, evidence, at=None):
        self.person(person)
        if not evidence.strip():
            raise Blocked('Suppression needs evidence')
        when = stamp(at or self.now)
        with self.transaction():
            self.db.execute('INSERT OR IGNORE INTO suppressions VALUES(?,?,?)', (person, when, evidence))
            self.db.execute("UPDATE attempts SET state='cancelled' WHERE person=? AND state='reserved'", (person,))
        return {'person': person, 'suppressed': True}

    def import_legacy(self, data):
        imported = 0
        unresolved = 0
        # Apply refusals first, including people never contacted.
        for r in data.get('suppression', []):
            if not isinstance(r, dict) or not (r.get('email') or r.get('source')):
                raise Blocked('Unsupported suppression record: reconcile it manually before sending')
            evidence = r.get('evidence') or ((r.get('source', '') + ' ' + r.get('reason', '')).strip())
            if not evidence:
                raise Blocked('Suppression record lacks evidence')
            ch, address = endpoint('email', r['email']) if r.get('email') else endpoint('profile', r['source'])
            row = self.db.execute('SELECT person FROM endpoints WHERE channel=? AND address=?', (ch, address)).fetchone()
            if row is None:
                required(r, 'name', 'source', 'reason')
                added = self.add({'identity': r['source'], 'name': r['name'], 'channel': ch, 'address': address, 'contact_source': r['source'], 'relevance_source': r['source'], 'relevance': 'Suppression-only record: ' + r['reason'], 'verified_at': r.get('checked_at') or self.now})
                person = added['person']
            else:
                person = row['person']
            self.suppress(person, evidence, r.get('at') or r.get('checked_at'))
        for original in data.get('records', []):
            r = dict(original)
            if not r.get('id') and not r.get('attempted_at'):
                raise Blocked('Legacy record needs a stable source ID when actual attempt time is missing')
            channel = r.get('channel', 'email')
            address = r.get('email') or r.get('contact_url')
            if not address:
                raise Blocked('Legacy record lacks a usable contact endpoint')
            r.setdefault('relevance_source', (r.get('relevance_sources') or [None])[0])
            r.setdefault('relevance', 'Legacy contact-form invitation; inspect preserved message and linked work.')
            required(r, 'name', 'contact_source', 'relevance_source', 'relevance')
            added = self.add({'identity': r['contact_source'], 'name': r['name'], 'channel': channel, 'address': address, 'contact_source': r['contact_source'], 'relevance_source': r['relevance_source'], 'relevance': r['relevance'], 'verified_at': r.get('verified_at') or r.get('attempted_at') or self.now})
            raw_id = r.get('message_id')
            message_id = provider_key(':'.join([r.get('channel', 'email'), r.get('from', 'legacy-unknown-account'), raw_id])) if raw_id else None
            source_key = json.dumps([r.get('id') or r.get('attempted_at'), endpoint(channel, address), r.get('from')], separators=(',', ':'))
            attempt_id = 'legacy-' + hashlib.sha256((str(data.get('date_utc')) + ':' + source_key).encode()).hexdigest()
            # Prefer the reconciled provider send time, not source-check time.
            actual_at = r.get('provider_sent_at') or r.get('attempted_at')
            state = 'sent' if r.get('status') == 'sent' and message_id and actual_at else 'unknown'
            if r.get('status') == 'accepted':
                if channel != 'contact_form':
                    raise Blocked('Legacy accepted status requires a contact_form receipt')
                if r.get('confirmation_text') and actual_at:
                    state = 'accepted'
            if r.get('status') == 'denied':
                state = 'denied'
            elif r.get('status') == 'failed' and r.get('not_executed') is True:
                state = 'failed'
            when = stamp(actual_at or self.now)
            if datetime.fromisoformat(when) > self.dt:
                raise Blocked('Legacy send is in the future')
            evidence = r.get('message_url') or ((r.get('confirmation_url') or r.get('contact_url') or '') + ' ' + r.get('confirmation_text', '')).strip() or 'legacy ledger; provider reconciliation required'
            existing = self.db.execute('SELECT * FROM attempts WHERE id=?', (attempt_id,)).fetchone()
            if existing:
                if existing['state'] in ('unknown', 'reserved') and state in ('sent', 'accepted', 'failed', 'denied'):
                    self.result(attempt_id, state, evidence, message_id if state == 'sent' else None, when)
                    imported += state in ('sent', 'accepted')
                continue
            if message_id and self.db.execute('SELECT 1 FROM attempts WHERE provider_id=?', (message_id,)).fetchone():
                continue
            with self.transaction():
                self.db.execute('INSERT INTO attempts VALUES(?,?,?,?,?,?,?,?,?,?)', (attempt_id, added['person'], added['endpoint'], 'first', state, when, when if state in ('sent', 'accepted') else None, message_id if state == 'sent' else None, evidence, json.dumps({'subject': r.get('subject'), 'body': r.get('body'), 'followup_allowed': False, 'previous_attempts': r.get('previous_attempts', []), 'send_result': r.get('send_result')}, ensure_ascii=False)))
            imported += state in ('sent', 'accepted')
            unresolved += state == 'unknown'
        return {'imported_confirmed': imported, 'imported_unresolved': unresolved}

    def report(self, day, tz='UTC', target=150):
        if target < 0:
            raise Blocked('Target must be nonnegative')
        zone = ZoneInfo(tz)
        requested = datetime.strptime(day, '%Y-%m-%d').date()
        in_day = lambda value: datetime.fromisoformat(value).astimezone(zone).date() == requested
        attempts = [dict(r) for r in self.db.execute('SELECT * FROM attempts')]
        first = {}
        for a in sorted((a for a in attempts if a['state'] in ('sent', 'accepted') and a['kind'] == 'first'), key=lambda a: a['sent_at']):
            first.setdefault(a['person'], a)
        cohort = {p for p, a in first.items() if in_day(a['sent_at'])}
        events = [dict(r) for r in self.db.execute('SELECT * FROM events')]
        replies = {e['person'] for e in events if e['kind'] == 'reply'}
        out = {'day': day, 'timezone': tz, 'target_unique_first_contacts': target, 'provider_confirmed_unique_first_contacts': len(cohort), 'confirmed_first_sends': sum(first[p]['state'] == 'sent' for p in cohort), 'confirmed_first_form_acceptances': sum(first[p]['state'] == 'accepted' for p in cohort), 'shortfall': max(0, target-len(cohort)), 'goal_met': len(cohort) >= target, 'confirmed_followup_sends': sum(a['state'] in ('sent', 'accepted') and a['kind'] == 'followup' and in_day(a['sent_at']) for a in attempts), 'policy_denied_attempts_all_days': sum(a['state'] == 'denied' for a in attempts), 'previous_denials_recorded': sum(p.get('status') == 'denied' for a in attempts for p in json.loads(a['draft']).get('previous_attempts', [])), 'unresolved_attempts_all_days': sum(a['state'] in ('reserved', 'unknown') for a in attempts), 'suppressed_creators_total': self.db.execute('SELECT COUNT(*) FROM suppressions').fetchone()[0], 'candidate_creators_total': self.db.execute('SELECT COUNT(*) FROM people').fetchone()[0], 'currently_ready_unique_creators': self.queue(tz)['ready_unique_creators'], 'sent_cohort_replies_observed': len(cohort & replies), 'sent_cohort_reply_rate_so_far': round(len(cohort & replies)/len(cohort), 4) if cohort else None, 'limitations': ['Provider-confirmed send is not verified delivery.', 'Counts are recorded evidence, not automated verification or causal growth.', 'Different creator accounts may have the same operator.']}
        for kind in ('delivered', 'bounced', 'reply', 'participation', 'reuse'):
            out[kind + '_creators_observed_on_day'] = len({e['person'] for e in events if e['kind'] == kind and in_day(e['at'])})
        return out

    def queue(self, tz='UTC'):
        ready, blocked = [], []
        for ep in self.db.execute('SELECT * FROM endpoints').fetchall():
            try:
                self._eligible(ep['person'], ep['id'], 'first', tz)
            except Blocked as exc:
                blocked.append({'person': ep['person'], 'endpoint': ep['id'], 'reason': str(exc)})
            else:
                ready.append({'person': ep['person'], 'endpoint': ep['id'], 'channel': ep['channel']})
        return {'ready_unique_creators': len({r['person'] for r in ready}), 'ready': ready, 'blocked': blocked}

    def checkpoint(self):
        with self.transaction():
            tables = {t: [dict(r) for r in self.db.execute('SELECT * FROM ' + t)] for t in TABLES}
        return {'schema_version': 1, 'exported_at': self.now, 'tables': tables}

    def restore(self, data):
        if data.get('schema_version') != 1 or set(data.get('tables', {})) != set(TABLES):
            raise Blocked('Unsupported checkpoint schema')
        with self.transaction():
            if any(self.db.execute('SELECT 1 FROM ' + t).fetchone() for t in TABLES):
                raise Blocked('Restore requires an empty ledger; never overwrite newer records')
            for table in TABLES:
                columns = [r['name'] for r in self.db.execute('PRAGMA table_info(' + table + ')')]
                for row in data['tables'][table]:
                    if set(row) != set(columns):
                        raise Blocked('Invalid checkpoint columns')
                    self.db.execute('INSERT INTO ' + table + ' VALUES(' + ','.join('?' for _ in columns) + ')', [row[c] for c in columns])
        return {'restored': True, 'exported_at': data.get('exported_at')}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True, help='Private SQLite file outside the public repository')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('add', 'import-legacy', 'restore'):
        sub.add_parser(name).add_argument('--input', required=True)
    p = sub.add_parser('review'); p.add_argument('--person', required=True); p.add_argument('--input', required=True)
    p = sub.add_parser('cap'); p.add_argument('--channel', required=True); p.add_argument('--limit', type=int, required=True); p.add_argument('--evidence', required=True)
    p = sub.add_parser('reserve'); p.add_argument('--person', required=True); p.add_argument('--endpoint', required=True); p.add_argument('--kind', choices=('first','followup'), default='first'); p.add_argument('--timezone', default='UTC')
    p = sub.add_parser('confirm-checkpoint'); p.add_argument('--attempt', required=True); p.add_argument('--evidence', required=True)
    p = sub.add_parser('result'); p.add_argument('--attempt', required=True); p.add_argument('--state', choices=('sent','accepted','unknown','failed','denied'), required=True); p.add_argument('--evidence', required=True); p.add_argument('--provider-id'); p.add_argument('--at')
    p = sub.add_parser('event'); p.add_argument('--person', required=True); p.add_argument('--kind', required=True); p.add_argument('--evidence', required=True); p.add_argument('--attempt'); p.add_argument('--at')
    p = sub.add_parser('suppress'); p.add_argument('--person', required=True); p.add_argument('--evidence', required=True); p.add_argument('--at')
    p = sub.add_parser('report'); p.add_argument('--day', required=True); p.add_argument('--timezone', default='UTC'); p.add_argument('--target', type=int, default=150)
    p = sub.add_parser('queue'); p.add_argument('--timezone', default='UTC')
    sub.add_parser('export')
    args = parser.parse_args(argv)
    ledger = None
    try:
        ledger = Ledger(args.db)
        cmd = args.command
        data = json.loads(Path(args.input).read_text()) if hasattr(args, 'input') else None
        if cmd == 'add': result = ledger.add(data)
        elif cmd == 'import-legacy': result = ledger.import_legacy(data)
        elif cmd == 'restore': result = ledger.restore(data)
        elif cmd == 'review': result = ledger.review(args.person, data)
        elif cmd == 'cap': result = ledger.cap(args.channel, args.limit, args.evidence)
        elif cmd == 'reserve': result = ledger.reserve(args.person, args.endpoint, args.kind, args.timezone)
        elif cmd == 'confirm-checkpoint': result = ledger.confirm_checkpoint(args.attempt, args.evidence)
        elif cmd == 'result': result = ledger.result(args.attempt, args.state, args.evidence, args.provider_id, args.at)
        elif cmd == 'event': result = ledger.event(args.person, args.kind, args.evidence, args.attempt, args.at)
        elif cmd == 'suppress': result = ledger.suppress(args.person, args.evidence, args.at)
        elif cmd == 'report': result = ledger.report(args.day, args.timezone, args.target)
        elif cmd == 'queue': result = ledger.queue(args.timezone)
        else: result = ledger.checkpoint()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (Blocked, ValueError, KeyError, sqlite3.IntegrityError) as exc:
        print(json.dumps({'blocked': True, 'reason': str(exc)}), file=sys.stderr)
        return 2
    finally:
        if ledger:
            ledger.close()


if __name__ == '__main__':
    sys.exit(main())
