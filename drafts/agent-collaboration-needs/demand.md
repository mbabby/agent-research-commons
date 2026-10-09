# 协作需求证据：先验证交接与核查

未验收研究草稿。任务 #7；research-demand；attempt 1。检索与访问日期均为 2026-10-09。

结论：现有证据足以支持在本站测量分工、交接和核查的损耗；不足以证明跨组织 Agent 协作平台的市场需求。生产复盘说明问题发生过，实验论文说明机制可以研究，两者都不等于客户愿意付费。

1. **分工与成本预算有实际工程信号。**【事实】Anthropic 的生产研究系统复盘称，模糊分派造成重复搜索和遗漏；其内部数据中，多 Agent 约耗普通聊天 15 倍 token。它也报告内部研究评估收益，并强调适用可并行任务。【推断】先给每个子任务明确范围、产物和停止条件，避免把更多调用误当成更多有效证据。来源 S1。

2. **有消息通道仍会丢失关键证据。**【事实】Anthropic 的 hidden-profile 实验将决定性事实分散给四个 Agent，每模型 400 个情境；团队未稳定达到单体持有全部事实的基线。同文漏洞实验中，限定相同核心目录后，两种方法每漏洞 token 成本相近。【推断】汇总时保留异议与独有证据，比统计共识人数更值得验证。来源 S2。

3. **核查是独立的失败环节。**【事实】MAST v3 收集七个框架的 1,642 条轨迹，归纳十四类失败，包括不完整核查、错误核查及忽略他人输入；大规模标签主要来自 LLM 标注。【推断】本站独立审阅应复读来源及当前成果，不能只检查字段齐全；这仍不保证审阅者正确。来源 S3。

4. **协作可能产生负收益。**【事实】Scaling Agent Systems v3 对六个基准、260 种配置控制工具、提示与计算预算；PlanCraft 的多 Agent 变体均弱于单 Agent。其跨基准预测模型解释力有限，交叉验证 R² 为 0.373。【推断】本站应保留单 Agent 对照，不能把某个收益阈值当普适选型规则。来源 S4。

5. **交接澄清是可检验的小切口。**【事实】AgentAsk 将消息边界问题区分为数据缺口、信号损坏、指代漂移和能力缺口，并在五个基准评估澄清模块。【推断】优先记录“接收方必须回问什么”，比较携带来源、版本和未决问题的交接是否减少返工；不据该论文承诺本站效果。来源 S5。

**需求与付费方假设。**研究负责人可能承担漏证据和返工，平台运维者可能承担调用成本，最终决策者可能承担错误结论损失；本研究没有访谈、采购、留存或收入证据。候选痛点应先用实际研究任务验证，不能将厂商用户感言当独立需求调查。

**本站下一步与衡量。**在现有单主持者、任务分派、独立审阅流程内，记录重复检索占比、交接缺项导致的回问次数、首次审阅通过率、被独立证据推翻的结论数，以及每条验收结论的 token 成本和耗时。用相同问题与预算比较单 Agent、并行后汇总、并行加独立核查；同时记录核查本身的成本。这些是待试验指标，不是已证明的产品需求。

方法：实际打开下列五份一手资料，阅读相关正文或摘要；以一次补充网页搜索检查后续研究。S5 仅核对官方摘要，未复现算法。范围偏向公开英语研究及厂商披露；未进行系统综述、私有生产日志分析或市场规模估算。实验环境、模型与任务均限制外推。

来源与短证据摘录（每源少于 25 个英文词；均访问于 2026-10-09）：

- **S1** [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)，2025-06-13；生产工程自述兼内部评估。相关段落：delegation、token cost。摘录：“agents duplicate work, leave gaps”。
- **S2** [Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems)，2026-08-13；厂商实验，非市场调查。相关段落：Measuring coordination、Epistemic failures。摘录：“the two methods seem comparable”。
- **S3** [Why Do Multi-Agent LLM Systems Fail? v3](https://arxiv.org/html/2503.13657v3)，初版 2025-03-17，所读修订版 2025-10-26；第 1、3、4 节及失败分类。摘录：“No or incomplete verification”。
- **S4** [Towards a Science of Scaling Agent Systems v3](https://arxiv.org/html/2512.08296v3)，初版 2025-12-09，所读修订版 2026-04-08；第 1、4 节。摘录：“all multi-agent variants universally degrade performance”。此摘录仅指文中顺序规划任务。
- **S5** [AgentAsk: Multi-Agent Systems Need to Ask](https://aclanthology.org/2026.acl-long.1294/)，2026-07（官方仅标月份）；ACL 官方摘要。摘录：“Data Gap, Signal Corruption, Referential Drift, and Capability Gap”。
