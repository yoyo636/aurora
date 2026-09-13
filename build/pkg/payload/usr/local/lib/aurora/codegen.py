"""Aurora AOT 编译器 — 将 Aurora AST 编译为 Python 源码

支持核心语法子集:
  表达式:字面量、标识符、数组/Map、二元/一元运算、调用、方法调用、
        成员访问、索引、Lambda、If 表达式、字符串插值
  语句:let/var、表达式语句、return、if/elif/else、for、while、
        break/continue、赋值、函数定义、import、块
  程序:Program

不支持的高级语法(match/spawn/channel/select/try/defer/yield/
trait/impl/type/enum/destructure/pipe/range/ref 等)会生成
明确的运行时错误提示,建议使用解释器运行。
"""

import os
from typing import Any, Dict, List, Optional

from .ast_nodes import *


# 内建函数 → Python 映射
_BUILTIN_MAP = {
    'println': 'print',
    'print': 'print',
    'len': 'len',
    'str': 'str',
    'int': 'int',
    'float': 'float',
    'bool': 'bool',
    'range': 'range',
    'abs': 'abs',
    'min': 'min',
    'max': 'max',
    'sum': 'sum',
    'sorted': 'sorted',
    'reversed': 'reversed',
    'enumerate': 'enumerate',
    'zip': 'zip',
    'map': 'map',
    'filter': 'filter',
    'type': 'type',
    'isinstance': 'isinstance',
    'input': 'input',
    'read_line': 'input',
    'read_int': '_aurora_read_int',
    'read_float': '_aurora_read_float',
    'sleep': '_aurora_sleep',
    'assert': 'assert',
    'panic': '_aurora_panic',
}

# std 模块调用 → Python 代码模板(用 {args} 占位)
_STD_CALL_MAP = {
    ('std.io', 'read_file'): 'open({0}, encoding="utf-8").read()',
    ('std.io', 'write_file'): 'open({0}, "w", encoding="utf-8").write({1})',
    ('std.io', 'append_file'): 'open({0}, "a", encoding="utf-8").write({1})',
    ('std.io', 'exists'): 'os.path.exists({0})',
    ('std.io', 'is_dir'): 'os.path.isdir({0})',
    ('std.io', 'list_dir'): 'sorted(os.listdir({0}))',
    ('std.io', 'mkdir'): '_aurora_mkdir({0})',
    ('std.io', 'read_line'): 'input({0})',
    ('std.json', 'parse'): 'json.loads({0})',
    ('std.json', 'stringify'): 'json.dumps({0}, ensure_ascii=False)',
    ('std.json', 'load'): 'json.load(open({0}, encoding="utf-8"))',
    ('std.json', 'save'): 'json.dump({1}, open({0}, "w", encoding="utf-8"), ensure_ascii=False, indent=2)',
    ('std.math', 'sqrt'): 'math.sqrt({0})',
    ('std.math', 'floor'): 'math.floor({0})',
    ('std.math', 'ceil'): 'math.ceil({0})',
    ('std.math', 'round'): 'round({0})',
    ('std.math', 'abs'): 'abs({0})',
    ('std.math', 'min'): 'min({0})',
    ('std.math', 'max'): 'max({0})',
    ('std.math', 'pow'): 'pow({0}, {1})',
    ('std.math', 'sin'): 'math.sin({0})',
    ('std.math', 'cos'): 'math.cos({0})',
    ('std.math', 'tan'): 'math.tan({0})',
    ('std.math', 'log'): 'math.log({0})',
    ('std.math', 'random'): 'random.random()',
    ('std.math', 'randint'): 'random.randint({0}, {1})',
    ('std.str', 'split'): '{0}.split({1})',
    ('std.str', 'join'): '{1}.join({0})',
    ('std.str', 'replace'): '{0}.replace({1}, {2})',
    ('std.str', 'contains'): '{1} in {0}',
    ('std.str', 'upper'): '{0}.upper()',
    ('std.str', 'lower'): '{0}.lower()',
    ('std.str', 'trim'): '{0}.strip()',
    ('std.str', 'starts_with'): '{0}.startswith({1})',
    ('std.str', 'ends_with'): '{0}.endswith({1})',
    ('std.html', 'escape'): '_aurora_html_escape({0})',
    ('std.html', 'page'): '_aurora_html_page({0}, {1})',
    ('std.html', 'render'): '_aurora_html_render({0}, {1})',
    ('std.html', 'write'): '_aurora_html_write({0}, {1})',
    ('std.html', 'link'): '_aurora_html_link({0}, {1})',
    ('std.html', 'list'): '_aurora_html_list({0})',
    ('std.html', 'json_script'): '_aurora_html_json_script({0}, {1})',
}

