"""Aurora 函数级增量编译缓存

基于函数 AST 内容哈希的编译产物缓存。
- 函数体未改变时直接复用缓存的编译结果，跳过重新编译；
- 缓存键是 AST 内容的 SHA256，不依赖文件名，函数移动到别的文件仍能命中；
- 磁盘持久化（JSON），跨编译会话复用；
- 简单调用图依赖跟踪：函数 A 调用函数 B，B 变更后 A 一并失效。

注意：本模块只定义 CompiledFunction 数据类与缓存逻辑，
不实际修改 codegen.py / asmgen.py；它们在编译流程中通过
cache.get / cache.put 接入即可。
"""

import os
import json
import time
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Set


@dataclass
class CompiledFunction:
    """一个函数的编译产物（占位结构，供 codegen/asmgen 填充）"""
    name: str
    func_hash: str
    machine_code: str = ""          # 真实后端中为字节码/汇编
    depends_on: List[str] = field(default_factory=list)  # 调用到的函数名
    compiled_at: float = 0.0
    compile_time_ms: float = 0.0


# ── AST 序列化（确定性、可哈希）────────────────────────────

def _serialize_node(node: Any) -> Any:
    """把 AST 节点树序列化为可 JSON 化的确定性结构。

    只取影响语义的字段，忽略 line/column 等位置信息，
    这样纯格式化/换行变化不会导致缓存失效。
    """
    if node is None or isinstance(node, (str, int, float, bool)):
        return node
    if isinstance(node, (list, tuple)):
        return [_serialize_node(x) for x in node]
    if isinstance(node, dict):
        return {k: _serialize_node(v) for k, v in sorted(node.items())}
    # dataclass / 普通对象
    cls_name = type(node).__name__
    if hasattr(node, "__dataclass_fields__"):
        out: Dict[str, Any] = {"__type__": cls_name}
        for fname, fval in vars(node).items():
            if fname in ("line", "column", "inferred_type"):
                continue
            out[fname] = _serialize_node(fval)
        return out
    return repr(node)


def _collect_callees(node: Any, out: Set[str]) -> None:
    """简单调用图：收集函数体内调用到的用户函数名（Identifier 作为 callee）"""
    from .ast_nodes import CallExpr, Identifier, MethodCall
    if node is None or isinstance(node, (str, int, float, bool)):
        return
    if isinstance(node, (list, tuple)):
        for x in node:
            _collect_callees(x, out)
        return
    if isinstance(node, CallExpr) and isinstance(node.callee, Identifier):
        out.add(node.callee.name)
    # 遍历 dataclass 字段
    if hasattr(node, "__dataclass_fields__"):
        for fname, fval in vars(node).items():
            _collect_callees(fval, out)


class IncrementalCompilerCache:
    """函数级增量编译缓存"""

    def __init__(self, cache_dir: str = "~/.aurora/cache"):
        self.cache_dir = os.path.expanduser(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        self._index_path = os.path.join(self.cache_dir, "index.json")
        # 内存索引：func_hash -> CompiledFunction 字段
        self._index: Dict[str, dict] = {}
        # 函数名 -> func_hash（用于 invalidate by name）
        self._name_to_hash: Dict[str, str] = {}
        # 调用图：name -> set(callee names)
        self._call_graph: Dict[str, Set[str]] = {}
        self._hits = 0
        self._misses = 0
        self._saved_ms = 0.0
        self._load()

    # ── 哈希 ──────────────────────────────────────────

    def function_hash(self, func_ast) -> str:
        """计算函数内容哈希（函数名+参数+返回类型+函数体 AST 序列化）"""
        payload = {
            "name": getattr(func_ast, "name", ""),
            "params": _serialize_node(getattr(func_ast, "params", [])),
            "return_type": _serialize_node(getattr(func_ast, "return_type", None)),
            "body": _serialize_node(getattr(func_ast, "body", None)),
        }
        blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    # ── 读写 ──────────────────────────────────────────

    def get(self, func_ast) -> Optional[CompiledFunction]:
        """获取缓存的编译结果；未命中返回 None"""
        h = self.function_hash(func_ast)
        entry = self._index.get(h)
        if entry is None:
            self._misses += 1
            return None
        self._hits += 1
        self._saved_ms += float(entry.get("compile_time_ms", 0.0))
        return CompiledFunction(**entry)

    def put(self, func_ast, compiled: CompiledFunction) -> None:
        """存入编译结果"""
        h = self.function_hash(func_ast)
        compiled.func_hash = h
        if not compiled.compiled_at:
            compiled.compiled_at = time.time()
        self._index[h] = asdict(compiled)
        self._name_to_hash[compiled.name] = h
        # 依赖跟踪
        callees = _collect_callees_safe(func_ast)
        self._call_graph[compiled.name] = callees
        self._save()

    # ── 失效 ──────────────────────────────────────────

    def invalidate(self, func_name: str) -> None:
        """使某个函数的缓存失效；并级联失效所有依赖它的调用者"""
        h = self._name_to_hash.get(func_name)
        if h is not None:
            self._index.pop(h, None)
            self._name_to_hash.pop(func_name, None)
        # 反向依赖：谁调用了 func_name，谁就失效
        dependents = self._reverse_dependents(func_name)
        for dep in dependents:
            dh = self._name_to_hash.get(dep)
            if dh is not None:
                self._index.pop(dh, None)
                self._name_to_hash.pop(dep, None)
        self._call_graph.pop(func_name, None)
        self._save()

    def _reverse_dependents(self, func_name: str) -> List[str]:
        """返回所有调用了 func_name 的函数名"""
        result = []
        for caller, callees in self._call_graph.items():
            if func_name in callees:
                result.append(caller)
        return result

    def clear(self) -> None:
        """清空所有缓存"""
        self._index.clear()
        self._name_to_hash.clear()
        self._call_graph.clear()
        self._hits = 0
        self._misses = 0
        self._saved_ms = 0.0
        self._save()

    # ── 统计 ──────────────────────────────────────────

    def stats(self) -> dict:
        """缓存统计：命中率、总条目、节省编译时间"""
        total = self._hits + self._misses
        return {
            "entries": len(self._index),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": (self._hits / total) if total else 0.0,
            "saved_compile_time_ms": round(self._saved_ms, 3),
            "call_graph_size": len(self._call_graph),
            "cache_dir": self.cache_dir,
        }

    # ── 持久化 ────────────────────────────────────────

    def _save(self) -> None:
        data = {
            "index": self._index,
            "name_to_hash": self._name_to_hash,
            "call_graph": {k: sorted(v) for k, v in self._call_graph.items()},
            "hits": self._hits,
            "misses": self._misses,
            "saved_ms": self._saved_ms,
        }
        tmp = self._index_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, self._index_path)

    def _load(self) -> None:
        if not os.path.exists(self._index_path):
            return
        try:
            with open(self._index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return
        self._index = data.get("index", {})
        self._name_to_hash = data.get("name_to_hash", {})
        self._call_graph = {k: set(v) for k, v in data.get("call_graph", {}).items()}
        self._hits = data.get("hits", 0)
        self._misses = data.get("misses", 0)
        self._saved_ms = data.get("saved_ms", 0.0)


def _collect_callees_safe(func_ast) -> Set[str]:
    out: Set[str] = set()
    try:
        _collect_callees(getattr(func_ast, "body", None), out)
    except Exception:
        pass
    return out
