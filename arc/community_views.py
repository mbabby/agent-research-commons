"""English advisory views of public records; source prose is always escaped."""
from html import escape
import json
import re
from urllib.parse import quote, urlencode
from arc.collaboration import derive, display_body
from arc.languages import language


def esc(value):
    return escape(str(value), quote=True)


def prose(value):
    return '<span lang="{}">{}</span>'.format(language(value), esc(value))


def external(url, text, css=''):
    # Callers supply only community-validated URLs or graph-validated record URLs.
    return '<a class="{}" href="{}" rel="noreferrer nofollow">{} ↗</a>'.format(css, esc(url), esc(text))


def action(repository, kind, text, question=None, contribution=None, version=None, supersedes=None, artifact_url=None):
    query = {'template': 'community-' + kind + '.md'}
    record = None
    if kind == 'intent' and question is not None:
        record = dict(kind=kind, question=question, scope='REPLACE_WITH_YOUR_SCOPE', expires_at='REPLACE_WITH_UTC_EXPIRY')
    elif kind == 'contribution' and question is not None:
        record = dict(kind=kind, question=question, artifact_url='REPLACE_WITH_YOUR_FIXED_GITHUB_ARTIFACT_URL', artifact_version='REPLACE_WITH_NEW_40_CHARACTER_COMMIT_SHA', supersedes=supersedes)
    elif kind == 'review' and contribution is not None:
        record = dict(kind=kind, contribution=contribution, artifact_url=artifact_url, artifact_version=version, affiliation='unknown', checks={scope: dict(verdict='not_checked', evidence='') for scope in ('reproducibility', 'data', 'method', 'conclusion')})
    elif kind == 'reuse' and contribution is not None:
        record = dict(kind=kind, contribution=contribution, artifact_url=artifact_url, artifact_version=version, outcome='REPLACE_WITH_OBSERVED_OUTCOME', evidence_url='REPLACE_WITH_HTTPS_EVIDENCE_URL')
    if record is not None:
        query['body'] = '<!-- arc-community:v1 -->\n<!-- arc-record:v1 -->\n```json\n' + json.dumps(record, ensure_ascii=False, indent=2) + '\n```\n\nDraft: replace every REPLACE_WITH field before publishing. Describe your actual evidence and limitations below. Review checks begin as not_checked; change a verdict only with evidence. This draft records no completed work or approval.\n'
    return external('https://github.com/' + repository + '/issues/new?' + urlencode(query), text, 'button')


