# Community correction paths implementation plan

**Goal:** Make parallel corrections discoverable without widening supersession rights.

**Architecture:** Reuse the existing action builder and contribution schema; change the contribution view and two explanatory paragraphs. No parser or authorization change.

**Tech Stack:** Python 3.9+ standard library, static HTML and Markdown.

## Constraints

English interface; preserve Chinese/English posts. Same GitHub author restriction remains. Same-operator tests/review do not establish external adoption. No governance activation or score.

## Steps

- [x] Inspect current code, live questions and existing tests; baseline 74 tests pass.
- [x] In tests/test_collaboration_site.py update generated contribution-draft coverage to require two drafts. Decode them, replace their artifact placeholders, and pass author-A revision/author-B parallel/author-B revision through arc.collaboration.derive. Check valid/invalid outcomes and original-review retention.
- [x] Run `python3 -m unittest discover -s tests -p test_collaboration_site.py -v`; observe a failure because only one correction path currently exists.
- [x] In arc/community_views.py split the correction action into parallel evidence (supersedes=None) and own revision (supersedes=item issue); add same-account restriction and prose attribution guidance. Keep review/reuse drafts unchanged.
- [x] Add material review/reuse correction and incomplete-export guidance to docs/collaboration.md, preserving sensitive-data withdrawal and avoiding automatic supersession promises.
- [x] Run `python3 -m unittest discover -s tests -v` and build/inspect the corrected page. Have a separate session review the diff against the approved spec and exercise the documentation scenarios.
- [ ] Publish a clearly labeled same-operator discussion record, create a reviewed PR, integrate within existing authorization and verify deployed routes and links.

Rollback is a revert of this view/documentation change. Existing public records are preserved.

## Review result

A separate same-operator reviewer reran 74 tests and caught a documentation ambiguity: prose-only changes would leave the old JSON verdict active. The guide now explicitly requires updating the structured assertion first. Follow-up review found no remaining blocking issues. This is not external independent review.
