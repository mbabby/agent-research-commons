"""Render the public governance draft; this module never grants permissions."""
import html
import json
from pathlib import Path
from arc.languages import language


def render(path, repository):
    document = path if isinstance(path, dict) else json.loads(Path(path).read_text(encoding='utf-8'))
    # This publication phase does not implement active governance or its migration.
    if document['status'] != 'draft' or document['effective_at'] is not None:
        raise ValueError('Governance publication only supports an inactive draft')
    esc = html.escape
    version = document['version']
    proposal = document['proposal_url']
    if not proposal.startswith('https://github.com/'):
        raise ValueError('Governance proposal must link to a GitHub record')
    discussion = 'https://github.com/{}/issues/new'.format(repository)
    body = '<div class="page-head"><p class="eyebrow">OPEN GOVERNANCE / {}</p><h1>Rules & governance</h1><p>Open participation, recognition through contribution and rules open to discussion.</p></div>'.format(esc(version))
    body += '<div class="notice"><strong>Public draft · Not in effect</strong><p>The current v1 collaboration protocol still applies. This publication does not grant automated governance permissions.</p><a href="../guide.md">Read the current protocol ↗</a></div>'
    body += '<div class="report-tools"><span>Version {} · Effective date: not in effect</span><a href="rules.md">Download Markdown ↗</a><a href="index.json">Read JSON ↗</a></div>'.format(esc(version))
    body += '<p>Rule discussions and implementation use the <a href="../philosophy/index.html">operating philosophy</a> as the project review baseline. The governance draft is not in effect.</p>'
    body += '<article class="prose report-prose">'
    lines = ['# ' + document['title'], '', 'Version: ' + version, '', 'Status: public draft, not in effect. Effective date: none.', '', 'Current protocol: [Collaboration protocol v1](../guide.md)', '']
    lines += ['Project review baseline: [Operating philosophy](../philosophy/index.html). The governance draft is not in effect.', '']
    for section in document['sections']:
        body += '<section lang="{}"><h2>{}</h2>'.format(language(section['paragraphs']), esc(section['title']))
        lines += ['## ' + section['title'], '']
        for paragraph in section['paragraphs']:
            body += '<p>{}</p>'.format(esc(paragraph))
            lines += [paragraph, '']
        body += '</section>'
    body += '<h2>Version history</h2><ul>'
    lines += ['## Version history', '']
    for change in document['changes']:
        text = change['date'] + ' · ' + change['text']
        body += '<li>{}</li>'.format(esc(text))
        lines += ['- ' + text]
    body += '</ul><p><a href="{}">Original design proposal ↗</a></p><a class="button" href="{}">Suggest a rule change ↗</a></article>'.format(esc(proposal, quote=True), esc(discussion, quote=True))
    lines += ['', '[Original design proposal](' + proposal + ')', '', '[Suggest a rule change](' + discussion + ')', '']
    index = {'schema_version': 1, 'status': document['status'], 'effective_at': document['effective_at'],
             'current_protocol': '../guide.md', 'discussion_url': discussion,
             'versions': [{**document, 'html': 'index.html', 'markdown': 'rules.md'}]}
    return body, '\n'.join(lines), index
