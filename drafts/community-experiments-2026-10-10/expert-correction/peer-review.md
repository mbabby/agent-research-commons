# Scoped peer review — expert correction experiment

Reviewer logical session: `tool_outcome_research`, 2026-10-10. This is a separate execution/review session from the artifact author within the same human-operated research task; it is not independent outside participation. I inspected the protocol, fixture, executable, freeze record, README and saved results before running the executable. I made no changes to the implementation, fixtures or reported results.

## Reproduction performed

From the repository root, Python 3.9.6:

```sh
python3 drafts/community-experiments-2026-10-10/expert-correction/experiment.py --output /tmp/expert-correction-tool-outcome-review.json
```

Exit status 0. This command executes all 18 query/order combinations for each method, all four overall checks and both negative controls. I separately compared the saved and reproduced JSON. Full-file bytes do **not** match because `executed_at_utc` changed; it was the only differing top-level value. `observations`, `negative_controls`, `checks`, `source_sha256` and `all_checks_pass` match exactly as parsed JSON. No separate test suite is supplied; the executable's exhaustive frozen-grid checks are the tests reproduced here.

## Four scoped verdicts

| Scope | Verdict | Evidence and boundary |
|---|---|---|
| Reproducibility | supported | Fresh execution exits 0; deterministic result fields and code/input digests match the saved run. Freeze hashes match the two frozen files. Local timestamps/hashes do not independently attest when expectations were written. |
| Data | supported | Inspected nine queries, two correction records and two arrival permutations. Both correction actors and the note are explicitly fictional; the candidate labels and expected verdicts are supplied inputs. The 18 calls are repeated evaluations of one case, not independent samples. No external expert-validity or model-performance claim is established. |
| Method | supported | Evaluator checks output enum, exact dataset/language, inclusive release range, and one applicable versioned decision. The v1 decision stays unresolved, including historical replay after v2. Selected v2 compares supplied labels. Both correction records survive as equal JSON values. Premature selection causes eight expectation mismatches; scope bypass causes two. These controls detect the named faults, not every possible failure. |
| Conclusion | supported | Saved and reproduced totals agree: overwrite decides 18/18 and matches 6 expectations; retained decides 6, leaves 8 unresolved, marks 4 inapplicable and matches 18. Only overwrite changes `v1-incident` and `v1-status` with arrival order. README correctly limits this to stipulated mechanics and a deliberately weak baseline, without claiming scientific label correctness or external usefulness. |

No publication blocker found within this stated synthetic scope. The malformed-output, missing-history and multiple-decision paths are not covered, and the README acknowledges these coverage limits. In particular, preservation here means retained claim values remain recoverable; it is not evidence of durable storage, tamper resistance or real organizational adjudication. The red development file records zero retained matches and `all_checks_pass=false`; I inspected those fields but did not reconstruct its unavailable earlier executable.

## Exact reviewed SHA-256 values

| File | SHA-256 |
|---|---|
| protocol.md | `f07c29e41dda09d3d2750bca874197c65b1fd2f247eaf322b84d785a48c2ff17` |
| fixtures.json | `c57093ac25b3c68fa8e2a5e1aaa04548907655de370bac51ea04e6a2728de7b4` |
| freeze.json | `59d4ae53e4d7716e486b13ae049a5c74924c9c6bf77c5ca05766d92b1a3f7cce` |
| experiment.py | `a79d3e164f3c6e612777ec37004cc8d45357d584dcf73b98341c79c7f6d8ea4a` |
| results.json | `92dd6d4dbce0b95c4e4532921a40290da007c58493e15cae811dba30d8ef96d6` |
| README.md | `1c90bc0d39fe1488028d844cd7a7a64135eeb8104d6dbb3be42ace9a58d00c2a` |
| red-results.json | `4ef4ed31bed13869fb3ed373518c3718abb92b87035f429b56a456d6d5b72ae7` |

These verdicts apply to the files identified above. A later changed executable, fixture or conclusion requires renewed review; this document neither accepts an official report nor transfers governance authority.
