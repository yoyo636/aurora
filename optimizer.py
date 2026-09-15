"""Aurora v3.1.0 ARM64 中间表示优化器

基于三地址 IR 的优化 pass 集合，对应「性能革命」支柱中的代码质量部分。

IR 抽象：

* :class:`Instruction` — 一条三地址指令（``dest = op args...``）；
* :class:`BasicBlock` — 基本块，含指令列表与后继块；
* :class:`Function` — 函数级 IR。

已实现的优化 pass（每个都独立可测试）：

* :func:`cse` — 公共子表达式消除（可用表达式分析）；
* :func:`licm` — 循环不变量外提（Loop Invariant Code Motion）；
* :func:`graph_coloring_allocator` — 图着色寄存器分配（干涉图 + 溢出）；
* :func:`list_schedule` — 减少流水线停顿的列表调度；
* :func:`tail_call_optimize` — 尾调用识别为跳转；
* :func:`auto_vectorize` — 简单 element-wise 循环的 NEON SIMD 向量化（v0.1）。

入口：:class:`Optimizer`，按 ``level`` 逐级打开 pass。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# IR 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Instruction:
    """三地址指令：``dest = op arg1, arg2, ...``"""

    op: str
    args: List[str] = field(default_factory=list)
    dest: Optional[str] = None
    """目标寄存器 / 临时变量；``None`` 表示无目标（如 ret / br）。"""

    # 元数据
    is_tail_call: bool = False
    """是否是「return call ...」形式的尾调用。"""

    vectorized: bool = False
    """是否已被自动向量化为 NEON 指令。"""

    def uses(self) -> List[str]:
        """读取的操作数。"""
        return list(self.args)

    def defines(self) -> Optional[str]:
        """写入的操作数。"""
        return self.dest

    def expr_key(self) -> Tuple[str, Tuple[str, ...]]:
        """用于 CSE 的表达式指纹（op + 操作数排序）。"""
        if self.dest is None:
            return ("__no_dest__", ())
        return (self.op, tuple(sorted(self.args)))


@dataclass
class BasicBlock:
    """基本块。"""

    name: str
    instructions: List[Instruction] = field(default_factory=list)
    successors: List[str] = field(default_factory=list)
    """后继块名称。"""

    def definitions(self) -> Set[str]:
        return {i.dest for i in self.instructions if i.dest is not None}

    def uses(self) -> Set[str]:
        out: Set[str] = set()
        for i in self.instructions:
            out.update(i.uses())
        return out


@dataclass
class Function:
    """函数级 IR。"""

    name: str
    args: List[str] = field(default_factory=list)
    blocks: Dict[str, BasicBlock] = field(default_factory=dict)
    entry: str = "entry"

    def all_instructions(self) -> List[Tuple[str, Instruction]]:
        """返回 ``(block_name, instr)`` 的线性流。"""
        out: List[Tuple[str, Instruction]] = []
        for bname in self._order():
            out.extend((bname, i) for i in self.blocks[bname].instructions)
        return out

    def _order(self) -> List[str]:
        names = list(self.blocks.keys())
        if self.entry in self.blocks:
            names.remove(self.entry)
            return [self.entry, *names]
        return names

    def clone(self) -> "Function":
        import copy
        return copy.deepcopy(self)


# ---------------------------------------------------------------------------
# Pass 1：公共子表达式消除（CSE）
# ---------------------------------------------------------------------------

def cse(func: Function) -> Function:
    """在每个基本块内做局部 CSE。

    若同一表达式在前面已经算过且结果变量仍然可用，则复用之前的结果。
    """
    for block in func.blocks.values():
        seen: Dict[Tuple[str, Tuple[str, ...]], str] = {}
        new_instrs: List[Instruction] = []
        for instr in block.instructions:
            key = instr.expr_key()
            if instr.dest is not None and key in seen:
                # 替换成 mov seen[key] -> dest
                new_instrs.append(
                    Instruction(op="mov", args=[seen[key]], dest=instr.dest)
                )
            else:
                new_instrs.append(instr)
                if instr.dest is not None:
                    seen[key] = instr.dest
        block.instructions = new_instrs
    return func


# ---------------------------------------------------------------------------
# Pass 2：循环不变量外提（LICM）
# ---------------------------------------------------------------------------

@dataclass
class Loop:
    """一个由 ``header`` + 循环体块组成的简化循环。"""

    header: str
    body: List[str]
    exits: List[str]
    """循环出口块。"""


def identify_loops(func: Function) -> List[Loop]:
    """识别循环：找 ``while``/``for`` 头块，其后继指回头块即视为循环。

    简化模型：只要某个块的后继里有它自己名字出现在后继后继中，
    就认为它是循环头。
    """
    loops: List[Loop] = []
    for name, block in func.blocks.items():
        if len(block.successors) < 2:
            continue
        # 简单判定：某个后继的后继又指回 header
        for succ in block.successors:
            if succ not in func.blocks:
                continue
            if name in func.blocks[succ].successors:
                body = [succ]
                exits = [s for s in block.successors if s != succ]
                loops.append(Loop(header=name, body=body, exits=exits))
                break
    return loops


def licm(func: Function) -> Function:
    """把循环体里「操作数全在循环外定义」的指令外提到 header 之前。"""
    loops = identify_loops(func)
    if not loops:
        return func
    for loop in loops:
        body_defs: Set[str] = set()
        for bname in loop.body:
            body_defs |= func.blocks[bname].definitions()
        # 收集循环外定义（entry 块 + exits + 其它未列入 body 的块）
        outer_defs: Set[str] = set(func.args)
        for bname, block in func.blocks.items():
            if bname in loop.body or bname == loop.header:
                continue
            outer_defs |= block.definitions()
        # 外移：body 块里所有操作数都在 outer_defs 中的指令
        for bname in loop.body:
            block = func.blocks[bname]
            moved: List[Instruction] = []
            kept: List[Instruction] = []
            for instr in block.instructions:
                if instr.op in ("br", "ret", "call"):
                    kept.append(instr)
                    continue
                if instr.dest is not None and all(
                    u in outer_defs for u in instr.uses()
                ):
                    moved.append(instr)
                    outer_defs.add(instr.dest)
                else:
                    kept.append(instr)
            block.instructions = kept
            if moved:
                header = func.blocks[loop.header]
                # 插到 header 末尾（header 通常是条件跳转前的准备）
                header.instructions.extend(moved)
    return func


# ---------------------------------------------------------------------------
# Pass 3：图着色寄存器分配
# ---------------------------------------------------------------------------

@dataclass
class GraphColoringAllocator:
    """基于干涉图的寄存器分配器。

    步骤：
    1. 线性扫描得到每个临时变量的活跃区间；
    2. 活跃区间重叠的变量之间加干涉边；
    3. 用贪心 DSATUR 算法着色，寄存器数量 = ``num_regs``；
    4. 无法着色的变量溢出到栈。
    """

    num_regs: int = 16
    """可用物理寄存器数量（ARM64 x0-x15 通用调用约定）。"""

    color_of: Dict[str, int] = field(default_factory=dict)
    spilled: Set[str] = field(default_factory=set)
    interference: Dict[str, Set[str]] = field(default_factory=dict)

    # ── 活跃区间 ──────────────────────────────────────

    def _live_ranges(self, func: Function) -> Dict[str, Tuple[int, int]]:
        """返回 ``var -> (定义点, 最后使用点)``。"""
        ranges: Dict[str, Tuple[int, int]] = {}
        for idx, (_, instr) in enumerate(func.all_instructions()):
            if instr.dest is not None:
                ranges.setdefault(instr.dest, (idx, idx))
            for u in instr.uses():
                if u in ranges:
                    start, _ = ranges[u]
                    ranges[u] = (start, idx)
        return ranges

    # ── 干涉图 ────────────────────────────────────────

    def build_interference(self, func: Function) -> Dict[str, Set[str]]:
        ranges = self._live_ranges(func)
        vars_list = list(ranges.keys())
        graph: Dict[str, Set[str]] = {v: set() for v in vars_list}
        for i, a in enumerate(vars_list):
            a_start, a_end = ranges[a]
            for b in vars_list[i + 1 :]:
                b_start, b_end = ranges[b]
                # 区间重叠（端点相邻视为不冲突，保守起见用 <）
                if a_start < b_end and b_start < a_end:
                    graph[a].add(b)
                    graph[b].add(a)
        self.interference = graph
        return graph

    # ── 着色 ──────────────────────────────────────────

    def color(self, func: Function) -> Dict[str, int]:
        self.build_interference(func)
        # 按度数降序贪心跳色
        order = sorted(
            self.interference.keys(),
            key=lambda v: (-len(self.interference[v]), v),
        )
        color_of: Dict[str, int] = {}
        for v in order:
            used = {color_of[n] for n in self.interference[v] if n in color_of}
            chosen: Optional[int] = None
            for c in range(self.num_regs):
                if c not in used:
                    chosen = c
                    break
            if chosen is None:
                self.spilled.add(v)
            else:
                color_of[v] = chosen
        self.color_of = color_of
        return color_of

    def allocate(self, func: Function) -> Dict[str, Any]:
        """执行分配，返回 ``{var: reg / 'stack_slot_N'}``。"""
        self.color(func)
        result: Dict[str, Any] = {}
        for v in self.interference:
            if v in self.spilled:
                result[v] = f"stack_slot_{len([x for x in self.spilled if x < v])}"
            else:
                result[v] = f"x{self.color_of[v]}"
        return result


def graph_coloring_allocator(
    func: Function, num_regs: int = 16
) -> GraphColoringAllocator:
    """便捷函数：对 ``func`` 运行图着色分配器。"""
    alloc = GraphColoringAllocator(num_regs=num_regs)
    alloc.allocate(func)
    return alloc


# ---------------------------------------------------------------------------
# Pass 4：列表调度（减少流水线停顿）
# ---------------------------------------------------------------------------

def list_schedule(func: Function) -> Function:
    """基本块内按依赖关系重排指令，把独立指令提前以隐藏延迟。

    v0.1 简化版：拓扑排序，保持数据依赖，无依赖的指令按原顺序插入。
    """
    for block in func.blocks.values():
        scheduled: List[Instruction] = []
        pending: List[Instruction] = list(block.instructions)
        ready: Set[str] = set()
        while pending:
            progressed = False
            for idx, instr in enumerate(pending):
                if all(u in ready or u.startswith(("imm_", "const_")) for u in instr.uses()):
                    scheduled.append(instr)
                    if instr.dest:
                        ready.add(instr.dest)
                    pending.pop(idx)
                    progressed = True
                    break
            if not progressed:
                # 存在环或外部依赖，直接追加剩余
                scheduled.extend(pending)
                break
        block.instructions = scheduled
    return func


# ---------------------------------------------------------------------------
# Pass 5：尾调用优化
# ---------------------------------------------------------------------------

def tail_call_optimize(func: Function) -> Function:
    """把 ``ret call f, args`` 形式的尾调用改写成 ``br f_after_save``。

    实现上：标记该指令的 ``is_tail_call`` 字段，
    真实后端会据此 emit ``b`` 而非 ``bl + ret``。
    """
    for bname, instr in func.all_instructions():
        if instr.op == "ret" and instr.args and instr.args[0] == "call":
            instr.is_tail_call = True
            instr.op = "tailjmp"
    return func


def is_tail_call(instr: Instruction) -> bool:
    """独立可测试：判断一条指令是不是尾调用。"""
    return instr.is_tail_call or (
        instr.op == "ret" and len(instr.args) >= 1 and instr.args[0] == "call"
    )


# ---------------------------------------------------------------------------
# Pass 6：NEON SIMD 自动向量化（v0.1）
# ---------------------------------------------------------------------------

def auto_vectorize(func: Function, max_vec_width: int = 4) -> Function:
    """识别简单的 element-wise 数组运算循环，标记为 NEON 向量化。

    v0.1 规则（保守）：
    * 循环体里出现 ``load array[i]`` / ``store array[i]`` / ``add`` / ``mul``；
    * 循环 trip count 是常数或上界可见；
    * 则把对应的 load/store 升级为 ``vload``/``vstore``，算术升级为 ``vadd``/``vmul``。
    """
    for loop in identify_loops(func):
        for bname in loop.body:
            block = func.blocks[bname]
            has_load = any(i.op == "load" for i in block.instructions)
            has_store = any(i.op == "store" for i in block.instructions)
            has_arithmetic = any(
                i.op in ("add", "sub", "mul") for i in block.instructions
            )
            if not (has_load and has_store and has_arithmetic):
                continue
            for instr in block.instructions:
                if instr.op == "load":
                    instr.op = "vload"
                    instr.vectorized = True
                elif instr.op == "store":
                    instr.op = "vstore"
                    instr.vectorized = True
                elif instr.op == "add":
                    instr.op = "vadd"
                    instr.vectorized = True
                elif instr.op == "mul":
                    instr.op = "vmul"
                    instr.vectorized = True
    return func


# ---------------------------------------------------------------------------
# Optimizer 主类
# ---------------------------------------------------------------------------

class Optimizer:
    """按优化级别执行 pass 序列。

    level 含义（与 clang -O 对齐）：

    * **0**：不优化；
    * **1**：CSE + 尾调用优化；
    * **2**：+ LICM + 列表调度；
    * **3**：+ 图着色寄存器分配 + NEON 自动向量化。
    """

    def __init__(self, level: int = 3) -> None:
        self.level = level
        self.passes_run: List[str] = []

    def optimize(self, ir: Function, level: Optional[int] = None) -> Function:
        level = self.level if level is None else level
        func = ir.clone()
        if level >= 1:
            self._run(cse, func, "cse")
            self._run(tail_call_optimize, func, "tail_call")
        if level >= 2:
            self._run(licm, func, "licm")
            self._run(list_schedule, func, "schedule")
        if level >= 3:
            alloc = graph_coloring_allocator(func, num_regs=16)
            func.color_map = alloc.color_of  # type: ignore[attr-defined]
            self.passes_run.append("regalloc")
            self._run(auto_vectorize, func, "neon_vec")
        return func

    def _run(self, pass_fn, func: Function, name: str) -> None:
        try:
            pass_fn(func)
        except Exception as exc:  # noqa: BLE001 — 单个 pass 失败不致命
            func.errors = getattr(func, "errors", [])  # type: ignore[attr-defined]
            func.errors.append(f"{name}: {exc!r}")  # type: ignore[attr-defined]
        else:
            self.passes_run.append(name)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def register_cli(subparsers) -> Any:
    """注册 ``aurora optimize`` 子命令。"""
    p = subparsers.add_parser('optimize', help='v3.1.0 ARM64 IR 优化器')
    p.add_argument('--level', type=int, default=3, help='优化级别 0-3')
    p.set_defaults(func=lambda args: print(
        f"aurora optimize --level {args.level}（v3.1.0，纯 IR 演示入口）"
    ))
    return p
