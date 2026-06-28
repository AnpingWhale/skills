# aik codex 命令参考

所有命令通过 `aik codex <subcommand>` 执行。默认工作目录为 `~/.codex`，bundle 输出目录默认为当前目录下的 `./codex_sessions/`。

## 查看类命令（安全）

这些命令只读，不会修改任何文件或会话状态。

### `aik codex list`

列出当前设备上所有 Codex 会话。输出包含会话 ID、标题、最后活跃时间等信息。每次导出前建议先执行，了解有哪些会话可以导出。

### `aik codex list-bundles`

列出 `./codex_sessions/` 下所有可用的 bundle。在导入前用于确认有哪些会话可供导入。

### `aik codex validate-bundles`

验证 `./codex_sessions/` 下所有 bundle 的完整性。检查必要文件是否齐全、数据格式是否正确。建议每次导入前运行。

## 导出类命令（安全）

这些命令只创建新文件（bundle），不修改任何已有会话。

### `aik codex export <session_id>`

导出单个指定会话。`session_id` 可从 `aik codex list` 获取。在 `./codex_sessions/<session_id>/` 下生成 bundle。

### `aik codex export-desktop-all`

导出所有桌面端 Codex 会话。包含活跃和已归档的会话。

### `aik codex export-active-desktop-all`

仅导出当前活跃（非归档）的桌面端 Codex 会话。适合只迁移还在使用的会话。

### `aik codex export-cli-all`

导出所有 CLI 端 Codex 会话。

## 导入类命令（破坏性，需确认）

这些命令会将 bundle 写入 `~/.codex` 下的实际会话存储，可能影响 Codex 的会话列表。已存在的会话默认跳过，但 `repair-desktop` 和 `clean-archived` 可能修改或删除已有数据。

### `aik codex import <session_id|bundle_dir>`

导入单个会话。参数可以是会话 ID（从 `./codex_sessions/<id>/` 读取）或完整的 bundle 目录路径。导入前会检查是否已存在同名会话；已存在则跳过。

### `aik codex import-desktop-all`

批量导入 `./codex_sessions/` 下所有 bundle 到桌面端 Codex。包含冲突检查：已存在的会话跳过。**执行前必须获得用户确认。**

## 维护类命令（部分破坏性）

### `aik codex repair-desktop`

修复桌面端 Codex 会话存储中的不一致状态（如孤立的索引条目、损坏的元数据等）。**会修改 `~/.codex` 下的实际数据。执行前必须获得用户确认。**

### `aik codex clean-archived`

清理已归档的会话数据。**会删除 `~/.codex` 下已归档会话的相关文件。执行前建议先用 `aik codex list` 确认哪些会话会被影响，并获得用户确认。**

## 通用参数

| 参数 | 说明 |
| --- | --- |
| `--help` | 查看子命令帮助 |
| `--version` | 查看 ai-cli-kit 版本 |

默认行为：
- 所有导出命令输出到 `./codex_sessions/`
- 所有命令基于 `~/.codex` 作为 Codex 数据根目录
- 导入命令默认非覆盖模式：已存在会话跳过

## 安全分类总结

| 命令 | 级别 | 说明 |
| --- | --- | --- |
| `list` | 安全 | 只读 |
| `list-bundles` | 安全 | 只读 |
| `validate-bundles` | 安全 | 只读 |
| `export` | 安全 | 只写 bundle，不改会话 |
| `export-desktop-all` | 安全 | 只写 bundle，不改会话 |
| `export-active-desktop-all` | 安全 | 只写 bundle，不改会话 |
| `export-cli-all` | 安全 | 只写 bundle，不改会话 |
| `import` | 需确认 | 写入 Codex 会话存储 |
| `import-desktop-all` | 需确认 | 批量写入 Codex 会话存储 |
| `repair-desktop` | 需确认 | 修改 Codex 会话存储 |
| `clean-archived` | 需确认 | 删除已归档会话数据 |
