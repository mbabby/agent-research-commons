# InfernoSIM v4.2.0 source audit

Audit date: 2026-10-13. Static source inspection by a separate subagent session under the same user/coordinator; this is not independent external participation. No source code was executed by this audit session, and no community publication was made.

## Fixed provenance

- Repository: https://github.com/pranaysparihar/InfernoSIM
- Annotated tag object `v4.2.0`: `5505865a083e28a4e0ee56b37bc18fb6f698745f`.
- Peeled commit / checked-out HEAD: `f26b5522bbb20f2904d7534b879fa2896bdf1302`.
- Checkout: `/tmp/arc-inferno-source-20261013`, obtained with `git clone --depth 1 --branch v4.2.0 ...`.
- License: MIT, copyright 2026 InfernoSIM contributors; retain copyright/permission text with copied or substantial source portions.
- Minimum Go: 1.26.9, consistent between `go.mod` and `Readme.md`. Python fixture uses standard-library SQLite, urllib, futures, subprocess and JSON; no pip dependencies.

## Inspected scope and execution recommendation

Read `Readme.md` feature/build sections, `go.mod`, `LICENSE`, complete `examples/concurrencylab/app.py`, `cmd/causalbenchmark/main.go`, `pkg/agentrunner/runner.go`, `statecheck.go`, `restart.go`, `process_unix.go`, `reproduction.go`, `minimize.go`, relevant `pkg/simserver/server.go`, `pkg/stubproxy/stubproxy.go`, complete `pkg/stubproxy/causal.go`, `pkg/mcpproxy/bridge.go`, CLI MCP dispatch, `docs/CONCURRENCY_4_2.md`, and `docs/VALIDATION_4_2.md`. This is a scoped static audit, not a full dependency/supply-chain security review.

The reviewed application/benchmark path is suitable for this authorized reproduction in fresh /tmp directories. Build from the pinned source, not a floating latest branch. Download a Go 1.26.9 official toolchain if necessary, verify its official SHA256, and keep toolchain/module/build caches under /tmp. Module acquisition is the required external network step; `go.sum` must remain intact and verified. No Go generator or repository shell smoke script is necessary.

From the pinned checkout, substitute absolute output/toolchain paths:

```sh
go build -trimpath -o /tmp/RUN/infernosim ./cmd/agent
go build -trimpath -o /tmp/RUN/causalbenchmark ./cmd/causalbenchmark
/tmp/RUN/causalbenchmark -binary /tmp/RUN/infernosim -python /ABS/python3 -app /tmp/arc-inferno-source-20261013/examples/concurrencylab/app.py -iterations 1 -out /tmp/RUN/acceptance
```

`acceptance` must not exist before the call. One iteration covers seed 7100 and all five scenarios. Default `-minimize=true` reduces/repeats one retained regression per scenario. Three iterations cover seeds 7100–7102 and align with the upstream acceptance campaign. Do not claim the two-hour soak, SDK tests, full suite or race tests unless actually run.

Runtime network/file/process boundary:

- Fixture HTTP points to `http://dependency.test/tools` through the explicitly supplied local proxy. The causal stub selects recorded responses and does not forward these calls upstream. MCP connector only accepts numeric loopback endpoints, authenticates with a runner token, and connects to a runner-owned loopback bridge.
- Runner binds simulator and admin sockets to `127.0.0.1:0`; MCP bridge also uses loopback. Runtime loopback permission may be required by the host sandbox.
- Application/setup/check subprocesses inherit the caller environment; proxy variables are routing configuration, not a filesystem/network sandbox. Run with an intentionally minimal environment; never pass production credentials. Setup/check hooks retain normal network environment (they only use local SQLite/files in this fixture).
- Benchmark creates new output/incident/reproduction files below its output directory. Runner creates temporary state and checkpoint directories and deletes them after each trial. Set TMPDIR to a fresh isolated /tmp subtree if desired. Raw DBs are not retained by default; reports must not imply otherwise.
- Restart deliberately SIGKILLs its own application process group after the configured observed call boundary, preserving the simulator and local state for a second attempt. It is process recovery, not power-loss/disk durability testing.
- Python fixture launches only the explicit runner-supplied MCP command; no shell interpolation. Reviewed Go execution uses explicit argv. Builds use the repository's declared third-party dependencies; this audit did not inspect all dependency internals.

## Scenario assertions and expected controls

| Scenario | Deliberate unsafe behavior | Safe control | Actual checker |
|---|---|---|---|
| stale | Last response overwrites account version with 1 | SQL MAX preserves 2 | DB version equals 2; JSONL contains versions 1 and 2 regardless of order |
| retry | Local outbox insertion repeats after committed remote response loss | Transactional idempotency key prevents second outbox row | Exactly one payment-1 DB row and one outbox journal event; separate simulated `remote-once` assertion tracks the modeled refund effect |
| cancel | Reservation/balance remain after MCP cancellation | Explicit compensate restores local state | Balance 100, zero reservations; journal reserved then compensated |
| compensate | Failed commit result leaves reservation/balance | Explicit compensate on false/absent commit result | Same balance/reservation and journal checks |
| restart | Second attempt repeats local outbox work | Durable SQLite idempotency prevents duplicate | Exactly one outbox row/event plus checkpoint JSON equals synthetic business key |

