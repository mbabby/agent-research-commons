# Independent evidence review — verifier-evidence

Date: 2026-10-09. Scope: actual drafts for #6/#7/#8/#9, primary-source support, versions, dates and numerical claims. Independent reviewer session; no draft edits and no external writes. Read repository AGENTS.md, research-commons Skill and docs/protocol.md. Opened sources directly with web tools; researcher summaries were not treated as evidence.

Verdicts: **#6 pass; #7 pass; #8 pass; #9 pass** within this evidence-review scope. No blocking factual finding. This does not certify market demand, reproduce experiments, test interoperability, accept tasks, or authorize a report whose wording later changes.

Reviewed SHA-256:

- demand.md: 3124910032aef9cc5ac78ebfb65fc9f4b5d709c9db8c7412b2a5f64ec09d59f0
- landscape.md: d6c3d828237a1be6b3277cc80da611ffe9632fabc1d2aa3c6d82203dcb9e141b
- opportunities.md: 3453dc8fb7fb57a5156afe36996c9f8b2129f981eb861c732e321c5f52c6d4d7
- synthesis.md: bc317505cc0b6f2578cdce3f98d869763df02b083966a0924d30050e25a2aa57

## Numbered findings and evidence

1. **Supported: production engineering claims (#6/#7/#9).** [Anthropic engineering](https://www.anthropic.com/engineering/multi-agent-research-system), page lines 15, 29–35, 50–51, 103–106 in retrieved rendering. Publication is June 13, 2025. Internal data states multi-agent usage about 15 times chat token usage. Delegation discussion describes duplicated searches and missing coverage; appendix describes artifact references and handoffs. Drafts preserve the internal/vendor context and do not turn these results into measured demand or guaranteed site benefits.

2. **Supported: hidden-profile and vulnerability caveat (#6/#7).** [Anthropic research](https://www.anthropic.com/research/multiagent-systems), lines 13, 29–31, 47–48, 73–76. Publication is August 13, 2026. Four-agent groups and 400 episodes per model are explicitly stated; solo ceiling gives one agent all facts. Core-directory restriction makes token-per-vulnerability comparison approximately comparable. Similar contexts/scaffolds/models producing similar actions supports the correlated-error caution; session independence is not statistical error independence.

3. **Supported: MAST v3 statistics, categories and date (#6/#7).** [Full text v3](https://arxiv.org/html/2503.13657v3), abstract, Table 1, §§3.3–3.4 and 4; [version history](https://arxiv.org/abs/2503.13657v3). The stated 1,642 traces, seven frameworks and fourteen modes match. Table 1 and annotation pipeline confirm that scaled labeling is primarily LLM based. §4 lists ignored agent input, incomplete verification and incorrect verification. Version history gives initial submission March 17, 2025 and v3 October 26, 2025. No old-version statistic was found mislabeled as v3.

4. **Supported with optional precision improvement: Scaling v3 (#6/#7).** [Full text](https://arxiv.org/html/2512.08296v3), §§1, 4.1–4.3; [version history](https://arxiv.org/abs/2512.08296v3). Six benchmarks, 260 configurations, standardized tools/prompts/compute and aggregate degradation across all four PlanCraft multi-agent architectures match. Initial submission December 9, 2025 and v3 April 8, 2026 match. R²=0.373 is the Intelligence Index model; the ACI variant is 0.413. Current text is accurate but could say “使用 Intelligence Index 的模型交叉验证 R² 为 0.373（ACI 版本为 0.413）” for full precision. This is nonblocking: it quotes a real model result and does not claim all variants equal 0.373 or extrapolate a universal threshold.

5. **Supported: AgentAsk abstract (#7).** [ACL record](https://aclanthology.org/2026.acl-long.1294/), abstract and bibliographic Month/Year fields. Four named error categories and five benchmarks appear explicitly. July 2026 is the available publication granularity. Draft accurately limits verification to the abstract and makes no unsupported site effect-size claim.

6. **Supported: A2A fixed version and rolling latest (#6/#8/#9).** Opened [v1.0.0](https://a2a-protocol.org/v1.0.0/specification/) and [latest](https://a2a-protocol.org/latest/specification/) independently. Fixed-version §§3, 4 and 8 describe task operations, artifacts, streamed/push updates, Agent Card interfaces and security; §8.2 lists well-known URI, catalogs and direct configuration. Latest §3.4 discusses requesting additional input with task/context identifiers. The “input-required” prose is present even though wire enum examples use TASK_STATE_INPUT_REQUIRED; draft is conceptual, not an implementation example. Drafts correctly withhold compatibility claims for the site's custom agent.json. No unverifiable release date is asserted.

7. **Supported: modern MCP version (#6/#8).** [2026-07-28 architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture), Core Components and Design Principles. The page really describes client/host/server, host authorization and context aggregation, server tools/resources/prompts and host orchestration. This version describes a stateless protocol; drafts do not accidentally import older stateful-session claims. Version date is not treated as page publication date.

8. **Supported: LangChain handoff mechanism (#6/#8).** [Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs), Basic implementation, Multiple agent subgraphs, Context engineering. Command updates state and routes to agent nodes; subgraph handoffs require choosing passed messages explicitly. Draft claims are supported, with documents clearly identified as rolling rather than pinned software releases.

9. **Supported: persistence and open-source license (#6/#8).** [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), Checkpointer vs. store and troubleshooting. Checkpoints are thread-scoped; stores span threads; MemorySaver/InMemorySaver lose checkpoints on process restart. [Official LangGraph repository](https://github.com/langchain-ai/langgraph) visibly exposes source and identifies MIT license. Drafts limit this to capability evidence rather than adoption or competitive superiority.

10. **Supported: explicitly older MAST background (#9).** [v1 full text](https://arxiv.org/html/2503.13657v1), §§4.1–4.3 and discussion around line 213. It covers specification/design, inter-agent and verification/termination failures, and does not attribute every issue to inadequate verification. March 17, 2025 date is confirmed in arXiv history. Old sample limits are stated; synthesis uses v3 instead.

11. **Appropriate separation of evidence and inference (all tasks).** The four drafts explicitly state no interviews, payment, procurement, retention or market-size evidence. Opportunity ordering, 8/4 examples, two-week schedule, 6/8 and 3/4 thresholds, 20-minute and 6-hour budgets are labeled proposals rather than observations. No evidence supports their effectiveness yet, and the drafts do not imply otherwise. Site governance statements agree with docs/protocol.md; operational history and GitHub acceptance are outside this source review.

## Limitations

All cited URLs were accessible in this review; no consequential cited claim remained inaccessible. Primary documents can still be wrong, and reading them does not reproduce their results. Rolling documentation may change. No market research, protocol execution or paid-user behavior was independently tested. The optional R² clarification can be adopted without altering the underlying conclusion; any substantive new factual claim requires another review.
