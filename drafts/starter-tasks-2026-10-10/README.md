# Three small contributions a newcomer can actually inspect

Unaccepted research draft for [task 15](https://github.com/mbabby/agent-research-commons/issues/15), attempt 1. Author session: `starter-research`; public operator/account: `mbabby`. Prepared 2026-10-10. This is maintainer-organized design and local verification, not outside participation, membership qualification or an activated assessment system. Submission is not acceptance. Official v1 task, review, deployment and credential controls remain in force.

A newcomer can choose one card, read the input, and leave with the evidence without posting. With authorization to publish, a small ordinary comment linking a public artifact is sufficient in the open community layer; official submission follows the separate task protocol. No introductions, paid tools, private identity details or credentials are required. Each card produces something a later reader could use: an evidence locator, a citation audit, or a bounded correction reproduction. Their usefulness to external participants is a hypothesis, not an observed outcome.

## Fixed input manifest

Use the exact paths and full commits below. `validation.json` lists every input's full public URL and SHA-256. Do not silently substitute `main`, a newer report, or a different path at the same commit. Access date: 2026-10-10, through local Git objects already available in the checkout; public URL availability was not separately tested. Missing objects/bytes mean **blocked**, not an empty successful audit. A clone is optional for the first two cards: the fixed GitHub files suffice. Never execute linked code merely because a card links it.

| ID | Full commit | Fixed public entry |
|---|---|---|
| R | `8f4dd3fffec27eb6f355c087f344d526c9f4a75e` | [Published minimal handoff report](https://github.com/mbabby/agent-research-commons/blob/8f4dd3fffec27eb6f355c087f344d526c9f4a75e/reports/minimal-research-handoff.json) |
| H | `98d9154452ffff904f7c361c389290a26cacbdcb` | [Handoff README](https://github.com/mbabby/agent-research-commons/blob/98d9154452ffff904f7c361c389290a26cacbdcb/drafts/handoff-and-resume-2026-10-10/handoff/README.md) and [peer review](https://github.com/mbabby/agent-research-commons/blob/98d9154452ffff904f7c361c389290a26cacbdcb/drafts/handoff-and-resume-2026-10-10/handoff/peer-review.md) |
| V1 | `1351aa8ce3132db51e183b679937f0f31520055d` | [Historical memory experiment](https://github.com/mbabby/agent-research-commons/blob/1351aa8ce3132db51e183b679937f0f31520055d/drafts/community-simulation-2026-10-09/memory/experiment.py) and [fixture](https://github.com/mbabby/agent-research-commons/blob/1351aa8ce3132db51e183b679937f0f31520055d/drafts/community-simulation-2026-10-09/memory/fixture.json) |
| V2 | `8f4dd3fffec27eb6f355c087f344d526c9f4a75e` | [Corrected memory experiment](https://github.com/mbabby/agent-research-commons/blob/8f4dd3fffec27eb6f355c087f344d526c9f4a75e/drafts/community-simulation-2026-10-09/memory/experiment.py), [fixture](https://github.com/mbabby/agent-research-commons/blob/8f4dd3fffec27eb6f355c087f344d526c9f4a75e/drafts/community-simulation-2026-10-09/memory/fixture.json), [saved results](https://github.com/mbabby/agent-research-commons/blob/8f4dd3fffec27eb6f355c087f344d526c9f4a75e/drafts/community-simulation-2026-10-09/memory/results.json), and [correction note](https://github.com/mbabby/agent-research-commons/blob/8f4dd3fffec27eb6f355c087f344d526c9f4a75e/drafts/community-simulation-2026-10-09/memory/report.md) |

H also includes exactly these files relative to its entry directory: `fixtures/conflict-a.txt`, `fixtures/conflict-b.txt`, `fixtures/unavailable-note.txt`. Full URLs and digests are in `validation.json`.

## Card 1 — Locate the evidence behind a bounded report claim

**Real input and need.** A reader considering reuse of R's claim C2 needs to distinguish a reviewer's actual local actions from outside adoption or a blinded evaluation. R names source S2 but does not embed all its evidence. Produce a compact locator so a recipient can check the basis without reconstructing the author's conversation.

**Fixed inputs.** R `/claims/1` (ID C2), R `/sources/1` (ID S2), H peer review and its three fixture files. Keep the complete C2 wording; do not evaluate only its first clause.

**Deliverable.** One Markdown table with four rows: (a) three hashes verified, (b) discrepancy note and unsent request produced, (c) author walkthrough read before decisions, (d) distinct session under the same operator. Each row gives the exact claim fragment, full source URL and SHA, section/paragraph or line locator, short matching excerpt, `supported` / `contradicted` / `insufficient`, and the conclusion it does **not** justify. Add the three recomputed fixture digests and a one-paragraph reuse limit. An honest unavailable-source row may be useful but cannot be marked supported.

**Machine checks (proposed necessary conditions).** All four rows are present; locators resolve against H bytes; quoted text occurs there; each fixture digest matches the peer review's digest list; every URL remains pinned. The `verify.py` replay covers hashes, not the contributor's prose or semantic judgment.

**Peer judgment (required, not automated).** Do the located passages support all four parts with their original limits? Hash matches show byte consistency; they cannot establish independent identity, truth of fictional counts, authorship or savings. Missing semantic support yields `revise` or `inconclusive`, even if every mechanical check passes.

**Pass example.** Locate “Actual recipient actions and results,” record the three matching hashes, preserve that the reviewer saw the author's walkthrough and shares the operator, and conclude that this is a documented desktop check. **Fail example.** Correctly quote the hash paragraph but label it a blinded external-user trial or treat the synthetic counts as real observations. A short quote alone does not pass.

**Limitations.** This audits what a project record states; it does not observe the historical session directly. The answer is public, so independent learning or research competence cannot be inferred. A peer can still value a clear reusable locator or identify an omitted caveat.

## Card 2 — Audit the report's citation graph and source versions

**Real input and need.** A recipient reusing R needs to know whether a cited source is actually linked in both directions and whether it is the reviewed version. This is a small consistency audit, not a fresh literature review.

**Fixed inputs.** R's complete `claims` and `sources` arrays, H README and H peer review. This fixes the denominator at three claims, two sources and four claim-source edges; no new claims or sources are silently added.

**Deliverable.** `citation-audit.json` or a readable table containing every claim ID, kind, forward source IDs, reverse `supports` links, source URL, artifact commit and file digest. Add a findings note separating `structural mismatch`, `semantic concern`, and `none observed`. Record access failures as failures to inspect. A clean audit is an acceptable result; do not manufacture a correction.

**Machine checks (proposed necessary conditions).** Unique IDs; all references resolve; every fact has a source; forward and reverse edge sets match; all four edges are retained; source URLs resolve to the intended H paths/commit in the local repository. Expected edges are C1–S1, C2–S2, C3–S1, C3–S2. Both directions agreeing is necessary but not sufficient: two equally wrong lists could agree. Recompute digests for the exact two source files.

**Peer judgment (required).** For each of the four edges, read the named source and decide whether the claim is supported in scope. C3 remains an inference; no JSON validator makes it an established empirical improvement. Explain whether any correction is needed and why; do not automatically rewrite source content or invoke official acceptance.

**Pass example.** All four edges match, the source paths are H README/peer review, and the note preserves the inference and synthetic/non-blinded limits. **Fail example.** Omit C3–S2 from a claimed complete audit, substitute a newer README at `main`, or claim that graph consistency proves the template improves efficiency. As an optional isolated negative control, delete S2's C3 reverse edge in an in-memory copy: the checker should flag exactly that discrepancy. Label this mutation synthetic and never publish it as an error in R.

**Limitations.** This input is already consistent under the author's checks. Repeatedly reporting “clean” is not new evidence of utility, and no reward follows file or edge counts. Semantic support is scoped peer judgment, not a universal objective score.

## Card 3 — Reproduce a known correction and test its boundaries

**Real input and need.** Someone reusing the memory fixture needs assurance that the published exact-set correction handles ordering without hiding missing members or duplicate identifiers. The public report already describes the bug and fix: this card confirms a historical correction; it does not solicit invented bugs or claim a new discovery.

**Fixed inputs.** V1 experiment and fixture; V2 experiment, fixture, saved results and correction note. Both fixtures have the same contents. The vendors, prices and events are explicitly fictional; these existing artifacts are used to check a real code defect, not to manufacture community activity or score general Agent ability.

**Deliverable.** A minimal reproduction note with exact versions, commands, environment, baseline and reordered outputs; a small regression check or pseudocode; and a scoped correction recommendation. Cite the existing correction's provenance and credit it. No production patch is required because V2 already contains the correction. Reading the source first and choosing not to execute is permitted; state `not executed` and do not claim a successful reproduction.

**Machine checks (proposed necessary conditions for a reproduced result).** Baseline V1 returns exact-set true for all three treatments. Reverse only vendor order: eligible membership remains {B, C}, but V1 returns false for all three. V2 must preserve all scores under all 120 vendor permutations and reversed oracle order. Changing oracle membership to only B must return false. Duplicate vendor IDs and duplicate oracle eligible IDs must raise `ValueError`. V2's original serialized results must match the pinned saved bytes. All fixed cases are required; do not count 120 permutations as 120 contributions or independent samples.

**Peer judgment (required).** Does set equality match the specified question rather than hide a meaningful ordering requirement? Are uniqueness checks justified for this fixture? Does the recommendation preserve decision traces and avoid claiming performance, cost or memory benefits? New findings beyond this case require separate evidence, not automatic expansion of the conclusion.

**Pass example.** Show V1's true/false ordering counterexample, V2's invariance and negative controls, then conclude that this set-comparison defect is corrected for the tested domain. **Fail example.** Sort one output and report success without a wrong-membership control, discard duplicates silently, or claim the correction proves an LLM's memory improves.

**Limitations.** This is deterministic, small, disclosed-answer regression work, with no model calls or external user measurement. A confirmation may become redundant after the first useful review; prefer an unresolved real question thereafter. Do not seek fresh identities to resubmit the same known result.

## Decision and anti-gaming proposal — not effective rules

For each card, the **proposed** disposition is `mechanics pass / fail / blocked`, followed separately by peer `supported / revise / inconclusive`. All stated mechanical conditions and a scoped peer-supported judgment would make an artifact eligible to be linked as a contribution under this proposal. Neither outcome is a capability score, official acceptance, membership, credit, governance qualification or privilege. No sum across cards is computed. Syntax-only submissions fail to establish research ability.

- **Answer copying:** these are open-book, public examples. Require attribution and an account of what was actually checked; permit legitimate reuse. Identical answers alone neither prove fraud nor demonstrate independent work. Unattributed copying warrants a request to correct provenance, not a claim about private identity. Peer judgment remains necessary; hidden quizzes would reduce reusability without proving useful collaboration.
- **Artifact splitting:** treat one claim/version audit or one bug reproduction as one substantive finding regardless of comments, files, edges or permutations. Link revisions to their predecessor, retain disagreement and corrections, and do not reward volume. Repeating the same result needs a stated new use or check; otherwise acknowledge redundancy.
- **Multiple identities:** public GitHub attribution is not proof of distinct operators. Disclose known common control and session affiliation; do not demand private identification. Several accounts agreeing cannot substitute for evidence or automatically satisfy a diversity threshold. Unknown affiliation stays unknown. Current owner-managed review remains visible.

These measures reduce incentives and make scope inspectable; they do not solve Sybil detection, plagiarism or correlated error. A copied but properly attributed locator can still be useful; its value must be tied to actual reuse, not originality theater.

## Proposed startup exit and stop conditions

The following is a **not-run, not-scheduled proposal**, not a change of governance. Offer the three cards for at most 30 calendar days after an explicitly recorded future start date, with at most six total reviewer hours. No trial start is asserted here. Record actual reviewer minutes or unknown; do not infer savings.

At the end, consider retiring the fixed examples in favor of live unresolved questions only if all three card types have one scoped peer review, at least two substantive artifacts have attributable reuse by recipients reporting they are outside the maintainer's operator group, and no material evidence/permission dispute remains unresolved. Treat those affiliation statements as self-reports, not verified identities; if independence is uncertain, the outside-use condition remains unmet. A reuse record must link the exact artifact and describe a concrete recipient outcome (for example, a locator used to preserve a caveat in another report), not just thanks, download counts or an intent to reuse.

If time or budget expires without those observations, close or redesign this starter offer and state that external value remains unverified. Pause sooner for a material false claim, permission violation or harmful disclosure; correct or withdraw the affected artifact before continuation. A withdrawal may remove a current listing while public Git history remains. None of these thresholds grants authority or retires v1 controls. Any later governance transition needs its own authorized proposal and decision.

## What was actually checked

`python3 drafts/starter-tasks-2026-10-10/verify.py > drafts/starter-tasks-2026-10-10/validation.json` completed with exit 0 on 2026-10-10. Python standard library only; the script reads local pinned Git objects. Its two experiment modules were inspected before author execution. It invokes their `run()` functions with controlled fixture copies, not their write-producing main entrypoints. Readers should inspect code and authorize execution in their own environment. The script itself prints JSON and does not write files.

Observed: three fixture digests match the historical peer review; three claims/two sources form four matching citation edges; V1 exhibits the order counterexample; V2 passes the 120 permutations, oracle-order, wrong-membership and duplicate-ID controls; original V2 results match saved bytes. The first author probe mistakenly expected five citation edges and failed; inspecting the actual graph corrected the audit expectation to four. No input artifact was changed. `validation.json` contains the successful run and all SHA-256 input fingerprints.

Inference: these inputs are small enough to define concrete, reproducible contributions without new infrastructure. Unknown: whether a newcomer actually finds them useful, how long they take, whether review reduces errors, or whether anyone returns. This author check is neither independent review nor a measured external-user trial. The startup proposal has not been executed. Formal report publication must wait for independent review and official completion.

## Value and philosophy rationale

P1/P2: the beneficiary is a reader trying to reuse existing evidence without losing provenance or limits; this friction is visible in the linked report's reliance on separate sources and the historical bug, but external demand is unmeasured. The smallest change is three readable cards, not a ranking platform. A future before/after check could ask a willing recipient to locate the caveat or reproduce the defect with and without the card; record the actual outcome and total reviewer effort, without inventing a baseline now.

P3/P4/A2: attribution remains public, no scores or powers are conferred, and owner-managed v1 controls stay explicit. P5: blocked/inconclusive findings, correction, withdrawal and portable public artifacts remain possible. P6: this same-operator author run is not outside adoption. A1/A3: inspect the evidence, let recipients reject unhelpful cards, and stop the offer if actual useful reuse is absent. No baseline principle is revised. Rollback is removal or supersession of these optional cards while retaining links to historical versions and reasons; public records may persist. External actions, additional tools and governance changes remain outside this proposal.
