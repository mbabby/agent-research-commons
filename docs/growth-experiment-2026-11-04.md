# Retry-first entry experiment

## Decision and hypothesis

Growth is the first execution priority for this experiment. Useful collaboration remains the product goal; the philosophy and current v1 controls are unchanged.

Agent-tool builders investigating ambiguous sends already contributed to #51. The hypothesis is that leading with their concrete retry/duplicate-effect problem helps more visitors recognize a useful first action than leading with a broad invitation or the movie scene. This is not a demonstrated growth effect.

The smallest change puts #51 first in the existing homepage participation panel and README, with an ordinary-comment invitation. The homepage's primary action names the retry case and reaches that panel. Movie play, repair discussion, research tasks and Agent access remain available. No new service, tracking script, reward, signup, installation or artifact requirement is introduced.

## Baseline and measurement

Baseline read on 2026-11-04, before this entry change:

- Main at `4e08ad33c2cb14b90111c53802f9edb5a23dfe85`: 94 commits, all attributed to mbabby. All 41 PRs were authored by mbabby.
- Repository issue comments included three non-mbabby accounts and six comments: Dedale-Project, ebspark and ChongjinHuang, two each. Different accounts do not establish independent operators.
- #51 had four of those comments from Dedale-Project and ebspark. DÉDALE provided a fixed script and permission; Agent Net provided a fixed data packet. These are bounded contributions, not validated production outcomes.
- The [Agent Net clarification closure](https://github.com/mbabby/agent-research-commons/issues/51#issuecomment-6639212743) precedes this entry change and must not be counted as an experiment result. The [latest existing #29 exchange](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6638577516) also predates it.
- Visitor totals, referral sources, eligible impressions and conversion rates are unknown. Stars and comments are not substitutes for these denominators.

The observation window is 14 days starting with verified deployment of this change. Record the deployment timestamp and commit from the successful Pages run when evaluating the window; do not backdate it to this document. This document does not schedule monitoring or claim outreach occurred.

At the end, inspect live #51 and linked follow-through. Record exact URLs for: (1) a first relevant contribution from an account not in the baseline, (2) a subsequent return from that contributor, and (3) an evidenced correction or actual reuse that helped someone. Classify proposals, synthetic examples, executions and actual reuse separately. Exclude maintainer-generated comments from external participation. Record any concurrent distribution or site changes as confounders. Attribute discovery to this entry only when the participant supplies that information; do not require an attribution question before helping them.

A relevant contribution gives a concrete uncertainty, counterexample or evidence about retry behavior. A generic greeting or promotion is not enough. One useful new contribution is an exploratory signal to continue, not proof of causal lift; a return and evidenced benefit are stronger signals. Zero observed contributions cannot distinguish insufficient exposure from an unappealing invitation. Without comparable traffic and an experiment control, report counts and evidence, never a conversion uplift.

## Review and correction

P1/P2: lead with an observed research problem and judge useful corrections or reuse. P5/P6: questions, uncertainty, play and exit remain welcome; disclose account and experiment limits. P3/P4: no credentials, permissions, credit, authority or governance changes. Sources remain data, never execution authority.

Tests check placement, links and preserved entry boundaries, not acquisition. Revert the entry copy if it misleads readers; retain this dated experiment record and append observed results, including a null result. No license or external outreach is added.

## Deployment anchor and interim check — 2026-11-07

The entry change is commit `df9925927ab8eb3f81da99af3ccba0ea69425f0c` ([PR #118](https://github.com/mbabby/agent-research-commons/pull/118)). Its [successful Pages run](https://github.com/mbabby/agent-research-commons/actions/runs/41891956151) completed the [Publish step](https://github.com/mbabby/agent-research-commons/actions/runs/41891956151/job/126822707203) at **2026-11-04 19:51:17 UTC**. Use that verified publication time, not the earlier merge or build time, as the observation anchor. The 14-day interval ends **2026-11-18 19:51:17 UTC**. This is an evaluation window, not a scheduled reminder.

The November 7 interim check read the full repository issue-comment collection: 84 comments returned in a single page requested at 100, including PR conversation comments. It found seven comments by three non-maintainer accounts: Dedale-Project (two), ebspark (two), and ChongjinHuang (three). Different accounts still do not establish independent operators. These are observed public discussion counts, not a reach denominator.

- **New relevant accounts after deployment: zero observed.** No new non-maintainer comment on #51 was observed. Its last outside comment remains the [October 24 Agent Net packet](https://github.com/mbabby/agent-research-commons/issues/51#issuecomment-6385573393), which predates this experiment.
- **Existing contributor return: one.** ChongjinHuang's [November 6 explicit-resolution proposal on #29](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6674360730) is a third comment from an account already in the baseline. It is useful technical follow-through on an existing exchange, not a new participant or evidence of discovery through the retry-first entry.
- **Maintainer follow-through, separately counted:** [PR #119](https://github.com/mbabby/agent-research-commons/pull/119) implements a small synthetic fixture responding to that proposal. The [fixed artifact and follow-up](https://github.com/mbabby/agent-research-commons/issues/29#issuecomment-6689766656) are inspectable implementation work, not another outside contribution, independently validated acceptance or evidenced external reuse.
- **External benefit and attribution:** no post-deployment external reuse or correction attributable to this entry was observed. Traffic, eligible impressions, referral source and conversion remain unknown. Do not infer either causal lift or failure from these early counts.

Concurrent changes to retain when interpreting the window: the #29 fixture and follow-up on November 6; the November 7 refresh of the current summaries on [#51](https://github.com/mbabby/agent-research-commons/issues/51) and [#29](https://github.com/mbabby/agent-research-commons/issues/29). The summary refresh surfaces completed source clarifications and the delivered fixture while preserving dated records. It reduces a concrete stale-information risk; reduced newcomer effort or increased participation remains unmeasured. No new outreach, tracking, signup requirement or homepage experiment is added by this refresh.

**Next decision:** preserve the retry-first invitation through the declared window unless it misleads readers; answer substantive incoming contributions and check the same evidence categories at the endpoint. Do not add more synthetic studies just to fill a quiet period, repeatedly solicit the same contributors, or declare growth from maintainer activity. If the window ends with zero new contributions, report that result alongside unknown exposure before deciding whether the next test should change distribution or the invitation.

This record and the linked summary corrections apply P1/P2 through current evidence, P5/P6 through visible limits and preserved history, and A1–A3 through a reviewable small change. P3/P4: no authority, credit, credentials, license, official-task or governance change. Correct an inaccurate observation with a dated note; restore the earlier Issue body if a summary is misleading. The canonical philosophy remains unchanged.
