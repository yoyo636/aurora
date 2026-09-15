"""AuroraUI v3.1.0 — 事件处理系统。

提供：

* :class:`Event` 基类及常用子事件（鼠标 / 键盘 / 控件动作 / 文本 / 变更 / 拖拽 / 绘制）；
* :class:`EventDispatcher` —— 支持事件冒泡（bubble）与捕获（capture）两阶段分发；
* :func:`on` 装饰器，用于在自定义控件类中声明式注册事件处理器。

事件分发模型遵循浏览器 DOM 的简化版：

::

    捕获阶段 (root -> target)  ->  目标阶段  ->  冒泡阶段 (target -> root)

调用 ``event.stop_propagation()`` 可在任意阶段终止后续分发。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Type


# ---------------------------------------------------------------------------
# 事件对象
# ---------------------------------------------------------------------------

@dataclass
class Event:
    """所有 UI 事件的基类。

    属性:
        type: 事件类型字符串，如 ``"click"`` / ``"key_down"``。
        target: 事件最初派发的控件（可能是 ``Window`` / ``Widget`` 等）。
        timestamp: 事件创建时间（epoch 秒）。
        propagation_stopped: 是否已经调用 ``stop_propagation()``。
        default_prevented: 是否阻止了默认行为。
    """

    type: str = "event"
    target: Any = None
    timestamp: float = field(default_factory=time.time)
    propagation_stopped: bool = False
    default_prevented: bool = False

    def stop_propagation(self) -> None:
        """阻止事件继续在捕获/冒泡链上传播。"""
        self.propagation_stopped = True

    def prevent_default(self) -> None:
        """通知后端不要执行该事件的默认处理逻辑。"""
        self.default_prevented = True


@dataclass
class MouseEvent(Event):
    """鼠标事件（移动 / 按下 / 释放 / 滚轮 / 进入 / 离开）。"""

    type: str = "mouse"
    x: float = 0.0
    y: float = 0.0
    button: int = 0          # 0=无 1=左键 2=右键 3=中键
    buttons: int = 0         # 位掩码：当前按下的所有按钮
    modifiers: int = 0       # 位掩码：shift/ctrl/alt/meta
    wheel_delta: float = 0.0


@dataclass
class KeyEvent(Event):
    """键盘事件（按下 / 释放 / 字符输入）。"""

    type: str = "key"
    key: str = ""            # 语义键名："Enter" / "Escape" / "a"
    code: str = ""            # 物理键码："KeyA" / "Enter"
    modifiers: int = 0
    text: str = ""            # 输入产生的实际字符（可打印字符时）


@dataclass
class ActionEvent(Event):
    """控件动作事件（按钮点击、菜单项触发、列表选中变化等）。"""

    type: str = "action"
    action: str = "clicked"
    value: Any = None


@dataclass
class TextEvent(Event):
    """文本编辑事件（输入框内容变化 / 提交）。"""

    type: str = "text"
    text: str = ""


@dataclass
class ChangeEvent(Event):
    """通用变更事件（复选框、滑块、单选等数值/状态变化）。"""

    type: str = "change"
    old_value: Any = None
    new_value: Any = None


@dataclass
class DragEvent(Event):
    """拖拽事件。"""

    type: str = "drag"
    x: float = 0.0
    y: float = 0.0
    mime_data: Dict[str, str] = field(default_factory=dict)
    drop_allowed: bool = True


@dataclass
class PaintEvent(Event):
    """重绘事件（Canvas / 自定义绘制控件使用）。"""

    type: str = "paint"
    context: Any = None       # GraphicsContext
    width: int = 0
    height: int = 0


# 修饰键位掩码常量
MOD_NONE = 0
MOD_SHIFT = 1 << 0
MOD_CTRL = 1 << 1
MOD_ALT = 1 << 2
MOD_META = 1 << 3


# ---------------------------------------------------------------------------
# 事件分发器
# ---------------------------------------------------------------------------

HandlerList = List[Tuple[int, Callable[..., Any]]]  # (优先级, 回调)


class EventDispatcher:
    """在一棵控件树上注册并分发事件。

    每个可派发事件的对象持有一个 ``EventDispatcher``，树上的祖先通过
    :meth:`attach_parent` / :meth:`detach_parent` 构成冒泡链。

    阶段说明：

    * ``capture=True`` 的处理器先在从根到目标的路上执行；
    * 目标自身的处理器随后执行；
    * ``capture=False`` 的处理器最后在从目标到根的回路上执行（冒泡）。
    """

    def __init__(self, owner: Any) -> None:
        self.owner = owner
        self._handlers: Dict[str, HandlerList] = {}
        self._parent: Optional[EventDispatcher] = None

    # -- 注册 ---------------------------------------------------------------

    def on(
        self,
        event_type: str,
        callback: Callable[..., Any],
        priority: int = 0,
        capture: bool = False,
    ) -> Callable[[], None]:
        """注册事件处理器，返回一个可调用的反注册函数。"""
        bucket = self._handlers.setdefault(event_type, [])
        entry = (priority, capture, callback)  # type: ignore[misc]
        bucket.append(entry)  # type: ignore[arg-type]
        bucket.sort(key=lambda item: item[0], reverse=True)

        def _off() -> None:
            if entry in bucket:
                bucket.remove(entry)

        return _off

    # -- 树结构 -------------------------------------------------------------

    def attach_parent(self, parent: "EventDispatcher") -> None:
        """把本 dispatcher 挂到父节点之下（用于冒泡链）。"""
        self._parent = parent

    def detach_parent(self) -> None:
        self._parent = None

    def _ancestors(self) -> List["EventDispatcher"]:
        chain: List[EventDispatcher] = []
        node = self._parent
        seen = set()
        while node is not None and id(node) not in seen:
            chain.append(node)
            seen.add(id(node))
            node = node._parent
        return chain

    # -- 分发 ---------------------------------------------------------------

    def dispatch(self, event: Event) -> Event:
        """把事件按 捕获 → 目标 → 冒泡 三个阶段分发出去。"""
        if event.target is None:
            event.target = self.owner

        ancestors = self._ancestors()  # 从父到根
        capture_chain = list(reversed(ancestors))  # 根到父

        # 1) 捕获阶段：只调用 capture=True 的处理器
        for dispatcher in capture_chain:
            if event.propagation_stopped:
                return event
            dispatcher._invoke(event, capture=True)

        # 2) 目标阶段：无论 capture 标志都调用目标上的处理器
        if not event.propagation_stopped:
            self._invoke(event, capture=None)

        # 3) 冒泡阶段：只调用 capture=False 的处理器
        for dispatcher in ancestors:
            if event.propagation_stopped:
                return event
            dispatcher._invoke(event, capture=False)

        return event

    # -- 内部 ---------------------------------------------------------------

    def _invoke(self, event: Event, capture: Optional[bool]) -> None:
        handlers = self._handlers.get(event.type, [])
        for priority, is_capture, callback in handlers:
            if capture is not None and bool(is_capture) != capture:
                continue
            if event.propagation_stopped:
                return
            try:
                callback(event)
            except Exception:
                # 单个处理器异常不应中断整个事件循环
                continue


# ---------------------------------------------------------------------------
# @on 装饰器（用于类方法声明式注册）
# ---------------------------------------------------------------------------

#: 类上收集到的所有事件处理器元信息的属性名
_ON_REGISTRY_ATTR = "_aurora_ui_event_handlers_"


def on(event_type: str, priority: int = 0, capture: bool = False) -> Callable:
    """把一个方法标记为 *event_type* 事件的处理器。

    用法::

        class MyWidget(Widget):
            @on("click")
            def handle_click(self, event):
                print("clicked at", event.x, event.y)

    控件基类在实例化时通过 :func:`install_event_handlers` 把这些方法
    绑定到自身的 :class:`EventDispatcher` 上。
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        registry: List[Dict[str, Any]] = getattr(func, _ON_REGISTRY_ATTR, [])
        registry.append(
            {"event_type": event_type, "priority": priority, "capture": capture}
        )
        setattr(func, _ON_REGISTRY_ATTR, registry)
        return func

    return decorator


def install_event_handlers(instance: Any, dispatcher: EventDispatcher) -> None:
    """扫描 *instance* 上所有被 ``@on`` 装饰的方法并注册到 *dispatcher*。"""
    seen: set = set()
    for cls in type(instance).__mro__:
        for attr_name, value in vars(cls).items():
            if attr_name in seen:
                continue
            seen.add(attr_name)
            meta_list = getattr(value, _ON_REGISTRY_ATTR, None)
            if not meta_list:
                continue
            bound = getattr(instance, attr_name)
            for meta in meta_list:
                dispatcher.on(
                    meta["event_type"],
                    bound,
                    priority=meta["priority"],
                    capture=meta["capture"],
                )


__all__ = [
    "ActionEvent",
    "ChangeEvent",
    "DragEvent",
    "Event",
    "EventDispatcher",
    "KeyEvent",
    "MOD_ALT",
    "MOD_CTRL",
    "MOD_META",
    "MOD_NONE",
    "MOD_SHIFT",
    "MouseEvent",
    "PaintEvent",
    "TextEvent",
    "install_event_handlers",
    "on",
]
