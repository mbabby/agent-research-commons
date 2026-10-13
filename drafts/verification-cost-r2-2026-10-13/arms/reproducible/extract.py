"""Extract source lines, not answers or verdicts. Python standard library only."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parents[2]
corpus = json.loads((base / 'common/corpus.json').read_text())
locators = json.loads(Path(__file__).with_name('locators.json').read_text())
sources = {}
for source in corpus['sources']:
    data = (base / 'common' / source['path']).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != source['sha256']:
        raise ValueError('source hash mismatch: ' + source['path'])
    sources[source['path']] = {'sha256': digest, 'lines': data.decode().splitlines()}
print(json.dumps({'git_sha': corpus['git_sha'], 'source_sha256': {
    path: source['sha256'] for path, source in sources.items()}, 'excerpts': [
        dict(locator, text='\n'.join(sources[locator['path']]['lines'][
            locator['start_line'] - 1:locator['end_line']]))
        for locator in locators]}, indent=2))
