---
name: multi-agent-orchestrator
description: "用于复杂或长期 Codex 项目的 multi-agent orchestration：主线程模式/编排模式下隔离 workstreams，自动派发 role agents/subagents、子智能体/子Agent、子线程/新线程/用户可见执行线程，治理上下文并避免 self-validation/自恋。Use when the user asks for 主线程模式、编排模式、多 Agent 协作、多线程协作、派发任务、回收结果、归档线程、Thread 工具自检、create_thread/codex_app.create_thread、list_threads/read_thread/send_message_to_thread、create-visible-thread、审查、专家评价、质量评估、独立验收、测试策略、安全隐私性能评估、修改文件、提交、推送 GitHub、配置、安装、凭据流程、排障、长命令、长日志, or delegated workstreams/context hygiene."
---

# Multi-Agent Orchestrator 多 Agent 主线程编排

## 实现方式

本 Skill 主要提供文档、触发描述和 AGENTS.md 模板。核心逻辑应通过项目根目录的 `AGENTS.md` 实现，因为 `AGENTS.md` 会直接约束 AI 在该项目中的行为。

本仓库的根 `AGENTS.md` 已包含 `Multi-Agent Orchestrator Mode`，用于当前项目。把这个 Skill 安装到其他长期项目时，应将 [references/agents-section.md](references/agents-section.md) 中的章节复制到目标项目 `AGENTS.md`，否则 Skill 只能作为提示和说明，无法稳定约束主线程行为。

`AGENTS.md` 负责实现：

- 任务类型判断和触发规则。
- subagent / 用户可见 thread 的选择与 spawn 策略。
- 状态处理：`DONE`、`DONE_WITH_CONCERNS`、`NEEDS_CONTEXT`、`BLOCKED`。
- 打断机制、状态监控、agent 自动关闭和 thread 归档提醒。

## 目的

使用这个 Skill 时，把复杂 Codex 工作作为 main-thread orchestration 来推进。主线程负责意图、边界、决策、证据整合和最终汇报；不承接主要审查结论，也不承接长执行或发布操作。执行载体负责命令密集或细节密集的工作，例如调研、实现、测试、review、修改文件、提交、推送、配置、安装、排障、发布检查、UI 操作、凭据流程和长日志。

目标不是尽量多用 Agent，而是保护判断质量、减少上下文污染，并避免 self-validation。

## AGENTS.md 运行规则摘要

以下内容是 `AGENTS.md` 行为规则摘要。执行时优先遵守当前项目 `AGENTS.md`；如果项目中没有对应章节，先安装或补齐 `references/agents-section.md`，再开始长期/复杂任务。

- 开始执行前，先说明选择的执行载体和原因：main thread、role agent/subagent、用户可见 Codex thread、staged single-thread fallback，或混合方式。
- 按任务长度和执行密度选择载体：短、窄、一次性任务可以在主线程内派 role agent/subagent；较长、多轮、会产生执行层对话或需要持续上下文的任务，应优先切到用户可见 Codex thread。
- 当用户要求“审查、专家评价、质量评估、架构检查、找问题、验收、测试策略、安全/隐私/性能评估”时，默认委派给独立 role agent/subagent 或用户可见 thread。主线程不要亲自生成主要审查结论，只负责给出边界、回收证据、整合判断。
- 当任务涉及修改文件、提交 git、推送 GitHub、创建/更新 PR、安装配置、凭据流程、长命令、长日志、反复排障、大量读文件、UI 观察、发布检查或多轮实现时，默认移到执行载体。主线程只保留调度、授权边界、结果整合和最终汇报。
- 不要把“用户只能和主线程沟通”当作硬规则。为了保护项目上下文，主线程可以要求用户去子 thread 处理执行层对话。
- 优先遵守更高层约束：system/developer 指令、工具政策、仓库规则、审批要求和用户安全偏好。如果理想载体被限制，说明 fallback。
- 用户可见 Codex thread 是主线程可以自主选择的执行载体。较长、多轮、会产生大量执行层上下文或需要持续状态的任务，主线程可以主动创建或要求切换到 thread，并说明目标、边界和回收方式；不要要求用户逐次明确提出“创建新 thread”才行动。
- 如果 `create_thread`、`codex_app.create_thread`、`list_threads`、`read_thread`、`send_message_to_thread`、`set_thread_archived` 等 thread 工具已暴露，优先直接使用这些工具创建、命名、投递、读取和归档用户可见 thread；不要再停留在“没有直接接口”的旧假设上。
- 如果更高层工具政策阻止自主创建，则说明限制，并请求授权。
- 需要委派但不确定工具是否可用时，先使用可用的工具发现机制，例如 `tool_search`。如果没有真正可用的 subagent/thread 机制，明确说明，并用分阶段方式模拟隔离：实现、独立检查、整合。
- 中间更新和最终汇报使用用户的语言。
- **agent 结果消费后立刻关闭**：不要让已完成的 subagent 堆积。结果回收、验收完成后，马上调用 `close_agent` 释放资源。

