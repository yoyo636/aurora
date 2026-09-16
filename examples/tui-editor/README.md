# tui-editor — TUI 文本编辑器

基于 `std.tui` 终端 UI 框架的仿 nano 文本编辑器示例，演示 TUI 控件、垂直布局与键盘/点击事件处理。

## 功能介绍

| 区域 | 控件 | 说明 |
| --- | --- | --- |
| 顶部标题条 | `tui.Text(...)` | 显示编辑器标题 |
| 文件名栏 | `tui.Input(x, y, w)` | 输入要打开 / 保存的文件名 |
| 主编辑区 | `tui.TextArea(x, y, w, h)` | 多行文本编辑，按键触发 `on_key` 回调 |
| 按钮栏 | `tui.Button("...", x, y)` + `on_click` | 保存 / 打开 / 退出三个按钮 |
| 状态栏 | `tui.Text(...)` | 显示当前操作状态 |
| 快捷键帮助 | `tui.Text(...)` | 底部一行快捷键提示 |

涉及的核心 API：

- `tui.App("标题")` —— 创建 TUI 应用
- `tui.VBox(x, y, w, h)` —— 垂直布局容器，`add(控件)` 加入子控件
- `tui.Text("文本", x, y)` —— 静态文本
- `tui.Input(x, y, w)` —— 单行输入框，`text()` 读取内容
- `tui.TextArea(x, y, w, h)` —— 多行编辑区，`set_text()` / `text()` / `on_key()`
- `tui.Button("文本", x, y)` —— 按钮，`on_click(fn() { ... })` 绑定点击
- `app.add(vbox)` —— 把布局挂到应用
- `app.run()` —— 进入事件循环

## 文件结构

```
tui-editor/
├── main.aur    # 入口:创建 App、组装 VBox 布局、绑定事件、启动
└── README.md
```

`main.aur` 中的关键流程：

1. `tui.App(...)` 创建应用。
2. `tui.VBox(0, 0, 80, 24)` 作为根容器，按行 `add` 标题、输入框、编辑区、按钮、状态栏。
3. `editor.on_key(...)` / `button.on_click(...)` 绑定事件回调。
4. `app.add(root)` 后 `app.run()` 进入主循环。

## 运行方式

```bash
cd examples/tui-editor
../../aurora-run run main.aur
```

也可只做语法静态检查：

```bash
../../aurora-run check main.aur
```

## 说明

- 界面按 80×24 终端布局；实际运行时 `std.tui` 会处理光标、重绘与键盘事件。
- 保存 / 打开对应的文件读写在本示例中以注释占位（`fs.write_file(...)`），重点演示 TUI 控件与事件。
- 本示例为 v3.2.0 概念演示，实际运行需要解释器注册 `std.tui` 模块支持。