# 运行时辅助函数(生成到编译产物顶部)
_RUNTIME_HELPERS = '''
# ── Aurora 运行时辅助(由编译器自动生成)──
import os, sys, json, math, random, html as _html_mod

def _aurora_read_int(prompt=""):
    return int(input(prompt))

def _aurora_read_float(prompt=""):
    return float(input(prompt))

def _aurora_sleep(ms):
    import time as _time
    _time.sleep(ms / 1000.0)

def _aurora_panic(msg=""):
    raise RuntimeError("panic: " + str(msg))

def _aurora_mkdir(path):
    if os.path.isdir(path):
        return False
    os.makedirs(path, exist_ok=True)
    return True

def _aurora_html_escape(s):
    return _html_mod.escape(str(s), quote=True)

def _aurora_html_page(title, body):
    return ("<!DOCTYPE html>\\n<html lang=\\"zh\\">\\n<head>\\n"
            "<meta charset=\\"utf-8\\">\\n<title>" + _html_mod.escape(str(title)) +
            "</title>\\n</head>\\n<body>\\n" + str(body) + "\\n</body>\\n</html>")

def _aurora_html_render(template, data):
    result = template
    for k, v in (data.items() if hasattr(data, "items") else []):
        result = result.replace("{{" + k + "}}", _html_mod.escape(str(v)))
        result = result.replace("{{!" + k + "}}", str(v))
    return result

def _aurora_html_write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def _aurora_html_link(href, text=None):
    t = text if text is not None else href
    return "<a href=\\"" + _html_mod.escape(str(href), quote=True) + "\\">" + _html_mod.escape(str(t)) + "</a>"

def _aurora_html_list(items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "".join("<li>" + _html_mod.escape(str(x)) + "</li>" for x in items)
    return "<" + tag + ">" + lis + "</" + tag + ">"

def _aurora_html_json_script(data, id="aurora-data"):
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\\\/")
    return "<script id=\\"" + str(id) + "\\" type=\\"application/json\\">" + payload + "</script>"

class _AuroraResult:
    def __init__(self, ok, value=None, error=None):
        self.ok = ok
        self.value = value
        self.error = error
    def is_ok(self):
        return self.ok
    def unwrap(self):
        if self.ok:
            return self.value
        raise RuntimeError("unwrap on Err: " + str(self.error))

def _aurora_ok(v):
    return _AuroraResult(True, value=v)

def _aurora_err(e):
    return _AuroraResult(False, error=e)

'''


