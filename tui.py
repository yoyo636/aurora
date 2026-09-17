"""AuroraTUI — Aurora v3.2.0 标准库扩展：终端 TUI 框架

仅依赖 Python 标准库。提供：

- 终端样式：16/256/真彩色、粗体/斜体/下划线/删除线，自动探测颜色级别
- 输出组件：ProgressBar / Spinner / Table / Tree / Panel / 代码高亮
- 交互提示：prompt_input / prompt_select / prompt_multiselect / prompt_confirm /
  prompt_password（非终端环境自动降级为返回默认值，不抛异常）
- TUI 组件：Widget 基类及 TextBox / ListBox / Button / Menu / Tabs /
  SplitPanel / StatusBar / Dialog
- 布局系统：HBox / VBox，flex_grow / justify_content / align_items / padding
- 事件系统：EventLoop（定时器 + 事件总线）、Key 按键解析
- PTY：基于 pty/os 的伪终端封装
- ANSI：AnsiParser 转义序列解析、TerminalBuffer 虚拟终端缓冲
"""

from __future__ import annotations

import fcntl
import os
import pty as _pty_mod
import re
import select
import shutil
import signal
import struct
import sys
import termios
import threading
import time
import unicodedata
from typing import Any, Callable, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# 终端环境探测
# ─────────────────────────────────────────────────────────────────────────────

def detect_color_level() -> str:
    """探测当前终端支持的颜色级别。

    返回：``"no_color"`` / ``"16"`` / ``"256"`` / ``"truecolor"``。
    遵循 ``NO_COLOR`` 环境变量约定；``TERM=dumb`` 视为不支持颜色。
    """
    if os.environ.get("NO_COLOR") is not None:
        return "no_color"
    term = os.environ.get("TERM", "").lower()
    if term == "dumb" or not term:
        return "no_color"
    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return "truecolor"
    if "256" in term:
        return "256"
    return "16"


COLOR_LEVEL = detect_color_level()


def terminal_size() -> Tuple[int, int]:
    """返回终端尺寸 (rows, cols)，探测失败时回退 (24, 80)。"""
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.lines, size.columns


# ─────────────────────────────────────────────────────────────────────────────
# ANSI 工具
# ─────────────────────────────────────────────────────────────────────────────

_ANSI_RE = re.compile(
    r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)"          # OSC（窗口标题等）
    r"|\x1b\[[0-9;?]*[ -/]*[@-~]"                 # CSI（光标/颜色/鼠标）
    r"|\x1b[@-Z\\-_]"                             # 其他两字节转义
)


def strip_ansi(text: str) -> str:
    """移除文本中的所有 ANSI 转义序列，返回纯文本。"""
    return _ANSI_RE.sub("", text)


def ansi_len(text: str) -> int:
    """计算去除 ANSI 后的可见字符长度，宽字符（CJK）按 2 计。"""
    plain = strip_ansi(text)
    width = 0
    for ch in plain:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def visible_pad(text: str, width: int, align: str = "left") -> str:
    """按可见长度把文本补齐到 width（支持左/中/右对齐）。"""
    pad = max(0, width - ansi_len(text))
    if align == "right":
        return " " * pad + text
    if align == "center":
        left = pad // 2
        return " " * left + text + " " * (pad - left)
    return text + " " * pad


# ─────────────────────────────────────────────────────────────────────────────
# 样式系统
# ─────────────────────────────────────────────────────────────────────────────

_NAMED_COLORS: Dict[str, int] = {
    "black": 0, "red": 1, "green": 2, "yellow": 3,
    "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
    "brightblack": 8, "brightred": 9, "brightgreen": 10, "brightyellow": 11,
    "brightblue": 12, "brightmagenta": 13, "brightcyan": 14, "brightwhite": 15,
    "gray": 8, "grey": 8, "darkgray": 8,
}


