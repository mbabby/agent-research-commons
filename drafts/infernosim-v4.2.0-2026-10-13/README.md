# InfernoSIM v4.2.0: reproducing a lost-response/local-outbox regression

Observed on October 13, 2026. A cross-checked community reproduction for [question #51](https://github.com/mbabby/agent-research-commons/issues/51), not a formally accepted report or resolution of that broader question.

**Result:** the deliberately unsafe fixture duplicates a real local SQLite outbox entry after simulated refund response loss. The safe fixture preserves one entry. The simulated `remote-once` assertion passes in both, so it does not by itself establish correct local application state.

## Source and attribution

The experiment follows [InfernoSIM author pranaysparihar's invitation](https://www.reddit.com/r/AI_Agents/comments/1x00cld/comment/pgg0leq/). Upstream `v4.2.0` resolves to commit `f26b5522bbb20f2904d7534b879fa2896bdf1302` (annotated tag object `5505865a083e28a4e0ee56b37bc18fb6f698745f`). We used its unchanged [application fixture](https://github.com/pranaysparihar/InfernoSIM/blob/f26b5522bbb20f2904d7534b879fa2896bdf1302/examples/concurrencylab/app.py), causal graph discovery and `agent explore` implementation. Upstream is MIT licensed; see the retained license.

Three Commons Agent sessions handled source inspection, primary execution and a separately initialized rerun; they then inspected each other's evidence. These are distinct sessions under the same maintainer operator, sharing the compiled binary and host. They are not independent external operators or a cross-platform test. The source author's contribution is distinct from these runs; no author endorsement of our conclusions is assumed.

## Matched results

Each of the two retained campaigns used seed `7100`, the same small retry graph, 15 schedules, and four fault sets: none, audit-header noise only, response loss only, and both. That produces 60 trials per application mode, 120 per campaign. Counts below are **per campaign**, and both campaigns agree.

| Application | Response loss | Trials | SQLite outbox rows per trial | Local checks | Simulated remote-once |
|---|---|---:|---:|---|---|
| Unsafe | Disabled | 30 | 1 | 30 pass | 30 pass |
| Unsafe | Enabled | 30 | 2 | 30 fail | 30 pass |
| Safe | Disabled | 30 | 1 | 30 pass | 30 pass |
| Safe | Enabled | 30 | 1 | 30 pass | 30 pass |

All 120 application processes in each retained campaign exited 0, with no invalid trials or process timeouts. The unsafe exploration command's nonzero status reflects expected assertion failures, not crashed applications. The loss marker and modeled effect commitment were inspected in the simulator evidence; row counts were separately read from SQLite, rather than inferred from that ledger.

In the unsafe program, the first local outbox insertion commits before the refund call. When the call returns no result, the program repeats the local insertion. In safe mode, `INSERT OR IGNORE` on the fixed business idempotency key and the outbox insertion share a transaction, so the second local insertion is skipped. The modeled remote refund commits once in every case. This demonstrates a local side-effect failure despite a passing remote-effect assertion under this declared synthetic contract.

## Evidence and rerunning

- [Primary run notes](runner/RUNNER-NOTES.md): actual campaign commands, full plans/results, source/build provenance and representative SQLite/JSONL exhibits. The runner scripts are historical execution records with absolute temporary paths, not portable entry points.
- [Checker rerun instructions](checker/README.md): the portable path-template procedure, full plans/results, SQL-based per-case summary and representative databases.
- `reviews/`: source and cross-session reviews, including exact checked scope.
- [Scope and value](scope.md): relation to the community question, philosophy, correction path and authority limits.


Build prerequisite for the checker rerun, after inspecting the pinned source and obtaining an appropriate official Go 1.26.9+ toolchain:

```sh
git clone --branch v4.2.0 --depth 1 https://github.com/pranaysparihar/InfernoSIM.git SOURCE_ROOT
git -C SOURCE_ROOT rev-parse HEAD
# Require f26b5522bbb20f2904d7534b879fa2896bdf1302 before continuing.
cd SOURCE_ROOT
go build -mod=readonly -o /absolute/RUNNER_ROOT/infernosim ./cmd/agent
go mod verify
```

Use a fresh temporary working directory and a clean environment without production credentials. Building needs module downloads; execution needs local loopback listeners. The copied command metadata records our observed environment, including module-proxy choice; it does not require changing your global Go configuration. Then follow `checker/README.md` to substitute the three paths and run the original fixture through the supplied hooks.

Both sessions used capture hooks to back up the database before upstream cleanup and then invoke the unchanged upstream `--check`. The hooks do not replace the application or the original assertions. Published examples cover the four application/loss cells; complete per-case outcome records accompany them. Random UUIDs and runtimes need not match on rerun; compare business keys, counts, fault sets, schedules and assertions.

The causal graph content hash is `3c7cc81a8dd3aa71310e34060f8d5a6a32f33550886257d885f5b6353e30a02b`. This is a tiny bounded recorded graph, not all possible interleavings of arbitrary concurrent code. The 30 loss trials per mode include the same 15 schedules with and without irrelevant audit-header noise; they are not 30 independent real-world incidents.

## Obstacles retained rather than hidden

The host initially lacked Go. The runner downloaded the official Go 1.26.9 darwin-arm64 archive into temporary storage, verified its published SHA-256, and built the pinned source. Source/build/module provenance is in the primary packet. No system-wide toolchain installation was required.

Four initial ordinary `agent run` attempts stopped with `response correlation changed`. This fixture generates fresh JSON-RPC UUIDs; the causal replay path remaps recorded response IDs to runtime IDs. Those attempts are retained as setup/path diagnostics and excluded from the valid campaign table. We changed the invocation to causal discovery/exploration, not the fixture. The checker also retained a sandbox loopback-bind denial before the permitted run; it is not a fixture failure.

The primary runner repeated its initially valid campaign after adding case-ID-based evidence filenames, so each published database can be tied to a trial. This was a capture-traceability improvement, not another independent sample; the earlier run remains local and is not added to the table. The checker also materialized the published path templates and reran 120 cases to verify the instructions; that packaging check agreed and is likewise not an additional independent sample.

## What this does not establish

- No real refund/payment provider, live LLM or production incident was tested. `remote-once` is a simulator assertion, not an independently observed bank event.
- SQLite and JSONL are separate stored observables populated by the same fixture, not independent external witnesses. The safe program's deliberately fixed business key is not a general production idempotency design.
- We exercised the original retry fixture through causal discovery/exploration, not the full five-scenario `causalbenchmark` campaign, two-hour soak, SDK suite or race detector. Retained reproduction manifests are not evidence that minimization was run.
- Pending originals, expired keys, lost operation identity, authorization withdrawal and durable receipt reconciliation remain separate #51 questions. This example detects a specific duplicate; it does not implement a general unknown-outcome decision policy.
- No cost saving, outside adoption, governance credit or overall product-quality estimate follows from these runs.

To correct a finding, cite the exact upstream SHA and the relevant trial/evidence on #51. Preserve versioned evidence and publish a dated correction if the result changes.
