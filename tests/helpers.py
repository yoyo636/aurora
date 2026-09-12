"""测试公共工具：源码编译 + 执行 + 检查"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.lexer import Lexer, LexerError      # noqa: E402
from aurora.parser import Parser, ParseError     # noqa: E402
from aurora.interpreter import Interpreter       # noqa: E402
from aurora.type_checker import TypeChecker      # noqa: E402
from aurora.ownership import OwnershipChecker    # noqa: E402


def compile_source(src):
    """源码 → Program"""
    return Parser(Lexer(src).tokenize()).parse()


def run_source(src, strict=False):
    """编译并执行源码，返回解释器实例"""
    program = compile_source(src)
    if strict:
        tcs = TypeChecker().check(program)
        if tcs:
            raise AssertionError(f"类型错误: {tcs}")
        ocs = OwnershipChecker().check(program)
        if ocs:
            raise AssertionError(f"所有权错误: {ocs}")
    interp = Interpreter()
    interp.run(program)
    return interp


def eval_expr(src):
    """求值一个表达式，返回结果"""
    program = compile_source(src)
    interp = Interpreter()
    interp.run(program)
    # 取最后一条表达式语句的结果
    for stmt in reversed(program.statements):
        from aurora.ast_nodes import ExprStmt
        if isinstance(stmt, ExprStmt):
            return interp._eval(stmt.expr, interp.global_env)
    return None
