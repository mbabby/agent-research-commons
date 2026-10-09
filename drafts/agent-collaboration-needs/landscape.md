# 既有协作能力与差异化边界（未验收草稿）

任务 #8，attempt 1；研究会话 research-landscape；资料截至及访问日期：2026-10-09。本文核查官方规范与开源文档，区分“存在接口”“已运行服务”“存在需求”。三者不能相互替代。未做部署或互操作实测。

**已有能力。** A2A v1.0.0 的 Agent Card 描述能力、接口及认证要求，可经 well-known 地址、目录或直接配置发现。规范定义有状态任务、产物、查询、取消，以及流式或推送更新。[S1] 这说明发现与跨系统任务交换已有可复用约定；仅聚合描述文件不足以证明新协作机制。

MCP 2026-07-28 采用 host/client/server 架构；服务端暴露 tools、resources、prompts，宿主负责权限、上下文聚合与跨服务协调。[S2] 可将研究任务查询、证据读取或受控提交包装成工具，但包装后的权限、验收规则及运行者仍须由项目实现。

LangGraph 官方仓库提供源码并标注 MIT 许可，是可检查的开源编排替代方案。[S3] LangChain 官方 handoffs 文档用状态更新与 `Command` 在步骤或 Agent 间转移控制，并要求显式选择跨 Agent 消息。[S4] LangGraph persistence 文档区分线程检查点与跨线程 store，支持中断恢复等用途；内存 saver 在进程重启后丢失内容。[S5] 因而“能交接”“能保存状态”本身并非充分差异点。

**项目判断（推论）。** 本站当前的静态 Pages、GitHub Issue 任务、Python CLI 与人工启动会话，可承担公开证据和责任记录。项目 `agent.json` 是自定义入口清单，不能据文件名宣称 A2A 兼容，更不能当作可调用的 A2A 服务。若要接入，应明确协议版本、真实端点、身份映射、状态映射、错误与重试语义，并验证一次完整调用；仅提供兼容字段是准备工作。

值得验证的差异化假设是：围绕公开研究，把问题拆分、证据溯源、独立复核、返工与验收连接成可追查成果链。它的价值取决于减少了多少人工追问、错误接续与不可复核结论。目录可以作为入口，但本轮证据不足以支持“目录本身有竞争壁垒”，也不能宣称上述治理能力在市场上无人提供。

另一项推论是，替代方案应按使用者的工作比较：只需团队内部接续的用户可以选编排框架；需让现有客户端读资料、调用动作的用户可以选工具接口；需调用远端独立智能体的用户才更直接涉及跨系统任务协议。这些路径可以组合。本站若要求每位参与者额外克隆仓库、理解状态规则，却没有提高复核效率，便利性可能反而弱于现有工作方式。优先检验完整研究交付体验，比增加协议标识更能回答是否值得继续投入。

**未知与验证。** 这些资料证明技术能力有现成选择，不证明用户愿意跨团队委托、付费或持续回访；没有比较实际成本、可靠性、隐私边界及学习负担。建议以同一公开研究任务，对比人工 Issue 流程和协议适配流程，记录交接耗时、恢复成功率、证据缺口、复核返工及最终可用性。先验证成果链是否有收益，再决定是否建设常驻执行服务；这是本研究的产品推论，不是来源给出的市场结论。

来源均已实际打开；未查得页面发布日期时不以访问日期替代。S1/S2 为固定协议版本；S3–S5 是滚动仓库/文档，未锁定软件发布号。

- [S1 A2A v1.0.0 specification](https://a2a-protocol.org/v1.0.0/specification/)：§3、§4.1、§8；支持发现、任务与接口事实。
- [S2 MCP 2026-07-28 architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture)：Core Components、Design Principles；支持工具/上下文与宿主边界。
- [S3 LangGraph 官方仓库](https://github.com/langchain-ai/langgraph)：源码及 MIT license 标识。
- [S4 LangChain Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)：Basic implementation、Multiple agent subgraphs；支持交接与消息选择。
- [S5 LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)：Checkpointer vs. store、MemorySaver does not persist between restarts；支持持久化能力及限制。

本地事实依据：已读取 `docs/protocol.md`，并采用协调方给定的当前架构范围。直接执行 `python3 -m arc.cli show 8` 返回 GitHub API request failed；随后读取协调方当次实时核验的 `.cache/collab-live.json`，确认任务 #8 为 research-landscape、attempt 1、in_progress。本会话未作远端状态写入。
