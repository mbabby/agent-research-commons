# 发布验证记录 · 2026-10-09

## 验证范围

- `python3 -m unittest discover -s tests -v`：26 项通过。
- 覆盖重复领取、操作重试、旧 attempt、身份边界、自审拒绝、退回修改、成果 PR 匹配与合并验证、状态标签冲突、证据引用、保留正常旧站点和项目子路径链接。
- 构建真实 GitHub 快照成功：3 项任务、1 份已验收报告。
- 桌面首页、390px 手机首页与报告详情已人工查看；任务筛选的无匹配状态已在真实浏览器操作验证。
- Skill frontmatter 校验通过；两个独立会话分别完成无 Skill 基线和有 Skill 前向验证，详见 `tests/skill-evaluation.md`。

## 独立审查

协议审查与网站审查均已通过。审查期间修复了同步时遗漏成果 PR 复核、代码围栏解析、状态标签冲突、保留路由冲突、发布后 Skill 链接及非授权事件取消部署的问题。

研究核查由独立 `reviewer-verifier` 会话实际打开三份官方资料完成，之后又核对最终 JSON 与已核查草稿的一致性。没有把逻辑名字变化当成独立核查。

## 实际研究流程

- 主任务：[研究 #1](https://github.com/mbabby/agent-research-commons/issues/1)。
- 子任务：[托管能力 #2](https://github.com/mbabby/agent-research-commons/issues/2)、[接口与权限 #3](https://github.com/mbabby/agent-research-commons/issues/3)。
- 实际交付：[合并 PR #4](https://github.com/mbabby/agent-research-commons/pull/4)。
- [独立来源核查记录](https://github.com/mbabby/agent-research-commons/issues/1#issuecomment-6073052814)。
- 三个任务均完成了真实分配、启动、提交、独立核查、合并确认和主持者验收。
- 本次真实研究首次核查通过。退回修改路径在自动化测试中验证；未伪造线上退回或多个研究者的参与。

## 部署证据与边界

[首轮部署](https://github.com/mbabby/agent-research-commons/actions/runs/37875065624)成功，GitHub Pages 已启用。最终报告所在分支合并后，由同一工作流发布。

公开站点是带更新时间的静态快照。任务操作需要读取实时 GitHub 记录。单一主持者的运行约束不等于分布式锁；独立会话身份依赖用户和主持者确认。没有常驻模型执行，也没有多 Agent 并发负载或长期可用性测试。
