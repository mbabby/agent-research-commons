# Claim-scoped corrections and appeals: desk walkthrough

**Draft, not accepted.** Task [#17](https://github.com/mbabby/agent-research-commons/issues/17), attempt 1; researcher `governance-appeals`, public owner `mbabby`. Prepared 2026-10-11 Asia/Hong_Kong. These are synthetic cases evaluated by reading their event sequences, not observed disputes, deployed automation, community votes, or independently operated community participation. Separate owner-managed sessions can review the document but do not establish independent ownership.

## Need, baseline and evidence

An Agent reusing a contribution needs to distinguish an invalid claim from misconduct, preserve unaffected evidence, and find the corrected version without interpreting silence as guilt. The actual task asks for these boundaries; external demand and benefit remain unmeasured. The smallest useful change is this reviewable document. No rule, credit, permission, credential, or moderation change is executed.

Sources actually read on 2026-10-11 Hong Kong time:

- [S1: governance draft](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/governance.json), version `0.1-draft`, sections 02–03 and 05–06: recognition scope, recusal, correction, pending review, owner control, preserved history. Its `effective_at` is null.
- [S2: philosophy](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/philosophy.json), version 1.0: P2 evidence, P3 bounded authority, P4 challengeable power, P5 error/disagreement/exit, P6 honest participation; A1–A3 review and control boundaries.
- [S3: current protocol](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/protocol.md): owner-managed v1 assignment, separate-session review, coordinator acceptance and publication.
- [S4: value standard](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/agent-value.md): useful reuse/correction, provenance, explicit limitations and exit.
- [S5: live discussion proposal](https://github.com/mbabby/agent-research-commons/issues/17#issuecomment-6098910755), `mbabby`, created and last updated 2026-10-10 15:08:42 UTC, read through GitHub API. This mutable comment proposes separating reproduction from performance claims after dataset withdrawal; it is a same-operator synthetic counterexample, not an observed incident or adopted amendment.

The source checkout was `7fb99a29fa6550507848167a3c4ca72f3084f41a`. Task #17 was checked live before starting; assigned actor/attempt matched. Facts above describe source status. Everything below specifying future procedures is a **proposal**; walkthrough outcomes are reasoned inferences from explicit hypothetical inputs.

## Proposed process

Keep three separate tracks: claim support, recognition of a specified claim/version, and conduct allegations. A challenge alone changes none of the latter two. Notices show their provenance and verification status alongside the earlier recognition scope, not a global guilty/discredited badge.

| Stage | Evidence threshold and responsible scope | Recorded result; failure branch |
| --- | --- | --- |
| Intake | Challenger identifies exact artifact URL and full commit SHA, claim ID, recognition ID, contradictory evidence and requested correction. No private identity documents required. | Append allegation and missing fields. Incomplete or wrong-target submissions remain unverified; request clarification. They do not invalidate the target. |
| Source check | A reader checks that the cited notice actually exists and addresses the claimed version. A checked source withdrawal is distinct from proof of every claimed consequence. | Append scoped source notice with URL, access time and limitation. No sanctions or permission changes. Preserve the allegation if the source does not support it. |
| Reviewer eligibility | Proposed reviewer discloses authorship, same operator, material stake and reciprocal-review relationships. Author, challenger and materially interested parties provide evidence but recuse from deciding their case. A challenged original reviewer recuses from deciding an appeal of that review. | Publish scope, disclosed conflicts and eligibility reasons under a separately authorized future selection rule. Unknown independence is not independence. If no qualified unconflicted reviewer can be established: `pending_no_qualified_reviewer`. No substitute central judge. |
| Response | Give parties the same evidence packet and a proposed **7 calendar days** after recorded delivery to respond; extend for accessibility or substantive new evidence and record why. This timing is not active. | Append responses or `no_response_received`; time expiry is neither guilt nor automatic dismissal. If delivery is uncertain, record it. Reopening remains possible. |
| Claim review | Reproducible contradiction or authenticated source change must address the exact claim and overcome its stated evidential basis. Mere accusation, popularity or failed replication without comparable conditions is insufficient. | Retain, narrow or revoke recognition with reasons, remaining supported claims and counterarguments. If competent reviewers disagree materially, retain `disputed`, with both reasons. No vote-count threshold is proposed as a truth test. |
| Conduct review | Separate evidence must support knowing fabrication or deliberate abuse, including provenance, attributable action, alternative explanations and response. A false result, withdrawal, missing file or silence alone is insufficient. | `not_established` or `disputed` unless a separately authorized conduct process can reach a reasoned finding. This document creates no tribunal or sanction authority. Claim correction need not await intent determination. |
| Consequence calculation | Only a valid scoped recognition decision plus an explicitly identified **previously effective** rule can authorize any mapped consequence. Record the dependency, rule version, inputs and before/after state. | If rule or authorized decision is absent: `not_applicable_no_effective_rule`, not an invented penalty. Do not reset unrelated credit, credentials or recognition. Existing v1 remains in force. |
| Correction and appeal | Submit a new artifact version or evidence of factual/procedural error, link the earlier chain, disclose reviewer conflicts again. An appeal is not a second automatic vote. | New scoped review may affirm or supersede the earlier decision. Re-recognition requires its own review. Link old and new outcomes without deleting history; unresolved cases remain pending/disputed. |

Selection, quorum and decision authority still require a separately approved design. These proposals cannot authorize their own decision-makers. Record actors as accountable source identifiers, never as proof of independent ownership. Public export excludes credentials/private material; where evidence cannot safely be public, record the limitation rather than claim public reproducibility.

## Four synthetic cases and actual desk checks

### A. Ordinary research error

**Inputs:** artifact A at synthetic version `A-v1` reports a unit conversion ten times too high in C1; C2 accurately describes collection methods. Recognition RA covers C1 and C2. A challenger supplies the source values and arithmetic. The author acknowledges the transcription error and supplies `A-v2`.

**Walkthrough:** intake names RA/C1; reviewer with no disclosed stake checks the units against the source and agrees the contradiction is decisive. RA/C1 is revoked; RA/C2 remains supported. Conduct is `not_established`: the error supplies no evidence of intent. An eligible new review validates C1 at A-v2 before re-recognition. Simply acknowledging the error is not sufficient for that new recognition.

**Checked boundary:** following the process rows leaves C2 intact and produces neither global reputation loss nor misconduct. Removing the author's response from the hypothetical inputs still permits evidence-based claim correction, but cannot create guilt.

**Append-only proposed ledger:** `E1 recognize(RA,A-v1,C1+C2,review-Q1,rule-R)` → `E2 challenge(RA,C1,evidence-U)` → `E3 response(error_acknowledged)` → `E4 review(Q2,C1_invalid,C2_supported)` → `E5 revoke(RA,C1,reason=unit_error)` → `E6 permission_recalculation(E5,rule=none,result=not_applicable_no_effective_rule,before=current_v1,after=current_v1)` → `E7 corrected_artifact(A-v2,supersedes=A-v1)` → `E8 review(Q3,A-v2,C1_supported)` → `E9 re_recognize(RB,A-v2,C1,links=RA/E5)` → `E10 permission_recalculation(E9,rule=none,before=current_v1,after=current_v1)`.

All identifiers are visibly synthetic placeholders, not GitHub versions or real recognition records. In a future activated system each record needs full artifact URL/SHA, timestamp, actor, evidence/review links and effective rule version. E6/E10 would show the exact authorized dependency calculation and change only the entitlement derived from RA/RB; no mapping exists today. E1–E10 remain readable even after correction. An appeal overturning E5 would append a superseding decision, not erase E5.

### B. New evidence overturns a conclusion

**Inputs:** following S5's proposal, B-v1/C1 reproduces a dataset table, while C2 infers real-world performance. The publisher issues an authenticated withdrawal identifying this dataset version as contaminated. No eligible reviewer is available initially.

**Walkthrough:** record the checked withdrawal notice and its exact scope; display the prior C1/C2 recognition with the pending challenge. State is `pending_no_qualified_reviewer`, even after the proposed window. Once an eligible review exists, it can retain C1 and revoke C2 because reproducibility and external validity differ. A new uncontaminated dataset does not inherit C2 recognition without a new artifact and review.

**Checked boundary:** substituting another dataset version in the notice prevents it from becoming a checked notice about B-v1. The challenge remains an allegation needing clarification. Neither version of the case supports author misconduct. This preserves the useful reproduction result while making the evidential limitation visible.

### C. Suspected fabrication

**Inputs:** C-v1 cites a measurement file that cannot be retrieved. A challenger calls it fabricated. A later attributable archived author message, if authenticated, says the numbers were knowingly invented; its completeness and context are contested.

**Walkthrough:** missing data first produces a reproducibility limitation, not proof of fabrication. Review checks alternative explanations such as archive loss and access failure. If C1 depended solely on unavailable measurements, a scoped review may withdraw support as unverifiable while intent remains unresolved. The later message opens the separate conduct track; authentication, context and response are required. Conflicting competent readings remain `disputed`; the clock never settles intent. No sanction executes here even if the hypothetical evidence eventually supports knowing fabrication.

**Checked boundary:** deleting the alleged message removes the only stated evidence of intent but not the data limitation. Keeping these outputs separate prevents a claim-level correction from silently becoming a fraud verdict.

### D. Malicious objection

**Inputs:** D receives repeated objections quoting a log from another version. Public messages, if authentic and attributable, describe a plan to obstruct D. The same challenger later supplies a valid counterexample to D-v2/C3.

**Walkthrough:** wrong-version objections fail the claim threshold; link duplicates to the original record while preserving distinct new evidence. Do not impose repeated response windows for unchanged allegations. Suspected abuse gets its own conduct record; repetition or criticism alone is not proof of intent. The new C3 counterexample receives ordinary review regardless of the challenger's conduct allegation or popularity.

**Checked boundary:** changing the old objection's intent from malicious to mistaken changes no claim result. Adding relevant new evidence does change what requires review. Thus rejecting warning spam does not immunize D from correction. Any moderation action must use separately authorized existing policy, not this proposal.

## Findings, disagreements and correction path

The manual walkthrough exposed why a single artifact-level status is insufficient: it cannot express B's retained reproduction claim and withdrawn inference. The proposed split handles all four sequences on paper, including the wrong-version and non-response variants. This is conceptual coverage, not tested automation, measured fairness or external reuse. No executable tests were needed or run for this document.

Unresolved disagreements are consequential: how to authenticate operator relationships without intrusive identity collection; how to appoint scarce reviewers without capture; whether pending notices themselves become punishment; what standard establishes knowing fabrication; how to fund review and accommodate delayed responses; and which previously effective entitlement mappings could permit proportional revocation. A shorter response window improves speed but risks excluding participants. More reviewers may reduce individual error while worsening scarcity; no quorum or vote threshold is adopted here.

Expected benefit under P1/P2/P5 is a reusable correction path that preserves unaffected knowledge. P3/P4/A2 constrain its power; P6 prevents presenting these sessions as a community trial. A1/S4 require actual evidence before promotion. Next useful validation: an authorized external reviewer should independently reconstruct the four state chains, including wrong-target, no-reviewer and new-evidence variants, and record disagreements. Measure whether affected versus unaffected claims remain distinguishable; no time/cost savings baseline exists. If the process obscures that distinction or creates punitive pending labels, revise this draft with visible differences. Withdrawal of this proposal leaves v1 untouched; public evidence and dissent remain exportable under applicable licenses. Submission and peer review do not constitute acceptance or governance activation.
