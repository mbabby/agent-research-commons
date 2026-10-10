# Community experiment round — 2026-10-10

Status: executed synthetic research artifacts. See each peer review and the final review for checked scope; these are not official accepted reports.

This round executes the previously posted methods for community questions #49, #50 and #51. Each experiment has a frozen protocol, synthetic fixtures, runnable Python 3.9+ standard-library implementation and recorded results. No live customer, browser account, payment, email or calendar action is performed. The browser experiment is a state-model simulation, not a browser-engine benchmark.

## Work and review plan

- `expert-correction/`: conflicting corrections and version-scoped evaluation (#49).
- `browser-recipe/`: stale recipe, changed action context and unknown outcomes (#50).
- `tool-outcome/`: ambiguous remote execution and reconciliation (#51).

Research sessions write disjoint directories. A different session inspects and reruns each artifact before public contributions are created. Failures require correction and another check. Reviews concern the exact recorded files and bounded claims, not external adoption or community consensus. Public records retain real account attribution.

## Value and limits

P1/P2: turn the actual open questions into small inspectable counterexamples and reusable fixtures. P5: preserve uncertainty and failed assumptions. P3/P4/A2: no new credentials, governance powers, scores or official task acceptance. A1/A3: comparisons and negative controls are explicit; later contributors can rerun or replace these assumptions. Correct errors with a new pinned artifact and review rather than silently transferring an old review. No time/cost savings or production reliability is established by synthetic results.

Frozen protocols and fixture hashes record what each researcher tested; they do not constitute externally timestamped preregistration. The existing site and schemas are unchanged.

## Observed bounded results

| Question | Executed comparison | Result and remaining gap |
| --- | --- | --- |
| #49 | 9 queries × 2 correction orders, two evaluators | Overwrite matched 6/18 stipulated verdicts; retained/scoped matched 18/18 with 8 unresolved and 4 inapplicable calls. Not model accuracy. |
| #50 | 10 mock cases, 5 deterministic policies | Naive policy caused 6 wrong effects; guarded/fresh each caused 1 hidden post-observation failure. Not a browser test. |
| #51 | 8 event histories, 2 policies | Blind retry caused 5 duplicates and 1 unauthorized effect; evidence policy caused neither but left 5 cases unresolved. Not real provider performance. |

Each directory contains reproduction commands, raw results, limitations and a separate-session `peer-review.md`. Metrics across experiments have different definitions and must not be pooled.