def _hex_to_rgb(hexstr: str) -> Tuple[int, int, int]:
    h = hexstr.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _palette_index(r: int, g: int, b: int) -> int:
    """把 RGB 近似映射到 256 色 6x6x6 立方。"""
    def c(v: int) -> int:
        return 0 if v < 48 else (1 if v < 115 else (v - 35) // 40)
    return 16 + 36 * c(r) + 6 * c(g) + c(b)


def _color_param(color: Any, is_bg: bool, level: str) -> Optional[str]:
    """根据颜色级别把 fg/bg 规格转成 SGR 参数串。"""
    if color is None or level == "no_color":
        return None
    base = 48 if is_bg else 38
    if isinstance(color, bool):
        return None
    if isinstance(color, int):
        if level in ("256", "truecolor"):
            return f"{base};5;{color}"
        # 16 色终端忽略编号色
        return None
    spec = str(color).strip().lower()
    if spec.startswith("#") and len(spec) == 7:
        if level == "truecolor":
            r, g, b = _hex_to_rgb(spec)
            return f"{base};2;{r};{g};{b}"
        if level == "256":
            r, g, b = _hex_to_rgb(spec)
            return f"{base};5;{_palette_index(r, g, b)}"
        return None
    idx = _NAMED_COLORS.get(spec)
    if idx is None:
        return None
    if level == "16":
        return str(40 + idx if is_bg else 30 + idx)
    # 256 / truecolor：调色板前 16 色与命名色一一对应
    return f"{base};5;{idx}"


class Style:
    """文本样式：前景色 / 背景色 / 粗体 / 斜体 / 下划线 / 删除线。

    颜色规格可为：命名色（``"red"``）、256 色编号（``42``）、
    真彩色 hex（``"#ff0000"``）。
    """

    def __init__(
        self,
        fg: Any = None,
        bg: Any = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ):
        self.fg = fg
        self.bg = bg
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough

    def _codes(self, level: str) -> List[str]:
        if level == "no_color":
            return []
        codes: List[str] = []
        if self.bold:
            codes.append("1")
        if self.italic:
            codes.append("3")
        if self.underline:
            codes.append("4")
        if self.strikethrough:
            codes.append("9")
        fg = _color_param(self.fg, False, level)
        if fg:
            codes.append(fg)
        bg = _color_param(self.bg, True, level)
        if bg:
            codes.append(bg)
        return codes

    def render(self, text: str, level: Optional[str] = None) -> str:
        """按当前样式把 text 包上 ANSI 序列。"""
        lv = level or COLOR_LEVEL
        codes = self._codes(lv)
        if not codes:
            return text
        return f"\x1b[{';'.join(codes)}m{text}\x1b[0m"

    def __repr__(self) -> str:  # pragma: no cover
        return (f"Style(fg={self.fg!r}, bg={self.bg!r}, bold={self.bold})")


def style(
    text: str,
    fg: Any = None,
    bg: Any = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    strikethrough: bool = False,
) -> str:
    """用给定样式渲染文本，自动适配终端颜色级别。"""
    return Style(fg, bg, bold, italic, underline, strikethrough).render(text)


def color(text: str, color_name: str) -> str:
    """以命名前景色渲染文本的快捷函数。"""
    return style(text, fg=color_name)


# ─────────────────────────────────────────────────────────────────────────────
# 输出组件
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_duration(seconds: float) -> str:
    """把秒数格式化为 ``1m23s`` 这样的紧凑形式。"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    m, s = divmod(int(seconds), 60)
    if m < 60:
        return f"{m}m{s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m"


class ProgressBar:
    """文本进度条。

    用法::

        pb = ProgressBar(100, label="下载")
        for i in range(101):
            pb.update(i)
        pb.done()
    """

    def __init__(
        self,
        total: int,
        width: int = 40,
        label: str = "",
        show_eta: bool = True,
    ):
        self.total = max(1, total)
        self.width = width
        self.label = label
        self.show_eta = show_eta
        self.current = 0
        self.started_at = time.monotonic()

    def update(self, n: int) -> None:
        """把进度更新到 n。"""
        self.current = max(0, min(self.total, n))

    @property
    def percent(self) -> float:
        return self.current / self.total * 100.0

    def eta(self) -> Optional[float]:
        """估算剩余秒数；进度为 0 时返回 None。"""
        if self.current <= 0 or self.current >= self.total:
            return None
        elapsed = time.monotonic() - self.started_at
        return elapsed / self.current * (self.total - self.current)

    def render(self) -> str:
        """渲染为单行字符串（不含换行）。"""
        filled = int(self.width * self.current / self.total)
        bar = "█" * filled + "░" * (self.width - filled)
        head = f"{self.label} " if self.label else ""
        line = f"{head}{bar} {self.percent:5.1f}% {self.current}/{self.total}"
        if self.show_eta and self.current < self.total:
            eta = self.eta()
            if eta is not None:
                line += f" ETA {_fmt_duration(eta)}"
        return line

    def done(self) -> None:
        """标记完成（把进度拉满）。"""
        self.current = self.total

    def __str__(self) -> str:  # pragma: no cover
        return self.render()


_SPINNER_FRAMES: Dict[str, Tuple[str, ...]] = {
    "dots": ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"),
    "lines": ("|", "/", "-", "\\"),
    "spinner": ("◜", "◝", "◞", "◟"),
    "moon": ("🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"),
    "burger": ("☱", "☲", "☴"),
}


class Spinner:
    """旋转指示器。在真实终端中后台线程动画；非终端环境仅打印文本。"""

    def __init__(self, text: str = "Loading...", style_name: str = "dots"):
        self.text = text
        self.frames = _SPINNER_FRAMES.get(style_name, _SPINNER_FRAMES["dots"])
        self._i = 0
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def _tick(self) -> None:
        stream = sys.stderr
        while not self._stop_event.is_set():
            frame = self.frames[self._i % len(self.frames)]
            self._i += 1
            stream.write(f"\r{frame} {self.text}")
            stream.flush()
            self._stop_event.wait(0.1)

    def start(self) -> "Spinner":
        """启动动画。非终端环境退化为直接打印一次。"""
        if not sys.stderr.isatty():
            sys.stderr.write(f"… {self.text}\n")
            sys.stderr.flush()
            return self
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._tick, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        """停止动画并清掉本行。"""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=0.5)
            self._thread = None
        if sys.stderr.isatty():
            sys.stderr.write("\r" + " " * (len(self.text) + 4) + "\r")
            sys.stderr.flush()

    def update(self, text: str) -> None:
        """更新提示文本。"""
        self.text = text


_BORDER_SETS: Dict[str, Dict[str, str]] = {
    "ascii": dict(tl="+", tr="+", bl="+", br="+", h="-", v="|",
                 ml="+", mr="+", mt="+", mb="+", mj="+"),
    "unicode": dict(tl="┌", tr="┐", bl="└", br="┘", h="─", v="│",
                    ml="├", mr="┤", mt="┬", mb="┴", mj="┼"),
    "rounded": dict(tl="╭", tr="╮", bl="╰", br="╯", h="─", v="│",
                    ml="├", mr="┤", mt="┬", mb="┴", mj="┼"),
}


class Table:
    """文本表格：自动列宽、对齐、边框样式、斑马纹。"""

    def __init__(
        self,
        headers: List[str],
        rows: Optional[List[List[str]]] = None,
        border: bool = True,
        align: str = "left",
        border_style: str = "unicode",
        zebra: bool = False,
    ):
        self.headers = list(headers)
        self.rows = [list(r) for r in (rows or [])]
        self.border = border
        self.align = align
        self.border_style = border_style if border_style in _BORDER_SETS else "unicode"
        self.zebra = zebra

    def _col_widths(self) -> List[int]:
        widths = [ansi_len(h) for h in self.headers]
        for row in self.rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], ansi_len(str(cell)))
        return widths

    def render(self) -> str:
        """渲染为多行字符串。"""
        widths = self._col_widths()
        n = len(widths)
        sep = _BORDER_SETS.get(self.border_style, _BORDER_SETS["unicode"])
        v = sep["v"] if self.border else " "

        def join_row(cells: List[str], zebra: bool = False) -> str:
            styled = []
            for i, cell in enumerate(cells):
                txt = str(cell)
                if zebra and COLOR_LEVEL != "no_color":
                    txt = style(txt, bg="brightblack")
                styled.append(visible_pad(txt, widths[i], self.align))
            if self.border:
                return v + v.join(" " + c + " " for c in styled) + v
            return "  ".join(styled)

        if not self.border:
            out = [join_row(self.headers)]
            for i, row in enumerate(self.rows):
                out.append(join_row(row, zebra=self.zebra and i % 2 == 1))
            return "\n".join(out) + "\n" if out else ""

        hline = sep["h"]
        top = sep["tl"] + sep["mt"].join(hline * (w + 2) for w in widths) + sep["tr"]
        mid = sep["ml"] + sep["mj"].join(hline * (w + 2) for w in widths) + sep["mr"]
        bottom = sep["bl"] + sep["mb"].join(hline * (w + 2) for w in widths) + sep["br"]

        header_cells = [
            visible_pad(style(h, bold=True) if COLOR_LEVEL != "no_color" else h,
                        widths[i], self.align)
            for i, h in enumerate(self.headers)
        ]
        out = [top, v + v.join(" " + c + " " for c in header_cells) + v, mid]
        for i, row in enumerate(self.rows):
            cells = [visible_pad(str(c), widths[j], self.align)
                     for j, c in enumerate(row)]
            line = v + v.join(" " + c + " " for c in cells) + v
            if self.zebra and i % 2 == 1 and COLOR_LEVEL != "no_color":
                line = style(line, bg="brightblack")
            out.append(line)
        out.append(bottom)
        return "\n".join(out)


class TreeNode:
    """树节点。"""

    def __init__(self, label: str, parent: Optional["TreeNode"] = None):
        self.label = label
        self.parent = parent
        self.children: List[TreeNode] = []


class Tree:
    """带连接线的文本树。

    用法::

        t = Tree("root")
        t.add("a", parent=t.root)
        t.add("b", parent=t.root)
        print(t.render())
    """

    def __init__(self, root_label: str = "."):
        self.root = TreeNode(root_label)

    def add(self, child_label: str, parent: Optional[TreeNode] = None) -> TreeNode:
        """向 parent（默认根节点）添加子节点并返回它。"""
        node = TreeNode(child_label, parent or self.root)
        (parent or self.root).children.append(node)
        return node

    def _render(self, node: TreeNode, prefix: str, is_last: bool,
                is_root: bool = False) -> List[str]:
        if is_root:
            lines = [node.label]
        else:
            branch = "└── " if is_last else "├── "
            lines = [prefix + branch + node.label]
        if is_root:
            child_prefix = ""
        elif is_last:
            child_prefix = "    "
        else:
            child_prefix = prefix + "│   "
        n = len(node.children)
        for i, child in enumerate(node.children):
            # 根节点的唯一子节点视为非末项，便于后续子树使用竖线连接
            if is_root and n == 1:
                last = False
            else:
                last = i == n - 1
            lines.extend(self._render(child, child_prefix, last))
        return lines

    def render(self) -> str:
        """渲染为树状多行字符串。"""
        return "\n".join(self._render(self.root, "", True, is_root=True))


def Panel(content: str, title: str = "", border_style: str = "rounded") -> str:
    """把内容包在带边框（及可选标题）的面板里。"""
    sep = _BORDER_SETS.get(border_style, _BORDER_SETS["rounded"])
    lines = content.splitlines() or [""]
    width = max((ansi_len(ln) for ln in lines), default=0)
    title_bar = title
    if title and ansi_len(title) < width:
        title_bar = f" {title} "
    top_mid = title_bar or ""
    top = (sep["tl"]
           + visible_pad(top_mid, max(1, width), "center")
           + sep["tr"])
    bottom = sep["bl"] + sep["h"] * max(1, width) + sep["br"]
    body = [sep["v"] + visible_pad(ln, width) + sep["v"] for ln in lines]
    return "\n".join([top, *body, bottom])


# ─────────────────────────────────────────────────────────────────────────────
# 代码高亮
# ─────────────────────────────────────────────────────────────────────────────

_HIGHLIGHT_KEYWORDS: Dict[str, set] = {
    "python": {
        "def", "class", "return", "if", "elif", "else", "for", "while",
        "import", "from", "as", "with", "try", "except", "finally", "raise",
        "lambda", "pass", "break", "continue", "and", "or", "not", "in",
        "is", "None", "True", "False", "yield", "global", "nonlocal", "assert",
        "del", "async", "await",
    },
    "json": set(),
    "sql": {
        "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE",
        "SET", "DELETE", "CREATE", "TABLE", "DROP", "ALTER", "JOIN", "ON",
        "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "AS", "AND", "OR", "NOT",
        "INNER", "LEFT", "RIGHT", "OUTER", "DISTINCT", "UNION", "ALL",
    },
    "shell": {
        "if", "then", "else", "elif", "fi", "for", "while", "do", "done",
        "case", "esac", "function", "in", "echo", "export", "local",
        "return", "exit", "cd", "ls", "mkdir", "rm", "cp", "mv",
    },
}


def _highlight_python(code: str, level: str) -> str:
    kw = _HIGHLIGHT_KEYWORDS["python"]
    pattern = re.compile(
        r"(?P<comment>#[^\n]*)"
        r"|(?P<str>\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?'''|\"(?:\\.|[^\"\\\n])*\""
        r"|'(?:\\.|[^'\\\n])*')"
        r"|(?P<num>\b\d+(?:\.\d+)?\b)"
        r"|(?P<kw>\b[A-Za-z_]\w*\b)"
    )

    def repl(m: re.Match) -> str:
        if m.lastgroup == "comment":
            return style(m.group(), fg="brightblack")
        if m.lastgroup == "str":
            return style(m.group(), fg="green")
        if m.lastgroup == "num":
            return style(m.group(), fg="yellow")
        if m.lastgroup == "kw" and m.group() in kw:
            return style(m.group(), fg="cyan", bold=True)
        return m.group()

    return pattern.sub(repl, code)


def _highlight_json(code: str, level: str) -> str:
    pattern = re.compile(
        r"(?P<key>\"(?:\\.|[^\"\\])*\"\s*:)"
        r"|(?P<str>\"(?:\\.|[^\"\\])*\")"
        r"|(?P<num>-?\d+(?:\.\d+)?)"
        r"|(?P<bool>\btrue\b|\bfalse\b|\bnull\b)"
    )

    def repl(m: re.Match) -> str:
        if m.lastgroup == "key":
            return style(m.group(), fg="cyan")
        if m.lastgroup == "str":
            return style(m.group(), fg="green")
        if m.lastgroup == "num":
            return style(m.group(), fg="yellow")
        return style(m.group(), fg="magenta", bold=True)

    return pattern.sub(repl, code)


def _highlight_sql(code: str, level: str) -> str:
    kw = _HIGHLIGHT_KEYWORDS["sql"]
    pattern = re.compile(
        r"(?P<comment>--[^\n]*)"
        r"|(?P<str>'(?:''|[^'])*')"
        r"|(?P<num>\b\d+(?:\.\d+)?\b)"
        r"|(?P<kw>\b[A-Za-z]\w*\b)"
    )

    def repl(m: re.Match) -> str:
        if m.lastgroup == "comment":
            return style(m.group(), fg="brightblack")
        if m.lastgroup == "str":
            return style(m.group(), fg="green")
        if m.lastgroup == "num":
            return style(m.group(), fg="yellow")
        if m.lastgroup == "kw" and m.group().upper() in kw:
            return style(m.group(), fg="cyan", bold=True)
        return m.group()

    return pattern.sub(repl, code)


def _highlight_shell(code: str, level: str) -> str:
    kw = _HIGHLIGHT_KEYWORDS["shell"]
    pattern = re.compile(
        r"(?P<comment>#[^\n]*)"
        r"|(?P<str>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')"
        r"|(?P<var>\$\w+|\$\{[^}]*\})"
        r"|(?P<kw>\b[A-Za-z_]\w*\b)"
    )

    def repl(m: re.Match) -> str:
        if m.lastgroup == "comment":
            return style(m.group(), fg="brightblack")
        if m.lastgroup == "str":
            return style(m.group(), fg="green")
        if m.lastgroup == "var":
            return style(m.group(), fg="yellow")
        if m.lastgroup == "kw" and m.group() in kw:
            return style(m.group(), fg="cyan", bold=True)
        return m.group()

    return pattern.sub(repl, code)


_HIGHLIGHTERS = {
    "python": _highlight_python,
    "json": _highlight_json,
    "sql": _highlight_sql,
    "shell": _highlight_shell,
}


def highlight(code: str, language: str = "python") -> str:
    """对源代码做基础语法高亮（关键字/字符串/注释/数字着色）。"""
    fn = _HIGHLIGHTERS.get(language.lower())
    if fn is None:
        return code
    return fn(code, COLOR_LEVEL)


# ─────────────────────────────────────────────────────────────────────────────
# 按键解析
# ─────────────────────────────────────────────────────────────────────────────

class Key:
    """解析后的按键事件。``name`` 为语义名（up/down/enter/...），
    ``char`` 为可打印字符。"""

    #: 特殊序列 → 语义名
    _SEQ_MAP = {
        b"\r": "enter", b"\n": "enter", b"\t": "tab", b"\x7f": "backspace",
        b"\x1b": "esc", b" ": "space", b"\x03": "ctrl-c",
        b"\x1b[A": "up", b"\x1b[B": "down", b"\x1b[C": "right", b"\x1b[D": "left",
        b"\x1b[H": "home", b"\x1b[F": "end", b"\x1bOH": "home", b"\x1bOF": "end",
        b"\x1b[3~": "delete", b"\x1b[Z": "shift-tab",
        b"\x1bOP": "f1", b"\x1bOQ": "f2", b"\x1bOR": "f3", b"\x1bOS": "f4",
    }

    def __init__(self, raw: bytes):
        self.raw = raw
        if raw in self._SEQ_MAP:
            self.name = self._SEQ_MAP[raw]
            self.char = ""
        elif len(raw) == 1 and raw[0] == 0x03:
            self.name = "ctrl-c"
            self.char = ""
        elif len(raw) == 1 and 1 <= raw[0] <= 26:
            self.name = f"ctrl-{chr(ord('a') + raw[0] - 1)}"
            self.char = ""
        else:
            try:
                self.char = raw.decode("utf-8")
                self.name = self.char
            except UnicodeDecodeError:
                self.char = ""
                self.name = "unknown"

    @classmethod
    def parse(cls, data: bytes) -> List["Key"]:
        """把一次 read 到的字节串拆成 Key 列表。"""
        keys: List[Key] = []
        buf = data
        # 长序列优先匹配，避免 "\x1b" 抢先吞掉 "\x1b[B" 等组合键
        ordered = sorted(cls._SEQ_MAP.keys(), key=len, reverse=True)
        while buf:
            hit = None
            for seq in ordered:
                if buf.startswith(seq):
                    hit = seq
                    break
            if hit is not None:
                keys.append(Key(hit))
                buf = buf[len(hit):]
            else:
                # 按字符消费（尽量按 UTF-8 解码）
                ch = buf[:1]
                try:
                    keys.append(Key(ch))
                    buf = buf[1:]
                except Exception:  # pragma: no cover
                    buf = buf[1:]
        return keys

    def __repr__(self) -> str:  # pragma: no cover
        return f"Key({self.name!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Key):
            return self.name == other.name
        return NotImplemented


# ─────────────────────────────────────────────────────────────────────────────
# ANSI 解析器与虚拟终端缓冲
# ─────────────────────────────────────────────────────────────────────────────

class _Event:
    """ANSI 解析事件基类。"""

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}()"


class TextEvent(_Event):
    """普通可打印文本。"""

    def __init__(self, text: str):
        self.text = text


class CursorMoveEvent(_Event):
    """光标移动事件（行列从 1 开始）。"""

    def __init__(self, row: int, col: int, relative: bool = False):
        self.row = row
        self.col = col
        self.relative = relative


class ClearEvent(_Event):
    """清屏/清行事件。mode: 0=到末尾 1=到开头 2=全部。"""

    def __init__(self, what: str, mode: int):
        self.what = what  # "screen" / "line"
        self.mode = mode


class ColorEvent(_Event):
    """SGR 颜色/样式事件。params 为整数参数列表。"""

    def __init__(self, params: List[int]):
        self.params = params


class ScrollEvent(_Event):
    """设置滚动区域（DECSTBM）。"""

    def __init__(self, top: int, bottom: int):
        self.top = top
        self.bottom = bottom


class ModeEvent(_Event):
    """终端模式开关（如鼠标追踪）。set=True 表示开启。"""

    def __init__(self, mode: int, on: bool):
        self.mode = mode
        self.on = on


class AnsiParser:
    """解析 ANSI 转义序列，产出事件流。"""

    _CSI_RE = re.compile(r"\x1b\[([0-9;?]*)([ -/]*)([@-~])")
    _OSC_RE = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
    _TWO_BYTE_RE = re.compile(r"\x1b[@-Z\\-_]")

    def parse(self, text: str) -> List[_Event]:
        """解析一段文本，返回事件列表。"""
        events: List[_Event] = []
        pos = 0
        pattern = re.compile(
            self._OSC_RE.pattern + "|" + self._CSI_RE.pattern + "|"
            + self._TWO_BYTE_RE.pattern
        )
        for m in pattern.finditer(text):
            if m.start() > pos:
                events.append(TextEvent(text[pos:m.start()]))
            token = m.group(0)
            if token.startswith("\x1b["):
                self._parse_csi(token, events)
            # OSC / 两字节转义直接忽略（不产生事件）
            pos = m.end()
        if pos < len(text):
            events.append(TextEvent(text[pos:]))
        return events

    def _parse_csi(self, token: str, events: List[_Event]) -> None:
        m = self._CSI_RE.match(token)
        if not m:
            return
        params_str, _inter, final = m.group(1), m.group(2), m.group(3)
        private = params_str.startswith("?")
        nums: List[int] = []
        for part in params_str.lstrip("?").split(";"):
            if part == "":
                nums.append(0)
            else:
                try:
                    nums.append(int(part))
                except ValueError:
                    nums.append(0)
        n = nums[0] if nums else 0
        if final == "A":
            events.append(CursorMoveEvent(-(n or 1), 0, relative=True))
        elif final == "B":
            events.append(CursorMoveEvent(n or 1, 0, relative=True))
        elif final == "C":
            events.append(CursorMoveEvent(0, n or 1, relative=True))
        elif final == "D":
            events.append(CursorMoveEvent(0, -(n or 1), relative=True))
        elif final == "H" or final == "f":
            events.append(CursorMoveEvent(nums[0] or 1, nums[1] or 1))
        elif final == "J":
            events.append(ClearEvent("screen", n))
        elif final == "K":
            events.append(ClearEvent("line", n))
        elif final == "m":
            events.append(ColorEvent(nums))
        elif final == "r":
            events.append(ScrollEvent(nums[0] or 1, nums[1] or 24))
        elif final in ("h", "l") and private:
            events.append(ModeEvent(nums[0], on=(final == "h")))
        # s/u（保存/恢复光标）等其余序列忽略


class TerminalBuffer:
    """虚拟终端缓冲区：把 ANSI 事件流应用到网格屏幕上。"""

    def __init__(self, rows: int = 24, cols: int = 80):
        self.rows = rows
        self.cols = cols
        self.grid = [[" "] * cols for _ in range(rows)]
        self.cursor_row = 0
        self.cursor_col = 0
        self._parser = AnsiParser()

    def feed(self, text: str) -> None:
        """喂入一段可能含 ANSI 的输出并更新屏幕。"""
        for ev in self._parser.parse(text):
            self._apply(ev)

    def _apply(self, ev: _Event) -> None:
        if isinstance(ev, TextEvent):
            for ch in ev.text:
                if ch == "\n":
                    self.cursor_row += 1
                    self.cursor_col = 0
                elif ch == "\r":
                    self.cursor_col = 0
                else:
                    if self.cursor_col >= self.cols:
                        self.cursor_col = 0
                        self.cursor_row += 1
                    if 0 <= self.cursor_row < self.rows:
                        self.grid[self.cursor_row][self.cursor_col] = ch
                    self.cursor_col += 1
        elif isinstance(ev, CursorMoveEvent):
            if ev.relative:
                self.cursor_row = max(0, min(self.rows - 1,
                                             self.cursor_row + ev.row))
                self.cursor_col = max(0, min(self.cols - 1,
                                             self.cursor_col + ev.col))
            else:
                self.cursor_row = max(0, min(self.rows - 1, ev.row - 1))
                self.cursor_col = max(0, min(self.cols - 1, ev.col - 1))
        elif isinstance(ev, ClearEvent):
            if ev.what == "screen":
                self.grid = [[" "] * self.cols for _ in range(self.rows)]
                if ev.mode == 2:
                    self.cursor_row, self.cursor_col = 0, 0
        elif isinstance(ev, ColorEvent):
            # 颜色属性暂存：默认不影响字符格，这里仅占位以便扩展
            pass

    def render(self) -> str:
        """把当前屏幕渲染成多行字符串。"""
        return "\n".join("".join(row).rstrip() for row in self.grid)


# ─────────────────────────────────────────────────────────────────────────────
# 事件循环
# ─────────────────────────────────────────────────────────────────────────────

class EventLoop:
    """主事件循环：定时器 + 事件订阅/发布。

    定时器基于单调时钟，测试时可替换 ``now_func``。
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[..., Any]]] = {}
        self._timers: Dict[int, Dict[str, Any]] = {}
        self._seq = 0
        self.now_func: Callable[[], float] = time.monotonic

    # 事件总线
    def on(self, event: str, fn: Callable[..., Any]) -> None:
        """订阅事件。"""
        self._handlers.setdefault(event, []).append(fn)

    def off(self, event: str, fn: Callable[..., Any]) -> None:
        """取消订阅。"""
        if event in self._handlers and fn in self._handlers[event]:
            self._handlers[event].remove(fn)

    def emit(self, event: str, *data: Any) -> None:
        """发布事件，同步调用所有订阅者。"""
        for fn in list(self._handlers.get(event, ())):
            fn(*data)

    # 定时器
    def set_timeout(self, fn: Callable[[], Any], ms: float) -> int:
        """一次性定时器，返回句柄。"""
        self._seq += 1
        self._timers[self._seq] = {
            "fn": fn, "due": self.now_func() + ms,
            "interval": None,
        }
        return self._seq

    def set_interval(self, fn: Callable[[], Any], ms: float) -> int:
        """重复定时器，返回句柄。"""
        self._seq += 1
        self._timers[self._seq] = {
            "fn": fn, "due": self.now_func() + ms,
            "interval": ms,
        }
        return self._seq

    def cancel(self, handle: int) -> None:
        """取消定时器。"""
        self._timers.pop(handle, None)

    def pump(self) -> int:
        """执行所有到期定时器，返回触发次数。"""
        now = self.now_func()
        fired = 0
        for handle, t in list(self._timers.items()):
            if t["due"] <= now:
                fn = t["fn"]
                fn()
                fired += 1
                if t["interval"] is not None:
                    t["due"] = now + t["interval"]
                else:
                    self._timers.pop(handle, None)
        return fired

    def run(self, idle: float = 0.05) -> None:  # pragma: no cover
        """持续运行直到收到 KeyboardInterrupt。"""
        try:
            while True:
                self.pump()
                time.sleep(idle)
        except KeyboardInterrupt:
            self.emit("interrupt")


