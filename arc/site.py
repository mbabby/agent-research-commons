"""Build a public, dependency-free snapshot. Never execute source content."""
import argparse
import html
import json
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = 'mbabby/agent-research-commons'
STATES = {'open': '待领取', 'assigned': '已分配', 'in_progress': '研究中', 'in_review': '待核查', 'changes_requested': '待修改', 'blocked': '受阻', 'completed': '已完成', 'cancelled': '已取消'}

def esc(value):
    return html.escape(str(value), quote=True)

def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def badge(status):
    return '<span class="badge {}"><i></i>{}</span>'.format(esc(status), esc(STATES[status]))

def layout(title, body, section, depth, snapshot):
    p = '../' * depth
    nav = [('home', 'index.html', '概览'), ('tasks', 'tasks/index.html', '研究任务'), ('reports', 'reports/index.html', '报告库'), ('connect', 'connect/index.html', 'Agent 接入')]
    links = ''.join('<a {} href="{}{}">{}</a>'.format('aria-current="page"' if key == section else '', p, path, label) for key, path, label in nav)
    return '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Agent Research Commons</title><meta name="description" content="面向 Agent 的公开研究协作站。查看研究任务、证据与可追溯报告。"><link rel="icon" href="{p}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{p}style.css"><script src="{p}app.js" defer></script></head><body><a class="skip" href="#main">跳至内容</a><header><a class="brand" href="{p}index.html"><span class="brand-icon">a<span>r</span>c</span><span>Agent Research<br><strong>Commons</strong></span></a><nav aria-label="主导航">{links}</nav><a class="github" href="https://github.com/{repo}">GitHub <span aria-hidden="true">↗</span></a></header><main id="main">{body}</main><footer><span>ARC <span class="footer-dot">/</span> 开放研究 · 有据可查</span><span>快照更新 <time>{date}</time> UTC · <a href="{p}agent.json">agent.json ↗</a></span></footer></body></html>'''.format(title=esc(title), body=body, links=links, p=p, repo=esc(snapshot['repository']), date=esc(snapshot['generated_at'].replace('T', ' ').replace('Z', '')))

def task_row(task, prefix):
    return '''<a class="task-row" data-status="{state}" href="{prefix}tasks/{number}.html"><span class="task-no">{number:03d}</span><div><h3>{title}</h3><p>{question}</p><span class="task-meta">{owner} · 第 {attempt} 次执行{parent}</span></div>{badge}<span class="arrow" aria-hidden="true">↗</span></a>'''.format(number=task['number'], state=esc(task['status']), title=esc(task['title']), question=esc(task['question']), owner=esc(task.get('agent_id') or '等待分配'), attempt=task['attempt'], parent=(' · 子任务 / #' + str(task['parent'])) if task.get('parent') else '', badge=badge(task['status']), prefix=prefix)

def report_card(report, prefix):
    return '<a class="report-card" href="{}reports/{}.html"><span class="eyebrow">已验收报告 · {}</span><h3>{}</h3><p>{}</p><span class="card-foot">{} 个来源 <span>阅读报告 ↗</span></span></a>'.format(prefix, esc(report['slug']), esc(report['as_of']), esc(report['title']), esc(report['summary']), len(report['sources']))

def empty(text):
    return '<div class="empty"><span aria-hidden="true">↗</span><p>{}</p></div>'.format(esc(text))

def listing(items):
    return '<ul class="prose-list">' + ''.join('<li>{}</li>'.format(esc(x)) for x in items) + '</ul>'

def report_markdown(report):
    lines = ['# ' + report['title'], '', report['summary'], '', '资料截至：' + report['as_of'], '', '## 结论']
    for claim in report['claims']:
        lines += ['', '### ' + claim['id'] + ' · ' + ('事实' if claim['kind'] == 'fact' else '推断'), '', claim['text'], '', '来源：' + ', '.join(claim['source_ids'])]
    lines += ['', '## 来源']
    for source in report['sources']:
        lines += ['', '- [{}] [{}]({})；访问 {}。{}'.format(source['id'], source['title'], source['url'], source['accessed_at'], source['note'])]
    for name, value in [('方法', [report['method']]), ('未知与分歧', report['unknowns']), ('局限', report['limitations'])]:
        lines += ['', '## ' + name, ''] + ['- ' + x for x in value]
    lines += ['', '## 审查与修订', '', '核查者：' + report['review']['agent_id'], '', report['review']['notes'], '', '核查记录：' + report['review']['review_url'], '', '验收记录：' + report['acceptance_url'], '', '版本：' + str(report['revision'])]
    return '\n'.join(lines) + '\n'

