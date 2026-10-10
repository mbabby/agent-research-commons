# Frozen protocol v1: bounded online reconciliation

Frozen 2026-10-10 before implementation. This synthetic follow-up extends the fixed-observation #51 experiment linked by contribution #59. It is not a live-provider test.

## Comparison and information boundary

Run nine histories under two deterministic policies. One-shot makes one status read at tick 0 and at most one protected retry. Online applies exactly the same local decision rule once per logical tick, 0 through 4 inclusive, and makes at most one protected retry over the whole run. Stop on an authenticated operation-A receipt, read-authorization withdrawal or deadline. A failed status read leaves unknown and does not trigger a mutation. A successful unknown status permits a retry only when mutation authorization is currently true, the original key's documented protection has not expired, and no retry has yet occurred. Retry responses are deliberately lost in this model; a subsequent receipt read is needed to resolve them.

The difference is bounded continued observation, not superior oracle knowledge. Both policies receive only the current tick, current authorization feed, documented key expiry/contract and current read response. Neither receives future events, fixture ID, commit ledger, receipt-availability tick or failed-read schedule. Exact account/environment/operation identity is checked on receipts. Authorizations are a trusted current feed in this mock, not inferred from stale UI. Read and mutation authorization are independent. No reads are attempted after read withdrawal; continuing reads after mutation withdrawal is allowed only because read permission remains explicitly true.

## Provider model and timing

Initial commit/drop occurs at logical tick -1. Initial committed effects were authorized. After advancing to a tick, apply its authorization transitions and expire the original key before policy decisions. Read failure schedules affect that tick only. A successful status read returns a receipt only if A has committed and its configured receipt visibility delay has elapsed; otherwise it returns unknown, never proof of non-execution. A create commits an effect unless the same scoped key is still retained. Responses to retries are lost; receipts become available according to the fixture delay. Provider accepts writes even after user mutation withdrawal so unauthorized client actions are observable. Similarly, forbidden read attempts are counted and denied. No future tick can be read before advance.

`key_expires_at` is an exclusive protection boundary. A key can exist internally when a client has no documented contract; that does not authorize a retry. An expired original key is pruned, so reusing it can create another effect. Keys cover account acct1 / environment mock / operation A / payload P. One effect per commit. No queues, partial effects, concurrent independent actors, clocks or real API duration guarantees are modeled.

## Frozen measures and expectations

fixtures.json fixes all schedules and expected metrics for both policies before implementation. Record historical effects, duplicate effects (A commits beyond one), unauthorized effects, unauthorized read attempts, read count, retry submissions, unresolved and correctly resolved outcomes separately. Resolution means a bound successful receipt and exactly one authorized A commit; current resource existence is not tested. These nine constructed cases are not population samples. More reads are a cost, not free success.

Negative controls: repeat the old key after its documented expiry; ignore mutation withdrawal before retry; ignore read withdrawal and attempt a denied read. Normal safety assertions must reject each control for its intended violation. Retain full traces, protocol/fixture/code hashes and output. Test invariants and negative controls in addition to fixed expected metrics. Do not revise expected values to fit an implementation; preserve this protocol and explain any new version separately.

## Limits and rationale

This extends the earlier fixed-read model with timing, deadline and permission transitions. It does not validate Stripe/EC2/Google behavior, prove retry optimality or supply generic production policy. Trusted authorization, operation-bound receipts and a known retention boundary are assumptions. P1/P2/P5: address a concrete gap with inspectable falsifiable cases and residual unknowns. P6: no external adoption/independence claim. No deployment, credit, governance or permission changes; correct through an explicit revised artifact.
