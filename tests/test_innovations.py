"""Aurora 三大创新特性测试：
1. @perf 自适应性能注解
2. Result 类型与异常的无缝互操作
3. 函数级增量编译缓存
"""

import os
import shutil
import unittest

from aurora.lexer import Lexer
from aurora.parser import Parser
from aurora.interpreter import Interpreter, AuroraError
from aurora.incremental_cache import IncrementalCompilerCache, CompiledFunction

from tests.helpers import compile_source, run_source


def _run(src):
    interp = Interpreter()
    interp.run(compile_source(src))
    return interp


# ============================================================
# 特性 1：@perf 自适应性能注解
# ============================================================

PERF_SRC_TEMPLATE = '''
@perf({level})
fn perf_fn(a: int) -> int {{
    return a * 2
}}
'''


class TestPerfAnnotation(unittest.TestCase):
    def _parse_fn(self, level):
        src = PERF_SRC_TEMPLATE.format(level=level)
        prog = compile_source(src)
        return prog.statements[0]

    def test_parse_all_levels(self):
        for level in ("critical", "hot", "cold", "size", "trace"):
            fn = self._parse_fn(level)
            self.assertEqual(fn.annotations, [{"level": level}], level)

    def test_get_perf_hints_critical(self):
        fn = self._parse_fn("critical")
        self.assertEqual(fn.get_perf_hints(),
                         {"inline": True, "unroll": 4,
                          "vectorize": True, "reg_pressure": "high"})

    def test_get_perf_hints_hot(self):
        fn = self._parse_fn("hot")
        self.assertEqual(fn.get_perf_hints(),
                         {"inline": True, "unroll": 2, "vectorize": False})

    def test_get_perf_hints_cold_and_size(self):
        for level in ("cold", "size"):
            fn = self._parse_fn(level)
            self.assertEqual(fn.get_perf_hints(),
                             {"inline": False, "unroll": 1,
                              "optimize_size": True}, level)

    def test_get_perf_hints_trace(self):
        fn = self._parse_fn("trace")
        self.assertEqual(fn.get_perf_hints(), {"trace": True})

    def test_no_annotation_returns_empty(self):
        fn = compile_source("fn plain(x: int) -> int { return x }").statements[0]
        self.assertEqual(fn.get_perf_hints(), {})

    def test_trace_records_call_stats(self):
        src = (
            "@perf(trace)\n"
            "fn add(a: int, b: int) -> int { return a + b }\n"
            "let r1 = add(1, 2)\n"
            "let r2 = add(3, 4)\n"
            "let r3 = add(5, 6)\n"
        )
        interp = _run(src)
        stats = interp._perf_trace.get("add")
        self.assertIsNotNone(stats)
        self.assertEqual(stats["calls"], 3)
        self.assertGreaterEqual(stats["total_time_ms"], 0.0)


# ============================================================
# 特性 2：Result 类型与异常的无缝互操作
# ============================================================

DIVIDE_SRC = '''
fn divide(a: int, b: int) -> Result[int, str] {
    if b == 0 {
        return Err("division by zero")
    }
    return Ok(a / b)
}
'''


class TestResultInterop(unittest.TestCase):
    def test_ok_creation(self):
        interp = _run('let r = Ok(42)')
        r = interp.global_env.get('r')
        self.assertTrue(r.is_ok())
        self.assertEqual(r._ok, 42)

    def test_err_creation(self):
        interp = _run('let r = Err("boom")')
        r = interp.global_env.get('r')
        self.assertTrue(r.is_err())
        self.assertEqual(r._err, "boom")

    def test_auto_unwrap_ok(self):
        interp = _run(DIVIDE_SRC + "let result = divide(10, 2)")
        self.assertEqual(interp.global_env.get('result'), 5.0)

    def test_err_auto_panics(self):
        with self.assertRaises(AuroraError) as ctx:
            _run(DIVIDE_SRC + "let bad = divide(10, 0)")
        self.assertIn("division by zero", str(ctx.exception))

    def test_try_catch_catches_err(self):
        src = (
            DIVIDE_SRC +
            'var msg = ""\n'
            'try {\n'
            '    let x = divide(10, 0)\n'
            '} catch e {\n'
            '    msg = e\n'
            '}\n'
        )
        interp = _run(src)
        self.assertIn("division by zero", interp.global_env.get('msg'))

    def test_question_operator_propagates(self):
        src = (
            DIVIDE_SRC +
            "fn compute() -> Result[int, str] {\n"
            "    let x = divide(10, 2)?\n"
            "    return Ok(x * 2)\n"
            "}\n"
            "let v = compute()\n"
        )
        interp = _run(src)
        self.assertEqual(interp.global_env.get('v'), 10.0)

    def test_question_operator_propagates_err(self):
        # divide(10,0)? 应把 Err 传出 compute()；compute 又自动解包 -> panic
        src = (
            DIVIDE_SRC +
            "fn compute() -> Result[int, str] {\n"
            "    let x = divide(10, 0)?\n"
            "    return Ok(x * 2)\n"
            "}\n"
            "let v = compute()\n"
        )
        with self.assertRaises(AuroraError) as ctx:
            _run(src)
        self.assertIn("division by zero", str(ctx.exception))

    def test_is_ok_is_err(self):
        # good 已被自动解包为值；用显式 Ok/Err 构造测试方法
        interp2 = _run('let o = Ok(1)\nlet e = Err("x")')
        o = interp2.global_env.get('o')
        e = interp2.global_env.get('e')
        self.assertTrue(o.is_ok())
        self.assertFalse(o.is_err())
        self.assertTrue(e.is_err())
        self.assertFalse(e.is_ok())

    def test_unwrap_or(self):
        interp = _run('let e = Err("x")\nlet v = e.unwrap_or(0)')
        self.assertEqual(interp.global_env.get('v'), 0)

    def test_unwrap_or_ok(self):
        interp = _run('let o = Ok(99)\nlet v = o.unwrap_or(0)')
        self.assertEqual(interp.global_env.get('v'), 99)


