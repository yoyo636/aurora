"""解释器测试 — 覆盖全部运行时特性"""

import unittest

from aurora.interpreter import Interpreter
from aurora.stdlib import AuroraResult, AuroraEnumVariant, AuroraChannel, AuroraError
from helpers import compile_source, run_source, eval_expr


def last_result(src):
    """执行源码，返回最后一条表达式语句的值"""
    program = compile_source(src)
    interp = Interpreter()
    interp.run(program)
    from aurora.ast_nodes import ExprStmt
    for stmt in reversed(program.statements):
        if isinstance(stmt, ExprStmt):
            return interp._eval(stmt.expr, interp.global_env)
    return None


class TestExpressions(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(last_result('1 + 2 * 3'), 7)
        self.assertEqual(last_result('2 ** 3 ** 2'), 512)  # 右结合? 2**(3**2)
        self.assertEqual(last_result('10 % 3'), 1)
        self.assertEqual(last_result('7 / 2'), 3.5)

    def test_comparison_logic(self):
        self.assertTrue(last_result('1 < 2 && 3 >= 3'))
        self.assertFalse(last_result('1 == 2 || false'))
        self.assertTrue(last_result('!false'))

    def test_bitwise_ops(self):
        self.assertEqual(last_result('5 << 2'), 20)
        self.assertEqual(last_result('16 >> 2'), 4)
        self.assertEqual(last_result('6 & 3'), 2)
        self.assertEqual(last_result('4 | 1'), 5)
        self.assertEqual(last_result('5 ^ 3'), 6)
        # C 语义优先级：加法高于移位
        self.assertEqual(last_result('1 + 2 << 3'), 24)
        self.assertEqual(last_result('1 << 2 + 3'), 32)

    def test_input_read_int(self):
        import io
        import sys as _sys
        old = _sys.stdin
        try:
            _sys.stdin = io.StringIO('42\n')
            interp = run_source('let x = read_int()')
            self.assertEqual(interp.global_env.get('x'), 42)
            _sys.stdin = io.StringIO('3.5\n')
            interp = run_source('let y = read_float()')
            self.assertEqual(interp.global_env.get('y'), 3.5)
            _sys.stdin = io.StringIO('abc\n')
            interp = run_source('let z = read_line()')
            self.assertEqual(interp.global_env.get('z'), 'abc')
        finally:
            _sys.stdin = old

    def test_string_concat(self):
        self.assertEqual(last_result('"a" + "b"'), 'ab')

    def test_collections(self):
        self.assertEqual(last_result('[1, 2, 3].len()'), 3)
        self.assertEqual(last_result('{"a": 1}.get("a")'), 1)
        self.assertEqual(last_result('(1, "x").len()'), 2)


class TestVariablesAndScope(unittest.TestCase):
    def test_let_and_mutation(self):
        interp = run_source('var x = 1\nx = x + 5')
        self.assertEqual(interp.global_env.get('x'), 6)

    def test_block_scope(self):
        interp = run_source('let a = 1\nif true { let b = 2 }')
        self.assertTrue(interp.global_env.has('a'))
        self.assertFalse(interp.global_env.has('b'))


class TestFunctions(unittest.TestCase):
    def test_plain_call(self):
        self.assertEqual(last_result(
            'fn add(a, b) { return a + b }\nadd(2, 3)'), 5)

    def test_default_args(self):
        self.assertEqual(last_result(
            'fn f(a, b = 10) { return a + b }\nf(1)'), 11)
        self.assertEqual(last_result(
            'fn f(a, b = 10) { return a + b }\nf(1, 2)'), 3)

    def test_named_args(self):
        self.assertEqual(last_result(
            'fn f(a, b) { return a * 10 + b }\nf(b: 2, a: 1)'), 12)

    def test_mixed_args(self):
        self.assertEqual(last_result(
            'fn f(a, b) { return a - b }\nf(5, b: 3)'), 2)

    def test_missing_arg_raises(self):
        with self.assertRaises(AuroraError):
            run_source('fn f(a) { return a }\nf()')

    def test_unknown_named_arg_raises(self):
        with self.assertRaises(AuroraError):
            run_source('fn f(a) { return a }\nf(a: 1, z: 2)')

    def test_closure(self):
        interp = run_source(
            'fn counter() { var n = 0; return || { n = n + 1; return n } }\n'
            'let c = counter()\nc()\nc()')
        # 闭包修改捕获变量：环境链共享
        self.assertIsNotNone(interp)

    def test_lambda_higher_order(self):
        self.assertEqual(last_result('[1,2,3].map(|x| x * 2)'), [2, 4, 6])
        self.assertEqual(last_result('[1,2,3,4].filter(|x| x % 2 == 0)'), [2, 4])
        self.assertEqual(last_result('[1,2,3,4].reduce(|a, b| a + b)'), 10)


class TestControlFlow(unittest.TestCase):
    def test_if_elif_else(self):
        interp = run_source(
            'var r = ""\n'
            'if 1 > 2 { r = "a" } elif 2 > 1 { r = "b" } else { r = "c" }')
        self.assertEqual(interp.global_env.get('r'), 'b')

    def test_if_expr_value(self):
        self.assertEqual(last_result('let x = if true { 1 } else { 2 }\nx'), 1)

    def test_for_range(self):
        interp = run_source('var s = 0\nfor i in range(5) { s = s + i }')
        self.assertEqual(interp.global_env.get('s'), 10)

    def test_for_dict(self):
        interp = run_source(
            'var total = 0\nfor k, v in {"a": 1, "b": 2} { total = total + v }')
        self.assertEqual(interp.global_env.get('total'), 3)

    def test_while_break_continue(self):
        interp = run_source(
            'var i = 0\nvar s = 0\n'
            'while true { i = i + 1; if i == 5 { break }; if i == 2 { continue }; s = s + i }')
        self.assertEqual(interp.global_env.get('s'), 1 + 3 + 4)


class TestMatch(unittest.TestCase):
    def test_literal_and_wildcard(self):
        interp = run_source('let r = match 3 { 1 => "one", 3 => "three", _ => "other" }')
        self.assertEqual(interp.global_env.get('r'), 'three')

    def test_bind_pattern(self):
        interp = run_source('let r = match 42 { x => x * 2 }')
        self.assertEqual(interp.global_env.get('r'), 84)


class TestTypesAndEnums(unittest.TestCase):
    def test_type_instantiation_named_args(self):
        interp = run_source('type P { x: float, y: float }\nlet p = P(x: 3.0, y: 4.0)')
        p = interp.global_env.get('p')
        self.assertEqual(p['x'], 3.0)
        self.assertEqual(p['y'], 4.0)

    def test_type_positional_args_and_default(self):
        interp = run_source(
            'type R { w: float = 1.0, h: float = 1.0 }\n'
            'let r = R(2.0)\nlet r2 = R()')
        self.assertEqual(interp.global_env.get('r')['w'], 2.0)
        self.assertEqual(interp.global_env.get('r2')['h'], 1.0)

    def test_impl_method_with_self(self):
        interp = run_source(
            'type P { x: float, y: float }\n'
            'impl P { fn mag2() -> float { return self.x * self.x + self.y * self.y } }\n'
            'let p = P(x: 3.0, y: 4.0)\n'
            'let m = p.mag2()')
        self.assertEqual(interp.global_env.get('m'), 25.0)

    def test_enum_variant(self):
        interp = run_source(
            'enum E { A(a: int), B }\n'
            'let a = E.A(a: 1)\nlet b = E.B()')
        va = interp.global_env.get('a')
        vb = interp.global_env.get('b')
        self.assertIsInstance(va, AuroraEnumVariant)
        self.assertEqual(va.a, 1)
        self.assertEqual(va._name, 'A')
        self.assertNotEqual(va, vb)

    def test_enum_match_binds_fields(self):
        interp = run_source(
            'enum Shape { Circle(radius: float), Rect(w: float, h: float) }\n'
            'fn area(s) -> float {\n'
            '  match s { Circle(r) => 3.14 * r * r, Rect(w, h) => w * h, _ => 0.0 }\n'
            '}\n'
            'let c = Shape.Circle(radius: 2.0)\n'
            'let ac = area(c)\n'
            'let r = Shape.Rect(w: 3.0, h: 4.0)\n'
            'let ar = area(r)')
        self.assertAlmostEqual(interp.global_env.get('ac'), 12.56)
        self.assertEqual(interp.global_env.get('ar'), 12.0)

    def test_match_type_instance(self):
        interp = run_source(
            'type P { x: float, y: float }\n'
            'let p = P(x: 1.0, y: 2.0)\n'
            'let r = match p { P(x, y) => x + y, _ => -1 }')
        self.assertEqual(interp.global_env.get('r'), 3.0)

    def test_trait_default_method(self):
        interp = run_source(
            'trait G { fn greet() -> str\nfn farewell() -> str { return "bye" } }\n'
            'type P { x: float }\n'
            'impl G for P { fn greet() -> str { return "hi" } }\n'
            'let p = P(x: 1.0)\n'
            'let g = p.greet()\n'
            'let f = p.farewell()')
        self.assertEqual(interp.global_env.get('g'), 'hi')
        self.assertEqual(interp.global_env.get('f'), 'bye')


class TestErrorsAndResult(unittest.TestCase):
    def test_try_catch_finally(self):
        interp = run_source(
            'let log = []\n'
            'try { panic("boom") }\n'
            'catch e: str { log.append(e) }\n'
            'finally { log.append("fin") }')
        self.assertEqual(interp.global_env.get('log'), ['[Panic] boom', 'fin'])

    def test_result_and_question(self):
        interp = run_source(
            'from std.result import Ok\n'
            'let r = Ok(42)\n'
            'let v = r?')
        self.assertEqual(interp.global_env.get('v'), 42)

    def test_result_match(self):
        interp = run_source(
            'from std.result import Ok, Err\n'
            'fn check(x) -> Result { if x > 0 { return Ok(x) }; return Err("neg") }\n'
            'let r = match check(5) { Ok(v) => v, Err(e) => -1 }')
        self.assertEqual(interp.global_env.get('r'), 5)


class TestConcurrency(unittest.TestCase):
    def test_channel_send_recv(self):
        interp = run_source(
            'let ch = chan(5)\nch <- 10\nlet v = <-ch')
        self.assertEqual(interp.global_env.get('v'), 10)

    def test_spawn_and_channel(self):
        interp = run_source(
            'fn worker(ch) { ch <- 99 }\n'
            'let ch = chan(1)\n'
            'spawn worker(ch)\n'
            'sleep(200)\n'
            'let v = <-ch')
        self.assertEqual(interp.global_env.get('v'), 99)

    def test_select_default(self):
        interp = run_source(
            'let ch = chan(1)\n'
            'var r = ""\n'
            'select { ch => { r = "got" }, default => { r = "default" } }')
        self.assertEqual(interp.global_env.get('r'), 'default')

    def test_select_ready_channel(self):
        interp = run_source(
            'let ch = chan(1)\nch <- 7\n'
            'var r = ""\n'
            'select { ch => { r = "got" }, default => { r = "default" } }')
        self.assertEqual(interp.global_env.get('r'), 'got')

    def test_select_binding(self):
        interp = run_source(
            'let ch = chan(1)\nch <- 42\n'
            'var r = -1\n'
            'select { v = <-ch => { r = v }, default => { r = -2 } }')
        self.assertEqual(interp.global_env.get('r'), 42)

    def test_channel_close_iteration(self):
        interp = run_source(
            'fn fill(ch) { ch <- 1; ch <- 2; ch.close() }\n'
            'let ch = chan(2)\nspawn fill(ch)\n'
            'let acc = []\n'
            'for v in ch { acc.append(v) }')
        self.assertEqual(interp.global_env.get('acc'), [1, 2])


class TestStrings(unittest.TestCase):
    def test_interpolation_var(self):
        interp = run_source('let name = "aurora"\nlet s = "hi {name}"')
        self.assertEqual(interp.global_env.get('s'), 'hi aurora')

    def test_interpolation_expression(self):
        interp = run_source('let s = "sum={1 + 2 * 3}"')
        self.assertEqual(interp.global_env.get('s'), 'sum=7')

    def test_interpolation_method_call(self):
        interp = run_source('let s = "[1,2].len()={[1, 2].len()}"')
        self.assertEqual(interp.global_env.get('s'), '[1,2].len()=2')

    def test_brace_escape(self):
        interp = run_source('let s = "{{literal}}"')
        self.assertEqual(interp.global_env.get('s'), '{literal}')


class TestImports(unittest.TestCase):
    def test_namespace_access(self):
        interp = run_source('import std.io\nlet v = std.io.exists("/tmp")')
        self.assertTrue(interp.global_env.get('v'))

    def test_leaf_module_alias(self):
        interp = run_source('import std.math as m\nlet v = m.sqrt(16)')
        self.assertEqual(interp.global_env.get('v'), 4.0)

    def test_from_import(self):
        interp = run_source('from std.math import sqrt\nlet v = sqrt(9)')
        self.assertEqual(interp.global_env.get('v'), 3.0)

    def test_from_import_alias(self):
        interp = run_source('from std.math import sqrt as sq\nlet v = sq(25)')
        self.assertEqual(interp.global_env.get('v'), 5.0)


class TestStdlib(unittest.TestCase):
    def test_json(self):
        interp = run_source(
            'import std.json\nlet s = std.json.stringify({"a": 1})')
        self.assertEqual(interp.global_env.get('s'), '{"a": 1}')

    def test_io_write_read(self):
        interp = run_source(
            'import std.io\n'
            'std.io.write_file("/tmp/aurora_test.txt", "hello")\n'
            'let c = std.io.read_file("/tmp/aurora_test.txt")')
        self.assertEqual(interp.global_env.get('c'), 'hello')

    def test_assert_pass(self):
        run_source('assert 1 == 1')

    def test_assert_fail_raises(self):
        with self.assertRaises(AuroraError):
            run_source('assert 1 == 2')

    def test_test_block(self):
        interp = run_source('test "add" { assert 1 + 1 == 2 }')
        self.assertIsNotNone(interp)


if __name__ == '__main__':
    unittest.main()


class TestModernSyntax(unittest.TestCase):
    """ZL 设计落地：可选链 ?.、空合并 ??、// 注释、nil 显示"""

    def test_optional_chain_dict(self):
        self.assertEqual(last_result('{ "a": 1 }?.a'), 1)
        self.assertIsNone(last_result('{ "a": 1 }?.b'))
        self.assertIsNone(last_result('nil?.a'))

    def test_optional_call(self):
        self.assertIsNone(last_result('nil?.len()'))
        self.assertEqual(last_result('[1, 2, 3]?.len()'), 3)

    def test_null_coalesce(self):
        self.assertEqual(last_result('nil ?? 42'), 42)
        self.assertEqual(last_result('0 ?? 42'), 0)
        self.assertEqual(last_result('false ?? 42'), False)
        self.assertEqual(last_result('nil ?? nil ?? 7'), 7)
        self.assertEqual(last_result('"x" ?? "y"'), "x")

    def test_coalesce_with_optional(self):
        src = 'let u = { "name": "A" }\nlet v = u?.name ?? "无名"\nv'
        self.assertEqual(last_result(src), "A")
        src2 = 'let u = nil\nlet v = u?.name ?? "无名"\nv'
        self.assertEqual(last_result(src2), "无名")

    def test_slash_slash_comment(self):
        self.assertEqual(last_result('1 + 2  // 加法\n// 独立注释行\n3'), 3)

    def test_nil_display(self):
        from io import StringIO
        import contextlib
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            run_source('println(nil)')
        self.assertEqual(buf.getvalue(), "nil\n")

    def test_newline_paren_not_call(self):
        # 回归:换行后以 ( 开头的新语句不得被吸进上一表达式当调用参数
        src = 'let s = 1 + 2\n(s * 2)\ns'
        self.assertEqual(last_result(src), 3)
        src2 = 'fn f(a) { let s = a + 1\n (s * s) ** 0.5 }\nf(3)'
        self.assertEqual(last_result(src2), 4.0)
        # 同行紧邻的括号仍是调用:f(2) 之后调用 f 的返回值不成立,但 f(x)(y) 保留
        src3 = 'fn g(x) { let y = x + 1\n (y + 5) }\ng(2)'
        self.assertEqual(last_result(src3), 8)
