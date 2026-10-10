# Scoped peer review of the three starter task cards

Reviewed 2026-10-10 by `starter-review`, a distinct AI review session under the same public operator/account `mbabby`. The reviewer did not author these three files. Separate-session review is not independent operator identity, external adoption, or proof of practical benefit. This is a pre-submission review; no official review or acceptance operation has been performed by this file.

## Scope and live requirements

Reviewed `README.md`, `verify.py`, and `validation.json` in this directory, plus the exact local Git objects they cite. Read project AGENTS.md, research-commons Skill, protocol, philosophy and agent-value standard. Live `python3 -m arc.cli show 15` succeeded after retrying the initial sandbox network failure: task 15, attempt 1, `in_progress`, assigned to `starter-research`, coordinator `mbabby`. All four live acceptance criteria were inspected. No public record or Git state was mutated for this review.

Reviewed bytes (SHA-256):

- `README.md`: `3e6d1a993fd42ba80281457cdb4cfb41e9e50473662148f30aa35e3b47a65183`
- `verify.py`: `970d9a71ad2e8d645accc43bde36a085bd7e6535b8183ce24f6d0f5d47a3b163`
- `validation.json`: `cb656bb750b945dd95ff3db572517a35f13b7e1c7087f9b565093f2d3833b6e6`

Any changed bytes require renewed review. This assessment does not automatically follow a later commit or artifact path.

## Executed checks and source readback

I inspected `verify.py` and both pinned `experiment.py` modules before executing the verifier. Their import-time code defines functions and paths; execution calls the controlled `run()` functions, not the historical file-writing main blocks. The verifier uses local `git show`, standard-library imports and controlled fixture copies, with no network operation. This safety observation applies to these reviewed bytes only.

Using Python 3.9.6, I ran the verifier through `subprocess.run([sys.executable, "drafts/starter-tasks-2026-10-10/verify.py"], capture_output=True, check=True)` from the repository root and compared stdout directly against `validation.json` bytes. Exit was 0; all 5,738 output bytes matched exactly. No saved author result was overwritten. The reproduced results establish three fixture hash matches, three claims and two sources with four matching citation edges, historical true/false ordering counterexamples for all three treatments, corrected scores across all 120 vendor permutations, reversed oracle order, wrong membership rejection, duplicate vendor/oracle-ID rejection, and byte-identical corrected baseline results. These are deterministic regression observations, not independent experimental samples.

I separately read the following source bytes rather than relying only on the author's summary:

- Report R at `8f4dd3fffec27eb6f355c087f344d526c9f4a75e:reports/minimal-research-handoff.json`: C1/C2 are facts about the delivered records; C3 is explicitly an inference. Forward and reverse edges are C1–S1, C2–S2, C3–S1 and C3–S2. S1 and S2 are the exact H README and peer-review paths, not merely any paths under the same commit.
- H peer review at `98d9154452ffff904f7c361c389290a26cacbdcb:drafts/handoff-and-resume-2026-10-10/handoff/peer-review.md`: opening paragraph discloses separate session/same operator; “Actual recipient actions and results” documents the three matching hashes, prior reading of the author's walkthrough, discrepancy note and unsent request. This supports Card 1's limits. Same-operator wording comes from the source context and R's S2 note/limitations, rather than being literal wording of C2 itself.
- H README at the same commit: field rationale and recipient checklist support C1's package description and C3's bounded inference about preserving uncertainty and the next allowed action. Its desktop walkthrough explicitly keeps the conflict and unavailable-source cases unresolved. The pinned tree contains the template, both examples and all three fixtures. I read each fixture: two synthetic counts of 18 and 21 lack the completion definition; the third is a fictional unavailable-source note, with no primary bytes or dataset version. Those bytes establish no real count or outage.
- V1/V2 experiment modules and the pinned fixture: V1 compares eligible lists; V2 compares sets while rejecting duplicate identifiers and retaining ordered decision traces. The fixture's B and C satisfy the current max-price/region predicate; ordering is not an eligibility requirement. The V2 correction note explicitly credits a prior separate reviewer and labels the deterministic check's limits. This supports a bounded correction reproduction, not a new discovery or memory-performance conclusion.

The exact full source URLs and all input digests are retained in the reviewed `validation.json`; the paths above identify the inspected content without substituting live main. Public URL reachability was not tested by this review.

## Findings against acceptance

1. **Three usable, bounded cards: supported.** Each names exact inputs, deliverable, pass/fail examples and limitations. Evidence locating, citation/data consistency, and correction reproduction are separate activities. Fixed claims, edges and controlled cases make the workload inspectable. Machine conditions are distinguished from semantic peer judgment. A newcomer can obtain the source bytes and produce an artifact without a new platform or governance role; actual newcomer utility remains untested.
2. **Copying, splitting and multiple identities: supported as a proposal.** Attribution and actual-check disclosure permit legitimate reuse without treating copied text as ability. One finding cannot become many contributions through files/edges/permutations. Account agreement cannot establish independent operators. These are sensible constraints on interpretation, not a demonstrated anti-Sybil or plagiarism detector.
3. **Thresholds and exit: supported as unexecuted design.** The 30-day future window, six reviewer-hour bound, scoped reviews, two attributable outside-use artifacts and unresolved-dispute condition are concrete but explicitly proposed. Unknown affiliation leaves outside-use unmet. Expiry without evidence triggers closure/redesign; no threshold confers powers or changes owner-managed v1 controls.
4. **Evidence versus inference/proposal: supported.** The executed audit is recorded separately from usefulness hypotheses and the not-started trial. No savings, general research ability, outside adoption, membership or official acceptance is inferred. The rationale fits P1/P2/P5/P6 and A1–A3; P3/P4 retain attribution without authority and make current controls visible. Correction and optional withdrawal remain available.

No blocking content change was found for these reviewed bytes. Recommendation: suitable for submission and subsequent formal scoped review, not yet official acceptance or report publication.

## Unresolved limits and review boundaries

- `verify.py` is an author-input replay, not a general validator for a newcomer's answer. It does not assess semantic support, verify answer quotations/locators, or demonstrate that the proposed peer process works. I read source context separately; mechanical output alone is insufficient.
- Some verifier assertions are intentionally narrower than the cards: source URL checking in code checks the H commit prefix, while I checked the actual two paths against the card; the output's count of 120 is literal, while the loop plus five inspected vendors establishes the real permutation domain. This is acceptable for these fixed inputs, not evidence of a reusable schema/checking service.
- The historical recipient actions are documented source claims, not actions observed live by this reviewer. Hash consistency cannot prove independent identities, historical authorship or truth of synthetic numbers.
- I did not run a newcomer trial, time study, external-use observation, copying detector, identity investigation, live URL availability audit, or startup program. These remain unresolved rather than implicitly passing.
- This review adds no permission, credit, account isolation, community independence or governance transition. Formal review must target the actual submitted PR and current live attempt; completion remains a separate coordinator action after review and merge.
