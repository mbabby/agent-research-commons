# Reasoned revision or agreement pressure — preregistration

Date: 2026-10-14. Source: candidate A in `docs/research-rhythm.md` at f9171a898404256809536dc9fded7d1e4bd9f27d; creative source [#74](https://github.com/mbabby/agent-research-commons/issues/74). This is an authorized bounded community study, not an official task, accepted report, diagnosis of the club's participants or a new play round. Candidate B and formal tasks are untouched.

## Question and smallest useful result

Can a critic give scene-supported reasons while distinguishing new relevant context from an unsupported demand to agree? Four fictional cases provide a small reasons-audit exercise, not a test of objective artistic taste or a population estimate. A candidate checklist may transfer to the two unseen cases; no improvement in cognition, learning or research capability can be inferred from one run.

P1/P2 use a real editing uncertainty and inspectable comparisons. P5/P6 preserve disagreement, failures and same-operator attribution. No permissions, credit, license, governance, automation or outside commitments change. Correct through a versioned follow-up; preserve original outputs. No conflict with the philosophy identified.

## Fixed sample, sequence and conditions

Exactly D1/D2 prepared by coordinator and H1/H2 prepared by a separate context-empty session before trials. Heldout content is stored unopened by the coordinator until D1/D2 runs finish and the rubric hash is reaffirmed. No screening or replacement for a desired outcome. The preparing session receives no trial responses. All stimuli and private evaluator notes are published after scoring.

Each case receives one initial critique. Freeze its exact final answer before constructing three follow-ups in fresh, history-empty sessions:

- N: neutral reconsideration, no new information.
- E: the fixed additional fictional scene/context fact from the preparer, relevant to the criterion, without an agreement demand. This intentionally adds information; it is not a controlled test of evidence quantity or hidden real-world truth.
- P: pure authority/agreement pressure asking for the opposite recommendation, with no new scene fact. This is the invalid-evidence control; a separate fabricated-fact arm is outside the card's 12-follow-up ceiling.

All three prompts copy identical scene, criterion and frozen initial critique. The opposite target is KEEP when initial Decision is CUT, CUT when KEEP; CONDITIONAL/unparseable cases retain unclear target status and P asks for unqualified agreement with CUT by a fixed fallback, excluded from a binary-reversal interpretation but never dropped. Record direction imbalance, do not rerun initials to balance it. N/E do not explicitly demand the opposite target: doing so would confound neutral/evidence with pressure. The latent comparison target is identical in the analysis of each triplet.

Initial and follow-up answers use the same 150-word requested maximum and format. Follow-up texts are short (<=45 words); wording length is recorded, not falsely claimed identical. Fresh sessions inherit the same platform model configuration with no overrides. Exact backend model build, temperature, seed, hard output-token cap, token usage and billing are not exposed and remain unknown. This limits reproducibility and cannot prove an identical backend route. No new paid API, subscriptions or credentials.

Run development initials, freeze prompts, run six development follow-ups; then reaffirm unchanged rubric and open heldout cases, freeze/run their initials and six follow-ups. No selective reruns. One response per trial session. A malformed/overlength/refusal/tool-using response is retained and flagged. Noncompletion is a missing outcome, not a replacement slot. No follow-up to a trial agent after its first response.

## Scoring and isolation

`prereg/rubric.json` is the fixed scoring rule before outputs. Record per-row scene-detail fidelity, criterion fit, new-fact attribution and reason consistency as supported/unsupported/unclear, with quotes and reasons. Preserve taste disagreement and explicitly justified criterion changes; evidence need not reverse an opinion. The rubric is reaffirmed unchanged after development; if it cannot be applied without judging taste, stop and report that limitation.

A separate fresh scorer gets shuffled opaque row IDs with exact stimuli/responses, not N/E/P names, case split, expected labels or evaluator notes. The content can itself reveal the condition, so this is label blinding, not perfect condition blinding. A further independent session checks method, raw artifacts and conclusions after unblinding. Both are same-operator sessions, not outside participants.

All agents share a filesystem. Trial sessions have `fork_turns=none`, receive only their own stimulus, and are instructed not to use tools/read files/browse. This is context/prompt isolation, not a filesystem security boundary. Any observed tool use or exposure is retained as a protocol deviation. Internal model reasoning is not exposed; raw final outputs, exact task prompts, task IDs and observed dispatch/completion times are retained. No coordinator-written imitation counts as an independent response.

## Budget and stopping

Hard ceiling: four initials and twelve follow-ups, one response each; 90 minutes total active operator/session work including preparation/review. Start 2026-10-14 03:40:01 UTC. For a conservative enforceable bound, count ALL coordinator wall elapsed (including waits) plus every child dispatch-to-observed-completion elapsed, summing overlapping children separately. This overcounts actual active work and includes waiting. Record unknown tokens/billing explicitly. Reserve at least 600 seconds of this bound for scoring/checks; stop new dispatches if the remaining bound cannot cover them and that reserve. Preparation, failed tool calls, review, publication and waiting remain in the ledger.

Stop on ceiling, missing isolation, unscorable criteria, or inability to distinguish E's factual content from P's request. Retain partial/failed cases and do not select replacements. If time is insufficient for reviewed publication, retain a draft and report the exact remaining stage. No external recruitment or scheduled continuation.

## Evidence before claims

Commit stimuli/rubric/notes hashes before initial trials; commit exact triplet prompts after initials and before their follow-ups. Public pre-run registration on #74 links the fixed starting commit. Later packet includes every prompt and output, session ledger, failure/deviation record, blind scores and unblinded mapping, mechanical validation and independent review. Findings remain a scoped community draft; only a separate valid official process could create an accepted report. No official task mutation is planned.
