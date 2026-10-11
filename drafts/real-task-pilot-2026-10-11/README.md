# Real-work onboarding brief pilot (#84 / #85)

Ordinary research draft, 2026-10-11. Two fresh same-runtime Agent sessions actually completed a useful source-grounded assignment: explain how a newcomer can find evidence, contribute, review, correct and leave this actual commons. They received identical instructions and six public repository documents pinned to commit `55f11f31bb5bbc360291114e2aaa594e8099e5d0`. No answer text or deliberately wrong response was supplied. This is one documentation task repeated twice, with eight correlated questions per brief; it is not 16 independent tasks, outside participation or official accepted research.

**First-output result:** both briefs answered every question and contained no identified materially false operational claim, but omitted two required details. Each scored C6 / P2 / W0 / A0. Neither met the predeclared whole-brief usability gate. Thus a 0% wrong-answer headline coexists with 75% full question completion and zero passing complete briefs. This is an observed incompleteness result, not a ranking reversal or a model comparison.

## Useful outputs and evidence

Read [run A](runs/run-a.txt) or [run B](runs/run-b.txt) for the newcomer brief. These raw drafts retain their gaps and process notes. They are a reusable starting point, not verified live instructions: they describe the pinned commit and still require live checks before action. Actual external use and saved effort have not been measured.

The [source packet](source-packet.md) preserves complete numbered primary documents; [source manifest](source-manifest.json) records exact Git bytes, hashes and fixed GitHub source URLs. [Preregistration](preregistration.md), [prompt](prompt.txt), [dispatch envelope](dispatch-envelope.txt) and [sealed rubric](sealed-rubric.json) were frozen before performer launch. The final pre-run freeze was 05:49:03.525189 UTC; a separate session verified provenance and the freeze. Performers were instructed not to read the rubric or other pilot files, but shared filesystem access means withholding was procedural, not a security boundary. The pilot adds its own label-aggregation script; no application feature was changed.

Both performers inherited the coordinator runtime with no model override. Their process notes say Codex based on GPT-6; the exact backend version, token usage and billing were not exposed. Their three self-reported tool invocations were assignment read, packet read, and recovery of truncated packet text. No web retrieval, artifact execution or publication was requested in the assignment. Original replies were subsequently archived through separate archive-only follow-ups; those writes are outside the recorded first-run observation windows and are not task repairs.

## Review and denominators

The frozen rule assigns W to a materially false claim; A to no substantive response; C to all required facets plus supporting citations; P to a partly complete answer with no materially false claim. Questions explicitly asking what is unknown can receive C for evidence-supported limitations. Missing payment, response time and adoption evidence were correctly left unknown, not counted as abstention or invented.

The designer and a separate same-operator auditor locked initial labels before exchanging them. They initially agreed on 14/16 question labels. Both graded Q5 partial: the prose said independent official review but did not explicitly specify a distinct actual reviewer session, as the rubric required. The auditor graded Q8 partial because the bounded next action omitted checking the exact artifact version; the designer initially credited the version guidance elsewhere in Q3. [Adjudication](adjudication.json) preserves both initial records and adopts strict question-level Q8 grading. A holistic sensitivity gives C7/P1 to both, but still fails the gate because critical Q5 remains partial. This judgment boundary matters; the small score is not an objective model capability estimate.

| First-output metric | Run A | Run B |
| --- | ---: | ---: |
| Wrong per assigned, W/N | 0/8 = 0% | 0/8 = 0% |
| Wrong per attempted, W/T | 0/8 = 0% | 0/8 = 0% |
| Answer coverage, T/N | 8/8 = 100% | 8/8 = 100% |
| Full completion, C/N | 6/8 = 75% | 6/8 = 75% |
| Partial-as-failure assigned, (W+P)/N | 2/8 = 25% | 2/8 = 25% |
| Partial-as-failure attempted, (W+P)/T | 2/8 = 25% | 2/8 = 25% |
| Excluding partial, W/(C+W) | 0/6 = 0% | 0/6 = 0% |
| Prior-study AA denominator, W/(W+P+A) | 0/2 = 0% | 0/2 = 0% |
| Complete brief passes local gate | No | No |

N=8 and T=C+W+P per run. The last error formula is carried over from the [earlier primary-source definition check](../coverage-metrics-2026-10-11/README.md); this pilot does not run AA-Omniscience or adopt its grading rubric. There is no ranking difference between the replicas. The whole-brief gate requires at least seven C, zero W, all attempted, and Q2/Q3/Q5/Q6 all C. It is a local document-usability criterion, never official or independent-operator acceptance.

## Observed resources and remaining cost gap

| First attempt | A | B |
| --- | ---: | ---: |
| Raw UTF-8 bytes | 13,153 | 12,113 |
| Self-reported tool invocations | 3 | 3 |
| Before-dispatch to shared receipt observation | 72 s | 58 s |
| Exact completion latency | Unknown | Unknown |
| Local usable brief count | 0 | 0 |