class CodeGenerator:
    """Aurora AST → Python 源码 生成器"""

    def __init__(self):
        self._indent = 0
        self._imported_std: set = set()   # 记录用到的 std 模块(决定 import 哪些)
        self._needs_runtime = False        # 是否需要运行时辅助
        self._local_imports: List[str] = []  # 本地模块 import

    # ── 主入口 ──────────────────────────────────────

    def generate(self, program: Program) -> str:
        """生成完整 Python 源码"""
        body_lines = []
        for stmt in program.statements:
            code = self.gen_stmt(stmt)
            if code:
                body_lines.append(code)

        # 组装
        parts = []
        parts.append("# Generated by Aurora compiler — do not edit")
        parts.append("")
        if self._imported_std or self._needs_runtime:
            parts.append(_RUNTIME_HELPERS)
        if self._local_imports:
            for mod in self._local_imports:
                parts.append(f"import {mod}")
            parts.append("")
        parts.extend(body_lines)
        return "\n".join(parts) + "\n"

    # ── 缩进工具 ────────────────────────────────────

    def _ind(self, code: str) -> str:
        return "    " * self._indent + code

    def _block(self, stmts) -> str:
        """接受 Block 对象或语句列表"""
        if isinstance(stmts, Block):
            stmts = stmts.statements
        self._indent += 1
        lines = []
        for s in stmts:
            c = self.gen_stmt(s)
            if c:
                lines.append(c)
        self._indent -= 1
        if not lines:
            lines.append(self._ind("pass"))
        return "\n".join(lines)

    def _block_last_expr(self, block) -> str:
        """从 Block 中取最后一个表达式作为值(用于 if 表达式)"""
        if isinstance(block, Block):
            stmts = block.statements
        else:
            stmts = block
        if not stmts:
            return "None"
        last = stmts[-1]
        if isinstance(last, ExprStmt):
            return self.gen_expr(last.expr)
        if isinstance(last, ReturnStmt) and last.value:
            return self.gen_expr(last.value)
        # 非表达式语句:用 lambda 包装执行
        self._indent += 1
        body = self._block(stmts)
        self._indent -= 1
        return "(lambda: (" + body.replace("\n", "; ") + ", None)[-1])()"

    def _gen_match(self, expr: MatchExpr) -> str:
        """match 表达式 → Python lambda + if/elif 链"""
        subject = self.gen_expr(expr.subject)
        # 构建嵌套三元表达式:val1 if cond1 else val2 if cond2 else default
        result = None
        for arm in reversed(expr.arms):
            body = self.gen_expr(arm.body)
            pat = arm.pattern
            if isinstance(pat, WildcardPattern):
                result = body
            elif isinstance(pat, LiteralPattern):
                cond = "_m == " + self.gen_expr(pat.value)
                result = body + " if " + cond + " else " + (result if result else "None")
            elif isinstance(pat, BindPattern):
                # 绑定模式:总是匹配,_m 即绑定值
                result = body
            elif isinstance(pat, ConstructorPattern):
                # 构造器模式:简化为类型检查
                cond = "isinstance(_m, tuple) and _m and _m[0] == " + repr(pat.name)
                result = body + " if " + cond + " else " + (result if result else "None")
            else:
                result = body
        if result is None:
            result = "None"
        return "(lambda _m: " + result + ")(" + subject + ")"

    def _gen_match_stmt(self, stmt: MatchStmt) -> str:
        """match 语句 → Python if/elif 链"""
        var_name = "_match_" + str(id(stmt))[-6:]
        lines = [self._ind(var_name + " = " + self.gen_expr(stmt.subject))]
        first = True
        for arm in stmt.arms:
            pat = arm.pattern
            body_code = self.gen_expr(arm.body)
            if isinstance(pat, WildcardPattern):
                lines.append(self._ind("else:"))
            elif isinstance(pat, LiteralPattern):
                kw = "if" if first else "elif"
                lines.append(self._ind(kw + " " + var_name + " == " + self.gen_expr(pat.value) + ":"))
                first = False
            elif isinstance(pat, BindPattern):
                lines.append(self._ind("else:"))
            else:
                kw = "if" if first else "elif"
                lines.append(self._ind(kw + " True:"))
                first = False
            lines.append(self._ind("    " + body_code))
        return "\n".join(lines)

    # ── 语句生成 ────────────────────────────────────

    def gen_stmt(self, stmt: Stmt) -> str:
        if isinstance(stmt, FnDef):
            return self._gen_fn_def(stmt)
        if isinstance(stmt, LetStmt):
            return self._gen_let(stmt)
        if isinstance(stmt, ConstStmt):
            return self._gen_let(stmt)  # const 同 let(Python 无常量)
        if isinstance(stmt, ExprStmt):
            return self._ind(self.gen_expr(stmt.expr))
        if isinstance(stmt, ReturnStmt):
            if stmt.value:
                return self._ind("return " + self.gen_expr(stmt.value))
            return self._ind("return")
        if isinstance(stmt, IfStmt):
            return self._gen_if_stmt(stmt)
        if isinstance(stmt, ForStmt):
            return self._gen_for(stmt)
        if isinstance(stmt, WhileStmt):
            return self._ind("while " + self.gen_expr(stmt.condition) + ":") + "\n" + self._block(stmt.body)
        if isinstance(stmt, BreakStmt):
            return self._ind("break")
        if isinstance(stmt, ContinueStmt):
            return self._ind("continue")
        if isinstance(stmt, AssignStmt):
            return self._ind(self.gen_expr(stmt.target) + " = " + self.gen_expr(stmt.value))
        if isinstance(stmt, ImportStmt):
            return self._gen_import(stmt)
        if isinstance(stmt, Block):
            return self._block(stmt.statements)
        if isinstance(stmt, MatchStmt):
            return self._gen_match_stmt(stmt)
        # 不支持的语句:生成运行时错误
        return self._ind(f'raise NotImplementedError("Aurora 编译器暂不支持语句: {type(stmt).__name__},请使用解释器运行")')

    def _gen_let(self, stmt: LetStmt) -> str:
        # let x = expr  →  x = expr
        # let x: Type = expr  →  x = expr(Python 动态类型)
        if stmt.initializer:
            return self._ind(stmt.name + " = " + self.gen_expr(stmt.initializer))
        return self._ind(stmt.name + " = None")

    def _gen_fn_def(self, stmt: FnDef) -> str:
        params = ", ".join(p.name for p in stmt.params)
        header = self._ind(f"def {stmt.name}({params}):")
        # 表达式导向:函数体最后一个表达式即返回值
        body_stmts = stmt.body.statements if isinstance(stmt.body, Block) else stmt.body
        processed = []
        for i, s in enumerate(body_stmts):
            if i == len(body_stmts) - 1:
                if isinstance(s, ExprStmt):
                    processed.append(ReturnStmt(value=s.expr))
                elif isinstance(s, MatchStmt):
                    # 函数末尾的 match 语句 → 转为 match 表达式返回
                    me = MatchExpr(subject=s.subject, arms=s.arms)
                    processed.append(ReturnStmt(value=me))
                else:
                    processed.append(s)
            else:
                processed.append(s)
        fake_block = Block(statements=processed)
        body = self._block(fake_block)
        return header + "\n" + body

    def _gen_if_stmt(self, stmt: IfStmt) -> str:
        lines = [self._ind("if " + self.gen_expr(stmt.condition) + ":")]
        lines.append(self._block(stmt.then_body))
        for cond, body in (stmt.elif_clauses or []):
            lines.append(self._ind("elif " + self.gen_expr(cond) + ":"))
            lines.append(self._block(body))
        if stmt.else_body:
            lines.append(self._ind("else:"))
            lines.append(self._block(stmt.else_body))
        return "\n".join(lines)

    def _gen_for(self, stmt: ForStmt) -> str:
        var_name = stmt.variables[0] if stmt.variables else "x"
        iterable = self.gen_expr(stmt.iterable)
        header = self._ind(f"for {var_name} in {iterable}:")
        return header + "\n" + self._block(stmt.body)

    def _gen_import(self, stmt: ImportStmt) -> str:
        path = ".".join(stmt.path)
        if path.startswith("std."):
            # std 模块:标记需要运行时,不生成 import(运行时辅助已内联)
            self._needs_runtime = True
            self._imported_std.add(path)
            return ""
        # 本地模块:import 模块名
        mod_name = "_".join(stmt.path)
        if stmt.alias:
            self._local_imports.append(f"{mod_name} as {stmt.alias}")
        else:
            self._local_imports.append(mod_name)
        return ""

    # ── 表达式生成 ──────────────────────────────────

    def gen_expr(self, expr: Expr) -> str:
        if isinstance(expr, IntLiteral):
            return str(expr.value)
        if isinstance(expr, FloatLiteral):
            return str(expr.value)
        if isinstance(expr, StringLiteral):
            return self._gen_string(expr.value)
        if isinstance(expr, BoolLiteral):
            return "True" if expr.value else "False"
        if isinstance(expr, NilLiteral):
            return "None"
        if isinstance(expr, Identifier):
            return self._map_identifier(expr.name)
        if isinstance(expr, ArrayLiteral):
            items = ", ".join(self.gen_expr(e) for e in expr.elements)
            return "[" + items + "]"
        if isinstance(expr, MapLiteral):
            pairs = ", ".join(
                self.gen_expr(k) + ": " + self.gen_expr(v)
                for k, v in expr.entries
            )
            return "{" + pairs + "}"
        if isinstance(expr, TupleLiteral):
            items = ", ".join(self.gen_expr(e) for e in expr.elements)
            return "(" + items + ")"
        if isinstance(expr, BinaryOp):
            return self._gen_binary(expr)
        if isinstance(expr, UnaryOp):
            op = expr.op
            if op == "!":
                op = "not "
            elif op == "-":
                op = "-"
            return "(" + op + self.gen_expr(expr.operand) + ")"
        if isinstance(expr, CallExpr):
            return self._gen_call(expr)
        if isinstance(expr, MethodCall):
            return self._gen_method_call(expr)
        if isinstance(expr, MemberAccess):
            return self.gen_expr(expr.object) + "." + expr.member
        if isinstance(expr, IndexAccess):
            return self.gen_expr(expr.object) + "[" + self.gen_expr(expr.index) + "]"
        if isinstance(expr, LambdaExpr):
            params = ", ".join(p.name for p in expr.params)
            return "(lambda " + params + ": " + self.gen_expr(expr.body) + ")"
        if isinstance(expr, IfExpr):
            # if c { a } else { b }  →  (a if c else b)
            cond = self.gen_expr(expr.condition)
            then_v = self._block_last_expr(expr.then_body)
            else_v = self._block_last_expr(expr.else_body) if expr.else_body else "None"
            return "(" + then_v + " if " + cond + " else " + else_v + ")"
        if isinstance(expr, MatchExpr):
            return self._gen_match(expr)
        if isinstance(expr, StringInterpolation):
            return self._gen_interpolation(expr)
        # 不支持的表达式
        return f'_aurora_unsupported_expr("{type(expr).__name__}")'

    def _map_identifier(self, name: str) -> str:
        return _BUILTIN_MAP.get(name, name)

    def _gen_string(self, value: str) -> str:
        # 生成 Python 字符串字面量,处理转义
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
        return '"' + escaped + '"'

    def _gen_interpolation(self, expr: StringInterpolation) -> str:
        # 字符串插值 "hello {name}" → f"hello {name}"
        parts = []
        for part in expr.parts:
            if isinstance(part, str):
                parts.append(part.replace("{", "{{").replace("}", "}}"))
            else:
                parts.append("{" + self.gen_expr(part) + "}")
        return 'f"' + "".join(parts) + '"'

    def _gen_binary(self, expr: BinaryOp) -> str:
        op = expr.op
        # Aurora 运算符 → Python
        op_map = {
            "and": "and", "or": "or", "not": "not",
            "&&": "and", "||": "or", "!": "not",
            "==": "==", "!=": "!=", "<": "<", ">": ">",
            "<=": "<=", ">=": ">=",
            "+": "+", "-": "-", "*": "*", "/": "/",
            "%": "%", "**": "**",
        }
        py_op = op_map.get(op, op)
        left = self.gen_expr(expr.left)
        right = self.gen_expr(expr.right)
        return "(" + left + " " + py_op + " " + right + ")"

    def _gen_call(self, expr: CallExpr) -> str:
        callee = expr.callee
        # 检查是否是 std 模块调用:std.io.read_file(...)
        if isinstance(callee, MemberAccess):
            result = self._try_std_call(callee, expr.args)
            if result is not None:
                return result
            # 普通成员调用:obj.method(args)
            obj = self.gen_expr(callee.object)
            method = callee.member
            args = ", ".join(self.gen_expr(a) for a in expr.args)
            # 内建方法映射
            method_map = {
                'len': 'len({obj})',
                'push': '{obj}.append({args})',
                'pop': '{obj}.pop()',
                'contains': '{args} in {obj}',
                'keys': 'list({obj}.keys())',
                'values': 'list({obj}.values())',
                'items': 'list({obj}.items())',
                'sort': '{obj}.sort()',
                'reverse': '{obj}.reverse()',
                'upper': '{obj}.upper()',
                'lower': '{obj}.lower()',
                'trim': '{obj}.strip()',
                'split': '{obj}.split({args})',
                'replace': '{obj}.replace({args})',
                'starts_with': '{obj}.startswith({args})',
                'ends_with': '{obj}.endswith({args})',
                'to_string': 'str({obj})',
                'to_int': 'int({obj})',
                'to_float': 'float({obj})',
            }
            if method in method_map:
                return method_map[method].format(obj=obj, args=args)
            return obj + "." + method + "(" + args + ")"

        # 普通函数调用
        if isinstance(callee, Identifier):
            name = self._map_identifier(callee.name)
        else:
            name = self.gen_expr(callee)
        args = ", ".join(self.gen_expr(a) for a in expr.args)
        return name + "(" + args + ")"

    def _try_std_call(self, callee: MemberAccess, args: List[Expr]) -> Optional[str]:
        """尝试将 std 模块调用翻译为 Python 原生代码"""
        # 构建模块路径:std.io.read_file → ("std.io", "read_file")
        parts = []
        node = callee
        while isinstance(node, MemberAccess):
            parts.append(node.member)
            node = node.object
        if isinstance(node, Identifier):
            parts.append(node.name)
        parts.reverse()
        if len(parts) >= 3 and parts[0] == "std":
            module = ".".join(parts[:-1])  # std.io
            func = parts[-1]                 # read_file
            key = (module, func)
            if key in _STD_CALL_MAP:
                self._needs_runtime = True
                self._imported_std.add(module)
                arg_strs = [self.gen_expr(a) for a in args]
                template = _STD_CALL_MAP[key]
                # 填充 {0}, {1} 占位
                try:
                    return template.format(*arg_strs)
                except (IndexError, KeyError):
                    pass
        return None

    def _gen_method_call(self, expr: MethodCall) -> str:
        # expr.method(args) — 同 CallExpr with MemberAccess callee
        obj = self.gen_expr(expr.object)
        args = ", ".join(self.gen_expr(a) for a in expr.args)
        return obj + "." + expr.method + "(" + args + ")"


def compile_program(program: Program) -> str:
    """便捷函数:编译 Program 为 Python 源码"""
    gen = CodeGenerator()
    return gen.generate(program)


def compile_file(source_path: str, output_path: str) -> str:
    """编译 .aur 文件为 .py 文件,返回输出路径"""
    from .lexer import Lexer
    from .parser import Parser

    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    py_code = compile_program(program)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(py_code)
    return output_path
