"""Deterministic synthetic ledger arithmetic; Python 3.9+ standard library."""
import json
from pathlib import Path


def grade(expected, answer):
    if len(answer) != 2 or any(x is not None and type(x) is not int for x in answer):
        raise ValueError('answer must have two integer-or-null facets')
    if all(x is None for x in answer):
        return 'abstain'
    if any(x is not None and x != y for x, y in zip(answer, expected)):
        return 'wrong'
    return 'correct' if all(x is not None for x in answer) else 'partial'


def ratio(num, den):
    return {'numerator': num, 'denominator': den, 'value': num / den if den else 'N/A'}


def metrics(labels):
    if any(x not in ('correct', 'wrong', 'partial', 'abstain') for x in labels):
        raise ValueError('unknown outcome')
    c, w, p, a = (labels.count(x) for x in ('correct', 'wrong', 'partial', 'abstain'))
    n, t = c + w + p + a, c + w + p
    return {'counts': dict(correct=c, wrong=w, partial=p, abstain=a),
            'per_assigned_wrong': ratio(w, n), 'attempted_wrong': ratio(w, t),
            'answer_coverage': ratio(t, n), 'full_correct_completion': ratio(c, n),
            'partial_as_failure_per_assigned': ratio(w + p, n),
            'partial_as_failure_attempted': ratio(w + p, t),
            'partial_excluded_attempted_wrong': ratio(w, c + w),
            'aa_denominator_illustration': ratio(w, w + p + a)}


def evaluate(rows):
    seen, cases, labels = set(), [], {'A': [], 'B': []}
    for row in rows:
        if row['id'] in seen or set(row['agents']) != {'A', 'B'}:
            raise ValueError('unique IDs and paired A/B answers required')
        if type(row['a']) is not int or type(row['b']) is not int:
            raise ValueError('integer inputs required')
        seen.add(row['id'])
        expected = [row['a'] + row['b'], row['a'] * row['b']]
        outcomes = {agent: grade(expected, ans) for agent, ans in row['agents'].items()}
        cases.append(dict(id=row['id'], expected=expected, outcomes=outcomes))
        for agent, label in outcomes.items():
            labels[agent].append(label)
    return {'kind': 'constructed_toy_not_model_run', 'cases': cases,
            'agents': {agent: metrics(outcomes) for agent, outcomes in labels.items()}}


if __name__ == '__main__':
    rows = json.loads(Path(__file__).with_name('ledger.json').read_text())
    print(json.dumps(evaluate(rows), indent=2, sort_keys=True))
