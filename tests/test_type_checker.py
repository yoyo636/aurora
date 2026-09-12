"""类型检查器测试"""

import unittest

from aurora.type_checker import TypeChecker
from helpers import compile_source


def errors(src):
    program = compile_source(src)
    return TypeChecker().check(program)


class TestTypeChecker(unittest.TestCase):
    def test_clean_program(self):
        self.assertEqual(errors('let x: int = 1\nfn f(a: int) -> int { return a }'), [])

    def test_type_mismatch(self):
        errs = errors('let x: int = "hello"')
        self.assertEqual(len(errs), 1)
        self.assertIn('类型不匹配', str(errs[0]))

    def test_let_without_type_or_value(self):
        errs = errors('let x')
        self.assertEqual(len(errs), 1)

    def test_if_condition_type(self):
        errs = errors('if 42 { println(1) }')
        self.assertTrue(errs)

    def test_impl_unknown_type(self):
        errs = errors('impl Foo { fn a() {} }')
        self.assertTrue(any('未定义的类型' in str(e) for e in errs))

    def test_impl_missing_trait_method(self):
        src = ('trait T { fn a() -> int\nfn b() -> int }\n'
               'type P { x: int }\n'
               'impl T for P { fn a() -> int { return 1 } }')
        errs = errors(src)
        self.assertTrue(any('未实现 trait' in str(e) for e in errs))

    def test_trait_default_not_required(self):
        src = ('trait T { fn a() -> int\nfn b() -> int { return 2 } }\n'
               'type P { x: int }\n'
               'impl T for P { fn a() -> int { return 1 } }')
        self.assertEqual(errors(src), [])

    def test_error_position(self):
        errs = errors('let x: int = "hello"')
        self.assertGreater(errs[0].node.line, 0)

    def test_unknown_identifier_lenient(self):
        # 宽松模式：未定义变量推断为 any，不报错
        self.assertEqual(errors('let y = undefined_var + 1'), [])


if __name__ == '__main__':
    unittest.main()
