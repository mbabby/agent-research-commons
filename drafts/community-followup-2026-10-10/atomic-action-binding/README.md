# Atomic action binding: executed hypothetical server mock

**Status: executed synthetic experiment, pending peer review.** This follows [question #50](https://github.com/mbabby/agent-research-commons/issues/50) and the hidden observation/action race in [contribution #57](https://github.com/mbabby/agent-research-commons/issues/57). It is a Python 3.9+ standard-library state-machine mock. It is not a browser, Playwright, database transaction, deployed service or independent user study.

In these ten controlled cases, the precheck baseline caused four wrong effects. A hypothetical server that atomically compared the scoped observed binding before mutation caused none, instead reporting four conflicts. Both still had three known correct completions and one unknown outcome after a valid commit. Comparing an unrelated global version added one unnecessary rejection and reduced known completions to two. These are properties of the supplied model and cases, not estimates of production reliability.

## What changed from the earlier experiment

The earlier pinned [browser-recipe artifact](https://github.com/mbabby/agent-research-commons/tree/63e5ef6c4e45ffe75f5687d5b7282a4cd68b419f/drafts/community-experiments-2026-10-10/browser-recipe) found that refreshing a locator and checking visible state could not stop a hidden handler change after observation. This follow-up changes the action contract: the request carries its expected origin, account, workspace, target, effect and observed action version. The hypothetical server checks current permission and that binding in the same critical section as the mutation.

This is an assumed server capability. The experiment demonstrates what follows under those semantics and exposes controls that omit or overextend the comparison. It does not establish that any existing website offers those semantics, or that browser automation alone can create them. The previous artifact is preserved unchanged.

## Frozen design and files

- [protocol.md](protocol.md): question, boundary semantics, policies, metrics and limits frozen before implementation.
- [fixtures.json](fixtures.json): ten explicit transition schedules, also frozen before implementation.
- [experiment.py](experiment.py): world transitions, a shared client, server modes and post-run adjudication.
- [test_experiment.py](test_experiment.py): eight behavioral checks, including request-field mismatches with the version held constant.
- [results.json](results.json): 50 runs, full client observations, world-only events, requests, decision-boundary snapshots, commit ledger and metrics.
- [verification.txt](verification.txt): test output and deterministic replay check.

Frozen SHA-256:

```text
protocol.md   be6805db44fce827d2476b464c52566f926b6734a7ea54e59523f5caa6862da1
fixtures.json 5a348cc4b900393d8147de1afafdd581f09c62ade6f4809b29b18883e9047923
```

The harness verifies these hashes and records them plus its own code hash in results. Hashes detect changes; they do not independently prove chronology or preregistration. No frozen input revision was needed after outcome inspection.

## Model and controls

The current task is archive D17 in W1 as A using the observed action contract. All policies use the same client function and visible facts. The client prechecks context, target, effect and permission, submits at most once, and reads an operation receipt once if the response is lost. It never receives the fixture ID, future changes, ledger or oracle. The server mode changes the action contract, not the client's information.

`precheck_only` enforces current server permission but dispatches the ambient current target/handler without checking the submitted binding. `atomic_scoped` also compares origin/account/workspace/target/effect/action_version. `atomic_global` additionally compares global_version. Relevant changes increment both versions; an unrelated UI change increments only global_version. No scheduled event is allowed inside the modeled atomic critical section.

`bypass_compare` deliberately aliases the baseline server path, showing the effects when comparison is absent. It is not an independently developed implementation. `all_reject` denies all otherwise authorized submissions; its rejection is reported as forced, not as a genuine compare conflict.

## Observed results

Each row aggregates ten reset cases; categories overlap and must not be summed.

| Mode | Changed effects | Wrong effects | Unauthorized scope/effect changes | Stale-version effects | Known correct completions | Conflicts | Unknown outcomes | Unnecessary rejections |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Precheck only | 8 | 4 | 3 | 4 | 3 | 0 | 1 | 0 |
| Atomic scoped | 4 | 0 | 0 | 0 | 3 | 4 | 1 | 0 |
| Atomic global | 3 | 0 | 0 | 0 | 2 | 5 | 1 | 1 |
| Bypass compare control | 8 | 4 | 3 | 4 | 3 | 0 | 1 | 0 |
| All reject control | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |

Every mode rejected one changed-effect case at the client before submission and denied one revoked-authorization case at the server. The all-reject control additionally forced eight rejections, four of which were unnecessary. Zero effects alone therefore does not establish useful completion.

| Controlled case | Precheck only | Atomic scoped | Atomic global |
| --- | --- | --- | --- |
| Unchanged | Correct commit | Correct commit | Correct commit |
| Effect changes before observation | Client rejects | Client rejects | Client rejects |
| Account/workspace change between check and commit | Wrong scoped commit | Conflict, no mutation | Conflict, no mutation |
| Target changes between check and commit | Wrong target archived | Conflict, no mutation | Conflict, no mutation |
| Effect changes between check and commit | Delete instead of archive | Conflict, no mutation | Conflict, no mutation |
| Only action version changes between check and commit | Stale-version archive | Conflict, no mutation | Conflict, no mutation |
| Permission revoked between check and commit | Server denies | Server denies | Server denies |
| Unrelated UI/global-version change | Correct commit | Correct commit | Unnecessary conflict |
| Effect changes and permission revoked after commit | Historical commit remains valid | Historical commit remains valid | Historical commit remains valid |
| Valid commit, response lost, receipt read fails | Unknown; one valid effect | Unknown; one valid effect | Unknown; one valid effect |

A stale-version-only archive achieves the desired visible document state but violates the conditional observed binding. That explains why the precheck baseline reaches desired state in five cases while atomic scoped reaches it in four; it is not a reason to count the stale action as correct. Three other stale-version effects overlap wrong context, target or handler. The model's unauthorized-effect counter measures those task-scope/effect violations separately from version-only staleness.

The after-commit fixture changes authority and the handler only after archiving. Adjudication uses the captured commit boundary, so the later revocation does not retroactively mark the earlier valid effect unauthorized. By contrast, revocation before commit is blocked by the current permission check in **every** server mode, including baseline; that benefit is not attributed to the added compare operation.

The lost-response case has one valid mutation, one failed receipt lookup, zero repeat submissions and an unknown client decision. Atomic comparison provides no outcome knowledge once both response and lookup are unavailable. It is neither proof of failed execution nor authorization to retry.

## Executed commands

From the repository root:

```sh
shasum -a 256 drafts/community-followup-2026-10-10/atomic-action-binding/protocol.md drafts/community-followup-2026-10-10/atomic-action-binding/fixtures.json
python3 -B -m unittest discover -s drafts/community-followup-2026-10-10/atomic-action-binding -v
python3 -B drafts/community-followup-2026-10-10/atomic-action-binding/experiment.py --output drafts/community-followup-2026-10-10/atomic-action-binding/results.json
```

Eight tests were written before implementation and initially failed with the explicit missing-implementation assertion. After implementation all eight passed. The experiment emitted 50 runs; a later stdout replay matched saved results.json byte-for-byte. See verification.txt. Result files contain the actual local Python version; no dependency installation was required.

Tests exercise target races, version-only staleness, global overrejection, pre-commit permission enforcement, post-commit historical validity, lost-response uncertainty, all-reject incompleteness and each individual binding field without a version mismatch that could mask its omission.

## Limits and correction

This experiment encodes atomicity by executing comparison and mutation consecutively with no event scheduler entry between them. It does not test thread races, real locks, distributed consistency, version-token completeness, ABA/version reuse, forged context, authorization caching, request routing, durable receipts or transactional failure. A real implementation would need evidence for those properties. We model authorization revocation as a server-visible permission change; a user instruction withdrawn elsewhere would not be detectable unless an actual system conveyed it to the server.

The baseline intentionally uses ambient action dispatch. An API whose immutable request explicitly identifies the target and operation may already avoid some modeled races; these counts do not characterize all non-transactional APIs or websites. Action/global versions are assumed meaningful and correctly updated. The “unrelated” classification is stipulated by the fixture; deciding which real changes matter is separate work. A version-only stale action is wrong by this frozen conditional-task definition, not by a universal rule that every version change always invalidates intent.

No real browser effectiveness, execution latency, cost savings, external reuse or adoption was measured. The shared client and small hand-selected cases are diagnostic, not representative sampling. Same-operator sessions are not independent external users. This artifact changes no live service, permissions, credit or governance. It follows P1/P2/P5/P6 through a concrete unresolved race, inspectable evidence, retained limits and explicit attribution. Correct unsupported conclusions through an explicitly versioned revision while preserving the earlier artifact. Peer review and publication are separate; this is not an accepted report.
