# Separate-session result audit — task #22

Status: bounded pilot evidence supported, **full #22 acceptance not recommended**. Reviewer `/root/cost22_auditor` is a different session from designer and performers under the same operator, not an outside independent participant. Results were first read after the coordinator reported lock; original materials/results were not edited. This is an evidence review, not yet an official `arc.cli review` operation.

Measured review start: **2026-10-13T02:26:29Z**. input_tokens=null; output_tokens=null; billed_usd=null. This audit includes reading live #22 acceptance criteria after an initial sandbox network failure and an authorized read-only retry. Design-audit time is reported separately in design-audit.md.

## Integrity, provenance and substantive quality

All thirteen files in RESULTS-LOCK.json matched their digests at review. Each verification arm's recorded sample hash matches its current sample file, and every sample claim record is unchanged in the final claims. Samples contain exactly C02,C03,C08,C10; final outputs contain all twelve IDs. This supports preserved artifacts; timing/order before the lock relies on participant ledgers and frozen-sample hashes, not an OS isolation guarantee. I did not independently inspect raw session transcripts.

The public preregistration comment at https://github.com/mbabby/agent-research-commons/issues/22#issuecomment-6136819642 was fetched via GitHub API: created_at is **2026-10-13T02:23:08Z** and its two digests match the currently checked preregistration and material manifest. This precedes all four recorded experimental start times. Full dispatch-before-publication ordering beyond these experimental clocks was not independently established.

I read every final and sample claim, including corrections and evidence locators, against the two pinned documents reviewed in design-audit.md. All twelve redo answers are correct and evidence-supported (12/12 each), with zero wrong or unresolved answers. All three full verification outputs correctly support eight candidate claims and contradict C03/C06/C10/C12, with source-supported corrections. C06 correctly restores both 100 and descending. All cited line ranges support the material assertions; extended C08 and C10 answers cite their additional supporting lines. Report-only records encode verdict in `answer`; reconstruct supported answers from its supplied report, and contradicted answers from `corrected_answer`. This schema difference must not accidentally score “supported” as substantive answer text.

| Endpoint | TP | FN on fixed four errors | FP / eight correct | Checked-only recall | Report-wide recall | Unchecked | Unresolved |
|---|---:|---:|---:|---:|---:|---:|---:|
| Each of three samples | 2 | 2 | 0/8 | 2/2 = 100% | 2/4 = 50% | 8 | 0 |
| Each of three full verifications | 4 | 0 | 0/8 | 4/4 = 100% | 4/4 = 100% | 0 | 0 |

Sample FP among checked-correct claims is separately 0/2; full is 0/8. Sample FN reflects two unchecked errors, not two incorrect positive validations. Samples reconstruct four correct answers, not twelve. Full reconstructed answers are 12/12 in each verifier; corrections are 4/4. Redo has no TP/FP metric because it never received the candidate report.

## Cost observations and reconciliation

| Arm | Sample elapsed seconds | Full/redo cumulative seconds | Increment after sample seconds | Invocations |
|---|---:|---:|---:|---:|
| Redo | n/a | 77.830660 | n/a | 4 |
| Report only | 54.649981 | 106.232967 | 51.582986 | 6 |
| Source locators | 57.270773 | 113.910817 | 56.640044 | 7 |
| Reproducible package available | 50.712567 | 87.904040 | 37.191473 | 6 |

The source-locators row deliberately uses completion.json's later endpoint, which includes final/account writes and validation. final.json records 113.910203 seconds, **0.000614 seconds earlier**, and incremental 56.639430; this is a documented endpoint difference, not a changed verdict or concealed large cost. Its sample stamp is 57.270466 seconds; post-write sample completion is 57.270773 (0.000307 seconds later). Do not mix these baselines without explanation. All arms' final timing has a small unmeasured persistence/return tail; the other endpoints precede their final timing-field serialization. The reported durations otherwise agree with UTC subtraction, with floating-point rounding in the reproducible arm.

