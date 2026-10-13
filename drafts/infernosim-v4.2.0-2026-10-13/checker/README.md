# Checker evidence: same operator, distinct agent session

Pinned source: `f26b5522bbb20f2904d7534b879fa2896bdf1302`. This checker independently initialized a fresh retry fixture and graph, ran 60 safe and 60 unsafe causal cases, and queried all 120 retained SQLite backups. It used the runner session's source-built executable; it did not independently build a second binary. These are not external independent participants.

`summary.json` joins each actual case ID to direct SQL observations and the simulator's response-loss/effect assertions. `safe/` and `unsafe/` include full plans, results, actual argument vectors, process exit codes, and stdout/stderr. Four `samples/` directories retain original DB backups, JSONL, SQL snapshots and corresponding results. Other raw DBs are retained locally. `graph.json` contains the declared causal graph; each result retains observed order and runtime-ID digest bindings. `summary.json` records SHA-256 hashes of graph file and executable; graph semantic hash also occurs in every case.

## Portable rerun

The command files and Python wrappers are path-parameterized templates of the actual executed artifacts. Replace `${CHECKER_ROOT}` with a new writable checker directory, `${RUNNER_ROOT}` with the directory containing the built `infernosim`, and `${SOURCE_ROOT}` with the verified pinned source checkout. No usernames or private credentials are needed. Require Python 3 with stdlib sqlite3 and the source-built v4.2.0 CLI. Source build/toolchain evidence is provided by the runner session.

Materialize the two wrapper templates (`check.py`, `run.py`) into CHECKER_ROOT after replacing those three placeholders. Create CHECKER_ROOT but do not create its `incident`, `graph.json`, `safe-report`, `unsafe-report-allowed`, or per-command output folders: upstream uses exclusive creation. Use the `argv` arrays from `init/command.json`, `discover/command.json`, `unsafe/command.json`, then `safe/command.json`, substituting placeholders. For each command execute:

```
python3 CHECKER_ROOT/run.py LABEL ARGV...
```

Here LABEL is respectively `init`, `discover`, `explore-unsafe-allowed`, `explore-safe`; ARGV means the arguments in the corresponding JSON array, preserving array boundaries (use Python `subprocess.run` rather than shell splitting). Each wrapper writes command metadata, stdout, stderr and exit into CHECKER_ROOT/LABEL. `check.py` obtains evidence destination from CHECKER_EVIDENCE set by run.py, opens application SQLite read-only, backs it up, dumps four tables and JSONL, then invokes the unchanged upstream `--check`. No application source or correlation check was changed.

Expected upstream explore exit: unsafe 1 (30 valid intentional state failures), safe 0. A loopback listener is necessary; restricted execution may need local bind permission. A first sandbox attempt here stopped at `bind: operation not permitted` before any fixture case and was not counted; successful rerun used a fresh report folder. The runner's separate ordinary `agent run` attempt hit response correlation errors and is not counted; this fixture uses random RPC IDs and its upstream benchmark runs causal scheduling, where responses are remapped.

No real remote dependency, credentials or payment service was used. All 120 processes exited zero, none were invalid or timed out. Thirty lost-response cases per mode cover 15 generated schedules with/without a header-noise fault; thirty without loss cover the same schedules. This is a bounded single-seed retry slice, not the five-scenario acceptance campaign, minimization or soak test.
