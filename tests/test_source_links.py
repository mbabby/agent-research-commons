"""Clickable source references must not turn untrusted prose into active HTML."""
from html.parser import HTMLParser
import unittest

from arc.community_views import source_prose


class ParsedSource(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.text, self.links, self.tags = [], [], []
        self.feed(body)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == 'a':
            self.links.append(dict(attrs))

    def handle_data(self, data):
        self.text.append(data)


class SourceLinkTests(unittest.TestCase):
    def check(self, source, expected):
        rendered = source_prose(source)
        parsed = ParsedSource(rendered)
        self.assertEqual(''.join(parsed.text), source)
        self.assertEqual([link['href'] for link in parsed.links], expected)
        self.assertTrue(all(link['rel'] == 'noreferrer nofollow' for link in parsed.links))
        self.assertTrue(set(parsed.tags) <= {'span', 'a'})
        return rendered

    def test_pinned_artifacts_queries_fragments_and_language(self):
        artifact = ('https://github.com/mbabby/agent-research-commons/tree/'
                    '177c0aced7d6b2b2ab29b45c1c21a7b302c0d975/drafts/cutoff-ledger-2026-11-06')
        comment = 'https://github.com/mbabby/agent-research-commons/issues/29?x=1&y=2#issuecomment-6674360730'
        source = '中文 [fixed fixture](' + artifact + ') and [proposal](' + comment + ').\n'
        rendered = self.check(source, [artifact, comment])
        self.assertIn('lang="zh-CN"', rendered)
        self.assertIn('?x=1&amp;y=2#issuecomment-', rendered)

    def test_unsafe_and_unsupported_destinations_stay_text(self):
        source = '\n'.join([
            '[bad](javascript:alert(1))', '[bad](data:text/html,bad)',
            '[bad](http://example.com)', '[bad](//example.com)',
            '[bad](https:///missing-host)', '[bad](https://user:secret@example.com/path)',
            '[bad](https://example.com:invalid/path)', '[bad](https://[broken/path)',
            '[bad](https://example.com/\x00evil)', '[bad](https://example.com/a b)',
            '[bad](https://example.com/" onclick="bad)', '[bad](https://example.com/\\evil)',
            '[nested](https://example.com/a(b))', '[title](https://example.com "title")',
            '![image](https://example.com/image.png)', r'\[escaped](https://example.com)',
            '<a href="https://example.com">raw</a><img src=x onerror=bad><script>bad</script>',
            'https://example.com/raw-url', '[reference][ref]', '[ref]: https://example.com',
        ])
        self.check(source, [])

    def test_code_fences_inline_code_and_indented_code_stay_text(self):
        literal = '[example](https://example.com/code)'
        source = ('```python\n' + literal + '\n````\n'
                  '~~~\n' + literal + '\n```\n' + literal + '\n~~~\n'
                  '    ' + literal + '\n\t' + literal + '\n'
                  '`' + literal + '` and ``' + literal + '``\n'
                  '[real](https://example.com/real)\n')
        self.check(source, ['https://example.com/real'])

    def test_unclosed_fence_and_empty_source(self):
        self.check('```\n[not a link](https://example.com)\n', [])
        self.check('', [])

    def test_multiline_code_quoted_code_and_nested_syntax_stay_text(self):
        for source in [
                '`multiline\n[code](https://example.com/code)\n`',
                '``multiline `\n[code](https://example.com/code)\n``',
                '> ```\n> [code](https://example.com/code)\n> ```',
                '[outer [inner](https://example.com/nested)](https://example.com/outer)']:
            with self.subTest(source=source):
                self.check(source, [])
        self.check('`multiline\n[code](https://example.com/code)\n` [real](https://example.com/real)',
                   ['https://example.com/real'])

    def test_labels_cannot_inject_html_or_hide_destination(self):
        source = '[<img src=x onerror=bad> & "label"](https://example.com/source)'
        rendered = self.check(source, ['https://example.com/source'])
        self.assertIn('&lt;img', rendered)
        self.assertIn('>https://example.com/source</a>', rendered)


if __name__ == '__main__':
    unittest.main()
