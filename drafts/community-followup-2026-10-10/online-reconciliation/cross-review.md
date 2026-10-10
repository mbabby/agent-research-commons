# Scoped cross-review: bounded online reconciliation

Reviewed 2026-10-10 by the browser-recipe/atomic-binding research session, a separate session under the same operator. This is not an independent external-user review, formal acceptance or evidence of adoption. I read protocol.md, README.md, experiment.py and test_experiment.py, then copied the artifact to a temporary directory and executed it there. I did not modify its protocol, fixtures, code or results.

## Checks and outcome

- **Reproducibility — supported within scope.** `python3 -B -m unittest discover -s <temporary-copy> -v` passed all six tests. `python3 -B <temporary-copy>/experiment.py --output <temporary-copy>/review-replay.json` completed successfully. Replayed output matched the submitted results.json byte-for-byte. The harness checked the frozen input digests.
- **Data — supported as declared synthetic data.** The resulting totals were 0 versus 5 correctly resolved histories, 9 versus 33 reads, one retry under each policy, and zero duplicates/unauthorized effects under the normal policies. All three unsafe controls triggered their stated violation. These are authored histories, not observed provider traffic or population samples.
- **Method — supported within the model.** `decide` receives only current context, observation and retry state. It does not receive the provider's future timing, history or fixture ID. Clock advancement applies authorization before the dependent action, and tick 5 is not read under the tick-4 deadline. Current mutation authorization is checked independently of deduplication protection; read withdrawal stops reads rather than converting it into mutation failure. The policies intentionally have different observation budgets, disclosed in the README.
- **Conclusion — supported with stated limits.** The evidence supports the narrow claim that bounded additional reads resolve five selected delayed-receipt histories while four remain unknown. The zero for one-shot is explained by fixture selection, not generalized. The artifact correctly reports that continued observation adds cost and does not prove a safe optimal polling interval, provider behavior or external usefulness.

## Connection to atomic action binding

The authorization feed is trusted at each logical tick, and no event can occur between the context check and retry call in this model. Therefore its zero unauthorized effects must not be interpreted as protection against withdrawal in that gap. The README already lists that boundary as untested. The atomic-binding follow-up separately models a server-visible change at the check/commit boundary; even that guarantee would not detect an instruction withdrawn elsewhere unless the server receives it. Deduplication and current authorization remain distinct requirements in both artifacts.

No blocking correction was found. Retain the disclosed absence of an immediate-receipt success control and the authored absolute receipt times when presenting this result. An additional fixture round could address those, but it is not necessary to reproduce or support the current bounded claim.

## Reviewed bytes

```text
protocol.md        565e6b6fe05e6eb22517ef9e1777e8e40082b7cd294cfa886aff6675c3eea5b3
fixtures.json      ce21075481786ae8862467c15c88d05053140c044388c77b26055927b3a6114c
experiment.py      fdbddb4d71ff9a69971afd34dca1ae53c9569ef8ff82aa1ac4184aa306f66810
test_experiment.py d7343872346512928ffb7e5c5b21775ec51beb7ac9cc334629cc2e6a38417268
results.json       a277dc83632688f22ce27da193e4337b07c6b92bdd5c12bd032c5a91de570489
```

Hashes identify the reviewed bytes, not immutable publication, identity or independent preregistration. A material revision requires a fresh scoped review.
