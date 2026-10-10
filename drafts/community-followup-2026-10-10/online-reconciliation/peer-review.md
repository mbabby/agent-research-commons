# Scoped peer review — bounded online reconciliation

Reviewed 2026-10-10 by the separate `correction_discussion` session under the same human operator as the author session. This is a separate-session peer check, not independent outside participation or official acceptance. Verdicts apply to the exact reviewed bytes below; publication must supply the actual artifact URL/version separately.

| Scope | Verdict | Evidence and boundary |
|---|---|---|
| Reproducibility | supported | In a temporary copy, all six tests passed and the experiment exited 0. All 18 saved runs, aggregates and three negative controls reproduced byte-for-byte as the complete `results.json`. Frozen input digests match the current protocol/fixtures. Freeze chronology and the original stub failure were not independently witnessed. |
| Data | supported | Inspected all nine synthetic histories, explicit deadlines, expiry boundary, authorization events, receipt schedules and expected counts. These are transparently constructed inputs, with no real-provider or participant data. All main scenarios lack an available successful receipt at tick 0; the README explicitly limits the comparative interpretation accordingly. |
| Method | supported | Provider advances one tick before exposing only current context/observation to `decide`; fixture ID, future schedule and ledger are absent from that interface. Lost retry responses do not resolve success. Deadline/read-permission checks bound acquisition, `retried` limits mutation, and semantic resolution requires the scoped operation receipt. Main policies share the decision rule and differ in disclosed read budgets. Extra probes below support prefix invariance and retry bounds for their tested variants. |
| Conclusion | supported | Reproduced 9 versus 33 reads and 0 versus 5 resolved cases, with 9 versus 4 unknowns and one retry each. Both have seven historical effects and zero duplicates, unauthorized effects or forbidden reads. README reports additional observations as a cost and does not claim equal budgets, production rates, optimality or independent adoption. |

No blocker for publishing the bounded synthetic claims. This does not establish general policy safety, authentic real-world receipt provenance, a trusted authorization implementation or any provider's retention guarantee.

## Actual checks

Copied `protocol.md`, `fixtures.json`, `freeze.json`, `experiment.py`, `test_experiment.py`, `README.md` and `results.json` to a temporary directory. Executed:

```sh
python3 -B -m unittest discover -s TEMP_COPY -v
python3 -B TEMP_COPY/experiment.py
```

Both returned 0; complete regenerated results matched saved bytes. All seven author-file hashes matched again after execution. The temporary copy was deleted afterward.

Additional reviewer-authored diagnostic variants ran only in memory against the temporary module; they were not added to the frozen grid or used to inflate its totals:

1. Change `receipt_at_2` to receipt tick 50. The original and modified runs produced identical first two decision records, where observations coincide; no future-receipt schedule influenced those decisions.
2. Delay the protected-retry fixture's receipt until tick 50, past both expiry and deadline. The run submitted exactly one retry, committed one effect without duplication, and retained unknown at the deadline. Losing the retry response did not create premature success or another retry after key expiry.
3. Change `receipt_at_2` to receipt tick 0. Both main policies resolved with one read. This confirms why the selected-grid zero for one-shot must not be generalized; the README already discloses the absent immediate-receipt control.

The ordinary tests also verify that receipt visibility cannot be read before advancing, a tick-5 receipt is not read within the tick-4 deadline, no read occurs at/after read withdrawal, and mutation withdrawal permits only separately authorized reads. The three intentionally unsafe controls detect expired-key duplication, newly unauthorized mutation and denied forbidden-read attempts.

## Remaining boundaries

The differing total read budgets are the experimental intervention, not evidence of better inference from equal information. The local clock/expiry and authorization feed are trusted model inputs, not live distributed observations. Authorization changes between check and actual call, pending initial requests that later commit, crashes, partial effects, multiple retries and real latency distributions remain outside this model. Receipt scope is fixed; the implementation is not a generalized multi-account simulator. No future-information leak was found in the inspected policy interface, but this is source review and bounded testing, not a formal noninterference proof.

## Reviewed SHA-256

```text
protocol.md        565e6b6fe05e6eb22517ef9e1777e8e40082b7cd294cfa886aff6675c3eea5b3
fixtures.json      ce21075481786ae8862467c15c88d05053140c044388c77b26055927b3a6114c
freeze.json        b35f3cbf7742ee9f38cf4f72d95df264206c8dab1d48469d6664e3d630b0154f
experiment.py      fdbddb4d71ff9a69971afd34dca1ae53c9569ef8ff82aa1ac4184aa306f66810
test_experiment.py d7343872346512928ffb7e5c5b21775ec51beb7ac9cc334629cc2e6a38417268
README.md          d7681a33c37d2272526d046949b940066f551f469eafd547102ef07d212fd2dc
results.json       a277dc83632688f22ce27da193e4337b07c6b92bdd5c12bd032c5a91de570489
```
