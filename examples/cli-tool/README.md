# cli-tool — 命令行工具示例

基于 `std.cli` 的命令行工具演示，模拟一个类似 git 的小工具，展示终端彩色输出、表格渲染、加载动画与交互提示。

## 功能介绍

| 演示项 | 用到的 API | 说明 |
| --- | --- | --- |
| 彩色输出 | `cli.color.fg(text, "green" / "yellow" / "red")` | 成功 / 警告 / 错误三色消息 |
| 样式文本 | `cli.bold(text)` / `cli.underline(text)` | 加粗与下划线 |
| 表格渲染 | `cli.Table(headers, rows)` + `table.render()` | 仿 git status 的文件状态表 |
| 加载动画 | `cli.Spinner("加载中")` + `start()` / `stop()` | 克隆仓库时的旋转指示器 |
| 交互确认 | `cli.confirm("继续吗?", default=false)` | y/N 确认，返回 bool |
| 单选菜单 | `cli.select("选择:", ["选项1", ...])` | 编号选择菜单，返回选中项 |

## 文件结构

```
cli-tool/
├── main.aur    # 入口:解析演示流程,调用各 demo_* 函数
└── README.md
```

`main.aur` 中的函数划分：

- `demo_colors()` —— 彩色 / 成功 / 警告 / 错误
- `demo_table()` —— `cli.Table` 渲染文件状态表
- `demo_spinner()` —— `cli.Spinner` 加载动画
- `demo_interactive()` —— `cli.confirm` 与 `cli.select`

## 运行方式

```bash
cd examples/cli-tool
../../aurora-run run main.aur
```

也可只做语法静态检查：

```bash
../../aurora-run check main.aur
```

## 说明

- 非终端（管道 / 重定向）环境下，颜色自动关闭，交互提示走降级路径。
- 本示例为 v3.2.0 概念演示，实际运行需要解释器注册 `std.cli` 模块支持。
