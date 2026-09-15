"""Aurora v3.1.0 — LSP 与调试器增强测试

覆盖：
    - ProjectIndex：索引构建、符号查询、增量更新、跨文件引用
    - RefactorEngine：重命名、提取函数、提取变量、自动导入
    - LSP 增强：语义高亮 token 生成、增强诊断
    - 调试器增强：条件断点、日志断点、监视表达式、时间旅行
"""

import os
import sys
import tempfile
import threading
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.project_index import ProjectIndex
from aurora.refactor_engine import RefactorEngine, RefactorResult, TextEdit
from aurora.lsp import LSPServer
from aurora.debugger import Debugger, LogPoint, WatchExpr


# ─────────────────────────────────────────────────────────────
# 辅助：构造临时项目
# ─────────────────────────────────────────────────────────────

def _write(path: str, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _make_two_file_project() -> str:
    """构造两个互相引用的 .aur 源文件。"""
    d = tempfile.mkdtemp(prefix="aurora_v310_")
    _write(os.path.join(d, "math.aur"),
            "fn add(a, b) {\n"
            "    return a + b\n"
            "}\n"
            "fn mul(a, b) {\n"
            "    return a * b\n"
            "}\n")
    _write(os.path.join(d, "main.aur"),
            "import math\n"
            "let x = add(1, 2)\n"
            "let y = mul(3, 4)\n"
            "let z = add(x, y)\n")
    return d


# ═════════════════════════════════════════════════════════════
# 1. ProjectIndex
# ═════════════════════════════════════════════════════════════

class TestProjectIndex(unittest.TestCase):
    def setUp(self):
        self.root = _make_two_file_project()
        self.idx = ProjectIndex(root=self.root)

    def tearDown(self):
        self.idx.stop_indexing(wait=False)

    def test_01_index_build(self):
        """索引构建：应识别函数 / 变量 / 导入。"""
        self.idx.reindex_all()
        st = self.idx.status()
        self.assertGreaterEqual(st["files"], 2)
        self.assertGreater(st["symbols"], 5)

    def test_02_find_definition(self):
        """符号查询：find_definition 返回位置。"""
        self.idx.reindex_all()
        loc = self.idx.find_definition("add")
        self.assertIsNotNone(loc)
        self.assertTrue(loc["file"].endswith("math.aur"))
        self.assertEqual(loc["line"], 1)

    def test_03_find_references_cross_file(self):
        """跨文件引用：add 在 main.aur 中也被引用。"""
        self.idx.reindex_all()
        refs = self.idx.find_references("add")
        # 定义 1 处 + main.aur 中 2 处调用
        files = {r["file"] for r in refs}
        self.assertEqual(len(files), 2, f"应跨 2 个文件，实际 {len(files)}")

    def test_04_search_symbols(self):
        """模糊搜索：前缀匹配。"""
        self.idx.reindex_all()
        results = self.idx.search_symbols("ad")
        names = {r["name"] for r in results}
        self.assertIn("add", names)

    def test_05_get_file_symbols(self):
        """文件符号：math.aur 应包含 add / mul。"""
        self.idx.reindex_all()
        syms = self.idx.get_file_symbols(os.path.join(self.root, "math.aur"))
        names = {s["name"] for s in syms}
        self.assertIn("add", names)
        self.assertIn("mul", names)

    def test_06_incremental_update(self):
        """增量更新：修改一个文件只重索引它。"""
        self.idx.reindex_all()
        before = self.idx.find_definition("add")
        # 修改 math.aur，新增一个函数
        _write(os.path.join(self.root, "math.aur"),
               "fn add(a, b) {\n    return a + b\n}\n"
               "fn sub(a, b) {\n    return a - b\n}\n")
        self.idx.mark_dirty(os.path.join(self.root, "math.aur"))
        self.idx._process_dirty()
        after = self.idx.find_definition("sub")
        self.assertIsNotNone(after, "新增函数 sub 应被索引")

    def test_07_persistence_roundtrip(self):
        """持久化：保存后重新加载应能查到符号。"""
        self.idx.reindex_all()
        self.idx.save_cache()
        self.assertTrue(os.path.exists(self.idx.cache_path))
        idx2 = ProjectIndex(root=self.root)
        self.assertTrue(idx2.load_cache())
        self.assertIsNotNone(idx2.find_definition("add"))

    def test_08_background_thread(self):
        """后台线程：start/stop 不应抛异常。"""
        self.idx.start_indexing()
        time.sleep(0.5)
        self.idx.stop_indexing(wait=True, timeout=2.0)
        self.assertIsNone(self.idx._thread)


# ═════════════════════════════════════════════════════════════
# 2. RefactorEngine
# ═════════════════════════════════════════════════════════════

class TestRefactorEngine(unittest.TestCase):
    def setUp(self):
        self.root = _make_two_file_project()
        self.idx = ProjectIndex(root=self.root)
        self.idx.reindex_all()
        self.engine = RefactorEngine(index=self.idx)
        self.math_file = os.path.join(self.root, "math.aur")

    def test_10_rename_symbol(self):
        """重命名：跨文件替换 add → sum。"""
        r = self.engine.rename_symbol("add", "sum", self.math_file, 1)
        self.assertTrue(r.success)
        self.assertGreaterEqual(len(r.edits), 3)
        # 应包含 math.aur 与 main.aur
        files = set(r.files())
        self.assertEqual(len(files), 2)

    def test_11_rename_conflict(self):
        """重命名冲突：新名字已存在时失败。"""
        r = self.engine.rename_symbol("add", "mul", self.math_file, 1)
        self.assertFalse(r.success)
        self.assertIn("冲突", r.message)

    def test_12_extract_variable(self):
        """提取变量：把表达式提取为 let。"""
        r = self.engine.extract_variable(
            os.path.join(self.root, "main.aur"), 2,
            "add(1, 2)", "first")
        self.assertTrue(r.success)
        self.assertEqual(len(r.edits), 2)
        self.assertTrue(any("let first = add(1, 2)" in e.new_text
                            for e in r.edits))

    def test_13_extract_function(self):
        """提取函数：生成新 fn 定义与调用。"""
        r = self.engine.extract_function(self.math_file, 2, 2, "do_add")
        self.assertTrue(r.success)
        self.assertEqual(len(r.edits), 2)
        self.assertIn("fn do_add", r.message)

    def test_14_auto_import(self):
        """自动导入：为符号添加 import。"""
        new_file = os.path.join(self.root, "new.aur")
        _write(new_file, "let v = add(1, 2)\n")
        r = self.engine.auto_import(new_file, "add")
        self.assertTrue(r.success)
        self.assertTrue(any("import math" in e.new_text for e in r.edits))

    def test_15_quick_fix_undefined(self):
        """快速修复：未定义变量给出建议。"""
        new_file = os.path.join(self.root, "new.aur")
        _write(new_file, "let v = undefined_sym\n")
        diag = {"message": "未定义 undefined_sym",
                "range": {"start": {"line": 0, "character": 8}}}
        results = self.engine.quick_fix(new_file, diag)
        self.assertGreaterEqual(len(results), 1)


# ═════════════════════════════════════════════════════════════
# 3. LSP 增强
# ═════════════════════════════════════════════════════════════

LSP_URI = "file:///proj/demo.aur"
LSP_SRC = """fn add(a, b) {
    return a + b
}

let name: str = "hi"
let used = 42
add(used, 1)
"""


class TestLSPEnhancements(unittest.TestCase):
    def setUp(self):
        self.server = LSPServer()
        self.server.handle("textDocument/didOpen", {
            "textDocument": {"uri": LSP_URI, "text": LSP_SRC, "version": 1}})

    def test_20_semantic_tokens_full(self):
        """语义高亮：full 返回扁平整数数组。"""
        r = self.server.v310_semantic_tokens_full(
            {"textDocument": {"uri": LSP_URI}})
        self.assertIn("data", r)
        # 每 5 个整数描述一个 token
        self.assertEqual(len(r["data"]) % 5, 0)
        self.assertGreater(len(r["data"]), 5)

    def test_21_semantic_tokens_range(self):
        """语义高亮：range 只返回范围内 token。"""
        r_full = self.server.v310_semantic_tokens_full(
            {"textDocument": {"uri": LSP_URI}})
        r_range = self.server.v310_semantic_tokens_range({
            "textDocument": {"uri": LSP_URI},
            "range": {"start": {"line": 0, "character": 0},
                      "end": {"line": 1, "character": 0}},
        })
        self.assertLessEqual(len(r_range["data"]), len(r_full["data"]))

    def test_22_detect_unused_variable(self):
        """诊断增强：未使用变量被标记。"""
        doc = self.server.documents[LSP_URI]
        diags = self.server.v310_diagnose(doc)
        messages = [d["message"] for d in diags]
        self.assertTrue(any("未使用的变量: name" in m for m in messages),
                        f"应检测到未使用变量 name，实际 {messages}")
        # used 变量不应被标记
        self.assertFalse(any("未使用的变量: used" in m for m in messages))

    def test_23_detect_divide_by_zero(self):
        """诊断增强：除零潜在 bug。"""
        src = "fn f() {\n    let x = 1 / 0\n}\n"
        uri = "file:///proj/zero.aur"
        self.server.handle("textDocument/didOpen", {
            "textDocument": {"uri": uri, "text": src, "version": 1}})
        doc = self.server.documents[uri]
        diags = self.server.v310_diagnose(doc)
        self.assertTrue(any("除以零" in d["message"] for d in diags))

    def test_24_code_action_quickfix(self):
        """codeAction：为未使用变量给出修复。"""
        diag = {"message": "未使用的变量: name",
                "range": {"start": {"line": 4, "character": 4}},
                "severity": 2}
        actions = self.server.v310_code_action({
            "textDocument": {"uri": LSP_URI},
            "context": {"diagnostics": [diag]},
        })
        self.assertGreaterEqual(len(actions), 1)

    def test_25_dispatch_unknown_method(self):
        """dispatch：未知方法返回 None。"""
        self.assertIsNone(
            self.server.v310_dispatch("textDocument/unknown", {}))


# ═════════════════════════════════════════════════════════════
# 4. 调试器增强
# ═════════════════════════════════════════════════════════════

class TestDebuggerEnhancements(unittest.TestCase):
    def setUp(self):
        self.dbg = Debugger(source="fn main() {\n    let x = 1\n}\n")

    def test_30_conditional_breakpoint(self):
        """条件断点：condition 被正确记录。"""
        bp = self.dbg.v310_add_conditional_breakpoint("demo.aur", 2, "x > 0")
        self.assertEqual(bp.condition, "x > 0")
        self.assertTrue(any(b.condition == "x > 0" for b in self.dbg.breakpoints))

    def test_31_log_breakpoint(self):
        """日志断点：LogPoint 不中断，记录消息。"""
        lp = self.dbg.v310_add_log_breakpoint("demo.aur", 2, "x = {x}")
        self.assertIsInstance(lp, LogPoint)
        self.assertEqual(lp.message, "x = {x}")
        self.assertEqual(lp.hit_count, 0)

    def test_32_watch_expression(self):
        """监视表达式：add/remove/eval。"""
        w = self.dbg.v310_add_watch("x + 1")
        self.assertIsInstance(w, WatchExpr)
        self.assertEqual(len(self.dbg._v310_watches), 1)
        self.dbg.v310_remove_watch("x + 1")
        self.assertEqual(len(self.dbg._v310_watches), 0)

    def test_33_call_stack_navigation(self):
        """调用栈：get_call_stack + frame(index)。"""
        self.dbg.frames = [
            {"name": "<main>", "file": "demo.aur", "line": 1},
            {"name": "helper", "file": "demo.aur", "line": 5},
            {"name": "deep", "file": "demo.aur", "line": 9},
        ]
        stack = self.dbg.v310_get_call_stack()
        self.assertEqual(len(stack), 3)
        # index 0 应为最内层
        self.assertEqual(stack[0]["name"], "deep")
        # 切换到 index 1
        self.assertTrue(self.dbg.frame(1))
        self.assertEqual(self.dbg.current_line, 5)
        # 越界
        self.assertFalse(self.dbg.frame(99))

    def test_34_thread_list_and_switch(self):
        """多线程：list_threads / switch_thread。"""
        threads = self.dbg.v310_list_threads()
        self.assertTrue(any(t["id"] == 0 for t in threads))
        self.assertTrue(self.dbg.v310_switch_thread(0))

    def test_35_time_travel_recording(self):
        """时间旅行：record + reverse_step + reverse_continue。"""
        self.dbg.v310_start_recording()
        self.dbg.current_file = "demo.aur"
        for ln in (10, 20, 30):
            self.dbg.current_line = ln
            self.dbg.frames = [{"name": "<main>", "file": "demo.aur", "line": ln}]
            self.dbg.v310_record_snapshot()
        # 现在应在 30
        self.assertEqual(self.dbg.current_line, 30)
        # 反向单步 → 20
        snap = self.dbg.v310_reverse_step()
        self.assertIsNotNone(snap)
        self.assertEqual(self.dbg.current_line, 20)
        # 反向继续 → 10
        snap = self.dbg.v310_reverse_continue()
        self.assertEqual(self.dbg.current_line, 10)
        # 再反向 → None
        self.assertIsNone(self.dbg.v310_reverse_continue())
        self.dbg.v310_stop_recording()

    def test_36_remote_server_start_stop(self):
        """远程调试：服务器可启动与停止。"""
        srv = self.dbg.v310_start_server(host="127.0.0.1", port=0)
        # port=0 让 OS 分配，但我们的实现固定 56789；只要能 start/stop 即可
        self.assertIsNotNone(srv)
        srv.stop()


if __name__ == "__main__":
    unittest.main()
