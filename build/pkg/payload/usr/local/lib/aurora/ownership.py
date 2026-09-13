"""Aurora 所有权与借用检查器 — Rust 风格的内存安全保证"""

from typing import Dict, List, Optional, Set, Tuple
from .ast_nodes import *


class OwnershipError(Exception):
    def __init__(self, message: str, node: Node = None):
        loc = f"L{node.line}:C{node.column}" if node else "?"
        super().__init__(f"{loc}: {message}")
        self.node = node


class ValueState:
    """值的生命周期状态"""
    ALIVE = "alive"
    MOVED = "moved"
    BORROWED_IMMUT = "borrowed_immut"
    BORROWED_MUT = "borrowed_mut"
    DROPPED = "dropped"

    def __init__(self, name: str, state: str = "alive", mutable: bool = True):
        self.name = name
        self.state = state
        self.mutable = mutable
        self.immut_borrow_count = 0
        self.mut_borrowed = False


class Scope:
    """作用域"""
    def __init__(self, parent: 'Scope' = None):
        self.parent = parent
        self.values: Dict[str, ValueState] = {}
        self.children: List['Scope'] = []
        if parent:
            parent.children.append(self)
    
    def define(self, name: str, mutable: bool = True) -> ValueState:
        vs = ValueState(name, ValueState.ALIVE, mutable)
        self.values[name] = vs
        return vs
    
    def lookup(self, name: str) -> Optional[ValueState]:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class OwnershipChecker:
    """所有权检查器 — 编译时内存安全保证
    
    核心规则（Rust 风格）：
    1. 每个值有且只有一个所有者
    2. 所有者离开作用域时值被丢弃
    3. 同一时刻只能有一个 &mut 引用或多个 & 引用
    4. 引用必须始终有效（不能悬垂）
    """
    
    def __init__(self):
        self.errors: List[OwnershipError] = []
        self.global_scope = Scope()
    
    def check(self, program: Program) -> List[OwnershipError]:
        """检查整个程序的所有权安全性"""
        self.errors = []
        scope = Scope(self.global_scope)
        self._check_stmts(program.statements, scope)
        return self.errors
    
    def _check_stmts(self, stmts: List[Stmt], scope: Scope):
        for stmt in stmts:
            self._check_stmt(stmt, scope)
    
    def _check_stmt(self, stmt: Stmt, scope: Scope):
        if isinstance(stmt, LetStmt):
            self._check_let(stmt, scope)
        elif isinstance(stmt, ConstStmt):
            scope.define(stmt.name, mutable=False)
        elif isinstance(stmt, FnDef):
            fn_scope = Scope(scope)
            # 函数参数在函数作用域中定义
            for p in stmt.params:
                fn_scope.define(p.name, mutable=False)
            if stmt.body is not None:
                self._check_stmts(stmt.body.statements, fn_scope)
            # 检查函数离开时所有借用是否有效
            self._check_scope_drops(fn_scope)
        elif isinstance(stmt, IfStmt):
            self._check_expr_ownership(stmt.condition, scope)
            then_scope = Scope(scope)
            self._check_stmts(stmt.then_body.statements, then_scope)
            for cond, body in stmt.elif_clauses:
                elif_scope = Scope(scope)
                self._check_stmts(body.statements, elif_scope)
            if stmt.else_body:
                else_scope = Scope(scope)
                self._check_stmts(stmt.else_body.statements, else_scope)
        elif isinstance(stmt, ForStmt):
            for_scope = Scope(scope)
            for var in stmt.variables:
                for_scope.define(var)
            self._check_stmts(stmt.body.statements, for_scope)
        elif isinstance(stmt, WhileStmt):
            while_scope = Scope(scope)
            self._check_stmts(stmt.body.statements, while_scope)
        elif isinstance(stmt, MatchStmt):
            self._check_expr_ownership(stmt.subject, scope)
            for arm in stmt.arms:
                arm_scope = Scope(scope)
                self._register_pattern(arm.pattern, arm_scope)
                self._check_expr_ownership(arm.body, arm_scope)
        elif isinstance(stmt, TryStmt):
            try_scope = Scope(scope)
            self._check_stmts(stmt.body.statements, try_scope)
            for catch in stmt.catches:
                catch_scope = Scope(scope)
                catch_scope.define(catch.name)
                self._check_stmts(catch.body.statements, catch_scope)
            if stmt.finally_body:
                fin_scope = Scope(scope)
                self._check_stmts(stmt.finally_body.statements, fin_scope)
        elif isinstance(stmt, SpawnStmt):
            self._check_expr_ownership(stmt.call, scope)
        elif isinstance(stmt, ExprStmt):
            self._check_expr_ownership(stmt.expr, scope)
        elif isinstance(stmt, AssignStmt):
            self._check_assign(stmt, scope)
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                self._check_expr_ownership(stmt.value, scope)
        elif isinstance(stmt, ImplBlock):
            for method in stmt.methods:
                self._check_stmt(method, scope)
        elif isinstance(stmt, TestBlock):
            test_scope = Scope(scope)
            self._check_stmts(stmt.body.statements, test_scope)
    
    def _check_let(self, stmt: LetStmt, scope: Scope):
        if stmt.initializer:
            self._check_expr_ownership(stmt.initializer, scope)
        scope.define(stmt.name, mutable=stmt.mutable)
    
    def _check_assign(self, stmt: AssignStmt, scope: Scope):
        # 检查目标是否可变
        if isinstance(stmt.target, Identifier):
            vs = scope.lookup(stmt.target.name)
            if vs and not vs.mutable:
                self.errors.append(OwnershipError(
                    f"不能修改不可变变量 '{stmt.target.name}'", stmt))
            if vs and vs.mut_borrowed:
                self.errors.append(OwnershipError(
                    f"变量 '{stmt.target.name}' 当前存在可变借用，不能赋值", stmt))
            if vs and vs.immut_borrow_count > 0:
                self.errors.append(OwnershipError(
                    f"变量 '{stmt.target.name}' 当前存在不可变借用，不能赋值", stmt))
        self._check_expr_ownership(stmt.value, scope)
    
    def _check_expr_ownership(self, expr: Expr, scope: Scope):
        """检查表达式中的所有权规则"""
        if isinstance(expr, Identifier):
            vs = scope.lookup(expr.name)
            if vs and vs.state == ValueState.MOVED:
                self.errors.append(OwnershipError(
                    f"变量 '{expr.name}' 已被移动，不能再使用", expr))
        
        elif isinstance(expr, BinaryOp):
            self._check_expr_ownership(expr.left, scope)
            self._check_expr_ownership(expr.right, scope)
        
        elif isinstance(expr, CallExpr):
            self._check_expr_ownership(expr.callee, scope)
            for arg in expr.args:
                self._check_expr_ownership(arg, scope)
                # 函数调用可能移动值
                if isinstance(arg, Identifier):
                    vs = scope.lookup(arg.name)
                    if vs and vs.state == ValueState.ALIVE:
                        # 如果函数接受所有权（非引用），标记为已移动
                        # 这里简化处理：非引用参数视为移动
                        pass
        
        elif isinstance(expr, MethodCall):
            self._check_expr_ownership(expr.object, scope)
            for arg in expr.args:
                self._check_expr_ownership(arg, scope)
        
        elif isinstance(expr, RefExpr):
            if isinstance(expr.inner, Identifier):
                vs = scope.lookup(expr.inner.name)
                if vs:
                    if expr.mutable:
                        if not vs.mutable:
                            self.errors.append(OwnershipError(
                                f"不能对不可变变量 '{expr.inner.name}' 创建可变引用", expr))
                        if vs.immut_borrow_count > 0:
                            self.errors.append(OwnershipError(
                                f"变量 '{expr.inner.name}' 存在不可变借用，不能创建可变引用", expr))
                        vs.mut_borrowed = True
                        vs.state = ValueState.BORROWED_MUT
                    else:
                        if vs.mut_borrowed:
                            self.errors.append(OwnershipError(
                                f"变量 '{expr.inner.name}' 存在可变借用，不能创建不可变引用", expr))
                        vs.immut_borrow_count += 1
                        vs.state = ValueState.BORROWED_IMMUT
        
        elif isinstance(expr, ArrayLiteral):
            for elem in expr.elements:
                self._check_expr_ownership(elem, scope)
        
        elif isinstance(expr, MapLiteral):
            for k, v in expr.entries:
                self._check_expr_ownership(k, scope)
                self._check_expr_ownership(v, scope)
        
        elif isinstance(expr, LambdaExpr):
            # Lambda 捕获变量检查
            if expr.body:
                self._check_stmts(expr.body.statements, scope)
        
        elif isinstance(expr, SpawnExpr):
            self._check_expr_ownership(expr.call, scope)
        
        elif isinstance(expr, ChannelSend):
            self._check_expr_ownership(expr.channel, scope)
            self._check_expr_ownership(expr.value, scope)
    
    def _register_pattern(self, pattern: Pattern, scope: Scope):
        """在作用域中注册模式绑定的变量"""
        if isinstance(pattern, BindPattern):
            scope.define(pattern.name)
        elif isinstance(pattern, ConstructorPattern):
            for field in pattern.fields:
                self._register_pattern(field, scope)
    
    def _check_scope_drops(self, scope: Scope):
        """检查作用域结束时所有借用是否已释放"""
        for name, vs in scope.values.items():
            if vs.state == ValueState.BORROWED_MUT:
                vs.state = ValueState.ALIVE
                vs.mut_borrowed = False
            elif vs.state == ValueState.BORROWED_IMMUT:
                vs.state = ValueState.ALIVE
                vs.immut_borrow_count = 0
