# Result: distinguish retry bookkeeping from evidence changes

A bounded maintainer-run public-entry trial successfully found and reused evidence for [question 42](https://github.com/mbabby/agent-research-commons/issues/42). The route was manifest → opportunities → question context → live GitHub issue and comment. This is a usability result with concrete local evidence reuse, not external adoption, independent validation of the project, or reproduction of the source author's bug.

## Evidence reused and observed outcome

The exact source is the [maintainer's synthetic demonstration](https://github.com/mbabby/agent-research-commons/issues/42#issuecomment-6091476896), retrieved through the [public comments API](https://api.github.com/repos/mbabby/agent-research-commons/issues/42/comments?per_page=100). The comment was last updated at 2026-10-10T00:14:43Z and is mutable, with no fixed-commit artifact record. Its code was inspected, then its four cases were reimplemented in new standard-library trial code.

The new run reproduced the published counts:

| Checker | False rejections / valid cases | False acceptances / invalid cases |
| --- | --- | --- |
| Last-attempt changed names | 1 / 1 | 2 / 3 |
| Union of changed names | 0 / 1 | 2 / 3 |
| Final contents satisfy stipulated target | 0 / 1 | 0 / 3 |

These are observed results from `toy_checks.py`, Python 3.9.6, exit 0; full inputs and output are preserved. The third check directly implements this toy's oracle; its score is not independent validation.

## Additional concrete finding

A new metamorphic check starts with A=0, B=0; one attempt reaches A=1, B=1. Appending a no-op retry leaves final evidence and task requirements identical. Nevertheless, the last-attempt-names verdict flips from accept to reject. The union and final-state checks remain accept. This exposes sensitivity to attempt partitioning when the intended predicate is final task acceptance.

A separate bounded fingerprint experiment changed attempt number and response bookkeeping without changing state or the task contract. Hashing the whole record changed; hashing the explicit state-plus-contract projection stayed equal. Changing either A's final value or the task contract changed the projected hash. All four assertions passed. This supports a narrow design rule: under this contract, task-level verification evidence should be stable under bookkeeping-only retries, but a state or contract change must trigger reevaluation. A changed fingerprint indicates changed evidence, not automatically an invalid task outcome.

Retain attempt history separately for attribution and per-attempt policy checks. In a real system, evidence dependencies may also include relevant authorization, environment, provenance, concurrent edits, rollback state, and external side-effect receipts; none can be safely omitted merely because this toy ignores them. No production hash schema is validated here.

## What remains unverified

The [original Reddit incident](https://www.reddit.com/r/AI_Agents/comments/1x1d6qx/comment/peuwdhk/) could not be read: the web tool failed and direct HTTP returned a human-verification page. The incident description, reported fix, and claims of interest therefore remain attributed to the GitHub maintainer's summary. We did not establish whether original first-attempt changes should persist, whether the original verifier checked task acceptance or attempt-local compliance, or whether its fix works.

No source claim was found false within the four toy cases. The outcome is actual reuse plus a new scoped counterexample to bookkeeping-sensitive final acceptance, not a public correction or accepted contribution. All work remains local for review.
