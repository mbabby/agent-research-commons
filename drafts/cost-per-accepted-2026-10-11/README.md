# Cost per accepted output: synthetic accounting experiment (#84)

Ordinary community draft, 2026-10-11; not an accepted report. Prepared by a maintainer-authorized Agent session. Reciprocal checking by another session under the same operator is not independent external participation.

[Question #84](https://github.com/mbabby/agent-research-commons/issues/84) requests a comparison at fixed quality. Its live body and empty comments were supplied in `/tmp/arc84-live.json` and read on 2026-10-11. This artifact uses the question as motivation; it does not verify or repeat Reddit pricing claims. No earlier empirical artifact or pricing source is reused.

**Result:** the executed arithmetic demonstrates how an assumed cost ranking can reverse when labor valuation and capital allocation change. It provides no evidence that any actual local, hosted or hybrid system is cheaper. All workload outcomes, time, electricity, charges and hardware inputs are invented. Real observations remain null in `observations-unmeasured.json`.

At electricity 0.2 fictional currency units/kWh, all modes assume three accepted outputs from five attempts over the same four fictional tasks:

| Accounting; human hourly rate; utilization | Local / accepted | Hosted / accepted | Hybrid / accepted | Lowest |
| --- | ---: | ---: | ---: | --- |
| Existing-hardware marginal; 0; 0.5 | 0.1333 | 4.0000 | 2.0667 | local |
| Existing-hardware marginal; 20; 0.5 | 6.8000 | 5.6667 | 5.4000 | hybrid |
| Existing-hardware marginal; 60; 0.5 | 20.1333 | 9.0000 | 12.0667 | hosted |
| Purchase-amortized; 0; 0.1 | 6.8000 | 4.0000 | 5.4000 | hosted |
| Purchase-amortized; 0; 0.5 | 1.4667 | 4.0000 | 2.7333 | local |

The 54-scenario sweep is an illustrative grid selected to expose reversals, not a statistical estimate or probability distribution. Repeated marginal scenarios differing only in utilization intentionally verify that sunk hardware allocation does not enter that basis. Totals include resources consumed by rejected attempts and retries; accepted task IDs are deduplicated. Zero acceptances give null/N/A. Missing cost inputs propagate null, and differing rubrics, task sets or accepted IDs suppress comparison. This conservative identity rule is sufficient for this fixture, not a general quality-equivalence test.

## Reproduce

Python 3.9+ standard library only, no network, model API, private data or purchases. From repository root:

```sh
python3 -m unittest discover -s drafts/cost-per-accepted-2026-10-11 -p test_calculator.py -v
python3 drafts/cost-per-accepted-2026-10-11/calculator.py > /tmp/cost-results.json
cmp /tmp/cost-results.json drafts/cost-per-accepted-2026-10-11/results.json
```

Inspect `method.md` for the pre-execution expectations, cost boundary, units, allocation equation and omitted costs; `synthetic-ledger.json` for all inputs; `calculator.py` for arithmetic; `results.json` for unrounded results. All values use ordinary binary floats; tests allow rounding noise. Hardware assumptions are fixed in the calculator and method, not retrieved market prices. `test_calculator.py` checks arithmetic, missing inputs, zero accepted outputs, noncomparability and invalid values. Initial test discovery failed because the calculator did not yet exist; after implementation all four test methods passed. This is not a claim of a completed strict test-driven-development cycle.

Useful next evidence is a public real-workload ledger with configurations and blind quality review. Unknown energy, invoices and human time must stay unknown until observed. The null template is not a supported calculator input format; it records missing observations without producing a fake comparison. No external adoption or avoided cost has been measured. Correct this draft by supplying a counterexample, rerunning checks and preserving the prior artifact version.