# ============================================================
# 特性 3：函数级增量编译缓存
# ============================================================

def _fn(name="foo", body="    return a + 1\n"):
    src = f"fn {name}(a: int) -> int {{\n{body}}}\n"
    return compile_source(src).statements[0]


class TestIncrementalCache(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.expanduser("~/.aurora/test_cache_innov")
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)
        self.cache = IncrementalCompilerCache(cache_dir=self.tmp)

    def tearDown(self):
        self.cache.clear()
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)

    def test_hash_stable_for_same_function(self):
        f1 = _fn("foo", "    return a + 1\n")
        f2 = _fn("foo", "    return a + 1\n")
        self.assertEqual(self.cache.function_hash(f1),
                         self.cache.function_hash(f2))

    def test_hash_differs_for_different_body(self):
        f1 = _fn("foo", "    return a + 1\n")
        f2 = _fn("foo", "    return a + 2\n")
        self.assertNotEqual(self.cache.function_hash(f1),
                            self.cache.function_hash(f2))

    def test_hash_differs_for_different_name(self):
        f1 = _fn("foo")
        f2 = _fn("bar")
        self.assertNotEqual(self.cache.function_hash(f1),
                            self.cache.function_hash(f2))

    def test_put_get_roundtrip(self):
        f = _fn("foo")
        self.assertIsNone(self.cache.get(f))
        self.cache.put(f, CompiledFunction(name="foo",
                                            func_hash=self.cache.function_hash(f),
                                            machine_code="X"))
        hit = self.cache.get(f)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.machine_code, "X")

    def test_invalidate_returns_none(self):
        f = _fn("foo")
        self.cache.put(f, CompiledFunction(
            name="foo", func_hash=self.cache.function_hash(f)))
        self.assertIsNotNone(self.cache.get(f))
        self.cache.invalidate("foo")
        self.assertIsNone(self.cache.get(f))

    def test_stats(self):
        f = _fn("foo")
        self.cache.put(f, CompiledFunction(
            name="foo", func_hash=self.cache.function_hash(f)))
        self.cache.get(f)  # hit
        stats = self.cache.stats()
        self.assertEqual(stats["entries"], 1)
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 0)
        self.assertAlmostEqual(stats["hit_rate"], 1.0)

    def test_persistence_to_disk(self):
        f = _fn("foo")
        self.cache.put(f, CompiledFunction(
            name="foo", func_hash=self.cache.function_hash(f),
            machine_code="PERSIST"))
        # 新实例从磁盘恢复
        cache2 = IncrementalCompilerCache(cache_dir=self.tmp)
        hit = cache2.get(f)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.machine_code, "PERSIST")

    def test_dependency_invalidation(self):
        # A 调用 B；B 失效后 A 也应被级联失效
        a_src = "fn caller() -> int { return callee() }\n"
        b_src = "fn callee() -> int { return 1 }\n"
        a = compile_source(a_src).statements[0]
        b = compile_source(b_src).statements[0]
        self.cache.put(a, CompiledFunction(name="caller",
                                           func_hash=self.cache.function_hash(a)))
        self.cache.put(b, CompiledFunction(name="callee",
                                           func_hash=self.cache.function_hash(b)))
        self.assertIsNotNone(self.cache.get(a))
        self.cache.invalidate("callee")
        self.assertIsNone(self.cache.get(a))  # 依赖被级联失效

    def test_clear(self):
        f = _fn("foo")
        self.cache.put(f, CompiledFunction(
            name="foo", func_hash=self.cache.function_hash(f)))
        self.cache.clear()
        self.assertEqual(self.cache.stats()["entries"], 0)


if __name__ == "__main__":
    unittest.main()
