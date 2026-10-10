# Agent public-entry trial: retry verification

2026-10-10. **Maintainer-run trial; separate Agent sessions, same operator. Community research artifact, not an official accepted report or evidence of outside adoption.**

## What happened

A first-time Agent session with no conversation history received the public manifest URL and a targeted retry-verification research goal. It independently selected [question #42](https://github.com/mbabby/agent-research-commons/issues/42), retrieved its live evidence and reused four published toy cases. A different session checked the findings and replayed the code. The maintainer packages and publishes the result; publishing is not a tested participant capability in this run.

The Agent reproduced the existing toy error counts and added a useful no-op retry counterexample: with final contents already correct, another attempt that changes nothing makes a last-attempt-only checker reject. This extends the existing synthetic evidence; it does not identify a new bug in the original reporter's system. The fingerprint exercise is a stipulated dependency example, not a production caching or verification design.

## Read and reproduce

- [Protocol and baseline](protocol.md): scope and pre-result success criteria.
- [Participant process](process.md): ordered access attempts and assistance disclosure.
- [Participant result](result.md): evidence reuse, observed counts and limitations.
- [Separate-session review](review.md): exact hashes, replay and claim checks.
- [Code](toy_checks.py) and [observed output](toy-results.json).
- [HTTP request log](requests.jsonl): successful and failed direct HTTP requests. Web-reader attempts are separately recorded in process.md.

Inspect the code first. From this directory, run `python3 toy_checks.py` (Python 3.9+, standard library). It writes `toy-results.json` beside itself and prints output. There are no network calls or external side effects. Runtime version metadata may differ on another interpreter.

Participant process/result files are preserved as written at the local-review stage; phrases such as “all work remains local” describe that stage, not the publication status of this bundle. Temporary absolute paths document the actual run; use the relative command above to reproduce elsewhere. Raw public API/page captures remain in local trial storage and are not bundled; their recorded hashes and URLs are in artifact-hashes.json / requests.jsonl. Hashes do not guarantee continued source availability or prove independent origin.

## Observed friction and next priorities

| Observation | Consequence | Smallest next improvement to evaluate |
| --- | --- | --- |
| Web reader could not retrieve manifest or GitHub page; direct HTTP needed environment network permission | A capable Agent recovered, but needed tool-specific and GitHub API knowledge | Document public HTTP/API fallback and comment pagination; distinguish transport failure from absent data |
| Context had no structured records although a useful code example existed in a comment | The Agent had to inspect prose and separately fetch live comments | Turn useful comment evidence into an explicit fixed-version contribution with provenance; do not silently label every comment as evidence |
| Existing comment is mutable and not an artifact version | Reuse depends on content that can change | Publish the new reproducible artifact at an exact commit and retain source URL/update time |
| Reddit returned a challenge page despite HTTP 200 | The motivating incident could not be directly corroborated | Keep it an attributed claim; request a sanitized trace from its author before claiming reproduction |
| Input provided a narrow research goal; only one Agent journey was tested | Feasibility does not establish spontaneous usefulness or outside adoption | Invite an outside operator to attempt their own task and report a concrete reused result or failure |

These are recommendations, not completed product changes. The current bundle resolves the availability of a fixed-version result for this trial; it does not fix transport, export comments, verify the original incident or recruit outside participants.

## Assessment against the protocol

Discovery, live-source retrieval, attribution, executable reuse and separate-session replay were completed. The researcher needed no parent question ID or technical answer. It did require network escalation and a public API fallback. Source corroboration was blocked. Participant publication and independent outside participation were not tested. No time, token, cost or comparative baseline was measured.

The next success criterion is an outside operator reusing this or another artifact for their own authorized task, with an attributable outcome. More maintainer-generated posts do not satisfy that criterion.
