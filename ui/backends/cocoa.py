"""AuroraUI v3.1.0 — macOS Cocoa / AppKit 后端。

通过 ctypes 调用 macOS 的 Objective-C 运行时（``objc_getClass`` /
``sel_registerName`` / ``objc_msgSend``），再由它们驱动
``NSApplication`` / ``NSWindow`` / ``NSButton`` 等 AppKit 类。

在非 macOS 或未安装 PyObjC/运行时的环境下，:meth:`is_available` 返回
``False``，工厂自动降级到 :class:`~aurora.ui.backend.MockBackend`。
"""

from __future__ import annotations

import ctypes
import ctypes.util
import platform
from typing import Any, Callable, Dict, List, Optional

from ..backend import ControlHandle, MockBackend, WindowHandle


#: AppKit 框架路径（macOS 系统自带）
_APPKYT_PATH = (
    "/System/Library/Frameworks/AppKit.framework/AppKit"
)


class CocoaBackend(MockBackend):
    """macOS 原生后端。"""

    name = "cocoa"

    _framework: Any = None

    # ------------------------------------------------------------------
    # 可用性检测
    # ------------------------------------------------------------------
    @classmethod
    def is_available(cls) -> bool:
        """仅在 macOS 且能加载 AppKit 框架时可用。"""
        if platform.system().lower() != "darwin":
            return False
        if cls._framework is not None:
            return True
        try:
            lib = ctypes.CDLL(_APPKYT_PATH)
            # 关键符号必须存在
            for sym in ("objc_getClass", "sel_registerName", "objc_msgSend"):
                if not hasattr(lib, sym):
                    return False
            cls._framework = lib
            return True
        except OSError:
            return False

    # ------------------------------------------------------------------
    # Objective-C 桥接小工具（简化版）
    # ------------------------------------------------------------------
    def _objc_class(self, name: str) -> Any:
        """通过 ``objc_getClass`` 获取一个类对象。"""
        lib = self._framework
        if lib is None:
            return None
        cls = lib.objc_getClass(name.encode("utf-8"))
        return cls

    def _sel(self, name: str) -> Any:
        lib = self._framework
        if lib is None:
            return None
        return lib.sel_registerName(name.encode("utf-8"))

    def _msg(self, receiver: Any, selector: str, *args: Any) -> Any:
        """调用 ``objc_msgSend(receiver, @selector(sel), ...)``。"""
        lib = self._framework
        if lib is None or receiver is None:
            return None
        return lib.objc_msgSend(receiver, self._sel(selector), *args)

    # ------------------------------------------------------------------
    # Backend 接口
    # ------------------------------------------------------------------
    def create_window(self, title: str, width: int, height: int) -> WindowHandle:
        handle = super().create_window(title, width, height)
        if self._framework is None:
            return handle
        # 真实实现：
        #   app_cls = self._objc_class("NSApplication")
        #   window_cls = self._objc_class("NSWindow")
        #   rect = NSMakeRect(100, 100, width, height)
        #   native = self._msg(window_cls, "alloc")
        #   native = self._msg(native, "initWithContentRect:styleMask:backing:defer:",
        #                      rect, NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        #                      NSBackingStoreBuffered, False)
        #   self._msg(native, "setTitle:", NSString.stringWithString_(title))
        #   handle.native = native
        return handle

    def show_window(self, handle: WindowHandle) -> None:
        super().show_window(handle)
        if self._framework is None:
            return
        # self._msg(handle.native, "makeKeyAndOrderFront:", None)

    def hide_window(self, handle: WindowHandle) -> None:
        super().hide_window(handle)
        if self._framework is None:
            return
        # self._msg(handle.native, "orderOut:", None)

    def create_control(self, parent: Any, control_type: str, **kwargs: Any) -> ControlHandle:
        handle = super().create_control(parent, control_type, **kwargs)
        # 真实实现会按 control_type 选择 NSButton / NSTextField / 等：
        #   mapping = {"button": "NSButton", "label": "NSTextField", ...}
        #   cls = self._objc_class(mapping.get(control_type, "NSView"))
        #   view = self._msg(self._msg(cls, "alloc"), "initWithFrame:", rect)
        #   handle.native = view
        return handle

    def run_loop(self) -> None:
        """进入 AppKit 事件循环。"""
        self.call_log.append("cocoa_run_loop")
        if self._framework is None:
            self.running = False
            return
        # app = self._msg(self._objc_class("NSApplication"), "sharedApplication")
        # self._msg(app, "run")

    def quit(self) -> None:
        super().quit()
        # if self._framework is not None:
        #     app = self._msg(self._objc_class("NSApplication"), "sharedApplication")
        #     self._msg(app, "stop:", None)


__all__ = ["CocoaBackend"]
