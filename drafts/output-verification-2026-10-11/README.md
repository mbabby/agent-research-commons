# Can format checks detect semantically wrong Agent output?

**Executed synthetic pilot, task #20, attempt 1; deliverable draft, not official acceptance.** As of 2026-10-11, the format-only checker passed all 12 cases and missed all nine injected defects. Both fresh Agent review sessions flagged all nine defects and passed all three clean controls. These are observations on this deliberately small, source-bounded dataset—not estimates of general accuracy or evidence that two agreeing Agents establish truth.

| Condition | TP / 9 defects | FN / 9 | FP / 3 controls | TN / 3 | Precision | Coverage |
|---|---:|---:|---:|---:|---:|---:|
| Format only | 0/9 | 9/9 | 0/3 | 3/3 | N/A (no flags) | 12/12 |
| Agent claim-by-claim source check | 9/9 | 0/9 | 0/3 | 3/3 | 9/9 | 12/12 |
| Independent-session Agent review | 9/9 | 0/9 | 0/3 | 3/3 | 9/9 | 12/12 |

All three conditions returned every case with no uncertain verdicts. Format sensitivity was 0/9; each semantic condition's sensitivity was 9/9. Specificity was 3/3 for each. For each defect class—numeric replacement, unsupported citation, required omission—the format checker detected 0/3 and each semantic review detected 3/3. With only three clean controls, zero observed false positives says little about false positives on other material. No significance test was preregistered or performed.

The separate audit session checked the findings against the fixed sources: each semantic reviewer identified the intended defect with supported reasoning in all nine flagged cases. That secondary supported-hit assessment is judgmental and independently audited, not an automated truth test. Full case outcomes and fixed defect explanations are in [the case table](results/case-table.md); unabridged reviewer findings are in [source-check.json](results/source-check.json) and [independent-review.json](results/independent-review.json). [scores.json](results/scores.json) preserves all counts, rates, denominators and findings.

## What was actually done