# ─────────────────────────────────────────────────────────────────────────────
# PTY 终端模拟
# ─────────────────────────────────────────────────────────────────────────────

class PTY:
    """伪终端：在子进程中运行命令，主进程通过 master fd 读写。"""

    def __init__(self) -> None:
        self.master_fd: Optional[int] = None
        self.pid: Optional[int] = None
        self._exit_code: Optional[int] = None

    def spawn(self, cmd, **kwargs: Any) -> "PTY":
        """fork 子进程并在新会话中执行 cmd（str 或 list）。"""
        pid, master_fd = _pty_mod.fork()
        if pid == 0:  # 子进程
            # 解除从父进程继承的信号阻塞/忽略，确保 SIGTERM/SIGHUP 等能正常终止子进程
            try:
                signal.pthread_sigmask(
                    signal.SIG_UNBLOCK,
                    [signal.SIGTERM, signal.SIGHUP, signal.SIGINT],
                )
            except (AttributeError, OSError):
                pass
            for _s in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
                try:
                    signal.signal(_s, signal.SIG_DFL)
                except (OSError, ValueError):
                    pass
            os.environ.setdefault("TERM", "xterm")
            if isinstance(cmd, str):
                args = ["/bin/sh", "-c", cmd]
            else:
                args = list(cmd)
            try:
                os.execvp(args[0], args)
            except Exception:  # pragma: no cover
                os._exit(127)
        self.pid = pid
        self.master_fd = master_fd
        return self

    def set_size(self, rows: int, cols: int) -> None:
        """设置 PTY 窗口大小。"""
        if self.master_fd is None:
            raise RuntimeError("PTY 尚未 spawn")
        fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ,
                    struct.pack("HHHH", rows, cols, 0, 0))

    def read(self, n: int = 4096, timeout: Optional[float] = None) -> bytes:
        """读取子进程输出，阻塞或带超时。"""
        if self.master_fd is None:
            return b""
        if timeout is not None:
            r, _, _ = select.select([self.master_fd], [], [], timeout)
            if not r:
                return b""
        return os.read(self.master_fd, n)

    def write(self, data) -> int:
        """向子进程写入输入。"""
        if self.master_fd is None:
            return 0
        if isinstance(data, str):
            data = data.encode("utf-8")
        return os.write(self.master_fd, data)

    def wait(self) -> int:
        """等待子进程结束并返回退出码。"""
        if self.pid is None:
            return -1
        _, status = os.waitpid(self.pid, 0)
        if os.WIFEXITED(status):
            self._exit_code = os.WEXITSTATUS(status)
        else:
            self._exit_code = -os.WTERMSIG(status)
        return self._exit_code

    def poll(self) -> Optional[int]:
        """非阻塞地检查进程是否结束；未结束返回 None。"""
        if self.pid is None:
            return -1
        try:
            pid, status = os.waitpid(self.pid, os.WNOHANG)
        except ChildProcessError:
            return self._exit_code if self._exit_code is not None else 0
        if pid == 0:
            return None
        if os.WIFEXITED(status):
            self._exit_code = os.WEXITSTATUS(status)
        else:
            self._exit_code = -os.WTERMSIG(status)
        return self._exit_code

    def terminate(self, sig: int = signal.SIGKILL) -> None:
        """强制终止子进程（默认 SIGKILL，不可被阻塞/忽略）。"""
        if self.pid is not None and self.poll() is None:
            os.kill(self.pid, sig)

    def close(self) -> None:
        """关闭主设备。"""
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None


