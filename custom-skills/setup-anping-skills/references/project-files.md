# Project Files

`setup-anping-skills` 写入项目配置时使用这些约定。先展示草案，得到用户确认后再写。

## AGENTS.md

优先更新项目已有的 agent 规则文件：

1. 如果 `AGENTS.md` 已存在，更新它。
2. 如果只有 `CLAUDE.md` 存在，询问用户是否也要为 Codex 创建 `AGENTS.md`。
3. 如果都不存在，询问用户是否创建 `AGENTS.md`。

建议加入一个 `## Anping Codex Setup` 或合并到已有 `## Agent skills` 章节，记录：

- 本项目是否启用主线程编排模式。
- 是否写入 `Delegation Authorization`：项目级授权主线程按规则自主创建/使用 subagent、role agent 和用户可见 Codex thread。
- 当前启用的 Skills 和各自边界。
- 上下文布局：`Single-context` 或 `Multi-context`。
- 项目知识库位置。
- 会话迁移或凭据相关安全边界。

如果启用 `multi-agent-orchestrator`，从已安装 Skill 的 `references/agents-section.md` 复制主线程编排规则；不要手写残缺版本。写入前提示用户确认 `Delegation Authorization`，并说明它不能覆盖 system/developer/tool policy 或跳过高风险操作审批。

## docs/agents/anping-skills.md

推荐结构：

```markdown
# Anping Skills Setup

## Enabled Skills

| Skill | Purpose | Source | When to use |
| --- | --- | --- | --- |

## Referenced Skills

记录已推荐但未安装的外部 Skills。

## Operating Rules

记录本项目关于主线程、subagent/thread、知识库、任务管理和安全边界的约定。
```

## docs/agents/project-knowledge.md

推荐记录：

- 哪些信息写入 `CONTEXT.md`。
- 哪些决策写入 `docs/adr/`，以及 ADR 默认使用中文书写。
- 哪些长期知识只写在 README 或产品文档里。
- 什么时候需要更新知识库。

## CONTEXT.md

`Single-context` 默认模板：

```markdown
# Project Context

## Purpose

## Domain Language

## Architecture Notes

## Current Constraints

## Open Questions
```

## CONTEXT-MAP.md

`Multi-context` 默认模板：

```markdown
# Context Map

| Area | Context file | Notes |
| --- | --- | --- |
```

每个子上下文目录可以有自己的 `CONTEXT.md` 和 `docs/adr/`。

## docs/adr/README.md

推荐内容：

```markdown
# 架构决策记录

这个目录用于记录需要长期保留的架构决策。ADR 默认使用中文书写，方便中文使用者长期阅读和维护；只有在项目协作需要时，才改用英文或中英双语。

每一篇 ADR 建议包含：

- 背景
- 决策
- 影响
- 备选方案
```

## .gitignore

按需追加：

```gitignore
codex_sessions/
```

只有项目需要使用 `transfer-codex-sessions` 或会话 bundle 时才添加。
