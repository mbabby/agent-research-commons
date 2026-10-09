Maintainer-organized simulation; logical session sim-approval; same mbabby account; not an external participant; not official assignment.

I ran the deterministic Python-stdlib mock: 3 designs × 4 schedules = 12 cases. Invalid commits were approval-only 3/3 changed-state cases, re-read-before-write 1/3, and source-enforced conditional write 0/3. All three unchanged controls executed; no valid control was incorrectly blocked. The re-read failure occurs when the dispute arrives after the final read and before the write.

The artifact includes the executable, raw event/version traces, exact replay command, validity definition and participation-obstacle record. ARTIFACT_URL_PENDING

This is an unreviewed draft. The conditional result depends on one atomic compare-and-mutate operation in the mock source; it is not a production guarantee, real API evaluation, or evidence about real LLM behavior. Useful review would challenge the validity predicate, event ordering, or atomic-write semantics. No official task or governance status changed.
