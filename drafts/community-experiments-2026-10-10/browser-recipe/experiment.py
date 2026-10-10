#!/usr/bin/env python3
"""Local deterministic state-machine MOCK. Does not launch or model a browser engine."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
POLICIES = ('naive_saved', 'guarded_recipe', 'fresh_discovery',
            'always_abstain', 'unguarded_mutant')
FROZEN = {
    'protocol.md': 'f37a925777ec27bf733ba0daefb4f5d96c816f7255ad9062478818dac36c3bbd',
    'fixtures.json': '184d056f054a6f1898ed9ecd3e9822d08eabf9a74b60c24b2469543431cf336f',
}


def key(account, workspace, target):
    return '/'.join((account, workspace, target))


class World:
    def __init__(self, state):
        self.state = deepcopy(state)
        self.documents = {key(a, w, d): 'active'
                          for a in ('A', 'B') for w in ('W1', 'W2')
                          for d in state['documents']}
        self.ledger = []
        self.trace = []
        self.calls = 0
        self.submissions = 0
        self._bind_selection()

    def _bind_selection(self):
        for button in self.state['buttons']:
            if button['selection_bound']:
                button['target'] = self.state['selected']

    def call(self, action, argument=None):
        self.calls += 1
        if self.calls > 12:
            raise RuntimeError('synthetic tool budget exceeded')
        if action == 'observe':
            fields = ('origin', 'account', 'workspace', 'selected',
                      'documents', 'permission', 'buttons')
            result = {field: deepcopy(self.state[field]) for field in fields}
        elif action == 'open_document':
            if argument not in self.state['documents']:
                result = {'status': 'not_available'}
            else:
                self.state['selected'] = argument
                self._bind_selection()
                result = {'status': 'opened'}
        elif action == 'status':
            if self.state['status_read_fails']:
                result = {'status': 'read_failed'}
            else:
                result = {'status': 'read', 'value': self.documents.get(argument)}
        elif action == 'click':
            self.submissions += 1
            if self.submissions > 2:
                raise RuntimeError('synthetic submission budget exceeded')
            transition = self.state['before_click_change']
            if transition is not None:
                for button in self.state['buttons']:
                    button.update(transition)
                self.trace.append({'kind': 'hidden_transition', 'change': deepcopy(transition)})
                self.state['before_click_change'] = None
            button = next((b for b in self.state['buttons'] if b['id'] == argument), None)
            if button is None or not button['enabled']:
                result = {'status': 'unavailable'}
            else:
                event = {field: self.state[field] for field in
                         ('origin', 'account', 'workspace', 'permission')}
                event.update({'target': button['target'], 'effect': button['effect'],
                              'operation_id': 'op' + str(self.submissions)})
                object_key = key(event['account'], event['workspace'], event['target'])
                before = self.documents[object_key]
                if not self.state['permission']:
                    event.update({'outcome': 'rejected', 'before': before,
                                  'after': before, 'changed': False})
                    result = {'status': 'rejected', 'reason': 'permission'}
                else:
                    after = {'archive': 'archived', 'delete': 'deleted'}[event['effect']]
                    self.documents[object_key] = after
                    event.update({'outcome': 'committed', 'before': before,
                                  'after': after, 'changed': before != after})
                    result = ({'status': 'timeout'} if self.state['response_lost'] else
                              dict(event, status='receipt'))
                self.ledger.append(event)
        else:
            raise ValueError('unknown action ' + action)
        self.trace.append({'kind': 'call', 'action': action, 'argument': argument,
                           'result': deepcopy(result)})
        return deepcopy(result)


def decide(policy, task, memory, call):
    """Inputs contain no fixture ID, oracle facts or expected outcomes."""
    observation = call('observe')
    if policy == 'always_abstain':
        return {'status': 'abstained', 'reason': 'negative_control', 'locator_repairs': 0}
    naive = policy in ('naive_saved', 'unguarded_mutant')
    repairs = 0
    if naive:
        candidates = [b for b in observation['buttons'] if b['label'] == memory['label']]
        if not candidates:
            candidates = [b for b in observation['buttons'] if b['enabled']]
        if not candidates:
            return {'status': 'abstained', 'reason': 'no_control', 'locator_repairs': 0}
        chosen = candidates[0]
    else:
        if task['mode'] == 'inspect':
            return {'status': 'inspected', 'reason': 'current_instruction', 'locator_repairs': 0}
        expected = memory if policy == 'guarded_recipe' else task
        if any(observation[field] != task[field] or expected[field] != task[field]
               for field in ('origin', 'account', 'workspace')):
            return {'status': 'abstained', 'reason': 'context_mismatch', 'locator_repairs': 0}
        if not observation['permission']:
            return {'status': 'abstained', 'reason': 'permission', 'locator_repairs': 0}
        if observation['selected'] != task['target']:
            call('open_document', task['target'])
            observation = call('observe')
        candidates = [b for b in observation['buttons']
                      if b['enabled'] and b['target'] == task['target']
                      and b['effect'] == task['effect']]
        if policy == 'guarded_recipe':
            remembered = [b for b in candidates if b['label'] == memory['label']]
            if remembered:
                candidates = remembered
            elif len(candidates) == 1:
                repairs = 1
        if len(candidates) != 1:
            return {'status': 'abstained', 'reason': 'no_unique_intended_action',
                    'locator_repairs': repairs}
        chosen = candidates[0]
    response = call('click', chosen['id'])
    if response['status'] == 'timeout':
        state = call('status', key(task['account'], task['workspace'], task['target']))
        if naive and state['status'] == 'read_failed':
            response = call('click', chosen['id'])
        if response['status'] == 'timeout':
            return {'status': 'unknown', 'reason': 'no_operation_receipt',
                    'locator_repairs': repairs}
    if response['status'] == 'receipt':
        matches = task['mode'] == 'archive' and all(
            response[field] == task[field]
            for field in ('origin', 'account', 'workspace', 'target', 'effect'))
        status = 'success' if matches else 'unexpected_effect'
    else:
        status = 'rejected'
    return {'status': status, 'reason': 'observed_response', 'locator_repairs': repairs}


def initial_feasibility(state, task):
    """Oracle for initial reachability; independent of policy candidate filtering."""
    if task['mode'] != 'archive' or not state['permission']:
        return False
    if (state['origin'], state['account'], state['workspace']) != (
            task['origin'], task['account'], task['workspace']):
        return False
    for button in state['buttons']:
        reachable_target = (task['target'] in state['documents']
                            if button['selection_bound'] else button['target'] == task['target'])
        if reachable_target and button['enabled'] and button['effect'] == task['effect']:
            return True
    return False


def evaluate(world, initial_documents, initial_state, task, decision):
    def authorized(event):
        return (task['mode'] == 'archive' and event['permission'] and
                (event['origin'], event['account'], event['workspace'], event['target'], event['effect']) ==
                (task['origin'], task['account'], task['workspace'], task['target'], task['effect']))
    effects = [event for event in world.ledger if event['changed']]
    wrong = sum(not authorized(event) for event in effects)
    requested = key(task['account'], task['workspace'], task['target'])
    desired = deepcopy(initial_documents)
    if task['mode'] == 'archive':
        desired[requested] = 'archived'
    achieved = world.documents == desired
    declined = decision['status'] == 'abstained' and world.submissions == 0 and task['mode'] == 'archive'
    feasible = initial_feasibility(initial_state, task)
    return {
        'submissions': world.submissions,
        'committed_calls': sum(event['outcome'] == 'committed' for event in world.ledger),
        'changed_state_effects': len(effects), 'wrong_effects': wrong,
        'unauthorized_effects': wrong,
        'unauthorized_attempts': sum(not authorized(event) for event in world.ledger),
        'redundant_committed_noops': sum(event['outcome'] == 'committed' and not event['changed']
                                       for event in world.ledger),
        'desired_state_achieved': achieved,
        'known_correct_completion': achieved and decision['status'] in ('success', 'inspected'),
        'justified_abstentions': int(declined and not feasible),
        'unnecessary_abstentions': int(declined and feasible),
        'unknown_outcomes': int(decision['status'] == 'unknown'),
        'locator_repairs': decision['locator_repairs'], 'synthetic_calls': world.calls,
    }


def run_case(fixtures, fixture, policy):
    state = deepcopy(fixtures['base'])
    state.update(deepcopy(fixture.get('state', {})))
    if 'buttons' in fixture:
        state['buttons'] = deepcopy(fixture['buttons'])
    task = dict(fixtures['task'], **fixture.get('task', {}))
    world = World(state)
    initial_state = deepcopy(world.state)
    initial_documents = deepcopy(world.documents)
    decision = decide(policy, deepcopy(task), deepcopy(fixtures['memory']), world.call)
    return {'case': fixture['id'], 'policy': policy, 'task': task, 'decision': decision,
            'metrics': evaluate(world, initial_documents, initial_state, task, decision),
            'trace': world.trace, 'ledger': world.ledger,
            'initial_documents': initial_documents, 'final_documents': world.documents}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in FROZEN}
    if hashes != FROZEN:
        raise SystemExit('Frozen inputs changed; use an explicit protocol revision.')
    fixtures = json.loads((HERE / 'fixtures.json').read_text())
    runs = [run_case(fixtures, fixture, policy)
            for fixture in fixtures['cases'] for policy in POLICIES]
    totals = {policy: {metric: sum(run['metrics'][metric] for run in runs if run['policy'] == policy)
                       for metric in runs[0]['metrics']} for policy in POLICIES}
    result = {'kind': 'deterministic state-machine MOCK, not browser evidence',
              'python_version': platform.python_version(), 'frozen_sha256': hashes,
              'experiment_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'run_count': len(runs), 'totals': totals, 'runs': runs}
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(encoded)
        print(json.dumps({'run_count': len(runs), 'totals': totals}, indent=2))
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
