# Post-lock review of reproducible arm

Reviewer: cost22-locators, a separate session under the same operator, previously performer of the source-locators arm. Review began after explicit lock/reveal authorization. This is not independent external review. Only this review file was written; raw outputs were unchanged.

## Evidence and correctness

Inspected reproducible sample.json, final.json, final.md, reproduce.py, extraction-data.json, both pinned source documents, hidden reference labels and RESULTS-LOCK.json. All four reproducible output files match the lock hashes. The four sample claim records are exactly unchanged in the full result. Corpus SHA-256 digests match the hashes recorded in final.json.

The four sample verdicts match reference labels (two contradicted, two supported). All twelve full verdicts match reference labels: C03, C06, C10 and C12 contradicted, the other eight supported; no unresolved claims. No semantic error or false correction found. Source line references directly support the answers. C03 properly separates closing from withdrawal and successful refresh; C06 corrects both 500 to 100 and ascending to descending; C10 rejects technical evidence as proof of benefit and grounds its additional external-outcome criterion in agent-value.md lines 37–39; C12 preserves owner control. C10's additional wording is supported rather than an invented requirement.

## Script and byte accounting

The reproduction script was inspected but, as final.md explicitly discloses, was not executed during the measured arm. The participant instead read both complete source documents and used a later internal reread for hash verification. Consequently this run measures availability/inspection of the reproducibility aid, not its execution benefit. It should not support a causal claim that running reproduction code saves verification work.

The recorded 4,634 + 4,394 = 9,028 distinct source bytes are consistent with actual files. One additional hash-only reread gives 9,028 repeated bytes, for 18,056 cumulative internal filesystem source bytes. Only 9,028 source-content bytes were reportedly returned as source text. Do not add that visible subset to the filesystem total. The field internal_source_read_bytes=9028 means the hash-only, non-visible pass here; its name is ambiguous if treated as all internal reads. This is an interpretation/labeling caveat, not evidence of an arithmetic error. Exact formatted stdout bytes remain unknown because line-number and wrapper formatting are separate from source bytes.

Static inspection of reproduce.py shows a hash-validation read of each source, then a full-file read for each of twelve extraction rows. If it were run once as written, source reads would total 63,676 bytes (9,028 initial bytes plus 54,648 per-record bytes). That is a hypothetical property of the inspected script, not observed participant work; it must not be charged to this arm. No script execution was performed in this review either.

## Timing and ledger

Recorded sample elapsed is 50.71256685256958 seconds; cumulative full elapsed is 87.90403985977173 seconds. Subtraction yields exactly the recorded full-stage increment, 37.19147300720215 seconds. UTC timestamp differences agree within displayed rounding. Sample after-write clock is 50.71292996406555, about 0.000363 seconds later than its primary timestamp. Comparing sample/full write-boundaries therefore has this small inconsistency, not a material 37-second arithmetic issue.

Six invocations are enumerated. The final ledger says its validated intermediate final.json was 14,811 bytes, whereas the frozen final is 15,770 bytes; subsequent persistence of final timing fields can explain this, but the intermediate bytes cannot now be independently recovered from the frozen files. The stated final boundary excludes final timing-field persistence latency. Source-read accounting is reconstructable from the ledger and file sizes; actual tool timing, stdout sizes, exact command transcripts and absence of extra reads cannot be independently established from these artifacts alone.

## Limitations and disposition

Accept semantic correctness and correction quality for the pinned corpus. Preserve timing/byte accounting caveats in any synthesis. All sources were visible before sample completion, so the later full stage benefits from earlier exposure and is paired rather than independent. Unknown preparation time, tokens, dollars and model telemetry remain null. The recorded /tmp timestamp exception and missing separate first-invocation elapsed check are procedural deviations already disclosed. One same-operator run per condition cannot establish general savings or external adoption.

Review interval: 2026-10-13T02:26:49.113003+00:00 to 2026-10-13T02:27:43.279623+00:00; 54.166620 elapsed seconds, including review reads and reasoning and excluding this final file write/response. Four review tool invocations including this write.
