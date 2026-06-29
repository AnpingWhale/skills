---
name: multi-agent-orchestrator
description: "主线程编排：为长期或复杂 Codex 项目安装并使用多 Agent 编排规则。Use when the user asks for 主线程编排、多 Agent 协作、执行隔离、独立验收, or when another skill needs the AGENTS.md template."
---

# Multi-Agent-Orchestrator

| field | value |
| --- | --- |
| name | `multi-agent-orchestrator` |
| description | 主线程编排：为长期或复杂 Codex 项目安装并使用多 Agent 编排规则。 |

为项目启用主线程编排模式。

## 实现方式

该 Skill 提供说明和模板，通过 prompt 驱动的方式引导 AI 在项目中落地 `AGENTS.md` 规则。主线程编排的核心逻辑写在项目根目录的 `AGENTS.md` 中。

`AGENTS.md` 面向 AI 智能体，可统一不同工具的上下文认知、行为边界和项目级授权。可复制的 `AGENTS.md` block 见 [references/agents-section.md](references/agents-section.md)。

## 功能目的

使用主线程编排模式时，Main thread 负责目标澄清、载体选择、结果整合和最终汇报；执行载体负责调研、实现、测试、review、配置、安装、排障和长执行。

目的不是增加 Agent 数量，而是做复杂度隔离、独立验证和上下文治理。

## 角色定义

- `Main thread`：与用户对话的主线程，不承担主要 review / audit 结论、写文件、长执行、提交、推送、安装配置或凭据流程。
- `subagent`：短、窄、一次性、有边界的调研、实现、测试、review、架构批判、质量评估、安全 / 隐私 / 性能检查或迁移规划任务。
- `Codex thread`：较长、多轮、需要持续状态的执行分支，例如环境配置、凭据流程、提交 / 推送、UI 驱动任务和大型 debug loop。
- `staged fallback`：没有可用委派工具，或授权受阻时，按阶段隔离实现、验证和整合。

## 项目授权

如果项目启用主线程编排，需将授权写入 `AGENTS.md`。授权内容应允许主线程按需要开启新线程或委派 `subagent`。
