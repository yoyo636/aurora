"""Aurora v3.1.0 — 浏览器引擎开发支持库

一个从零实现的、教学/嵌入式向的最小浏览器引擎：

* :class:`HTMLParser` + :class:`DOMNode` — HTML 词法 / 语法分析，容错构建 DOM 树。
* :class:`CSSParser` — 解析选择器 + 声明块，计算特异性。
* :class:`StyleEngine` — 级联 + 继承，把样式表应用到 DOM。
* :class:`LayoutEngine` — 盒模型布局（content / padding / border / margin）。
* :class:`Renderer` — 简化绘制顺序。
* :class:`JSEngineBinding` — QuickJS / V8 绑定接口。

不依赖任何第三方包；CLI 通过 :func:`register_cli` 注册 ``aurora browser``。
"""

from __future__ import annotations

import html as _html
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ===========================================================================
# 1. HTML 解析器
# ===========================================================================

#: 自闭合标签（void elements），不需要配对
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

_ENTITY_RE = re.compile(r"&(#?\w+);")


def decode_entities(text: str) -> str:
    """解码 HTML 实体（``&amp;`` / ``&#65;`` 等）。"""
    return _html.unescape(text)


class DOMNode:
    """DOM 树节点。"""

    def __init__(self, tag: str, attrs: Optional[Dict[str, str]] = None,
                 text: str = "") -> None:
        self.tag = tag
        self.attrs: Dict[str, str] = dict(attrs or {})
        self.text = text
        self.children: List["DOMNode"] = []
        self.parent: Optional[DOMNode] = None
        self.styles: Dict[str, str] = {}

    @property
    def is_text(self) -> bool:
        return self.tag == "#text"

    @property
    def text_content(self) -> str:
        """自身文本 + 所有后代文本。"""
        if self.is_text:
            return self.text
        return "".join(c.text_content for c in self.children)

    @property
    def id(self) -> Optional[str]:
        return self.attrs.get("id")

    @property
    def classes(self) -> List[str]:
        cls = self.attrs.get("class", "")
        return [c for c in cls.split() if c]

    def append_child(self, child: "DOMNode") -> None:
        child.parent = self
        self.children.append(child)

    def walk(self):
        """深度优先遍历整棵子树。"""
        yield self
        for c in self.children:
            yield from c.walk()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.tag} {self.attrs}>"


class HTMLParser:
    """极简 HTML 解析器。

    支持开始/结束/自闭合标签、属性、实体解码；
    对未闭合标签与无效嵌套做容错（自动闭合）。
    """

    def __init__(self) -> None:
        self.pos = 0
        self.s = ""
        self.root = DOMNode("#document")

    # -- 入口 ---------------------------------------------------------------

    def parse(self, source: str) -> DOMNode:
        """解析 HTML 字符串，返回根节点。"""
        self.s = source
        self.pos = 0
        self.root = DOMNode("#document")
        stack: List[DOMNode] = [self.root]
        text_buf = ""

        def _flush_text() -> None:
            nonlocal text_buf
            if text_buf.strip():
                t = DOMNode("#text", text=decode_entities(text_buf))
                stack[-1].append_child(t)
            text_buf = ""

        while self.pos < len(self.s):
            if self.s[self.pos] == "<":
                _flush_text()
                tag = self._read_tag()
                if tag is None:
                    text_buf += self.s[self.pos]
                    self.pos += 1
                    continue
                name, attrs, closing, self_closing = tag
                if closing:
                    # 找到最近的同名开标签闭合（容错：弹到匹配处）
                    for i in range(len(stack) - 1, 0, -1):
                        if stack[i].tag == name:
                            del stack[i:]
                            break
                else:
                    node = DOMNode(name, attrs)
                    stack[-1].append_child(node)
                    if not self_closing and name not in VOID_TAGS:
                        stack.append(node)
            else:
                end = self.s.find("<", self.pos)
                chunk = self.s[self.pos:end if end != -1 else len(self.s)]
                text_buf += chunk
                self.pos += len(chunk)
        _flush_text()
        return self.root

    # -- 词法 ---------------------------------------------------------------

    def _read_tag(self) -> Optional[Tuple[str, Dict[str, str], bool, bool]]:
        """读取 ``<...>`` 内容，返回 (name, attrs, closing, self_closing)。"""
        assert self.s[self.pos] == "<"
        start = self.pos
        end = self.s.find(">", self.pos)
        if end == -1:
            return None
        inner = self.s[self.pos + 1:end].strip()
        self.pos = end + 1

        closing = inner.startswith("/")
        if closing:
            inner = inner[1:].strip()
        self_closing = inner.endswith("/")
        if self_closing:
            inner = inner[:-1].strip()

        if not inner:
            return None
        parts = inner.split(None, 1)
        name = parts[0].lower()
        attr_str = parts[1] if len(parts) > 1 else ""
        attrs = self._read_attrs(attr_str)
        return name, attrs, closing, self_closing

    @staticmethod
    def _read_attrs(s: str) -> Dict[str, str]:
        """读取 ``name="value" name2 value`` 属性列表。"""
        attrs: Dict[str, str] = {}
        # 匹配 key="..." / key='...' / key=... / bare_key
        pattern = re.compile(r"""([\w-]+)(?:\s*=\s*("([^"]*)"|'([^']*)'|(\S+))?)?""")
        for m in pattern.finditer(s):
            key = m.group(1)
            value = m.group(3) or m.group(4) or m.group(5) or ""
            attrs[key] = decode_entities(value)
        return attrs


