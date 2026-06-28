---
name: transfer-codex-sessions
description: "在多台设备之间导出、传输和导入 Codex 会话（sessions），基于 ai-cli-kit 的 aik codex 子命令。Use when the user asks to transfer Codex sessions between devices, export sessions for backup or migration, import sessions from another machine, or manage session bundles."
---

# Transfer Codex Sessions 多设备会话迁移

## 目的

使用这个 Skill 时，通过上游工具 `ai-cli-kit`（命令入口 `aik`）在多台设备之间导出、传输和导入 Codex 会话。适用于换机迁移、会话备份、设备间同步等场景。

核心原则：优先使用安全命令（查看、导出、验证），破坏性命令（导入、清理、修复）需要 dry-run 预览和用户确认。

## 前置条件

首次使用前需安装上游工具：

```bash
npm install -g ai-cli-kit
```

验证安装：

```bash
aik --version
```

## 核心流程

### 1. 在源设备上导出会话

```bash
# 查看所有会话
aik codex list

# 导出单个会话
aik codex export <session_id>

# 导出所有桌面端会话
aik codex export-desktop-all

# 仅导出活跃的桌面端会话
aik codex export-active-desktop-all

# 导出所有 CLI 会话
aik codex export-cli-all
```

导出产物默认放在当前目录的 `./codex_sessions/` 下，按会话 ID 组织为独立 bundle 目录。

### 2. 传输 bundle

将 `codex_sessions/` 目录整体传输到目标设备（U 盘、AirDrop、rsync、压缩包等方式）。如果只迁移部分会话，只传对应的 bundle 子目录即可。

### 3. 在目标设备上验证 bundle

在目标设备上导入前，先验证 bundle 完整性：

```bash
aik codex validate-bundles
```

### 4. 导入到目标设备

```bash
# 导入单个会话
aik codex import <session_id|bundle_dir>

# 导入所有 bundle
aik codex import-desktop-all
```

导入前会自动做冲突检查；已存在的会话默认跳过，不会覆盖。

### 5. 验证导入结果

导入后在目标设备上检查会话是否可用：打开 Codex 确认会话列表包含已导入的会话，且可正常打开和继续对话。

## 安全边界

- **bundle 含敏感信息**：导出的 bundle 包含完整对话历史、文件引用、凭据上下文等敏感数据。不得将 bundle 上传到公开仓库、共享网盘或不安全通道。
- **传输中加密**：跨网络传输时使用加密通道（rsync over SSH、加密压缩包等）。
- **用后清理**：传输完成后在传输介质上删除 bundle。
- **破坏性命令需确认**：`import`、`import-desktop-all`、`repair-desktop`、`clean-archived` 默认不为用户自动执行。先解释影响范围，获得用户明确确认后再运行。
- **dry-run 先行**：不确定结果时，先用 `list`、`list-bundles`、`validate-bundles` 等只读命令探查状态。

## 参考

详细的命令清单、参数说明和安全分类见 [references/commands.md](references/commands.md)。当用户需要了解特定命令的参数、行为细节或破坏性命令的影响范围时，读取该文件。
