# Repository Agent Guidance

这个仓库用于发布 AnpingWhale 的自建 Codex Skills。维护时优先保持公开仓库干净、可安装、可解释。

## Scope

- 保留自建 Skill 目录，例如 `multi-agent-orchestrator/`。
- 不要提交第三方 vendored Skills，例如 `.agents/skills/`。
- 不要提交本地工具状态，例如 `skills-lock.json`、`.scratch/`、`.DS_Store`。
- 新增 Skill 时，一个 Skill 一个独立目录；目录名应与 `SKILL.md` frontmatter 的 `name` 一致。

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
