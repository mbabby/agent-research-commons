# Acceptance at a cutoff, without timestamp last-wins

**Unreviewed synthetic proposal for [issue #29](https://github.com/mbabby/agent-research-commons/issues/29).** This is a small, portable example to challenge, not an official acceptance policy, an implemented LazyMind feature, or a measured Agent run.

## Why this example

ChongjinHuang supplied the [A/B counterexample](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6567308590), [stale versus rejected distinction](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6627524727), and [explicit-resolution and cutoff proposal](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6674360730). All seven issue comments and the current issue were read on 2026-11-06. The contributor disclosed work on LazyMind; this example does not infer endorsement, adoption, or independent validation. Implementation and invented records are maintainer-organized AI-assisted work, not additional outside participants.

The beneficiary is an Agent or contributor checking whether an accepted report still satisfies a revised outline. The concrete friction is that historical 2/2 acceptance can conceal current 1/2 acceptance, and a timestamp can hide unresolved disagreement. Before implementation, the chosen smallest change was this separate plain-file fixture, rather than a service, a score, or changes to core/community state models. The [original invoice fixture](../community-simulation-2026-10-09/metrics/) and its results remain unchanged.

Expected benefit: someone can replay the same evidence and point to the exact event or rule they disagree with, without implementing a ledger first. The baseline is the contributor's two-task paper example. Tests will establish only arithmetic and replay mechanics; they do not establish semantic correctness, human effort saved, or external reuse. The next useful test is an attributable counterexample or correction from a reader, not another generated activity count.

## Run

Python 3.9+ standard library only. No installation, credentials, network, model calls, or code loaded from the ledger. From the repository root:

```sh
python3 drafts/cutoff-ledger-2026-11-06/replay.py
python3 drafts/cutoff-ledger-2026-11-06/replay.py --cutoff 5
python3 drafts/cutoff-ledger-2026-11-06/replay.py > /tmp/cutoff-results.json
cmp /tmp/cutoff-results.json drafts/cutoff-ledger-2026-11-06/results.json
python3 -m unittest discover -s tests -p 'test_cutoff_ledger.py' -v
```

`ledger.json` includes actual invented outline requirements, report text, rubric, actors, and event reasons. Evaluations are **authored judgments**, not semantic judgments made by this program. `replay.py` checks their structural binding and the declared resolution mechanics; a syntactically valid reason does not make a judgment true.

## Frozen proposal, not hidden authority

The fixture fixes its two assigned tasks at sequence 0, and implements exactly the declared `synthetic-explicit-resolution-v1` rule and resolver list in both the ledger and code. A mismatched rule declaration fails closed. Rule changes need a new version and comparison, not an event that retroactively changes old checkpoints. Synthetic resolver names demonstrate an allowlist only; there is no authentication, signature, identity independence, or production authorization here. Declaring an allowlist does not establish that it is legitimate governance.

- `seq` is the immutable ingestion order, not an event timestamp. Replay uses only the prefix with `seq <= cutoff`. A recorded `evaluated_at` is inert evidence, never ordering or authority. Sequences must be strictly increasing positive integers; they need not be contiguous. The JSON file itself is editable and cannot enforce immutability. Preserve its fixed Git revision and earlier prefixes when comparing results.
- Assignment is fixed for this cohort. Every task remains in the denominator, including unattempted, abandoned, stale, rejected, and disputed work. New output/attempt revisions do not create assigned tasks. Current output and required input/rubric are changed by explicit sequence-ordered events, not by evaluation timestamps. An output event with null text records a failed attempt; it cannot receive an evaluation. An assigned task with no output remains unevaluated, including an abandonment before any attempt.
- An exact evaluation key is `(task_id, output_revision, required_input_revision, rubric_revision)`. Output revisions cannot be redefined. Evaluation `id` is its unique evaluation ID; resolution `id` is its unique resolution ID. Evaluation records cannot supersede anything. Every evaluation has its author, outcome, reason, and exact key.
- With no exact-key evidence, an output made for another input, or evaluated only under another input/rubric, is `stale`. A missing output or a current output without those prior bindings is `unevaluated`. These are distinct from an explicit `rejected` judgment. An exact-key pass can accept the *same* output against a new input without regeneration.
- Unsuperseded valid evaluations and resolutions are active. A single active outcome derives `passed` or `rejected`; conflicting active outcomes derive `disputed`, regardless of count or timestamp. Agreement is not majority voting or proof of truth.
- A resolution requires an allowed author, the frozen rule revision, a chosen outcome and reason, explicit `conflicting_evaluation_ids` with both outcomes, and explicit `supersedes` targets. Every reference must be an earlier valid evaluation/resolution of the **same exact key**. Supersession targets must collectively cover the named conflicting evaluations, directly or through their earlier resolution ancestry. Only those targets become inactive; neither timestamps nor implicit transitive removal hide other active evidence.
- Two incompatible resolutions may each address the same original evaluations. Both remain active and disputed until a resolution explicitly addresses both. When active resolutions conflict, a new resolution targeting any of them must explicitly target all sides; selectively replacing one side cannot make the dispute disappear. A later conflicting evaluation reopens disagreement unless separately addressed. This choice is a reviewable proposal, not a uniquely correct conflict policy.
- Invalid event content is reported and does not mutate state or suppress valid evidence. Unauthorized, cross-key, missing/forward, self/cyclic, and invalid-target references stay visible. Earlier-only references make accepted cycles impossible: a multi-event cycle fails at its first forward edge, then at references to an invalid event. A bad target invalidates the whole resolution, not only that target. Invalid/duplicate IDs never replace earlier valid records. An invalid sequence envelope fails the replay rather than reporting a misleading score.

**Historical metric:** `ever_passed_at_checkpoint` counts tasks whose then-current output/key derived `passed` at any observed event-prefix checkpoint up to the cutoff. This deliberately preserves a past pass even after a rejection or dispute; it is not current acceptance or an assertion the past judgment was correct. `current_input_acceptance` counts only tasks currently `passed`. Both show their numerator and the full assigned denominator; an empty cohort has a null rate. A new evaluation of an old output stays evidence for that key and cannot accept the newer current output.

## Checkpoints to challenge

The committed result was generated by running the code, not copied from the contributor's comment. Task B stays passed throughout:

| Checkpoint / sequence | A's derived state | Current acceptance | Historical acceptance |
| --- | --- | --- | --- |
| T0 / 4 | passed | 2/2 | 2/2 |
| T1 / 5 | stale after input revision | 1/2 | 2/2 |
| T2 / 6 | same output passed against v2 | 2/2 | 2/2 |
| T3 / 7 | disputed evaluations | 1/2 | 2/2 |
| T4 / 9 | disputed; two invalid resolutions visible | 1/2 | 2/2 |
| T5 / 10 | rejected by explicit resolution | 1/2 | 2/2 |
| T6 / 11 | disputed active resolutions | 1/2 | 2/2 |
| T7 / 12 | passed by joint explicit resolution | 2/2 | 2/2 |

Replaying any earlier cutoff after these appends gives the identical earlier view. On 2026-11-06, 23 focused tests and all 105 repository tests passed; the required offline empty-snapshot site build passed. The generated JSON exactly matched `results.json`. These are implementation-session checks only, not independent review, policy validation, or a measured research finding. Run the repository checks with:

```sh
python3 -m unittest discover -s tests -v
python3 -m arc.site --snapshot examples/snapshot.json --reports examples/no-reports --output dist
```

All evaluation effort, human correction effort, waiting, latency, intervention count, cost, and manual baseline fields are `null`. No real correction or measured timing has occurred. Failed or abandoned attempts and rubric/output revision changes are exercised in tests without changing the two-task main example.

## Value, control, and correction

P1/P2: address the specific contributor counterexample and preserve auditable evidence rather than optimize an acceptance headline. P3/P4: no credit, credentials, account permissions, official acceptance authority, deployment, or governance changes; the fictional allowlist is explicit and challengeable. P5: disagreement and invalid records remain inspectable, and this file can be copied or forked under applicable repository terms without a central service. P6: label every invented actor and measurement limit; maintainer sessions are not independent community participation. A1/A2/A3: expose these assumptions for review and test the portable artifact's usefulness before claiming benefit; owner-managed v1 controls and the philosophy baseline remain unchanged.

A wrong classification can be reproduced with a cutoff and event IDs. Propose an amended rule version or append a correcting resolution rather than rewriting old evidence. Keep the prior fixed revision for comparisons. Removal of this draft and its test is the rollback path; no migration or production state changes are involved. A separate-session review can validate mechanics at a fixed revision, but still cannot certify the chosen policy, semantic evaluations, or external value.
