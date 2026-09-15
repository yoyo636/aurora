"""AuroraUI v3.1.0 — 布局系统。

布局负责在给定的可用矩形区域内，计算每个子控件的位置和尺寸。

提供：

* :class:`LayoutParams` —— 每个子控件在布局中的拉伸/对齐/最小最大尺寸；
* :class:`Layout` 抽象基类；
* 五种内置布局：:class:`VBox` / :class:`HBox` / :class:`Grid` /
  :class:`Stack` / :class:`Anchor`。

布局只操作控件上的 ``bounds`` 属性（``x, y, width, height``），
不关心后端如何真正放置控件 —— 这让布局逻辑可以在无显示环境下完整测试。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# 布局参数
# ---------------------------------------------------------------------------

#: 对齐方式
ALIGN_START = "start"
ALIGN_CENTER = "center"
ALIGN_END = "end"
ALIGN_STRETCH = "stretch"


@dataclass
class LayoutParams:
    """单个子控件在父布局中的参数。

    属性:
        stretch: 拉伸因子。大于 0 时按比例瓜分多余空间；0 表示使用自然尺寸。
        alignment: 交叉轴对齐方式（当控件未被拉伸时生效）。
        min_width / min_height: 最小尺寸。
        max_width / max_height: 最大尺寸。
        margin: 四周外边距 (top, right, bottom, left)。
        row / col: Grid 布局中的格子位置。
        col_span / row_span: Grid 中跨格数。
    """

    stretch: int = 0
    alignment: str = ALIGN_STRETCH
    min_width: int = 0
    min_height: int = 0
    max_width: int = 0       # 0 表示不限
    max_height: int = 0
    margin: Tuple[int, int, int, int] = (0, 0, 0, 0)
    row: int = 0
    col: int = 0
    row_span: int = 1
    col_span: int = 1

    def clamped_size(self, width: float, height: float) -> Tuple[float, float]:
        """根据 min/max 约束夹紧给定尺寸。"""
        w = max(self.min_width, width)
        h = max(self.min_height, height)
        if self.max_width:
            w = min(w, self.max_width)
        if self.max_height:
            h = min(h, self.max_height)
        return w, h


# ---------------------------------------------------------------------------
# 布局基类
# ---------------------------------------------------------------------------

class Layout:
    """所有布局的基类。

    子类实现 :meth:`layout`，在给定容器与可用尺寸后，
    直接设置每个子控件的 ``bounds`` = ``(x, y, w, h)``。
    """

    def __init__(self) -> None:
        self.children: List[Any] = []
        self.params: Dict[int, LayoutParams] = {}

    # -- 增删 ----------------------------------------------------------------

    def add(self, widget: Any, **params: Any) -> LayoutParams:
        """把 *widget* 加入布局，返回其 :class:`LayoutParams`。"""
        lp = LayoutParams(**params)
        self.children.append(widget)
        self.params[id(widget)] = lp
        widget.layout_params = lp  # type: ignore[attr-defined]
        return lp

    def remove(self, widget: Any) -> None:
        if widget in self.children:
            self.children.remove(widget)
        self.params.pop(id(widget), None)

    def clear(self) -> None:
        self.children.clear()
        self.params.clear()

    def update(self) -> None:
        """标记布局需要重新计算（默认空实现，子类可覆盖）。"""

    # -- 测量与布局 ----------------------------------------------------------

    def measure(
        self, available_width: float, available_height: float
    ) -> Tuple[float, float]:
        """估算布局在给定可用空间下的"自然"尺寸。默认返回可用空间本身。"""
        return available_width, available_height

    def layout(
        self, container: Any, available_width: float, available_height: float
    ) -> None:
        """在 *available_width* x *available_height* 区域内布置所有子控件。

        默认实现：所有可见子控件占满整个区域。子类应覆盖。
        """
        for child in self.children:
            if not getattr(child, "visible", True):
                continue
            set_bounds(child, 0, 0, available_width, available_height)

    # -- 工具 ----------------------------------------------------------------

    def _lp(self, widget: Any) -> LayoutParams:
        return self.params.get(id(widget), LayoutParams())


def set_bounds(widget: Any, x: float, y: float, width: float, height: float) -> None:
    """统一设置控件的矩形区域。"""
    widget.bounds = (x, y, width, height)  # type: ignore[attr-defined]


def natural_size(widget: Any) -> Tuple[float, float]:
    """读取控件的自然尺寸；没有时给一个合理默认值。"""
    w = getattr(widget, "preferred_width", None)
    h = getattr(widget, "preferred_height", None)
    if w is None:
        w = getattr(widget, "width", 80)
    if h is None:
        h = getattr(widget, "height", 24)
    return float(w), float(h)


# ---------------------------------------------------------------------------
# VBox / HBox
# ---------------------------------------------------------------------------

class Box(Layout):
    """垂直/水平盒子布局的公共实现。"""

    #: True 表示主轴为竖直方向（VBox）；False 表示水平（HBox）
    vertical: bool = True

    def __init__(self, spacing: int = 0, padding: int = 0, alignment: str = ALIGN_START):
        super().__init__()
        self.spacing = spacing
        self.padding = padding
        self.alignment = alignment

    def layout(self, container: Any, available_width: float, available_height: float) -> None:
        pad = self.padding
        inner_w = max(0.0, available_width - 2 * pad)
        inner_h = max(0.0, available_height - 2 * pad)

        visible = [c for c in self.children if getattr(c, "visible", True)]
        if not visible:
            return

        # 主轴方向上：先分配自然尺寸，剩余空间按 stretch 瓜分
        if self.vertical:
            main_total = inner_h
            cross_total = inner_w
        else:
            main_total = inner_w
            cross_total = inner_h

        gaps = self.spacing * (len(visible) - 1)
        fixed_main = 0.0
        stretch_sum = 0
        natural: Dict[int, float] = {}
        for child in visible:
            lp = self._lp(child)
            nw, nh = natural_size(child)
            main_natural = nh if self.vertical else nw
            main_natural = max(lp.min_height if self.vertical else lp.min_width, main_natural)
            natural[id(child)] = main_natural
            fixed_main += main_natural
            stretch_sum += lp.stretch

        extra = max(0.0, main_total - gaps - fixed_main)
        main_pos = pad

        for child in visible:
            lp = self._lp(child)
            if stretch_sum > 0:
                main_size = natural[id(child)] + extra * lp.stretch / stretch_sum
            else:
                main_size = natural[id(child)]
            main_size = max(
                lp.min_height if self.vertical else lp.min_width, main_size
            )

            if self.vertical:
                child_h = main_size
                child_w = self._cross_size(lp, cross_total)
                x = pad + self._cross_offset(child_w, cross_total)
                y = main_pos
                main_pos += child_h + self.spacing
            else:
                child_w = main_size
                child_h = self._cross_size(lp, cross_total)
                x = main_pos
                y = pad + self._cross_offset(child_h, cross_total)
                main_pos += child_w + self.spacing

            set_bounds(child, x, y, child_w, child_h)

    def _cross_size(self, lp: LayoutParams, cross_total: float) -> float:
        """根据对齐方式决定交叉轴尺寸。"""
        if lp.alignment == ALIGN_STRETCH or lp.alignment == ALIGN_START:
            return cross_total
        return min(cross_total, float(lp.max_width or cross_total))

    def _cross_offset(self, child_size: float, cross_total: float) -> float:
        if self.alignment == ALIGN_CENTER:
            return (cross_total - child_size) / 2
        if self.alignment == ALIGN_END:
            return cross_total - child_size
        return 0.0


class VBox(Box):
    """垂直盒子布局：子控件从上到下排列。"""

    vertical = True


class HBox(Box):
    """水平盒子布局：子控件从左到右排列。"""

    vertical = False


# ---------------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------------

class Grid(Layout):
    """网格布局。

    通过 ``add(widget, row=0, col=1, col_span=2)`` 指定格子位置。
    """

    def __init__(
        self,
        rows: int = 1,
        cols: int = 1,
        row_spacing: int = 0,
        col_spacing: int = 0,
    ) -> None:
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.row_spacing = row_spacing
        self.col_spacing = col_spacing

    def layout(self, container: Any, available_width: float, available_height: float) -> None:
        rows = max(self.rows, 1)
        cols = max(self.cols, 1)
        cell_w = (available_width - self.col_spacing * (cols - 1)) / cols
        cell_h = (available_height - self.row_spacing * (rows - 1)) / rows

        for child in self.children:
            if not getattr(child, "visible", True):
                continue
            lp = self._lp(child)
            x = lp.col * (cell_w + self.col_spacing)
            y = lp.row * (cell_h + self.row_spacing)
            w = cell_w * lp.col_span + self.col_spacing * (lp.col_span - 1)
            h = cell_h * lp.row_span + self.row_spacing * (lp.row_span - 1)
            set_bounds(child, x, y, w, h)


# ---------------------------------------------------------------------------
# Stack（重叠堆叠）
# ---------------------------------------------------------------------------

class Stack(Layout):
    """堆叠布局：所有子控件完全重叠，按 z 顺序从下到上绘制。"""

    def layout(self, container: Any, available_width: float, available_height: float) -> None:
        for child in self.children:
            if not getattr(child, "visible", True):
                continue
            set_bounds(child, 0, 0, available_width, available_height)


# ---------------------------------------------------------------------------
# Anchor（锚点布局）
# ---------------------------------------------------------------------------

@dataclass
class Annotations:
    """锚点说明（内部使用）。"""

    top: Optional[int] = None
    bottom: Optional[int] = None
    left: Optional[int] = None
    right: Optional[int] = None
    center_x: bool = False
    center_y: bool = False
    width: float = 0
    height: float = 0


class Anchor(Layout):
    """锚点布局：把每个子控件锚定到容器的某条边/某个角/中心。"""

    def add_anchored(
        self,
        widget: Any,
        *,
        top: Optional[int] = None,
        bottom: Optional[int] = None,
        left: Optional[int] = None,
        right: Optional[int] = None,
        center_x: bool = False,
        center_y: bool = False,
        width: float = 0,
        height: float = 0,
    ) -> None:
        lp = self.add(widget)
        lp.min_width = int(width) if width else 0
        lp.min_height = int(height) if height else 0
        widget._anchor = Annotations(  # type: ignore[attr-defined]
            top=top, bottom=bottom, left=left, right=right,
            center_x=center_x, center_y=center_y, width=width, height=height,
        )

    def layout(self, container: Any, available_width: float, available_height: float) -> None:
        for child in self.children:
            if not getattr(child, "visible", True):
                continue
            ann: Annotations = getattr(child, "_anchor", Annotations())
            nw, nh = natural_size(child)
            w = ann.width or nw
            h = ann.height or nh

            if ann.left is not None and ann.right is not None:
                x = ann.left
                w = available_width - ann.left - ann.right
            elif ann.left is not None:
                x = ann.left
            elif ann.right is not None:
                x = available_width - ann.right - w
            elif ann.center_x:
                x = (available_width - w) / 2
            else:
                x = 0.0

            if ann.top is not None and ann.bottom is not None:
                y = ann.top
                h = available_height - ann.top - ann.bottom
            elif ann.top is not None:
                y = ann.top
            elif ann.bottom is not None:
                y = available_height - ann.bottom - h
            elif ann.center_y:
                y = (available_height - h) / 2
            else:
                y = 0.0

            set_bounds(child, x, y, w, h)


__all__ = [
    "ALIGN_CENTER",
    "ALIGN_END",
    "ALIGN_START",
    "ALIGN_STRETCH",
    "Anchor",
    "Grid",
    "HBox",
    "Layout",
    "LayoutParams",
    "Stack",
    "VBox",
    "set_bounds",
]
