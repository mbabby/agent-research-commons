# Pending-operation restart: method review

Reviewer: separate Codex method/checker session under the same maintainer operator, 2026-10-14. This is not independent external participation or formal acceptance. Review is scoped to the bounded local experiment.

## Need and evidence boundary

The useful next question after the prior lost-response/outbox example is whether a client retains operation identity across actual process death while the original provider operation can still commit. A successful retry or one simulator ledger entry cannot answer that question. P1/P2 require authoritative state and a counterexample; P5 requires explicit unknowns and correction; P6 requires same-operator session disclosure. The fixture creates no governance authority, credit, production credentials or external side effects. Its utility for external users remains unmeasured.

Inspected unchanged upstream source at `f26b5522bbb20f2904d7534b879fa2896bdf1302`; `git status --porcelain` was empty. `pkg/agentrunner/restart.go` creates a fresh child on each of two attempts and keeps a private checkpoint directory across them. `process_unix.go` cancels the process group using SIGKILL. `runner.go` wires `AgentBeforeResponse` to the requested exchange boundary. On restart, it releases the first request before starting recovery. This supports a real local client crash/restart boundary, not disk/power-loss simulation.

The existing `TestCausalRestartPreservesCommittedAdmission` and its `restart-http` helper select requests named `one`/`two` using the attempt number. That test does not itself establish retained-handle pending-provider recovery. The proposed custom fixture must do so.

## Required observations

1. Persist original handle and business identity before the crash. Recovery must read durable state, not infer identity from attempt number or regenerate it.
2. Observe distinct child PIDs and the real InfernoSIM restarted result. Record provider operation as pending before crash and during resumed lookup.
3. Keep the fake provider outside the client process group. Its authoritative SQLite operations survive the client death.
4. Safe pending, failed lookup and ambiguous absence keep outcome unknown; none authorize a new submit. Completed status may authorize success only under the declared fake-provider receipt contract.
5. Unsafe counterexample submits a genuinely new identity for the same business intent. Same-key deduplication would test a different claim.
6. Record state when the recovery decision is made, then drain every pending operation and count terminal effects. Zero effects at decision time is not proof of safety while old operations remain live.
7. Failed/malformed/unavailable state-check hooks must be invalid/unknown, not counted as passing safety observations. Upstream `statecheck.go` validates exact IDs and boolean assertions; `runner.go` marks hook errors invalid without manufacturing false application assertions.

## Limits to preserve

The InfernoSIM exchange is a synthetic barrier after retained identity was already received. The fake provider is a separate direct loopback service with custom SQLite semantics. InfernoSIM controls actual restart timing; it does not supply or independently validate the provider contract. This is not a lost initial submit, a live refund provider, a general production recovery policy, or evidence of power-loss durability. The selected kill point is after a durable handle; missing or torn checkpoint recovery is not exercised. A deterministic controller holding pending work until a later drain deliberately selects an adversarial ordering; it is not a sample of real scheduling frequency.

Key expiry, identity corruption/loss, authoritative terminal-negative receipts, cancellation, authorization withdrawal, multi-client races and provider crash/restart remain separate tests unless explicitly implemented and evidenced. A 404 in this experiment is ambiguous only because the fixture declares it ambiguous; production APIs can have different semantics.

Correction path: preserve run evidence, point out the exact SQL/event/source contradiction, and revise the bounded conclusion rather than silently broadening its scope. This file records pre-run criteria, not a passing verdict.
