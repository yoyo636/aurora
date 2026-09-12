"""所有权与借用检查器测试"""

import unittest

from aurora.ownership import OwnershipChecker
from helpers import compile_source


def errors(src):
    program = compile_source(src)
    return OwnershipChecker().check(program)


class TestOwnership(unittest.TestCase):
    def test_clean_program(self):
        src = 'let x = 1\nlet y = 2\nfn f() { let z = x + y; return z }'
        self.assertEqual(errors(src), [])

    def test_mutate_immutable(self):
        src = 'const X = 5\nX = 10'
        errs = errors(src)
        self.assertTrue(any('不能修改不可变变量' in str(e) for e in errs))

    def test_mut_ref_on_immutable(self):
        src = 'const X = 5\nlet r = &mut X'
        errs = errors(src)
        self.assertTrue(any('不能对不可变变量' in str(e) for e in errs))

    def test_borrow_conflict(self):
        src = 'let mut y = 1\nlet r1 = &y\nlet r2 = &mut y'
        errs = errors(src)
        self.assertTrue(any('存在不可变借用' in str(e) for e in errs))

    def test_assign_while_borrowed(self):
        src = 'let mut y = 1\nlet r = &y\ny = 2'
        errs = errors(src)
        self.assertTrue(any('存在不可变借用' in str(e) for e in errs))

    def test_many_immutable_borrows_ok(self):
        src = 'let y = 1\nlet a = &y\nlet b = &y\nlet c = y + 1'
        self.assertEqual(errors(src), [])

    def test_trait_method_without_body_ok(self):
        src = ('trait T { fn a() -> int }\n'
               'type P { x: int }\n'
               'impl T for P { fn a() -> int { return 1 } }')
        self.assertEqual(errors(src), [])

    def test_error_position(self):
        src = 'const X = 5\nX = 10'
        errs = errors(src)
        self.assertGreater(errs[0].node.line, 0)


if __name__ == '__main__':
    unittest.main()
