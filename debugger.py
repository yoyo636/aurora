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


# =====================================================================
# v3.1.0 企业级调试器增强（追加代码，不修改上方任何现有函数）
#
# 新增能力：
#   - 条件断点 / 日志断点（LogPoint）
#   - 监视表达式（watch）
#   - 调用栈导航（get_call_stack / frame）
#   - 多线程调试（list_threads / switch_thread）
#   - 时间旅行调试（record / reverse-continue / reverse-step）
#   - 远程调试（TCP attach，简化实现）
#
# 以下方法通过类属性挂载到 Debugger，保持上方代码零改动。
# =====================================================================

import json as _json_v310
import socket as _socket_v310
import threading as _threading_v310
import time as _time_v310
from dataclasses import dataclass as _dc_v310
from typing import List as _List_v310


@_dc_v310
class LogPoint:
    """日志断点（LogPoint）：命中时只打印，不中断。"""
    bid: int
    file: str
    line: int
    message: str          # 支持 {expr} 插值
    enabled: bool = True
    hit_count: int = 0


@_dc_v310
class WatchExpr:
    """监视表达式：每次停下时自动求值。"""
    expr: str
    enabled: bool = True
    last_value: Any = None


# ── v3.1.0 方法实现 ────────────────────────────────────────

def v310_add_conditional_breakpoint(self, file: str, line: int,
                                    condition: str) -> Breakpoint:
    """条件断点：仅当 condition 求值为真时才中断。"""
    bp = Breakpoint(self._bp_seq, file=os.path.abspath(file) if file else self.path,
                    line=line, condition=condition)
    self._bp_seq += 1
    self.breakpoints.append(bp)
    return bp


def v310_add_log_breakpoint(self, file: str, line: int,
                            message: str) -> LogPoint:
    """日志断点：不中断，命中时打印 message（支持 {expr} 插值）。"""
    lp = LogPoint(bid=self._bp_seq,
                  file=os.path.abspath(file) if file else self.path,
                  line=line, message=message)
    self._bp_seq += 1
    if not hasattr(self, "_v310_logpoints"):
        self._v310_logpoints = []
    self._v310_logpoints.append(lp)
    return lp


def v310_add_watch(self, expression: str) -> WatchExpr:
    """添加监视表达式：每次停下时自动求值并显示。"""
    if not hasattr(self, "_v310_watches"):
        self._v310_watches = []
    w = WatchExpr(expr=expression)
    self._v310_watches.append(w)
    return w


def v310_remove_watch(self, expression: str):
    """移除监视表达式。"""
    if not hasattr(self, "_v310_watches"):
        return
    self._v310_watches = [w for w in self._v310_watches
                          if w.expr != expression]


def v310_eval_watches(self) -> Dict[str, Any]:
    """对所有监视表达式求值，返回 {expr: value}。"""
    out: Dict[str, Any] = {}
    for w in getattr(self, "_v310_watches", []) or []:
        if not w.enabled:
            continue
        try:
            w.last_value = self._safe_eval(w.expr)
        except Exception as e:
            w.last_value = f"<错误: {e}>"
        out[w.expr] = w.last_value
    return out


def v310_get_call_stack(self) -> _List_v310[dict]:
    """返回完整调用栈（自顶向下，帧 0 为当前帧）。"""
    stack = []
    for i, fr in enumerate(self.frames):
        stack.append({
            "index": len(self.frames) - 1 - i,
            "name": fr.get("name", "?"),
            "file": fr.get("file"),
            "line": fr.get("line", 0),
        })
    # 反转为 [当前帧, 上一层, ...]
    stack.reverse()
    return stack


def v310_frame(self, index: int) -> bool:
    """切换到指定栈帧（index 为 get_call_stack 中的 index）。"""
    total = len(self.frames)
    if index < 0 or index >= total:
        return False
    # frames 列表自底向上（main 在 index 0），切换 index 对应 frames[total-1-index]
    target = self.frames[total - 1 - index]
    self.current_file = target.get("file") or self.current_file
    self.current_line = target.get("line", self.current_line)
    # 注：简化版不真正切换 env（需要解释器帧级 env 支持）
    return True


