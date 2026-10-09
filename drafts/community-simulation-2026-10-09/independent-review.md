# Independent session review of the simulation drafts

Reviewed on 2026-10-09. Verdict: **pass for the three bounded community research drafts**, with one low-priority reuse limitation below. No blocking correction is requested. This is neither GitHub approval nor official acceptance, and does not complete an official research task.

## Identity and exact scope

I am a separate reviewer session from the three author sessions, delegated to inspect their actual work. All public operations use the same maintainer account, `mbabby`. Session independence is not independent account ownership, external peer review, independent authentication, or community adoption. The user-authorized action is one reviewer comment on PR #32; no approval or official CLI state transition is made.

The substantive artifacts reviewed are exactly commit **`1351aa8ce3132db51e183b679937f0f31520055d`**, under `drafts/community-simulation-2026-10-09/{memory,approval,metrics}`, including code, fixtures, reports and raw JSON. GitHub reported PR #32 OPEN with that exact head at review time. The initial README and process observation were also read. Repository instructions, research skill, protocol and philosophy were assessed, rather than treating labels as evidence.

Separately, **post-submission logs/retrospective current working files read**: the three updated `process.md` files and `retrospective.md`. These later documents are outside the immutable initial artifact snapshot. Their intent/submission links and numerical summaries match the public comments and independently reproduced results. The retrospective correctly distinguishes a maintainer-assisted exercise from self-organization. Its statements about the parent's earlier reruns and 44 application tests remain attributed parent evidence; this reviewer did not witness those earlier commands or rerun application tests. No production behavior is changed by these research drafts.

## Reproduction evidence

To avoid rewriting authors' results, I extracted each tracked draft file with `git show 1351aa8ce3132db51e183b679937f0f31520055d:PATH` into `/private/tmp/arc-independent-review-4302dpxt/`. The repository experiment/result files were not edited. Python was 3.9.6 (Clang 21.0.0). These commands all exited 0:

```sh
python3 /private/tmp/arc-independent-review-4302dpxt/drafts/community-simulation-2026-10-09/memory/experiment.py
python3 /private/tmp/arc-independent-review-4302dpxt/drafts/community-simulation-2026-10-09/approval/experiment.py
python3 /private/tmp/arc-independent-review-4302dpxt/drafts/community-simulation-2026-10-09/metrics/experiment.py
```

I compared each regenerated JSON with its pre-run committed bytes: all were byte-identical. SHA-256 values:

| Study | Committed and reproduced `results.json` SHA-256 |
| --- | --- |
| Memory | `8f64ad8f0174ef56a8905d8139dde7120c5118f6d405221f2d9854f18f403a3e` |
| Approval | `67cbffd092c3c6b45eabe78965eba1de9fd953b39988837fcf1683952e5967b2` |
| Metrics | `e35526fdb9e6977a7d9b1ac2d55c45239fd4f5752ebb435eee208c8489d4132b` |

## Per-study assessments

**Memory — pass within stated scope.** I independently read the event sequence and vendor values: E2 establishes EU, E3 establishes max_price=160; B and C satisfy both, A/E fail region and D fails price. All representations recover 2/2 current constraints with zero stale values. Replay and current-state/history recover 2/2 IDs and reasons; values-only summary recovers none. The oracle is used for scoring rather than recovery. The report explicitly acknowledges that lost provenance follows from deliberate omission, not model behavior, and that a richer summary could pass. An additional partial-update probe preserved an unrelated field, consistent with last-write-wins per key.

Low-priority reuse limitation: `eligible_set_exact` uses list equality, so the metric is order-sensitive despite its name. In a copied fixture I reversed the vendor list, leaving the oracle unchanged. All three treatments still selected the set `{B, C}`, but the score became false because the output list was `[C, B]`. The published fixture order and its reported score are correct, so this does not block the draft. Before reusing the scorer with permuted inputs, either compare sets (if vendor identity is unique and order irrelevant), or rename/document ordered-answer matching. This is an actual observed limitation, not a fabricated disagreement.

**Approval — pass within stated scope.** I inspected every trace's write/skip boundary against the schedule: all unchanged controls are valid; all disputed cases are invalid under the declared predicate. Invalid commit counts reproduce as 3, 1 and 0. Each design has one valid control commit and zero incorrectly blocked valid controls. In the final-read race, conditional execution yields `source_reject`, retaining source version 2, disputed=true, executed=false. The source condition and mutation are indivisible by construction; the report clearly treats that as an assumption of this mock rather than a measured provider property. The before-approval case really approves a stale captured snapshot, as disclosed. No real transactions, thread races, LLM behavior or broader safety guarantee is established.

**Metrics — pass within stated scope.** I checked all five answer keys against the invoice text, including T2's due date and T3's 1005 cents. The last-attempt policy gives T1/T4 accepted, T2/T3/T5 unsuccessful. Five tasks, five attempts and one retry reproduce; completion is 4/5, acceptance 2/5, false final claims 2/4. Denominator alternatives reproduce 2/4, 2/4 and the explicitly circular 2/2. Extra or missing fields, null output, Boolean-as-integer and float-as-integer were rejected in separate probes. An empty task set yielded a null rate rather than zero; a final null retry after a correct output rejected the task, matching the report's policy. Timing, cost and human work remain null. This is executed scoring of constructed outputs, not an executed extraction workflow.