def pty_spawn(cmd, **kwargs: Any) -> PTY:
    """在 PTY 中启动命令并返回 PTY 对象。"""
    return PTY().spawn(cmd, **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# 布局系统（Flexbox 风格）
# ─────────────────────────────────────────────────────────────────────────────

class Rect:
    """矩形区域。"""

    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self) -> str:  # pragma: no cover
        return f"Rect(x={self.x}, y={self.y}, w={self.w}, h={self.h})"


class Widget:
    """所有 TUI 组件的基类。"""

    def __init__(self, name: str = ""):
        self.name = name
        self.focus = False
        self.visible = True
        self.flex_grow = 0
        self.flex_shrink = 1
        self.flex_basis = 0
        self.min_width = 0
        self.min_height = 1
        self.margin = 0
        self.padding = 0
        self.rect = Rect()

    def draw(self, width: int, height: int) -> List[str]:  # pragma: no cover
        """返回高 height 行、宽 width 列的渲染结果。"""
        return [" " * width] * height

    def handle_key(self, key: Key) -> bool:  # pragma: no cover
        """处理按键，返回是否已消费。"""
        return False

    def handle_mouse(self, x: int, y: int, button: int) -> None:  # pragma: no cover
        """处理鼠标事件。"""

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.__class__.__name__} {self.name!r}>"


