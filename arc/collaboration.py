"""Pure advisory graph for optional community metadata; never fetch artifacts."""
from datetime import datetime, timezone
import json
import re
from urllib.parse import unquote, urlsplit

MARKER = '<!-- arc-record:v1 -->'
_MARKER_LINE = re.compile(r'^' + re.escape(MARKER) + r'(?:\r?\n|$)', re.MULTILINE)
_BLOCK = re.compile(r'^' + re.escape(MARKER) + r'\r?\n```json\r?\n(.*?)\r?\n```(?:\r?\n|$)', re.MULTILINE | re.DOTALL)
_VERSION = re.compile(r'[0-9a-f]{40}')
_NEEDS = {'evidence', 'reproduction', 'counterexample', 'review', 'method'}
_CHECKS = {'reproducibility', 'data', 'method', 'conclusion'}
_FIELDS = {'question': {'kind', 'needs'}, 'intent': {'kind', 'question', 'scope', 'expires_at'},
           'contribution': {'kind', 'question', 'artifact_url', 'artifact_version', 'supersedes'},
           'review': {'kind', 'contribution', 'artifact_version', 'artifact_url', 'affiliation', 'checks'},
           'reuse': {'kind', 'contribution', 'artifact_version', 'artifact_url', 'outcome', 'evidence_url'}}


def _require(condition, reason='Invalid record fields'):
    if not condition:
        raise ValueError(reason)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _number(value):
    return type(value) is int and value > 0


def _date(value):
    _require(isinstance(value, str) and re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', value), 'Invalid UTC timestamp')
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError('Invalid UTC timestamp') from None


def _url(value):
    _require(_text(value) and not any(c.isspace() or ord(c) < 32 for c in value), 'Invalid HTTPS URL')
    try:
        url = urlsplit(value)
        _require(url.scheme == 'https' and bool(url.hostname) and url.username is None and url.password is None and '\\' not in value, 'Invalid HTTPS URL')
        # Evaluate port to reject malformed or out-of-range authority values.
        url.port
    except ValueError:
        raise ValueError('Invalid HTTPS URL') from None
    return url


def _artifact_path(parts):
    """Require a canonical repository and path that cannot discard its revision."""
    _require(len(parts) >= 5, 'Invalid fixed GitHub artifact URL')
    _require(re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', parts[1]) is not None
             and re.fullmatch(r'[A-Za-z0-9_.-]+', parts[2]) is not None
             and parts[2] not in ('.', '..'), 'Invalid GitHub repository path')
    for segment in parts[5:]:
        # Repeated decoding also rejects disguised encoded separators/dot segments.
        # Ordinary encoded spaces and Unicode file names remain allowed.
        while True:
            _require(segment not in ('.', '..') and '/' not in segment and '\\' not in segment
                     and not any(ord(c) < 32 or ord(c) == 127 for c in segment),
                     'Unsafe artifact path')
            decoded = unquote(segment)
            if decoded == segment:
                break
            segment = decoded


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'Duplicate JSON keys')
        result[key] = value
    return result


def _validate_unicode(record):
    """Reject malformed decoded Unicode before it reaches UTF-8 publications."""
    pending = [record]
    while pending:
        value = pending.pop()
        if isinstance(value, str):
            try:
                value.encode('utf-8', errors='strict')
            except UnicodeEncodeError:
                raise ValueError('Invalid record Unicode') from None
        elif isinstance(value, dict):
            pending.extend(value.keys())
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)


def _validate(record):
    _require(isinstance(record, dict), 'Record must be a JSON object')
    kind = record.get('kind')
    _require(isinstance(kind, str) and kind in _FIELDS and set(record) == _FIELDS[kind])
    if kind == 'question':
        needs = record['needs']
        _require(isinstance(needs, list) and all(isinstance(n, str) and n in _NEEDS for n in needs) and len(set(needs)) == len(needs), 'Invalid requested needs')
    if kind in ('intent', 'contribution'):
        _require(_number(record['question']), 'Invalid question reference')
    if kind == 'intent':
        _require(_text(record['scope']), 'Intent scope is required')
        _date(record['expires_at'])
    if kind in ('contribution', 'review', 'reuse'):
        _require(isinstance(record['artifact_version'], str) and _VERSION.fullmatch(record['artifact_version']) is not None, 'Invalid artifact version')
    if kind == 'contribution':
        _require(record['supersedes'] is None or _number(record['supersedes']), 'Invalid supersession reference')
    if kind in ('contribution', 'review', 'reuse'):
        url = _url(record['artifact_url'])
        parts = url.path.split('/')
        _artifact_path(parts)
        _require(url.netloc == 'github.com' and '?' not in record['artifact_url'] and '#' not in record['artifact_url'] and len(parts) >= 5 and parts[1] not in ('', '.', '..') and parts[2] not in ('', '.', '..') and parts[3] in ('blob', 'tree', 'commit') and parts[4] == record['artifact_version'], 'Invalid fixed GitHub artifact URL')
    if kind in ('review', 'reuse'):
        _require(_number(record['contribution']), 'Invalid contribution reference')
    if kind == 'review':
        _require(record['affiliation'] in ('same_operator', 'different_operator', 'unknown'), 'Invalid affiliation disclosure')
        checks = record['checks']
        _require(isinstance(checks, dict) and set(checks) == _CHECKS, 'All four review checks are required')
        for check in checks.values():
            _require(isinstance(check, dict) and set(check) == {'verdict', 'evidence'}, 'Invalid review check')
            _require(check['verdict'] in ('supported', 'concerns', 'not_checked') and isinstance(check['evidence'], str), 'Invalid review check')
            _require(check['verdict'] == 'not_checked' or _text(check['evidence']), 'Review evidence is required')
    if kind == 'reuse':
        _require(_text(record['outcome']), 'Reuse outcome is required')
        _url(record['evidence_url'])


