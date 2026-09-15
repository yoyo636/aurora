"""Aurora v3.1.0 并行编译引擎

利用 ``concurrent.futures.ThreadPoolExecutor`` 对文件级编译流水线做并行化：

* **依赖图构建**：扫描每个源文件的 ``import`` 语句，建立文件级有向依赖图；
* **拓扑排序**：按依赖顺序分层，同一层内的文件互不依赖，可以并行编译；
* **并行执行**：用线程池把「解析 → 类型检查 → 代码生成」三个阶段流水线化，
  同层文件之间真正并行；
* **增量增强**：与 :mod:`aurora.persistent_cache` 配合，只重编译变更文件及其
  下游依赖（被谁 import 就谁失效），未变更的文件直接复用缓存产物。

目标架构：1000 文件项目冷编译 < 5 秒（在多核 / 多线程解释器下）。

公共 API：
* :class:`ParallelCompiler` — 编译引擎主类
* :func:`compile_files` — 便捷函数，``compile_files(files, workers=4)``
* :func:`register_cli` — 注册 ``aurora compile-parallel`` 子命令
"""

from __future__ import annotations

import os
import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class CompileUnit:
    """单个源文件的编译状态。"""

    path: str
    """源文件绝对路径。"""

    imports: List[str] = field(default_factory=list)
    """该文件 import 的其它文件路径（已解析为绝对路径）。"""

    ast: Any = None
    """解析阶段产出（默认模拟阶段填占位对象）。"""

    type_info: Any = None
    """类型检查阶段产出。"""

    artifact: Any = None
    """代码生成阶段产出。"""

    mtime: float = 0.0
    """文件最后修改时间。"""

    status: str = "pending"
    """pending / parsing / checked / emitted / cached / failed。"""

    duration_ms: float = 0.0
    """实际编译耗时（不含缓存命中）。"""


@dataclass
class CompileResult:
    """一次并行编译的汇总结果。"""

    units: Dict[str, CompileUnit] = field(default_factory=dict)
    elapsed_ms: float = 0.0
    compiled_count: int = 0
    cached_count: int = 0
    failed: List[str] = field(default_factory=list)
    layers: List[List[str]] = field(default_factory=list)
    """拓扑分层，每层是一组可并行的文件路径。"""

    def summary(self) -> str:
        return (
            f"[parallel-compile] {self.compiled_count} compiled, "
            f"{self.cached_count} cached, "
            f"{len(self.failed)} failed, "
            f"{len(self.layers)} layers, "
            f"{self.elapsed_ms:.1f} ms"
        )


# ---------------------------------------------------------------------------
# 依赖图
# ---------------------------------------------------------------------------

#: 匹配 Aurora import 语句的正则。支持 ``import foo`` / ``import foo.bar``。
_IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z_][\w\.]*)", re.MULTILINE)


def _resolve_import(source_file: str, module: str, roots: List[str]) -> Optional[str]:
    """把 ``import foo.bar`` 解析成具体文件路径。

    查找顺序：
    1. 相对于源文件所在目录的 ``foo/bar.aur`` 与 ``foo/bar/index.aur``；
    2. 在给定的 roots（项目根 / stdlib 目录）下查找。
    """
    rel = module.replace(".", os.sep)
    candidates = [
        os.path.normpath(os.path.join(os.path.dirname(source_file), rel + ".aur")),
        os.path.normpath(os.path.join(os.path.dirname(source_file), rel, "index.aur")),
    ]
    for root in roots:
        candidates.append(
            os.path.normpath(os.path.join(root, rel + ".aur"))
        )
        candidates.append(
            os.path.normpath(os.path.join(root, rel, "index.aur"))
        )
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def build_dependency_graph(
    files: List[str],
    roots: Optional[List[str]] = None,
) -> Tuple[Dict[str, List[str]], Dict[str, CompileUnit]]:
    """扫描文件 import 语句，构建文件级依赖图。

    :param files: 参与编译的源文件绝对路径列表。
    :param roots: 额外的模块搜索根目录（如 stdlib 目录）。
    :return: ``(graph, units)``，``graph[file] = [依赖的文件列表]``。
    """
    roots = roots or []
    units: Dict[str, CompileUnit] = {}
    graph: Dict[str, List[str]] = {}

    for path in files:
        apath = os.path.abspath(path)
        unit = CompileUnit(path=apath, mtime=os.path.getmtime(apath))
        try:
            with open(apath, "r", encoding="utf-8") as f:
                source = f.read()
        except OSError:
            units[apath] = unit
            graph[apath] = []
            continue
        deps: List[str] = []
        for m in _IMPORT_RE.finditer(source):
            resolved = _resolve_import(apath, m.group(1), roots)
            if resolved is not None and resolved != apath and resolved not in deps:
                deps.append(resolved)
                unit.imports.append(resolved)
        units[apath] = unit
        graph[apath] = deps
    return graph, units


