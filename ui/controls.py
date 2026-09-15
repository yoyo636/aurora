"""AuroraUI v3.1.0 — 控件库。

所有控件都继承自 :class:`Widget`。控件本身是跨平台的"模型"对象：
它们持有属性、事件处理器和布局参数；真正创建原生控件的工作由
:meth:`Widget.create` 委托给当前 :class:`~aurora.ui.backend.Backend`。

这样设计的好处：

* 在无显示环境下也能完整地构建控件树、计算布局、断言属性；
* 后端只需要实现 ``create_control / set_control_property / connect_event``。
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from .events import (
    ActionEvent,
    ChangeEvent,
    Event,
    EventDispatcher,
    TextEvent,
    install_event_handlers,
)
from .layout import Layout, LayoutParams, Stack as _StackLayout


# ---------------------------------------------------------------------------
# Widget 基类
# ---------------------------------------------------------------------------

class Widget:
    """所有 UI 控件的基类。

    属性:
        id: 可选的字符串 ID（用于 CSS ``#id`` 选择器与查找）。
        parent: 父控件（容器控件设置）。
        layout_params: :class:`LayoutParams`，由父布局填充。
        visible / enabled: 可见性与可用性。
        tooltip: 悬停提示文本。
        style_class: CSS 类名列表（空格分隔的字符串，类似 HTML class）。
        style: 内联 CSS 字符串。
        bounds: 布局计算后的 ``(x, y, w, h)``。
        backend_handle: 后端创建出来的原生句柄。
    """

    #: 子类对应的后端控件类型字符串
    control_type: str = "widget"

    def __init__(self, **kwargs: Any) -> None:
        self.id: Optional[str] = kwargs.pop("id", None)
        self.parent: Optional["Widget"] = None
        self.layout_params: LayoutParams = kwargs.pop("layout_params", LayoutParams())
        self.visible: bool = kwargs.pop("visible", True)
        self.enabled: bool = kwargs.pop("enabled", True)
        self.tooltip: str = kwargs.pop("tooltip", "")
        self.style_class: str = kwargs.pop("style_class", "")
        self.style: str = kwargs.pop("style", "")
        self.bounds: Tuple[float, float, float, float] = (0, 0, 0, 0)
        self.preferred_width: float = kwargs.pop("width", 80)
        self.preferred_height: float = kwargs.pop("height", 24)
        self.children: List[Widget] = []
        self.dispatcher = EventDispatcher(self)
        self.backend_handle: Any = None
        install_event_handlers(self, self.dispatcher)

    # -- 事件便捷方法 -------------------------------------------------------

    def on_event(self, event_type: str, callback: Callable[[Event], Any]) -> Callable[[], None]:
        """注册一个事件处理器，返回反注册函数。"""
        return self.dispatcher.on(event_type, callback)

    def dispatch(self, event: Event) -> Event:
        """从本控件开始分发事件（默认 target=self）。"""
        event.target = self
        return self.dispatcher.dispatch(event)

    # -- 后端对接 -----------------------------------------------------------

    def backend_props(self) -> Dict[str, Any]:
        """返回应交给后端的初始属性字典。"""
        return {
            "visible": self.visible,
            "enabled": self.enabled,
            "tooltip": self.tooltip,
        }

    def create(self, backend: Any, parent: Any = None) -> Any:
        """在 *backend* 上创建对应的原生控件，并把事件处理器连接上去。"""
        handle = backend.create_control(parent, self.control_type, **self.backend_props())
        self.backend_handle = handle
        if parent is not None and hasattr(parent, "backend_handle"):
            parent = parent.backend_handle
        return handle

    # -- 树操作 -------------------------------------------------------------

    def add_child(self, child: "Widget") -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "Widget") -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def find_by_id(self, widget_id: str) -> Optional["Widget"]:
        if self.id == widget_id:
            return self
        for child in self.children:
            found = child.find_by_id(widget_id)
            if found is not None:
                return found
        return None


# ---------------------------------------------------------------------------
# 基本控件
# ---------------------------------------------------------------------------

class Button(Widget):
    """按钮。"""

    control_type = "button"

    def __init__(
        self,
        text: str = "",
        on_click: Optional[Callable[[Event], Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.preferred_width = max(80, len(text) * 9 + 24)
        self.preferred_height = 28
        if on_click is not None:
            self.on_event("clicked", lambda ev: on_click(ev))

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        return props


class Label(Widget):
    """文本标签，支持简单富文本（用 ``**kwargs`` 传样式）。"""

    control_type = "label"

    def __init__(self, text: str = "", rich: bool = False, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.rich = rich
        self.preferred_width = max(40, len(text) * 8)
        self.preferred_height = 20

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        props["rich"] = self.rich
        return props


class TextField(Widget):
    """单行文本输入框。"""

    control_type = "textfield"

    def __init__(
        self,
        text: str = "",
        placeholder: str = "",
        on_change: Optional[Callable[[str], Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.placeholder = placeholder
        self.preferred_width = 200
        self.preferred_height = 26
        if on_change is not None:
            def _wrap(ev: Event) -> Any:
                if isinstance(ev, TextEvent):
                    return on_change(ev.text)
                return on_change(getattr(ev, "text", ""))
            self.on_event("text_changed", _wrap)

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        props["placeholder"] = self.placeholder
        return props


class TextArea(Widget):
    """多行文本编辑区。"""

    control_type = "textarea"

    def __init__(self, text: str = "", rows: int = 4, cols: int = 40, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.rows = rows
        self.cols = cols
        self.preferred_width = cols * 8
        self.preferred_height = rows * 18

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        props["rows"] = self.rows
        return props


class CheckBox(Widget):
    """复选框。"""

    control_type = "checkbox"

    def __init__(
        self,
        text: str = "",
        checked: bool = False,
        on_change: Optional[Callable[[bool], Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.checked = checked
        self.preferred_width = max(60, len(text) * 8 + 24)
        self.preferred_height = 24
        if on_change is not None:
            self.on_event("toggled", lambda ev: on_change(getattr(ev, "new_value", self.checked)))

    def toggle(self) -> None:
        self.checked = not self.checked
        self.dispatch(ChangeEvent(type="toggled", old_value=not self.checked, new_value=self.checked))

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        props["checked"] = self.checked
        return props


class RadioButton(Widget):
    """单选按钮（同组内同一时刻只能选一个）。"""

    control_type = "radio"

    def __init__(
        self,
        text: str = "",
        group: str = "default",
        checked: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.group = group
        self.checked = checked
        self.preferred_width = max(60, len(text) * 8 + 24)
        self.preferred_height = 24

    def select(self) -> None:
        self.checked = True

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        props["group"] = self.group
        props["checked"] = self.checked
        return props


class ComboBox(Widget):
    """下拉选择框。"""

    control_type = "combobox"

    def __init__(
        self,
        items: Optional[Sequence[str]] = None,
        selected_index: int = 0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.items: List[str] = list(items or [])
        self.selected_index = selected_index
        self.preferred_width = 160
        self.preferred_height = 26

    @property
    def selected_text(self) -> Optional[str]:
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["items"] = list(self.items)
        props["selected_index"] = self.selected_index
        return props


class Slider(Widget):
    """滑块。"""

    control_type = "slider"

    def __init__(
        self,
        min: float = 0,
        max: float = 100,
        value: float = 0,
        orientation: str = "horizontal",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.min = min
        self.max = max
        self.value = value
        self.orientation = orientation
        self.preferred_width = 160 if orientation == "horizontal" else 24
        self.preferred_height = 24 if orientation == "horizontal" else 160

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["min"] = self.min
        props["max"] = self.max
        props["value"] = self.value
        props["orientation"] = self.orientation
        return props


class ProgressBar(Widget):
    """进度条。"""

    control_type = "progressbar"

    def __init__(self, value: float = 0, maximum: float = 100, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.value = value
        self.maximum = maximum
        self.preferred_width = 200
        self.preferred_height = 18

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["value"] = self.value
        props["maximum"] = self.maximum
        return props


# ---------------------------------------------------------------------------
# 容器控件
# ---------------------------------------------------------------------------

class Container(Widget):
    """带一个布局的通用容器。"""

    control_type = "container"

    def __init__(self, layout: Optional[Layout] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.layout: Optional[Layout] = layout

    def add(self, widget: Widget, **params: Any) -> Widget:
        self.add_child(widget)
        if self.layout is not None:
            self.layout.add(widget, **params)
        return widget


class ListView(Widget):
    """列表视图。"""

    control_type = "listview"

    def __init__(
        self,
        items: Optional[Sequence[str]] = None,
        on_select: Optional[Callable[[int, str], Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.items: List[str] = list(items or [])
        self.selected_index: int = -1
        self.preferred_width = 200
        self.preferred_height = 150
        if on_select is not None:
            def _wrap(ev: Event) -> Any:
                idx = getattr(ev, "new_value", -1)
                text = self.items[idx] if 0 <= idx < len(self.items) else ""
                return on_select(idx, text)
            self.on_event("selection_changed", _wrap)

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["items"] = list(self.items)
        return props


class TreeView(Widget):
    """树形视图。"""

    control_type = "treeview"

    def __init__(
        self,
        nodes: Optional[Sequence[Dict[str, Any]]] = None,
        on_select: Optional[Callable[[str], Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.nodes: List[Dict[str, Any]] = list(nodes or [])
        self.preferred_width = 200
        self.preferred_height = 180
        if on_select is not None:
            self.on_event("selection_changed", lambda ev: on_select(getattr(ev, "new_value", "")))

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["nodes"] = list(self.nodes)
        return props


class TableView(Widget):
    """表格视图。"""

    control_type = "tableview"

    def __init__(
        self,
        columns: Optional[Sequence[str]] = None,
        rows: Optional[Sequence[Sequence[Any]]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.columns: List[str] = list(columns or [])
        self.rows: List[List[Any]] = [list(r) for r in (rows or [])]
        self.preferred_width = 400
        self.preferred_height = 200

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["columns"] = list(self.columns)
        props["rows"] = [list(r) for r in self.rows]
        return props


class TabView(Widget):
    """标签页容器。"""

    control_type = "tabview"

    def __init__(self, tabs: Optional[Sequence[Tuple[str, Widget]]] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.tabs: List[Tuple[str, Widget]] = list(tabs or [])
        self.active_index: int = 0
        for _, page in self.tabs:
            self.add_child(page)
        self.preferred_width = 400
        self.preferred_height = 300

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["titles"] = [t for t, _ in self.tabs]
        return props


class Stack(Container):
    """堆叠容器：子控件完全重叠（z 轴顺序即添加顺序）。"""

    control_type = "stack"

    def __init__(self, widgets: Optional[Sequence[Widget]] = None, **kwargs: Any) -> None:
        super().__init__(layout=_StackLayout(), **kwargs)
        for w in widgets or []:
            self.add(w)


# ---------------------------------------------------------------------------
# 系统控件
# ---------------------------------------------------------------------------

class MenuItem(Widget):
    """菜单项。"""

    control_type = "menu_item"

    def __init__(
        self,
        text: str = "",
        shortcut: str = "",
        on_click: Optional[Callable[[], Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.shortcut = shortcut
        if on_click is not None:
            self.on_event("activated", lambda ev: on_click())

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        props["shortcut"] = self.shortcut
        return props


class Menu(Widget):
    """菜单（菜单栏中的一个下拉菜单，或上下文菜单）。"""

    control_type = "menu"

    def __init__(self, title: str = "", items: Optional[Sequence[Widget]] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.items: List[Widget] = list(items or [])
        for item in self.items:
            self.add_child(item)

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["title"] = self.title
        return props


class Toolbar(Widget):
    """工具栏。"""

    control_type = "toolbar"

    def __init__(self, items: Optional[Sequence[Widget]] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.items: List[Widget] = list(items or [])
        self.preferred_height = 36
        for item in self.items:
            self.add_child(item)


class StatusBar(Widget):
    """窗口底部状态栏。"""

    control_type = "statusbar"

    def __init__(self, text: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.preferred_height = 22

    def set_text(self, text: str) -> None:
        self.text = text

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["text"] = self.text
        return props


# ---------------------------------------------------------------------------
# 对话框
# ---------------------------------------------------------------------------

class Dialog(Widget):
    """对话框基类。"""

    control_type = "dialog"

    def __init__(self, title: str = "Dialog", parent: Optional[Widget] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.parent_widget = parent
        self.result: Optional[int] = None
        self.preferred_width = 360
        self.preferred_height = 240

    def open(self) -> Optional[int]:
        """模态打开对话框，返回用户选择结果。"""
        self.result = 0
        return self.result

    def close(self, result: int = 0) -> None:
        self.result = result

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["title"] = self.title
        return props


class MessageDialog(Dialog):
    """消息对话框（OK / Cancel 等按钮）。"""

    control_type = "message_dialog"

    def __init__(
        self,
        title: str = "Message",
        message: str = "",
        buttons: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(title=title, **kwargs)
        self.message = message
        self.buttons: List[str] = list(buttons or ["OK"])

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["message"] = self.message
        props["buttons"] = list(self.buttons)
        return props


class FileDialog(Dialog):
    """文件选择对话框。"""

    control_type = "file_dialog"

    def __init__(self, mode: str = "open", **kwargs: Any) -> None:
        """*mode* 为 ``"open"`` / ``"save"`` / ``"open_directory"``。"""
        super().__init__(title=kwargs.pop("title", mode.title()), **kwargs)
        self.mode = mode
        self.selected_path: str = ""

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["mode"] = self.mode
        return props


class InputDialog(Dialog):
    """文本输入对话框。"""

    control_type = "input_dialog"

    def __init__(self, title: str = "Input", prompt: str = "", default: str = "", **kwargs: Any) -> None:
        super().__init__(title=title, **kwargs)
        self.prompt = prompt
        self.default = default
        self.value: str = default

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["prompt"] = self.prompt
        props["default"] = self.default
        return props


__all__ = [
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
]
