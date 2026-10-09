"""Source-bound presentation translations; never change canonical research records."""
import copy
import json
import re
from pathlib import Path

TASK_FIELDS = ('title', 'question', 'scope', 'exclusions', 'deliverable', 'acceptance')
PROSE_FIELDS = frozenset(TASK_FIELDS + ('summary', 'text', 'paragraphs', 'note', 'notes', 'method', 'unknowns', 'limitations'))


def language(value):
    """Label supported prose; Chinese-containing text may also include English."""
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return 'zh-CN' if re.search(r'[\u3400-\u9fff]', text) else 'en'


def label(code):
    return 'Chinese / 中文' if code == 'zh-CN' else 'English'


def validate_translation(source, translated, field=''):
    # Preserve structure, all identifiers, links, dates and acceptance metadata.
    if type(source) is not type(translated):
        raise ValueError('Translation changes source structure')
    if isinstance(source, dict):
        if source.keys() != translated.keys():
            raise ValueError('Translation changes source fields')
        for key in source:
            validate_translation(source[key], translated[key], key)
    elif isinstance(source, list):
        if len(source) != len(translated):
            raise ValueError('Translation changes source list length')
        for a, b in zip(source, translated):
            validate_translation(a, b, field)
    elif field not in PROSE_FIELDS or not isinstance(source, str):
        if source != translated:
            raise ValueError('Translation changes protected field: ' + field)
    elif sorted(re.findall(r'https?://[^\s<>）)]+', source)) != sorted(re.findall(r'https?://[^\s<>）)]+', translated)):
        # URLs embedded in prose must retain exactly the same destinations.
        raise ValueError('Translation changes embedded URLs: ' + field)


def localize(source, category, key, root):
    projection = {k:source[k] for k in TASK_FIELDS} if category == 'tasks' else source
    result = copy.deepcopy(source)
    translated = False
    # key comes from validated task numbers/report slugs or fixed document names.
    path = Path(root) / category / (str(key) + '.json')
    if path.is_file():
        sidecar = json.loads(path.read_text(encoding='utf-8'))
        if sidecar['source'] == projection:
            validate_translation(projection, sidecar['translation'])
            result.update(copy.deepcopy(sidecar['translation']))
            translated = True
    result['_publication'] = {'language': 'en' if translated else language(projection),
                              'source_language': language(projection), 'is_translation': translated}
    return result


def exported(record, original_url):
    result = {k:v for k,v in record.items() if k != '_publication'}
    result['publication'] = {**record['_publication'], 'original': original_url,
                             'translation_review': 'Presentation translation; original research review applies to the source record only.'}
    return result


def guide_translation(source_path, english_path, metadata_path):
    import hashlib
    source = Path(source_path).read_text(encoding='utf-8')
    metadata_path = Path(metadata_path)
    translated = (metadata_path.is_file() and Path(english_path).is_file()
                  and json.loads(metadata_path.read_text(encoding='utf-8'))['source_sha256']
                  == hashlib.sha256(Path(source_path).read_bytes()).hexdigest())
    text = Path(english_path).read_text(encoding='utf-8') if translated else source
    kind = 'English translation' if translated else 'Original protocol (no current English translation)'
    header = '> {}. [Original Chinese protocol](guide.original.md). Translation does not change the protocol.\n\n'.format(kind)
    return header + text.replace('](protocol.md)', '](guide.original.md)'), translated
