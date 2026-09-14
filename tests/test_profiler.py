"""Aurora 性能分析器测试"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.profiler import (  # noqa: E402
    profile, to_json, to_flamegraph, print_report, register_cli,
)


SIMPLE = """
fn add(a, b) {
    return a + b
}

fn main() {
    var s = 0
    var i = 0
    while i < 100 {
        s = s + add(i, i)
        i = i + 1
    }
    return s
}

main()
"""

RECURSIVE = """
fn fib(n) {
    if n < 2 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

fn main() {
    return fib(10)
}

main()
"""


class TestProfileBasics(unittest.TestCase):
    def setUp(self):
        self.result = profile(SIMPLE)

    def test_functions_recorded(self):
        self.assertIn("add", self.result.functions)
        self.assertIn("main", self.result.functions)

    def test_call_count(self):
        # add 在循环中被调用 100 次
        self.assertEqual(self.result.functions["add"].calls, 100)

    def test_total_time_positive(self):
        self.assertGreater(self.result.total_time, 0)
        self.assertGreater(self.result.functions["add"].total_time, 0)

    def test_self_time_non_negative(self):
        for st in self.result.functions.values():
            self.assertGreaterEqual(st.self_time, 0)
            self.assertGreaterEqual(st.total_time, st.self_time)

    def test_peak_memory_positive(self):
        self.assertGreater(self.result.peak_memory, 0)

    def test_call_graph(self):
        self.assertIn("main", self.result.call_graph)
        self.assertIn("add", self.result.call_graph["main"])
        self.assertEqual(self.result.call_graph["main"]["add"], 100)


class TestProfileRecursive(unittest.TestCase):
    def test_recursive_calls(self):
        r = profile(RECURSIVE)
        # fib(10) 共调用 177 次
        self.assertEqual(r.functions["fib"].calls, 177)
        # 递归自调用边
        self.assertEqual(r.call_graph["fib"]["fib"], 176)


class TestProfileOutput(unittest.TestCase):
    def setUp(self):
        self.result = profile(SIMPLE)

    def test_to_json_keys(self):
        data = json.loads(to_json(self.result))
        for key in ("total_time", "peak_memory", "functions", "call_graph"):
            self.assertIn(key, data)
        self.assertIn("add", data["functions"])
        for sub in ("calls", "total_time", "self_time", "avg_time"):
            self.assertIn(sub, data["functions"]["add"])

    def test_to_flamegraph_format(self):
        text = to_flamegraph(self.result)
        lines = [ln for ln in text.splitlines() if ln.strip()]
        self.assertTrue(lines)
        seen_nested = False
        for ln in lines:
            parts = ln.rsplit(" ", 1)
            self.assertEqual(len(parts), 2)
            # 最后一段是计数
            self.assertTrue(parts[1].isdigit())
            # 路径由函数名以分号分隔
            self.assertTrue(all(p for p in parts[0].split(";")))
            if ";" in parts[0]:
                seen_nested = True
        # 至少存在一条嵌套调用栈
        self.assertTrue(seen_nested)

    def test_print_report_runs(self):
        # 只要求不抛异常
        print_report(self.result, top_n=5)


class TestCli(unittest.TestCase):
    def test_register_cli(self):
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers()
        register_cli(sub)
        args = parser.parse_args([
            "profile", "x.aur", "--json", "o.json",
            "--flamegraph", "o.fg", "--top", "10",
        ])
        self.assertEqual(args.file, "x.aur")
        self.assertEqual(args.json_out, "o.json")
        self.assertEqual(args.flame_out, "o.fg")
        self.assertEqual(args.top, 10)


if __name__ == "__main__":
    unittest.main()