# ===========================================================================
# 2. CSS 解析器
# ===========================================================================

@dataclass
class Selector:
    """CSS 选择器。支持 tag / #id / .class / 组合。"""

    raw: str = ""
    tag: str = ""
    ids: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)

    def matches(self, node: DOMNode) -> bool:
        if node.is_text:
            return False
        if self.tag and node.tag != self.tag:
            return False
        for i in self.ids:
            if node.id != i:
                return False
        node_classes = set(node.classes)
        for c in self.classes:
            if c not in node_classes:
                return False
        return True

    def specificity(self) -> Tuple[int, int, int]:
        """返回 (id 数, class 数, tag 数)。"""
        return (len(self.ids), len(self.classes),
                1 if self.tag else 0)


@dataclass
class Declaration:
    """一条 ``property: value`` 声明。"""

    prop: str = ""
    value: str = ""


@dataclass
class CSSRule:
    """一条 CSS 规则：选择器列表 + 声明块。"""

    selectors: List[Selector] = field(default_factory=list)
    declarations: List[Declaration] = field(default_factory=list)


@dataclass
class StyleSheet:
    """样式表。"""

    rules: List[CSSRule] = field(default_factory=list)
    media: str = ""
    keyframes: Dict[str, List[Tuple[List[str], Dict[str, str]]]] = field(
        default_factory=dict)


class CSSParser:
    """极简 CSS 解析器：规则 + @media + @keyframes。"""

    def parse(self, source: str) -> StyleSheet:
        sheet = StyleSheet()
        # 去掉注释
        source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
        pos = 0
        while pos < len(source):
            m_at = re.match(r"\s*@(\w+)\s*([^{]*)\{", source[pos:])
            if m_at:
                keyword = m_at.group(1)
                header = m_at.group(2).strip()
                block, pos = self._read_block(source, pos + m_at.end() - 1)
                if keyword == "media":
                    inner = CSSParser().parse(block)
                    for r in inner.rules:
                        r  # 保留
                    sheet.rules.extend(inner.rules)
                elif keyword == "keyframes":
                    sheet.keyframes[header] = self._parse_keyframes(block)
                continue
            m = re.match(r"\s*([^{}]+)\{", source[pos:])
            if not m:
                break
            selector_text = m.group(1).strip()
            block, pos = self._read_block(source, pos + m.end() - 1)
            rule = CSSRule(selectors=[self._parse_selector(s)
                                      for s in selector_text.split(",") if s.strip()],
                           declarations=self._parse_decls(block))
            sheet.rules.append(rule)
        return sheet

    @staticmethod
    def _read_block(s: str, start: int) -> Tuple[str, int]:
        """读取一个 ``{ ... }`` 块（支持嵌套计数）。"""
        depth = 0
        i = start
        while i < len(s):
            if s[i] == "{":
                depth += 1
            elif s[i] == "}":
                depth -= 1
                if depth == 0:
                    return s[start + 1:i], i + 1
            i += 1
        return s[start + 1:], len(s)

    @staticmethod
    def _parse_selector(text: str) -> Selector:
        text = text.strip()
        sel = Selector(raw=text)
        for m in re.finditer(r"(#[\w-]+)|\.([\w-]+)|^([a-zA-Z][\w-]*)", text):
            if m.group(1):
                sel.ids.append(m.group(1)[1:])
            elif m.group(2):
                sel.classes.append(m.group(2))
            elif m.group(3):
                sel.tag = m.group(3)
        return sel

    @staticmethod
    def _parse_decls(block: str) -> List[Declaration]:
        out: List[Declaration] = []
        for chunk in block.split(";"):
            chunk = chunk.strip()
            if not chunk or ":" not in chunk:
                continue
            prop, _, value = chunk.partition(":")
            out.append(Declaration(prop.strip(), value.strip()))
        return out

    @staticmethod
    def _parse_keyframes(block: str) -> List[Tuple[List[str], Dict[str, str]]]:
        out: List[Tuple[List[str], Dict[str, str]]] = []
        for m in re.finditer(r"([\d\s%,]+)\s*\{([^}]*)\}", block):
            times = [t.strip() for t in m.group(1).split(",")]
            props: Dict[str, str] = {}
            for decl in m.group(2).split(";"):
                if ":" in decl:
                    k, _, v = decl.partition(":")
                    props[k.strip()] = v.strip()
            out.append((times, props))
        return out