def topological_layers(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Kahn 算法分层拓扑排序。

    同一层内的节点之间没有依赖，可以并行处理。
    若存在环，则环上节点全部放到最后一层（保证不卡死）。
    """
    indeg: Dict[str, int] = {node: 0 for node in graph}
    for node, deps in graph.items():
        for d in deps:
            indeg.setdefault(d, 0)
            indeg[node] += 1

    layers: List[List[str]] = []
    remaining = set(graph.keys())
    while remaining:
        layer = sorted(n for n in remaining if indeg[n] == 0)
        if not layer:
            # 有环：把剩余节点作为最后一层
            layers.append(sorted(remaining))
            break
        layers.append(layer)
        for node in layer:
            remaining.discard(node)
            # 所有「依赖 node」的节点入度 -1
            for other in remaining:
                if node in graph.get(other, []):
                    indeg[other] -= 1
    return layers


# ---------------------------------------------------------------------------
# 编译阶段钩子（允许替换成真实 parser / type_checker / codegen）
# ---------------------------------------------------------------------------

ParseHook = Callable[[CompileUnit], Any]
CheckHook = Callable[[CompileUnit], Any]
CodegenHook = Callable[[CompileUnit], Any]


def _default_parse(unit: CompileUnit) -> Any:
    """默认占位解析：返回文件大小作为 AST 占位。"""
    try:
        size = os.path.getsize(unit.path)
    except OSError:
        size = 0
    return {"kind": "ast", "path": unit.path, "size": size}


def _default_check(unit: CompileUnit) -> Any:
    """默认占位类型检查。"""
    return {"kind": "types", "imports": list(unit.imports)}


def _default_codegen(unit: CompileUnit) -> Any:
    """默认占位代码生成。"""
    return {"kind": "artifact", "path": unit.path}


# ---------------------------------------------------------------------------
# 并行编译器
# ---------------------------------------------------------------------------

class ParallelCompiler:
    """文件级并行编译器。

    典型用法::

        pc = ParallelCompiler(workers=4)
        result = pc.compile(["src/main.aur", "src/util.aur"])
        print(result.summary())
    """

    def __init__(
        self,
        workers: int = 4,
        roots: Optional[List[str]] = None,
        cache: Any = None,
        parse_hook: Optional[ParseHook] = None,
        check_hook: Optional[CheckHook] = None,
        codegen_hook: Optional[CodegenHook] = None,
    ) -> None:
        self.workers = max(1, workers)
        self.roots = roots or []
        self.cache = cache
        self._parse = parse_hook or _default_parse
        self._check = check_hook or _default_check
        self._codegen = codegen_hook or _default_codegen
        self._lock = threading.Lock()

    # ── 单文件编译 ─────────────────────────────────────

    def _compile_one(self, unit: CompileUnit) -> CompileUnit:
        """编译单个文件：parse → check → codegen。"""
        # 增量：先尝试缓存
        if self.cache is not None:
            cached = self.cache.get(unit.path)
            if cached is not None:
                unit.ast = cached.get("ast")
                unit.type_info = cached.get("type_info")
                unit.artifact = cached.get("artifact")
                unit.status = "cached"
                return unit

        t0 = time.perf_counter()
        try:
            unit.status = "parsing"
            unit.ast = self._parse(unit)
            unit.type_info = self._check(unit)
            unit.artifact = self._codegen(unit)
            unit.status = "emitted"
        except Exception as exc:  # noqa: BLE001 — 编译错误不中断其它文件
            unit.status = "failed"
            unit.artifact = {"error": repr(exc)}
        finally:
            unit.duration_ms = (time.perf_counter() - t0) * 1000.0

        # 写回缓存
        if self.cache is not None and unit.status == "emitted":
            self.cache.set(
                unit.path,
                {
                    "ast": unit.ast,
                    "type_info": unit.type_info,
                    "artifact": unit.artifact,
                    "imports": unit.imports,
                },
            )
        return unit

    # ── 入口 ──────────────────────────────────────────

    def compile(self, files: List[str]) -> CompileResult:
        """编译给定文件列表，按依赖分层并行执行。"""
        t0 = time.perf_counter()
        graph, units = build_dependency_graph(files, roots=self.roots)
        layers = topological_layers(graph)
        result = CompileResult(units=units, layers=layers)

        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            for layer in layers:
                futures = {
                    pool.submit(self._compile_one, units[path]): path
                    for path in layer
                }
                for fut in as_completed(futures):
                    path = futures[fut]
                    unit = units[path]
                    if unit.status == "cached":
                        result.cached_count += 1
                    elif unit.status == "emitted":
                        result.compiled_count += 1
                    elif unit.status == "failed":
                        result.failed.append(path)

        result.elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return result

    # ── 增量：只编译变更及下游 ──────────────────────────

    def compile_incremental(
        self,
        files: List[str],
        changed: Optional[Set[str]] = None,
    ) -> CompileResult:
        """增量编译：``changed`` 中的文件及其下游依赖重新编译。

        未变更且缓存命中的文件直接走缓存路径。
        """
        changed = {os.path.abspath(p) for p in (changed or [])}
        graph, units = build_dependency_graph(files, roots=self.roots)
        affected = self._downstream(graph, changed)

        # 对未受影响的文件，强制走缓存（_compile_one 内部判断）
        # 这里把变更文件从缓存中剔除，确保重编译
        if self.cache is not None:
            for path in affected:
                self.cache.invalidate(path)

        return self._run_layers(graph, units, layers=topological_layers(graph))

    # ── 内部工具 ──────────────────────────────────────

    @staticmethod
    def _downstream(
        graph: Dict[str, List[str]], seeds: Set[str]
    ) -> Set[str]:
        """返回 seeds 加上所有间接依赖它们的文件（反向闭包）。"""
        # 反向边：who -> [谁依赖 who]
        reverse: Dict[str, Set[str]] = {n: set() for n in graph}
        for node, deps in graph.items():
            for d in deps:
                reverse.setdefault(d, set()).add(node)
            reverse.setdefault(node, set())
        seen: Set[str] = set()
        stack = list(seeds)
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(reverse.get(cur, ()))
        return seen

    def _run_layers(
        self,
        graph: Dict[str, List[str]],
        units: Dict[str, CompileUnit],
        layers: List[List[str]],
    ) -> CompileResult:
        t0 = time.perf_counter()
        result = CompileResult(units=units, layers=layers)
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            for layer in layers:
                futures = {
                    pool.submit(self._compile_one, units[p]): p for p in layer
                }
                for fut in as_completed(futures):
                    u = units[futures[fut]]
                    if u.status == "cached":
                        result.cached_count += 1
                    elif u.status == "emitted":
                        result.compiled_count += 1
                    elif u.status == "failed":
                        result.failed.append(u.path)
        result.elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return result


# ---------------------------------------------------------------------------
# 便捷函数
# ---------------------------------------------------------------------------

def compile_files(
    files: List[str],
    workers: int = 4,
    cache: Any = None,
    roots: Optional[List[str]] = None,
) -> CompileResult:
    """并行编译 ``files``，返回 :class:`CompileResult`。

    :param files: 源文件路径列表。
    :param workers: 线程池大小。
    :param cache: 可选的持久化缓存（与 :mod:`aurora.persistent_cache` 兼容）。
    :param roots: 模块搜索根目录。
    """
    compiler = ParallelCompiler(workers=workers, cache=cache, roots=roots)
    return compiler.compile(files)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def register_cli(subparsers) -> Any:
    """在主 CLI 上注册 ``aurora compile-parallel`` 子命令。"""
    p = subparsers.add_parser(
        'compile-parallel', help='v3.1.0 并行编译引擎（文件级并行 + 增量）'
    )
    p.add_argument('files', nargs='+', help='要编译的 .aur 文件')
    p.add_argument('-j', '--workers', type=int, default=4, help='线程数（默认 4）')
    p.add_argument('--cache-dir', default='.aurora_cache', help='缓存目录')
    p.set_defaults(func=_cmd_compile_parallel)
    return p


def _cmd_compile_parallel(args) -> None:
    from aurora.persistent_cache import PersistentCache

    cache = PersistentCache(cache_dir=args.cache_dir)
    result = compile_files(args.files, workers=args.workers, cache=cache)
    print(result.summary())
    if result.failed:
        print("失败文件：")
        for f in result.failed:
            print(f"  - {f}")
