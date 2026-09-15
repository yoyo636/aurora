"""AuroraUI v3.1.0 — 平台后端包。

通过 :func:`register_builtin_backends` 把所有内置后端注册到
:class:`~aurora.ui.backend.BackendFactory`。每个后端都有 ``is_available()``
检测自己能否在当前环境加载；不可用时工厂函数返回 ``None``，工厂
会自动降级到 Mock 后端。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..backend import BackendFactory


def register_builtin_backends(factory: "BackendFactory") -> None:
    """把 cocoa / win32 / gtk / web 四个后端注册到 *factory*。"""
    from .cocoa import CocoaBackend
    from .gtk import GtkBackend
    from .web import WebBackend
    from .win32 import Win32Backend

    factory.register("cocoa", _lazy(CocoaBackend))
    factory.register("win32", _lazy(Win32Backend))
    factory.register("gtk", _lazy(GtkBackend))
    factory.register("web", _lazy(WebBackend))


def _lazy(backend_cls):
    """包装一个后端类：不可用时返回 ``None`` 而不是抛错。"""

    def loader():
        try:
            if not backend_cls.is_available():
                return None
            return backend_cls()
        except Exception:
            return None

    return loader


__all__ = ["register_builtin_backends"]
