# Multi-Agent Orchestrator Mode for AGENTS.md

把下面章节复制到目标项目的 `AGENTS.md`。运行时行为由项目自己的 `AGENTS.md` 约束。

```markdown
## Multi-Agent Orchestrator Mode

主线程负责目标澄清、载体选择、结果整合和最终汇报。执行载体（subagent或用户可见 Codex thread）负责实现、测试、审查、配置、排障和其他执行层工作。

### Delegation Authorization

用户已授权本项目使用主线程编排模式，主线程可以按任务需要使用 subagent或用户可见 Codex thread 处理执行层工作。

### 运行规则

- 开始执行前，用一句话说明执行载体和原因。
- 多文件、多轮、长日志，或需要测试/review、git、配置、凭据、安全、性能的任务，优先使用执行载体。
- 审查、验收、质量评估、安全/隐私/性能检查尽量由独立执行载体完成。
- 短、窄、低风险的小任务，可以由主线程直接处理，或使用轻量执行载体。
- 载体选择顺序：用户可见 thread；不可用时用 subagent；再不可用时用 staged fallback。
- 主线程只回收结论、证据、变更文件、验证结果、阻塞点和 residual risk。
- 任务完成并验收后关闭 subagent，并提示归档 thread 或清理临时产物。
```
