# First-contribution improvements — 2026-10-10

User-approved scope: group help requests by question, surface #42 progress, and offer plain comments before versioned artifacts.

Implementation: group only the display layer, retaining machine-readable needs; mark #42, #36 and #28 as maintainer-selected entry points only when their questions still request help. Add direct GitHub comment/discussion links and extract only same-Issue HTTPS comment permalinks into a clearly attributed update panel. Keep source prose escaped. Explain the lightweight path in the guide. Update #42 from its live body with the experiment permalink, actual status and outstanding questions.

Philosophy: P1 reduces duplicated choices; P2 preserves unreviewed evidence and attribution; P3/P4 expose maintainer curation without scores, permission or governance changes; P5 keeps every other open question accessible and excludes withdrawn/closed questions; P6 does not describe maintainer work as outside adoption. Benefit evidence: one rendered card per question, correct links and no stale recommendations. No autonomy or credit changes. Revert the display commit and remove the dated Issue update to correct a failure; GitHub history remains.

Checks: regression tests for grouping, direct comment links, safe same-Issue update links and closed/withdrawn recommendations; full repository unittest suite; live snapshot build; deployment and browser inspection. The site continues to show body snapshots, while comments remain on GitHub.
