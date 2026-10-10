# Community correction paths

Approved by the maintainer in chat on 2026-10-10 after three same-operator subagents inspected entry, evidence and governance separately and exchanged objections. This is a maintainer-directed implementation decision, not an independent community vote or proof of external adoption.

## Need and evidence

At baseline 4bd284b, the contribution panel universally offers “Publish a corrected version” with supersedes prefilled. The parser accepts supersession only by the original GitHub author. A different author retaining that draft value creates a public but structurally invalid record. Plain comments, manual edits to null, and parallel contributions already work. No external participant was observed failing this path; #51 had zero comments when inspected.

## Approved design

Keep the parser, schema, permissions and ordinary comment entry unchanged. The static page cannot identify its visitor. Offer “Publish parallel evidence or a correction” with the same question and supersedes=null, alongside “Revise your own contribution” with the existing supersedes value. Explain the original GitHub account restriction and ask parallel contributors to identify the disputed record in prose. Both drafts still require a new fixed artifact reference; neither imports old review results.

Add two brief sections to the existing collaboration guide: material review/reuse corrections should identify the date, earlier and current assertion, reason/evidence and exact affected artifact; exports are snapshots, not full research archives, and exclude comment bodies and external artifact files. Preserve withdrawal and sensitive-data removal; no ceremony for spelling edits, no automatic review/reuse supersession.

## Alternatives and boundaries

Renaming alone is smaller but still leaves external authors searching for a valid path. Relaxing parser authorship would grant control over another author's revision chain and is rejected. New review state machines, comment ingestion, credit and governance activation are deferred. Closed-question detail actions are a separately observed issue outside this approved change.

## Value and power review

P2/P5: make counterevidence and corrections reachable and attributable. P4: retain the same-author supersession boundary. P1/P6: fix a demonstrated mechanism rather than manufacture activity; no claim of external benefit. P3/A2: no scores, roles, identity assertions or new authority. A1: tests and review evidence accompany this design. A3: reduce the need for maintainer explanation while preserving external artifacts and exit. Revert presentation/documentation if confusing; never rewrite posted participant history as rollback.

## Acceptance

Decode both generated drafts. After replacing artifact placeholders, another author’s parallel record resolves; the original author's revision resolves; another author using the revision draft is still rejected. Old review evidence stays attached only to its original contribution. Read the documentation as a participant correcting a material verdict and leaving with an export: it must expose the manual work and missing material without promising immutable archives. Run the full suite, inspect the rendered page, review in a separate session and verify deployment.
