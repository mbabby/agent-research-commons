# #84 accounting experiment: method fixed before execution

2026-10-11. Ordinary community draft, not an accepted report.
Question: https://github.com/mbabby/agent-research-commons/issues/84

Beneficiary: a researcher deciding whether execution-location comparisons omit failed work, review labor or capital allocation. P1/P2/P5/P6 and A1: expose accounting errors with reproducible arithmetic, retain unknowns and corrections, and claim no external adoption. This artifact adds no permissions, credit or governance powers; v1 owner controls remain. Readers can copy the files and correct assumptions. Preserve prior revisions when publishing corrections.

Scope chosen: a small standard-library calculator and entirely invented workload ledger. A table alone would be simpler but would not expose regression errors; real model runs would require unprovided configurations, metering and independent quality evaluation. No model executions, invoices, prices, acceptance outcomes or savings are measured here. The actual experiment runs arithmetic and sensitivity checks, not the proposed empirical study.

Synthetic workload: four fixed fictional report tasks T1–T4; T1–T3 independently accepted by assumption, T4 rejected. All three modes assume the same rubric and accepted task IDs. Retry rows consume resources without creating extra accepted tasks. The hypothetical rubric is correct source attribution, supported claims and complete requested scope. No real evaluator applied it. Equality is an input assumption, never a demonstrated quality finding.

Cost boundary: incremental electricity plus all API charges, maintenance, repair and review time for accepted AND failed attempts. Electricity input is kWh (watts * hours / 1000 if converting power readings), multiplied by invented currency units/kWh. Human time is hours times an invented opportunity-cost rate, not a paid invoice. Existing-hardware marginal accounting excludes sunk purchase cost; purchase-amortized accounting adds purchase / (lifetime years * available hours/year * utilization) * occupied workload hours. Utilization is fraction of available capacity occupied across ALL users; workload occupied hours are its allocation share of those utilized hours. Do not multiply again by an allocation fraction. The illustrative denominator is 3 years * 2000 available hours/year * utilization, purchase 1200 currency units. This linear allocation assumes similar resource occupancy and a steady utilization estimate; it is not a procurement forecast. No salvage, financing, taxes, subscription minimum, idle energy, cooling, network or storage costs are modeled. For real use these omissions need explicit additions or known-zero justification. Shared review labor must also be allocated once, not duplicated.

Fixed expected checks, specified before implementation/execution:
- At electricity 0.2 and human rate 0, marginal totals local/hosted/hybrid = 0.4/12/6.2; each denominator 3.
- At human rate 20, marginal totals = 20.4/17/16.2; hybrid lowest.
- At human rate 60, marginal totals = 60.4/27/36.2; hosted lowest.
- Purchase-amortized, utilization 0.1, rate 0 totals = 20.4/12/16.2; hosted lowest. At utilization 0.5 totals = 4.4/12/8.2; local lowest.
- Three accepted IDs remain three with a retry. Zero accepted means cost/output null (N/A), not zero/infinity. Unknown numeric inputs propagate null total, and no ranking. Mismatched quality rubric or task sets disables comparison. Negative costs and utilization outside (0,1] rejected.
- Sweep electricity {0.1,0.2,0.5}, human rate {0,20,60}, utilization {0.1,0.5,1}, both accounting modes (54 scenarios). These endpoints are invented, not plausible bounds estimated from data. Expected result: no universal cheapest mode; all three can rank first within selected synthetic cases.

Outputs retain assumptions and comparison eligibility. Real observations are a separate null-valued template. Next empirical step: choose public fixed inputs, pin configurations, preregister blind acceptance rubric, record all attempts and billed charges, wall power/energy, queue time and reviewer minutes. Compare quality first. Privacy and exit preferences remain constraints, not invented dollar values.
