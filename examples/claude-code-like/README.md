# claude-code-like — AI 编程助手

把 `std.tui` + `std.git` + 文件系统 + AI 引擎组合在一起的类 Claude Code 终端助手示例。一个界面里同时显示 Git 状态、文件列表、AI 对话与聊天输入框。

## 功能介绍

| 区域 | 用到的 API | 说明 |
| --- | --- | --- |
| Git 状态栏 | `git.Repo(".")` + `repo.status()` | 显示当前分支与工作区变更摘要 |
| 最近提交 | `repo.log(max_count=5)` | 列出最近 5 条提交 |
| 文件列表 | 文件系统遍历（`std.fs` 概念演示） | 当前目录文件 |
| AI 对话区 | `tui.TextArea(...)` + `append_text()` | 显示用户提问与 AI 回复 |
| 聊天输入框 | `tui.Input(...)` + `text()` | 输入问题 |
| 发送按钮 | `tui.Button(...).on_click(...)` | 触发 `ask_ai(...)` |
| 快捷提交 | `repo.add(".")` + `repo.commit(msg)` | 一键 add + commit |

涉及的核心 API：

- **Git 绑定**：`git.Repo(".")`、`repo.add(".")`、`repo.commit(message)`、`repo.status()`、`repo.log(max_count=10)`
- **TUI**：`tui.App(...)`、`tui.VBox(...)`、`tui.Text(...)`、`tui.TextArea(...)`、`tui.Input(...)`、`tui.Button(...).on_click(...)`、`app.add(...)`、`app.run()`
- **AI 调用（占位）**：`ask_ai(...)` 把 git 状态 + 文件列表 + 用户问题组装成上下文，实际运行时替换为 `std.ai.chat(...)`

## 文件结构

```
claude-code-like/
├── main.aur    # 入口:TUI 布局 + Git 绑定 + 文件列表 + AI 对话
└── README.md
```

`main.aur` 中的函数划分：

- `load_git_info()` —— 打开仓库，取 `status()` 与 `log()`
- `list_files()` —— 列出当前目录文件
- `ask_ai(question, git_info, files)` —— 组装上下文并调用 AI（占位）
- `quick_commit(repo, message)` —— `add` + `commit` 一键提交
- `main()` —— 组装 TUI 界面并启动事件循环

## 运行方式

```bash
cd examples/claude-code-like
../../aurora-run run main.aur
```

> 注意：本示例会在当前目录打开 Git 仓库，请在一个 `git init` 过的目录里运行。

也可只做语法静态检查：

```bash
../../aurora-run check main.aur
```

## 说明

- AI 调用目前为占位实现（`ask_ai` 返回说明性文本），配置真实模型后替换为 `std.ai.chat(...)`。
- 文件列表以概念形式返回；实际运行由 `std.fs` 提供目录遍历。
- 本示例为 v3.2.0 概念演示，实际运行需要解释器注册 `std.tui` / `std.git` 等模块支持。
