"""Read opt-in community issues without granting official task authority."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile

from .github import GitHub

MARKER = '<!-- arc-community:v1 -->'
_LOGIN = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?(?:\[bot\])?')
_DATE = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
_FIELDS = {'number', 'title', 'body', 'author', 'state', 'created_at',
           'updated_at', 'url', 'comments'}


def _repository(repository):
    if not isinstance(repository, str):
        raise ValueError('Invalid community repository')
    GitHub(repository)
    if any(part in ('.', '..') for part in repository.split('/')):
        raise ValueError('Invalid community repository')


def _date(value):
    if not isinstance(value, str) or not _DATE.fullmatch(value):
        raise ValueError('Invalid community timestamp')
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise ValueError('Invalid community timestamp') from None


def _post(post, repository):
    if not isinstance(post, dict) or set(post) != _FIELDS:
        raise ValueError('Invalid community post fields')
    if type(post['number']) is not int or post['number'] <= 0:
        raise ValueError('Invalid community issue number')
    if not isinstance(post['title'], str) or not isinstance(post['body'], str):
        raise ValueError('Invalid community text')
    if not isinstance(post['author'], str) or not _LOGIN.fullmatch(post['author']):
        raise ValueError('Invalid community author')
    if post['state'] not in ('open', 'closed'):
        raise ValueError('Invalid community state')
    if type(post['comments']) is not int or post['comments'] < 0:
        raise ValueError('Invalid community comment count')
    _date(post['created_at'])
    _date(post['updated_at'])
    if post['url'] != 'https://github.com/{}/issues/{}'.format(repository, post['number']):
        raise ValueError('Invalid community issue URL')


def validate_snapshot(snapshot, repository):
    """Return validated posts, raising ValueError on any invalid saved record."""
    _repository(repository)
    if (not isinstance(snapshot, dict)
            or set(snapshot) != {'repository', 'generated_at', 'posts'}
            or snapshot['repository'] != repository
            or not isinstance(snapshot['posts'], list)):
        raise ValueError('Invalid community snapshot')
    _date(snapshot['generated_at'])
    seen = set()
    for post in snapshot['posts']:
        _post(post, repository)
        if post['number'] in seen:
            raise ValueError('Duplicate community issue')
        seen.add(post['number'])
    return snapshot['posts']


def _parse_issue(issue, repository):
    if not isinstance(issue, dict) or 'pull_request' in issue:
        return None
    labels = issue.get('labels')
    if (not isinstance(labels, list)
            or any(not isinstance(label, dict) or not isinstance(label.get('name'), str)
                   for label in labels)):
        return None
    if any(label['name'] in ('arc:task', 'community:hidden') for label in labels):
        return None
    body = issue.get('body')
    if not isinstance(body, str):
        return None
    # Only LF/CRLF delimit GitHub Markdown lines; whitespace is not opt-in.
    marker_line = re.compile(r'^' + re.escape(MARKER) + r'(?:\r?\n|$)', re.MULTILINE)
    if not marker_line.search(body):
        return None
    user = issue.get('user')
    if not isinstance(user, dict):
        return None
    post = {field: issue.get(field) for field in _FIELDS}
    post['author'] = user.get('login')
    post['body'] = marker_line.sub('', body)
    post['url'] = 'https://github.com/{}/issues/{}'.format(repository, issue.get('number'))
    try:
        _post(post, repository)
    except ValueError:
        return None
    return post


def fetch_snapshot(repository):
    """Fetch every issue page. API errors never become an empty snapshot."""
    _repository(repository)
    github = GitHub(repository)
    posts = []
    seen = set()
    page = 1
    while True:
        batch = github.api('repos/{}/issues?state=all&per_page=100&page={}'.format(repository, page))
        if not isinstance(batch, list):
            raise ValueError('Invalid community issue listing')
        for issue in batch:
            post = _parse_issue(issue, repository)
            if post is not None and post['number'] not in seen:
                posts.append(post)
                seen.add(post['number'])
        if len(batch) < 100:
            break
        page += 1
    snapshot = dict(repository=repository,
                    generated_at=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    posts=posts)
    validate_snapshot(snapshot, repository)
    return snapshot


def sync(repository, output):
    """Atomically replace the local snapshot after a complete successful fetch."""
    snapshot = fetch_snapshot(repository)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent,
                                         prefix='.' + output.name + '.', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(snapshot, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return snapshot


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    snapshot = sync(args.repo, args.output)
    print('Synced {} community posts → {}'.format(len(snapshot['posts']), args.output))


if __name__ == '__main__':
    main()
