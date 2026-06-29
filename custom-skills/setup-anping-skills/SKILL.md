---
name: setup-anping-skills
description: "Anping 风格的 Codex 项目启动器：为当前 repo 初始化 AI 协作环境、主线程编排、项目知识库和可安装 Skills 清单。Use when the user explicitly asks to use Setup Anping Skills, 初始化/配置 Codex 项目, 启用 Anping 项目启动器, or prepare a repo for Anping-style Codex collaboration."
---

# Setup Anping Skills 项目启动器

把当前仓库初始化成适合 Codex 长期协作的项目环境。这个 Skill 是 prompt-driven，不是确定性安装脚本：先探索，后询问，再展示草案，最后写入。

目标不是把所有 Skill 都装上，而是按项目需要组合：

- Anping 自建 Skills，例如 `multi-agent-orchestrator`、`transfer-codex-sessions`。
- 外部优秀 Skills，例如 Matt Pocock 的 engineering skills。
- 项目级规则和知识文件，例如 `AGENTS.md`、`CONTEXT.md`、`CONTEXT-MAP.md`、`docs/agents/`、`docs/adr/`。

## 运行原则

- 开始前说明执行载体。长期或多文件初始化应遵守当前项目的 multi-agent orchestration 规则；如果工具政策不允许委派，说明使用 staged fallback。
- 一次只问用户一个部分的问题。不要把所有决策一次性抛给用户。
- 每个推荐的 Skill 都要说明用途、来源和为什么适合当前项目。
- 不要 vendor 第三方 Skill 源码。外部 Skill 只通过安装来源或引用目录接入。
- 写文件前先展示将要修改的文件、关键 block 和默认选择，得到用户确认后再写。
- 不要覆盖用户已有的 `AGENTS.md`、`README.md`、`CONTEXT.md` 或 `docs/agents/*` 内容；更新已有 block，避免重复追加。

## 工作流

### 1. 预检依赖 Skills

先检查当前会话和 `~/.codex/skills/` 中是否已有关键 Skills。读取 [references/skill-catalog.md](references/skill-catalog.md)，按项目需要判断哪些是必需、推荐或可选：

- Skill 选择和目标澄清：`ask-matt`、`grill-with-docs`。
- 领域和知识沉淀：`domain-modeling`。
- 主线程编排：`multi-agent-orchestrator`。
- 工程项目配置：`setup-matt-pocock-skills`。

不要自动安装所有缺失项。先向用户说明缺失的 Skill、来源、用途和推荐等级；用户确认后，再使用 `skill-installer` 或上游推荐方式安装。

### 2. 探索项目

快速读取当前仓库状态，只给用户简短快照，不做过度结论：

- `git remote -v` 和 `.git/config`：是否是 GitHub/GitLab/本地项目。
- 根目录 `AGENTS.md`、`CLAUDE.md`：是否已有 agent 规则或 `Agent skills` 相关章节。
- 根目录 `README.md`：是否已经写清项目目标。
- 根目录 `CONTEXT.md`、`CONTEXT-MAP.md`。
- `docs/agents/`、`docs/adr/`、`src/*/docs/adr/`。
- `.scratch/`：是否已有 local markdown issue convention。
- `~/.codex/skills/` 或当前会话的可用 Skills：哪些自建和外部 Skills 已安装。

### 3. 展示发现

用简短列表告诉用户：

- 当前项目大概是什么类型。
- 已存在的 AI 协作文件。
- 缺失但可能有价值的文件。
- 已安装/未安装的关键 Skills。
- 接下来会逐步询问哪些决策。

### 4. 逐步询问

每节都先用 1-3 句话解释用途和影响，再给默认建议，等待用户回答后进入下一节。

**A. 项目目标**

如果项目目标不清楚，优先使用 `ask-matt` 选择合适流程；需要边访谈边沉淀文档时使用 `grill-with-docs`。目标达成一致后，询问是否写入或更新 `README.md` 的项目说明。

**B. 主线程编排模式**

询问是否启用 `multi-agent-orchestrator`。说明收益是上下文治理、独立验证和减少 self-validation；代价是短任务可能增加总 token。用户同意后，继续询问是否写入项目级委派授权：允许主线程在遵守 system/developer/tool policy、仓库规则和审批要求的前提下，自主创建或使用 subagent / role agent 与用户可见 Codex thread。用户确认后，把主线程编排规则和授权写入 `AGENTS.md`，优先使用已安装 Skill 的模板。

**C. 上下文布局**

让用户选择：

- `Single-context`：根目录一个 `CONTEXT.md` 和 `docs/adr/`。多数仓库默认选这个。
- `Multi-context`：根目录 `CONTEXT-MAP.md` 指向多个上下文目录，适合 monorepo 或多产品仓库。

需要写入具体文件时，读取 [references/project-files.md](references/project-files.md)。

**D. 项目知识库**

询问是否创建面向人类和 AI 的项目知识库。默认建议：

- `docs/agents/anping-skills.md`：本项目启用的 Skill、用途和调用边界。
- `docs/agents/project-knowledge.md`：项目知识沉淀规则。
- `docs/adr/README.md`：ADR 使用说明。默认使用中文书写 ADR，除非用户明确希望改用英文或双语。

**E. 外部 Skills 接入**

按项目类型推荐外部 Skills。默认不要全装；只推荐当前项目会用到的组合。安装第三方 Skills 前先说明来源和理由，并请求确认。

### 5. 展示草案并确认

写入前展示：

- 将修改或创建的文件列表。
- `AGENTS.md` 中拟加入/更新的章节摘要，包括是否写入 `Delegation Authorization`。
- `docs/agents/anping-skills.md` 中拟记录的 Skill 清单。
- `CONTEXT.md` 或 `CONTEXT-MAP.md` 的布局。
- 是否安装或建议安装外部 Skills。

用户确认后再执行文件修改。

### 6. 写入项目配置

按用户选择写入：

- `AGENTS.md` 或已有 agent 规则文件中的 Anping/Codex 协作章节。
- `docs/agents/anping-skills.md`。
- `docs/agents/project-knowledge.md`。
- `CONTEXT.md` 或 `CONTEXT-MAP.md`。
- `docs/adr/README.md`。
- `.gitignore` 中的安全忽略项，例如 `codex_sessions/`，如果项目会使用会话迁移。

如果项目也使用 `setup-matt-pocock-skills`，不要重复写同一含义的 `Agent skills` block；更新或合并已有章节。

### 7. 验证

写入后先做轻量验证，再汇报完成：

- 重新读取已修改的关键章节，确认内容落在预期文件中。
- 检查没有重复的 Anping / Agent skills / Multi-Agent Orchestrator block。
- 确认应创建的文件存在，例如 `docs/agents/anping-skills.md`、`CONTEXT.md` 或 `CONTEXT-MAP.md`、`docs/adr/README.md`。
- 如果修改了 YAML、TOML、JSON 或其他可解析配置，使用本地解析器校验格式。
- 如果某个选择没有执行，记录原因和剩余风险。

### 8. 收尾

最后汇报：

- 已启用哪些能力。
- 修改了哪些文件。
- 哪些 Skills 已安装，哪些只是推荐。
- 后续用户如何说一句话触发这些能力。
- 剩余风险，例如外部 Skill 未安装、GitHub 凭据不可用、项目目标仍不明确。

不要自动 commit、push 或公开上传，除非用户明确要求。
