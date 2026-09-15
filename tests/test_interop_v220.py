"""Aurora v2.2.0 多语言互操作测试 — JS/Java/Interop/WASM/FFI 增强"""

import os
import sys
import shutil
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 让 `from helpers import ...` 与 `import aurora...` 在 `python3 -m pytest tests/...` 下都可解析
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))            # tests/ 目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))                                          # aurora 包的父目录

from helpers import run_source, eval_expr                                 # noqa: E402
from aurora.stdlib import AuroraError                                     # noqa: E402
from aurora.stdlib import (                                              # noqa: E402
    AuroraJS, AuroraJava, AuroraInterop, AuroraWASM, AuroraFFI,
    STDLIB_MODULES,
)

# 环境检测
HAS_NODE = shutil.which("node") is not None
HAS_JAVA = shutil.which("java") is not None
HAS_JAVAC = shutil.which("javac") is not None


@unittest.skipUnless(HAS_NODE, "需要 Node.js 环境")
class TestAuroraJS(unittest.TestCase):
    def test_available(self):
        self.assertTrue(AuroraJS.available())

    def test_version(self):
        v = AuroraJS.version()
        self.assertIsInstance(v, str)
        self.assertTrue(v.startswith("v"))

    def test_eval_basic(self):
        self.assertEqual(AuroraJS.eval("1 + 2 * 3"), 7)

    def test_eval_array(self):
        result = AuroraJS.eval("[1, 2, 3].map(x => x * 2)")
        self.assertEqual(result, [2, 4, 6])

    def test_eval_object(self):
        result = AuroraJS.eval("({name: 'Aurora', version: 2.2})")
        self.assertEqual(result["name"], "Aurora")
        self.assertAlmostEqual(result["version"], 2.2)

    def test_call_global(self):
        self.assertEqual(AuroraJS.call("parseInt", "42"), 42)

    # 说明:AuroraJS.call 按 globalThis[name] 精确键解析,不支持 "Math.sqrt" 这类点路径;
    # Math.* 跨作用域通过 eval 求值。
    def test_eval_math_sqrt(self):
        self.assertAlmostEqual(AuroraJS.eval("Math.sqrt(81)"), 9.0)

    def test_eval_math_max(self):
        self.assertEqual(AuroraJS.eval("Math.max(3, 7, 2)"), 7)

    def test_require_os(self):
        info = AuroraJS.require("os")
        self.assertIn("platform", info)
        self.assertIn("arch", info)

    def test_eval_error(self):
        with self.assertRaises(AuroraError) as ctx:
            AuroraJS.eval("undefined_variable_xyz")
        self.assertEqual(ctx.exception.kind, "JSError")

    def test_run_file_js(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "test.js")
            with open(p, "w") as f:
                f.write("console.log(JSON.stringify({result: 42}));")
            r = AuroraJS.run_file(p)
            self.assertEqual(r["code"], 0)
            self.assertIn("42", r["out"])


@unittest.skipUnless(HAS_JAVA, "需要 Java 环境")
class TestAuroraJava(unittest.TestCase):
    def test_available(self):
        self.assertTrue(AuroraJava.available())

    def test_version(self):
        v = AuroraJava.version()
        self.assertIsInstance(v, str)
        self.assertIn("1", v)  # 版本号包含数字

    # 说明:jshell -s 静默模式不回显裸表达式,需用 System.out.println 并以换行结尾才会输出。
    def test_eval_basic(self):
        result = AuroraJava.eval("System.out.println(1 + 2 * 3);\n")
        self.assertEqual(result, "7")

    def test_eval_string(self):
        result = AuroraJava.eval('System.out.println("Hello".toUpperCase());\n')
        self.assertEqual(result, "HELLO")

    def test_call_math_sqrt(self):
        result = AuroraJava.call("java.lang.Math", "sqrt", 81.0)
        self.assertAlmostEqual(result, 9.0)

    def test_call_math_abs(self):
        result = AuroraJava.call("java.lang.Math", "abs", -42)
        self.assertEqual(result, 42)

    def test_call_integer_parseInt(self):
        result = AuroraJava.call("java.lang.Integer", "parseInt", "100")
        self.assertEqual(result, 100)

    def test_call_string_valueOf(self):
        result = AuroraJava.call("java.lang.String", "valueOf", 123)
        self.assertEqual(result, "123")

    @unittest.skipUnless(HAS_JAVAC, "需要 javac 编译器")
    def test_compile_and_run(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "Hello.java")
            with open(src, "w") as f:
                f.write('public class Hello { public static void main(String[] args) { System.out.println("hello from java"); } }')
            AuroraJava.compile(src, output_dir=d)
            r = AuroraJava.run("Hello", classpath=d)
            self.assertEqual(r["code"], 0)
            self.assertIn("hello from java", r["out"])


