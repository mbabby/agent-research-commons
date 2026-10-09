"""Publish the project philosophy from a single repository-owned document."""
import html
import json
from pathlib import Path


def render(path):
    document = json.loads(Path(path).read_text(encoding='utf-8'))
    esc = html.escape
    body = '<div class="page-head"><p class="eyebrow">OPERATING PHILOSOPHY / {}</p><h1>{}</h1><p>{}</p></div>'.format(esc(document['version']), esc(document['title']), esc(document['summary']))
    body += '<div class="report-tools"><span>项目审查基准 · {}</span><a href="philosophy.md">Markdown ↗</a><a href="index.json">JSON ↗</a></div><article class="prose report-prose">'.format(esc(document['adopted_on']))
    lines = ['# ' + document['title'], '', document['summary'], '', '版本：' + document['version'], '', '项目审查基准 · ' + document['adopted_on'], '']
    for section in document['sections']:
        title = section['id'] + ' · ' + section['title']
        body += '<section id="{}"><h2>{}</h2>'.format(esc(section['id'], quote=True), esc(title))
        lines += ['## ' + title, '']
        for paragraph in section['paragraphs']:
            body += '<p>{}</p>'.format(esc(paragraph))
            lines += [paragraph, '']
        body += '</section>'
    body += '<h2>版本记录</h2>'
    lines += ['## 版本记录', '']
    for change in document['changes']:
        text = change['date'] + ' · ' + change['text']
        body += '<p>{}</p>'.format(esc(text))
        lines += [text, '']
    body += '<p><a href="../rules/index.html">规则与治理草案 ↗</a> · <a href="../guide.md">现行协作协议 ↗</a></p></article>'
    lines += ['[规则与治理草案](../rules/index.html) · [现行协作协议](../guide.md)', '']
    return body, '\n'.join(lines), {**document, 'html': 'index.html', 'markdown': 'philosophy.md'}
