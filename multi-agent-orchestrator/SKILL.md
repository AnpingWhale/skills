---
name: multi-agent-orchestrator
description: "Coordinate long-running Codex projects through a main-thread orchestration model with focused role agents or subagents. Use when the user wants multi-agent collaboration, main-thread/subagent project management, 主线程/子线程编排, 多 Agent 协作, independent implementation and QA separation, context-window and token hygiene, or a reusable operating protocol for complex Codex projects."
---

# Multi-Agent Orchestrator 多 Agent 主线程编排

## 概览

使用这个 Skill 时，保持当前对话作为唯一面向用户的主线程（main thread），由主线程按需派发聚焦任务给角色 Agent（role agents）或子 Agent（subagents）。主线程负责理解意图、决策、整合、冲突处理和最终汇报；被派发的 Agent 负责独立调研、实现、测试、评审或发布检查。

## 运行模式

- 保持用户只和主线程沟通。不要要求用户切换到其他线程来协调常规子任务。
- 优先使用 subagent 或 multi-agent 工具处理需要独立性、并行性或上下文隔离的任务。
- 只有在用户明确要求创建新的、用户可见的 Codex thread 时，才创建持久线程。
- 如果当前上下文没有可见的 multi-agent 工具，先使用可用的工具发现机制，例如 `tool_search`，再决定是否退回单线程工作。
- 如果没有真正可用的 subagent 机制，说明限制，并在可行时用清晰分离的阶段来模拟实现、验证和评审的隔离。
- 使用用户的语言进行中间更新和最终汇报。
- 保持主线程有决策权：主线程派发任务、权衡证据、解决冲突、执行或批准修改，并输出最终结论。
- 在初始 intake 或 tool discovery 之后，开始任何任务工作前，简要告诉用户是否会使用 role agents / subagents，以及原因。如果主线程直接完成，也要说明原因，例如范围小、风险低、强顺序依赖或委派成本过高。

## 启动或恢复项目

长期项目开始时，或在上下文压缩、长时间暂停之后恢复时，建立一份简短项目状态：

- 目标（Objective）：用户真正想完成什么，什么算成功。
- 约束（Constraints）：仓库规则、风格偏好、时间限制、审批要求和非目标。
- 工作流（Workstreams）：实现、调研、验证、文档、发布等当前活动线索。
- 决策记录（Decision log）：已经做出的关键选择及原因。
- 验证计划（Verification plan）：测试、评审、截图、构建检查或验收标准。
- 未决问题（Open questions）：只保留真正阻塞推进的问题。

在重要节点更新这份状态。保持简短；它用于防止上下文漂移，不应变成冗长日志。

## 何时委派

当独立性、并行性或上下文隔离能明显提高质量时，委派给角色 Agent：

- 实现完成后的独立 QA、测试或 review。
- 大改动前的架构评审或备选方案探索。
- 需要阅读大量文件的代码库侦察，同时主线程保留项目状态。
- 外部资料、文档、API、历史 issue 或相似实现的调研。
- 安全、隐私、性能或可访问性检查。
- 发布准备、迁移说明、交接材料或验收清单。

当任务很小、强顺序依赖明显，或委派成本高于收益时，可以由主线程直接完成。

在初始 intake 或 tool discovery 之后继续行动前，必须让委派决策可见。说明可以只有一句话，但必须包含选择的路径：委派给具名角色 Agent、主线程直接完成，或采用混合方式。

## 角色模式

使用短生命周期、职责清晰的 role agents。常见角色：

- `Planner`：澄清范围、拆解任务、识别风险和依赖。
- `Researcher`：调研文档、API、issue 历史或相似实现。
- `Architect`：评估设计方案、架构边界和集成方式。
- `Implementer`：完成明确范围内的代码或文档修改。
- `Tester`：设计并执行验收、回归、边界和负向测试。
- `Reviewer`：检查 diff 中的缺陷、可维护性风险、遗漏测试和行为回归。
- `Release steward`：准备发布说明、迁移步骤、部署检查或交接摘要。

给每个被委派的 Agent 一个紧凑任务契约：

```text
Role:
Mission:
Inputs: 相关文件、命令、工件或需求
Constraints:
Allowed actions: 只读检查、运行测试、编辑限定文件等
Output: 简洁结论、证据、变更文件、执行命令、风险
```

## 验证完整性

防止 self-validation，也就是实现者自测自证：

- 不要把同一个实现上下文作为唯一验证者。
- 给 QA、Tester 或 Reviewer 的输入应尽量是原始需求、变更文件、命令和可观察工件。
- 除非任务明确需要，否则不要泄露实现者的解释、怀疑点、期望结论或预期答案。
- 要求验证者优先寻找失败，并用证据支撑结论：文件路径、行号、命令输出、截图或可复现步骤。
- 把验证者输出当作证据，而不是最终权威。主线程必须检查关键主张后再采纳或驳回。
- 如果多个 Reviewer 结论冲突，主线程根据原始目标和证据解决冲突。
- 对高风险工作，至少进行一次独立验证。

## Context Hygiene 上下文治理

- 只向 subagents 传递任务局部上下文：目标、相关路径、约束和期望输出。
- 如果 Agent 能自己检查文件，优先传文件路径和工件，不要粘贴大量上下文。
- 将 subagent 结果汇总回主线程。除非决策需要，不要粘贴完整日志。
- 长期项目中保持简短的 decision log 和 current-state summary。
- 当文件、测试或用户新指令推翻旧假设时，删除或更新旧假设。
- 上下文压缩或长时间暂停后，先从源文件和最近用户指令重建当前状态，再继续推进。

## 标准流程

1. Intake：复述目标、约束和 definition of done。
2. Plan：判断是否需要委派、需要哪些角色，并告诉用户为什么会或不会使用 Agent。
3. Dispatch：发送范围清晰的任务，说明输入、权限和输出契约。
4. Execute：实现或协调修改，同时遵守用户约束。
5. Validate：运行测试，并对有意义的工作使用独立 QA / review。
6. Integrate：检查 subagent 结果，解决冲突，只采纳有证据支持的修改。
7. Report：总结变更、验证结果、剩余风险和后续建议。

## 汇报规则

主线程汇报应简洁、整合后再输出：

- 相关时说明使用了哪些角色，以及每个角色的目的。
- 先报告最终结论或结果。
- 包含变更文件、执行命令、验证结果和未解决风险。
- 如果无法进行独立 subagent 验证，要明确说明。
- 不要转发完整 subagent 记录，除非用户要求。
