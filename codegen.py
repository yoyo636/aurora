"""
Aurora 原生编译器 — 代码生成器(AST → C)
将 Aurora AST 转换为 C 代码,然后由 gcc/clang 编译为原生机器码。
"""
import os
from .ast_nodes import *


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
        # C 关键字和内置函数名映射
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

    # ============================================================
    # 程序生成
    # ============================================================
    def generate(self, program: Program) -> str:
        """生成完整的 C 程序"""
        self.output = []
        self.indent_level = 0

        # 头文件
        self.emit_raw('#include "aurora_rt.h"')
        self.emit_raw('#include <stdio.h>')
        self.emit_raw('#include <stdlib.h>')
        self.emit_raw('#include <string.h>')
        self.emit_raw('')

        # 前向声明所有函数
        for stmt in program.statements:
            if isinstance(stmt, FnDef):
                params = ", ".join(["AuValue"] * len(stmt.params)) if stmt.params else "void"
                self.emit_raw(f"AuValue {self.c_ident(stmt.name)}({params});")
        self.emit_raw('')

        # 生成所有函数定义
        for stmt in program.statements:
            self.gen_stmt(stmt)
            self.emit('')

        # 生成 C 的 main 入口
        if self.has_main:
            # 有 Aurora main 函数,生成 C main 调用它
            self.emit_raw('int main(int argc, char** argv) {')
            self.emit_raw('    au_runtime_init();')
            self.emit_raw('    AuValue _result = aurora_main();')
            self.emit_raw('    (void)_result;')
            self.emit_raw('    au_runtime_shutdown();')
            self.emit_raw('    return 0;')
            self.emit_raw('}')
        else:
            # 没有 main 函数,生成默认入口(执行顶层语句)
            self.emit_raw('int main(int argc, char** argv) {')
            self.emit_raw('    au_runtime_init();')
            self.emit_raw('    /* 顶层语句将被内联到这里 */')
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

    def gen_fn_def(self, fn: FnDef):
        """生成函数定义"""
        if fn.name == "main":
            self.has_main = True

        self.in_function = True
        params = ", ".join([f"AuValue {self.c_ident(p.name)}" for p in fn.params])
        if not params:
            params = "void"

        self.emit(f"AuValue {self.c_ident(fn.name)}({params}) {{")
        self.indent()

        # 函数体
        if fn.body:
            for stmt in fn.body.statements:
                self.gen_stmt(stmt)

        # 如果函数体最后一个语句不是 return,添加默认 return nil
        if fn.body and fn.body.statements:
            last = fn.body.statements[-1]
            if not isinstance(last, ReturnStmt):
                self.emit("return AU_NIL_VAL();")
        else:
            self.emit("return AU_NIL_VAL();")

        self.dedent()
        self.emit("}")
        self.emit("")
        self.in_function = False

    def gen_let_stmt(self, stmt: LetStmt):
        """生成 let/var 声明"""
        name = self.c_ident(stmt.name)
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
        """生成 if 语句"""
        cond = self.gen_expr(stmt.condition)
        self.emit(f"if (au_value_truthy({cond})) {{")
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
        """生成 while 循环"""
        cond = self.gen_expr(stmt.condition)
        self.emit(f"while (au_value_truthy({cond})) {{")
        self.indent()
        if stmt.body:
            for s in stmt.body.statements:
                self.gen_stmt(s)
        self.dedent()
        self.emit("}")

    def gen_return_stmt(self, stmt: ReturnStmt):
        """生成 return 语句"""
        if stmt.value:
            value = self.gen_expr(stmt.value)
            self.emit(f"return {value};")
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
        """生成表达式,返回 C 表达式字符串"""
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
                    from .lexer import Lexer
                    from .parser import Parser
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

    def gen_call_expr(self, expr: CallExpr) -> str:
        """生成函数调用"""
        callee_name = None
        if isinstance(expr.callee, Identifier):
            callee_name = expr.callee.name

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
    from .parser import Parser
    from .lexer import Lexer

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
                      optimize: str = "-O2", cc: str = "cc") -> tuple:
    """
    编译 Aurora 源代码为原生可执行文件。
    返回 (可执行文件路径, 编译输出)。
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
        from .parser import Parser
        from .lexer import Lexer
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

    # 编译命令
    rt_header = os.path.join(runtime_dir, "aurora_rt.h")
    rt_source = os.path.join(runtime_dir, "aurora_rt.c")

    cmd = [
        cc, optimize, "-Wall",
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
