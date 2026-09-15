"""Aurora v3.1.0 基准测试框架

``aurora bench`` 命令：跑内置微基准、记录历史、检测性能回归。

内置套件：

* ``fibonacci`` — 递归斐波那契（CPU 分支预测）；
* ``matrix_multiply`` — N×N 矩阵乘（CPU cache / 向量化）；
* ``string_concat`` — 字符串累加（分配器 / GC）；
* ``loop_iteration`` — 纯循环空转（解释器开销）；
* ``dict_access`` — 哈希表读写（字典 / map 性能）；
* ``json_parse`` — JSON 文本解析（分配器 + 字符串）。

对比基线：用纯 Python 实现 Aurora 参考版本；C++/Mojo 条目标注为
「需要外部环境」，不在本机实际运行。

回归检测：把每次结果写到 ``.aurora_bench_history.json``，与上一次对比，
任何 benchmark 慢于阈值（默认 20%）即视为回归。
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


HISTORY_FILE = ".aurora_bench_history.json"
REGRESSION_THRESHOLD = 0.20  # 20% 即视为回归


# ---------------------------------------------------------------------------
# 内置基准
# ---------------------------------------------------------------------------

def _fib(n: int) -> int:
    if n < 2:
        return n
    return _fib(n - 1) + _fib(n - 2)


def fibonacci() -> int:
    return _fib(22)


def matrix_multiply() -> int:
    n = 32
    a = [[i * j for j in range(n)] for i in range(n)]
    b = [[(i + j) % 7 for j in range(n)] for i in range(n)]
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = a[i][k]
            for j in range(n):
                c[i][j] += aik * b[k][j]
    return sum(c[i][j] for i in range(n) for j in range(n))


def string_concat() -> int:
    s = ""
    for i in range(2000):
        s += "ab"
    return len(s)


def loop_iteration() -> int:
    total = 0
    for i in range(200000):
        total += i
    return total


def dict_access() -> int:
    d = {f"k{i}": i for i in range(5000)}
    acc = 0
    for i in range(5000):
        acc += d[f"k{i}"]
    return acc


def json_parse() -> int:
    text = '{"a": 1, "b": [1, 2, 3], "c": {"d": "hello"}, "e": null, "f": true}'
    acc = 0
    for _ in range(500):
        obj = json.loads(text)
        acc += obj["a"] + len(obj["b"])
    return acc


BUILTIN_SUITES: Dict[str, Callable[[], Any]] = {
    "fibonacci": fibonacci,
    "matrix_multiply": matrix_multiply,
    "string_concat": string_concat,
    "loop_iteration": loop_iteration,
    "dict_access": dict_access,
    "json_parse": json_parse,
}


#: 外部语言参考基线（仅标注，不在本机执行）
EXTERNAL_BASELINES: Dict[str, Dict[str, str]] = {
    "fibonacci": {"C++": "需 g++ -O2 外部环境", "Mojo": "需 mojo 外部环境"},
    "matrix_multiply": {"C++": "需 g++ -O3 -march=native 外部环境", "Mojo": "需 mojo 外部环境"},
    "string_concat": {"C++": "需 g++ -O2 外部环境", "Mojo": "需 mojo 外部环境"},
    "loop_iteration": {"C++": "需 g++ -O2 外部环境", "Mojo": "需 mojo 外部环境"},
    "dict_access": {"C++": "需 libstdc++ 外部环境", "Mojo": "需 mojo 外部环境"},
    "json_parse": {"C++": "需 cJSON/nlohmann 外部环境", "Mojo": "需 mojo 外部环境"},
}


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkResult:
    name: str
    iterations: int
    total_seconds: float
    mean_ms: float
    min_ms: float
    max_ms: float
    result: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "iterations": self.iterations,
            "total_seconds": round(self.total_seconds, 6),
            "mean_ms": round(self.mean_ms, 3),
            "min_ms": round(self.min_ms, 3),
            "max_ms": round(self.max_ms, 3),
        }


# ---------------------------------------------------------------------------
# 运行器
# ---------------------------------------------------------------------------

def run_benchmark(
    name: str, func: Callable[[], Any], iterations: int = 5
) -> BenchmarkResult:
    """跑单个基准，返回 :class:`BenchmarkResult`。"""
    # 预热一次
    warmup = func()
    times: List[float] = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        val = func()
        times.append(time.perf_counter() - t0)
        warmup = val
    total = sum(times)
    return BenchmarkResult(
        name=name,
        iterations=iterations,
        total_seconds=total,
        mean_ms=total / iterations * 1000.0,
        min_ms=min(times) * 1000.0,
        max_ms=max(times) * 1000.0,
        result=warmup,
    )


@dataclass
class BenchmarkRunner:
    """批量运行内置基准，支持过滤 / 回归检测。"""

    suites: Dict[str, Callable[[], Any]] = field(default_factory=lambda: dict(BUILTIN_SUITES))
    iterations: int = 5
    history_file: str = HISTORY_FILE
    regression_threshold: float = REGRESSION_THRESHOLD

    def run(self, filter_name: Optional[str] = None) -> List[BenchmarkResult]:
        names = (
            [filter_name] if filter_name in self.suites else list(self.suites.keys())
        )
        out: List[BenchmarkResult] = []
        for name in names:
            out.append(run_benchmark(name, self.suites[name], self.iterations))
        return out

    # ── 历史 / 回归 ──────────────────────────────────

    def save_history(self, results: List[BenchmarkResult]) -> str:
        payload = {
            "saved_at": time.time(),
            "results": {r.name: r.to_dict() for r in results},
        }
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return self.history_file

    def load_history(self) -> Dict[str, Any]:
        if not os.path.isfile(self.history_file):
            return {}
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f).get("results", {})
        except (json.JSONDecodeError, OSError):
            return {}

    def detect_regression(
        self, results: List[BenchmarkResult]
    ) -> List[Dict[str, Any]]:
        """与历史对比，返回回归列表。"""
        prev = self.load_history()
        regressions: List[Dict[str, Any]] = []
        for r in results:
            old = prev.get(r.name)
            if not old:
                continue
            old_mean = old.get("mean_ms", 0)
            if old_mean <= 0:
                continue
            ratio = r.mean_ms / old_mean
            if ratio > 1 + self.regression_threshold:
                regressions.append(
                    {
                        "name": r.name,
                        "old_mean_ms": old_mean,
                        "new_mean_ms": r.mean_ms,
                        "slowdown_x": round(ratio, 3),
                    }
                )
        return regressions

    # ── 输出 ──────────────────────────────────────────

    def format_table(self, results: List[BenchmarkResult]) -> str:
        header = f"{'benchmark':<20} {'iters':>6} {'mean(ms)':>10} {'min(ms)':>10} {'max(ms)':>10}"
        sep = "-" * len(header)
        rows = [header, sep]
        for r in results:
            rows.append(
                f"{r.name:<20} {r.iterations:>6} {r.mean_ms:>10.3f} "
                f"{r.min_ms:>10.3f} {r.max_ms:>10.3f}"
            )
        return "\n".join(rows)

    def compare_with(
        self, results: List[BenchmarkResult], other_file: str
    ) -> List[Dict[str, Any]]:
        """与另一份历史结果文件对比。"""
        with open(other_file, "r", encoding="utf-8") as f:
            other = json.load(f).get("results", {})
        out: List[Dict[str, Any]] = []
        for r in results:
            o = other.get(r.name)
            if not o:
                continue
            out.append(
                {
                    "name": r.name,
                    "other_mean_ms": o.get("mean_ms"),
                    "current_mean_ms": round(r.mean_ms, 3),
                    "delta_pct": round(
                        (r.mean_ms - o.get("mean_ms", 0)) / max(o.get("mean_ms", 1), 1e-9) * 100,
                        2,
                    ),
                }
            )
        return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def register_cli(subparsers) -> Any:
    """在主 CLI 上注册 ``aurora bench`` 子命令。"""
    p = subparsers.add_parser('bench', help='v3.1.0 基准测试与回归检测')
    p.add_argument('--iterations', type=int, default=5, help='每个基准迭代次数')
    p.add_argument('--filter', default=None, help='只跑指定名字的基准')
    p.add_argument('--json', action='store_true', help='JSON 输出')
    p.add_argument(
        '--compare',
        default=None,
        metavar='FILE',
        help='与历史基准文件对比',
    )
    p.add_argument(
        '--threshold',
        type=float,
        default=REGRESSION_THRESHOLD,
        help=f'回归阈值（默认 {REGRESSION_THRESHOLD}）',
    )
    p.set_defaults(func=_cmd_bench)
    return p


def _cmd_bench(args) -> None:
    runner = BenchmarkRunner(
        iterations=args.iterations,
        regression_threshold=args.threshold,
    )
    results = runner.run(filter_name=args.filter)
    runner.save_history(results)

    if args.json:
        payload: Dict[str, Any] = {
            "results": [r.to_dict() for r in results],
            "external_baselines": EXTERNAL_BASELINES,
        }
        if args.compare:
            payload["compare"] = runner.compare_with(results, args.compare)
        else:
            payload["regressions"] = runner.detect_regression(results)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(runner.format_table(results))
    print()
    print("外部语言参考（需外部环境，未实际运行）：")
    for name, refs in EXTERNAL_BASELINES.items():
        if args.filter and name != args.filter:
            continue
        for lang, note in refs.items():
            print(f"  {name:<18} {lang:<6} {note}")

    if args.compare:
        print(f"\n与 {args.compare} 对比：")
        for row in runner.compare_with(results, args.compare):
            print(
                f"  {row['name']:<18} {row['other_mean_ms']} -> "
                f"{row['current_mean_ms']} ms ({row['delta_pct']:+.2f}%)"
            )
    else:
        regs = runner.detect_regression(results)
        if regs:
            print("\n⚠ 检测到性能回归：")
            for r in regs:
                print(
                    f"  {r['name']:<18} {r['old_mean_ms']:.2f} -> "
                    f"{r['new_mean_ms']:.2f} ms ({r['slowdown_x']:.2f}x)"
                )
        else:
            print("\n✓ 未检测到性能回归")
