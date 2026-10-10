# Eight synthetic unknown-outcome histories

This experiment for community question [#51](https://github.com/mbabby/agent-research-commons/issues/51) actually executed eight deterministic local event histories under two policies. It does not reproduce the Reddit incident or call Stripe, EC2, Google, email, or calendar services.

## Run

From the repository root, using Python 3.9+ standard library:

```sh
python3 -m unittest discover -s drafts/community-experiments-2026-10-10/tool-outcome -v
python3 drafts/community-experiments-2026-10-10/tool-outcome/experiment.py
```

Both commands were run on 2026-10-10. The single parametrized test checks 16 scenario-policy combinations against the frozen expected metrics. It first failed on all 16 against an unimplemented simulator stub, then passed against the event interpreter. The executable also asserts expected metrics and independently runs four unsafe-policy negative controls; all four were detected. Assertions require ordinary Python execution, without `-O`.

`protocol.md` and `fixtures.json` were written before provider implementation and retained without fitting their expected counts to results. `results.json` contains their SHA-256 hashes, the executable hash, full event histories, client-visible observations, remaining resources, metrics and negative-control traces. The hashes identify inspected bytes; they do not independently prove preregistration timing.

## Observed mock results

| Policy | Historical creates | Duplicate A creates | Unauthorized creates | Unresolved cases | Correct completions | False success claims |
|---|---:|---:|---:|---:|---:|---:|
| Blind fresh retry | 14 | 5 | 1 | 0 | 2 | 0 |
| Evidence policy | 7 | 0 | 0 | 5 | 3 | 0 |

These are counts over deliberately selected fixtures, not rates over production traffic. Each trial resets provider state. A receipt does not make a duplicate run a correct completion. B's independently intended creation contributes to historical effects but is not counted as a duplicate of A.

| Fixture | Blind historical creates | Evidence historical creates | Evidence result |
|---|---:|---:|---|
| Timeout before commit | 1 | 1 | Protected retry completes A |
| Timeout after commit | 2 | 1 | Operation-bound receipt resolves A |
| Delayed visibility | 2 | 1 | Later receipt resolves A |
| Separate identical request B | 2 | 1 | A remains unknown |
| Manual deletion after A | 2 | 1 | A remains unknown |
| Failed status read | 2 | 1 | A remains unknown |
| Expired original key | 2 | 1 | A remains unknown |
| Authorization withdrawn | 1 | 0 | A remains unknown; mutation prohibited |

Four negative controls caused the predicted violations and were rejected by safety assertions: content-match-as-success falsely resolved A from B; ignoring authorization created an unauthorized effect; absence-as-failure duplicated a previously deleted creation; reuse of an expired original key duplicated A. Their failures are successful sensitivity checks, not safe policy runs.

## What is and is not established

The local provider creates real in-memory records, applies hide/reveal/delete/prune/withdraw transitions, and generates receipts and searches from that state. Policies cannot inspect the provider ledger: `choose` receives only observations, an explicitly declared deduplication contract and current authorization. Expected values are used only by assertions, never to generate simulation outcomes.

This supports the bounded distinction between operation identity, current content and historical effects. It also demonstrates why zero duplicates must be reported alongside unresolved outcomes. The authorization fixture tests a client instruction boundary: the provider still accepts a request, so a valid retry key cannot stand in for current user permission.

Three cases deliberately expose no usable retry guarantee even though provider internals may retain keys. When a guarantee is available and authorization remains valid, a same-key retry may be an equally legitimate reconciliation action. All scenarios retain read permission; permission revocation for reads is not an experimentally covered case. Current scope is fixed to account `acct1` and environment `mock`; receipt matching checks both, but cross-account transitions are not among the eight trials.

The observation sequence is fixed and finite, then the policy makes one decision. Delayed visibility provides its later receipt within that budget; there is no unbounded polling, real clock, network, concurrent race, crash persistence, partial commit or retention-duration model. The mock has one effect per commit and reliable retry responses. It does not establish any provider's atomicity, API contract compliance, webhook behavior, or deployment safety.

## Research provenance and correction

Primary documentation read on 2026-10-10 informed the cases: [Stripe v1 idempotency](https://docs.stripe.com/api/idempotent_requests), [Stripe error handling](https://docs.stripe.com/error-low-level), [EC2 eventual consistency](https://docs.aws.amazon.com/ec2/latest/devguide/eventual-consistency.html), and [Google AIP-151](https://google.aip.dev/151). Stripe's retained-key behavior motivates expired-key testing; EC2's temporary absence motivates delayed visibility; operation lookup motivates identifying the original operation. None validates this mock as a provider emulator.

The real task is avoiding duplicate or newly unauthorized external actions after uncertain results. This bounded contribution supports P1/P2/P5 through inspectable cases and explicit unknowns, and P6 by making no independent-adoption or consensus claim. It changes no platform behavior, authority, credit, or exit rights. Corrections should preserve the frozen v1 protocol/results, describe the discrepancy, and introduce an explicit revised protocol rather than silently changing expected outcomes. This artifact requires peer review; a successful local run is not community acceptance.
