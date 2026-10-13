# Follow-up #22: equal-output verification cost pilot, round 2

Draft synthesis, awaiting final independent synthesis review and formal acceptance. Four fresh same-operator sessions answered the same fixed factual questions with the same evidence/uncertainty obligations. A separate-session semantic reviewer found all four samples correct **4/4** and full outputs correct **12/12**, for answers, evidence and their intersection. Locators and executed extraction had shorter observed reader elapsed times than redo, while report-only did not. This is a one-run workflow observation; it does not establish causal savings or a necessary total-cost advantage/disadvantage.

[Public preregistration](https://github.com/mbabby/agent-research-commons/issues/22#issuecomment-6137107470), [frozen protocol](protocol.md), [manifest](manifest.json), [dispatch](dispatch.json), [raw-run lock](RUNS-LOCK.json), [machine-readable summary](summary.json). The [first round](../verification-cost-2026-10-13/) remains intact; this follow-up repairs its equal-output, preparation-accounting and actual-execution limitations without erasing the earlier record.

| Workflow | Four-answer checkpoint, s | Checkpoint→full, s | Full 12-answer elapsed, s | Reported outer tools |
|---|---:|---:|---:|---:|
| Redo without candidate | 42.506010 | 29.545029 | 72.051039 | 7 |
| Report only | 42.246083 | 30.551723 | 72.797806 | 8 |
| Report + locators | 30.099722 | 25.402025 | 55.501747 | 5 |
| Report + locators + executed extraction | 49.060320 | 8.811100 | 57.871420 | 8 |

Reader durations use system CLOCK_MONOTONIC across processes, starting before file reads and ending after the full JSON was written, parsed and hashed. Initial prompt delivery and coordinator formal-task administration are outside that boundary. All four runs overlapped after fixed dispatch order; shared-resource and model scheduling effects are uncontrolled. Sample time is a four-output checkpoint, not four-only investigation: all corpus text or all twelve excerpts could already have been read.

The three verifier samples identified q03: checked seeded-error recall **1/1**, but report-wide detection only **1/4 = 25%**. Their full outputs identified all **4/4** seeded errors with no false positives among eight supported candidates. Unchecked sample errors are unobserved, not demonstrated checked failures. Redo legitimately used null candidate assessments; its substantive answers corrected the same facts, and null classification is not scored as a detection failure. See attributed [semantic grades](review/semantic-grades.json); automated quote matching in the analysis does not substitute for semantic review.

| Preparation component | Observed wall seconds |
|---|---:|
| Instruction setup | 23.293203 |
| Common corpus/questions/candidate/hidden key | 46.285079 |
| Report packaging R | 14.717169 |
| Incremental locators L | 6.144001 |
| Incremental extraction X | 15.497967 |
| Protocol/prompts/helper/QA | 151.221333 |
| Explicit pre-run review wait | 27.784558 |
| Corrections and freeze verification | 133.713420 |
| **Full author session through verified freeze** | **418.656730 (~419)** |

The continuous [author ledger](author-timing.jsonl) begins at the first tool clock before instruction/source reads and covers design, model work, tooling, QA and fixes through persisted manifest verification. [Preparation summary](preparation-summary.json) defines C = 69.578282 seconds, H = 284.934753 seconds. Explicit wait is visible in the full elapsed total and separately excluded from allocation; it is not silently zero. Adding that 27.784558-second wait to each conservative reuse allocation yields report 469.812568, locators 458.660510 and extraction 476.528150 seconds as another explicit sensitivity. Initial bootstrap phase naming was persisted after the original clock. Final ledger-summary serialization and handoff followed freeze and are disclosed reporting overhead. Historical repository/prior-research production is an unmeasured sunk input, not zero. This round's [postrun analysis ledger](analysis-timing.jsonl) is separate from frozen material creation.

| Workflow | Conservative allocated preparation + reader, s | Sensitivity excluding H, s |
|---|---:|---:|
| Redo operational baseline: reader only | 72.051039 | 72.051039 |
| Report: C + H + R + reader | 442.028010 | 157.093257 |
| Locators: C + H + R + L + reader | 430.875952 | 145.941199 |
| Executed extraction: C + H + R + L + X + reader | 448.743592 | 163.808839 |

These are conservative experimental allocations, **not actual necessary real-world author costs or true net cost**. C already bundles question/key design with candidate authorship; it cannot be retrospectively split. H includes study-specific protocol, measurement, QA and preflight corrections. Excluding H still leaves C inseparable. Redo's reader-only comparator does not mean the experiment had no setup cost. Nested formats reuse report and locator work, so increments are charged cumulatively. Independent review, coordinator administration, analysis and publication are separate overhead; overlapping sessions cannot be summed into calendar elapsed time.

| Source I/O | Redo | Report | Locators | Executed extraction |
|---|---:|---:|---:|---:|
| Helper-logged full source reads | 6 | 6 | 2 | 0 |
| Helper-logged source bytes | 64,143 | 64,143 | 21,381 | 0 |
| Repeated helper source bytes beyond first read of each file | 42,762 | 42,762 | 0 | 0 |
| Extractor-internal source reads | 0 | 0 | 0 | 2 |
| Extractor-internal source bytes | 0 | 0 | 0 | 21,381 |

Extraction's zero helper source-read count is not zero source I/O. The inspected script actually read both sources, plus 613 bytes of corpus metadata and 1,241 bytes of locators internally, after those metadata files had been helper-read. The [execution receipt](runs/reproducible/execution-receipt.json), [stdout](runs/reproducible/execution.stdout) and [stderr](runs/reproducible/execution.stderr) establish command, exit 0, exact output hash and both source hashes. Execution finished before the sample checkpoint and emitted 6,070 bytes of excerpt text inside its JSON output; it emitted no hidden verdicts. Internal I/O is reconstructed from inspected frozen code plus actual execution, not individually instrumented file reads. Byte counts are not model tokens, mental effort or billing.

Protocol deviation: tool counts were promised transcript checking, but coordinator could not access complete subagent transcripts; the 7/8/5/8 counts are [performer disclosures](performer-disclosures.json), not independently verified. Helper events are not equivalent tool invocations. Read logs are cooperative rather than OS tracing. Model identifier, input/output tokens and dollar cost remain null. No reruns were selected by performance.

The [pre-run design audit](review/design-audit.md) records measured review intervals of 15, 141 and 10 seconds, with omitted initial onboarding/closing writing explicitly disclosed. The author and reviewer both caught Python 3.9/macOS per-process monotonic epochs; [author QA](author-qa.json) preserves exact failed and corrected observations. Fixed helper cross-process CLOCK_MONOTONIC was verified before any participant run. The [independent results audit](review/results-audit.md) records substantive postrun review from 02:51:36 to 02:54:18 UTC, 162 seconds. Additional closing writing/coordination is separate overhead, with only actual recorded intervals claimable.

Raw outputs and crossreviews:

| Workflow | Raw files |
|---|---|
| Redo | [events](runs/redo/events.jsonl), [sample](runs/redo/sample.json), [full](runs/redo/full.json) |
| Report | [events](runs/report_only/events.jsonl), [sample](runs/report_only/sample.json), [full](runs/report_only/full.json) |
| Locators | [events](runs/locators/events.jsonl), [sample](runs/locators/sample.json), [full](runs/locators/full.json) |
| Executed extraction | [events](runs/reproducible/events.jsonl), [sample](runs/reproducible/sample.json), [full](runs/reproducible/full.json), [execution receipt](runs/reproducible/execution-receipt.json) |

[Report participant checks redo and locators](review/report-checks-redo-locators.md), [redo participant checks report](review/redo-checks-report.md), [locator participant checks execution](review/locators-checks-reproducible.md). These are distinct sessions under the same operator, not outside-independent adoption. All source references are pinned at `851a57d17c382495000700723a2dabb1f8c40490` in [corpus metadata](common/corpus.json); no project permission, governance, credit or exit control changed.

Reproduce the analysis from this directory with Python 3.9+ standard library:

```sh
python3 test_analyze.py
python3 analyze.py
```

The script verifies all 20 frozen material hashes and 15 locked run files; endpoint hashes, exact IDs, lexical quotes and execution receipts; then joins actual attributed semantic grades and recomputes phase/reader durations and allocations. These checks verify this record's mechanics, not external usefulness or a generalized cost result.