# ===========================================================================
# 3. 样式计算
# ===========================================================================

#: CSS 属性初始值表
INITIAL_VALUES: Dict[str, str] = {
    "color": "black",
    "background-color": "transparent",
    "font-size": "16px",
    "font-weight": "normal",
    "display": "inline",
    "margin": "0",
    "padding": "0",
    "border-width": "0",
    "width": "auto",
    "height": "auto",
    "text-align": "start",
    "line-height": "normal",
}

#: 可继承属性
INHERITED_PROPERTIES = {"color", "font-size", "font-weight", "text-align",
                        "line-height", "font-family"}


class StyleEngine:
    """把样式表应用到 DOM 树：级联 + 继承 + 初始值。"""

    def __init__(self, sheet: Optional[StyleSheet] = None) -> None:
        self.sheet = sheet or StyleSheet()

    def apply(self, root: DOMNode) -> None:
        """对整棵 DOM 树计算样式。"""
        # 收集每个节点匹配的声明，按特异性排序后应用
        for node in root.walk():
            matched: List[Tuple[Tuple[int, int, int], Declaration]] = []
            for rule in self.sheet.rules:
                for sel in rule.selectors:
                    if sel.matches(node):
                        for d in rule.declarations:
                            matched.append((sel.specificity(), d))
            # 高特异性优先（越大越优先）
            matched.sort(key=lambda t: t[0], reverse=True)
            node.styles = dict(INITIAL_VALUES)
            # 继承父节点可继承属性
            if node.parent is not None:
                for prop in INHERITED_PROPERTIES:
                    if prop in node.parent.styles:
                        node.styles[prop] = node.parent.styles[prop]
            for _, d in matched:
                node.styles[d.prop] = d.value


# ===========================================================================
# 4. 布局引擎
# ===========================================================================

@dataclass
class LayoutBox:
    """盒模型布局结果。"""

    node: Optional[DOMNode] = None
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    padding: int = 0
    border: int = 0
    margin: int = 0
    children: List["LayoutBox"] = field(default_factory=list)

    @property
    def content_box(self) -> Tuple[int, int, int, int]:
        """内容区 (x, y, w, h)。"""
        pad = self.padding + self.border
        return (self.x + pad, self.y + pad,
                max(0, self.width - 2 * pad), max(0, self.height - 2 * pad))

    @property
    def margin_box(self) -> Tuple[int, int, int, int]:
        return (self.x - self.margin, self.y - self.margin,
                self.width + 2 * self.margin, self.height + 2 * self.margin)


def _px(value: str, default: int = 0) -> int:
    """把 ``12px`` / ``auto`` 之类的值转为 int。"""
    if not value or value == "auto":
        return default
    m = re.match(r"(-?\d+)", value)
    return int(m.group(1)) if m else default


class LayoutEngine:
    """简化布局引擎：块级 / 行内 + 盒模型。"""

    def __init__(self, viewport_width: int = 800, viewport_height: int = 600) -> None:
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def layout(self, dom_node: DOMNode,
               styles: Optional[Dict[str, str]] = None,
               x: int = 0, y: int = 0) -> LayoutBox:
        """递归布局一个 DOM 节点。"""
        styles = styles or dom_node.styles
        box = LayoutBox(node=dom_node)
        box.padding = _px(styles.get("padding", "0"))
        box.border = _px(styles.get("border-width", "0"))
        box.margin = _px(styles.get("margin", "0"))
        box.x = x + box.margin
        box.y = y + box.margin

        display = styles.get("display", "inline")
        width = _px(styles.get("width", "0"))
        height = _px(styles.get("height", "0"))
        if display == "block" or dom_node.tag in ("div", "p", "h1", "h2", "h3",
                                                  "ul", "li", "section"):
            box.width = self.viewport_width - 2 * (x + box.margin) if width == 0 else width
            box.height = height or 24
            child_y = box.y + box.padding + box.border
            for child in dom_node.children:
                if child.is_text:
                    continue
                child_box = self.layout(
                    child, child.styles,
                    x=box.x + box.padding + box.border,
                    y=child_y)
                box.children.append(child_box)
                child_y += child_box.height + child_box.margin
        else:
            box.width = width or 100
            box.height = height or 20
        return box

    # 便捷别名
    layout_node = layout


