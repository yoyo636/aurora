# -*- coding: utf-8 -*-
"""
Aurora v3.2.0 CLI/TUI 框架
纯 Python 标准库实现，使用 ANSI 转义码。
提供终端工具（颜色、spinner、进度条、表格、树、交互提示）和 TUI 框架。
"""

import os
import sys
import time
import shutil
import threading
import unicodedata
from typing import Callable, List, Optional, Tuple, Dict, Any


# ============================================================
# 环境检测与基础工具
# ============================================================

def _supports_color() -> bool:
    """检测当前环境是否支持颜色输出。NO_COLOR 环境变量或非 TTY 时禁用。"""
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    return True


def _term_size() -> Tuple[int, int]:
    """获取终端尺寸，默认 80x24。"""
    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
        return size.columns, size.lines
    except Exception:
        return 80, 24


# ANSI 码正则（用于 strip_ansi 和显示宽度计算）
import re
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07|\x1b[()][AB012]")


def strip_ansi(text: str) -> str:
    """移除文本中的 ANSI 转义码。"""
    return _ANSI_RE.sub("", text)


def _char_width(ch: str) -> int:
    """估算单个字符的显示宽度（东亚宽字符算 2）。"""
    if ch == "\n":
        return 1
    try:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            return 2
    except Exception:
        pass
    return 1


def display_width(text: str) -> int:
    """计算字符串的显示宽度（先去除 ANSI 码）。"""
    plain = strip_ansi(text)
    width = 0
    for ch in plain:
        width += _char_width(ch)
    return width


# ============================================================
# 颜色与样式
# ============================================================

_COLOR_MAP = {
    "black": 30, "red": 31, "green": 32, "yellow": 33,
    "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
}

# 样式码
_STYLE_MAP = {
    "bold": "1", "dim": "2", "italic": "3",
    "underline": "4", "blink": "5", "reverse": "7",
    "strikethrough": "9",
}


def fg(text: str, color: str) -> str:
    """前景色着色。color: black/red/green/yellow/blue/magenta/cyan/white。"""
    if not _supports_color():
        return text
    code = _COLOR_MAP.get(color)
    if code is None:
        return text
    return f"\x1b[{code}m{text}\x1b[0m"


def bg(text: str, color: str) -> str:
    """背景色着色。"""
    if not _supports_color():
        return text
    code = _COLOR_MAP.get(color)
    if code is None:
        return text
    return f"\x1b[{code + 10}m{text}\x1b[0m"


def bold(text: str) -> str:
    """粗体。"""
    if not _supports_color():
        return text
    return f"\x1b[1m{text}\x1b[22m"


def underline(text: str) -> str:
    """下划线。"""
    if not _supports_color():
        return text
    return f"\x1b[4m{text}\x1b[24m"


def dim(text: str) -> str:
    """暗淡。"""
    if not _supports_color():
        return text
    return f"\x1b[2m{text}\x1b[22m"


def italic(text: str) -> str:
    """斜体。"""
    if not _supports_color():
        return text
    return f"\x1b[3m{text}\x1b[23m"


def strikethrough(text: str) -> str:
    """删除线。"""
    if not _supports_color():
        return text
    return f"\x1b[9m{text}\x1b[29m"


def rgb(text: str, r: int, g: int, b: int) -> str:
    """24 位真彩色前景色。"""
    if not _supports_color():
        return text
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"


def style(text: str, *styles: str) -> str:
    """组合多种样式。styles 可以是颜色名（fg）或 bold/underline 等。"""
    if not _supports_color():
        return text
    codes = []
    for s in styles:
        if s in _COLOR_MAP:
            codes.append(str(_COLOR_MAP[s]))
        elif s in _STYLE_MAP:
            codes.append(_STYLE_MAP[s])
    if not codes:
        return text
    return f"\x1b[{';'.join(codes)}m{text}\x1b[0m"


# ============================================================
# 加载动画 Spinner
# ============================================================

_SPINNER_FRAMES = {
    "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    "lines": ["|", "/", "-", "\\"],
    "blocks": ["▖", "▘", "▝", "▗"],
    "arrows": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
    "bouncing_bar": ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]", "[    ]"],
    "clock": ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"],
}


class Spinner:
    """终端加载动画。

    用法：
        with Spinner('处理中') as s:
            ...
    或：
        s = Spinner('加载中'); s.start(); ...; s.stop()
    非 TTY 环境降级为简单文本输出。
    """

    def __init__(self, text: str = "加载中", style: str = "dots"):
        self.text = text
        self.frames = _SPINNER_FRAMES.get(style, _SPINNER_FRAMES["dots"])
        self._idx = 0
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False
        self._is_tty = sys.stdout.isatty() if hasattr(sys.stdout, "isatty") else False

    def start(self) -> "Spinner":
        """启动 spinner。"""
        self._running = True
        if self._is_tty:
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()
        else:
            # 非 TTY：直接输出初始文本（带换行）
            sys.stderr.write(f"[*] {self.text}\n")
            sys.stderr.flush()
        return self

    def _spin(self):
        """动画循环。"""
        while not self._stop_event.is_set():
            frame = self.frames[self._idx % len(self.frames)]
            line = f"\r{frame} {self.text}"
            sys.stderr.write(line)
            sys.stderr.flush()
            self._idx += 1
            time.sleep(0.1)

    def update(self, text: str):
        """更新提示文本。"""
        self.text = text

    def stop(self, success: bool = True, message: Optional[str] = None):
        """停止 spinner。"""
        self._running = False
        if self._is_tty:
            self._stop_event.set()
            if self._thread:
                self._thread.join(timeout=0.5)
            # 清行
            sys.stderr.write("\r" + " " * (display_width(self.text) + 10) + "\r")
        if message is None:
            message = self.text
        if success:
            marker = "✓"
            color = "green"
        else:
            marker = "✗"
            color = "red"
        line = f"{fg(marker, color)} {message}\n"
        sys.stderr.write(line)
        sys.stderr.flush()

    def __enter__(self) -> "Spinner":
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._running:
            self.stop(success=(exc_type is None))
        return False


