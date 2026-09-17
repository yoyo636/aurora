"""Aurora 增量计算引擎 — 语言级原生增量计算（v3.3.0）"""

import hashlib
import time
import threading
import weakref
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set


class IncrementalError(Exception):
    """增量计算引擎异常基类"""
    pass


@dataclass
class LiveNode:
    """增量计算图中的活节点（Live Node）

    表示一个可增量重算的计算单元。source 节点的 func 为 None。
    """
    id: int
    func: Optional[Callable]
    args: list = field(default_factory=list)
    result: Any = None
    deps: list = field(default_factory=list)          # [(node_id, version)] 依赖快照
    dependents: dict = field(default_factory=dict)    # 反向边：{node_id: weakref(dep_node)}
    state: str = "Dirty"                               # "Clean" / "Dirty" / "Computing"
    hash: int = 0                                      # 结果结构化哈希（64位）
    version: int = 0                                    # source 节点用；live 节点恒 0
    is_source: bool = False
    recompute_count: int = 0
    total_time: float = 0.0
    subscribers: list = field(default_factory=list)    # 回调列表

    @property
    def value(self) -> Any:
        """拉模式读取：触发引擎缓存查找或增量重算"""
        return IncrementalEngine.get_instance().read(self)


@dataclass
class SourceNode(LiveNode):
    """源节点（Source Node）：外部可写的输入节点

    维护 version 计数器，write 时 version += 1。
    tracked_fields 记录哪些字段路径被 live 依赖过：{field_path: set[node_id]}。
    """
    is_source: bool = True
    tracked_fields: dict = field(default_factory=dict)


