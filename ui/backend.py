"""AuroraUI v3.1.0 — 抽象后端接口层。

所有平台后端（Cocoa / Win32 / GTK / Web）必须实现 :class:`Backend` 抽象基类，
上层窗口与控件代码只依赖这层抽象，从而实现"一次编写、跨平台运行"。

设计要点：

* :class:`WindowHandle` / :class:`ControlHandle` 是对平台原生句柄的薄封装，
  后端实现里可以塞入 NSWindow* / HWND / GtkWidget* / DOM Element 等任意对象；
* :class:`BackendFactory` 根据当前操作系统自动挑选可用后端；
  在无显示环境（如 CI、无头测试）下自动降级到 :class:`MockBackend`，绝不抛错。
"""

from __future__ import annotations

import platform
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# 句柄封装
# ---------------------------------------------------------------------------

@dataclass
class WindowHandle:
    """封装一个平台原生窗口句柄。

    属性:
        native: 平台原生窗口对象/指针（NSWindow / HWND / GtkWindow / 等）。
        title:  窗口标题（缓存，便于 Mock 后端查询）。
        width:  窗口宽度（缓存）。
        height: 窗口高度（缓存）。
        visible: 是否可见。
        meta:   扩展元数据字典。
    """

    native: Any = None
    title: str = ""
    width: int = 800
    height: int = 600
    visible: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ControlHandle:
    """封装一个平台原生控件句柄。"""

    native: Any = None
    control_type: str = ""
    parent: Optional["ControlHandle"] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    event_handlers: Dict[str, List[Callable[..., Any]]] = field(default_factory=dict)
    children: List["ControlHandle"] = field(default_factory=list)
    visible: bool = True
    enabled: bool = True


# ---------------------------------------------------------------------------
# 抽象后端
# ---------------------------------------------------------------------------

class Backend(ABC):
    """所有平台后端必须实现的抽象接口。

    生命周期::

        backend = BackendFactory.get_backend()
        win = backend.create_window("Hello", 800, 600)
        btn = backend.create_control(win, "button", text="OK")
        backend.connect_event(btn, "clicked", on_click)
        backend.show_window(win)
        backend.run_loop()
    """

    #: 后端名称，子类覆盖
    name: str = "abstract"

    # -- 窗口 ---------------------------------------------------------------

    @abstractmethod
    def create_window(self, title: str, width: int, height: int) -> WindowHandle:
        """创建一个新窗口并返回句柄。"""

    @abstractmethod
    def destroy_window(self, handle: WindowHandle) -> None:
        """销毁窗口。"""

    @abstractmethod
    def show_window(self, handle: WindowHandle) -> None:
        """显示窗口。"""

    @abstractmethod
    def hide_window(self, handle: WindowHandle) -> None:
        """隐藏窗口。"""

    # -- 控件 ---------------------------------------------------------------

    @abstractmethod
    def create_control(
        self, parent: Any, control_type: str, **kwargs: Any
    ) -> ControlHandle:
        """在 *parent* 下创建指定类型的控件。

        *parent* 可以是 :class:`WindowHandle` 或 :class:`ControlHandle`。
        """

    @abstractmethod
    def set_control_property(self, handle: ControlHandle, prop: str, value: Any) -> None:
        """设置控件属性（text / enabled / visible / 等）。"""

    @abstractmethod
    def get_control_property(self, handle: ControlHandle, prop: str) -> Any:
        """读取控件属性。"""

    @abstractmethod
    def connect_event(
        self, handle: ControlHandle, event_name: str, callback: Callable[..., Any]
    ) -> None:
        """把事件 *event_name* 连接到 *callback*。"""

    # -- 主循环 -------------------------------------------------------------

    @abstractmethod
    def run_loop(self) -> None:
        """进入事件循环（阻塞）。"""

    @abstractmethod
    def quit(self) -> None:
        """退出事件循环。"""

    # -- 平台信息 -----------------------------------------------------------

    def get_platform(self) -> str:
        """返回后端标识字符串，如 ``"cocoa"`` / ``"win32"`` / ``"gtk"`` / ``"web"``。"""
        return self.name

    # -- 可选的扩展 ---------------------------------------------------------

    def request_quit(self, handle: WindowHandle) -> bool:
        """窗口关闭前的钩子，返回 ``False`` 阻止关闭。默认允许。"""
        return True


# ---------------------------------------------------------------------------
# Mock 后端（测试 / 无头环境 / 平台不可用时降级）
# ---------------------------------------------------------------------------

