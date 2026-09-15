#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aurora v3.0.0 AI 引擎性能基准测试。

对比 Aurora Tensor / DataFrame 与纯 Python(list / dict 列表)实现的耗时。
当前 Tensor 为纯 Python 参考实现(扁平化 list + shape/strides 索引),
因此预期在大矩阵上比优化过的纯 Python 手写循环略慢或相当——本脚本
诚实测量,不编造数据。

用法:
    cd /Users/wuyuanduo/aurora
    python3 benchmarks/ai_benchmark.py
"""

import os
import sys
import time
import random
import platform
import subprocess

# 把项目父目录加入 sys.path,以便独立运行时导入 aurora 包
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(_PROJECT_ROOT))

from aurora.ai.tensor import Tensor            # noqa: E402
from aurora.ai.data import DataFrame            # noqa: E402

try:  # 可选加速对比
    import numpy as _np                          # type: ignore
    HAS_NUMPY = True
except Exception:                                # pragma: no cover
    _np = None
    HAS_NUMPY = False

RUNS = 3  # 每个测试重复次数,取平均


def bench(fn, runs=RUNS):
    """运行 runs 次,返回平均耗时(毫秒)。"""
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000.0)
    return sum(times) / len(times)


# ---------------------------------------------------------------------------
# 基准 1: 张量元素运算
# ---------------------------------------------------------------------------
def benchmark_elementwise():
    N = 100  # 100x100 = 10000 元素(纯 Python 大矩阵太慢,缩小规模)
    a = Tensor.randn((N, N))
    b = Tensor.randn((N, N))
    pa = [random.gauss(0, 1) for _ in range(N * N)]
    pb = [random.gauss(0, 1) for _ in range(N * N)]

    def aurora_add():
        return a + b

    def py_add():
        return [x + y for x, y in zip(pa, pb)]

    row = {"size": f"{N}x{N}"}
    row["aurora"] = bench(aurora_add)
    row["python"] = bench(py_add)
    if HAS_NUMPY:
        na, nb = _np.array(a.data).reshape(N, N), _np.array(b.data).reshape(N, N)

        def np_add():
            return na + nb
        row["numpy"] = bench(np_add)
    return row


# ---------------------------------------------------------------------------
# 基准 2: 矩阵乘法
# ---------------------------------------------------------------------------
def benchmark_matmul():
    N = 100
    a = Tensor.randn((N, N))
    b = Tensor.randn((N, N))
    pa = a.data
    pb = b.data

    def aurora_mm():
        return a.matmul(b)

    def py_mm():
        out = [0.0] * (N * N)
        for i in range(N):
            base = i * N
            for k in range(N):
                aik = pa[base + k]
                kb = k * N
                for j in range(N):
                    out[base + j] += aik * pb[kb + j]
        return out

    row = {"size": f"{N}x{N}"}
    row["aurora"] = bench(aurora_mm)
    row["python"] = bench(py_mm)
    if HAS_NUMPY:
        na = _np.array(pa).reshape(N, N)
        nb = _np.array(pb).reshape(N, N)

        def np_mm():
            return na @ nb
        row["numpy"] = bench(np_mm)
    return row


# ---------------------------------------------------------------------------
# 基准 3: 通用函数(sigmoid / relu / exp)
# ---------------------------------------------------------------------------
def benchmark_unary():
    M = 100000
    t = Tensor.randn((M,))
    vals = t.data

    def aurora_fn():
        x = t.sigmoid()
        x = x.relu()
        return x.exp()

    def py_fn():
        import math
        out = []
        for v in vals:
            s = 1.0 / (1.0 + math.exp(-v)) if v >= 0 else \
                math.exp(v) / (1.0 + math.exp(v))
            r = s if s > 0 else 0.0
            out.append(math.exp(r))
        return out

    row = {"size": f"{M} elems"}
    row["aurora"] = bench(aurora_fn)
    row["python"] = bench(py_fn)
    if HAS_NUMPY:
        nv = _np.array(vals)

        def np_fn():
            s = _np.where(nv >= 0, 1.0 / (1.0 + _np.exp(-nv)),
                          _np.exp(nv) / (1.0 + _np.exp(nv)))
            return _np.exp(_np.maximum(s, 0.0))
        row["numpy"] = bench(np_fn)
    return row


# ---------------------------------------------------------------------------
# 基准 4: 数据处理 (DataFrame)
# ---------------------------------------------------------------------------
def benchmark_dataframe():
    ROWS = 5000
    rng = random.Random(0)
    rows = []
    for i in range(ROWS):
        rows.append({
            "grp": rng.choice(["a", "b", "c"]),
            "x": rng.gauss(0, 1),
            "y": rng.gauss(5, 2),
            "z": rng.gauss(-3, 0.5),
        })
    df = DataFrame(rows)

    def aurora_gb():
        return df.groupby("grp").mean()

    def py_gb():
        agg = {}
        for r in rows:
            g = r["grp"]
            d = agg.setdefault(g, {"x": [], "y": [], "z": []})
            d["x"].append(r["x"])
            d["y"].append(r["y"])
            d["z"].append(r["z"])
        return {g: {k: sum(v) / len(v) for k, v in d.items()}
                for g, d in agg.items()}

    def aurora_filter():
        return df.filter(lambda r: r["x"] > 0.5)

    def py_filter():
        return [r for r in rows if r["x"] > 0.5]

    def aurora_std():
        return df.standardize(["x", "y"])

    def py_std():
        xs = [r["x"] for r in rows]
        m = sum(xs) / len(xs)
        var = sum((v - m) ** 2 for v in xs) / len(xs)
        sd = var ** 0.5 or 1.0
        return [(v - m) / sd for v in xs]

    return {
        "groupby_mean": {
            "size": f"{ROWS} rows",
            "aurora": bench(aurora_gb),
            "python": bench(py_gb),
        },
        "filter": {
            "size": f"{ROWS} rows",
            "aurora": bench(aurora_filter),
            "python": bench(py_filter),
        },
        "standardize": {
            "size": f"{ROWS} rows",
            "aurora": bench(aurora_std),
            "python": bench(py_std),
        },
    }


# ---------------------------------------------------------------------------
# 基准 5: 启动时间
# ---------------------------------------------------------------------------
def benchmark_startup():
    # Python 解释器空启动
    py_t = bench(lambda: subprocess.run(
        [sys.executable, "-c", "pass"],
        capture_output=True), runs=5)
    # import aurora 包(含 AI 子模块导入开销)
    imp_t = bench(lambda: subprocess.run(
        [sys.executable, "-c", "import aurora; import aurora.ai"],
        capture_output=True), runs=5)
    return {"python_empty": py_t, "aurora_import": imp_t}


# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------
def fmt(ms):
    if ms < 1.0:
        return f"{ms*1000:.0f} us"
    return f"{ms:.2f} ms"


def speedup(aurora_ms, python_ms):
    if aurora_ms <= 0:
        return "inf"
    return f"{python_ms / aurora_ms:.2f}x"


def main():
    print("=" * 64)
    print("Aurora v3.0.0 AI 引擎性能基准")
    print("=" * 64)
    print(f"机器      : {platform.machine()} ({platform.processor() or 'Apple Silicon'})")
    print(f"系统      : {platform.system()} {platform.release()}")
    print(f"Python    : {platform.python_version()}")
    print(f"Aurora    : 3.0.0")
    print(f"NumPy     : {'可用 ' + _np.__version__ if HAS_NUMPY else '不可用(仅对比纯 Python)'}")
    print(f"每测试重复: {RUNS} 次取平均")
    print()

    print("[1/5] 张量元素运算 ...")
    r1 = benchmark_elementwise()
    print("[2/5] 矩阵乘法 ...")
    r2 = benchmark_matmul()
    print("[3/5] 通用函数 (sigmoid+relu+exp) ...")
    r3 = benchmark_unary()
    print("[4/5] 数据处理 (DataFrame) ...")
    r4 = benchmark_dataframe()
    print("[5/5] 启动时间 ...")
    r5 = benchmark_startup()

    print()
    print("=" * 64)
    print("结果汇总 (单位 ms,越小越好;加速比 = Python / Aurora)")
    print("=" * 64)

    def row_line(op, r, extra_numpy=False):
        line = f"{op:<28} | Aurora {fmt(r['aurora']):>10} | Python {fmt(r['python']):>10} | 加速 {speedup(r['aurora'], r['python']):>8}"
        if extra_numpy and "numpy" in r:
            line += f" | NumPy {fmt(r['numpy']):>10}"
        return line

    print(row_line(f"元素相加 ({r1['size']})", r1, True))
    print(row_line(f"矩阵乘法 ({r2['size']})", r2, True))
    print(row_line(f"逐元素函数 ({r3['size']})", r3, True))
    for op, r in r4.items():
        print(row_line(f"DF.{op} ({r['size']})", r))
    print(f"{'启动: python -c pass':<28} | {'':>10} | {fmt(r5['python_empty']):>10} |")
    print(f"{'启动: import aurora.ai':<28} | {fmt(r5['aurora_import']):>10} | {'':>10} |")
    print()

    # 输出机器可读 JSON,供报告引用
    import json
    out = {
        "env": {
            "machine": platform.machine(),
            "system": platform.system(),
            "python": platform.python_version(),
            "aurora": "3.0.0",
            "numpy": _np.__version__ if HAS_NUMPY else None,
        },
        "elementwise": r1,
        "matmul": r2,
        "unary": r3,
        "dataframe": r4,
        "startup": r5,
    }
    print("--- JSON ---")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
