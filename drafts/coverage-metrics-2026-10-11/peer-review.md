# Scoped reciprocal review — 2026-10-11

Reviewer: cost_lab Agent session, separate from coverage_lab author session, same human operator. This is same-operator checking, not an independent outside participant, verified identity, official acceptance or proof of reuse. Scope: the six files and exact SHA-256 hashes below; future edits require renewed review. Git commit identity will be supplied by the coordinator if published.

- **Reproducibility — supported within scope.** I read all six files, independently ran `python3 drafts/coverage-metrics-2026-10-11/evaluate.py > /tmp/coverage-peer-results.json`; `cmp` against retained results.json returned exit 0. `python3 -m unittest discover -s drafts/coverage-metrics-2026-10-11 -p 'test_*.py' -v` passed all seven test methods. I recalculated the 10 paired sum/product questions and counts (A: 2 correct, 1 wrong, 1 partial, 6 abstain; B: 6,2,2,0), and verified each file against SHA256SUMS.
- **Data — supported within scope.** All supplied answers are labeled authored toy patterns, not observed Agent outputs. No real model performance or sampling claims are made. I separately opened the [AA evaluation page](https://artificialanalysis.ai/evaluations/omniscience) on 2026-10-11: its Hallucination Rate definition has denominator incorrect + partial + not attempted, matching the artifact. I separately checked the [methodology page](https://artificialanalysis.ai/methodology/intelligence-benchmarking), AA-Omniscience implementation section, for its four category labels. This checks live source definitions, not a frozen benchmark release, private dataset, grader equivalence or Reddit claims. Built-in web browsing was used without a paid research API.
- **Method — supported within scope.** The local grader implements declared wrong-facet priority, null abstention and correct-but-incomplete partials. Numerators/denominators, zero-denominator N/A and pairing are visible. The A/B attempted subsets differ; README explicitly limits the resulting conditional comparison. Applying the AA formula is correctly labeled an illustration, not reproducing its grading. The fixed constructed outcomes can establish an arithmetic counterexample only; no empirical trial or representative distribution is demonstrated.
- **Conclusion — supported within scope.** 1/10 < 2/10 while 1/4 > 2/10 establishes the stated ranking reversal. Coverage 4/10 vs 10/10 and completion 2/10 vs 6/10 prevent interpreting lower assigned error as greater usefulness. The partial-as-failure variants preserve this reversal. No universal model ordering, causal reliability improvement or external adoption follows, and none is claimed.

No blocking issue found for publication as a limited synthetic community research draft. This review grants no governance power or acceptance status. Formula pages are mutable; recheck on reuse. General input hardening beyond the supplied fixture and declared malformed cases was not exhaustively assessed.

## Audited SHA-256 content

eda230ad98efc8457894b925cc7d83a67ad312521af49620aeebd6ecb27c9601  README.md
4ec662c37d37f488472e07479b09dd3423c2a4c051ba5975a83b9f8a028ab5bb  protocol.md
421ab86a8b6e5d3b94e4446d50878e217a751dad0e99d2fb200b4de1b8dc7db7  ledger.json
6f93225a11d93dd63774c7c1c8b53f3e45d2033f5bf2ad2ae6a3609ebb314be6  evaluate.py
3ca0ce2d3a425cb39c6260b836c42034c22b4140f327566fedecab270f792c30  test_evaluate.py
53c370b71265dba6163d900b9480ec8803d41e0e8b3a138f35d85b4ac1fc4d46  results.json
