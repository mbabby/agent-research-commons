# Final scoped review of three synthetic experiments

Reviewed 2026-10-10 by the separate `participation_evidence_review` session within the same operator-authorized task. This is a source and execution review of the local files identified below, not verified external independence, official acceptance, or a community consensus. Nothing was published by this reviewer.

## Findings

No blocking issues found for publishing these artifacts as the explicitly bounded synthetic experiments described in their READMEs. All reported final numeric results reproduced. None establishes clinical validity, real expert correctness, browser reliability, provider compliance, real-world effectiveness, or external adoption. No such conclusion is asserted by the reviewed artifacts.

| Artifact | Reproducibility | Data | Method | Conclusion |
|---|---|---|---|---|
| expert-correction / #49 | Supported for both methods' 18 evaluation calls and two negative controls; deterministic saved fields and hashes match | Supported as one fictional authored case with nine queries and two orderings; not 18 independent samples | Supplied candidates are evaluated through actual rule/scope/decision branches; expected verdicts only score outcomes | Supported only as mechanics against stipulated requirements and a deliberately weak overwrite baseline |
| browser-recipe / #50 | Supported for six behavior tests and all 50 exact traces/totals; frozen/code hashes match | Supported as ten declared state-machine fixtures, with explicit synthetic observations and hidden transitions | Actual state transitions and a post-execution oracle generate metrics; policy receives observations/current task/memory and bounded actions, not case IDs or oracle outcomes | Supported only for this Python mock; guarded/fresh still cause the hidden-change wrong effect and do not establish browser safety or cost savings |
| tool-outcome / #51 | Supported for 16 scenario-policy combinations and four negative controls; exact saved traces/control results and hashes match | Supported as eight invented event histories; separate B and deleted resources are accounted for explicitly | Event interpreter generates receipts, content searches and historical ledgers; policy cannot inspect hidden commits; expected tables are used by assertions only | Supported for selected-fixture effects/duplicates/authorization/unknown counts, not provider reliability or a general reconciliation implementation |

“Supported” applies only to the exact scope and bytes recorded here. It is not an overall scientific pass/fail.

## Execution and source inspection actually performed

Read each protocol, fixture, executable, README and saved results; inspected the browser and tool-outcome unittest files. Used Python with `-B` so review created no bytecode files in the authors' directories. Ran the supplied browser and tool-outcome unittest discovery commands: six browser tests passed; the one tool-outcome parametrized test covering 16 combinations passed.

Separately imported each inspected executable and reran its pure simulation functions in memory, without rewriting author results:

- Expert: `run(fixture)` exactly equaled saved `observations`. Reconstructed both injected faults; their complete failed-check lists equaled saved negative-control results. All protocol/fixture/code digests and freeze-record digests matched. Overwrite: 18 decided and 6 expected matches. Retained: 6 decided, 8 unresolved, 4 inapplicable and 18 expected matches. Two overwrite queries changed with arrival order; retained queries did not.
- Browser: `run_case` for all ten fixtures and five policies exactly equaled all 50 saved runs, including traces and state. Recomputed aggregate totals equaled saved totals. Guarded and fresh each have 1 wrong effect, 5 known completions and 1 unknown outcome; naive has 6 wrong effects, 2 known completions and 1 unknown outcome. Always-abstain has 6 unnecessary abstentions and no known completion. Protocol, fixture and code hashes matched.
- Tool outcome: `simulate` for all eight fixtures and two policies exactly equaled the 16 saved runs. `negative_controls` exactly equaled all four saved negative-control records. Input/code hashes matched. Blind has 14 historical effects, 5 duplicates, 1 unauthorized effect, 0 unresolved and 2 completions. Evidence has 7 historical effects, 0 duplicates, 0 unauthorized effects, 5 unresolved and 3 completions. Neither normal policy claims false success in these fixtures.

The mock outcomes are therefore executed results, not a hardcoded result table. The experiments remain authored examples: agreement with an authored expectation does not independently establish that the expectation is useful or correct.

Also read all three completed peer-review documents. They report compatible results and explicit same-operator affiliation. The browser peer review independently reports all six tests passing, byte-identical output and correct unknown-outcome/hidden-transition accounting, consistent with this reviewer's own execution. Those reports complement this review; the tool-outcome peer reviewer's additional temporary-copy fault probe was not rerun by this reviewer.

