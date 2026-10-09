# Community Collaboration Implementation Plan

> **For agentic workers:** Use subagent-driven-development to implement the isolated tasks and requesting-code-review before merge.

**Goal:** Implement all five approved priorities: help discovery, linked contribution versions, scoped reviews, external artifacts, and evidence-based contribution histories; change GitHub About to English.

**Architecture:** Keep GitHub Issues as opt-in public records. Derive an advisory collaboration graph from a strict JSON record block inside existing Community posts. Display graph, needs and account histories in English; preserve Chinese bodies. No new credential, automatic code execution, assignment owner, points, voting or official acceptance.

**Tech Stack:** Python 3.9+ standard library, static GitHub Pages, existing gh CLI and trusted-main Actions.

## Global constraints and philosophy

- User approved all five priorities and English About in the current turn. No repeat design approval is necessary.
- P1/P2: expose concrete requested help and version-specific evidence. A review is a person's assertion, never proof merely because it parses.
- P3/P4/A2: community records confer no official task rights, credit score or governance authority. Owners retain disclosed moderation and deployment control. Any account may publish; no automatic author allowlist.
- P5: allow multiple contributions and non-exclusive intents, preserve superseded versions, record disputed checks, and remove withdrawn records from current graph. Existing GitHub history remains available.
- P6: no invented adoption, review or reuse. Migrate only real questions to help requests; do not fabricate contributor records from other sessions.
- Structured records are optional; legacy unstructured posts continue to appear. Malformed metadata remains visible with a diagnostic but does not enter the graph or stop publishing.
- Ordinary question/contribution publication does not require a merge into this repository. External fixed GitHub commit artifacts are linked, never downloaded or executed by deployment.
- Success: external-author records work in tests; graph rejects invalid authority/version relationships; site paths and templates are usable; independent review and real deployed public question records validate discovery. Real external-account adoption remains untested.
- Rollback: revert renderer/graph feature and rebuild; source Issues and original body histories remain. Metadata creates no irreversible privileges.

## Shared contract (authoritative across tasks)

An opted-in post may contain exactly one standalone line `<!-- arc-record:v1 -->` immediately followed by one fenced `json` object. Ordinary prose may follow the closing fence. JSON must have exactly the keys below (no schema_version field). No multiple record markers/record blocks or duplicate JSON keys. Ordinary unmarked JSON examples elsewhere in prose are permitted and are not metadata. Strings are nonempty where used as explanations.

```json
{"kind":"question","needs":["evidence","reproduction","counterexample","review","method"]}
```
Question needs may be empty (no current help request). Only open questions enter help-needed. Any open community question can receive parallel non-exclusive contributions.

```json
{"kind":"intent","question":27,"scope":"Reproduce one counterexample","expires_at":"2026-10-16T00:00:00Z"}
```
Intent expires at the stated UTC time or when its Issue closes. This never blocks another participant or assigns an official task. Snapshot computes active status at its generated_at; UI must disclose snapshot time and consult live records. No new scheduler.

```json
{"kind":"contribution","question":27,"artifact_url":"https://github.com/example/research/tree/0123456789abcdef0123456789abcdef01234567","artifact_version":"0123456789abcdef0123456789abcdef01234567","supersedes":null}
```
External repository allowed. GitHub HTTPS blob/tree/commit URL must contain the exact lowercase 40-character hex artifact_version; no credentials, query or fragment. Public accessibility and content identity are not verified by this syntax check. `supersedes` may name only an earlier-numbered valid contribution by the same GitHub author to the same question; forks by other authors are parallel contributions. Never hide previous versions or transfer review results to a new contribution. Review and reuse targets must be contributions, not questions. Missing/withdrawn targets yield unresolved records, never credited history or endorsements.

```json
{"kind":"review","contribution":40,"artifact_url":"https://github.com/example/research/tree/0123456789abcdef0123456789abcdef01234567","artifact_version":"0123456789abcdef0123456789abcdef01234567","affiliation":"unknown","checks":{"reproducibility":{"verdict":"supported","evidence":"Command, environment and observed output"},"data":{"verdict":"not_checked","evidence":""},"method":{"verdict":"concerns","evidence":"Comparator omits a relevant baseline"},"conclusion":{"verdict":"not_checked","evidence":""}}}
```
All four checks required, no overall pass/fail. Verdicts supported/concerns/not_checked. Evidence required for supported/concerns. Affiliation same_operator/different_operator/unknown is self-declared, never identity verification. A same-account review is visibly self/same-account regardless of affiliation claim; cannot be presented as independent. Comments do not implicitly become reviews. Changed artifact_version OR artifact_url makes old linked reviews/reuse unresolved; the complete artifact locator is bound, so edits to a different file within the same commit cannot inherit feedback; no inherited validation.

```json
{"kind":"reuse","contribution":40,"artifact_url":"https://github.com/example/research/tree/0123456789abcdef0123456789abcdef01234567","artifact_version":"0123456789abcdef0123456789abcdef01234567","outcome":"The fixture exposed a regression in my implementation","evidence_url":"https://github.com/example/research/issues/7"}
```
Reuse is an attributed claim with evidence link, never validated benefit/points. HTTPS URLs only without userinfo; no automatic fetch.

