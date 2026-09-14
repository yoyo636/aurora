"""Aurora 代码格式化器 — 基于 lexer 的词法序列做确定性重排。

设计要点：
* Lexer 会丢弃注释，且记录的行列位置对字符串不可靠。因此这里：
  1. 用 ``Lexer`` 得到 token 类型序列（驱动缩进与空格规则）；
  2. 按源码顺序做一次前向扫描，精确保留字符串/原始字符串的原文，
     并把 ``#`` / ``//`` 注释按其出现位置重新挂回。
* 块级缩进由 ``{`` / ``}`` 驱动（Aurora 是花括号语言，缩进无语义）。
* 输出确定性：对同一源码反复格式化结果不变（幂等）。

公共 API：
* format_code(source: str) -> str
* format_file(input_path: str, output_path: str = None)
* register_cli(subparsers)
"""

import os
import sys
from typing import List, Optional, Tuple

from .lexer import Lexer, LexerError
from .tokens import TokenType


INDENT_UNIT = "    "  # 4 个空格


# ---------------------------------------------------------------------------
# 源码前向扫描：把 token 流还原成带原文/注释/换行的事件序列
# ---------------------------------------------------------------------------

def _scan_events(src: str) -> List[Tuple]:
    """返回事件列表。

    事件类型：
    * ('code', TokenType, raw_text)  —— 一个代码 token（raw_text 为源码原文）
    * ('comment', text)             —— 一行注释（不含换行）
    * ('nl',)                       —— 一个换行
    """
    tokens = [t for t in Lexer(src).tokenize()
              if t.type != TokenType.EOF and t.type != TokenType.NEWLINE]

    events: List[Tuple] = []
    ptr = 0
    n = len(src)

    def skip_gap() -> None:
        nonlocal ptr
        while ptr < n:
            c = src[ptr]
            if c in ' \t\r':
                ptr += 1
            elif c == '\n':
                events.append(('nl',))
                ptr += 1
            elif c == '#' or (c == '/' and ptr + 1 < n and src[ptr + 1] == '/'):
                end = src.find('\n', ptr)
                if end == -1:
                    end = n
                events.append(('comment', src[ptr:end].rstrip()))
                ptr = end
            else:
                break

    def consume(tok) -> str:
        nonlocal ptr
        start = ptr
        tt = tok.type
        if tt == TokenType.STRING:
            quote = src[ptr]
            ptr += 1
            while ptr < n and src[ptr] != quote:
                if src[ptr] == '\\':
                    ptr += 1
                ptr += 1
            ptr += 1  # 闭引号
        elif tt == TokenType.RAW_STRING:
            if src[ptr] in 'rR':
                ptr += 1
            quote = src[ptr]
            ptr += 1
            while ptr < n and src[ptr] != quote:
                ptr += 1
            ptr += 1
        else:
            ptr += len(tok.value)
        return src[start:ptr]

    for tok in tokens:
        skip_gap()
        raw = consume(tok)
        events.append(('code', tok.type, raw))

    # 文件末尾：扫出最后一个 token 之后的尾部注释
    skip_gap()

    return events


# ---------------------------------------------------------------------------
# 空格规则
# ---------------------------------------------------------------------------

# 这些 token 后面紧接的 token 不加分隔空格
_NO_SPACE_AFTER = {
    TokenType.LPAREN, TokenType.LBRACKET, TokenType.DOT,
    TokenType.RANGE,
}
# 这些 token 前面不加空格
_NO_SPACE_BEFORE = {
    TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
    TokenType.COMMA, TokenType.DOT, TokenType.SEMICOLON, TokenType.RANGE,
}


def _needs_space(prev_type, cur_type) -> bool:
    """判断两个相邻代码 token 之间是否需要一个普通空格。"""
    if prev_type is None:
        return False
    if cur_type in _NO_SPACE_BEFORE or prev_type in _NO_SPACE_AFTER:
        return False
    # 幂运算 ** 两侧不加空格
    if prev_type == TokenType.POWER or cur_type == TokenType.POWER:
        return False
    # 冒号前不加空格，冒号后加空格
    if cur_type == TokenType.COLON:
        return False
    if prev_type == TokenType.COLON:
        return True
    # 标识符后紧跟 ( 视为调用，不加空格： foo(...)
    if cur_type == TokenType.LPAREN and prev_type == TokenType.IDENTIFIER:
        return False
    # 默认：二元运算符、关键字、值之间加空格
    return True


# 顶层定义关键字（用于函数/类型定义之间保留一个空行）
_TOPLEVEL_DEF_KEYWORDS = {
    TokenType.FN, TokenType.TYPE, TokenType.ENUM, TokenType.TRAIT,
    TokenType.IMPL, TokenType.IMPORT, TokenType.CONST, TokenType.PUB,
    TokenType.TEST,
}


# ---------------------------------------------------------------------------
# 核心格式化器
# ---------------------------------------------------------------------------

