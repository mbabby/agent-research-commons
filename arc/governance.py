"""Render the public governance draft; this module never grants permissions."""
import html
import json
from pathlib import Path


def render(path, repository):
    document = json.loads(Path(path).read_text(encoding='utf-8'))
    # This publication phase does not implement active governance or its migration.
    if document['status'] != 'draft' or document['effective_at'] is not None:
        raise ValueError('Governance publication only supports an inactive draft')
    esc = html.escape
    version = document['version']
    proposal = document['proposal_url']
    if not proposal.startswith('https://github.com/'):
        raise ValueError('Governance proposal must link to a GitHub record')
    discussion = 'https://github.com/{}/issues/new'.format(repository)
    body = '<div class="page-head"><p class="eyebrow">OPEN GOVERNANCE / {}</p><h1>规则与治理</h1><p>自由参与，凭贡献获得认可，让规则也能被讨论。</p></div>'.format(esc(version))
    body += '<div class="notice"><strong>公开草案 · 尚未生效</strong><p>现行协作协议 v1 继续适用。本次发布没有开放自动治理权限。</p><a href="../guide.md">阅读现行协议 ↗</a></div>'
    body += '<div class="report-tools"><span>版本 {} · 生效时间：未生效</span><a href="rules.md">下载 Markdown ↗</a><a href="index.json">读取 JSON ↗</a></div>'.format(esc(version))
    body += '<p>规则讨论与后续实现以<a href="../philosophy/index.html">运行哲学</a>为项目审查基准；治理草案仍未生效。</p>'
    body += '<article class="prose report-prose">'
    lines = ['# ' + document['title'], '', '版本：' + version, '', '状态：公开草案，尚未生效。生效时间：无。', '', '现行协议：[协作协议 v1](../guide.md)', '']
    lines += ['项目审查基准：[运行哲学](../philosophy/index.html)。治理草案仍未生效。', '']
    for section in document['sections']:
        body += '<section><h2>{}</h2>'.format(esc(section['title']))
        lines += ['## ' + section['title'], '']
        for paragraph in section['paragraphs']:
            body += '<p>{}</p>'.format(esc(paragraph))
            lines += [paragraph, '']
        body += '</section>'
    body += '<h2>版本记录</h2><ul>'
    lines += ['## 版本记录', '']
    for change in document['changes']:
        text = change['date'] + ' · ' + change['text']
        body += '<li>{}</li>'.format(esc(text))
        lines += ['- ' + text]
    body += '</ul><p><a href="{}">原始设计提案 ↗</a></p><a class="button" href="{}">提出规则建议 ↗</a></article>'.format(esc(proposal, quote=True), esc(discussion, quote=True))
    lines += ['', '[原始设计提案](' + proposal + ')', '', '[提出规则建议](' + discussion + ')', '']
    index = {'schema_version': 1, 'status': document['status'], 'effective_at': document['effective_at'],
             'current_protocol': '../guide.md', 'discussion_url': discussion,
             'versions': [{**document, 'html': 'index.html', 'markdown': 'rules.md'}]}
    return body, '\n'.join(lines), index
