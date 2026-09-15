"""AuroraUI v3.1.0 — Web (WASM + DOM) 后端。

这个后端不直接调用系统库；它把 AuroraUI 控件树翻译成一份可在浏览器里
运行的 DOM 绑定代码（WASM 编译目标）。

在非浏览器环境下 :meth:`is_available` 返回 ``False``（运行在 CPython 上时
永远如此），工厂会降级到 Mock。真正在 WASM 中运行时，``document`` /
``window`` 等全局对象由 Emscripten 注入。
"""

from __future__ import annotations

import json
import platform
from typing import Any, Callable, Dict, List, Optional

from ..backend import ControlHandle, MockBackend, WindowHandle


class WebBackend(MockBackend):
    """WebAssembly + DOM 目标后端。"""

    name = "web"

    #: 已经生成的 DOM 节点列表（用于回放/测试）
    dom_nodes: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 可用性
    # ------------------------------------------------------------------
    @classmethod
    def is_available(cls) -> bool:
        """在 CPython 下永远返回 False；仅在 Emscripten/WASM 环境中为 True。"""
        import sys

        impl_name = type(getattr(sys, "implementation", None)).__module__ \
            if hasattr(sys, "implementation") else ""
        return "emscripten" in impl_name.lower()

    # ------------------------------------------------------------------
    # Backend 接口 —— 这里记录 DOM 调用序列
    # ------------------------------------------------------------------
    def create_window(self, title: str, width: int, height: int) -> WindowHandle:
        handle = super().create_window(title, width, height)
        self._dom_call(
            "document.createElement",
            {"tag": "main", "id": f"window-{len(self.windows)}",
             "style": f"width:{width}px;height:{height}px"},
        )
        return handle

    def create_control(self, parent: Any, control_type: str, **kwargs: Any) -> ControlHandle:
        handle = super().create_control(parent, control_type, **kwargs)
        self._dom_call(
            "document.createElement",
            {"tag": self._dom_tag(control_type), "props": kwargs},
        )
        return handle

    def set_control_property(self, handle: ControlHandle, prop: str, value: Any) -> None:
        super().set_control_property(handle, prop, value)
        self._dom_call(
            "element.setAttribute",
            {"handle": id(handle), "prop": prop, "value": value},
        )

    def connect_event(
        self, handle: ControlHandle, event_name: str, callback: Callable[..., Any]
    ) -> None:
        super().connect_event(handle, event_name, callback)
        self._dom_call(
            "element.addEventListener",
            {"handle": id(handle), "event": self._dom_event_name(event_name)},
        )

    # ------------------------------------------------------------------
    # 生成可执行的 JS 绑定代码
    # ------------------------------------------------------------------
    def export_js(self) -> str:
        """把录制下来的 DOM 调用序列导出为一段 JS 代码。"""
        lines: List[str] = []
        for call in self.dom_nodes:
            lines.append(f"// {call['api']}")
            lines.append(f"console.log({json.dumps(call['args'])});")
        return "\n".join(lines)

    # -- 内部 ---------------------------------------------------------------

    def _dom_call(self, api: str, args: Dict[str, Any]) -> None:
        self.dom_nodes.append({"api": api, "args": args})

    @staticmethod
    def _dom_tag(control_type: str) -> str:
        return {
            "button": "button",
            "label": "span",
            "textfield": "input",
            "textarea": "textarea",
            "checkbox": "input",
            "radio": "input",
            "combobox": "select",
            "slider": "input",
            "progressbar": "progress",
            "listview": "ul",
            "treeview": "div",
            "tableview": "table",
            "tabview": "div",
            "canvas": "canvas",
            "container": "div",
            "stack": "div",
        }.get(control_type, "div")

    @staticmethod
    def _dom_event_name(event_name: str) -> str:
        return {
            "clicked": "click",
            "toggled": "change",
            "text_changed": "input",
            "selection_changed": "change",
        }.get(event_name, event_name)


__all__ = ["WebBackend"]
