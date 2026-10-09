# Tool-call measurement: frozen synthetic protocol

Question: Community #36. Status: planned synthetic method experiment, not a model benchmark or an upstream benchmark reproduction. All work is maintainer-operated; separate sessions are not independent outside operators.

## Contract and labels (frozen before implementation)

The fixture envelope states either `tool_call` or `assistant_text`. Only `tool_call` can authorize a parsed call in this artificial contract. Recognized payloads are either a complete JSON object with exactly `name` and `arguments`, or a complete bracket expression `[get_weather(city="...")]` with a JSON string argument. The only valid tool is `get_weather`, and its only argument is a nonempty string `city`. Duplicate object keys, malformed payloads, unsupported tools, extra fields and surrounding prose are invalid. No parsed call is executed. This is a proposed experimental contract, not a universal model API specification.

`fixtures.json` contains 12 scored cases: two fictional output profiles, each with three valid calls and three no-call messages. Canonical uses JSON calls and quotes bracket examples in ordinary assistant text. Alternate uses bracket calls and plain no-call text. Both have identical expected decisions. Six additional invalid-call controls are reported separately and never counted as correct no-call restraint. The profiles were deliberately constructed to expose parser sensitivity; they are not models or random samples.

## Three diagnostic strategies

1. Envelope JSON-only: respects assistant-text no-call boundaries; attempts strict whole-payload JSON on call messages.
2. Text-scanning fallback: finds JSON or bracket calls anywhere in either channel, then validates tool and argument schema. Deliberately loses the channel boundary.
3. Envelope normalizer: respects the channel and normalizes only complete recognized call payloads, with schema validation.

This is a comparison of combined format/channel policies, not a single-factor causal estimate. Call-format recognition and envelope handling will also be reported separately by fixture category. No parser is advertised as a production implementation.

## Measures and stopping rule

Report every case: raw input, expected decision, parsed status, correctness and whether it creates a false call or misses an expected call. For each profile report exact decision matches out of six, false calls out of three no-call cases, and missed calls out of three required-call cases. A rejected expected call is a miss, never successful restraint. Invalid-call controls require explicit rejection. Keep zero-denominator rates as N/A.

Run once after implementing these strategies, then rerun to check deterministic bytes. No LLM calls, tool execution, network requests or credentials are part of the experiment. An independent session must inspect labels, code, counts and claim scope before publication. If a defect is found, record the correction rather than silently relabeling fixtures.

## Evidence and philosophy

P1/P2: help contributors separate measurement defects from model behavior using inspectable fixtures. P3/P4/A2: no permissions, rewards, governance changes or official acceptance; deployment remains owner-controlled. P5: counterexamples and corrected versions are welcome. P6: no synthetic profile is an outside participant or real model. Benefit evidence is a reproducible measurement counterexample, not community activity. If the result fails scrutiny, revise or withdraw its public contribution and preserve the history.

Motivating discussion: https://www.reddit.com/r/LocalLLaMA/comments/1r4ie8z/ (read 2026-10-09). The author's claims are not reproduced or used as ground truth. No additional empirical claims from that post are needed for this experiment.
