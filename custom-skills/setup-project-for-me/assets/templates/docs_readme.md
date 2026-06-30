# 文档地图

这里是 `docs/` 的地图，只说明项目长期文档放在哪里。项目总览和 owner-first 入口放在根目录 `README.md`。

## 区域

- `docs/knowledge/`：术语、背景知识、调研、踩坑和可复用上下文。
- `docs/decisions/`：轻量 ADR，记录长期影响项目方向、结构、流程或协作方式的决策。
- `docs/work/`：当前状态、任务、交接和正在推进的工作。
- `docs/operations.md`：运行、验证、发布、排障等操作手册。
- `docs/integrations.md`：GitHub、飞书等外部系统入口和同步原则。

## 相关入口

- [根目录 README](../README.md)：给人看的项目入口；如果当前目录本身是交付物，它也可能同时服务交付物读者。
- [AI 协作说明](../AGENTS.md)：给 AI 看的项目协作入口。
- [输入材料索引](../inputs/README.md)：用户提供的资料和处理状态。
- [交付物索引](../deliverables/README.md)：项目计划交付或已经交付的成品。

## 新内容应该放哪里？

- 是给人快速理解工作区的入口？放根目录 `README.md`。
- 是 AI 如何工作的规则？放 `AGENTS.md`。
- 是用户提供的资料、链接或原始材料？登记到 `inputs/README.md`。
- 是要交付、发布、分享给外部或特定受众的成品？登记到 `deliverables/README.md`。
- 是当前状态或下一步？放 `docs/work/current.md`。
- 是可执行任务？放 `docs/work/tasks/`。
- 是会话交接？放 `docs/work/handoffs/`。
- 是长期决策？放 `docs/decisions/`。
- 是术语、背景知识、踩坑？放 `docs/knowledge/`。
- 是运行、验证、发布、排障步骤？放 `docs/operations.md`。
- 是外部平台链接和同步规则？放 `docs/integrations.md`。
- 是 AI 执行 brief？放 `.agents/briefs/`，并引用对应的任务或交接文档。

## 归档原则

默认通过索引和状态归档；只有当某类文件数量明显变多、影响阅读时，才创建对应的 `archive/` 目录。

## 索引维护

新增 ADR、任务、交接、知识文件或交付物时，同步更新对应目录的 `README.md` 索引表。