class Box(Widget):
    """弹性盒子容器基类。"""

    #: 主轴方向："row"（水平）或 "column"（垂直）
    direction: str = "row"

    def __init__(self, name: str = "", children: Optional[List[Widget]] = None,
                 justify_content: str = "start", align_items: str = "stretch"):
        super().__init__(name)
        self.children: List[Widget] = children or []
        self.justify_content = justify_content
        self.align_items = align_items

    def add(self, child: Widget) -> Widget:
        self.children.append(child)
        return child

    def compute(self, width: int, height: int) -> List[Tuple[Widget, Rect]]:
        """按 flex 规则把子控件排布到 (width, height) 区域内。"""
        is_row = self.direction == "row"
        main_axis_size = width if is_row else height
        cross_axis_size = height if is_row else width

        n = len(self.children)
        if n == 0:
            return []

        # 1) 分配固定 basis 与最小尺寸
        used = 0
        grow_units = 0
        for ch in self.children:
            basis = ch.flex_basis or (ch.min_width if is_row else ch.min_height)
            ch._basis = basis
            used += basis
            grow_units += ch.flex_grow

        # 2) 把剩余空间按 flex_grow 分配
        remaining = main_axis_size - used
        rects: List[Tuple[Widget, Rect]] = []
        sizes = [0] * n
        for i, ch in enumerate(self.children):
            extra = 0
            if grow_units > 0 and remaining > 0:
                extra = int(round(remaining * ch.flex_grow / grow_units))
            sizes[i] = ch._basis + extra

        # 3) 主轴对齐
        total = sum(sizes)
        if self.justify_content == "end":
            offset = main_axis_size - total
        elif self.justify_content == "center":
            offset = (main_axis_size - total) // 2
        elif self.justify_content == "space_between" and n > 1:
            offset = 0
        elif self.justify_content == "space_around" and n > 1:
            gap = total / n
            offset = 0
        else:
            offset = 0

        cursor = offset
        gaps: List[float] = [0.0] * n
        if self.justify_content == "space_between" and n > 1 and total < main_axis_size:
            gap = (main_axis_size - total) / (n - 1)
            gaps = [gap] * n
            gaps[-1] = 0
        elif self.justify_content == "space_around" and n > 1 and total < main_axis_size:
            gap = (main_axis_size - total) / (2 * n)
            gaps = [gap * 2] * n
            gaps[0] = gap
            gaps[-1] = gap

        for i, ch in enumerate(self.children):
            main = max(0, int(sizes[i]))
            if self.align_items == "stretch":
                cross = cross_axis_size
            else:
                cross = ch.min_height if is_row else ch.min_width
            if self.align_items == "start":
                cross_off = 0
            elif self.align_items == "center":
                cross_off = (cross_axis_size - cross) // 2
            elif self.align_items == "end":
                cross_off = cross_axis_size - cross
            else:  # stretch
                cross_off = 0
            if is_row:
                rect = Rect(int(cursor), int(cross_off), main, cross)
            else:
                rect = Rect(int(cross_off), int(cursor), cross, main)
            ch.rect = rect
            rects.append((ch, rect))
            cursor += main + gaps[i]
        return rects

    def draw(self, width: int, height: int) -> List[str]:  # pragma: no cover
        lines = [""] * height
        for child, rect in self.compute(width, height):
            for j, row in enumerate(child.draw(rect.w, rect.h)):
                if rect.y + j < height:
                    line = lines[rect.y + j]
                    pad = rect.x
                    line = line[:pad] + row + line[pad + ansi_len(row):]
                    lines[rect.y + j] = line
        return lines


