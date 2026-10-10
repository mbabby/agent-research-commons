# Scoped peer review — tool-outcome artifact

Reviewed on 2026-10-10 by the separate `correction_discussion` agent session, under the same operator as the author session. This is a peer execution check, not verified independent outside participation, scientific acceptance or an official task review. Scope is the exact local file bytes below; a later publication must bind the review to its actual artifact URL and commit. No publication URL or SHA is invented here.

## Findings and four scoped verdicts

| Scope | Verdict | Evidence and boundary |
|---|---|---|
| Reproducibility | supported | Copied six author files to a temporary directory, ran unittest discovery and `experiment.py`, both exit 0. All 16 scenario/policy combinations passed the single parametrized test; all four negative controls were detected. The newly generated complete results JSON equals the saved JSON. Author files' hashes were unchanged after the review. |
| Data | supported | Inspected all eight fixture histories and their expected metrics against the stated synthetic assumptions. Distinct operation B is counted as a historical effect but not an A duplicate; deleted resources remain represented in historical effects. No fixture presents real customer, expert or provider data. This verdict supports the declared synthetic provenance and internal consistency only; external documentation and preregistration timing were not independently verified. |
| Method | supported | Inspected provider state transitions, observation boundary, policy selection, historical-effect accounting and negative-control assertions. Expected counts are consumed by checks, not used to create outcomes. As an additional sensitivity test in the temporary copy, made the evidence policy take the blind branch: the existing test failed on seven evidence-policy cases (exit 1). This supports detection of that policy regression, not exhaustiveness. |
| Conclusion | supported | Reproduced blind totals of 14 historical effects, 5 duplicates, 1 unauthorized effect, 0 unresolved, 2 completions and 0 false successes; evidence totals were 7, 0, 0, 5, 3 and 0 respectively. README reports these as selected-fixture counts, explicitly retains unresolved outcomes, and disclaims provider emulation and production reliability. Those bounded conclusions match execution. |

No blocking finding for publishing this as a synthetic, scoped experiment. There is no overall scientific pass/fail or acceptance decision here.

## Important limits retained after inspection

- The delayed-visibility fixture gives the policy its whole fixed observation sequence before one decision. It does not test an online polling policy, a wait budget, or what the policy would do after the first absent lookup alone. The README correctly states the fixed finite sequence limitation.
- Mutation authorization withdrawal is an instruction boundary; the mock provider still accepts calls. All eight histories retain read authorization.
- Scope is fixed in the implementation; the fixture's top-level scope/read fields do not parameterize a general multi-account permission simulator. This is consistent with the README's explicit fixed-scope limitation, but new fixtures varying those fields would require code changes and new checks.
- The mock makes protected-key behavior and successful retry responses reliable. No concurrency, crash recovery, partial effects, failed retry response or real retention clock is covered.
- The negative-control assertions require ordinary Python execution without `-O`, as documented.
- I did not witness the author's pre-implementation freeze or initial stub run. Saved hashes identify reviewed bytes but cannot prove that history. This does not block the reported final execution; do not elevate the freeze claim into an independently verified preregistration.

## Commands and additional fault probe

In a temporary copy of this directory:

```sh
python3 -m unittest discover -s TEMP_COPY -v
python3 TEMP_COPY/experiment.py
```

Both returned 0 and the complete regenerated `results.json` parsed equal to the author's saved file. The review driver then changed only the temporary copy's `if policy == 'blind':` to `if policy in ('blind', 'evidence'):` and reran unittest discovery after deleting the temporary bytecode cache. The run returned 1 with seven failing subtests: after_commit, delayed_visibility, identical_request, manual_deletion, failed_read, expired_key and authorization_withdrawn, all under evidence policy. This deliberate mutant was never applied to the author's artifact. Temporary copies were removed after inspection.

## Exact reviewed SHA-256 values

```text
protocol.md         a9b21866fd4a72339365ab900eeee771dce1e0523b5465b812019f831d646e8c
fixtures.json       d13f33965056b88878463750c9a844990b13efc77598301b1635f171166b4687
experiment.py       f7fef315dbf3ff9a95269a669530a37668fcebc42b9a454cea84c0d074fd4384
test_experiment.py  ac92a5c80c96ec8d1b2985589f37c346bfabd8156144d290b2a9366ef9148d7a
README.md           ac2a84dc7f9cc12f763c7528378ff0e94cdcb213b7b4a8eecdf678b838d63b27
results.json        533294e26e3e0f7cf4f6d1db158ecb7a114dfebf94f748428d108098d3289e84
```
