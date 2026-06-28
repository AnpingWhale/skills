# Repository Agent Guidance

这个仓库用于发布 AnpingWhale 的自建 Codex Skills。维护时优先保持公开仓库干净、可安装、可解释。

## Scope

- 保留自建 Skill 目录，例如 `multi-agent-orchestrator/`。
- 不要提交第三方 vendored Skills，例如 `.agents/skills/`。
- 不要提交本地工具状态，例如 `skills-lock.json`、`.scratch/`、`.DS_Store`。
- 新增 Skill 时，一个 Skill 一个独立目录；目录名应与 `SKILL.md` frontmatter 的 `name` 一致。

## Multi-Agent Orchestrator Mode

本仓库启用主线程编排模式。`multi-agent-orchestrator` Skill 主要提供说明、模板和辅助材料；真正约束当前项目内 AI 行为的是本节 AGENTS.md 规则。

### 任务类型判断

开始执行前，先用一句话说明执行载体和原因。

| 任务类型 | 默认载体 |
| --- | --- |
| 目标澄清、边界确认、决策整合、最终汇报 | 主线程 |
| 审查、专家评价、质量评估、验收、测试策略、安全/隐私/性能评估 | 独立 subagent 或用户可见 thread |
| 修改文件、提交 git、推送 GitHub、安装配置、凭据流程、长命令、长日志、反复排障 | 用户可见 thread；不可用时用中文命名 subagent；再不可用才 staged fallback |
| 短、窄、一次性、低风险检查 | 主线程或中文命名 subagent |

主线程可以做少量事实核对，但不承担主要 review / audit 结论，不把执行日志搬进主线程。

### 子代理与 Thread

- Subagent 适合短、窄、一次性任务。命名使用中文 `动词-对象`，例如 `审查-编排Skill`、`测试-导入Bundle`。
- 用户可见 Codex thread 适合较长、多轮、会产生执行层上下文的任务。命名使用中文 `动词-项目名`，例如 `整改-编排Skill质量`、`配置-GitHub认证`。
- 如果工具已暴露 `create_thread` 或 `codex_app.create_thread`，优先直接创建用户可见 thread；配合 `list_threads`、`read_thread`、`send_message_to_thread`、`set_thread_archived` 等工具完成投递、验证、回收和归档提醒。
- 如果工具没有直接暴露 create thread，不把“没有接口”当最终答案；先用 `tool_search` 等可用发现机制自检，再评估 Codex CLI、Codex Desktop deeplink、MCP/插件、`codex_app`、app-server/remote-control 协议或本地只读状态发现是否能补齐 `create-visible-thread` 工具。
- 如果直接工具和可补齐桥接都不可用，明确说这是 fallback，再用中文命名 subagent 或 staged single-thread fallback。

### 状态处理

执行载体回报时使用以下状态之一：

- `DONE`：任务完成，可进入主线程整合。
- `DONE_WITH_CONCERNS`：完成但有疑虑，主线程读取证据后决定是否返工。
- `NEEDS_CONTEXT`：缺少信息，主线程补充上下文后重新派发。
- `BLOCKED`：无法继续，主线程判断是否换载体、降级 fallback 或请求用户输入。

主线程只回收结论、证据、变更文件、验证结果、阻塞点和 residual risk。

### 打断与监控

- 如果用户说“停”“打断”“先别做”“换方向”，主线程立即停止当前执行载体或发送 interrupt，并回收当前状态。
- 如果 subagent 超时或无有效进展，主线程关闭它，记录原因，并换更窄任务或 fallback。
- subagent 结果被消费并验收后，立即调用 `close_agent`；不要保留 completed agent。
- 用户可见 thread 完成后，主线程提示用户可以归档，并说明临时产物路径和清理建议。

### 触发失败自救

如果主线程发现自己正在亲自做执行活，例如写文件、跑长命令、读长日志、安装配置、提交、推送、生成审查结论或质量评价，应立即停下：

1. 说明纠偏：当前工作应由执行载体承担。
2. 选择载体：用户可见 thread、中文命名 subagent，或 staged fallback。
3. 交接状态：目标、约束、已知证据、允许动作、禁止动作和预期输出。
4. 回收结果：只带回 executive summary。

## Skill Layout

每个 Skill 目录默认只需要：

```text
skill-name/
├── SKILL.md
└── agents/
    └── openai.yaml
```

只有在确实需要时才添加：

- `scripts/`：可复用脚本。
- `references/`：按需读取的详细参考资料。
- `assets/`：输出素材、模板或静态资源。

不要在单个 Skill 目录里放安装指南、临时日志、过程记录或泛用 README。

## Maintenance Checklist

- 更新 `README.md`，让公开读者知道新增或移除的 Skill 是做什么的。
- 校验 `SKILL.md` frontmatter 和 `agents/openai.yaml` 都能被 YAML 解析。
- 如果当前机器也安装了该 Skill，同步更新 `~/.codex/skills/<skill-name>/`。
- 不要在普通聊天、subagent 输出或提交内容中暴露 token、secret 或本机私有路径。
- 长任务按 `multi-agent-orchestrator` 的规则选择执行载体；主线程只保留决策、摘要和最终结论。
