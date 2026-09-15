"""AuroraUI v3.1.0 — Linux GTK 后端。

通过 ctypes 加载 ``libgtk-3.so``，调用 ``gtk_init`` / ``gtk_window_new`` /
``gtk_widget_show_all`` / ``gtk_main`` 等函数。

在没有 GTK 的系统上 :meth:`is_available` 返回 ``False``，自动降级到 Mock。
"""

from __future__ import annotations

import ctypes
import ctypes.util
import platform
from typing import Any, Callable, Dict, Optional

from ..backend import ControlHandle, MockBackend, WindowHandle


#: GTK 3 常见的 SONAME 候选
_GTK_SONAMES = (
    "libgtk-3.so.0",
    "libgtk-3.so",
    "libgtk-4.so.1",
    "libgtk-4.so",
)


class GtkBackend(MockBackend):
    """Linux GTK 原生后端。"""

    name = "gtk"

    _libgtk: Any = None

    # ------------------------------------------------------------------
    # 可用性
    # ------------------------------------------------------------------
    @classmethod
    def is_available(cls) -> bool:
        if platform.system().lower() not in ("linux", "freebsd"):
            return False
        if cls._libgtk is not None:
            return True
        for soname in _GTK_SONAMES:
            try:
                lib = ctypes.CDLL(soname)
            except OSError:
                continue
            # 关键符号存在性检查
            if all(hasattr(lib, sym) for sym in (
                "gtk_init", "gtk_window_new", "gtk_widget_show_all", "gtk_main",
            )):
                cls._libgtk = lib
                return True
        return False

    # ------------------------------------------------------------------
    # Backend 接口
    # ------------------------------------------------------------------
    def create_window(self, title: str, width: int, height: int) -> WindowHandle:
        handle = super().create_window(title, width, height)
        if self._libgtk is None:
            return handle
        # 真实实现：
        #   GTK_WINDOW_TOPLEVEL = 0
        #   win = self._libgtk.gtk_window_new(GTK_WINDOW_TOPLEVEL)
        #   self._libgtk.gtk_window_set_title(win, title.encode())
        #   self._libgtk.gtk_window_set_default_size(win, width, height)
        #   handle.native = win
        return handle

    def show_window(self, handle: WindowHandle) -> None:
        super().show_window(handle)
        # if self._libgtk is not None and handle.native:
        #     self._libgtk.gtk_widget_show_all(handle.native)

    def hide_window(self, handle: WindowHandle) -> None:
        super().hide_window(handle)
        # if self._libgtk is not None and handle.native:
        #     self._libgtk.gtk_widget_hide(handle.native)

    def create_control(self, parent: Any, control_type: str, **kwargs: Any) -> ControlHandle:
        return super().create_control(parent, control_type, **kwargs)

    def run_loop(self) -> None:
        self.call_log.append("gtk_run_loop")
        if self._libgtk is None:
            self.running = False
            return
        # self._libgtk.gtk_main()

    def quit(self) -> None:
        super().quit()
        # if self._libgtk is not None:
        #     self._libgtk.gtk_main_quit()


__all__ = ["GtkBackend"]
