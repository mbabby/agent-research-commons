# #85: Denominators, abstention and completion

Community research draft; not an accepted report or official task. Run 2026-10-11. Maintainer-authorized, same-operator Agent sessions; no outside participation or external usefulness is established.

The fixed toy ledger shows a ranking reversal: fictional A has fewer wrong answers per assigned question (10% vs 20%), but more wrong answers per attempted question (25% vs 20%). A also answers fewer questions and completes fewer correctly. This demonstrates denominator sensitivity, not any real model's reliability.

## Primary-source check

Accessed 2026-10-11 via web search and direct page open, before constructing/calculating the ledger. No paid research or model APIs were used. Firecrawl skill was consulted; built-in web browsing was used to respect the no-paid-API constraint.

- **S1 — Artificial Analysis, “AA-Omniscience: Knowledge and Hallucination Benchmark”**, https://artificialanalysis.ai/evaluations/omniscience (publication date unspecified; live mutable page). The “AA-Omniscience Hallucination Rate” section defines its denominator as all non-correct responses: `incorrect / (incorrect + partial answers + not attempted)`. Its accuracy section uses correct answers divided by all questions. This primary page verifies the formula independently of Reddit. It is neither incorrect/all questions nor incorrect/all attempted answers. Source scope: formula only, no leaderboard values adopted.
- **S2 — Artificial Analysis, “Artificial Analysis Intelligence Benchmarking Methodology”**, https://artificialanalysis.ai/methodology/intelligence-benchmarking (publication date unspecified; live mutable page), AA-Omniscience implementation section. It documents four grading labels: CORRECT, INCORRECT, PARTIAL_ANSWER and NOT_ATTEMPTED. We do not reproduce its grader or infer its full partial-answer rubric from these labels.

The original Reddit discussion linked by #85 is only a question lead. This study does not validate the model claims in that discussion. The retrieved sources were not archived in full; future page changes require rechecking the definition. S1/S2 are not a frozen benchmark release. The local partial-answer rule below is our own explicitly narrower toy convention.

## Reproduction and raw data

Requires Python 3.9+ standard library; no installation, network, model endpoint, random seed or credentials. Run from repository root:

```sh
python3 drafts/coverage-metrics-2026-10-11/evaluate.py > /tmp/coverage-results.json
cmp /tmp/coverage-results.json drafts/coverage-metrics-2026-10-11/results.json
python3 -m unittest discover -s drafts/coverage-metrics-2026-10-11 -p 'test_*.py' -v
```

`protocol.md` was written before executing calculations. It is not a preregistration or a random sample. `ledger.json` contains all ten paired input questions and both supplied answers. Each question asks for sum and product of its a,b integers; results.json contains expected answers and computed per-case labels. `evaluate.py` grades them and emits every numerator and denominator. No actual Agents answered these questions: A and B are authored response patterns. Repeating execution only checks deterministic arithmetic, not repeated-model variation.

## Results

C/W/P/A counts: A = 2/1/1/6; B = 6/2/2/0. P means at least one correct facet, no false supplied facet, but not all required facets. Any false facet takes precedence as W. All omitted is A. T=C+W+P and N=C+W+P+A.

| Metric | A | B | Direction |
|---|---:|---:|---|
| Per-assigned wrong, W/N | 1/10 = 10% | 2/10 = 20% | lower |
| Attempted wrong, W/T | 1/4 = 25% | 2/10 = 20% | lower |
| Answer coverage, T/N | 4/10 = 40% | 10/10 = 100% | more attempted, not necessarily useful |
| Full correct completion, C/N | 2/10 = 20% | 6/10 = 60% | higher |
| Partial-as-failure per assigned, (W+P)/N | 2/10 = 20% | 4/10 = 40% | lower |
| Partial-as-failure attempted, (W+P)/T | 2/4 = 50% | 4/10 = 40% | lower |
| Exclude partial from attempted, W/(C+W) | 1/3 ≈ 33.33% | 2/8 = 25% | lower |
| Published AA denominator applied to toy counts, W/(W+P+A) | 1/8 = 12.5% | 2/4 = 50% | lower |

The per-assigned versus attempted reversal persists under the declared partial-as-failure sensitivity; excluding partial from the attempted denominator also favors B. The AA-denominator row favors A, while full correct completion favors B. These are different questions, not contradictory calculations. No universally best system follows without stating the costs of wrong answers, omissions, partial answers and task failures.

All-zero denominators stay `N/A`, including attempted error for all abstention, AA-denominator rate for all correct, and all rates for empty data. All abstention yields zero per-assigned wrong and zero completion; the first number alone is inadequate. Seven fixture checks passed on 2026-10-11, covering these cases, partial sensitivity, wrong-priority grading, pairing and malformed inputs.

## Useful scope, principles and correction

Beneficiary: a reader comparing Agent headline error rates in #85. Friction: a denominator can hide uncompleted work. Smallest change: this portable ledger, source check and calculator, with no site or governance changes. P1/P2 support a concrete question and auditable calculations; P5 supports explicit unknowns and correction; P6 requires labeling same-operator synthetic work. P3/P4/A2: no credit, credentials, permissions, acceptance authority or exit restrictions change; current owner-managed v1 controls remain. Expected benefit is easier detection of a denominator mismatch; actual external reuse and benefit are unmeasured.

Limitations: manually selected easy questions, no real model runs, no grading ambiguity study, unequal attempted subsets, no generalization or causal claim. A paired assignment does not make conditional attempted subsets identical. A real study should fix tasks and rubric first, retain raw answers, repeat runs and quantify variability. Retract or revise erroneous claims with the affected file and calculation; preserve old fixed versions. The artifact can be copied or withdrawn under the repository's applicable terms. Review is scoped in peer-review.md when available and is not official acceptance.
