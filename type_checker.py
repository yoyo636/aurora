"""Aurora 类型系统 — 渐进式类型推断与检查（TypeScript 风格）"""

from typing import Dict, List, Optional, Set, Tuple
from .ast_nodes import *


class TypeError(Exception):
    def __init__(self, message: str, node: Node = None):
        loc = f"L{node.line}:C{node.column}" if node else "?"
        super().__init__(f"{loc}: {message}")
        self.node = node


class TypeInfo:
    """类型信息"""
    def __init__(self, name: str, params: List['TypeInfo'] = None):
        self.name = name
        self.params = params or []
    
    def __repr__(self):
        if self.params:
            return f"{self.name}<{', '.join(repr(p) for p in self.params)}>"
        return self.name
    
    def __eq__(self, other):
        if not isinstance(other, TypeInfo):
            return False
        return self.name == other.name and self.params == other.params
    
    def is_compatible(self, other: 'TypeInfo') -> bool:
        """检查类型兼容性"""
        if self == other:
            return True
        # 数值兼容
        if self.name == 'float' and other.name == 'int':
            return True
        # Result 兼容
        if self.name == 'Result' and other.name in ('Ok', 'Err'):
            return True
        # 联合类型兼容
        if other.name == 'Union':
            return any(self.is_compatible(p) for p in other.params)
        return False


class TypeEnvironment:
    """类型环境（作用域链）"""
    def __init__(self, parent: 'TypeEnvironment' = None):
        self.parent = parent
        self.bindings: Dict[str, TypeInfo] = {}
        self.type_defs: Dict[str, TypeDef] = {}
        self.trait_defs: Dict[str, TraitDef] = {}
        self.impls: Dict[str, List[ImplBlock]] = {}
    
    def define(self, name: str, type_info: TypeInfo):
        self.bindings[name] = type_info
    
    def lookup(self, name: str) -> Optional[TypeInfo]:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def child(self) -> 'TypeEnvironment':
        return TypeEnvironment(parent=self)


