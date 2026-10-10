# Scoped peer review — browser recipe mock

Reviewer logical session: `tool_outcome_research`, 2026-10-10; separate session from the author, within the same human-operated task. This is not independent outside participation. I inspected protocol, fixtures, executable, tests, README and saved results before execution. No implementation or source-data edits were made.

## Checks performed

Python 3.9.6, repository root:

```sh
python3 -B -m unittest discover -s drafts/community-experiments-2026-10-10/browser-recipe -v
python3 -B drafts/community-experiments-2026-10-10/browser-recipe/experiment.py --output /tmp/browser-recipe-tool-outcome-review.json
```

All six behavioral tests passed; the run emitted 50 fixture/policy records. I compared the temporary output with saved `results.json`: **exact byte-for-byte match**. Frozen protocol/fixture hashes match. I separately inspected unknown-outcome and hidden-TOCTOU traces, decisions and metric fields for all three main policies.

| Review scope | Verdict | Evidence and boundary |
|---|---|---|
| Reproducibility | supported | Tests pass and all 50 saved records reproduce byte-for-byte under Python 3.9.6. The local freeze hashes detect changes but do not independently attest chronological preregistration. |
| Data | supported | Ten explicit synthetic fixtures, five deterministic policies and reset worlds are transparent. The ledger records submissions, actual transitions and no-ops. No real browser, human sample, model performance or provider behavior is represented. |
| Method | supported | Actual world transitions supply results; policies receive visible observations rather than fixture IDs or oracle outcomes. Current task, target, context, permission and effect drive guards. Tests expose wrong-target dispatch, permission-versus-instruction differences, redundant retry, abstention and the hidden transition. The two controls are deliberately specified policies, not independently developed agents. |
| Conclusion | supported | README totals and qualifications agree with the reproduced results. Guarded/fresh each have one wrong effect, five known completions and one unknown outcome; naive has six wrong effects and two known completions. Shared checks explain guarded/fresh agreement; the README does not treat it as independent corroboration. |

## Focused findings

**Unknown effect:** guarded/fresh each submit once, produce one archive transition, retain `unknown`, and report desired-state achievement true but known completion false. Naive submits twice; the second archive is a committed no-op. Its one redundant submission is correctly distinguished from a second changed-state effect. This fixture does not demonstrate a non-idempotent duplicate, and the README explicitly says so. All status reads fail here; successful-but-unattributed reads remain a separate untested case.

**TOCTOU:** all three main policies observe archive, then the hidden transition changes the actual handler to delete before dispatch. Each deletes D17 and receives `unexpected_effect`; each has one wrong/unauthorized effect, zero known completion and zero unknown outcomes. The result is known wrong rather than unknown. A post-action receipt detects harm after it happened; the README correctly refuses to claim prevention.

Metrics are coherent within the defined scope. Wrong and unauthorized effects overlap rather than add. Permission-denied attempts contribute no mutation. Always-abstain has six unnecessary abstentions and no known completions; its desired-state count of one is merely the inspect-only no-mutation state. Initial-feasibility scoring, including its treatment of hidden future danger, is explicitly disclosed.

No publication blocker found for these bounded mock claims. No real-browser reliability or documentation/API behavior was independently reproduced in this review. Six tests plus trace inspection cover the stated branches, not arbitrary workflows or every future change.

## Exact reviewed SHA-256 values

| File | SHA-256 |
|---|---|
| protocol.md | `f37a925777ec27bf733ba0daefb4f5d96c816f7255ad9062478818dac36c3bbd` |
| fixtures.json | `184d056f054a6f1898ed9ecd3e9822d08eabf9a74b60c24b2469543431cf336f` |
| experiment.py | `17ba20b4d00cf4257b58365fbc9248ace73e5ec6ee2b36df83c5f59bcdfdf34a` |
| test_experiment.py | `f9b63d099bfe0d75a3c31f9d14b5b05c26378e59dfcdc8166239d5bcd357e36c` |
| results.json | `3be35b3392b2c8e73857bff1669f4542e550954ff300a2da04d80e34b54920f3` |
| README.md | `e10f4ca64dbe6a107e47812b939431dac5cf7569cdec29483fa99d184d56d8b1` |

Verdicts apply only to these reviewed bytes and stated scope. Later changes need renewed review; this document is not official acceptance or a transfer of authority.
