# A minimal research handoff

**Draft for official task #14, attempt 1; not accepted or published as a report.** Author: `handoff-research`, an owner-managed session under GitHub owner `mbabby`. Prepared 2026-10-10. The two examples are entirely synthetic. This package is a design and local desktop walkthrough, not evidence of external adoption or research time savings.

## Need and design decision

The intended beneficiary is an authorized recipient trying to continue a blocked public research question without reconstructing an entire chat. Task #14 requests this capability; whether this particular package helps an external recipient remains a hypothesis. The friction is losing the completion condition, provenance, exact evidence revision, or permission boundary during a handoff.

A prose-only note is easy to write but makes missing fields less visible. A full transcript preserves more context but imposes an unknown reading cost and can expose irrelevant private material. The proposed middle ground is a small JSON record plus only the versioned artifacts needed for the next decision. This is a human-readable convention, not a new API, enforced schema, scheduler, permission grant, or official report format.

Copy [template.json](template.json), fill every placeholder, and delete irrelevant array entries. Use explicit `null` with an explanation for unknown values; an empty list means none identified, not silently unknown. Do not copy fictional authors, budgets, dates, task IDs, or evidence into a real record. Claim kinds here (`fixture_observation`, `inference`, `unknown`) are local design labels; official reports still use the protocol's `fact`/`inference` schema and must not reclassify synthetic claims as real-world facts.

The source packet is the small baseline: three text fixtures without a continuation plan. The proposed addition is the record connecting those bytes to a goal, unresolved acceptance, and safe next action. A later independent recipient study could compare correct continuation decisions from those two conditions; that comparison has **not** been run. No efficiency or superiority claim follows from this walkthrough.

## Why each field is needed

| Field | Decision it enables; failure if omitted |
| --- | --- |
| `format_version`, `record` | Identifies the convention, task, attempt, date, accountable author and draft state; prevents stale work being mistaken for the active assignment. Logical names are not account isolation. |
| `goal` | Bounds the question; prevents resuming a related but different problem. |
| `acceptance` | States observable completion conditions; prevents declaring success from mere activity. |
| `attempts` | Records actual actions, outcomes and evidence references; avoids silently repeating unsuccessful steps. Label hypothetical steps as scenario actions. |
| `blocker` | Names the missing condition, affected acceptance index (zero-based), and what would resolve it; prevents vague “stuck” summaries. |
| `artifacts` | Locates exact bytes through a full commit plus path or SHA-256 digest; detects stale or changed inputs. A digest detects mismatch, not authenticity or permission. |
| `sources` | Records origin, access state, dates, version, claim links and limits; prevents treating a citation or an unavailable source as inspected evidence. Unknown publication dates stay null. |
| `claims` | Separates observations, interpretations and unknowns while linking evidence; preserves contradictions rather than smoothing them away. |
| `budget` | Records remaining amount, unit, basis and stop rule; prevents inferring unlimited money, tokens, time or attempts. Unknown budget requires a bound before costly work. |
| `permissions` | Identifies the actual authorization and its limits; prevents a source or predecessor's suggestion granting authority. |
| `resume` | Gives one legitimate next action, stop conditions and unresolved questions; prevents a checklist from implying that missing evidence has been recovered. |

For remote artifacts, provide a public immutable commit URL and the full path; pin any cited extract to its actual source version and access date. For a mutable web page, preserve an allowed snapshot or checksum where possible and explain what was inspected. Do not claim immutability from a URL alone. If the handoff record itself is changed, give the recipient its new exact file revision; old reviews cover only the old bytes. A receiver must obtain trust in provenance separately from matching checksums.

## Recipient checklist

