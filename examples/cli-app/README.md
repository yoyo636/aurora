# cli-app — Aurora CLI 框架示例

基于 `std.cli` 的命令行工具演示，一个文件展示终端彩色输出、进度条、表格、树状结构与交互式输入。

## 功能介绍

| 演示项 | 用到的 API | 说明 |
| --- | --- | --- |
| 彩色输出 | `cli.fg(text, color)` / `cli.bold(text)` / `cli.style(text, ...)` | 红 / 绿 / 黄 / 青等前景色与粗体组合 |
| 状态消息 | `cli.fg(..., "green" / "yellow" / "red")` | 成功 ✔ / 警告 ⚠ / 错误 ✘ 三色消息 |
| 进度条 | `cli.ProgressBar(total, prefix: ..., width: ...)` + `advance()` / `finish()` | 单段进度条，带百分比与前缀 |
| 表格 | `cli.Table(headers, rows)` + `add_row()` + `render()` | 圆角边框终端表格 |
| 树状结构 | `cli.TreeNode(name, icon=)` + `add_child()` + `render()` | 带 📁 图标的目录树 |
| 交互输入 | `cli.input(prompt, default: ...)` / `cli.confirm()` / `cli.select()` | 文本输入、y/N 确认、单选菜单 |

> 说明：非终端（管道 / 重定向）环境下，颜色自动关闭、交互输入走降级路径，脚本仍可正常跑完。

## 运行命令

```bash
cd examples/cli-app
../../aurora-run run cli_app.aur
```

也可只做语法静态检查：

```bash
../../aurora-run check cli_app.aur
```

## 代码结构

```
cli_app.aur
├── section(title)        # 分节标题打印
├── demo_colors()         # 1. 彩色 / 成功 / 警告 / 错误
├── demo_progress()       # 2. 进度条
├── demo_table()          # 3. 表格
├── demo_tree()           # 4. 树状结构
└── demo_input()          # 5. input / confirm / select
```

主流程直接按顺序调用五个 `demo_*` 函数；每个函数内部用 `section()` 打印分隔标题，便于阅读输出。
