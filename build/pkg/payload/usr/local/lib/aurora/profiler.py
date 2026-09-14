"""Aurora 性能分析器 — 基于解释器执行采集函数级性能数据。

工作原理：
* 继承 :class:`~aurora.interpreter.Interpreter`，覆写 ``_make_function`` /
  ``_make_lambda``，把每个 Aurora 用户函数包装成带计时的调用器；
* 用 ``time.perf_counter()`` 在函数入口/出口打点，维护调用栈，从而
  同时得到：调用次数、总耗时（inclusive）、自身耗时（exclusive，不含子调用）；
* 用 ``tracemalloc`` 统计峰值内存；
* 边执行边记录调用边（call graph）与完整调用栈，供火焰图使用。

公共 API：
* profile(source, args=None) -> ProfileResult
* print_report(result, sort_by='total_time', top_n=20)
* to_json(result) -> str
* to_flamegraph(result) -> str
* register_cli(subparsers)
"""

import os
import sys
import json
import time
import tracemalloc
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class FunctionStat:
    """单个函数的性能统计。"""
    name: str
    calls: int = 0
    total_time: float = 0.0   # 总耗时（含子调用，inclusive）
    self_time: float = 0.0    # 自身耗时（不含子调用，exclusive）

    @property
    def avg_time(self) -> float:
        return self.total_time / self.calls if self.calls else 0.0


