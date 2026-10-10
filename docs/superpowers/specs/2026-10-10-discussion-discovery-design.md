# Discussion discovery and starter tasks

The user approved improving discussion discovery and delivering task #15. Implement in the existing checkout on a dedicated branch, preserving unrelated gateway drafts.

## Discussion discovery

Need: newcomers currently cannot see that comments changed without visiting every GitHub issue. Add a recent discussion page and machine-readable activity resource, linked from community and Agent entry. Show eligible issue title, commenter, updated time and exact GitHub comment link. Do not copy comment bodies or generate summaries. Include opted-in community issues and owner-authored official task issues, excluding PRs, hidden and withdrawn community posts. Fetch a bounded recent repository-comment window and explicitly state its coverage; no claim of a complete archive. Errors must fail publication, never masquerade as no activity. Old offline snapshots remain usable with an explicit unavailable state. Validate IDs, dates and links, escape all display text. Keep official task authority unchanged.

Alternatives: manual summaries remain stale; full comment mirroring needs a separate publication/withdrawal contract. Metadata discovery is the smallest useful option.

## Starter tasks

Deliver task #15 through the existing assignment/review/acceptance workflow: three English cards for evidence location, data/citation consistency, and correction. Each pins inputs, states deliverable, objective checks, example pass/fail and judgment limits. Expose the accepted result from the Agent entry after acceptance. This is a reusable invitation, not membership or credit.

## Value and philosophy

P1: find actual new discussion and one bounded useful action. P2: link source evidence rather than infer truth from activity. P3/P4: no scores, ranking by popularity, new credentials or governance power. P5: withdrawal follows eligible source visibility; versions and corrections remain inspectable. P6: deployment/tests prove mechanics, not outside adoption. Roll back discovery by reverting its isolated code; retain accepted artifacts and real attribution. No baseline philosophy conflict identified.

## Verification

Cover eligibility including hidden/withdrawn/PR records, exact comment URLs, escaped text, bounded-window labels, network failure, legacy snapshot, and discovery links. Independently review task cards against #15 and code against this scope. Run the full stdlib suite and live-snapshot build before deployment; inspect deployed resource and pages after.
