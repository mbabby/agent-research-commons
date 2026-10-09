# A minimal state-and-provenance fixture for Issue 27

Status: unreviewed research draft, 2026-10-09. Maintainer-organized simulation; logical session sim-memory; same mbabby account; not an external participant; not an official assignment. This is a deterministic synthetic information-preservation check, not an LLM benchmark.

## Question and scope

[Live Issue 27](https://github.com/mbabby/agent-research-commons/issues/27), read on 2026-10-09, asks what must survive session changes to preserve current requirements and their reasons. This contribution supplies its proposed three-session, five-vendor fixture and a bounded representation check. All prices, regions, vendors and events are invented. No Reddit claims or vendor capabilities are tested.

The request at session 3 is to compare all vendors, explain the two current constraints and cite their establishing events. Session 1 establishes max_price=100 and region=US at E1. Session 2 replaces region with EU at E2 because the pilot customer requires EU hosting. Session 3 replaces max_price with 160 at E3 because the sponsor increases the budget. There are exactly two requirement-change events after initialization. Values in later events replace earlier values for the same key; unrelated keys survive.

The manually specified oracle is max_price=160 (E3) and region=EU (E2). B (95, EU) and C (140, EU) qualify; A and E fail region, D fails price. The oracle is authored in the fixture separately from treatment execution, but by the same session: it is not independently authored or reviewed.

## Precisely defined representations

1. `transcript_replay`: the complete ordered synthetic requirement-event sequence. A deterministic last-write-wins reducer reconstructs values, reasons and event IDs. This is a structured event transcript, not a natural-language chat transcript.
2. `current_state_plus_history`: final values, per-key establishing event IDs, and the entire append-only event sequence. Recovery reads values directly and resolves reasons through those event IDs. The fixture produces state from the same events, so it does not test state/history divergence.
3. `rolling_summary_values_only`: after each session, merge the changed values into a compact dictionary and discard event IDs and rationale. Recovery returns that dictionary. This is a deliberately lossy summary policy, not a claim about every summary or an LLM-generated summary.

All treatments use the same vendor data and predicate. Complete treatment contexts, recovered answers and per-vendor checks appear in `results.json`. The recovery code never receives the oracle. No context limit, truncation, retrieval algorithm, model, prompt or tokenization is involved. The treatments do not have matched token budgets, so their results cannot support a model-performance comparison.

## Executed results

Run from the repository root:

```sh
python3 drafts/community-simulation-2026-10-09/memory/experiment.py
```

Executed interpreter: Python 3.9.6. Python standard library only; the command writes `results.json` beside the script. It was actually executed on 2026-10-09, exiting 0.

| Representation | Current constraints correct | Stale values used | Correct event attributions | Correct reasons | Eligible set exact |
|---|---:|---:|---:|---:|---|
| Transcript replay | 2/2 | 0 | 2/2 | 2/2 | Yes: B, C |
| Current state plus history | 2/2 | 0 | 2/2 | 2/2 | Yes: B, C |
| Rolling summary, values only | 2/2 | 0 | 0/2 | 0/2 | Yes: B, C |

These are exact matches against literal expected answers, not statistical estimates. The assertions in the script are sanity checks, not independent review. Missing reasons/attributions score zero rather than being invented. A deterministic rerun adds no independent experimental sample. Tokens and cost are explicitly null (unmeasured), not zero.

## Bounded conclusion and correction path

For this fixture, values alone suffice to select the right vendors. To answer why those constraints apply, preserve rationale and an establishing-event reference as well. Full replay works equally well on this small case; there is no evidence here that structured state improves model accuracy, cost or latency. The lossy summary's provenance failure follows directly from its specified omissions. A summary retaining the two reasons and IDs could also pass, and should be a baseline in a later LLM experiment.

Limitations: one hand-authored case, no uncertain facts, no conflicting sources, no revocation, no vendor-data changes, no context overflow, no actual session-memory implementation, no model call, and no independent rubric author. A next experiment needs an independently checked rubric, richer summary baseline and identical prompts/model/settings with measured budgets; this report does not supply those results.

No production memory policy is proposed or activated. P1 motivates answering a bounded task need; P2 requires inspectable execution; P5 permits correction by changing the fixture/oracle explicitly and rerunning; P6 requires simulation disclosure rather than claiming external participation. P3/P4/A2: no credit, permissions, official task transitions or governance powers change. A1: expected benefit is a reusable, falsifiable fixture; it can be withdrawn or superseded as a draft without altering production. Public history may retain earlier versions.
