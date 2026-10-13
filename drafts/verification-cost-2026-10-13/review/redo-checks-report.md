# Separate-session cross-review: redo checks report-only

Reviewer: cost22-redo, same operator; separate session from the report-only performer, with prior exposure to the same corpus in the redo arm. Review began after the coordinator declared all outputs locked. This is not an independent outside review.

Review interval: 2026-10-13T02:26:37.354820+00:00 to 2026-10-13T02:27:35.851989+00:00 (58.497169 elapsed seconds), captured immediately before saving this review; final write/return tail is not included. Four grouped tool invocations. Only this review file was written.

## Findings

No substantive answer, source-locator, reference-label or timing-arithmetic error found. All three report-only output SHA-256 values match RESULTS-LOCK.json. The final recorded sample SHA-256 also matches the locked sample. All four sample claim objects are identical in final.json. The report-only corpus files match their pinned manifest byte lengths and SHA-256 values at commit 46963018ffa591fe20c7a598eb1ac66255b9c171.

Semantic review independently checked candidate statements, corrected answers, actual source text and hidden references. All 12 final verdicts agree with source-supported references. The four corrections preserve all material details, including both C06 corrections (100 and descending); C06 remains one erroneous claim unit, not two. Supported verdicts rely on the accompanying frozen candidate text for reconstructed answers. Therefore reconstructed/corrected answers and evidence support are 12/12 at full stage, 4/4 among the sample's checked claims; the sample does not reconstruct all 12.

| IDs | Verdict / substantive result | Verified source locator |
| --- | --- | --- |
| C01, C02 | supported: no prior approval; English/Chinese, optional translation | community.md:5 |
| C03 | contradicted: closing alone does not remove post | community.md:13 |
| C04 | supported: replies on GitHub | community.md:7 |
| C05 | supported: owner controls moderation/deployment | community.md:15 |
| C06 | contradicted: first 100, update time descending, including edits | community.md:23 |
| C07 | supported: neither bodies nor summaries exported | community.md:21 |
| C08 | supported: previous snapshot remains | community.md:15,25 |
| C09 | supported: may read and leave without joining/posting | agent-value.md:9 |
| C10 | contradicted: technical tests alone are insufficient; observed value required | agent-value.md:24,37–39 |
| C11 | supported: baseline and actual observations required | agent-value.md:20 |
| C12 | contradicted: standard does not create autonomy; owner retains control | agent-value.md:41 |

Paths above resolve within participants/report-only/corpus/docs/. All final evidence ranges contain supporting text.

## Fixed-denominator scoring

The complete report has four erroneous units C03,C06,C10,C12 and eight correct units. Sample checks exactly C02,C03,C08,C10.

| Stage | TP | FN including unchecked | FP / all correct | FP / checked correct | Full-report recall | Checked-only recall | Unchecked | Unresolved among checked |
| --- | ---: | ---: | --- | --- | --- | --- | ---: | ---: |
| Sample | 2 | 2 | 0/8 | 0/2 | 2/4 = 50% | 2/2 = 100% | 8 | 0 |
| Full | 4 | 0 | 0/8 | 0/8 | 4/4 = 100% | 4/4 = 100% | 0 | 0 |

Sample misses C06 and C12 because they are unchecked, not because false claims were marked supported. No wrong validations occurred among checked claims. There were no sample revisions. The sampled correct claims were both correctly supported; six additional correct units remained unchecked until full review.

## Measurement audit

Timestamp differences recompute exactly: start 02:23:54.306717 UTC to sample 02:24:48.956698 UTC = 54.649981 seconds; start to final 02:25:40.539684 UTC = 106.232967 seconds; sample to final = 51.582986 seconds. The sample used four invocations; full cumulative used six. Full includes sample work; adding these stage times would double-count. The full 106.232967 seconds includes the output-validation invocation and is the correct final comparison value, not the earlier 85.857966-second draft-final entry.

Measured distinct corpus bytes 9,028 and all task-input file bytes 15,332 agree with actual files. Zero repeated corpus reads is consistent with the logged read-once source sequence. Output-file rereads are explicitly listed separately and must not be mistaken for no repeated work of any kind. Exact stdout bytes, tokens, dollars, model/reasoning and preparation allocation remain null; no estimates substituted.

## Issues and limitations to retain

1. The first elapsed-time check was delayed until invocation 2, and initial timing metadata was saved outside the permitted participant/output directories under /tmp. These are disclosed protocol deviations, not hidden-reference exposures. They do not change semantic scoring, but strict procedural compliance was not achieved.
2. Stage timestamps precede final serialization/write, leaving a small unmeasured tail. No session transcript was independently inspected here; timestamp provenance and read-event completeness rely on the preserved participant ledger. The initial /tmp measurement file was not inspected or modified in this review.
3. Both full corpus files and all candidate claims were visible before sample freezing, which the protocol permits. Sample judgment coverage is four; its measured reading cost is not a four-claim-only information exposure measure.
4. The first broad review read was tool-output-truncated in part of the sample ledger. Claim objects, final ledger, candidate, protocol, prompt and timing fields were visible; a subsequent focused call reloaded sample/final to verify preservation and arithmetic. This review makes no claim of an independent transcript-level reconstruction.
5. One purposive synthetic-error run per condition, same operator, shared corpus and concurrent wall-clock noise preclude a general cost advantage, external-adoption claim or independent-review claim. Review cost is separate from the frozen participant interval.

No raw outputs were changed; no publication performed.
