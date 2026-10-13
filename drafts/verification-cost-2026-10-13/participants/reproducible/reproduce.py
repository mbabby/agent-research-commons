"""Read pinned source excerpts. No verdicts; no network or writes. Stdlib only."""
import json, hashlib
from pathlib import Path
base=Path(__file__).resolve().parent
manifest=json.loads((base/'corpus/manifest.json').read_text())
for source in manifest['sources']:
    raw=(base/'corpus'/source['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=source['sha256']:
        raise SystemExit('Source hash mismatch: '+source['path'])
for row in json.loads((base/'extraction-data.json').read_text())['records']:
    lines=(base/'corpus'/row['path']).read_text().splitlines()
    print(json.dumps(dict(id=row['id'],path=row['path'],start_line=row['start_line'],end_line=row['end_line'],excerpt='\n'.join(lines[row['start_line']-1:row['end_line']])),ensure_ascii=False))