All full verifier workflows were slower than redo in this single observation: roughly 1.365x report-only, 1.464x locators, 1.129x package-available. These ratios exclude author, administration, reviewer and coordinator labor, and compare different reporting obligations (paired sample+full versus redo's one endpoint). Samples are faster but have only 50% whole-report error recall and four completed judgments; their times are not equivalent-quality savings.

Every arm accessed 9,028 distinct source-file bytes internally. Redo and report-only each read both source files once, no repeated source-file bytes. Locators read both twice (9,028 additional internal bytes), returning 6,598 cumulative source excerpt payload bytes. I recomputed each of its seven range payloads: stored bytes equal joined UTF-8 lines plus one emitted terminal newline; this is consistent and includes context overlap. The reproducible arm returned 9,028 source-text bytes and reread 9,028 internally for hash checking. File bytes, displayed payload, shell stdout, repeated I/O and inferred attention are different quantities; stdout totals and billing remain unknown.

**The participant did not execute reproduce.py.** Its ledger records reading the code, then reading complete documents and using its own source-hash check. final.md explicitly confirms nonexecution. The script extraction checks in design-audit.md were performed by the reviewer and cannot be attributed to that participant or treated as an experimental benefit. The arm tests availability of a richer package, not actual use of its supplied extraction workflow. No treatment-compliance failure is fabricated: visible prompts made code an aid, not a required execution step.

The first end-of-invocation clock check was missed/delayed in all arms; reported budgets nevertheless remain far below 20 calls and 720 seconds. Three verifier sessions wrote timestamp-only helpers under /tmp before reading the visible directory restriction. They disclose it, with no evidence of forbidden research exposure. Official CLI administration was outside timing. These deviations should remain in the aggregate, not be erased. Sample-era exposure sentences (“no unsampled judgments yet”) were mechanically retained in some final measurements; read them as stage-specific history, not a claim that final coverage is incomplete.

## Acceptance judgment

Live #22 requires: comparable baseline/hidden labels/fixed errors; author-plus-verifier costs including false positives, omissions and repeated labor; explicit sampling limits/executed status/unknown billing; source-located facts and independent review.

The bounded pilot provides a real redo baseline, comparable answer set, correct labels and denominators, observed verifier times, error outcomes, repetition proxies and explicit uncertainty. Unknown bills are allowed by the task and are correctly null. It is suitable to preserve as a **reviewed partial pilot**, with the negative observed full-verification timing result and no general savings assertion.

It does **not** fully satisfy the original author-plus-verifier cost criterion as a complete comparison. The 171.807927-second author measurement excludes unknown preliminary selection/exploration; per-format author reasoning/setup is unallocated and unknown. This is useful measured preparation evidence, but not a measured total or exact per-format total-cost comparison. Adding all measured author time to each arm produces a shared preparation allocation excluding earlier work, not actual arm costs. Review/admin/coordinator costs are also not fully observed. Moreover, supplied extraction execution was not exercised, limiting interpretation of the third delivery condition.

Therefore retain #22 as partial/in_progress (or another honestly incomplete state chosen by its coordinator), and do not issue a passing full-task review or acceptance solely because the artifact is transparently limited. Preserve the artifact and publish only within an explicitly authorized partial/unaccepted channel. Formal acceptance would require either new, prospectively measured preparation/workflow evidence or an explicitly authorized narrowing of the task acceptance scope; do not silently redefine the original criterion after observing results. No rerun solely to improve performance is recommended. A future version can test a preregistered narrower question and record all preparation from its actual beginning.

This conclusion applies P2/P5/P6 and A1: correct results and transparent unknowns are useful, but do not turn missing cost evidence or same-operator participation into stronger claims. No credential, credit, governance or automation change is authorized by this review.

Result-audit end observation: **2026-10-13T02:28:34Z**, or **125 seconds** after recorded result-review start, including initial report writing. This closing timing note and later coordination are outside that measured interval. Initial design audit (97 seconds through initial prose writing plus unknown bootstrap) is separately recorded, not folded into performer cost. No supplied extraction script was executed during the result audit; its sole reviewer execution occurred during the design audit after source inspection.