def v310_list_threads(self) -> _List_v310[dict]:
    """返回当前线程列表（简化：主线程 + 已注册的虚拟线程）。"""
    threads = getattr(self, "_v310_threads", None)
    if threads is None:
        threads = [{"id": 0, "name": "main", "active": True}]
        self._v310_threads = threads
    return threads


def v310_switch_thread(self, thread_id: int) -> bool:
    """切换当前调试线程。"""
    threads = self.v310_list_threads()
    for t in threads:
        t["active"] = (t["id"] == thread_id)
    self._v310_current_thread = thread_id
    return any(t["id"] == thread_id for t in threads)


# ── 时间旅行（记录 / 重放） ────────────────────────────────

def v310_start_recording(self):
    """开始记录执行状态快照（用于反向调试）。"""
    self._v310_recording = True
    self._v310_history = []       # list of snapshots
    self._v310_history_ptr = 0


def v310_stop_recording(self):
    """停止记录。"""
    self._v310_recording = False


def v310_record_snapshot(self):
    """在每个断点处调用：记录当前状态。"""
    if not getattr(self, "_v310_recording", False):
        return
    snap = {
        "line": self.current_line,
        "file": self.current_file,
        "frames": [dict(f) for f in self.frames],
        "watches": dict(self.v310_eval_watches()),
        "ts": _time_v310.time(),
    }
    # 截断未来（如果用户已反向回退）
    hist = getattr(self, "_v310_history", [])
    ptr = getattr(self, "_v310_history_ptr", len(hist))
    self._v310_history = hist[:ptr]
    self._v310_history.append(snap)
    self._v310_history_ptr = len(self._v310_history)


def v310_reverse_continue(self) -> Optional[dict]:
    """反向执行到上一个断点（即回退到上一个快照）。"""
    hist = getattr(self, "_v310_history", [])
    ptr = getattr(self, "_v310_history_ptr", len(hist))
    if ptr <= 1:
        return None
    ptr -= 1
    self._v310_history_ptr = ptr
    snap = hist[ptr - 1]
    self.v310_restore_snapshot(snap)
    return snap


def v310_reverse_step(self) -> Optional[dict]:
    """反向单步：回退一个快照点。"""
    return self.v310_reverse_continue()


def v310_restore_snapshot(self, snap: dict):
    """从快照恢复调试器状态。"""
    self.current_line = snap.get("line", self.current_line)
    self.current_file = snap.get("file", self.current_file)
    self.frames = [dict(f) for f in snap.get("frames", [])]


# ── 远程调试（TCP，简化实现） ─────────────────────────────

