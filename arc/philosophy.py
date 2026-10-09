"""Publish the project philosophy from a single repository-owned document."""
import html
import json
from pathlib import Path
from arc.languages import language


def render(path):
    document = path if isinstance(path, dict) else json.loads(Path(path).read_text(encoding='utf-8'))
    esc = html.escape
    body = '<div class="page-head"><p class="eyebrow">OPERATING PHILOSOPHY / {}</p><h1>{}</h1><p>{}</p></div>'.format(esc(document['version']), esc(document['title']), esc(document['summary']))
    body += '<div class="report-tools"><span>Project review baseline · {}</span><a href="philosophy.md">Markdown ↗</a><a href="index.json">JSON ↗</a></div><article class="prose report-prose">'.format(esc(document['adopted_on']))
    lines = ['# ' + document['title'], '', document['summary'], '', 'Version: ' + document['version'], '', 'Project review baseline · ' + document['adopted_on'], '']
    for section in document['sections']:
        title = section['id'] + ' · ' + section['title']
        body += '<section id="{}" lang="{}"><h2>{}</h2>'.format(esc(section['id'], quote=True), language(section['paragraphs']), esc(title))
        lines += ['## ' + title, '']
        for paragraph in section['paragraphs']:
            body += '<p>{}</p>'.format(esc(paragraph))
            lines += [paragraph, '']
        body += '</section>'
    body += '<h2>Version history</h2>'
    lines += ['## Version history', '']
    for change in document['changes']:
        text = change['date'] + ' · ' + change['text']
        body += '<p>{}</p>'.format(esc(text))
        lines += [text, '']
    body += '<p><a href="../rules/index.html">Governance draft ↗</a> · <a href="../guide.md">Current collaboration protocol ↗</a></p></article>'
    lines += ['[Governance draft](../rules/index.html) · [Current collaboration protocol](../guide.md)', '']
    return body, '\n'.join(lines), {**document, 'html': 'index.html', 'markdown': 'philosophy.md'}
