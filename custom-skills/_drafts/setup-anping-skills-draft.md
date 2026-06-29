# Setup-anping-skills-草稿

### 目标

仿照 `setup-matt-pocock-skills` 设计一个技能Setup-anping-skills，作为自己的 Codex 项目启动器，它负责给一个项目选择并配置一套 AI 协作环境。这将是一项由提示驱动的技能，而非确定性脚本。

### 工作流

#### 1. 检查依赖性

检查以下Skill是否安装可用，如不可用则进行安装

| 名称                     | 描述                                       | 来源                                 |
| ------------------------ | ------------------------------------------ | ------------------------------------ |
| grill-me                 | 一场毫不留情的访谈，旨在完善计划或设计。   | https://github.com/mattpocock/skills |
| grilling                 | 就某项计划或设计对用户进行不遗余力的追问。 | https://github.com/mattpocock/skills |
| grill-with-docs          |                                            | https://github.com/mattpocock/skills |
| domain-modeling          | 构建并完善项目的领域模型                   | https://github.com/mattpocock/skills |
| handoff                  |                                            | https://github.com/mattpocock/skills |
| Multi-Agent Orchestrator | 为项目启用主线程编排模式                   | 自建Agent                            |
|                          |                                            |                                      |
|                          |                                            |                                      |

#### 2. 探索项目

查看当前仓库以了解其初始状态，并简短快速地介绍当前仓库情况，不要妄下结论

- `git remote -v` and `.git/config` — is this a GitHub repo? Which one?
- `AGENTS.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` — does this skill's prior output already exist?



#### 3. 对用户进行询问

对用户进行逐一地询问，先展示一个部分，获取用户的回答，再进入下一个，不要一次性把问题都抛给用户。



##### a. 项目目标

使用 `grilling` 技能，询问用户该项目的目标，达成一致后写入ReadMe文档中。



##### b. 编排模式

询问用户是否需要启用主线程编排模式，简单介绍这个模式带来的收益与影响，如用户需要，则使用`Multi-Agent Orchestrator`技能，启用主线程编排模式，如不需要，则进入下个流程。



##### c. 上下文管理

Confirm the layout:

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).



##### d. 知识管理

询问用户是否需要创建知识库（为人类服务）作为项目的知识沉淀



#### 4. 确认和编辑

简短地向用户说明 AGENTS.md 的意义。

如果存在 AGENTS.md ，请用户对其进行编辑，如果不存在，请创建后，然后请用户进行编辑。



### 引用

[1]: https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills	"setup-matt-pocock-skills"