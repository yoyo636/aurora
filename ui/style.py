"""AuroraUI v3.1.0 — CSS 子集样式系统。

支持一个精简但实用的 CSS 子集：

* 选择器：类型选择器（``Button``）、类选择器（``.primary``）、
  ID 选择器（``#submit``）、后代选择器（``.dialog Button``）、
  状态伪类（``:hover`` / ``:active`` / ``:focus`` / ``:disabled``）；
* 属性：``color / background-color / font-size / font-family /
  font-weight / width / height / padding / margin / border /
  border-radius / opacity / visibility / text-align``；
* 级联：按 (特异性, 源码顺序) 排序；
* 内联样式：``widget.style = "color: red; font-size: 14px;"``。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# 选择器
# ---------------------------------------------------------------------------

@dataclass
class Selector:
    """解析后的选择器。

    组件列表从右到左匹配（CSS 习惯）。每个组件是一个字典::

        {"type": "Button", "class": "primary", "id": "submit", "pseudo": "hover"}
    """

    parts: List[Dict[str, Optional[str]]] = field(default_factory=list)
    specificity: int = 0
    raw: str = ""

    def matches(self, widget: Any, ancestors: List[Any]) -> bool:
        """判断 *widget* 是否匹配本选择器。"""
        if not self.parts:
            return False
        # 最后一个组件必须匹配 widget 本身
        if not self._match_part(self.parts[-1], widget):
            return False
        # 其余组件按"后代"关系依次在祖先链上找
        needle = len(self.parts) - 2
        for ancestor in reversed(ancestors):
            if needle < 0:
                break
            if self._match_part(self.parts[needle], ancestor):
                needle -= 1
        return needle < 0

    @staticmethod
    def _match_part(part: Dict[str, Optional[str]], widget: Any) -> bool:
        if part.get("type") is not None:
            if type(widget).__name__ != part["type"]:
                return False
        if part.get("id") is not None:
            if getattr(widget, "id", None) != part["id"]:
                return False
        if part.get("class") is not None:
            classes = getattr(widget, "style_class", "") or ""
            if part["class"] not in classes.split():
                return False
        if part.get("pseudo") is not None:
            state = part["pseudo"]
            if state == "disabled" and getattr(widget, "enabled", True):
                return False
            if state == "hover" and not getattr(widget, "_hovered", False):
                return False
            if state == "active" and not getattr(widget, "_pressed", False):
                return False
            if state == "focus" and not getattr(widget, "_focused", False):
                return False
        return True


_PART_RE = re.compile(
    r"^(?P<type>[A-Za-z][\w-]*)?"
    r"(?:#(?P<id>[\w-]+))?"
    r"(?:\.(?P<class>[\w-]+))?"
    r"(?::(?P<pseudo>hover|active|focus|disabled))?$"
)


def _parse_selector(text: str) -> Selector:
    """把 ``".dialog Button.primary:hover"`` 解析成 :class:`Selector`。"""
    parts: List[Dict[str, Optional[str]]] = []
    specificity = 0
    for chunk in text.split():
        m = _PART_RE.match(chunk)
        if not m:
            continue
        gd = m.groupdict()
        part = {
            "type": gd.get("type"),
            "id": gd.get("id"),
            "class": gd.get("class"),
            "pseudo": gd.get("pseudo"),
        }
        parts.append(part)
        if part["id"]:
            specificity += 100
        if part["class"] or part["pseudo"]:
            specificity += 10
        if part["type"]:
            specificity += 1
    sel = Selector(parts=parts, specificity=specificity, raw=text.strip())
    return sel


# ---------------------------------------------------------------------------
# 样式表
# ---------------------------------------------------------------------------

@dataclass
class StyleRule:
    """一条 CSS 规则：选择器 + 声明块。"""

    selector: Selector
    declarations: Dict[str, str]
    order: int = 0


#: 一个极简的 CSS 子集词法分析
_TOKEN_RE = re.compile(r"[^{}]+|\{|\}|[^{}]+")


class StyleSheet:
    """解析后的样式表。

    用法::

        src = 'Button { color: red; font-size: 14px; }\\n' \\
              'Button.primary { background-color: blue; }\\n' \\
              '#submit:hover { opacity: 0.8; }'
        sheet = StyleSheet(src)
    """

    def __init__(self, source: str = "") -> None:
        self.source = source
        self.rules: List[StyleRule] = []
        if source:
            self.parse(source)

    # -- 解析 ---------------------------------------------------------------

    def parse(self, source: str) -> None:
        self.rules = []
        order = 0
        # 去掉注释
        source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
        # 按 "selector { declarations }" 切分
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", source):
            selector_text = m.group(1).strip()
            body = m.group(2).strip()
            if not selector_text or not body:
                continue
            declarations = self._parse_declarations(body)
            if not declarations:
                continue
            for sel_text in selector_text.split(","):
                sel_text = sel_text.strip()
                if not sel_text:
                    continue
                self.rules.append(
                    StyleRule(
                        selector=_parse_selector(sel_text),
                        declarations=declarations,
                        order=order,
                    )
                )
                order += 1

    @staticmethod
    def _parse_declarations(body: str) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for decl in body.split(";"):
            decl = decl.strip()
            if not decl or ":" not in decl:
                continue
            prop, _, value = decl.partition(":")
            out[prop.strip().lower()] = value.strip()
        return out

    # -- 查询 ---------------------------------------------------------------

    def match(self, widget: Any, ancestors: List[Any]) -> List[Tuple[int, StyleRule]]:
        """返回所有匹配 *widget* 的规则 ``(specificity, rule)``。"""
        matched: List[Tuple[int, StyleRule]] = []
        for rule in self.rules:
            if rule.selector.matches(widget, ancestors):
                matched.append((rule.selector.specificity, rule))
        return matched


# ---------------------------------------------------------------------------
# 样式引擎
# ---------------------------------------------------------------------------

#: 内联样式的特异性（最高）
INLINE_SPECIFICITY = 10000


class StyleEngine:
    """把 :class:`StyleSheet` 应用到一棵控件树，计算最终样式。"""

    def __init__(self, stylesheet: Optional[StyleSheet] = None) -> None:
        self.stylesheet = stylesheet or StyleSheet()

    def compute_style(self, widget: Any, ancestors: Optional[List[Any]] = None) -> Dict[str, str]:
        """计算 *widget* 的最终样式表。"""
        ancestors = ancestors if ancestors is not None else self._collect_ancestors(widget)
        candidates: List[Tuple[int, int, Dict[str, str]]] = []

        for specificity, rule in self.stylesheet.match(widget, ancestors):
            candidates.append((specificity, rule.order, rule.declarations))

        # 内联样式最后覆盖
        inline = getattr(widget, "style", "") or ""
        inline_decls = StyleSheet._parse_declarations(inline)
        if inline_decls:
            candidates.append((INLINE_SPECIFICITY, 1 << 30, inline_decls))

        # 按 (specificity, order) 升序应用 —— 后面的覆盖前面的
        candidates.sort(key=lambda item: (item[0], item[1]))
        final: Dict[str, str] = {}
        for _, _, decls in candidates:
            final.update(decls)
        return final

    def apply(self, widget: Any, ancestors: Optional[List[Any]] = None) -> Dict[str, str]:
        """计算并把结果写到 ``widget._computed_style``，返回它。"""
        style = self.compute_style(widget, ancestors)
        widget._computed_style = style  # type: ignore[attr-defined]
        return style

    def apply_tree(self, root: Any) -> None:
        """对一棵控件树递归应用样式。"""
        self._walk(root, [])

    # -- 内部 ---------------------------------------------------------------

    def _walk(self, widget: Any, ancestors: List[Any]) -> None:
        self.apply(widget, ancestors)
        children = getattr(widget, "children", []) or []
        for child in children:
            self._walk(child, ancestors + [widget])

    def _collect_ancestors(self, widget: Any) -> List[Any]:
        chain: List[Any] = []
        node = getattr(widget, "parent", None)
        seen = set()
        while node is not None and id(node) not in seen:
            chain.append(node)
            seen.add(id(node))
            node = getattr(node, "parent", None)
        return chain


def apply_style(widget: Any, stylesheet: StyleSheet) -> Dict[str, str]:
    """便捷函数：用 *stylesheet* 计算并返回 *widget* 的最终样式。"""
    engine = StyleEngine(stylesheet)
    return engine.apply(widget)


__all__ = [
    "INLINE_SPECIFICITY",
    "Selector",
    "StyleEngine",
    "StyleRule",
    "StyleSheet",
    "apply_style",
]
