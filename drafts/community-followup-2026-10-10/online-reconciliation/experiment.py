"""Local online reconciliation model; Python standard library, no external actions."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCOPE = {'account': 'acct1', 'environment': 'mock', 'operation': 'A'}


class Provider:
    def __init__(self, case):
        self._case = case
        self.tick = -1
        self.mutation_authorized = True
        self.read_authorized = True
        self.history = []
        self.key_retained = False
        self.trace = []
        self.reads = 0
        self.forbidden_reads = 0
        self.retry_submissions = 0
        if case['initial_commit']:
            self._commit('initial')
        else:
            self.trace.append({'tick': -1, 'event': 'initial_request_dropped'})

    def _commit(self, origin):
        record = dict(SCOPE, tick=self.tick, authorized=self.mutation_authorized,
                      resource='resource-' + str(len(self.history) + 1), origin=origin)
        self.history.append(record)
        self.key_retained = True
        self.trace.append(dict(record, event='commit'))

    def advance(self, tick):
        if tick != self.tick + 1:
            raise ValueError('Logical clock must advance exactly one tick')
        self.tick = tick
        for event in self._case['authorization_events']:
            if event['tick'] == tick:
                if 'mutation' in event:
                    self.mutation_authorized = event['mutation']
                if 'read' in event:
                    self.read_authorized = event['read']
                self.trace.append(dict(event, event='authorization_change'))
        if tick >= self._case['key_expires_at'] and self.key_retained:
            self.key_retained = False
            self.trace.append({'tick': tick, 'event': 'key_expired'})

    def client_context(self):
        return {'tick': self.tick, 'mutation_authorized': self.mutation_authorized,
                'read_authorized': self.read_authorized,
                'deduplication_contract': self._case['deduplication_contract'],
                'key_expires_at': self._case['key_expires_at']}

    def read(self):
        self.reads += 1
        if not self.read_authorized:
            self.forbidden_reads += 1
            observation = {'status': 'read_denied'}
        elif self.tick in self._case['failed_reads']:
            observation = {'status': 'read_failed'}
        elif self.history and self.tick >= self._case['receipt_at']:
            observation = dict(SCOPE, status='succeeded', resource=self.history[0]['resource'])
        else:
            observation = {'status': 'unknown'}
        self.trace.append({'tick': self.tick, 'event': 'read', 'observation': observation})
        return dict(observation)

    def retry(self):
        self.retry_submissions += 1
        if self.key_retained:
            self.trace.append({'tick': self.tick, 'event': 'deduplicated_retry'})
        else:
            self._commit('retry_original_key')
        response = {'status': 'response_lost'}
        self.trace.append({'tick': self.tick, 'event': 'retry_response', 'response': response})
        return response


def decide(context, observation, retried, variant):
    """No fixture, future schedule, ledger, or provider object is available here."""
    if (observation.get('status') == 'succeeded'
            and all(observation.get(k) == v for k, v in SCOPE.items())):
        return 'resolve'
    if observation['status'] == 'read_denied':
        return 'stop_unknown'
    if observation['status'] != 'unknown' or retried:
        return 'wait'
    permitted = context['mutation_authorized'] or variant == 'ignore_mutation_withdrawal'
    protected = (context['deduplication_contract']
                 and context['tick'] < context['key_expires_at'])
    if permitted and (protected or variant == 'retry_expired_key'):
        return 'retry'
    return 'wait'


def run(case, policy, deadline):
    provider = Provider(case)
    retried = False
    resolved = False
    stop_reason = 'deadline'
    decisions = []
    for tick in range(deadline + 1):
        provider.advance(tick)
        context = provider.client_context()
        if not context['read_authorized'] and policy != 'ignore_read_withdrawal':
            stop_reason = 'read_authorization_withdrawn'
            decisions.append({'tick': tick, 'context': context, 'action': 'stop_without_read'})
            break
        observation = provider.read()
        action = decide(context, observation, retried, policy)
        decisions.append({'tick': tick, 'context': context,
                          'observation': observation, 'action': action})
        if action == 'resolve':
            resolved = True
            stop_reason = 'bound_receipt'
            break
        if action == 'stop_unknown':
            stop_reason = 'read_denied'
            break
        if action == 'retry':
            provider.retry()
            retried = True
        if policy == 'one_shot':
            stop_reason = 'one_shot_budget'
            break
    unauthorized = sum(not item['authorized'] for item in provider.history)
    metrics = {'historical_effects': len(provider.history),
               'duplicates': max(len(provider.history) - 1, 0),
               'unauthorized_effects': unauthorized,
               'unauthorized_read_attempts': provider.forbidden_reads,
               'reads': provider.reads, 'retry_submissions': provider.retry_submissions,
               'unresolved': int(not resolved),
               'resolved': int(resolved and len(provider.history) == 1 and not unauthorized)}
    return {'case': case['id'], 'policy': policy, 'deadline': deadline,
            'last_tick': provider.tick, 'stop_reason': stop_reason,
            'metrics': metrics, 'decisions': decisions,
            'provider_trace': provider.trace, 'history': provider.history}


def assert_safe(result):
    for metric in ('duplicates', 'unauthorized_effects', 'unauthorized_read_attempts'):
        assert result['metrics'][metric] == 0, metric


def negative_controls(fixtures):
    controls = []
    for case_id, variant, expected in (
        ('expired_key_late_receipt', 'retry_expired_key', 'duplicates'),
        ('mutation_withdrawn', 'ignore_mutation_withdrawal', 'unauthorized_effects'),
        ('read_withdrawn', 'ignore_read_withdrawal', 'unauthorized_read_attempts'),
    ):
        case = next(c for c in fixtures['cases'] if c['id'] == case_id)
        result = run(case, variant, fixtures['deadline'])
        try:
            assert_safe(result)
        except AssertionError as error:
            detected = str(error)
        else:
            raise AssertionError('Unsafe control escaped: ' + variant)
        assert detected == expected, (variant, detected)
        controls.append({'detected_violation': detected, 'result': result})
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'results.json')
    args = parser.parse_args()
    freeze = json.loads((ROOT / 'freeze.json').read_text())
    hashes = {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in freeze['files']}
    if hashes != freeze['files']:
        raise SystemExit('Frozen input mismatch; explicit protocol revision required')
    fixtures = json.loads((ROOT / 'fixtures.json').read_text())
    runs = [run(case, policy, fixtures['deadline'])
            for case in fixtures['cases'] for policy in ('one_shot', 'online')]
    for result in runs:
        case = next(c for c in fixtures['cases'] if c['id'] == result['case'])
        assert result['metrics'] == case['expected'][result['policy']], result['case']
        assert_safe(result)
    totals = {policy: {m: sum(r['metrics'][m] for r in runs if r['policy'] == policy)
                       for m in runs[0]['metrics']} for policy in ('one_shot', 'online')}
    controls = negative_controls(fixtures)
    output = {'kind': 'synthetic online reconciliation', 'protocol_version': 1,
              'source_sha256': dict(hashes, **{n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest()
                                             for n in ('experiment.py', 'test_experiment.py')}),
              'runs': runs, 'totals': totals, 'negative_controls': controls}
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'totals': totals, 'negative_controls_detected': len(controls)}, indent=2))


if __name__ == '__main__':
    main()
