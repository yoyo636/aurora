"""ZL 设计落地回归测试:let/var、管道、区间、解构、defer、yield"""

import unittest

from helpers import run_source, eval_expr
from aurora.stdlib import AuroraError


def last_result(src):
    """执行源码,返回最后一个表达式语句的值"""
    return eval_expr(src)


def expect_error(src, kind, fragment=None):
    """断言源码执行抛指定类型的 AuroraError"""
    try:
        run_source(src)
    except AuroraError as e:
        if e.kind != kind:
            raise AssertionError(f"期望 {kind},实际 {e.kind}: {e}")
        if fragment and fragment not in str(e):
            raise AssertionError(f"错误消息不含 {fragment!r}: {e}")
        return
    raise AssertionError(f"期望 {kind} 错误,但未抛出")


class TestLetVarSemantics(unittest.TestCase):
    def test_let_immutable(self):
        # let 绑定不可变,赋值报错
        expect_error(
            'let x = 1\nx = 2',
            'TypeError', '不可变绑定')

    def test_var_mutable(self):
        self.assertEqual(
            last_result('var x = 1\nx = x + 5\nx'), 6)

    def test_let_mut_explicit(self):
        self.assertEqual(
            last_result('let mut y = 1\ny = y + 1\ny'), 2)

    def test_compound_assign_on_let_fails(self):
        expect_error('let a = 10\na += 1', 'TypeError', '不可变绑定')


class TestPipe(unittest.TestCase):
    def test_pipe_into_function(self):
        src = 'fn double(x) { x * 2 }\n5 |> double'
        self.assertEqual(last_result(src), 10)

    def test_pipe_as_last_arg(self):
        src = 'fn add(a, b) { a + b }\n5 |> add(3)'
        self.assertEqual(last_result(src), 8)

    def test_pipe_chain(self):
        src = 'fn inc(x) { x + 1 }\nfn dbl(x) { x * 2 }\n5 |> inc |> dbl'
        self.assertEqual(last_result(src), 12)

    def test_pipe_builtin(self):
        self.assertEqual(last_result('[1, 2, 3] |> len'), 3)
        self.assertEqual(last_result('[3, 1, 2] |> sorted'), [1, 2, 3])

    def test_pipe_into_named_args_fn(self):
        # 左侧值作为最后一个位置参数;具名参数不受影响
        src = 'fn draw(w, h, color) { w + h + color }\n5 |> draw(3, color: 2)'
        self.assertEqual(last_result(src), 10)


class TestRange(unittest.TestCase):
    def test_range_inclusive(self):
        self.assertEqual(last_result('1..5'), [1, 2, 3, 4, 5])

    def test_range_variable(self):
        self.assertEqual(last_result('let n = 3\n1..n'), [1, 2, 3])

    def test_range_in_for(self):
        src = 'var s = 0\nfor i in 2..4 { s = s + i }\ns'
        self.assertEqual(last_result(src), 9)

    def test_range_in_pipe(self):
        self.assertEqual(last_result('1..3 |> len'), 3)


class TestDestructure(unittest.TestCase):
    def test_tuple(self):
        self.assertEqual(last_result('let (a, b) = (1, "x")\na + 1'), 2)
        self.assertEqual(last_result('let (a, b) = (1, "x")\nb'), "x")

    def test_list(self):
        self.assertEqual(
            last_result('let [x, y, z] = [7, 8, 9]\nx + y + z'), 24)

    def test_dict_keys(self):
        src = 'let p = {"name": "Aurora", "ver": "0.3"}\nlet (name, ver) = p\nname'
        self.assertEqual(last_result(src), "Aurora")

    def test_short_values_error(self):
        expect_error('let (a, b) = [1]', 'ValueError')

    def test_missing_dict_key(self):
        expect_error('let (a, b) = {"a": 1}', 'KeyError')


class TestDefer(unittest.TestCase):
    def test_lifo_order(self):
        from io import StringIO
        import contextlib
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            run_source(
                'fn f() { defer println("A")\n defer println("B")\n println("run") }\nf()')
        self.assertEqual(buf.getvalue(), "run\nB\nA\n")

    def test_defer_with_return(self):
        from io import StringIO
        import contextlib
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            interp = run_source(
                'fn f() { defer { println("c") }\n return 1 }\nlet r = f()')
        self.assertEqual(buf.getvalue(), "c\n")
        self.assertEqual(interp.global_env.get('r'), 1)

    def test_defer_captures_args_at_registration(self):
        from io import StringIO
        import contextlib
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            run_source(
                'fn f() {\n for i in 1..3 { defer println("clean-" + str(i)) }\n println("run")\n}\nf()')
        self.assertEqual(buf.getvalue(), "run\nclean-3\nclean-2\nclean-1\n")

    def test_defer_in_if(self):
        from io import StringIO
        import contextlib
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            run_source('fn f() { if true { defer println("d") }\n println("b") }\nf()')
        self.assertEqual(buf.getvalue(), "b\nd\n")


class TestYield(unittest.TestCase):
    def test_generator_collect(self):
        src = 'fn squares(n) { for i in 1..n { yield i * i } }\nsquares(4)'
        self.assertEqual(last_result(src), [1, 4, 9, 16])

    def test_yield_then_return(self):
        self.assertEqual(last_result('fn f() { yield 1\n yield 2\n return 99 }\nf()'),
                         [1, 2])

    def test_yield_in_lambda(self):
        self.assertEqual(
            last_result('let g = || { yield 5\n yield 6 }\ng()'), [5, 6])


if __name__ == '__main__':
    unittest.main()
