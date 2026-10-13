# Crossreview: redo and locators

Reviewer: the report_only participant, now in a separate post-lock review phase; same operator, not independent operator evidence. Assigned scope: redo and locators sample/full answers, source support, schema, cooperative read ledger, event hashes, timing, and denominators. No raw run files changed, no publication, no reruns.

Review start: 2026-10-13T02:51:53Z (first review tool clock, seconds precision).
Review end: 2026-10-13T02:53:13.262497+00:00 (final report-writing clock).
These are review overhead boundaries, separate from participant trial timings. The first broad read exceeded the output limit; a focused subsequent read recovered every answer and all ledger data required below. This affected review only.

## Findings

No answer, evidence, assessment, schema, or frozen-artifact hash discrepancies found in the assigned scope. Every q01–q12 semantic answer in both full outputs matches the essential distinctions in the hidden answer key and pinned sources; all four sample answers match as well. Additional detail in redo (closed historical questions, intent expiry, review evidence requirements, accessibility caveats) is source-supported. Each cited quote occurs verbatim within its specified 1-based line span. Every evidence obligation supports its answer, including redo q06's distinction between an unavailable offline activity snapshot and an empty discussion.

| Arm | Stage | Answer correct | Evidence correct | Joint correct | Seeded errors corrected | False contradictions |
|---|---|---:|---:|---:|---:|---:|
| redo | sample | 4/4 | 4/4 | 4/4 | 1/1 checked; 1/4 report-wide | N/A |
| redo | full | 12/12 | 12/12 | 12/12 | 4/4 | N/A |
| locators | sample | 4/4 | 4/4 | 4/4 | 1/1 checked; 1/4 report-wide | 0/3 supported candidates |
| locators | full | 12/12 | 12/12 | 12/12 | 4/4 | 0/8 supported candidates |

The fixed sample is exactly q01,q03,q07,q10 and includes only seeded error q03. Full outputs cover exactly q01–q12; seeded errors are q03,q06,q09,q12. Sample 1/1 checked-error recall is not 4/4 report-wide coverage; it is 1/4 (25%) coverage. Redo has null assessments as permitted; its substantive corrected answers satisfy error correction, without pretending it classified an unseen report. All uncertainty fields are 'none'; no unsupported substantive gaps were identified.

Schema equality passes: top-level only answers; each item exactly id, answer, evidence, uncertainty, assessment; evidence exactly path, start_line, end_line, quote with nonempty quotations and valid spans. Both arms share identical output obligations, while redo assessment=null is the expressly permitted exception. Multiple evidence spans in redo q01 do not violate equality. Sample entries remain identical in their respective full outputs.

## Measured timing and reads

| Arm | Start→sample seconds | Start→full seconds | Reported outer calls | Logged file reads | Logged read bytes | Corpus reads | Corpus bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| redo | 42.506010 | 72.051039 | 7 | 11 | 77534 | 6 | 64143 |
| locators | 30.099722 | 55.501747 | 5 | 7 | 33704 | 2 | 21381 |

Durations are CLOCK_MONOTONIC end/checkpoint minus each arm's own start, not differences between arm dispatch times. Full durations are cumulative and include sample work. Read byte totals count file_read events only, including repeated reads, and exclude checkpoint/end artifact reads. Corpus-only counts cover the two pinned docs. Both meet the 20-call/12-minute limits on disclosed calls and observed durations. Calls are coordinator-recorded performer disclosures, not independently recountable from the helper ledger; this review did not access full participant transcripts. Do not infer tool counts from event counts. These descriptive reader durations do not establish total author-plus-reader savings; this review did not audit preparation allocations.

## Exposure and integrity

Redo's 11 file_read events contain only its prompt, common helper/questions/corpus metadata, the two source documents (three reads each), and its own sample. There are zero logged reads of candidate.json, any report, locators, other arms, hidden keys, or prior results. Its supplied prompt path is expected and is not report exposure. This supports zero candidate exposure in the cooperative ledger only; it cannot prove absence of unlogged reads. The shared disclosure reports no unlogged reads/deviations; no OS trace is available. Post-lock reviewer access to hidden keys is outside trial time.

All six assigned raw files (sample/full/events for redo and locators) match RUNS-LOCK.json SHA256 values. Every assigned checkpoint/end artifact byte count and hash matches the current frozen artifact. Every file_read event's recorded byte count and hash matches its referenced file, including pinned source bytes. Event chronology has one start, one sample checkpoint, and one full end per arm, in that order. No post-end answer revisions were performed in this review.

Limitations: same-operator review; cooperative logs and self-reported outer calls; one run per arm; nonrandom sample; no token/billing telemetry; no claim of outside adoption or generalizable causal effect. Preparation costs, other two arm outputs, and external GitHub state are outside this assigned crosscheck.
