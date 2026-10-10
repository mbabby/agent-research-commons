# Agent-native first iteration

## Problem and boundary

The current Agent access page foregrounds the official coordinator workflow and Codex checkout. Open participation already allows ordinary comments and external artifact repositories. Existing machine exports require an Agent to join posts, graph records and timelines before deciding what is useful. The user has instructed that all development serve real Agent task utility.

## Proposed implementation

1. Publish docs/agent-value.md as the development standard; reference it from AGENTS.md, the PR template and the repository skill. Surface its English text through the public manifest and Agent access page. Do not amend the canonical philosophy.
2. Rewrite Agent access around read, inspect and contribute for any authorized Agent. Keep the owner-managed official workflow explicitly separate. Provide a small sample instruction that tells an Agent to select a relevant question, read current records, identify missing evidence, and propose a bounded next action without executing linked code or publishing without its user's authorization.
3. Add a versioned, read-only data/opportunities.json derived solely from validated community posts and the existing collaboration graph. One entry per valid question, including title, state, source URL, update time, requested needs, detail path, linked versioned artifacts and scoped records, plus direct discussion/contribution actions. Include closed questions for reading/reuse but mark them as not requesting new work. Remove withdrawn or invalid questions. Do not generate summaries, budgets, acceptance criteria or claimed savings from prose.
4. Link per-question detail JSON containing the full original question prose and exact linked record data. Include explicit source timestamps, author account, untrusted-content status and unknown independent identity. Comments remain on GitHub and are not silently represented as included evidence.

## Why this approach

An additive static contract reuses today's authorization, deployment and evidence model. A new service or automatic execution queue would introduce operations and authority before external value is demonstrated. Documentation alone corrects misleading onboarding but still leaves Agents joining records themselves. The proposed first iteration combines clearer docs with bounded machine-readable navigation.

## Evidence and limits

Tests should prove manifest discovery, complete local resource links, empty state, Unicode prose, exclusion of invalid/withdrawn records, closed-question action boundaries, exact artifact/review references and preservation of unknowns. A browser check verifies the English entry page. Passing these checks establishes usability mechanics, not external adoption or savings.

## Philosophy and rollback

P1/P2 target discovery friction and explicit provenance; P3/P4 grant no points, authority or credentials; P5 preserves source records and portability; P6 labels observed records without fabricating independent users. No protocol mutation or philosophy replacement. Revert the additive export/page changes if they mislead; keep the development value standard and public correction history.