class TestAuroraInterop(unittest.TestCase):
    def test_languages(self):
        langs = AuroraInterop.languages()
        self.assertIn("python", langs)
        self.assertIn("js", langs)
        self.assertIn("java", langs)
        self.assertIn("c", langs)
        self.assertIn("cpp", langs)
        self.assertIn("rust", langs)
        self.assertIn("go", langs)

    def test_status(self):
        status = AuroraInterop.status()
        self.assertTrue(status["python"])  # python 永远可用
        self.assertIn("js", status)
        self.assertIn("java", status)

    def test_eval_python(self):
        self.assertEqual(AuroraInterop.eval("python", "1 + 2 * 3"), 7)

    def test_eval_python_string(self):
        self.assertEqual(AuroraInterop.eval("python", "'hello'.upper()"), "HELLO")

    def test_call_python(self):
        result = AuroraInterop.call("python", "__import__('math').sqrt(81)")
        self.assertAlmostEqual(result, 9.0)

    # 说明:Python 关键字 import 不能写成 AuroraInterop.import(...),类上的实际方法名为 _import
    # (在 STDLIB_MODULES 中以 'import' 名注册)。
    def test_import_python(self):
        m = AuroraInterop._import("python", "math")
        self.assertAlmostEqual(m.sqrt(144), 12.0)

    def test_unknown_language(self):
        with self.assertRaises(AuroraError) as ctx:
            AuroraInterop.eval("ruby", "1 + 1")
        self.assertEqual(ctx.exception.kind, "InteropError")

    def test_unknown_language_call(self):
        with self.assertRaises(AuroraError) as ctx:
            AuroraInterop.call("ruby", "puts 1")
        self.assertEqual(ctx.exception.kind, "InteropError")

    @unittest.skipUnless(HAS_NODE, "需要 Node.js")
    def test_eval_js(self):
        self.assertEqual(AuroraInterop.eval("js", "1 + 2 * 3"), 7)

    @unittest.skipUnless(HAS_NODE, "需要 Node.js")
    def test_call_js(self):
        self.assertEqual(AuroraInterop.call("js", "parseInt", "42"), 42)

    @unittest.skipUnless(HAS_JAVA, "需要 Java")
    def test_eval_java(self):
        result = AuroraInterop.eval("java", "System.out.println(1 + 2 * 3);\n")
        self.assertEqual(result, "7")


