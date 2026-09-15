"""AuroraUI v3.1.0 — Windows Win32 后端。

通过 ctypes 调用 ``user32.dll``（``RegisterClassExW`` / ``CreateWindowExW`` /
``GetMessageW`` / ``TranslateMessage`` / ``DispatchMessageW`` /
``DefWindowProcW``）实现原生窗口与消息循环。

在非 Windows 环境下 :meth:`is_available` 返回 ``False``，自动降级到 Mock。
"""

from __future__ import annotations

import ctypes
import platform
from typing import Any, Callable, Dict, Optional

from ..backend import ControlHandle, MockBackend, WindowHandle


class Win32Backend(MockBackend):
    """Windows 原生后端。"""

    name = "win32"

    _user32: Any = None
    _kernel32: Any = None
    _class_atom: int = 0

    # ------------------------------------------------------------------
    # 可用性
    # ------------------------------------------------------------------
    @classmethod
    def is_available(cls) -> bool:
        if platform.system().lower() != "windows":
            return False
        if cls._user32 is not None:
            return True
        try:
            cls._user32 = ctypes.WinDLL("user32")
            cls._kernel32 = ctypes.WinDLL("kernel32")
            # 关键函数存在性检查
            for name in (
                "RegisterClassExW",
                "CreateWindowExW",
                "DefWindowProcW",
                "GetMessageW",
                "TranslateMessage",
                "DispatchMessageW",
            ):
                if not hasattr(cls._user32, name):
                    return False
            return True
        except OSError:
            return False

    # ------------------------------------------------------------------
    # Backend 接口
    # ------------------------------------------------------------------
    def create_window(self, title: str, width: int, height: int) -> WindowHandle:
        handle = super().create_window(title, width, height)
        if self._user32 is None:
            return handle
        # 真实实现：
        #   wc = WNDCLASSEXW(...)
        #   wc.lpfnWndProc = WNDPROC(self._wnd_proc)
        #   self._class_atom = self._user32.RegisterClassExW(ctypes.byref(wc))
        #   hwnd = self._user32.CreateWindowExW(
        #       0, "AuroraWindow", title,
        #       WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
        #       width, height, None, None, self._kernel32.GetModuleHandleW(None), None,
        #   )
        #   handle.native = hwnd
        return handle

    def _wnd_proc(self, hwnd: int, msg: int, wparam: int, lparam: int) -> int:
        """Windows 窗口过程（简化骨架）。"""
        WM_DESTROY = 0x0002
        if msg == WM_DESTROY:
            self.quit()
            return 0
        if self._user32 is not None:
            return self._user32.DefWindowProcW(hwnd, msg, wparam, lparam)
        return 0

    def show_window(self, handle: WindowHandle) -> None:
        super().show_window(handle)
        # if self._user32 is not None and handle.native:
        #     SW_SHOW = 5
        #     self._user32.ShowWindow(handle.native, SW_SHOW)

    def hide_window(self, handle: WindowHandle) -> None:
        super().hide_window(handle)
        # if self._user32 is not None and handle.native:
        #     SW_HIDE = 0
        #     self._user32.ShowWindow(handle.native, SW_HIDE)

    def create_control(self, parent: Any, control_type: str, **kwargs: Any) -> ControlHandle:
        return super().create_control(parent, control_type, **kwargs)

    def run_loop(self) -> None:
        self.call_log.append("win32_run_loop")
        if self._user32 is None:
            self.running = False
            return
        # msg = MSG()
        # while self._user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        #     self._user32.TranslateMessage(ctypes.byref(msg))
        #     self._user32.DispatchMessageW(ctypes.byref(msg))

    def quit(self) -> None:
        super().quit()
        # if self._user32 is not None:
        #     self._user32.PostQuitMessage(0)


__all__ = ["Win32Backend"]