class TypeChecker:
    """类型检查器 — 渐进式类型推断"""
    
    # 内建类型
    BUILTIN_TYPES = {
        'int': TypeInfo('int'),
        'float': TypeInfo('float'),
        'str': TypeInfo('str'),
        'bool': TypeInfo('bool'),
        'char': TypeInfo('char'),
        'nil': TypeInfo('nil'),
        'void': TypeInfo('void'),
    }
    
    # 内建函数
    BUILTIN_FUNCTIONS = {
        'print': TypeInfo('fn', [TypeInfo('any'), TypeInfo('void')]),
        'println': TypeInfo('fn', [TypeInfo('any'), TypeInfo('void')]),
        'len': TypeInfo('fn', [TypeInfo('any'), TypeInfo('int')]),
        'range': TypeInfo('fn', [TypeInfo('int'), TypeInfo('[int]')]),
        'str': TypeInfo('fn', [TypeInfo('any'), TypeInfo('str')]),
        'int': TypeInfo('fn', [TypeInfo('any'), TypeInfo('int')]),
        'float': TypeInfo('fn', [TypeInfo('any'), TypeInfo('float')]),
        'type': TypeInfo('fn', [TypeInfo('any'), TypeInfo('str')]),
        'assert': TypeInfo('fn', [TypeInfo('bool'), TypeInfo('void')]),
        'panic': TypeInfo('fn', [TypeInfo('str'), TypeInfo('never')]),
        'chan': TypeInfo('fn', [TypeInfo('any'), TypeInfo('channel')]),
        'sleep': TypeInfo('fn', [TypeInfo('int'), TypeInfo('void')]),
    }
    
    def __init__(self):
        self.global_env = TypeEnvironment()
        self.errors: List[TypeError] = []
        
        # 注册内建类型和函数
        for name, ti in self.BUILTIN_TYPES.items():
            self.global_env.define(name, ti)
        for name, ti in self.BUILTIN_FUNCTIONS.items():
            self.global_env.define(name, ti)
    
    def check(self, program: Program) -> List[TypeError]:
        """类型检查整个程序"""
        self.errors = []
        self._check_stmts(program.statements, self.global_env)
        return self.errors
    
    def _check_stmts(self, stmts: List[Stmt], env: TypeEnvironment):
        for stmt in stmts:
            self._check_stmt(stmt, env)
    
    def _check_stmt(self, stmt: Stmt, env: TypeEnvironment):
        if isinstance(stmt, LetStmt):
            self._check_let(stmt, env)
        elif isinstance(stmt, ConstStmt):
            self._check_const(stmt, env)
        elif isinstance(stmt, FnDef):
            self._check_fn_def(stmt, env)
        elif isinstance(stmt, TypeDef):
            self._check_type_def(stmt, env)
        elif isinstance(stmt, EnumDef):
            self._check_enum_def(stmt, env)
        elif isinstance(stmt, TraitDef):
            self._check_trait_def(stmt, env)
        elif isinstance(stmt, ImplBlock):
            self._check_impl(stmt, env)
        elif isinstance(stmt, IfStmt):
            self._check_if(stmt, env)
        elif isinstance(stmt, ForStmt):
            self._check_for(stmt, env)
        elif isinstance(stmt, WhileStmt):
            self._check_while(stmt, env)
        elif isinstance(stmt, MatchStmt):
            self._check_match(stmt, env)
        elif isinstance(stmt, TryStmt):
            self._check_try(stmt, env)
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                self._infer_expr(stmt.value, env)
        elif isinstance(stmt, ExprStmt):
            self._infer_expr(stmt.expr, env)
        elif isinstance(stmt, AssignStmt):
            self._check_assign(stmt, env)
        elif isinstance(stmt, SpawnStmt):
            self._infer_expr(stmt.call, env)
        elif isinstance(stmt, TestBlock):
            child_env = env.child()
            self._check_stmts(stmt.body.statements, child_env)
        elif isinstance(stmt, ImportStmt):
            pass  # TODO: 模块解析
    
    def _check_let(self, stmt: LetStmt, env: TypeEnvironment):
        if stmt.initializer:
            inferred = self._infer_expr(stmt.initializer, env)
            if stmt.type_annotation:
                declared = self._resolve_type_node(stmt.type_annotation, env)
                if not declared.is_compatible(inferred):
                    self.errors.append(TypeError(
                        f"类型不匹配: 声明为 {declared}，推断为 {inferred}", stmt))
                env.define(stmt.name, declared)
            else:
                env.define(stmt.name, inferred)
        elif stmt.type_annotation:
            env.define(stmt.name, self._resolve_type_node(stmt.type_annotation, env))
        else:
            self.errors.append(TypeError(
                f"变量 '{stmt.name}' 必须提供类型注解或初始值", stmt))
    
    def _check_const(self, stmt: ConstStmt, env: TypeEnvironment):
        inferred = self._infer_expr(stmt.initializer, env)
        if stmt.type_annotation:
            declared = self._resolve_type_node(stmt.type_annotation, env)
            env.define(stmt.name, declared)
        else:
            env.define(stmt.name, inferred)
    
    def _check_fn_def(self, stmt: FnDef, env: TypeEnvironment):
        fn_env = env.child()
        param_types = []
        for p in stmt.params:
            if p.type_annotation:
                ti = self._resolve_type_node(p.type_annotation, env)
            else:
                ti = TypeInfo('any')
            fn_env.define(p.name, ti)
            param_types.append(ti)
        
        ret_type = TypeInfo('void')
        if stmt.return_type:
            ret_type = self._resolve_type_node(stmt.return_type, env)
        
        fn_type = TypeInfo('fn', param_types + [ret_type])
        env.define(stmt.name, fn_type)

        if stmt.body is not None:
            self._check_stmts(stmt.body.statements, fn_env)
    
    def _check_type_def(self, stmt: TypeDef, env: TypeEnvironment):
        env.type_defs[stmt.name] = stmt
        fields = {}
        for f_name, f_type, _ in stmt.fields:
            fields[f_name] = self._resolve_type_node(f_type, env)
        env.define(stmt.name, TypeInfo(stmt.name))
    
    def _check_enum_def(self, stmt: EnumDef, env: TypeEnvironment):
        ti = TypeInfo(stmt.name)
        env.define(stmt.name, ti)
        for variant in stmt.variants:
            env.define(f"{stmt.name}.{variant.name}",
                      TypeInfo(f"{stmt.name}.{variant.name}"))
    
    def _check_trait_def(self, stmt: TraitDef, env: TypeEnvironment):
        env.trait_defs[stmt.name] = stmt
        trait_env = env.child()
        for method in stmt.methods:
            self._check_fn_def(method, trait_env)
    
    def _check_impl(self, stmt: ImplBlock, env: TypeEnvironment):
        if stmt.type_name not in env.type_defs and stmt.type_name not in env.bindings:
            self.errors.append(TypeError(f"未定义的类型: {stmt.type_name}", stmt))
        if stmt.trait_name:
            trait = env.trait_defs.get(stmt.trait_name)
            if trait is None:
                self.errors.append(TypeError(f"未定义的 trait: {stmt.trait_name}", stmt))
            else:
                # trait 声明的方法必须全部实现（有函数体的默认实现除外）
                implemented = {m.name for m in stmt.methods}
                missing = [m.name for m in trait.methods
                           if m.name not in implemented and m.body is None]
                if missing:
                    self.errors.append(TypeError(
                        f"类型 '{stmt.type_name}' 未实现 trait '{stmt.trait_name}' 的方法: "
                        + ', '.join(missing), stmt))
        # 同一方法重复实现检查
        seen = set()
        for method in stmt.methods:
            if method.name in seen:
                self.errors.append(TypeError(
                    f"impl 块中方法 '{method.name}' 重复定义", stmt))
            seen.add(method.name)

        type_env = env.child()
        type_env.define('self', TypeInfo(stmt.type_name))
        for method in stmt.methods:
            self._check_fn_def(method, type_env)
    
    def _check_if(self, stmt: IfStmt, env: TypeEnvironment):
        cond_type = self._infer_expr(stmt.condition, env)
        if cond_type.name != 'bool' and cond_type.name != 'any':
            self.errors.append(TypeError(
                f"if 条件必须是 bool 类型，得到 {cond_type}", stmt))
        
        then_env = env.child()
        self._check_stmts(stmt.then_body.statements, then_env)
        
        for cond, body in stmt.elif_clauses:
            ec = self._infer_expr(cond, env)
            if ec.name != 'bool' and ec.name != 'any':
                self.errors.append(TypeError(f"elif 条件必须是 bool 类型", stmt))
            eb_env = env.child()
            self._check_stmts(body.statements, eb_env)
        
        if stmt.else_body:
            else_env = env.child()
            self._check_stmts(stmt.else_body.statements, else_env)
    
    def _check_for(self, stmt: ForStmt, env: TypeEnvironment):
        iter_type = self._infer_expr(stmt.iterable, env)
        for_env = env.child()
        for var in stmt.variables:
            for_env.define(var, TypeInfo('any'))
        self._check_stmts(stmt.body.statements, for_env)
    
    def _check_while(self, stmt: WhileStmt, env: TypeEnvironment):
        cond_type = self._infer_expr(stmt.condition, env)
        while_env = env.child()
        self._check_stmts(stmt.body.statements, while_env)
    
    def _check_match(self, stmt: MatchStmt, env: TypeEnvironment):
        self._infer_expr(stmt.subject, env)
        for arm in stmt.arms:
            arm_env = env.child()
            self._register_pattern_bindings(arm.pattern, arm_env)
            self._infer_expr(arm.body, arm_env)
    
    def _check_try(self, stmt: TryStmt, env: TypeEnvironment):
        try_env = env.child()
        self._check_stmts(stmt.body.statements, try_env)
        for catch in stmt.catches:
            catch_env = env.child()
            catch_env.define(catch.name, TypeInfo('Error'))
            self._check_stmts(catch.body.statements, catch_env)
        if stmt.finally_body:
            self._check_stmts(stmt.finally_body.statements, env.child())
    
    def _check_assign(self, stmt: AssignStmt, env: TypeEnvironment):
        self._infer_expr(stmt.target, env)
        self._infer_expr(stmt.value, env)
    
    def _register_pattern_bindings(self, pattern: Pattern, env: TypeEnvironment):
        if isinstance(pattern, BindPattern):
            env.define(pattern.name, TypeInfo('any'))
        elif isinstance(pattern, ConstructorPattern):
            for field in pattern.fields:
                self._register_pattern_bindings(field, env)
    
    # ── 类型推断 ────────────────────────────────────────
    
    def _infer_expr(self, expr: Expr, env: TypeEnvironment) -> TypeInfo:
        if isinstance(expr, IntLiteral):
            return TypeInfo('int')
        elif isinstance(expr, FloatLiteral):
            return TypeInfo('float')
        elif isinstance(expr, StringLiteral):
            return TypeInfo('str')
        elif isinstance(expr, BoolLiteral):
            return TypeInfo('bool')
        elif isinstance(expr, NilLiteral):
            return TypeInfo('nil')
        elif isinstance(expr, Identifier):
            ti = env.lookup(expr.name)
            if ti is None:
                # 宽松模式：未定义变量推断为 any
                return TypeInfo('any')
            return ti
        elif isinstance(expr, ArrayLiteral):
            if expr.elements:
                elem_type = self._infer_expr(expr.elements[0], env)
                return TypeInfo(f'[{elem_type.name}]')
            return TypeInfo('[any]')
        elif isinstance(expr, MapLiteral):
            if expr.entries:
                k = self._infer_expr(expr.entries[0][0], env)
                v = self._infer_expr(expr.entries[0][1], env)
                return TypeInfo('map', [k, v])
            return TypeInfo('map', [TypeInfo('any'), TypeInfo('any')])
        elif isinstance(expr, TupleLiteral):
            types = [self._infer_expr(e, env) for e in expr.elements]
            return TypeInfo('tuple', types)
        elif isinstance(expr, BinaryOp):
            left = self._infer_expr(expr.left, env)
            right = self._infer_expr(expr.right, env)
            if expr.op in ('==', '!=', '<', '<=', '>', '>='):
                return TypeInfo('bool')
            if expr.op in ('+', '-', '*', '/', '%', '**'):
                # 数值提升
                if left.name == 'float' or right.name == 'float':
                    return TypeInfo('float')
                if left.name == 'str' and expr.op == '+':
                    return TypeInfo('str')
                return TypeInfo('int')
            if expr.op in ('<<', '>>', '&', '|', '^'):
                return TypeInfo('int')
            if expr.op in ('&&', '||'):
                return TypeInfo('bool')
            return left
        elif isinstance(expr, UnaryOp):
            operand = self._infer_expr(expr.operand, env)
            if expr.op == '!':
                return TypeInfo('bool')
            return operand
        elif isinstance(expr, CallExpr):
            if isinstance(expr.callee, Identifier):
                callee_type = env.lookup(expr.callee.name)
                if callee_type and callee_type.params:
                    return callee_type.params[-1]
            for arg in expr.args:
                self._infer_expr(arg, env)
            for _, val in expr.named_args:
                self._infer_expr(val, env)
            return TypeInfo('any')
        elif isinstance(expr, MethodCall):
            self._infer_expr(expr.object, env)
            for arg in expr.args:
                self._infer_expr(arg, env)
            for _, val in expr.named_args:
                self._infer_expr(val, env)
            return TypeInfo('any')
        elif isinstance(expr, MemberAccess):
            self._infer_expr(expr.object, env)
            return TypeInfo('any')
        elif isinstance(expr, IndexAccess):
            obj_type = self._infer_expr(expr.object, env)
            self._infer_expr(expr.index, env)
            # 数组索引返回元素类型
            if obj_type.name.startswith('['):
                return TypeInfo(obj_type.name[1:-1] if len(obj_type.name) > 2 else 'any')
            return TypeInfo('any')
        elif isinstance(expr, LambdaExpr):
            return TypeInfo('fn')
        elif isinstance(expr, IfExpr):
            return self._infer_expr(expr.then_body.statements[-1] if expr.then_body.statements else NilLiteral(), env)
        elif isinstance(expr, MatchExpr):
            return TypeInfo('any')
        elif isinstance(expr, SpawnExpr):
            return TypeInfo('fiber')
        elif isinstance(expr, ChannelSend):
            self._infer_expr(expr.channel, env)
            self._infer_expr(expr.value, env)
            return TypeInfo('void')
        elif isinstance(expr, ChannelRecv):
            return TypeInfo('any')
        elif isinstance(expr, TryExpr):
            return self._infer_expr(expr.expr, env)
        elif isinstance(expr, OptionalAccess):
            obj = self._infer_expr(expr.object, env)
            return obj if obj.name != 'nil' else TypeInfo('any')
        elif isinstance(expr, OptionalCall):
            self._infer_expr(expr.object, env)
            return TypeInfo('any')
        elif isinstance(expr, NullCoalesce):
            left = self._infer_expr(expr.left, env)
            right = self._infer_expr(expr.right, env)
            return left if left.name != 'nil' else right
        elif isinstance(expr, RefExpr):
            inner = self._infer_expr(expr.inner, env)
            return TypeInfo('ref', [inner])
        elif isinstance(expr, DerefExpr):
            inner = self._infer_expr(expr.inner, env)
            if inner.params:
                return inner.params[0]
            return TypeInfo('any')
        elif isinstance(expr, StringInterpolation):
            return TypeInfo('str')
        
        return TypeInfo('any')
    
    def _resolve_type_node(self, node: TypeNode, env: TypeEnvironment) -> TypeInfo:
        if isinstance(node, NamedType):
            return TypeInfo(node.name)
        elif isinstance(node, ArrayType):
            elem = self._resolve_type_node(node.element_type, env)
            return TypeInfo(f'[{elem.name}]')
        elif isinstance(node, MapType):
            k = self._resolve_type_node(node.key_type, env)
            v = self._resolve_type_node(node.value_type, env)
            return TypeInfo('map', [k, v])
        elif isinstance(node, TupleType):
            types = [self._resolve_type_node(t, env) for t in node.element_types]
            return TypeInfo('tuple', types)
        elif isinstance(node, FunctionType):
            params = [self._resolve_type_node(t, env) for t in node.param_types]
            ret = self._resolve_type_node(node.return_type, env) if node.return_type else TypeInfo('void')
            return TypeInfo('fn', params + [ret])
        elif isinstance(node, GenericType):
            args = [self._resolve_type_node(a, env) for a in node.type_args]
            return TypeInfo(node.base, args)
        elif isinstance(node, UnionType):
            variants = [self._resolve_type_node(v, env) for v in node.variants]
            return TypeInfo('Union', variants)
        elif isinstance(node, RefType):
            inner = self._resolve_type_node(node.inner, env)
            return TypeInfo('ref', [inner])
        return TypeInfo('any')
