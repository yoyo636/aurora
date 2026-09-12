"""语法分析器测试"""

import unittest

from aurora.lexer import Lexer
from aurora.parser import Parser, ParseError
from aurora.ast_nodes import (
    Program, LetStmt, FnDef, IfStmt, ForStmt, WhileStmt, MatchStmt,
    ImportStmt, TraitDef, ImplBlock, TypeDef, EnumDef, CallExpr,
    MethodCall, ChannelRecv, AssignStmt, BinaryOp,
)

from helpers import compile_source


class TestParserStatements(unittest.TestCase):
    def test_program_shape(self):
        prog = compile_source('let x = 1\nfn f() { return 2 }')
        self.assertIsInstance(prog, Program)
        self.assertEqual(len(prog.statements), 2)

    def test_let_variants(self):
        prog = compile_source('let a = 1\nlet b: int = 2\nlet c\nlet mut d = 3')
        stmts = prog.statements
        self.assertTrue(all(isinstance(s, LetStmt) for s in stmts))
        self.assertEqual(stmts[1].type_annotation.name, 'int')
        self.assertIsNone(stmts[2].initializer)

    def test_semicolon_separator(self):
        # 分号可作为语句分隔符
        prog = compile_source('let a = 1; let b = 2; println(a + b);')
        self.assertEqual(len(prog.statements), 3)

    def test_assignment_ops(self):
        prog = compile_source('let x = 1\nx += 2\nx *= 3')
        self.assertIsInstance(prog.statements[1], AssignStmt)
        self.assertEqual(prog.statements[1].op, '+=')

    def test_control_flow(self):
        prog = compile_source('if a { b() } elif c { d() } else { e() }')
        self.assertIsInstance(prog.statements[0], IfStmt)
        prog = compile_source('for i in range(3) { println(i) }')
        self.assertIsInstance(prog.statements[0], ForStmt)
        prog = compile_source('while x < 10 { x = x + 1 }')
        self.assertIsInstance(prog.statements[0], WhileStmt)

    def test_match_stmt(self):
        prog = compile_source('match x { 1 => a(), _ => b() }')
        self.assertIsInstance(prog.statements[0], MatchStmt)

    def test_fn_def(self):
        prog = compile_source('fn add(a: int, b: int = 1) -> int { return a + b }')
        fn = prog.statements[0]
        self.assertIsInstance(fn, FnDef)
        self.assertEqual(fn.name, 'add')
        self.assertEqual(len(fn.params), 2)
        self.assertIsNotNone(fn.params[1].default_value)


class TestParserNewFeatures(unittest.TestCase):
    def test_named_args(self):
        prog = compile_source('f(x: 1, y: 2)')
        call = prog.statements[0].expr
        self.assertIsInstance(call, CallExpr)
        self.assertEqual([name for name, _ in call.named_args], ['x', 'y'])

    def test_mixed_args(self):
        prog = compile_source('f(1, y: 2)')
        call = prog.statements[0].expr
        self.assertEqual(len(call.args), 1)
        self.assertEqual(call.named_args[0][0], 'y')

    def test_method_named_args(self):
        prog = compile_source('obj.m(a: 1)')
        call = prog.statements[0].expr
        self.assertIsInstance(call, MethodCall)
        self.assertEqual(call.named_args[0][0], 'a')

    def test_prefix_channel_recv(self):
        prog = compile_source('let v = <-ch')
        expr = prog.statements[0].initializer
        self.assertIsInstance(expr, ChannelRecv)

    def test_trait_declaration_without_body(self):
        prog = compile_source('trait T { fn a() -> int\nfn b() -> int {} }')
        trait = prog.statements[0]
        self.assertIsInstance(trait, TraitDef)
        self.assertIsNone(trait.methods[0].body)   # 纯声明
        self.assertIsNotNone(trait.methods[1].body)  # 默认实现

    def test_import_as(self):
        prog = compile_source('import std.math as m\nfrom std.result import Ok as R')
        self.assertIsInstance(prog.statements[0], ImportStmt)
        self.assertEqual(prog.statements[0].alias, 'm')
        self.assertEqual(prog.statements[1].names, ['Ok'])
        self.assertEqual(prog.statements[1].alias, 'R')

    def test_type_enum_impl(self):
        prog = compile_source(
            'type P { x: float }\n'
            'enum E { A(a: int), B }\n'
            'impl P { fn get() -> float { return self.x } }')
        self.assertIsInstance(prog.statements[0], TypeDef)
        self.assertIsInstance(prog.statements[1], EnumDef)
        self.assertIsInstance(prog.statements[2], ImplBlock)

    def test_expression_precedence(self):
        prog = compile_source('1 + 2 * 3')
        expr = prog.statements[0].expr
        self.assertIsInstance(expr, BinaryOp)
        self.assertEqual(expr.op, '+')
        self.assertIsInstance(expr.right, BinaryOp)
        self.assertEqual(expr.right.op, '*')

    def test_parse_errors(self):
        with self.assertRaises(ParseError):
            compile_source('let = 3')
        with self.assertRaises(ParseError):
            compile_source('fn { }')


if __name__ == '__main__':
    unittest.main()
