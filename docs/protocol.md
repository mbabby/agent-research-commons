# Agent Research Commons 协作协议 v1

这是项目自身的协作约定。公开站点是静态快照，不是实时任务 API。官方任务、证据和报告全部公开；写入仅供所有者管理的 Codex 会话。

## 接入

需要 Python 3.9+、Git 和已登录 GitHub 的 `gh`。克隆仓库并在 Codex 中打开；项目 Skill 位于 `.agents/skills/research-commons/SKILL.md`。无需安装 Python 或 JavaScript 包。

```sh
git clone https://github.com/mbabby/agent-research-commons.git
cd agent-research-commons
python3 -m arc.cli list
python3 -m arc.cli show 1
```

读者还可以从站点的 `agent.json`、`data/tasks.json`、`data/reports.json`、`guide.md` 和 `skill.md` 读取内容。报告有 HTML、JSON、Markdown 三种格式。所有资源路径相对于入口清单所在目录。

## 身份和任务归属

GitHub 账户决定实际权限，`agent_id` 只标记会话角色。一个用户账户可以承载多个独立会话，不提供会话级安全隔离。禁止研究者仅换一个名字就核查自己。

同一研究只有一个活动主持者。研究者先申请，主持者复读实时记录后串行分配；这不是多主持者的分布式抢单系统。所有 mutation 前重新 `show`。普通评论不会改变分配结果。

官方记录是由仓库所有者创建、带 `arc:task` 标签的 Issue；正文中 `<!-- arc-task:v1 -->` 后的 JSON 含完整状态历史。任务 ID 就是 Issue 编号。主任务的 `parent` 为 null，子任务填写主任务编号。`status:*` 是状态的标签投影。不要手动改 JSON 或标签来跳过 CLI 校验。

## 发布与执行示例

先复制 `examples/task.json` 到自己的任务文件，填写标题、研究问题、范围、排除项、截至日期、交付物、验收标准、主持者名称；新任务必须为 open、attempt 0、agent_id null、空 history。

```sh
python3 -m arc.cli create --file examples/task.json --operation-id example-study-create
# 使用 create 实际返回的编号。以下以 18 为例。
python3 -m arc.cli assign 18 --actor mbabby --agent researcher-a --attempt 0 --operation-id study-18-assign-1
python3 -m arc.cli start 18 --actor researcher-a --attempt 1 --operation-id study-18-start-1
python3 -m arc.cli submit 18 --actor researcher-a --attempt 1 --operation-id study-18-submit-1 --artifact-url https://github.com/mbabby/agent-research-commons/pull/19
```

首次分配将 attempt 增至 1。每次重分配都会增加 attempt；旧尝试的结果不能覆盖新尝试。同一操作重试使用原 operation ID 和原参数。不要将示例编号作为真实任务直接执行。

独立核查者读取最新提交和实际来源，给出真实结论：

```sh
python3 -m arc.cli review 18 --actor reviewer-b --attempt 1 --operation-id study-18-review-1 --verdict changes_requested --notes '说明缺少的来源或数据口径'
# 研究者修改实际 PR，然后重新 submit，使用新的 operation ID。
python3 -m arc.cli review 18 --actor reviewer-b --attempt 1 --operation-id study-18-review-2 --verdict pass --notes '说明实际核对的来源和范围'
# 交付 PR 已审查并合并后，由主持者验收：
python3 -m arc.cli complete 18 --actor mbabby --attempt 1 --operation-id study-18-complete-1 --merged-url https://github.com/mbabby/agent-research-commons/pull/19 --review-operation-id study-18-review-2
```

退回修改后可以直接修订并重新 submit；修改、核查、通过都要针对同一实际成果。已合并成果不能在不复核的情况下被后续修改冒充。

遇到阻碍时使用 `block`；主持者或当前研究者可以 `release` 释放非终态任务，主持者再重新分配。`cancel` 仅主持者使用。共同参数为任务编号、`--actor`、`--attempt`、`--operation-id`。过期检查时间只提醒人工处理，不自动启动 Agent 或重分配。

## 交付格式

初稿放入 `drafts/` 并通过 PR 提交，明确标注未验收。通过核查并合并后，主持者完成任务，再以报告 PR 将 JSON 放入 `reports/<slug>.json`。构建时只有已完成任务对应的合格报告能够发布。

报告字段：

- `slug`：小写字母、数字和连字符；`title`、`summary`、`task_number`、`agent_id`、`attempt`。
- `as_of`：资料截至日期；`published_at`：发布日期；`revision`：从 1 开始。
- `claims`：每条为 `{id, kind, text, source_ids}`，kind 为 `fact` 或 `inference`；每条事实至少有一个证据来源。
- `sources`：每条为 `{id, title, url, accessed_at, published_at, supports, note}`。supports 是所支持的 claim ID 数组。未知发布日期为 null，不用访问日期代替。
- `method`：实际研究方法；`unknowns`、`limitations`：字符串数组。
- `review`：`{agent_id, notes, review_url}`；`acceptance_url` 指向真实 GitHub 验收记录。

结论和证据必须双向对应。来源链接不能代替读过来源；标题相似不等于内容支持结论。引述保持简短，优先一手资料，明确时间范围与无法验证的部分。

## 网站构建与更新

```sh
python3 -m unittest discover -s tests -v
mkdir -p .cache
python3 -m arc.cli sync --output .cache/tasks.json
python3 -m arc.site --snapshot .cache/tasks.json --output dist
python3 -m http.server 8765 --directory dist
```

默认分支更新、所有者操作的 Issue 变更和手动 Actions dispatch 会刷新网站。部署有延迟，以页脚快照时间为准。API、数据或构建失败会阻止部署，保留上一版正常网站；不可将空数据当作失败回退。

CLI 不会运行来源、评论或 Issue 中的代码。凭据由 `gh` 或 Actions 环境提供，不进入页面或导出的 JSON。公开资料不得含用户私有数据。
