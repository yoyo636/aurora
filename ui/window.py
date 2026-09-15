"""AuroraUI v3.1.0 — 窗口管理与全局应用对象。

:class:`Window` 是对平台原生窗口的跨平台封装；:class:`Application`
是进程级单例，持有打开的窗口列表、负责启动/退出事件循环。
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional

from .backend import Backend, BackendFactory, WindowHandle
from .events import Event, EventDispatcher


# ---------------------------------------------------------------------------
# Application 单例
# ---------------------------------------------------------------------------

class Application:
    """全局应用对象（单例）。

    用法::

        app = Application.instance()
        app.set_app_name("MyApp")
        win = Window("Hello")
        win.show()
        app.run()
    """

    _instance: Optional["Application"] = None

    def __init__(self, backend: Optional[Backend] = None) -> None:
        self.app_name: str = "Aurora App"
        self.backend: Backend = backend or BackendFactory.get_backend()
        self.open_windows: List["Window"] = []

    # -- 单例 ---------------------------------------------------------------

    @classmethod
    def instance(cls, backend: Optional[Backend] = None) -> "Application":
        if cls._instance is None:
            cls._instance = cls(backend=backend)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """丢弃当前单例（主要用于测试隔离）。"""
        cls._instance = None

    # -- 生命周期 -----------------------------------------------------------

    def set_app_name(self, name: str) -> None:
        self.app_name = name

    def run(self) -> None:
        """进入主事件循环（阻塞）。"""
        self.backend.run_loop()

    def quit(self) -> None:
        """请求退出事件循环并关闭所有窗口。"""
        for win in list(self.open_windows):
            win.close()
        self.backend.quit()


# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------

class Window:
    """跨平台顶层窗口。

    属性可读写：``title / width / height / x / y / visible / resizable /
    modal / always_on_top``。

    事件回调（直接赋值即可）：``on_close / on_resize / on_move /
    on_focus / on_blur``，签名均为 ``callback(window)``。
    """

    def __init__(
        self,
        title: str = "Aurora",
        width: int = 800,
        height: int = 600,
        backend: Optional[Backend] = None,
    ) -> None:
        self._title = title
        self._width = width
        self._height = height
        self._x: int = 100
        self._y: int = 100
        self._visible: bool = False
        self.resizable: bool = True
        self.modal: bool = False
        self.always_on_top: bool = False

        self.backend: Backend = backend or Application.instance().backend
        self.handle: WindowHandle = self.backend.create_window(title, width, height)
        self.content: Any = None
        self.menu_bar: Any = None
        self.status_bar: Any = None

        self.dispatcher = EventDispatcher(self)

        # 用户可直接赋值的事件回调
        self.on_close: Optional[Callable[["Window"], Any]] = None
        self.on_resize: Optional[Callable[["Window"], Any]] = None
        self.on_move: Optional[Callable[["Window"], Any]] = None
        self.on_focus: Optional[Callable[["Window"], Any]] = None
        self.on_blur: Optional[Callable[["Window"], Any]] = None

        Application.instance().open_windows.append(self)

    # -- 属性 ---------------------------------------------------------------

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self.set_title(value)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def visible(self) -> bool:
        return self._visible

    # -- 几何操作 -----------------------------------------------------------

    def show(self) -> None:
        self.backend.show_window(self.handle)
        self._visible = True

    def hide(self) -> None:
        self.backend.hide_window(self.handle)
        self._visible = False

    def close(self) -> None:
        if self.on_close is not None:
            self.on_close(self)
        self.backend.destroy_window(self.handle)
        if self in Application.instance().open_windows:
            Application.instance().open_windows.remove(self)

    def resize(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self.handle.width = width
        self.handle.height = height
        if self.on_resize is not None:
            self.on_resize(self)

    def move(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        if self.on_move is not None:
            self.on_move(self)

    def set_title(self, title: str) -> None:
        self._title = title
        self.handle.title = title

    # -- 内容/菜单/状态栏 ---------------------------------------------------

    def set_content(self, widget: Any) -> None:
        """设置窗口根控件或布局。"""
        self.content = widget
        if widget is not None and hasattr(widget, "create"):
            widget.create(self.backend, self.handle)

    def set_menu_bar(self, menu: Any) -> None:
        self.menu_bar = menu

    def set_status_bar(self, status_bar: Any) -> None:
        self.status_bar = status_bar

    # -- 事件 ---------------------------------------------------------------

    def dispatch(self, event: Event) -> Event:
        """从窗口开始分发事件。"""
        event.target = self
        return self.dispatcher.dispatch(event)


__all__ = ["Application", "Window"]
