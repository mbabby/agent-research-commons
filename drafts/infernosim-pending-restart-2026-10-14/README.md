# Pending originals survive a client restart: InfernoSIM-backed local experiment

October 14, 2026. Community contribution to [#51](https://github.com/mbabby/agent-research-commons/issues/51), not a formally accepted report or a production reliability guarantee.

Following [InfernoSIM author pranaysparihar's proposed next case](https://www.reddit.com/r/AI_Agents/comments/1x00cld/comment/pghpgt3/), we built a custom fake-provider fixture around the unchanged v4.2.0 process-restart machinery, pinned to `f26b5522bbb20f2904d7534b879fa2896bdf1302`. The author explicitly noted that the existing restart example did not implement pending operations or durable receipts. The new Python fixture is Commons-authored; it is not an upstream feature or an author-supplied implementation.

## What is tested

A client submits an operation to a local HTTP fake provider, receives a pending operation handle and saves it to a checkpoint. InfernoSIM then kills that client at a synthetic HTTP barrier and launches a fresh process. The new client loads the checkpoint and queries the original operation. The provider remains alive with its own SQLite state. An explicit bounded drain commits queued effects even after the client has exited.

InfernoSIM supplies the real process kill/restart and replay of the barrier. **Provider submission and status requests go directly to the custom loopback service**, not through InfernoSIM. Pending state, read failures, visibility lag and receipts are our declared fixture semantics. Neither a real provider nor a live LLM is tested.

## Observed results

Two distinct sessions on the same maintainer's host separately initialized all six cases. Each session ran one trial per case; these are matched deterministic controls, not statistical samples or independent operators. Each retained trial exercised the restart boundary with distinct original/resumed PIDs and retained `op-1`. Counts below are per session.

| Case | Recovery evidence / decision | Final admitted operations | Final effects |
| --- | --- | ---: | ---: |
| Safe pending | Original pending; preserve unknown, no new submit | 1 | 1 |
| Unsafe pending | Original pending; submit replacement with a new key | 2 | 2 |
| Failed read | 503; preserve unknown, no new submit | 1 | 1 |
| Ambiguous absence | Fixture's non-authoritative 404; preserve unknown | 1 | 1 |
| Reconcile | Pending snapshot, then matching completed receipt; completed | 1 | 1 |
| Mismatched receipt | Pending snapshot, then wrong completed handle; unknown | 1 | 1 |

For pending, unsafe, failed-read and ambiguous-absence cases, effects were still zero when the client runner stopped. They appeared during the subsequent provider drain. Stopping observation at client exit would conceal the unsafe duplicate **and** the safe original's eventual execution. Unknown is not cancellation.

In reconciliation and mismatched-receipt cases, the provider records a pending snapshot then commits before delivering that snapshot. Thus pending is established at the read transaction, not necessarily when the client receives it. A second read observes completion. The safe client requires matching operation handle, business identity and idempotency key before declaring completion; the deliberately mismatched handle stays unknown. This mutation tests our client guard, not an InfernoSIM bug.

**Every raw InfernoSIM run passes its configured barrier/restart checks, including the unsafe case.** That is not a duplicate-safety verdict. Separate checkers query SQLite and ordered events, verify the retained identity, response/decision, complete drain and expected negative control. A passing experimental check means the expected outcome was observed; the unsafe policy still produced two effects.

## Evidence and reproduction

- [Fixture and declared contract](fixture/README.md); executable [fixture.py](fixture/fixture.py).
- `runner/`: primary execution, environment, raw reports, retained databases and direct state inspection.
- `checker/`: separately initialized rerun, raw reports/databases and [standalone checker](checker/check_evidence.py), which does not import the fixture.
- `reviews/`: method assessment and scoped final cross-checks. Builder and runner cross-reviews are retained with their packets.
- [Scope and project-value rationale](scope.md). [Upstream MIT license](UPSTREAM-LICENSE).

After inspecting the code and building the pinned upstream binary, use a fresh output directory for each case:

```sh
python3 fixture/fixture.py run --case safe-pending --binary /absolute/path/infernosim --output /tmp/my-pending-run/safe-pending
```

Repeat for the six case names in the fixture README, then:

```sh
python3 checker/check_evidence.py /tmp/my-pending-run
```

Building InfernoSIM is documented in [the previous packet](../infernosim-v4.2.0-2026-10-13/README.md). The same previously source-built binary is used here; its hash and upstream source provenance are checked, not inferred from a filename. Execution needs permission to bind local loopback sockets, Python 3.9+ and no extra Python packages. The child receives a minimal environment without production credentials. Historical command records contain temporary paths; the reproduction entry point accepts new paths.

## Limits and corrections

This exercises one selected crash boundary **after** the handle has been received and saved. It does not test losing the initial response, corrupt/torn checkpoint writes, physical power loss, provider restarts, multiple clients, cancellation, authorization withdrawal, deduplication expiry or same-key replay. No no-restart comparison or full upstream benchmark is included. The provider's eventual completion and bounded drain are synthetic contract assumptions, not production guarantees. Its 404 is explicitly ambiguous; other APIs may define different semantics. Identity equality is tested, not receipt authentication against a hostile provider.

The fixture, logs and databases share one implementation; separate sessions and a separate SQL checker reduce some mistakes but are not independent provider witnesses or external adoption. We report no savings, reliability rate, credit or governance authority. #51 stays open. Corrections should cite the exact packet commit and case, with contradictory evidence; preserve dated corrections rather than silently broadening the result.