# ============================================================
# 进度条
# ============================================================

class ProgressBar:
    """单段进度条。

    显示：百分比、进度条、已完成/总数、ETA、速度。
    """

    def __init__(self, total: int, prefix: str = "", width: int = 30,
                 show_eta: bool = True, show_speed: bool = True):
        self.total = max(1, total)
        self.prefix = prefix
        self.width = width
        self.show_eta = show_eta
        self.show_speed = show_speed
        self.current = 0
        self._start_time = time.time()
        self._is_tty = sys.stdout.isatty() if hasattr(sys.stdout, "isatty") else False
        self._finished = False

    def _format_eta(self, seconds: float) -> str:
        """格式化为可读时间。"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        m, s = divmod(int(seconds), 60)
        if m < 60:
            return f"{m}m{s:02d}s"
        h, m = divmod(m, 60)
        return f"{h}h{m:02d}m"

    def render_line(self) -> str:
        """生成当前进度条字符串（不含换行）。"""
        ratio = min(1.0, self.current / self.total)
        filled = int(self.width * ratio)
        bar = "█" * filled + "░" * (self.width - filled)
        pct = f"{ratio * 100:5.1f}%"
        count = f"{self.current}/{self.total}"
        parts = [f"{self.prefix}", f"{pct}", f"[{bar}]", count]
        if self.show_speed and self.current > 0:
            elapsed = time.time() - self._start_time
            speed = self.current / max(elapsed, 0.001)
            parts.append(f"{speed:.1f}/s")
            if self.show_eta:
                remaining = (self.total - self.current) / max(speed, 0.001)
                parts.append(f"ETA {self._format_eta(remaining)}")
        return " ".join(parts)

    def update(self, current: int):
        """设置当前进度。"""
        self.current = max(0, min(self.total, current))
        self._draw()

    def advance(self, delta: int = 1):
        """前进 delta。"""
        self.update(self.current + delta)

    def _draw(self):
        """绘制到终端。"""
        line = self.render_line()
        if self._is_tty:
            sys.stderr.write("\r" + line)
            sys.stderr.flush()
        else:
            sys.stderr.write(line + "\n")
            sys.stderr.flush()

    def finish(self):
        """完成进度条。"""
        self.current = self.total
        self._finished = True
        self._draw()
        if self._is_tty:
            sys.stderr.write("\n")
            sys.stderr.flush()

    def __enter__(self) -> "ProgressBar":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._finished:
            self.finish()
        return False


class MultiProgress:
    """多段并行进度条。"""

    def __init__(self):
        self.bars: List[ProgressBar] = []

    def add(self, total: int, prefix: str = "", **kwargs) -> ProgressBar:
        """添加一个进度条。"""
        bar = ProgressBar(total, prefix=prefix, **kwargs)
        self.bars.append(bar)
        return bar

    def render(self) -> str:
        """渲染所有进度条为一个多行字符串。"""
        return "\n".join(b.render_line() for b in self.bars)

    def finish(self):
        """完成所有进度条。"""
        for b in self.bars:
            b.finish()

    def __enter__(self) -> "MultiProgress":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()
        return False


# ============================================================
# 表格
# ============================================================

_BORDER_STYLES = {
    # 字符: (tl, t, tr, l, r, ml, mr, bl, br, h, v)
    "rounded": ("╭", "─", "╮", "│", "│", "├", "┤", "╰", "╯", "─", "│"),
    "square":  ("┌", "─", "┐", "│", "│", "├", "┤", "└", "┘", "─", "│"),
    "thick":   ("┏", "━", "┓", "┃", "┃", "╂", "╂", "┗", "┛", "━", "┃"),
    "minimal": ("", "", "", "", "", "", "", "", "", "─", ""),
    "none":    None,
}

_ALIGN_CHARS = {"left": "<", "center": "^", "right": ">"}


class Table:
    """终端表格。

    支持多种边框样式、列对齐、ANSI 颜色内容。
    """

    def __init__(self, headers: List[str], rows: Optional[List[List[str]]] = None,
                 border_style: str = "rounded", align: Optional[List[str]] = None):
        self.headers = list(headers)
        self.rows: List[List[str]] = [list(r) for r in (rows or [])]
        self.border_style = border_style
        self.ncols = len(self.headers)
        # 每列对齐
        self.align = align or ["left"] * self.ncols

    def add_row(self, row: List[str]):
        """添加一行。"""
        self.rows.append(list(row))

    def _compute_widths(self) -> List[int]:
        """计算每列宽度（考虑 ANSI）。"""
        widths = [display_width(h) for h in self.headers]
        for row in self.rows:
            for i, cell in enumerate(row[: self.ncols]):
                widths[i] = max(widths[i], display_width(str(cell)))
        return widths

    def _pad_cell(self, text: str, width: int, align: str) -> str:
        """按对齐方式填充单元格（考虑 ANSI）。"""
        vis = display_width(text)
        pad = max(0, width - vis)
        if align == "right":
            return " " * pad + text
        if align == "center":
            left = pad // 2
            right = pad - left
            return " " * left + text + " " * right
        return text + " " * pad

    def render(self) -> str:
        """渲染为字符串。"""
        widths = self._compute_widths()
        style = _BORDER_STYLES.get(self.border_style)

        if style is None:
            # none: 无边框
            lines = [self._render_row(self.headers, widths, border=False)]
            for row in self.rows:
                lines.append(self._render_row(row, widths, border=False))
            return "\n".join(lines)

        tl, t, tr, l, r, ml, mr, bl, br, h, v = style

        if self.border_style == "minimal":
            # 最小化：只画横线
            lines = [self._render_row(self.headers, widths, v=" ")
                     if not v else self._render_row(self.headers, widths)]
            lines.append(h + h.join(h * (w + 2) for w in widths) + h)
            for row in self.rows:
                lines.append(self._render_row(row, widths))
            return "\n".join(lines)

        def hline(c_left, c_mid, c_right):
            inner = c_mid.join(h * (w + 2) for w in widths)
            return f"{c_left}{inner}{c_right}"

        lines = [hline(tl, t, tr)]
        lines.append(self._render_row(self.headers, widths, l, r, v))
        lines.append(hline(ml, h, mr))
        for row in self.rows:
            lines.append(self._render_row(row, widths, l, r, v))
        lines.append(hline(bl, h, br))
        return "\n".join(lines)

    def _render_row(self, row: List[str], widths: List[int],
                    l: str = "", r: str = "", v: str = "") -> str:
        cells = []
        for i in range(self.ncols):
            val = str(row[i]) if i < len(row) else ""
            cells.append(" " + self._pad_cell(val, widths[i], self.align[i]) + " ")
        if v:
            return v + v.join(cells) + r
        return "".join(cells)


# ============================================================
# 树状结构
# ============================================================

class TreeNode:
    """树节点。"""

    def __init__(self, name: str, children: Optional[List["TreeNode"]] = None,
                 icon: str = ""):
        self.name = name
        self.children: List[TreeNode] = list(children or [])
        self.icon = icon

    def add_child(self, node: "TreeNode") -> "TreeNode":
        """添加子节点。"""
        self.children.append(node)
        return node

    def render(self) -> str:
        """渲染整棵树为字符串。"""
        lines = []
        prefix = self.icon + " " if self.icon else ""
        lines.append(f"{prefix}{self.name}")
        self._render_children(lines, self.children, "")
        return "\n".join(lines)

    def _render_children(self, lines: List[str], children: List["TreeNode"], prefix: str):
        """递归渲染子节点。"""
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            connector = "└── " if is_last else "├── "
            icon = child.icon + " " if child.icon else ""
            lines.append(f"{prefix}{connector}{icon}{child.name}")
            extension = "    " if is_last else "│   "
            self._render_children(lines, child.children, prefix + extension)


# ============================================================
# 交互提示
# ============================================================

def _is_interactive() -> bool:
    return (hasattr(sys.stdin, "isatty") and sys.stdin.isatty()
            and hasattr(sys.stdout, "isatty") and sys.stdout.isatty())


def confirm(prompt: str, default: bool = False) -> bool:
    """y/N 确认提示。非 TTY 返回 default。"""
    if not _is_interactive():
        return default
    suffix = " [Y/n] " if default else " [y/N] "
    try:
        ans = input(prompt + suffix).strip().lower()
    except EOFError:
        return default
    if not ans:
        return default
    return ans.startswith("y")


def select(prompt: str, options: List[str], default_index: int = 0):
    """单选（方向键）。非 TTY 降级为编号输入。"""
    if not options:
        return None
    if not _is_interactive():
        # 非 TTY：尝试读编号
        print(prompt)
        for i, opt in enumerate(options):
            print(f"  {i + 1}. {opt}")
        try:
            raw = input(f"选择 [1-{len(options)}] (默认 {default_index + 1}): ").strip()
            idx = int(raw) - 1 if raw else default_index
        except (EOFError, ValueError):
            idx = default_index
        idx = max(0, min(len(options) - 1, idx))
        return options[idx]

    # 简单 TUI 选择（使用 readline 风格）
    idx = default_index
    try:
        import tty, termios
    except ImportError:
        return options[default_index]
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            # 重绘
            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.write(prompt + "\n")
            for i, opt in enumerate(options):
                marker = "▶ " if i == idx else "  "
                sys.stdout.write(f"{marker}{opt}\n")
            sys.stdout.flush()
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    idx = (idx - 1) % len(options)
                elif seq == "[B":
                    idx = (idx + 1) % len(options)
            elif ch in ("\r", "\n"):
                return options[idx]
            elif ch == "\x03":
                raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def multiselect(prompt: str, options: List[str],
                default_indices: Optional[List[int]] = None) -> List:
    """多选（空格勾选，Enter 确认）。非 TTY 降级为编号输入。"""
    if not options:
        return []
    selected = set(default_indices or [])
    if not _is_interactive():
        print(prompt)
        for i, opt in enumerate(options):
            mark = "x" if i in selected else " "
            print(f"  [{mark}] {i + 1}. {opt}")
        try:
            raw = input("输入编号（逗号分隔，回车结束）: ").strip()
            if raw:
                selected = set()
                for part in raw.split(","):
                    n = int(part.strip()) - 1
                    if 0 <= n < len(options):
                        selected.add(n)
        except (EOFError, ValueError):
            pass
        return [options[i] for i in sorted(selected)]

    try:
        import tty, termios
    except ImportError:
        return [options[i] for i in sorted(selected)]
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    idx = 0
    try:
        tty.setraw(fd)
        while True:
            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.write(prompt + " (空格勾选, Enter 确认)\n")
            for i, opt in enumerate(options):
                mark = "[x]" if i in selected else "[ ]"
                marker = "▶" if i == idx else " "
                sys.stdout.write(f"{marker} {mark} {opt}\n")
            sys.stdout.flush()
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    idx = (idx - 1) % len(options)
                elif seq == "[B":
                    idx = (idx + 1) % len(options)
            elif ch == " ":
                if idx in selected:
                    selected.discard(idx)
                else:
                    selected.add(idx)
            elif ch in ("\r", "\n"):
                return [options[i] for i in sorted(selected)]
            elif ch == "\x03":
                raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def input_prompt(prompt: str, default: Optional[str] = None,
                 validator: Optional[Callable[[str], Tuple[bool, str]]] = None) -> str:
    """带默认值和校验的输入。

    validator: (str) -> (是否合法, 错误消息)
    """
    suffix = f" [{default}] " if default else ": "
    while True:
        try:
            value = input(prompt + suffix).strip()
        except EOFError:
            value = ""
        if not value and default is not None:
            value = default
        if validator is None:
            return value
        ok, err = validator(value)
        if ok:
            return value
        print(err)


def password_prompt(prompt: str = "密码: ") -> str:
    """隐藏输入密码。"""
    if not _is_interactive():
        try:
            return input(prompt)
        except EOFError:
            return ""
    try:
        import getpass
        return getpass.getpass(prompt)
    except Exception:
        try:
            return input(prompt)
        except EOFError:
            return ""


def password_with_confirm(prompt: str = "密码: ",
                         confirm_prompt: str = "确认密码: ") -> str:
    """两次输入密码确认。"""
    while True:
        p1 = password_prompt(prompt)
        p2 = password_prompt(confirm_prompt)
        if p1 == p2:
            return p1
        print("两次输入不一致，请重试。")


# ============================================================
# 事件系统
# ============================================================

class KeyEvent:
    """键盘事件。"""

    # 特殊键常量
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    ENTER = "enter"
    ESC = "escape"
    TAB = "tab"
    BACKSPACE = "backspace"
    DELETE = "delete"
    HOME = "home"
    END = "end"
    PAGE_UP = "page_up"
    PAGE_DOWN = "page_down"

    def __init__(self, key: str, ctrl: bool = False, alt: bool = False, shift: bool = False):
        self.key = key
        self.ctrl = ctrl
        self.alt = alt
        self.shift = shift

    def __repr__(self):
        mods = []
        if self.ctrl:
            mods.append("ctrl")
        if self.alt:
            mods.append("alt")
        if self.shift:
            mods.append("shift")
        return f"KeyEvent({self.key!r}, {','.join(mods)})"

    def __eq__(self, other):
        return (isinstance(other, KeyEvent) and self.key == other.key
                and self.ctrl == other.ctrl and self.alt == other.alt)

    @staticmethod
    def parse_escape_seq(seq: str) -> "KeyEvent":
        """解析 ANSI 转义序列为 KeyEvent。

        支持方向键、Home/End、PageUp/Down、Delete、Enter 等。
        """
        if not seq:
            return KeyEvent("")
        # 单字符
        if len(seq) == 1:
            if seq == "\r" or seq == "\n":
                return KeyEvent(KeyEvent.ENTER)
            if seq == "\x1b":
                return KeyEvent(KeyEvent.ESC)
            if seq == "\t":
                return KeyEvent(KeyEvent.TAB)
            if seq == "\x7f" or seq == "\b":
                return KeyEvent(KeyEvent.BACKSPACE)
            if ord(seq) < 32:
                return KeyEvent(chr(ord(seq) + ord("a") - 1), ctrl=True)
            return KeyEvent(seq)

        # 转义序列
        mapping = {
            "[A": KeyEvent.UP,
            "[B": KeyEvent.DOWN,
            "[C": KeyEvent.RIGHT,
            "[D": KeyEvent.LEFT,
            "[H": KeyEvent.HOME,
            "[F": KeyEvent.END,
            "[3~": KeyEvent.DELETE,
            "[5~": KeyEvent.PAGE_UP,
            "[6~": KeyEvent.PAGE_DOWN,
            "OH": KeyEvent.HOME,
            "OF": KeyEvent.END,
        }
        key = mapping.get(seq)
        if key:
            return KeyEvent(key)
        # 未知序列
        return KeyEvent(seq)


class MouseEvent:
    """鼠标事件。"""

    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    DRAG = "drag"
    SCROLL_UP = "scroll_up"
    SCROLL_DOWN = "scroll_down"

    def __init__(self, x: int, y: int, button: str = "", action: str = CLICK):
        self.x = x
        self.y = y
        self.button = button
        self.action = action

    def __repr__(self):
        return f"MouseEvent(x={self.x}, y={self.y}, button={self.button!r}, action={self.action!r})"


# ============================================================
# 屏幕管理
# ============================================================

class MockScreen:
    """非 TTY 环境的 Mock 屏幕，记录操作不实际输出。"""

    def __init__(self, width: int = 80, height: int = 24):
        self._width = width
        self._height = height
        self.calls: List[str] = []
        self.buffer: List[List[str]] = [" " * width for _ in range(height)]

    def enter_alternate(self):
        self.calls.append("enter_alternate")

    def exit_alternate(self):
        self.calls.append("exit_alternate")

    def clear(self):
        self.calls.append("clear")
        self.buffer = [" " * self._width for _ in range(self._height)]

    def move_cursor(self, x: int, y: int):
        self.calls.append(f"move_cursor({x},{y})")

    def hide_cursor(self):
        self.calls.append("hide_cursor")

    def show_cursor(self):
        self.calls.append("show_cursor")

    def size(self) -> Tuple[int, int]:
        return self._width, self._height

    def render(self, buffer: List[str]):
        self.calls.append(f"render({len(buffer)} lines)")
        self.buffer = list(buffer)

    def __enter__(self):
        self.enter_alternate()
        return self

    def __exit__(self, *args):
        self.exit_alternate()
        return False


class Screen:
    """真实终端屏幕管理。非 TTY 自动降级为 MockScreen。"""

    def __new__(cls, *args, **kwargs):
        is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        if not is_tty:
            return MockScreen(*args, **kwargs)
        return super().__new__(cls)

    def __init__(self):
        # 真实终端初始化
        self._w, self._h = _term_size()

    def enter_alternate(self):
        sys.stdout.write("\x1b[?1049h")
        sys.stdout.flush()

    def exit_alternate(self):
        sys.stdout.write("\x1b[?1049l")
        sys.stdout.flush()

    def clear(self):
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()

    def move_cursor(self, x: int, y: int):
        sys.stdout.write(f"\x1b[{y + 1};{x + 1}H")
        sys.stdout.flush()

    def hide_cursor(self):
        sys.stdout.write("\x1b[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        sys.stdout.write("\x1b[?25h")
        sys.stdout.flush()

    def size(self) -> Tuple[int, int]:
        self._w, self._h = _term_size()
        return self._w, self._h

    def render(self, buffer: List[str]):
        """渲染字符缓冲区。buffer 是每行字符串的列表。"""
        out = []
        for y, line in enumerate(buffer[: self._h]):
            out.append(f"\x1b[{y + 1};1H{line}")
        sys.stdout.write("".join(out))
        sys.stdout.flush()

    def __enter__(self):
        self.enter_alternate()
        self.hide_cursor()
        return self

    def __exit__(self, *args):
        self.show_cursor()
        self.exit_alternate()
        return False


# ============================================================
# 控件基类
# ============================================================

class Widget:
    """所有 TUI 控件的基类。"""

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._focused = False
        self.on_key: Optional[Callable[[KeyEvent], bool]] = None
        self.on_click: Optional[Callable[[MouseEvent], bool]] = None
        self.parent: Optional["Widget"] = None

    def focus(self):
        self._focused = True

    def blur(self):
        self._focused = False

    @property
    def focused(self) -> bool:
        return self._focused

    def draw(self, screen) -> List[str]:
        """绘制到屏幕，返回该控件区域的行缓冲。子类覆写。"""
        return [" " * max(1, self.width)] * max(1, self.height)

    def handle_key(self, event: KeyEvent) -> bool:
        """处理按键，返回是否消费事件。"""
        if self.on_key:
            return bool(self.on_key(event))
        return False

    def handle_mouse(self, event: MouseEvent) -> bool:
        """处理鼠标，返回是否消费事件。"""
        if self.on_click:
            return bool(self.on_click(event))
        return False


# ============================================================
# 布局容器
# ============================================================

class Box(Widget):
    """带边框的容器。"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 title: Optional[str] = None, border: bool = True):
        super().__init__(x, y, width, height)
        self.title = title
        self.border = border
        self.children: List[Widget] = []

    def add(self, widget: Widget):
        self.children.append(widget)
        widget.parent = self
        return widget

    def draw(self, screen) -> List[str]:
        lines = []
        if not self.border:
            # 无框，直接绘制子控件（占位）
            for i in range(self.height):
                lines.append(" " * max(1, self.width))
            return lines

        w = max(2, self.width)
        h = max(2, self.height)
        # 顶
        top = "┌"
        if self.title:
            title = f" {self.title} "
            top += title
            top += "─" * max(0, w - 2 - display_width(title))
        else:
            top += "─" * (w - 2)
        top += "┐"
        lines.append(top[:w])
        # 中间
        for i in range(h - 2):
            inner_w = w - 2
            lines.append("│" + " " * inner_w + "│")
        # 底
        lines.append("└" + "─" * (w - 2) + "┘")
        return lines[:h]


