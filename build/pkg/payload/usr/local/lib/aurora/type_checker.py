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
        self.warnings: List[TypeError] = []
        self._fn_defs: Dict[str, FnDef] = {}
        # v3.3.0: 记录 live 块与其绑定变量，用于循环依赖检测
        self._live_blocks: List[Tuple[str, 'LiveBlockExpr']] = []
        # v3.3.0: 当前作用域中所有 let mut 变量名（按作用域栈管理）
        self._mutable_vars_stack: List[Set[str]] = [set()]
        # v3.3.0: extern 函数名 -> 是否标注为 pure
        self._extern_functions: Dict[str, bool] = {}
        # v3.3.0: 全程序纯度分析得出的不纯用户函数名集合
        self._impure_functions: Set[str] = set()

        # 注册内建类型和函数
        for name, ti in self.BUILTIN_TYPES.items():
            self.global_env.define(name, ti)
        for name, ti in self.BUILTIN_FUNCTIONS.items():
            self.global_env.define(name, ti)

    # ── 作用域栈辅助（let mut 追踪） ─────────────────────
    def _push_scope(self):
        self._mutable_vars_stack.append(set())

    def _pop_scope(self):
        if len(self._mutable_vars_stack) > 1:
            self._mutable_vars_stack.pop()

    def _is_mutable(self, name: str) -> bool:
        """name 是否在任一可见作用域中以 let mut 声明"""
        return any(name in scope for scope in self._mutable_vars_stack)

    def _warn(self, message: str, node: Node = None):
        """记录一条警告（不阻止编译）"""
        self.warnings.append(TypeError(message, node))
    
    def check(self, program: Program) -> List[TypeError]:
        """类型检查整个程序"""
        self.errors = []
        self._live_blocks = []
        self._mutable_vars_stack = [set()]
        self._extern_functions = {}
        self._impure_functions = set()
        self._fn_defs = {}

        # v3.3.0: 全程序预处理（必须在语句检查之前，以便 live 块纯度检查
        # 能利用完整的调用图）：
        #   1. 收集 extern 函数纯度标注
        #   2. 收集所有函数定义
        #   3. 过程间纯度分析（不动点）-> self._impure_functions
        self._prepass_program(program)

        self._check_stmts(program.statements, self.global_env)
        # v3.3.0: live 块循环依赖检测
        self._check_live_cycles()
        return self.errors

    # ── v3.3.0: 全程序预处理与过程间纯度分析 ──────────────

    def _prepass_program(self, program: Program):
        """在正式检查前收集 extern 纯度、全部 FnDef，并做过程间纯度分析。"""
        # 1. 收集 extern 函数纯度
        self._collect_extern_walk(program.statements)
        # 2. 收集所有函数定义（含嵌套）
        self._collect_fn_defs_walk(program.statements)
        # 3. 过程间纯度分析
        self._analyze_interprocedural_purity()

    def _collect_extern_walk(self, node):
        """递归收集 extern 块中声明的函数及其 pure 标注。"""
        if node is None:
            return
        if isinstance(node, (list, tuple)):
            for item in node:
                self._collect_extern_walk(item)
            return
        if not hasattr(node, '__dict__'):
            return
        if isinstance(node, ExternBlock):
            for decl in node.declarations:
                self._extern_functions[decl.name] = bool(getattr(decl, 'is_pure', False))
        for key, value in vars(node).items():
            if key in ('line', 'column', 'inferred_type'):
                continue
            if isinstance(value, (list, tuple)) or hasattr(value, '__dict__'):
                self._collect_extern_walk(value)

    def _collect_fn_defs_walk(self, node):
        """递归收集所有 FnDef（含嵌套定义、impl 方法）。"""
        if node is None:
            return
        if isinstance(node, (list, tuple)):
            for item in node:
                self._collect_fn_defs_walk(item)
            return
        if not hasattr(node, '__dict__'):
            return
        if isinstance(node, FnDef):
            self._fn_defs[node.name] = node
        for key, value in vars(node).items():
            if key in ('line', 'column', 'inferred_type'):
                continue
            if isinstance(value, (list, tuple)) or hasattr(value, '__dict__'):
                self._collect_fn_defs_walk(value)

    def _collect_callees(self, fn_def: FnDef) -> Set[str]:
        """收集函数体中所有以 Identifier 形式调用的函数名。"""
        names: Set[str] = set()
        self._collect_callees_walk(fn_def.body, names)
        return names

    def _collect_callees_walk(self, node, names: Set[str]):
        if node is None:
            return
        if isinstance(node, (list, tuple)):
            for item in node:
                self._collect_callees_walk(item, names)
            return
        if not hasattr(node, '__dict__'):
            return
        if isinstance(node, CallExpr) and isinstance(node.callee, Identifier):
            names.add(node.callee.name)
        for key, value in vars(node).items():
            if key in ('line', 'column', 'inferred_type'):
                continue
            if isinstance(value, (list, tuple)) or hasattr(value, '__dict__'):
                self._collect_callees_walk(value, names)

    def _analyze_interprocedural_purity(self):
        """过程间纯度分析（不动点迭代）。

        初始不纯集合：函数体直接调用 I/O 函数或未标注 pure 的 extern 函数。
        迭代：若 A 调用了不纯函数 B，则 A 也不纯。直到无变化。
        """
        impure: Set[str] = set()

        # 初始：直接调用 I/O 或非 pure extern 的函数
        for name, fn_def in self._fn_defs.items():
            callees = self._collect_callees(fn_def)
            for callee in callees:
                if callee in self._IO_FUNCTIONS:
                    impure.add(name)
                    break
                if callee in self._extern_functions and not self._extern_functions[callee]:
                    impure.add(name)
                    break

        # 不动点传播
        changed = True
        while changed:
            changed = False
            for name, fn_def in self._fn_defs.items():
                if name in impure:
                    continue
                callees = self._collect_callees(fn_def)
                for callee in callees:
                    if callee in impure:
                        impure.add(name)
                        changed = True
                        break

        self._impure_functions = impure
    
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
            self._push_scope()
            self._check_stmts(stmt.body.statements, child_env)
            self._pop_scope()
        elif isinstance(stmt, ImportStmt):
            pass  # TODO: 模块解析
        elif isinstance(stmt, ExternBlock):
            # v3.3.0: 记录 extern 函数纯度（pre-pass 已收集，这里同步到当前 env）
            for decl in stmt.declarations:
                self._extern_functions[decl.name] = bool(getattr(decl, 'is_pure', False))
                # 注册为函数类型，使调用能通过类型推断
                param_types = [TypeInfo('any') for _ in decl.params]
                ret_type = (self._resolve_type_node(decl.return_type, env)
                            if decl.return_type else TypeInfo('void'))
                env.define(decl.name, TypeInfo('fn', param_types + [ret_type]))
    
    def _check_let(self, stmt: LetStmt, env: TypeEnvironment):
        if stmt.initializer:
            inferred = self._infer_expr(stmt.initializer, env)
            # v3.3.0: 记录 live 块与其绑定变量，供循环依赖检测
            if isinstance(stmt.initializer, LiveBlockExpr):
                self._live_blocks.append((stmt.name, stmt.initializer))
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
        # v3.3.0: 追踪 let mut 变量，供 live 块捕获检查与 Source 重绑定检查
        if stmt.mutable:
            self._mutable_vars_stack[-1].add(stmt.name)
    
    def _check_const(self, stmt: ConstStmt, env: TypeEnvironment):
        inferred = self._infer_expr(stmt.initializer, env)
        if stmt.type_annotation:
            declared = self._resolve_type_node(stmt.type_annotation, env)
            env.define(stmt.name, declared)
        else:
            env.define(stmt.name, inferred)
    
    def _check_fn_def(self, stmt: FnDef, env: TypeEnvironment):
        # 可变参数检查：variadic 参数之后不能再有普通位置参数（警告）
        seen_variadic = False
        for p in stmt.params:
            if seen_variadic and not p.variadic and p.default_value is None:
                self._warn(f"可变参数 '{[q.name for q in stmt.params if q.variadic][0]}' 之后不应再有普通位置参数 '{p.name}'", stmt)
            if p.variadic:
                seen_variadic = True

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
        self._fn_defs[stmt.name] = stmt

        if stmt.body is not None:
            self._push_scope()
            try:
                self._check_stmts(stmt.body.statements, fn_env)
            finally:
                self._pop_scope()
    
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
        self._push_scope()
        self._check_stmts(stmt.then_body.statements, then_env)
        self._pop_scope()

        for cond, body in stmt.elif_clauses:
            ec = self._infer_expr(cond, env)
            if ec.name != 'bool' and ec.name != 'any':
                self.errors.append(TypeError(f"elif 条件必须是 bool 类型", stmt))
            eb_env = env.child()
            self._push_scope()
            self._check_stmts(body.statements, eb_env)
            self._pop_scope()

        if stmt.else_body:
            else_env = env.child()
            self._push_scope()
            self._check_stmts(stmt.else_body.statements, else_env)
            self._pop_scope()
    
    def _check_for(self, stmt: ForStmt, env: TypeEnvironment):
        iter_type = self._infer_expr(stmt.iterable, env)
        for_env = env.child()
        self._push_scope()
        for var in stmt.variables:
            for_env.define(var, TypeInfo('any'))
        self._check_stmts(stmt.body.statements, for_env)
        self._pop_scope()

    def _check_while(self, stmt: WhileStmt, env: TypeEnvironment):
        cond_type = self._infer_expr(stmt.condition, env)
        while_env = env.child()
        self._push_scope()
        self._check_stmts(stmt.body.statements, while_env)
        self._pop_scope()
    
    def _check_match(self, stmt: MatchStmt, env: TypeEnvironment):
        subject_type = self._infer_expr(stmt.subject, env)
        for arm in stmt.arms:
            arm_env = env.child()
            self._register_pattern_bindings(arm.pattern, arm_env)
            self._infer_expr(arm.body, arm_env)
        self._check_match_exhaustive(stmt, subject_type, env)

    def _check_match_exhaustive(self, stmt: MatchStmt, subject_type: TypeInfo, env: TypeEnvironment):
        """Match 穷尽性检查（警告级别，不报错）"""
        patterns = [arm.pattern for arm in stmt.arms]

        # 有通配符 -> 穷尽
        if any(isinstance(p, WildcardPattern) for p in patterns):
            return

        # bool 类型：检查 true/false 是否都覆盖
        if subject_type.name == 'bool':
            covered = set()
            for p in patterns:
                if isinstance(p, LiteralPattern) and isinstance(p.value, BoolLiteral):
                    covered.add(p.value.value)
            if covered == {True, False}:
                return
            self._warn(f"match 未穷尽：bool 未覆盖 {'true' if False not in covered else 'false'} 分支", stmt)
            return

        # enum 类型：检查所有变体是否都被覆盖
        enum_name = subject_type.name
        enum_def = env.type_defs.get(enum_name)
        # EnumDef 注册在 global_env 上；通过遍历查找
        for top_name, top_def in env.type_defs.items():
            if isinstance(top_def, EnumDef) and top_def.name == enum_name:
                enum_def = top_def
                break
        if enum_def is None:
            # 向上查找 enum 定义
            cur = env
            while cur is not None:
                for tn, td in cur.type_defs.items():
                    if isinstance(td, EnumDef) and td.name == enum_name:
                        enum_def = td
                        break
                if enum_def is not None:
                    break
                cur = cur.parent
        if enum_def is not None and isinstance(enum_def, EnumDef):
            covered = set()
            for p in patterns:
                if isinstance(p, ConstructorPattern):
                    # ConstructorPattern.name 可能是 "Enum.Variant" 或 "Variant"
                    short = p.name.split('.')[-1]
                    covered.add(short)
            all_variants = {v.name for v in enum_def.variants}
            missing = all_variants - covered
            if missing:
                self._warn(f"match 未穷尽：枚举 '{enum_name}' 缺少变体 {sorted(missing)}", stmt)
            return

        # 其他类型（如 tuple/struct）：宽松，不警告
        return
    
    def _check_try(self, stmt: TryStmt, env: TypeEnvironment):
        try_env = env.child()
        self._push_scope()
        self._check_stmts(stmt.body.statements, try_env)
        self._pop_scope()
        for catch in stmt.catches:
            catch_env = env.child()
            catch_env.define(catch.name, TypeInfo('Error'))
            self._push_scope()
            self._check_stmts(catch.body.statements, catch_env)
            self._pop_scope()
        if stmt.finally_body:
            finally_env = env.child()
            self._push_scope()
            self._check_stmts(stmt.finally_body.statements, finally_env)
            self._pop_scope()
    
    def _check_assign(self, stmt: AssignStmt, env: TypeEnvironment):
        target_type = self._infer_expr(stmt.target, env)
        value_type = self._infer_expr(stmt.value, env)

        # v3.3.0: Source 的 mut 语义检查
        #  - x = value（右值为内部值类型 T）：修改 source 内部值，允许。
        #  - x = source(...)（右值也是 Source<T>）：重新绑定 source。
        #    若 x 不是 let mut 声明，则报错。
        if isinstance(stmt.target, Identifier):
            tname = stmt.target.name
            if target_type.name == 'Source':
                if value_type.name == 'Source' and not self._is_mutable(tname):
                    self.errors.append(TypeError(
                        f"不能重新绑定 source 变量 '{tname}'。"
                        f"source 内部值总是可变的，使用 '{tname} = value' 修改内部值；"
                        f"如需重新绑定，请用 'let mut {tname} = source(...)'。",
                        stmt))

    # ── v3.3.0: live 块纯度检查 ───────────────────────────

    # 已知的 I/O / 不纯内置函数名
    _IO_FUNCTIONS = {
        'print', 'println', 'echo', 'read', 'read_line', 'read_file',
        'write_file', 'append_file', 'open', 'close', 'input',
        'sleep', 'exec', 'system', 'rand', 'random', 'now',
        'http_get', 'http_post', 'fetch',
    }

    def _check_live_purity(self, expr: 'LiveBlockExpr', env: TypeEnvironment):
        """检查 live 块的纯度 —— 不允许 I/O 操作、对 source 的赋值、
        捕获非 source 的 let mut 变量、或调用未标注 pure 的 extern 函数。
        违规作为 TypeError 收集到 self.errors（编译期错误，精确到行号）。"""
        violations: List[Tuple[object, str]] = []

        # v3.3.0 Fix 1: live 块中捕获的 let mut 变量必须是 source
        self._check_live_mutable_capture(expr, env)

        # v3.3.0 Fix 2/3/4: 纯度违规检测（含 extern 标注、过程间不纯调用、调用链追溯）
        self._check_purity_walk(expr.body, self._IO_FUNCTIONS, violations)
        for node, msg in violations:
            self.errors.append(TypeError(f"live 块纯度违规: {msg}", node))

    def _check_live_mutable_capture(self, expr: 'LiveBlockExpr', env: TypeEnvironment):
        """Fix 1: live 块引用的 let mut 变量必须是 Source<T>，否则无法触发重算。"""
        names = self._collect_identifiers(expr)
        for name in names:
            if not self._is_mutable(name):
                continue
            ti = env.lookup(name)
            if ti is not None and ti.name == 'Source':
                continue
            self.errors.append(TypeError(
                f"live 块中引用了可变变量 '{name}'，但它不是 source。"
                f"可变状态必须用 source() 包裹以启用依赖追踪。", expr))

    def _format_call_chain(self, call_stack: List[str], leaf_loc: str) -> str:
        """格式化调用链信息。超过 5 层折叠。"""
        chain = call_stack
        if len(chain) > 5:
            shown = " → ".join(chain[:5])
            chain_str = f"{shown} → ... (还有 {len(chain) - 5} 层)"
        else:
            chain_str = " → ".join(chain)
        return f"live → {chain_str} → {leaf_loc}"

    def _add_purity_violation(self, violations: List[Tuple[object, str]],
                              node, call_stack: List[str],
                              leaf_name: str, leaf_kind: str):
        """记录一条纯度违规。leaf_kind: 'io' 或 'extern'。"""
        if leaf_kind == 'extern':
            leaf_loc = f"{leaf_name} (extern 函数，未标注 pure)"
            direct_msg = (f"extern 函数 '{leaf_name}' 未标注为 pure，"
                          f"不能在 live 块中调用。请确认其无副作用后标注为 "
                          f"'extern \"C\" pure fn'。")
        else:
            leaf_loc = leaf_name
            direct_msg = f"调用了 I/O 函数 '{leaf_name}'"

        if call_stack:
            chain = self._format_call_chain(call_stack, leaf_loc)
            violations.append((node, f"调用了不纯函数 '{call_stack[0]}'。调用链: {chain}"))
        else:
            violations.append((node, direct_msg))

    def _check_purity_walk(self, node, io_funcs: Set[str],
                           violations: List[Tuple[object, str]],
                           call_stack: Optional[List[str]] = None,
                           visited: Optional[Set[str]] = None):
        """递归遍历 AST，检测 live 块内的不纯操作。

        - call_stack: live 块到当前调用点之间的用户函数链（不含 leaf）。
        - visited: 当前追踪链上已进入的用户函数，防止递归导致无限循环。
        """
        if call_stack is None:
            call_stack = []
        if visited is None:
            visited = set()
        if node is None:
            return
        if isinstance(node, (list, tuple)):
            for item in node:
                self._check_purity_walk(item, io_funcs, violations, call_stack, visited)
            return
        if not hasattr(node, '__dict__'):
            return

        # 检测函数调用中的 I/O 函数 / extern 非 pure / 不纯用户函数
        traced_callee: Optional[str] = None
        if isinstance(node, CallExpr):
            callee = node.callee
            if isinstance(callee, Identifier):
                name = callee.name
                if name in io_funcs:
                    self._add_purity_violation(violations, node, call_stack, name, 'io')
                elif name in self._extern_functions and not self._extern_functions[name]:
                    self._add_purity_violation(violations, node, call_stack, name, 'extern')
                elif (name in self._impure_functions
                      and name in self._fn_defs
                      and name not in visited):
                    # 间接不纯调用：递归进入函数体追溯根因
                    traced_callee = name

        # 检测方法调用中的 I/O 方法
        if isinstance(node, MethodCall):
            if node.method in io_funcs:
                violations.append((node, f"调用了 I/O 方法 '{node.method}'"))

        # 检测赋值（可能修改 source）
        if isinstance(node, AssignStmt):
            violations.append((node, "live 块中不允许赋值操作（可能修改 source）"))

        # 递归子节点（跳过元信息字段）
        for key, value in vars(node).items():
            if key in ('line', 'column', 'inferred_type'):
                continue
            if isinstance(value, (list, tuple)) or hasattr(value, '__dict__'):
                self._check_purity_walk(value, io_funcs, violations, call_stack, visited)

        # 递归进入不纯用户函数体以追溯调用链
        if traced_callee is not None:
            fn_def = self._fn_defs[traced_callee]
            new_stack = call_stack + [traced_callee]
            new_visited = visited | {traced_callee}
            self._check_purity_walk(fn_def.body, io_funcs, violations,
                                    new_stack, new_visited)

    def _collect_identifiers(self, node) -> Set[str]:
        """收集节点子树中所有标识符引用名。"""
        names: Set[str] = set()
        self._collect_ident_walk(node, names)
        return names

    def _collect_ident_walk(self, node, names: Set[str]):
        if node is None:
            return
        if isinstance(node, (list, tuple)):
            for item in node:
                self._collect_ident_walk(item, names)
            return
        if not hasattr(node, '__dict__'):
            return
        if isinstance(node, Identifier):
            names.add(node.name)
        for key, value in vars(node).items():
            if key in ('line', 'column', 'inferred_type'):
                continue
            if isinstance(value, (list, tuple)) or hasattr(value, '__dict__'):
                self._collect_ident_walk(value, names)

    def _check_live_cycles(self):
        """检测 live 块之间的循环依赖（含直接自引用）。
        构建依赖图：live 变量 A 依赖 live 变量 B 当且仅当 A 的块引用了 B。
        DFS 检测环，命中则报编译期错误。"""
        if len(self._live_blocks) <= 1:
            # 仅 0/1 个 live 块时仍需检查直接自引用
            names = {name for name, _ in self._live_blocks}
            for name, block in self._live_blocks:
                refs = self._collect_identifiers(block)
                if name in refs:
                    self.errors.append(TypeError(
                        f"live 块 '{name}' 直接引用自身，存在循环依赖", block))
            return

        # 依赖图：var -> set(依赖的 live 变量)
        live_names = {name for name, _ in self._live_blocks}
        deps: Dict[str, Set[str]] = {}
        block_of: Dict[str, 'LiveBlockExpr'] = {}
        for name, block in self._live_blocks:
            refs = self._collect_identifiers(block)
            deps[name] = refs & live_names
            block_of[name] = block

        # DFS 三色标记检测环
        WHITE, GRAY, BLACK = 0, 1, 2
        color: Dict[str, int] = {n: WHITE for n in live_names}
        cycle_path: List[str] = []

        def dfs(node: str) -> bool:
            color[node] = GRAY
            cycle_path.append(node)
            for nxt in sorted(deps.get(node, set())):
                if color.get(nxt, WHITE) == GRAY:
                    # 找到环
                    idx = cycle_path.index(nxt)
                    cycle = cycle_path[idx:] + [nxt]
                    self.errors.append(TypeError(
                        "live 块循环依赖: " + " -> ".join(cycle),
                        block_of.get(node)))
                    return True
                if color.get(nxt, WHITE) == WHITE:
                    if dfs(nxt):
                        return True
            cycle_path.pop()
            color[node] = BLACK
            return False

        for n in sorted(live_names):
            if color[n] == WHITE:
                dfs(n)

    
    def _register_pattern_bindings(self, pattern: Pattern, env: TypeEnvironment):
        if isinstance(pattern, BindPattern):
            env.define(pattern.name, TypeInfo('any'))
        elif isinstance(pattern, ConstructorPattern):
            for field in pattern.fields:
                self._register_pattern_bindings(field, env)
        elif isinstance(pattern, StructPattern):
            # 结构体模式：Point { x, y } 或 User { name: n, age: a }
            for field_name, sub in pattern.fields:
                if sub is None:
                    # 简写 Point { x }：字段名即绑定名
                    env.define(field_name, TypeInfo('any'))
                else:
                    self._register_pattern_bindings(sub, env)
        elif isinstance(pattern, TuplePattern):
            for elem in pattern.elements:
                self._register_pattern_bindings(elem, env)
    
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
                # 命名参数检查：命名参数名必须在函数参数列表中存在
                fn_def = self._fn_defs.get(expr.callee.name)
                if fn_def is not None and expr.named_args:
                    declared_names = {p.name for p in fn_def.params}
                    for arg_name, _ in expr.named_args:
                        if arg_name not in declared_names:
                            self._warn(
                                f"命名参数 '{arg_name}' 不在函数 '{expr.callee.name}' 的参数列表中",
                                expr)
                # 默认参数检查：有默认值的参数可以不传；缺失的必选参数警告
                if fn_def is not None:
                    positional_count = len(expr.args)
                    required = [p.name for p in fn_def.params
                                if p.default_value is None and not p.variadic]
                    # 已通过位置参数覆盖的必选参数
                    covered_pos = positional_count
                    missing = []
                    for i, p in enumerate(fn_def.params):
                        if p.variadic or p.default_value is not None:
                            continue
                        if i >= covered_pos:
                            # 检查是否通过命名参数提供
                            named_provided = any(n == p.name for n, _ in expr.named_args)
                            if not named_provided:
                                missing.append(p.name)
                    if missing:
                        self._warn(
                            f"函数 '{expr.callee.name}' 缺少必选参数: {missing}", expr)
                if callee_type and callee_type.params:
                    result = callee_type.params[-1]
                    for arg in expr.args:
                        self._infer_expr(arg, env)
                    for _, val in expr.named_args:
                        self._infer_expr(val, env)
                    return result
            for arg in expr.args:
                self._infer_expr(arg, env)
            for _, val in expr.named_args:
                self._infer_expr(val, env)
            return TypeInfo('any')
        elif isinstance(expr, MethodCall):
            obj_type = self._infer_expr(expr.object, env)
            # 可选类型空安全：对 Optional 直接调方法 -> 警告（除非用 ?. 或 !）
            if obj_type.name == 'Option' or obj_type.name.endswith('?'):
                self._warn(
                    f"对可选类型直接调用方法 '{expr.method}'，建议使用 ?. 或 ! 解包", expr)
            for arg in expr.args:
                self._infer_expr(arg, env)
            for _, val in expr.named_args:
                self._infer_expr(val, env)
            return TypeInfo('any')
        elif isinstance(expr, MemberAccess):
            obj_type = self._infer_expr(expr.object, env)
            if obj_type.name == 'Option' or obj_type.name.endswith('?'):
                self._warn(
                    f"对可选类型直接访问字段 '{expr.member}'，建议使用 ?. 或 ! 解包", expr)
            return TypeInfo('any')
        elif isinstance(expr, IndexAccess):
            obj_type = self._infer_expr(expr.object, env)
            self._infer_expr(expr.index, env)
            # 数组索引返回元素类型
            if obj_type.name.startswith('['):
                return TypeInfo(obj_type.name[1:-1] if len(obj_type.name) > 2 else 'any')
            return TypeInfo('any')
        elif isinstance(expr, TupleIndex):
            # 元组索引：返回对应位置的元素类型
            obj_type = self._infer_expr(expr.object, env)
            if obj_type.name == 'tuple' and obj_type.params:
                if 0 <= expr.index < len(obj_type.params):
                    return obj_type.params[expr.index]
            return TypeInfo('any')
        elif isinstance(expr, (ListComp, SetComp)):
            elem = self._infer_expr(expr.expr, env)
            for gen in expr.generators:
                self._infer_expr(gen.iterable, env)
            for cond in expr.conditions:
                self._infer_expr(cond, env)
            return TypeInfo(f'[{elem.name}]')
        elif isinstance(expr, MapComp):
            k = self._infer_expr(expr.key_expr, env)
            v = self._infer_expr(expr.value_expr, env)
            for gen in expr.generators:
                self._infer_expr(gen.iterable, env)
            for cond in expr.conditions:
                self._infer_expr(cond, env)
            return TypeInfo('map', [k, v])
        elif isinstance(expr, StructLiteral):
            for _, val in expr.fields:
                self._infer_expr(val, env)
            return TypeInfo(expr.type_name)
        elif isinstance(expr, ForcedUnwrap):
            inner = self._infer_expr(expr.operand, env)
            # 去掉 Optional 包装
            if inner.name == 'Option' and inner.params:
                return inner.params[0]
            return inner
        elif isinstance(expr, LambdaExpr):
            return TypeInfo('fn')
        elif isinstance(expr, IfExpr):
            return self._infer_expr(expr.then_body.statements[-1] if expr.then_body.statements else NilLiteral(), env)
        elif isinstance(expr, MatchExpr):
            return TypeInfo('any')
        elif isinstance(expr, SpawnExpr):
            return TypeInfo('fiber')
        elif isinstance(expr, SourceExpr):
            # v3.3.0: source(value) → Source<T>
            inner = self._infer_expr(expr.value, env)
            return TypeInfo("Source", [inner])
        elif isinstance(expr, LiveBlockExpr):
            # v3.3.0: live { block } → Live<T>
            inner_type = TypeInfo("dynamic")
            if expr.body and expr.body.statements:
                for stmt in reversed(expr.body.statements):
                    if hasattr(stmt, 'expr') and stmt.expr is not None:
                        inner_type = self._infer_expr(stmt.expr, env)
                        break
            # 编译期纯度检查（违规作为错误收集）
            self._check_live_purity(expr, env)
            return TypeInfo("Live", [inner_type])
        elif isinstance(expr, TransactBlockExpr):
            # v3.3.0: transact { block } → 块内最后表达式类型
            inner_type = TypeInfo("dynamic")
            if expr.body and expr.body.statements:
                for stmt in reversed(expr.body.statements):
                    if hasattr(stmt, 'expr') and stmt.expr is not None:
                        inner_type = self._infer_expr(stmt.expr, env)
                        break
            return inner_type
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
        elif isinstance(node, OptionalType):
            inner = self._resolve_type_node(node.inner, env)
            return TypeInfo('Option', [inner])
        elif isinstance(node, ResultType):
            ok = self._resolve_type_node(node.ok_type, env) if node.ok_type else TypeInfo('any')
            err = self._resolve_type_node(node.err_type, env) if node.err_type else TypeInfo('any')
            return TypeInfo('Result', [ok, err])
        return TypeInfo('any')
