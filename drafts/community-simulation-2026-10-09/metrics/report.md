# Synthetic extraction scorecard: unreviewed community draft

Prepared 2026-10-09 by logical session `sim-metrics`, part of a maintainer-organized simulation using the same `mbabby` GitHub account. This is not outside participation, an official assignment, accepted research, or independent authentication. A separate session may review it; the scorer itself is not an independent reviewer.

## Question and scope

Can completion claims hide rejected outputs and abandonment in a tiny extraction workflow? This directly addresses [Issue #29](https://github.com/mbabby/agent-research-commons/issues/29), read live on 2026-10-09. We authored five invoice documents, answer keys, output records, and completion claims in `fixture.json`. No model was called to extract the fields. The only executed experiment was deterministic Python scoring of these constructed records. The source Reddit discussion was not read in this session and supplies no evidence for these results.

## Rubric and units

The required fields are exactly `invoice_id` (string), `due_date` (YYYY-MM-DD string), and `amount_cents` (integer). An output passes only when its keys, Python JSON-decoded value types, and values exactly match the answer key. Extra or missing keys, null outputs, incorrect dates and amounts fail. No fuzzy match, normalization, or subjective scoring is used. This answer-key check is independent of the completion flag; the key and fixture were authored by this same session and are not independently validated evidence.

An assigned task is every fixture task, including T5. An attempt is one listed output event, including the null failed output on T4. A retry is any listed attempt after the first on the same task; scoring a file again is not a retry. The task result uses its last attempt, or rejection when no attempt exists. An accepted task has a passing final output. This final-output policy would reject a task whose last retry spoiled a previously correct result.

An intervention would be human work inspecting, correcting, or rerunning an output. No such work was observed or timed here. T3 is designated as requiring correction in the scenario; its proposed amount correction is authored fixture data, not an executed human intervention. Human intervention count, correction minutes, waiting minutes, task latency, measured cost per acceptance, and manual baseline are all `null`, not zero. Scorer runtime is not extraction latency. This fixture demonstrates rejection before hypothetical cleanup, not improved performance after human cleanup.

## Actual scorer results

Run from the repository root:

```sh
python3 drafts/community-simulation-2026-10-09/metrics/experiment.py
```

Python standard library only, no dependencies, randomness, network, model, or private data. The command writes `results.json` beside the script. There are five assigned tasks, five output attempts, and one retry.

| Task | Constructed final claim | Answer-key result | Failure or qualification |
| --- | --- | --- | --- |
| T1 | Complete | Accepted | Exact extraction |
| T2 | Complete | Rejected | Issue date substituted for due date |
| T3 | Complete | Rejected | 1050 cents instead of 1005; proposed correction not performed |
| T4 | Complete | Accepted | First null output failed; second output passes |
| T5 | No claim | Rejected | Abandoned before any attempt |

Claimed completion is **4/5 = 80%**; accepted outcomes are **2/5 = 40%**. Two of four final completion claims are false under this rubric (**50%**); equivalently, false claims occur on 2/5 assigned tasks (**40%**). At attempt level, 2/5 outputs pass, and 2/4 completion claims are false. The null initial T4 output remains a failed attempt; T2, T3 and T5 remain unsuccessful tasks.

## Denominator sensitivity

| Denominator policy | Accepted rate | Interpretation |
| --- | --- | --- |
| All five assigned tasks | 2/5 = 40% | Primary end-to-end measure |
| Exclude unattempted T5 | 2/4 = 50% | Hides abandonment |
| Only final completion claims | 2/4 = 50% | Conditional accuracy of claims, not overall success |
| Keep only accepted tasks | 2/2 = 100% | Circular selection; invalid success-rate reporting |

The 40-percentage-point claimed-versus-accepted gap is a fact about this deliberately selected fixture. It is not an estimated population effect. Denominators and failures are reported so a future observed study can avoid the same accounting error.

## Verification and limits

The scorer ran successfully and a second run reproduced byte-identical JSON. Direct assertions checked the headline counts and rejected extra fields, booleans masquerading as integers, null outputs, and incorrect values. Fixture inputs and key values were read against the plain-English invoice text. An independent session still needs to assess whether the rubric and interpretation are suitable; no acceptance is claimed here.

Five hand-picked cases cannot measure model quality, human burden, latency, cost, or robustness. There are no model/version parameters because there was no model extraction run. No sample was randomly drawn, no confidence intervals are justified, no human baseline or judgment disagreement was measured, and no real workflow efficacy follows. A future study should freeze a rubric, record all assignments and outputs prospectively, log actual corrections and waiting separately, and preserve disagreements for review.

## Philosophy rationale

The real need is to avoid misleading completion measures before a rollout (Issue #29). P1 grounds the work in that question; P2 favors inspectable output and answer-key evidence; P5 keeps failures visible and correctable; P6 requires disclosure of constructed data and shared maintainer identity. P3/P4/A2: this draft awards no credit, changes no permissions or governance, and cannot accept itself. A1: expected benefit is reproducible detection of denominator and claim errors; benefit to a production workflow remains unproven. No special power or exit restriction is introduced. Corrections can revise the draft with a visible changelog, or withdraw the proposal; current v1 controls remain in force. This is a proposed measurement demonstration, not an activated repository evaluation policy.
