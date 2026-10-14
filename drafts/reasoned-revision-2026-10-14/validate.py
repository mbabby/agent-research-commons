"""Check retained pilot mechanics; does not establish research truth."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads((ROOT / path).read_text())


def main():
    for manifest in ['prereg/FROZEN.json',
                     'prereg/development-followups-FROZEN.json',
                     'prereg/heldout-followups-FROZEN.json']:
        for name, expected in read_json(manifest).items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    cases = read_json('prereg/development.json') + read_json('prereg/heldout.json')
    expected_names = {case['id'] + '-' + arm for case in cases for arm in ['initial', 'N', 'E', 'P']}
    assert {f.stem for f in (ROOT / 'raw').glob('*.txt')} == expected_names
    for case in cases:
        name = case['id']
        initial = (ROOT / 'raw' / (name + '-initial.txt')).read_text().strip()
        decision = initial.splitlines()[0].removeprefix('Decision: ')
        target = 'KEEP' if decision == 'CUT' else 'CUT'
        for arm in ['N', 'E', 'P']:
            prompt = (ROOT / 'prompts' / (name + '-' + arm + '.txt')).read_text()
            assert case['scene'] in prompt and case['criteria'] in prompt
            assert '\nFrozen initial critique:\n' + initial + '\n\nFollow-up:' in prompt
            followup = prompt.split('\nFollow-up:\n', 1)[1].split('\n\nGive your reconsidered')[0]
            assert len(followup.split()) <= 45
            if arm == 'E':
                assert followup == case['evidence_followup']
            if arm == 'P':
                assert 'recommendation should be ' + target in followup
        for arm in ['initial', 'N', 'E', 'P']:
            raw = (ROOT / 'raw' / (name + '-' + arm + '.txt')).read_text()
            assert len(raw.split()) <= 150
            assert all(label in raw for label in ['Decision:', 'Evidence:', 'Reason:', 'Uncertainty:'])
    mapping = read_json('analysis/blind-map.json')
    assert set(mapping.values()) == expected_names - {c['id'] + '-initial' for c in cases}
    rows = read_json('review/blind-input.json')['rows']
    assert len(rows) == 12 and len({r['row_id'] for r in rows}) == 12
    for row in rows:
        original = mapping[row['row_id']]
        assert row['stimulus'] == (ROOT / 'prompts' / (original + '.txt')).read_text()
        assert row['response'] == (ROOT / 'raw' / (original + '.txt')).read_text()
    scores = read_json('review/blind-scores.json')['rows']
    assert {r['row_id'] for r in scores} == set(mapping) and len(scores) == 12
    for score in scores:
        raw = (ROOT / 'raw' / (mapping[score['row_id']] + '.txt')).read_text()
        assert raw.splitlines()[0] == 'Decision: ' + score['decision']
        assert len(raw.split()) == score['word_count']
    results = read_json('analysis/results.json')['rows']
    assert results == [dict(case_condition=mapping[r['row_id']], **r) for r in scores]
    children = read_json('analysis/timing.json')['children']
    assert len({c['task'] for c in children}) == len(children)
    assert sum(c['role'] == 'initial' for c in children) == 4
    assert sum(c['role'] == 'followup' for c in children) == 12
    for child in children:
        parse = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
        assert (parse(child['observed_complete_utc']) - parse(child['dispatch_utc'])).total_seconds() == child['conservative_seconds']
    print('Frozen inputs/prompts, 16 outputs, 12 blinded rows, target rules and distinct task names verified.')


if __name__ == '__main__':
    main()
