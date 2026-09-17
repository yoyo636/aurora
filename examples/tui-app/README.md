# tui-app — Aurora TUI 框架示例

基于 `std.tui` 的终端 UI 应用，演示窗口、面板、输入框、列表、按钮与事件循环。

## 功能介绍

| 演示项 | 用到的 API | 说明 |
| --- | --- | --- |
| Window(窗口) | `tui.App(title=...)` | 应用主窗口，自带事件循环与状态栏 |
| Panel(面板) | `tui.Box(x, y, w, h, title: ..., border: true)` | 带边框和标题的容器 |
| TextInput | `tui.Input(x: ..., y: ..., width: ..., placeholder: ...)` | 单行文本输入框，`.value` 读内容 |
| ListBox | `tui.List(items, width: ..., height: ...)` | 上下方向键选择，`.selected_value` 读选中项 |
| Button | `tui.Button("确认", on_click: \|\| {...})` | 回车触发回调 |
| 布局 | `tui.VBox` / `tui.HBox` + `.add(widget)` | 垂直 / 水平排列子控件 |
| 事件循环 | `app.run()` | 方向键/制表键切换焦点，Esc 退出 |

## 运行命令

```bash
cd examples/tui-app
../../aurora-run run tui_app.aur
```

> 本程序需要真实终端（TTY）运行；在管道或非交互环境下会自动进入 Mock 模式，不会阻塞。
> 只做语法检查：`../../aurora-run check tui_app.aur`

## 操作方式

- 输入框中直接打字（退格可删除）
- ↑ / ↓ 在列表中选择项目
- 回车触发「确认」按钮，结果文本会显示当前输入与选中项
- Esc 退出程序

## 代码结构

```
tui_app.aur
└── main()
    ├── App(title=...)              # 主窗口 / 事件循环
    ├── VBox(...)                   # 根垂直布局
    │   ├── Text(标题)
    │   ├── Box(title="输入区")     # 面板
    │   │   └── HBox(...)           # 水平行
    │   │       ├── Input(...)      # 文本输入框
    │   │       └── List(...)       # 列表选择
    │   ├── Text(result)            # 结果显示
    │   └── Button(on_click: ||{}) # 确认按钮
    ├── app.set_status(...)         # 底部状态栏
    └── app.run()                   # 进入事件循环
```

按钮回调里通过闭包读取 `input.value` 和 `list.selected_value`，并写入 `result.text`，完成一次完整的交互闭环。
