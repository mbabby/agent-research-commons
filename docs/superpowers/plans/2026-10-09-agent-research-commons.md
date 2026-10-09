# Agent Research Commons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Publish a working, public research collaboration site on GitHub with a usable Codex task workflow.

**Architecture:** GitHub Issues hold structured task records. A Python standard-library CLI validates lifecycle operations and writes them through `gh api`. A static generator renders task snapshots, validated reports, Markdown and JSON for GitHub Pages. GitHub Actions builds only trusted main-branch code.

**Tech Stack:** Python 3.9+, unittest, HTML/CSS/vanilla JavaScript, GitHub CLI, GitHub Actions/Pages. No runtime package dependencies.

## Global Constraints

- Public read access; first-party Codex sessions only for official writes.
- User starts Codex sessions manually. No unattended model calls.
- One coordinator serializes assignments per study. Logical agent names are not authentication identities.
- Fact, inference and unknown are distinct; final reports require independent review and acceptance.
- Invalid data/API errors stop deployment and preserve the previous site.
- GitHub Pages project-subpath compatible; Chinese interface and stable English field names.
- All work stays in this new repository on `feat/research-commons` until verified integration.
- No invented completed research, fabricated citations, or fake independent reviews.

### Task 1: Task protocol and GitHub CLI

**Files:** `arc/__init__.py`, `arc/model.py`, `arc/github.py`, `arc/cli.py`, `tests/test_model.py`, `tests/test_cli.py`, `examples/task.json`.

**Interfaces:** `validate_task(task) -> None`; `transition(task, action, actor, operation_id, **fields) -> dict`; `validate_report(report, tasks) -> None`; `GitHub(repo).tasks() -> list[dict]`; `GitHub(repo).get_task(number) -> dict`. CLI entry is `python3 -m arc.cli` with `list`, `show`, `create`, `assign`, `start`, `submit`, `review`, `complete`, `block`, `release`, `cancel`, `sync`.

Task fields: `number`, `title`, `question`, `scope`, `exclusions`, `as_of`, `deliverable`, `acceptance`, `parent` (null/integer), `status`, `agent_id` (null/string), `coordinator`, `attempt` (integer), `updated_at`, `history` (event array). Events record `action`, `actor`, `operation_id`, `at`, `attempt` and relevant operation fields. Submission includes HTTPS `artifact_url`; review includes `verdict` (`pass`/`changes_requested`) and `notes`. Completion includes HTTPS `merged_url` and a reference to the passing review. Reviewer must differ from the assigned researcher. All state writes validate logical authority, current state and attempt.

Store the task as a fenced JSON block after marker `<!-- arc-task:v1 -->` in the Issue body, with readable introductory text. Update body and `status:*` label together in one Issue PATCH. Preserve non-status labels. `arc:task` identifies official tasks, but additionally require Issue author to equal configured repository owner. Body history is the authoritative control record. Unknown/unauthorized Issues are excluded; malformed official records fail synchronization. Regular comments never change state. Multi-host atomic assignment is out of scope.

`create --file PATH --operation-id ID` is idempotent by searching existing official task histories before creating. `assign NUMBER --agent ID --actor COORDINATOR --operation-id ID`, then `start/submit` with `--actor AGENT --attempt N`. `review` takes `--actor REVIEWER --attempt N --verdict ... --notes ...`; `complete` requires coordinator, passed review, same attempt and verified merged GitHub PR. `sync --output PATH` writes `{generated_at, repository, tasks}` after validation. CLI repo option defaults to `mbabby/agent-research-commons` and supports explicit override. No shell interpolation; use subprocess argv and JSON stdin. Fail nonzero on API errors.

Report fields for site consumption: `slug`, `title`, `summary`, `task_number`, `agent_id`, `attempt`, `as_of`, `published_at`, `claims` (array of `{id,kind,text,source_ids}` where kind is `fact` or `inference`), `sources` (array of `{id,title,url,accessed_at,published_at,supports,note}`), `unknowns` (string array), `method`, `limitations` (string array), `review` (`{agent_id,notes,review_url}`), `acceptance_url`, `revision`. Matching task must be completed with matching researcher/attempt and review identity. Source IDs and claim references must exist; every fact has at least one source; all links HTTPS or HTTP; reject unsafe slugs. Review/acceptance URLs must point to this repository's task or PR records, not unrelated pages.