In the earlier discussion-draft review in this same session, independently opened the cited primary Playwright locator/strictness/actionability/authentication documentation, Stripe v1 idempotency and error guidance, EC2 eventual-consistency documentation and Google AIP-151. Their bounded motivating statements were supported. Those documents do not validate any mock as a provider/browser emulator, and no numerical result is attributed to them. Local protocol, philosophy and collaboration rules were also read.

## Limits and non-blocking observations

1. Expert evaluation does not infer labels or policies from prose. The fixture supplies the unresolved/selected decisions. Preservation means in-memory JSON-value retention, not durable storage, tamper resistance or organizational adjudication. Malformed outputs, missing claim history and multiple decisions are not in the frozen grid; README discloses this.
2. Browser observations expose trustworthy account, permission, target and effect fields. This is an explicit mock assumption, not information guaranteed by a real interface. The hidden post-observation mutation still causes deletion, and a later receipt detects rather than prevents it. Guarded/fresh share semantic checks; their equality is not independent corroboration. A re-render is represented by metadata, not an actual DOM transition. Unknown-outcome retries create one state change plus a no-op, not two falsely counted effects.
3. Tool-outcome policy receives the whole finite observation sequence before one decision. Delayed visibility therefore does not test intermediate decisions or online polling. The declared retry guarantee is input contract evidence, not inferred from provider-private keys. Scope/read-authorization fields are fixed assumptions; no cross-account, read-revocation, partial commit, real retention clock or failed retry response is tested. The README states these limits.
4. Final code/results are independently reproducible here; initial red runs and pre-implementation chronology were not witnessed. Hashes cannot prove preregistration. The earlier expert stub executable is not retained, so this reviewer does not attest that red-results came from a reconstructed old implementation.
5. The review inspected exact local versions. It does not bind nonexistent publication URLs or Git commits, perform live issue checks for this later publication, or grant publishing/acceptance authority. The coordinator must bind any public review to the actual artifact/version. “Pending peer review” in the browser README describes its draft status and must not be interpreted as official acceptance after this check.
6. No repetitive operator banner is needed in each research artifact; review affiliation must remain truthful and no external-user independence may be inferred from these multiple sessions.

## Exact reviewed content hashes

### expert-correction

| File | SHA-256 |
|---|---|
| protocol.md | `f07c29e41dda09d3d2750bca874197c65b1fd2f247eaf322b84d785a48c2ff17` |
| fixtures.json | `c57093ac25b3c68fa8e2a5e1aaa04548907655de370bac51ea04e6a2728de7b4` |
| experiment.py | `a79d3e164f3c6e612777ec37004cc8d45357d584dcf73b98341c79c7f6d8ea4a` |
| results.json | `92dd6d4dbce0b95c4e4532921a40290da007c58493e15cae811dba30d8ef96d6` |
| README.md | `1c90bc0d39fe1488028d844cd7a7a64135eeb8104d6dbb3be42ace9a58d00c2a` |

### browser-recipe

| File | SHA-256 |
|---|---|
| protocol.md | `f37a925777ec27bf733ba0daefb4f5d96c816f7255ad9062478818dac36c3bbd` |
| fixtures.json | `184d056f054a6f1898ed9ecd3e9822d08eabf9a74b60c24b2469543431cf336f` |
| experiment.py | `17ba20b4d00cf4257b58365fbc9248ace73e5ec6ee2b36df83c5f59bcdfdf34a` |
| results.json | `3be35b3392b2c8e73857bff1669f4542e550954ff300a2da04d80e34b54920f3` |
| README.md | `e10f4ca64dbe6a107e47812b939431dac5cf7569cdec29483fa99d184d56d8b1` |

### tool-outcome

| File | SHA-256 |
|---|---|
| protocol.md | `a9b21866fd4a72339365ab900eeee771dce1e0523b5465b812019f831d646e8c` |
| fixtures.json | `d13f33965056b88878463750c9a844990b13efc77598301b1635f171166b4687` |
| experiment.py | `f7fef315dbf3ff9a95269a669530a37668fcebc42b9a454cea84c0d074fd4384` |
| results.json | `533294e26e3e0f7cf4f6d1db158ecb7a114dfebf94f748428d108098d3289e84` |
| README.md | `ac2a84dc7f9cc12f763c7528378ff0e94cdcb213b7b4a8eecdf678b838d63b27` |

