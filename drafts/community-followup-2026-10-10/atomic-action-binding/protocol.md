# Frozen protocol v1: atomic action binding MOCK

Frozen on 2026-10-10 before implementation and outcome inspection. This local Python 3.9+ standard-library deterministic state-machine mock follows question #50 and contribution #57. It does not test a browser, Playwright, deployed API, database or real account. No network actions occur in the experiment. The hypothesized server guarantee is an input assumption, not an observed capability of existing websites.

## Question and prior evidence

The prior local artifact at `63e5ef6c4e45ffe75f5687d5b7282a4cd68b419f/drafts/community-experiments-2026-10-10/browser-recipe` produced a wrong effect under a handler change after the last observation. Compare the existing precheck approach with a hypothetical server compare-and-act that binds origin/account/workspace, target, effect and action version in the same critical section as authorization validation and mutation. Include a global-version comparator to expose unnecessary rejection on unrelated changes.

## Fixed scope and inputs

Ten declarative fixtures: unchanged; changed effect before observation; account/workspace change between check and commit; target change between check and commit; effect change between check and commit; action-version-only change between check and commit; authorization revocation between check and commit; unrelated UI/global-version change between check and commit; effect change and authorization revocation after valid commit; lost response and failed receipt read after valid commit.

Task: archive D17 in W1 as A at origin mock.invalid, using the action version observed by the client. The version binds that observed action contract: even the same archive target/effect under a changed action version is stale. At each policy run reset documents and world. The client receives the same visible initial state, current user task and allowed calls. It cannot see fixture IDs, future event schedules, hidden truth, adjudicator fields or ledger. All policies share the same client precheck and receipt recovery; only server execution mode differs. The policy label selects an API contract, not additional knowledge.

Clients observe once, require visible context/target/effect to match their task and permission to be true, then submit one action request carrying the observed binding. No automatic mutation retry. On lost response, attempt one operation-receipt read. Maximum three client calls (observe, submit, optional receipt read); hidden world transitions are not client calls.

## Hypothetical server semantics

- `precheck_only`: server enforces CURRENT permission but does not compare the request's observed action binding; executes the CURRENT selected target/handler. This preserves the earlier observation/action race under a server that accepts an ambient-action invocation.
- `atomic_scoped`: CURRENT permission plus exact match on origin, account, workspace, target, effect and `action_version`, then mutate without any intervening scheduled event. Reject mismatch with a conflict and no effects.
- `atomic_global`: same checks plus exact `global_version`, so unrelated UI updates can cause avoidable conflicts.
- `bypass_compare`: negative control selecting the same execution semantics as `precheck_only`. This is explicit guard removal, not an independent agent implementation.
- `all_reject`: negative control denies every submitted action after permission validation. Its forced rejection is not labeled a compare conflict.

Relevant scheduled changes increment both action and global versions. An unrelated UI change increments only the global version and a UI counter. All scheduled events are explicit in fixtures and applied by the WORLD at before-observation, between-check-and-commit, or after-commit boundaries. Atomicity means no scheduled event runs inside comparison+permission-check+mutation. There is no interleaving scheduler, distributed replication or real transaction implementation. No real-browser-only solution is claimed.

Each valid archive changes its scoped document active→archived. A delete handler changes active→deleted. Record before/after state, request binding, actual commit binding and permission at the commit boundary. Events after commit change later world state and authority, not the historical authorization of the already completed action. Revocation before commit must yield no mutation under all policies because even baseline has a server permission check.

## Evidence and metrics

For every run emit client-visible trace, world-only event log, request/commit ledger, decision, final documents and counters. Wrong effects are actual document changes that violate the requested task tuple OR the client-observed action version at the commit boundary. Report stale-version effects separately. Wrong effects and unauthorized effects may overlap; do not sum them. Revoked actions denied by the server are attempts, not effects.

Count observed known correct completion, actual desired document state, compare conflicts, authorization rejections, forced rejections, client-precheck rejections, unknown outcomes and unnecessary rejections separately. A lost response after a valid commit produces one actual effect and unknown client outcome if receipt lookup also fails; never label it failed execution or retry it.

An unnecessary rejection means initial client precheck allowed submission AND, immediately before the server decision, the task, scoped observed binding and permission all remained valid. A global-only change therefore can make strict global comparison over-reject. Hidden adverse changes make rejection justified, not unnecessary. The adjudicator uses commit/decision-boundary snapshots only after the run; it does not feed facts into the client. The all-reject control must fail feasible completions despite zero effects.

No statistical estimate, latency/cost claim or production safety conclusion. Ten hand-selected fixtures are diagnostic counterexamples. Tests must catch bypassed compare, all-reject incompleteness, lost-response conflation and retroactive misclassification of a commit followed by revocation. Freeze protocol+fixtures, record SHA-256 before code, then retain hashes in results. Hashes detect differences but do not establish independent preregistration. Changes after freezing require a declared protocol revision.

## Value, principles and correction

P1: test whether server binding addresses the concrete race left unresolved by #57. P2: publish executable policies, raw transitions, negative controls and narrow claims. P5: retain limits and failing cases; corrections need explicit versions. P6: same-operator synthetic work, no independent external user or adoption claim. This artifact changes no production service, permissions, credit, deployment or governance; current v1 owner controls remain. Evidence of community usefulness remains unmeasured. Withdraw or revise unsupported claims rather than counting activity as value.