The user authorized a small public experiment and independent review. The assigned researcher started [task 20](https://github.com/mbabby/agent-research-commons/issues/20) through the repository CLI with logical role `verification-research`, attempt 1 and operation `verification-20-20261011-start`. The task's Reddit anecdote supplied problem motivation only; no real incident was reproduced, no Reddit user was contacted, and no outside participation is claimed.

The researcher hand-authored 12 English summaries of public project documents: three numerical alterations, three correct claims paired with citations that do not support them, three omissions of explicitly requested information, and three clean controls. Each case includes its request, required information and structured output with line-addressed citations. Missing information was assessed against those requested facets; arbitrary source details were not required. Citation-support failures are distinct from false claims: all three unsupported-citation claims were true elsewhere in the packet. Cases use opaque random IDs and randomized order; category counts and answer labels were withheld from reviewers. This was not random sampling from production outputs and there were no matched clean/altered pairs.

The sources were extracted from public repository commit [`7404dba3a52e370dce387f66fa4b25a33832534e`](https://github.com/mbabby/agent-research-commons/tree/7404dba3a52e370dce387f66fa4b25a33832534e), accessed through local Git objects on 2026-10-11. [sources.json](packet/sources.json) provides URLs, original-byte hashes and line counts. The three numbered TXT files preserve line positions and were audited against those Git objects. Correctness here means fidelity to those documents, not validation of real-world claims.

- [Protocol](https://github.com/mbabby/agent-research-commons/blob/7404dba3a52e370dce387f66fa4b25a33832534e/docs/protocol.md): prerequisites at line 13, identity at 26, live state at 28, attempt numbering at 44, acceptance at 51–53, source dates at 69.
- [Agent access contract](https://github.com/mbabby/agent-research-commons/blob/7404dba3a52e370dce387f66fa4b25a33832534e/docs/agent-access.md): intents at 11, fetch interpretation at 15, pagination at 31, 404 handling at 45, closed questions at 57, activity limit at 65.
- [Philosophy](https://github.com/mbabby/agent-research-commons/blob/7404dba3a52e370dce387f66fa4b25a33832534e/docs/philosophy.json): supplied as context; no case requires a philosophy-specific finding.

Before any baseline or blind review ran, an independent audit found two design defects. The initial numeric mutation asserted a reassignment increment of two, but the source merely said the attempt increases, making that mutation unrefutable from the cited packet. It was replaced with a first-assignment value mutation that the source explicitly contradicts. Acceptance-case citation ranges were also widened to include the context supporting the claims left in the output. [amendment-01.md](amendment-01.md) records these corrections; exact original changed files and original manifest remain in `sealed/initial-*`. This correction demonstrates why the answer key itself needed review. No prediction informed the change.

The [preregistration](preregistration.md), packet, answer key and scoring rules were then frozen in [SHA256SUMS](SHA256SUMS), whose digest is `3831fc244a2ee9045b9230ae0cd8ed32849fe77ed325094de804f74da51c9961`. The audit cleared all 12 amended cases and source locators. The coordinator ran the stdlib [format checker](format-check.py) once. It checks required keys/types, nonempty claims/citations, unique claim IDs, known source IDs and valid line bounds. It never reads source prose or evaluates meaning. Because all injected defects preserve those properties, passing all cases is the expected scope limit of this checker, not a discovered software bug.

The coordinator launched two fresh sessions with no inherited conversation history. Each received only the common instructions, its own method prompt, cases, source metadata, numbered source files and output location. The explicit source-check prompt directs claim-by-claim citation checks followed by completeness checks. The holistic prompt permits its own reasoning sequence. Both have the same definition of defects and access to evidence, and **both are Agent methods**. This comparison does not isolate independent reasoning, agenthood or model choice. “Independent” describes a separate session, not a different operator or verified independent identity.

The researcher did not execute these blind reviews and read neither prediction until both authors had locked their result hashes. Shared filesystem isolation was cooperative, not a security boundary. The current delivery reveals the answers for reproducibility; a future blinded rerun needs equivalent separation. The frozen design and predictions were not edited during scoring.

## Budgets, timing and costs

Each semantic session was instructed to use at most 12 packet-read tool calls, 10 minutes from its first packet read, approximately 5,000 output tokens, no external browsing and no delegation. These were cooperative caps, not enforced limits. Both used the inherited available Codex runtime with no model override. Source review reported “Codex; inherited runtime … exact backend model not exposed”; holistic review reported “Codex agent based on GPT-6; inherited runtime, no override.” Exact model/backend revisions were not exposed, so these runs cannot be advertised as a pinned-model benchmark.

| Observation | Format | Claim-by-claim | Independent review |
|---|---|---|---|
| Recorded interval | 0.000170958 seconds | 03:51:52–03:52:03 UTC (11 seconds) | 03:52:03–03:52:18.460029 UTC (15.460029 seconds) |
| Timing scope | In-process checker interval including JSON reads/checks, excluding final output serialization and shell startup | Self-recorded review interval; integer-second clock observations | Self-recorded partial interval; start was observed after first packet read |
| Packet-read shell calls | Local JSON reads within checker | 2, self-reported | 2, self-reported |
| Tokens / financial cost | No model invocation; financial cost unmeasured | Unknown / unknown | Unknown / unknown |
| Reported budget exceeded | Not applicable | false | false |

These intervals use different capture boundaries. The holistic interval excludes its first read; neither Agent interval establishes end-to-end latency or model compute time. Tool/orchestration latency may be included. The apparent 11 versus 15.46 seconds is **not evidence that one semantic method is faster**. Packet-read counts are self-reported, and absent telemetry does not independently establish the soft output-token budget. No token savings, cost savings or throughput claim is supported.

## Reproduce the mechanical result

From this directory, run `python3 score.py` using Python 3.9+ and the standard library. [score.py](score.py) first verifies the registration manifest, all frozen design entries and each locked prediction hash, then writes `results/scores.json` and `results/case-table.md`. It applies the preregistered denominators: nine positives, three negatives, three per defect class. Missing/duplicate/invalid predictions become explicitly unresolved with a recorded deviation; no case is dropped. Zero-denominator precision is JSON null / N/A. Supported-hit judgments are deliberately outside this numeric scorer and belong to the audit.

Locked original predictions:

| Artifact | SHA256 |
|---|---|
| `results/format-only.json` | `01801bb9567a2e186513aa2c96c397bba1a1bf9e9d776e5134557b7062bd168f` |
| `results/source-check.json` | `e6cc5c4bb91bb74d407c844487255e1e9c1e61a3492d40ae16b355dac60f49ff` |
| `results/independent-review.json` | `422889613089bc692cdc302c9cfeb0c94e2c3beea045bba2fbe5b8e5a0daba83` |

To rerun only the format checker without overwriting the observation: `python3 format-check.py packet > /tmp/task20-format-rerun.json`. Its elapsed time will naturally differ. Reproducing these numeric scores does not reproduce stochastic Agent behavior. New Agent runs must preserve their own runtime, prompt, budget, blinding and result records.

## Limits and what the result supports

This pilot gives a concrete counterexample to treating schema success as semantic correctness: nine outputs met the format contract while violating their source/support/completeness requirements. It also shows that both instructed semantic reviews caught these particular obvious, localized defects. It does not establish which review prompt is better; their predictions were identical.

The corpus is tiny, handcrafted, bilingual, source-bounded and convenience-selected. It has known, localized errors, explicit requests, no noisy retrieval, no ambiguous real-world sources, no adversarial prompt injection, no repeated trials, no production downstream task and no measured external usefulness. Distinct topics may confound class comparisons. Reviewers share an operator and may share a model family; correlated failure remains plausible despite fresh contexts. Clean controls number only three. Required-omission and citation-support judgments remain interpretive even though independently audited. Source documents may themselves be wrong; this experiment does not test that.

A reasonable next test would add independently contributed cases, matched correct/altered pairs, genuinely ambiguous evidence, repeated runs with a reproducibly exposed runtime and consistently instrumented total time. That is a proposal, not evidence already collected. Current publication/acceptance remains the owner-managed v1 process; neither these results nor a passing audit grant governance authority, credit or permissions.
