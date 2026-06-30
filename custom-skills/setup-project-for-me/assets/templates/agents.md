# AI 协作说明

{{MARKER_START}}
本文件是项目专属的 AI 协作入口，默认中文维护。它不记录个人通用 AI 哲学，而是说明 AI 在这个项目里如何读上下文、放置文件、保持可接手。

## 项目目标

{{LONG_TERM_GOAL}}

## 工作区类型

{{WORKSPACE_TYPE}}

如果工作区类型仍为“未确认”，AI 在创建或移动交付物前应先澄清：当前目录本身是交付物，还是用于产出其他 GitHub、飞书、网站、报告等交付物的协作工作区。

## 开始前预读

所有任务开始前先读：

- `README.md`
- `AGENTS.md`
- `docs/README.md`
- `docs/work/current.md`

按任务需要继续读取：

- 设计、架构、流程相关：`docs/decisions/README.md` 和相关 ADR
- 领域概念、历史背景、踩坑：`docs/knowledge/README.md`、`docs/knowledge/glossary.md` 和相关知识文件
- AI 执行任务：对应的 `.agents/briefs/*.md`
- 外部同步或发布：`docs/integrations.md`、`deliverables/README.md`

## 强规则：保持可读、可接手

项目 owner 可能不是技术人员。AI 必须主动维护项目地图，不要假设用户会在事后整理结构。

- 可以创建完成任务所需的文件和目录。
- 新增长期目录、交付物或协作入口时，必须补充对应 README、索引或交接记录。
- 新增交付物时，更新 `deliverables/README.md`；如果交付物放在仓库内，也要给交付物自己的 README。
- 任务未完成且未来需要继续时，更新 `docs/work/current.md` 或新增 handoff。
- 做出长期决策时，写入 `docs/decisions/` 并更新索引。
- 发现可复用知识、术语、踩坑或外部系统规则时，写入 `docs/knowledge/` 或更新 `docs/knowledge/glossary.md`。

## 新内容放哪里

- 给人快速理解工作区的入口：根目录 `README.md`
- AI 如何工作的规则：`AGENTS.md`
- 用户提供的资料、链接和处理状态：`inputs/README.md`
- 要交付、发布、分享给外部或特定受众的成品：`deliverables/README.md`
- 当前状态或下一步：`docs/work/current.md`
- 可执行任务：`docs/work/tasks/`
- 会话交接：`docs/work/handoffs/`
- 长期决策：`docs/decisions/`
- 术语、背景知识、踩坑：`docs/knowledge/`
- 运行、验证、发布、排障步骤：`docs/operations.md`
- 外部平台链接和同步规则：`docs/integrations.md`
- AI 执行 brief：`.agents/briefs/`

完整决策树见 `docs/README.md`。

## 用户输入去向判定

当用户提供文件、链接、截图、PDF、草稿、聊天片段、飞书内容或其他材料时，先判断：

- 是否需要落盘到 `inputs/`
- 是否只需要提炼，不保留原始材料
- 是否只登记外部链接
- 提炼结果应进入 `docs/knowledge/`、`docs/work/tasks/`、`docs/decisions/` 还是 `deliverables/`
- 是否需要更新 `inputs/README.md`

AI 可以整理、重命名、分组输入材料，但必须在 `inputs/README.md` 记录来源、用途、处理状态和保留策略。删除已经落盘的用户原始文件前要确认。

## README 分层

- Workspace README：根目录 `README.md`，服务整个 AI 协作项目。
- Deliverable README：某个具体交付物自己的 README，服务外部用户、开发者或接收方。
- 不要把 Workspace README 直接当成交付物 README，除非当前工作区本身就是该交付物。
- 如果当前目录本身就是交付物，根目录 `README.md` 可以同时服务该交付物和协作入口；AI 应把内部协作细节沉淀到 `docs/`，不要把公开说明变成工作日志。

## 上下文收束

每次完成有意义的工作后，自检是否需要沉淀上下文。

需要沉淀的情况：

- 项目状态或下一步发生变化
- 有未完成工作需要未来继续
- 做出了长期决策
- 发现了可复用知识或踩坑记录
- 产生了新的任务、交付物或交接材料

不需要沉淀的情况：

- 一次性小修复
- 没有改变项目状态的查询
- 已在代码、测试或 README 中充分表达的信息

低风险文档可以直接更新，例如 `docs/work/current.md`、`docs/work/handoffs/`、`docs/knowledge/` 的新文件。新增 ADR、修改 README 项目目标、改变任务优先级时要更谨慎，必要时先确认。

## 外部同步

本地 `README.md` 和 `docs/` 是项目长期记忆的事实源。GitHub、飞书等外部系统是协作、发布或执行出口。

- 不要默认直接同步、发布、推送或改写外部系统。
- 需要同步时，先根据本地文档生成草稿。
- 从外部系统获得的重要目标、决策、任务变化，必须回写到本地 `docs/`。
- 外部链接记录在 `docs/integrations.md`，交付物链接记录在 `deliverables/README.md`。

## 验证

优先参考 `docs/operations.md` 中记录的运行、检查、发布和排障方式。没有明确命令时，不要猜测执行高风险命令；先补充 TODO 或询问。
{{MARKER_END}}
