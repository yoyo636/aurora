"""AuroraUI v3.1.0 — 跨平台 GUI 框架。

一行导入即可使用全部公共 API::

    from aurora.ui import (
        Application, Window, Button, VBox, StyleSheet, Canvas, BackendFactory,
    )

本包不强制任何图形环境：在无显示设备 / CI / 无头环境下，
:class:`BackendFactory` 会自动选择 Mock 后端，保证所有 API 可导入、可测试。
"""

from __future__ import annotations

__version__ = "3.1.0"

# -- 后端 -------------------------------------------------------------------
from .backend import (
    Backend,
    BackendFactory,
    ControlHandle,
    MockBackend,
    WindowHandle,
)

# -- 事件 -------------------------------------------------------------------
from .events import (
    ActionEvent,
    ChangeEvent,
    DragEvent,
    Event,
    EventDispatcher,
    KeyEvent,
    MouseEvent,
    PaintEvent,
    TextEvent,
    install_event_handlers,
    on,
)

# -- 布局 -------------------------------------------------------------------
from .layout import (
    ALIGN_CENTER,
    ALIGN_END,
    ALIGN_START,
    ALIGN_STRETCH,
    Anchor,
    Grid,
    HBox,
    Layout,
    LayoutParams,
    Stack as StackLayout,
    VBox,
)

# -- 样式 -------------------------------------------------------------------
from .style import (
    INLINE_SPECIFICITY,
    Selector,
    StyleEngine,
    StyleRule,
    StyleSheet,
    apply_style,
)

# -- 控件 -------------------------------------------------------------------
from .controls import (
    Button,
    CheckBox,
    ComboBox,
    Container,
    Dialog,
    FileDialog,
    InputDialog,
    Label,
    ListView,
    Menu,
    MenuItem,
    MessageDialog,
    ProgressBar,
    RadioButton,
    Slider,
    Stack,
    StatusBar,
    TableView,
    TabView,
    TextArea,
    TextField,
    Toolbar,
    TreeView,
    Widget,
)

# -- Canvas -----------------------------------------------------------------
from .canvas import Canvas, GraphicsContext, Matrix, Path

# -- 窗口 / 应用 ------------------------------------------------------------
from .window import Application, Window


# ---------------------------------------------------------------------------
# CLI 脚手架：``aurora ui new my-app`` 生成项目模板
# ---------------------------------------------------------------------------

def register_cli(subparsers) -> None:
    """把 ``aurora ui`` 子命令注册到 CLI 的 ``subparsers``。

    生成的项目结构::

        my-app/
            main.aur        # 入口
            aurora.toml     # 项目清单
            ui/             # 资源目录
    """
    parser = subparsers.add_parser("ui", help="AuroraUI GUI 脚手架")
    sub = parser.add_subparsers(dest="ui_command")

    new_parser = sub.add_parser("new", help="创建一个新的 AuroraUI 项目")
    new_parser.add_argument("name", help="项目名（同时作为目录名）")
    new_parser.set_defaults(_handler=_cmd_new)


def _cmd_new(args) -> int:
    """实际执行 ``aurora ui new <name>``。"""
    import os
    import sys

    name = getattr(args, "name", "my-aurora-app")
    root = os.path.abspath(name)
    os.makedirs(os.path.join(root, "ui"), exist_ok=True)

    main_src = (
        '// AuroraUI v3.1.0 入口\n'
        'use aurora.ui\n'
        '\n'
        'fn main() {\n'
        '    let app = Application()\n'
        '    app.set_app_name("' + name + '")\n'
        '\n'
        '    let win = Window("Hello Aurora", width=640, height=480)\n'
        '    let vbox = VBox(spacing=8, padding=16)\n'
        '    vbox.add(Label("Welcome to AuroraUI!"))\n'
        '    vbox.add(Button("Click me", on_click=fn(e) { print("clicked!") }))\n'
        '\n'
        '    win.set_content(vbox)\n'
        '    win.show()\n'
        '    app.run()\n'
        '}\n'
    )

    toml_src = (
        f'[project]\n'
        f'name = "{name}"\n'
        f'version = "0.1.0"\n'
        f'description = "AuroraUI application"\n'
        f'\n'
        f'[dependencies]\n'
        f'aurora-ui = ">={__version__}"\n'
    )

    with open(os.path.join(root, "main.aurora"), "w", encoding="utf-8") as f:
        f.write(main_src)
    with open(os.path.join(root, "aurora.toml"), "w", encoding="utf-8") as f:
        f.write(toml_src)

    print(f"✓ 已创建 AuroraUI 项目：{root}")
    print(f"  下一步：cd {name} && aurora run main.aur")
    return 0


__all__ = [
    # 版本
    "__version__",
    # 后端
    "Backend",
    "BackendFactory",
    "ControlHandle",
    "MockBackend",
    "WindowHandle",
    # 事件
    "ActionEvent",
    "ChangeEvent",
    "DragEvent",
    "Event",
    "EventDispatcher",
    "KeyEvent",
    "MouseEvent",
    "PaintEvent",
    "TextEvent",
    "install_event_handlers",
    "on",
    # 布局
    "ALIGN_CENTER",
    "ALIGN_END",
    "ALIGN_START",
    "ALIGN_STRETCH",
    "Anchor",
    "Grid",
    "HBox",
    "Layout",
    "LayoutParams",
    "StackLayout",
    "VBox",
    # 样式
    "INLINE_SPECIFICITY",
    "Selector",
    "StyleEngine",
    "StyleRule",
    "StyleSheet",
    "apply_style",
    # 控件
    "Button",
    "CheckBox",
    "ComboBox",
    "Container",
    "Dialog",
    "FileDialog",
    "InputDialog",
    "Label",
    "ListView",
    "Menu",
    "MenuItem",
    "MessageDialog",
    "ProgressBar",
    "RadioButton",
    "Slider",
    "Stack",
    "StatusBar",
    "TableView",
    "TabView",
    "TextArea",
    "TextField",
    "Toolbar",
    "TreeView",
    "Widget",
    # Canvas
    "Canvas",
    "GraphicsContext",
    "Matrix",
    "Path",
    # 窗口
    "Application",
    "Window",
    # CLI
    "register_cli",
]
