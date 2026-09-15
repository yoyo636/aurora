"""
Aurora 类型推断器
分析 AST,推断函数参数类型、返回值类型和变量类型。
用于代码生成器的类型特化优化。
"""
from .ast_nodes import *
from enum import Enum


class TypeKind(Enum):
    UNKNOWN = "unknown"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    ARRAY = "array"
    MAP = "map"
    TUPLE = "tuple"
    NIL = "nil"
    OPTIONAL = "optional"


class InferType:
    """推断出的类型"""
    def __init__(self, kind=TypeKind.UNKNOWN, elem_type=None, tuple_types=None):
        self.kind = kind
        self.elem_type = elem_type  # 用于 ARRAY 的元素类型
        # 用于 TUPLE 的元素类型列表；OPTIONAL 时 elem_type 为内部类型
        self.tuple_types = tuple_types or []

    def is_int(self):
        return self.kind == TypeKind.INT

    def is_float(self):
        return self.kind == TypeKind.FLOAT

    def is_bool(self):
        return self.kind == TypeKind.BOOL

    def is_string(self):
        return self.kind == TypeKind.STRING

    def is_numeric(self):
        return self.kind in (TypeKind.INT, TypeKind.FLOAT)

    def is_known(self):
        return self.kind != TypeKind.UNKNOWN

    def __repr__(self):
        if self.kind == TypeKind.ARRAY and self.elem_type:
            return f"[{self.elem_type}]"
        if self.kind == TypeKind.TUPLE:
            return "(" + ", ".join(repr(t) for t in self.tuple_types) + ")"
        if self.kind == TypeKind.OPTIONAL and self.elem_type:
            return f"{self.elem_type}?"
        return self.kind.value


# 常用类型常量
TYPE_UNKNOWN = InferType(TypeKind.UNKNOWN)
TYPE_INT = InferType(TypeKind.INT)
TYPE_FLOAT = InferType(TypeKind.FLOAT)
TYPE_BOOL = InferType(TypeKind.BOOL)
TYPE_STRING = InferType(TypeKind.STRING)
TYPE_NIL = InferType(TypeKind.NIL)


def merge_types(t1: InferType, t2: InferType) -> InferType:
    """合并两个类型,如果一致返回该类型,否则返回 UNKNOWN"""
    if t1.kind == TypeKind.UNKNOWN:
        return t2
    if t2.kind == TypeKind.UNKNOWN:
        return t1
    if t1.kind == t2.kind:
        # 数组需要检查元素类型
        if t1.kind == TypeKind.ARRAY:
            elem = merge_types(t1.elem_type or TYPE_UNKNOWN, t2.elem_type or TYPE_UNKNOWN)
            return InferType(TypeKind.ARRAY, elem)
        # 元组逐元素合并
        if t1.kind == TypeKind.TUPLE and len(t1.tuple_types) == len(t2.tuple_types):
            merged = [merge_types(a, b) for a, b in zip(t1.tuple_types, t2.tuple_types)]
            return InferType(TypeKind.TUPLE, tuple_types=merged)
        # 可选类型合并内部类型
        if t1.kind == TypeKind.OPTIONAL:
            inner = merge_types(t1.elem_type or TYPE_UNKNOWN, t2.elem_type or TYPE_UNKNOWN)
            return InferType(TypeKind.OPTIONAL, inner)
        return t1
    # 可选类型与内部类型合并为内部类型（解包语义）
    if t1.kind == TypeKind.OPTIONAL and t2.kind != TypeKind.OPTIONAL:
        return merge_types(t1.elem_type or TYPE_UNKNOWN, t2)
    if t2.kind == TypeKind.OPTIONAL and t1.kind != TypeKind.OPTIONAL:
        return merge_types(t1, t2.elem_type or TYPE_UNKNOWN)
    # int 和 float 合并为 float
    if t1.is_numeric() and t2.is_numeric():
        return TYPE_FLOAT
    return TYPE_UNKNOWN