class VBox(Widget):
    """垂直布局容器：子控件按顺序垂直排列。"""

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        super().__init__(x, y, width, height)
        self.children: List[Widget] = []

    def add(self, widget: Widget):
        self.children.append(widget)
        widget.parent = self
        # 自动布局
        self._relayout()
        return widget

    def _relayout(self):
        """根据子控件高度重新排列。"""
        if not self.children:
            return
        total_h = sum(max(1, c.height) for c in self.children)
        y = self.y
        for c in self.children:
            c.x = self.x
            c.y = y
            c.width = self.width or c.width
            y += max(1, c.height)

    def draw(self, screen) -> List[str]:
        self._relayout()
        lines = [" " * max(1, self.width)] * max(1, self.height)
        for c in self.children:
            c_lines = c.draw(screen)
            for i, cl in enumerate(c_lines):
                ly = (c.y - self.y) + i
                if 0 <= ly < len(lines):
                    cur = lines[ly]
                    lines[ly] = cur[: c.x - self.x] + cl + cur[c.x - self.x + display_width(cl):]
        return lines


class HBox(Widget):
    """水平布局容器：子控件按顺序水平排列。"""

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        super().__init__(x, y, width, height)
        self.children: List[Widget] = []

    def add(self, widget: Widget):
        self.children.append(widget)
        widget.parent = self
        self._relayout()
        return widget

    def _relayout(self):
        if not self.children:
            return
        x = self.x
        for c in self.children:
            c.x = x
            c.y = self.y
            c.height = self.height or c.height
            x += max(1, c.width)

    def draw(self, screen) -> List[str]:
        self._relayout()
        lines = [" " * max(1, self.width)] * max(1, self.height)
        for c in self.children:
            c_lines = c.draw(screen)
            for i, cl in enumerate(c_lines):
                ly = (c.y - self.y) + i
                if 0 <= ly < len(lines):
                    cur = lines[ly]
                    seg = cl[: max(1, c.width)]
                    seg = seg + " " * max(0, c.width - len(seg))
                    start = c.x - self.x
                    lines[ly] = cur[:start] + seg + cur[start + len(seg):]
        return lines


