# Cross-review: atomic action binding mock

Reviewer logical session: `tool_outcome_research`, 2026-10-10. Separate session from the author within the same human-operated task; no independent external participation claim. I inspected protocol, fixtures, code, tests, README and results, then ran the commands below. I changed only this review file.

```sh
python3 -B -m unittest discover -s drafts/community-followup-2026-10-10/atomic-action-binding -v
python3 -B drafts/community-followup-2026-10-10/atomic-action-binding/experiment.py --output /tmp/atomic-action-binding-cross-review.json
```

Python 3.9.6: eight tests passed. All 50 generated records matched saved `results.json` **byte-for-byte**. Frozen input hashes match. I separately checked after-commit authority changes and lost-response ledger/decision metrics.

| Scope | Verdict | Evidence and limits |
|---|---|---|
| Reproducibility | supported | Full suite passes; raw output reproduces exactly. Hashes below identify inspected bytes, not an independently witnessed freeze chronology. |
| Data | supported | Ten explicit synthetic event schedules, five execution modes, reset document states and full request/commit traces. No empirical population or real-provider evidence. |
| Method | supported | Shared client sees current observation only; hidden scheduled changes apply in world code. Scoped comparison checks six binding fields plus current permission before mutation. Individual-field tests hold version constant, preventing version mismatch from masking a missing field check. Baseline and bypass intentionally share ambient dispatch. |
| Conclusion | supported | Reproduced baseline four wrong effects versus scoped zero/four conflicts; both have three known completions and one unknown. Global binding adds one unnecessary rejection. README accurately frames atomicity as an assumed server capability, not a measured browser or transaction guarantee. |

The most useful cross-question result is the separation of **commit validity** from **outcome knowledge**. In the lost-response case, scoped mode records one authorized effect, one submission, desired state achieved, unknown client outcome and zero known completions. Atomic comparison does not recover a lost receipt or authorize retry. In the after-commit case, the historical binding/permission snapshot remains valid despite later revocation: one known completion and no wrong effect. Current authority is not retroactively substituted for commit-time authority.

The revocation-before-commit case is denied in every mode, so its benefit correctly belongs to the common current-permission check, not added binding comparison. Global-only change is scoped-valid at the decision boundary; the extra global conflict is therefore unnecessary under the frozen task definition. Version-only staleness is wrong by that conditional definition even when the visible document state is achieved; metrics and prose disclose this convention rather than treating it as universally required.

Critical limits: the simulator prevents interleaving by construction inside compare/permission/mutation; it does not establish a real linearizable implementation. Correct version updates, trusted account/permission context and receipt integrity are assumed. The timeout response supplies `operation_id=op1`, so receipt correlation remains available; a real transport failure that loses the identifier is outside the fixture. The baseline uses an ambient current handler; immutable target/operation APIs may already avoid part of its failure mode. All are scope limits, not evidence against these conditional results. A future study should test transaction-boundary failures/ABA or unavailable operation identity before making a stronger implementation claim.

No publication blocker found for the stated model. This review supports the bounded executable illustration, not production safety, external usefulness or official acceptance.

## Exact reviewed SHA-256

| File | SHA-256 |
|---|---|
| protocol.md | `be6805db44fce827d2476b464c52566f926b6734a7ea54e59523f5caa6862da1` |
| fixtures.json | `5a348cc4b900393d8147de1afafdd581f09c62ade6f4809b29b18883e9047923` |
| experiment.py | `c1936eaa701241496fa0e9965357638b37ac3ac06808c105c8303881656ee372` |
| test_experiment.py | `8e72ffe4a2523f7917376186b35e977b242d470ae8f09ef459213cda5c701b10` |
| results.json | `44f7304389dcd9ad0ac817bd4626642edd5379e2df90b8c0fbbdd7ae39bc592c` |
| README.md | `9c50e2288c9a9c86beb8fb13874f2461c9a544f03913d9f13467f059df0b724b` |

Later source or conclusion changes require renewed review of the affected scope.
