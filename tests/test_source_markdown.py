"""The small reader must format source without granting it HTML authority."""
from html.parser import HTMLParser
import unittest
from arc.source_markdown import render


class Parsed(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags, self.links, self.attrs = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.extend(attrs)
        if tag == 'a':
            self.links.append(dict(attrs)['href'])


class SourceMarkdownTests(unittest.TestCase):
    def test_readable_structure(self):
        html = render('## 中文 case\n\n**Bounded result** and `code`.\n\n- first\n- second\n\n1. third\n2. fourth\n\n```python\nprint("<x>")\n```')
        for fragment in ['<h3>中文 case</h3>', '<strong>Bounded result</strong>', '<code>code</code>', '<ul><li>first</li><li>second</li></ul>', '<ol><li>third</li><li>fourth</li></ol>', '<pre><code>print(&quot;&lt;x&gt;&quot;)</code></pre>', 'lang="zh-CN"']:
            self.assertIn(fragment, html)
        self.assertNotIn('<h1>', html)

    def test_links_show_destinations_and_escape_labels(self):
        html = render('[<img src=x>](https://example.com/?a=1&b=2)')
        self.assertEqual(Parsed(html).links, ['https://example.com/?a=1&b=2'])
        self.assertIn('&lt;img src=x&gt;', html)
        self.assertIn('>https://example.com/?a=1&amp;b=2</a>', html)

    def test_unsafe_and_unsupported_syntax_never_becomes_active(self):
        source = '\n\n'.join(['<script>alert(1)</script><img src=x onerror=bad>',
            '[x](javascript:alert(1))', '[x](data:text/html,bad)', '[x](//example.com)',
            '[x](https://u:p@example.com)', '[x](https://example.com:bad)',
            '[x](https://example.com/\x00bad)', '[x](https://example.com/" onmouseover="bad)',
            '![img](https://example.com/img)', r'\[escaped](https://example.com)',
            '[nested [x](https://example.com)](https://example.org)',
            'https://example.com/bare', '<iframe src="https://example.com">',
            '> [quoted](https://example.com)', '    [indented](https://example.com)'])
        parsed = Parsed(render(source))
        self.assertEqual(parsed.links, [])
        self.assertTrue(set(parsed.tags) <= {'div', 'p'})
        self.assertTrue(all(k in {'lang', 'class'} for k, v in parsed.attrs))

    def test_code_is_inert_including_unclosed_and_mismatched_fences(self):
        for source in ['```html\n[x](https://example.com)\n<script>bad</script>\n```',
                       '~~~\n[x](https://example.com)\n```\n[x](https://example.com)',
                       '`[x](https://example.com)`', '``[x](https://example.com)`\nnext``',
                       '`unclosed [x](https://example.com)',
                       '```unclosed\n[x](https://example.com)']:
            with self.subTest(source=source):
                parsed = Parsed(render(source))
                self.assertEqual(parsed.links, [])
                self.assertNotIn('script', parsed.tags)

    def test_ordered_list_preserves_start(self):
        self.assertIn('<ol start="3"><li>third</li><li>fourth</li></ol>', render("3. third\n4. fourth"))

    def test_empty_and_unknown_markup(self):
        self.assertEqual(Parsed(render('')).links, [])
        self.assertIn('| a | b |', render('| a | b |\n| -- | -- |'))
