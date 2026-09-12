"""生态链测试:JSON / Python 桥 / FFI / HTML / 进程 / VEX / 原始字符串"""

import os
import sys
import tempfile
import unittest

from helpers import run_source, eval_expr
from aurora.stdlib import AuroraError
from aurora.stdlib import (
    AuroraJson, AuroraPython, AuroraFFI, AuroraHtml,
    AuroraProc, AuroraVex,
)


class TestRawString(unittest.TestCase):
    def test_raw_no_interpolation(self):
        # 原始字符串:不插值、保留反斜杠(Aurora 源码 r"\\" = 两个反斜杠)
        src = 'let n = 42\nr"hello {n} \\\\ path"'
        self.assertEqual(eval_expr(src), "hello {n} \\\\ path")

    def test_raw_json_literal(self):
        src = "r'{\"a\": 1}'"
        self.assertEqual(eval_expr(src), '{"a": 1}')

    def test_normal_string_still_interpolates(self):
        self.assertEqual(eval_expr('let n = 7\n"v={n}"'), "v=7")


class TestJsonModule(unittest.TestCase):
    def test_parse_stringify(self):
        data = AuroraJson.parse('{"a": 1, "b": [1, 2, 3]}')
        self.assertEqual(data["a"], 1)
        self.assertEqual(AuroraJson.stringify({"x": "你好"}), '{"x": "你好"}')

    def test_load_save(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "data.json")
            AuroraJson.save(p, {"k": [1, 2]})
            self.assertEqual(AuroraJson.load(p), {"k": [1, 2]})

    def test_parse_error(self):
        with self.assertRaises(AuroraError) as ctx:
            AuroraJson.parse("{bad")
        self.assertEqual(ctx.exception.kind, "JsonError")


class TestPythonBridge(unittest.TestCase):
    def test_eval(self):
        self.assertEqual(AuroraPython.eval("1 + 2 * 3"), 7)

    def test_import_and_call(self):
        m = AuroraPython.import_module("math")
        self.assertEqual(m.sqrt(81), 9.0)
        self.assertEqual(AuroraPython.call(m.floor, 3.7), 3)

    def test_error(self):
        with self.assertRaises(AuroraError) as ctx:
            AuroraPython.eval("1 / 0")
        self.assertEqual(ctx.exception.kind, "PythonError")


class TestFfiModule(unittest.TestCase):
    def test_load_system_lib(self):
        # macOS 系统 libm,不依赖项目内编译产物
        lib = AuroraFFI.load("/usr/lib/libm.dylib")
        fn = AuroraFFI.func(lib, "pow", ["f64", "f64"], "f64")
        self.assertAlmostEqual(fn(2.0, 10.0), 1024.0)

    def test_missing_symbol(self):
        with self.assertRaises(AuroraError) as ctx:
            lib = AuroraFFI.load("/usr/lib/libm.dylib")
            AuroraFFI.func(lib, "no_such_symbol_xyz", [], "void")
        self.assertEqual(ctx.exception.kind, "FFIError")

    def test_cstr(self):
        self.assertEqual(AuroraFFI.cstr("hi"), b"hi")


class TestHtmlModule(unittest.TestCase):
    def test_escape(self):
        self.assertEqual(AuroraHtml.escape("<b>&"), "&lt;b&gt;&amp;")

    def test_render(self):
        out = AuroraHtml.render("<p>{{name}}</p>", {"name": "<x>"})
        self.assertEqual(out, "<p>&lt;x&gt;</p>")

    def test_page_and_write(self):
        doc = AuroraHtml.page("t", "<p>hi</p>")
        self.assertIn("<!DOCTYPE html>", doc)
        self.assertIn("<title>t</title>", doc)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.html")
            self.assertEqual(AuroraHtml.write(p, doc), p)
            self.assertIn("<title>t</title>", open(p).read())


class TestProcModule(unittest.TestCase):
    def test_run(self):
        r = AuroraProc.run("python3 -c 'print(40 + 2)'")
        self.assertEqual(r["code"], 0)
        self.assertEqual(r["out"].strip(), "42")

    def test_call_args(self):
        out = AuroraProc.call_args(["python3", "-c", "print(sum(range(5)))"])
        self.assertEqual(out.strip(), "10")

    def test_stdin_exchange(self):
        # 子进程读 stdin JSON,回写结果
        code = (
            "import sys, json; "
            "d = json.load(sys.stdin); "
            "print(json.dumps({'n': len(d)}))")
        out = AuroraProc.call_args(
            ["python3", "-c", code], stdin='[1, 2, 3]')
        self.assertEqual(out.strip(), '{"n": 3}')

    def test_error_on_nonzero(self):
        with self.assertRaises(AuroraError):
            AuroraProc.call("python3 -c 'import sys; sys.exit(3)'")


class TestVexModule(unittest.TestCase):
    def test_export_python(self):
        with tempfile.TemporaryDirectory() as d:
            info = AuroraVex.python(d, "bot", "brain.screen.print(\"hi\")")
            self.assertEqual(info["file"], "main.py")
            content = open(os.path.join(d, "bot", "main.py")).read()
            self.assertIn("from vex import *", content)
            self.assertIn('print("hi")', content)

    def test_export_cpp(self):
        with tempfile.TemporaryDirectory() as d:
            info = AuroraVex.cpp(d, "bot", "vex::brain Brain;")
            self.assertEqual(info["file"], "main.cpp")
            content = open(os.path.join(d, "bot", "main.cpp")).read()
            self.assertIn('#include "vex.h"', content)

    def test_bad_lang(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(AuroraError) as ctx:
                AuroraVex.export(d, "bot", "x", "ruby")
            self.assertEqual(ctx.exception.kind, "VexError")


if __name__ == '__main__':
    unittest.main()
