# AnpingWhale Codex Skills

这是 AnpingWhale 的个人 Codex Skills 仓库，用来公开、同步和安装自建 Skills。

这个仓库不是本机 Codex 工作区快照，也不镜像第三方 Skills。每个自建 Skill 都是一个独立目录，目录名与 Skill 名称一致，并包含自己的 `SKILL.md`。

## 当前包含的 Skills

| Skill | 用途 |
| --- | --- |
| `multi-agent-orchestrator` | 用于复杂或长期 Codex 项目的多 Agent 编排。Skill 提供触发入口、说明和 AGENTS.md 模板；核心行为通过目标项目 `AGENTS.md` 中的主线程编排规则实现。 |
| `transfer-codex-sessions` | 在多台设备之间导出、传输和导入 Codex 会话（sessions），基于 ai-cli-kit 的 aik codex 子命令。适用于换机迁移、会话备份和设备间同步。 |

## 安装

如果你的 `skills` CLI 支持从 GitHub 仓库安装，可以直接运行：

```bash
npx skills@latest add AnpingWhale/skills
```

也可以手动安装需要的 Skill：

```bash
git clone https://github.com/AnpingWhale/skills.git anpingwhale-codex-skills
mkdir -p ~/.codex/skills
cp -R anpingwhale-codex-skills/multi-agent-orchestrator ~/.codex/skills/
cp -R anpingwhale-codex-skills/transfer-codex-sessions ~/.codex/skills/
```

更新手动安装的 Skill：

```bash
cd anpingwhale-codex-skills
git pull
cp -R multi-agent-orchestrator ~/.codex/skills/
cp -R transfer-codex-sessions ~/.codex/skills/
```

## 使用示例

```text
使用 $multi-agent-orchestrator 管理这个长期项目。主线程负责目标、决策和整合；请按任务长度和执行密度，自主选择 role agent、subagent 或用户可见 Codex thread。

使用 $transfer-codex-sessions 把 Codex 会话迁移到新设备。先 list / validate bundle，导入前做冲突分析并确认；导出的 codex_sessions 目录只放在私有传输位置。
```

长期项目建议同时把 `multi-agent-orchestrator/references/agents-section.md` 复制到目标项目的 `AGENTS.md`。只安装 Skill 但不配置 `AGENTS.md`，会降低触发成功率和执行一致性。

## 仓库结构

```text
.
├── README.md
├── AGENTS.md
├── multi-agent-orchestrator/
│   ├── SKILL.md
│   ├── references/
│   │   └── agents-section.md
│   └── agents/
│       └── openai.yaml
└── transfer-codex-sessions/
    ├── SKILL.md
    ├── references/
    │   └── commands.md
    └── agents/
        └── openai.yaml
```

目录约定：

- `SKILL.md` 是每个 Skill 的入口文件，包含 YAML frontmatter 和 Codex 使用该 Skill 时需要读取的说明。
- `multi-agent-orchestrator` 的运行时核心规则放在项目 `AGENTS.md`；`references/agents-section.md` 是复制到其他项目的模板。
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
- Skill 正文只保留入口说明和必要规则；详细材料、AGENTS 模板或命令参考放到 `references/`，并在 `SKILL.md` 中说明何时读取。
- 不要在单个 Skill 目录中放无关 README、安装指南、临时日志或过程记录。

## 维护

本仓库的 `AGENTS.md` 同时承担仓库维护约定和当前项目的 `multi-agent-orchestrator` 行为规则。把该 Skill 用到其他项目时，需要把 `multi-agent-orchestrator/references/agents-section.md` 复制进目标项目的 `AGENTS.md`。

提交前建议检查：

```bash
ruby -ryaml -e 'ARGV.each do |skill| text=File.read(skill+"/SKILL.md"); m=text.match(/\A---\n(.*?)\n---/m); abort "#{skill}: invalid frontmatter" unless m; fm=YAML.safe_load(m[1]); abort "#{skill}: missing name" unless fm["name"].is_a?(String); abort "#{skill}: missing description" unless fm["description"].is_a?(String); YAML.safe_load(File.read(skill+"/agents/openai.yaml")) if File.exist?(skill+"/agents/openai.yaml"); puts "#{skill}: ok"; end' multi-agent-orchestrator transfer-codex-sessions
```

## License

本仓库暂未声明开源许可证。公开仓库用于同步和安装个人 Skills；如果要允许他人复制、修改或再分发，请先补充明确的 `LICENSE`。