class MockBackend(Backend):
    """纯内存后端：不创建任何原生窗口，全部状态保存在 Python 对象里。

    主要用途：

    * 单元测试（无需显示环境）；
    * 在不支持图形的平台/CI 上优雅降级，保证 UI 框架代码仍可导入与运行。
    """

    name = "mock"

    def __init__(self) -> None:
        self.windows: List[WindowHandle] = []
        self.controls: List[ControlHandle] = []
        self.running: bool = False
        self.quit_requested: bool = False
        #: 录制所有被调用的方法，便于测试断言
        self.call_log: List[str] = []

    # -- 窗口 ---------------------------------------------------------------

    def create_window(self, title: str, width: int, height: int) -> WindowHandle:
        self.call_log.append(f"create_window({title!r},{width},{height})")
        handle = WindowHandle(
            native=f"<mock-window-{len(self.windows)}>",
            title=title,
            width=width,
            height=height,
        )
        self.windows.append(handle)
        return handle

    def destroy_window(self, handle: WindowHandle) -> None:
        self.call_log.append("destroy_window")
        if handle in self.windows:
            self.windows.remove(handle)

    def show_window(self, handle: WindowHandle) -> None:
        self.call_log.append("show_window")
        handle.visible = True

    def hide_window(self, handle: WindowHandle) -> None:
        self.call_log.append("hide_window")
        handle.visible = False

    # -- 控件 ---------------------------------------------------------------

    def create_control(
        self, parent: Any, control_type: str, **kwargs: Any
    ) -> ControlHandle:
        self.call_log.append(f"create_control({control_type!r})")
        parent_handle: Optional[ControlHandle] = None
        if isinstance(parent, ControlHandle):
            parent_handle = parent
        handle = ControlHandle(
            native=f"<mock-{control_type}-{len(self.controls)}>",
            control_type=control_type,
            parent=parent_handle,
            properties=dict(kwargs),
        )
        if parent_handle is not None:
            parent_handle.children.append(handle)
        self.controls.append(handle)
        return handle

    def set_control_property(self, handle: ControlHandle, prop: str, value: Any) -> None:
        handle.properties[prop] = value
        if prop == "visible":
            handle.visible = bool(value)
        elif prop == "enabled":
            handle.enabled = bool(value)

    def get_control_property(self, handle: ControlHandle, prop: str) -> Any:
        return handle.properties.get(prop)

    def connect_event(
        self, handle: ControlHandle, event_name: str, callback: Callable[..., Any]
    ) -> None:
        handle.event_handlers.setdefault(event_name, []).append(callback)

    # -- 主循环 -------------------------------------------------------------

    def run_loop(self) -> None:
        """Mock 主循环：默认只跑一次空转，便于测试不阻塞。

        若需要真实阻塞行为，可在子类中覆盖。
        """
        self.call_log.append("run_loop")
        self.running = True
        self.quit_requested = False
        # 立即返回 —— 测试里我们手动分发事件。
        self.running = False

    def quit(self) -> None:
        self.call_log.append("quit")
        self.quit_requested = True
        self.running = False

    # -- 测试辅助 -----------------------------------------------------------

    def simulate_click(self, handle: ControlHandle) -> List[Any]:
        """同步触发控件上所有 ``clicked`` / ``on_click`` 处理器，返回返回值列表。"""
        results: List[Any] = []
        for evt_name in ("clicked", "on_click", "action"):
            for cb in handle.event_handlers.get(evt_name, []):
                results.append(cb(handle))
        return results


# ---------------------------------------------------------------------------
# 后端工厂
# ---------------------------------------------------------------------------

class BackendFactory:
    """根据平台自动选择合适的 :class:`Backend`。

    用法::

        backend = BackendFactory.get_backend()              # 自动检测
        backend = BackendFactory.get_backend("cocoa")       # 强制指定
        backend = BackendFactory.get_backend("mock")        # 强制 Mock
    """

    _registry: Dict[str, Callable[[], Optional[Backend]]] = {}
    _cache: Dict[str, Backend] = {}

    @classmethod
    def register(
        cls, name: str, factory: Callable[[], Optional[Backend]]
    ) -> None:
        """注册一个后端工厂函数。

        *factory* 应当在后端不可用时返回 ``None``。
        """
        cls._registry[name] = factory
        cls._cache.pop(name, None)

    @classmethod
    def detect_platform(cls) -> str:
        """根据当前操作系统返回推荐后端名称。"""
        system = platform.system().lower()
        if system == "darwin":
            return "cocoa"
        if system == "windows":
            return "win32"
        if system == "linux":
            return "gtk"
        return "mock"

    @classmethod
    def get_backend(cls, platform_name: Optional[str] = None) -> Backend:
        """获取一个可用的后端实例（带缓存）。

        解析顺序：

        1. 显式传入 *platform_name*（``"mock"`` 直接返回 Mock）；
        2. 自动检测当前平台；
        3. 该后端不可用时降级到 :class:`MockBackend`。
        """
        if platform_name == "mock":
            return cls._cached("mock", lambda: MockBackend())

        if platform_name is None:
            platform_name = cls.detect_platform()

        # 懒加载内置后端，避免导入失败影响整个包。
        cls._ensure_builtins_registered()

        factory = cls._registry.get(platform_name)
        if factory is not None:
            try:
                instance = factory()
            except Exception:
                instance = None
            if instance is not None:
                return cls._cache.setdefault(platform_name, instance)

        # 降级到 Mock
        return cls._cached("mock", lambda: MockBackend())

    # -- 内部 ---------------------------------------------------------------

    @classmethod
    def _cached(cls, name: str, make: Callable[[], Backend]) -> Backend:
        if name not in cls._cache:
            cls._cache[name] = make()
        return cls._cache[name]

    @classmethod
    def _ensure_builtins_registered(cls) -> None:
        if cls._registry:
            return
        try:
            from .backends import (  # noqa: WPS433  延迟导入
                register_builtin_backends,
            )

            register_builtin_backends(cls)
        except Exception:
            # 后端注册失败绝不影响框架核心 —— 用 Mock 兜底。
            pass


__all__ = [
    "Backend",
    "BackendFactory",
    "ControlHandle",
    "MockBackend",
    "WindowHandle",
]
