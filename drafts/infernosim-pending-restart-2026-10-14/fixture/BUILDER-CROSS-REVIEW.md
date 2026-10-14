# Builder cross-review (same-operator session)

Scope: inspected the separately authored `checker/check_evidence.py`, checker summary, runner campaign driver and actual captured evidence. This author implemented the fixture and is not an independent outside reviewer. This record cross-checks other sessions’ checks; it is not self-awarded formal acceptance.

Result: scoped pass for the six declared synthetic controls. I executed the checker independently against both `checker/runs` and `runner/campaign`; both commands exited 0 with all six checks passing. I also queried the checker campaign SQLite databases directly, without importing the fixture/checker, and inspected event order and the before-drain snapshots. All non-reconciliation cases had zero pre-drain effects; safe cases ended with one, unsafe replacement ended with two. Reconciliation and deliberately mismatched receipt had one effect before the final drain, as declared.

The checker establishes distinct client PIDs, actual simulator restarted=true, original pending operation query, matching retained handle/business/idempotency row, decision-to-provider-response correspondence, replacement new identity, completed queue drain, and delayed effect ordering for the stopped-client cases. It does not infer safety from simulator raw pass. Its unsafe case “checks: pass” means the expected duplicate negative control was observed.

Correction requested and applied during cross-review: bind checkpoint business/idempotency identity to the authoritative DB row, and bind first/terminal decision observations to the corresponding provider event responses. I reread the final checker after those additions and reran it on both campaigns. No blocker remains for the bounded claim.

Limits: replay barrier is synthetic and distinct from provider calls; original handle was received before crash. Provider read failures and receipt mutation are custom fixture semantics. No external adoption, model behavior, power-loss durability, or general exactly-once guarantee is established. Runner hashes the fixture before each case and after the campaign; source-to-binary provenance relies on the separately recorded build evidence. No-restart baseline and checker-hook failure are not exercised. Fixture controller errors outside normal subprocess completion may leave only partial evidence; those cannot be counted safe.

Commands executed from repository root:

```sh
python3 drafts/infernosim-pending-restart-2026-10-14/checker/check_evidence.py drafts/infernosim-pending-restart-2026-10-14/checker/runs
python3 drafts/infernosim-pending-restart-2026-10-14/checker/check_evidence.py drafts/infernosim-pending-restart-2026-10-14/runner/campaign
```

Exact reviewed SHA256 hashes (paths relative to packet):

| Artifact | SHA256 |
| --- | --- |
| `fixture/fixture.py` | `01eee5d28400bd388492ef86505ea526923e100ff660ef199795ad2886136aa7` |
| `checker/check_evidence.py` | `08162672d3392511fdf9dced3c19ce8ee9d9cad2dd1eda8ef9346bd1ebc15e32` |
| `checker/summary.json` | `0bcdc58e32fb99ecaba3228fb5bd0fe79831f45cee96e04881a24886506e2641` |
| `runner/run_campaign.py` | `5010dc9615ee53d248bfe266985e771374faa3255954e4241acd067d3606b5c6` |
| `runner/campaign/campaign.json` | `b84664dcf08d255eb1407754711380cdebdf0ce626f03b46a4ea5a8d2c0fc713` |
| `checker/runs/safe-ambiguous-absence/provider.sqlite` | `04be034c3ae2efc810971c71744a314bfcbdfa881cc99583671d1e8faf4a3395` |
| `checker/runs/safe-mismatched-receipt/provider.sqlite` | `68b92d0dae00db9446b8f98f0e9c73c817da70ae52e06013b16952ddebb827e8` |
| `checker/runs/safe-pending/provider.sqlite` | `995311852be566187b9e228254658faa5f83f03b3ed41e45fbea1e734bfa75ee` |
| `checker/runs/safe-read-failed/provider.sqlite` | `ce482e63c94cac5598d6a26b436e65e29bc5193d2831d434e27a33ab5e85a352` |
| `checker/runs/safe-reconcile/provider.sqlite` | `607920ea961ea91a680137c36b1bb4223dc2931190dc57f6acac2a35b02ef64b` |
| `checker/runs/unsafe-pending/provider.sqlite` | `f8b84cd24b65db056872eff1bcebc7ee580ac9e956152015b82845ea04ec3530` |
| `runner/campaign/safe-ambiguous-absence/provider.sqlite` | `04be034c3ae2efc810971c71744a314bfcbdfa881cc99583671d1e8faf4a3395` |
| `runner/campaign/safe-mismatched-receipt/provider.sqlite` | `68b92d0dae00db9446b8f98f0e9c73c817da70ae52e06013b16952ddebb827e8` |
| `runner/campaign/safe-pending/provider.sqlite` | `995311852be566187b9e228254658faa5f83f03b3ed41e45fbea1e734bfa75ee` |
| `runner/campaign/safe-read-failed/provider.sqlite` | `ce482e63c94cac5598d6a26b436e65e29bc5193d2831d434e27a33ab5e85a352` |
| `runner/campaign/safe-reconcile/provider.sqlite` | `607920ea961ea91a680137c36b1bb4223dc2931190dc57f6acac2a35b02ef64b` |
| `runner/campaign/unsafe-pending/provider.sqlite` | `f8b84cd24b65db056872eff1bcebc7ee580ac9e956152015b82845ea04ec3530` |
