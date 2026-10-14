# Separately initialized checker rerun

Executed 2026-10-14 by the method/checker Codex session, separate from the fixture
builder and primary runner under the same operator and on the same host. Shared
upstream binary, independently initialized provider database/client processes for
each of six cases. These are deterministic reproductions, not independent samples.

After source inspection and permission for loopback execution, ran:

```sh
python3 /absolute/PACKET/fixture/fixture.py run --case CASE \
  --binary /absolute/path/infernosim --output /absolute/NEW_OUTPUT/CASE
```

Substitute each of `safe-pending`, `unsafe-pending`, `safe-read-failed`,
`safe-ambiguous-absence`, `safe-reconcile`, `safe-mismatched-receipt` for CASE.
Every output directory must be absent. `runs/CASE/command.json` contains the actual
per-case argv/environment and binary hash. Verify source and binary provenance
before execution; these command records are historical, not portable entry points.

Then independently queried captured SQLite state and correlated reports/receipts:

```sh
python3 /absolute/PACKET/checker/check_evidence.py /absolute/NEW_OUTPUT
```

The checker imports no fixture code. Its `checks: pass` means the expected result
for that case was observed, including the unsafe counterexample with two effects;
it is not a statement that the unsafe client is safe. It requires all six cases,
real restart report, distinct PIDs, retained identity, correct response/decision
correlation, complete drain, and expected effects. All six passed these checks in
`summary.json`. The same checker also passed the primary campaign in
`runner-crosscheck.json`.

Initial default-sandbox execution failed on loopback bind before any client ran.
The initialized empty DB remains in `initial-bind-denial/`; it is excluded from
results. The denied invocation returned PermissionError `[Errno 1] Operation not
permitted` from `HTTPServer.server_bind`. Re-execution with loopback permission
completed all six cases with exit 0. No provider or live external service was used.

`provenance.json` records source, binary and inspected source hashes. `runs/`
retains the authoritative provider database and raw InfernoSIM reports for each
case. Consult `../reviews/method-final-review.md` for conclusions and limits.