@unittest.skipUnless(HAS_NODE, "需要 Node.js 环境")
class TestAuroraWASM(unittest.TestCase):
    def test_available(self):
        self.assertTrue(AuroraWASM.available())

    def _make_add_wasm(self, d):
        """创建一个简单的 add(i32,i32)->i32 WASM 模块"""
        # WASM 二进制: magic + version + type section + function section + export section + code section
        wasm_bytes = bytes([
            0x00, 0x61, 0x73, 0x6d,  # magic \0asm
            0x01, 0x00, 0x00, 0x00,  # version 1
            0x01, 0x07, 0x01,        # type section: 1 type
            0x60, 0x02, 0x7f, 0x7f,  # func (i32, i32)
            0x01, 0x7f,               # -> i32
            0x03, 0x02, 0x01, 0x00,  # function section: 1 func, type 0
            0x07, 0x07, 0x01,        # export section: 1 export
            0x03, 0x61, 0x64, 0x64,  # name "add"
            0x00, 0x00,               # func index 0
            0x0a, 0x09, 0x01,        # code section: 1 body
            0x07, 0x00,               # body size 7, 0 locals
            0x20, 0x00,               # local.get 0
            0x20, 0x01,               # local.get 1
            0x6a,                      # i32.add
            0x0b,                      # end
        ])
        p = os.path.join(d, "add.wasm")
        with open(p, "wb") as f:
            f.write(wasm_bytes)
        return p

    def test_load(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._make_add_wasm(d)
            module = AuroraWASM.load(p)
            self.assertTrue(module["loaded"])
            self.assertIn("add", module["exports"])

    def test_exports(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._make_add_wasm(d)
            exports = AuroraWASM.exports(p)
            self.assertIn("add", exports)

    def test_call_add(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._make_add_wasm(d)
            module = AuroraWASM.load(p)
            result = AuroraWASM.call(module, "add", 3, 4)
            self.assertEqual(result, 7)

    def test_call_add_large(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._make_add_wasm(d)
            module = AuroraWASM.load(p)
            result = AuroraWASM.call(module, "add", 100, 200)
            self.assertEqual(result, 300)


class TestFFIEnhanced(unittest.TestCase):
    def test_struct(self):
        Point = AuroraFFI.struct("Point", [("x", "i32"), ("y", "i32")])
        p = Point(x=10, y=20)
        self.assertEqual(p.x, 10)
        self.assertEqual(p.y, 20)

    def test_struct_multiple_fields(self):
        Config = AuroraFFI.struct("Config", [
            ("port", "i32"), ("enabled", "bool"), ("ratio", "f64")
        ])
        c = Config(port=8080, enabled=True, ratio=3.14)
        self.assertEqual(c.port, 8080)
        self.assertTrue(c.enabled)
        self.assertAlmostEqual(c.ratio, 3.14)

    def test_callback(self):
        CallbackType = AuroraFFI.callback("i32", ["i32", "i32"])
        def add(a, b):
            return a + b
        cb = CallbackType(add)
        self.assertEqual(cb(3, 4), 7)

    def test_callback_void(self):
        CallbackType = AuroraFFI.callback("void", ["str"])
        called = []
        def log(s):
            called.append(s)
        cb = CallbackType(log)
        cb(b"hello")
        self.assertEqual(called, [b"hello"])

    def test_string_array(self):
        arr = AuroraFFI.string_array(["hello", "world", "aurora"])
        self.assertEqual(arr[0], b"hello")
        self.assertEqual(arr[1], b"world")
        self.assertEqual(arr[2], b"aurora")

    def test_string_array_empty(self):
        arr = AuroraFFI.string_array([])
        self.assertEqual(len(arr), 0)

    def test_ptr_and_deref(self):
        p = AuroraFFI.ptr(42, "i32")
        self.assertEqual(AuroraFFI.deref(p), 42)

    def test_ptr_float(self):
        p = AuroraFFI.ptr(3.14, "f64")
        self.assertAlmostEqual(AuroraFFI.deref(p), 3.14)

    def test_gen_bindings_rust(self):
        code = AuroraFFI.gen_bindings("rust", [
            {"name": "add", "args": ["i32", "i32"], "ret": "i32"}
        ])
        self.assertIn("#[no_mangle]", code)
        self.assertIn('extern "C"', code)
        self.assertIn("fn add", code)

    def test_gen_bindings_cpp(self):
        code = AuroraFFI.gen_bindings("cpp", [
            {"name": "add", "args": ["i32", "i32"], "ret": "i32"}
        ])
        self.assertIn('extern "C"', code)
        self.assertIn("add", code)

    def test_gen_bindings_go(self):
        code = AuroraFFI.gen_bindings("go", [
            {"name": "add", "args": ["i32", "i32"], "ret": "i32"}
        ])
        self.assertIn('import "C"', code)
        self.assertIn("//export add", code)
        self.assertIn("func add", code)

    def test_gen_bindings_multiple(self):
        code = AuroraFFI.gen_bindings("rust", [
            {"name": "add", "args": ["i32", "i32"], "ret": "i32"},
            {"name": "multiply", "args": ["f64", "f64"], "ret": "f64"},
        ])
        self.assertIn("fn add", code)
        self.assertIn("fn multiply", code)

    def test_gen_bindings_output_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "bindings.rs")
            AuroraFFI.gen_bindings("rust", [
                {"name": "add", "args": ["i32", "i32"], "ret": "i32"}
            ], output_path=p)
            self.assertTrue(os.path.exists(p))
            content = open(p).read()
            self.assertIn("#[no_mangle]", content)

    def test_gen_bindings_bad_lang(self):
        with self.assertRaises(AuroraError):
            AuroraFFI.gen_bindings("ruby", [{"name": "f", "args": [], "ret": "void"}])


class TestModuleRegistration(unittest.TestCase):
    def test_std_js_registered(self):
        self.assertIn("std.js", STDLIB_MODULES)
        self.assertIn("eval", STDLIB_MODULES["std.js"])
        self.assertIn("call", STDLIB_MODULES["std.js"])
        self.assertIn("require", STDLIB_MODULES["std.js"])
        self.assertIn("run_file", STDLIB_MODULES["std.js"])
        self.assertIn("version", STDLIB_MODULES["std.js"])
        self.assertIn("available", STDLIB_MODULES["std.js"])

    def test_std_java_registered(self):
        self.assertIn("std.java", STDLIB_MODULES)
        self.assertIn("call", STDLIB_MODULES["std.java"])
        self.assertIn("run", STDLIB_MODULES["std.java"])
        self.assertIn("eval", STDLIB_MODULES["std.java"])
        self.assertIn("compile", STDLIB_MODULES["std.java"])

    def test_std_interop_registered(self):
        self.assertIn("std.interop", STDLIB_MODULES)
        self.assertIn("call", STDLIB_MODULES["std.interop"])
        self.assertIn("import", STDLIB_MODULES["std.interop"])
        self.assertIn("eval", STDLIB_MODULES["std.interop"])
        self.assertIn("languages", STDLIB_MODULES["std.interop"])
        self.assertIn("status", STDLIB_MODULES["std.interop"])

    def test_std_wasm_registered(self):
        self.assertIn("std.wasm", STDLIB_MODULES)
        self.assertIn("load", STDLIB_MODULES["std.wasm"])
        self.assertIn("call", STDLIB_MODULES["std.wasm"])
        self.assertIn("exports", STDLIB_MODULES["std.wasm"])

    def test_std_ffi_enhanced(self):
        self.assertIn("struct", STDLIB_MODULES["std.ffi"])
        self.assertIn("callback", STDLIB_MODULES["std.ffi"])
        self.assertIn("string_array", STDLIB_MODULES["std.ffi"])
        self.assertIn("ptr", STDLIB_MODULES["std.ffi"])
        self.assertIn("deref", STDLIB_MODULES["std.ffi"])
        self.assertIn("gen_bindings", STDLIB_MODULES["std.ffi"])
        # 原有方法不变
        self.assertIn("load", STDLIB_MODULES["std.ffi"])
        self.assertIn("func", STDLIB_MODULES["std.ffi"])
        self.assertIn("cstr", STDLIB_MODULES["std.ffi"])


class TestAuroraSourceLevel(unittest.TestCase):
    """通过 Aurora 源码测试模块导入和基本调用"""

    def test_import_std_interop(self):
        src = """
import std.interop
let langs = std.interop.languages()
println("langs count: " + str(langs.len()))
"""
        run_source(src)
        # 不抛异常即通过

    def test_interop_eval_python_via_aurora(self):
        src = """
import std.interop
let result = std.interop.eval("python", "1 + 2 * 3")
println("result: " + str(result))
"""
        run_source(src)

    def test_import_std_js_module(self):
        src = """
import std.js
let avail = std.js.available()
println("js available: " + str(avail))
"""
        run_source(src)

    def test_import_std_java_module(self):
        src = """
import std.java
let avail = std.java.available()
println("java available: " + str(avail))
"""
        run_source(src)

    def test_import_std_wasm_module(self):
        src = """
import std.wasm
let avail = std.wasm.available()
println("wasm available: " + str(avail))
"""
        run_source(src)

    def test_ffi_struct_via_aurora(self):
        src = """
import std.ffi
let Point = std.ffi.struct("Point", [["x", "i32"], ["y", "i32"]])
println("struct created")
"""
        run_source(src)

    def test_ffi_gen_bindings_via_aurora(self):
        src = """
import std.ffi
let code = std.ffi.gen_bindings("rust", [{"name": "add", "args": ["i32", "i32"], "ret": "i32"}])
println("bindings generated: " + str(code.len()) + " chars")
"""
        run_source(src)


if __name__ == '__main__':
    unittest.main()
