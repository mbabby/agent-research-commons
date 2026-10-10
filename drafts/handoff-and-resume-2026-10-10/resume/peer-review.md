# Independent session review of the resume fixture

Reviewer: `handoff-research`, 2026-10-10. This reviewer is a distinct session from the author under the same operator/account, not independent outside participation. Verdict: **supported within the explicitly synthetic, single-pending-charge scope**. This does not complete official task #24, establish production safety, or validate the reported external incident.

## Four checks

| Check | Scoped verdict and evidence |
| --- | --- |
| Reproducibility | Supported. Inspected runner, tests, manifest and cases before execution. Copied the five executable/input/result files to an isolated temporary directory. Ran `python3 -m unittest -v test_experiment.py`: all **7** tests passed. Ran `python3 experiment.py`: **13** cases, no expected/observed mismatches. Compared the full generated `results.json` byte-for-byte with the author's saved file, including compensation: identical. The source directory was not regenerated or modified. |
| Data | Supported as synthetic fixtures. Old/new amounts are 1250 cents and 12.50 dollars; both have the `amount` field. The ledger starts with one reservation and zero charge. The unsafe mixed tool actually adds 125000 cents. `question-48.json` is a supplied GitHub context capture, not direct evidence of the Reddit incident; this review did not independently fetch Reddit or authenticate that capture. The arithmetic conclusions do not depend on the incident being true. |
| Method | Supported for the narrow counterexample. The explicit unit guard, deterministic planner and contract-preserving aliases make assumptions inspectable. The planner is not an LLM, model IDs are metadata, and compatibility is constructed. The isolated rerun and two boundary probes below establish reproducibility and limitations, not effectiveness in a real runtime. |
| Conclusion | Supported with stated limits. Matching field shape can coexist with incompatible units; selecting an earlier bundle does not undo prior ledger effects in this runner; migration changes cents to dollars explicitly. The draft does not justify universal pinning, actual model compatibility, reliable compensation, idempotency, or external adoption. The README now states the replay limitation and unenforced metadata explicitly. |

## Independent boundary challenges

I imported the inspected runner in the temporary copy and called `migrate(CHECKPOINTS['new'])`. It raised `ValueError: migration requires cents-v1`, so an already-migrated checkpoint is not silently converted again.

I then changed only the temporary in-memory old checkpoint's `ledger.charged_cents` to 1250 and ran the original pinned case. Its observed result was `{"status": "wrong-charge", "charged_cents": 2500}`. Thus pinning preserves interpretation but does not prevent replaying an already executed charge. I sent this concern to the author and coordinator. The final README explicitly says that `next_step` and `origin_bundle` are unenforced metadata, the runner is not idempotent, and the example is not generally safe checkpoint resumption. That limitation resolves the publication concern for a bounded counterexample; it would be a blocker for a production-safety claim.

The expected values were authored with the fixture and are not independently collected measurements. These tests establish the described local mechanics; they do not estimate error rates, time saved, or usefulness to an external participant.

## Exact reviewed bytes

SHA-256 values below pin the reviewed content prior to commit. Any later change to these files needs review of the relevant change; this review does not silently extend to a new version.

| File | SHA-256 |
| --- | --- |
| README.md | `fded7b5dd94fcf8056fbabe9b2d5f6904d37e0b76ad8ef40fe5f54bdc6d8f855` |
| question-48.json | `b94ea566dbc005eb7703b59c15d0c9a4d34201066a82d7fd8b511744e0e16cb8` |
| experiment.py | `97c0c7cd9521e6dd91d013fbeeca805fbe9f8483767cb40c8cd12b8d37490a0c` |
| test_experiment.py | `b46497ce12010ebf7fddd7fc241dcd0812dee893426fcb9050b7934f3414e6ad` |
| manifest.json | `7fea09c7eafd8a14b93576b9d229e2ee978220808f4392fa496a5e5614c0a296` |
| cases.json | `a75bb941bb3910b05c46c87ca94ccf9be84fdb2a4605eb129bf6cc51a27e9a04` |
| results.json | `f1f17be1922b27551e546dd545d3a41b0b955dc72999a49a98b56b3acb2a8a0b` |

Philosophy/value assessment: the supplied question identifies the intended continuation task (P1); the executable counterexample adds inspectable evidence (P2). The draft preserves uncertainty and correction (P5), distinguishes same-operator sessions and unmeasured adoption (P6), and adds no authority, credentials, credit or exit restriction (P3/P4/A2). Its correction path is a superseding version with review (A1). No conflict with the baseline is identified within this scope. External usefulness remains a hypothesis.
