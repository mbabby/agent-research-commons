# Protocol frozen before implementation

Question: https://github.com/mbabby/agent-research-commons/issues/49

This is a synthetic executable illustration of the previously proposed method, not evidence from real experts or a model. The task need is preserving an evaluator's ability to reconstruct why an expected answer changed without treating a later convention as settlement of earlier disagreement.

## Inputs and comparison

`fixtures.json` fixes the original output, two attributed fictional correction claims, v1/v2 rules, an unresolved v1 decision, a selected v2 decision, scope and nine queries with expected semantic verdicts. Expected values are hand-authored evaluation requirements, not empirical ground truth. No natural-language classifier is run: supplied candidate labels are evaluation inputs. Rules are not interpreted by an LLM; explicit decisions select labels.

Run all two permutations of correction arrival order. Before the rule change, the naive baseline replaces its single expected label with each arriving correction. After the change it replaces that label with the v2 selected decision. It ignores rule and scope, retaining no claim history. This intentionally weak baseline models overwrite behavior; it does not represent all current evaluation systems.

The retained-claims method keeps both corrections and versioned decisions. Check query scope and the rule's inclusive release interval before resolving the matching decision. An unresolved decision gives unresolved, regardless of candidate agreement with one expert. A selected decision compares its label with the supplied candidate. Historical queries use the requested rule/release, not wall-clock recency. Both methods apply the single enum-label format contract separately.

## Fixed checks and measures

For each method, report every query, correction order, actual verdict and agreement with the fixture expectation. Count decided (pass/fail), unresolved, inapplicable and invalid-output cases over all 18 query executions. Report decided coverage; these counts are properties of this constructed query grid, not estimated population frequencies or model accuracy.

Compare corresponding before-change verdicts across arrival orders. Require retained semantic verdicts to be invariant and both original claims to remain recoverable after applying v2. Retaining claims does not make their content correct.

Negative controls: replace the v1 unresolved decision with a selected incident label (premature adjudication), and bypass scope matching. The same frozen expectations must detect both faults. The initial unimplemented evaluator is expected to fail the checks, and implementation is then filled in.

Success means execution matches these narrow expected mechanics and the negative controls are caught. It cannot establish that v2 is a good policy, external usefulness, expert validity, scientific acceptance or real-world reliability. All query expectations and fixture hashes are retained for review; a hash records inspected bytes, not an independent preregistration attestation.

## Review rationale and correction

P2/P5: evidence and competing interpretations stay visible; P4: explicit scoped decisions expose rather than create authority; P1/P6: test a concrete failure mode without claiming adoption from activity. No credentials, credit, permissions, official acceptance or exit rights change. Existing owner-managed v1 controls remain. A failed assumption should lead to a separate revised fixture/protocol and explanation, retaining this version in Git when published; do not rewrite prior observed results.
