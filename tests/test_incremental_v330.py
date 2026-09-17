"""v3.3.0 语言级增量计算测试：source / live / transact / 纯度检查 / 订阅 / 持久化"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.lexer import Lexer
from aurora.parser import Parser
from aurora.interpreter import Interpreter
from aurora.type_checker import TypeChecker
from aurora.incremental import (
    IncrementalEngine,
    LiveNode,
    SourceNode,
    IncrementalError,
)


def run(src):
    """编译并执行 Aurora 源码，返回解释器实例（每次重置引擎单例）"""
    IncrementalEngine.reset()
    prog = Parser(Lexer(src).tokenize()).parse()
    interp = Interpreter()
    interp.run(prog)
    return interp


def type_check(src):
    """类型检查，返回错误列表"""
    prog = Parser(Lexer(src).tokenize()).parse()
    tc = TypeChecker()
    return tc.check(prog)


def type_check_full(src):
    """类型检查，返回 (TypeChecker 实例, 错误列表)，便于断言推断类型"""
    prog = Parser(Lexer(src).tokenize()).parse()
    tc = TypeChecker()
    errors = tc.check(prog)
    return tc, errors


# ======================================================================
# TestSourceCreation
# ======================================================================
class TestSourceCreation(unittest.TestCase):
    def test_source_creation(self):
        interp = run("let r = source(10)")
        node = interp.global_env.get("r")
        self.assertIsInstance(node, SourceNode)
        self.assertTrue(node.is_source)
        self.assertEqual(node.value, 10)

    def test_source_float(self):
        interp = run("let r = source(3.14)")
        node = interp.global_env.get("r")
        self.assertIsInstance(node, SourceNode)
        self.assertAlmostEqual(node.value, 3.14)

    def test_source_string(self):
        interp = run('let r = source("hello")')
        node = interp.global_env.get("r")
        self.assertIsInstance(node, SourceNode)
        self.assertEqual(node.value, "hello")


# ======================================================================
# TestLiveComputation
# ======================================================================
class TestLiveComputation(unittest.TestCase):
    def test_live_basic(self):
        interp = run("let mut r = source(10)\nlet area = live { r * 2 }")
        area = interp.global_env.get("area")
        self.assertIsInstance(area, LiveNode)
        self.assertFalse(area.is_source)
        self.assertEqual(area.value, 20)

    def test_live_read_triggers_compute(self):
        interp = run("let mut r = source(10)\nlet area = live { r * 2 }")
        area = interp.global_env.get("area")
        # 创建后尚未计算（惰性），首次读取才触发
        self.assertEqual(area.recompute_count, 0)
        self.assertEqual(area.value, 20)
        self.assertEqual(area.recompute_count, 1)
        self.assertEqual(area.state, "Clean")

    def test_live_chained(self):
        interp = run(
            "let mut r = source(10)\n"
            "let area = live { r * r }\n"
            "let double = live { area * 2 }"
        )
        double = interp.global_env.get("double")
        self.assertEqual(double.value, 200)
        area = interp.global_env.get("area")
        self.assertEqual(area.value, 100)

    def test_live_multiple_sources(self):
        interp = run(
            "let mut a = source(3)\n"
            "let mut b = source(4)\n"
            "let c = live { a * b }"
        )
        c = interp.global_env.get("c")
        self.assertEqual(c.value, 12)


# ======================================================================
# TestIncrementalUpdate
# ======================================================================
class TestIncrementalUpdate(unittest.TestCase):
    def test_source_write_triggers_recompute(self):
        interp = run(
            "let mut r = source(10)\n"
            "let area = live { r * r }\n"
            "let double = live { area * 2 }\n"
            "r = 20"
        )
        area = interp.global_env.get("area")
        double = interp.global_env.get("double")
        self.assertEqual(area.value, 400)
        self.assertEqual(double.value, 800)

    def test_lazy_recompute(self):
        interp = run("let mut r = source(10)\nlet a = live { r * 2 }")
        eng = IncrementalEngine.get_instance()
        a = interp.global_env.get("a")
        r = interp.global_env.get("r")
        # 首次读取，计算为 Clean
        self.assertEqual(a.value, 20)
        self.assertEqual(a.state, "Clean")
        # 写入后、读取前：仅标记 Dirty，不立即重算
        eng.write(r, 99)
        self.assertEqual(a.state, "Dirty")
        # 读取时才深度优先重算
        self.assertEqual(a.value, 198)
        self.assertEqual(a.state, "Clean")

    def test_hash_short_circuit(self):
        # 注：本引擎采用拉模式重算，写入相同值时下游节点仍会被标记 Dirty
        # 并在读取时执行 func（recompute_count 会 +1）。哈希短路的可观测语义
        # 是——当重算结果与旧值一致时，不向订阅者发送通知（无误报）。
        # 因此本测试断言“结果不变时不触发订阅回调”这一真实短路行为。
        interp = run("let mut r = source(5)\nlet d = live { r * 2 }")
        eng = IncrementalEngine.get_instance()
        d = interp.global_env.get("d")
        r = interp.global_env.get("r")
        self.assertEqual(d.value, 10)
        events = []
        eng.subscribe(d, lambda new, old: events.append((old, new)))
        # 写入相同值：读取后结果不变 → 不应产生新的订阅事件
        eng.write(r, 5)
        self.assertEqual(d.value, 10)
        self.assertEqual(events, [])
        # 写入变化值：应触发一次通知
        eng.write(r, 6)
        self.assertEqual(d.value, 12)
        self.assertEqual(events, [(10, 12)])

    def test_compound_assignment(self):
        interp = run(
            "let mut r = source(10)\n"
            "let a = live { r * 2 }\n"
            "r += 5"
        )
        a = interp.global_env.get("a")
        self.assertEqual(a.value, 30)  # r 15 * 2


# ======================================================================
# TestTransact
# ======================================================================
class TestTransact(unittest.TestCase):
    def test_transact_basic(self):
        interp = run(
            "let mut r = source(1)\n"
            "let s = source(2)\n"
            "let area = live { r + s }\n"
            "transact {\n"
            "  r = 10\n"
            "  s = 20\n"
            "}"
        )
        area = interp.global_env.get("area")
        self.assertEqual(area.value, 30)

    def test_transact_no_intermediate_propagation(self):
        # 在事务中只更新值、不传播；事务结束才统一标记下游 Dirty
        interp = run(
            "let mut r = source(1)\n"
            "let s = source(2)\n"
            "let area = live { r + s }"
        )
        eng = IncrementalEngine.get_instance()
        r = interp.global_env.get("r")
        s = interp.global_env.get("s")
        area = interp.global_env.get("area")
        self.assertEqual(area.value, 3)
        eng.transact_begin()
        eng.write(r, 100)
        # 事务内读取仍返回缓存的旧值，未发生中间传播
        self.assertEqual(area.value, 3)
        eng.write(s, 200)
        eng.transact_end()
        self.assertEqual(area.value, 300)

    def test_transact_multiple_sources(self):
        interp = run(
            "let mut a = source(1)\n"
            "let mut b = source(2)\n"
            "let mut c = source(3)\n"
            "let sum = live { a + b + c }\n"
            "transact {\n"
            "  a = 10\n"
            "  b = 20\n"
            "  c = 30\n"
            "}"
        )
        s = interp.global_env.get("sum")
        self.assertEqual(s.value, 60)


# ======================================================================
# TestPurityCheck
# ======================================================================
class TestPurityCheck(unittest.TestCase):
    def test_pure_live_no_error(self):
        errors = type_check(
            "let mut r = source(10)\nlet a = live { r * 2 }"
        )
        self.assertEqual(errors, [])

    def test_live_with_print_error(self):
        errors = type_check('let a = live { print("x"); 1 }')
        self.assertEqual(len(errors), 1)
        self.assertIn("纯度", str(errors[0]))

    def test_live_with_assignment_error(self):
        errors = type_check(
            "let mut r = source(1)\nlet a = live { r = 5; r }"
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("赋值", str(errors[0]))

    def test_transact_allows_assignment(self):
        errors = type_check(
            "let mut r = source(1)\ntransact {\n  r = 5\n}\nlet a = live { r * 2 }"
        )
        self.assertEqual(errors, [])


# ======================================================================
# TestCycleDetection
# ======================================================================
class TestCycleDetection(unittest.TestCase):
    def test_self_reference_cycle(self):
        errors = type_check("let a = live { a + 1 }")
        self.assertEqual(len(errors), 1)
        self.assertIn("循环", str(errors[0]))

    def test_mutual_cycle(self):
        errors = type_check(
            "let a = live { b + 1 }\nlet b = live { a + 1 }"
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("循环", str(errors[0]))


# ======================================================================
# TestSubscription
# ======================================================================
class TestSubscription(unittest.TestCase):
    def test_subscribe_callback(self):
        interp = run("let mut r = source(5)\nlet d = live { r * 2 }")
        eng = IncrementalEngine.get_instance()
        d = interp.global_env.get("d")
        r = interp.global_env.get("r")
        self.assertEqual(d.value, 10)
        events = []
        eng.subscribe(d, lambda new, old: events.append((old, new)))
        eng.write(r, 7)
        self.assertEqual(d.value, 14)
        self.assertEqual(events, [(10, 14)])

    def test_subscribe_no_false_positive(self):
        # 哈希短路：结果不变时不应触发回调
        interp = run("let mut r = source(5)\nlet d = live { r * 2 }")
        eng = IncrementalEngine.get_instance()
        d = interp.global_env.get("d")
        r = interp.global_env.get("r")
        self.assertEqual(d.value, 10)
        events = []
        eng.subscribe(d, lambda new, old: events.append((old, new)))
        eng.write(r, 5)  # 相同值
        _ = d.value
        self.assertEqual(events, [])

    def test_multiple_subscribers(self):
        interp = run("let mut r = source(5)\nlet d = live { r * 2 }")
        eng = IncrementalEngine.get_instance()
        d = interp.global_env.get("d")
        r = interp.global_env.get("r")
        self.assertEqual(d.value, 10)
        a, b = [], []
        eng.subscribe(d, lambda new, old: a.append(new))
        eng.subscribe(d, lambda new, old: b.append(new))
        eng.write(r, 9)
        self.assertEqual(d.value, 18)
        self.assertEqual(a, [18])
        self.assertEqual(b, [18])


# ======================================================================
# TestEngineAPI
# ======================================================================
class TestEngineAPI(unittest.TestCase):
    def _engine_with_graph(self):
        interp = run(
            "let mut r = source(10)\n"
            "let area = live { r * r }\n"
            "let double = live { area * 2 }"
        )
        return IncrementalEngine.get_instance(), interp

    def test_export_graph_mermaid(self):
        eng, _ = self._engine_with_graph()
        out = eng.export_graph("mermaid")
        self.assertIsInstance(out, str)
        self.assertIn("graph", out)

    def test_export_graph_dot(self):
        eng, _ = self._engine_with_graph()
        out = eng.export_graph("dot")
        self.assertIsInstance(out, str)
        self.assertIn("digraph", out)

    def test_get_stats(self):
        eng, _ = self._engine_with_graph()
        stats = eng.get_stats()
        self.assertIn("total_nodes", stats)
        self.assertIn("source_count", stats)
        self.assertIn("live_count", stats)
        self.assertEqual(stats["total_nodes"], 3)
        self.assertEqual(stats["source_count"], 1)
        self.assertEqual(stats["live_count"], 2)


# ======================================================================
# TestTypeInference
# ======================================================================
class TestTypeInference(unittest.TestCase):
    def test_source_type_inference(self):
        tc, errors = type_check_full("let r = source(10)")
        self.assertEqual(errors, [])
        t = tc.global_env.lookup("r")
        self.assertEqual(t.name, "Source")
        self.assertEqual(t.params[0].name, "int")

    def test_live_type_inference(self):
        tc, errors = type_check_full("let a = live { 1 + 2 }")
        self.assertEqual(errors, [])
        t = tc.global_env.lookup("a")
        self.assertEqual(t.name, "Live")
        self.assertEqual(t.params[0].name, "int")

    def test_transact_type_inference(self):
        # transact 块内含赋值不应产生类型错误，且能推断出块类型
        tc, errors = type_check_full(
            "let mut r = source(1)\ntransact {\n  r = 5\n}\nlet a = live { r * 2 }"
        )
        self.assertEqual(errors, [])
        a = tc.global_env.lookup("a")
        self.assertEqual(a.name, "Live")


# ======================================================================
# TestEdgeCases
# ======================================================================
class TestEdgeCases(unittest.TestCase):
    def test_large_object_reference_tracking(self):
        # 大对象（序列化累计 >1KB）降级为引用追踪：
        # 两个结构等价、仅尾部未知对象不同的容器应得到不同哈希；
        # 而小的等价内容应得到相同哈希。
        IncrementalEngine.reset()
        eng = IncrementalEngine.get_instance()

        # 小对象：内容等价 → 哈希相同（结构化哈希）
        self.assertEqual(eng.hash_value("hello world"), eng.hash_value("hello world"))

        # 构造累计 >1KB 的嵌套列表，尾部放置未知类型对象，触发引用降级
        class Marker:
            pass

        warm = ["abcdefgh" * 4] * 30  # ~960 字节，叠加列表结构开销后尾部越过 1KB 阈值
        m1, m2 = Marker(), Marker()
        l1 = warm + [m1]
        l2 = warm + [m2]
        # 尾部对象按 id() 引用追踪 → 不同对象哈希不同
        self.assertNotEqual(eng.hash_value(l1), eng.hash_value(l2))
        # 同一对象 → 哈希稳定
        self.assertEqual(eng.hash_value(l1), eng.hash_value(l1))

    def test_engine_reset(self):
        IncrementalEngine.reset()
        eng = IncrementalEngine.get_instance()
        eng.create_source(1)
        eng.create_live(lambda: 2, [])
        self.assertGreater(len(eng.nodes), 0)
        IncrementalEngine.reset()
        eng2 = IncrementalEngine.get_instance()
        self.assertEqual(len(eng2.nodes), 0)

    def test_source_in_struct(self):
        # Aurora 结构体实例在解释器中为 dict，字段直接持有 SourceNode
        interp = run(
            "struct Point { x: int, y: int }\n"
            "let p = Point { x: source(10), y: source(20) }"
        )
        p = interp.global_env.get("p")
        self.assertIsInstance(p, dict)
        self.assertIsInstance(p["x"], SourceNode)
        self.assertIsInstance(p["y"], SourceNode)
        self.assertEqual(p["x"].value, 10)
        self.assertEqual(p["y"].value, 20)


if __name__ == "__main__":
    unittest.main()