# ============================================================
# 具体控件
# ============================================================

class Text(Widget):
    """静态文本控件。支持自动换行、对齐。"""

    def __init__(self, text: str, x: int = 0, y: int = 0, width: Optional[int] = None,
                 color: Optional[str] = None, bold_: bool = False, align: str = "left"):
        super().__init__(x, y, width or display_width(text), 1)
        self._text = text
        self.color = color
        self.bold_ = bold_
        self.align = align

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    def draw(self, screen) -> List[str]:
        vis = display_width(self._text)
        w = self.width or vis
        if vis >= w:
            content = self._text[: max(1, w - 1)] + "…"
        else:
            if self.align == "right":
                content = " " * (w - vis) + self._text
            elif self.align == "center":
                pad = (w - vis) // 2
                content = " " * pad + self._text + " " * (w - vis - pad)
            else:
                content = self._text + " " * (w - vis)
        if self.bold_:
            content = bold(content)
        if self.color:
            content = fg(content, self.color)
        return [content]


class Input(Widget):
    """单行输入框。"""

    def __init__(self, x: int = 0, y: int = 0, width: int = 20,
                 placeholder: str = "", password: bool = False):
        super().__init__(x, y, width, 1)
        self._value = ""
        self.placeholder = placeholder
        self.password = password
        self._cursor = 0  # 光标位置（字符索引）

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, v: str):
        self._value = v
        self._cursor = len(v)

    def handle_key(self, event: KeyEvent) -> bool:
        if event.key == KeyEvent.LEFT:
            self._cursor = max(0, self._cursor - 1)
            return True
        if event.key == KeyEvent.RIGHT:
            self._cursor = min(len(self._value), self._cursor + 1)
            return True
        if event.key == KeyEvent.HOME:
            self._cursor = 0
            return True
        if event.key == KeyEvent.END:
            self._cursor = len(self._value)
            return True
        if event.key == KeyEvent.BACKSPACE:
            if self._cursor > 0:
                self._value = self._value[: self._cursor - 1] + self._value[self._cursor:]
                self._cursor -= 1
            return True
        if event.key == KeyEvent.DELETE:
            if self._cursor < len(self._value):
                self._value = self._value[: self._cursor] + self._value[self._cursor + 1:]
            return True
        if len(event.key) == 1 and not event.ctrl:
            self._value = self._value[: self._cursor] + event.key + self._value[self._cursor:]
            self._cursor += 1
            return True
        return False

    def draw(self, screen) -> List[str]:
        w = max(1, self.width)
        if self.password:
            shown = "*" * len(self._value)
        else:
            shown = self._value or self.placeholder
        # 简单裁剪到宽度
        if len(shown) > w:
            shown = shown[-w:]
        line = shown + " " * max(0, w - len(shown))
        if not self._value and self.placeholder:
            line = dim(line)
        return [line]


