"""Small, non-fetching Markdown view for untrusted community source text.

Only paragraphs, headings, flat lists, fences, inline code, bold and explicit
HTTPS links are supported. This is deliberately not a full Markdown/HTML parser.
Unsupported constructs stay escaped; source exports remain authoritative.
"""
from html import escape
import re
from urllib.parse import urlsplit

from arc.languages import language


_INLINE = re.compile(
    r'(?P<ticks>`+)|'
    r'(?P<strong>\*\*(?P<bold>[^*\n]+)\*\*)|'
    r'(?<![!\\])\[(?P<label>[^\[\]\n]+)\]\((?P<url>https://[^\s()<>"\'\\]+)\)',
    re.DOTALL)
_FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
_HEADING = re.compile(r'^ {0,3}(#{1,6})\s+(.+)$')
_LIST = re.compile(r'^ {0,3}(?:([-+*])|([0-9]{1,9})[.)])\s+(.+)$')


def inline(value):
    # Do not interpret nested links or escaped/image-like constructs piecemeal.
    if re.search(r'\[[^\]\n]*\[', value):
        return escape(value)
    parts, cursor = [], 0
    while cursor < len(value):
        match = _INLINE.search(value, cursor)
        if match is None:
            break
        parts.append(escape(value[cursor:match.start()]))
        if match['ticks']:
            closing = re.search(r'(?<!`)' + re.escape(match['ticks']) + r'(?!`)', value[match.end():])
            if closing is None:
                parts.append(escape(value[match.start():]))
                cursor = len(value)
                break
            end = match.end() + closing.start()
            parts.append('<code>' + escape(value[match.end():end]) + '</code>')
            cursor = match.end() + closing.end()
            continue
        elif match['strong']:
            rendered = '<strong>' + escape(match['bold']) + '</strong>'
        else:
            url = match['url']
            try:
                parsed = urlsplit(url)
                safe = (parsed.scheme == 'https' and parsed.hostname
                        and parsed.username is None and parsed.password is None
                        and not any(ord(c) < 32 or ord(c) == 127 for c in url))
                parsed.port
            except ValueError:
                safe = False
            rendered = ('{} (<a href="{}" rel="noreferrer nofollow">{}</a>)'.format(
                escape(match['label']), escape(url), escape(url))
                if safe else escape(match[0]))
        parts.append(rendered)
        cursor = match.end()
    parts.append(escape(value[cursor:]))
    return ''.join(parts)


def render(value):
    blocks, paragraph, items = [], [], []
    list_kind = None
    list_start = None
    fence, code = None, []

    def flush():
        nonlocal list_kind, list_start
        if paragraph:
            blocks.append('<p>' + inline('\n'.join(paragraph)) + '</p>')
            paragraph.clear()
        if items:
            start = ' start="{}"'.format(list_start) if list_kind == 'ol' and list_start != 1 else ''
            blocks.append('<' + list_kind + start + '>' + ''.join(items) + '</' + list_kind + '>')
            items.clear()
            list_kind = None
            list_start = None

    for line in value.splitlines():
        marker = _FENCE.match(line)
        if fence is not None:
            if (marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence)
                    and not marker[2].strip()):
                blocks.append('<pre><code>' + escape('\n'.join(code)) + '</code></pre>')
                fence, code = None, []
            else:
                code.append(line)
            continue
        if marker:
            flush()
            fence = marker[1]
            continue
        if not line.strip():
            flush()
            continue
        heading = _HEADING.match(line)
        item = _LIST.match(line)
        if heading:
            flush()
            level = min(6, len(heading[1]) + 1)  # Page title owns h1.
            blocks.append('<h{0}>{1}</h{0}>'.format(level, inline(heading[2])))
        elif item:
            kind = 'ul' if item[1] else 'ol'
            if paragraph or (items and list_kind != kind):
                flush()
            if not items and kind == 'ol':
                list_start = int(item[2])
            list_kind = kind
            items.append('<li>' + inline(item[3]) + '</li>')
        elif line.startswith(('    ', '\t')) or re.match(r'^ {0,3}>', line):
            flush()
            blocks.append('<p class="source-literal">' + escape(line) + '</p>')
        else:
            if items:
                flush()
            paragraph.append(line)
    if fence is not None:
        blocks.append('<pre><code>' + escape('\n'.join(code)) + '</code></pre>')
    flush()
    return '<div lang="{}">{}</div>'.format(language(value), '\n'.join(blocks))