## 执行载体

- Main thread：intake、planning、decision-making、integration、少量只读检查，或委派成本高于收益的强顺序任务。只有任务极小、低风险且没有合适执行载体时，才可做微小修改；不得承担主要 review/audit 结论、长执行、提交、推送、安装配置或凭据流程。
- Role agent / subagent：短、窄、一次性、有边界的调研、实现、测试、review、架构批判、质量评估、安全/隐私/性能检查、迁移规划，或任何需要独立视角并能返回简洁证据的任务。
- 用户可见 Codex thread：当主线程判断必要且工具政策允许时，用于较长或多轮执行分支、反复用户输入、环境配置、安装、凭据流程、提交/推送、UI 驱动任务、大型 debug loop，或需要在主线程之外保留持久上下文的工作。
- Staged fallback：没有可用委派工具时，显式拆分阶段，避免实现者推理成为唯一验证面。

如果主线程开始堆积执行日志或低层排障细节，应停下来重新选择执行载体。

## Thread 工具自检与扩展

当任务应该进入用户可见 Codex thread 时，主线程先做工具自检，不把“当前没有直接按钮/工具”当成最终结论：

1. 检查当前可调用工具：如果有 `create_thread` 或 `codex_app.create_thread`，优先直接创建用户可见 thread；配合 `list_threads`、`read_thread`、`send_message_to_thread`、`handoff_thread`、`set_thread_title`、`set_thread_archived` 等工具完成投递、验证、交接和归档提醒。
2. 如果没有直接创建工具，先用 `tool_search` 等可用发现机制确认是否能加载 thread 工具；不要只因为初始工具列表里没看到就放弃。
3. 如果仍没有直接工具，检查能否补齐桥接能力：Codex CLI、Codex Desktop deeplink、MCP/插件接口、`codex_app` 工具、`codex app-server` / `remote-control` 协议和本地只读状态发现。优先使用正式协议或可发现 schema，不直接写本地 SQLite/JSONL 状态。
4. 发现可桥接协议时，设计最小工具而不是放弃。推荐工具名：`create-visible-thread`。
5. 只有直接工具和桥接方案都暂不可用时，才使用中文命名 role agent/subagent 或 staged fallback，并在主线程说明这是 fallback。

`create-visible-thread` 的最小契约：

```text
Input: thread_name, objective, initial_prompt, cwd?, model?, sandbox?, approval_policy?, parent_thread_id?
Behavior: 通过受支持的 Codex app-server/remote-control 协议创建非 ephemeral thread，设置用户可见名称，投递 initial_prompt，必要时记录 parent/child 关系。
Output: thread_id, session_id, name, open_link 或可打开方式, status, residual_risk
```

当直接 `create_thread` / `codex_app.create_thread` 不可用时，可优先评估的协议路径是 app-server v2：`thread/start` 创建 thread，`thread/name/set` 设置名称，`turn/start` 投递初始 prompt，`thread/list` / `thread/read` 验证可见性。CLI 的 `fork`/`resume` 只能作为特定场景补充；Desktop deeplink 只有在明确 route 可用时才使用；本地数据库只可只读取证。

## 触发失败自救

如果主线程发现自己正在亲自做执行活（例如写文件、跑长命令、读长日志、排障循环、安装配置、处理凭据、提交、推送、生成审查结论或质量评价），立即停下并自检：

1. 说明纠偏：当前工作应由执行载体承担，主线程改回编排。
2. 选择载体：role agent/subagent、用户可见 thread，或 staged fallback。
3. 交接状态：目标、约束、已知证据、允许动作、禁止动作和预期输出。
4. 回收结果：只把结论、证据、变更文件、验证结果、阻塞点和 residual risk 带回主线程。

不要为了“已经开始了”继续在主线程把执行做完。

## 项目状态

项目开始、上下文压缩后或长时间暂停后，维护一份简短状态：

- Objective：什么算成功。
- Constraints：仓库规则、审批要求、用户偏好和非目标。
- Workstreams：实现、调研、验证、文档、发布等活动线索。
- Decision log：关键选择及原因。
- Verification plan：测试、review、截图、build、验收检查。
- Open questions：只保留会改变下一步行动的阻塞问题。

状态是 executive summary，不是 execution diary。

## 委派契约

使用短生命周期、边界清晰的角色：

- `Planner`：澄清范围、拆解任务、识别风险和依赖。
- `Researcher`：调研文档、API、issue 历史或相似实现。
- `Architect`：评估设计方案、架构边界和集成方式。
- `Implementer`：完成明确范围内的代码或文档修改。
- `Tester`：设计并执行验收、回归、边界和负向测试。
- `Reviewer`：检查 diff 中的缺陷、可维护性风险、遗漏测试和行为回归。
- `Release steward`：准备发布说明、迁移步骤、部署检查或交接摘要。

给每个执行载体一个紧凑任务契约：

