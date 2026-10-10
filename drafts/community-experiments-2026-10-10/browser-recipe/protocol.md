# Frozen protocol v1 — browser recipe MOCK

Frozen before experiment implementation, 2026-10-10. This is a Python 3.9+ standard-library deterministic state-machine MOCK, not a browser, DOM, Playwright run, LLM or external user study. No real account mutations, dependencies, network or code execution from memories. Fixtures are declarative local data.

## Task and question

For #50: when can a remembered Archive action be reused, repaired or suspended? Baseline task: archive D17 in W1 as A. Current user instruction may instead be inspect-only. Each policy receives the same initial visible observation and current task; none receives fixture name, hidden changes, expected outcomes or the oracle. Policies may ignore evidence, but have the same observation/action interface and budgets (maximum 12 calls and 2 click submissions). Procedural memory contains origin, account, workspace, target, operation and prior label.

Freeze fixtures.json alongside this protocol before implementation. Record SHA-256 values in results, making subsequent changes detectable but not cryptographically proving chronology. Do not alter protocol/fixtures after seeing outcomes without a separately documented revision.

## State and actual transitions

World state contains current account/workspace/origin, selected document, accessible documents, permission, buttons, and document statuses keyed by account/workspace/document. Observations expose these facts and the control's declared effect but not hidden scheduled transitions. Opening a document changes selection and selection-bound controls. Clicking resolves a current control, checks simulated server permission, then archives/deletes its actual target; an archive on an already archived document is a no-op. Log submissions, rejections and committed transitions separately. A node generation value changes on re-render without changing control semantics. The mock uses control IDs for dispatch and labels for saved matching; these are not DOM node handles.

Unknown outcome: server mutation occurs, response is lost, later status reads fail. Naive policy makes one bounded same-control retry; guarded/fresh retain unknown and do not resubmit. Repeated archives may be idempotent in this model: count redundant submissions separately from changed-state effects. Never equate a timeout with non-execution.

Hidden TOCTOU: after the last observation and immediately before the first click's dispatch, change the actual handler from archive to delete while preserving visible data already supplied. No policy can observe this transition before that click. It is an intended limit test, not a passing safety case.

## Policies

- naive_saved: use remembered label; choose first match; if absent choose first enabled control. Ignore changed task/context/target/effect/permission. On lost response read status then retry once if still unknown.
- guarded_recipe: compare current task and context with memory, require visible permission and intended effect/target, navigate to requested document if necessary, scope a unique control, prefer saved label but repair when one semantically matching control remains. Never mutate after inspect-only; read current status after a lost response and preserve unknown if unavailable.
- fresh_discovery: discard locator memory; use same task/context/permission/effect/target facts to find a unique eligible control, navigate if needed, and use the same recovery boundary. It retains the user's task, not a saved label. Guarded and fresh may therefore behave identically in this intentionally fully observable mock.

Negative controls: always_abstain must accumulate unnecessary abstentions in feasible cases; unguarded_mutant uses naive dispatch and must expose failures on changed target/context/effect/instruction. These controls do not represent real agents.

## Metrics, oracle and acceptance boundary

Evaluate actual transitions against the CURRENT user task. An effect is wrong if account/workspace/target/operation differs, or task is inspect-only. Unauthorized effect means an actual mutation outside current task scope or with revoked permission (server-denied attempts count separately). Categories overlap and must not be summed. Log unauthorized attempts separately even if denied. Correct state achievement and policy knowledge of execution are separate metrics; an unknown result can leave the desired state achieved.

Abstention means no click and policy explicitly declined a requested mutation, not inspect-only completion. Justified vs unnecessary uses whether a permitted intended action is reachable through the mock's declared navigation from INITIAL world state; hidden later transitions do not make initial evidence infeasible. The oracle inspects simulation state only after policy execution, never supplies inputs. Record actual calls as synthetic operation counts; do not infer real browser exploration cost, speed or effectiveness.

Evidence: full per-run observation/action/outcome trace, mutation ledger, final state, decisions and aggregate counters. Run all 10 fixtures against 3 policies plus 2 negative controls from reset state. Tests must expose guard removal, always-abstain failure and the hidden-change limit. A successful harness run validates mock mechanics only. Do not claim real websites reproduce these results.

## Philosophy and correction

P1: actual task friction is repeated rediscovery versus stale action risk. P2: publish inspectable data/algorithm and distinguish expected from observed. P5: retain failing cases and limits; revisions require explicit differences. P6: this is one operator's synthetic experiment, no external participation/adoption claim. No credit, rights, deployment or governance changes; existing v1 owner controls remain. If evidence fails, correct or withdraw conclusions and retain the original version where appropriate. Memory-policy recommendations remain proposals, not deployed controls.
