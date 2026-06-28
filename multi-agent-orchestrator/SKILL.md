---
name: multi-agent-orchestrator
description: "用于复杂或长期 Codex 项目的 multi-agent orchestration：由主线程编排隔离的 workstreams、role agents/subagents 和独立验证。Use when the user asks for 多 Agent 协作, 主线程/子线程编排, main-thread orchestration, delegated workstreams, or a reusable protocol for complex Codex projects."
---

# Multi-Agent Orchestrator 多 Agent 主线程编排

## 目的

使用这个 Skill 时，把复杂 Codex 工作作为 main-thread orchestration 来推进。主线程负责意图、边界、决策、证据整合、验收和最终汇报；执行载体负责命令密集或细节密集的工作，例如调研、实现、测试、review、配置、排障、发布检查、UI 操作、凭据流程和长日志。

目标不是尽量多用 Agent，而是保护判断质量、减少上下文污染，并避免 self-validation。

## 核心规则

- 开始执行前，先说明选择的执行载体和原因：main thread、role agent/subagent、用户可见 Codex thread、staged single-thread fallback，或混合方式。
- 按任务长度和执行密度选择载体：短、窄、一次性任务可以在主线程内派 role agent/subagent；较长、多轮、会产生执行层对话或需要持续上下文的任务，应优先切到用户可见 Codex thread。
- 当任务会产生长日志、反复排障、大量读文件、凭据处理、UI 观察、安装配置、发布推送或多轮实现时，优先把执行细节移出主线程。
- 不要把“用户只能和主线程沟通”当作硬规则。为了保护项目上下文，主线程可以要求用户去子 thread 处理执行层对话。
- 优先遵守更高层约束：system/developer 指令、工具政策、仓库规则、审批要求和用户安全偏好。如果理想载体被限制，说明 fallback。
- 用户可见 Codex thread 是主线程可以自主选择的执行载体。较长、多轮、会产生大量执行层上下文或需要持续状态的任务，主线程可以主动创建或要求切换到 thread，并说明目标、边界和回收方式；不要要求用户逐次明确提出“创建新 thread”才行动。如果更高层工具政策阻止自主创建，则说明限制，并请求授权。
- 需要委派但不确定工具是否可用时，先使用可用的工具发现机制，例如 `tool_search`。如果没有真正可用的 subagent/thread 机制，明确说明，并用分阶段方式模拟隔离：实现、独立检查、整合。
- 中间更新和最终汇报使用用户的语言。
- **agent 结果消费后立刻关闭**：不要让已完成的 subagent 堆积。结果回收、验收完成后，马上调用 `close_agent` 释放资源。

## 执行载体

- Main thread：intake、planning、decision-making、integration、少量只读检查、微小低风险修改，或委派成本高于收益的强顺序任务。
- Role agent / subagent：短、窄、一次性、有边界的调研、实现、测试、review、架构批判、安全/隐私/性能检查、迁移规划，或任何需要独立视角并能返回简洁证据的任务。
- 用户可见 Codex thread：当主线程判断必要且工具政策允许时，用于较长或多轮执行分支、反复用户输入、环境配置、凭据流程、UI 驱动任务、大型 debug loop，或需要在主线程之外保留持久上下文的工作。
- Staged fallback：没有可用委派工具时，显式拆分阶段，避免实现者推理成为唯一验证面。

如果主线程开始堆积执行日志或低层排障细节，应停下来重新选择执行载体。

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

可读的命名让用户一眼看出谁在做什么。禁止使用系统自动生成的昵称（如 Kuhn、Kant、Mill）作为执行载体的身份标识。

**Subagent / Role agent（中文命名）：**

格式：`动词-对象`，中文，连字符分隔。从名字就能看出任务内容。

- `测试-导入Bundle` ← 好：做什么（测试）+ 对什么做（导入Bundle）
- `构建-迁移Skill` ← 好：做什么（构建）+ 对什么做（迁移Skill）
- `审查-编排Skill` ← 好：做什么（审查）+ 对什么做（编排Skill）
- `Kuhn` / `Mill` ← 禁止：系统昵称，完全看不出任务

**用户可见 Codex thread（中文命名）：**

格式：`动词-项目名` 或 `项目名-动词`，中文，连字符分隔。技术上必需的英文关键词（如 Skill 名、工具名）可保留。

- `构建-会话迁移Skill` ← 好
- `验证-Skill架构` ← 好
- `配置-GitHub认证` ← 好

命名不需要版本号或日期后缀，thread 本身就是时间线。

## 验证完整性

避免 self-validation：实现上下文不应成为唯一验证上下文。

当工作涉及大范围代码修改、用户可见行为、发布/推送、迁移、凭据、安全/隐私风险、数据丢失风险或模糊验收标准时，必须进行独立验证。小范围低风险修改可以由主线程验证。

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
