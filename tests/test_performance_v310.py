"""Aurora v3.1.0 性能革命支柱测试

覆盖模块：
* :mod:`aurora.parallel_compiler`
* :mod:`aurora.persistent_cache`
* :mod:`aurora.optimizer`
* :mod:`aurora.memory_manager`
* :mod:`aurora.benchmark`

全部测试独立运行，不依赖显示环境。
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.parallel_compiler import (  # noqa: E402
    ParallelCompiler,
    build_dependency_graph,
    compile_files,
    topological_layers,
)
from aurora.persistent_cache import PersistentCache  # noqa: E402
from aurora.optimizer import (  # noqa: E402
    BasicBlock,
    Function,
    GraphColoringAllocator,
    Instruction,
    Optimizer,
    auto_vectorize,
    cse,
    graph_coloring_allocator,
    is_tail_call,
    licm,
    tail_call_optimize,
)
from aurora.memory_manager import (  # noqa: E402
    EscapeAnalyzer,
    HybridGC,
    ObjectPool,
    WriteBarrier,
)
from aurora.benchmark import (  # noqa: E402
    BUILTIN_SUITES,
    BenchmarkRunner,
    run_benchmark,
)


def _write(path: str, source: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(source)
    return path


# ---------------------------------------------------------------------------
# parallel_compiler
# ---------------------------------------------------------------------------

class TestParallelCompiler(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aurora_pc_")
        self.util = _write(os.path.join(self.tmp, "util.aur"), "fn helper() {}\n")
        self.main = _write(
            os.path.join(self.tmp, "main.aur"),
            "import util\nfn main() { helper() }\n",
        )
        self.lib = _write(
            os.path.join(self.tmp, "lib.aur"),
            "import util\nfn lib() {}\n",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dependency_graph_builds(self):
        graph, units = build_dependency_graph([self.main, self.lib, self.util], roots=[self.tmp])
        self.assertIn(os.path.abspath(self.util), graph[os.path.abspath(self.main)])
        self.assertIn(os.path.abspath(self.util), graph[os.path.abspath(self.lib)])
        # util 自己没有依赖
        self.assertEqual(graph[os.path.abspath(self.util)], [])

    def test_topological_layers(self):
        graph, _ = build_dependency_graph(
            [self.main, self.lib, self.util], roots=[self.tmp]
        )
        layers = topological_layers(graph)
        # util 必须在第一层
        self.assertIn(os.path.abspath(self.util), layers[0])

    def test_parallel_compile_runs(self):
        result = compile_files(
            [self.main, self.lib, self.util], workers=2
        )
        self.assertEqual(result.failed, [])
        self.assertGreaterEqual(result.compiled_count, 1)
        self.assertGreater(len(result.layers), 0)
        print(result.summary())

    def test_incremental_only_recompiles_changed(self):
        pc = ParallelCompiler(workers=2)
        r1 = pc.compile([self.main, self.util])
        self.assertEqual(r1.failed, [])
        # 改一下 util，main 应该被标记为受影响
        graph = build_dependency_graph([self.main, self.util], roots=[self.tmp])[0]
        affected = ParallelCompiler._downstream(graph, {os.path.abspath(self.util)})
        self.assertIn(os.path.abspath(self.main), affected)


# ---------------------------------------------------------------------------
# persistent_cache
# ---------------------------------------------------------------------------

class TestPersistentCache(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aurora_cache_")
        self.cache_dir = os.path.join(self.tmp, ".aurora_cache")
        self.src = _write(os.path.join(self.tmp, "a.aur"), "fn a() {}\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_save_load_roundtrip(self):
        c = PersistentCache(self.cache_dir)
        c.set(self.src, {"ast": "fake-ast", "type_info": "int"})
        hit = c.get(self.src)
        self.assertIsNotNone(hit)
        self.assertEqual(hit["ast"], "fake-ast")

    def test_cache_invalidation_cascades(self):
        c = PersistentCache(self.cache_dir)
        b = _write(os.path.join(self.tmp, "b.aur"), "import a\nfn b() {}\n")
        c.set(self.src, {"ast": "A"}, imports=[])
        c.set(b, {"ast": "B"}, imports=[self.src])
        # 让 mtime 新鲜一点
        self.assertIsNotNone(c.get(self.src))
        removed = c.invalidate(self.src)
        self.assertIn(os.path.abspath(self.src), removed)
        self.assertIn(os.path.abspath(b), removed)
        self.assertIsNone(c.get(b))

    def test_aurc_precompile(self):
        c = PersistentCache(self.cache_dir)
        path = c.save_aurc("std_string", {"module": "string", "v": 42})
        self.assertTrue(os.path.isfile(path))
        loaded = c.load_aurc("std_string")
        self.assertEqual(loaded["v"], 42)
        self.assertIsNone(c.load_aurc("nonexistent"))

    def test_clear(self):
        c = PersistentCache(self.cache_dir)
        c.set(self.src, {"x": 1})
        c.clear()
        self.assertEqual(len(c._entries), 0)
        self.assertIsNone(c.get(self.src))


# ---------------------------------------------------------------------------
# optimizer
# ---------------------------------------------------------------------------

def _make_func_with_loop() -> Function:
    """构造一个 LICM 可识别的循环：

    entry: x0 = const 10
    loop_header: br body | exit
    body:        x1 = add x0, x0   <- x0 在循环外，应外提
                 br loop_header
    exit:        ret
    """
    entry = BasicBlock(name="entry", instructions=[
        Instruction(op="const", args=["10"], dest="x0"),
    ])
    header = BasicBlock(name="loop_header", successors=["body", "exit"])
    body = BasicBlock(name="body", successors=["loop_header"], instructions=[
        Instruction(op="add", args=["x0", "x0"], dest="x1"),
    ])
    exit_ = BasicBlock(name="exit", instructions=[Instruction(op="ret", args=["x1"])])
    return Function(name="f", blocks={
        "entry": entry, "loop_header": header, "body": body, "exit": exit_
    })


class TestOptimizer(unittest.TestCase):
    def test_cse_eliminates_duplicate(self):
        block = BasicBlock(name="b", instructions=[
            Instruction(op="add", args=["a", "b"], dest="t1"),
            Instruction(op="add", args=["b", "a"], dest="t2"),  # 同表达式
            Instruction(op="add", args=["t1", "t2"], dest="out"),
        ])
        func = Function(name="f", blocks={"b": block})
        out = cse(func)
        ops = [i.op for i in out.blocks["b"].instructions]
        # 第二条应该被替换成 mov
        self.assertIn("mov", ops)

    def test_licm_moves_invariant(self):
        func = _make_func_with_loop()
        licm(func)
        header_ops = [i.op for i in func.blocks["loop_header"].instructions]
        # add x0,x0 应被外提到 header
        self.assertIn("add", header_ops)
        body_ops = [i.op for i in func.blocks["body"].instructions]
        self.assertNotIn("add", body_ops)

    def test_graph_coloring_allocates(self):
        block = BasicBlock(name="b", instructions=[
            Instruction(op="const", args=["1"], dest="a"),
            Instruction(op="const", args=["2"], dest="b"),
            Instruction(op="add", args=["a", "b"], dest="c"),
            Instruction(op="const", args=["3"], dest="d"),
        ])
        func = Function(name="f", blocks={"b": block})
        alloc = graph_coloring_allocator(func, num_regs=2)
        self.assertIsInstance(alloc.color_of, dict)
        self.assertGreater(len(alloc.color_of), 0)

    def test_tail_call_recognized(self):
        instr = Instruction(op="ret", args=["call", "foo", "x", "y"])
        self.assertTrue(is_tail_call(instr))
        func = Function(name="f", blocks={
            "b": BasicBlock(name="b", instructions=[instr])
        })
        out = tail_call_optimize(func)
        self.assertTrue(out.blocks["b"].instructions[0].is_tail_call)

    def test_auto_vectorize_flags_arrays(self):
        body = BasicBlock(name="body", instructions=[
            Instruction(op="load", args=["arr", "i"], dest="v1"),
            Instruction(op="add", args=["v1", "v1"], dest="v2"),
            Instruction(op="store", args=["arr", "i", "v2"]),
        ], successors=["loop_header"])
        header = BasicBlock(name="loop_header", successors=["body", "exit"])
        exit_ = BasicBlock(name="exit")
        func = Function(name="vec", blocks={
            "loop_header": header, "body": body, "exit": exit_
        })
        auto_vectorize(func)
        ops = [i.op for i in func.blocks["body"].instructions]
        self.assertIn("vload", ops)
        self.assertIn("vadd", ops)
        self.assertIn("vstore", ops)

    def test_optimizer_levels(self):
        opt = Optimizer(level=3)
        func = _make_func_with_loop()
        out = opt.optimize(func)
        self.assertGreater(len(opt.passes_run), 0)
        # level 3 应跑过 regalloc
        self.assertIn("regalloc", opt.passes_run)


# ---------------------------------------------------------------------------
# memory_manager
# ---------------------------------------------------------------------------

class TestMemoryManager(unittest.TestCase):
    def test_allocate_deallocate(self):
        gc = HybridGC()
        a = gc.allocate(64)
        b = gc.allocate(128)
        self.assertGreater(a, 0)
        self.assertGreater(b, 0)
        self.assertEqual(len(gc._objects), 2)
        gc.deallocate(a)
        self.assertEqual(len(gc._objects), 1)
        s = gc.stats()
        self.assertEqual(s["heap_objects"], 1)

    def test_generational_scavenge(self):
        gc = HybridGC()
        young = gc.allocate(64)
        old = gc.allocate(64)
        gc._objects[old].generation = 1
        gc.release_ref(young)  # 引用归零，应被 minor GC 回收
        report = gc.collect(minor=True)
        self.assertEqual(report["phase"], "minor")
        self.assertNotIn(young, gc._objects)

    def test_escape_analysis_stack_alloc(self):
        analyzer = EscapeAnalyzer()
        # 未知 oid 保守视为逃逸（堆分配）
        self.assertFalse(analyzer.should_stack_alloc(1))
        # 显式标记未逃逸 -> 栈分配
        analyzer.mark_stack_alloc(1)
        self.assertTrue(analyzer.should_stack_alloc(1))
        analyzer.mark_escape(2, EscapeAnalyzer.ESCAPES_RETURN)
        self.assertFalse(analyzer.should_stack_alloc(2))
        # 端到端：HybridGC 应把 on_stack=True 的对象放进栈统计
        gc = HybridGC()
        gc.analyzer = analyzer
        oid = gc.allocate(64, on_stack=True)
        self.assertNotIn(oid, gc._objects)
        self.assertEqual(gc.stats()["stack_allocs"], 1)

    def test_object_pool_reuse(self):
        pool = ObjectPool(slot_size=64, capacity=8)
        o1 = pool.acquire(1)
        pool.release(o1)
        o2 = pool.acquire(2)
        self.assertIs(o1, o2)
        self.assertEqual(pool.stats()["hits"], 1)

    def test_write_barrier_records_old_to_young(self):
        barrier = WriteBarrier()
        old = type("O", (), {"generation": 1, "oid": 1})()
        young = type("Y", (), {"generation": 0, "oid": 2})()
        barrier.on_reference_write(old, young)
        self.assertIn(1, barrier.remembered)


# ---------------------------------------------------------------------------
# benchmark
# ---------------------------------------------------------------------------

class TestBenchmark(unittest.TestCase):
    def test_run_builtin_benchmark(self):
        r = run_benchmark("loop_iteration", BUILTIN_SUITES["loop_iteration"], iterations=2)
        self.assertEqual(r.name, "loop_iteration")
        self.assertGreater(r.mean_ms, 0)
        self.assertEqual(r.iterations, 2)

    def test_runner_filter_and_history(self):
        with tempfile.TemporaryDirectory() as d:
            hist = os.path.join(d, "hist.json")
            runner = BenchmarkRunner(iterations=1, history_file=hist)
            results = runner.run(filter_name="loop_iteration")
            self.assertEqual(len(results), 1)
            path = runner.save_history(results)
            self.assertTrue(os.path.isfile(path))
            loaded = runner.load_history()
            self.assertIn("loop_iteration", loaded)

    def test_regression_detection(self):
        with tempfile.TemporaryDirectory() as d:
            hist = os.path.join(d, "hist.json")
            # 写一份"快"的历史
            with open(hist, "w") as f:
                json.dump({"results": {"loop_iteration": {"mean_ms": 0.001}}}, f)
            runner = BenchmarkRunner(iterations=1, history_file=hist, regression_threshold=0.1)
            results = runner.run(filter_name="loop_iteration")
            regs = runner.detect_regression(results)
            # 当前 loop_iteration 远慢于 0.001ms，应判回归
            self.assertGreaterEqual(len(regs), 1)

    def test_json_output_via_runner(self):
        runner = BenchmarkRunner(iterations=1)
        results = runner.run(filter_name="loop_iteration")
        payload = {"results": [r.to_dict() for r in results]}
        text = json.dumps(payload)
        self.assertIn("loop_iteration", text)


if __name__ == "__main__":
    unittest.main()
