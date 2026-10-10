#!/usr/bin/env python3
"""Synthetic label-evaluator comparison; no network, dependencies, or model calls."""
import argparse
import copy
import datetime
import hashlib
import itertools
import json
import pathlib
import platform

ROOT = pathlib.Path(__file__).resolve().parent


def evaluate_retained(fixture, query, claims, decisions):
    if query['candidate'] not in fixture['output_contract']['labels']:
        return 'invalid_output'
    if any(query.get(key) != value for key, value in fixture['scope'].items()):
        return 'inapplicable_scope'
    rule = fixture['rules'].get(query['rule_version'])
    if rule is None:
        return 'inapplicable_rule'
    start, end = rule['applies_to_release']
    if query['release'] < start or (end is not None and query['release'] > end):
        return 'inapplicable_rule'
    matching = [d for d in decisions if d['rule_version'] == query['rule_version']]
    if len(matching) != 1:
        return 'unresolved'
    decision = matching[0]
    available = {c['id'] for c in claims}
    if not set(decision.get('considered_corrections', [])).issubset(available):
        return 'unresolved'
    if decision['status'] != 'selected_in_fixture':
        return 'unresolved'
    return 'pass' if query['candidate'] == decision['selected_label'] else 'fail'


def evaluate_overwrite(fixture, query, expected_label):
    if query['candidate'] not in fixture['output_contract']['labels']:
        return 'invalid_output'
    return 'pass' if query['candidate'] == expected_label else 'fail'


def coverage(rows):
    statuses = [r['actual'] for r in rows]
    counts = {
        'decided': sum(x in ('pass', 'fail') for x in statuses),
        'unresolved': statuses.count('unresolved'),
        'inapplicable': sum(x.startswith('inapplicable_') for x in statuses),
        'invalid_output': statuses.count('invalid_output'),
        'total': len(statuses),
    }
    counts['decided_coverage'] = counts['decided'] / counts['total']
    counts['matches_fixture_expectation'] = sum(r['matches_expected'] for r in rows)
    return counts


def run(fixture, retained=evaluate_retained):
    rows = {'overwrite': [], 'retained': []}
    retained_claims = []
    for corrections in itertools.permutations(fixture['corrections']):
        claims = []
        expected_label = fixture['original_output']
        for correction in corrections:
            claims.append(copy.deepcopy(correction))
            expected_label = correction['proposed_output']
        before_label = expected_label
        decisions_before = [d for d in fixture['decisions'] if d['rule_version'] == 'v1']
        decisions_after = copy.deepcopy(fixture['decisions'])
        selected = [d for d in decisions_after if d['status'] == 'selected_in_fixture']
        for decision in selected:
            expected_label = decision['selected_label']
        for query in fixture['queries']:
            before = query['stage'] == 'before_change'
            actuals = {
                'overwrite': evaluate_overwrite(fixture, query, before_label if before else expected_label),
                'retained': retained(fixture, query, claims, decisions_before if before else decisions_after),
            }
            for method, actual in actuals.items():
                rows[method].append({
                    'order': [c['id'] for c in corrections],
                    'query': query['id'], 'candidate': query['candidate'],
                    'stage': query['stage'], 'rule_version': query['rule_version'],
                    'actual': actual, 'expected': query['expected'],
                    'matches_expected': actual == query['expected'],
                })
        retained_claims.append({'order': [c['id'] for c in corrections], 'claims_after_v2': claims,
                                'matches_original_claims': sorted(claims, key=lambda c: c['id']) == sorted(fixture['corrections'], key=lambda c: c['id'])})
    order_changes = {}
    for method, records in rows.items():
        order_changes[method] = [q['id'] for q in fixture['queries'] if len({r['actual'] for r in records if r['query'] == q['id']}) > 1]
    return {'rows': rows, 'coverage': {k: coverage(v) for k, v in rows.items()},
            'order_sensitive_queries': order_changes, 'retained_claims': retained_claims}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=pathlib.Path, default=ROOT / 'results.json')
    args = parser.parse_args()
    fixture = json.loads((ROOT / 'fixtures.json').read_text())
    freeze = json.loads((ROOT / 'freeze.json').read_text())
    digests = {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in freeze['files']}
    if digests != freeze['files']:
        raise SystemExit('Frozen protocol/fixture digest mismatch')
    results = run(fixture)
    premature = copy.deepcopy(fixture)
    premature['decisions'][0].update(status='selected_in_fixture', selected_label='incident')
    premature_results = run(premature)

    def ignore_scope(f, q, claims, decisions):
        q = dict(q, **f['scope'])
        return evaluate_retained(f, q, claims, decisions)

    no_scope_results = run(fixture, retained=ignore_scope)
    negatives = {}
    for name, mutant in [('premature_adjudication', premature_results), ('scope_bypass', no_scope_results)]:
        failures = [r for r in mutant['rows']['retained'] if not r['matches_expected']]
        negatives[name] = {'detected': bool(failures), 'failed_checks': failures}
    checks = {
        'all_retained_expectations_match': all(r['matches_expected'] for r in results['rows']['retained']),
        'retained_order_invariant': not results['order_sensitive_queries']['retained'],
        'claims_preserved': all(x['matches_original_claims'] for x in results['retained_claims']),
        'negative_controls_detected': all(x['detected'] for x in negatives.values()),
    }
    document = {
        'kind': 'synthetic_evaluator_execution',
        'executed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python_version': platform.python_version(),
        'source_sha256': dict(digests, **{'experiment.py': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}),
        'observations': results, 'negative_controls': negatives, 'checks': checks,
        'all_checks_pass': all(checks.values()),
        'limitations': ['No real experts, model calls or external adoption data.', 'Expected labels and scope are stipulated, not scientifically validated.', 'Baseline deliberately omits provenance/version/scope, so result does not compare all evaluator designs.'],
    }
    args.output.write_text(json.dumps(document, indent=2) + '\n')
    print(json.dumps({'coverage': results['coverage'], 'order_sensitive_queries': results['order_sensitive_queries'], 'checks': checks}, indent=2))
    return 0 if document['all_checks_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