class HBox(Box):
    """水平排列的弹性容器。"""
    direction = "row"


class VBox(Box):
    """垂直排列的弹性容器。"""
    direction = "column"


# ─────────────────────────────────────────────────────────────────────────────
# TUI 组件
# ─────────────────────────────────────────────────────────────────────────────

class TextBox(Widget):
    """单行/多行文本输入框。"""

    def __init__(self, text: str = "", multiline: bool = False, name: str = "textbox"):
        super().__init__(name)
        self.text = text
        self.multiline = multiline
        self.cursor = len(text)
        self.min_width = 10

    def insert(self, ch: str) -> None:
        self.text = self.text[:self.cursor] + ch + self.text[self.cursor:]
        self.cursor += 1

    def backspace(self) -> None:
        if self.cursor > 0:
            self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
            self.cursor -= 1

    def handle_key(self, key: Key) -> bool:
        if key.name == "left":
            self.cursor = max(0, self.cursor - 1)
        elif key.name == "right":
            self.cursor = min(len(self.text), self.cursor + 1)
        elif key.name == "backspace":
            self.backspace()
        elif key.char and key.name not in ("esc", "ctrl-c", "enter"):
            self.insert(key.char)
        else:
            return False
        return True

    def draw(self, width: int, height: int) -> List[str]:
        visible = self.text[:]
        left = max(0, self.cursor - width + 1)
        visible = visible[left:left + width]
        cursor_vis = style("│", fg="cyan")
        line = visible[:self.cursor - left] + cursor_vis + visible[self.cursor - left:]
        return [visible_pad(line, width, "left")] * max(1, height)


