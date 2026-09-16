"""
Aurora 原生编译器 — 代码生成器(AST → C)
将 Aurora AST 转换为 C 代码,然后由 gcc/clang 编译为原生机器码。
支持类型特化:纯 int 函数直接编译为 int64_t,性能接近 C。
"""
import os
from .ast_nodes import *
from .type_infer import infer_program_types, is_pure_int_function, TypeKind


class CodeGenerator:
    """Aurora AST → C 代码生成器"""

    def __init__(self):
        self.output = []        # 生成的 C 代码行
        self.indent_level = 0   # 当前缩进级别
        self.temp_counter = 0   # 临时变量计数器
        self.functions = []     # 函数名集合(用于检测内置函数)
        self.imports = set()    # 需要的 C include
        self.has_main = False   # 是否有 main 函数
        self.string_literals = []  # 字符串字面量(避免重复)
        self.in_function = False  # 是否在函数体内
        self.function_types = {}  # 类型推断结果
        self.current_fn_type = None  # 当前函数的类型信息
        self.current_fn_pure_int = False  # 当前函数是否是纯 int 函数
        self.current_fn_name = None  # 当前函数名
        self._current_fn_memoized = False  # 当前函数是否启用记忆化
        self._memo_param_name = None  # 记忆化的参数名
        self.variable_types = {}  # 当前函数的变量类型 {name: InferType}
        self._program_statements = []  # 程序语句列表(用于编译期求值)

    # ============================================================
    # 工具方法
    # ============================================================
    def emit(self, code=""):
        """输出一行 C 代码"""
        if code:
            self.output.append("    " * self.indent_level + code)
        else:
            self.output.append("")

    def emit_raw(self, code):
        """输出原始代码(不缩进)"""
        self.output.append(code)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    def new_temp(self, prefix="_t"):
        """生成一个新的临时变量名"""
        self.temp_counter += 1
        return f"{prefix}{self.temp_counter}"

    def c_ident(self, name):
        """将 Aurora 标识符转换为合法的 C 标识符"""
        keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
            'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
            'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            '_Alignas', '_Alignof', '_Atomic', '_Bool', '_Complex',
            '_Generic', '_Imaginary', '_Noreturn', '_Static_assert',
            '_Thread_local', 'main',
        }
        if name in keywords or name.startswith('au_'):
            return f"aurora_{name}"
        # 替换特殊字符
        result = name.replace('?', '_q').replace('!', '_b').replace('-', '_')
        return result

    def c_string_literal(self, s):
        """生成 C 字符串字面量,处理转义"""
        escaped = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')
        return f'"{escaped}"'

    def _infer_expr_type(self, expr: Expr):
        """在代码生成时推断表达式类型(简化版)"""
        from .type_infer import TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TYPE_STRING, TYPE_NIL, TYPE_UNKNOWN

        if isinstance(expr, IntLiteral):
            return TYPE_INT
        elif isinstance(expr, FloatLiteral):
            return TYPE_FLOAT
        elif isinstance(expr, BoolLiteral):
            return TYPE_BOOL
        elif isinstance(expr, StringLiteral):
            return TYPE_STRING
        elif isinstance(expr, NilLiteral):
            return TYPE_NIL
        elif isinstance(expr, Identifier):
            return self.variable_types.get(expr.name, TYPE_UNKNOWN)
        elif isinstance(expr, BinaryOp):
            if expr.op in ('==', '!=', '<', '<=', '>', '>=', '&&', '||'):
                return TYPE_BOOL
            left_type = self._infer_expr_type(expr.left)
            right_type = self._infer_expr_type(expr.right)
            if left_type.is_int() and right_type.is_int():
                return TYPE_INT
            if left_type.is_numeric() and right_type.is_numeric():
                return TYPE_FLOAT
            if left_type.is_string() or right_type.is_string():
                return TYPE_STRING
            return TYPE_UNKNOWN
        elif isinstance(expr, UnaryOp):
            if expr.op == '!':
                return TYPE_BOOL
            if expr.op == '#':
                return TYPE_INT
            return self._infer_expr_type(expr.operand)
        elif isinstance(expr, CallExpr):
            if isinstance(expr.callee, Identifier):
                func_name = expr.callee.name
                if func_name in self.function_types:
                    return self.function_types[func_name].get('return', TYPE_UNKNOWN)
                if func_name in ('len', 'now_ms', 'floor', 'ceil', 'round', 'min', 'max', 'gcd', 'lcm', 'factorial', 'fibonacci'):
                    return TYPE_INT
                if func_name in ('sqrt', 'sin', 'cos', 'tan', 'log', 'exp'):
                    return TYPE_FLOAT
                if func_name in ('is_prime', 'file_exists'):
                    return TYPE_BOOL
            return TYPE_UNKNOWN
        return TYPE_UNKNOWN

    # ============================================================
    # 程序生成
    # ============================================================
    def generate(self, program: Program) -> str:
        """生成完整的 C 程序"""
        self.output = []
        self.indent_level = 0

        # 运行类型推断器
        self.function_types = infer_program_types(program)
        self._program_statements = program.statements

        # 分离函数定义和顶层语句
        fn_defs = []
        top_level_stmts = []
        for stmt in program.statements:
            if isinstance(stmt, FnDef):
                fn_defs.append(stmt)
                if stmt.name == "main":
                    self.has_main = True
            elif isinstance(stmt, (TypeDef, EnumDef, TraitDef, ImplBlock, ImportStmt, TestBlock)):
                pass  # 忽略
            else:
                top_level_stmts.append(stmt)

        # 头文件
        self.emit_raw('#include "aurora_rt.h"')
        self.emit_raw('#include <stdio.h>')
        self.emit_raw('#include <stdlib.h>')
        self.emit_raw('#include <string.h>')
        self.emit_raw('#include <stdint.h>')
        self.emit_raw('')

        # 前向声明所有函数
        for stmt in fn_defs:
            fn_type = self.function_types.get(stmt.name, {})
            pure_int = is_pure_int_function(fn_type) if fn_type else False
            if pure_int:
                params = ", ".join(["int64_t"] * len(stmt.params)) if stmt.params else "void"
                self.emit_raw(f"int64_t {self.c_ident(stmt.name)}({params});")
            else:
                params = ", ".join(["AuValue"] * len(stmt.params)) if stmt.params else "void"
                self.emit_raw(f"AuValue {self.c_ident(stmt.name)}({params});")
        if top_level_stmts:
            self.emit_raw('void _aurora_top_level(void);')
        self.emit_raw('')

        # 生成所有函数定义
        for stmt in fn_defs:
            self.gen_stmt(stmt)
            self.emit('')

        # 生成顶层语句包装函数
        if top_level_stmts:
            self.emit_raw('void _aurora_top_level(void) {')
            self.indent()
            self.in_function = True
            self.current_fn_pure_int = False
            self.current_fn_name = "_aurora_top_level"
            self.variable_types = {}
            for stmt in top_level_stmts:
                self.gen_stmt(stmt)
            self.in_function = False
            self.current_fn_name = None
            self.variable_types = {}
            self.dedent()
            self.emit_raw('}')
            self.emit_raw('')

        # 生成 C 的 main 入口
        self.emit_raw('int main(int argc, char** argv) {')
        self.emit_raw('    au_runtime_init();')
        if self.has_main:
            self.emit_raw('    AuValue _result = aurora_main();')
            self.emit_raw('    (void)_result;')
        if top_level_stmts:
            self.emit_raw('    _aurora_top_level();')
        self.emit_raw('    au_runtime_shutdown();')
        self.emit_raw('    return 0;')
        self.emit_raw('}')

        return "\n".join(self.output)

    # ============================================================
    # 语句生成
    # ============================================================
    def gen_stmt(self, stmt: Stmt):
        """生成语句"""
        if isinstance(stmt, FnDef):
            self.gen_fn_def(stmt)
        elif isinstance(stmt, LetStmt):
            self.gen_let_stmt(stmt)
        elif isinstance(stmt, ConstStmt):
            self.gen_const_stmt(stmt)
        elif isinstance(stmt, AssignStmt):
            self.gen_assign_stmt(stmt)
        elif isinstance(stmt, IfStmt):
            self.gen_if_stmt(stmt)
        elif isinstance(stmt, ForStmt):
            self.gen_for_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            self.gen_while_stmt(stmt)
        elif isinstance(stmt, ReturnStmt):
            self.gen_return_stmt(stmt)
        elif isinstance(stmt, ExprStmt):
            self.gen_expr_stmt(stmt)
        elif isinstance(stmt, BreakStmt):
            self.emit("break;")
        elif isinstance(stmt, ContinueStmt):
            self.emit("continue;")
        elif isinstance(stmt, Block):
            self.gen_block(stmt)
        elif isinstance(stmt, TypeDef) or isinstance(stmt, EnumDef) or isinstance(stmt, TraitDef) or isinstance(stmt, ImplBlock):
            # 类型定义在动态类型版本中暂时忽略(运行时处理)
            pass
        elif isinstance(stmt, ImportStmt):
            # 导入在编译期处理,这里忽略
            pass
        elif isinstance(stmt, TestBlock):
            # 测试块暂时忽略
            pass
        else:
            self.emit(f"/* TODO: {type(stmt).__name__} */")

    def gen_block(self, block: Block):
        """生成代码块"""
        self.emit("{")
        self.indent()
        for stmt in block.statements:
            self.gen_stmt(stmt)
        self.dedent()
        self.emit("}")

    def _is_recursive_function(self, fn: FnDef) -> bool:
        """检测函数是否递归(函数体内调用自身)"""
        def check_expr(expr):
            if isinstance(expr, CallExpr):
                if isinstance(expr.callee, Identifier) and expr.callee.name == fn.name:
                    return True
                for arg in expr.args:
                    if check_expr(arg):
                        return True
            elif isinstance(expr, BinaryOp):
                return check_expr(expr.left) or check_expr(expr.right)
            elif isinstance(expr, UnaryOp):
                return check_expr(expr.operand)
            elif isinstance(expr, IfExpr):
                if check_expr(expr.condition):
                    return True
                if expr.then_body:
                    for s in expr.then_body.statements:
                        if check_stmt(s):
                            return True
                if expr.else_body:
                    for s in expr.else_body.statements:
                        if check_stmt(s):
                            return True
            elif isinstance(expr, MethodCall):
                if check_expr(expr.object):
                    return True
                for arg in expr.args:
                    if check_expr(arg):
                        return True
            elif isinstance(expr, IndexAccess):
                return check_expr(expr.object) or check_expr(expr.index)
            return False

        def check_stmt(stmt):
            if isinstance(stmt, ReturnStmt) and stmt.value:
                return check_expr(stmt.value)
            elif isinstance(stmt, IfStmt):
                if check_expr(stmt.condition):
                    return True
                if stmt.then_body:
                    for s in stmt.then_body.statements:
                        if check_stmt(s):
                            return True
                for cond, body in stmt.elif_clauses:
                    if check_expr(cond):
                        return True
                    if body:
                        for s in body.statements:
                            if check_stmt(s):
                                return True
                if stmt.else_body:
                    for s in stmt.else_body.statements:
                        if check_stmt(s):
                            return True
            elif isinstance(stmt, ExprStmt):
                return check_expr(stmt.expr)
            elif isinstance(stmt, LetStmt) and stmt.initializer:
                return check_expr(stmt.initializer)
            elif isinstance(stmt, AssignStmt):
                return check_expr(stmt.value)
            elif isinstance(stmt, ForStmt):
                if check_expr(stmt.iterable):
                    return True
                if stmt.body:
                    for s in stmt.body.statements:
                        if check_stmt(s):
                            return True
            elif isinstance(stmt, WhileStmt):
                if check_expr(stmt.condition):
                    return True
                if stmt.body:
                    for s in stmt.body.statements:
                        if check_stmt(s):
                            return True
            return False

        if fn.body:
            for stmt in fn.body.statements:
                if check_stmt(stmt):
                    return True
        return False

    def gen_fn_def(self, fn: FnDef):
        """生成函数定义(支持类型特化和自动记忆化)"""
        if fn.name == "main":
            self.has_main = True

        # 获取函数类型信息
        fn_type = self.function_types.get(fn.name, {})
        self.current_fn_type = fn_type
        self.current_fn_name = fn.name
        self.current_fn_pure_int = is_pure_int_function(fn_type) if fn_type else False

        # 检测是否需要自动记忆化(递归纯int单参数函数)
        self._current_fn_memoized = False
        self._memo_param_name = None
        if (self.current_fn_pure_int and len(fn.params) == 1 and
            self._is_recursive_function(fn)):
            self._current_fn_memoized = True
            self._memo_param_name = fn.params[0].name

        # 收集变量类型
        self.variable_types = {}
        if fn_type and 'params' in fn_type:
            for i, param in enumerate(fn.params):
                if i < len(fn_type['params']):
                    self.variable_types[param.name] = fn_type['params'][i]

        self.in_function = True

        if self.current_fn_pure_int:
            # 纯 int 函数:生成 int64_t 版本
            params = ", ".join([f"int64_t {self.c_ident(p.name)}" for p in fn.params])
            if not params:
                params = "void"
            self.emit(f"int64_t {self.c_ident(fn.name)}({params}) {{")
        else:
            # 普通函数:生成 AuValue 版本
            params = ", ".join([f"AuValue {self.c_ident(p.name)}" for p in fn.params])
            if not params:
                params = "void"
            self.emit(f"AuValue {self.c_ident(fn.name)}({params}) {{")

        self.indent()

        # 自动记忆化:静态缓存声明和查找
        if self._current_fn_memoized:
            memo_name = f"_memo_{self.c_ident(fn.name)}"
            self.emit(f"static int64_t {memo_name}_cache[100000];")
            self.emit(f"static int8_t {memo_name}_valid[100000];")
            param_c = self.c_ident(self._memo_param_name)
            self.emit(f"if ({param_c} >= 0 && {param_c} < 100000 && {memo_name}_valid[{param_c}]) {{")
            self.indent()
            self.emit(f"return {memo_name}_cache[{param_c}];")
            self.dedent()
            self.emit("}")

        # 函数体
        if fn.body:
            for stmt in fn.body.statements:
                self.gen_stmt(stmt)

        # 如果函数体最后一个语句不是 return,添加默认 return
        if fn.body and fn.body.statements:
            last = fn.body.statements[-1]
            if not isinstance(last, ReturnStmt):
                if self.current_fn_pure_int:
                    self.emit("return 0;")
                else:
                    self.emit("return AU_NIL_VAL();")
        else:
            if self.current_fn_pure_int:
                self.emit("return 0;")
            else:
                self.emit("return AU_NIL_VAL();")

        self.dedent()
        self.emit("}")
        self.emit("")
        self.in_function = False
        self.current_fn_pure_int = False
        self.current_fn_name = None
        self._current_fn_memoized = False
        self._memo_param_name = None
        self.variable_types = {}

    def gen_let_stmt(self, stmt: LetStmt):
        """生成 let/var 声明(支持类型特化)"""
        name = self.c_ident(stmt.name)

        # 推断变量类型
        var_type = None
        if stmt.initializer:
            var_type = self._infer_expr_type(stmt.initializer)

        if self.current_fn_pure_int and var_type and var_type.is_int():
            # 纯 int 函数中的 int 变量
            self.variable_types[stmt.name] = var_type
            if stmt.initializer:
                expr_code = self.gen_expr(stmt.initializer)
                self.emit(f"int64_t {name} = {expr_code};")
            else:
                self.emit(f"int64_t {name} = 0;")
        else:
            # 普通变量
            if stmt.initializer:
                expr_code = self.gen_expr(stmt.initializer)
                self.emit(f"AuValue {name} = {expr_code};")
            else:
                self.emit(f"AuValue {name} = AU_NIL_VAL();")

    def gen_const_stmt(self, stmt: ConstStmt):
        """生成 const 声明(let 的不可变版本)"""
        name = self.c_ident(stmt.name)
        if stmt.initializer:
            expr_code = self.gen_expr(stmt.initializer)
            self.emit(f"const AuValue {name} = {expr_code};")
        else:
            self.emit(f"const AuValue {name} = AU_NIL_VAL();")

    def gen_assign_stmt(self, stmt: AssignStmt):
        """生成赋值语句"""
        target = self.gen_expr(stmt.target)
        value = self.gen_expr(stmt.value)

        if stmt.op == "=":
            # 简单赋值
            if isinstance(stmt.target, Identifier):
                self.emit(f"{target} = {value};")
            elif isinstance(stmt.target, IndexAccess):
                # 数组/Map 索引赋值
                obj = self.gen_expr(stmt.target.object)
                idx = self.gen_expr(stmt.target.index)
                temp = self.new_temp()
                self.emit(f"AuValue {temp}_obj = {obj};")
                self.emit(f"AuValue {temp}_idx = {idx};")
                self.emit(f"AuValue {temp}_val = {value};")
                self.emit(f"if ({temp}_obj.type == AU_ARRAY) {{ au_array_set({temp}_obj.as.arr, {temp}_idx.as.i, {temp}_val); }}")
                self.emit(f"else if ({temp}_obj.type == AU_MAP && {temp}_idx.type == AU_STRING) {{ au_map_set({temp}_obj.as.map, {temp}_idx.as.s, {temp}_val); }}")
            else:
                self.emit(f"{target} = {value};")
        else:
            # 复合赋值 +=, -=, *=, /=
            op_map = {"+=": "au_add", "-=": "au_sub", "*=": "au_mul", "/=": "au_div"}
            if stmt.op in op_map:
                self.emit(f"{target} = {op_map[stmt.op]}({target}, {value});")

    def gen_if_stmt(self, stmt: IfStmt):
        """生成 if 语句(支持类型特化)"""
        cond = self.gen_expr(stmt.condition)

        # 纯 int 函数中,如果条件是比较运算或 bool 变量,直接使用
        if self.current_fn_pure_int:
            cond_type = self._infer_expr_type(stmt.condition)
            if cond_type.is_bool() or cond_type.is_int():
                cond_code = cond
            else:
                cond_code = f"au_value_truthy({cond})"
        else:
            cond_code = f"au_value_truthy({cond})"

        self.emit(f"if ({cond_code}) {{")
        self.indent()
        if stmt.then_body:
            for s in stmt.then_body.statements:
                self.gen_stmt(s)
        self.dedent()
        self.emit("}")

        # elif 子句
        for cond_expr, body in stmt.elif_clauses:
            cond_code = self.gen_expr(cond_expr)
            self.emit(f"else if (au_value_truthy({cond_code})) {{")
            self.indent()
            if body:
                for s in body.statements:
                    self.gen_stmt(s)
            self.dedent()
            self.emit("}")

        # else 子句
        if stmt.else_body:
            self.emit("else {")
            self.indent()
            for s in stmt.else_body.statements:
                self.gen_stmt(s)
            self.dedent()
            self.emit("}")

    def gen_for_stmt(self, stmt: ForStmt):
        """生成 for 循环"""
        iterable = self.gen_expr(stmt.iterable)
        temp_iter = self.new_temp("_iter")
        temp_idx = self.new_temp("_idx")
        temp_len = self.new_temp("_len")

        # 保存可迭代对象
        self.emit(f"AuValue {temp_iter} = {iterable};")
        self.emit(f"int64_t {temp_len} = au_len({temp_iter});")

        if len(stmt.variables) == 1:
            # for x in iterable
            var_name = self.c_ident(stmt.variables[0])
            self.emit(f"for (int64_t {temp_idx} = 0; {temp_idx} < {temp_len}; {temp_idx}++) {{")
            self.indent()
            self.emit(f"AuValue {var_name} = au_array_get({temp_iter}.as.arr, {temp_idx});")
            if stmt.body:
                for s in stmt.body.statements:
                    self.gen_stmt(s)
            self.dedent()
            self.emit("}")
        elif len(stmt.variables) == 2:
            # for key, value in iterable
            key_name = self.c_ident(stmt.variables[0])
            val_name = self.c_ident(stmt.variables[1])
            self.emit(f"for (int64_t {temp_idx} = 0; {temp_idx} < {temp_len}; {temp_idx}++) {{")
            self.indent()
            self.emit(f"AuValue {key_name} = AU_INT_VAL({temp_idx});")
            self.emit(f"AuValue {val_name} = au_array_get({temp_iter}.as.arr, {temp_idx});")
            if stmt.body:
                for s in stmt.body.statements:
                    self.gen_stmt(s)
            self.dedent()
            self.emit("}")

    def gen_while_stmt(self, stmt: WhileStmt):
        """生成 while 循环(支持类型特化)"""
        cond = self.gen_expr(stmt.condition)
        if self.current_fn_pure_int:
            cond_type = self._infer_expr_type(stmt.condition)
            if cond_type.is_bool() or cond_type.is_int():
                cond_code = cond
            else:
                cond_code = f"au_value_truthy({cond})"
        else:
            cond_code = f"au_value_truthy({cond})"
        self.emit(f"while ({cond_code}) {{")
        self.indent()
        if stmt.body:
            for s in stmt.body.statements:
                self.gen_stmt(s)
        self.dedent()
        self.emit("}")

    def gen_return_stmt(self, stmt: ReturnStmt):
        """生成 return 语句(支持类型特化和记忆化)"""
        if stmt.value:
            value = self.gen_expr(stmt.value)
            if self._current_fn_memoized and self.current_fn_name:
                # 记忆化:将返回值写入缓存
                memo_name = f"_memo_{self.c_ident(self.current_fn_name)}"
                param_c = self.c_ident(self._memo_param_name)
                temp = self.new_temp("_ret")
                self.emit(f"int64_t {temp} = {value};")
                self.emit(f"if ({param_c} >= 0 && {param_c} < 100000) {{")
                self.indent()
                self.emit(f"{memo_name}_cache[{param_c}] = {temp};")
                self.emit(f"{memo_name}_valid[{param_c}] = 1;")
                self.dedent()
                self.emit("}")
                self.emit(f"return {temp};")
            else:
                self.emit(f"return {value};")
        else:
            if self.current_fn_pure_int:
                self.emit("return 0;")
            else:
                self.emit("return AU_NIL_VAL();")

    def gen_expr_stmt(self, stmt: ExprStmt):
        """生成表达式语句"""
        expr = self.gen_expr(stmt.expr)
        # 只有函数调用等有副作用的表达式才需要保留
        if isinstance(stmt.expr, (CallExpr, MethodCall, AssignStmt)):
            self.emit(f"(void){expr};")
        # 其他表达式语句忽略(无副作用)

    # ============================================================
    # 表达式生成
    # ============================================================
    def gen_expr(self, expr: Expr) -> str:
        """生成表达式,返回 C 表达式字符串(支持类型特化)"""
        # 纯 int 函数中,对 int/bool 类型表达式使用特化代码
        if self.current_fn_pure_int:
            expr_type = self._infer_expr_type(expr)
            if expr_type.is_int() or expr_type.is_bool():
                return self.gen_expr_typed(expr)

        if isinstance(expr, IntLiteral):
            return f"AU_INT_VAL({expr.value})"
        elif isinstance(expr, FloatLiteral):
            return f"AU_FLOAT_VAL({expr.value})"
        elif isinstance(expr, BoolLiteral):
            return f"AU_BOOL_VAL({'true' if expr.value else 'false'})"
        elif isinstance(expr, NilLiteral):
            return "AU_NIL_VAL()"
        elif isinstance(expr, StringLiteral):
            return self.gen_string_literal(expr)
        elif isinstance(expr, Identifier):
            return self.c_ident(expr.name)
        elif isinstance(expr, BinaryOp):
            return self.gen_binary_op(expr)
        elif isinstance(expr, UnaryOp):
            return self.gen_unary_op(expr)
        elif isinstance(expr, CallExpr):
            return self.gen_call_expr(expr)
        elif isinstance(expr, MethodCall):
            return self.gen_method_call(expr)
        elif isinstance(expr, ArrayLiteral):
            return self.gen_array_literal(expr)
        elif isinstance(expr, MapLiteral):
            return self.gen_map_literal(expr)
        elif isinstance(expr, IndexAccess):
            return self.gen_index_access(expr)
        elif isinstance(expr, MemberAccess):
            return self.gen_member_access(expr)
        elif isinstance(expr, IfExpr):
            return self.gen_if_expr(expr)
        elif isinstance(expr, RangeExpr):
            return self.gen_range_expr(expr)
        elif isinstance(expr, PipeExpr):
            return self.gen_pipe_expr(expr)
        elif isinstance(expr, StringInterpolation):
            return self.gen_string_interpolation(expr)
        elif isinstance(expr, LambdaExpr):
            # lambda 暂时不支持,返回 nil
            return "AU_NIL_VAL()"
        elif isinstance(expr, MatchExpr):
            return self.gen_match_expr(expr)
        else:
            return f"AU_NIL_VAL() /* TODO: {type(expr).__name__} */"

    def gen_expr_typed(self, expr: Expr) -> str:
        """生成类型特化的表达式(纯 int/bool 函数中使用,直接使用 C 原生类型)"""
        if isinstance(expr, IntLiteral):
            return f"((int64_t){expr.value})"
        elif isinstance(expr, BoolLiteral):
            return "true" if expr.value else "false"
        elif isinstance(expr, Identifier):
            return self.c_ident(expr.name)
        elif isinstance(expr, BinaryOp):
            return self.gen_binary_op_typed(expr)
        elif isinstance(expr, UnaryOp):
            operand = self.gen_expr_typed(expr.operand)
            if expr.op == '-':
                return f"(-{operand})"
            elif expr.op == '!':
                return f"(!{operand})"
            return operand
        elif isinstance(expr, CallExpr):
            # 函数调用:如果是纯 int 函数,直接调用
            if isinstance(expr.callee, Identifier):
                func_name = expr.callee.name
                fn_type = self.function_types.get(func_name, {})
                if fn_type and is_pure_int_function(fn_type):
                    args = ", ".join([self.gen_expr_typed(a) for a in expr.args])
                    return f"{self.c_ident(func_name)}({args})"
                # 内置 int 函数
                builtin_int = {
                    'len', 'now_ms', 'floor', 'ceil', 'round', 'min', 'max',
                    'gcd', 'lcm', 'factorial', 'fibonacci',
                }
                if func_name in builtin_int:
                    args = ", ".join([self.gen_expr(a) for a in expr.args])
                    if func_name == 'len':
                        return f"au_len({args})"
                    return f"{func_name}({args})"
                if func_name == 'is_prime':
                    args = ", ".join([self.gen_expr_typed(a) for a in expr.args])
                    return f"au_is_prime({args})"
            # 回退到普通生成
            return self.gen_call_expr(expr)
        elif isinstance(expr, IfExpr):
            # 三元运算符
            cond = self.gen_expr_typed(expr.condition)
            then_val = "0"
            else_val = "0"
            if expr.then_body and expr.then_body.statements:
                last = expr.then_body.statements[-1]
                if isinstance(last, ExprStmt):
                    then_val = self.gen_expr_typed(last.expr)
                elif isinstance(last, ReturnStmt) and last.value:
                    then_val = self.gen_expr_typed(last.value)
            if expr.else_body and expr.else_body.statements:
                last = expr.else_body.statements[-1]
                if isinstance(last, ExprStmt):
                    else_val = self.gen_expr_typed(last.expr)
                elif isinstance(last, ReturnStmt) and last.value:
                    else_val = self.gen_expr_typed(last.value)
            return f"({cond} ? {then_val} : {else_val})"
        else:
            # 回退到普通生成
            return self.gen_expr(expr)

    def gen_binary_op_typed(self, expr: BinaryOp) -> str:
        """生成类型特化的二元运算(直接使用 C 运算符)"""
        left = self.gen_expr_typed(expr.left)
        right = self.gen_expr_typed(expr.right)
        op = expr.op

        # 算术运算
        if op == '+':
            return f"({left} + {right})"
        elif op == '-':
            return f"({left} - {right})"
        elif op == '*':
            return f"({left} * {right})"
        elif op == '/':
            return f"({left} / {right})"
        elif op == '%':
            return f"({left} % {right})"
        elif op == '**':
            # 幂运算:使用简单实现
            return f"_aurora_pow_int({left}, {right})"

        # 比较运算
        elif op == '==':
            return f"({left} == {right})"
        elif op == '!=':
            return f"({left} != {right})"
        elif op == '<':
            return f"({left} < {right})"
        elif op == '<=':
            return f"({left} <= {right})"
        elif op == '>':
            return f"({left} > {right})"
        elif op == '>=':
            return f"({left} >= {right})"

        # 逻辑运算
        elif op == '&&':
            return f"({left} && {right})"
        elif op == '||':
            return f"({left} || {right})"

        return f"({left} {op} {right})"

    def gen_string_literal(self, expr: StringLiteral) -> str:
        """生成字符串字面量(处理插值 {expr})"""
        if expr.raw:
            # 原始字符串,不处理转义和插值
            return f"(AuValue){{.type=AU_STRING, .as.s=au_string_from_literal({self.c_string_literal(expr.value)})}}"

        # 检查是否包含插值
        if '{' not in expr.value:
            # 普通字符串,无插值
            return f"(AuValue){{.type=AU_STRING, .as.s=au_string_new({self.c_string_literal(expr.value)})}}"

        # 包含插值,需要解析并生成拼接代码
        # 简单解析:找到 { 和 } 之间的内容作为表达式
        # 注意:这里不处理嵌套的 {}
        temp = self.new_temp("_str")
        self.emit(f"AuString* {temp} = au_string_new(\"\");")

        i = 0
        s = expr.value
        while i < len(s):
            if s[i] == '{' and i + 1 < len(s):
                # 找到插值开始
                end = s.find('}', i + 1)
                if end == -1:
                    # 没有闭合的 },当作普通字符
                    part = s[i:]
                    part_code = self.c_string_literal(part)
                    self.emit(f"{{ AuString* _p = au_string_new({part_code}); AuString* _t = au_string_concat({temp}, _p); au_string_free({temp}); au_string_free(_p); {temp} = _t; }}")
                    break
                expr_str = s[i+1:end].strip()
                # 解析表达式字符串为 AST
                try:
                    from aurora.lexer import Lexer
                    from aurora.parser import Parser
                    lexer = Lexer(expr_str)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens)
                    # 解析为表达式
                    expr_ast = parser.parse_expression()
                    expr_code = self.gen_expr(expr_ast)
                    self.emit(f"{{ AuValue _v = {expr_code}; AuString* _p = au_value_to_string(_v); AuString* _t = au_string_concat({temp}, _p); au_string_free({temp}); au_string_free(_p); {temp} = _t; }}")
                except Exception:
                    # 解析失败,当作普通字符串
                    part = s[i:end+1]
                    part_code = self.c_string_literal(part)
                    self.emit(f"{{ AuString* _p = au_string_new({part_code}); AuString* _t = au_string_concat({temp}, _p); au_string_free({temp}); au_string_free(_p); {temp} = _t; }}")
                i = end + 1
            else:
                # 普通字符,找到下一个 {
                next_brace = s.find('{', i)
                if next_brace == -1:
                    part = s[i:]
                    i = len(s)
                else:
                    part = s[i:next_brace]
                    i = next_brace
                if part:
                    part_code = self.c_string_literal(part)
                    self.emit(f"{{ AuString* _p = au_string_new({part_code}); AuString* _t = au_string_concat({temp}, _p); au_string_free({temp}); au_string_free(_p); {temp} = _t; }}")

        return f"(AuValue){{.type=AU_STRING, .as.s={temp}}}"

    def gen_binary_op(self, expr: BinaryOp) -> str:
        """生成二元运算"""
        left = self.gen_expr(expr.left)
        right = self.gen_expr(expr.right)
        op = expr.op

        # 算术运算
        if op == "+":
            return f"au_add({left}, {right})"
        elif op == "-":
            return f"au_sub({left}, {right})"
        elif op == "*":
            return f"au_mul({left}, {right})"
        elif op == "/":
            return f"au_div({left}, {right})"
        elif op == "%":
            return f"au_mod({left}, {right})"
        elif op == "**":
            return f"au_pow({left}, {right})"

        # 比较运算(返回 bool,但在 Aurora 中 bool 也是 AuValue)
        elif op == "==":
            return f"AU_BOOL_VAL(au_value_eq({left}, {right}))"
        elif op == "!=":
            return f"AU_BOOL_VAL(!au_value_eq({left}, {right}))"
        elif op == "<":
            return f"AU_BOOL_VAL(au_lt({left}, {right}))"
        elif op == "<=":
            return f"AU_BOOL_VAL(au_le({left}, {right}))"
        elif op == ">":
            return f"AU_BOOL_VAL(au_gt({left}, {right}))"
        elif op == ">=":
            return f"AU_BOOL_VAL(au_ge({left}, {right}))"

        # 逻辑运算
        elif op == "&&":
            return f"AU_BOOL_VAL(au_and({left}, {right}))"
        elif op == "||":
            return f"AU_BOOL_VAL(au_or({left}, {right}))"

        else:
            return f"AU_NIL_VAL() /* TODO: op {op} */"

    def gen_unary_op(self, expr: UnaryOp) -> str:
        """生成一元运算"""
        operand = self.gen_expr(expr.operand)
        if expr.op == "-":
            return f"au_neg({operand})"
        elif expr.op == "!":
            return f"AU_BOOL_VAL(au_not({operand}))"
        elif expr.op == "#":
            # 长度运算符
            return f"AU_INT_VAL(au_len({operand}))"
        else:
            return operand

    def _try_compile_time_eval(self, expr: CallExpr):
        """尝试编译期常量计算。成功返回C表达式字符串,失败返回None"""
        if not isinstance(expr.callee, Identifier):
            return None
        func_name = expr.callee.name

        # 检查参数是否全是字面量
        const_args = []
        for arg in expr.args:
            if isinstance(arg, IntLiteral):
                const_args.append(('int', arg.value))
            elif isinstance(arg, FloatLiteral):
                const_args.append(('float', arg.value))
            elif isinstance(arg, BoolLiteral):
                const_args.append(('bool', arg.value))
            elif isinstance(arg, StringLiteral):
                const_args.append(('string', arg.value))
            elif isinstance(arg, NilLiteral):
                const_args.append(('nil', None))
            else:
                return None  # 非常量参数

        # 内置数学函数的编译期计算
        builtin_compute = {
            'sqrt': lambda args: ('float', args[0][1] ** 0.5),
            'abs': lambda args: ('int', abs(args[0][1])) if args[0][0] == 'int' else ('float', abs(args[0][1])),
            'floor': lambda args: ('int', int(args[0][1] // 1)),
            'ceil': lambda args: ('int', int(-(-args[0][1] // 1))),
            'round': lambda args: ('int', int(round(args[0][1]))),
            'min': lambda args: ('int', min(a[1] for a in args)) if all(a[0]=='int' for a in args) else ('float', min(a[1] for a in args)),
            'max': lambda args: ('int', max(a[1] for a in args)) if all(a[0]=='int' for a in args) else ('float', max(a[1] for a in args)),
            'gcd': lambda args: ('int', self._py_gcd(args[0][1], args[1][1])),
            'lcm': lambda args: ('int', abs(args[0][1] * args[1][1]) // self._py_gcd(args[0][1], args[1][1])),
            'is_prime': lambda args: ('bool', self._py_is_prime(args[0][1])),
            'factorial': lambda args: ('int', self._py_factorial(args[0][1])),
            'fibonacci': lambda args: ('int', self._py_fibonacci(args[0][1])),
        }

        if func_name in builtin_compute:
            try:
                result_type, result_val = builtin_compute[func_name](const_args)
                return self._const_to_c(result_type, result_val)
            except:
                return None

        # 用户定义的纯 int 函数的编译期计算
        if func_name in self.function_types:
            fn_type = self.function_types[func_name]
            if is_pure_int_function(fn_type) and all(a[0] == 'int' for a in const_args):
                # 查找函数定义
                fn_def = None
                for stmt in self._program_statements:
                    if isinstance(stmt, FnDef) and stmt.name == func_name:
                        fn_def = stmt
                        break
                if fn_def:
                    try:
                        result = self._ct_eval_function(fn_def, [a[1] for a in const_args], {})
                        if result is not None:
                            # 根据当前函数类型返回不同的结果
                            if self.current_fn_pure_int:
                                return f"((int64_t){result})"
                            else:
                                return f"AU_INT_VAL({result})"
                    except:
                        return None

        return None

    def _const_to_c(self, result_type, result_val):
        """将编译期计算结果转换为C表达式"""
        if result_type == 'int':
            return f"((int64_t){result_val})"
        elif result_type == 'float':
            return f"((double){result_val})"
        elif result_type == 'bool':
            return "true" if result_val else "false"
        elif result_type == 'string':
            return f'(AuValue){{.type=AU_STRING, .as.s=au_string_new({self.c_string_literal(result_val)})}}'
        return None

    @staticmethod
    def _py_gcd(a, b):
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def _py_is_prime(n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    @staticmethod
    def _py_factorial(n):
        if n < 0:
            return 0
        r = 1
        for i in range(2, n + 1):
            r *= i
        return r

    @staticmethod
    def _py_fibonacci(n):
        if n < 0:
            return 0
        if n < 2:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def _ct_eval_function(self, fn_def: FnDef, args, cache):
        """编译期递归求值器(用于纯int函数)"""
        # 检查缓存(记忆化)
        cache_key = (fn_def.name, tuple(args))
        if cache_key in cache:
            return cache[cache_key]

        # 构建局部环境
        env = {}
        for i, param in enumerate(fn_def.params):
            if i < len(args):
                env[param.name] = args[i]

        # 求值函数体
        result = self._ct_eval_block(fn_def.body, env, cache) if fn_def.body else 0
        if isinstance(result, tuple) and result[0] == 'return':
            result = result[1]

        # 写入缓存
        cache[cache_key] = result
        return result

    def _ct_eval_block(self, block: Block, env, cache):
        """编译期求值代码块,返回最后一个表达式的值"""
        result = 0
        for stmt in block.statements:
            r = self._ct_eval_stmt(stmt, env, cache)
            if r is not None:
                if isinstance(r, tuple) and r[0] == 'return':
                    return r  # 保持 return 标记,不解除
                result = r
        return result

    def _ct_eval_stmt(self, stmt, env, cache):
        """编译期求值语句"""
        if isinstance(stmt, ReturnStmt):
            if stmt.value:
                return ('return', self._ct_eval_expr(stmt.value, env, cache))
            return ('return', 0)
        elif isinstance(stmt, IfStmt):
            cond = self._ct_eval_expr(stmt.condition, env, cache)
            if cond:
                if stmt.then_body:
                    r = self._ct_eval_block(stmt.then_body, env, cache)
                    if isinstance(r, tuple) and r[0] == 'return':
                        return r
            else:
                for cond_expr, body in stmt.elif_clauses:
                    if self._ct_eval_expr(cond_expr, env, cache):
                        if body:
                            r = self._ct_eval_block(body, env, cache)
                            if isinstance(r, tuple) and r[0] == 'return':
                                return r
                        break
                else:
                    if stmt.else_body:
                        r = self._ct_eval_block(stmt.else_body, env, cache)
                        if isinstance(r, tuple) and r[0] == 'return':
                            return r
            return None
        elif isinstance(stmt, LetStmt) or isinstance(stmt, ConstStmt):
            if stmt.initializer:
                env[stmt.name] = self._ct_eval_expr(stmt.initializer, env, cache)
            return None
        elif isinstance(stmt, AssignStmt):
            if isinstance(stmt.target, Identifier):
                env[stmt.target.name] = self._ct_eval_expr(stmt.value, env, cache)
            return None
        elif isinstance(stmt, ExprStmt):
            return self._ct_eval_expr(stmt.expr, env, cache)
        return None

    def _ct_eval_expr(self, expr, env, cache):
        """编译期求值表达式"""
        if isinstance(expr, IntLiteral):
            return expr.value
        elif isinstance(expr, Identifier):
            return env.get(expr.name, 0)
        elif isinstance(expr, BinaryOp):
            left = self._ct_eval_expr(expr.left, env, cache)
            right = self._ct_eval_expr(expr.right, env, cache)
            if expr.op == '+':
                return left + right
            elif expr.op == '-':
                return left - right
            elif expr.op == '*':
                return left * right
            elif expr.op == '/':
                return left // right if right != 0 else 0
            elif expr.op == '%':
                return left % right if right != 0 else 0
            elif expr.op == '<':
                return left < right
            elif expr.op == '>':
                return left > right
            elif expr.op == '<=':
                return left <= right
            elif expr.op == '>=':
                return left >= right
            elif expr.op == '==':
                return left == right
            elif expr.op == '!=':
                return left != right
            return 0
        elif isinstance(expr, UnaryOp):
            val = self._ct_eval_expr(expr.operand, env, cache)
            if expr.op == '-':
                return -val
            return val
        elif isinstance(expr, CallExpr):
            if isinstance(expr.callee, Identifier):
                func_name = expr.callee.name
                # 递归调用当前函数
                for stmt in self._program_statements:
                    if isinstance(stmt, FnDef) and stmt.name == func_name:
                        args = [self._ct_eval_expr(a, env, cache) for a in expr.args]
                        return self._ct_eval_function(stmt, args, cache)
            return 0
        return 0

    def gen_call_expr(self, expr: CallExpr) -> str:
        """生成函数调用(支持类型特化和编译期常量计算)"""
        callee_name = None
        if isinstance(expr.callee, Identifier):
            callee_name = expr.callee.name

        # 编译期常量计算:如果参数全是字面量,且是纯函数,在编译时直接计算结果
        const_result = self._try_compile_time_eval(expr)
        if const_result is not None:
            return const_result

        # 如果调用的是纯 int 函数,且当前不是纯 int 函数,需要类型转换
        if callee_name and callee_name in self.function_types:
            fn_type = self.function_types[callee_name]
            if is_pure_int_function(fn_type) and not self.current_fn_pure_int:
                # 将 AuValue 参数转换为 int64_t,将 int64_t 返回值包装为 AuValue
                temp = self.new_temp("_call")
                args_converted = []
                for i, arg in enumerate(expr.args):
                    arg_code = self.gen_expr(arg)
                    arg_temp = f"{temp}_arg{i}"
                    self.emit(f"AuValue {arg_temp} = {arg_code};")
                    args_converted.append(f"{arg_temp}.as.i")
                args_str = ", ".join(args_converted)
                self.emit(f"int64_t {temp}_result = {self.c_ident(callee_name)}({args_str});")
                return f"AU_INT_VAL({temp}_result)"

        # 内置函数映射
        builtin_map = {
            "println": "au_println",
            "print": "au_print",
            "len": "au_len",
            "range": "au_range",
            "read_line": "au_read_line",
            "read_file": "au_read_file",
            "write_file": "au_write_file",
            "append_file": "au_append_file",
            "file_exists": "au_file_exists",
            "list_dir": "au_list_dir",
            "shell": "au_shell",
            "get_env": "au_get_env",
            "set_env": "au_set_env",
            "now_ms": "au_now_ms",
            "sleep_ms": "au_sleep_ms",
            "sqrt": "au_sqrt",
            "abs": "au_abs",
            "sin": "au_sin",
            "cos": "au_cos",
            "tan": "au_tan",
            "log": "au_log",
            "exp": "au_exp",
            "floor": "au_floor",
            "ceil": "au_ceil",
            "round": "au_round",
            "min": "au_min",
            "max": "au_max",
            "gcd": "au_gcd",
            "lcm": "au_lcm",
            "is_prime": "au_is_prime",
            "factorial": "au_factorial",
            "fibonacci": "au_fibonacci",
            "json_parse": "au_json_parse",
            "json_stringify": "au_json_stringify",
            "type": "au_value_type_name",
            "to_string": "au_value_to_string",
        }

        args = ", ".join([self.gen_expr(a) for a in expr.args])

        if callee_name in builtin_map:
            c_func = builtin_map[callee_name]
            # 某些内置函数需要特殊的类型转换
            if c_func == "au_json_parse":
                # au_json_parse(AuString*) → AuValue,需要从 AuValue 提取 .as.s
                if expr.args:
                    arg_code = self.gen_expr(expr.args[0])
                    temp = self.new_temp("_json")
                    self.emit(f"AuValue {temp}_in = {arg_code};")
                    self.emit(f"AuValue {temp} = au_json_parse({temp}_in.type == AU_STRING ? {temp}_in.as.s : NULL);")
                    return temp
            elif c_func == "au_json_stringify":
                # au_json_stringify(AuValue) → AuString*,需要包装为 AuValue
                if expr.args:
                    arg_code = self.gen_expr(expr.args[0])
                    return f"(AuValue){{.type=AU_STRING, .as.s=au_json_stringify({arg_code})}}"
            elif c_func in ("au_read_file", "au_file_exists", "au_list_dir", "au_shell", "au_get_env"):
                # 这些函数接受 AuString* 参数,需要从 AuValue 提取
                if expr.args:
                    arg_codes = [self.gen_expr(a) for a in expr.args]
                    temps = []
                    for i, ac in enumerate(arg_codes):
                        t = self.new_temp("_arg")
                        self.emit(f"AuValue {t} = {ac};")
                        temps.append(t)
                    if c_func == "au_read_file":
                        return f"au_read_file({temps[0]}.as.s)"
                    elif c_func == "au_file_exists":
                        return f"AU_BOOL_VAL(au_file_exists({temps[0]}.as.s))"
                    elif c_func == "au_list_dir":
                        return f"(AuValue){{.type=AU_ARRAY, .as.arr=au_list_dir({temps[0]}.as.s)}}"
                    elif c_func == "au_shell":
                        self.emit(f"au_shell({temps[0]}.as.s);")
                        return "AU_NIL_VAL()"
                    elif c_func == "au_get_env":
                        return f"au_get_env({temps[0]}.as.s)"
            elif c_func == "au_set_env":
                if len(expr.args) >= 2:
                    arg_codes = [self.gen_expr(a) for a in expr.args]
                    t0 = self.new_temp("_envk")
                    t1 = self.new_temp("_envv")
                    self.emit(f"AuValue {t0} = {arg_codes[0]};")
                    self.emit(f"AuValue {t1} = {arg_codes[1]};")
                    self.emit(f"au_set_env({t0}.as.s, {t1}.as.s);")
                    return "AU_NIL_VAL()"
            elif c_func == "au_write_file" or c_func == "au_append_file":
                if len(expr.args) >= 2:
                    arg_codes = [self.gen_expr(a) for a in expr.args]
                    t0 = self.new_temp("_fpath")
                    t1 = self.new_temp("_fcont")
                    self.emit(f"AuValue {t0} = {arg_codes[0]};")
                    self.emit(f"AuValue {t1} = {arg_codes[1]};")
                    self.emit(f"{c_func}({t0}.as.s, {t1}.as.s);")
                    return "AU_NIL_VAL()"

            # 某些内置函数返回的不是 AuValue,需要包装
            non_auvalue_funcs = {
                "au_len", "au_range", "au_sqrt", "au_abs", "au_sin", "au_cos",
                "au_tan", "au_log", "au_exp", "au_floor", "au_ceil", "au_round",
                "au_min", "au_max", "au_gcd", "au_lcm", "au_is_prime",
                "au_factorial", "au_fibonacci", "au_now_ms",
            }
            if c_func in non_auvalue_funcs:
                # 判断返回类型
                if c_func in ("au_len", "au_range", "au_gcd", "au_lcm", "au_is_prime", "au_factorial", "au_fibonacci", "au_now_ms"):
                    if c_func == "au_is_prime":
                        return f"AU_BOOL_VAL({c_func}({args}))"
                    elif c_func == "au_range":
                        return f"{c_func}({args})"  # au_range 返回 AuValue
                    else:
                        return f"AU_INT_VAL({c_func}({args}))"
                else:
                    return f"AU_FLOAT_VAL({c_func}({args}))"
            else:
                return f"{c_func}({args})"
        elif callee_name:
            # 用户定义函数
            return f"{self.c_ident(callee_name)}({args})"
        else:
            # 复杂的 callee(如 lambda 调用),暂时不支持
            return "AU_NIL_VAL()"

    def gen_method_call(self, expr: MethodCall) -> str:
        """生成方法调用(转换为运行时函数)"""
        obj = self.gen_expr(expr.object)
        method = expr.method
        args = ", ".join([self.gen_expr(a) for a in expr.args])

        # 字符串方法
        string_methods = {
            "len": "au_len",
            "to_lower": "au_string_to_lower",
            "to_upper": "au_string_to_upper",
            "trim": "au_string_trim",
            "contains": "au_string_contains",
            "starts_with": "au_string_starts_with",
            "ends_with": "au_string_ends_with",
            "to_int": "au_string_to_int",
            "to_float": "au_string_to_float",
        }

        # 数组方法
        array_methods = {
            "len": "au_len",
            "push": "au_array_push",
            "pop": "au_array_pop",
            "reverse": "au_array_reverse",
            "sort": "au_array_sort",
            "contains": "au_array_contains",
        }

        # Map 方法
        map_methods = {
            "len": "au_len",
            "has": "au_map_has",
            "keys": "au_map_keys",
            "values": "au_map_values",
        }

        temp_obj = self.new_temp("_obj")
        self.emit(f"AuValue {temp_obj} = {obj};")

        if method in string_methods:
            c_func = string_methods[method]
            if c_func == "au_len":
                return f"AU_INT_VAL(au_len({temp_obj}))"
            elif c_func in ("au_string_to_int",):
                return f"AU_INT_VAL({c_func}({temp_obj}.as.s))"
            elif c_func in ("au_string_to_float",):
                return f"AU_FLOAT_VAL({c_func}({temp_obj}.as.s))"
            elif c_func in ("au_string_contains", "au_string_starts_with", "au_string_ends_with"):
                return f"AU_BOOL_VAL({c_func}({temp_obj}.as.s, {args}))"
            else:
                return f"(AuValue){{.type=AU_STRING, .as.s={c_func}({temp_obj}.as.s{', ' + args if args else ''})}}"
        elif method in array_methods:
            c_func = array_methods[method]
            if c_func == "au_len":
                return f"AU_INT_VAL(au_len({temp_obj}))"
            elif c_func == "au_array_push":
                self.emit(f"au_array_push({temp_obj}.as.arr, {args});")
                return temp_obj
            elif c_func == "au_array_pop":
                return f"au_array_pop({temp_obj}.as.arr)"
            elif c_func in ("au_array_reverse", "au_array_sort"):
                self.emit(f"{c_func}({temp_obj}.as.arr);")
                return temp_obj
            elif c_func == "au_array_contains":
                return f"AU_BOOL_VAL(au_array_contains({temp_obj}.as.arr, {args}))"
        elif method in map_methods:
            c_func = map_methods[method]
            if c_func == "au_len":
                return f"AU_INT_VAL(au_len({temp_obj}))"
            elif c_func == "au_map_has":
                return f"AU_BOOL_VAL(au_map_has({temp_obj}.as.map, {args}))"
            elif c_func == "au_map_keys":
                return f"(AuValue){{.type=AU_ARRAY, .as.arr=au_map_keys({temp_obj}.as.map)}}"
            elif c_func == "au_map_values":
                return f"(AuValue){{.type=AU_ARRAY, .as.arr=au_map_values({temp_obj}.as.map)}}"

        # 默认:尝试作为函数调用,对象作为第一个参数
        return f"{self.c_ident(method)}({temp_obj}{', ' + args if args else ''})"

    def gen_array_literal(self, expr: ArrayLiteral) -> str:
        """生成数组字面量"""
        temp = self.new_temp("_arr")
        self.emit(f"AuArray* {temp} = au_array_new();")
        for elem in expr.elements:
            elem_code = self.gen_expr(elem)
            self.emit(f"au_array_push({temp}, {elem_code});")
        return f"(AuValue){{.type=AU_ARRAY, .as.arr={temp}}}"

    def gen_map_literal(self, expr: MapLiteral) -> str:
        """生成 Map 字面量"""
        temp = self.new_temp("_map")
        self.emit(f"AuMap* {temp} = au_map_new();")
        for key, value in expr.entries:
            key_code = self.gen_expr(key)
            value_code = self.gen_expr(value)
            temp_key = self.new_temp("_key")
            self.emit(f"AuValue {temp_key} = {key_code};")
            self.emit(f"if ({temp_key}.type == AU_STRING) {{ au_map_set({temp}, {temp_key}.as.s, {value_code}); }}")
        return f"(AuValue){{.type=AU_MAP, .as.map={temp}}}"

    def gen_index_access(self, expr: IndexAccess) -> str:
        """生成索引访问"""
        obj = self.gen_expr(expr.object)
        index = self.gen_expr(expr.index)
        temp_obj = self.new_temp("_idxobj")
        temp_idx = self.new_temp("_idxval")
        self.emit(f"AuValue {temp_obj} = {obj};")
        self.emit(f"AuValue {temp_idx} = {index};")
        self.emit(f"if ({temp_obj}.type == AU_ARRAY) {{ {temp_obj} = au_array_get({temp_obj}.as.arr, {temp_idx}.as.i); }}")
        self.emit(f"else if ({temp_obj}.type == AU_MAP && {temp_idx}.type == AU_STRING) {{ {temp_obj} = au_map_get({temp_obj}.as.map, {temp_idx}.as.s); }}")
        return temp_obj

    def gen_member_access(self, expr: MemberAccess) -> str:
        """生成成员访问(暂时不支持,返回 nil)"""
        return "AU_NIL_VAL()"

    def gen_if_expr(self, expr: IfExpr) -> str:
        """生成 if 表达式(用三元运算符或临时变量)"""
        temp = self.new_temp("_if")
        cond = self.gen_expr(expr.condition)
        self.emit(f"AuValue {temp};")
        self.emit(f"if (au_value_truthy({cond})) {{")
        self.indent()
        if expr.then_body:
            for i, s in enumerate(expr.then_body.statements):
                if i == len(expr.then_body.statements) - 1 and isinstance(s, ExprStmt):
                    self.emit(f"{temp} = {self.gen_expr(s.expr)};")
                else:
                    self.gen_stmt(s)
        self.dedent()
        self.emit("}")
        if expr.else_body:
            self.emit("else {")
            self.indent()
            for i, s in enumerate(expr.else_body.statements):
                if i == len(expr.else_body.statements) - 1 and isinstance(s, ExprStmt):
                    self.emit(f"{temp} = {self.gen_expr(s.expr)};")
                else:
                    self.gen_stmt(s)
            self.dedent()
            self.emit("}")
        else:
            self.emit("else {")
            self.indent()
            self.emit(f"{temp} = AU_NIL_VAL();")
            self.dedent()
            self.emit("}")
        return temp

    def gen_range_expr(self, expr: RangeExpr) -> str:
        """生成区间表达式"""
        start = self.gen_expr(expr.start)
        end = self.gen_expr(expr.end)
        return f"au_range({start}.as.i, {end}.as.i)"

    def gen_pipe_expr(self, expr: PipeExpr) -> str:
        """生成管道表达式(x |> f → f(x))"""
        left = self.gen_expr(expr.left)
        temp = self.new_temp("_pipe")
        self.emit(f"AuValue {temp} = {left};")

        # 处理管道右侧的调用
        if isinstance(expr.call, CallExpr):
            callee_name = None
            if isinstance(expr.call.callee, Identifier):
                callee_name = expr.call.callee.name
            args = [temp] + [self.gen_expr(a) for a in expr.call.args]
            args_str = ", ".join(args)
            if callee_name:
                return f"{self.c_ident(callee_name)}({args_str})"
        elif isinstance(expr.call, Identifier):
            # x |> funcname → funcname(x)
            return f"{self.c_ident(expr.call.name)}({temp})"

        return temp

    def gen_string_interpolation(self, expr: StringInterpolation) -> str:
        """生成字符串插值"""
        temp = self.new_temp("_str")
        self.emit(f"AuString* {temp} = au_string_new(\"\");")
        for part in expr.parts:
            if isinstance(part, StringLiteral):
                part_code = self.c_string_literal(part.value)
                self.emit(f"{{ AuString* _p = au_string_new({part_code}); AuString* _t = au_string_concat({temp}, _p); au_string_free({temp}); au_string_free(_p); {temp} = _t; }}")
            else:
                part_code = self.gen_expr(part)
                self.emit(f"{{ AuValue _v = {part_code}; AuString* _p = au_value_to_string(_v); AuString* _t = au_string_concat({temp}, _p); au_string_free({temp}); au_string_free(_p); {temp} = _t; }}")
        return f"(AuValue){{.type=AU_STRING, .as.s={temp}}}"

    def gen_match_expr(self, expr: MatchExpr) -> str:
        """生成 match 表达式(转换为 if-else 链)"""
        temp = self.new_temp("_match")
        subject = self.gen_expr(expr.subject)
        temp_subj = self.new_temp("_subj")
        self.emit(f"AuValue {temp_subj} = {subject};")
        self.emit(f"AuValue {temp} = AU_NIL_VAL();")

        first = True
        for arm in expr.arms:
            cond = self.gen_match_pattern(arm.pattern, temp_subj)
            if first:
                self.emit(f"if ({cond}) {{")
                first = False
            else:
                self.emit(f"else if ({cond}) {{")
            self.indent()
            body_code = self.gen_expr(arm.body)
            self.emit(f"{temp} = {body_code};")
            self.dedent()
            self.emit("}")

        return temp

    def gen_match_pattern(self, pattern: Pattern, subject_var: str) -> str:
        """生成 match 模式的条件"""
        if isinstance(pattern, LiteralPattern):
            value = self.gen_expr(pattern.value)
            return f"au_value_eq({subject_var}, {value})"
        elif isinstance(pattern, WildcardPattern):
            return "1"
        elif isinstance(pattern, BindPattern):
            # 绑定模式:总是匹配,并绑定变量
            self.emit(f"AuValue {self.c_ident(pattern.name)} = {subject_var};")
            return "1"
        else:
            return "0"


# ============================================================
# 便捷函数
# ============================================================
def generate_c(program: Program) -> str:
    """从 AST 生成 C 代码"""
    gen = CodeGenerator()
    return gen.generate(program)


def compile_to_c(source: str, output_path: str, runtime_dir: str = None) -> str:
    """
    编译 Aurora 源代码为 C 文件。
    返回生成的 C 文件路径。
    """
    from aurora.parser import Parser
    from aurora.lexer import Lexer

    # 解析
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    # 生成 C 代码
    c_code = generate_c(program)

    # 写入文件
    with open(output_path, "w") as f:
        f.write(c_code)

    return output_path


def compile_to_binary(source_path: str, output_path: str = None, runtime_dir: str = None,
                      optimize: str = "-O3", cc: str = "cc") -> tuple:
    """
    编译 Aurora 源代码为原生可执行文件。
    返回 (可执行文件路径, 编译输出)。
    默认使用 -O3 + -flto + -march=native 激进优化。
    """
    import subprocess
    import tempfile

    if runtime_dir is None:
        # 默认 runtime 目录在 aurora/runtime/
        runtime_dir = os.path.join(os.path.dirname(__file__), "runtime")

    # 读取源代码
    with open(source_path, "r") as f:
        source = f.read()

    # 生成临时 C 文件
    with tempfile.NamedTemporaryFile(suffix=".c", mode="w", delete=False) as f:
        c_path = f.name
        from aurora.parser import Parser
        from aurora.lexer import Lexer
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        c_code = generate_c(program)
        f.write(c_code)

    # 确定输出路径
    if output_path is None:
        base = os.path.splitext(os.path.basename(source_path))[0]
        output_path = os.path.join(os.path.dirname(source_path), base)

    # 编译命令:激进优化
    rt_header = os.path.join(runtime_dir, "aurora_rt.h")
    rt_source = os.path.join(runtime_dir, "aurora_rt.c")

    cmd = [
        cc, optimize,
        "-flto",              # 链接时优化
        "-march=native",      # 针对当前 CPU 优化
        "-fomit-frame-pointer",  # 省略帧指针
        "-Wall",
        "-I", runtime_dir,
        c_path, rt_source,
        "-o", output_path,
        "-lm",  # 数学库
    ]

    # 执行编译
    result = subprocess.run(cmd, capture_output=True, text=True)
    compile_output = result.stdout + result.stderr

    # 清理临时文件
    try:
        os.unlink(c_path)
    except:
        pass

    if result.returncode != 0:
        raise RuntimeError(f"编译失败:\n{compile_output}")

    return output_path, compile_output


# ══════════════════════════════════════════════════════════════════════
# Aurora v3.2.0 — 代码生成器与项目脚手架工具
# 对应命令:`aurora new` / `aurora generate` / `aurora dev` / `aurora deploy`
# 说明:本段为纯标准库实现;开发服务器采用轮询监听(不依赖 watchdog)。
# ══════════════════════════════════════════════════════════════════════

import sys as _cg_sys
import json as _cg_json
import shutil as _cg_shutil
import subprocess as _cg_subprocess


# ------------------------------------------------------------
# 通用小工具
# ------------------------------------------------------------
def _cg_snake(name):
    """把 PascalCase / camelCase 转换为 snake_case。"""
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0 and not name[i - 1].isupper():
            out.append('_')
        out.append(ch.lower())
    return ''.join(out).replace('-', '_')


def _cg_kebab(name):
    """把 PascalCase 转换为 kebab-case(用于 Docker 镜像名等)。"""
    return _cg_snake(name).replace('_', '-')


def _cg_write(path, content, overwrite=None):
    """
    写文件(UTF-8)。
    - 文件不存在:直接写入;
    - 文件已存在:overwrite=True 覆盖;overwrite=False 跳过;
      overwrite=None(默认)时交互式询问,非交互(TTY 不可用)自动跳过。
    返回 True 表示确实写入了文件。
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if os.path.exists(path):
        if overwrite is True:
            pass  # 明确要求覆盖
        elif overwrite is False:
            return False  # 明确跳过
        else:
            # 交互模式:TTY 可用才询问,否则视为非交互直接跳过
            try:
                if not _cg_sys.stdin or not _cg_sys.stdin.isatty():
                    return False
                ans = input("文件已存在 %s,是否覆盖? [y/N] " % path)
            except (EOFError, KeyboardInterrupt):
                return False
            if ans.strip().lower() not in ("y", "yes"):
                return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def _cg_mkdirs(root, dirs):
    """在 root 下批量创建目录。"""
    for d in dirs:
        os.makedirs(os.path.join(root, d), exist_ok=True)


def _cg_project_root(name, target_dir):
    """项目根目录 = target_dir/name。"""
    root = os.path.join(target_dir, name)
    os.makedirs(root, exist_ok=True)
    return root


# ------------------------------------------------------------
# 脚手架:项目模板(使用 __NAME__ 占位,避免与 Aurora 的花括号冲突)
# ------------------------------------------------------------
_TPL_TOML = '''[project]
name = "__NAME__"
version = "0.1.0"
aurora = ">=3.2.0"

[dependencies]

[scripts]
dev = "aurora dev src/main.aur"
build = "aurora build src/main.aur"
'''

_TPL_README = '''# __NAME__

基于 Aurora v3.2.0 创建的项目。

## 快速开始

```bash
# 安装依赖(可选)
aurora install

# 开发模式运行(自动重载)
aurora dev src/main.aur

# 构建
aurora build src/main.aur
```

## 目录结构

- `src/` — 源码
- `tests/` — 测试
- `config/` — 多环境配置
'''

_TPL_FULLSTACK_MAIN = '''// ============================================
// __NAME__ 全栈应用入口
// 路由 + 数据库 + 静态资源
// ============================================
use std.web.{App, Request, Response};
use std.db.Connection;

fn main() {
    // 创建主应用
    let app = App("__NAME__");

    // 连接数据库(SQLite)
    let db = Connection("sqlite:///__NAME__.db");

    // 注册路由
    app.get("/", index);
    app.get("/api/users", user_list);
    app.post("/api/users", user_create);

    // 启动 HTTP 服务
    app.run(port=8080);
}

// 首页:返回一段 HTML
fn index(req: Request) -> Response {
    return Response.html("<h1>欢迎来到 __NAME__</h1>");
}

// 用户列表接口
fn user_list(req: Request) -> Response {
    return Response.json({ "message": "用户列表接口" });
}

// 创建用户接口
fn user_create(req: Request) -> Response {
    return Response.json({ "message": "创建用户成功" });
}
'''

_TPL_USER_MODEL = '''// User 模型示例
// 字段:id / name / email
use std.db;

struct User extends db.Model {
    id: int,
    name: str,
    email: str
}
'''

_TPL_USER_CONTROLLER = '''// User REST 控制器示例
// 提供标准 CRUD 接口
use std.web.{Request, Response};

fn index(req: Request) -> Response {
    // 列表
    return Response.json({ "action": "index" });
}

fn show(req: Request) -> Response {
    // 详情
    return Response.json({ "action": "show" });
}

fn create(req: Request) -> Response {
    // 新建
    return Response.json({ "action": "create" });
}

fn update(req: Request) -> Response {
    // 更新
    return Response.json({ "action": "update" });
}

fn destroy(req: Request) -> Response {
    // 删除
    return Response.json({ "action": "destroy" });
}
'''

_TPL_APP_COMPONENT = '''// 前端根组件示例
// 演示 mount / render / unmount 生命周期
use std.web.Component;

struct App extends Component {
    title: str
}

fn mount(self: App) {
    // 组件挂载时调用
    self.title = "__NAME__";
}

fn render(self: App) {
    // 渲染视图
    return "<h1>" + self.title + "</h1>";
}

fn unmount(self: App) {
    // 组件卸载时调用
}
'''

_TPL_DEV_TOML = '''[server]
host = "127.0.0.1"
port = 8080
debug = true

[db]
url = "sqlite:///__NAME__.db"
'''

_TPL_PROD_TOML = '''[server]
host = "0.0.0.0"
port = 8080
debug = false

[db]
url = "sqlite:///__NAME___prod.db"
'''


def _tpl(template, name):
    """模板渲染:替换项目名占位符。"""
    return template.replace("__NAME__", name)


# ------------------------------------------------------------
# 1. 项目脚手架生成器
# ------------------------------------------------------------
def scaffold_fullstack(name, target_dir='.'):
    """
    生成全栈项目脚手架。
    目录:src/{controllers,models,components}、static/、migrations/、tests/、config/
    """
    root = _cg_project_root(name, target_dir)
    _cg_mkdirs(root, [
        'src', 'src/controllers', 'src/models', 'src/components',
        'static', 'migrations', 'tests', 'config',
    ])

    # 项目清单
    _cg_write(os.path.join(root, 'aurora.toml'), _tpl(_TPL_TOML, name))
    # 入口与示例代码
    _cg_write(os.path.join(root, 'src/main.aur'), _tpl(_TPL_FULLSTACK_MAIN, name))
    _cg_write(os.path.join(root, 'src/models/user.aur'), _TPL_USER_MODEL)
    _cg_write(os.path.join(root, 'src/controllers/user_controller.aur'), _TPL_USER_CONTROLLER)
    _cg_write(os.path.join(root, 'src/components/app.aur'), _tpl(_TPL_APP_COMPONENT, name))
    # 多环境配置
    _cg_write(os.path.join(root, 'config/dev.toml'), _tpl(_TPL_DEV_TOML, name))
    _cg_write(os.path.join(root, 'config/prod.toml'), _tpl(_TPL_PROD_TOML, name))
    # 说明文档
    _cg_write(os.path.join(root, 'README.md'), _tpl(_TPL_README, name))
    return root


_TPL_CLI_MAIN = '''// ============================================
// __NAME__ — 命令行工具示例
// 演示 std.cli 的彩色输出、表格、确认与选择
// ============================================
use std.cli;

fn main() {
    // 彩色欢迎信息
    cli.println(cli.color.fg("__NAME__", "green"));

    // 子命令:hello
    // 运行:aurora run src/main.aur hello 世界
    let args = std.argv();
    if args.len() > 1 and args[1] == "hello" {
        let who = args.len() > 2 ? args[2] : "world";
        cli.println(cli.bold("你好, " + who + "!"));
        return;
    }

    // 子命令:table
    if args.len() > 1 and args[1] == "table" {
        let t = cli.Table(["姓名", "年龄"], [["Alice", "18"], ["Bob", "20"]]);
        cli.println(t.render());
        return;
    }

    // 交互确认
    if cli.confirm("继续吗?") {
        let choice = cli.select("请选择:", ["选项 A", "选项 B"]);
        cli.println("你选择了: " + choice);
    }
}
'''


def scaffold_cli(name, target_dir='.'):
    """生成 CLI 工具项目脚手架。"""
    root = _cg_project_root(name, target_dir)
    _cg_mkdirs(root, ['src'])
    _cg_write(os.path.join(root, 'aurora.toml'), _tpl(_TPL_TOML, name))
    _cg_write(os.path.join(root, 'src/main.aur'), _tpl(_TPL_CLI_MAIN, name))
    _cg_write(os.path.join(root, 'README.md'), _tpl(_TPL_README, name))
    return root


_TPL_TUI_MAIN = '''// ============================================
// __NAME__ — TUI 应用示例
// 一个简单的文本编辑器界面
// ============================================
use std.tui;

fn main() {
    // 创建应用与主窗口
    let app = tui.App("__NAME__");

    // 根布局:纵向盒子(坐标 x=0, y=0, 宽 80, 高 24)
    let root = tui.VBox(0, 0, 80, 24);

    // 标题
    root.add(tui.Text("== __NAME__ 文本编辑器 =="));

    // 输入框(编辑区)
    let input = tui.Input();
    root.add(input);

    // 文件列表(侧边栏)
    root.add(tui.List(["main.aur", "README.md", "aurora.toml"]));

    // 底部按钮
    root.add(tui.Button("保存"));
    root.add(tui.Button("退出"));

    app.add(root);
    app.run();
}
'''


def scaffold_tui(name, target_dir='.'):
    """生成 TUI 应用项目脚手架。"""
    root = _cg_project_root(name, target_dir)
    _cg_mkdirs(root, ['src'])
    _cg_write(os.path.join(root, 'aurora.toml'), _tpl(_TPL_TOML, name))
    _cg_write(os.path.join(root, 'src/main.aur'), _tpl(_TPL_TUI_MAIN, name))
    _cg_write(os.path.join(root, 'README.md'), _tpl(_TPL_README, name))
    return root


_TPL_MICRO_MAIN = '''// ============================================
// __NAME__ — 微服务示例
// 提供 HTTP 接口与健康检查端点
// ============================================
use std.web.{App, Request, Response};

fn main() {
    let app = App("__NAME__-service");

    // 业务接口
    app.get("/api/ping", ping);
    // 健康检查(容器编排存活探针)
    app.get("/health", health);

    app.run(port=8080);
}

fn ping(req: Request) -> Response {
    return Response.json({ "message": "pong" });
}

fn health(req: Request) -> Response {
    return Response.json({ "status": "ok" });
}
'''

_TPL_DOCKERFILE = '''# __NAME__ 容器镜像
FROM aurora/runner:3.2.0

WORKDIR /app
COPY . /app

EXPOSE 8080

CMD ["aurora", "run", "src/main.aur"]
'''


def scaffold_microservice(name, target_dir='.'):
    """生成微服务项目脚手架(HTTP 服务 + 健康检查 + Dockerfile + 配置)。"""
    root = _cg_project_root(name, target_dir)
    _cg_mkdirs(root, ['src', 'config'])
    _cg_write(os.path.join(root, 'aurora.toml'), _tpl(_TPL_TOML, name))
    _cg_write(os.path.join(root, 'src/main.aur'), _tpl(_TPL_MICRO_MAIN, name))
    _cg_write(os.path.join(root, 'config/prod.toml'), _tpl(_TPL_PROD_TOML, name))
    _cg_write(os.path.join(root, 'Dockerfile'), _tpl(_TPL_DOCKERFILE, name))
    _cg_write(os.path.join(root, 'README.md'), _tpl(_TPL_README, name))
    return root


_TPL_WEBAPP_MAIN = '''// ============================================
// __NAME__ — 纯后端 Web 应用
// ============================================
use std.web.{App, Request, Response};

fn main() {
    let app = App("__NAME__");
    app.get("/", index);
    app.get("/api/hello", hello);
    app.run(port=8080);
}

fn index(req: Request) -> Response {
    return Response.html("<h1>__NAME__ 运行中</h1>");
}

fn hello(req: Request) -> Response {
    return Response.json({ "message": "hello" });
}
'''


def scaffold_webapp(name, target_dir='.'):
    """生成纯后端 Web 应用脚手架(仅 App + 路由)。"""
    root = _cg_project_root(name, target_dir)
    _cg_mkdirs(root, ['src'])
    _cg_write(os.path.join(root, 'aurora.toml'), _tpl(_TPL_TOML, name))
    _cg_write(os.path.join(root, 'src/main.aur'), _tpl(_TPL_WEBAPP_MAIN, name))
    return root


# ------------------------------------------------------------
# 2. 代码生成器
# ------------------------------------------------------------
def generate_controller(name, actions=None, target_dir='src/controllers'):
    """
    生成 REST 控制器文件,包含 CRUD 动作。
    actions:要生成的动作列表,默认 index/show/create/update/destroy。
    """
    if actions is None:
        actions = ['index', 'show', 'create', 'update', 'destroy']
    filename = _cg_snake(name) + '_controller.aur'
    path = os.path.join(target_dir, filename)

    lines = [
        '// %s 控制器(由 aurora generate 生成)' % name,
        'use std.web.{Request, Response};',
        '',
    ]
    doc = {
        'index': '列表', 'show': '详情', 'create': '新建',
        'update': '更新', 'destroy': '删除',
    }
    for act in actions:
        lines += [
            '// %s: %s' % (act, doc.get(act, '自定义动作')),
            'fn %s(req: Request) -> Response {' % act,
            '    return Response.json({ "action": "%s" });' % act,
            '}',
            '',
        ]
    _cg_write(path, '\n'.join(lines))
    return path


def generate_model(name, fields=None, target_dir='src/models'):
    """
    生成模型文件与迁移文件。
    fields 格式:[("name", "str"), ("age", "int", {"unique": True})]
    第三项为字段选项(如 unique/index)。
    """
    if fields is None:
        fields = [("id", "int"), ("name", "str")]
    snake = _cg_snake(name)
    model_path = os.path.join(target_dir, snake + '.aur')

    # 组装字段行与迁移列定义
    field_lines, column_lines = [], []
    for f in fields:
        fname, ftype = f[0], f[1]
        options = f[2] if len(f) > 2 and isinstance(f[2], dict) else {}
        suffix = ' '.join('%s' % k for k in sorted(options))
        field_lines.append('    %s: %s%s' % (fname, ftype, ('  # ' + suffix) if suffix else ''))
        column_lines.append('    %s %s' % (fname, ftype))

    content = (
        '// %s 模型(由 aurora generate 生成)\n'
        'use std.db;\n\n'
        'struct %s extends db.Model {\n' % (name, name) +
        ',\n'.join(field_lines) + '\n}\n'
    )
    _cg_write(model_path, content)

    # 同时生成迁移文件到 migrations/
    migration_path = os.path.join('migrations', '001_create_%s.aur' % snake)
    migration = (
        '// 迁移:创建 %s 表(由 aurora generate 生成)\n'
        'migration create_%s {\n' % (snake, snake) +
        '  table "%s" {\n' % snake +
        ',\n'.join(column_lines) + '\n  }\n'
        '}\n'
    )
    _cg_write(migration_path, migration)
    return model_path


def generate_component(name, props=None, target_dir='src/components'):
    """生成前端组件文件,包含 props 与 mount/render/unmount 生命周期。"""
    if props is None:
        props = [("title", "str"), ("items", "list")]
    path = os.path.join(target_dir, _cg_snake(name) + '.aur')

    prop_lines = ['    %s: %s' % (p[0], p[1]) for p in props]
    content = (
        '// %s 组件(由 aurora generate 生成)\n'
        'use std.web.Component;\n\n'
        'struct %s extends Component {\n' % (name, name) +
        ',\n'.join(prop_lines) + '\n}\n\n'
        '// 生命周期:挂载\n'
        'fn mount(self: %s) {\n}\n\n' % name +
        '// 生命周期:渲染\n'
        'fn render(self: %s) {\n    return "";\n}\n\n' % name +
        '// 生命周期:卸载\n'
        'fn unmount(self: %s) {\n}\n' % name
    )
    _cg_write(path, content)
    return path


def generate_service(name, methods=None, target_dir='src/services'):
    """生成服务层文件,包含业务逻辑方法骨架。"""
    if methods is None:
        methods = ['create', 'list', 'get', 'update', 'delete']
    path = os.path.join(target_dir, _cg_snake(name) + '_service.aur')

    lines = [
        '// %s 服务层(由 aurora generate 生成)' % name,
        '// 此处放置与控制器解耦的业务逻辑',
        '',
    ]
    for m in methods:
        lines += [
            '// %s 方法骨架' % m,
            'fn %s(args) {' % m,
            '    // TODO: 实现业务逻辑',
            '    return nil;',
            '}',
            '',
        ]
    _cg_write(path, '\n'.join(lines))
    return path


# ------------------------------------------------------------
# 3. 开发模式
# ------------------------------------------------------------
def _cg_snapshot(entry):
    """记录入口及其依赖文件的修改时间快照。"""
    snap = {}
    if os.path.isdir(entry):
        roots = [entry]
    else:
        roots = [os.path.dirname(os.path.abspath(entry)) or '.']
    for root in roots:
        for dirpath, _dirs, files in os.walk(root):
            if '__pycache__' in dirpath:
                continue
            for fn in files:
                if fn.endswith('.aur'):
                    fp = os.path.join(dirpath, fn)
                    try:
                        snap[fp] = os.path.getmtime(fp)
                    except OSError:
                        pass
    return snap


def dev_server(entry='src/main.aur', port=8080, interval=1.0):
    """
    开发模式:轮询监听 .aur 文件变化,变化时自动重启进程,
    控制台输出彩色日志。纯标准库实现(不依赖 watchdog)。
    """
    import time
    _GREEN, _CYAN, _YELLOW, _RESET = '\033[32m', '\033[36m', '\033[33m', '\033[0m'

    def _log(msg, color=_GREEN):
        print('%s[aurora dev] %s%s' % (color, msg, _RESET))

    _log('监听 %s,端口 %d(轮询间隔 %.1fs)' % (entry, port, interval))
    snapshot = _cg_snapshot(entry)
    proc = None
    try:
        while True:
            # 检查文件是否有变化
            new_snap = _cg_snapshot(entry)
            if new_snap != snapshot:
                changed = set(new_snap) ^ set(snapshot) or new_snap
                snapshot = new_snap
                _log('检测到文件变化,正在重启...', _YELLOW)
                if proc is not None:
                    try:
                        proc.terminate()
                    except OSError:
                        pass
                # 重启子进程运行入口文件
                cmd = [_cg_sys.executable, '-m', 'aurora', 'run', entry]
                proc = _cg_subprocess.Popen(cmd)
            time.sleep(interval)
    except KeyboardInterrupt:
        _log('开发服务器已停止', _CYAN)
        if proc is not None:
            proc.terminate()


# ------------------------------------------------------------
# 4. 部署工具
# ------------------------------------------------------------
def deploy_docker(project_dir, name, tag='latest'):
    """生成 Dockerfile 并(尽力)执行 docker build。返回镜像标签。"""
    dockerfile = os.path.join(project_dir, 'Dockerfile')
    image = '%s:%s' % (_cg_kebab(name), tag)
    content = _tpl(_TPL_DOCKERFILE, name)
    _cg_write(dockerfile, content)
    # 尝试调用 docker 构建;失败不影响 Dockerfile 的生成
    try:
        _cg_subprocess.run(
            ['docker', 'build', '-t', image, project_dir],
            capture_output=True,
        )
    except Exception:
        pass
    return image


def deploy_static(project_dir, output_dir='dist'):
    """把 static/ 下的静态资源导出到 output_dir,并生成清单文件。"""
    os.makedirs(output_dir, exist_ok=True)
    src = os.path.join(project_dir, 'static')
    files = []
    if os.path.isdir(src):
        for dirpath, _dirs, names in os.walk(src):
            for fn in names:
                sp = os.path.join(dirpath, fn)
                rel = os.path.relpath(sp, src)
                dp = os.path.join(output_dir, rel)
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                _cg_shutil.copy2(sp, dp)
                files.append(rel)
    manifest = {
        'project': os.path.basename(os.path.abspath(project_dir)),
        'files': files,
    }
    _cg_write(os.path.join(output_dir, 'manifest.json'),
              _cg_json.dumps(manifest, ensure_ascii=False, indent=2))
    return output_dir


# ------------------------------------------------------------
# 5. OpenAPI 3.0 文档生成
# ------------------------------------------------------------
def _cg_route_to_dict(route):
    """把路由统一成 dict 形式。兼容 (method, path) 元组与 dict。"""
    if isinstance(route, dict):
        return dict(route)
    if isinstance(route, (list, tuple)) and len(route) >= 2:
        return {'method': str(route[0]), 'path': str(route[1])}
    raise ValueError('无法识别的路由定义: %r' % (route,))


def generate_openapi(routes, title='Aurora API', version='1.0.0'):
    """
    从路由定义生成 OpenAPI 3.0 文档(JSON 字符串)。
    支持路径参数({id})、查询参数、请求体与响应体。
    """
    doc = {
        'openapi': '3.0.0',
        'info': {'title': title, 'version': version},
        'paths': {},
    }
    for route in routes:
        r = _cg_route_to_dict(route)
        method = r.get('method', 'get').lower()
        path = r.get('path', '/')
        # 解析路径参数:/users/{id} -> path 段参数
        params = []
        for seg in path.strip('/').split('/'):
            if seg.startswith('{') and seg.endswith('}'):
                pname = seg[1:-1]
                params.append({
                    'name': pname,
                    'in': 'path',
                    'required': True,
                    'schema': {'type': 'integer' if pname == 'id' else 'string'},
                })
        # 查询参数
        for q in r.get('query_params', r.get('query', [])) or []:
            if isinstance(q, dict):
                params.append(dict(q))
            else:
                params.append({'name': str(q), 'in': 'query', 'schema': {'type': 'string'}})
        operation = {
            'summary': r.get('summary', r.get('name', '%s %s' % (method.upper(), path))),
            'responses': {
                '200': {
                    'description': r.get('response_desc', '成功'),
                    'content': {'application/json': {'schema': {'type': 'object'}}},
                }
            },
        }
        if params:
            operation['parameters'] = params
        if r.get('body'):
            operation['requestBody'] = {
                'required': True,
                'content': {'application/json': {'schema': r['body']}},
            }
        doc['paths'].setdefault(path, {})[method] = operation
    return _cg_json.dumps(doc, ensure_ascii=False, indent=2)


# ------------------------------------------------------------
# CLI 命令注册
# ------------------------------------------------------------
def register_cli(subparsers) -> None:
    """
    向 CLI 注册 v3.2.0 脚手架相关命令:
      aurora new {fullstack|cli|tui|microservice|webapp} <name>
      aurora generate {controller|model|component|service} ...
      aurora dev [entry]
      aurora deploy [--docker] [--static]
    webapp 若已被 web_framework.py 注册则跳过,避免重复。
    """
    def _add(subparsers, name, **kw):
        """安全添加子解析器,已存在则返回现有解析器。"""
        existing = getattr(subparsers, '_name_parser_map', {})
        if name in existing:
            return existing[name]
        return subparsers.add_parser(name, **kw)

    existing = getattr(subparsers, '_name_parser_map', {})

    # ---- aurora new <kind> <name> ----
    p_new = _add(subparsers, 'new', help='创建新 Aurora 项目')
    # 主 CLI 可能已把 'name' 注册为必填位置参数;改为子命令模式后移除它
    if hasattr(p_new, '_actions'):
        for act in list(p_new._actions):
            if not act.option_strings and act.dest == 'name':
                p_new._actions.remove(act)
    if hasattr(p_new, '_defaults') and 'name' in p_new._defaults:
        p_new._defaults.pop('name', None)
    new_sub = p_new.add_subparsers(dest='new_kind')

    def _bind_new(kind, fn):
        p = new_sub.add_parser(kind, help='创建 %s 项目' % kind)
        p.add_argument('name', help='项目名称')
        p.set_defaults(func=lambda args: fn(args.name))

    _bind_new('fullstack', scaffold_fullstack)
    _bind_new('cli', scaffold_cli)
    _bind_new('tui', scaffold_tui)
    _bind_new('microservice', scaffold_microservice)
    # webapp 可能已由 web_framework.py 注册,避免重复
    if 'webapp' not in existing:
        _bind_new('webapp', scaffold_webapp)

    # ---- aurora generate <kind> ... ----
    p_gen = _add(subparsers, 'generate', help='生成代码(控制器/模型/组件/服务)')
    gen_sub = p_gen.add_subparsers(dest='gen_kind')

    p_c = gen_sub.add_parser('controller', help='生成 REST 控制器')
    p_c.add_argument('name', help='资源名,如 user')
    p_c.add_argument('actions', nargs='*', default=None,
                     help='动作列表,如 index show create(默认全部 CRUD)')
    p_c.set_defaults(func=lambda a: generate_controller(a.name, a.actions or None))

    p_m = gen_sub.add_parser('model', help='生成模型与迁移')
    p_m.add_argument('name', help='模型名,如 User')
    p_m.add_argument('fields', nargs='*', default=None,
                     help='字段列表,如 name:str age:int')
    p_m.set_defaults(func=lambda a: generate_model(
        a.name,
        [tuple(f.split(':')) for f in a.fields] if a.fields else None,
    ))

    p_comp = gen_sub.add_parser('component', help='生成前端组件')
    p_comp.add_argument('name', help='组件名,如 App')
    p_comp.add_argument('props', nargs='*', default=None,
                        help='props 列表,如 title:str items:list')
    p_comp.set_defaults(func=lambda a: generate_component(
        a.name,
        [tuple(p.split(':')) for p in a.props] if a.props else None,
    ))

    p_svc = gen_sub.add_parser('service', help='生成服务层')
    p_svc.add_argument('name', help='服务名,如 Auth')
    p_svc.add_argument('methods', nargs='*', default=None, help='方法名列表')
    p_svc.set_defaults(func=lambda a: generate_service(a.name, a.methods or None))

    # ---- aurora dev [entry] ----
    p_dev = _add(subparsers, 'dev', help='开发模式(自动重载)')
    p_dev.add_argument('entry', nargs='?', default='src/main.aur', help='入口文件')
    p_dev.add_argument('--port', type=int, default=8080)
    p_dev.set_defaults(func=lambda a: dev_server(a.entry, port=a.port))

    # ---- aurora deploy [--docker] [--static] ----
    p_dep = _add(subparsers, 'deploy', help='部署:容器化 / 静态导出')
    p_dep.add_argument('--docker', action='store_true', help='生成 Dockerfile 并构建镜像')
    p_dep.add_argument('--static', action='store_true', help='导出静态资源到 dist/')
    p_dep.add_argument('--name', default=None, help='项目名(默认当前目录名)')
    p_dep.set_defaults(func=_cmd_deploy)


def _cmd_deploy(args):
    """`aurora deploy` 的执行函数。"""
    project_dir = os.getcwd()
    name = args.name or os.path.basename(project_dir)
    if args.docker:
        image = deploy_docker(project_dir, name)
        print('Docker 镜像:', image)
    if args.static:
        out = deploy_static(project_dir, 'dist')
        print('静态资源已导出到:', out)
    if not args.docker and not args.static:
        print('提示:使用 --docker 或 --static 指定部署方式')


# ══════════════════════════════════════════════════════════════════════
# 标准库注册入口(本模块主要提供 CLI 脚手架能力)
# ══════════════════════════════════════════════════════════════════════
STDLIB_REGISTRATION = {
    'std.codegen': {
        'scaffold_fullstack': scaffold_fullstack,
        'scaffold_cli': scaffold_cli,
        'scaffold_tui': scaffold_tui,
        'scaffold_microservice': scaffold_microservice,
        'scaffold_webapp': scaffold_webapp,
        'generate_controller': generate_controller,
        'generate_model': generate_model,
        'generate_component': generate_component,
        'generate_service': generate_service,
        'dev_server': dev_server,
        'deploy_docker': deploy_docker,
        'deploy_static': deploy_static,
        'generate_openapi': generate_openapi,
        'register_cli': register_cli,
    }
}
