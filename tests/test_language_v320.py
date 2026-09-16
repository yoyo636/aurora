"""v3.2.0 语言级简洁性增强测试：属性简写、展开运算符、字典解构、解构默认值、自动导入"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.lexer import Lexer
from aurora.parser import Parser
from aurora.interpreter import Interpreter
from aurora.ast_nodes import SpreadExpr, BindPattern, StructPattern
import unittest


def run(src):
    """编译并执行 Aurora 源码，返回解释器实例"""
    prog = Parser(Lexer(src).tokenize()).parse()
    interp = Interpreter()
    interp.run(prog)
    return interp


class TestPropertyShorthand(unittest.TestCase):
    """属性简写：User { name, age } 等价于 User { name: name, age: age }"""

    def test_struct_shorthand(self):
        src = """
        struct Point { x: int, y: int }
        let x = 10
        let y = 20
        let p = Point { x, y }
        println(p.x)
        println(p.y)
        """
        interp = run(src)
        p = interp.global_env.get('p')
        self.assertEqual(p['x'], 10)
        self.assertEqual(p['y'], 20)

    def test_struct_mixed_shorthand_and_explicit(self):
        src = """
        struct User { name: str, age: int, active: bool }
        let name = "Alice"
        let age = 30
        let u = User { name, age, active: true }
        println(u.name)
        """
        interp = run(src)
        u = interp.global_env.get('u')
        self.assertEqual(u['name'], "Alice")
        self.assertEqual(u['active'], True)


class TestSpreadOperator(unittest.TestCase):
    """展开运算符：[...arr, 4]、{...obj, b: 2}"""

    def test_array_spread(self):
        src = """
        let a = [1, 2, 3]
        let b = [...a, 4, 5]
        println(b)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('b'), [1, 2, 3, 4, 5])

    def test_array_spread_at_start(self):
        src = """
        let a = [1, 2]
        let b = [...a]
        println(b)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('b'), [1, 2])

    def test_array_spread_multiple(self):
        src = """
        let a = [1, 2]
        let c = [3, 4]
        let d = [...a, ...c, 5]
        println(d)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('d'), [1, 2, 3, 4, 5])

    def test_map_spread(self):
        src = """
        let a = {"x": 1, "y": 2}
        let b = {...a, "z": 3}
        println(b)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('b'), {"x": 1, "y": 2, "z": 3})

    def test_map_spread_override(self):
        src = """
        let a = {"x": 1, "y": 2}
        let b = {...a, "x": 10}
        println(b)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('b'), {"x": 10, "y": 2})

    def test_spread_ast_node(self):
        """验证 SpreadExpr AST 节点被正确创建"""
        src = "let b = [...a, 4]"
        prog = Parser(Lexer(src).tokenize()).parse()
        # 找到 ArrayLiteral
        from aurora.ast_nodes import LetStmt, ArrayLiteral
        for stmt in prog.statements:
            if isinstance(stmt, LetStmt) and isinstance(stmt.initializer, ArrayLiteral):
                self.assertIsInstance(stmt.initializer.elements[0], SpreadExpr)
                break
        else:
            self.fail("未找到 ArrayLiteral")


class TestDictDestructuring(unittest.TestCase):
    """字典解构：let { name, age } = user"""

    def test_basic_dict_destructuring(self):
        src = """
        let user = {"name": "Alice", "age": 30}
        let {name, age} = user
        println(name)
        println(age)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('name'), "Alice")
        self.assertEqual(interp.global_env.get('age'), 30)

    def test_dict_destructuring_renamed(self):
        src = """
        let user = {"name": "Bob", "age": 25}
        let {name: username, age: userage} = user
        println(username)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('username'), "Bob")


class TestDestructuringDefaults(unittest.TestCase):
    """解构默认值：let { name = "Unknown", age = 0 } = user"""

    def test_default_when_key_missing(self):
        src = """
        let user = {"name": "Charlie"}
        let {name, age = 18} = user
        println(name)
        println(age)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('name'), "Charlie")
        self.assertEqual(interp.global_env.get('age'), 18)

    def test_default_not_used_when_key_exists(self):
        src = """
        let user = {"name": "Dave", "age": 40}
        let {name = "Unknown", age = 0} = user
        println(name)
        println(age)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('name'), "Dave")
        self.assertEqual(interp.global_env.get('age'), 40)

    def test_default_expression(self):
        src = """
        let default_age = 21
        let user = {"name": "Eve"}
        let {name, age = default_age} = user
        println(age)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('age'), 21)


class TestAutoImport(unittest.TestCase):
    """自动导入：常用模块无需手动 import"""

    def test_math_auto_import(self):
        src = """
        println(math.abs(-5))
        println(math.sqrt(16))
        """
        interp = run(src)
        # 不报错即通过

    def test_io_auto_import(self):
        src = """
        let result = io.exists("nonexistent_file_xyz.aur")
        println(result)
        """
        interp = run(src)
        self.assertFalse(interp.global_env.get('result'))

    def test_proc_auto_import(self):
        """std.proc 自动导入，可通过 proc 快捷名访问"""
        src = """
        let result = proc.run("echo hello")
        println(result)
        """
        interp = run(src)
        # 不报错即通过（proc.run 执行 echo hello）

    def test_multiple_auto_imports(self):
        """多个自动导入模块同时可用"""
        src = """
        let abs_val = math.abs(-42)
        let now = time.now()
        println(abs_val)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('abs_val'), 42)


class TestOptionalChaining(unittest.TestCase):
    """可选链（已有功能，确认完善）"""

    def test_optional_chaining_nil(self):
        src = """
        let obj = nil
        let result = obj?.prop
        println(result)
        """
        interp = run(src)
        self.assertIsNone(interp.global_env.get('result'))

    def test_nullish_coalescing(self):
        src = """
        let a = nil
        let b = a ?? "default"
        println(b)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('b'), "default")

    def test_nullish_coalescing_with_value(self):
        src = """
        let a = "hello"
        let b = a ?? "default"
        println(b)
        """
        interp = run(src)
        self.assertEqual(interp.global_env.get('b'), "hello")


if __name__ == '__main__':
    unittest.main()
