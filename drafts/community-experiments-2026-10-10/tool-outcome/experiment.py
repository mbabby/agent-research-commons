"""Deterministic local experiment. No network, credentials, or third-party packages."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
SCOPE = {'account': 'acct1', 'environment': 'mock'}


class Provider:
    def __init__(self):
        self.history = []
        self.resources = {}
        self.keys = {}
        self.receipts = {}
        self.mutation_authorized = True
        self.read_authorized = True
        self.events = []

    def create(self, operation, key, payload='P'):
        scoped_key = (SCOPE['account'], SCOPE['environment'], key)
        if scoped_key in self.keys:
            old_payload, receipt = self.keys[scoped_key]
            if old_payload != payload:
                raise ValueError('Same key with different parameters')
            self.events.append({'event': 'deduplicated', 'operation': operation})
            return dict(receipt)
        resource = 'resource-' + str(len(self.history) + 1)
        receipt = dict(SCOPE, operation=operation, resource=resource, status='succeeded')
        self.history.append({'operation': operation, 'resource': resource,
                             'authorized': self.mutation_authorized})
        self.resources[resource] = {'operation': operation, 'payload': payload, 'visible': True}
        self.keys[scoped_key] = (payload, receipt)
        self.receipts[operation] = receipt
        self.events.append({'event': 'committed', **self.history[-1]})
        return dict(receipt)

    def observe(self, kind):
        if not self.read_authorized:
            return {'kind': 'read_denied'}
        if kind == 'receipt':
            receipt = self.receipts.get('A')
            return {'kind': 'receipt', 'value': dict(receipt) if receipt else None}
        if kind == 'lookup':
            # Content search does not expose operation identity.
            return {'kind': 'lookup', 'matches': [r['payload'] for r in self.resources.values()
                                                 if r['visible'] and r['payload'] == 'P']}
        return {'kind': kind}

    def event(self, text):
        verb, _, argument = text.partition(':')
        self.events.append({'event': text})
        if verb == 'commit':
            self.create(argument, 'K_' + argument)
        elif verb in ('hide', 'reveal', 'delete'):
            for rid, resource in list(self.resources.items()):
                if resource['operation'] == argument:
                    if verb == 'delete':
                        del self.resources[rid]
                    else:
                        resource['visible'] = verb == 'reveal'
        elif verb == 'expire':
            self.keys.pop((SCOPE['account'], SCOPE['environment'], 'K_' + argument), None)
        elif verb == 'withdraw':
            self.mutation_authorized = False
        elif verb == 'observe':
            return self.observe(argument)
        elif verb not in ('drop', 'timeout'):
            raise ValueError('Unknown fixture event: ' + text)
        return None


def bound_success(observation):
    receipt = observation.get('value') or {}
    return (observation['kind'] == 'receipt' and receipt.get('operation') == 'A'
            and receipt.get('status') == 'succeeded'
            and all(receipt.get(k) == v for k, v in SCOPE.items()))


def choose(observations, protected, authorized, policy):
    # Only public observations and contractual state cross the policy boundary.
    if policy == 'blind':
        return 'fresh_retry'
    if policy == 'content_is_success' and any(o.get('matches') for o in observations):
        return 'claim_success'
    if policy == 'absence_is_failure' and any(o.get('matches') == [] for o in observations):
        return 'fresh_retry'
    if policy == 'expired_is_safe':
        return 'same_retry'
    if any(bound_success(o) for o in observations):
        return 'claim_success'
    if protected and (authorized or policy == 'ignore_authorization'):
        return 'same_retry'
    return 'stop_unknown'


def simulate(case, policy):
    provider = Provider()
    observations = []
    for event in case['events']:
        observation = provider.event(event)
        if observation is not None:
            observations.append(observation)
    action = choose(observations, case['deduplication_protected'],
                    provider.mutation_authorized, policy)
    classification = 'unknown'
    if action in ('fresh_retry', 'same_retry'):
        key = 'fresh-K_A' if action == 'fresh_retry' else 'K_A'
        receipt = provider.create('A', key)
        observations.append({'kind': 'receipt', 'value': receipt})
        classification = 'succeeded'
    elif action == 'claim_success':
        classification = 'succeeded'
    a_commits = sum(item['operation'] == 'A' for item in provider.history)
    unauthorized = sum(not item['authorized'] for item in provider.history)
    metrics = {'historical_effects': len(provider.history),
               'duplicates': max(a_commits - 1, 0),
               'unauthorized_effects': unauthorized,
               'unresolved': int(classification == 'unknown'),
               'completion': int(classification == 'succeeded' and a_commits == 1 and not unauthorized),
               'false_success': int(classification == 'succeeded' and a_commits == 0)}
    return {'case': case['id'], 'policy': policy, 'action': action,
            'classification': classification, 'observations': observations,
            'events': provider.events, 'history': provider.history,
            'remaining_resources': provider.resources, 'metrics': metrics}


def assert_safety(result):
    for metric in ('duplicates', 'unauthorized_effects', 'false_success'):
        assert result['metrics'][metric] == 0, metric


def negative_controls(cases):
    controls = []
    for case_id, policy, violation in (
        ('identical_request', 'content_is_success', 'false_success'),
        ('authorization_withdrawn', 'ignore_authorization', 'unauthorized_effects'),
        ('manual_deletion', 'absence_is_failure', 'duplicates'),
        ('expired_key', 'expired_is_safe', 'duplicates'),
    ):
        result = simulate(next(c for c in cases if c['id'] == case_id), policy)
        try:
            assert_safety(result)
        except AssertionError as exc:
            detected = str(exc)
        else:
            raise AssertionError('Negative control escaped detection: ' + policy)
        assert detected == violation, (policy, detected)
        controls.append({'expected_violation': violation, 'detected_violation': detected,
                         'result': result})
    return controls


def main():
    fixtures = json.loads((ROOT / 'fixtures.json').read_text())
    runs = [simulate(case, policy) for case in fixtures['cases'] for policy in ('blind', 'evidence')]
    for run in runs:
        case = next(c for c in fixtures['cases'] if c['id'] == run['case'])
        for metric, expected in case['expected'][run['policy']].items():
            assert run['metrics'][metric] == expected, (run['case'], run['policy'], metric)
        if run['policy'] == 'evidence':
            assert_safety(run)
    aggregates = {policy: {metric: sum(r['metrics'][metric] for r in runs if r['policy'] == policy)
                          for metric in runs[0]['metrics']} for policy in ('blind', 'evidence')}
    result = {'synthetic': True, 'protocol_version': 1,
              'input_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                               for name in ('protocol.md', 'fixtures.json', 'experiment.py')},
              'runs': runs, 'aggregates': aggregates,
              'negative_controls': negative_controls(fixtures['cases'])}
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'aggregates': aggregates, 'negative_controls_detected': len(result['negative_controls'])}, indent=2))


if __name__ == '__main__':
    main()