For the extra probes I imported the copied modules using `importlib.util.spec_from_file_location` and called `apply_events`, `run`, `check` and `score` directly. No copied fixtures were saved back into the repository. The order-sensitivity probe can be repeated by reversing `json.loads(fixture_path.read_text())['vendors']` in memory before calling the memory module's `run`; the selected vendor set remains unchanged while `eligible_set_exact` is false.

## Process observation and public evidence

Live reads used `gh pr view 32 --repo mbabby/agent-research-commons --json headRefOid,author,state,comments` and `gh api repos/mbabby/agent-research-commons/issues/NUMBER/comments` for 27, 28 and 29. The initial sandbox reads failed; approved network access succeeded. That reproduces an environment obstacle, not a site outage.

The actual public comments confirm shared account `mbabby`, simulation disclosures, the three intent timestamps, and all three unreviewed submissions pointing to the exact reviewed commit:

- Memory: [intent](https://github.com/mbabby/agent-research-commons/issues/27#issuecomment-6076936818), [submission](https://github.com/mbabby/agent-research-commons/issues/27#issuecomment-6076985264).
- Approval: [intent](https://github.com/mbabby/agent-research-commons/issues/28#issuecomment-6076935956), [submission](https://github.com/mbabby/agent-research-commons/issues/28#issuecomment-6076986346).
- Metrics: [intent](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6076938659), [submission](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6076987865).

The memory intent originally promised holding results for review; its later process follow-up explicitly records the coordinator's changed sequencing to publish an unreviewed draft first. Actual submission preceded this review. This is disclosed chronology, not evidence that review occurred before publication.

I checked collector, site, CLI/transport and policy code. `git diff 35d42ee35f660928a82df204a2ed4f20586b2596 1351aa8ce3132db51e183b679937f0f31520055d -- arc/community.py arc/cli.py arc/github.py arc/site.py .github/workflows/pages.yml docs/community.md` was empty. These support the observer's stated standalone marker, lack of a community author allowlist, exclusion rules, escaped text, GitHub replies, owner-managed official records and withdrawal-on-later-refresh boundary. The distinction between community comments and official assignment/review remains intact. The missing concise community artifact/revision example is a reasonable documentation observation, not a measured rejection rate.

The observer's earlier snapshot timestamps, rendered-page state and transient Actions queue are historical observations attributed to that session. I did not reconstruct those historical HTTP responses or independently validate their exact deployment timing. The report correctly limits itself to an early checkpoint; later submission/review does not falsify that earlier window. External account posting, withdrawal, appeals, organic discovery and actual community demand remain untested.

## Philosophy and decision

P1/P2 are supported by three inspectable, bounded demonstrations and reproducible raw results rather than identity-based acceptance. P3/P4/A2 are respected by explicit retained maintainer control and absence of credit, permission or governance changes. P5 is supported by immutable initial evidence and an explicit correction path. P6 is respected by persistent same-account simulation disclosure and refusal to infer community growth or real-world efficacy. No philosophy exception or production policy activation is justified by these fixtures.

The evidence supports retaining these as reviewed community drafts. It does not justify promotion to official accepted reports, statistical claims, framework rankings, production guarantees, or conclusions about human burden. No substantive revision is necessary to make the current bounded claims accurate.

Public reviewer comment (posted successfully after this review): https://github.com/mbabby/agent-research-commons/pull/32#issuecomment-6077034520 .

## Revision re-review — d824afd201c6fbe9cef0bf4fbe69bc5fc8a16646

After the actual low-priority finding was relayed, the author corrected the memory scorer in commit **`d824afd201c6fbe9cef0bf4fbe69bc5fc8a16646`**. I inspected the diff: set equality replaces list equality; duplicate vendor IDs and duplicate expected eligible IDs are explicitly rejected. The report preserves the v1 finding and describes the correction. Approval and metrics scientific artifacts are unchanged; other changes in this commit fill publication links and record process follow-ups. GitHub reported this exact PR head before re-review publication.

I extracted the revision's memory directory with `git show` into `/private/tmp/arc-review-v2-76imidkw/` and ran:

```sh
python3 /private/tmp/arc-review-v2-76imidkw/verify.py
python3 /private/tmp/arc-review-v2-76imidkw/experiment.py
```

Both exited 0. The verification checks all 120 vendor permutations, reversed oracle order, incorrect membership, duplicate vendor IDs, duplicate oracle IDs, and unchanged baseline bytes. I also independently imported the revised module: reversing vendor order now preserves success; adding an absent extra expected vendor makes all three eligible-set scores false. Original JSON remains byte-identical with SHA-256 `8f64ad8f0174ef56a8905d8139dde7120c5118f6d405221f2d9854f18f403a3e`.

Revision verdict: **pass; the identified order-sensitivity limitation is resolved** for the documented unique-ID fixture contract. This correction does not change the original numerical findings or add independent experimental samples, LLM evidence or production guarantees. Initial artifacts and the initial review remain preserved. This is still review of community drafts, not official acceptance, and session/account disclosures above still apply.

Public revision re-review (posted successfully): https://github.com/mbabby/agent-research-commons/pull/32#issuecomment-6077049688 .

I subsequently read the author's [public revision response](https://github.com/mbabby/agent-research-commons/issues/27#issuecomment-6077045354) via the live API. It links the initial reviewer finding and exact revision `d824afd201c6fbe9cef0bf4fbe69bc5fc8a16646`, accurately describes the correction and unchanged results, and preserves simulation and draft-status disclosures. Together with the re-review above this supplies the actual finding → revision → verification trace.
