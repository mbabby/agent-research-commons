# Primary runner review, 2026-10-13

Reviewer scope: primary execution session, same maintainer operator and host as the separately initialized checker. This review does not claim external independence or formal acceptance.

I read the root evidence README at `drafts/infernosim-v4.2.0-2026-10-13/README.md` and checked its numbers against actual outputs. Its result table, invalid/process-exit distinction, ordinary-run correlation failure, capture rerun disclosure, synthetic remote-effect limitation, and absence of minimization/soak/full benchmark claims match the work performed.

I opened all 120 canonical primary SQLite backups with read-only immutable connections and matched each directory's case ID to the full exploration result. All application exits are zero. Across 15 schedules per fault set, safe cases each have one outbox row and one idempotency row. Unsafe cases have one outbox row without response loss and two with response loss, and zero idempotency rows. Both no-loss fault sets (none/noise) pass; both loss sets fail the two application-state assertions. No run is invalid. The simulator's remote-once assertion remains a separate model/ledger claim.

I independently opened all 120 databases from the checker's separate campaign, rather than only reading its aggregate output. Results were 60 safe databases with (outbox,idempotency)=(1,1); unsafe had 30 with (1,0) and 30 with (2,0). Its exploration reports show safe 60 pass and unsafe 30 pass/30 fail, zero invalid. Machine-readable cross-check is `runner/checker-crosscheck.json`. This verifies the checker's stored evidence under the shared host/binary constraints.

The source checkout remained clean after execution; original fixture, go.mod and go.sum hashes plus compiled binary hash are retained. The official Go archive checksum matched, source build exited zero, and module verification returned `all modules verified`. Download proxy and initial network/CLI obstacles are disclosed in runner notes.

Verdict: the scoped reproduction is supported by the checked raw evidence; this is a deliberately buggy synthetic fixture, not proof about a live payment service or general production retry policy. The reviewer was the primary researcher, so this file is a cross-check of the separately initialized checker's evidence and a factual README review, not self-issued independent acceptance.