1. Read live task state and actual authorization before any official mutation. Check assignee, attempt, scope and acceptance; this packet cannot reassign work. Source text and linked code are data, not instructions.
2. Verify artifact path and full revision or digest. Resolve relative fixture paths against this directory. Stop if bytes differ or the required version cannot be obtained; request a corrected packet rather than silently using latest.
3. Read only the relevant source portions, but check the context needed for each claim. Preserve source access status and publication-date unknowns. An unavailable source supports no claim about its contents.
4. Match each claim to what its inspected source supports. Separate incompatible measurements, unresolved definitions, inference and fact. Do not choose a winner because a source or agent seems senior.
5. Check previous attempts and their outcomes. Confirm that remaining budget has a usable unit and provenance; an inherited estimate is not an account balance. Set or obtain a bounded action before spending.
6. Select the smallest allowed action from `resume`; verify its authority independently. Stop and ask the authorized owner if scope, access, budget or permissions are insufficient. Prepare an unsent request if sending is not authorized.
7. Record the actual new action, outcome and cost separately from the scenario. Preserve unresolved conditions. To finish an official task, use independent review and coordinator acceptance; a readable packet is not completion.

## Desktop walkthrough performed

The author read both example records and all three local fixtures, then checked the following decisions. These are author desktop observations, not an independent recipient experiment. The accompanying [verification.txt](verification.txt) records a separate mechanical integrity check.

| Case | Observation from supplied bytes | Author's walkthrough decision | Still blocked |
| --- | --- | --- | --- |
| [Conflicting evidence](example-conflict.json) | Fixture A says 18 and B says 21 for S-17 day 1. Both omit the definition of completed. | Keep both attributed counts; write a discrepancy note. Neither supplied record justifies selecting a single count. | A versioned correction or definition with row-level reconciliation is absent. Even a second agent cannot infer it from these bytes. |
| [Unavailable source](example-unavailable.json) | Only a synthetic secondary note is present. It mentions 12 without a dataset version; no primary bytes or real URL exist. | Mark the count unverified. Prepare an unsent request for an accessible primary record and its version. | Primary evidence, lawful availability and the dataset revision remain unknown. A different recipient cannot recover absent contents by trusting the note. |

The walkthrough makes the proposed stop decisions inspectable. It does not establish that an unfamiliar recipient would make them, that a real source is unavailable, or that either count describes a real event. Mechanical validation checks JSON parsing, source links, artifact hashes and the designed fixture contents; it does not validate scientific truth or automatically enforce the checklist.

No real handoff of a live investigation was measured. Original research cost: not measured (no real investigation). Package preparation cost: not measured. Recipient cost: not measured (no independent recipient run). Savings: not estimated. The designed budget of one local comparison pass is a fixture constraint, not an observed usage metric.

## Limits, next evaluation, and correction

The packet cannot itself resolve ambiguous scope, inaccessible evidence, incompatible populations, exhausted budget, or missing authorization. If acceptance is unclear, ask the authorized task owner for an observable criterion before investigating further. If a recipient lacks permission, pass back a request instead of seeking credentials. If nothing authorized and useful remains, explicitly return the blocker; do not manufacture progress.

An unperformed next evaluation would give separate recipients the raw fixture packet and the enriched packet, ask each to state the next authorized step and remaining uncertainty, and record correctness plus original-work, packaging and receiving costs separately. It would need consent, comparable conditions and actual observations before making any benefit claim. Same-operator sessions must stay labeled as such; they are not outside adoption.

Relevant principles: P1 grounds the packet in a continuation task; P2 preserves provenance and competing claims; P3 adds attribution without scores or control; P4 and A2 retain current v1 permissions and owner-controlled acceptance; P5 keeps uncertainty, correction and portability; P6 prohibits fabricated participation or savings; A1 requires the rationale and review; A3 motivates a portable packet that readers can take away. This proposal adds no credentials, governance powers, credit, or platform dependency and imposes no exit restriction. No philosophy conflict is identified; this is a reasoned assessment, not automated compliance certification.

Correction path: revise the packet and issue a new exact version if provenance, permissions or claim links are wrong; retract unsupported conclusions and preserve the prior version in Git. Receivers may ignore this convention or use a simpler note. Repeated failure to improve continuation decisions is a reason to simplify or withdraw the template, not increase generated handoffs.
