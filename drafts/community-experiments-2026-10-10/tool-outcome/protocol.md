# Frozen protocol v1 — unknown tool outcomes

Frozen before implementation, 2026-10-10. Scope: eight deterministic synthetic histories; no live provider calls, production changes, or general reliability estimate. Implements the approved #51 discussion design.

Each run starts with operation A in account/acct1, environment/mock, payload P. Distinct B can have identical content. Provider event interpreter maintains historical creation records, current resources, receipts, deduplication entries and authorization state. Policy receives only explicit public observations, not hidden commit events. Run one blind fresh-key retry or the evidence policy after the scenario observations. Delayed visibility supplies two successive reads; policy must not convert first absence into success/failure.

Evidence policy: recognize only successful receipts bound to A and its account/environment. Otherwise retain unknown. Retry with original key/payload only when documented protection is still valid and current mutation authorization holds; otherwise stop. Reads are allowed only when read authorization holds. This experiment keeps read permission in all eight fixtures; withdrawal affects mutation only. No inference that withdrawal automatically permits reads.

Blind policy: always retry once with a fresh key, disregarding observations and authorization. A provider that accepts requests after policy-level permission withdrawal exposes the client's obligation; withdrawal here is a user instruction, not credential revocation.

Fixture expected metrics are fixed before implementation. Historical effects count all commits, including B and deleted resources. Duplicates = max(A historical commits - 1, 0), not count of identical payloads. Unauthorized effects count commits after mutation authorization is withdrawn. Completion = policy correctly identifies one successful A operation, with exactly one A commit and no unauthorized effect; historical success need not imply current resource existence. False-success = policy says success when A has no commit. Unresolved = policy retains unknown. These overlapping metrics must remain separate.

Cases with no declared usable deduplication contract: identical request, deletion and failed status read. The provider can retain internal entries without exposing a client guarantee; the evidence policy cannot infer one. Expired-key fixture explicitly prunes the original key. Before/after/delayed/withdrawal cases declare protection. None tests a real Stripe/EC2/Google API or its exact retention duration.

Negative controls: (1) content match incorrectly resolves A, caught by false-success assertion; (2) ignoring current authorization produces an unauthorized effect; (3) missing resource treated as non-execution produces a duplicate after deletion; (4) retrying an expired original key produces a duplicate. Controls must fail normal safety assertions, and the harness reports those expected detections without pretending controls pass the policy requirements.

Run and retain fixture/protocol SHA-256 in results. Expected outcomes must not be edited to fit implementation. If unexpected results arise, report discrepancy before changing protocol. Python 3.9+ standard library only.

Research basis (read 2026-10-10): https://docs.stripe.com/api/idempotent_requests ; https://docs.stripe.com/error-low-level ; https://docs.aws.amazon.com/ec2/latest/devguide/eventual-consistency.html ; https://google.aip.dev/151 . Provider documents motivate cases, not validate the mock.