- [ ] Write behavior tests first. Example:
  ```python
  assigned = transition(open_task, 'assign', 'host', 'assign-1', agent_id='researcher')
  with self.assertRaises(ValueError):
      transition(assigned, 'assign', 'host', 'assign-2', agent_id='other')
  self.assertEqual(transition(assigned, 'assign', 'host', 'assign-1', agent_id='researcher'), assigned)
  ```
- [ ] Run `python3 -m unittest discover -s tests -v`, observe absent functionality, implement and rerun.
- [ ] Cover release/reassignment rejecting stale attempts, independent review, changes requested followed by resubmission, unauthorized actor, invalid statuses, malformed evidence and idempotent operations.
- [ ] Exercise `gh` transport with controlled subprocess fixture responses; test real CLI failures/outputs without external mutations.
- [ ] Commit only task files after checks.

### Task 2: Static public website and safe report publication

**Files:** `arc/site.py`, `web/style.css`, `web/app.js`, `web/favicon.svg`, `tests/test_site.py`, `reports/`, `examples/snapshot.json`.

**Interfaces:** `build(snapshot, reports, output_dir, repo, guide_path) -> None` validates all records before replacing local output. `python3 -m arc.site --snapshot PATH --output dist` builds; published data URLs are `agent.json`, `data/tasks.json`, `data/reports.json`, `reports/<slug>.json`, `reports/<slug>.md`. HTML routes: root, `tasks/index.html`, `tasks/<number>.html`, `reports/index.html`, `reports/<slug>.html`, `connect/index.html`. All navigation is relative to page depth.

- [ ] Write generator integration tests with a hand-authored valid task and report. Verify a malicious title is escaped, unsafe evidence URLs fail, draft tasks are visible but draft reports are excluded, internal links resolve under a project subpath, and invalid input leaves the existing output untouched.
- [ ] Build a warm white / charcoal / muted orange research board with task rows, readable typography, status pills, restrained grid lines and a prominent Agent access entry. Use progressive enhancement for state filters; all content readable without JS. Include empty states instead of fake records.
- [ ] Generate JSON/Markdown from the exact validated report data. Include snapshot timestamp and canonical GitHub links. Do not copy environment/configuration values into output.
- [ ] Run `python3 -m unittest discover -s tests -v`; serve `dist` under the repository subpath and inspect desktop/mobile rendering and task filter behavior.
- [ ] Commit the website implementation.

### Task 3: Codex skill and operating documentation

**Files:** `.agents/skills/research-commons/SKILL.md`, `README.md`, `docs/protocol.md`, `AGENTS.md`, `tests/skill-evaluation.md`.

- [ ] Test a realistic claim/reassignment/review scenario without the skill using an independent evaluator; record misunderstandings.
- [ ] Write a focused repo-local Skill using the CLI's actual help and examples. Explain live state reads, coordinator confirmation, exact attempts, claim/evidence structure, separate reviewer and human authorization for external writes. Do not install globally or alter unrelated Codex settings.
- [ ] Add a complete copyable sequence using example task JSON and CLI commands. Publish the same guide for external Agent readers with repository-relative links resolved for the website.
- [ ] Validate Skill frontmatter with the skill-creator validator and independently forward-test stale-attempt and self-review scenarios.
- [ ] Commit documentation and Skill.

### Task 4: GitHub deployment and real research exercise

**Files:** `.github/workflows/pages.yml`, `.github/workflows/check.yml`, `reports/github-pages-agent-research.json`, `docs/verification.md`.

- [ ] Fetch official GitHub Pages/Issues/Actions documents for the bounded research topic. Record actual citations, access date, inferences and limits.
- [ ] Create public repository only after confirming it does not exist; push code and enable Pages Actions build. User has explicitly authorized implementation and publication on GitHub.
- [ ] Workflow uses main branch code, read-only contents/issues permissions for build, Pages/id-token permissions only for deployment, concurrency to serialize publication, and no untrusted PR execution with write credentials. Trigger main push, trusted issue changes and manual dispatch.
- [ ] Run a real issue workflow with researcher and separate verifier; preserve an actual returned-for-revision round. Produce and merge reviewed report PR, attach any created PR to this chat, mark task complete, and publish the verified report.
- [ ] Run complete unit/integration checks, inspect public HTML/JSON/Markdown, verify deployed URL and workflow success, and record evidence in `docs/verification.md`.
- [ ] Perform final code review, address findings, integrate to main and report site/repository links and manual start instructions.

## Progress

- Plan and interfaces written; implementation pending.
