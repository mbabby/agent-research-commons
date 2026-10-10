"""Deterministic local experiment. No network, model calls, or real side effects."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / 'manifest.json').read_text())
CASES = json.loads((ROOT / 'cases.json').read_text())
CHECKPOINTS = MANIFEST['checkpoints']


def select_deployment(name):
    return deepcopy(MANIFEST['bundles'][name])


def migrate(checkpoint):
    if checkpoint['semantics'] != 'cents-v1':
        raise ValueError('migration requires cents-v1')
    result = deepcopy(checkpoint)
    result.update(semantics='dollars-v2', amount=format(Decimal(checkpoint['amount']) / 100, '.2f'))
    return result


def compensate(ledger):
    # This deliberately idealized local inverse is NOT a real payment refund API.
    ledger['charged_cents'] = 0
    ledger['reserved_items'] = 0


def run(case):
    bundle = select_deployment(case['bundle'])
    bundle.update(case.get('substitute', {}))
    checkpoint = deepcopy(CHECKPOINTS[case.get('checkpoint', 'old')])
    ledger = deepcopy(checkpoint['ledger'])
    before = deepcopy(ledger)
    trace = []
    if case.get('migrate'):
        checkpoint = migrate(checkpoint)
        trace.append({'stage': 'migration', 'implementation': 'cents-to-dollars-v1', 'amount': checkpoint['amount']})
    prompt = MANIFEST['prompts'][bundle['prompt']]
    trace.append({'stage': 'checkpoint', 'semantics': checkpoint['semantics'], 'required': prompt['checkpoint_semantics']})
    status = 'checkpoint-rejected'
    if checkpoint['semantics'] == prompt['checkpoint_semantics']:
        # A fixed planner interprets the prompt contract; it is not an LLM.
        arguments = {prompt['field']: checkpoint['amount']}
        trace.append({'stage': 'prompt', 'implementation': bundle['prompt'], 'arguments': arguments,
                      'model_id_metadata': bundle['model'], 'model_called': False})
        schema = MANIFEST['schemas'][bundle['schema']]
        trace.append({'stage': 'schema', 'implementation': bundle['schema'], 'required_field': schema['field']})
        status = 'schema-rejected'
        if set(arguments) == {schema['field']}:
            tool = MANIFEST['tools'][bundle['tool']]
            status = 'tool-contract-rejected'
            checkpoint_unit = checkpoint['semantics'].split('-')[0]
            if case.get('unsafe') or checkpoint_unit == schema['unit'] == tool['unit']:
                # Both tool versions accept `amount`, exposing shape-compatible unit drift.
                number = Decimal(arguments['amount'])
                cents = number if tool['unit'] == 'cents' else number * 100
                ledger['charged_cents'] += int(cents)
                trace.append({'stage': 'tool', 'implementation': bundle['tool'], 'interpreted_unit': tool['unit'], 'added_cents': int(cents)})
                status = 'charged' if ledger['charged_cents'] == 1250 else 'wrong-charge'
    return {'id': case['id'], 'requested_bundle': bundle, 'expected': case['expected'],
            'observed': {'status': status, 'charged_cents': ledger['charged_cents']},
            'ledger_before': before, 'ledger_after': ledger, 'trace': trace}


def main():
    results = [run(case) for case in CASES]
    ledger = {'reserved_items': 1, 'charged_cents': 1250}
    original = deepcopy(ledger)
    selected = select_deployment('old')
    after_rollback = deepcopy(ledger)
    compensate(ledger)
    output = {'scope': 'synthetic deterministic stubs; model IDs metadata only',
              'results': results, 'rollback_and_compensation': {
                  'before': original, 'selected_deployment': selected,
                  'after_deployment_rollback': after_rollback,
                  'after_explicit_synthetic_compensation': ledger}}
    (ROOT / 'results.json').write_text(json.dumps(output, indent=2) + '\n')
    mismatches = [r['id'] for r in results if r['observed'] != r['expected']]
    print(json.dumps({'cases': len(results), 'mismatches': mismatches}))
    return bool(mismatches)


if __name__ == '__main__':
    raise SystemExit(main())