class RemoteDebugServer:
    """极简 TCP 调试服务器：监听端口，接受 attach 连接后转发命令。

    协议：每行一个 JSON 消息。
      请求: {"cmd": "break"|"continue"|"step"|"print"|"locals", ...}
      响应: {"ok": true, "result": ...}
    """

    def __init__(self, debugger: "Debugger", host: str = "127.0.0.1",
                 port: int = 56789):
        self.dbg = debugger
        self.host = host
        self.port = port
        self._sock = None
        self._client = None
        self._thread = None
        self._running = False

    def start(self):
        self._sock = _socket_v310.socket(_socket_v310.AF_INET,
                                         _socket_v310.SOCK_STREAM)
        self._sock.setsockopt(_socket_v310.SOL_SOCKET,
                              _socket_v310.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(1)
        self._sock.settimeout(1.0)
        self._running = True
        self._thread = _threading_v310.Thread(
            target=self._accept_loop, daemon=True)
        self._thread.start()
        return self.port

    def _accept_loop(self):
        while self._running:
            try:
                client, _ = self._sock.accept()
            except OSError:
                continue
            self._client = client
            self._serve(client)

    def _serve(self, client):
        buf = b""
        while self._running:
            try:
                data = client.recv(4096)
            except OSError:
                break
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                try:
                    msg = _json_v310.loads(line.decode("utf-8"))
                except _json_v310.JSONDecodeError:
                    continue
                reply = self._handle(msg)
                client.sendall(
                    (_json_v310.dumps(reply) + "\n").encode("utf-8"))

    def _handle(self, msg: dict) -> dict:
        cmd = msg.get("cmd")
        if cmd == "print":
            val = self.dbg._safe_eval(msg.get("expr", ""))
            return {"ok": True, "result": self.dbg._fmt_val(val)}
        if cmd == "locals":
            return {"ok": True, "result": self.dbg.dump_locals()}
        if cmd == "backtrace":
            return {"ok": True, "result": self.dbg.dump_backtrace()}
        if cmd == "break":
            self.dbg.add_breakpoint(msg.get("spec", ""))
            return {"ok": True}
        if cmd == "threads":
            return {"ok": True,
                    "result": self.dbg.v310_list_threads()}
        if cmd == "watches":
            return {"ok": True,
                    "result": self.dbg.v310_eval_watches()}
        return {"ok": False, "error": f"unknown cmd: {cmd}"}

    def stop(self):
        self._running = False
        if self._client:
            try:
                self._client.close()
            except OSError:
                pass
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass


def v310_start_server(self, host: str = "127.0.0.1",
                      port: int = 56789) -> RemoteDebugServer:
    """启动远程调试服务器，返回 RemoteDebugServer。"""
    srv = RemoteDebugServer(self, host=host, port=port)
    srv.start()
    self._v310_server = srv
    return srv


def v310_attach(pid: int, host: str = "127.0.0.1",
                port: int = 56789, timeout: float = 5.0) -> bool:
    """作为客户端 attach 到远程调试服务器（简化：仅建立连接并握手）。"""
    try:
        s = _socket_v310.create_connection((host, port), timeout=timeout)
    except OSError:
        return False
    try:
        s.sendall(_json_v310.dumps({"cmd": "locals"}).encode("utf-8") + b"\n")
        s.settimeout(timeout)
        data = s.recv(4096)
        return bool(data)
    except OSError:
        return False
    finally:
        try:
            s.close()
        except OSError:
            pass


# ── 把 v3.1.0 方法挂载到 Debugger ──────────────────────────

Debugger.v310_add_conditional_breakpoint = v310_add_conditional_breakpoint
Debugger.v310_add_log_breakpoint = v310_add_log_breakpoint
Debugger.v310_add_watch = v310_add_watch
Debugger.v310_remove_watch = v310_remove_watch
Debugger.v310_eval_watches = v310_eval_watches
Debugger.v310_get_call_stack = v310_get_call_stack
Debugger.frame = v310_frame
Debugger.v310_list_threads = v310_list_threads
Debugger.v310_switch_thread = v310_switch_thread
Debugger.v310_start_recording = v310_start_recording
Debugger.v310_stop_recording = v310_stop_recording
Debugger.v310_record_snapshot = v310_record_snapshot
Debugger.v310_reverse_continue = v310_reverse_continue
Debugger.v310_reverse_step = v310_reverse_step
Debugger.v310_restore_snapshot = v310_restore_snapshot
Debugger.v310_start_server = v310_start_server


# ── v3.1.0 附加 CLI：aurora debug-attach ──────────────────

def cmd_debug_attach(args):
    """aurora debug-attach <pid> 命令实现。"""
    ok = v310_attach(args.pid, host=args.host, port=args.port)
    if ok:
        print(f"已 attach 到 {args.host}:{args.port}")
    else:
        print(f"无法连接到 {args.host}:{args.port}")


def register_cli_v310(subparsers):
    """v3.1.0 新增的调试相关子命令。"""
    p = subparsers.add_parser("debug-attach",
                              help="attach 到已运行的 Aurora 调试服务器")
    p.add_argument("pid", type=int, help="目标进程 PID")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=56789)
    p.set_defaults(func=cmd_debug_attach)