class List(Widget):
    """列表选择控件。支持上下导航和滚动。"""

    def __init__(self, items: List[str], x: int = 0, y: int = 0,
                 width: int = 30, height: int = 10):
        super().__init__(x, y, width, height)
        self.items = list(items)
        self._selected_index = 0
        self._scroll_offset = 0

    @property
    def selected_index(self) -> int:
        return self._selected_index

    @selected_index.setter
    def selected_index(self, v: int):
        self._selected_index = max(0, min(len(self.items) - 1, v))

    @property
    def selected_value(self) -> Optional[str]:
        if 0 <= self._selected_index < len(self.items):
            return self.items[self._selected_index]
        return None

    def handle_key(self, event: KeyEvent) -> bool:
        if event.key == KeyEvent.UP:
            self.selected_index = max(0, self._selected_index - 1)
            self._adjust_scroll()
            return True
        if event.key == KeyEvent.DOWN:
            self.selected_index = min(len(self.items) - 1, self._selected_index + 1)
            self._adjust_scroll()
            return True
        if event.key == KeyEvent.PAGE_UP:
            self.selected_index = max(0, self._selected_index - self.height)
            self._adjust_scroll()
            return True
        if event.key == KeyEvent.PAGE_DOWN:
            self.selected_index = min(len(self.items) - 1, self._selected_index + self.height)
            self._adjust_scroll()
            return True
        return False

    def _adjust_scroll(self):
        """确保选中项可见。"""
        if self._selected_index < self._scroll_offset:
            self._scroll_offset = self._selected_index
        elif self._selected_index >= self._scroll_offset + self.height:
            self._scroll_offset = self._selected_index - self.height + 1

    def draw(self, screen) -> List[str]:
        w = max(1, self.width)
        lines = []
        end = min(len(self.items), self._scroll_offset + self.height)
        for row in range(self.height):
            idx = self._scroll_offset + row
            if idx < end:
                text = self.items[idx]
                if self._focused and idx == self._selected_index:
                    line = ("> " + text).ljust(w)[:w]
                    line = bg(line, "blue")
                else:
                    line = ("  " + text).ljust(w)[:w]
            else:
                line = " " * w
            lines.append(line)
        return lines


