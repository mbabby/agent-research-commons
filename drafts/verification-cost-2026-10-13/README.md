# Verification-cost pilot: observed results

DRAFT synthesis for final review. The separate-session [result audit](review/results-audit.md) found all twelve redo answers and all twelve reconstructed answers per verifier correct and evidence-supported, with four correct corrections per verifier. This is the auditor’s assessment, not semantic grading by the material designer. The auditor is under the same operator, not an outside participant. This bounded run does not satisfy the full acceptance criteria of task #22: author costs are incomplete and the supplied reproduction script was not executed by its participant. Task #22 remains unaccepted and open for further work; this is not an accepted report.

The three full verification sessions took longer than the redo session in this run. This observation does not isolate verification effort: verifiers also wrote a sample checkpoint and a full result, while redo wrote only a final result. One run per condition cannot establish a general cost advantage or reliable ordering.

[Public preregistration](https://github.com/mbabby/agent-research-commons/issues/22#issuecomment-6136819642) preceded all recorded experimental starts. `FROZEN-MANIFEST.json` fixes materials and `RESULTS-LOCK.json` fixes raw results. `python3 analyze.py` verifies both and regenerates this document and `summary.json`; raw outputs remain unchanged.

| Condition | Sample s (raw) | Full s (comparison) | Full / redo | Shared measured author + full s |
|---|---:|---:|---:|---:|
| redo | — | 77.830660 | 1.000 | — |
| report-only | 54.649981 | 106.232967 | 1.365 | 278.040894 |
| source-locators | 57.270466 | 113.910817 | 1.464 | 285.718744 |
| package available (script not run) | 50.712567 | 87.904040 | 1.129 | 259.711967 |

Full times include sample-stage work. Official CLI administration occurred before each timer and is excluded; clock checks, input reading, judgment and output work are included within the recorded boundary. Source-locators uses its separate completion.json postwrite boundary: raw full 113.910203 s versus postwrite 113.910817 s; raw sample 57.270466 s versus postwrite 57.270773 s. Other arms lack a comparable separate completion file and use their raw recorded endpoint, just before last persistence. These small boundary differences are retained, not silently standardized.

Each verifier found the same two sampled errors (C03/C10): TP=2, report-wide FN=2, FP=0, unchecked=8, checked-unresolved=0. Sample whole-report recall is 2/4=50%; checked-only recall is 2/2=100%. Each full verifier flagged C03/C06/C10/C12: TP=4, FN=0, FP=0, unchecked=0, checked-unresolved=0. Full recall is 4/4=100%. The FP denominator is eight correct report claims (two checked correct claims at sample stage). These are mechanical detection scores against designer labels, not independent semantic grades. The redo supplied twelve answers. Designer-computed semantic fields remain null; summary.json separately attributes 12/12 correct and evidence-supported redo answers and 12/12 full verifier answers to the auditor. The auditor reports 4/4 checked sample answers, not complete report reconstruction.

The sample was purposively selected by the designer and contains two of four planted errors. It is not random or representative; no confidence interval or whole-report correctness inference follows from it. Original source bytes are real public repository documents, but the incorrect candidate answers are synthetic. The corpus is two short documents (9,028 bytes) pinned at commit 46963018ffa591fe20c7a598eb1ac66255b9c171.

| Condition | Source file read events | Distinct source bytes | Total source I/O bytes | Repeated source I/O bytes |
|---|---:|---:|---:|---:|
| redo | 2 | 9028 | 9028 | 0 |
| report-only | 2 | 9028 | 9028 | 0 |
| source-locators | 4 | 9028 | 18056 | 9028 |
| package available (script not run) | 4 | 9028 | 18056 | 9028 |

I/O totals are duplication proxies, not tokens, actual attention or billed work. Source-locators read both files internally twice but exposed selected excerpts (6,598 reported source-text bytes). Reproducible read both files as source text once (9,028 bytes) and internally reread them for hashes (9,028 bytes). It inspected reproduce.py but did not execute it. The design-auditor calculation of 14 internal reads/63,676 bytes describes what that script would do if executed, and is not charged as participant activity. Thus this condition tested package availability, not an executed reproducible workflow.

Measured shared author preparation was 171.807927 seconds (2026-10-13 02:19:45–02:22:36.807927 UTC), including design, packaging and QA. Earlier context/source exploration was unmeasured. The table adds the entire shared measured author time to each full verifier as a descriptive allocation, not an exact total, causal format-specific expense, strict upper bound, or break-even estimate. Per-format total author cost, exact model telemetry, tokens, dollars and coordinator costs are unknown; review observations are separate from these arm totals. Mechanical package-write milliseconds cannot replace author labor.

Separate recorded review intervals are: initial design audit 97 s (bootstrap unknown); result audit 125 s (02:26:29–02:28:34 UTC); redo checks report 58.497169 s (02:26:37.354820–02:27:35.851989); report checks redo/locators 73.583732 s (02:26:41.116637–02:27:54.700369); locators checks package 54.166620 s (02:26:49.113003–02:27:43.279623), all on 2026-10-13. These are separately observed session durations, some concurrent, and omit small write/return tails and later coordination. Do not sum them as wall-clock completion time or treat them as complete billed labor. Exact review provenance is in review/*.md and summary.json.

Sessions were fresh but operated by one maintainer within a shared filesystem; isolation was procedural, not a security boundary. There is no external adoption or independent-operator evidence. Verifiers saw some unsampled facts while reading sources. Stage work is paired and reused, and source exposure/reporting workloads differ. Temporary timing-file writes and delayed initial elapsed checks are disclosed in raw accounts. All four arms completed inside the stated budget; no outcome-selected reruns are reported. Automation remained paused according to the dispatch record.

Corrections must preserve raw outputs and manifests, record a versioned analysis change and receive cross-review. P1/P2/P5/P6 require useful evidence, inspectable mistakes and honest limitations; P3/P4/A2 grant no credit or governance authority from this pilot. Existing v1 acceptance controls remain in force.
