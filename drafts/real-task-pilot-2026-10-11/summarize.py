"""Aggregate manual source-reviewed labels, never automatically judge answer text."""
import json
import sys
from pathlib import Path


def summarize(labels):
    if len(labels) != 8 or any(label not in {'C', 'W', 'P', 'A'} for label in labels):
        raise ValueError('Exactly eight C/W/P/A labels in Q1..Q8 order required')
    counts = {label: labels.count(label) for label in 'CWPA'}
    c, w, p, a = (counts[label] for label in 'CWPA')
    n, t = c + w + p + a, c + w + p
    pairs = {'W/N': (w,n), 'W/T': (w,t), 'T/N': (t,n), 'C/N': (c,n),
             '(W+P)/N': (w+p,n), '(W+P)/T': (w+p,t), 'W/(C+W)': (w,c+w),
             'W/(W+P+A)': (w,w+p+a)}
    return {'counts': counts, 'N': n, 'T': t,
            'rates': {key: {'numerator': x, 'denominator': y, 'value': x/y if y else None}
                      for key, (x,y) in pairs.items()},
            'locally_usable': c >= 7 and w == 0 and t == 8 and
                              all(labels[index] == 'C' for index in (1,2,4,5))}


def main():
    directory = Path(__file__).resolve().parent
    filename = 'repair-adjudication.json' if '--repair' in sys.argv else 'adjudication.json'
    scores = json.loads((directory / filename).read_text())
    results = {run: summarize([rows['labels']['Q' + str(i)] for i in range(1, 9)])
               for run, rows in scores['final_runs'].items()}
    print(json.dumps({'stage': 'posthoc_assisted_repair' if '--repair' in sys.argv else 'first_output',
                      'runs': results,
                      'locally_usable_briefs': sum(r['locally_usable'] for r in results.values()),
                      'unique_assignments': 1, 'replicate_briefs': len(results),
                      'official_accepted_outputs': 0,
                      'financial_cost_per_independently_accepted_task': None}, indent=2))


if __name__ == '__main__':
    main()