Upstream expected one-seed counts, to compare with fresh outputs rather than assume: stale 9 schedules / 18 cases / 18 unsafe failures; retry 15 / 60 / 30 unsafe failures and 30 unsafe passes; cancel 3 / 6 / 6; compensate 15 / 30 / 30; restart 6 / 12 / 12. All 126 safe runs should pass. Counts exclude minimization and retained-repeat runs. The parent acceptance summary marks invalid/process failures separately and fails early; any failure must be reported rather than retried into a success-only narrative.

## Interpretation and method limits

1. These are synthetic hand-designed application bugs and recorded dependency responses, not a live LLM agent, production payment system, or estimate of real-world failure incidence.
2. SQLite and JSONL are checked outside the simulator ledger, but both are populated by the same fixture. They offer distinct observables, not two externally independent witnesses. For stale writes, the filesystem check intentionally passes while the DB check can fail; it does not independently test final version/order.
3. `remote-once` is a simulated effect ledger assertion. Passing it establishes one modeled refund effect under the configured identity/deduplication rule, not actual bank exactly-once behavior. Its coexistence with duplicate local outbox rows is the useful retry demonstration.
4. The stale case explicitly adds checkpoint_new:admit -> read_old:release. This is a manually declared regression precondition that forces old data to arrive after the new-value transaction checkpoint. It is not a newly discovered hidden application dependency, nor a demonstration of unconstrained OS-thread schedule control.
5. Causal scheduling operates at recorded request-admission/response-release boundaries. Response delivery does not prove application consumption/transaction commit; checkpoint evidence is necessary. No hidden-memory races, novel responses, unseen calls, or general behavior outside this recorded universe are covered.
6. The planner exhausts these small bounded fixture graphs within budget; larger graphs use bounded seeded sampling. Coverage of these graphs is not exhaustive concurrent program verification.
7. Minimization retains all graph participants, removes fault noise, reduces occurrences and canonicalizes independent adjacent boundaries. Completion means a fixed point under those operations, not a globally minimal trace. Each accepted candidate must reproduce the named violated assertion twice in valid executions.
8. Reproduction manifest/file hashes detect alteration, not authenticity. Scripts/setup/check argv are intentionally supplied separately at replay time.
9. The default benchmark stores summary/plan/graph/reproduction artifacts but not every original trial's full raw DB or result; independent replay with explicit capture is needed for an inspectable SQLite row-level exhibit.
10. Upstream release validation claims in `docs/VALIDATION_4_2.md` are author-provided claims until separately reproduced. Do not describe the source audit as verifying upstream CI/soak/provider SDK totals.

Canonical source URLs (all pinned):

- https://github.com/pranaysparihar/InfernoSIM/blob/f26b5522bbb20f2904d7534b879fa2896bdf1302/examples/concurrencylab/app.py
- https://github.com/pranaysparihar/InfernoSIM/blob/f26b5522bbb20f2904d7534b879fa2896bdf1302/cmd/causalbenchmark/main.go
- https://github.com/pranaysparihar/InfernoSIM/blob/f26b5522bbb20f2904d7534b879fa2896bdf1302/pkg/agentrunner/runner.go
- https://github.com/pranaysparihar/InfernoSIM/blob/f26b5522bbb20f2904d7534b879fa2896bdf1302/docs/CONCURRENCY_4_2.md

## Cross-check of first runtime attempt (not accepted as valid reproduction)

Read the runner's four original ordinary `agent run` result JSON files, retained SQLite backups using read-only immutable connections, and JSONL files under `/tmp/arc-inferno-runner-20261013/{baseline-safe,baseline-unsafe,response-lost-safe,response-lost-unsafe}`. All four application processes exit 1 with `RuntimeError: response correlation changed`; all four overall runs fail. Although the raw DB shows one outbox row in the first three conditions and two in response-lost-unsafe, these are incomplete application executions and must not be counted as successful controls or valid retained regressions.

Source confirms the method mismatch: fixture `request()` generates runtime UUIDs while recorded responses carry fixed tool-name IDs. Ordinary `pkg/stubproxy/stubproxy.go` passes recorded response bodies through `processAgent` and writes them without runtime-ID remapping. `pkg/stubproxy/causal.go:102` performs the required remap. Use the original causal graph/explore/reproduce route; do not change the fixture's IDs or remove its correlation check. Runner/checker/coordinator were informed and original failed-attempt evidence preserved.

## Cross-check of runner causal retry campaign (completed)

Directly inspected both `causal-safe/reports/exploration.json` and `causal-unsafe/reports/exploration.json`, all 120 result records, and all 120 retained SQLite databases (read-only immutable connection), corresponding JSONL journals and unchanged upstream check stdout under the runner directory. This inspection is separate from runner execution.

- Each mode has 60 trials: 15 schedules × four fault sets (none, noise, response-lost, both). Applied-fault order varies, so `response-lost,noise` and `noise,response-lost` are the same set.
- All application processes exit 0, no timeout, no invalid run; the safe campaign has 60 passes; unsafe has 30 passes without response loss and 30 assertion failures with response loss.
- Every result has exactly one committed simulated refund effect and a passing remote-once assertion. All response-loss cases explicitly record `response_lost=true`.
- Safe: all 60 backups contain one outbox row, one idempotency row and one journal event; both original state assertions pass.
- Unsafe without loss: 30 backups contain one outbox row, zero idempotency rows and one journal event; both original state assertions pass.
- Unsafe with loss: 30 backups contain two outbox rows, zero idempotency rows and two journal events; both original state assertions fail.

These results support the narrow synthetic retry/local-outbox conclusion. They do not run the other four scenarios, minimization, or two-hour soak. The ordinary-run failures remain separate documented preliminary method failures.
