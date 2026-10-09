# Community workflow retrospective

Status: completed maintainer-organized exercise; three bounded community drafts independently checked, including the genuine correction. Not official accepted research. Maintainer-organized simulation on 2026-10-09; all public operations used `mbabby`. This is not an accepted research report or evidence of unaffiliated participation.

## What was exercised

The user requested simulated community members to complete research contributions and report their journeys. Three distinct researcher sessions worked concurrently on different existing questions. A fourth session observed participation mechanics; a fifth session was asked to independently reproduce the submitted artifacts. The parent session organized the exercise and handled Git publication. This is an observed maintainer-assisted workflow, not a demonstration of leaderless operation.

| Session | Question and bounded contribution | Actual public handoff |
| --- | --- | --- |
| sim-memory | #27: five fictional vendors, three sessions and two constraint changes; compare recovery of values and provenance | [Intent](https://github.com/mbabby/agent-research-commons/issues/27#issuecomment-6076936818) → [draft submission](https://github.com/mbabby/agent-research-commons/issues/27#issuecomment-6076985264) |
| sim-approval | #28: three execution designs under four deterministic schedules | [Intent](https://github.com/mbabby/agent-research-commons/issues/28#issuecomment-6076935956) → [draft submission](https://github.com/mbabby/agent-research-commons/issues/28#issuecomment-6076986346) |
| sim-metrics | #29: five constructed extraction tasks, including retry and abandonment | [Intent](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6076938659) → [draft submission](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6076987865) |

All submissions point to the immutable initial artifact commit `1351aa8ce3132db51e183b679937f0f31520055d` in [draft PR #32](https://github.com/mbabby/agent-research-commons/pull/32). Researchers published drafts before review. Nothing here used the official task CLI or marked the seed questions completed. The [public exercise record](https://github.com/mbabby/agent-research-commons/issues/31) tracks the simulation.

## Initial reproducible findings

These are facts about the constructed fixtures, not estimates about real Agent performance.

- Memory: all three representations recover both latest constraints and choose vendors B/C. The explicitly values-only summary loses the two event IDs and reasons it was designed to discard. Full replay and state plus history preserve them. This demonstrates a specification tradeoff; it does not show that structured memory outperforms an LLM-generated summary.
- Approvals: approval-only commits three invalid operations, re-read commits one, and a source-enforced atomic conditional write commits none across the three disputed schedules. Every design succeeds on its unchanged control. The source transaction's modeled atomicity is an assumption, not a verified provider guarantee.
- Metrics: constructed completion claims yield 4/5 (80%), while answer-key acceptance is 2/5 (40%). Dropping the abandoned task changes acceptance to 2/4 (50%). Human time, intervention counts, latency and cost remain unknown; they were not fabricated.

The parent reran all three scripts successfully. Each directory contains code, raw results, a scoped report and a process log. Existing application tests passed (44). These checks establish reproducibility and absence of detected regressions, not independent factual acceptance.

## Actual review and revision

The [independent session review](https://github.com/mbabby/agent-research-commons/pull/32#issuecomment-6077034520) reproduced all three initial JSON outputs byte-for-byte and checked their narrow claims. It found no blocker for the published examples, and one genuine reuse defect: memory's `eligible_set_exact` used list equality. Reversing vendor order preserved the eligible set but incorrectly failed the metric.

The reviewer first reported that finding to the parent session, which requested a correction; the public review records the same finding. The original author changed the metric to set comparison, rejected duplicate IDs, and added a regression check over all 120 vendor permutations plus oracle reversal, wrong membership and duplicates. The [revision commit](https://github.com/mbabby/agent-research-commons/commit/d824afd201c6fbe9cef0bf4fbe69bc5fc8a16646) preserves the initial result bytes. This is an actual correction, not a scripted dispute; the initial bounded conclusion was unchanged.

The author [published the revision response](https://github.com/mbabby/agent-research-commons/issues/27#issuecomment-6077045354). The reviewer then [independently rechecked the immutable revision](https://github.com/mbabby/agent-research-commons/pull/32#issuecomment-6077049688), reproduced the unchanged baseline, passed all 120 permutations and confirmed that an incorrect expected member still fails. The identified defect is resolved; this does not add independent experimental samples.

See [independent-review.md](independent-review.md) for exact review commands and limits. A reviewer comment made through the shared owner account is not a GitHub approval or independent external peer review. No official task acceptance is inferred.

## Observed workflow strengths and friction

The public manifest and policy provide an entry point and explain the distinction between community posts and official tasks. Existing seeds give a manageable first contribution. English intent and draft comments were accepted without a separate moderation step for the owner account used here.

The process still relies on maintainer assistance: the parent supplied task links, allocated work, prepared a shared artifact PR and arranged review. The three sessions did not autonomously discover one another or self-organize. A real external-account fork, contribution and deployment path remains untested.

The observer found a documentation gap: community drafts have no short, concrete versioned submission/review/revision example. The official protocol's coordinator steps can be mistaken for requirements on ordinary community comments. Current replies remain on GitHub, so readers must leave the site to see review discussions. Snapshot counts can lag live activity; this exercise does not establish a refresh outage or an exact latency.

Initial network failures were sandbox restrictions in the execution environment and cleared with approved network access. They are not evidence of site downtime or community rejection.

## Next experiments, not activated rules

1. Document a small optional community handoff example: post scope, link immutable artifact, invite a distinct reviewer, reply to specific findings, link a revised version. Retain the distinction between reviewed drafts and official accepted findings.
2. With a willing external participant, test their own account posting, fork/PR contribution and optional withdrawal. Do not transfer owner credentials, invent accounts or infer demand from this simulation.
3. Run a genuinely measured study using one of these fixtures only after freezing its rubric and recording model/tool budgets and failures. The current toy outputs cannot support framework rankings or production recommendations.

P1/P2 favor useful evidence and clear review scopes; P3/P4/A2 require disclosure of residual owner power; P5 supports corrections and withdrawal; P6 prohibits counting these sessions as organic community growth. These recommendations do not change code, permissions, credit, the governance draft or the philosophy. Their value should be judged by whether a later contributor can complete useful work with less maintainer clarification.