# ===========================================================================
# 5. 渲染（简化）
# ===========================================================================

class Renderer:
    """按 背景 → 边框 → 内容 → 子元素 的顺序绘制布局树。"""

    def __init__(self, canvas: Any = None) -> None:
        self.canvas = canvas  # AuroraUI Canvas 或类似对象
        self.commands: List[Tuple[str, Any]] = []

    def render(self, layout_tree: LayoutBox) -> List[Tuple[str, Any]]:
        """生成绘制指令序列。"""
        self.commands = []
        self._draw(layout_tree)
        return self.commands

    def _draw(self, box: LayoutBox) -> None:
        styles = box.node.styles if box.node else {}
        # 1) 背景
        bg = styles.get("background-color", "transparent")
        if bg != "transparent":
            self.commands.append(("fill_rect", (box.x, box.y, box.width, box.height, bg)))
        # 2) 边框
        if box.border > 0:
            self.commands.append(("stroke_rect",
                                  (box.x, box.y, box.width, box.height, box.border)))
        # 3) 内容
        if box.node and box.node.text:
            self.commands.append(("draw_text", (box.x + box.padding, box.y + box.padding,
                                                box.node.text)))
        # 4) 子元素
        for child in box.children:
            self._draw(child)


# ===========================================================================
# 6. JS 引擎绑定接口
# ===========================================================================

class JSEngineBinding:
    """JS 引擎（QuickJS / V8）绑定接口。

    通过 ctypes 加载动态库；当前仅定义接口轮廓，未实现具体引擎的 ABI。
    """

    def __init__(self, library_path: str = "") -> None:
        self.library_path = library_path
        self._lib: Any = None
        if library_path and os.path.exists(library_path):
            try:
                import ctypes
                self._lib = ctypes.CDLL(library_path)
            except OSError:
                self._lib = None

    def available(self) -> bool:
        return self._lib is not None

    def evaluate(self, code: str) -> Any:
        """执行一段 JS 源码。"""
        raise NotImplementedError("QuickJS/V8 ABI 投影待实现")

    def call_function(self, name: str, *args: Any) -> Any:
        """调用全局函数。"""
        raise NotImplementedError

    def set_global(self, name: str, value: Any) -> None:
        """写入全局变量。"""
        raise NotImplementedError

    def get_global(self, name: str) -> Any:
        """读取全局变量。"""
        raise NotImplementedError


class QuickJSBinding(JSEngineBinding):
    """QuickJS 绑定接口（``libquickjs.so`` / ``libquickjs.dylib``）。"""

    def __init__(self, library_path: str = "libquickjs.dylib") -> None:
        super().__init__(library_path)


class V8Binding(JSEngineBinding):
    """V8 绑定接口（通过 C++ 桥接 DLL）。"""

    def __init__(self, library_path: str = "libv8bridge.dylib") -> None:
        super().__init__(library_path)


# ===========================================================================
# CLI 注册
# ===========================================================================

def register_cli(subparsers: Any) -> None:
    """注册 ``aurora browser`` 命令。"""
    p = subparsers.add_parser("browser", help="浏览器引擎：解析 HTML/CSS 并输出树结构")
    p.add_argument("file", help="HTML 或 CSS 文件")
    p.add_argument("--css", action="store_true", help="按 CSS 解析")
    p.add_argument("--dump", choices=["dom", "style"], default="dom",
                   help="输出 DOM 树或样式树")
    p.set_defaults(func=_cmd_browser)


def _cmd_browser(args: Any) -> int:
    with open(args.file, "r", encoding="utf-8") as f:
        source = f.read()
    if args.css:
        sheet = CSSParser().parse(source)
        print(f"/* {len(sheet.rules)} rules */")
        for r in sheet.rules:
            sel = ",".join(s.raw for s in r.selectors)
            decls = "; ".join(f"{d.prop}: {d.value}" for d in r.declarations)
            print(f"  {sel} {{ {decls} }}")
    else:
        root = HTMLParser().parse(source)
        _print_dom(root)
    return 0


def _print_dom(node: DOMNode, depth: int = 0) -> None:
    indent = "  " * depth
    if node.is_text:
        if node.text.strip():
            print(f"{indent}#text: {node.text.strip()!r}")
        return
    print(f"{indent}<{node.tag}> {node.attrs}")
    for c in node.children:
        _print_dom(c, depth + 1)


__all__ = [
    "HTMLParser", "DOMNode", "decode_entities",
    "CSSParser", "StyleSheet", "CSSRule", "Selector", "Declaration",
    "StyleEngine", "INITIAL_VALUES", "INHERITED_PROPERTIES",
    "LayoutEngine", "LayoutBox", "Renderer",
    "JSEngineBinding", "QuickJSBinding", "V8Binding",
    "register_cli",
]