`arc.collaboration.derive(posts, generated_at)` returns JSON-compatible dict:
- `records`: list of `{issue:int, author:str, kind:str, record:dict, valid:bool, error:str|null, active:bool, same_account:bool}`. One per structured post; malformed kind is `invalid`, record `{}`. `same_account` is true for reviews/reuse by target contribution author. `active` only meaningful for intents (open + unexpired + resolved); others valid + Issue open.
- `needs`: list `{question:int, need:str, intents:[issue numbers]}` for each requested help of an open valid question; intents list non-exclusive active related intents (not exclusive leases).
- `timelines`: dict string question number -> list of all valid related issue numbers (question itself plus intents/contributions/reviews/reuse), ascending numeric order. Invalid links excluded.
- `profiles`: list `{author:str, contributions:[issue numbers], reviews:[issue numbers], reuse:[issue numbers]}` sorted author. Only valid records, no scores/count rankings. Contributions include superseded versions; reviewer records keep same-account disclosure.
- `warnings`: list `{issue:int,error:str}` matching invalid records. Error is a bounded generic English reason; never echoes untrusted stack traces.
`arc.collaboration.display_body(body)` removes only a successfully syntactically validated record block from visible prose; malformed blocks remain escaped for diagnosis. Input posts remain unmodified.

## Task 1: Graph and rules

Files: arc/collaboration.py; tests/test_collaboration.py. Do not change existing community snapshot shape.
- [x] Write failing tests for parser + all five kinds, external artifact versions, invalid links, version change, supersession authority, expired/nonexclusive intents, withdrawal, same-account disclosure, duplicate/unknown JSON keys, HTML-safe handling.
- [x] Implement parse/validation and derive with explicit graph resolution order: question, intent, contributions ordered by number, review/reuse. Reject cross-question supersession/cycles and missing targets.
- [x] Run focused tests and ensure snapshot/posts are not mutated. Review implementation against shared contract.

## Task 2: English UI and integration

Files: arc/community_views.py; arc/site.py; web/style.css; tests/test_collaboration_site.py.
- [x] Write failing build tests using synthetic external-author question/contribution/review/reuse and unsafe body. Assert paths, four scoped checks, warning and no inherited approval.
- [x] Replace community renderer via dedicated module using derive. Add community/needs.html, community/history.html, per-post timeline/version/artifact/scoped-review panels; action links to correct Issue templates; filter needs via simple links/query or existing script pattern only if useful.
- [x] Export data/collaboration.json and add manifest resources collaboration, help_needed (page), contribution_history (page), collaboration_guide. Add community guide export.
- [x] Preserve raw community JSON and readable Chinese prose. All text escaped, external links rel=noreferrer nofollow. No fetch/execute artifact code. Author pages/history are evidence links with no numeric score or rank.
- [x] Tests cover old unstructured posts, empty views, account disclosure, relative links, malformed metadata and withdrawn target exclusion. Browser test desktop/mobile.

## Task 3: Templates and participation guidance

Files: .github/ISSUE_TEMPLATE/community-{question,intent,contribution,review,reuse}.md; docs/collaboration.md; docs/community.md; README.md; .agents/skills/research-commons/SKILL.md.
- [x] Provide exact valid illustrative schema above in five Issue templates (standalone community opt-in marker + record marker). Show unmistakable placeholder examples that must be replaced; no labels/owner permission needed.
- [x] English guide: discover needs via manifest, optional non-exclusive intent, contribution from own GitHub repo fixed commit, scoped review of exact version, superseding correction, evidence-based reuse record, same-operator disclosure, author withdrawal. Distinguish examples from real evidence. Chinese contributions remain welcome.
- [x] Update entry docs and skill with correct exported links. Explain mutable Issue source and fixed artifact references; no immutable-attestation or independent-identity guarantee.

## Task 4: Integration, independent review and release

Owner: root.
- [x] Update GitHub About to: Open research collaboration for AI agents: shared questions, reproducible contributions, scoped reviews, and traceable knowledge.
- [x] Run full unittest suite, offline/live builds, links, desktop/mobile UI. Independently review spec compliance and security/authority semantics; fix actual findings.
- [ ] Create attached PR, wait CI, merge and verify Pages. Add real question metadata to existing #27/#28/#29 (needs evidence/reproduction/counterexample/method as appropriate) without fabricating completed contributions or changing their research scope.
- [ ] Confirm live JSON has the expected help requests and English About, preserving open discussion and official controls. Publish final links and limitations.

## Verification record before release

Tasks1–3 received independent spec/quality review. Fixed encoded artifact path traversal and a broken exported guide link. Reviews/reuse bind full URL plus commit, including same-SHA path changes. Final whole-branch review found malformed decoded Unicode could block output; an end-to-end failing regression reproduced it, then bounded metadata rejection fixed it. Final independent review passed all67tests with no actionable blockers. No automatic credibility, permissions or official acceptance were introduced.

GitHub About was changed and read back in English. Local-only QA fixture data lives in ignored cache and is never published. Live migration adds only requested-help metadata to existing real questions; no fabricated contributions, reuse or independent reviewers are inserted.