class ListBox(Widget):
    """可滚动列表，选中项高亮。"""

    def __init__(self, items: Optional[List[str]] = None, name: str = "listbox"):
        super().__init__(name)
        self.items: List[str] = list(items or [])
        self.selected = 0
        self.offset = 0

    def handle_key(self, key: Key) -> bool:
        if key.name == "up":
            self.selected = max(0, self.selected - 1)
            return True
        if key.name == "down":
            self.selected = min(len(self.items) - 1, self.selected + 1)
            return True
        return False

    def draw(self, width: int, height: int) -> List[str]:
        if self.selected < self.offset:
            self.offset = self.selected
        elif self.selected >= self.offset + height:
            self.offset = self.selected - height + 1
        out = []
        for i in range(height):
            idx = self.offset + i
            if 0 <= idx < len(self.items):
                txt = self.items[idx]
                if idx == self.selected:
                    txt = style(visible_pad(txt, width), bg="blue", fg="white")
                else:
                    txt = visible_pad(txt, width)
                out.append(txt)
            else:
                out.append(" " * width)
        return out


class Button(Widget):
    """按钮：回车/空格触发回调。"""

    def __init__(self, label: str = "OK", on_click: Optional[Callable[[], Any]] = None,
                 name: str = "button"):
        super().__init__(name)
        self.label = label
        self.on_click = on_click or (lambda: None)
        self.flex_basis = len(label) + 4

    def handle_key(self, key: Key) -> bool:
        if key.name in ("enter", "space"):
            self.on_click()
            return True
        return False

    def draw(self, width: int, height: int) -> List[str]:
        box = f"[ {self.label} ]"
        if self.focus:
            box = style(box, fg="black", bg="cyan", bold=True)
        return [visible_pad(box, width, "center")] * max(1, height)


class Menu(Widget):
    """菜单项（可带子菜单与快捷键）。"""

    def __init__(self, items: Optional[List[Tuple[str, str]]] = None,
                 name: str = "menu"):
        super().__init__(name)
        #: items: (label, shortcut)
        self.items = list(items or [])

    def draw(self, width: int, height: int) -> List[str]:
        parts = []
        for label, shortcut in self.items:
            parts.append(f"{label} {style(f'({shortcut})', fg='brightblack')}")
        return [visible_pad("  ".join(parts), width)] * max(1, height)