class Button(Widget):
    """按钮控件。"""

    def __init__(self, label: str, x: int = 0, y: int = 0,
                 on_click: Optional[Callable[[], None]] = None):
        super().__init__(x, y, display_width(label) + 4, 1)
        self.label = label
        self._on_click = on_click

    def handle_key(self, event: KeyEvent) -> bool:
        if event.key in (KeyEvent.ENTER, " "):
            self.trigger()
            return True
        return False

    def trigger(self):
        if self._on_click:
            self._on_click()

    def draw(self, screen) -> List[str]:
        content = f"[{self.label}]"
        if self._focused:
            content = bg(content, "blue")
        return [content.ljust(self.width)]


class TextArea(Widget):
    """多行文本编辑控件。"""

    def __init__(self, x: int = 0, y: int = 0, width: int = 40, height: int = 10,
                 text: str = ""):
        super().__init__(x, y, width, height)
        self._lines = text.split("\n") if text else [""]
        self._cursor_row = 0
        self._cursor_col = 0
        self._scroll_row = 0

    @property
    def text(self) -> str:
        return "\n".join(self._lines)

    @text.setter
    def text(self, value: str):
        self._lines = value.split("\n") if value else [""]
        self._cursor_row = 0
        self._cursor_col = 0

    def handle_key(self, event: KeyEvent) -> bool:
        row = self._cursor_row
        col = self._cursor_col
        if event.key == KeyEvent.UP:
            self._cursor_row = max(0, row - 1)
            self._cursor_col = min(col, len(self._lines[self._cursor_row]))
            return True
        if event.key == KeyEvent.DOWN:
            self._cursor_row = min(len(self._lines) - 1, row + 1)
            self._cursor_col = min(col, len(self._lines[self._cursor_row]))
            return True
        if event.key == KeyEvent.LEFT:
            if col > 0:
                self._cursor_col = col - 1
            elif row > 0:
                self._cursor_row = row - 1
                self._cursor_col = len(self._lines[row - 1])
            return True
        if event.key == KeyEvent.RIGHT:
            if col < len(self._lines[row]):
                self._cursor_col = col + 1
            elif row < len(self._lines) - 1:
                self._cursor_row = row + 1
                self._cursor_col = 0
            return True
        if event.key == KeyEvent.BACKSPACE:
            if col > 0:
                self._lines[row] = self._lines[row][: col - 1] + self._lines[row][col:]
                self._cursor_col = col - 1
            elif row > 0:
                prev_len = len(self._lines[row - 1])
                self._lines[row - 1] += self._lines[row]
                del self._lines[row]
                self._cursor_row = row - 1
                self._cursor_col = prev_len
            return True
        if event.key == KeyEvent.ENTER:
            rest = self._lines[row][col:]
            self._lines[row] = self._lines[row][:col]
            self._lines.insert(row + 1, rest)
            self._cursor_row = row + 1
            self._cursor_col = 0
            return True
        if len(event.key) == 1 and not event.ctrl:
            self._lines[row] = self._lines[row][:col] + event.key + self._lines[row][col:]
            self._cursor_col = col + 1
            return True
        return False

    def draw(self, screen) -> List[str]:
        w = max(1, self.width)
        h = max(1, self.height)
        # 调整滚动
        if self._cursor_row < self._scroll_row:
            self._scroll_row = self._cursor_row
        elif self._cursor_row >= self._scroll_row + h:
            self._scroll_row = self._cursor_row - h + 1
        lines = []
        for r in range(h):
            idx = self._scroll_row + r
            if 0 <= idx < len(self._lines):
                line = self._lines[idx].ljust(w)[:w]
            else:
                line = " " * w
            lines.append(line)
        return lines


