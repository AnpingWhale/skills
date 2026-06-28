---
name: transfer-codex-sessions
description: "在多台设备之间导出、传输和导入 Codex 会话（sessions），基于 ai-cli-kit 的 aik codex 子命令。Use when the user asks to transfer Codex sessions between devices, 换机迁移、备份/恢复 Codex 会话、导出/import sessions、validate/list session bundles、让桌面端会话可见、clone/watch provider sessions, repair desktop sessions, clean archived/cloned sessions, or manage session bundles."
---

# Transfer Codex Sessions 会话迁移

## 目的

这个 Skill 通过上游工具 `ai-cli-kit`（命令入口 `aik`）操作 Codex 会话，覆盖三大能力：

- **会话迁移**：设备间的 export / import / validate
- **供应商克隆**：`clone-provider`、`watch-provider`（切换 AI 供应商时自动复制历史会话）
- **维护清理**：`repair-desktop`、`clean-archived`、`clean-clones`、`dedupe-clones`

核心原则：优先使用只读命令探查状态；在私有目录处理 bundle，不把 `codex_sessions/` 放进公开仓库；`import` / `import-desktop-all` 不支持 dry-run，导入前必须先 `validate-bundles`、`list-bundles`、冲突分析并获得用户确认；支持 dry-run 的清理、修复和克隆命令先预览再执行。

## 前置条件

首次使用前，先只读检查是否已有可用命令：

```bash
command -v aik
aik --version
```

如果没有安装，再征得用户确认后克隆并安装上游工具：

```bash
git clone https://github.com/goodnightzsj/codex-session-cloner.git
cd codex-session-cloner
chmod +x install.sh
./install.sh
```

安装会访问网络并写入本机工具目录；如果当前环境需要权限审批，先请求审批，不要静默安装。安装后，`aik` 命令注册在安装目录的 venv/bin 下。也可直接在项目目录内用 `./aik` 零污染运行：

```bash
cd codex-session-cloner && ./aik --version
aik --version
```

## 会话迁移流程

### 1. 源设备：查看与导出

```bash
# 查看所有本地会话
aik codex list [pattern] --limit 30

# 导出单个会话
aik codex export <session_id>

# 导出全部桌面端会话
aik codex export-desktop-all [--dry-run]

# 仅导出活跃桌面端会话
aik codex export-active-desktop-all [--dry-run]

# 导出全部 CLI 会话
aik codex export-cli-all [--dry-run]
```

导出产物放在当前目录 `./codex_sessions/` 下，按会话 ID 组织为独立 bundle 目录。执行导出前先确认当前目录是私有工作目录；如果当前目录在 Git 仓库、公开同步目录或共享目录内，先切到安全位置再导出。

### 2. 传输 bundle

将 `codex_sessions/` 目录传输到目标设备（U 盘、AirDrop、rsync、压缩包等）。如果只迁移部分会话，只传对应 bundle 子目录。

### 3. 目标设备：验证与导入

```bash
# 列出所有 bundle
aik codex list-bundles [pattern] --limit 30 [--source all|bundle|desktop]

# 验证 bundle 完整性
aik codex validate-bundles [pattern] [--source all|bundle|desktop] [--verbose]

# 导入命令不支持 --dry-run；先完成只读预检、冲突分析并获得用户确认

# 导入单个会话
aik codex import <session_id|bundle_dir> [--desktop-visible] [--machine MACHINE] [--export-group GROUP]

# 批量导入全部桌面端 bundle
aik codex import-desktop-all [--desktop-visible] [--machine MACHINE] [--export-group GROUP] [--latest-only]
```

导入前不要给 `import` 或 `import-desktop-all` 添加 `--dry-run`。应先用 `list-bundles` 和 `validate-bundles` 确认候选 bundle，再检查目标设备是否已有同 ID 会话、说明将导入哪些 bundle、哪些会因冲突跳过，获得用户确认后再执行。导入时已存在会话默认跳过，不覆盖。

### 4. 验证导入结果

导入后在目标设备上打开 Codex，确认会话列表中包含已导入的会话，且可正常打开和继续对话。

## 供应商克隆（Provider Cloning）

当用户切换 AI 供应商（如从 OpenAI 迁移到其他 provider）时，原有会话可能在新供应商下不可见。`clone-provider` 会将活跃会话复制为当前供应商可读的副本。

```bash
# 预览克隆（dry-run）
aik codex clone-provider --dry-run

# 执行克隆
aik codex clone-provider [target_provider]

# 持续监听供应商变化并自动克隆
aik codex watch-provider [--interval SECONDS] [--dry-run] [--no-initial-sync] [--once]
```

`watch-provider` 适用于长期保持多供应商同步的场景。`--once` 只检查一次后退出。

## 维护清理

```bash
# 修复桌面端侧边栏可见性/索引/供应商
aik codex repair-desktop [target_provider] [--dry-run] [--include-cli]

# 清理已归档会话（需 --yes 确认）
aik codex clean-archived [--dry-run] [--yes]

# 删除遗留的未标记克隆文件
aik codex clean-clones [target_provider] [--dry-run]

# 去重：当原始会话仍存在时删除克隆副本
aik codex dedupe-clones [target_provider] [--dry-run]
```

破坏性命令（`clean-archived`、`clean-clones`、`dedupe-clones`）默认不为用户自动执行。先解释影响范围，获得用户明确确认后再运行。不确定时用 `--dry-run` 预览。

## 安全边界

- **bundle 含敏感信息**：导出 bundle 包含完整对话历史、文件引用、凭据上下文等。不得上传到公开仓库、共享网盘或不安全通道。
- **导出目录要私有**：`aik codex export*` 默认写入当前目录下的 `codex_sessions/`。不要在公开 Git 仓库、桌面同步目录或共享目录中导出；如果误生成，先从工作区移走并确认未被提交。
- **传输加密**：跨网络传输时使用加密通道（rsync over SSH、加密压缩包等）。
- **用后清理**：传输完成后在传输介质上删除 bundle。
- **导入命令无 dry-run**：`import`、`import-desktop-all` 会写入会话存储，但不支持 `--dry-run`。必须先做 `validate-bundles`、`list-bundles`、冲突分析和用户确认。
- **支持 dry-run 的命令先预览**：`repair-desktop`、`clean-archived`、`clean-clones`、`dedupe-clones`、`clone-provider`、`watch-provider` 等在执行前先用 `--dry-run` 预览并获得用户确认。
- **只读探查先行**：不确定结果时，先用 `list`、`list-bundles`、`validate-bundles` 等只读命令探查状态，不要假设某个写入命令一定支持 `--dry-run`。

## 参考

详细的命令清单、参数说明和安全分类见 [references/commands.md](references/commands.md)。当用户需要了解特定命令的参数、行为细节或破坏性命令的影响范围时，读取该文件。