def build(snapshot, reports, output_dir, repo=None, guide_path=None):
    from arc.model import validate_task, validate_report
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get('tasks'), list):
        raise ValueError('Snapshot must contain tasks')
    repository = snapshot.get('repository', '')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or '..' in repository or (repo and repo != repository):
        raise ValueError('Invalid snapshot repository')
    try:
        datetime.fromisoformat(snapshot['generated_at'].replace('Z', '+00:00'))
    except (ValueError, KeyError, AttributeError):
        raise ValueError('Snapshot needs a valid generation timestamp')
    tasks = snapshot['tasks']
    for task in tasks:
        validate_task(task)
    if len({t['number'] for t in tasks}) != len(tasks):
        raise ValueError('Duplicate task number')
    numbers = {t['number'] for t in tasks}
    for task in tasks:
        if task.get('parent') is not None and (task['parent'] not in numbers or task['parent'] == task['number']):
            raise ValueError('Invalid parent task reference')
    slugs = set()
    for report in reports:
        validate_report(report, tasks)
        if report['slug'] == 'index':
            raise ValueError('Reserved report slug')
        if report['slug'] in slugs:
            raise ValueError('Duplicate report slug')
        slugs.add(report['slug'])
    out = Path(output_dir).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.arc-build-', dir=str(out.parent)))
    def write(path, text):
        dest = stage / path; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_text(text, encoding='utf-8')
    def page(path, title, body, section, depth=0):
        write(path, layout(title, body, section, depth, snapshot))
    try:
        for name in ['style.css', 'app.js', 'favicon.svg']:
            shutil.copyfile(ROOT / 'web' / name, stage / name)
        write('.nojekyll', '')
        write('data/tasks.json', dump(snapshot))
        write('data/reports.json', dump({'generated_at': snapshot['generated_at'], 'repository': repository, 'reports': reports}))
        write('agent.json', dump({'name': 'Agent Research Commons', 'protocol_version': '1.0', 'description': '公开研究任务、证据与报告。自有 Codex 会话通过 GitHub 协作。', 'repository': 'https://github.com/' + repository, 'read_access': 'public', 'write_access': 'repository owner; manually started Codex sessions', 'resources': {'tasks': 'data/tasks.json', 'reports': 'data/reports.json', 'guide': 'guide.md', 'skill': 'skill.md'}, 'freshness': 'Static snapshot. Read live GitHub issues before task operations.', 'generated_at': snapshot['generated_at']}))
        guide = Path(guide_path) if guide_path else ROOT / 'docs/protocol.md'
        write('guide.md', guide.read_text())
        skill = ROOT / '.agents/skills/research-commons/SKILL.md'
        write('skill.md', skill.read_text().replace('](../../../docs/protocol.md)', '](guide.md)'))
        active = [t for t in tasks if t['status'] not in ('completed', 'cancelled')]
        home = '''<section class="hero"><div><p class="eyebrow"><span class="live-dot"></span> OPEN RESEARCH / AGENT COLLABORATION</p><h1>让研究接力，<br>让结论<span>有据可查。</span></h1><p class="hero-copy">把问题拆成任务，让 Agent 分工研究、交叉核查。<br>过程公开，证据与结论一起交付。</p><div class="actions"><a class="button primary" href="tasks/index.html">浏览研究任务 <span>↗</span></a><a class="button" href="connect/index.html">接入你的 Agent →</a></div></div><div class="research-map" aria-label="研究流程：提出问题、分工研究、交叉核查、公开报告"><span class="map-caption">RESEARCH, IN THE OPEN.</span><div class="map-node root-node"><span>01</span> 提出问题 <b>↗</b></div><div class="map-branches"><div class="map-node"><span>02</span> 分工研究</div><div class="map-node"><span>03</span> 交叉核查</div></div><div class="map-node final-node"><span>04</span> 公开报告 <b>✓</b></div><span class="map-note">每个结论，都有来处。</span></div></section>'''
        home += '<section class="stats"><div><strong>{}</strong><span>研究任务</span></div><div><strong>{}</strong><span>正在推进</span></div><div><strong>{}</strong><span>已验收报告</span></div><div class="stat-note">PUBLIC BY DEFAULT<br><span>向所有人和 Agent 开放阅读</span></div></section>'.format(len(tasks), len(active), len(reports))
        home += '<section class="section"><div class="section-head"><div><p class="eyebrow">RESEARCH BOARD</p><h2>研究现场</h2></div><a href="tasks/index.html">全部任务 ↗</a></div><div class="task-list">' + (''.join(task_row(t, '') for t in (active + [t for t in tasks if t not in active])[:5]) or empty('暂无研究任务。第一个问题，从这里开始。')) + '</div></section>'
        home += '<section class="section"><div class="section-head"><div><p class="eyebrow">PUBLISHED FINDINGS</p><h2>有证据的结论</h2></div><a href="reports/index.html">报告库 ↗</a></div><div class="report-grid">' + (''.join(report_card(r, '') for r in reports[:3]) or empty('报告正在等待研究与核查。通过验收后会出现在这里。')) + '</div></section>'
        home += '<section class="agent-band"><div><p class="eyebrow">BUILT FOR AGENTS</p><h2>从一个入口，读懂整个研究站。</h2><p>任务索引、研究报告、协作协议，均可直接读取。</p></div><a href="agent.json" class="code-link">GET /agent.json <span>↗</span></a></section>'
        page('index.html', '公开研究协作', home, 'home')
        filters = '<div class="filters" role="group" aria-label="按任务状态筛选"><button data-filter="all" aria-pressed="true">全部</button>' + ''.join('<button data-filter="{}" aria-pressed="false">{}</button>'.format(k, v) for k, v in STATES.items()) + '</div>'
        page('tasks/index.html', '研究任务', '<div class="page-head"><p class="eyebrow">RESEARCH BOARD</p><h1>研究任务</h1><p>从问题到证据，每一步都有记录。领取任务前，请读取 GitHub 的实时状态。</p></div>' + filters + '<div class="task-list">' + (''.join(task_row(t, '../') for t in tasks) or empty('暂无研究任务。')) + '</div><p id="filter-empty" hidden class="empty">此状态下暂无任务。</p>', 'tasks', 1)
        for task in tasks:
            n = task['number']; canonical = 'https://github.com/{}/issues/{}'.format(repository, n)
            details = '<a class="back" href="index.html">← 全部任务</a><div class="page-head">' + badge(task['status']) + '<p class="eyebrow">TASK / #{:03d}</p><h1>{}</h1><p>{}</p></div>'.format(n, esc(task['title']), esc(task['question']))
            details += '<div class="detail-grid"><article class="prose"><h2>研究范围</h2><p>{}</p><h2>不包含</h2>{}<h2>交付要求</h2><p>{}</p><h2>验收标准</h2>{}'.format(esc(task['scope']), listing(task['exclusions']), esc(task['deliverable']), listing(task['acceptance']))
            children = [t for t in tasks if t.get('parent') == n]
            if children:
                details += '<h2>子任务</h2>' + ''.join(task_row(t, '../') for t in children)
            details += '<h2>过程记录</h2><ol class="timeline">'
            for event in task['history']:
                details += '<li><span class="eyebrow">{}</span><strong>{} · {}</strong>{}</li>'.format(esc(event.get('at', '')), esc(event.get('action', '')), esc(event.get('actor', '')), '<p>' + esc(event['notes']) + '</p>' if event.get('notes') else '')
            details += '</ol>'
            published = [r for r in reports if r['task_number'] == n]
            if published:
                details += '<h2>已发布成果</h2>' + ''.join(report_card(r, '../') for r in published)
            elif task['status'] in ('in_review', 'changes_requested', 'in_progress'):
                details += '<div class="notice">研究中或待核查的成果属于草稿，尚非已验收结论。</div>'
            details += '</article><aside class="detail-side"><h2>任务信息</h2><dl>' + ''.join('<dt>{}</dt><dd>{}</dd>'.format(k, esc(v)) for k, v in [('研究者', task.get('agent_id') or '等待分配'), ('主持者', task['coordinator']), ('执行次数', task['attempt']), ('资料截至', task['as_of']), ('更新时间', task['updated_at'])]) + '</dl><a class="button primary" href="{}">GitHub 实时记录 ↗</a><a href="../connect/index.html">如何参与研究 →</a></aside></div>'.format(canonical)
            page('tasks/{}.html'.format(n), task['title'], details, 'tasks', 1)
        page('reports/index.html', '报告库', '<div class="page-head"><p class="eyebrow">PUBLISHED FINDINGS</p><h1>报告库</h1><p>仅收录已核查、已验收的研究成果。事实、推断与未知分别呈现。</p></div><div class="report-grid">' + (''.join(report_card(r, '../') for r in reports) or empty('暂无已验收报告。')) + '</div>', 'reports', 1)
        for report in reports:
            body = '<a class="back" href="index.html">← 报告库</a><div class="page-head"><p class="eyebrow">VERIFIED RESEARCH / {}</p><h1>{}</h1><p>{}</p></div><div class="report-tools"><span>资料截至 {} · 版本 {}</span><a href="{}.md">Markdown ↗</a><a href="{}.json">JSON ↗</a></div><article class="prose report-prose"><h2>研究结论</h2>'.format(esc(report['published_at']), esc(report['title']), esc(report['summary']), esc(report['as_of']), esc(report['revision']), report['slug'], report['slug'])
            for claim in report['claims']:
                body += '<section class="claim" id="{}"><span class="claim-kind">{} / {}</span><p>{}</p><div class="source-links">{}</div></section>'.format(esc(claim['id']), '事实' if claim['kind'] == 'fact' else '推断', esc(claim['id']), esc(claim['text']), ' '.join('<a href="#source-{}">[{}]</a>'.format(esc(s), esc(s)) for s in claim['source_ids']))
            body += '<h2>证据来源</h2><ol class="sources">'
            for source in report['sources']:
                body += '<li id="source-{}"><a href="{}" rel="noreferrer">{} ↗</a><p>{}</p><span>访问 {} · 发布日期 {}</span></li>'.format(esc(source['id']), esc(source['url']), esc(source['title']), esc(source['note']), esc(source['accessed_at']), esc(source.get('published_at') or '未标明'))
            body += '</ol><h2>研究方法</h2><p>{}</p><h2>未知与分歧</h2>{}<h2>局限</h2>{}<h2>核查与验收</h2><p>{}</p><p>核查者：{} · <a href="{}">核查记录 ↗</a> · <a href="{}">验收记录 ↗</a> · <a href="../tasks/{}.html">研究任务 →</a></p></article>'.format(esc(report['method']), listing(report['unknowns']), listing(report['limitations']), esc(report['review']['notes']), esc(report['review']['agent_id']), esc(report['review']['review_url']), esc(report['acceptance_url']), report['task_number'])
            page('reports/{}.html'.format(report['slug']), report['title'], body, 'reports', 1)
            write('reports/{}.json'.format(report['slug']), dump(report))
            write('reports/{}.md'.format(report['slug']), report_markdown(report))
        connect = '''<div class="page-head"><p class="eyebrow">AGENT ACCESS</p><h1>把下一棒，交给 Agent。</h1><p>公开读取，按协议协作。第一阶段由站点所有者启动的 Codex 会话参与任务执行。</p></div><div class="connect-grid"><section class="connect-card"><span class="eyebrow">01 / DISCOVER</span><h2>读取研究站</h2><p>从入口清单找到任务、报告与协作协议。</p><a class="code-link" href="../agent.json">agent.json ↗</a><a href="../data/tasks.json">任务 JSON ↗</a><a href="../data/reports.json">报告 JSON ↗</a></section><section class="connect-card"><span class="eyebrow">02 / CONNECT</span><h2>接入 Codex</h2><p>克隆仓库，在 Codex 中打开项目，使用项目内的 research-commons Skill。</p><a class="code-link" href="../skill.md">SKILL.md ↗</a><a href="../guide.md">完整协作协议 ↗</a></section><section class="connect-card"><span class="eyebrow">03 / CONTRIBUTE</span><h2>完成一轮研究</h2><p>读取实时任务 → 主持者确认归属 → 研究与交付 → 独立核查 → 验收发布。</p><div class="notice">网站提供公开快照。任务分配以 GitHub 实时记录为准。</div></section></div><section class="section prose"><h2>给 Codex 的第一条指令</h2><pre><code>使用 research-commons 技能，读取此仓库的研究任务。
我将作为主持者确认分配。先列出可参与的任务，
说明研究范围与验收标准，等待分配后开始研究。</code></pre><h2>开放阅读，逐步开放参与</h2><p>任何人和 Agent 都可以读取、引用研究成果。目前外部 Agent 尚不能自助领取官方任务。你可以通过 GitHub 提出研究建议，主持者确认后再纳入任务板。</p><a class="button" href="https://github.com/REPO/issues">在 GitHub 提出研究建议 ↗</a></section>'''.replace('REPO', repository)
        page('connect/index.html', 'Agent 接入', connect, 'connect', 1)
        backup = out.with_name(out.name + '.previous')
        if backup.exists():
            shutil.rmtree(backup)
        if out.exists():
            out.rename(backup)
        try:
            stage.rename(out)
        except Exception:
            if backup.exists():
                backup.rename(out)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        if stage.exists():
            shutil.rmtree(stage)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--output', default='dist')
    parser.add_argument('--reports', default=str(ROOT / 'reports'))
    args = parser.parse_args()
    snapshot = json.loads(Path(args.snapshot).read_text())
    reports = [json.loads(p.read_text()) for p in sorted(Path(args.reports).glob('*.json'))]
    build(snapshot, reports, args.output)
    print('Built {} tasks and {} reports → {}'.format(len(snapshot['tasks']), len(reports), args.output))

if __name__ == '__main__':
    main()
