# Matt Pocock Skills

Matt Pocock 的工程 Skills 适合作为项目维护、架构、TDD、triage、PRD 和 issue 拆解流程的参考来源。

## 建议接入方式

从上游安装，而不是复制到本仓库：

```bash
npx skills@latest add mattpocock/skills
```

## 本仓库采用策略

- 本仓库可以学习其任务拆解、skill layout 和工程流程设计。
- 不提交 `.agents/skills/` 或任何从上游安装下来的 vendored Skill 内容。
- 如果需要把某个流程改造成 AnpingWhale 自建 Skill，应在 `custom-skills/` 新建独立 Skill，并在 README 中说明它是自建适配，不是上游镜像。