# ============================================================
# TUI 应用主循环
# ============================================================

class App:
    """TUI 应用主循环。

    非 TTY 环境下降级为 Mock 模式（可测试，不阻塞）。
    """

    def __init__(self, title: str = "Aurora TUI"):
        self.title = title
        self.root: Optional[Widget] = None
        self._running = False
        self._status = ""
        self._global_key_cb: Optional[Callable[[KeyEvent], bool]] = None
        self._fps = 30
        self._frame_interval = 1.0 / self._fps
        # Mock 模式：可注入按键队列用于测试
        self.mock_mode = not (_is_interactive())
        self._mock_key_queue: List[KeyEvent] = []
        # 屏幕
        self.screen = MockScreen() if self.mock_mode else Screen()

    def add(self, widget: Widget):
        """添加根控件。"""
        self.root = widget
        return widget

    def on_key(self, callback: Callable[[KeyEvent], bool]):
        """注册全局键盘回调。返回 True 表示消费事件。"""
        self._global_key_cb = callback

    def set_status(self, text: str):
        """设置状态栏文本。"""
        self._status = text

    def enqueue_key(self, event: KeyEvent):
        """Mock 模式：注入按键事件。"""
        self._mock_key_queue.append(event)

    def stop(self):
        """退出主循环。"""
        self._running = False

    def _read_key(self) -> Optional[KeyEvent]:
        """读取一个按键事件。真实模式读 stdin，Mock 模式从队列取。"""
        if self.mock_mode:
            if self._mock_key_queue:
                return self._mock_key_queue.pop(0)
            return None
        # 真实模式（简化：使用 sys.stdin read）
        try:
            import tty, termios
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == "\x1b":
                    seq = ch + sys.stdin.read(2)
                    return KeyEvent.parse_escape_seq(seq)
                return KeyEvent.parse_escape_seq(ch)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except Exception:
            return None

    def _dispatch_key(self, event: KeyEvent):
        """分发按键事件。"""
        if self._global_key_cb and self._global_key_cb(event):
            return
        if event.key == "q" and not event.ctrl:
            # 全局退出（可被 global callback 拦截）
            pass
        if self.root:
            self.root.handle_key(event)

    def render_frame(self) -> List[str]:
        """渲染一帧到 buffer。"""
        w, h = self.screen.size()
        buffer = [" " * w for _ in range(h)]
        if self.root:
            lines = self.root.draw(self.screen)
            for i, line in enumerate(lines[:h]):
                ly = self.root.y + i
                if 0 <= ly < h:
                    vis = display_width(line)
                    start = self.root.x
                    end = start + vis
                    old = buffer[ly]
                    buffer[ly] = old[:start] + line + old[end:]
        # 状态栏
        if self._status:
            buffer[-1] = self._status.ljust(w)[:w]
        return buffer

    def run(self):
        """启动主循环。"""
        self._running = True
        if self.mock_mode:
            self._run_mock()
            return
        # 真实模式
        with self.screen:
            self.screen.clear()
            while self._running:
                buffer = self.render_frame()
                self.screen.render(buffer)
                event = self._read_key()
                if event is None:
                    continue
                if event.key == KeyEvent.ESC:
                    self.stop()
                    break
                self._dispatch_key(event)
                time.sleep(self._frame_interval)

    def _run_mock(self):
        """Mock 模式主循环：处理注入的按键，不阻塞。"""
        while self._running:
            buffer = self.render_frame()
            self.screen.render(buffer)
            event = self._read_key()
            if event is None:
                # 没有更多注入事件，自动停止
                self._running = False
                break
            self._dispatch_key(event)
            time.sleep(0.001)


# ============================================================
# 标准库注册
# ============================================================

STDLIB_REGISTRATION: Dict[str, Dict[str, Any]] = {
    "std.cli": {
        "color": fg,
        "fg": fg,
        "bg": bg,
        "bold": bold,
        "underline": underline,
        "dim": dim,
        "italic": italic,
        "strikethrough": strikethrough,
        "rgb": rgb,
        "style": style,
        "strip_ansi": strip_ansi,
        "Spinner": Spinner,
        "ProgressBar": ProgressBar,
        "MultiProgress": MultiProgress,
        "Table": Table,
        "TreeNode": TreeNode,
        "confirm": confirm,
        "select": select,
        "multiselect": multiselect,
        "input": input_prompt,
        "password": password_prompt,
        "password_with_confirm": password_with_confirm,
    },
    "std.tui": {
        "App": App,
        "Screen": Screen,
        "MockScreen": MockScreen,
        "Box": Box,
        "VBox": VBox,
        "HBox": HBox,
        "Text": Text,
        "Input": Input,
        "List": List,
        "Button": Button,
        "TextArea": TextArea,
        "KeyEvent": KeyEvent,
        "MouseEvent": MouseEvent,
        "Widget": Widget,
    },
}