@dataclass
class ProfileResult:
    """一次性能分析的完整结果。"""
    functions: Dict[str, FunctionStat] = field(default_factory=dict)
    total_time: float = 0.0
    peak_memory: int = 0
    call_graph: Dict[str, Dict[str, int]] = field(default_factory=dict)
    # 行级统计（可选，默认关闭）：{(file, line): [calls, time]}
    line_stats: Dict[str, List[float]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# 采集器
# ---------------------------------------------------------------------------

class _ProfileCollector:
    """在函数入口/出口打点，统计调用次数、耗时与调用图。"""

    def __init__(self):
        self.functions: Dict[str, FunctionStat] = {}
        self.call_graph: Dict[str, Dict[str, int]] = {}
        # 调用栈：每项 (name, start_time, child_time)
        self._stack: List[list] = []
        # 已见调用栈路径 -> 次数（火焰图用）
        self._stacks: Dict[str, int] = {}

    def _stat(self, name: str) -> FunctionStat:
        st = self.functions.get(name)
        if st is None:
            st = FunctionStat(name=name)
            self.functions[name] = st
        return st

    def wrap(self, fn: Callable, name: str) -> Callable:
        """把一个 Aurora 函数包装成带计时的可调用对象。"""
        collector = self

        def profiled(*args, **kwargs):
            now = time.perf_counter()
            # 调用图：记录 caller -> callee
            caller = collector._stack[-1][0] if collector._stack else None
            if caller is not None:
                edges = collector.call_graph.setdefault(caller, {})
                edges[name] = edges.get(name, 0) + 1

            collector._stack.append([name, now, 0.0])
            stack_path = ";".join(frame[0] for frame in collector._stack)
            collector._stacks[stack_path] = collector._stacks.get(stack_path, 0) + 1
            stat = collector._stat(name)
            stat.calls += 1
            try:
                return fn(*args, **kwargs)
            finally:
                end = time.perf_counter()
                frame = collector._stack.pop()
                duration = end - frame[1]
                self_time = duration - frame[2]
                stat.total_time += duration
                stat.self_time += self_time
                # 把本次耗时累加到父帧的子调用时间，用于计算父函数自身耗时
                if collector._stack:
                    collector._stack[-1][2] += duration

        # 保留 Aurora 函数的标识，便于解释器内部识别
        profiled.__name__ = getattr(fn, "__name__", name)
        profiled._aurora = getattr(fn, "_aurora", True)
        profiled._ast = getattr(fn, "_ast", None)
        return profiled


class _ProfiledInterpreter(Interpreter):
    """注入计时包装的解释器。"""

    def __init__(self, collector: _ProfileCollector):
        super().__init__()
        self._collector = collector

    def _make_function(self, fn_def, closure_env, is_impl=False):
        fn = super()._make_function(fn_def, closure_env, is_impl=is_impl)
        return self._collector.wrap(fn, fn_def.name)

    def _make_lambda(self, expr, closure_env):
        fn = super()._make_lambda(expr, closure_env)
        return self._collector.wrap(fn, "<lambda>")


# ---------------------------------------------------------------------------
# 公共 API
# ---------------------------------------------------------------------------

def profile(source: str, args: Optional[List[str]] = None) -> ProfileResult:
    """执行 Aurora 源码并采集性能数据。

    args 保留作为命令行参数占位（当前 Aurora 程序不消费它）。
    """
    if args is not None:
        sys.argv = list(args)

    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    collector = _ProfileCollector()
    interp = _ProfiledInterpreter(collector)

    tracemalloc.start()
    start = time.perf_counter()
    try:
        interp.run(program)
    finally:
        total = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    result = ProfileResult(
        functions=collector.functions,
        total_time=total,
        peak_memory=peak,
        call_graph=collector.call_graph,
    )
    # 把火焰图栈路径挂到结果上（内部使用）
    result._flame_stacks = collector._stacks  # type: ignore[attr-defined]
    return result


def to_json(result: ProfileResult) -> str:
    """导出 JSON 格式分析结果。"""
    data = {
        "total_time": round(result.total_time, 6),
        "peak_memory": result.peak_memory,
        "functions": {
            name: {
                "calls": st.calls,
                "total_time": round(st.total_time, 6),
                "self_time": round(st.self_time, 6),
                "avg_time": round(st.avg_time, 6),
            }
            for name, st in result.functions.items()
        },
        "call_graph": result.call_graph,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def to_flamegraph(result: ProfileResult) -> str:
    """导出折叠栈（folded stack）火焰图数据。

    每行 ``func1;func2;func3 count``，可直接用于 speedscope / flamegraph.pl。
    """
    stacks: Dict[str, int] = getattr(result, "_flame_stacks", {})
    lines = [f"{path} {count}" for path, count in sorted(stacks.items())]
    return "\n".join(lines) + ("\n" if lines else "")


def print_report(result: ProfileResult, sort_by: str = "total_time",
                 top_n: int = 20) -> None:
    """打印人类可读的性能分析报告。"""
    print("=" * 64)
    print("Aurora 性能分析报告")
    print("=" * 64)
    print(f"总耗时: {result.total_time * 1000:.3f} ms")
    print(f"峰值内存: {_human_size(result.peak_memory)}")
    print(f"函数数: {len(result.functions)}")
    print("-" * 64)

    rows = list(result.functions.values())
    key_map = {
        "total_time": lambda s: s.total_time,
        "self_time": lambda s: s.self_time,
        "calls": lambda s: s.calls,
        "avg_time": lambda s: s.avg_time,
    }
    key = key_map.get(sort_by, key_map["total_time"])
    rows.sort(key=key, reverse=True)
    rows = rows[:top_n]

    header = f"{'函数':<24} {'调用次数':>8} {'总耗时(ms)':>12} {'自身(ms)':>12} {'平均(ms)':>12}"
    print(header)
    print("-" * 64)
    for st in rows:
        print(f"{st.name:<24} {st.calls:>8} "
              f"{st.total_time * 1000:>12.3f} "
              f"{st.self_time * 1000:>12.3f} "
              f"{st.avg_time * 1000:>12.3f}")
    print("=" * 64)


def _human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.1f} GB"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def register_cli(subparsers):
    """注册 ``profile`` 子命令到 aurora CLI。"""
    p = subparsers.add_parser('profile', help='性能分析 Aurora 程序')
    p.add_argument('file', help='要分析的 .aur 文件')
    p.add_argument('--json', metavar='OUT', dest='json_out',
                   help='导出 JSON 到文件')
    p.add_argument('--flamegraph', metavar='OUT', dest='flame_out',
                   help='导出火焰图(折叠栈)数据到文件')
    p.add_argument('--top', type=int, default=20, help='显示前 N 个耗时函数')
    p.set_defaults(func=_cmd_profile)


def _cmd_profile(args):
    if not os.path.exists(args.file):
        print(f"错误: 文件不存在 '{args.file}'")
        sys.exit(1)
    with open(args.file, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        result = profile(source)
    except Exception as e:  # noqa: BLE001
        print(f"分析失败: {e}")
        sys.exit(1)

    print_report(result, top_n=args.top)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            f.write(to_json(result))
        print(f"JSON 已写入: {args.json_out}")

    if args.flame_out:
        with open(args.flame_out, "w", encoding="utf-8") as f:
            f.write(to_flamegraph(result))
        print(f"火焰图数据已写入: {args.flame_out}")
