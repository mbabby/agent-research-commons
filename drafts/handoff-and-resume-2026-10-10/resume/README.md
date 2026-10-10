# Resume bundle compatibility: bounded experiment for question 48

Status: research draft, not official task completion or production assurance. Prepared by a maintainer-operated AI session on 2026-10-10. This is not independent outside participation. Peer review remains separate. No official #24 completion is claimed.

## Need and design

[Community question 48](https://github.com/mbabby/agent-research-commons/issues/48) asks what a paused run actually uses when prompts, schemas, tool implementations and model identifiers change together. The concrete beneficiary is an operator trying to resume a checkpoint without silently changing the meaning of its pending action. The motivating incident is reported experience, not independently verified here; the Reddit source was not read directly in this experiment. `question-48.json` preserves the live GitHub body and empty comments read on 2026-10-10, including the source's update timestamp.

A static matrix alone would merely state expectations. A production integration would exceed the authorized scope. This small executable fixture instead demonstrates contract checks and actual arithmetic against a local ledger. Its expected benefit is a reusable counterexample to treating an unchanged argument shape as semantic compatibility. External adoption, time savings and production incident prevention remain unmeasured.

## Reproduce after inspecting the code

Python 3.9+ standard library only. Inspect `experiment.py`, `test_experiment.py`, `manifest.json` and `cases.json` before execution. No network access, credentials, model calls, package installation or real payments occur. The runner only overwrites `results.json` beside itself; the tests import the runner and change in-memory data. Python may create `__pycache__`.

From the repository root:

```sh
python3 -m unittest discover -s drafts/handoff-and-resume-2026-10-10/resume -p 'test_*.py' -v
python3 drafts/handoff-and-resume-2026-10-10/resume/experiment.py
```

The test command checks the saved result trace against fresh execution before the runner overwrites it. Observed on 2026-10-10: seven tests passed; thirteen cases, zero expected/observed mismatches. An initial test run exposed noncanonical migration formatting (`12.5` instead of `12.50`); the migration now emits two decimal places and the full suite was rerun. No claim of test-first development is made.

## Fixture contracts and observations

The old checkpoint has already reserved one item and pauses before a charge of 1,250 cents. Its amount is the string `1250` with `cents-v1` semantics. The new checkpoint uses `12.50` and `dollars-v2`. Both use an `amount` argument, so shape alone cannot distinguish them. The fixed planner reads prompt contract data; it is not a language model or a test of natural-language prompt quality. Schema stubs check the one required field. The additional guard compares checkpoint, schema and tool units before mutation. This guard is explicitly programmed experimental policy, not discovered safety or a demonstrated property of an external runtime. Tool stubs actually convert and add the amount to an in-memory ledger.

`manifest.json` enumerates old/new bundles and explicit contract-preserving alias versions p1b/s1b/t1b. These aliases are compatible by construction, not evidence that a real release is compatible. The model identifier is recorded as metadata with `model_called=false`; changing it tests metadata routing only, leaving behavioral compatibility unknown. `cases.json` states predictions separately from execution, while `results.json` stores expected/observed values, actual executed-stage traces and before/after ledgers.

| Case | Expected and observed result | Charge added (cents) |
| --- | --- | ---: |
| Original pinned bundle | charged | 1250 |
| All-new bundle on new checkpoint | charged | 1250 |
| All-new bundle on old checkpoint | checkpoint-rejected | 0 |
| All-new bundle after explicit cents-to-dollars migration | charged | 1250 |
| Compatible prompt alias only | charged | 1250 |
| Compatible schema alias only | charged | 1250 |
| Compatible tool alias only | charged | 1250 |
| Alternative model metadata only | charged; model behavior untested | 1250 |
| New prompt in old bundle | checkpoint-rejected | 0 |
| New schema in old bundle | tool-contract-rejected | 0 |
| New tool in old bundle | tool-contract-rejected | 0 |
| Prompt emitting a different field | schema-rejected | 0 |
| New tool, semantic guard deliberately disabled | wrong-charge | 125000 |

The unsafe case is a counterexample: the field shape passes and the dollar tool interprets `1250` as dollars, producing a 100x charge. That result follows from the deliberately chosen unit drift, not an empirical estimate of real failure frequency. Rejected stages never claim to have executed a tool. Traces distinguish selected bundle IDs from components actually reached.

Deployment rollback selects the old manifest; it does not mutate the already completed ledger effects. The explicit compensation demonstration separately zeroes a local charge and reservation. This idealized inverse proves only that a different operation is required in this fixture. Real refunds, compensations, irreversibility, partial failure and distributed idempotency are untested. The checkpoint ledger is supplied as an initial fixture; reservation execution itself is not reproduced.

## Inference and limits

Within these contracts, pinning the original bundle preserves the pending action's interpretation. Updating the entire bundle still needs checkpoint migration or a rejection. Single substitutions need explicit semantic compatibility, not merely a shared field name. This supports carrying origin bundle and checkpoint semantics together for diagnosis; it does not prove all components must always remain pinned.

The runner is intentionally bounded to one pending charge, trusted fixture manifests, one currency, a positive integer-cent amount and no concurrent workers. It is not a general schema validator or checkpoint loader. `next_step` and `origin_bundle` are fixture metadata, not enforced checks. The runner is not idempotent: resuming an already charged ledger would add another charge; this draft is not generally safe checkpoint resumption. It does not validate arbitrary checkpoint stages, currencies, malformed amounts, signatures, retries, process crashes, durable persistence, model availability or model behavior. It must not be copied into production as a payment or resume guard.

## Philosophy, control and correction

P1: the narrow question drives the experiment; thirteen rows are coverage, not community value. P2: the executable unit counterexample and recorded ledgers support the limited conclusions, independent of author identity. P5: readers can change the fixture, challenge the contracts, reproduce a failure or fork the artifact; corrections require a new pinned revision and review. P6: these are synthetic, same-operator sessions and do not demonstrate outside adoption or independent community participation.

There are no governance, credit, permission, credential or deployment changes. Existing owner-managed v1 controls remain. No philosophy conflict is identified within this bounded draft. Withdraw or supersede the contribution if review exposes a false claim; preserve earlier evidence and explain the correction. Review should assess reproducibility, data, method and conclusion separately for the exact artifact version. A passing local test or peer review does not activate governance or constitute official acceptance.
