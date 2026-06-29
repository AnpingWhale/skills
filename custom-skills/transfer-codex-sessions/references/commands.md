# aik codex 命令参考

所有命令通过 `aik codex <subcommand>` 执行。默认 Codex 数据根目录为 `~/.codex`，bundle 输出目录默认为当前目录下的 `./codex_sessions/`。导出前先切到私有工作目录；不要在公开 Git 仓库、同步盘或共享目录中生成 bundle。

## 查看类命令（安全，只读）

这些命令不修改任何文件或会话状态。

### `aik codex list [pattern] [--limit N]`

列出本地 Codex 会话。输出包含会话 ID、标题、最后活跃时间等。可选 `pattern` 做子串过滤，`--limit` 控制最大输出行数（默认 30）。

### `aik codex list-bundles [pattern] [--limit N] [--source all|bundle|desktop]`

列出 `./codex_sessions/` 下可用的导出 bundle。`--source` 过滤 bundle 来源：`all`（全部）、`bundle`（单次导出）、`desktop`（批量导出）。

### `aik codex validate-bundles [pattern] [--source all|bundle|desktop] [--limit N] [--verbose]`

验证 bundle 完整性：检查必要文件是否齐全、数据格式是否正确。`--verbose` 同时输出验证通过的 bundle。建议每次导入前运行。

## 导出类命令（安全，只创建新文件）

这些命令只创建 bundle 文件，不修改已有会话。bundle 仍然包含完整会话内容和潜在敏感上下文，输出目录必须保持私有。

### `aik codex export <session_id>`

导出单个会话。`session_id` 从 `aik codex list` 获取。在 `./codex_sessions/<session_id>/` 下生成 bundle。

### `aik codex export-desktop-all [--dry-run]`

批量导出所有桌面端 Codex 会话（含活跃和已归档）。`--dry-run` 预览不写文件。

### `aik codex export-active-desktop-all [--dry-run]`

仅导出当前活跃（非归档）的桌面端 Codex 会话。

### `aik codex export-cli-all [--dry-run]`

批量导出所有 CLI 端 Codex 会话。

## 导入类命令（需确认，写入 Codex 会话存储）

这些命令将 bundle 写入 `~/.codex` 下的实际会话存储。已存在会话默认跳过，不会覆盖。

导入命令不支持 `--dry-run`。执行前必须先运行 `list-bundles` 和 `validate-bundles`，确认候选 bundle、来源、machine/export group、目标设备冲突和默认跳过项，并把影响范围说明给用户确认。不要向 `import` 或 `import-desktop-all` 添加不存在的 `--dry-run` 参数。

### `aik codex import <input_value> [--desktop-visible] [--source all|bundle|desktop] [--machine MACHINE] [--export-group GROUP]`

导入单个会话。`input_value` 可以是会话 ID（从 bundle 搜索匹配）或完整 bundle 目录路径。`--desktop-visible` 使导入的会话在桌面端侧边栏可见。`--machine` 和 `--export-group` 用于在多 machine/bundle 中精确定位。执行前必须获得用户确认。

### `aik codex import-desktop-all [--desktop-visible] [--machine MACHINE] [--export-group GROUP] [--latest-only]`

批量导入 `./codex_sessions/` 下所有匹配条件的 bundle。`--latest-only` 仅导入每个 machine 和 session id 的最新版本。**不支持 dry-run，执行前必须完成只读预检和用户确认。**

## 供应商克隆类命令

### `aik codex clone-provider [target_provider] [--dry-run]`

将活跃 Codex 会话克隆为当前（或指定）AI 供应商可读的副本。`target_provider` 可选覆盖目标供应商。`--dry-run` 预览变更不写文件。

### `aik codex watch-provider [--interval SECONDS] [--dry-run] [--no-initial-sync] [--once]`

持续监听供应商配置变化，变化时自动触发 `clone-provider`。`--interval` 轮询间隔（秒），`--no-initial-sync` 跳过启动时的首次同步，`--once` 执行一次检查后退出。

## 维护清理类命令（部分破坏性，需确认）

### `aik codex repair-desktop [target_provider] [--dry-run] [--include-cli]`

修复桌面端 Codex 会话存储的一致性问题（侧边栏可见性、索引、供应商元数据）。`--include-cli` 同时修复 CLI 会话。**会修改 `~/.codex` 实际数据，执行前必须获得用户确认。**

### `aik codex clean-archived [--dry-run] [--yes]`

删除已归档 Codex 会话的所有相关文件。**`--yes` 必须显式提供才执行实际删除。** 建议先用 `aik codex list` 确认哪些会话会被影响。

### `aik codex clean-clones [target_provider] [--dry-run]`

删除之前克隆运行遗留的未标记 clone 文件。

### `aik codex dedupe-clones [target_provider] [--dry-run]`

保守去重：当原始会话仍然存在时，删除其 clone 副本（而非反向）。

## 通用参数

| 参数 | 适用命令 | 说明 |
| --- | --- | --- |
| `--dry-run` | clone-provider, watch-provider, export-desktop-all, export-active-desktop-all, export-cli-all, clean-clones, clean-archived, dedupe-clones, repair-desktop | 预览变更不写文件 |
| `--source` | list-bundles, validate-bundles, import | 过滤 bundle 来源：`all` / `bundle` / `desktop` |
| `--machine` | import, import-desktop-all | 限制 bundle 匹配到指定 machine key |
| `--export-group` | import, import-desktop-all | 限制 bundle 匹配到指定导出批次（desktop/active/cli/single） |
| `--desktop-visible` | import, import-desktop-all | 导入后使会话在桌面端侧边栏可见 |
| `--limit` | list, list-bundles, validate-bundles | 最大输出/处理行数 |
| `--verbose` | validate-bundles | 同时输出验证通过的 bundle |

## 安全分类

| 级别 | 命令 |
| --- | --- |
| **安全（只读）** | `list`、`list-bundles`、`validate-bundles` |
| **安全（只写 bundle，不改会话）** | `export`、`export-desktop-all`、`export-active-desktop-all`、`export-cli-all`、`clone-provider`（dry-run）、`watch-provider`（dry-run） |
| **需确认（写入会话存储，不支持 dry-run）** | `import`、`import-desktop-all` |
| **需确认（写入会话存储，支持 dry-run）** | `clone-provider`（执行）、`watch-provider`（执行） |
| **需确认（修改/删除数据）** | `repair-desktop`、`clean-archived`、`clean-clones`、`dedupe-clones` |
