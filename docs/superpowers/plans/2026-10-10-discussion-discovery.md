# Discussion Discovery Implementation Plan

Goal: expose recent comment metadata without mirroring bodies, and publish accepted starter cards.
Architecture: isolated activity fetch/validation/export integrated into existing site builder and Pages workflow; existing official research workflow for task #15.
Tech stack: Python 3.9+ standard library, GitHub CLI, GitHub Pages.

- [ ] Add focused red tests for activity eligibility, exact metadata URLs, failure behavior and bounded coverage; implement minimal fetch/validation.
- [ ] Add rendering tests for escaping, sorting, unavailable/empty distinction and links; integrate page and JSON resource, CLI and workflow. Document bounded metadata-only contract.
- [ ] Researcher starts #15, delivers three pinned task cards and validation notes; a separate session checks acceptance.
- [ ] Run full tests/live build, independent review, fix material issues, create and attach deliverable PR, submit/review/merge/complete #15.
- [ ] Publish a separately reviewed accepted report and link it from the Agent entry; correct #18's stale #14 listing.
- [ ] Verify deployment and final URLs, preserving unrelated drafts.