class _Formatter:
    # } 之后应保持同行的关键字
    _CONTINUATION = {
        TokenType.ELSE, TokenType.ELIF, TokenType.CATCH, TokenType.FINALLY,
    }

    def __init__(self, src: str):
        self.events = _scan_events(src)
        self.out: List[str] = []       # 已完成的行
        self.buf = []                  # 当前正在累积的代码片段
        self.indent = 0
        self.blank_run = 0             # 当前连续空行数
        self.prev_type = None
        self.at_line_start = True      # 下一个代码 token 是否在行首
        self.drop_next_nl = False      # 忽略紧随花括号头后的换行
        self.merge_next = False        # 把 } 与 else/elif 等合并到一行
        self.prev_line_was_def = False
        self.pending_blank = False
        self.i = 0
        self.n = len(self.events)

    # -- 行操作 ----------------------------------------------------------

    def _commit(self):
        """把当前 buf 作为一行提交。"""
        line = "".join(self.buf).rstrip()
        self.buf = []
        if line == "":
            self.blank_run += 1
        else:
            self._emit(line)

    def _emit(self, line: str):
        # 折叠连续空行到最多 1 个
        if self.blank_run > 0:
            if self.out and self.out[-1] != "":
                self.out.append("")
            self.blank_run = 0

        if self.pending_blank and self.out and self.out[-1] != "":
            self.out.append("")
        self.pending_blank = False

        self.out.append(INDENT_UNIT * self.indent + line)

    def _peek_code(self, j: int):
        """从 j 起跳过 nl/comment，返回下一个代码事件。"""
        while j < self.n:
            ev = self.events[j]
            if ev[0] == 'code':
                return ev
            j += 1
        return None

    # -- token 处理 ------------------------------------------------------

    def _on_code(self, tt: TokenType, raw: str):
        first_on_line = self.at_line_start
        self.at_line_start = False

        if tt == TokenType.LBRACE:
            if self.buf:
                self.buf.append(" ")
            self.buf.append("{")
            self._commit()
            self.indent += 1
            self.at_line_start = True
            self.drop_next_nl = True
            self.prev_type = tt
            return

        if tt == TokenType.RBRACE:
            # 仅当有语句与 } 同行时才先提交该行
            if self.buf:
                self._commit()
            self.indent = max(0, self.indent - 1)
            self.buf.append("}")
            self.prev_type = tt
            nxt = self._peek_code(self.i + 1)
            if nxt and nxt[1] in self._CONTINUATION:
                # } 与 else/elif/catch/finally 保持同行
                self.merge_next = True
                self.at_line_start = False
            else:
                # 否则 } 独占一行
                self._commit()
                self.drop_next_nl = True
                self.at_line_start = True
            return

        # 普通代码 token
        if self.buf and _needs_space(self.prev_type, tt):
            self.buf.append(" ")
        self.buf.append(raw)
        self.prev_type = tt

        # 顶层定义边界
        if first_on_line and self.indent == 0 and tt in _TOPLEVEL_DEF_KEYWORDS:
            if self.prev_line_was_def:
                self.pending_blank = True
            self.prev_line_was_def = True
        elif first_on_line and self.indent == 0:
            self.prev_line_was_def = False

    def run(self) -> str:
        while self.i < self.n:
            ev = self.events[self.i]
            kind = ev[0]

            if kind == 'nl':
                if self.drop_next_nl:
                    self.drop_next_nl = False
                elif self.merge_next:
                    # 吞掉 } 与 else 之间的换行，保持同行
                    pass
                else:
                    self._commit()
                    self.at_line_start = True
                    self.prev_type = None
                self.i += 1
                continue

            if kind == 'comment':
                text = ev[1]
                if self.buf:
                    if not self.buf[-1].endswith(" "):
                        self.buf.append(" ")
                    self.buf.append(text)
                else:
                    self._commit()
                    self.out.append(INDENT_UNIT * self.indent + text)
                    self.blank_run = 0
                    self.drop_next_nl = True
                self.i += 1
                continue

            # code
            if self.merge_next:
                self.merge_next = False
            tt, raw = ev[1], ev[2]
            self._on_code(tt, raw)
            self.i += 1

        if self.buf:
            self._commit()

        text = "\n".join(self.out).rstrip("\n") + "\n"
        return text


# ---------------------------------------------------------------------------
# 公共 API
# ---------------------------------------------------------------------------

def format_code(source: str) -> str:
    """格式化 Aurora 源代码字符串，返回格式化后的代码。"""
    if source == "":
        return ""
    try:
        return _Formatter(source).run()
    except LexerError:
        # 词法错误时原样返回，避免破坏用户文件
        return source


def format_file(input_path: str, output_path: Optional[str] = None) -> bool:
    """格式化文件。output_path 为 None 时原地覆盖。返回文件是否被修改。"""
    with open(input_path, "r", encoding="utf-8") as f:
        original = f.read()

    formatted = format_code(original)

    target = output_path if output_path is not None else input_path
    if formatted != original:
        with open(target, "w", encoding="utf-8") as f:
            f.write(formatted)
        return True
    return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _iter_aur_files(path: str):
    if os.path.isfile(path):
        yield path
        return
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames
                       if d not in {'.git', '__pycache__', 'node_modules',
                                    '.venv', 'target'}]
        for name in sorted(filenames):
            if name.endswith('.aur'):
                yield os.path.join(dirpath, name)


def register_cli(subparsers):
    """注册 ``fmt`` 子命令到 aurora CLI。"""
    p_fmt = subparsers.add_parser('fmt', help='格式化 Aurora 代码')
    p_fmt.add_argument('path', help='文件或目录(目录则递归格式化 .aur)')
    p_fmt.add_argument('--check', action='store_true',
                       help='只检查不修改；需要格式化时返回非零退出码')
    p_fmt.set_defaults(func=_cmd_fmt)


def _cmd_fmt(args):
    paths = list(_iter_aur_files(args.path))
    if not paths:
        print(f"未找到 .aur 文件: {args.path}")
        sys.exit(1)

    need_format = 0
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        formatted = format_code(original)
        if formatted != original:
            need_format += 1
            if args.check:
                print(f"需要格式化: {path}")
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(formatted)
                print(f"格式化: {path}")

    if args.check:
        if need_format:
            print(f"\n{need_format} 个文件需要格式化")
            sys.exit(1)
        print("所有文件已格式化 ✓")
    else:
        print(f"\n完成: {len(paths)} 个文件, {need_format} 个被修改")
