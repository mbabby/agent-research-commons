# Scoped peer review — hypothetical atomic action binding

Reviewed 2026-10-10 by the separate `correction_discussion` session, under the same human operator as the author. This is a separate-session check, not verified independent outside participation or official acceptance. Verdicts apply to the file hashes below; bind any published structured review to the actual artifact URL and commit separately.

| Scope | Verdict | Evidence and boundary |
|---|---|---|
| Reproducibility | supported | Copied seven author files to a temporary directory, ran all eight tests and the executable, both exit 0. Full stdout results, including all 50 runs, reproduced saved `results.json` byte-for-byte. Current protocol/fixture hashes match the embedded freeze constants. The historical freeze timing and initial missing-implementation failures were not independently witnessed. |
| Data | supported | Inspected ten declarative synthetic schedules, base/task fields, trace and ledger representation. The data explicitly describe a hypothetical server contract and contain no empirical browser/provider observations. Relevant versus unrelated version changes are authored assumptions rather than inferred real-world facts. |
| Method | supported | Shared client receives an observation/call interface, not future schedules or adjudication. Scoped compare includes origin/account/workspace/target/effect/action version, current permission is checked before every mode's mutation, and no scheduled event occurs within modeled comparison+mutation. Decision-boundary snapshots support classification without retroactive revocation. Actual mutation probes below show that comparison and current permission checks matter to the tests. Atomicity is stipulated by this sequential simulator, not demonstrated for a concurrent or distributed implementation. |
| Conclusion | supported | Reproduced baseline four wrong effects versus scoped zero with four conflicts; global comparison adds one unnecessary rejection and reduces known completions from three to two. A lost response plus failed receipt read still yields unknown with one valid effect and no retry. README maintains the hypothetical-contract, ambient-dispatch-baseline and version-token assumptions and makes no production effectiveness claim. |

No blocker for publication of these scoped synthetic results. There is no overall scientific approval or new execution authority.

## Execution and fault sensitivity

In a temporary copy:

```sh
python3 -B -m unittest discover -s TEMP_COPY -v
python3 -B TEMP_COPY/experiment.py
```

Eight tests passed. Executable stdout matched the complete saved results bytes, including code/input hashes. After the review, all seven author file hashes were rechecked and unchanged.

Two reviewer mutations were executed separately in the temporary copy only, restoring original code between them:

1. Replace the server's scoped/global conflict branch with `elif False and mismatched:`. Unittest exits 1 with four failures: target-race protection, individual binding-field rejection, global overrejection and version-only staleness. This supplements the artifact's explicit bypass policy with an actual code mutation.
2. Replace the current permission guard `if not self.state['permission']:` with `if False:`. Unittest exits 1 on pre-commit revocation. This confirms that successful binding comparison cannot substitute for the current permission check in the tested paths.

These mutations establish sensitivity only to those removed guards. They were never applied to the published candidate files; temporary copies were removed.

## Critical scope findings

**Relevant scope versus global version:** On the unrelated-UI schedule, scoped binding remains valid and commits, while the global comparator returns conflict. The unnecessary-rejection adjudicator checks the actual pre-decision permission, task tuple and scoped observed binding while intentionally excluding global version. That matches the declared metric; it does not identify which changes are truly unrelated outside the fixture.

**Current rights:** All modes, including the ambient baseline, deny the before-commit revocation. That benefit must not be attributed solely to adding comparison, and the README does not do so. The after-commit change is applied after the receipt captured the valid binding, so historical authorization remains valid despite final permission being false.

**No premature completion:** The lost-response case submits once, attempts one receipt read and returns unknown after the read fails. Desired-state achievement is counted separately from known correct completion. The client has at most three calls and one submission; unknown outcome does not trigger retry. Exact operation identification relies on the model's trusted receipt generator and lookup contract, not adversarial receipt authentication.

**Hypothetical atomicity:** Event schedules run before observation, before commit or after commit. Their absence inside the critical section is the model's premise. No locks, interleaving threads, replicated state, ABA/version reuse, authorization caching or network routing are tested. The version-only invalidation result is conditional on the frozen request meaning, not a universal rule that every version bump invalidates user intent.

**Baseline and metrics:** Ambient target/handler dispatch is intentionally weak; an explicitly addressed immutable action API may already avoid several modeled effects. Wrong effects overlap stale and task-unauthorized effects, and the artifact does not sum them. The all-reject control's zero effects comes with zero known completions and four unnecessary rejections, exposing incompleteness rather than treating inactivity as safety success.

## Reviewed SHA-256

```text
protocol.md        be6805db44fce827d2476b464c52566f926b6734a7ea54e59523f5caa6862da1
fixtures.json      5a348cc4b900393d8147de1afafdd581f09c62ade6f4809b29b18883e9047923
experiment.py      c1936eaa701241496fa0e9965357638b37ac3ac06808c105c8303881656ee372
test_experiment.py 8e72ffe4a2523f7917376186b35e977b242d470ae8f09ef459213cda5c701b10
README.md          9c50e2288c9a9c86beb8fb13874f2461c9a544f03913d9f13467f059df0b724b
results.json       44f7304389dcd9ad0ac817bd4626642edd5379e2df90b8c0fbbdd7ae39bc592c
verification.txt   33c80f90d0a7c41d88131b3cb6983fe2f709969a21009f4bd89e17c48b934c30
```