class Tabs(Widget):
    """标签页切换。"""

    def __init__(self, tabs: Optional[List[str]] = None, name: str = "tabs"):
        super().__init__(name)
        self.tabs = list(tabs or [])
        self.active = 0

    def handle_key(self, key: Key) -> bool:
        if key.name == "right":
            self.active = (self.active + 1) % len(self.tabs) if self.tabs else 0
            return True
        if key.name == "left":
            self.active = (self.active - 1) % len(self.tabs) if self.tabs else 0
            return True
        return False

    def draw(self, width: int, height: int) -> List[str]:
        parts = []
        for i, tab in enumerate(self.tabs):
            label = f" {tab} "
            if i == self.active:
                parts.append(style(label, bg="blue", fg="white", bold=True))
            else:
                parts.append(label)
        return [visible_pad("".join(parts), width)] * max(1, height)


class SplitPanel(Widget):
    """分割面板：按比例把区域分给两个子面板。"""

    def __init__(self, left: Widget, right: Widget, horizontal: bool = True,
                 ratio: float = 0.5, name: str = "split"):
        super().__init__(name)
        self.left = left
        self.right = right
        self.horizontal = horizontal
        self.ratio = ratio

    def draw(self, width: int, height: int) -> List[str]:
        if self.horizontal:
            w = max(1, int(width * self.ratio))
            left_lines = self.left.draw(w, height)
            right_lines = self.right.draw(width - w, height)
            return [l + r for l, r in zip(left_lines, right_lines)]
        top = self.left.draw(width, max(1, int(height * self.ratio)))
        bottom = self.right.draw(width, height - len(top))
        return top + bottom


class StatusBar(Widget):
    """底部状态栏：左/右两段文本。"""

    def __init__(self, left: str = "", right: str = "", name: str = "statusbar"):
        super().__init__(name)
        self.left = left
        self.right = right

    def draw(self, width: int, height: int) -> List[str]:
        gap = max(0, width - ansi_len(self.left) - ansi_len(self.right))
        line = style(self.left + " " * gap + self.right,
                     bg="blue", fg="white")
        return [visible_pad(line, width)] * max(1, height)


class Dialog(Widget):
    """模态对话框。"""

    def __init__(self, title: str, body: str = "",
                 buttons: Optional[List[str]] = None, name: str = "dialog"):
        super().__init__(title or name)
        self.title = title
        self.body = body
        self.buttons = list(buttons or ["OK"])
        self.choice: Optional[str] = None

    def draw(self, width: int, height: int) -> List[str]:
        inner_w = max(10, min(width - 4, 60))
        lines = [Panel(self.body, title=self.title, border_style="rounded")]
        bar = "  ".join(f"[{b}]" for b in self.buttons)
        lines.append(visible_pad(bar, inner_w, "center"))
        return ([""] * ((height - len(lines)) // 2) + lines
                + [""] * (height - len(lines) - (height - len(lines)) // 2))


# ─────────────────────────────────────────────────────────────────────────────
# 交互式提示（非终端环境自动降级）
# ─────────────────────────────────────────────────────────────────────────────

def _is_interactive() -> bool:
    return bool(sys.stdin and sys.stdin.isatty() and sys.stdout.isatty())


def prompt_input(label: str, default: Optional[str] = None,
                 validator: Optional[Callable[[str], bool]] = None,
                 mask: Optional[str] = None) -> str:
    """读取一行输入；可带校验与密码掩码。非终端返回 default。"""
    if not _is_interactive():
        return default if default is not None else ""
    while True:
        try:
            if mask:
                import getpass
                value = getpass.getpass(label)
            else:
                suffix = f" [{default}]" if default is not None else ""
                value = input(f"{label}{suffix}: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise
        if not value and default is not None:
            value = default
        if validator is None or validator(value):
            return value
        print("输入无效，请重试。")


def prompt_select(label: str, options: List[str], default: int = 0) -> int:
    """上下箭头选择；非终端返回 default。"""
    if not _is_interactive():
        return default
    import termios as _t
    tty = sys.stdin.fileno()
    old = _t.tcgetattr(tty)
    sel = default
    try:
        # cbreak 模式
        new = old.copy()
        new[3] &= ~_t.ECHO & ~_t.ICANON
        _t.tcsetattr(tty, _t.TCSANOW, new)
        while True:
            sys.stdout.write(f"\r{label} {options[sel]} ")
            sys.stdout.flush()
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    sel = (sel - 1) % len(options)
                elif seq == "[B":
                    sel = (sel + 1) % len(options)
            elif ch in ("\r", "\n"):
                break
        return sel
    finally:
        _t.tcsetattr(tty, _t.TCSANOW, old)


def prompt_multiselect(label: str, options: List[str],
                       defaults: Optional[List[int]] = None) -> List[int]:
    """空格勾选多项；非终端返回 defaults 或首项。"""
    if not _is_interactive():
        return list(defaults or [0])
    selected = set(defaults or [])
    sel = 0
    import termios as _t
    tty = sys.stdin.fileno()
    old = _t.tcgetattr(tty)
    try:
        new = old.copy()
        new[3] &= ~_t.ECHO & ~_t.ICANON
        _t.tcsetattr(tty, _t.TCSANOW, new)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    sel = (sel - 1) % len(options)
                elif seq == "[B":
                    sel = (sel + 1) % len(options)
            elif ch == " ":
                if sel in selected:
                    selected.discard(sel)
                else:
                    selected.add(sel)
            elif ch in ("\r", "\n"):
                break
        return sorted(selected)
    finally:
        _t.tcsetattr(tty, _t.TCSANOW, old)


def prompt_confirm(label: str, default: bool = True) -> bool:
    """y/n 确认；非终端返回 default。"""
    if not _is_interactive():
        return default
    hint = "Y/n" if default else "y/N"
    try:
        ans = input(f"{label} [{hint}]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return default
    if not ans:
        return default
    return ans in ("y", "yes")


def prompt_password(label: str, confirm: bool = False) -> str:
    """密码输入，可选二次确认；非终端返回空串。"""
    if not _is_interactive():
        return ""
    import getpass
    p1 = getpass.getpass(label)
    if confirm:
        p2 = getpass.getpass("再次输入: ")
        while p1 != p2:
            print("两次输入不一致。")
            p1 = getpass.getpass(label)
            p2 = getpass.getpass("再次输入: ")
    return p1
