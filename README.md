# AnpingWhale Codex Skills

这是 AnpingWhale 的个人 Codex Skills 仓库，用来公开、同步和安装自建 Skills，同时记录值得参考的外部 Skill 生态。

这个仓库不是本机 Codex 工作区快照，也不镜像第三方 Skills。正式发布和维护的自建 Skill 放在 `custom-skills/`；外部优秀 Skill 的目录、推荐和接入策略放在 `referenced-skills/`，只做引用，不 vendor 源码。

## 仓库结构

```text
.
├── README.md
├── AGENTS.md
├── custom-skills/
│   ├── multi-agent-orchestrator/
│   ├── setup-project-for-me/
│   └── transfer-codex-sessions/
└── referenced-skills/
    ├── skill-catalog.md
    ├── matt-pocock.md
    └── openai-curated.md
```

目录约定：

- `custom-skills/`：本仓库实际维护、可发布、可安装的自建 Skills。每个正式 Skill 一个独立目录，目录名与 `SKILL.md` frontmatter 的 `name` 一致。
- `custom-skills/_drafts/`：尚未达到发布标准的构想或草稿。这里的内容不是正式 Skill，不应被安装命令自动复制。
- `referenced-skills/`：外部 Skill 的索引、评价、安装建议和接入策略。这里不提交第三方源码。
- `.agents/`、`skills-lock.json`、`.scratch/` 和 `.DS_Store` 都是本地工作区或工具生成文件，不应提交到公开仓库。

## 自建 Skills

| Skill | 用途 |
| --- | --- |
| `multi-agent-orchestrator` | 用于复杂或长期 Codex 项目的多 Agent 编排。Skill 提供触发入口、说明和 AGENTS.md 模板；核心行为通过目标项目 `AGENTS.md` 中的主线程编排规则实现。 |
| `setup-project-for-me` | 为非技术项目 owner 初始化长期 AI 协作项目记忆结构，生成 owner-first README、AGENTS.md、inputs、deliverables、docs/work、handoffs 和 `.agents/briefs`。 |
| `transfer-codex-sessions` | 在多台设备之间导出、传输和导入 Codex 会话（sessions），基于 ai-cli-kit 的 aik codex 子命令。适用于换机迁移、会话备份和设备间同步。 |

## 安装

正式 Skill 位于 `custom-skills/<skill-name>/`。安装时应指定具体 Skill 路径，或手动复制对应目录；不要假设仓库根目录一定会自动发现嵌套的 Skills。

在 Codex 中，可以使用 `skill-installer` 指定仓库中的具体 Skill path 安装，例如 `custom-skills/setup-project-for-me`、`custom-skills/multi-agent-orchestrator` 或 `custom-skills/transfer-codex-sessions`。

手动安装方式如下：

```bash
git clone https://github.com/AnpingWhale/skills.git anpingwhale-codex-skills
mkdir -p ~/.codex/skills
cp -R anpingwhale-codex-skills/custom-skills/multi-agent-orchestrator ~/.codex/skills/
cp -R anpingwhale-codex-skills/custom-skills/setup-project-for-me ~/.codex/skills/
cp -R anpingwhale-codex-skills/custom-skills/transfer-codex-sessions ~/.codex/skills/
```

如果某个 `skills` CLI 版本明确支持仓库根目录递归发现，也可以尝试 root 安装；但这取决于 installer 兼容性，失败时请改用指定 path 或手动复制。

更新手动安装的 Skill：

```bash
cd anpingwhale-codex-skills
git pull
cp -R custom-skills/multi-agent-orchestrator ~/.codex/skills/
cp -R custom-skills/setup-project-for-me ~/.codex/skills/
cp -R custom-skills/transfer-codex-sessions ~/.codex/skills/
```

长期项目建议同时把 `custom-skills/multi-agent-orchestrator/references/agents-section.md` 复制到目标项目的 `AGENTS.md`。只安装 Skill 但不配置 `AGENTS.md`，会降低触发成功率和执行一致性。

## 引用外部 Skills

`referenced-skills/` 用来记录外部 Skill 来源、适用场景和接入方式。例如：

- Matt Pocock 的工程 Skills：见 `referenced-skills/matt-pocock.md`。
- OpenAI curated / bundled Skills：见 `referenced-skills/openai-curated.md`。
- 统一索引和选择建议：见 `referenced-skills/skill-catalog.md`。

需要安装外部 Skills 时，请从上游来源安装，避免把第三方、deprecated、in-progress 或 personal Skills 混进本仓库的公开发布面。

## 新增自建 Skill

新增自建 Skill 时，建议遵守以下规则：

- 在 `custom-skills/` 下使用小写 hyphen-case 命名目录，例如 `custom-skills/my-new-skill/`。
- 每个正式 Skill 目录必须包含 `SKILL.md`。
- `SKILL.md` 的 frontmatter 只保留必要字段，尤其是清楚的 `name` 和 `description`。
- `description` 要说明 Skill 做什么，以及什么时候应该触发。
- Skill 正文只保留入口说明和必要规则；详细材料、AGENTS 模板或命令参考放到 `references/`，并在 `SKILL.md` 中说明何时读取。
- 不要在单个 Skill 目录中放无关 README、安装指南、临时日志或过程记录。
- 草稿先放到 `custom-skills/_drafts/`，等 `SKILL.md`、`agents/openai.yaml` 和 README 说明完整后再发布。

## 维护

本仓库的 `AGENTS.md` 同时承担仓库维护约定和当前项目的 `multi-agent-orchestrator` 行为规则。把该 Skill 用到其他项目时，需要把 `custom-skills/multi-agent-orchestrator/references/agents-section.md` 复制进目标项目的 `AGENTS.md`。

提交前建议检查：

```bash
ruby -ryaml -e 'Dir.glob("custom-skills/*/SKILL.md").sort.each do |path| skill=File.dirname(path); text=File.read(path); m=text.match(/\A---\n(.*?)\n---/m); abort "#{skill}: invalid frontmatter" unless m; fm=YAML.safe_load(m[1]); abort "#{skill}: missing name" unless fm["name"].is_a?(String); abort "#{skill}: missing description" unless fm["description"].is_a?(String); yaml=File.join(skill,"agents/openai.yaml"); YAML.safe_load(File.read(yaml)) if File.exist?(yaml); puts "#{skill}: ok"; end'
```

## License

本仓库暂未声明开源许可证。公开仓库用于同步和安装个人 Skills；如果要允许他人复制、修改或再分发，请先补充明确的 `LICENSE`。
