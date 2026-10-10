#!/usr/bin/env python3
"""Deterministic hypothetical atomic-server MOCK; no browser or network access."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
TASK_FIELDS = ('origin', 'account', 'workspace', 'target', 'effect')
SCOPED_FIELDS = TASK_FIELDS + ('action_version',)
POLICIES = ('precheck_only', 'atomic_scoped', 'atomic_global', 'bypass_compare', 'all_reject')
FROZEN = {
    'protocol.md': 'be6805db44fce827d2476b464c52566f926b6734a7ea54e59523f5caa6862da1',
    'fixtures.json': '5a348cc4b900393d8147de1afafdd581f09c62ade6f4809b29b18883e9047923',
}


def object_key(state):
    return '/'.join(state[field] for field in ('account', 'workspace', 'target'))


class World:
    def __init__(self, base, fixture, mode):
        self.state = deepcopy(base)
        self.fixture = deepcopy(fixture)
        self.mode = mode
        self.documents = {'/'.join((account, workspace, target)): 'active'
                          for account in ('A', 'B') for workspace in ('W1', 'W2')
                          for target in ('D17', 'D18')}
        self.ledger = []
        self.client_trace = []
        self.world_events = []
        self.calls = 0
        self.submissions = 0
        self.applied_events = set()
        self.boundary = None
        self.request = None
        self.server_result = None

    def _events_at(self, when):
        for index, event in enumerate(self.fixture['events']):
            if event['when'] != when or index in self.applied_events:
                continue
            before = deepcopy(self.state)
            self.state.update(event['set'])
            self.state['global_version'] += 1
            if event['version_scope'] == 'action':
                self.state['action_version'] += 1
            self.applied_events.add(index)
            self.world_events.append({'when': when, 'before': before,
                                      'after': deepcopy(self.state)})

    def call(self, action, payload=None):
        self.calls += 1
        if self.calls > 3:
            raise RuntimeError('client call budget exceeded')
        if action == 'observe':
            self._events_at('before_observe')
            result = deepcopy(self.state)
        elif action == 'submit':
            self.submissions += 1
            if self.submissions > 1:
                raise RuntimeError('automatic mutation retry is outside protocol')
            self.request = deepcopy(payload)
            self._events_at('before_commit')
            self.boundary = deepcopy(self.state)
            # Hypothetical critical section begins. No event application until
            # after permission validation, comparison and document mutation.
            fields = SCOPED_FIELDS + (('global_version',) if self.mode == 'atomic_global' else ())
            mismatched = [field for field in fields if payload[field] != self.state[field]]
            if not self.state['permission']:
                response = {'status': 'authorization_rejected'}
            elif self.mode == 'all_reject':
                response = {'status': 'forced_rejection'}
            elif self.mode in ('atomic_scoped', 'atomic_global') and mismatched:
                response = {'status': 'conflict', 'fields': mismatched}
            else:
                target = object_key(self.state)
                before = self.documents[target]
                after = {'archive': 'archived', 'delete': 'deleted'}[self.state['effect']]
                self.documents[target] = after
                receipt = {'operation_id': 'op1', 'binding': deepcopy(self.state),
                           'object': target, 'before': before, 'after': after,
                           'changed': before != after}
                self.ledger.append(receipt)
                response = {'status': 'receipt', 'receipt': deepcopy(receipt)}
            # Hypothetical critical section ends.
            self.server_result = deepcopy(response)
            if response['status'] == 'receipt':
                self._events_at('after_commit')
                if self.fixture.get('response_lost', False):
                    response = {'status': 'timeout', 'operation_id': 'op1'}
            result = response
        elif action == 'read_receipt':
            if self.fixture.get('receipt_read_fails', False):
                result = {'status': 'read_failed'}
            elif self.ledger and payload == self.ledger[0]['operation_id']:
                result = {'status': 'receipt', 'receipt': deepcopy(self.ledger[0])}
            else:
                result = {'status': 'not_found'}
        else:
            raise ValueError('unknown action: ' + action)
        self.client_trace.append({'action': action, 'payload': deepcopy(payload),
                                  'response': deepcopy(result)})
        return deepcopy(result)


def client(task, call):
    """No policy mode, fixture name, future schedule or oracle is passed here."""
    observed = call('observe')
    if not observed['permission'] or any(observed[field] != task[field] for field in TASK_FIELDS):
        return {'status': 'client_precheck_rejected'}
    response = call('submit', observed)
    if response['status'] == 'timeout':
        response = call('read_receipt', response['operation_id'])
        if response['status'] != 'receipt':
            return {'status': 'unknown'}
    if response['status'] == 'receipt':
        binding = response['receipt']['binding']
        if any(binding[field] != observed[field] for field in SCOPED_FIELDS):
            return {'status': 'unexpected_effect'}
        return {'status': 'completed', 'operation_id': response['receipt']['operation_id']}
    return {'status': response['status']}


def evaluate(world, task, initial_documents, decision):
    """Post-run adjudication; snapshots are not accessible through client API."""
    def task_authorized(binding):
        return binding['permission'] and (
            binding['origin'], binding['account'], binding['workspace'], binding['target'], binding['effect']) == (
            task['origin'], task['account'], task['workspace'], task['target'], task['effect'])

    effects = [receipt for receipt in world.ledger if receipt['changed']]
    stale = sum(receipt['binding']['action_version'] != world.request['action_version']
                for receipt in effects)
    wrong = sum(not task_authorized(receipt['binding']) or
                receipt['binding']['action_version'] != world.request['action_version']
                for receipt in effects)
    unauthorized = sum(not task_authorized(receipt['binding']) for receipt in effects)
    desired = deepcopy(initial_documents)
    desired[object_key(task)] = 'archived'
    achieved = world.documents == desired
    server_status = world.server_result['status'] if world.server_result else None
    # Reachability uses the actual decision-boundary snapshot, never final
    # post-commit context, and ignores only unrelated/global-version changes.
    scoped_still_valid = world.boundary is not None and task_authorized(world.boundary) and all(
        world.boundary[field] == world.request[field]
        for field in ('origin', 'account', 'workspace', 'target', 'effect', 'action_version'))
    rejected = server_status in ('conflict', 'forced_rejection', 'authorization_rejected')
    return {
        'submissions': world.submissions,
        'changed_state_effects': len(effects),
        'wrong_effects': wrong,
        'unauthorized_effects': unauthorized,
        'stale_version_effects': stale,
        'desired_state_achieved': achieved,
        'known_correct_completion': decision['status'] == 'completed' and achieved and wrong == 0,
        'conflicts': int(server_status == 'conflict'),
        'authorization_rejections': int(server_status == 'authorization_rejected'),
        'forced_rejections': int(server_status == 'forced_rejection'),
        'client_precheck_rejections': int(decision['status'] == 'client_precheck_rejected'),
        'unknown_outcomes': int(decision['status'] == 'unknown'),
        'unnecessary_rejections': int(rejected and scoped_still_valid),
        'client_calls': world.calls,
    }


def run_case(fixtures, fixture, policy):
    world = World(fixtures['base'], fixture, policy)
    initial_documents = deepcopy(world.documents)
    decision = client(deepcopy(fixtures['task']), world.call)
    return {'case': fixture['id'], 'policy': policy, 'decision': decision,
            'metrics': evaluate(world, fixtures['task'], initial_documents, decision),
            'client_trace': world.client_trace, 'world_only_events': world.world_events,
            'server_decision_boundary': world.boundary, 'server_request': world.request,
            'server_result': world.server_result, 'ledger': world.ledger,
            'initial_documents': initial_documents, 'final_documents': world.documents,
            'final_world': world.state}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in FROZEN}
    if hashes != FROZEN:
        raise SystemExit('Frozen inputs changed; an explicit protocol revision is required.')
    fixtures = json.loads((HERE / 'fixtures.json').read_text())
    runs = [run_case(fixtures, fixture, policy)
            for fixture in fixtures['cases'] for policy in POLICIES]
    totals = {policy: {metric: sum(run['metrics'][metric] for run in runs if run['policy'] == policy)
                       for metric in runs[0]['metrics']} for policy in POLICIES}
    result = {'kind': 'hypothetical atomic-server state-machine MOCK, not browser evidence',
              'python_version': platform.python_version(), 'frozen_sha256': hashes,
              'experiment_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'run_count': len(runs), 'totals': totals, 'runs': runs}
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
        print(json.dumps({'run_count': len(runs), 'totals': totals}, indent=2))
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
