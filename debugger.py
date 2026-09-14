"""Aurora 源码级调试器 — 基于解释器执行钩子实现的交互式调试器

用法（由 cli.py 的 register_cli 注册后）：
    aurora debug <file>                 启动交互式调试
    aurora debug <file> --break 10      启动时在第 10 行设断点
    aurora debug <file> --cmd cmds.txt  从文件批量读取调试命令（非交互）

支持的调试命令：
    break <file>:<line> | b <line>          行断点
    break <func>                            函数入口断点
    break <line> if <cond>                  条件断点
    continue / c                            继续执行
    step / s                                单步进入
    next / n                                单步跳过
    finish / f                              执行到当前函数返回
    print <expr> / p <expr>                 求值表达式并打印
    locals                                  打印当前作用域所有变量
    backtrace / bt                          打印调用栈
    list / l                                显示当前位置周围 5 行源码
    delete <n>                              删除第 n 号断点
    info breakpoints                        列出所有断点
    quit / q                                退出
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .ast_nodes import (
    Program, Stmt, LetStmt, ConstStmt, AssignStmt, ReturnStmt, ExprStmt,
    IfStmt, ForStmt, WhileStmt, FnDef, DestructureLet, DeferStmt, YieldStmt,
    BreakStmt, ContinueStmt, MatchStmt, TryStmt, Block,
)
from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .interpreter import (
    Interpreter, Environment, ReturnSignal, BreakSignal, ContinueSignal,
)
from .stdlib import AuroraError, BUILTIN_GLOBALS


# ── 退出信号（继承 BaseException，避免被用户 try/catch 吞掉） ──

class DebuggerQuit(BaseException):
    """用户在调试器中输入 quit 时抛出，用于中断解释器执行"""


# ── 断点 ────────────────────────────────────────────────

@dataclass
class Breakpoint:
    bid: int
    file: Optional[str] = None      # None 表示任意文件
    line: int = 0                    # 0 表示函数断点
    func: Optional[str] = None
    condition: Optional[str] = None
    enabled: bool = True
    hit_count: int = 0


# ── 带调试钩子的解释器 ──────────────────────────────────

class DebuggableInterpreter(Interpreter):
    """在语句执行循环与函数调用点插入调试钩子的解释器子类"""

    def __init__(self, debugger: 'Debugger'):
        super().__init__()
        self.dbg = debugger

    # 语句执行前回调
    def _exec_stmts(self, stmts: List[Stmt], env: Environment) -> Any:
        result = None
        for stmt in stmts:
            self.dbg.hook(stmt, env)
            result = self._exec_stmt(stmt, env)
            if isinstance(result, ReturnSignal):
                return result
        return result

    # 包装函数：记录调用栈帧 / 函数断点
    def _make_function(self, fn_def, closure_env, is_impl: bool = False):
        fn = super()._make_function(fn_def, closure_env, is_impl)
        name = fn_def.name
        entry_line = 0
        if isinstance(fn_def.body, Block) and fn_def.body.statements:
            entry_line = self.dbg.stmt_line(fn_def.body.statements[0])
        wrapped = _make_wrapped(fn, name, self)
        return wrapped


def _make_wrapped(fn, name: str, interp: DebuggableInterpreter):
    def wrapped(*args, **kwargs):
        interp.dbg.enter_frame(name)
        try:
            return fn(*args, **kwargs)
        finally:
            interp.dbg.leave_frame()
    wrapped.__name__ = getattr(fn, '__name__', name)
    wrapped._aurora = True
    wrapped._ast = getattr(fn, '_ast', None)
    return wrapped


# ── 调试器 ──────────────────────────────────────────────

class Debugger:
    """交互式源码级调试器"""

    def __init__(self, path: Optional[str] = None, source: Optional[str] = None):
        self.interp = DebuggableInterpreter(self)
        self.path = os.path.abspath(path) if path else None
        self.source = source
        self.program: Optional[Program] = None
        self.sources: Dict[str, List[str]] = {}   # file -> lines

        self.breakpoints: List[Breakpoint] = []
        self._bp_seq = 1

        # 执行控制状态
        self.mode = 'step'          # run / step / next
        self.finish_depth: Optional[int] = None
        self.next_depth: Optional[int] = None

        # 当前上下文
        self.current_file: Optional[str] = None
        self.current_line: int = 0
        self.current_env: Optional[Environment] = None
        self.current_stmt: Optional[Stmt] = None
        self.frames: List[Dict[str, Any]] = []
        self._func_entry: Optional[str] = None   # 刚进入的函数名（待第一条语句触发）

        self.running = True
        # 批量命令模式
        self._cmd_queue: List[str] = []
        self._interactive = True

    # ── 源码加载 ──────────────────────────────────

    def load(self):
        if self.source is None and self.path:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.source = f.read()
        lexer = Lexer(self.source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        self.program = parser.parse()
        if self.path:
            self.sources[self.path] = self.source.splitlines()

    def add_source(self, path: str, text: str):
        self.sources[os.path.abspath(path)] = text.splitlines()

    # ── 行号推导（多数语句自身不带行号，从子表达式提取） ──

    @staticmethod
    def stmt_line(stmt: Stmt) -> int:
        if getattr(stmt, 'line', 0):
            return stmt.line
        # 从常见子节点提取
        for attr in ('initializer', 'value', 'target', 'condition',
                     'iterable', 'subject', 'expr'):
            child = getattr(stmt, attr, None)
            if child is not None and getattr(child, 'line', 0):
                return child.line
        body = getattr(stmt, 'body', None)
        if isinstance(body, Block) and body.statements:
            return Debugger.stmt_line(body.statements[0])
        return 0

    # ── 断点管理 ──────────────────────────────────

    def add_breakpoint(self, spec: str) -> Breakpoint:
        """解析并添加断点。spec 形式：
            <file>:<line> | <line> | <func> | <line> if <cond>
        """
        condition = None
        head = spec.strip()
        if ' if ' in head:
            head, condition = head.split(' if ', 1)
            head = head.strip()
            condition = condition.strip()

        # file:line
        if ':' in head and head.split(':')[-1].isdigit():
            file_part, line_part = head.rsplit(':', 1)
            if self.path:
                file_part = os.path.abspath(file_part)
            bp = Breakpoint(self._bp_seq, file=file_part or None,
                            line=int(line_part), condition=condition)
        elif head.isdigit():
            bp = Breakpoint(self._bp_seq, file=self.path, line=int(head),
                            condition=condition)
        else:
            # 函数名断点
            bp = Breakpoint(self._bp_seq, file=self.path, func=head,
                            condition=condition)
        self._bp_seq += 1
        self.breakpoints.append(bp)
        return bp

    def delete_breakpoint(self, bid: int) -> bool:
        for i, bp in enumerate(self.breakpoints):
            if bp.bid == bid:
                del self.breakpoints[i]
                return True
        return False

    def info_breakpoints(self) -> str:
        if not self.breakpoints:
            return "No breakpoints."
        out = ["Num\tType\tWhere\tCondition"]
        for bp in self.breakpoints:
            where = f"{bp.func}()" if bp.func else f"{os.path.basename(bp.file or '?')}:{bp.line}"
            cond = bp.condition or '-'
            flag = '' if bp.enabled else ' (disabled)'
            out.append(f"{bp.bid}\t{'func' if bp.func else 'line'}\t{where}\t{cond}{flag}")
        return '\n'.join(out)

    # ── 调用栈帧 ──────────────────────────────────

    def enter_frame(self, name: str):
        file = self.interp._file_stack[-1] if self.interp._file_stack else self.path
        self.frames.append({'name': name, 'file': file, 'line': self.current_line})
        self._func_entry = name

    def leave_frame(self):
        if len(self.frames) > 1:
            self.frames.pop()

    # ── 条件求值 ──────────────────────────────────

    def cond_true(self, condition: Optional[str], env: Environment) -> bool:
        if not condition:
            return True
        try:
            val = self.interp._eval_interp(condition, env)
        except Exception:
            return False
        if val == 'nil':
            return False
        return bool(val)

    # ── 主钩子 ──────────────────────────────────────

    def hook(self, stmt: Stmt, env: Environment):
        if not self.running:
            raise DebuggerQuit()
        line = self.stmt_line(stmt)
        if not line:
            return
        file = self.interp._file_stack[-1] if self.interp._file_stack else self.path
        self.current_file = file
        self.current_line = line
        self.current_env = env
        self.current_stmt = stmt

        reason = self._should_stop(file, line, env)
        if reason:
            self._stop(file, line, reason)

    def _should_stop(self, file: str, line: int, env: Environment) -> Optional[str]:
        # 1) 函数入口断点（仅在进入函数后的第一条语句检查一次）
        if self._func_entry is not None:
            fname, self._func_entry = self._func_entry, None
            for bp in self.breakpoints:
                if bp.enabled and bp.func == fname and self.cond_true(bp.condition, env):
                    bp.hit_count += 1
                    return f"函数断点: {fname}()"
        # 2) 行断点 / 条件断点
        for bp in self.breakpoints:
            if not bp.enabled or bp.func:
                continue
            if bp.line != line:
                continue
            if bp.file is not None and bp.file != file:
                continue
            if self.cond_true(bp.condition, env):
                bp.hit_count += 1
                where = f"{os.path.basename(file or '?')}:{line}"
                return f"断点 {bp.bid} at {where}"
        # 3) finish：返回到外层函数时停下
        if self.finish_depth is not None and len(self.frames) < self.finish_depth:
            self.finish_depth = None
            self.mode = 'run'
            return "已从当前函数返回"
        # 4) step / next
        if self.mode == 'step':
            return "单步"
        if self.mode == 'next' and self.next_depth is not None:
            if len(self.frames) <= self.next_depth:
                return "单步跳过"
        return None

    # ── 停下 → 进入命令循环 ──────────────────────────

    def _stop(self, file: str, line: int, reason: str):
        print(f"[{reason}] {os.path.basename(file or '?')}:{line}")
        self.print_list(5)
        self._command_loop()

    def _command_loop(self):
        while True:
            try:
                cmd = self._next_command()
            except EOFError:
                self.running = False
                raise DebuggerQuit()
            if cmd is None:
                # 批量队列耗尽：继续运行直到结束或下一断点
                self.mode = 'run'
                return
            self.exec_command(cmd)
            if self.mode in ('run', 'step', 'next') and not self._should_pause:
                return

    # 标记：exec_command 内部是否要求立即回到解释器
    _should_pause = False

    def _next_command(self) -> Optional[str]:
        if self._interactive:
            try:
                return input("aurora-dbg> ")
            except EOFError:
                return None
        if self._cmd_queue:
            return self._cmd_queue.pop(0)
        return None

    # ── 命令解释 ──────────────────────────────────

    def exec_command(self, raw: str):
        text = raw.strip()
        if not text:
            # 空输入默认继续
            self.mode = 'run'
            self._should_pause = False
            return
        parts = text.split(maxsplit=1)
        head = parts[0]
        rest = parts[1] if len(parts) > 1 else ''

        if head in ('continue', 'c'):
            self.mode = 'run'
            self.finish_depth = None
            self._should_pause = False
        elif head in ('step', 's'):
            self.mode = 'step'
            self._should_pause = False
        elif head in ('next', 'n'):
            self.mode = 'next'
            self.next_depth = len(self.frames)
            self._should_pause = False
        elif head in ('finish', 'f'):
            self.mode = 'run'
            self.finish_depth = len(self.frames)
            self._should_pause = False
        elif head in ('break', 'b'):
            bp = self.add_breakpoint(rest)
            print(f"断点 {bp.bid} 已设置", end='')
            if bp.condition:
                print(f" (条件: {bp.condition})", end='')
            print()
            self._should_pause = True
        elif head in ('print', 'p'):
            val = self._safe_eval(rest)
            print(self._fmt_val(val))
            self._should_pause = True
        elif head == 'locals':
            print(self.dump_locals())
            self._should_pause = True
        elif head in ('backtrace', 'bt'):
            print(self.dump_backtrace())
            self._should_pause = True
        elif head in ('list', 'l'):
            self.print_list(5)
            self._should_pause = True
        elif head == 'delete':
            ok = self.delete_breakpoint(int(rest.strip()))
            print("已删除" if ok else "未找到该断点")
            self._should_pause = True
        elif head == 'info' and rest.strip().startswith('break'):
            print(self.info_breakpoints())
            self._should_pause = True
        elif head in ('quit', 'q'):
            self.running = False
            raise DebuggerQuit()
        else:
            print(f"未知命令: {head} (输入 help 查看命令)")
            self._should_pause = True

    def _safe_eval(self, expr: str):
        if not expr:
            return None
        try:
            return self.interp._eval_interp(expr, self.current_env)
        except Exception as e:
            return f"<错误: {e}>"

    @staticmethod
    def _fmt_val(v) -> str:
        if v is None or v == 'nil':
            return 'nil'
        return repr(v) if isinstance(v, (list, dict, tuple)) else str(v)

    def dump_locals(self) -> str:
        if self.current_env is None:
            return "(无活动作用域)"
        lines = []
        env = self.current_env
        depth = 0
        seen = set()
        while env is not None:
            label = "全局" if env is getattr(self.interp, 'global_env', None) else f"局部#{depth}"
            for name, val in env.bindings.items():
                if name.startswith('_') or name in seen or name in BUILTIN_GLOBALS:
                    continue
                seen.add(name)
                lines.append(f"  {name} = {self._fmt_val(val)}   ({label})")
            if label == "全局":
                break
            env = env.parent
            depth += 1
        return '\n'.join(lines) if lines else "(无局部变量)"

    def dump_backtrace(self) -> str:
        out = []
        for i, fr in enumerate(reversed(self.frames)):
            name = fr['name']
            file = os.path.basename(fr['file']) if fr['file'] else '?'
            out.append(f"#{i} {name}  {file}:{fr['line']}")
        return '\n'.join(out)

    def print_list(self, radius: int = 5):
        if not self.current_file:
            return
        text = self.sources.get(self.current_file)
        if text is None:
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    text = f.read().splitlines()
                self.sources[self.current_file] = text
            except OSError:
                return
        lo = max(1, self.current_line - radius)
        hi = min(len(text), self.current_line + radius)
        for i in range(lo, hi + 1):
            marker = '>' if i == self.current_line else ' '
            print(f"{marker}{i:4d}\t{text[i - 1] if i - 1 < len(text) else ''}")

    # ── 运行 ──────────────────────────────────

    def run(self, commands: Optional[List[str]] = None) -> Any:
        if self.program is None:
            self.load()
        self._interactive = commands is None
        self._cmd_queue = list(commands or [])

        # 初始栈帧
        first_line = 0
        if self.program.statements:
            first_line = self.stmt_line(self.program.statements[0])
        self.frames = [{'name': '<main>', 'file': self.path, 'line': first_line}]
        self.mode = 'step'   # 启动后停在第一条语句

        try:
            return self.interp.run(self.program, file_path=self.path)
        except DebuggerQuit:
            print("(调试器已退出)")
            return None
        except (AuroraError, LexerError, ParseError) as e:
            print(f"运行时错误: {e}")
            return None


# ── CLI 注册 ──────────────────────────────────────────

def cmd_debug(args):
    """aurora debug <file> 命令实现"""
    if not os.path.exists(args.file):
        print(f"错误: 文件不存在 '{args.file}'")
        sys.exit(1)
    dbg = Debugger(path=args.file)
    try:
        dbg.load()
    except (LexerError, ParseError) as e:
        print(f"解析失败: {e}")
        sys.exit(1)

    # 启动时断点
    if getattr(args, 'break_line', None):
        dbg.add_breakpoint(str(args.break_line))

    # 批量命令文件
    commands = None
    if getattr(args, 'cmd', None):
        with open(args.cmd, 'r', encoding='utf-8') as f:
            commands = [ln.rstrip('\n') for ln in f if ln.strip()]

    dbg.run(commands=commands)


def register_cli(subparsers):
    """把 debug 子命令注册到全局 argparse"""
    p = subparsers.add_parser('debug', help='启动 Aurora 源码级交互式调试器')
    p.add_argument('file', help='要调试的 .aur 源文件')
    p.add_argument('--break', dest='break_line',
                   help='启动时在指定行设置断点，如 10')
    p.add_argument('--cmd',
                   help='从文件读取调试命令批量执行（非交互模式）')
    p.set_defaults(func=cmd_debug)
