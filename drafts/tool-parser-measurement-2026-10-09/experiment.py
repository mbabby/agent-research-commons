#!/usr/bin/env python3
"""Synthetic parser measurement only. Never dispatches tools or uses a network."""
import argparse
import hashlib
import json
import platform
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRACKET = re.compile(r'\[get_weather\(city=("(?:[^"\\]|\\.)*")\)\]')


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


DECODER = json.JSONDecoder(object_pairs_hook=unique_pairs)


def validate(value):
    if not isinstance(value, dict) or set(value) != {'name', 'arguments'}:
        raise ValueError('invalid call fields')
    args = value['arguments']
    if value['name'] != 'get_weather' or not isinstance(args, dict) or set(args) != {'city'}:
        raise ValueError('invalid tool or argument fields')
    if not isinstance(args['city'], str) or not args['city'].strip():
        raise ValueError('invalid city')
    return dict(status='call', name=value['name'], arguments=args)


def bracket_value(match):
    return {'name': 'get_weather', 'arguments': {'city': json.loads(match.group(1))}}


def parse(strategy, row):
    text = row['text'].strip()
    try:
        if strategy != 'text_scanning_fallback' and row['channel'] == 'assistant_text':
            return {'status': 'no_call'}
        if strategy == 'envelope_json_only':
            return validate(DECODER.decode(text))
        if strategy == 'envelope_normalizer':
            match = BRACKET.fullmatch(text)
            return validate(bracket_value(match) if match else DECODER.decode(text))
        if strategy != 'text_scanning_fallback':
            raise ValueError('unknown strategy')
        match = BRACKET.search(text)
        brace = text.find('{')
        # Deliberately searches prose and ignores the envelope. First candidate wins.
        if brace >= 0 and (match is None or brace < match.start()):
            value, _ = DECODER.raw_decode(text[brace:])
            return validate(value)
        if match:
            return validate(bracket_value(match))
        return {'status': 'no_call' if row['channel'] == 'assistant_text' else 'reject'}
    except (ValueError, TypeError):
        return {'status': 'reject'}


def measure(rows):
    strategies = ['envelope_json_only', 'text_scanning_fallback', 'envelope_normalizer']
    records = []
    summary = {}
    for strategy in strategies:
        for row in rows:
            parsed = parse(strategy, row)
            expected = row['expected']
            records.append(dict(strategy=strategy, id=row['id'], profile=row['profile'],
                                channel=row['channel'], raw=row['text'], expected=expected,
                                parsed=parsed, correct=(parsed == expected)))
        summary[strategy] = {}
        for profile in ['canonical', 'alternate', 'control']:
            items = [r for r in records if r['strategy'] == strategy and r['profile'] == profile]
            call_cases = [r for r in items if r['expected']['status'] == 'call']
            no_call_cases = [r for r in items if r['expected']['status'] == 'no_call']
            invalid = [r for r in items if r['expected']['status'] == 'reject']
            summary[strategy][profile] = {
                'correct': sum(r['correct'] for r in items), 'total': len(items),
                'missed_expected_calls': sum(not r['correct'] for r in call_cases),
                'expected_call_cases': len(call_cases),
                'false_calls': sum(r['parsed']['status'] == 'call' for r in no_call_cases),
                'no_call_cases': len(no_call_cases),
                'invalid_calls_accepted': sum(r['parsed']['status'] == 'call' for r in invalid),
                'invalid_cases': len(invalid),
            }
    return dict(summary=summary, records=records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'results.json')
    args = parser.parse_args()
    raw = (ROOT / 'fixtures.json').read_bytes()
    rows = json.loads(raw)
    assert len(rows) == 18 and len({r['id'] for r in rows}) == 18
    result = measure(rows)
    result.update(status='synthetic_method_experiment', fixtures_sha256=hashlib.sha256(raw).hexdigest(),
                  python=platform.python_version(), fixture_count=len(rows),
                  strategy_count=3, model_calls=0, dispatched_tools=0)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
