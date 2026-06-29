# Referenced Skill Catalog

这个目录记录值得关注的外部 Skill 来源和接入策略。它不是 third-party Skill mirror，也不保存外部源码。

## 分类

| 来源 | 文档 | 采用方式 |
| --- | --- | --- |
| Matt Pocock engineering skills | `matt-pocock.md` | 从上游安装，按项目需要选择启用。 |
| OpenAI curated / bundled skills | `openai-curated.md` | 优先使用 Codex / ChatGPT / 插件运行环境内置版本。 |

## 维护规则

- 只记录来源、用途、安装建议、风险和本仓库是否需要互操作说明。
- 不复制外部 `SKILL.md`、脚本、模板或资产。
- 外部 Skill 如需本仓库适配，适配代码应放在本仓库的自建 Skill 中，并清楚说明边界。
- 如果某个外部 Skill 已 deprecated、experimental 或 personal-only，在推荐中明确标注。
