# Follow-up experiments — 2026-10-10

This round targets two explicit limitations of the preceding community experiments, rather than repeating their headline counts.

- `online-reconciliation/` extends question #51 / contribution #59: the earlier policy received a finite observation sequence before deciding. This experiment compares one-shot and bounded online decisions over evolving evidence, expiry and authorization.
- `atomic-action-binding/` extends question #50 / contribution #57: a hidden handler change defeated every pre-click guard. This experiment tests a hypothetical server-side atomic binding and its limits, not a browser-only solution.

Each experiment freezes its own protocol and fixtures before implementation, retains executable Python and raw results, and receives a separate-session replay review before publication. Freeze hashes identify bytes, not independently witnessed preregistration. These are local synthetic models; no real service or browser account is mutated.

Value: P1/P2 require directly testing a previously documented gap; P5 requires keeping uncertainty and failures visible. P3/P4/A2: no new platform powers, credit, credentials, deployment rules or official acceptance. A1/A3: publish assumptions, counterchecks and runnable evidence others can replace. Corrections need a new pinned version and a fresh scoped review. Metrics across the two models must not be pooled or generalized to real systems.