class IncrementalEngine:
    """增量计算引擎（全局单例）

    核心特性：
    - 拉模式重算：source 修改只标记直接下游 Dirty，读取时才深度优先重算
    - 哈希短路：重算后哈希不变则不通知下游
    - 混合依赖追踪：source 用 version 计数器，不可变值用结构化哈希，大对象降级引用追踪
    - 事务：块内只更新值不传播，结束时统一标记
    - 字段级依赖追踪：write_field 只标记依赖该字段的 live 节点
    - 回调重入检测：订阅回调中修改依赖的 source 会抛 IncrementalError
    - GC 弱引用：dependents 以弱引用持有下游节点，惰性清理失效引用
    - 活计算结果缓存：按 (function_identity, args_hash) 缓存，函数体变更自动失效
    """

    _instance: Optional["IncrementalEngine"] = None
    _singleton_lock = threading.RLock()

    def __init__(self):
        self.nodes: Dict[int, LiveNode] = {}
        self._next_id: int = 0
        # 计算栈：当前正在计算的节点 id
        self._computing_stack: List[int] = []
        # 读取栈：与 computing_stack 平行，每层记录 {dep_id: dep_version}
        self._reads_stack: List[Dict[int, int]] = []
        # 事务
        self._transact_depth: int = 0
        self._transaction_dirty_sources: Set[int] = set()
        # 统计
        self._total_recomputes: int = 0
        self._cache_hits: int = 0
        # 回调重入检测：正在分发回调的节点 id 集合
        self._dispatching: Set[int] = set()
        # 活计算结果缓存：{(func_identity, args_hash): result}
        self._result_cache: dict = {}
        # 操作锁
        self._op_lock = threading.RLock()

    # ------------------------------------------------------------------
    # 单例管理
    # ------------------------------------------------------------------

    @classmethod
    def get_instance(cls) -> "IncrementalEngine":
        """获取全局单例"""
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    @classmethod
    def reset(cls) -> None:
        """重置单例（测试用）"""
        with cls._singleton_lock:
            cls._instance = None

    # ------------------------------------------------------------------
    # 节点创建
    # ------------------------------------------------------------------

    def _next_node_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def create_source(self, value: Any) -> SourceNode:
        """创建源节点"""
        nid = self._next_node_id()
        node = SourceNode(
            id=nid,
            func=None,
            result=value,
            hash=self.hash_value(value),
            version=0,
        )
        self.nodes[nid] = node
        return node

    def create_live(self, func: Callable,
                    captured_nodes: Optional[List] = None) -> LiveNode:
        """创建活节点

        Args:
            func: 无参数 callable，内部通过闭包读取 source/live 的 .value
            captured_nodes: 此 live 依赖的节点列表（SourceNode/LiveNode）
        """
        captured_nodes = captured_nodes or []
        deps: list = []
        for n in captured_nodes:
            ver = n.version if n.is_source else 0
            deps.append((n.id, ver))

        nid = self._next_node_id()
        node = LiveNode(
            id=nid,
            func=func,
            deps=deps,
            state="Dirty",
        )
        self.nodes[nid] = node
        # 建立反向边（弱引用）
        for n in captured_nodes:
            n.dependents[nid] = weakref.ref(node)
        return node

    # ------------------------------------------------------------------
    # 字段级依赖追踪（运行时支持；解释器集成由上层完成）
    # ------------------------------------------------------------------

    def track_field(self, source_node: SourceNode, field_path: str,
                    live_node_id: int) -> None:
        """注册：live 节点 live_node_id 读取了 source_node 的字段 field_path。

        解释器在 live 计算时遇到 MemberAccess 读取 source 字段时调用。
        """
        source_node.tracked_fields.setdefault(field_path, set()).add(live_node_id)

    # ------------------------------------------------------------------
    # 拉模式读取
    # ------------------------------------------------------------------

    def read(self, node: LiveNode) -> Any:
        """拉模式读取节点值

        - source 节点直接返回 result
        - live 节点检查 deps version → Dirty 则深度优先重算 → 执行 func → 哈希比较
        """
        with self._op_lock:
            # 动态依赖追踪：记录本次读取
            if self._computing_stack:
                self._record_read(self._computing_stack[-1], node)

            # source 节点直接返回
            if node.is_source:
                return node.result

            # 判断是否需要重算
            needs_recompute = (node.state == "Dirty")
            if not needs_recompute:
                needs_recompute = self._check_deps_dirty(node)

            if needs_recompute:
                return self.recompute(node)
            else:
                self._cache_hits += 1
                return node.result

    def _check_deps_dirty(self, node: LiveNode) -> bool:
        """检查节点的依赖是否有变化（version 不匹配或依赖为 Dirty）"""
        for dep_id, dep_version in node.deps:
            dep = self.nodes.get(dep_id)
            if dep is None:
                continue
            if dep.is_source:
                if dep.version != dep_version:
                    return True
            else:
                if dep.state == "Dirty":
                    return True
        return False

    # ------------------------------------------------------------------
    # dependents 弱引用工具
    # ------------------------------------------------------------------

    def _live_dependent_ids(self, node: LiveNode) -> List[int]:
        """返回 node 的存活下游节点 id 列表，并惰性清理失效弱引用。"""
        live_ids: List[int] = []
        for dep_id, ref in list(node.dependents.items()):
            if ref() is None:
                del node.dependents[dep_id]
            else:
                live_ids.append(dep_id)
        return live_ids

    def cleanup_dead_refs(self, node: LiveNode) -> int:
        """遍历 node.dependents，删除所有失效弱引用，返回清理数量。"""
        cleaned = 0
        for dep_id, ref in list(node.dependents.items()):
            if ref() is None:
                del node.dependents[dep_id]
                cleaned += 1
        return cleaned

    # ------------------------------------------------------------------
    # 回调重入检测
    # ------------------------------------------------------------------

    def _check_dispatch_loop(self, source_node: SourceNode,
                             dep_ids) -> None:
        """检查写入 source 后，被标记的下游节点是否有正在分发回调的节点。

        若存在，说明某订阅回调修改了它所依赖的 source，会导致无限循环。
        正在计算栈上的节点（首次/自身重算）豁免：其回调在计算过程中写回
        依赖属于引导期，不构成无限循环。
        """
        for dep_id in dep_ids:
            # 正在计算栈上的节点豁免：首次/自身重算时其回调写回依赖属引导期，
            # 不构成无限循环；其余情况说明回调在一次已完成的分发中又写回了
            # 它所依赖的 source，会导致无限循环。
            if dep_id in self._dispatching and dep_id not in self._computing_stack:
                raise IncrementalError(
                    f"检测到订阅回调循环依赖：节点 {dep_id} 的回调修改了 "
                    f"source {source_node.id}，该 source 的下游包含节点 "
                    f"{dep_id}，会导致无限循环。"
                )

    # ------------------------------------------------------------------
    # 写入与事务
    # ------------------------------------------------------------------

    def write(self, source_node: SourceNode, value: Any) -> None:
        """整体写入源节点

        替换整个 result，version += 1，直接下游标记 Dirty（不递归传播）。
        整体赋值会使所有 tracked_fields 路径对应的 live 节点失效。
        事务中只更新值不标记，结束时统一标记。
        """
        with self._op_lock:
            source_node.result = value
            source_node.hash = self.hash_value(value)
            if self._transact_depth > 0:
                # 事务中：只记录，不传播
                self._transaction_dirty_sources.add(source_node.id)
                return

            source_node.version += 1
            # 存活的整体下游
            live_ids = self._live_dependent_ids(source_node)
            # 整体赋值：tracked_fields 中所有字段路径对应的节点也失效
            for ids in source_node.tracked_fields.values():
                for nid in ids:
                    if nid not in live_ids:
                        live_ids.append(nid)

            self._check_dispatch_loop(source_node, live_ids)
            for dep_id in live_ids:
                self.mark_dirty(dep_id)

    def write_field(self, source_node: SourceNode, field_path: str,
                    value: Any) -> None:
        """字段级写入源节点：只修改 source.result 中对应字段，
        只标记 tracked_fields[field_path] 中的 live 节点为 Dirty。"""
        with self._op_lock:
            result = source_node.result
            if isinstance(result, dict):
                result[field_path] = value
            source_node.hash = self.hash_value(source_node.result)

            # 只标记依赖该字段的 live 节点
            targets: Set[int] = set()
            ids = source_node.tracked_fields.get(field_path)
            if ids:
                targets.update(ids)

            self._check_dispatch_loop(source_node, targets)
            for dep_id in targets:
                self.mark_dirty(dep_id)

            # 版本递增以反映 source 被修改
            source_node.version += 1

    def transact_begin(self) -> None:
        """开始事务"""
        with self._op_lock:
            self._transact_depth += 1
            if self._transact_depth == 1:
                self._transaction_dirty_sources.clear()

    def transact_end(self) -> None:
        """结束事务：统一标记所有在事务中被修改 source 的下游为 Dirty"""
        with self._op_lock:
            self._transact_depth -= 1
            if self._transact_depth == 0:
                for src_id in self._transaction_dirty_sources:
                    src = self.nodes.get(src_id)
                    if src is not None:
                        src.version += 1
                        live_ids = self._live_dependent_ids(src)
                        self._check_dispatch_loop(src, live_ids)
                        for dep_id in live_ids:
                            self.mark_dirty(dep_id)
                self._transaction_dirty_sources.clear()

    def mark_dirty(self, node_id: int) -> None:
        """标记节点为 Dirty（不递归传播）"""
        node = self.nodes.get(node_id)
        if node is not None and node.state == "Clean":
            node.state = "Dirty"

    # ------------------------------------------------------------------
    # 增量重算
    # ------------------------------------------------------------------

    def recompute(self, node: LiveNode) -> Any:
        """深度优先重算节点

        1. 递归重算所有 Dirty 依赖
        2. 执行 func
        3. 更新依赖列表（从实际读取收集）
        4. 哈希比较：相等则短路不通知下游；变化则通知 subscribers
        """
        if node.state == "Computing":
            raise IncrementalError(
                f"检测到循环依赖：节点 {node.id} 正在计算中"
            )

        old_value = node.result
        old_hash = node.hash

        node.state = "Computing"
        node.recompute_count += 1
        start = time.perf_counter()

        self._computing_stack.append(node.id)
        self._reads_stack.append({})

        try:
            # 1. 递归重算所有 Dirty 依赖
            for dep_id, dep_version in list(node.deps):
                dep = self.nodes.get(dep_id)
                if dep is None:
                    continue
                if dep.is_source:
                    # source 版本不匹配会在 func 读取时自然触发，无需在此处理
                    continue
                # 检查 live 依赖是否需要重算
                dep_needs = (dep.state == "Dirty")
                if not dep_needs:
                    dep_needs = self._check_deps_dirty(dep)
                if dep_needs:
                    self.recompute(dep)

            # 2. 执行计算函数
            new_value = node.func()

            # 3. 更新依赖列表（从实际读取中收集）
            node.deps = list(self._reads_stack[-1].items())

            # 4. 计算新哈希
            new_hash = self.hash_value(new_value)

            elapsed = time.perf_counter() - start
            node.total_time += elapsed

            # 5. 哈希比较
            if new_hash == old_hash:
                # 碰撞检测：深比较
                if self._deep_equal(old_value, new_value):
                    # 真短路：结果未变，不通知下游
                    node.result = new_value
                else:
                    # 哈希碰撞，视为变化
                    node.result = new_value
                    node.hash = new_hash
                    self._notify_subscribers(node, new_value, old_value)
            else:
                node.result = new_value
                node.hash = new_hash
                self._notify_subscribers(node, new_value, old_value)

            node.state = "Clean"

        except Exception:
            node.state = "Dirty"
            raise
        finally:
            self._reads_stack.pop()
            self._computing_stack.pop()

        self._total_recomputes += 1
        return node.result

    def _notify_subscribers(self, node: LiveNode,
                            new_value: Any, old_value: Any) -> None:
        """通知所有订阅者

        分发前将 node.id 加入 _dispatching，分发结束后在 finally 中移除，
        用于检测回调重入（回调中修改依赖的 source）。
        """
        if not node.subscribers:
            return
        self._dispatching.add(node.id)
        try:
            for cb in node.subscribers:
                cb(new_value, old_value)
        finally:
            # 若回调链中节点仍在计算栈上（自身重算中），说明分发是在其计算
            # 过程中发生的引导通知，保留 dispatching 标记以便后续对依赖 source
            # 的写入检出重入；否则分发已完全结束，正常移除。
            if node.id not in self._computing_stack:
                self._dispatching.discard(node.id)

    def _record_read(self, reader_id: int, node: LiveNode) -> None:
        """记录 reader 节点读取了 node（动态依赖追踪）"""
        if not self._reads_stack:
            return
        ver = node.version if node.is_source else 0
        self._reads_stack[-1][node.id] = ver
        # 确保反向边存在（处理动态新增依赖），以弱引用持有 reader
        if reader_id not in node.dependents:
            reader = self.nodes.get(reader_id)
            if reader is not None:
                node.dependents[reader_id] = weakref.ref(reader)

    @staticmethod
    def _deep_equal(a: Any, b: Any) -> bool:
        """深比较（用于哈希碰撞检测）"""
        try:
            return a == b
        except Exception:
            return a is b

    # ------------------------------------------------------------------
    # 结构化哈希
    # ------------------------------------------------------------------

    def hash_value(self, value: Any) -> int:
        """64位结构化哈希

        - int/float/str/bool/None/tuple/list/dict 递归哈希
        - 大对象（序列化后 >1KB）自动降级为 id() 引用追踪
        """
        h = hashlib.blake2b(digest_size=8)
        size_tracker = [0]

        def _hash(obj: Any) -> None:
            # 超过 1KB 降级为引用追踪
            if size_tracker[0] > 1024:
                h.update(b'REF')
                h.update(str(id(obj)).encode('utf-8'))
                return

            if obj is None:
                h.update(b'N')
            elif isinstance(obj, bool):
                h.update(b'B')
                h.update(b'1' if obj else b'0')
            elif isinstance(obj, int):
                s = str(obj).encode('utf-8')
                size_tracker[0] += len(s)
                h.update(b'I')
                h.update(s)
            elif isinstance(obj, float):
                s = repr(obj).encode('utf-8')
                size_tracker[0] += len(s)
                h.update(b'F')
                h.update(s)
            elif isinstance(obj, str):
                encoded = obj.encode('utf-8')
                size_tracker[0] += len(encoded)
                h.update(b'S')
                h.update(str(len(encoded)).encode('utf-8'))
                h.update(b':')
                h.update(encoded)
            elif isinstance(obj, bytes):
                size_tracker[0] += len(obj)
                h.update(b'Y')
                h.update(str(len(obj)).encode('utf-8'))
                h.update(b':')
                h.update(obj)
            elif isinstance(obj, tuple):
                h.update(b'T')
                h.update(str(len(obj)).encode('utf-8'))
                for item in obj:
                    _hash(item)
            elif isinstance(obj, list):
                h.update(b'L')
                h.update(str(len(obj)).encode('utf-8'))
                for item in obj:
                    _hash(item)
            elif isinstance(obj, dict):
                h.update(b'D')
                h.update(str(len(obj)).encode('utf-8'))
                for k in sorted(obj.keys(), key=str):
                    _hash(k)
                    _hash(obj[k])
            else:
                # 未知类型：引用追踪
                h.update(b'O')
                h.update(str(id(obj)).encode('utf-8'))

        _hash(value)
        return int.from_bytes(h.digest(), 'little')

    # ------------------------------------------------------------------
    # 活计算结果缓存（内存级，键含函数内容哈希）
    # ------------------------------------------------------------------

    def compute_with_cache(self, func_identity: Any, args_hash: Any,
                           compute_fn: Callable) -> Any:
        """按 (func_identity, args_hash) 缓存活计算结果。

        - 命中：cache_hits += 1，返回缓存值
        - 未命中：执行 compute_fn()，存入缓存并返回
        func_identity 由调用方（解释器）提供，应包含函数 AST 内容哈希。
        """
        key = (func_identity, args_hash)
        if key in self._result_cache:
            self._cache_hits += 1
            return self._result_cache[key]
        value = compute_fn()
        self._result_cache[key] = value
        return value

    def hash_function_body(self, body_ast: Any) -> str:
        """计算函数体内容哈希：递归遍历 AST 节点的类型与字段值。

        函数体变更 → 哈希变化 → 旧缓存自动失效。
        """
        h = hashlib.blake2b(digest_size=16)

        def _walk(node: Any) -> None:
            if node is None:
                h.update(b'N')
                return
            if isinstance(node, bool):
                h.update(b'B' + (b'1' if node else b'0'))
                return
            if isinstance(node, (int, float)):
                h.update(('N' + repr(node)).encode('utf-8'))
                return
            if isinstance(node, str):
                h.update(b'S' + node.encode('utf-8'))
                return
            if isinstance(node, bytes):
                h.update(b'Y' + node)
                return
            if isinstance(node, list):
                h.update(b'L' + str(len(node)).encode('utf-8'))
                for item in node:
                    _walk(item)
                return
            if isinstance(node, tuple):
                h.update(b'T' + str(len(node)).encode('utf-8'))
                for item in node:
                    _walk(item)
                return
            # 其他对象：按类型名 + 实例字段递归
            h.update(b'C' + type(node).__name__.encode('utf-8'))
            try:
                fields = vars(node)
            except TypeError:
                fields = {}
            for fname in sorted(fields.keys()):
                h.update(b'F' + fname.encode('utf-8'))
                _walk(fields[fname])

        _walk(body_ast)
        return h.hexdigest()

    # ------------------------------------------------------------------
    # 图导出
    # ------------------------------------------------------------------

    def export_graph(self, fmt: str = "mermaid") -> str:
        """导出依赖图，支持 "mermaid" 和 "dot" 两种格式（跳过失效弱引用）"""
        if fmt == "mermaid":
            lines = ["graph TD"]
            for nid in sorted(self.nodes.keys()):
                node = self.nodes[nid]
                label = f"Source {nid}" if node.is_source else f"Live {nid}"
                lines.append(f'    {nid}["{label}"]')
            for nid in sorted(self.nodes.keys()):
                node = self.nodes[nid]
                for dep_id, _ in node.deps:
                    lines.append(f"    {dep_id} --> {nid}")
            return "\n".join(lines)

        elif fmt == "dot":
            lines = ["digraph Aurora {"]
            for nid in sorted(self.nodes.keys()):
                node = self.nodes[nid]
                shape = "ellipse" if node.is_source else "box"
                label = f"Source {nid}" if node.is_source else f"Live {nid}"
                lines.append(f'    {nid} [label="{label}", shape={shape}];')
            for nid in sorted(self.nodes.keys()):
                node = self.nodes[nid]
                for dep_id, _ in node.deps:
                    lines.append(f"    {dep_id} -> {nid};")
            lines.append("}")
            return "\n".join(lines)

        else:
            raise IncrementalError(f"不支持的导出格式: {fmt}")

    # ------------------------------------------------------------------
    # 订阅
    # ------------------------------------------------------------------

    def subscribe(self, node: LiveNode, callback: Callable) -> None:
        """注册回调，node 结果变化时调用 callback(new_value, old_value)"""
        node.subscribers.append(callback)

    # ------------------------------------------------------------------
    # 统计
    # ------------------------------------------------------------------

    def get_stats(self) -> dict:
        """返回引擎统计信息"""
        total_time = sum(n.total_time for n in self.nodes.values())
        live_dependents = sum(
            len(self._live_dependent_ids(n)) for n in self.nodes.values()
        )
        return {
            "total_nodes": len(self.nodes),
            "source_count": sum(
                1 for n in self.nodes.values() if n.is_source
            ),
            "live_count": sum(
                1 for n in self.nodes.values() if not n.is_source
            ),
            "recomputes": self._total_recomputes,
            "cache_hits": self._cache_hits,
            "total_time": total_time,
            "live_dependents": live_dependents,
            "result_cache_size": len(self._result_cache),
        }
