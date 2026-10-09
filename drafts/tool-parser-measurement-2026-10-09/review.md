# Separate-session review of the synthetic parser experiment

Review date: 2026-10-09. Scope: the local Community #36 draft in this directory. This review was conducted in a separate Codex session under the same operator as the researcher. It is not external independent participation, an independently owned review, or official acceptance. No Issue, contribution record, PR, or deployment was published by this reviewer.

## Reproducibility verdict: supported within the inspected environment

I read the protocol, all 18 fixtures, implementation, stored results and report, together with the repository research rules and philosophy. After inspecting the script, I ran:

```sh
python3 drafts/tool-parser-measurement-2026-10-09/experiment.py --output /tmp/arc-parser-independent-review.json
```

The replay was byte-identical to `results.json`, including Python 3.9.6 metadata. I independently checked the expected status category of each of the 18 fixtures and all 54 parser outcomes against a case/strategy map, and checked each recorded correctness value against full expected/parsed equality. I verified that current `protocol.md` and `fixtures.json` are byte-identical to their contents in freeze commit `6ca5cdb`, where `experiment.py` is absent. This establishes the recorded Git ordering, not that the author had no earlier informal design or unpublished implementation.

The implementation, report and results were untracked local files at review time. This review therefore binds to the following file hashes, not an as-yet-uncreated fixed contribution version. A later published review record must target the actual exact artifact URL and full commit SHA; changed content requires renewed review.

| File | SHA-256 |
| --- | --- |
| protocol.md | `3ded36bfb69e80174cb99d004ec2650bc13cc7a5b8f1e501ab88c583a8515881` |
| fixtures.json | `6b09e6b5a00f2a265a91807e24ccc85561d5dd93cab8c3cd791aa1773c92f3b2` |
| experiment.py | `ceeb77a92f7f5321badafe2be48bcad7825344475901fa65234dbc6988cd3eac` |
| results.json | `563e8e3e8d3a29098cc5d0ecd54d1a2b6b4f7293bc62c2fd9b7b0e8573a79d22` |
| report.md | `49c7eea49928e0ee568b44054b9047df21bfa4433f2975c1d03a2d86a1944db8` |

I did not reproduce on another Python version or operating system. The implementation contains no network, model-call or tool-dispatch path; parsed calls are dictionaries only.

## Data verdict: supported for these assigned synthetic labels

The six valid calls contain the three stated cities with the correct tool and sole argument; three are JSON and three bracket expressions. The other six scored messages belong to the assistant-text channel, so their no-call labels follow the declared contract even when their prose contains bracket examples. Both profiles consequently have identical expected decisions and city arguments.

The controls cover truncated JSON, wrong tool, wrong argument type, an extra argument, a duplicate key and surrounding prose. Each rejection label follows the frozen contract. The duplicate-key hook applies to nested JSON objects as well as the outer object. No rejected valid call is credited as restraint, and controls are excluded from the profile score denominators.

Per-case error accounting is exact: JSON-only misses `alternate-call-1`, `alternate-call-2`, and `alternate-call-3`; fallback makes false calls on `canonical-restraint-1`, `canonical-restraint-2`, and `canonical-restraint-3`, and incorrectly accepts `control-surrounded-call`. Every other case/strategy pair matches its label. Thus the table's scores (6 versus 3, 3 versus 6, then 6 versus 6) and control rejections (6, 5, 6) follow directly. Zero-denominator fields in JSON are counts accompanied by zero denominators, not claimed rates.

These labels are author-assigned ground truth, not empirical annotations of real intent. The three plain alternate no-call strings are identical; city substitutions provide little structural diversity. Eighteen fixture identifiers do not establish 18 independent samples, and the report correctly disclaims 54 independent observations.

## Method verdict: supported as a constructed counterexample only

Changing the parser over the same fixed profiles reverses the direction of the profile-score difference. This is a valid existence example. It is partly built into the experimental design: the fallback intentionally drops the channel boundary, and the JSON-only strategy intentionally does not implement both recognized formats. Passing the normalizer is expected for this small contract-conforming set.

I specifically challenged the potential causal interpretation. Profiles vary in both call encoding and no-call wording; strategies vary in both format recognition and envelope policy. The experiment cannot isolate a single factor's effect or attribute differences to model ability. The protocol and report explicitly acknowledge this, and their case-level explanation distinguishes the format misses from the channel false calls. No statistical significance or prevalence claim is justified or made.

The controls are useful diagnostics, not a comprehensive robustness or security suite. They do not exhaust bracket syntax, escaping, multiple candidate calls, empty strings, unknown channels, nesting or resource limits. In particular, code rejects whitespace-only city strings using `.strip()`, while the protocol says only “nonempty”; no current fixture depends on this edge case. Any expanded contract test should resolve that wording before adding labels. This does not change any reported score or require relabeling the frozen fixtures.

## Conclusion verdict: supported within the report's explicit limits

The narrow ranking-reversal claim is supported: JSON-only gives canonical a three-decision advantage, and fallback gives alternate a three-decision advantage on the same twelve scored messages. Normalization with envelope preservation ties them. This supplies no evidence that a named model, real benchmark, upstream parser, or deployment has this behavior. I did not inspect the motivating Reddit source, and none of its empirical claims is required for, or verified by, this review.

The report adequately distinguishes synthetic profiles, maintainer-operated sessions, actual tool execution and official acceptance. Its recommendation to disclose parsing contracts and both error types is a reasonable methodological inference, not an experimentally measured improvement in real-world evaluation. Under P1/P2 this artifact supplies inspectable evidence for a bounded question; P3/P4/A2 permissions and acceptance stay unchanged; P5 correction remains possible; P6 requires preserving the same-operator disclosure wherever this review is cited.

No blocking defect was found in the inspected calculation or bounded conclusion. This is scope-limited support, not general parser certification. Useful follow-up would be held-out fixtures and a factorial format/channel comparison with labels fixed before implementation; those are new studies, not prerequisites for the present existence example. No experiment or report content was changed by this reviewer.
