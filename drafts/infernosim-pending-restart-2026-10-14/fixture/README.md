# Pending operation restart fixture (research draft)

Python 3.9+ standard library. Run from any directory with an already compiled
InfernoSIM v4.2.0 binary (source commit
`f26b5522bbb20f2904d7534b879fa2896bdf1302`):

```sh
python3 fixture.py run --case safe-pending --binary /absolute/path/infernosim --output /tmp/pending-safe-fresh
```

Output must not exist. Repeat for all six cases below. No credentials are inherited
by the subprocess. All sockets bind loopback; the synthetic `barrier.test` URL is
sent directly to the simulator's loopback HTTP proxy without DNS resolution.
Binary SHA256 and exact command are saved, but the runner cannot itself prove a
binary was built from the declared source. Verify provenance separately.

## Why this fixture

An author identified a missing pending/durable-receipt boundary. This is a small
reproducible artifact for checking that boundary rather than modifying production
InfernoSIM or building another platform. Relevant principles: P1/P2 (specific
question and observable counterexample), P5 (uncertain outcomes remain explicit),
P6 (same-operator sessions, not independent outside adoption), A1–A3 (reviewable
scope, no authority or permission changes). Value to external users remains a
hypothesis until actual reuse. Withdraw/correct this draft if the controls fail;
no credentials, governance, credit, or production state are changed.

## Declared provider contract and execution

A single-threaded loopback fake provider commits each submission to SQLite before
returning HTTP 202 and an operation handle, business identity and idempotency key.
An idempotency key identifies one operation; different keys can create two effects
for the same business key. Each accepted operation eventually produces exactly one
effect under the bounded explicit drain. This is synthetic; no external payment,
model or provider is contacted.

The first client persists and fsyncs the received pending receipt, then makes a
synthetic checkpoint-barrier HTTP call through InfernoSIM. Actual
`--restart-after-call 1` machinery kills the process before delivering that
barrier's response and starts a fresh client with the retained checkpoint directory.
Recovery selection depends on checkpoint existence, not INFERNOSIM_ATTEMPT. The
fresh client reads the retained operation handle and queries the same provider.
The provider lives in the fixture controller and survives the child restart.

**The barrier is not a provider call.** InfernoSIM supplies a real process crash
and HTTP boundary; custom Python/SQLite supplies durable receipts, pending effects
and read faults. We do not claim InfernoSIM natively implements these provider
semantics or fault injection on the provider calls. The initial submit response
has already arrived; this does not test losing the handle or crashing during its
write. fsync here is process-recovery evidence, not disk/power-loss durability.

All cases except reconciliation and the mismatched-receipt control keep the original operation pending until the
InfernoSIM child runner has stopped. `before-drain.json` records that boundary;
then the still-live provider commits every queued effect. `after-drain.json` and
`provider.sqlite` expose both immediate state and delayed effects. Provider event
sequence numbers, not wall-clock sleeps, determine the schedule. There are no
unmodeled timer/background jobs after drain; this bound is a fixture assumption.

| Case | Recovery read | Expected decision | Operations/effects after drain |
| --- | --- | --- | --- |
| safe-pending | HTTP 200, original pending | unknown, no resubmit | 1 / 1 |
| unsafe-pending | HTTP 200, original pending | new-key replacement submitted | 2 / 2 (negative safety control) |
| safe-read-failed | HTTP 503 while original pending | unknown, no resubmit | 1 / 1 |
| safe-ambiguous-absence | HTTP 404 due to declared visibility lag, original exists | unknown, no resubmit | 1 / 1 |
| safe-reconcile | pending read transaction then completed read | completed only after matching handle/business/idempotency receipt | 1 / 1 |
| safe-mismatched-receipt | pending then deliberately wrong completed handle | unknown, no resubmit | 1 / 1 |

In safe-reconcile and safe-mismatched-receipt the provider commits after recording the first pending read,
before replying to that read; the returned pending snapshot may therefore already
be stale at delivery. Other cases remain pending throughout client recovery.
A 404 is explicitly non-authoritative in this contract, not a universal rule about
404 semantics. Unknown is not cancellation: safe clients that stop still have one
later provider effect. Unsafe replacement uses a **new** key; same-key replay is
not tested. No general exactly-once guarantee, real-agent behavior, real provider
cancellation, checkpoint corruption, failed simulator checker hook, or physical
crash durability is established.

## Evidence and interpretation

`first-client.json` and `decision.json` record distinct process IDs and retained
handle. `checkpoint-copy.json` captures the fsynced receipt before crash; simulator
reports must say process.restarted=true. The SQLite tables and ordered events
are the provider oracle; the external checker must verify identity, event order,
decision correctness, stopped-client boundary, and the post-drain effect counts.
InfernoSIM's raw pass only checks the recorded synthetic exchange and crash
boundary. It can pass the deliberately unsafe case; that is **not** a duplicate
safety verdict. A subprocess failure is retained with logs and nonzero exit;
never count it as evidence of safety. These controls are designed same-operator
comparisons, not independent external participation or adoption.

The mismatched-receipt case deliberately mutates a provider response to test the client identity guard; it is not an InfernoSIM product bug. A no-restart comparison is not included; the five non-mutation cases all exercise the same actual restart boundary.
