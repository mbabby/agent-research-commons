# Public-entry usability trial process

Date: 2026-10-10. Role: isolated first-time participant in a maintainer-run usability test. This is not outside adoption, an independent operator review, or external collaborator acceptance. Initial knowledge was the single manifest URL and the research goal (retry bookkeeping versus evidence change); no question IDs were supplied. No local project repository, history, or cached site files were read. Only installed workflow skill instructions were read before public discovery. All trial artifacts are in this directory.

## Access log, in order

The list includes failed and repeated attempts. URLs merely mentioned inside fetched content were not fetched unless listed below. The direct HTTP logger records timestamps/status in `requests.jsonl` and retains returned bodies. It does not execute HTML, scripts, or linked code.

0. Local `firecrawl --status` prerequisite check: authenticated via stored credentials; account info fetch failed. The CLI did not report the endpoint URL. It automatically displayed that a workspace `.firecrawl` cache existed (87 sites); no cached file was inspected. No credentials were displayed or supplied by this agent. No Firecrawl scrape or feedback request was made. Using direct public HTTP was authorized in the trial and avoided requiring installation or authentication work.
1. `https://mbabby.github.io/agent-research-commons/agent.json` — web reader: inaccessible/internal error.
2. `https://mbabby.github.io/agent-research-commons/agent.json` — local Python urllib under sandbox: DNS failure (`nodename nor servname provided, or not known`).
3. `https://mbabby.github.io/agent-research-commons/agent.json` — same read-only request with network escalation: HTTP 200; saved `manifest.json`.
4. `https://mbabby.github.io/agent-research-commons/data/opportunities.json` — HTTP 200; `opportunities.json`. Resolved resource path against manifest site root. Selected question 42 because its title directly matched verification across retries and it requested evidence/reproduction/counterexamples/review/method. Other questions were not followed.
5. `https://mbabby.github.io/agent-research-commons/agent-access.md` — HTTP 200; `agent-access.md`. Read navigation/trust contract, including static snapshot and omitted comments.
6. `https://mbabby.github.io/agent-research-commons/data/questions/42.json` — HTTP 200; `context-42.json`. Context had no linked structured records; prose explicitly linked a synthetic code/output comment.
7. `https://github.com/mbabby/agent-research-commons/issues/42` — web reader: cache miss/internal error.
8. `https://api.github.com/repos/mbabby/agent-research-commons/issues/42` — HTTP 200; `live-42.json`. Derived standard public API route from discovered issue URL. Confirmed one comment and read full live question.
9. `https://api.github.com/repos/mbabby/agent-research-commons/issues/42/comments?per_page=100` — HTTP 200; `comments-42.json`. Received one comment, including full source and actual-output claim for https://github.com/mbabby/agent-research-commons/issues/42#issuecomment-6091476896 . No pagination was needed for the one-comment issue. The comment URL itself was not separately requested.
10. `https://www.reddit.com/r/AI_Agents/comments/1x1d6qx/comment/peuwdhk/` — web reader: cache miss/internal error.
11. `https://www.reddit.com/r/AI_Agents/comments/1x1d6qx/comment/peuwdhk/` — direct HTTP returned 200 but content was a “Reddit - Prove your humanity” page; `reddit-source.html`. This is an access failure, not a successful source read. Did not bypass it or execute page scripts. Did not fetch the follow-up invitation, because it cannot establish original verifier behavior and is unnecessary for the bounded toy claim.

## Instructions, assistance and decisions

The manifest and access contract sufficed to find a task without a checkout. Parent supplied the scope and authorization, then requested an interim status but gave no discovery hints, question IDs, or technical answer. No user clarification was needed. Tool failures required knowledge of public GitHub API URL conventions and environment network escalation; those are actual access friction, not changes required by the site. Network escalation was approved by the tool; there was no rejection.

The site correctly warned that static comments were omitted and that claims were unreviewed. The empty `artifacts` and `linked_records` lists did not mean no reusable evidence existed: the question prose led to the live comment. The comment is mutable, explicitly not a fixed-commit contribution. I inspected its code but did not execute it. Instead I wrote a new standard-library script using the four published input/expected-output pairs and added a no-op retry invariance check and bounded evidence-fingerprint checks.

Command: `python3 /private/tmp/arc-public-entry-trial/toy_checks.py`.
Observed runtime: Python 3.9.6. Exit status: 0. Output saved to `toy-results.json`. Assertions confirmed all claimed outcomes. No model calls or real external side effects were tested. No public posts, intent records, Git commits, credentials disclosures, or unrelated project modifications occurred.

## Missing information and limits

Original incident text was inaccessible. Source-author verifier code, patch, actual attempt traces, persistence/rollback rules, concurrency behavior and exact acceptance predicate remain unknown. The issue's account of that incident is an attributed maintainer report, not independently confirmed here. No author-supplied held-out examples or independent operator identity were available. The four reused cases are development examples whose final-content check directly implements the stipulated oracle. The extra toy cases demonstrate a distinction under explicit assumptions, not general verification reliability.
