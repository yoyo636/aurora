"""Aurora v3.1.0 高级内存管理

纯 Python 模拟层，用于展示运行时内存架构并供解释器集成：

* **混合 GC 模型** :class:`HybridGC` — 引用计数立即回收 + 分代 GC 处理循环引用；
* **分代**：年轻代用复制收集（scavenge），老年代用标记-清除；
* **逃逸分析** :class:`EscapeAnalyzer` — 未逃逸对象直接栈分配，零 GC 压力；
* **对象池** :class:`ObjectPool` — 高频小对象（Box / Closure / 小 vector）池化复用；
* **写屏障**：引用从老年代指向年轻代时记录到 remembered set，避免整堆扫描。

公共接口：``allocate(size)`` / ``deallocate(ptr)`` / ``collect()`` / ``stats()``。
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set


# ---------------------------------------------------------------------------
# 对象表示
# ---------------------------------------------------------------------------

@dataclass
class AuroraObject:
    """堆上对象的模拟描述。"""

    oid: int
    size: int
    refs: int = 0
    generation: int = 0
    """0=年轻代，1=老年代。"""

    escaped: bool = True
    """逃逸分析结论：未逃逸对象应栈分配，不进堆。"""

    stack_allocated: bool = False
    """是否实际分配在栈上（逃逸分析为否时置 True）。"""

    fields: Dict[str, int] = field(default_factory=dict)
    """字段 -> 另一个对象 oid 的引用。"""


# ---------------------------------------------------------------------------
# 对象池
# ---------------------------------------------------------------------------

class ObjectPool:
    """固定大小小对象的无锁池化分配器。

    ``acquire()`` 优先复用 freelist 上的对象；``release(obj)`` 归还。
    """

    def __init__(self, slot_size: int, capacity: int = 64) -> None:
        self.slot_size = slot_size
        self.capacity = capacity
        self._freelist: List[AuroraObject] = []
        self._total_borrowed = 0
        self._hits = 0
        self._misses = 0

    def acquire(self, oid: int) -> AuroraObject:
        if self._freelist:
            self._hits += 1
            obj = self._freelist.pop()
            obj.refs = 1
            obj.fields.clear()
            return obj
        self._misses += 1
        self._total_borrowed += 1
        return AuroraObject(oid=oid, size=self.slot_size, refs=1)

    def release(self, obj: AuroraObject) -> None:
        if len(self._freelist) < self.capacity:
            obj.refs = 0
            obj.fields.clear()
            self._freelist.append(obj)

    def stats(self) -> Dict[str, int]:
        return {
            "slot_size": self.slot_size,
            "free": len(self._freelist),
            "capacity": self.capacity,
            "hits": self._hits,
            "misses": self._misses,
            "borrowed": self._total_borrowed,
        }


# ---------------------------------------------------------------------------
# 逃逸分析
# ---------------------------------------------------------------------------

class EscapeAnalyzer:
    """简单的逃逸分析：根据对象的使用方式判断是否逃逸当前函数。

    判定规则（保守）：

    * 把对象作为返回值 → 逃逸；
    * 把对象存入堆字段 → 逃逸；
    * 把对象传给函数调用 → 视为逃逸（v0.1 不做跨过程分析）；
    * 只在局部算术 / 比较中使用 → 未逃逸，可栈分配。
    """

    ESCAPES_RETURN = "return"
    ESCAPES_HEAP = "heap_store"
    ESCAPES_CALL = "call_arg"

    def __init__(self) -> None:
        self._flags: Dict[int, Set[str]] = {}

    def mark_escape(self, oid: int, reason: str) -> None:
        self._flags.setdefault(oid, set()).add(reason)

    def mark_stack_alloc(self, oid: int) -> None:
        """显式标记该对象未逃逸，可栈分配。"""
        self._flags.setdefault(oid, set()).discard(self.ESCAPES_RETURN)

    def escapes(self, oid: int) -> bool:
        # 保守：未知对象默认视为逃逸（堆分配），只有显式标记才栈分配
        return bool(self._flags.get(oid, {self.ESCAPES_RETURN}))

    def should_stack_alloc(self, oid: int) -> bool:
        return not self.escapes(oid)


# ---------------------------------------------------------------------------
# 写屏障
# ---------------------------------------------------------------------------

class WriteBarrier:
    """分代写屏障：记录「老年代 → 年轻代」的指针写，供 minor GC 用。"""

    def __init__(self) -> None:
        self.remembered: Set[int] = set()
        self._writes = 0

    def on_reference_write(
        self, source: AuroraObject, target: AuroraObject
    ) -> None:
        """当 ``source.field = target`` 时调用。"""
        self._writes += 1
        if source.generation > target.generation:
            # 老年代指向年轻代：把 source 加入 remembered set
            self.remembered.add(source.oid)

    def stats(self) -> Dict[str, int]:
        return {"writes": self._writes, "remembered": len(self.remembered)}


# ---------------------------------------------------------------------------
# 混合 GC
# ---------------------------------------------------------------------------

class HybridGC:
    """引用计数 + 分代 GC 混合模型。

    * 引用计数负责立即回收无环的死对象；
    * 分代 GC 负责回收循环引用；
    * 年轻代 GC（``collect(minor=True)``）复制存活对象到老年代；
    * 老年代 GC（``collect(minor=False)``）标记-清除。
    """

    def __init__(self, young_threshold: int = 8, pool_capacity: int = 64) -> None:
        self._objects: Dict[int, AuroraObject] = {}
        self._next_oid = itertools.count(1)
        self.analyzer = EscapeAnalyzer()
        self.barrier = WriteBarrier()
        self.pools: Dict[int, ObjectPool] = {
            64: ObjectPool(64, pool_capacity),
            128: ObjectPool(128, pool_capacity),
        }
        self.young_threshold = young_threshold
        self._scavenges = 0
        self._major_collections = 0
        self._bytes_allocated = 0
        self._bytes_freed = 0
        self._stack_allocs = 0

    # ── 分配 ──────────────────────────────────────────

    def allocate(self, size: int, on_stack: bool = False) -> int:
        """分配一个 ``size`` 字节的对象，返回 oid。"""
        oid = next(self._next_oid)
        if on_stack or self.analyzer.should_stack_alloc(oid):
            obj = AuroraObject(
                oid=oid, size=size, refs=1, escaped=False, stack_allocated=True
            )
            self._stack_allocs += 1
            # 栈对象不进堆字典，不参与 GC
            return oid
        pool = self._pick_pool(size)
        obj = pool.acquire(oid) if pool else AuroraObject(oid=oid, size=size, refs=1)
        self._objects[oid] = obj
        self._bytes_allocated += size
        return oid

    def _pick_pool(self, size: int) -> Optional[ObjectPool]:
        for slot, pool in self.pools.items():
            if size <= slot:
                return pool
        return None

    # ── 引用计数 ───────────────────────────────────────

    def retain(self, oid: int) -> None:
        obj = self._objects.get(oid)
        if obj:
            obj.refs += 1

    def release_ref(self, oid: int) -> None:
        obj = self._objects.get(oid)
        if not obj:
            return
        obj.refs -= 1
        if obj.refs <= 0:
            self.deallocate(oid)

    def deallocate(self, oid: int) -> None:
        """立即释放对象（引用计数归零时调用）。"""
        obj = self._objects.pop(oid, None)
        if obj is None:
            return
        self._bytes_freed += obj.size
        pool = self._pick_pool(obj.size)
        if pool:
            pool.release(obj)

    # ── 分代 GC ────────────────────────────────────────

    def collect(self, minor: bool = True) -> Dict[str, int]:
        """触发 GC。``minor=True`` 做 young-gen 回收，否则做 full GC。"""
        if minor:
            return self._scavenge()
        return self._major_collection()

    def _scavenge(self) -> Dict[str, int]:
        """年轻代复制收集：把存活的年轻代对象晋升到老年代。"""
        self._scavenges += 1
        promoted = 0
        collected = 0
        for oid, obj in list(self._objects.items()):
            if obj.generation != 0:
                continue
            if obj.refs > 0 or self._is_reachable_from_old(oid):
                obj.generation = 1
                promoted += 1
            else:
                self.deallocate(oid)
                collected += 1
        return {"phase": "minor", "promoted": promoted, "collected": collected}

    def _major_collection(self) -> Dict[str, int]:
        """老年代标记-清除。"""
        self._major_collections += 1
        roots: Set[int] = set()
        for oid, obj in self._objects.items():
            if obj.refs > 0:
                roots.add(oid)
        # 从 roots 沿字段引用 BFS
        live: Set[int] = set()
        stack = list(roots)
        while stack:
            cur = stack.pop()
            if cur in live:
                continue
            live.add(cur)
            obj = self._objects.get(cur)
            if obj:
                stack.extend(v for v in obj.fields.values() if v in self._objects)
        collected = 0
        for oid in list(self._objects.keys()):
            if oid not in live:
                self.deallocate(oid)
                collected += 1
        return {"phase": "major", "live": len(live), "collected": collected}

    def _is_reachable_from_old(self, oid: int) -> bool:
        """检查 remembered set 里有没有老年代对象直接指向 oid。"""
        for src in self.barrier.remembered:
            obj = self._objects.get(src)
            if obj and oid in obj.fields.values():
                return True
        return False

    # ── 引用写入（写屏障入口）─────────────────────────

    def write_field(self, owner_oid: int, field_name: str, target_oid: int) -> None:
        owner = self._objects.get(owner_oid)
        target = self._objects.get(target_oid)
        if owner is None or target is None:
            return
        owner.fields[field_name] = target_oid
        self.barrier.on_reference_write(owner, target)

    # ── 统计 ──────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        young = sum(1 for o in self._objects.values() if o.generation == 0)
        old = len(self._objects) - young
        return {
            "heap_objects": len(self._objects),
            "young": young,
            "old": old,
            "stack_allocs": self._stack_allocs,
            "bytes_allocated": self._bytes_allocated,
            "bytes_freed": self._bytes_freed,
            "scavenges": self._scavenges,
            "major_collections": self._major_collections,
            "write_barrier": self.barrier.stats(),
            "pools": {str(k): p.stats() for k, p in self.pools.items()},
        }


# ---------------------------------------------------------------------------
# 顶层便捷接口（与 HybridGC 单例等价的薄封装）
# ---------------------------------------------------------------------------

_default_gc = HybridGC()


def allocate(size: int, on_stack: bool = False) -> int:
    return _default_gc.allocate(size, on_stack=on_stack)


def deallocate(ptr: int) -> None:
    _default_gc.deallocate(ptr)


def collect(minor: bool = True) -> Dict[str, int]:
    return _default_gc.collect(minor=minor)


def stats() -> Dict[str, Any]:
    return _default_gc.stats()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def register_cli(subparsers) -> Any:
    """注册 ``aurora mem`` 子命令。"""
    p = subparsers.add_parser('mem', help='v3.1.0 内存管理 / GC 统计')
    p.add_argument('--json', action='store_true', help='JSON 输出')
    p.set_defaults(func=lambda args: print(
        __import__("json").dumps(stats(), indent=2, ensure_ascii=False)
        if args.json else stats()
    ))
    return p
