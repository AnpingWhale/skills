# Skill Catalog

这个文件是 `setup-anping-skills` 的可扩展 Skill 目录。选择 Skill 时只推荐当前项目真正需要的组合；不要默认全装。

每个可跨设备安装的 Skill 都应写清楚 GitHub repo/path。换设备时，优先使用 `skill-installer` 指定 `repo` + `path` 安装；不要只依赖简称。

## Anping 自建 Skills

| Skill | 安装坐标 | 适用场景 | 默认建议 |
| --- | --- | --- | --- |
| `setup-anping-skills` | `AnpingWhale/skills`, path `custom-skills/setup-anping-skills`<br>https://github.com/AnpingWhale/skills/tree/main/custom-skills/setup-anping-skills | 初始化项目的 AI 协作环境和 Skill 组合 | 项目启动时运行 |
| `multi-agent-orchestrator` | `AnpingWhale/skills`, path `custom-skills/multi-agent-orchestrator`<br>https://github.com/AnpingWhale/skills/tree/main/custom-skills/multi-agent-orchestrator | 长期项目、复杂任务、主线程编排、独立验证、上下文治理 | 长期项目推荐 |
| `transfer-codex-sessions` | `AnpingWhale/skills`, path `custom-skills/transfer-codex-sessions`<br>https://github.com/AnpingWhale/skills/tree/main/custom-skills/transfer-codex-sessions | 多设备迁移、备份/恢复 Codex 会话、查看或导入 session bundles | 按需启用 |

## Matt Pocock Engineering Skills

这些 Skill 来自 `mattpocock/skills`。优先使用 `skill-installer` 从对应 path 安装；安装前可先列出上游可用 Skills，避免路径过期。

| Skill | 安装坐标 | 适用场景 | 默认建议 |
| --- | --- | --- | --- |
| `ask-matt` | `mattpocock/skills`, path `skills/engineering/ask-matt`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt | 作为 Matt engineering skills 的选择路由 | 不确定用哪个 Matt Skill 时推荐 |
| `setup-matt-pocock-skills` | `mattpocock/skills`, path `skills/engineering/setup-matt-pocock-skills`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills | 初始化 issue tracker、triage labels、domain docs | 工程项目推荐 |
| `grill-with-docs` | `mattpocock/skills`, path `skills/engineering/grill-with-docs`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs | 在访谈中同步沉淀 ADR 和 glossary | 复杂领域推荐 |
| `domain-modeling` | `mattpocock/skills`, path `skills/engineering/domain-modeling`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling | 构建 ubiquitous language、领域词汇和模型 | 长期产品推荐 |
| `diagnosing-bugs` | `mattpocock/skills`, path `skills/engineering/diagnosing-bugs`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs | 系统性诊断 hard bugs、性能回归或复杂失败 | 调试项目推荐 |
| `improve-codebase-architecture` | `mattpocock/skills`, path `skills/engineering/improve-codebase-architecture`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture | 扫描代码架构并提出 deep-module 改进机会 | 成熟代码库推荐 |
| `tdd` | `mattpocock/skills`, path `skills/engineering/tdd`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd | test-first 开发或修 bug | 有测试文化时推荐 |
| `to-prd` | `mattpocock/skills`, path `skills/engineering/to-prd`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/to-prd | 把对话整理成 PRD | 需要产品文档时推荐 |
| `to-issues` | `mattpocock/skills`, path `skills/engineering/to-issues`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/to-issues | 把 PRD 或计划拆成 issue | 需要任务拆解时推荐 |
| `triage` | `mattpocock/skills`, path `skills/engineering/triage`<br>https://github.com/mattpocock/skills/tree/main/skills/engineering/triage | issue / PR triage state machine | 有 issue tracker 时推荐 |

## OpenAI / Built-in Skills

这些通常由 Codex 环境预装或插件提供，不应写成第三方 GitHub 安装坐标。换环境时先检查当前会话可用 Skills。

| Skill | 来源 | 适用场景 | 默认建议 |
| --- | --- | --- | --- |
| `skill-installer` | Codex system skill | 从 GitHub 或 curated list 安装 Skills | 安装时使用 |
| `skill-creator` | Codex system skill | 创建或迭代 Skills | 维护本仓库时使用 |
| `openai-docs` | Codex system skill | 查询 OpenAI / Codex 官方文档 | OpenAI 产品问题时使用 |

## 推荐策略

- 新项目：`setup-anping-skills` + 视情况启用 `multi-agent-orchestrator`。
- 长期工程项目：加上 `setup-matt-pocock-skills`、`domain-modeling`；需要选择 Matt Skill 时先用 `ask-matt`。
- 需求不清：优先用 `ask-matt` 选择合适流程；需要边访谈边沉淀文档时用 `grill-with-docs`。
- 架构/质量治理：使用 `improve-codebase-architecture`、`diagnosing-bugs`、`tdd`。
- 多设备 Codex 迁移：使用 `transfer-codex-sessions`。

新增外部 Skill 时，只记录来源、用途、安装建议和风险；不要复制第三方源码。能跨设备安装的 Skill 必须写清 `repo`、`path` 和 GitHub URL；无法确认稳定来源的 Skill 不写入 catalog，也不要把它作为必需依赖。
