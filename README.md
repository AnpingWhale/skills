# Codex Skills 工作区

这个目录用于存放多个 Codex Skill。每个 Skill 都应是一个独立子目录，目录名与 Skill 名称一致，并包含自己的 `SKILL.md`。

当前已有 Skill：

- `multi-agent-orchestrator`：用于长期项目中的主线程编排和多 Agent 协作。
- `.agents/skills/`：通过 `npx skills@latest add mattpocock/skills` 安装的第三方 Skills。

## 推荐目录结构

```text
/Users/admin/Desktop/skills/
├── README.md
├── skills-lock.json
├── multi-agent-orchestrator/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
├── .agents/
│   └── skills/
│       └── third-party-skill-name/
│           └── SKILL.md
└── future-skill-name/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── scripts/
    ├── references/
    └── assets/
```

其中 `scripts/`、`references/`、`assets/` 都是可选目录，只在对应 Skill 真正需要时创建。

## Skill 目录规则

每个 Skill 子目录应尽量保持精简：

- `SKILL.md`：必需。包含 YAML frontmatter 和 Codex 使用该 Skill 时需要读取的核心说明。
- `agents/openai.yaml`：推荐。用于展示名称、简介和默认调用提示。
- `scripts/`：可选。放可复用脚本。
- `references/`：可选。放按需读取的详细参考资料。
- `assets/`：可选。放模板、图片、字体、示例资源等输出素材。

不要在单个 Skill 子目录中放不必要的辅助文档，例如 `README.md`、`INSTALLATION_GUIDE.md`、`QUICK_REFERENCE.md`、`CHANGELOG.md`。这就是之前提到的 Skill Creator 建议：Skill 文件夹本身应该只包含会直接帮助 Codex 执行该 Skill 的必要材料，避免额外文档增加噪音。

根目录的 `README.md` 不属于某个单独 Skill，因此适合用来说明整个 Skills 工作区的结构、索引和维护规则。

## 当前 Skill

### 自建 Skill：multi-agent-orchestrator

路径：

```text
/Users/admin/Desktop/skills/multi-agent-orchestrator
```

用途：

- 让当前会话作为用户唯一沟通的主线程。
- 由主线程按需创建或使用角色 Agent / subagent。
- 将实现、测试、评审、调研等职责拆开。
- 降低长期项目中的上下文堆积和 token 消耗。
- 避免实现者自测自证，提高验收质量。

典型调用：

```text
Use $multi-agent-orchestrator to coordinate this project through a main thread and focused role agents.
```

中文调用：

```text
从现在开始，这个项目采用主线程编排模式。我只和当前主线程对话；请按需使用角色 Agent 或 subagent 完成实现、测试、评审和调研。
```

### 第三方 Skills：.agents/skills

路径：

```text
/Users/admin/Desktop/skills/.agents/skills
```

这些 Skills 由 `skills` CLI 管理，`skills-lock.json` 记录来源、路径和 hash。同步到 GitHub 时建议一起提交 `.agents/skills` 和 `skills-lock.json`，这样其他机器可以看到当前已安装版本；如果只想同步自建 Skills，可以在后续调整 `.gitignore` 排除 `.agents/`。

## 新增 Skill 流程

建议使用 Skill Creator 的初始化脚本创建新 Skill：

```bash
python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/init_skill.py new-skill-name --path /Users/admin/Desktop/skills
```

如果需要预先创建资源目录：

```bash
python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/init_skill.py new-skill-name --path /Users/admin/Desktop/skills --resources scripts,references,assets
```

创建后重点检查：

- Skill 名称是否为小写 hyphen-case。
- `SKILL.md` frontmatter 是否只包含必要字段。
- `description` 是否清楚说明什么时候触发该 Skill。
- `SKILL.md` 正文是否只保留核心执行规则。
- 资源目录是否确实有必要存在。
- `agents/openai.yaml` 是否与 Skill 说明一致。

## 验证

可以使用 Skill Creator 的校验脚本检查某个 Skill：

```bash
python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/admin/Desktop/skills/multi-agent-orchestrator
```

如果当前 Python 环境缺少 `PyYAML`，脚本可能会因为依赖缺失失败；这不一定代表 Skill 内容无效。可以换到具备 `PyYAML` 的环境运行，或使用其他 YAML 解析工具做等价检查。

## 维护原则

- 根目录 README 负责维护整个 Skills 工作区的索引和规则。
- 单个 Skill 的执行说明写在对应的 `SKILL.md` 中。
- 详细但非核心的资料放进该 Skill 的 `references/`，并在 `SKILL.md` 中说明何时读取。
- 可重复执行的确定性操作优先沉淀为 `scripts/`。
- 不要把临时日志、项目过程记录或泛用说明塞进 Skill 子目录。
