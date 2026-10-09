# Public Governance Rules Implementation Plan

> Execute in this session task-by-task; use executing-plans and an independent code review before merge.

**Goal:** Publish the approved governance direction as an explicitly inactive draft, accessible to people and Agents.

**Architecture:** A repository-owned JSON document is the content source. A small stdlib renderer produces escaped HTML and Markdown plus a JSON index. Existing static build and GitHub Pages deployment publish these alongside the unchanged v1 protocol.

**Tech Stack:** Python 3.9+, standard library, existing static CSS and unittest.

## Global Constraints

- No dependencies, no activation of autonomous permissions, no fabricated contributions or votes.
- Draft status and null effective date must agree. Current v1 remains in force.
- Repository, deployment and compute control limits remain visible.
- Use a feature branch; preserve existing reports/tasks.

## Task 1: Public content and discovery

Files: create docs/governance.json and arc/governance.py; modify arc/site.py and tests/test_site.py.

- [x] Add a build integration test that follows agent.json resources.rules to rules/index.json, checks the draft has null effective_at, follows HTML/Markdown paths, verifies content in both, and confirms existing write_access remains owner-managed.
- [x] Run `python3 -m unittest discover -s tests -p test_site.py -v`; verify missing rules discovery fails.
- [x] Store version, status, effective_at, source proposal URL, sections and changelog in governance.json. Generate HTML and Markdown from identical section paragraphs, escaping all HTML. Reject any status other than draft or non-null effective_at in this phase.
- [x] Integrate build output rules/index.html, rules/index.json and rules/rules.md; add navigation, home and connect links. Use relative resource paths and preserve existing guide.md and skill.md.
- [x] Add a regression test that invalid governance metadata fails without replacing a previous valid site. Run full test suite.

## Task 2: Review and publish

Files: web/style.css if navigation needs mobile wrapping; docs/verification.md and this plan for evidence.

- [x] Build against a live verified task snapshot; inspect desktop/mobile rules page and link destinations. Fix any overflow without unrelated styling.
- [x] Request independent review of implementation against the approved spec; resolve actionable findings.
- [x] Commit and open a PR, attach it to the chat; require successful CI before merge.
- [ ] Deploy through existing Pages workflow. Fetch public HTML, Markdown, JSON and agent.json; verify content and draft status. Report live URL and explicitly distinguish publication from governance activation.
