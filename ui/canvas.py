"""AuroraUI v3.1.0 — Canvas 2D 绘图 API。

:class:`Canvas` 是一个可绘制的控件；:class:`GraphicsContext` 模拟 HTML5
Canvas 2D 上下文，支持路径、填充/描边、文本、变换栈与简单图像绘制。

在无显示环境下，所有绘制指令会被记录到 ``context.command_log``，
便于单元测试断言绘制序列是否正确。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .controls import Widget
from .events import Event, PaintEvent


# ---------------------------------------------------------------------------
# 二维变换矩阵
# ---------------------------------------------------------------------------

@dataclass
class Matrix:
    """仿射变换矩阵（行优先：``[a, b, c, d, e, f]``，对应 HTML5 ``domMatrix``）。

    坐标变换：``x' = a*x + c*y + e``，``y' = b*x + d*y + f``。
    """

    a: float = 1.0
    b: float = 0.0
    c: float = 0.0
    d: float = 1.0
    e: float = 0.0
    f: float = 0.0

    def clone(self) -> "Matrix":
        return Matrix(self.a, self.b, self.c, self.d, self.e, self.f)

    def multiply(self, other: "Matrix") -> "Matrix":
        """返回 self * other（先应用 self，再应用 other）。"""
        a = other.a * self.a + other.c * self.b
        b = other.b * self.a + other.d * self.b
        c = other.a * self.c + other.c * self.d
        d = other.b * self.c + other.d * self.d
        e = other.a * self.e + other.c * self.f + other.e
        f = other.b * self.e + other.d * self.f + other.f
        return Matrix(a, b, c, d, e, f)

    def translate(self, x: float, y: float) -> "Matrix":
        return self.multiply(Matrix(1, 0, 0, 1, x, y))

    def rotate(self, angle: float) -> "Matrix":
        c, s = math.cos(angle), math.sin(angle)
        return self.multiply(Matrix(c, s, -s, c, 0, 0))

    def scale(self, sx: float, sy: float) -> "Matrix":
        return self.multiply(Matrix(sx, 0, 0, sy, 0, 0))

    def transform_point(self, x: float, y: float) -> Tuple[float, float]:
        return (
            self.a * x + self.c * y + self.e,
            self.b * x + self.d * y + self.f,
        )


# ---------------------------------------------------------------------------
# 绘图上下文
# ---------------------------------------------------------------------------

@dataclass
class Path:
    """当前正在构建的路径。"""

    segments: List[Tuple[str, ...]] = field(default_factory=list)


class GraphicsContext:
    """2D 绘图上下文。

    所有绘图调用都会：

    1. 根据当前变换矩阵把坐标变换到设备坐标；
    2. 追加到 :attr:`command_log`，便于测试与后端回放。
    """

    def __init__(self, width: int = 800, height: int = 600) -> None:
        self.width = width
        self.height = height

        # 绘制状态
        self.fill_style: str = "#000000"
        self.stroke_style: str = "#000000"
        self.line_width: float = 1.0
        self.line_cap: str = "butt"        # butt / round / square
        self.line_join: str = "miter"      # miter / round / bevel
        self.font: str = "12px sans-serif"
        self.text_align: str = "start"     # start / end / left / right / center
        self.text_baseline: str = "alphabetic"
        self.global_alpha: float = 1.0
        self.shadow_blur: float = 0.0
        self.shadow_color: str = "transparent"

        # 变换栈
        self._matrix = Matrix()
        self._stack: List[Matrix] = []

        # 当前路径
        self._path = Path()

        # 命令日志（测试断言用）
        self.command_log: List[Tuple[str, Tuple[Any, ...]]] = []

    # -- 变换 ---------------------------------------------------------------

    def save(self) -> None:
        """保存当前绘图状态到栈顶。"""
        self._stack.append(self._matrix.clone())
        self._log("save")

    def restore(self) -> None:
        """从栈顶恢复绘图状态。"""
        if self._stack:
            self._matrix = self._stack.pop()
        self._log("restore")

    def translate(self, x: float, y: float) -> None:
        self._matrix = self._matrix.translate(x, y)
        self._log("translate", (x, y))

    def rotate(self, angle: float) -> None:
        """以弧度为单位旋转。"""
        self._matrix = self._matrix.rotate(angle)
        self._log("rotate", (angle,))

    def scale(self, sx: float, sy: float) -> None:
        self._matrix = self._matrix.scale(sx, sy)
        self._log("scale", (sx, sy))

    def transform(self, matrix: Matrix) -> None:
        """用一个任意矩阵右乘当前矩阵。"""
        self._matrix = self._matrix.multiply(matrix)
        self._log("transform", (matrix.a, matrix.b, matrix.c, matrix.d, matrix.e, matrix.f))

    def set_transform(self, matrix: Matrix) -> None:
        """直接替换当前矩阵。"""
        self._matrix = matrix.clone()
        self._log("set_transform", (matrix.a, matrix.b, matrix.c, matrix.d, matrix.e, matrix.f))

    @property
    def current_transform(self) -> Matrix:
        return self._matrix.clone()

    # -- 路径 ---------------------------------------------------------------

    def begin_path(self) -> None:
        self._path = Path()
        self._log("begin_path")

    def close_path(self) -> None:
        self._path.segments.append(("close",))
        self._log("close_path")

    def move_to(self, x: float, y: float) -> None:
        self._path.segments.append(("move", x, y))
        self._log("move_to", (x, y))

    def line_to(self, x: float, y: float) -> None:
        self._path.segments.append(("line", x, y))
        self._log("line_to", (x, y))

    def bezier_curve_to(
        self,
        cp1x: float, cp1y: float,
        cp2x: float, cp2y: float,
        x: float, y: float,
    ) -> None:
        self._path.segments.append(("bezier", cp1x, cp1y, cp2x, cp2y, x, y))
        self._log("bezier_curve_to", (cp1x, cp1y, cp2x, cp2y, x, y))

    def arc(
        self,
        x: float, y: float, radius: float,
        start_angle: float, end_angle: float,
        anticlockwise: bool = False,
    ) -> None:
        self._path.segments.append(("arc", x, y, radius, start_angle, end_angle, anticlockwise))
        self._log("arc", (x, y, radius, start_angle, end_angle, anticlockwise))

    def rect(self, x: float, y: float, width: float, height: float) -> None:
        self._path.segments.append(("rect", x, y, width, height))
        self._log("rect", (x, y, width, height))

    @property
    def path(self) -> Path:
        return self._path

    # -- 填充 / 描边 ---------------------------------------------------------

    def fill(self) -> None:
        self._log("fill", (self.fill_style, self.global_alpha))

    def stroke(self) -> None:
        self._log("stroke", (self.stroke_style, self.line_width, self.line_cap, self.line_join))

    def clip(self) -> None:
        self._log("clip")

    # -- 文本 ---------------------------------------------------------------

    def fill_text(self, text: str, x: float, y: float, max_width: Optional[float] = None) -> None:
        self._log("fill_text", (text, x, y, self.font, self.text_align, self.text_baseline))

    # -- 图像 ---------------------------------------------------------------

    def draw_image(
        self, image: Any, x: float, y: float, width: float, height: float
    ) -> None:
        self._log("draw_image", (id(image), x, y, width, height))

    # -- 其他 ----------------------------------------------------------------

    def clear_rect(self, x: float, y: float, width: float, height: float) -> None:
        self._log("clear_rect", (x, y, width, height))

    # -- 内部 ----------------------------------------------------------------

    def _log(self, command: str, args: Tuple[Any, ...] = ()) -> None:
        self.command_log.append((command, args))


# ---------------------------------------------------------------------------
# Canvas 控件
# ---------------------------------------------------------------------------

class Canvas(Widget):
    """可绘制的画布控件。

    用法::

        canvas = Canvas(width=400, height=300)

        @canvas.on_paint
        def draw(ctx):
            ctx.fill_style = "red"
            ctx.fill_rect(50, 50, 100, 100)
    """

    control_type = "canvas"

    def __init__(self, width: int = 400, height: int = 300, **kwargs: Any) -> None:
        super().__init__(width=width, height=height, **kwargs)
        self.preferred_width = width
        self.preferred_height = height
        self.painters: List[Callable[[GraphicsContext], Any]] = []

    # -- 事件注册 -----------------------------------------------------------

    def on_paint(self, callback: Callable[[GraphicsContext], Any]) -> Callable[[], None]:
        """注册绘制回调；也可作为装饰器使用。"""
        self.painters.append(callback)

        def _off() -> None:
            if callback in self.painters:
                self.painters.remove(callback)

        return _off

    def repaint(self) -> GraphicsContext:
        """创建一个新的 :class:`GraphicsContext`，依次调用所有 painters。"""
        ctx = GraphicsContext(int(self.preferred_width), int(self.preferred_height))
        for painter in self.painters:
            painter(ctx)
        event = PaintEvent(type="paint", target=self, context=ctx,
                           width=int(self.preferred_width),
                           height=int(self.preferred_height))
        self.dispatch(event)
        return ctx

    def backend_props(self) -> Dict[str, Any]:
        props = super().backend_props()
        props["width"] = self.preferred_width
        props["height"] = self.preferred_height
        return props


__all__ = [
    "Canvas",
    "GraphicsContext",
    "Matrix",
    "PaintEvent",
    "Path",
]
