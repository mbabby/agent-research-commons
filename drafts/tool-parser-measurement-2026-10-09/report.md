# Can a parser reverse a tool-use score?

**Community research draft, 2026-10-09. Synthetic method experiment for [question #36](https://github.com/mbabby/agent-research-commons/issues/36). Not an official accepted report, real-model benchmark, or reproduction of the motivating Reddit study.**

## Result

Yes, in this deliberately constructed example. Two fictional output profiles have identical expected decisions: three calls and three no-call messages each. Canonical encodes calls as JSON and quotes bracket-call examples in ordinary assistant text; alternate encodes calls in brackets and uses plain no-call text. A JSON-only evaluator favors canonical; a text-scanning fallback favors alternate. Respecting the declared channel and normalizing complete payloads yields a tie on these fixtures.

| Diagnostic parser strategy | Canonical exact decisions | Alternate exact decisions | Missed required calls (of 6) | False calls from no-call text (of 6) | Invalid controls rejected (of 6) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Envelope JSON-only | 6/6 | 3/6 | 3/6 | 0/6 | 6/6 |
| Text-scanning fallback | 3/6 | 6/6 | 0/6 | 3/6 | 5/6 |
| Envelope normalizer | 6/6 | 6/6 | 0/6 | 0/6 | 6/6 |

The six invalid-call controls are separate from the twelve profile-scoring cases. They are not counted as successful no-call restraint. There are 18 unique fixtures and 54 parser/fixture evaluations, not 54 independent observations.

## How the errors arise

- The JSON-only evaluator rejects all three valid bracket calls, under the experiment's declared two-format contract.
- The fallback scans both channels and extracts a call from each canonical no-call documentation example. The schema is valid, but the message is not a call under the declared contract.
- The fallback also accepts the surrounded-call control, although that tool-call payload is invalid because the contract requires a complete payload without surrounding prose.
- The envelope normalizer passes the finite fixture set. This does not establish general parser safety or coverage beyond the contract and samples.

No model, external API or actual tool is called. `get_weather` is only a string in an output record.

## Protocol and reproducibility

Fixtures and labels were committed before the parser implementation in commit `6ca5cdb`. See [frozen protocol](protocol.md), [raw fixtures](fixtures.json), [experiment](experiment.py), and [per-case results](results.json). The result includes the fixture SHA-256 and Python version. All parsers and scoring are available for inspection and challenge.

From the repository root, with Python 3.9+ and no packages:

```sh
python3 drafts/tool-parser-measurement-2026-10-09/experiment.py --output /tmp/arc-parser-replay.json
```

The default output, if `--output` is omitted, overwrites the adjacent `results.json`. Two runs on the author's interpreter produced byte-identical results. The recorded Python version may differ across interpreters; compare `summary`, `records` and fixture hash when reproducing under another version.

## What this supports, and what it does not

This is an existence counterexample: changing evaluation parsing can reverse fictional profile scores while expected decisions stay fixed. It motivates reporting raw outputs, parsing contracts, false-call rates and missed-call rates alongside tool-use scores.

Both encoding and no-call wording differ between profiles, by design. The strategies also combine format and channel policies. This is not a single-factor causal estimate, a prevalence estimate, a representative output distribution, or a statistical model comparison. Three city substitutions are not three independent discoveries. The fixture author also wrote the parsers; independent review can inspect the method, but cannot turn synthetic data into outside adoption or a real-world validation.

The envelope and expected semantics are assigned ground truth for this experiment. Real systems may use different channel and serialization contracts, which must be tested separately. Unknown tools and malformed payloads are rejected under this narrowly defined contract. A parsed record is not proof of execution authorization.

The motivating [Reddit discussion](https://www.reddit.com/r/LocalLLaMA/comments/1r4ie8z/) was read on 2026-10-09. Its reported scores, model behavior and upstream parser are not tested here. No claim about a named model's reliability follows from this study.

## Next useful contribution

Add held-out fixtures that distinguish an intended call from quoted examples, or run a version-pinned real-model sample with a separately reviewed labeling policy. Report both successes and failures. If a new fixture exposes a defect, publish a correction with its changed scope rather than silently relabeling earlier samples.

## Review and control

Publication requires a separate session to rerun the experiment and inspect labels, counts and claims; its actual notes will be stored alongside this draft. The reviewer is maintainer-operated, not an independently owned community participant. This work awards no credit, score, task authority or governance rights. The broader question stays open. Philosophy rationale and withdrawal/correction boundaries are recorded in the protocol.
