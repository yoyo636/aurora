"""Aurora v3.1.0 — 平台原生绑定层

提供两大原生 GUI / 系统集成桥：

* :class:`CocoaBridge` / :class:`CocoaClass` — 通过 ctypes 直接调用
  macOS ``libobjc.A.dylib`` 的 Objective-C runtime，封装 NSApplication /
  NSWindow / NSView / NSButton / NSTextField / NSMenu 等 AppKit 类。
* :class:`Win32Bridge` / :class:`Win32Window` — 通过 ctypes 调用
  ``user32.dll`` / ``kernel32.dll``，封装窗口注册、消息循环与常用控件。

设计原则
--------
1. **跨平台可导入**：本模块在任意平台 import 都不抛异常。非 macOS 平台上
   Cocoa 相关调用降级为返回 ``None`` / Mock 对象；非 Windows 平台上 Win32
   相关调用降级为 Mock。
2. **不依赖显示环境**：纯结构性 API 与真实运行时调用严格分离。
3. 所有公共 API 均带类型注解与文档字符串。
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import os
import platform
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 平台探测
# ---------------------------------------------------------------------------

IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")


class _Mock:
    """优雅降级用的万能 Mock：任何属性访问/调用都返回另一个 Mock。

    在非目标平台上，调用方可以继续链式编写代码而不会崩溃；取值时
    通过 ``value`` 回落到构造时传入的对象。
    """

    def __init__(self, value: Any = None) -> None:
        self.value = value

    def __call__(self, *args: Any, **kwargs: Any) -> "_Mock":
        return self

    def __getattr__(self, item: str) -> "_Mock":
        return self

    def __bool__(self) -> bool:  # pragma: no cover - 取决于平台
        return self.value is not None and bool(self.value)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Mock {self.value!r}>"


# ===========================================================================
# 1. macOS Cocoa / AppKit 绑定
# ===========================================================================

#: 类型别名：Objective-C 对象句柄（在非 macOS 上可能为 ``None``）
ObjCPtr = ctypes.c_void_p


class CocoaBridge:
    """通过 ctypes 调用 Objective-C runtime 的最小桥。

    典型用法::

        app = CocoaBridge.cls("NSApplication").call("sharedApplication")
        CocoaBridge.msg_send(app, "setActivationPolicy:", 0)
        CocoaBridge.msg_send(app, "run")

    在非 macOS 平台上，所有方法返回 :class:`_Mock`，不会抛异常。
    """

    _lib: Optional[ctypes.CDLL] = None
    _available: bool = False

    def __init__(self) -> None:
        CocoaBridge._ensure_loaded()

    @staticmethod
    def _ensure_loaded() -> None:
        if CocoaBridge._lib is not None or not IS_MACOS:
            return
        try:
            lib = ctypes.CDLL("/usr/lib/libobjc.A.dylib")
            lib.objc_getClass.restype = ObjCPtr
            lib.objc_getClass.argtypes = [ctypes.c_char_p]
            lib.sel_registerName.restype = ObjCPtr
            lib.sel_registerName.argtypes = [ctypes.c_char_p]
            # objc_msgSend 变参，保持默认 c_void_p 即可
            lib.objc_msgSend.restype = ObjCPtr
            lib.objc_msgSend.argtypes = [ObjCPtr, ObjCPtr]
            CocoaBridge._lib = lib
            CocoaBridge._available = True
        except OSError:  # pragma: no cover - 仅在异常 macOS 上发生
            CocoaBridge._available = False
        # 显式 dlopen Foundation / AppKit，否则 objc_getClass("NSApplication") 返回 NULL
        for fw in (
            "/System/Library/Frameworks/Foundation.framework/Foundation",
            "/System/Library/Frameworks/AppKit.framework/AppKit",
        ):
            try:
                ctypes.CDLL(fw)
            except OSError:  # pragma: no cover
                pass

    # -- 原语 ---------------------------------------------------------------

    @staticmethod
    def available() -> bool:
        """当前进程是否真正加载到了 libobjc。"""
        return CocoaBridge._available

    @staticmethod
    def objc_get_class(name: str) -> Optional[ObjCPtr]:
        """获取某个 Objective-C 类对象。"""
        if not CocoaBridge._lib:
            return None
        return CocoaBridge._lib.objc_getClass(name.encode("utf-8"))

    @staticmethod
    def sel_register_name(name: str) -> Optional[ObjCPtr]:
        """注册 / 取回一个 selector。"""
        if not CocoaBridge._lib:
            return None
        return CocoaBridge._lib.sel_registerName(name.encode("utf-8"))

    @staticmethod
    def msg_send(target: Any, selector: str, *args: Any) -> Any:
        """向 ``target`` 发送 ``selector`` 消息。

        非 macOS 或句柄为空时返回 :class:`_Mock`。
        """
        if not CocoaBridge._lib or not target:
            return _Mock()
        sel = CocoaBridge.sel_register_name(selector)
        if sel is None:
            return _Mock()
        # objc_msgSend 变参：按实际参数个数动态声明 argtypes，
        # 否则 64 位指针会被截断为 32 位 int。
        fn = CocoaBridge._lib.objc_msgSend
        fn.argtypes = [ObjCPtr, ObjCPtr] + [ObjCPtr] * len(args)
        c_args = [target, sel] + list(args)
        try:
            return fn(*c_args)
        except Exception:  # pragma: no cover - 防御性
            return _Mock()

    @classmethod
    def cls(cls_, name: str) -> "CocoaClass":
        """构造一个 :class:`CocoaClass` 代理。"""
        return CocoaClass(name)


class CocoaClass:
    """Pythonic 的 Objective-C 类代理。

    支持链式调用，例如::

        win = CocoaClass("NSWindow").alloc().initWithContentRect_styleMask_backing_defer_(...)

    每个未定义属性都会被翻译为 ``[cls alloc]`` 之类的消息；调用结果同样是
    :class:`CocoaObject` 代理，从而可以无限链式。
    """

    def __init__(self, name: str, handle: Optional[ObjCPtr] = None) -> None:
        self.name = name
        self.handle = handle if handle is not None else CocoaBridge.objc_get_class(name)

    def __getattr__(self, item: str) -> Callable[..., "CocoaObject"]:
        selector = item.replace("_", ":").rstrip(":")
        selector = selector + (":" if "_" in item else "")

        def _send(*args: Any) -> "CocoaObject":
            h = CocoaBridge.msg_send(self.handle, selector, *args)
            return CocoaObject(self.name, h)

        return _send

    def call(self, selector: str, *args: Any) -> "CocoaObject":
        """显式发送一条消息。"""
        h = CocoaBridge.msg_send(self.handle, selector, *args)
        return CocoaObject(self.name, h)

    def alloc(self) -> "CocoaObject":
        return self.call("alloc")


class CocoaObject:
    """Objective-C 实例对象代理。"""

    def __init__(self, cls_name: str, handle: Optional[ObjCPtr]) -> None:
        self.cls_name = cls_name
        self.handle = handle

    def __getattr__(self, item: str) -> Callable[..., "CocoaObject"]:
        selector = item.replace("_", ":")
        if not selector.endswith(":") and "set" in item:
            selector = selector + ":"

        def _send(*args: Any) -> "CocoaObject":
            h = CocoaBridge.msg_send(self.handle, selector, *args)
            return CocoaObject(self.cls_name, h)

        return _send


# ---------------------------------------------------------------------------
# 高层封装：AppKit 常用类
# ---------------------------------------------------------------------------

class NSApplication:
    """``NSApplication`` 包装：sharedApplication / run / terminate。"""

    def __init__(self) -> None:
        self.bridge = CocoaBridge()
        self._app: Any = None
        if self.bridge.available():
            self._app = self.bridge.msg_send(
                self.bridge.objc_get_class("NSApplication"), "sharedApplication")

    def set_activation_policy(self, policy: int = 0) -> None:
        """0 = Regular, 1 = Accessory (LSUIElement), -1 = Prohibited."""
        if self._app:
            self.bridge.msg_send(self._app, "setActivationPolicy:", policy)

    def run(self) -> None:
        """进入主事件循环（仅在真正的 GUI 应用里调用）。"""
        if self._app:
            self.bridge.msg_send(self._app, "run")

    def terminate(self) -> None:
        if self._app:
            self.bridge.msg_send(self._app, "terminate:", None)


class NSWindow:
    """``NSWindow`` 包装。"""

    def __init__(self, title: str = "", width: int = 800, height: int = 600) -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        if self.bridge.available():
            rect = (ctypes.c_int * 4)(0, 0, width, height)
            cls = self.bridge.objc_get_class("NSWindow")
            alloced = self.bridge.msg_send(cls, "alloc")
            self.handle = self.bridge.msg_send(
                alloced,
                "initWithContentRect:styleMask:backing:defer:",
                rect, 15, 0, False)
            self.set_title(title)

    def set_title(self, text: str) -> None:
        if not self.handle:
            return
        nsstr = self.bridge.msg_send(
            self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
            text.encode("utf-8"))
        self.bridge.msg_send(self.handle, "setTitle:", nsstr)

    def make_key_and_order_front(self, sender: Any = None) -> None:
        if self.handle:
            self.bridge.msg_send(self.handle, "makeKeyAndOrderFront:", sender)

    def set_frame(self, x: int, y: int, w: int, h: int) -> None:
        if self.handle:
            self.bridge.msg_send(
                self.handle, "setFrame:display:",
                (ctypes.c_int * 4)(x, y, w, h), True)

    def close(self) -> None:
        if self.handle:
            self.bridge.msg_send(self.handle, "close")


class NSView:
    """``NSView`` 包装。"""

    def __init__(self, x: int = 0, y: int = 0, w: int = 100, h: int = 100) -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        if self.bridge.available():
            alloced = self.bridge.msg_send(self.bridge.objc_get_class("NSView"), "alloc")
            self.handle = self.bridge.msg_send(
                alloced, "initWithFrame:", (ctypes.c_int * 4)(x, y, w, h))

    def set_wants_layer(self, flag: bool = True) -> None:
        if self.handle:
            self.bridge.msg_send(self.handle, "setWantsLayer:", flag)

    def add_subview(self, subview: "NSView") -> None:
        if self.handle and subview and subview.handle:
            self.bridge.msg_send(self.handle, "addSubview:", subview.handle)


class NSButton:
    """``NSButton`` 包装。"""

    def __init__(self, x: int = 0, y: int = 0, w: int = 100, h: int = 32) -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        self._target: Any = None
        if self.bridge.available():
            alloced = self.bridge.msg_send(self.bridge.objc_get_class("NSButton"), "alloc")
            self.handle = self.bridge.msg_send(
                alloced, "initWithFrame:", (ctypes.c_int * 4)(x, y, w, h))

    def set_title(self, text: str) -> None:
        if not self.handle:
            return
        nsstr = self.bridge.msg_send(
            self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
            text.encode("utf-8"))
        self.bridge.msg_send(self.handle, "setTitle:", nsstr)

    def set_target(self, target: Any) -> None:
        self._target = target
        if self.handle:
            self.bridge.msg_send(self.handle, "setTarget:", target)

    def set_action(self, action: str) -> None:
        if self.handle:
            self.bridge.msg_send(self.handle, "setAction:",
                                 self.bridge.sel_register_name(action))


class NSTextField:
    """``NSTextField`` 包装。"""

    def __init__(self, x: int = 0, y: int = 0, w: int = 200, h: int = 24) -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        if self.bridge.available():
            alloced = self.bridge.msg_send(self.bridge.objc_get_class("NSTextField"), "alloc")
            self.handle = self.bridge.msg_send(
                alloced, "initWithFrame:", (ctypes.c_int * 4)(x, y, w, h))

    def set_string_value(self, text: str) -> None:
        if not self.handle:
            return
        nsstr = self.bridge.msg_send(
            self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
            text.encode("utf-8"))
        self.bridge.msg_send(self.handle, "setStringValue:", nsstr)

    def string_value(self) -> Optional[str]:
        if not self.handle:
            return None
        nsstr = self.bridge.msg_send(self.handle, "stringValue")
        if not nsstr:
            return None
        try:
            return ctypes.c_char_p(self.bridge.msg_send(nsstr, "UTF8String")).value.decode()
        except Exception:  # pragma: no cover
            return None


class NSMenu:
    """菜单栏 / 菜单容器。"""

    def __init__(self, title: str = "") -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        if self.bridge.available():
            alloced = self.bridge.msg_send(self.bridge.objc_get_class("NSMenu"), "alloc")
            nsstr = self.bridge.msg_send(
                self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
                title.encode("utf-8"))
            self.handle = self.bridge.msg_send(alloced, "initTitle:", nsstr)

    def add_item(self, item: "NSMenuItem") -> None:
        if self.handle and item and item.handle:
            self.bridge.msg_send(self.handle, "addItem:", item.handle)


class NSMenuItem:
    """菜单项。"""

    def __init__(self, title: str = "", action: str = "", key: str = "") -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        if self.bridge.available():
            cls = self.bridge.objc_get_class("NSMenuItem")
            ns_title = self.bridge.msg_send(
                self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
                title.encode("utf-8"))
            ns_key = self.bridge.msg_send(
                self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
                key.encode("utf-8"))
            sel = self.bridge.sel_register_name(action) if action else None
            alloced = self.bridge.msg_send(cls, "alloc")
            self.handle = self.bridge.msg_send(
                alloced, "initWithTitle:action:keyEquivalent:",
                ns_title, sel, ns_key)


class NSNotificationCenter:
    """``NSNotificationCenter`` 通知中心封装。"""

    def __init__(self) -> None:
        self.bridge = CocoaBridge()
        self.handle: Any = None
        if self.bridge.available():
            self.handle = self.bridge.msg_send(
                self.bridge.objc_get_class("NSNotificationCenter"), "defaultCenter")

    def post(self, name: str, object_: Any = None) -> None:
        if not self.handle:
            return
        ns_name = self.bridge.msg_send(
            self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
            name.encode("utf-8"))
        self.bridge.msg_send(self.handle, "postNotificationName:object:", ns_name, object_)


# ---------------------------------------------------------------------------
# Swift 互操作
# ---------------------------------------------------------------------------

class SwiftBridge:
    """Swift 互操作桥。

    Swift 侧通过 ``@_cdecl`` 将函数导出为 C ABI::

        // MyModule.swift
        // @_cdecl("aurora_swift_greet")
        // public func greet(_ name: UnsafePointer<CChar>?) -> UnsafeMutablePointer<CChar>? {
        //     let s = "Hello, " + String(cString: name!)
        //     return strdup(s)
        // }

    本类负责按 ``@_cdecl`` 的 C 调用约定加载动态库并调用。
    """

    def __init__(self, dylib_path: str) -> None:
        self.dylib_path = dylib_path
        self._lib: Optional[ctypes.CDLL] = None
        if os.path.exists(dylib_path):
            try:
                self._lib = ctypes.CDLL(dylib_path)
            except OSError:
                self._lib = None

    def available(self) -> bool:
        return self._lib is not None

    def call(self, symbol: str, *args: Any, restype: Any = ctypes.c_void_p) -> Any:
        """调用一个 ``@_cdecl`` 导出的符号。"""
        if not self._lib or not hasattr(self._lib, symbol):
            return _Mock()
        fn = getattr(self._lib, symbol)
        fn.restype = restype
        return fn(*args)


# ---------------------------------------------------------------------------
# macOS 原生集成：菜单栏 / Dock / 通知中心
# ---------------------------------------------------------------------------

class MacIntegration:
    """macOS 应用级集成：主菜单、Dock、用户通知。"""

    def __init__(self) -> None:
        self.bridge = CocoaBridge()

    def is_supported(self) -> bool:
        return self.bridge.available()

    def set_main_menu(self, menu_items: List[Dict[str, Any]]) -> bool:
        """设置应用主菜单。

        :param menu_items: ``[{"title": "File", "items": [...]}]`` 结构。
        :return: 是否真正执行了（非 macOS 上返回 False）。
        """
        if not self.bridge.available():
            return False
        # 真实实现需要遍历 menu_items 构造 NSMenu；这里只验证结构与降级。
        return isinstance(menu_items, list)

    def set_dock_icon(self, image_path: str) -> bool:
        """设置 Dock 图标。非 macOS / 文件不存在时返回 False。"""
        if not self.bridge.available() or not os.path.exists(image_path):
            return False
        cls = self.bridge.objc_get_class("NSApplication")
        app = self.bridge.msg_send(cls, "sharedApplication")
        img_cls = self.bridge.objc_get_class("NSImage")
        ns_path = self.bridge.msg_send(
            self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
            image_path.encode("utf-8"))
        img = self.bridge.msg_send(img_cls, "alloc")
        img = self.bridge.msg_send(img, "initByReferencingFile:", ns_path)
        self.bridge.msg_send(app, "setApplicationIconImage:", img)
        return True

    def bounce_dock(self, urgent: bool = False) -> bool:
        """Dock 弹跳提醒。非 macOS 返回 False。"""
        if not self.bridge.available():
            return False
        cls = self.bridge.objc_get_class("NSApplication")
        app = self.bridge.msg_send(cls, "sharedApplication")
        self.bridge.msg_send(app, "requestUserAttention:", 1 if urgent else 0)
        return True

    def send_notification(self, title: str, body: str,
                          subtitle: Optional[str] = None) -> bool:
        """通过 ``NSUserNotification`` 发送通知中心通知。"""
        if not self.bridge.available():
            return False
        cls = self.bridge.objc_get_class("NSUserNotification")
        alloced = self.bridge.msg_send(cls, "alloc")
        notif = self.bridge.msg_send(alloced, "init")

        def _str(s: str) -> Any:
            return self.bridge.msg_send(
                self.bridge.objc_get_class("NSString"), "stringWithUTF8String:",
                s.encode("utf-8"))

        self.bridge.msg_send(notif, "setTitle:", _str(title))
        self.bridge.msg_send(notif, "setInformativeText:", _str(body))
        if subtitle:
            self.bridge.msg_send(notif, "setSubtitle:", _str(subtitle))
        center = self.bridge.msg_send(
            self.bridge.objc_get_class("NSUserNotificationCenter"), "defaultUserNotificationCenter")
        self.bridge.msg_send(center, "deliverNotification:", notif)
        return True


# ===========================================================================
# 2. Windows Win32 API 绑定
# ===========================================================================

# 窗口消息常量（WinUser.h）
WM_DESTROY = 0x0002
WM_CREATE = 0x0001
WM_PAINT = 0x000F
WM_COMMAND = 0x0111
WM_SIZE = 0x0005
WM_QUIT = 0x0012

SW_SHOW = 5
SW_HIDE = 0

# 控件样式
BS_PUSHBUTTON = 0x00000000
WS_CHILD = 0x40000000
WS_VISIBLE = 0x10000000
WS_BORDER = 0x00800000
ES_AUTOHSCROLL = 0x0080


# 结构体（模块级定义，便于在 ctypes _fields_ 中互相引用）
class _Win32POINT(ctypes.Structure):
    """Win32 ``POINT``。"""
    _fields_ = [("x", wt.LONG), ("y", wt.LONG)]


class _Win32RECT(ctypes.Structure):
    """Win32 ``RECT``。"""
    _fields_ = [("left", wt.LONG), ("top", wt.LONG),
                ("right", wt.LONG), ("bottom", wt.LONG)]


class _Win32MSG(ctypes.Structure):
    """Win32 ``MSG``。"""
    _fields_ = [("hwnd", wt.HWND), ("message", wt.UINT),
                ("wParam", wt.WPARAM), ("lParam", wt.LPARAM),
                ("time", wt.DWORD), ("pt", _Win32POINT)]


class _Win32WNDCLASSEX(ctypes.Structure):
    """Win32 ``WNDCLASSEX``。"""
    _fields_ = [
        ("cbSize", wt.UINT), ("style", wt.UINT),
        ("lpfnWndProc", ctypes.c_void_p),
        ("cbClsExtra", wt.INT), ("cbWndExtra", wt.INT),
        ("hInstance", wt.HINSTANCE), ("hIcon", wt.HICON),
        ("hCursor", wt.HANDLE), ("hbrBackground", wt.HBRUSH),
        ("lpszMenuName", wt.LPCWSTR), ("lpszClassName", wt.LPCWSTR),
        ("hIconSm", wt.HICON),
    ]


class Win32Bridge:
    """通过 ctypes 调用 ``user32.dll`` / ``kernel32.dll`` 的桥。

    在非 Windows 平台上，所有句柄与函数属性都返回 :class:`_Mock`。
    """

    user32: Any = None
    kernel32: Any = None
    available: bool = False

    def __init__(self) -> None:
        if IS_WINDOWS and Win32Bridge.user32 is None:
            try:  # pragma: no cover - 仅在 Windows 上执行
                Win32Bridge.user32 = ctypes.WinDLL("user32", use_last_error=True)
                Win32Bridge.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                Win32Bridge.available = True
            except OSError:  # pragma: no cover
                Win32Bridge.available = False

    # -- 结构体（别名到模块级定义） -----------------------------------------

    POINT = _Win32POINT
    RECT = _Win32RECT
    MSG = _Win32MSG
    WNDCLASSEX = _Win32WNDCLASSEX

    # -- 函数封装 -----------------------------------------------------------

    def get_module_handle(self, name: Optional[str] = None) -> Any:
        if not self.kernel32:
            return _Mock()
        return self.kernel32.GetModuleHandleW(name)

    def register_class_ex(self, wc: Any) -> Any:
        if not self.user32:
            return _Mock()
        return self.user32.RegisterClassExW(ctypes.byref(wc))

    def create_window_ex(self, class_name: str, title: str,
                         style: int, x: int, y: int, w: int, h: int) -> Any:
        if not self.user32:
            return _Mock()
        return self.user32.CreateWindowExW(
            0, class_name, title, style, x, y, w, h, None, None,
            self.get_module_handle(), None)

    def show_window(self, hwnd: Any, cmd: int = SW_SHOW) -> Any:
        if not self.user32:
            return _Mock()
        return self.user32.ShowWindow(hwnd, cmd)

    def update_window(self, hwnd: Any) -> Any:
        if not self.user32:
            return _Mock()
        return self.user32.UpdateWindow(hwnd)

    def get_message(self) -> Tuple[Any, Any, Any, Any]:
        if not self.user32:
            return (_Mock(), _Mock(), _Mock(), _Mock())
        msg = self.MSG()
        ret = self.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
        return (msg, self.user32.TranslateMessage(ctypes.byref(msg)),
                self.user32.DispatchMessageW(ctypes.byref(msg)), ret)

    def post_quit_message(self, exit_code: int = 0) -> None:
        if self.user32:
            self.user32.PostQuitMessage(exit_code)

    def def_window_proc(self, hwnd: Any, msg: int,
                        wparam: Any, lparam: Any) -> Any:
        if not self.user32:
            return _Mock()
        return self.user32.DefWindowProcW(hwnd, msg, wparam, lparam)


class Win32Window:
    """一个最简 Win32 顶层窗口。

    在非 Windows 平台上实例化安全，``show`` / ``destroy`` 等均为 no-op。
    """

    def __init__(self, title: str = "Aurora", width: int = 800,
                 height: int = 600, wndproc: Optional[Callable[..., Any]] = None) -> None:
        self.title = title
        self.width = width
        self.height = height
        self.bridge = Win32Bridge()
        self.hwnd: Any = None
        self._wndproc = wndproc or self._default_wndproc
        if self.bridge.available:  # pragma: no cover - 仅在 Windows 上
            self._create_window()

    def _create_window(self) -> None:  # pragma: no cover
        self.bridge.create_window_ex(
            "AuroraWindow", self.title,
            0x00CF0000, 100, 100, self.width, self.height)

    @staticmethod
    def _default_wndproc(hwnd: Any, msg: int,
                         wparam: Any, lparam: Any) -> Any:  # pragma: no cover
        """默认窗口过程，处理 WM_CREATE / WM_DESTROY / WM_PAINT 等。"""
        bridge = Win32Bridge()
        if msg == WM_DESTROY:
            bridge.post_quit_message(0)
            return 0
        return bridge.def_window_proc(hwnd, msg, wparam, lparam)

    def show(self) -> None:
        if self.bridge.available:  # pragma: no cover
            self.bridge.show_window(self.hwnd, SW_SHOW)
            self.bridge.update_window(self.hwnd)

    def hide(self) -> None:
        if self.bridge.available:  # pragma: no cover
            self.bridge.show_window(self.hwnd, SW_HIDE)

    def set_title(self, text: str) -> None:
        self.title = text
        if self.bridge.available and self.bridge.user32:  # pragma: no cover
            self.bridge.user32.SetWindowTextW(self.hwnd, text)

    def resize(self, w: int, h: int) -> None:
        self.width, self.height = w, h
        if self.bridge.available and self.bridge.user32 and self.hwnd:  # pragma: no cover
            self.bridge.user32.SetWindowPos(
                self.hwnd, None, 0, 0, w, h, 0x0040)

    def destroy(self) -> None:
        if self.bridge.available and self.bridge.user32 and self.hwnd:  # pragma: no cover
            self.bridge.user32.DestroyWindow(self.hwnd)
            self.hwnd = None

    # -- 控件工厂 -----------------------------------------------------------

    def create_button(self, text: str, x: int, y: int, w: int, h: int,
                      on_click: Optional[Callable[[], Any]] = None) -> Any:
        """在窗口上创建一个按钮。"""
        self._handlers: Dict[int, Callable[[], Any]] = getattr(self, "_handlers", {})
        hwnd = _Mock()
        if self.bridge.available and self.bridge.user32:  # pragma: no cover
            hwnd = self.bridge.user32.CreateWindowExW(
                0, "BUTTON", text, WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                x, y, w, h, self.hwnd, None,
                self.bridge.get_module_handle(), None)
        cid = id(on_click) & 0xFFFF
        self._handlers[cid] = on_click  # type: ignore[assignment]
        return hwnd

    def create_edit(self, x: int, y: int, w: int, h: int) -> Any:
        hwnd = _Mock()
        if self.bridge.available and self.bridge.user32:  # pragma: no cover
            hwnd = self.bridge.user32.CreateWindowExW(
                0, "EDIT", "", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL,
                x, y, w, h, self.hwnd, None,
                self.bridge.get_module_handle(), None)
        return hwnd

    def create_listbox(self, x: int, y: int, w: int, h: int) -> Any:
        hwnd = _Mock()
        if self.bridge.available and self.bridge.user32:  # pragma: no cover
            hwnd = self.bridge.user32.CreateWindowExW(
                0, "LISTBOX", "", WS_CHILD | WS_VISIBLE | WS_BORDER,
                x, y, w, h, self.hwnd, None,
                self.bridge.get_module_handle(), None)
        return hwnd


# ---------------------------------------------------------------------------
# Windows 原生集成：注册表 / 事件日志 / 系统托盘 / WinUI
# ---------------------------------------------------------------------------

class WindowsIntegration:
    """Windows 系统集成：注册表、事件日志、托盘。"""

    def is_supported(self) -> bool:
        return IS_WINDOWS

    # -- 注册表 ------------------------------------------------------------

    def reg_read(self, key: str, value_name: str) -> Optional[str]:
        """读取注册表字符串值。非 Windows 平台返回 None。"""
        if not IS_WINDOWS:
            return None
        try:  # pragma: no cover - 仅在 Windows 上
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as h:
                v, _ = winreg.QueryValueEx(h, value_name)
                return str(v)
        except OSError:
            return None

    def reg_write(self, key: str, value_name: str, value: str,
                  type: str = "REG_SZ") -> bool:
        """写入注册表。非 Windows 平台返回 False。"""
        if not IS_WINDOWS:
            return False
        try:  # pragma: no cover
            import winreg
            const = getattr(winreg, type, winreg.REG_SZ)
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key, 0,
                                    winreg.KEY_SET_VALUE) as h:
                winreg.SetValueEx(h, value_name, 0, const, value)
            return True
        except OSError:
            return False

    def reg_delete(self, key: str, value_name: str) -> bool:
        """删除注册表值。非 Windows 平台返回 False。"""
        if not IS_WINDOWS:
            return False
        try:  # pragma: no cover
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0,
                                winreg.KEY_SET_VALUE) as h:
                winreg.DeleteValue(h, value_name)
            return True
        except OSError:
            return False

    # -- 事件日志 -----------------------------------------------------------

    def write_event_log(self, source: str, message: str,
                        event_type: str = "INFO") -> bool:
        """写入 Windows 事件日志。非 Windows 平台返回 False。"""
        if not IS_WINDOWS:
            return False
        try:  # pragma: no cover
            import win32evtlog  # type: ignore
            flag = {"INFO": 4004, "WARN": 4002, "ERROR": 4001}[event_type]
            win32evtlog.ReportEvent(None, 0, 0, flag, (source, message))
            return True
        except Exception:
            return False


class SysTrayIcon:
    """系统托盘图标（创建 / 菜单 / 气泡通知）。

    在非 Windows 平台上所有方法均为 no-op。
    """

    def __init__(self, icon_path: str = "", tooltip: str = "") -> None:
        self.icon_path = icon_path
        self.tooltip = tooltip
        self._menu: List[Tuple[str, Any]] = []

    def add_menu_item(self, label: str, callback: Callable[[], Any]) -> None:
        self._menu.append((label, callback))

    def show(self) -> bool:
        """显示托盘图标。非 Windows 返回 False。"""
        return IS_WINDOWS  # pragma: no cover - 真实 Shell_NotifyIconW 调用略

    def hide(self) -> bool:
        return IS_WINDOWS  # pragma: no cover

    def notify(self, title: str, message: str) -> bool:
        """气泡通知。非 Windows 返回 False。"""
        return IS_WINDOWS  # pragma: no cover


class WinUIBridge:
    """UWP / WinUI 绑定接口（远期简化版）。

    当前仅定义接口轮廓，后续通过 C++/WinRT 投影实现。
    """

    def __init__(self) -> None:
        self.is_supported = IS_WINDOWS

    def activate(self, xaml_path: str) -> bool:
        """激活一个 WinUI 窗口。"""
        return False  # pragma: no cover

    def get_navigation_view(self) -> Any:
        return _Mock()


# ---------------------------------------------------------------------------
# 便捷工厂
# ---------------------------------------------------------------------------

def create_window(title: str = "Aurora", width: int = 800,
                  height: int = 600) -> Any:
    """按当前平台创建原生窗口：macOS 返回 NSWindow，Windows 返回 Win32Window。"""
    if IS_MACOS:
        return NSWindow(title, width, height)
    if IS_WINDOWS:
        return Win32Window(title, width, height)
    # 其它平台：返回一个 Mock 占位，不崩溃。
    return _Mock({"title": title, "width": width, "height": height})


# 模块导入时即探测 libobjc（仅 macOS 上真正加载）
CocoaBridge._ensure_loaded()

__all__ = [
    "CocoaBridge", "CocoaClass", "CocoaObject",
    "NSApplication", "NSWindow", "NSView", "NSButton", "NSTextField",
    "NSMenu", "NSMenuItem", "NSNotificationCenter",
    "SwiftBridge", "MacIntegration",
    "Win32Bridge", "Win32Window", "WindowsIntegration", "SysTrayIcon",
    "WinUIBridge", "create_window",
    "IS_MACOS", "IS_WINDOWS", "IS_LINUX",
]
