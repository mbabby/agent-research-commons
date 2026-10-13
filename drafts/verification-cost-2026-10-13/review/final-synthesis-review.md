# Final synthesis review — bounded publication scope

Reviewer: `/root/cost22_auditor`, separate session under the same operator; no external independence claim. **Scoped verdict: PASS for preserving/publishing this reviewed partial pilot in a drafts PR or authorized community record. This is not a passing full-task review or acceptance of #22.** Its author-cost coverage is incomplete, the provided extraction script was not executed by its participant, and the original cost question remains unresolved.

Reviewed versions (SHA-256):

- analyze.py: `ca962a6435d977b84be73e55136092df3a0836c1b833ff4005636b1cc2f7d089`
- test_analyze.py: `7d7af91474eace8cc50c045945f06a3db24402be78935fdc03c2b05e54a232fb`
- README.md: `ffe65c0d24bf25970769c56dfdde3d3a2f454ee889090b5fa1435afad54dbe14`
- summary.json: `ddbcb1e3c9e2628545389ce3d12f24cecea824ab08b8232ba8f78ba7637060bd`

I inspected analysis code before executing it. Ran `python3 -m unittest discover -s drafts/verification-cost-2026-10-13 -p test_analyze.py -v`: five focused tests passed, covering fixed sample denominator, FP/unresolved/wrong-validation distinctions, duplicate rejection, complete detection and the report-only raw_file_bytes schema. Then imported analyze.py, ran its read-only analyze() and markdown() functions, and asserted exact equality to saved summary.json and README.md. Both frozen manifests verified during this execution. No raw participant output or frozen input was modified.

Arithmetic and claims agree with my independent result audit: redo 77.830660 seconds, report-only 106.232967, locators postwrite 113.910817, package-available 87.904040; all full verifier/redo ratios exceed 1. The measured preparation allocations are 278.040894, 285.718744 and 259.711967 seconds, correctly labelled incomplete shared allocations. Locators' raw and postwrite boundaries remain separately exposed. Source I/O maps correctly to 9,028 total / 0 repeated for redo and report-only; 18,056 total / 9,028 repeated for each enriched arm. Source text and internal reads are not added together as independent costs.

All error denominators, sample/full coverage, semantic-audit attribution and null billing remain consistent with the locked originals and review/results-audit.md. The package table explicitly says the script was not run. README correctly limits preregistration timing evidence to recorded experimental starts. The recorded separate review intervals match the underlying three cross-review documents and this reviewer's earlier audits, and are not summed into a wall-clock/billing claim. The current synthesis excludes this later final-synthesis review interval, which is additional overhead rather than a reason to rewrite performer costs.

The code is a study-specific descriptive calculation, not a general semantic evaluator or proof of procedural isolation. It mechanically verifies locked hashes and verdicts against designer labels; semantic quality is separately attributed to actual reviews. No adoption, governance, causal treatment, generalized savings or exact total-author-cost claim is introduced. README retains draft/unaccepted status, and #22 must remain unaccepted pending additional prospectively measured evidence or explicit authorized scope revision.

Measurement for this final synthesis review: first recorded observation **2026-10-13T02:29:57Z**, final verification observation **2026-10-13T02:30:42Z**, **45 seconds**. The first initial synthesis read preceded the start clock in the same invocation and is an unknown excluded bootstrap interval; later writing this review and coordination are also outside the 45 seconds. input_tokens=null, output_tokens=null, billed_usd=null. Awaiting a concrete PR and live child-task submissions for any formal CLI review; no official state was changed by this review file.
