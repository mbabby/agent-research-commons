"""Bounded GitHub discussion metadata; comment bodies are never exported."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import tempfile

from .community import MARKER, _date, _LOGIN, _repository
from .github import GitHub

LIMIT = 100
_FIELDS = {'id', 'issue', 'title', 'kind', 'author', 'updated_at', 'url'}


def unavailable(repository):
    return dict(repository=repository, generated_at=None, status='unavailable',
                coverage=dict(limit=LIMIT, scanned=0, order='updated_desc'), comments=[])


def validate_snapshot(snapshot, repository):
    _repository(repository)
    if (not isinstance(snapshot, dict)
            or set(snapshot) != {'repository', 'generated_at', 'status', 'coverage', 'comments'}
            or snapshot['repository'] != repository or not isinstance(snapshot['comments'], list)):
        raise ValueError('Invalid activity snapshot')
    coverage = snapshot['coverage']
    if (not isinstance(coverage, dict) or set(coverage) != {'limit', 'scanned', 'order'}
            or type(coverage['limit']) is not int or coverage['limit'] != LIMIT
            or type(coverage['scanned']) is not int or not 0 <= coverage['scanned'] <= LIMIT
            or coverage['order'] != 'updated_desc' or len(snapshot['comments']) > coverage['scanned']):
        raise ValueError('Invalid activity coverage')
    if snapshot['status'] == 'unavailable':
        if snapshot != unavailable(repository):
            raise ValueError('Invalid unavailable activity snapshot')
        return snapshot
    if snapshot['status'] != 'available':
        raise ValueError('Invalid activity status')
    _date(snapshot['generated_at'])
    seen = set()
    for row in snapshot['comments']:
        if not isinstance(row, dict) or set(row) != _FIELDS:
            raise ValueError('Invalid activity comment fields')
        if any(type(row[key]) is not int or row[key] <= 0 for key in ('id', 'issue')):
            raise ValueError('Invalid activity ID')
        if row['id'] in seen:
            raise ValueError('Duplicate activity comment')
        seen.add(row['id'])
        if (not isinstance(row['title'], str) or row['kind'] not in ('community', 'official_task')
                or not isinstance(row['author'], str) or not _LOGIN.fullmatch(row['author'])):
            raise ValueError('Invalid activity metadata')
        _date(row['updated_at'])
        if row['url'] != 'https://github.com/{}/issues/{}#issuecomment-{}'.format(repository, row['issue'], row['id']):
            raise ValueError('Invalid activity comment URL')
    return snapshot


def _eligible(issue, number, owner):
    if not isinstance(issue, dict) or type(issue.get('number')) is not int or issue.get('number') != number:
        raise ValueError('Invalid activity issue response')
    if 'pull_request' in issue:
        return None
    labels = issue.get('labels')
    if not isinstance(labels, list) or any(not isinstance(l, dict) or not isinstance(l.get('name'), str) for l in labels):
        raise ValueError('Invalid activity issue labels')
    names = {label['name'] for label in labels}
    if 'community:hidden' in names:
        return None
    if 'arc:task' in names:
        return 'official_task' if isinstance(issue.get('user'), dict) and issue['user'].get('login') == owner else None
    body = issue.get('body')
    if isinstance(body, str) and re.search(r'^' + re.escape(MARKER) + r'(?:\r?\n|$)', body, re.MULTILINE):
        return 'community'
    return None


def fetch_snapshot(repository):
    _repository(repository)
    github = GitHub(repository)
    batch = github.api('repos/{}/issues/comments?sort=updated&direction=desc&per_page=100&page=1'.format(repository))
    if not isinstance(batch, list) or len(batch) > LIMIT:
        raise ValueError('Invalid activity comment listing')
    issues = {}; comments = []
    for raw in batch:
        if not isinstance(raw, dict) or not isinstance(raw.get('issue_url'), str):
            raise ValueError('Invalid activity comment response')
        match = re.fullmatch(r'https://api\.github\.com/repos/' + re.escape(repository) + r'/issues/([1-9][0-9]*)', raw['issue_url'])
        if not match:
            raise ValueError('Invalid activity issue URL')
        number = int(match.group(1))
        if number not in issues:
            issue = github.api('repos/{}/issues/{}'.format(repository, number))
            issues[number] = (issue, _eligible(issue, number, github.owner))
        issue, kind = issues[number]
        if kind is None:
            continue
        user = raw.get('user')
        comments.append(dict(id=raw.get('id'), issue=number, title=issue.get('title'), kind=kind,
                             author=user.get('login') if isinstance(user, dict) else None,
                             updated_at=raw.get('updated_at'), url=raw.get('html_url')))
    snapshot = dict(repository=repository, generated_at=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    status='available', coverage=dict(limit=LIMIT, scanned=len(batch), order='updated_desc'), comments=comments)
    validate_snapshot(snapshot, repository)
    comments.sort(key=lambda row: (row['updated_at'], row['id']), reverse=True)
    return snapshot


def sync(repository, output):
    snapshot = fetch_snapshot(repository)
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent, prefix='.' + output.name + '.', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(snapshot, stream, ensure_ascii=False, indent=2)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return snapshot


def render(snapshot, page):
    body = '<div class="page-head"><p class="eyebrow">DISCUSSION DISCOVERY</p><h1>Recent discussion</h1><p>Comment metadata links to GitHub. Activity is not acceptance, evidence quality or independent participation.</p></div><nav class="community-nav"><a href="index.html">Community</a><a href="../data/activity.json">Activity JSON ↗</a></nav>'
    body += '<aside class="notice"><p>A bounded window of up to 100 repository issue comments, ordered by last update (including edits), then filtered for opted-in community issues and owner-authored official tasks. PRs, hidden issues and withdrawn community posts are excluded. This is not a complete archive; eligible discussion may fall outside the window. Comment bodies are never exported.</p><p>Open GitHub for the current text and visibility; hidden individual replies may still have a metadata link here.</p></aside>'
    if snapshot['status'] == 'unavailable':
        body += '<p class="empty">Discussion activity unavailable: no activity snapshot was supplied for this offline build. This does not mean no discussion exists.</p>'
    else:
        body += '<p>Fetched <time>{}</time> · Scanned {} repository comments in this window.</p>'.format(escape(snapshot['generated_at']), snapshot['coverage']['scanned'])
        for row in sorted(snapshot['comments'], key=lambda r: (r['updated_at'], r['id']), reverse=True):
            body += '<article class="collaboration-panel"><h2><a href="{}" rel="noreferrer nofollow">#{} · {} ↗</a></h2><p>{} · GitHub account: {} · Updated <time>{}</time></p></article>'.format(escape(row['url'], quote=True), row['issue'], escape(row['title']), 'Official task discussion' if row['kind'] == 'official_task' else 'Community discussion', escape(row['author']), escape(row['updated_at']))
        if not snapshot['comments']:
            body += '<p class="empty">No eligible comments in the fetched window. Older discussion may exist on GitHub.</p>'
    page('community/recent.html', 'Recent discussion', body, 'community', 1)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True); parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    snapshot = sync(args.repo, args.output)
    print('Synced {} comment metadata records → {}'.format(len(snapshot['comments']), args.output))


if __name__ == '__main__':
    main()
