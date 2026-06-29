# OpenAI Curated And Bundled Skills

OpenAI curated / bundled Skills 通常由 Codex、ChatGPT、插件或运行环境直接提供。它们适合作为能力入口，例如 GitHub、文档、表格、演示、PDF、浏览器控制和 OpenAI API 文档工作流。

## 建议接入方式

- 优先使用当前 Codex 运行环境暴露的内置 Skill 或插件能力。
- 需要最新 OpenAI 产品/API 文档时，按运行环境中的 OpenAI docs 工作流读取官方文档。
- 不把 OpenAI curated / bundled Skill 源码复制到本仓库。

## 本仓库采用策略

- `custom-skills/` 只放 AnpingWhale 自建 Skills。
- 对 OpenAI curated / bundled Skills 的引用只记录在 `referenced-skills/`。
- 如果自建 Skill 依赖某个内置能力，应在该 Skill 的 `SKILL.md` 中说明触发条件和 fallback，而不是 vendor 依赖源码。