class TypeInferer:
    """类型推断器"""

    def __init__(self, program: Program):
        self.program = program
        self.functions = {}  # name -> FnDef
        self.function_types = {}  # name -> {'params': [InferType], 'return': InferType}
        self.variable_types = {}  # 函数名 -> {变量名: InferType}
        self.current_function = None

    def infer(self) -> dict:
        """执行类型推断,返回函数类型信息"""
        # 收集所有函数定义
        for stmt in self.program.statements:
            if isinstance(stmt, FnDef):
                self.functions[stmt.name] = stmt

        # 初始化所有函数类型为 UNKNOWN
        for name in self.functions:
            fn = self.functions[name]
            self.function_types[name] = {
                'params': [TYPE_UNKNOWN] * len(fn.params),
                'return': TYPE_UNKNOWN,
            }

        # 第一轮:从调用点推断参数类型
        self._infer_call_sites()

        # 迭代求解(处理递归函数)
        for iteration in range(10):  # 最多迭代 10 次
            changed = False
            for name in self.functions:
                if self._infer_function(name):
                    changed = True
            # 每轮后重新从调用点推断
            self._infer_call_sites()
            if not changed:
                break

        return self.function_types

    def _infer_call_sites(self):
        """从所有调用点推断函数参数类型"""
        for stmt in self.program.statements:
            if isinstance(stmt, FnDef):
                self.current_function = stmt.name
                self.variable_types[stmt.name] = {}
                for i, param in enumerate(stmt.params):
                    self.variable_types[stmt.name][param.name] = self.function_types[stmt.name]['params'][i]
                if stmt.body:
                    self._infer_call_sites_in_block(stmt.body)

    def _infer_call_sites_in_block(self, block: Block):
        """在代码块中查找调用点并推断参数类型"""
        for stmt in block.statements:
            self._infer_call_sites_in_stmt(stmt)

    def _infer_call_sites_in_stmt(self, stmt: Stmt):
        """在语句中查找调用点"""
        if isinstance(stmt, (LetStmt, ConstStmt)) and stmt.initializer:
            self._infer_call_sites_in_expr(stmt.initializer)
        elif isinstance(stmt, AssignStmt):
            self._infer_call_sites_in_expr(stmt.value)
        elif isinstance(stmt, IfStmt):
            self._infer_call_sites_in_expr(stmt.condition)
            if stmt.then_body:
                self._infer_call_sites_in_block(stmt.then_body)
            for cond, body in stmt.elif_clauses:
                self._infer_call_sites_in_expr(cond)
                if body:
                    self._infer_call_sites_in_block(body)
            if stmt.else_body:
                self._infer_call_sites_in_block(stmt.else_body)
        elif isinstance(stmt, ForStmt):
            self._infer_call_sites_in_expr(stmt.iterable)
            if stmt.body:
                self._infer_call_sites_in_block(stmt.body)
        elif isinstance(stmt, WhileStmt):
            self._infer_call_sites_in_expr(stmt.condition)
            if stmt.body:
                self._infer_call_sites_in_block(stmt.body)
        elif isinstance(stmt, ReturnStmt) and stmt.value:
            self._infer_call_sites_in_expr(stmt.value)
        elif isinstance(stmt, ExprStmt):
            self._infer_call_sites_in_expr(stmt.expr)
        elif isinstance(stmt, Block):
            self._infer_call_sites_in_block(stmt)

    def _infer_call_sites_in_expr(self, expr: Expr):
        """在表达式中查找调用点并推断参数类型"""
        if isinstance(expr, CallExpr):
            if isinstance(expr.callee, Identifier):
                func_name = expr.callee.name
                if func_name in self.function_types:
                    for i, arg in enumerate(expr.args):
                        if i < len(self.function_types[func_name]['params']):
                            arg_type = self._infer_expr(arg)
                            old_type = self.function_types[func_name]['params'][i]
                            merged = merge_types(old_type, arg_type)
                            self.function_types[func_name]['params'][i] = merged
            # 递归处理参数
            for arg in expr.args:
                self._infer_call_sites_in_expr(arg)
        elif isinstance(expr, BinaryOp):
            self._infer_call_sites_in_expr(expr.left)
            self._infer_call_sites_in_expr(expr.right)
        elif isinstance(expr, UnaryOp):
            self._infer_call_sites_in_expr(expr.operand)
        elif isinstance(expr, MethodCall):
            self._infer_call_sites_in_expr(expr.object)
            for arg in expr.args:
                self._infer_call_sites_in_expr(arg)
        elif isinstance(expr, IndexAccess):
            self._infer_call_sites_in_expr(expr.object)
            self._infer_call_sites_in_expr(expr.index)
        elif isinstance(expr, IfExpr):
            self._infer_call_sites_in_expr(expr.condition)
            if expr.then_body:
                self._infer_call_sites_in_block(expr.then_body)
            if expr.else_body:
                self._infer_call_sites_in_block(expr.else_body)
        elif isinstance(expr, ArrayLiteral):
            for elem in expr.elements:
                self._infer_call_sites_in_expr(elem)
        elif isinstance(expr, MapLiteral):
            for key, value in expr.entries:
                self._infer_call_sites_in_expr(key)
                self._infer_call_sites_in_expr(value)
        elif isinstance(expr, TupleLiteral):
            for elem in expr.elements:
                self._infer_call_sites_in_expr(elem)
        elif isinstance(expr, (ListComp, SetComp)):
            self._infer_call_sites_in_expr(expr.expr)
            for gen in expr.generators:
                self._infer_call_sites_in_expr(gen.iterable)
            for cond in expr.conditions:
                self._infer_call_sites_in_expr(cond)
        elif isinstance(expr, MapComp):
            self._infer_call_sites_in_expr(expr.key_expr)
            self._infer_call_sites_in_expr(expr.value_expr)
            for gen in expr.generators:
                self._infer_call_sites_in_expr(gen.iterable)
            for cond in expr.conditions:
                self._infer_call_sites_in_expr(cond)
        elif isinstance(expr, StructLiteral):
            for _, value in expr.fields:
                self._infer_call_sites_in_expr(value)
        elif isinstance(expr, (ForcedUnwrap, TupleIndex)):
            self._infer_call_sites_in_expr(expr.operand if isinstance(expr, ForcedUnwrap) else expr.object)
        elif isinstance(expr, MatchExpr):
            self._infer_call_sites_in_expr(expr.subject)
            for arm in expr.arms:
                self._infer_call_sites_in_expr(arm.body)
        elif isinstance(expr, PipeExpr):
            self._infer_call_sites_in_expr(expr.left)
            self._infer_call_sites_in_expr(expr.call)

    def _infer_function(self, name: str) -> bool:
        """推断单个函数的类型,返回是否有变化"""
        fn = self.functions[name]
        self.current_function = name
        self.variable_types[name] = {}

        # 参数类型初始化为已知的(从之前的迭代)
        for i, param in enumerate(fn.params):
            self.variable_types[name][param.name] = self.function_types[name]['params'][i]

        # 推断函数体
        return_type = TYPE_UNKNOWN
        if fn.body:
            return_type = self._infer_block(fn.body)

        # 函数体最后一个表达式也是返回值(如果没有 return)
        if fn.body and fn.body.statements:
            last = fn.body.statements[-1]
            if isinstance(last, ExprStmt):
                expr_type = self._infer_expr(last.expr)
                return_type = merge_types(return_type, expr_type)

        # 更新返回类型
        old_return = self.function_types[name]['return']
        new_return = merge_types(old_return, return_type)
        self.function_types[name]['return'] = new_return

        # 更新参数类型(从变量类型中提取)
        changed = (new_return.kind != old_return.kind)
        for i, param in enumerate(fn.params):
            old_param = self.function_types[name]['params'][i]
            new_param = self.variable_types[name].get(param.name, TYPE_UNKNOWN)
            merged = merge_types(old_param, new_param)
            self.function_types[name]['params'][i] = merged
            if merged.kind != old_param.kind:
                changed = True

        return changed

    def _infer_block(self, block: Block) -> InferType:
        """推断代码块的返回类型(最后一个 return 语句)"""
        return_type = TYPE_UNKNOWN
        for stmt in block.statements:
            t = self._infer_stmt(stmt)
            if t is not None:
                return_type = merge_types(return_type, t)
        return return_type

    def _infer_stmt(self, stmt: Stmt) -> InferType:
        """推断语句,返回该语句产生的返回值类型(如果有)"""
        if isinstance(stmt, LetStmt) or isinstance(stmt, ConstStmt):
            if stmt.initializer:
                t = self._infer_expr(stmt.initializer)
                self.variable_types[self.current_function][stmt.name] = t
            return None

        elif isinstance(stmt, AssignStmt):
            value_type = self._infer_expr(stmt.value)
            if isinstance(stmt.target, Identifier):
                old_type = self.variable_types[self.current_function].get(stmt.target.name, TYPE_UNKNOWN)
                merged = merge_types(old_type, value_type)
                self.variable_types[self.current_function][stmt.target.name] = merged
            return None

        elif isinstance(stmt, IfStmt):
            return_type = TYPE_UNKNOWN
            # then 分支
            if stmt.then_body:
                t = self._infer_block(stmt.then_body)
                return_type = merge_types(return_type, t)
            # elif 分支
            for cond, body in stmt.elif_clauses:
                self._infer_expr(cond)
                if body:
                    t = self._infer_block(body)
                    return_type = merge_types(return_type, t)
            # else 分支
            if stmt.else_body:
                t = self._infer_block(stmt.else_body)
                return_type = merge_types(return_type, t)
            return return_type

        elif isinstance(stmt, ForStmt):
            self._infer_expr(stmt.iterable)
            # 循环变量类型
            iter_type = self._infer_expr(stmt.iterable)
            for var in stmt.variables:
                if iter_type.kind == TypeKind.ARRAY:
                    self.variable_types[self.current_function][var] = iter_type.elem_type or TYPE_UNKNOWN
                else:
                    self.variable_types[self.current_function][var] = TYPE_UNKNOWN
            if stmt.body:
                return self._infer_block(stmt.body)
            return None

        elif isinstance(stmt, WhileStmt):
            self._infer_expr(stmt.condition)
            if stmt.body:
                return self._infer_block(stmt.body)
            return None

        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                return self._infer_expr(stmt.value)
            return TYPE_NIL

        elif isinstance(stmt, ExprStmt):
            self._infer_expr(stmt.expr)
            return None

        elif isinstance(stmt, Block):
            return self._infer_block(stmt)

        return None

    def _infer_expr(self, expr: Expr) -> InferType:
        """推断表达式的类型"""
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
            return self.variable_types[self.current_function].get(expr.name, TYPE_UNKNOWN)

        elif isinstance(expr, BinaryOp):
            left_type = self._infer_expr(expr.left)
            right_type = self._infer_expr(expr.right)

            # 类型传播:如果一边是已知数值类型,另一边是 unknown 的 Identifier,更新其类型
            self._propagate_numeric_type(expr.left, left_type, right_type)
            self._propagate_numeric_type(expr.right, right_type, left_type)

            # 比较运算返回 bool
            if expr.op in ('==', '!=', '<', '<=', '>', '>='):
                return TYPE_BOOL

            # 逻辑运算返回 bool
            if expr.op in ('&&', '||'):
                return TYPE_BOOL

            # 字符串拼接
            if expr.op == '+' and (left_type.is_string() or right_type.is_string()):
                return TYPE_STRING

            # 字符串重复
            if expr.op == '*' and (left_type.is_string() or right_type.is_string()):
                return TYPE_STRING

            # 数组合并
            if expr.op == '+' and left_type.kind == TypeKind.ARRAY and right_type.kind == TypeKind.ARRAY:
                elem = merge_types(left_type.elem_type or TYPE_UNKNOWN, right_type.elem_type or TYPE_UNKNOWN)
                return InferType(TypeKind.ARRAY, elem)

            # 数值运算
            if left_type.is_numeric() and right_type.is_numeric():
                if left_type.is_float() or right_type.is_float():
                    return TYPE_FLOAT
                return TYPE_INT

            # 幂运算
            if expr.op == '**':
                if left_type.is_int() and right_type.is_int():
                    return TYPE_INT
                if left_type.is_numeric() and right_type.is_numeric():
                    return TYPE_FLOAT

            return TYPE_UNKNOWN

        elif isinstance(expr, UnaryOp):
            operand_type = self._infer_expr(expr.operand)
            if expr.op == '-':
                return operand_type
            if expr.op == '!':
                return TYPE_BOOL
            if expr.op == '#':
                return TYPE_INT
            return operand_type

        elif isinstance(expr, CallExpr):
            # 函数调用
            if isinstance(expr.callee, Identifier):
                func_name = expr.callee.name
                # 内置函数
                builtin_returns = {
                    'len': TYPE_INT,
                    'range': InferType(TypeKind.ARRAY, TYPE_INT),
                    'now_ms': TYPE_INT,
                    'sleep_ms': TYPE_NIL,
                    'sqrt': TYPE_FLOAT,
                    'abs': TYPE_INT,  # 可能是 float,简化为 int
                    'sin': TYPE_FLOAT,
                    'cos': TYPE_FLOAT,
                    'tan': TYPE_FLOAT,
                    'log': TYPE_FLOAT,
                    'exp': TYPE_FLOAT,
                    'floor': TYPE_INT,
                    'ceil': TYPE_INT,
                    'round': TYPE_INT,
                    'min': TYPE_INT,
                    'max': TYPE_INT,
                    'gcd': TYPE_INT,
                    'lcm': TYPE_INT,
                    'is_prime': TYPE_BOOL,
                    'factorial': TYPE_INT,
                    'fibonacci': TYPE_INT,
                    'type': TYPE_STRING,
                    'to_string': TYPE_STRING,
                    'read_line': TYPE_STRING,
                    'read_file': TYPE_STRING,
                    'file_exists': TYPE_BOOL,
                    'get_env': TYPE_STRING,
                    'json_parse': TYPE_UNKNOWN,
                    'json_stringify': TYPE_STRING,
                }
                if func_name in builtin_returns:
                    return builtin_returns[func_name]

                # 用户定义函数
                if func_name in self.function_types:
                    return self.function_types[func_name]['return']

            return TYPE_UNKNOWN

        elif isinstance(expr, MethodCall):
            obj_type = self._infer_expr(expr.object)
            method = expr.method
            # 字符串方法
            if obj_type.is_string():
                string_returns = {
                    'len': TYPE_INT,
                    'to_lower': TYPE_STRING,
                    'to_upper': TYPE_STRING,
                    'trim': TYPE_STRING,
                    'contains': TYPE_BOOL,
                    'starts_with': TYPE_BOOL,
                    'ends_with': TYPE_BOOL,
                    'to_int': TYPE_INT,
                    'to_float': TYPE_FLOAT,
                }
                return string_returns.get(method, TYPE_UNKNOWN)
            # 数组方法
            if obj_type.kind == TypeKind.ARRAY:
                array_returns = {
                    'len': TYPE_INT,
                    'pop': obj_type.elem_type or TYPE_UNKNOWN,
                    'contains': TYPE_BOOL,
                    'reverse': obj_type,
                    'sort': obj_type,
                }
                return array_returns.get(method, TYPE_UNKNOWN)
            # Map 方法
            if obj_type.kind == TypeKind.MAP:
                map_returns = {
                    'len': TYPE_INT,
                    'has': TYPE_BOOL,
                    'keys': InferType(TypeKind.ARRAY, TYPE_STRING),
                    'values': InferType(TypeKind.ARRAY, TYPE_UNKNOWN),
                }
                return map_returns.get(method, TYPE_UNKNOWN)
            return TYPE_UNKNOWN

        elif isinstance(expr, ArrayLiteral):
            if expr.elements:
                elem_type = self._infer_expr(expr.elements[0])
                for elem in expr.elements[1:]:
                    elem_type = merge_types(elem_type, self._infer_expr(elem))
                return InferType(TypeKind.ARRAY, elem_type)
            return InferType(TypeKind.ARRAY, TYPE_UNKNOWN)

        elif isinstance(expr, MapLiteral):
            return InferType(TypeKind.MAP)

        elif isinstance(expr, IndexAccess):
            obj_type = self._infer_expr(expr.object)
            if obj_type.kind == TypeKind.ARRAY:
                return obj_type.elem_type or TYPE_UNKNOWN
            if obj_type.kind == TypeKind.MAP:
                return TYPE_UNKNOWN
            if obj_type.is_string():
                return TYPE_STRING
            return TYPE_UNKNOWN

        elif isinstance(expr, IfExpr):
            self._infer_expr(expr.condition)
            then_type = TYPE_UNKNOWN
            else_type = TYPE_UNKNOWN
            if expr.then_body:
                then_type = self._infer_block(expr.then_body)
            if expr.else_body:
                else_type = self._infer_block(expr.else_body)
            return merge_types(then_type, else_type)

        elif isinstance(expr, RangeExpr):
            return InferType(TypeKind.ARRAY, TYPE_INT)

        elif isinstance(expr, PipeExpr):
            left_type = self._infer_expr(expr.left)
            # 管道右侧是函数调用,返回函数的返回类型
            if isinstance(expr.call, CallExpr) and isinstance(expr.call.callee, Identifier):
                func_name = expr.call.callee.name
                if func_name in self.function_types:
                    return self.function_types[func_name]['return']
            if isinstance(expr.call, Identifier):
                func_name = expr.call.name
                if func_name in self.function_types:
                    return self.function_types[func_name]['return']
            return TYPE_UNKNOWN

        elif isinstance(expr, StringInterpolation):
            return TYPE_STRING

        elif isinstance(expr, MatchExpr):
            self._infer_expr(expr.subject)
            result_type = TYPE_UNKNOWN
            for arm in expr.arms:
                arm_type = self._infer_expr(arm.body)
                result_type = merge_types(result_type, arm_type)
            return result_type

        elif isinstance(expr, OkExpr):
            # Ok(value) -> Result[value, E]：先推断成功分支的内部类型
            return self._infer_expr(expr.value)

        elif isinstance(expr, ErrExpr):
            # Err(error) -> Result[T, error]：错误分支不影响成功类型
            return TYPE_UNKNOWN

        elif isinstance(expr, TryExpr):
            # expr? 解包 Result：传播成功分支的内部类型
            return self._infer_expr(expr.expr)

        elif isinstance(expr, TupleLiteral):
            # 元组字面量：逐元素推断
            elem_types = [self._infer_expr(e) for e in expr.elements]
            return InferType(TypeKind.TUPLE, tuple_types=elem_types)

        elif isinstance(expr, TupleIndex):
            # 元组索引 tup.0：返回对应位置的元素类型
            obj_type = self._infer_expr(expr.object)
            if obj_type.kind == TypeKind.TUPLE:
                if 0 <= expr.index < len(obj_type.tuple_types):
                    return obj_type.tuple_types[expr.index]
            return TYPE_UNKNOWN

        elif isinstance(expr, (ListComp, SetComp)):
            # 列表/集合推导式：元素类型为 expr 的推断类型
            elem_type = self._infer_expr(expr.expr)
            # 注册生成器绑定到临时变量类型（宽松：按 unknown 处理）
            for gen in expr.generators:
                iter_t = self._infer_expr(gen.iterable)
                if iter_t.kind == TypeKind.ARRAY:
                    self.variable_types.setdefault(self.current_function, {})[gen.target] = iter_t.elem_type or TYPE_UNKNOWN
            for cond in expr.conditions:
                self._infer_expr(cond)
            return InferType(TypeKind.ARRAY, elem_type)

        elif isinstance(expr, MapComp):
            # Map 推导式：key/value 类型分别推断
            k = self._infer_expr(expr.key_expr)
            v = self._infer_expr(expr.value_expr)
            for gen in expr.generators:
                self._infer_expr(gen.iterable)
            for cond in expr.conditions:
                self._infer_expr(cond)
            return InferType(TypeKind.MAP)

        elif isinstance(expr, StructLiteral):
            # 结构体字面量：类型由类型名决定，推断为 unknown（具体字段信息由类型检查器处理）
            for _, value in expr.fields:
                self._infer_expr(value)
            return TYPE_UNKNOWN

        elif isinstance(expr, ForcedUnwrap):
            # 强制解包 a!：去掉 OptionalType 包装
            inner = self._infer_expr(expr.operand)
            if inner.kind == TypeKind.OPTIONAL:
                return inner.elem_type or TYPE_UNKNOWN
            return inner

        return TYPE_UNKNOWN

    def _propagate_numeric_type(self, var_expr: Expr, var_type: InferType, other_type: InferType):
        """类型传播:如果变量类型 unknown 但参与了数值运算,更新为数值类型"""
        if isinstance(var_expr, Identifier) and var_type.kind == TypeKind.UNKNOWN:
            if other_type.is_int():
                self.variable_types[self.current_function][var_expr.name] = TYPE_INT
            elif other_type.is_float():
                self.variable_types[self.current_function][var_expr.name] = TYPE_FLOAT


def infer_program_types(program: Program) -> dict:
    """便捷函数:推断整个程序的类型"""
    inferer = TypeInferer(program)
    return inferer.infer()


def is_pure_int_function(func_type: dict) -> bool:
    """判断函数是否是纯 int 函数(所有参数和返回值都是 int)"""
    for param_type in func_type['params']:
        if not param_type.is_int():
            return False
    return func_type['return'].is_int()
