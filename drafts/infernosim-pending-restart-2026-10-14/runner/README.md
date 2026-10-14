# Primary runner evidence

This session inspected pinned upstream restart code, executed the final frozen
fixture and independently read both campaigns' SQLite databases. Same host and
operator as builder/checker; not independent external participation.

## Reproduce

From the packet root, with an inspected source-built InfernoSIM binary:

```sh
python3 runner/run_campaign.py --fixture fixture/fixture.py --binary /absolute/path/infernosim --output /tmp/fresh-pending-campaign
python3 runner/verify_sql.py /tmp/fresh-pending-campaign
python3 checker/check_evidence.py /tmp/fresh-pending-campaign
```

The output directory must not exist. The campaign launches a fresh controller,
provider SQLite database and InfernoSIM invocation for each of six selected cases.
Actual execution used the paths recorded in `campaign/campaign.json`; per-case
`command.json` records the InfernoSIM argv and minimal child environment.
The fixture hash before and after the final campaign is recorded in `campaign.json`.
Binary/source provenance and Python/SQLite/platform versions are in `environment.json`.

## Observations and cross-review

All six final launcher commands and all six InfernoSIM commands exited 0. All
reports show restarted=true, distinct original/resumed client PIDs, one recorded
barrier call and no invalid run. This only establishes the configured protocol
and restart checks; the unsafe case also passes them.

`summary.json` comes from `verify_sql.py` against this campaign. The verifier opens
SQLite read-only, checks integrity, compares every retained table against the JSON
export, checks the checkpoint's pending identity against original provider data,
and uses ordered events to place effects before/after client-runner stop. The
unsafe case has two final effects for payment-1; each other case has one. Four
cases start with zero effects at client exit and commit them afterward; reconcile
and mismatched-receipt commit between the first and second reads.

`checker-crosscheck.json` runs the same independent SQL verification against the
checker session's `checker/runs` databases. All six matched. I also read and ran
the separate `checker/check_evidence.py` against primary output: all six checks
passed. Its expected unsafe outcome is two effects, so its pass is experimental
agreement, not a safe-policy result. It additionally checks read status codes,
no resubmit for safe cases, differing replacement idempotency keys, and full
terminal receipt matching.

The root README's measured claims match both retained campaigns. Review scope is
the six synthetic cases and their stored evidence; no production API semantics,
external adoption, disk/power-loss durability or no-restart comparison follows.

## Files and preliminary attempts

Each `campaign/<case>/` retains provider.sqlite, lossless before/after JSON,
checkpoint/first-client/decision JSON, incident inputs, all simulator report
formats, command metadata, stdout/stderr and exact exit status. Python's generated
HOME/Library cache was removed from the packet; it contains no experimental data.

`provisional/` retains the initial bind-denied database and five permitted setup
runs, with an explicit notes record. The initial sandbox rejected loopback bind
before any client launched; the authorized escalated retry succeeded. The fixture
was still being finalized during these setup runs. They are excluded from the
result table, not additional samples, and not used to select favorable outcomes.
The final campaign reruns every case with an unchanged fixture hash.

Upstream `pkg/agentrunner/restart.go` cancels the first child after the simulator
boundary and starts attempt 1 with the same private checkpoint directory. The
simulator and controller remain alive. The fixture's provider calls bypass replay
and its declared drain creates the delayed effects; these are not native pending
provider semantics supplied by InfernoSIM.