```text
Role:
Mission:
Inputs: 相关文件、命令、工件或需求
Constraints:
Allowed actions: 只读检查、运行测试、编辑限定文件等
Output: 简洁结论、证据、变更文件、执行命令、风险
```

如果委派代码修改，要指定文件或模块 ownership，并提醒 worker 不要回滚无关改动或其他 Agent 的工作。

## 命名规范

可读的命名让用户一眼看出谁在做什么。工具可能返回系统昵称（如 Kuhn、Kant、Mill），但主线程对用户汇报、状态表和任务记录时，始终使用中文任务名作为执行载体身份。

**Subagent / Role agent（中文命名）：**

格式：`动词-对象`，中文，连字符分隔。从名字就能看出任务内容。

- `测试-导入Bundle` ← 好：做什么（测试）+ 对什么做（导入Bundle）
- `构建-迁移Skill` ← 好：做什么（构建）+ 对什么做（迁移Skill）
- `审查-编排Skill` ← 好：做什么（审查）+ 对什么做（编排Skill）
- `Kuhn` / `Mill` ← 不作为用户可见任务名：系统昵称看不出任务

**用户可见 Codex thread（中文命名）：**

格式：`动词-项目名` 或 `项目名-动词`，中文，连字符分隔。技术上必需的英文关键词（如 Skill 名、工具名）可保留。

- `构建-会话迁移Skill` ← 好
- `验证-Skill架构` ← 好
- `配置-GitHub认证` ← 好

命名不需要版本号或日期后缀，thread 本身就是时间线。

## 验证完整性

避免 self-validation：实现上下文不应成为唯一验证上下文。

当工作涉及大范围代码修改、用户可见行为、发布/推送、迁移、凭据、安全/隐私风险、性能风险、数据丢失风险、模糊验收标准，或用户明确要求审查/专家评价/质量评估/验收/测试策略时，必须进行独立验证。小范围低风险修改可以由主线程验证。

给验证者原始需求、变更文件、命令和可观察工件。除非任务需要，不要泄露实现者解释、怀疑点、预期结论或期望结果。验证者应优先寻找失败，并用证据支撑：文件路径、行号、命令输出、截图或复现步骤。

验证者输出是 evidence，不是 authority。主线程根据原始目标和源工件解决冲突。如果独立验证受阻，明确说明并描述 residual risk。

## 上下文治理

- Agent 能自己检查文件时，传路径和工件，不要粘贴大量上下文。
- 回到主线程的内容只保留结论、证据、变更文件、验证结果、阻塞点和 residual risk。
- 除非决策需要，不把完整 debug logs 或 trial-and-error 历史搬进主线程。
- 当文件、测试或用户新指令推翻旧假设时，更新或删除旧假设。

## 生命周期管理

执行载体不是无限的。每个 agent 和 thread 都有明确的生命终点。

**Subagent：**
- 结果被主线程消费并验收后，**立即关闭**（调用 `close_agent`）。不保留已完成 agent。
- 主线程在每次委派前，检查是否有历史残留 agent 未关闭；如有，先清理再派新任务。
- 如果 agent 超时无响应，关闭它并改用 fallback 方式。

**用户可见 Codex thread：**
- 任务完成、结果已回收后，主线程在汇报中告知用户该 thread 可以归档或关闭。
- 如果 thread 产出临时工件（如测试数据、bundle、clone 的仓库），在汇报中说明路径和清理建议。

**临时产物：**
- 测试用的 clone 仓库、导出 bundle、安装目录等，完成后说明位置和建议清理命令。
- 不要假设 `/tmp` 会自动清理——显式告诉用户哪些可以删。

主线程自身也应定期检查：是否有已完成的 agent 未关闭？是否有 thread 已结束但未告知用户归档？这些是 context hygiene 的一部分。

## 标准流程

1. Intake：复述目标、约束和 definition of done。
2. Plan：根据任务长度、执行密度和工具约束选择执行载体，并用一句话告诉用户原因。
3. Dispatch：给执行载体明确输入、权限、边界和输出契约。
4. Execute：让执行载体承载细节；主线程只做必要协调。
5. Validate：按风险选择独立验证或主线程验证。
6. Integrate：检查 subagent 结果，解决冲突，只采纳有证据支持的修改。
7. Report：总结变更、验证结果、剩余风险和后续建议。

## 汇报

- 先报告最终结论或结果。
- 相关时说明使用了哪些执行载体，以及为什么。
- 包含变更文件、验证结果和未解决风险。
- 除非用户要求，不转发完整 subagent 记录。

## 安装到其他项目

1. 安装本 Skill。
2. 打开目标项目根目录的 `AGENTS.md`。
3. 复制 [references/agents-section.md](references/agents-section.md) 中的 `Multi-Agent Orchestrator Mode` 章节。
4. 之后再使用 `$multi-agent-orchestrator` 开始长期项目。

如果目标项目没有 `AGENTS.md`，先创建它。只安装 Skill 但不更新 `AGENTS.md`，会降低触发成功率和执行一致性。
