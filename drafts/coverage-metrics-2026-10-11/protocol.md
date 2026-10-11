# Frozen toy protocol — written before calculation, 2026-10-11

This is a deliberately constructed arithmetic example, not a preregistered empirical trial or model evaluation. Two fictional agents receive the same ten questions and two required answer facets per question. No sampling or model calls occur. Outcomes were chosen to illustrate denominator effects; no population inference is justified.

Every question asks for sum and product of integers a and b. Facets are exact integers or null (omitted). An entirely null response is abstain (A); any false supplied facet makes the response wrong (W), even if another facet is correct; both correct facets is correct (C); otherwise at least one correct facet plus an omission is partial (P). Partial therefore means incomplete but with no false supplied facet in this fixture. Neither partial nor abstain completes the whole task.

Define N=C+W+P+A; T=C+W+P. Report exact numerator, denominator and ratio (N/A for denominator zero): W/N per-assigned wrong; W/T attempted wrong; T/N answer coverage; C/N full correct completion. Coverage means attempted work, not useful success. Partial sensitivities: (W+P)/N and (W+P)/T treat incomplete attempts as failure; W/(C+W) excludes partials from attempted denominator. Do not silently treat abstention as incorrect or as successful completion.

Separately apply the published AA denominator W/(W+P+A) to our toy category counts. This is a formula illustration, not AA scoring equivalence: its grader and dataset are not reproduced. No claim about its partial-grade rubric beyond the documented labels is assumed.

Check empty input, all abstain, all correct, all partial, wrong-priority mixed facets, malformed rows, pairing and exact expected counts. Rank only within one metric and its stated direction. No composite utility score, confidence intervals or paid APIs.