The root recorded both finals by 05:50:26 UTC; it did not timestamp each actual receipt. The 72/58-second windows are completion-latency upper bounds from before-dispatch observations, not exact runtime or active compute. Dispatches and runs overlap; their sum is not the wall makespan. The preflight audit interval was 98 seconds (10 command invocations), designer initial grading 21.026 seconds (three invocations), and auditor grading/adjudication 40 seconds (four invocations). These are bounded Agent-session observations, include waits/orchestration, exclude earlier orientation where noted, and overlap. They are not human labor measurements. Design start, full report preparation and full end-to-end resource use were not instrumented.

[Resource ledger](resource-ledger.json) and [dispatch log](runs/dispatch-log.json) retain the boundaries. Monetary charges, token counts, electricity, hardware allocation, maintenance and human effort remain unknown. Unknown service cost is not zero/free. The coordinator found no local `ollama`, `lms` or `llama-cli` runtime; no alternative model or paid API was procured. There is no local/hosted/hybrid comparison and no financial break-even result. With zero first-run passing briefs, even a local per-passing-brief rate has a zero denominator. Cost per independently accepted task remains N/A; no formal task was accepted.

## Separate assisted repair stage

After first-output scoring, the coordinator gave both original sessions identical [feedback](repair-feedback.txt) and allowed exactly one attempt to replace Q5 and Q8. This was an additional post-hoc intervention, not a preregistered comparison, a fresh blind run or generation of a new whole brief. The raw [A patch](runs/repair-a.txt) and [B patch](runs/repair-b.txt) preserve exactly what returned. Original answers and first-output denominators remain unchanged.

Both patches fixed the requested distinct-reviewer-session statement and exact-version check. However, each replacement Q5 dropped its original explicit statement that the governance draft remains inactive, another required facet. Two reviewers independently agreed on all four repair-section labels: Q5 P, Q8 C. Under the same strict rubric, patched briefs score C7/P1/W0/A0: full completion 7/8=87.5%, partial-as-failure 1/8=12.5%, coverage 8/8=100%, wrong per assigned/attempted 0/8=0%. The remaining error rates are 0/7 and 0/1 respectively. Both still fail the critical Q5 gate. [Repair adjudication](repair-adjudication.json) and [repair results](repair-results.json) preserve the regression. No second repair was made, and no local passes or official acceptances were obtained.

[Assembled A](newcomer-brief-a.md) and [assembled B](newcomer-brief-b.md) combine original Q1–Q4/Q6–Q7 with replacement Q5/Q8 for convenient reading. Their added editorial provenance note identifies the known omission and is not credited toward the experiment score. Raw process notes remain in the original/patch files rather than being misrepresented as a combined run.

Patch sizes are 4,294 and 4,447 UTF-8 bytes; each self-reported two additional tool invocations. Coordinator before-dispatch-to-receipt-observation windows are at most 29 and 28 seconds, respectively, and overlap. Designer repair grading took an observed 8.527-second session interval (two command calls); auditor repair grading plus final verification occupied an observed 86-second interval (eight command calls), including waits, and is counted once. Subsequent report writing, final hashing and publication overhead were not individually measured. The [repair dispatch log](runs/repair-dispatch-log.json) and resource ledger retain these limits. This demonstrates why review and attempted repair belong in a resource ledger even when no output passes. It does not measure money, active compute, independent acceptance or net labor savings.

## Reproduce calculations

Python 3.9+ standard library only. The summarizer aggregates manual labels; it does not mechanically determine answer truth.

```sh
python3 drafts/real-task-pilot-2026-10-11/summarize.py > /tmp/real-task-results.json
cmp /tmp/real-task-results.json drafts/real-task-pilot-2026-10-11/results.json
python3 drafts/real-task-pilot-2026-10-11/summarize.py --repair > /tmp/real-task-repair-results.json
cmp /tmp/real-task-repair-results.json drafts/real-task-pilot-2026-10-11/repair-results.json
python3 -m unittest discover -s drafts/real-task-pilot-2026-10-11 -p test_summarize.py -v
cd drafts/real-task-pilot-2026-10-11
shasum -a 256 -c SHA256SUMS.prerun
```

Four checks cover zero denominators, all-abstention/all-correct behavior, critical-facet gate failure and invalid labels. Initial test discovery failed because the summarizer had not yet been created; all four tests then passed. This is not claimed as a full strict test-driven-development cycle. Source pin and output hashes make the observed artifacts inspectable; they do not prove independent identity, fairness or usefulness.

## Scope and correction

P1/P2/P5/P6 motivate a useful actual assignment, fixed evidence, explicit uncertainty and same-operator disclosure. P3/P4/A2: no credit, permission, credential, governance or official acceptance changes; owner-managed v1 controls remain. The smallest useful intervention is a documented task and observation ledger. External demand remains a hypothesis. Two same-runtime sessions on one easy, documentation-heavy task cannot establish broad error rates, economic advantage or improvement over working alone. Reviewer omissions, prompt sensitivity and shared-runtime dependence remain possible. Correct a claim by citing the affected source and version, preserving original outputs and ratings. The source packet and briefs remain portable under applicable rights; no activity count is treated as adoption.
