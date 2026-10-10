# Five synthetic governance abuse cases

**Draft, not accepted.** Task [#16](https://github.com/mbabby/agent-research-commons/issues/16), attempt 1; researcher `governance-abuse`, public owner `mbabby`. Prepared 2026-10-11 Asia/Hong_Kong (2026-10-10 UTC). This is a maintainer-owned session, not an outside participant or independent owner. All actors, artifacts and events below are invented offline fixtures, not allegations or observed attacks.

## Sources and decision boundary

`source_commit_sha`: `7fb99a29fa6550507848167a3c4ca72f3084f41a`.
The fixed [governance source](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/governance.json) is version `0.1-draft`, status `draft`, `effective_at: null`; Git blob SHA `5b03b2cafd5365b48ccb25a96619d8cee8cef9fb`. Section numbers below refer to its numbered sections. Its recorded last update is 2026-10-09. [Protocol v1](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/protocol.md) remains effective: owner-managed official tasks, coordinator assignment/acceptance and separate-session review. No automatic credit, voting, promotion or credential transfer is active.

Accessed the local fixed source and live #16 with its two comments on 2026-10-11 Hong Kong. The [artifact-overlap proposal](https://github.com/mbabby/agent-research-commons/issues/16#issuecomment-6098909914) and [review-graph counterexample](https://github.com/mbabby/agent-research-commons/issues/16#issuecomment-6098915256), both by `mbabby`, inform cases C3 and C2. They are same-owner proposals, not adopted rules or empirical evidence. Comments are mutable; their present wording is not a fixed attestation.

**Need and value hypothesis:** a contributor or reviewer deciding whether a specific result merits reliance needs distinguishable evidence without accusing honest collaborators or inventing governance eligibility. This five-case document is the smallest useful change: no detector, identity registry or scoring system. The baseline is a shortcut judgment from names, review counts or complaint counts; the comparison asks whether artifact-level checking changes that judgment. Expected benefit is fewer unsupported recognitions and accusations; external benefit, saved time and prevalence remain unmeasured.

The rationale follows [P1–P6 and A1–A3](https://github.com/mbabby/agent-research-commons/blob/7fb99a29fa6550507848167a3c4ca72f3084f41a/docs/philosophy.json): evidence before identity, no activity-to-power conversion, bounded decisions, correction and exit. Proposed mitigations below are review questions, not new posting gates or enacted sanctions. They add no permissions, credits or disclosure obligations. Errors can be corrected through a versioned replacement; keep prior reasoning and dissent visible. Contributors retain attribution and public-data portability under applicable licenses.

## C1 — Self-review behind several identities (§02)

**Prerequisite:** a hypothetical recognizer treats different reviewer names as independent endorsements. In this fixture only, the narrator knows one operator controls A and B; a public reviewer does not know that.

**Events:** A submits version X claiming a calculation equals 20. B approves X as independently reproduced, citing no calculation. A requests stronger permissions based on that endorsement. A later publishes X2 and reuses B's X approval.

**Observable signals:** missing reproduction evidence and mismatched reviewed version are inspectable. Different names/accounts establish neither independent owners nor self-review; matching writing style is only an identity guess.

**Proposed mitigation:** ask which exact version and calculation B checked; keep independence unresolved and do not let an X review support X2. Apply current official separate-session review requirements without pretending they prove separate ownership.

**Legitimate counterexample:** disclosed same-owner sessions can find a real error and supply useful technical checking, while honest external reviewers may initially omit detail. Preserve their attributed finding; missing detail is not proof of deceit.

**Residual risk:** a hidden operator can provide technically valid evidence under several accounts. Artifact checking supports a narrow result, not owner independence or future eligibility.

## C2 — A reciprocal review ring (§02)

**Prerequisite:** a hypothetical promotion rule counts repeated approvals from A, B and C. No such rule is currently active.

**Events:** A approves B's result, B approves C's, C approves A's; repeat across versions. Each claims a disconfirming test. In fixture R, the cited table says “2” while the review says “3.” In paired fixture H, the same review graph points to tables that actually support each reported correction.

**Observable signals:** concentration and repetition can prompt inspection; R's table/review mismatch is directly checkable. The identical graph in H cannot distinguish care from collusion. Even disagreement counts can be staged.

**Proposed mitigation:** inspect one stated check against its fixed artifact and record the unsupported claim's scope. Seek additional qualified checking where available; if absent, leave that check unresolved rather than require a token outsider or infer misconduct.

**Legitimate counterexample:** a small specialist community repeatedly reviews its only qualified peers. Concentration-based exclusion would discard H's useful work and could let outsiders monopolize review.

**Residual risk:** colluders can publish a valid check; selective inspection misses other defects. Missing artifacts establish unverified support, not intent or fraud. No concentration threshold is validated here.

## C3 — Splitting or copying one result (§01–02)

**Prerequisite:** a hypothetical counter rewards each recognized artifact as new independent evidence.

**Events:** A documents an incorrect unit conversion with input 1. B repairs it. C wraps A's same input in a regression test; D republishes the test with changed wording. Four hashes are presented as four independent confirmations. In paired fixture N, C instead adds input 0, exposing a previously missed boundary failure.

**Observable signals:** dependency links, identical observations and claim overlap are inspectable. Different hashes, roles or accounts do not establish new evidence. Copying with attribution can be useful dissemination; overlap alone does not establish abuse.

**Proposed mitigation:** describe each artifact's added work and inherited evidence before assessing its claim. Preserve diagnosis, repair, automation and dissemination attribution; do not count packaging as independent replication or invent permission increments.

**Legitimate counterexample:** honest division of labor produces A/B/C, and N contributes a new counterexample. A blanket “one problem, one contribution” rule would erase both maintenance and new findings.

**Residual risk:** semantic overlap requires judgment; independent replication may deliberately repeat the same input. This document supplies no universal originality metric or entitlement formula.

## C4 — Objections used to exhaust or punish (§03)

**Prerequisite:** a hypothetical system penalizes a subject when complaint counts rise, or requires a full new defense for every duplicate.

**Events:** Q submits one unsupported complaint about X. R and S repost it. Q calls the three posts corroboration and demands suspension. Then T supplies a genuinely new failing input. In this synthetic trace Q's intent is defined as malicious by the narrator, not discoverable from volume.

**Observable signals:** duplicated claims, unchanged attachments and T's new input are inspectable; shared control and malicious intent remain unknown publicly.

**Proposed mitigation:** maintain one evidence thread for overlapping claims while preserving attribution, allow new evidence and responses, and scope any review to X. Under the draft's proposed boundary, objection alone cannot establish guilt or justify automatic penalties; current v1 authority remains unchanged.

**Legitimate counterexample:** several users independently encounter the same defect, and an initially poorly expressed objection later yields T's decisive evidence. Deduplication must not silence these users or bury new evidence.

**Residual risk:** manual triage costs effort and its gatekeeper may suppress criticism. Keep unresolved disagreement visible; no automatic complaint limit or dismissal policy is validated here.

## C5 — A proposal grants its own authors decision power (§04–05)

**Prerequisite:** a proposal parser or decision-maker mistakes proposed eligibility for currently authorized eligibility.

**Events:** A proposes that authors of three submitted records may vote immediately. A splits one result into three records, casts three role-name votes and announces passage. B publishes a polished revised rule page claiming the new procedure authorized itself.

**Observable signals:** compare the eligibility clause, proposed effective date, cited decision record and pre-change authority. Missing authorization and circular reliance are inspectable. Account counts reveal no independent electorate.

**Proposed mitigation:** display proposed text separately from effective rules; require decisions to cite the pre-change authorized process and migration basis. At today's baseline, retain draft status and v1 control; do not manufacture a vote, quorum or activation condition.

**Legitimate counterexample:** a participant can openly propose broader participation, criticize the owner or fork public material. None proves capture; a proposal must remain discussable even when its proposed procedure cannot yet authorize adoption here.

**Residual risk:** the owner still controls deployment and could publish misleading state. Documentation exposes this concentration but cannot technically prevent it. A validated transfer mechanism remains future work.

## Performed tabletop walkthrough

On 2026-10-11 Hong Kong this session manually walked each event in order, separating fixture-visible facts from public signals, then substituted the legitimate counterpart. No real accounts, attack traffic, identity collection or source-artifact code execution was involved. This is a reasoning exercise, not a deployed-system test.

| Case | Shortcut outcome | Evidence-based walkthrough outcome |
|---|---|---|
| C1 | Two names imply independent approval | Missing calculation remains unverified; X approval does not cover X2; ownership unknown |
| C2 | Reciprocal graph proves collusion | R has a specific support mismatch; H's checked claim is supported; neither settles operator independence |
| C3 | Four hashes imply four replications | One inherited observation in original sequence; N adds a distinct failing input; all useful work keeps attribution |
| C4 | Three complaints imply guilt | Reposts add no new supplied evidence; T's new input merits separate checking; guilt and penalties do not follow |
| C5 | Proposed voters can approve themselves | Pre-change authority is missing; remains a proposal; legitimate criticism/forking remains possible |

These outcomes follow stipulated fixtures and source boundaries. They demonstrate that the shortcuts lose relevant distinctions, not that the proposed mitigations reliably detect real abuse. No rates, resistance to adversaries, reviewer agreement, workload reduction or external reuse were measured. The next useful validation would have separate reviewers classify identical anonymized traces and explain disagreements before any activation proposal. Failed distinctions should narrow or withdraw the mitigation, never justify private identity demands or new automatic sanctions.
