# Method and separately initialized rerun: final review

Reviewed 2026-10-14 by a separate Codex method/checker session under the same
maintainer operator. Not an independent outside operator or formal acceptance.

## Exact reviewed artifacts

- `fixture/fixture.py`: `01eee5d28400bd388492ef86505ea526923e100ff660ef199795ad2886136aa7`
- `fixture/README.md`: `92089818e8a94ded4b556af36630c99ccc349396fb9b010f78793a8837282df8`
- `checker/check_evidence.py`: `08162672d3392511fdf9dced3c19ce8ee9d9cad2dd1eda8ef9346bd1ebc15e32`
- `README.md`: `4eea26ec9df5d50d40fb40454601eb5c1fa4d36c00e2e0b8a30c2403b8d8a415`
- `checker/summary.json`: `0bcdc58e32fb99ecaba3228fb5bd0fe79831f45cee96e04881a24886506e2641`
- `checker/runner-crosscheck.json`: `9a0a154b5bd7035d1a66d325fcec36f402e2280815bcf8b636021e3055f9f8d7`

Upstream source HEAD was verified clean at
`f26b5522bbb20f2904d7534b879fa2896bdf1302`. Shared compiled binary SHA-256:
`195b9b833ea7855dbba602fad03ae748fecbbedcfe14b588645b4ee5b02e57e7`.
The previous packet records its source build; this session did not rebuild it.

## Reproducibility: supported within stated host and boundary

I ran all six final fixture cases in fresh `checker/runs/CASE` directories with
new provider databases and clients. All subprocess exits were 0. All raw
InfernoSIM reports had one observed/expected `checkpoint_barrier`, restarted=true,
process exit 0, no timeout, and a passing recorded-only assertion. All client
PID pairs differed. The retained original was op-1 in each case. Initial sandbox
loopback bind denial was preserved separately and excluded.

I also ran the standalone checker against the primary `runner/campaign` evidence.
All six checks passed in both campaigns, and semantic summaries match after
excluding PIDs. These are same-host deterministic reruns using a shared binary,
not statistical replications or independent external witnesses.

## Data: supported by correlated SQL/events and captured decisions

The checker imports no fixture code and opens provider SQLite read-only. It
correlates checkpoint handle/business/idempotency identity with the original row,
client first/terminal observations with actual recorded provider responses,
original pending read with retained handle, decisions with case expectations,
submissions with operation count, and effects with completed operations.

In each campaign, the unsafe replacement has two distinct idempotency keys and
two effects for payment-1; the other five cases each have one. Pending, 503,
ambiguous 404 and mismatched completed receipt remain unknown without a new
submit. The matching completed receipt permits completed. Provider effects are
committed after client-runner stop for the four pending-through-exit cases. All
operations are completed after drain with no queued original left uncounted.
`checks: pass` for unsafe means its expected duplicate was observed, not safe.

## Method: adequate for the bounded synthetic question

Actual InfernoSIM supplies process death and fresh restart at a recorded synthetic
HTTP barrier. The direct loopback provider and durable state are custom Python,
not an InfernoSIM provider-fault implementation. Recovery uses durable checkpoint
existence/content rather than the attempt number. The original submit response
has arrived before the chosen crash, so retained identity is a precondition.

The earlier method review identified a missing completed-receipt identity guard;
the final source checks handle, business key and idempotency key, with a wrong
handle control. Builder cross-review identified missing artifact bindings in the
standalone checker; those bindings were added before this final check. This was
concrete cross-session correction, not an outside endorsement.

For reconciliation, pending is a snapshot captured before commit; commit happens
before pending response delivery, and the second read returns terminal state.
This ordering is accurately stated in the root README. The explicit drain is a
logical scheduler selected for the counterexample, not a timing-frequency study.

## Conclusion: supported only as written in the reviewed README

The README accurately reports preserved identity across a real client restart,
a delayed duplicate under deliberate new-key replacement, unknown outcomes for
failed/ambiguous/mismatched observations, and later completion only with a matching
receipt under the fake contract. It correctly warns that all raw InfernoSIM runs
pass even though one policy duplicates effects. It does not infer product failure,
provider guarantees, independent adoption or closure of #51.

Unmeasured: no-restart baseline, initial-response loss, missing/torn checkpoint,
power loss, provider restart, multiple clients, key expiry, same-key replay,
authorization withdrawal/cancellation, or receipt authentication. Invalid simulator
state-check hooks were inspected in source but not exercised by this fixture.
The provider/logs/DB share implementation and the oracle's completeness depends on
the declared bounded drain. No broader safety or liveness claim follows.

No blocking concerns remain for publishing this precisely scoped draft contribution.
A changed fixture, checker, result set or conclusion requires renewed scoped review.
