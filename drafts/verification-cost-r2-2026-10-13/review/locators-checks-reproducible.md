# Reproducible arm crosscheck by locators performer

Review interval: 2026-10-13T02:52:06.933420+00:00 to 2026-10-13T02:52:55.705736+00:00 (UTC; initial inventory immediately preceded this interval). Post-lock review; the blind phase had ended. This is a same-operator crosscheck, not independent-operator evidence.

All checked obligations are supported. The sample has exactly q01, q03, q07 and q10 (4/4); full has q01–q12 (12/12), with exact required object fields. I compared every answer semantically with the hidden answer key and source text: all are correct, including all four deliberately false candidate claims (q03, q06, q09, q12). Every answer has a nonempty exact quotation within the cited one-based source span; all paths and ranges match the key. All assessments match. The four sample answers are also consistent with full.

The extraction script was inspected before the reviewer rerun. It uses only Python standard-library file reads, SHA-256 validation and JSON output; reads the corpus manifest, locators and two pinned sources; and extracts lines rather than constructing answers or verdicts. It has no network calls, file writes, or subprocess invocation. Both source files' recomputed hashes match corpus metadata, original receipt and original stdout. The source key spans were independently checked against source bytes, not trusted merely because the key exists.

Actual performer execution is evidenced by a matching command_start at 2026-10-13T02:50:19.389336+00:00 and command_end at 2026-10-13T02:50:19.411063+00:00, receipt exit code 0, captured stdout and empty stderr. The command_end matches every receipt field. Captured stdout has 12 excerpts, each exactly matching the pinned source lines. Its Git SHA is 851a57d17c382495000700723a2dabb1f8c40490. The logged script read predates execution and its recorded hash matches the inspected script. This supports actual execution rather than mere script availability, within the limits of a local, non-tamper-proof logger.

Reviewer action (outside measured participant run): after script inspection, reran extract.py at 2026-10-13T02:52:55.684486+00:00. Exit code was 0, stderr empty, and stdout byte-for-byte identical to the original, SHA-256 `7767549e3f739a8755aa8a47f5be5758f42988c9709e3ea6bc8320b3d138dba9`. This embedded receipt is kept only in this review, outside raw runs; no participant timing or answer artifacts were modified.

Every reproducible raw artifact hash matches RUNS-LOCK.json; checkpoint/end output hashes and byte counts match current sample/full, all logged file-read hashes and byte counts match their files, and event monotonic timestamps are ordered. Recomputed raw hashes:

- `runs/reproducible/events.jsonl`: `45fd8966ef471929be2d7ad7a337a3969ad36ddab2547b434d80d3aef83a58a3`
- `runs/reproducible/execution-receipt.json`: `fb7a758125dde2499cf33e9652d2f8ade33f44d12dfd98c1259717d5d72d1655`
- `runs/reproducible/execution.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `runs/reproducible/execution.stdout`: `7767549e3f739a8755aa8a47f5be5758f42988c9709e3ea6bc8320b3d138dba9`
- `runs/reproducible/full.json`: `1b7db211be0f08096cf4c65b2c4c06715beac74fb8aef26709cc19403e57e7f4`
- `runs/reproducible/sample.json`: `c6eabe1219e360ce821962256036d2bd1596e4ef2938b2a10e226bd8a6ca85c9`

Recomputed source hashes:

- `docs/agent-access.md`: `4be0a8206be8f283eac9654360dfdffbe11105b16d3db1c312d8839fb951e166`
- `docs/collaboration.md`: `be4237e0696816d3b12794e06376b329f325090834433d97bbb2e3699c3e1945`

No mismatch or missing execution evidence found. This review validates this bounded run; it does not establish general time savings, external usefulness, independent identity, or billing cost. No raw edits or publication were performed.
