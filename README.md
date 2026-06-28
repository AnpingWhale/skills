# AnpingWhale Codex Skills

这是 AnpingWhale 的个人 Codex Skills 仓库，用来公开、同步和安装自建 Skills。

这个仓库不是本机 Codex 工作区快照，也不镜像第三方 Skills。每个自建 Skill 都是一个独立目录，目录名与 Skill 名称一致，并包含自己的 `SKILL.md`。

## 当前包含的 Skills

| Skill | 用途 |
| --- | --- |
| `multi-agent-orchestrator` | 用于复杂或长期 Codex 项目的多 Agent 编排。它让主线程负责目标、边界、决策、整合和最终汇报，并按任务长度和执行密度选择 role agent、subagent 或用户可见 Codex thread。 |

## 安装

如果你的 `skills` CLI 支持从 GitHub 仓库安装，可以直接运行：

```bash
npx skills@latest add AnpingWhale/skills
```

也可以手动安装单个 Skill：

```bash
git clone https://github.com/AnpingWhale/skills.git anpingwhale-codex-skills
mkdir -p ~/.codex/skills
cp -R anpingwhale-codex-skills/multi-agent-orchestrator ~/.codex/skills/
```

更新手动安装的 Skill：

```bash
cd anpingwhale-codex-skills
git pull
cp -R multi-agent-orchestrator ~/.codex/skills/
```

## 使用示例

```text
使用 $multi-agent-orchestrator 管理这个长期项目。主线程负责目标、决策和整合；请按任务长度和执行密度，自主选择 role agent、subagent 或用户可见 Codex thread。
```

## 仓库结构

```text
.
├── README.md
├── AGENTS.md
└── multi-agent-orchestrator/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

目录约定：

- `SKILL.md` 是每个 Skill 的核心文件，包含 YAML frontmatter 和 Codex 使用该 Skill 时需要读取的说明。
- `agents/openai.yaml` 是推荐的 UI metadata，用于展示名称、简介和默认调用提示。
- `scripts/`、`references/`、`assets/` 只在某个 Skill 真正需要可复用脚本、详细参考资料或输出素材时才创建。
- `.agents/`、`skills-lock.json`、`.scratch/` 和 `.DS_Store` 都是本地工作区或工具生成文件，不应提交到这个公开仓库。

## 第三方 Skills

这个仓库不 vendor 第三方 Skills。需要安装 Matt Pocock 的工程 Skills 时，请直接从上游安装：

```bash
npx skills@latest add mattpocock/skills
```

这样可以避免把第三方、deprecated、in-progress 或 personal Skills 混进本仓库的公开发布面。

## 新增 Skill

新增自建 Skill 时，建议遵守以下规则：

- 使用小写 hyphen-case 命名目录，例如 `my-new-skill/`。
- 每个 Skill 目录必须包含 `SKILL.md`。
- `SKILL.md` 的 frontmatter 只保留必要字段，尤其是清楚的 `name` 和 `description`。
- `description` 要说明 Skill 做什么，以及什么时候应该触发。
- Skill 正文只保留核心执行规则；详细但非核心的材料放到 `references/`，并在 `SKILL.md` 中说明何时读取。
- 不要在单个 Skill 目录中放无关 README、安装指南、临时日志或过程记录。

## 维护

`AGENTS.md` 是给 Codex 或其他维护 Agent 看的仓库维护约定，不是安装 Skill 的必要文件。

提交前建议检查：

```bash
ruby -ryaml -e 'skill=ARGV[0]; text=File.read(skill+"/SKILL.md"); m=text.match(/\A---\n(.*?)\n---/m); abort "Invalid frontmatter" unless m; fm=YAML.safe_load(m[1]); abort "Missing name" unless fm["name"].is_a?(String); abort "Missing description" unless fm["description"].is_a?(String); YAML.safe_load(File.read(skill+"/agents/openai.yaml")) if File.exist?(skill+"/agents/openai.yaml"); puts "Skill parses successfully"' multi-agent-orchestrator
```

## License

本仓库暂未声明开源许可证。公开仓库用于同步和安装个人 Skills；如果要允许他人复制、修改或再分发，请先补充明确的 `LICENSE`。