def _parse(body):
    markers = list(_MARKER_LINE.finditer(body))
    if not markers:
        return None
    _require(len(markers) == 1, 'Exactly one record marker is required')
    block = _BLOCK.search(body)
    _require(block is not None and block.start() == markers[0].start(), 'Record marker must precede one JSON fence')
    try:
        record = json.loads(block.group(1), object_pairs_hook=_pairs,
                            parse_constant=lambda value: _require(False, 'Invalid JSON value'))
    except (ValueError, RecursionError):
        raise ValueError('Invalid record JSON') from None
    _validate_unicode(record)
    _validate(record)
    return record, block.span()


def display_body(body):
    """Remove validated metadata only; the HTML renderer must escape prose."""
    try:
        parsed = _parse(body)
    except (ValueError, TypeError, RecursionError):
        return body
    if parsed is None:
        return body
    start, end = parsed[1]
    return body[:start] + body[end:]


def derive(posts, generated_at):
    """Resolve optional records using snapshot time, without mutating sources."""
    now = _date(generated_at)
    records = []
    states = {}
    for post in sorted(posts, key=lambda p: p['number']):
        try:
            parsed = _parse(post['body'])
            if parsed is None:
                continue
            record = parsed[0]
            error = None
        except (ValueError, TypeError, RecursionError) as exc:
            record = {}
            error = str(exc) if isinstance(exc, ValueError) else 'Invalid record fields'
        item = dict(issue=post['number'], author=post['author'], kind=record.get('kind', 'invalid'),
                    record=record, valid=error is None, error=error, active=False, same_account=False)
        records.append(item)
        states[item['issue']] = post['state']
    by_issue = {r['issue']: r for r in records}

    def reject(item, reason):
        item.update(valid=False, active=False, error=reason)

    def target(item, number, kind):
        other = by_issue.get(number)
        if other is None or not other['valid'] or other['kind'] != kind:
            reject(item, 'Unresolved ' + kind + ' reference')
            return None
        return other

    for kind in ('question', 'intent', 'contribution', 'review', 'reuse'):
        for item in records:
            if not item['valid'] or item['kind'] != kind:
                continue
            record = item['record']
            if kind in ('intent', 'contribution'):
                if target(item, record['question'], 'question') is None:
                    continue
            if kind == 'contribution' and record['supersedes'] is not None:
                previous = target(item, record['supersedes'], 'contribution')
                if previous is None:
                    continue
                if previous['issue'] >= item['issue'] or previous['author'].casefold() != item['author'].casefold() or previous['record']['question'] != record['question']:
                    reject(item, 'Invalid supersession authority or order')
                    continue
            if kind in ('review', 'reuse'):
                previous = target(item, record['contribution'], 'contribution')
                if previous is None:
                    continue
                item['same_account'] = previous['author'].casefold() == item['author'].casefold()
                if (previous['record']['artifact_version'] != record['artifact_version']
                        or previous['record']['artifact_url'] != record['artifact_url']):
                    reject(item, 'Artifact URL or version does not match contribution')
                    continue
            item['active'] = states[item['issue']] == 'open'
            if kind == 'intent':
                item['active'] = item['active'] and _date(record['expires_at']) > now

    timelines = {}
    profiles = {}
    for item in records:
        if not item['valid']:
            continue
        kind, record = item['kind'], item['record']
        question = item['issue'] if kind == 'question' else (record['question'] if kind in ('intent', 'contribution') else by_issue[record['contribution']]['record']['question'])
        timelines.setdefault(str(question), []).append(item['issue'])
        if kind in ('contribution', 'review', 'reuse'):
            profile = profiles.setdefault(item['author'], dict(author=item['author'], contributions=[], reviews=[], reuse=[]))
            profile[{'contribution': 'contributions', 'review': 'reviews', 'reuse': 'reuse'}[kind]].append(item['issue'])
    needs = []
    for item in records:
        if item['kind'] == 'question' and item['valid'] and item['active']:
            intents = [r['issue'] for r in records if r['kind'] == 'intent' and r['valid'] and r['active'] and r['record']['question'] == item['issue']]
            for need in item['record']['needs']:
                needs.append(dict(question=item['issue'], need=need, intents=list(intents)))
    return dict(records=records, needs=needs, timelines=timelines,
                profiles=[profiles[a] for a in sorted(profiles)],
                warnings=[dict(issue=r['issue'], error=r['error']) for r in records if not r['valid']])
