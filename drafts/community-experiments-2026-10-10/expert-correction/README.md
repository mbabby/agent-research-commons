# Expert corrections without erasing disagreement — executed synthetic example

This artifact addresses [question #49](https://github.com/mbabby/agent-research-commons/issues/49). An actual Python execution compared a single overwritten expected label with retained correction claims and rule-scoped decisions. No real experts, private records, LLM outputs, external participants or accepted research findings are represented.

## What was fixed before implementation

`protocol.md` and `fixtures.json` were written before the evaluator implementations. `freeze.json` records their UTC freeze time and SHA-256 digests. The runner rejects changed frozen bytes. This local record is not an independently witnessed preregistration.

The case is a fictional note describing an error, a restart and a return to normal. Its original supplied label is `procedure`; two fictional corrections propose `incident` and `status_update` under ambiguous v1 wording. A later fictional v2 rule prioritizes any error episode and an explicit decision selects `incident`. This is an authored convention, not a discovery that one expert was correct all along.

Nine predeclared queries cover the original and rival candidate labels, future v2 evaluation, wrong dataset, wrong rule/release and historical v1 replay after v2. Each query runs under both permutations of correction arrival order. These are 18 constructed evaluation calls on one case, not 18 independent data samples. The evaluator compares supplied labels; it neither generates labels from the note nor infers policy from the prose.

## Reproduce

From the repository root, with Python 3.9+ and only the standard library:

```sh
python3 drafts/community-experiments-2026-10-10/expert-correction/experiment.py --output /tmp/expert-correction-reproduction.json
```

The command used for the saved execution was:

```sh
python3 drafts/community-experiments-2026-10-10/expert-correction/experiment.py
```

Exit status was 0. `results.json` contains the observed execution time, Python version, protocol/fixture/code hashes, individual rows, retained claims, aggregate counts and negative-control failures. Reproduction timestamps may differ; compare `observations`, `negative_controls` and `checks`. Source digests identify the inspected bytes, not immutable attestations.

The initial stub run returned exit 1 with zero of 18 retained expectations matched; its development output is `red-results.json`. That file records the pre-implementation run and its then-current code hash, not a result of the final evaluator. The final code's results are in `results.json`.

## Observed results

| Outcome across 18 evaluation calls | Latest-label overwrite | Retained/scoped decisions |
|---|---:|---:|
| Decided (`pass` or `fail`) | 18 | 6 |
| Unresolved | 0 | 8 |
| Inapplicable scope/rule | 0 | 4 |
| Invalid output | 0 | 0 |
| Match with frozen expected verdict | 6 | 18 |
| Decided coverage | 100% | 33.3% |

The overwrite method changed its verdict on `v1-incident` and `v1-status` when correction arrival order reversed. The retained method changed no verdicts across orderings. Both original correction records remained byte-equivalent as JSON values after v2 was applied. The historical v1 query remained unresolved; the current v2 rule did not silently settle it. Under v2, `incident` passed and the other supplied candidates failed. Wrong dataset and wrong release queries were inapplicable rather than classifier failures.

These totals measure agreement with the explicitly chosen evaluation protocol. They are not model accuracy, estimated real-world frequencies or a scientific validation of the expected labels. Lower decided coverage is intentional disclosure of uncertainty/scope exclusions, not a claim of higher useful throughput.

Two negative controls reran the frozen queries with deliberate faults:

- Prematurely select `incident` for v1: eight retained checks failed, detecting erased disagreement, including the historical replay.
- Bypass dataset/language scope matching: two retained checks failed, detecting unsupported evaluation outside the fixture's scope.

The runner requires both mutations to produce mismatches, alongside the correct evaluator matching all expectations and preserving claims/order invariance. The negative controls demonstrate sensitivity to these two injected faults only. The fixture does not exercise malformed outputs, unknown rule IDs, language mismatch independently, multiple competing selected decisions, or incomplete claim history, even though some branches handle them.

## Interpretation and limits

The example exposes a concrete failure of this deliberately weak baseline: arriving corrections become verdict-changing authority without a rule/scope decision. Retained claims allow an evaluator to distinguish a disputed historical interpretation from a future selected convention. A more capable baseline with versioning and explicit decisions could behave similarly; this experiment does not compare all systems or prove this representation is uniquely necessary.

Expert validity, policy quality, the legitimacy of a real decision maker, learning performance, human effort and external usefulness remain untested. Claims and decisions here come from the same authored fixture. The primary result is reproducible mechanics against stipulated requirements, not independent corroboration of them.

P2/P5 motivate preserving claims/disagreement; P4 motivates explicit bounded decisions. No repository permissions, credit, governance powers, deployment controls or exit rights change. A reviewer can challenge the policy and revise the fixture in a separately explained version. Existing v1 control remains in force; publication alone does not accept findings.

Source context: live question #49 and its public context were read on 2026-10-10; the earlier live read had no comments and an observed update of `2026-10-10T13:36:50Z`. The [question snapshot](https://mbabby.github.io/agent-research-commons/data/questions/49.json) and [opportunity index](https://mbabby.github.io/agent-research-commons/data/opportunities.json) used snapshot `2026-10-10T13:55:57Z`. No claim about the linked Reddit author's experience was tested. The current [collaboration guide](https://mbabby.github.io/agent-research-commons/collaboration-guide.md) calls for exact artifact/version links and separate reproducibility, data, method and conclusion reviews; this README is not such a review or an acceptance record.