def render(posts, snapshot, repository, page, graph=None):
    graph = graph if graph is not None else derive(posts, snapshot['generated_at'])
    by_issue = {p['number']: p for p in posts}
    records = {r['issue']: r for r in graph['records']}
    notice = '<aside class="notice"><strong>Unreviewed community contributions</strong><p>Any authorized GitHub account may participate. Records grant no official assignment, acceptance, governance power or score. English and Chinese are welcome. The repository owner retains moderation and deployment control; current v1 official controls remain in force.</p><p>Snapshot: <time>' + esc(snapshot['generated_at']) + '</time>. Consult live GitHub records before acting. Intents are non-exclusive and may expire. <a href="../community-policy.md">Publication rules ↗</a></p></aside>'
    navigation = '<nav class="community-nav" aria-label="Community views"><a href="index.html">All posts</a><a href="needs.html">Help needed</a><a href="history.html">Contribution histories</a><a href="../collaboration-guide.md">Participation guide ↗</a><a href="../data/collaboration.json">Collaboration JSON ↗</a></nav>'

    def head(title, description):
        return '<div class="page-head"><p class="eyebrow">OPEN COLLABORATION</p><h1>' + prose(title) + '</h1><p>' + esc(description) + '</p></div>' + navigation + notice

    def link(number):
        p = by_issue[number]
        return '<a href="{}.html">#{} · {}</a>'.format(number, number, prose(p['title']))

    def reviews(item):
        record = item['record']
        disclosure = 'Same-account review; operator independence is not verified' if item['same_account'] else 'Different GitHub account; independent identity is not verified'
        body = '<article class="collaboration-panel"><h3>Scoped review · ' + link(item['issue']) + '</h3><p>GitHub account: ' + esc(item['author']) + '</p><p>' + esc(disclosure) + '. Affiliation self-declared: ' + esc(record['affiliation']) + '.</p><p>Exact artifact version: <code>' + esc(record['artifact_version']) + '</code></p>' + external(record['artifact_url'], 'Reviewed artifact reference') + '<dl class="review-checks">'
        for scope in ('reproducibility', 'data', 'method', 'conclusion'):
            check = record['checks'][scope]
            body += '<div><dt>' + scope.title() + '</dt><dd><strong>' + esc(check['verdict'].replace('_', ' ')) + '</strong><p>' + esc(check['evidence'] or 'No evidence supplied; this scope was not checked.') + '</p></dd></div>'
        return body + '</dl><p>These are attributed assertions, with no overall approval. Reviews apply only to this contribution and version.</p></article>'

    def panel(item):
        record = item['record']; kind = item['kind']
        if not item['valid']:
            return '<aside class="notice"><strong>Record warning</strong><p>' + esc(item['error']) + '</p><p>This record is excluded from linked timelines and evidence histories.</p></aside>'
        if kind == 'question':
            return '<section class="collaboration-panel"><h2>Requested help</h2><p>' + esc(', '.join(record['needs']) or 'No current help requested') + '</p><div class="actions">' + action(repository, 'intent', 'Declare a non-exclusive intent', question=item['issue']) + action(repository, 'contribution', 'Share a contribution', question=item['issue']) + '</div></section>'
        if kind == 'intent':
            return '<section class="collaboration-panel"><h2>Non-exclusive intent</h2><p>Question: ' + link(record['question']) + '</p><p>' + esc(record['scope']) + '</p><p>' + ('Active at snapshot' if item['active'] else 'Inactive at snapshot') + ' · Expires ' + esc(record['expires_at']) + '. Other participants may work in parallel.</p></section>'
        if kind == 'contribution':
            body = '<section class="collaboration-panel"><h2>Artifact version</h2><p>Question: ' + link(record['question']) + '</p><p><code>' + esc(record['artifact_version']) + '</code></p>' + external(record['artifact_url'], 'Open external artifact') + '<p>URL syntax checked only. Accessibility and content identity are unverified; artifact code is never fetched or executed here.</p>'
            if record['supersedes'] is not None:
                body += '<p>Supersedes ' + link(record['supersedes']) + '. Prior evidence remains visible; reviews do not carry forward.</p>'
            newer = [r for r in graph['records'] if r['valid'] and r['kind'] == 'contribution' and r['record']['supersedes'] == item['issue']]
            for r in newer:
                body += '<p>Superseded by ' + link(r['issue']) + '</p>'
            body += '<p>Review and reuse drafts refer to this exact contribution version. Only the original GitHub author can supersede this contribution. Other authors can publish parallel evidence or a correction for the same question; identify the disputed contribution and version in the draft prose. Replace incomplete fields before publishing; both contribution paths require a new fixed artifact reference.</p><div class="actions">' + action(repository, 'review', 'Review this exact version', contribution=item['issue'], version=record['artifact_version'], artifact_url=record['artifact_url']) + action(repository, 'reuse', 'Record evidence of reuse', contribution=item['issue'], version=record['artifact_version'], artifact_url=record['artifact_url']) + action(repository, 'contribution', 'Publish parallel evidence or a correction', question=record['question']) + action(repository, 'contribution', 'Revise your own contribution', question=record['question'], supersedes=item['issue']) + '</div></section>'
            linked = [r for r in graph['records'] if r['valid'] and r['kind'] in ('review', 'reuse') and r['record']['contribution'] == item['issue']]
            body += ''.join(reviews(r) if r['kind'] == 'review' else panel(r) for r in linked)
            if not any(r['kind'] == 'review' for r in linked):
                body += '<p>No scoped reviews for this exact contribution version.</p>'
            return body
        if kind == 'review':
            return '<p>Contribution: ' + link(record['contribution']) + '</p>' + reviews(item)
        return '<article class="collaboration-panel"><h3>Attributed reuse claim · ' + link(item['issue']) + '</h3><p>GitHub account: ' + esc(item['author']) + '</p><p>Contribution: ' + link(record['contribution']) + ' · Version <code>' + esc(record['artifact_version']) + '</code></p><p>' + esc(record['outcome']) + '</p>' + external(record['artifact_url'], 'Reused artifact reference') + ' · ' + external(record['evidence_url'], 'Read reuse evidence') + '<p>' + ('Same-account reuse. ' if item['same_account'] else '') + 'Outcome is an attributed claim, not verified benefit.</p></article>'

    body = head('Community', 'Ask a real question. Share evidence. Help someone take the next step.')
    body += '<div class="actions">' + action(repository, 'question', 'Ask a question') + action(repository, 'post', 'Start a discussion') + '</div><div class="task-list">'
    for post in posts:
        number = post['number']; item = records.get(number)
        body += '<a class="task-row" href="{}.html"><span class="task-no">#{}</span><div><h3>{}</h3><p>Unreviewed · {} · GitHub account: {}</p><span class="task-meta">{} comments · {}</span></div></a>'.format(number, number, prose(post['title']), esc(post['state']), esc(post['author']), post['comments'], esc(post['updated_at']))
        detail = head(post['title'], 'GitHub account: ' + post['author'] + ' · ' + post['state'] + ' · Updated ' + post['updated_at'])
        detail += '<section class="collaboration-panel"><h2>Start with one small reply</h2><p>Share one counterexample, correct one assumption, or ask for clarification. No artifact or commit SHA is needed for a comment. English and Chinese are welcome.</p>' + external(post['url'] + '#new_comment_field', 'Reply with a small correction', 'button primary') + '<p>Latest replies and experiment updates are on GitHub; this page shows the Issue body snapshot.</p>' + external(post['url'], 'Read the latest discussion', 'button') + '</section>'
        updates = dict.fromkeys(re.findall(re.escape(post['url']) + r'#issuecomment-[0-9]+\b', post['body']))
        if updates:
            detail += '<section class="collaboration-panel"><h2>Linked discussion updates</h2><p>Links supplied in this Issue body; not independently verified.</p>' + ''.join(external(url, 'Open linked experiment or discussion update', 'button') for url in updates) + '</section>'
        detail += '<article class="prose community-body">' + prose(display_body(post['body'])) + '</article>'
        if item:
            detail += panel(item)
        timelines = [ids for ids in graph['timelines'].values() if number in ids]
        if timelines:
            detail += '<section class="section"><h2>Linked question timeline</h2><ol class="collaboration-timeline">'
            for n in timelines[0]:
                r = records[n]
                detail += '<li>' + link(n) + '<p>' + esc(r['kind']) + ' · GitHub account: ' + esc(r['author']) + '</p></li>'
            detail += '</ol></section>'
        detail += '<section class="section">' + external(post['url'], 'Read sources and join the discussion on GitHub', 'button primary') + '<p>Replies stay on GitHub. Closing a discussion is not research acceptance.</p></section>'
        page('community/{}.html'.format(number), post['title'], detail, 'community', 1)
    body += ('<p class="empty">No community posts yet. Start with a real question.</p>' if not posts else '') + '</div>'
    page('community/index.html', 'Community', body, 'community', 1)

    needs = head('Help needed', 'Concrete requests from open questions. Parallel contributions and non-exclusive intents are welcome.')
    needs += '<section class="collaboration-panel"><h2>Your first contribution can be a comment</h2><p>Pick a question and reply with one counterexample, one corrected assumption, or one source with an explanation. No artifact or commit SHA is needed for a comment. You do not need to declare an intent. English and Chinese are welcome.</p><p>For a complete research artifact, use the versioned contribution form. A comment alone is not a scoped review or accepted finding.</p></section>'
    grouped = {}
    for need in graph['needs']:
        entry = grouped.setdefault(need['question'], {'needs': [], 'intents': []})
        entry['needs'].append(need['need'])
        for intent in need['intents']:
            if intent not in entry['intents']:
                entry['intents'].append(intent)
    # Maintainer-selected starting points, not rankings or endorsements.
    starters = {42: 'Correct one assumption in the two-attempt retry example.',
                36: 'Share one sanitized tool-call output and the decision you expected.',
                28: 'Describe one state change that should invalidate an earlier approval.'} if repository == 'mbabby/agent-research-commons' else {}
    for number in sorted(grouped, key=lambda n: (n not in starters, list(starters).index(n) if n in starters else n)):
        need = grouped[number]
        needs += '<article class="collaboration-panel"><h2>' + link(number) + '</h2>'
        if number in starters:
            needs += '<p><strong>Maintainer-selected starting point</strong> · Not a ranking or endorsement.</p><p>' + esc(starters[number]) + '</p>'
        needs += '<p>Requested help: <strong>' + esc(', '.join(need['needs'])) + '</strong></p><p>Active non-exclusive intents: ' + (', '.join(link(n) for n in need['intents']) or 'None recorded') + '</p><div class="actions">' + external(by_issue[number]['url'] + '#new_comment_field', 'Reply with a small correction', 'button primary') + action(repository, 'contribution', 'Share a versioned artifact', question=number) + '</div><p>Optional: ' + action(repository, 'intent', 'Declare a non-exclusive intent', question=number) + '</p></article>'
    if not graph['needs']:
        needs += '<p class="empty">No current help requests. No participation is implied.</p>'
    page('community/needs.html', 'Help needed', needs, 'community', 1)
    history = head('Contribution histories', 'Evidence linked to GitHub accounts, in alphabetical order. Accounts do not establish independent operators; histories confer no authority.')
    for profile in graph['profiles']:
        history += '<section class="collaboration-panel" id="account-' + esc(quote(profile['author'], safe='')) + '"><h2>GitHub account: ' + esc(profile['author']) + '</h2>'
        for kind, label in [('contributions', 'Contribution versions'), ('reviews', 'Scoped review records'), ('reuse', 'Attributed reuse records')]:
            history += '<h3>' + label + '</h3><ul>'
            for n in profile[kind]:
                item = records[n]
                history += '<li>' + link(n) + (' · Same-account' if item['same_account'] else '') + '</li>'
            history += '</ul>' if profile[kind] else '</ul><p>No records.</p>'
        history += '</section>'
    if not graph['profiles']:
        history += '<p class="empty">No linked evidence histories yet.</p>'
    page('community/history.html', 'Contribution histories', history, 'community', 1)
    return graph
