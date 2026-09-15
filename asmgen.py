"""
Aurora ARM64 汇编代码生成器
将 Aurora AST 直接转换为 ARM64 汇编代码，通过系统 as/ld 生成原生可执行文件。
不依赖 C 编译器和 C 运行时库，直接使用 macOS 系统调用。

支持特性:
- 纯整数函数的类型特化(直接使用 x 寄存器,零运行时开销)
- 函数定义与递归调用
- 算术/比较/逻辑运算
- if/elif/else 条件语句
- while 循环 + break/continue
- for 循环(range)
- 变量声明与赋值
- println 整数输出(通过 write syscall)
- 编译期常量折叠
- 自动记忆化(递归纯 int 单参数函数)

P1 性能优化 Pass(在代码生成前对 AST 做保守变换,顺序执行):
1. DCE  死代码消除 dead_code_elimination(fn):
   a) 函数级基本块可达性分析 —— 删除 return/throw/panic/break/continue 之后
      的不可达语句(解析器可能保留了 return 后的代码);
   b) 简单 def-use 分析 —— 删除"赋值后从未被读取、且初值无副作用"的局部
      let/const 标量变量;
   c) 调用图可达性分析 —— 删除从未被 main/顶层语句/活跃函数调用的函数。
   保守原则:初值含函数调用/索引访问/容器构造等副作用一律不删。
2. 常量传播 constant_propagation(fn):
   跟踪"从未重新赋值、初值为字面量"的 let/const 标量变量,在其作用域内把使用点
   直接替换为字面量副本。与编译期求值配合:传播后更多函数调用变为全字面量参数,
   自动触发 _try_compile_time_eval。函数参数/for 循环变量/被重新赋值的变量不处理。
3. TCO  尾调用优化(在代码生成阶段识别,见 gen_return_stmt / _try_gen_tail_call):
   识别 `return f(args...)` 尾调用:目标为直接函数调用、目标参数个数 <= 当前参数
   个数、实参 <= 8 个且无嵌套调用/索引/容器构造、当前函数未启用记忆化时,把实参
   载入 x0-x7,执行与 epilogue 对称的弹栈后 `b f` 跳转(而非 `bl`),复用当前栈帧,
   目标函数的 ret 直接返回给本函数的调用者,使尾递归占用 O(1) 栈。
"""
import os
import tempfile
from aurora.ast_nodes import *
from aurora.type_infer import infer_program_types, is_pure_int_function, TypeKind, TYPE_INT


class ARM64CodeGenerator:
    """Aurora AST → ARM64 汇编代码生成器"""

    def __init__(self):
        self.output = []           # 汇编代码行
        self.data_section = []     # 数据段
        self.string_literals = {}  # 字符串字面量 -> 标签
        self.string_counter = 0
        self.label_counter = 0
        self.function_types = {}
        self._program_statements = []
        self.functions = {}        # name -> FnDef
        self.current_fn = None
        self.current_fn_pure_int = False
        self.variable_regs = {}    # 变量名 -> 栈偏移
        self.var_types = {}        # 变量名 -> 'int'/'float'/'str'/'array'/'map'
        self.stack_offset = 0      # 当前栈偏移
        self.stack_frame_size = 0  # 当前函数栈帧大小
        self._memoized_funcs = set()  # 需要记忆化的函数

    # ============================================================
    # 工具方法
    # ============================================================
    def emit(self, code=""):
        """输出一行汇编代码(带缩进)"""
        if code:
            self.output.append("    " + code)
        else:
            self.output.append("")

    def emit_raw(self, code):
        """输出原始代码(不缩进)"""
        self.output.append(code)

    def new_label(self, prefix="L"):
        """生成新标签"""
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"

    def get_string_label(self, s):
        """获取字符串字面量的标签,不存在则创建"""
        if s not in self.string_literals:
            self.string_counter += 1
            label = f"_str_{self.string_counter}"
            self.string_literals[s] = label
            # 转义特殊字符,使用 .asciz 自动添加 null terminator
            escaped = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
            self.data_section.append(f'{label}: .asciz "{escaped}"')
            self.data_section.append(f'{label}_len = . - {label} - 1')
        return self.string_literals[s]

    def c_ident(self, name):
        """转换为合法的汇编标识符"""
        result = name.replace('?', '_q').replace('!', '_b').replace('-', '_')
        return f"_aurora_{result}"

    # ============================================================
    # 寄存器与栈管理
    # ============================================================
    def _alloc_stack_var(self, name):
        """在栈上分配一个变量,返回偏移量(相对于 FP)。如果变量已分配到寄存器,返回 None。"""
        if hasattr(self, 'var_to_reg') and name in self.var_to_reg:
            return None
        self.stack_offset += 8
        self.variable_regs[name] = self.stack_offset
        return self.stack_offset

    def _get_var_offset(self, name):
        """获取变量的栈偏移。如果变量在寄存器中,返回 None。"""
        if hasattr(self, 'var_to_reg') and name in self.var_to_reg:
            return None
        if name in self.variable_regs:
            return self.variable_regs[name]
        return None

    def _get_var_reg(self, name):
        """获取变量所在的寄存器。如果变量在栈上,返回 None。"""
        if hasattr(self, 'var_to_reg') and name in self.var_to_reg:
            return self.var_to_reg[name]
        return None

    def _load_var_to_reg(self, name, dest_reg):
        """将变量加载到目标寄存器(自动判断寄存器还是栈)"""
        reg = self._get_var_reg(name)
        if reg:
            if reg != dest_reg:
                self.emit(f'mov {dest_reg}, {reg}')
        else:
            offset = self._get_var_offset(name)
            if offset:
                self.emit(f'ldr {dest_reg}, [x29, #-{offset}]')
            else:
                self.emit(f'mov {dest_reg}, #0')

    def _store_reg_to_var(self, src_reg, name):
        """将寄存器值存储到变量(自动判断寄存器还是栈)"""
        reg = self._get_var_reg(name)
        if reg:
            if reg != src_reg:
                self.emit(f'mov {reg}, {src_reg}')
        else:
            offset = self._get_var_offset(name)
            if offset:
                self.emit(f'str {src_reg}, [x29, #-{offset}]')

    # ============================================================
    # 程序生成
    # ============================================================
    def generate(self, program: Program) -> str:
        """生成完整的 ARM64 汇编程序"""
        self.output = []
        self.data_section = []
        self.string_literals = {}
        self.string_counter = 0
        self.label_counter = 0

        # 运行类型推断器
        self.function_types = infer_program_types(program)
        self._program_statements = program.statements

        # 收集函数定义
        for stmt in program.statements:
            if isinstance(stmt, FnDef):
                self.functions[stmt.name] = stmt

        # ============================================================
        # P1 优化 Pass 管线 (在代码生成前对 AST 做变换)
        # 顺序: DCE(删死函数 → 每函数 DCE) → 常量传播
        # TCO 在代码生成阶段(gen_return_stmt)按模式识别,无需 AST 改写。
        # 全部保守实现:不确定安全时不优化。
        # ============================================================
        self._pass_dce_functions(program)
        for fn in list(self.functions.values()):
            self.dead_code_elimination(fn)
            self.constant_propagation(fn)

        # 分离顶层语句
        top_level_stmts = []
        for stmt in program.statements:
            if isinstance(stmt, FnDef):
                pass
            elif isinstance(stmt, (TypeDef, EnumDef, TraitDef, ImplBlock, ImportStmt, TestBlock)):
                pass
            else:
                top_level_stmts.append(stmt)

        # 文件头
        self.emit_raw('// Aurora ARM64 汇编输出')
        self.emit_raw('// 由 Aurora 编译器自动生成')
        self.emit_raw('')
        self.emit_raw('.global _main')
        self.emit_raw('.align 2')
        self.emit_raw('')

        # 文本段
        self.emit_raw('.text')
        self.emit_raw('')

        # 生成所有函数
        for stmt in program.statements:
            if isinstance(stmt, FnDef):
                self.gen_function(stmt)

        # 生成顶层语句包装函数
        if top_level_stmts:
            self._gen_top_level(top_level_stmts)

        # 生成 _main 入口
        self._gen_main_entry(top_level_stmts)

        # 生成内置辅助函数
        self._gen_builtin_helpers()

        # 数据段
        if self.data_section:
            self.emit_raw('')
            self.emit_raw('.data')
            self.emit_raw('.align 3')
            for line in self.data_section:
                self.emit_raw(line)

        return "\n".join(self.output)

    # ============================================================
    # P1 优化 Pass: DCE → 常量传播 → (TCO 见 gen_return_stmt)
    # 所有 pass 均为保守实现:不确定安全时不做变换。
    # ============================================================

    # ---------- 通用 AST 遍历工具 ----------
    def _expr_children(self, expr):
        """返回表达式的所有子表达式(不含 CallExpr.callee,函数名不是变量读取)"""
        ch = []
        if isinstance(expr, BinaryOp):
            ch = [expr.left, expr.right]
        elif isinstance(expr, UnaryOp):
            ch = [expr.operand]
        elif isinstance(expr, CallExpr):
            ch = list(expr.args) + [v for _, v in expr.named_args]
        elif isinstance(expr, MethodCall):
            ch = [expr.object] + list(expr.args) + [v for _, v in expr.named_args]
        elif isinstance(expr, IndexAccess):
            ch = [expr.object, expr.index]
        elif isinstance(expr, ArrayLiteral):
            ch = list(expr.elements)
        elif isinstance(expr, MapLiteral):
            for k, v in expr.entries:
                ch.append(k); ch.append(v)
        elif isinstance(expr, StringInterpolation):
            ch = list(expr.parts)
        elif isinstance(expr, IfExpr):
            ch = [expr.condition]
        elif isinstance(expr, OptionalAccess):
            ch = [expr.object]
        elif isinstance(expr, OptionalCall):
            ch = [expr.object] + list(expr.args)
        elif isinstance(expr, NullCoalesce):
            ch = [expr.left, expr.right]
        elif isinstance(expr, RefExpr):
            ch = [expr.inner]
        elif isinstance(expr, TupleLiteral):
            ch = list(expr.elements)
        elif isinstance(expr, TupleIndex):
            ch = [expr.object]
        elif isinstance(expr, ForcedUnwrap):
            ch = [expr.operand]
        elif isinstance(expr, PipeExpr):
            ch = [expr.left, expr.call]
        elif isinstance(expr, (ListComp, SetComp)):
            ch = [expr.expr] + [g.iterable for g in expr.generators] + list(expr.conditions)
        elif isinstance(expr, MapComp):
            ch = ([expr.key_expr, expr.value_expr]
                  + [g.iterable for g in expr.generators] + list(expr.conditions))
        elif isinstance(expr, StructLiteral):
            ch = [v for _, v in expr.fields]
        elif isinstance(expr, MatchExpr):
            ch = [expr.subject] + [arm.body for arm in expr.arms]
        return [c for c in ch if c is not None]

    def _exprs_of_stmt(self, stmt):
        """语句中直接包含的表达式列表(一层,不递归)"""
        out = []
        if isinstance(stmt, (LetStmt, ConstStmt)):
            if stmt.initializer:
                out.append(stmt.initializer)
        elif isinstance(stmt, AssignStmt):
            out.append(stmt.value)
            if isinstance(stmt.target, IndexAccess):
                out.append(stmt.target.object)
                out.append(stmt.target.index)
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                out.append(stmt.value)
        elif isinstance(stmt, ExprStmt):
            out.append(stmt.expr)
        elif isinstance(stmt, IfStmt):
            out.append(stmt.condition)
        elif isinstance(stmt, WhileStmt):
            out.append(stmt.condition)
        elif isinstance(stmt, ForStmt):
            out.append(stmt.iterable)
        elif isinstance(stmt, DestructureLet):
            if stmt.initializer:
                out.append(stmt.initializer)
        elif isinstance(stmt, MatchStmt):
            out.append(stmt.subject)
            out += [arm.body for arm in stmt.arms]
        return out

    def _visit_all_stmts(self, block, visit):
        """深度优先遍历块内及所有嵌套位置(含 IfExpr 表达式内嵌块)的语句"""
        if block is None:
            return
        for stmt in list(block.statements):
            visit(stmt)
            if isinstance(stmt, IfStmt):
                self._visit_all_stmts(stmt.then_body, visit)
                for _, b in stmt.elif_clauses:
                    self._visit_all_stmts(b, visit)
                self._visit_all_stmts(stmt.else_body, visit)
            elif isinstance(stmt, (ForStmt, WhileStmt)):
                self._visit_all_stmts(stmt.body, visit)
            elif isinstance(stmt, TryStmt):
                self._visit_all_stmts(stmt.body, visit)
                for c in stmt.catches:
                    self._visit_all_stmts(c.body, visit)
                self._visit_all_stmts(stmt.finally_body, visit)
            elif isinstance(stmt, Block):
                self._visit_all_stmts(stmt, visit)
            # 表达式内嵌的语句块(IfExpr 等)
            for expr in self._exprs_of_stmt(stmt):
                self._visit_expr_blocks(expr, visit)

    def _visit_expr_blocks(self, expr, visit):
        """递归表达式,访问其中嵌套的语句块(IfExpr 的分支块)"""
        if expr is None:
            return
        if isinstance(expr, IfExpr):
            self._visit_all_stmts(expr.then_body, visit)
            for cond, b in expr.elif_clauses:
                self._visit_all_stmts(b, visit)
            self._visit_all_stmts(expr.else_body, visit)
        for ch in self._expr_children(expr):
            self._visit_expr_blocks(ch, visit)

    def _for_each_block(self, block, fn):
        """对函数中所有语句块(含嵌套)应用 fn(block)"""
        if block is None:
            return
        fn(block)
        for stmt in list(block.statements):
            if isinstance(stmt, IfStmt):
                self._for_each_block(stmt.then_body, fn)
                for _, b in stmt.elif_clauses:
                    self._for_each_block(b, fn)
                self._for_each_block(stmt.else_body, fn)
            elif isinstance(stmt, (ForStmt, WhileStmt)):
                self._for_each_block(stmt.body, fn)
            elif isinstance(stmt, TryStmt):
                self._for_each_block(stmt.body, fn)
                for c in stmt.catches:
                    self._for_each_block(c.body, fn)
                self._for_each_block(stmt.finally_body, fn)
            elif isinstance(stmt, Block):
                self._for_each_block(stmt, fn)
            for expr in self._exprs_of_stmt(stmt):
                self._for_each_expr_blocks(expr, fn)

    def _for_each_expr_blocks(self, expr, fn):
        if expr is None:
            return
        if isinstance(expr, IfExpr):
            self._for_each_block(expr.then_body, fn)
            for _, b in expr.elif_clauses:
                self._for_each_block(b, fn)
            self._for_each_block(expr.else_body, fn)
        for ch in self._expr_children(expr):
            self._for_each_expr_blocks(ch, fn)

    # ---------- Pass 1a/1b: 函数级 DCE ----------
    def dead_code_elimination(self, fn: FnDef):
        """函数级死代码消除:
        (a) 删除 return/throw/panic/break/continue 之后的不可达语句;
        (b) 删除从未被读取、且初值无副作用的 let/const 局部标量变量。"""
        self._dce_block(fn.body)
        self._dce_remove_unused_lets(fn)

    def _dce_block(self, block):
        """线性扫描块:遇到终止语句后丢弃其后的语句,并递归处理嵌套块"""
        if block is None:
            return
        kept = []
        for stmt in list(block.statements):
            kept.append(stmt)
            self._dce_recurse(stmt)
            if self._dce_is_terminator(stmt):
                break
        block.statements = kept

    def _dce_recurse(self, stmt):
        """递归进入语句的嵌套块,对每个嵌套块做不可达删除"""
        if isinstance(stmt, IfStmt):
            self._dce_block(stmt.then_body)
            for _, body in stmt.elif_clauses:
                self._dce_block(body)
            self._dce_block(stmt.else_body)
        elif isinstance(stmt, WhileStmt):
            self._dce_block(stmt.body)
        elif isinstance(stmt, ForStmt):
            self._dce_block(stmt.body)
        elif isinstance(stmt, TryStmt):
            self._dce_block(stmt.body)
            for c in stmt.catches:
                self._dce_block(c.body)
            self._dce_block(stmt.finally_body)
        elif isinstance(stmt, Block):
            self._dce_block(stmt)
        elif isinstance(stmt, IfExpr):
            self._dce_block(stmt.then_body)
            for _, body in stmt.elif_clauses:
                self._dce_block(body)
            self._dce_block(stmt.else_body)

    def _dce_is_terminator(self, stmt):
        """该语句是否使当前基本块后续代码不可达"""
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, (BreakStmt, ContinueStmt)):
            return True
        if isinstance(stmt, ExprStmt) and isinstance(stmt.expr, CallExpr):
            callee = stmt.expr.callee
            if isinstance(callee, Identifier) and callee.name in ('throw', 'panic'):
                return True
        return False

    def _collect_reassigned_names(self, block, out):
        """收集所有被赋值(含复合赋值)的标识符变量名"""
        def visit(stmt):
            if isinstance(stmt, AssignStmt) and isinstance(stmt.target, Identifier):
                out.add(stmt.target.name)
        self._visit_all_stmts(block, visit)

    def _collect_for_var_names(self, block, out):
        """收集 for 循环变量名(由循环自行赋值,不能视为常量)"""
        def visit(stmt):
            if isinstance(stmt, ForStmt):
                out.update(stmt.variables)
        self._visit_all_stmts(block, visit)

    def _collect_idents_in_expr(self, expr, out):
        """递归统计表达式中所有标识符的读取次数(CallExpr.callee 不算变量读取)"""
        if expr is None:
            return
        if isinstance(expr, Identifier):
            out[expr.name] = out.get(expr.name, 0) + 1
            return
        for ch in self._expr_children(expr):
            self._collect_idents_in_expr(ch, out)

    def _expr_is_pure(self, expr):
        """判断表达式是否无副作用(保守:无函数调用/索引读/容器构造等)"""
        if expr is None:
            return True
        if isinstance(expr, (IntLiteral, FloatLiteral, StringLiteral,
                             BoolLiteral, NilLiteral, Identifier)):
            return True
        if isinstance(expr, BinaryOp):
            return self._expr_is_pure(expr.left) and self._expr_is_pure(expr.right)
        if isinstance(expr, UnaryOp):
            return self._expr_is_pure(expr.operand)
        return False

    def _dce_remove_unused_lets(self, fn: FnDef):
        """删除"从未被读取且初值无副作用"的 let/const 局部标量变量。
        只处理纯初值(字面量/纯算术/纯变量引用),有副作用的初值一律保留。"""
        if not fn.body:
            return
        params = {p.name for p in fn.params}
        reassigned = set()
        for_vars = set()
        self._collect_reassigned_names(fn.body, reassigned)
        self._collect_for_var_names(fn.body, for_vars)

        # 统计所有标识符的读取次数
        uses = {}
        def visit(stmt):
            if isinstance(stmt, AssignStmt):
                if isinstance(stmt.target, IndexAccess):
                    self._collect_idents_in_expr(stmt.target.object, uses)
                    self._collect_idents_in_expr(stmt.target.index, uses)
                self._collect_idents_in_expr(stmt.value, uses)
            else:
                for e in self._exprs_of_stmt(stmt):
                    self._collect_idents_in_expr(e, uses)
        self._visit_all_stmts(fn.body, visit)

        # 扫描每个块,删除候选未使用变量
        def scan(block):
            kept = []
            for stmt in block.statements:
                drop = False
                if isinstance(stmt, (LetStmt, ConstStmt)):
                    name = stmt.name
                    if (name not in params and name not in for_vars
                            and name not in reassigned
                            and uses.get(name, 0) == 0
                            and self._expr_is_pure(stmt.initializer)):
                        drop = True
                if not drop:
                    kept.append(stmt)
            block.statements = kept
        self._for_each_block(fn.body, scan)

    # ---------- Pass 1c: 删除从未被调用的函数 ----------
    def _collect_fn_refs_in_expr(self, expr, fn_names, out):
        """递归收集表达式中以已知函数名为 callee 的直接调用"""
        if expr is None:
            return
        if isinstance(expr, CallExpr):
            if isinstance(expr.callee, Identifier) and expr.callee.name in fn_names:
                out.add(expr.callee.name)
        for ch in self._expr_children(expr):
            self._collect_fn_refs_in_expr(ch, fn_names, out)

    def _collect_fn_refs_block(self, block, fn_names, out):
        def visit(stmt):
            for e in self._exprs_of_stmt(stmt):
                self._collect_fn_refs_in_expr(e, fn_names, out)
        self._visit_all_stmts(block, visit)

    def _pass_dce_functions(self, program: Program):
        """调用图可达性分析:从 main 和顶层语句出发,删除从未被活跃代码调用的函数。
        保守:只删除无任何直接调用引用的函数;有引用的一律保留。"""
        fn_names = {s.name for s in program.statements if isinstance(s, FnDef)}
        if not fn_names:
            return

        live = set()
        if 'main' in fn_names:
            live.add('main')
        # 顶层语句中直接调用的函数都视为活跃(运行时会被执行)
        top_block = Block(statements=[
            s for s in program.statements if not isinstance(s, FnDef)
        ])
        self._collect_fn_refs_block(top_block, fn_names, live)

        # 迭代传播调用图:活跃函数调用的函数也活跃
        worklist = list(live)
        while worklist:
            name = worklist.pop()
            fn = self.functions.get(name)
            if fn is None or not fn.body:
                continue
            refs = set()
            self._collect_fn_refs_block(fn.body, fn_names, refs)
            for r in refs:
                if r not in live:
                    live.add(r)
                    worklist.append(r)

        dead = fn_names - live
        if not dead:
            return
        program.statements = [
            s for s in program.statements
            if not (isinstance(s, FnDef) and s.name in dead)
        ]
        for n in dead:
            self.functions.pop(n, None)

    # ---------- Pass 2: 常量传播 ----------
    def constant_propagation(self, fn: FnDef):
        """函数级常量传播:
        对"从未重新赋值、初值为字面量"的 let/const 标量变量,在其作用域内把使用点
        直接替换为字面量副本。与编译期求值配合:传播后更多调用变为全字面量参数,
        自动触发 _try_compile_time_eval。
        限制:函数参数、for 循环变量、任何被重新赋值过的变量都不处理。"""
        if not fn.body:
            return
        params = {p.name for p in fn.params}
        reassigned = set()
        for_vars = set()
        self._collect_reassigned_names(fn.body, reassigned)
        self._collect_for_var_names(fn.body, for_vars)
        excluded = params | reassigned | for_vars
        self._cp_block(fn.body, excluded, {})

    def _cp_block(self, block, excluded, env):
        """顺序遍历块:遇到可传播的常量声明则记入 env,块结束后恢复 env"""
        if block is None:
            return
        saved = dict(env)
        for stmt in block.statements:
            if isinstance(stmt, (LetStmt, ConstStmt)):
                if stmt.initializer is not None:
                    # 先传播初值中的变量(如 let x = y,而 y 已是常量)
                    stmt.initializer = self._cp_expr(stmt.initializer, env)
                    lit = self._as_pure_literal(stmt.initializer)
                    name = stmt.name
                    if lit is not None and name not in excluded:
                        env[name] = lit
            else:
                self._cp_stmt(stmt, excluded, env)
        env.clear()
        env.update(saved)

    def _cp_stmt(self, stmt, excluded, env):
        """在语句表达式中传播常量;递归进入嵌套块"""
        if isinstance(stmt, AssignStmt):
            stmt.value = self._cp_expr(stmt.value, env)
            if isinstance(stmt.target, IndexAccess):
                stmt.target.object = self._cp_expr(stmt.target.object, env)
                stmt.target.index = self._cp_expr(stmt.target.index, env)
            # 赋值会改写目标变量,失效其常量传播
            if isinstance(stmt.target, Identifier):
                env.pop(stmt.target.name, None)
            elif isinstance(stmt.target, TupleLiteral):
                for tgt in stmt.target.elements:
                    if isinstance(tgt, Identifier):
                        env.pop(tgt.name, None)
        elif isinstance(stmt, DestructureLet):
            if stmt.initializer is not None:
                stmt.initializer = self._cp_expr(stmt.initializer, env)
            # 解构绑定会改写这些变量,失效其常量
            for name in stmt.names:
                env.pop(name, None)
        elif isinstance(stmt, MatchStmt):
            stmt.subject = self._cp_expr(stmt.subject, env)
            for arm in stmt.arms:
                arm.body = self._cp_expr(arm.body, env)
        elif isinstance(stmt, IfStmt):
            stmt.condition = self._cp_expr(stmt.condition, env)
            self._cp_block(stmt.then_body, excluded, env)
            new_clauses = []
            for cond, body in stmt.elif_clauses:
                new_clauses.append((self._cp_expr(cond, env), body))
                self._cp_block(body, excluded, env)
            stmt.elif_clauses = new_clauses
            self._cp_block(stmt.else_body, excluded, env)
        elif isinstance(stmt, WhileStmt):
            stmt.condition = self._cp_expr(stmt.condition, env)
            self._cp_block(stmt.body, excluded, env)
        elif isinstance(stmt, ForStmt):
            stmt.iterable = self._cp_expr(stmt.iterable, env)
            self._cp_block(stmt.body, excluded, env)
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                stmt.value = self._cp_expr(stmt.value, env)
        elif isinstance(stmt, ExprStmt):
            stmt.expr = self._cp_expr(stmt.expr, env)
        elif isinstance(stmt, TryStmt):
            self._cp_block(stmt.body, excluded, env)
            for c in stmt.catches:
                self._cp_block(c.body, excluded, env)
            self._cp_block(stmt.finally_body, excluded, env)
        elif isinstance(stmt, Block):
            self._cp_block(stmt, excluded, env)

    def _cp_expr(self, expr, env):
        """递归复制表达式:env 中的常量变量替换为字面量副本"""
        if expr is None:
            return expr
        if isinstance(expr, Identifier):
            if expr.name in env:
                return self._copy_literal(env[expr.name])
            return expr
        if isinstance(expr, BinaryOp):
            expr.left = self._cp_expr(expr.left, env)
            expr.right = self._cp_expr(expr.right, env)
        elif isinstance(expr, UnaryOp):
            expr.operand = self._cp_expr(expr.operand, env)
        elif isinstance(expr, CallExpr):
            expr.args = [self._cp_expr(a, env) for a in expr.args]
            expr.named_args = [(n, self._cp_expr(v, env)) for n, v in expr.named_args]
        elif isinstance(expr, MethodCall):
            expr.object = self._cp_expr(expr.object, env)
            expr.args = [self._cp_expr(a, env) for a in expr.args]
        elif isinstance(expr, IndexAccess):
            expr.object = self._cp_expr(expr.object, env)
            expr.index = self._cp_expr(expr.index, env)
        elif isinstance(expr, ArrayLiteral):
            expr.elements = [self._cp_expr(e, env) for e in expr.elements]
        elif isinstance(expr, MapLiteral):
            expr.entries = [(self._cp_expr(k, env), self._cp_expr(v, env))
                            for k, v in expr.entries]
        elif isinstance(expr, StringInterpolation):
            expr.parts = [self._cp_expr(p, env) for p in expr.parts]
        elif isinstance(expr, IfExpr):
            expr.condition = self._cp_expr(expr.condition, env)
            self._cp_block(expr.then_body, None, env)
            for i, (cond, body) in enumerate(expr.elif_clauses):
                expr.elif_clauses[i] = (self._cp_expr(cond, env), body)
                self._cp_block(body, None, env)
            self._cp_block(expr.else_body, None, env)
        elif isinstance(expr, OptionalCall):
            expr.object = self._cp_expr(expr.object, env)
            expr.args = [self._cp_expr(a, env) for a in expr.args]
        elif isinstance(expr, OptionalAccess):
            expr.object = self._cp_expr(expr.object, env)
        elif isinstance(expr, NullCoalesce):
            expr.left = self._cp_expr(expr.left, env)
            expr.right = self._cp_expr(expr.right, env)
        elif isinstance(expr, TupleLiteral):
            expr.elements = [self._cp_expr(e, env) for e in expr.elements]
        elif isinstance(expr, TupleIndex):
            expr.object = self._cp_expr(expr.object, env)
        elif isinstance(expr, ForcedUnwrap):
            expr.operand = self._cp_expr(expr.operand, env)
        elif isinstance(expr, PipeExpr):
            expr.left = self._cp_expr(expr.left, env)
            expr.call = self._cp_expr(expr.call, env)
        elif isinstance(expr, (ListComp, SetComp)):
            expr.expr = self._cp_expr(expr.expr, env)
            for g in expr.generators:
                g.iterable = self._cp_expr(g.iterable, env)
            expr.conditions = [self._cp_expr(c, env) for c in expr.conditions]
        elif isinstance(expr, MapComp):
            expr.key_expr = self._cp_expr(expr.key_expr, env)
            expr.value_expr = self._cp_expr(expr.value_expr, env)
            for g in expr.generators:
                g.iterable = self._cp_expr(g.iterable, env)
            expr.conditions = [self._cp_expr(c, env) for c in expr.conditions]
        elif isinstance(expr, StructLiteral):
            expr.fields = [(n, self._cp_expr(v, env)) for n, v in expr.fields]
        elif isinstance(expr, MatchExpr):
            expr.subject = self._cp_expr(expr.subject, env)
            for arm in expr.arms:
                arm.body = self._cp_expr(arm.body, env)
        return expr

    def _as_pure_literal(self, expr):
        """若表达式是纯字面量则返回它,否则 None(用于常量传播的资格判断)"""
        if isinstance(expr, (IntLiteral, FloatLiteral, StringLiteral,
                             BoolLiteral, NilLiteral)):
            return expr
        return None

    def _copy_literal(self, lit):
        """字面量深拷贝(避免改写 AST 共享节点)"""
        if isinstance(lit, IntLiteral):
            return IntLiteral(value=int(lit.value))
        if isinstance(lit, FloatLiteral):
            return FloatLiteral(value=float(lit.value))
        if isinstance(lit, StringLiteral):
            return StringLiteral(value=lit.value, raw=getattr(lit, 'raw', False))
        if isinstance(lit, BoolLiteral):
            return BoolLiteral(value=bool(lit.value))
        if isinstance(lit, NilLiteral):
            return NilLiteral()
        return lit

    def _gen_main_entry(self, top_level_stmts):
        """生成 _main 入口函数"""
        self.emit_raw('')
        self.emit_raw('_main:')
        self.emit('// 函数 prologue')
        self.emit('stp x29, x30, [sp, #-16]!')
        self.emit('mov x29, sp')
        self.emit('')

        has_main = 'main' in self.functions

        if has_main:
            self.emit('// 调用 Aurora main()')
            self.emit('bl _aurora_main')
            self.emit('')

        if top_level_stmts:
            self.emit('// 执行顶层语句')
            self.emit('bl _aurora_top_level')
            self.emit('')

        self.emit('// exit(0)')
        self.emit('mov x0, #0')
        self.emit('mov x16, #1')
        self.emit('svc #0')

    def _gen_top_level(self, stmts):
        """生成顶层语句包装函数"""
        # 估算局部变量数量
        local_count = 0
        for stmt in stmts:
            if isinstance(stmt, (LetStmt, ConstStmt)):
                local_count += 1
        stack_size = 16 + 128 + (local_count + 5) * 8  # FP/LR + 临时槽位 + 局部变量 + 预留
        stack_size = (stack_size + 15) & ~15

        self.emit_raw('')
        self.emit_raw('_aurora_top_level:')
        self.emit('stp x29, x30, [sp, #-16]!')
        self.emit('mov x29, sp')
        if stack_size > 16:
            self.emit(f'sub sp, sp, #{stack_size - 16}')
        self.emit('')

        self.current_fn = '_aurora_top_level'
        self.current_fn_pure_int = False
        self.variable_regs = {}
        self.var_to_reg = {}
        self.var_to_stack = {}
        self.stack_offset = 128
        self._temp_depth = 0
        self._current_epilogue_label = None

        for stmt in stmts:
            self.gen_stmt(stmt)

        self.emit('')
        if stack_size > 16:
            self.emit(f'add sp, sp, #{stack_size - 16}')
        self.emit('ldp x29, x30, [sp], #16')
        self.emit('ret')

        self.current_fn = None
        self.variable_regs = {}

    # ============================================================
    # 函数生成
    # ============================================================
    # 可用于变量分配的被调用者保存寄存器
    ALLOCATABLE_REGS = ['x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25']

    def _collect_variables(self, fn: FnDef) -> list:
        """收集函数中所有变量(参数 + let/var 声明),按出现顺序"""
        vars_list = []
        seen = set()
        for param in fn.params:
            if param.name not in seen:
                vars_list.append(param.name)
                seen.add(param.name)
        if fn.body:
            for stmt in fn.body.statements:
                self._collect_vars_from_stmt(stmt, vars_list, seen)
        return vars_list

    def _collect_vars_from_stmt(self, stmt, vars_list, seen):
        """从语句中收集变量声明"""
        if isinstance(stmt, (LetStmt, ConstStmt)):
            if stmt.name not in seen:
                vars_list.append(stmt.name)
                seen.add(stmt.name)
        elif isinstance(stmt, DestructureLet):
            for name in stmt.names:
                if name not in seen:
                    vars_list.append(name)
                    seen.add(name)
        elif isinstance(stmt, IfStmt):
            if stmt.then_body:
                for s in stmt.then_body.statements:
                    self._collect_vars_from_stmt(s, vars_list, seen)
            if stmt.else_body:
                for s in stmt.else_body.statements:
                    self._collect_vars_from_stmt(s, vars_list, seen)
            for _, body in stmt.elif_clauses:
                if body:
                    for s in body.statements:
                        self._collect_vars_from_stmt(s, vars_list, seen)
        elif isinstance(stmt, (ForStmt, WhileStmt)):
            if isinstance(stmt, ForStmt) and stmt.variables:
                for v in stmt.variables:
                    if v not in seen:
                        vars_list.append(v)
                        seen.add(v)
            if stmt.body:
                for s in stmt.body.statements:
                    self._collect_vars_from_stmt(s, vars_list, seen)

    def gen_function(self, fn: FnDef):
        """生成函数定义"""
        fn_type = self.function_types.get(fn.name, {})
        pure_int = is_pure_int_function(fn_type) if fn_type else False

        # 检测是否需要自动记忆化
        need_memo = (pure_int and len(fn.params) == 1 and
                     self._is_recursive_function(fn))
        if need_memo:
            self._memoized_funcs.add(fn.name)

        self.emit_raw('')
        self.emit_raw(f'{self.c_ident(fn.name)}:')
        self.emit(f'// 函数: {fn.name} (pure_int={pure_int}, memo={need_memo})')

        # 创建统一的 epilogue 标签
        epilogue_label = self.new_label("epilogue")
        self._current_epilogue_label = epilogue_label

        # 寄存器分配:前 N 个变量分配到寄存器
        all_vars = self._collect_variables(fn)
        self.var_to_reg = {}  # 变量名 -> 寄存器
        self.var_to_stack = {}  # 变量名 -> 栈偏移
        reg_idx = 0
        for var_name in all_vars:
            if reg_idx < len(self.ALLOCATABLE_REGS):
                self.var_to_reg[var_name] = self.ALLOCATABLE_REGS[reg_idx]
                reg_idx += 1
            else:
                self.var_to_stack[var_name] = None  # 延迟分配

        used_regs = list(self.var_to_reg.values())
        num_used_regs = len(used_regs)

        # 计算栈帧大小: FP/LR(16) + 保存的寄存器 + 临时槽位(128) + 栈上变量
        stack_var_count = len(all_vars) - num_used_regs
        stack_size = 16 + num_used_regs * 8 + 128 + stack_var_count * 8
        stack_size = (stack_size + 15) & ~15
        self._current_stack_size = stack_size
        # TCO 需要对称地弹栈(恢复 callee-saved 寄存器并释放帧),记录这些信息
        self._tco_used_regs = used_regs
        self._tco_stack_size = stack_size

        self.current_fn = fn.name
        self.current_fn_pure_int = pure_int
        self.variable_regs = {}  # 兼容旧代码,存栈变量偏移
        self.stack_offset = 128 + num_used_regs * 8  # 临时槽位 + 保存的寄存器之后
        self._temp_depth = 0

        # Prologue
        self.emit('stp x29, x30, [sp, #-16]!')
        self.emit('mov x29, sp')
        if stack_size > 16:
            self.emit(f'sub sp, sp, #{stack_size - 16}')
        # 保存使用的被调用者保存寄存器
        for i, reg in enumerate(used_regs):
            self.emit(f'str {reg}, [sp, #{i * 8}]')

        # 参数加载到分配的位置(寄存器或栈)
        param_regs = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7']
        for i, param in enumerate(fn.params):
            if i < 8:
                if param.name in self.var_to_reg:
                    self.emit(f'mov {self.var_to_reg[param.name]}, {param_regs[i]}')
                else:
                    offset = self._alloc_stack_var(param.name)
                    self.emit(f'str {param_regs[i]}, [x29, #-{offset}]')

        self.emit('')

        # 记忆化:查找缓存
        if need_memo:
            self._gen_memo_lookup(fn.params[0].name, epilogue_label)

        # 函数体
        if fn.body:
            for stmt in fn.body.statements:
                self.gen_stmt(stmt)

        # 默认返回值
        if fn.body and fn.body.statements:
            last = fn.body.statements[-1]
            if not isinstance(last, ReturnStmt):
                self.emit('mov x0, #0')

        # Epilogue(统一标签)
        self.emit_raw(f'{epilogue_label}:')
        # 恢复使用的被调用者保存寄存器
        for i, reg in enumerate(used_regs):
            self.emit(f'ldr {reg}, [sp, #{i * 8}]')
        if stack_size > 16:
            self.emit(f'add sp, sp, #{stack_size - 16}')
        self.emit('ldp x29, x30, [sp], #16')
        self.emit('ret')

        self.current_fn = None
        self.current_fn_pure_int = False
        self.variable_regs = {}
        self.var_to_reg = {}
        self.var_to_stack = {}
        self._current_epilogue_label = None
        self._tco_used_regs = []
        self._tco_stack_size = 16

    def _gen_epilogue(self, stack_size):
        """生成函数 epilogue"""
        label = self.new_label("epilogue")
        self.emit_raw(f'{label}:')
        if stack_size > 16:
            self.emit(f'add sp, sp, #{stack_size - 16}')
        self.emit('ldp x29, x30, [sp], #16')
        self.emit('ret')

    def _count_local_vars(self, fn: FnDef) -> int:
        """估算函数中的局部变量数量"""
        count = 0
        if fn.body:
            for stmt in fn.body.statements:
                if isinstance(stmt, (LetStmt, ConstStmt)):
                    count += 1
        return count + 5  # 预留一些临时空间

    def _is_recursive_function(self, fn: FnDef) -> bool:
        """检测函数是否递归"""
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
                if stmt.else_body:
                    for s in stmt.else_body.statements:
                        if check_stmt(s):
                            return True
            elif isinstance(stmt, ExprStmt):
                return check_expr(stmt.expr)
            return False

        if fn.body:
            for stmt in fn.body.statements:
                if check_stmt(stmt):
                    return True
        return False

    def _gen_memo_lookup(self, param_name, epilogue_label):
        """生成记忆化缓存查找代码"""
        memo_label = f"_memo_{self.c_ident(self.current_fn)}"
        end_label = self.new_label("memo_end")

        self.emit(f'// 记忆化:查找缓存')
        self._load_var_to_reg(param_name, 'x9')
        self.emit(f'cmp x9, #0')
        self.emit(f'b.lt {end_label}')
        self._load_big_immediate('x10', 100000)
        self.emit(f'cmp x9, x10')
        self.emit(f'b.ge {end_label}')
        # 检查 valid 数组
        self.emit(f'adrp x10, {memo_label}_valid@PAGE')
        self.emit(f'add x10, x10, {memo_label}_valid@PAGEOFF')
        self.emit(f'ldrb w11, [x10, x9]')
        self.emit(f'cbz w11, {end_label}')
        # 命中缓存,返回
        self.emit(f'adrp x10, {memo_label}_cache@PAGE')
        self.emit(f'add x10, x10, {memo_label}_cache@PAGEOFF')
        self.emit(f'ldr x0, [x10, x9, lsl #3]')
        self.emit(f'b {epilogue_label}')
        self.emit_raw(f'{end_label}:')
        self.emit('')

    # ============================================================
    # 语句生成
    # ============================================================
    def gen_stmt(self, stmt: Stmt):
        """生成语句"""
        if isinstance(stmt, FnDef):
            pass  # 函数已在顶层处理
        elif isinstance(stmt, LetStmt):
            self.gen_let_stmt(stmt)
        elif isinstance(stmt, ConstStmt):
            self.gen_let_stmt(stmt)
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
        elif isinstance(stmt, DestructureLet):
            self.gen_destructure_let(stmt)
        elif isinstance(stmt, MatchStmt):
            self.gen_match_stmt(stmt)
        elif isinstance(stmt, BreakStmt):
            self.emit(f'b {self._current_loop_end}')
        elif isinstance(stmt, ContinueStmt):
            self.emit(f'b {self._current_loop_cond}')
        elif isinstance(stmt, TryStmt):
            self.gen_try_stmt(stmt)
        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self.gen_stmt(s)

    def gen_let_stmt(self, stmt: LetStmt):
        """生成 let/var 声明"""
        if stmt.initializer:
            # 推断变量类型
            if self._expr_is_float(stmt.initializer):
                self.var_types[stmt.name] = 'float'
                self.gen_expr_to_reg(stmt.initializer, 'd0')
                # 存储浮点数到变量(栈或寄存器)
                offset = self._get_var_offset(stmt.name)
                vreg = self._get_var_reg(stmt.name)
                if vreg:
                    self.emit(f'fmov {vreg}, d0')
                elif offset:
                    self.emit(f'str d0, [x29, #-{offset}]')
                else:
                    # 分配栈空间
                    offset = self._alloc_stack_var(stmt.name)
                    self.emit(f'str d0, [x29, #-{offset}]')
            elif self._expr_is_string(stmt.initializer):
                self.var_types[stmt.name] = 'str'
                self.gen_expr_to_reg(stmt.initializer, 'x9')
                self._store_reg_to_var('x9', stmt.name)
                if self._get_var_offset(stmt.name) is None and self._get_var_reg(stmt.name) is None:
                    self._alloc_stack_var(stmt.name)
                    self._store_reg_to_var('x9', stmt.name)
            elif isinstance(stmt.initializer, MapLiteral):
                self.var_types[stmt.name] = 'map'
                self.gen_expr_to_reg(stmt.initializer, 'x9')
                self._store_reg_to_var('x9', stmt.name)
                if self._get_var_offset(stmt.name) is None and self._get_var_reg(stmt.name) is None:
                    self._alloc_stack_var(stmt.name)
                    self._store_reg_to_var('x9', stmt.name)
            elif isinstance(stmt.initializer, ArrayLiteral):
                self.var_types[stmt.name] = 'array'
                self.gen_expr_to_reg(stmt.initializer, 'x9')
                self._store_reg_to_var('x9', stmt.name)
                if self._get_var_offset(stmt.name) is None and self._get_var_reg(stmt.name) is None:
                    self._alloc_stack_var(stmt.name)
                    self._store_reg_to_var('x9', stmt.name)
            else:
                self.var_types[stmt.name] = 'int'
                # 优化:如果初始值是寄存器中的变量,直接 mov
                if isinstance(stmt.initializer, Identifier):
                    src_reg = self._get_var_reg(stmt.initializer.name)
                    if src_reg:
                        # 确保目标变量已分配
                        if self._get_var_offset(stmt.name) is None and self._get_var_reg(stmt.name) is None:
                            self._alloc_stack_var(stmt.name)
                        dst_reg = self._get_var_reg(stmt.name)
                        if dst_reg:
                            self.emit(f'mov {dst_reg}, {src_reg}')
                        else:
                            offset = self._get_var_offset(stmt.name)
                            self.emit(f'str {src_reg}, [x29, #-{offset}]')
                        return
                self.gen_expr_to_reg(stmt.initializer, 'x9')
                self._store_reg_to_var('x9', stmt.name)
                if self._get_var_offset(stmt.name) is None and self._get_var_reg(stmt.name) is None:
                    self._alloc_stack_var(stmt.name)
                    self._store_reg_to_var('x9', stmt.name)
        else:
            self.var_types[stmt.name] = 'int'
            self.emit('mov x9, #0')
            self._store_reg_to_var('x9', stmt.name)
            if self._get_var_offset(stmt.name) is None and self._get_var_reg(stmt.name) is None:
                self._alloc_stack_var(stmt.name)
                self._store_reg_to_var('x9', stmt.name)

    def gen_assign_stmt(self, stmt: AssignStmt):
        """生成赋值语句"""
        if isinstance(stmt.target, TupleLiteral):
            # 元组赋值: a, b = b, a
            # 先求值右侧到临时元组,再依次取出元素赋值给各目标
            self.gen_expr_to_reg(stmt.value, 'x9')
            self.emit('str x9, [x29, #-128]')   # 保存右侧元组指针
            for i, tgt in enumerate(stmt.target.elements):
                self.emit('ldr x0, [x29, #-128]')
                self.emit(f'mov x1, #{i}')
                self.emit('bl _aurora_array_get')
                self.emit('mov x9, x0')
                if isinstance(tgt, Identifier):
                    self._store_reg_to_var('x9', tgt.name)
                    if (self._get_var_offset(tgt.name) is None
                            and self._get_var_reg(tgt.name) is None):
                        self._alloc_stack_var(tgt.name)
                        self._store_reg_to_var('x9', tgt.name)
            return
        if isinstance(stmt.target, IndexAccess):
            # arr[i] = val 或 map[key] = val
            is_map = False
            if isinstance(stmt.target.object, Identifier):
                is_map = self.var_types.get(stmt.target.object.name) == 'map'
            self.gen_expr_to_reg(stmt.target.object, 'x0')
            self.emit('str x0, [x29, #-120]')
            self.gen_expr_to_reg(stmt.target.index, 'x1')
            self.emit('str x1, [x29, #-112]')
            self.gen_expr_to_reg(stmt.value, 'x2')
            self.emit('ldr x0, [x29, #-120]')
            self.emit('ldr x1, [x29, #-112]')
            if is_map:
                self.emit('bl _aurora_map_set')
            else:
                self.emit('bl _aurora_array_set')
            return
        if isinstance(stmt.target, Identifier):
            var_name = stmt.target.name
            if stmt.op == '=':
                # 优化: var = other_var (直接寄存器 mov)
                if isinstance(stmt.value, Identifier):
                    src_reg = self._get_var_reg(stmt.value.name)
                    dst_reg = self._get_var_reg(var_name)
                    if src_reg and dst_reg:
                        self.emit(f'mov {dst_reg}, {src_reg}')
                        return
                # 优化: var = var + expr 或 var = var - expr
                if (isinstance(stmt.value, BinaryOp) and
                    isinstance(stmt.value.left, Identifier) and
                    stmt.value.left.name == var_name and
                    stmt.value.op in ('+', '-')):
                    vreg = self._get_var_reg(var_name)
                    if vreg:
                        if isinstance(stmt.value.right, IntLiteral):
                            val = int(stmt.value.right.value)
                            if 0 <= val <= 4095:
                                if stmt.value.op == '+':
                                    self.emit(f'add {vreg}, {vreg}, #{val}')
                                else:
                                    self.emit(f'sub {vreg}, {vreg}, #{val}')
                                return
                        self.gen_expr_to_reg(stmt.value.right, 'x10')
                        if stmt.value.op == '+':
                            self.emit(f'add {vreg}, {vreg}, x10')
                        else:
                            self.emit(f'sub {vreg}, {vreg}, x10')
                        return
                # 优化:如果目标在寄存器中,直接生成到目标寄存器
                dst_reg = self._get_var_reg(var_name)
                if dst_reg and not isinstance(stmt.value, (CallExpr,)):
                    # 避免函数调用覆盖参数寄存器
                    self.gen_expr_to_reg(stmt.value, dst_reg)
                    return
                self.gen_expr_to_reg(stmt.value, 'x9')
                self._store_reg_to_var('x9', var_name)
            else:
                # 复合赋值
                self._load_var_to_reg(var_name, 'x9')
                self.gen_expr_to_reg(stmt.value, 'x10')
                op_map = {'+=': 'add', '-=': 'sub', '*=': 'mul', '/=': 'sdiv'}
                if stmt.op in op_map:
                    if stmt.op == '*=':
                        self.emit(f'mul x9, x9, x10')
                    elif stmt.op == '/=':
                        self.emit(f'sdiv x9, x9, x10')
                    else:
                        self.emit(f'{op_map[stmt.op]} x9, x9, x10')
                    self._store_reg_to_var('x9', var_name)

    def gen_if_stmt(self, stmt: IfStmt):
        """生成 if 语句"""
        end_label = self.new_label("if_end")
        else_label = self.new_label("if_else")

        # 条件(优化:比较运算直接分支)
        self._gen_cond_branch(stmt.condition, else_label, True)

        # then 分支
        if stmt.then_body:
            for s in stmt.then_body.statements:
                self.gen_stmt(s)
        self.emit(f'b {end_label}')

        # elif 分支
        for i, (cond, body) in enumerate(stmt.elif_clauses):
            elif_label = self.new_label("elif")
            self.emit_raw(f'{else_label}:')
            self.gen_expr_to_reg(cond, 'x9')
            self.emit('cmp x9, #0')
            next_elif = self.new_label("elif") if i < len(stmt.elif_clauses) - 1 else end_label
            self.emit(f'b.eq {next_elif}')
            if body:
                for s in body.statements:
                    self.gen_stmt(s)
            self.emit(f'b {end_label}')
            else_label = next_elif

        # else 分支
        if stmt.else_body:
            self.emit_raw(f'{else_label}:')
            for s in stmt.else_body.statements:
                self.gen_stmt(s)
        else:
            self.emit_raw(f'{else_label}:')

        self.emit_raw(f'{end_label}:')

    def gen_while_stmt(self, stmt: WhileStmt):
        """生成 while 循环"""
        cond_label = self.new_label("while_cond")
        body_label = self.new_label("while_body")
        end_label = self.new_label("while_end")

        self._current_loop_cond = cond_label
        self._current_loop_end = end_label

        self.emit_raw(f'{cond_label}:')
        self._gen_cond_branch(stmt.condition, end_label, True)
        self.emit_raw(f'{body_label}:')
        if stmt.body:
            for s in stmt.body.statements:
                self.gen_stmt(s)
        self.emit(f'b {cond_label}')

        self.emit_raw(f'{end_label}:')

    def _gen_cond_branch(self, condition, false_label, jump_if_false=True):
        """生成条件分支:如果条件为假则跳转到 false_label
        对比较运算直接生成 cmp+b.cond,消除 cset 冗余"""
        if isinstance(condition, BinaryOp) and condition.op in ('==', '!=', '<', '<=', '>', '>='):
            # 直接比较,跳过 cset
            self.gen_expr_to_reg(condition.left, 'x9')
            # 右操作数可能覆盖 x9,需要保存
            if not self._is_simple_leaf(condition.right):
                temp_offset = 8 + self._temp_depth * 8
                self._temp_depth += 1
                self.emit(f'str x9, [x29, #-{temp_offset}]')
                self.gen_expr_to_reg(condition.right, 'x10')
                self._temp_depth -= 1
                self.emit(f'ldr x9, [x29, #-{temp_offset}]')
            else:
                self.gen_expr_to_reg(condition.right, 'x10')
            self.emit('cmp x9, x10')
            invert_map = {
                '==': 'ne', '!=': 'eq',
                '<': 'ge', '<=': 'gt',
                '>': 'le', '>=': 'lt'
            }
            if jump_if_false:
                self.emit(f'b.{invert_map[condition.op]} {false_label}')
            else:
                self.emit(f'b.{condition.op} {false_label}')
        else:
            self.gen_expr_to_reg(condition, 'x9')
            self.emit('cmp x9, #0')
            if jump_if_false:
                self.emit(f'b.eq {false_label}')
            else:
                self.emit(f'b.ne {false_label}')

    def gen_for_stmt(self, stmt: ForStmt):
        """生成 for 循环(仅支持 range)"""
        if isinstance(stmt.iterable, CallExpr) and isinstance(stmt.iterable.callee, Identifier):
            if stmt.iterable.callee.name == 'range' and len(stmt.iterable.args) == 1:
                # for i in range(n)
                var_name = stmt.variables[0]

                # 检查循环体是否适合展开(无 break/continue)
                body_stmts = stmt.body.statements if stmt.body else []
                can_unroll = True
                for s in body_stmts:
                    if isinstance(s, (BreakStmt, ContinueStmt)):
                        can_unroll = False
                        break
                    if isinstance(s, (ForStmt, WhileStmt)):
                        can_unroll = False
                        break

                if can_unroll and len(body_stmts) <= 5:
                    self._gen_for_unrolled(stmt, var_name, body_stmts, 4)
                    return

                # 普通 for 循环
                cond_label = self.new_label("for_cond")
                end_label = self.new_label("for_end")

                # 初始化循环变量为 0
                self.emit('mov x9, #0')
                self._store_reg_to_var('x9', var_name)
                if self._get_var_offset(var_name) is None and self._get_var_reg(var_name) is None:
                    self._alloc_stack_var(var_name)
                    self._store_reg_to_var('x9', var_name)

                # 获取上限
                self.gen_expr_to_reg(stmt.iterable.args[0], 'x10')
                limit_name = "_for_limit"
                if not hasattr(self, 'var_to_reg') or limit_name not in self.var_to_reg:
                    used_regs = set(self.var_to_reg.values()) if hasattr(self, 'var_to_reg') else set()
                    for reg in self.ALLOCATABLE_REGS:
                        if reg not in used_regs:
                            if not hasattr(self, 'var_to_reg'):
                                self.var_to_reg = {}
                            self.var_to_reg[limit_name] = reg
                            break
                self._store_reg_to_var('x10', limit_name)
                if self._get_var_offset(limit_name) is None and self._get_var_reg(limit_name) is None:
                    self._alloc_stack_var(limit_name)
                    self._store_reg_to_var('x10', limit_name)

                self._current_loop_cond = cond_label
                self._current_loop_end = end_label

                self.emit_raw(f'{cond_label}:')
                self._load_var_to_reg(var_name, 'x9')
                self._load_var_to_reg(limit_name, 'x10')
                self.emit('cmp x9, x10')
                self.emit(f'b.ge {end_label}')

                if stmt.body:
                    for s in stmt.body.statements:
                        self.gen_stmt(s)

                # 递增
                vreg = self._get_var_reg(var_name)
                if vreg:
                    self.emit(f'add {vreg}, {vreg}, #1')
                else:
                    self._load_var_to_reg(var_name, 'x9')
                    self.emit('add x9, x9, #1')
                    self._store_reg_to_var('x9', var_name)
                self.emit(f'b {cond_label}')

                self.emit_raw(f'{end_label}:')
                return

        # 通用 for 循环:暂不支持复杂迭代
        pass

    def _gen_for_unrolled(self, stmt, var_name, body_stmts, unroll_factor):
        """生成展开的 for 循环"""
        cond_label = self.new_label("for_cond")
        end_label = self.new_label("for_end")
        remainder_label = self.new_label("for_remainder")

        # 初始化循环变量为 0
        self.emit('mov x9, #0')
        self._store_reg_to_var('x9', var_name)
        if self._get_var_offset(var_name) is None and self._get_var_reg(var_name) is None:
            self._alloc_stack_var(var_name)
            self._store_reg_to_var('x9', var_name)

        # 获取上限
        self.gen_expr_to_reg(stmt.iterable.args[0], 'x10')
        limit_name = "_for_limit"
        if not hasattr(self, 'var_to_reg') or limit_name not in self.var_to_reg:
            used_regs = set(self.var_to_reg.values()) if hasattr(self, 'var_to_reg') else set()
            for reg in self.ALLOCATABLE_REGS:
                if reg not in used_regs:
                    if not hasattr(self, 'var_to_reg'):
                        self.var_to_reg = {}
                    self.var_to_reg[limit_name] = reg
                    break
        self._store_reg_to_var('x10', limit_name)
        if self._get_var_offset(limit_name) is None and self._get_var_reg(limit_name) is None:
            self._alloc_stack_var(limit_name)
            self._store_reg_to_var('x10', limit_name)

        self._current_loop_cond = cond_label
        self._current_loop_end = end_label

        # 主循环:每次迭代 unroll_factor 次
        self.emit_raw(f'{cond_label}:')
        self._load_var_to_reg(var_name, 'x9')
        self._load_var_to_reg(limit_name, 'x10')
        # 检查 i + unroll_factor <= limit
        self.emit(f'add x11, x9, #{unroll_factor}')
        self.emit('cmp x11, x10')
        self.emit(f'b.gt {remainder_label}')

        # 展开 unroll_factor 次
        for k in range(unroll_factor):
            if k > 0:
                # 递增循环变量
                vreg = self._get_var_reg(var_name)
                if vreg:
                    self.emit(f'add {vreg}, {vreg}, #1')
                else:
                    self._load_var_to_reg(var_name, 'x9')
                    self.emit('add x9, x9, #1')
                    self._store_reg_to_var('x9', var_name)
            # 生成循环体
            for s in body_stmts:
                self.gen_stmt(s)

        # 最后递增一次
        vreg = self._get_var_reg(var_name)
        if vreg:
            self.emit(f'add {vreg}, {vreg}, #1')
        else:
            self._load_var_to_reg(var_name, 'x9')
            self.emit('add x9, x9, #1')
            self._store_reg_to_var('x9', var_name)
        self.emit(f'b {cond_label}')

        # 剩余循环:一次迭代一次
        self.emit_raw(f'{remainder_label}:')
        self._load_var_to_reg(var_name, 'x9')
        self._load_var_to_reg(limit_name, 'x10')
        self.emit('cmp x9, x10')
        self.emit(f'b.ge {end_label}')
        for s in body_stmts:
            self.gen_stmt(s)
        vreg = self._get_var_reg(var_name)
        if vreg:
            self.emit(f'add {vreg}, {vreg}, #1')
        else:
            self._load_var_to_reg(var_name, 'x9')
            self.emit('add x9, x9, #1')
            self._store_reg_to_var('x9', var_name)
        self.emit(f'b {remainder_label}')

        self.emit_raw(f'{end_label}:')

    def gen_try_stmt(self, stmt: TryStmt):
        """生成 try-catch 语句"""
        catch_label = self.new_label("catch")
        end_label = self.new_label("try_end")

        # 保存 jmpbuf: sp 和 catch 入口地址
        self.emit('// try: 保存跳转点')
        self.emit('adrp x0, _aurora_jmpbuf_sp@PAGE')
        self.emit('add x0, x0, _aurora_jmpbuf_sp@PAGEOFF')
        self.emit('mov x1, sp')
        self.emit('str x1, [x0]')
        self.emit('adrp x0, _aurora_jmpbuf_pc@PAGE')
        self.emit('add x0, x0, _aurora_jmpbuf_pc@PAGEOFF')
        self.emit(f'adr x1, {catch_label}')
        self.emit('str x1, [x0]')

        # try 块
        if stmt.body:
            for s in stmt.body.statements:
                self.gen_stmt(s)

        # 正常结束: 清除 jmpbuf,跳过 catch
        self.emit('// try 正常结束')
        self.emit('adrp x0, _aurora_jmpbuf_sp@PAGE')
        self.emit('add x0, x0, _aurora_jmpbuf_sp@PAGEOFF')
        self.emit('str xzr, [x0]')
        self.emit(f'b {end_label}')

        # catch 块
        self.emit_raw(f'{catch_label}:')
        self.emit('// catch: 清除 jmpbuf')
        self.emit('adrp x0, _aurora_jmpbuf_sp@PAGE')
        self.emit('add x0, x0, _aurora_jmpbuf_sp@PAGEOFF')
        self.emit('str xzr, [x0]')

        # 加载异常值到 catch 变量
        if stmt.catches and stmt.catches[0].name:
            catch_var = stmt.catches[0].name
            self.var_types[catch_var] = 'int'
            self.emit('adrp x0, _aurora_exception@PAGE')
            self.emit('add x0, x0, _aurora_exception@PAGEOFF')
            self.emit('ldr x9, [x0]')
            # 分配 catch 变量
            if self._get_var_offset(catch_var) is None and self._get_var_reg(catch_var) is None:
                self._alloc_stack_var(catch_var)
            self._store_reg_to_var('x9', catch_var)
            # 清除异常
            self.emit('adrp x0, _aurora_exception@PAGE')
            self.emit('add x0, x0, _aurora_exception@PAGEOFF')
            self.emit('str xzr, [x0]')

        # catch 体
        if stmt.catches and stmt.catches[0].body:
            for s in stmt.catches[0].body.statements:
                self.gen_stmt(s)

        self.emit_raw(f'{end_label}:')

    def gen_return_stmt(self, stmt: ReturnStmt):
        """生成 return 语句"""
        # ---- 尾调用优化 (TCO): return f(args...) ----
        # 若识别为尾调用,直接把实参载入 x0-x7 并 b 到目标函数(复用当前栈帧),
        # 由本方法内部完成,不再走下面的统一 epilogue。
        if self._try_gen_tail_call(stmt):
            return
        if stmt.value:
            # 记忆化:写入缓存
            if self.current_fn in self._memoized_funcs:
                self.gen_expr_to_reg(stmt.value, 'x9')
                # 保存返回值到临时槽位
                self.emit(f'str x9, [x29, #-120]')  # 使用临时槽位
                # 写入缓存(第一个参数)
                fn_def = self.functions.get(self.current_fn)
                param_name = fn_def.params[0].name if fn_def and fn_def.params else None
                memo_label = f"_memo_{self.c_ident(self.current_fn)}"
                if param_name:
                    self._load_var_to_reg(param_name, 'x10')
                else:
                    self.emit('mov x10, #0')
                self.emit(f'cmp x10, #0')
                skip_label = self.new_label("memo_skip")
                self.emit(f'b.lt {skip_label}')
                self._load_big_immediate('x11', 100000)
                self.emit(f'cmp x10, x11')
                self.emit(f'b.ge {skip_label}')
                self.emit(f'adrp x11, {memo_label}_cache@PAGE')
                self.emit(f'add x11, x11, {memo_label}_cache@PAGEOFF')
                self.emit(f'str x9, [x11, x10, lsl #3]')
                self.emit(f'adrp x11, {memo_label}_valid@PAGE')
                self.emit(f'add x11, x11, {memo_label}_valid@PAGEOFF')
                self.emit(f'mov w12, #1')
                self.emit(f'strb w12, [x11, x10]')
                self.emit_raw(f'{skip_label}:')
                self.emit(f'ldr x0, [x29, #-120]')
            else:
                self.gen_expr_to_reg(stmt.value, 'x0')
        else:
            self.emit('mov x0, #0')

        # 跳转到统一的 epilogue
        if hasattr(self, '_current_epilogue_label') and self._current_epilogue_label:
            self.emit(f'b {self._current_epilogue_label}')
        else:
            self._gen_inline_epilogue()

    def _gen_inline_epilogue(self):
        """生成内联的函数返回(用于 return 语句)"""
        self.emit('mov sp, x29')
        self.emit('ldp x29, x30, [sp], #16')
        self.emit('ret')

    # ---------- Pass 3: 尾调用优化 (TCO) ----------
    # 触发条件(全部满足才启用,保守):
    #   1. return 值是直接函数调用 callee(args...),callee 是 Identifier;
    #   2. 目标是已知用户函数(在 self.functions 中),非内置/宏;
    #   3. 目标函数参数个数 <= 当前函数参数个数(多余寄存器值保持,目标忽略);
    #   4. 实参个数 <= 8 (ARM64 整数参数寄存器 x0-x7);
    #   5. 实参全部是"安全"表达式(无嵌套调用/索引读/容器构造) —— 否则求值实参
    #      会通过 bl 破坏已载入 x0-x7 的实参;
    #   6. 当前函数未启用记忆化(记忆化有缓存读写副作用,不能跳过)。
    # 实现:实参载入 x0-x7 → 与本函数 epilogue 对称地恢复 callee-saved 寄存器并
    # 释放当前栈帧 → `b target`。目标函数的 ret 直接返回给本函数的调用者,
    # 尾递归 thus 占用 O(1) 栈。
    def _try_gen_tail_call(self, stmt: ReturnStmt):
        """识别尾调用 return f(args...),成功则生成跳转代码并返回 True。"""
        if not stmt.value:
            return False
        call = stmt.value
        if not isinstance(call, CallExpr) or not isinstance(call.callee, Identifier):
            return False
        target = call.callee.name
        # 宏调用 name!(...) 不做尾调用
        if target.endswith('!'):
            return False
        # 内置函数不做尾调用
        if target in ('println', 'print', 'len', 'push', 'append',
                      'float', 'int', 'throw', 'panic'):
            return False
        target_fn = self.functions.get(target)
        cur_fn = self.functions.get(self.current_fn)
        if target_fn is None or cur_fn is None:
            return False
        # 目标参数个数不能多于当前函数(多余的实参寄存器无对应位置可放)
        if len(target_fn.params) > len(cur_fn.params):
            return False
        if len(call.args) > 8:
            return False
        # 实参安全性:不允许嵌套调用等破坏 x0-x7 的表达式
        for arg in call.args:
            if not self._expr_tco_safe(arg):
                return False
        # 记忆化函数有缓存写回副作用,不做尾调用
        if self.current_fn in self._memoized_funcs:
            return False

        self.emit(f'// 尾调用优化: return {target}(...) -> b {self.c_ident(target)}')
        param_regs = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7']
        for i, arg in enumerate(call.args):
            self.gen_expr_to_reg(arg, param_regs[i])
        # 与 gen_function epilogue 对称地释放当前栈帧(不 ret,留给 b 目标)
        self._emit_tco_frame_epilogue()
        self.emit(f'b {self.c_ident(target)}')
        return True

    def _expr_tco_safe(self, expr):
        """TCO 实参安全性检查:只允许字面量/标识符/纯算术,
        禁止 CallExpr/IndexAccess/容器构造等会通过 bl 破坏 x0-x7 的表达式。"""
        if isinstance(expr, (IntLiteral, FloatLiteral, StringLiteral,
                             BoolLiteral, NilLiteral, Identifier)):
            return True
        if isinstance(expr, BinaryOp):
            return self._expr_tco_safe(expr.left) and self._expr_tco_safe(expr.right)
        if isinstance(expr, UnaryOp):
            return self._expr_tco_safe(expr.operand)
        return False

    def _emit_tco_frame_epilogue(self):
        """尾调用用的帧释放:与 gen_function 的 epilogue 对称,但不 ret,而是 b 目标。
        恢复 callee-saved 寄存器、释放栈帧、弹出保存的 FP/LR(x30 仍指向本函数调用者)。"""
        used_regs = getattr(self, '_tco_used_regs', None) or []
        stack_size = getattr(self, '_tco_stack_size', 16)
        for i, reg in enumerate(used_regs):
            self.emit(f'ldr {reg}, [sp, #{i * 8}]')
        if stack_size > 16:
            self.emit(f'add sp, sp, #{stack_size - 16}')
        self.emit('ldp x29, x30, [sp], #16')

    def gen_expr_stmt(self, stmt: ExprStmt):
        """生成表达式语句"""
        if isinstance(stmt.expr, CallExpr):
            self.gen_expr_to_reg(stmt.expr, 'x9')

    # ============================================================
    # 表达式生成(结果放入指定寄存器)
    # ============================================================
    def _is_simple_leaf(self, expr) -> bool:
        """检测表达式是否是简单叶子节点(不会使用 x9 临时寄存器)"""
        return isinstance(expr, (Identifier, IntLiteral, BoolLiteral, NilLiteral))

    def _expr_is_float(self, expr) -> bool:
        """判断表达式是否为浮点类型"""
        if isinstance(expr, FloatLiteral):
            return True
        if isinstance(expr, BinaryOp):
            if expr.op in ('+', '-', '*', '/', '%'):
                return self._expr_is_float(expr.left) or self._expr_is_float(expr.right)
            return False
        if isinstance(expr, UnaryOp):
            return self._expr_is_float(expr.operand)
        if isinstance(expr, Identifier):
            return self.var_types.get(expr.name) == 'float'
        if isinstance(expr, CallExpr):
            # 简单假设: 函数返回类型从函数名推断
            if isinstance(expr.callee, Identifier):
                name = expr.callee.name
                if name in ('sqrt', 'sin', 'cos', 'tan', 'exp', 'log', 'pow', 'float'):
                    return True
            return False
        return False

    def _expr_is_string(self, expr) -> bool:
        """判断表达式是否为字符串类型"""
        if isinstance(expr, StringLiteral):
            return True
        if isinstance(expr, BinaryOp) and expr.op == '+':
            return self._expr_is_string(expr.left) or self._expr_is_string(expr.right)
        if isinstance(expr, Identifier):
            return self.var_types.get(expr.name) == 'str'
        return False

    def gen_expr_to_reg(self, expr: Expr, reg: str):
        """生成表达式,结果放入 reg (整数用x寄存器,浮点用d寄存器)"""
        # 编译期常量计算
        if isinstance(expr, CallExpr):
            const_val = self._try_compile_time_eval(expr)
            if const_val is not None:
                self._load_big_immediate(reg, const_val)
                return

        if isinstance(expr, IntLiteral):
            val = int(expr.value)
            if abs(val) <= 65535:
                self.emit(f'mov {reg}, #{val}')
            else:
                self._load_big_immediate(reg, val)
        elif isinstance(expr, FloatLiteral):
            # 浮点数加载到 d0 (调用者约定)
            self._gen_float_literal(expr.value, 'd0')
            if reg != 'd0':
                self.emit(f'fmov {reg}, d0')
        elif isinstance(expr, StringLiteral):
            # 字符串字面量: 返回数据段中的指针
            label = self.get_string_label(expr.value)
            self.emit(f'adrp {reg}, {label}@PAGE')
            self.emit(f'add {reg}, {reg}, {label}@PAGEOFF')
        elif isinstance(expr, ArrayLiteral):
            # 创建数组: 先分配,再逐个填充
            n = len(expr.elements)
            self.emit(f'mov x0, #{max(n, 1)}')
            self.emit('bl _aurora_array_new')
            self.emit('str x0, [x29, #-128]')  # 保存数组指针到栈
            for i, elem in enumerate(expr.elements):
                self.gen_expr_to_reg(elem, 'x2')  # x2 = 值
                self.emit('str x2, [x29, #-120]')
                self.emit('ldr x0, [x29, #-128]')  # x0 = 数组
                self.emit(f'mov x1, #{i}')        # x1 = 索引
                self.emit('bl _aurora_array_set')
                # 更新 length
                self.emit(f'mov x8, #{i + 1}')
                self.emit('ldr x9, [x29, #-128]')
                self.emit(f'str x8, [x9, #8]')
            self.emit(f'ldr {reg}, [x29, #-128]')
        elif isinstance(expr, MapLiteral):
            # 创建 Map: {key1: val1, key2: val2, ...}
            n = len(expr.entries)
            self.emit(f'mov x0, #{max(n * 2, 16)}')  # 容量 = 2*entries
            self.emit('bl _aurora_map_new')
            self.emit('str x0, [x29, #-128]')  # 保存 map 指针到栈
            for key, val in expr.entries:
                self.gen_expr_to_reg(val, 'x2')  # x2 = value
                self.emit('str x2, [x29, #-120]')
                self.gen_expr_to_reg(key, 'x1')  # x1 = key
                self.emit('ldr x2, [x29, #-120]')
                self.emit('ldr x0, [x29, #-128]')
                self.emit('bl _aurora_map_set')
            self.emit(f'ldr {reg}, [x29, #-128]')
        elif isinstance(expr, IndexAccess):
            # arr[i] 或 map[key]
            is_map = False
            if isinstance(expr.object, Identifier):
                is_map = self.var_types.get(expr.object.name) == 'map'
            self.gen_expr_to_reg(expr.object, 'x0')
            self.emit('str x0, [x29, #-120]')
            self.gen_expr_to_reg(expr.index, 'x1')
            self.emit('ldr x0, [x29, #-120]')
            if is_map:
                self.emit('bl _aurora_map_get')
            else:
                self.emit('bl _aurora_array_get')
            self.emit(f'mov {reg}, x0')
        elif isinstance(expr, BoolLiteral):
            self.emit(f'mov {reg}, #{1 if expr.value else 0}')
        elif isinstance(expr, NilLiteral):
            self.emit(f'mov {reg}, #0')
        elif isinstance(expr, Identifier):
            vtype = self.var_types.get(expr.name, 'int')
            if vtype == 'float':
                # 浮点数变量存在栈上(8字节),加载到 d0
                offset = self._get_var_offset(expr.name)
                vreg = self._get_var_reg(expr.name)
                if vreg:
                    self.emit(f'fmov d0, {vreg}')
                elif offset:
                    self.emit(f'ldr d0, [x29, #-{offset}]')
                else:
                    self.emit(f'fmov d0, #0.0')
                if reg != 'd0':
                    self.emit(f'fmov {reg}, d0')
            else:
                self._load_var_to_reg(expr.name, reg)
        elif isinstance(expr, BinaryOp):
            self.gen_binary_op(expr, reg)
        elif isinstance(expr, UnaryOp):
            self.gen_unary_op(expr, reg)
        elif isinstance(expr, CallExpr):
            self.gen_call_expr(expr, reg)
        elif isinstance(expr, IfExpr):
            self.gen_if_expr(expr, reg)
        elif isinstance(expr, TupleLiteral):
            self.gen_tuple_literal(expr, reg)
        elif isinstance(expr, TupleIndex):
            self.gen_tuple_index(expr, reg)
        elif isinstance(expr, ForcedUnwrap):
            self.gen_forced_unwrap(expr, reg)
        elif isinstance(expr, NullCoalesce):
            self.gen_null_coalesce(expr, reg)
        elif isinstance(expr, OptionalAccess):
            self.gen_optional_access(expr, reg)
        elif isinstance(expr, PipeExpr):
            self.gen_pipe_expr(expr, reg)
        elif isinstance(expr, ListComp):
            self.gen_list_comp(expr, reg)
        elif isinstance(expr, SetComp):
            self.gen_set_comp(expr, reg)
        elif isinstance(expr, MapComp):
            self.gen_map_comp(expr, reg)
        elif isinstance(expr, StructLiteral):
            self.gen_struct_literal(expr, reg)
        elif isinstance(expr, MatchExpr):
            self.gen_match_expr(expr, reg)
        elif isinstance(expr, LambdaExpr):
            # 降级:后端不支持闭包,返回 0(不崩溃)
            self.emit(f'mov {reg}, #0')
        else:
            self.emit(f'mov {reg}, #0')

    def _gen_float_literal(self, value, dreg):
        """生成浮点字面量加载"""
        val = float(value)
        # 尝试用 fmov 直接加载(仅支持特定常量)
        # 通用方法: 存入数据段,然后 ldr
        label = f'_float_const_{self.string_counter}'
        self.string_counter += 1
        self.data_section.append(f'.align 3')
        self.data_section.append(f'{label}: .double {val}')
        self.emit(f'adrp x9, {label}@PAGE')
        self.emit(f'add x9, x9, {label}@PAGEOFF')
        self.emit(f'ldr {dreg}, [x9]')

    def _load_big_immediate(self, reg, val):
        """加载大立即数到寄存器"""
        if val < 0:
            # 负数:先加载绝对值,然后取反
            abs_val = -val
            self._load_big_immediate(reg, abs_val)
            self.emit(f'neg {reg}, {reg}')
            return
        # 使用 movz + movk
        parts = []
        v = val
        for shift in [0, 16, 32, 48]:
            part = (v >> shift) & 0xFFFF
            if part or shift == 0:
                parts.append((part, shift))
        for i, (part, shift) in enumerate(parts):
            if i == 0:
                self.emit(f'movz {reg}, #{part}, lsl #{shift}')
            else:
                self.emit(f'movk {reg}, #{part}, lsl #{shift}')

    def gen_binary_op(self, expr: BinaryOp, reg: str):
        """生成二元运算"""
        op = expr.op
        is_float = self._expr_is_float(expr)
        is_string = self._expr_is_string(expr)

        # 字符串拼接
        if is_string and op == '+':
            self.gen_expr_to_reg(expr.left, 'x0')
            self.emit('str x0, [x29, #-120]')  # 临时保存
            self.gen_expr_to_reg(expr.right, 'x1')
            self.emit('ldr x0, [x29, #-120]')
            self.emit('bl _aurora_str_concat')
            self.emit(f'mov {reg}, x0')
            return

        # 浮点比较运算
        if is_float and op in ('==', '!=', '<', '<=', '>', '>='):
            self.gen_expr_to_reg(expr.left, 'd0')
            self.emit('str d0, [x29, #-120]')
            self.gen_expr_to_reg(expr.right, 'd1')
            self.emit('ldr d0, [x29, #-120]')
            self.emit('fcmp d0, d1')
            cond_map = {
                '==': 'eq', '!=': 'ne',
                '<': 'mi', '<=': 'ls',
                '>': 'gt', '>=': 'ge'
            }
            self.emit(f'cset {reg}, {cond_map[op]}')
            return

        # 比较运算(整数)
        if op in ('==', '!=', '<', '<=', '>', '>=') and not is_float:
            self.gen_expr_to_reg(expr.left, 'x9')
            self.gen_expr_to_reg(expr.right, 'x10')
            self.emit('cmp x9, x10')
            cond_map = {
                '==': 'eq', '!=': 'ne',
                '<': 'lt', '<=': 'le',
                '>': 'gt', '>=': 'ge'
            }
            self.emit(f'cset {reg}, {cond_map[op]}')
            return

        # 逻辑运算
        if op == '&&':
            self.gen_expr_to_reg(expr.left, 'x9')
            self.emit('cmp x9, #0')
            false_label = self.new_label("and_false")
            end_label = self.new_label("and_end")
            self.emit(f'b.eq {false_label}')
            self.gen_expr_to_reg(expr.right, 'x9')
            self.emit('cmp x9, #0')
            self.emit(f'b.eq {false_label}')
            self.emit(f'mov {reg}, #1')
            self.emit(f'b {end_label}')
            self.emit_raw(f'{false_label}:')
            self.emit(f'mov {reg}, #0')
            self.emit_raw(f'{end_label}:')
            return

        if op == '||':
            self.gen_expr_to_reg(expr.left, 'x9')
            self.emit('cmp x9, #0')
            true_label = self.new_label("or_true")
            end_label = self.new_label("or_end")
            self.emit(f'b.ne {true_label}')
            self.gen_expr_to_reg(expr.right, 'x9')
            self.emit('cmp x9, #0')
            self.emit(f'b.ne {true_label}')
            self.emit(f'mov {reg}, #0')
            self.emit(f'b {end_label}')
            self.emit_raw(f'{true_label}:')
            self.emit(f'mov {reg}, #1')
            self.emit_raw(f'{end_label}:')
            return

        # 浮点算术运算
        if is_float:
            self.gen_expr_to_reg(expr.left, 'd0')
            self.emit('str d0, [x29, #-120]')
            self.gen_expr_to_reg(expr.right, 'd1')
            self.emit('ldr d0, [x29, #-120]')
            if op == '+':
                self.emit(f'fadd d0, d0, d1')
            elif op == '-':
                self.emit(f'fsub d0, d0, d1')
            elif op == '*':
                self.emit(f'fmul d0, d0, d1')
            elif op == '/':
                self.emit(f'fdiv d0, d0, d1')
            if reg != 'd0':
                self.emit(f'fmov {reg}, d0')
            return

        # 整数算术运算
        # 优化:如果左操作数是变量且在寄存器中,直接用该寄存器
        left_reg = 'x9'
        left_is_reg_var = False
        if isinstance(expr.left, Identifier):
            vreg = self._get_var_reg(expr.left.name)
            if vreg:
                left_reg = vreg
                left_is_reg_var = True

        # 优化:如果右操作数是变量且在寄存器中,直接用该寄存器
        right_reg = 'x10'
        right_is_reg_var = False
        if isinstance(expr.right, Identifier):
            vreg = self._get_var_reg(expr.right.name)
            if vreg:
                right_reg = vreg
                right_is_reg_var = True

        # 强度削减和常量加法提前判断
        if op == '*' and isinstance(expr.right, IntLiteral):
            val = int(expr.right.value)
            if val > 0 and (val & (val - 1)) == 0:
                shift = val.bit_length() - 1
                if not left_is_reg_var:
                    self.gen_expr_to_reg(expr.left, 'x9')
                self.emit(f'lsl {reg}, {left_reg}, #{shift}')
                return
        if op == '/' and isinstance(expr.right, IntLiteral):
            val = int(expr.right.value)
            if val > 0 and (val & (val - 1)) == 0:
                shift = val.bit_length() - 1
                if not left_is_reg_var:
                    self.gen_expr_to_reg(expr.left, 'x9')
                self.emit(f'asr {reg}, {left_reg}, #{shift}')
                return
        if op in ('+', '-') and isinstance(expr.right, IntLiteral):
            val = int(expr.right.value)
            if 0 <= val <= 4095:
                if not left_is_reg_var:
                    self.gen_expr_to_reg(expr.left, 'x9')
                if op == '+':
                    self.emit(f'add {reg}, {left_reg}, #{val}')
                else:
                    self.emit(f'sub {reg}, {left_reg}, #{val}')
                return

        if not left_is_reg_var:
            self.gen_expr_to_reg(expr.left, 'x9')

        if not right_is_reg_var:
            if not self._is_simple_leaf(expr.right):
                if left_is_reg_var:
                    self.gen_expr_to_reg(expr.right, 'x10')
                else:
                    temp_offset = 8 + self._temp_depth * 8
                    self._temp_depth += 1
                    self.emit(f'str x9, [x29, #-{temp_offset}]')
                    self.gen_expr_to_reg(expr.right, 'x10')
                    self._temp_depth -= 1
                    self.emit(f'ldr x9, [x29, #-{temp_offset}]')
            else:
                self.gen_expr_to_reg(expr.right, 'x10')

        if op == '+':
            self.emit(f'add {reg}, {left_reg}, {right_reg}')
        elif op == '-':
            self.emit(f'sub {reg}, {left_reg}, {right_reg}')
        elif op == '*':
            self.emit(f'mul {reg}, {left_reg}, {right_reg}')
        elif op == '/':
            self.emit(f'sdiv {reg}, {left_reg}, {right_reg}')
        elif op == '%':
            self.emit(f'sdiv x11, {left_reg}, {right_reg}')
            self.emit(f'msub {reg}, x11, {right_reg}, {left_reg}')
        elif op == '**':
            self.emit(f'mov x0, {left_reg}')
            self.emit(f'mov x1, {right_reg}')
            self.emit('bl _aurora_pow_int')
            self.emit(f'mov {reg}, x0')

    def gen_unary_op(self, expr: UnaryOp, reg: str):
        """生成一元运算"""
        if self._expr_is_float(expr.operand):
            self.gen_expr_to_reg(expr.operand, 'd0')
            if expr.op == '-':
                self.emit(f'fneg d0, d0')
                if reg != 'd0':
                    self.emit(f'fmov {reg}, d0')
            else:
                if reg != 'd0':
                    self.emit(f'fmov {reg}, d0')
            return
        self.gen_expr_to_reg(expr.operand, 'x9')
        if expr.op == '-':
            self.emit(f'neg {reg}, x9')
        elif expr.op == '!':
            self.emit('cmp x9, #0')
            self.emit(f'cset {reg}, eq')
        else:
            self.emit(f'mov {reg}, x9')

    def gen_call_expr(self, expr: CallExpr, reg: str):
        """生成函数调用"""
        if not isinstance(expr.callee, Identifier):
            self.emit(f'mov {reg}, #0')
            return

        func_name = expr.callee.name

        # 内置函数
        if func_name == 'println':
            self._gen_println(expr.args, reg)
            return
        elif func_name == 'print':
            self._gen_print(expr.args, reg)
            return
        elif func_name == 'len':
            # len(arr) 或 len(str) 或 len(map)
            if expr.args:
                arg = expr.args[0]
                is_map = isinstance(arg, Identifier) and self.var_types.get(arg.name) == 'map'
                if is_map:
                    self.gen_expr_to_reg(arg, 'x0')
                    self.emit('bl _aurora_map_len')
                elif self._expr_is_string(arg):
                    self.gen_expr_to_reg(arg, 'x0')
                    self.emit('bl _aurora_strlen')
                else:
                    self.gen_expr_to_reg(arg, 'x0')
                    self.emit('bl _aurora_array_len')
                self.emit(f'mov {reg}, x0')
            return
        elif func_name == 'push' or func_name == 'append':
            # push(arr, val) 或 arr.push(val) - 简化为 push(arr, val)
            if len(expr.args) >= 2:
                self.gen_expr_to_reg(expr.args[0], 'x0')
                self.emit('str x0, [x29, #-120]')
                self.gen_expr_to_reg(expr.args[1], 'x1')
                self.emit('ldr x0, [x29, #-120]')
                self.emit('bl _aurora_array_push')
            self.emit(f'mov {reg}, #0')
            return
        elif func_name == 'float':
            # int -> float 转换
            if expr.args:
                self.gen_expr_to_reg(expr.args[0], 'x9')
                self.emit('scvtf d0, x9')
                if reg != 'd0':
                    self.emit(f'fmov {reg}, d0')
            return
        elif func_name == 'int':
            # float -> int 转换
            if expr.args:
                self.gen_expr_to_reg(expr.args[0], 'd0')
                self.emit('fcvtzs x0, d0')
                self.emit(f'mov {reg}, x0')
            return
        elif func_name == 'throw' or func_name == 'panic':
            # throw(value) / panic(value) - 抛出异常
            if expr.args:
                self.gen_expr_to_reg(expr.args[0], 'x0')
            else:
                self.emit('mov x0, #1')
            self.emit('bl _aurora_throw')
            self.emit(f'mov {reg}, #0')
            return
        elif func_name.endswith('!'):
            # 宏调用: name!(args) - 编译期展开
            self._gen_macro_call(func_name, expr.args, reg)
            return

        # 保存调用者保存寄存器(x9-x15)
        # 简化:假设参数不超过8个,且不需要保存太多

        # 调用函数
        if func_name in self.functions:
            fn_def = self.functions[func_name]
            # 尝试内联:非递归、小函数、参数<=4
            if self._can_inline(fn_def, expr.args):
                self._gen_inlined_call(fn_def, expr.args, reg)
                return
            # 加载参数到 x0-x7
            param_regs = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7']
            for i, arg in enumerate(expr.args[:8]):
                self.gen_expr_to_reg(arg, param_regs[i])
            self.emit(f'bl {self.c_ident(func_name)}')
        else:
            # 未知函数,返回 0
            self.emit(f'mov x0, #0')

        self.emit(f'mov {reg}, x0')

    def _can_inline(self, fn_def, args) -> bool:
        """判断函数是否可以内联"""
        # 不内联递归函数
        if self._is_recursive_function(fn_def):
            return False
        # 参数不超过 4 个
        if len(fn_def.params) > 4:
            return False
        # 函数体语句数不超过 10
        if not fn_def.body:
            return True
        count = len(fn_def.body.statements)
        if count > 10:
            return False
        # 不内联包含循环的函数(循环内联会导致代码膨胀和性能下降)
        for stmt in fn_def.body.statements:
            if isinstance(stmt, (ForStmt, WhileStmt)):
                return False
        return True

    def _gen_inlined_call(self, fn_def, args, reg):
        """生成内联函数调用"""
        # 保存当前变量映射
        old_var_types = dict(self.var_types)
        old_var_to_reg = dict(self.var_to_reg) if hasattr(self, 'var_to_reg') else {}
        old_var_to_stack = dict(self.var_to_stack) if hasattr(self, 'var_to_stack') else {}

        inline_id = self.new_label("inline")
        end_label = f"{inline_id}_end"

        # 为参数分配临时栈槽位并存储实参
        param_offsets = {}
        base_offset = 64  # 临时区域起始
        for i, param in enumerate(fn_def.params):
            offset = base_offset + i * 8
            param_offsets[param.name] = offset
            if i < len(args):
                self.gen_expr_to_reg(args[i], 'x9')
                self.emit(f'str x9, [x29, #-{offset}]')
            else:
                self.emit(f'str xzr, [x29, #-{offset}]')

        # 临时覆盖变量访问:参数直接用栈槽位
        original_get_var_offset = self._get_var_offset
        original_load_var = self._load_var_to_reg
        original_store_var = self._store_reg_to_var

        # 保存返回值的位置
        self._inline_return_reg = reg
        self._inline_end_label = end_label

        # 生成函数体(return 会跳转到 end_label)
        if fn_def.body:
            for stmt in fn_def.body.statements:
                self._gen_inlined_stmt(stmt, param_offsets, end_label)

        self.emit_raw(f'{end_label}:')

        # 恢复
        self.var_types = old_var_types
        if hasattr(self, 'var_to_reg'):
            self.var_to_reg = old_var_to_reg
        if hasattr(self, 'var_to_stack'):
            self.var_to_stack = old_var_to_stack

    def _gen_inlined_stmt(self, stmt, param_offsets, end_label):
        """生成内联函数体语句(参数用栈槽位,return 跳转)"""
        if isinstance(stmt, ReturnStmt):
            if stmt.value:
                self._gen_inlined_expr(stmt.value, param_offsets, self._inline_return_reg)
            else:
                self.emit(f'mov {self._inline_return_reg}, #0')
            self.emit(f'b {end_label}')
        elif isinstance(stmt, LetStmt):
            if stmt.initializer:
                self._gen_inlined_expr(stmt.initializer, param_offsets, 'x9')
            else:
                self.emit('mov x9, #0')
            # 内联函数的局部变量用临时栈槽位
            offset = param_offsets.get(stmt.name)
            if offset is None:
                # 分配新的临时槽位
                offset = 64 + len(param_offsets) * 8
                param_offsets[stmt.name] = offset
            self.emit(f'str x9, [x29, #-{offset}]')
        elif isinstance(stmt, AssignStmt):
            if isinstance(stmt.target, Identifier):
                self._gen_inlined_expr(stmt.value, param_offsets, 'x9')
                offset = param_offsets.get(stmt.target.name)
                if offset:
                    self.emit(f'str x9, [x29, #-{offset}]')
        elif isinstance(stmt, IfStmt):
            self._gen_inlined_if(stmt, param_offsets, end_label)
        elif isinstance(stmt, WhileStmt):
            self._gen_inlined_while(stmt, param_offsets, end_label)
        elif isinstance(stmt, ExprStmt):
            self._gen_inlined_expr(stmt.expr, param_offsets, 'x9')
        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self._gen_inlined_stmt(s, param_offsets, end_label)

    def _gen_inlined_if(self, stmt, param_offsets, end_label):
        """生成内联 if 语句"""
        end_label_if = self.new_label("inline_if_end")
        else_label = self.new_label("inline_if_else")
        self._gen_inlined_expr(stmt.condition, param_offsets, 'x9')
        self.emit('cmp x9, #0')
        self.emit(f'b.eq {else_label}')
        if stmt.then_body:
            for s in stmt.then_body.statements:
                self._gen_inlined_stmt(s, param_offsets, end_label)
        self.emit(f'b {end_label_if}')
        self.emit_raw(f'{else_label}:')
        if stmt.else_body:
            for s in stmt.else_body.statements:
                self._gen_inlined_stmt(s, param_offsets, end_label)
        self.emit_raw(f'{end_label_if}:')

    def _gen_inlined_while(self, stmt, param_offsets, end_label):
        """生成内联 while 循环"""
        cond_label = self.new_label("inline_while_cond")
        end_label_while = self.new_label("inline_while_end")
        self.emit_raw(f'{cond_label}:')
        self._gen_inlined_expr(stmt.condition, param_offsets, 'x9')
        self.emit('cmp x9, #0')
        self.emit(f'b.eq {end_label_while}')
        if stmt.body:
            for s in stmt.body.statements:
                self._gen_inlined_stmt(s, param_offsets, end_label)
        self.emit(f'b {cond_label}')
        self.emit_raw(f'{end_label_while}:')

    def _gen_inlined_expr(self, expr, param_offsets, reg):
        """生成内联表达式(参数从栈槽位加载)"""
        if isinstance(expr, Identifier):
            offset = param_offsets.get(expr.name)
            if offset:
                self.emit(f'ldr {reg}, [x29, #-{offset}]')
                return
        if isinstance(expr, IntLiteral):
            val = int(expr.value)
            if abs(val) <= 65535:
                self.emit(f'mov {reg}, #{val}')
            else:
                self._load_big_immediate(reg, val)
            return
        if isinstance(expr, BinaryOp):
            # 左操作数
            self._gen_inlined_expr(expr.left, param_offsets, 'x9')
            if not self._is_simple_leaf(expr.right):
                self.emit('str x9, [x29, #-8]')
                self._gen_inlined_expr(expr.right, param_offsets, 'x10')
                self.emit('ldr x9, [x29, #-8]')
            else:
                self._gen_inlined_expr(expr.right, param_offsets, 'x10')
            op = expr.op
            if op == '+':
                self.emit(f'add {reg}, x9, x10')
            elif op == '-':
                self.emit(f'sub {reg}, x9, x10')
            elif op == '*':
                self.emit(f'mul {reg}, x9, x10')
            elif op == '/':
                self.emit(f'sdiv {reg}, x9, x10')
            elif op == '%':
                self.emit(f'sdiv x11, x9, x10')
                self.emit(f'msub {reg}, x11, x10, x9')
            elif op in ('==', '!=', '<', '<=', '>', '>='):
                self.emit('cmp x9, x10')
                cond_map = {'==': 'eq', '!=': 'ne', '<': 'lt', '<=': 'le', '>': 'gt', '>=': 'ge'}
                self.emit(f'cset {reg}, {cond_map[op]}')
            return
        if isinstance(expr, CallExpr):
            # 内联函数中的调用:递归调用不内联
            if isinstance(expr.callee, Identifier):
                fname = expr.callee.name
                if fname in self.functions and not self._is_recursive_function(self.functions[fname]):
                    # 递归检查:如果调用的是当前正在内联的函数,不内联
                    # 简化:直接生成普通调用
                    pass
            # 普通调用
            param_regs = ['x0', 'x1', 'x2', 'x3']
            for i, arg in enumerate(expr.args[:4]):
                self._gen_inlined_expr(arg, param_offsets, param_regs[i])
            if isinstance(expr.callee, Identifier) and expr.callee.name in self.functions:
                self.emit(f'bl {self.c_ident(expr.callee.name)}')
            else:
                self.emit('mov x0, #0')
            self.emit(f'mov {reg}, x0')
            return
        # 兜底:用普通表达式生成(但变量访问可能不对)
        self.gen_expr_to_reg(expr, reg)

    def _gen_macro_call(self, macro_name, args, reg):
        """生成宏调用(编译期展开)"""
        if macro_name == 'assert!':
            # assert!(cond): 如果条件为假,panic(1)
            if args:
                self.gen_expr_to_reg(args[0], 'x9')
                self.emit('cmp x9, #0')
                fail_label = self.new_label("assert_fail")
                end_label = self.new_label("assert_end")
                self.emit(f'b.ne {end_label}')
                self.emit_raw(f'{fail_label}:')
                self.emit('mov x0, #1')
                self.emit('bl _aurora_throw')
                self.emit_raw(f'{end_label}:')
            self.emit(f'mov {reg}, #0')
        elif macro_name == 'dbg!':
            # dbg!(expr): 打印表达式值并返回
            if args:
                self.gen_expr_to_reg(args[0], 'x0')
                self.emit('str x0, [x29, #-120]')
                self.emit('bl _aurora_print_int')
                # 打印换行
                nl_label = self.get_string_label("\n")
                self.emit('mov x0, #1')
                self.emit(f'adrp x1, {nl_label}@PAGE')
                self.emit(f'add x1, x1, {nl_label}@PAGEOFF')
                self.emit('mov x2, #1')
                self.emit('mov x16, #4')
                self.emit('svc #0')
                self.emit('ldr x0, [x29, #-120]')
                self.emit(f'mov {reg}, x0')
            else:
                self.emit(f'mov {reg}, #0')
        elif macro_name == 'vec!':
            # vec![a, b, c]: 创建数组
            n = len(args)
            self.emit(f'mov x0, #{max(n, 1)}')
            self.emit('bl _aurora_array_new')
            self.emit('str x0, [x29, #-128]')
            for i, arg in enumerate(args):
                self.gen_expr_to_reg(arg, 'x2')
                self.emit('str x2, [x29, #-120]')
                self.emit('ldr x0, [x29, #-128]')
                self.emit(f'mov x1, #{i}')
                self.emit('bl _aurora_array_set')
                self.emit(f'mov x8, #{i + 1}')
                self.emit('ldr x9, [x29, #-128]')
                self.emit(f'str x8, [x9, #8]')
            self.emit(f'ldr {reg}, [x29, #-128]')
        else:
            # 未知宏,返回 0
            self.emit(f'mov {reg}, #0')

    def _gen_println(self, args, reg):
        """生成 println 调用(支持整数和字符串)"""
        if not args:
            # 空行
            label = self.get_string_label("\n")
            self.emit(f'mov x0, #1')
            self.emit(f'adrp x1, {label}@PAGE')
            self.emit(f'add x1, x1, {label}@PAGEOFF')
            self.emit(f'mov x2, #1')
            self.emit(f'mov x16, #4')
            self.emit(f'svc #0')
            self.emit(f'mov {reg}, #0')
            return

        for i, arg in enumerate(args):
            if isinstance(arg, StringLiteral):
                self._gen_print_string(arg)
            elif isinstance(arg, IntLiteral):
                self._gen_print_int_literal(int(arg.value))
            elif isinstance(arg, FloatLiteral):
                self._gen_float_literal(arg.value, 'd0')
                self.emit('bl _aurora_print_float')
            elif self._expr_is_float(arg):
                self.gen_expr_to_reg(arg, 'd0')
                self.emit('bl _aurora_print_float')
            elif self._expr_is_string(arg):
                # 字符串变量:调用 write 系统调用
                self.gen_expr_to_reg(arg, 'x9')
                self.emit('str x9, [x29, #-120]')
                self.emit('mov x0, x9')
                self.emit('bl _aurora_strlen')
                self.emit('mov x2, x0')
                self.emit('mov x0, #1')
                self.emit('ldr x1, [x29, #-120]')
                self.emit('mov x16, #4')
                self.emit('svc #0')
            else:
                self.gen_expr_to_reg(arg, 'x0')
                self.emit('bl _aurora_print_int')
            if i < len(args) - 1:
                space_label = self.get_string_label(" ")
                self.emit(f'mov x0, #1')
                self.emit(f'adrp x1, {space_label}@PAGE')
                self.emit(f'add x1, x1, {space_label}@PAGEOFF')
                self.emit(f'mov x2, #1')
                self.emit(f'mov x16, #4')
                self.emit(f'svc #0')

        # 换行
        nl_label = self.get_string_label("\n")
        self.emit(f'mov x0, #1')
        self.emit(f'adrp x1, {nl_label}@PAGE')
        self.emit(f'add x1, x1, {nl_label}@PAGEOFF')
        self.emit(f'mov x2, #1')
        self.emit(f'mov x16, #4')
        self.emit(f'svc #0')
        self.emit(f'mov {reg}, #0')

    def _gen_print(self, args, reg):
        """生成 print 调用(不换行)"""
        for arg in args:
            if isinstance(arg, StringLiteral):
                self._gen_print_string(arg)
            elif isinstance(arg, IntLiteral):
                self._gen_print_int_literal(int(arg.value))
            else:
                self.gen_expr_to_reg(arg, 'x0')
                self.emit('bl _aurora_print_int')
        self.emit(f'mov {reg}, #0')

    def _gen_print_string(self, string_expr):
        """打印字符串(处理插值)"""
        s = string_expr.value
        if '{' not in s:
            # 纯字符串
            label = self.get_string_label(s)
            self.emit(f'mov x0, #1')
            self.emit(f'adrp x1, {label}@PAGE')
            self.emit(f'add x1, x1, {label}@PAGEOFF')
            self.emit(f'mov x2, #{len(s)}')
            self.emit(f'mov x16, #4')
            self.emit(f'svc #0')
        else:
            # 包含插值:分段打印
            i = 0
            while i < len(s):
                if s[i] == '{':
                    end = s.find('}', i + 1)
                    if end == -1:
                        break
                    expr_str = s[i+1:end].strip()
                    # 解析并打印表达式
                    from aurora.lexer import Lexer
                    from aurora.parser import Parser
                    try:
                        lexer = Lexer(expr_str)
                        tokens = lexer.tokenize()
                        parser = Parser(tokens)
                        expr_ast = parser.parse_expression()
                        self.gen_expr_to_reg(expr_ast, 'x0')
                        self.emit('bl _aurora_print_int')
                    except:
                        pass
                    i = end + 1
                else:
                    next_brace = s.find('{', i)
                    if next_brace == -1:
                        part = s[i:]
                        i = len(s)
                    else:
                        part = s[i:next_brace]
                        i = next_brace
                    if part:
                        label = self.get_string_label(part)
                        self.emit(f'mov x0, #1')
                        self.emit(f'adrp x1, {label}@PAGE')
                        self.emit(f'add x1, x1, {label}@PAGEOFF')
                        self.emit(f'mov x2, #{len(part)}')
                        self.emit(f'mov x16, #4')
                        self.emit(f'svc #0')

    def _gen_print_int_literal(self, val):
        """打印整数字面量"""
        s = str(val)
        label = self.get_string_label(s)
        self.emit(f'mov x0, #1')
        self.emit(f'adrp x1, {label}@PAGE')
        self.emit(f'add x1, x1, {label}@PAGEOFF')
        self.emit(f'mov x2, #{len(s)}')
        self.emit(f'mov x16, #4')
        self.emit(f'svc #0')

    def gen_if_expr(self, expr: IfExpr, reg: str):
        """生成 if 表达式(三元运算符风格)"""
        else_label = self.new_label("ifexpr_else")
        end_label = self.new_label("ifexpr_end")

        self.gen_expr_to_reg(expr.condition, 'x9')
        self.emit('cmp x9, #0')
        self.emit(f'b.eq {else_label}')

        # then 分支
        if expr.then_body and expr.then_body.statements:
            last = expr.then_body.statements[-1]
            if isinstance(last, ExprStmt):
                self.gen_expr_to_reg(last.expr, reg)
            elif isinstance(last, ReturnStmt) and last.value:
                self.gen_expr_to_reg(last.value, reg)
        self.emit(f'b {end_label}')

        # else 分支
        self.emit_raw(f'{else_label}:')
        if expr.else_body and expr.else_body.statements:
            last = expr.else_body.statements[-1]
            if isinstance(last, ExprStmt):
                self.gen_expr_to_reg(last.expr, reg)
            elif isinstance(last, ReturnStmt) and last.value:
                self.gen_expr_to_reg(last.value, reg)
        else:
            self.emit(f'mov {reg}, #0')

        self.emit_raw(f'{end_label}:')

    # ============================================================
    # Aurora v2.1.0 新特性:元组 / 可选链 / 推导式 / 结构体 / 模式匹配
    # ============================================================
    def gen_tuple_literal(self, expr: TupleLiteral, reg: str):
        """元组字面量:按数组布局创建,元素存于 data 区(+16 起)"""
        n = len(expr.elements)
        self.emit(f'mov x0, #{max(n, 1)}')
        self.emit('bl _aurora_array_new')
        self.emit('str x0, [x29, #-128]')
        for i, elem in enumerate(expr.elements):
            self.gen_expr_to_reg(elem, 'x2')
            self.emit('str x2, [x29, #-120]')
            self.emit('ldr x0, [x29, #-128]')
            self.emit(f'mov x1, #{i}')
            self.emit('bl _aurora_array_set')
        self.emit(f'mov x8, #{n}')
        self.emit('ldr x9, [x29, #-128]')
        self.emit('str x8, [x9, #8]       // 元组长度')
        self.emit(f'ldr {reg}, [x29, #-128]')

    def gen_tuple_index(self, expr: TupleIndex, reg: str):
        """元组索引 tup.0:计算偏移量加载"""
        self.gen_expr_to_reg(expr.object, 'x0')
        self.emit(f'mov x1, #{int(expr.index)}')
        self.emit('bl _aurora_array_get')
        self.emit(f'mov {reg}, x0')

    def gen_forced_unwrap(self, expr: ForcedUnwrap, reg: str):
        """强制解包 a!:求值后若为 nil(0)则 panic"""
        self.gen_expr_to_reg(expr.operand, reg)
        self.emit(f'cmp {reg}, #0')
        ok_label = self.new_label("unwrap_ok")
        self.emit(f'b.ne {ok_label}')
        self.emit('mov x0, #2            // nil 强制解包 panic')
        self.emit('bl _aurora_throw')
        self.emit_raw(f'{ok_label}:')

    def gen_null_coalesce(self, expr: NullCoalesce, reg: str):
        """空合并 left ?? right:left 为 nil(0)时取 right"""
        self.gen_expr_to_reg(expr.left, reg)
        end_label = self.new_label("nc_end")
        self.emit(f'cmp {reg}, #0')
        self.emit(f'b.ne {end_label}')
        self.gen_expr_to_reg(expr.right, reg)
        self.emit_raw(f'{end_label}:')

    def gen_optional_access(self, expr: OptionalAccess, reg: str):
        """可选链 obj?.member:obj 为 nil 时结果为 nil。
        后端无对象/成员系统,降级为对 obj 求值(保留副作用)后返回 0。"""
        self.gen_expr_to_reg(expr.object, 'x9')
        self.emit(f'mov {reg}, #0')

    def gen_pipe_expr(self, expr: PipeExpr, reg: str):
        """管道 x |> f(args):左侧值作为最后一个位置实参"""
        call = expr.call
        if isinstance(call, CallExpr) and isinstance(call.callee, Identifier):
            new_call = CallExpr(callee=call.callee,
                                args=list(call.args) + [expr.left],
                                named_args=list(call.named_args))
            self.gen_call_expr(new_call, reg)
        else:
            self.emit(f'mov {reg}, #0')

    # ---------- 推导式(ListComp/SetComp/MapComp) ----------
    def gen_list_comp(self, expr: ListComp, reg: str):
        self._gen_compile(expr.generators, expr.conditions,
                          value_expr=expr.expr, kind='list', reg=reg)

    def gen_set_comp(self, expr: SetComp, reg: str):
        self._gen_compile(expr.generators, expr.conditions,
                          value_expr=expr.expr, kind='set', reg=reg)

    def gen_map_comp(self, expr: MapComp, reg: str):
        self._gen_compile(expr.generators, expr.conditions,
                          key_expr=expr.key_expr, value_expr=expr.value_expr,
                          kind='map', reg=reg)

    def _gen_compile(self, generators, conditions, value_expr, kind, reg,
                     key_expr=None):
        """推导式降级为 for 循环 + 收集"""
        if not generators:
            self.emit(f'mov {reg}, #0')
            return
        # 容器容量 = 外层可迭代长度(单生成器上界)
        self.gen_expr_to_reg(generators[0].iterable, 'x0')
        self.emit('str x0, [x29, #-112]')
        self.emit('bl _aurora_array_len')
        if kind == 'list':
            self.emit('bl _aurora_array_new')
        else:
            self.emit('bl _aurora_map_new')
        self.emit('str x0, [x29, #-128]')    # result ptr
        self.emit('mov x9, #0')
        self.emit('str x9, [x29, #-120]')    # out_len = 0
        self._gen_comp_loops(generators, 0, conditions, kind,
                             value_expr, key_expr)
        self.emit(f'ldr {reg}, [x29, #-128]')

    def _gen_comp_loops(self, generators, k, conditions, kind,
                        value_expr, key_expr):
        """递归生成推导式的嵌套循环 + 条件 + 收集"""
        if k == len(generators):
            # 叶子:依次检查条件
            skip_labels = []
            for cond in conditions:
                self.gen_expr_to_reg(cond, 'x9')
                self.emit('cmp x9, #0')
                lbl = self.new_label("comp_cond_skip")
                self.emit(f'b.eq {lbl}')
                skip_labels.append(lbl)
            # 收集
            self.emit('ldr x0, [x29, #-128]')    # result
            if kind == 'list':
                self.gen_expr_to_reg(value_expr, 'x2')
                self.emit('str x2, [x29, #-104]')  # 暂存值
                self.emit('ldr x0, [x29, #-128]')
                self.emit('ldr x1, [x29, #-120]')  # out_len
                self.emit('ldr x2, [x29, #-104]')
                self.emit('bl _aurora_array_set')
                self.emit('ldr x9, [x29, #-120]')
                self.emit('add x9, x9, #1')
                self.emit('str x9, [x29, #-120]')
            elif kind == 'set':
                self.gen_expr_to_reg(value_expr, 'x1')
                self.emit('str x1, [x29, #-112]')  # 暂存 key
                self.emit('ldr x0, [x29, #-128]')
                self.emit('ldr x1, [x29, #-112]')
                self.emit('mov x2, x1')            # dummy value
                self.emit('bl _aurora_map_set')
            elif kind == 'map':
                self.gen_expr_to_reg(key_expr, 'x1')
                self.emit('str x1, [x29, #-112]')
                self.gen_expr_to_reg(value_expr, 'x2')
                self.emit('str x2, [x29, #-104]')
                self.emit('ldr x0, [x29, #-128]')
                self.emit('ldr x1, [x29, #-112]')
                self.emit('ldr x2, [x29, #-104]')
                self.emit('bl _aurora_map_set')
            for lbl in skip_labels:
                self.emit_raw(f'{lbl}:')
            return

        # 第 k 层:for target in iterable
        gen = generators[k]
        it_off = -56 - k * 24
        lim_off = -48 - k * 24
        i_off = -40 - k * 24
        self.gen_expr_to_reg(gen.iterable, 'x0')
        self.emit(f'str x0, [x29, #{it_off}]')
        self.emit('bl _aurora_array_len')
        self.emit(f'str x0, [x29, #{lim_off}]')
        # i = 0
        self.emit('mov x9, #0')
        self.emit(f'str x9, [x29, #{i_off}]')
        cond_label = self.new_label("comp_loop")
        end_label = self.new_label("comp_loop_end")
        self.emit_raw(f'{cond_label}:')
        self.emit(f'ldr x9, [x29, #{i_off}]')
        self.emit(f'ldr x10, [x29, #{lim_off}]')
        self.emit('cmp x9, x10')
        self.emit(f'b.ge {end_label}')
        # element = iter[i]
        self.emit(f'ldr x0, [x29, #{it_off}]')
        self.emit(f'ldr x1, [x29, #{i_off}]')
        self.emit('bl _aurora_array_get')
        # 绑定到 gen.target
        self.emit('mov x9, x0')
        self._store_reg_to_var('x9', gen.target)
        if self._get_var_offset(gen.target) is None and self._get_var_reg(gen.target) is None:
            self._alloc_stack_var(gen.target)
            self._store_reg_to_var('x9', gen.target)
        # 内层
        self._gen_comp_loops(generators, k + 1, conditions, kind,
                             value_expr, key_expr)
        # i++
        self.emit(f'ldr x9, [x29, #{i_off}]')
        self.emit('add x9, x9, #1')
        self.emit(f'str x9, [x29, #{i_off}]')
        self.emit(f'b {cond_label}')
        self.emit_raw(f'{end_label}:')

    # ---------- 结构体字面量 ----------
    def gen_struct_literal(self, expr: StructLiteral, reg: str):
        """结构体字面量:调用类型构造函数,字段按声明顺序作为位置参数"""
        args = [v for _, v in expr.fields]
        call = CallExpr(callee=Identifier(name=expr.type_name), args=args)
        self.gen_call_expr(call, reg)

    # ---------- 模式匹配 ----------
    def gen_match_expr(self, expr: MatchExpr, reg: str):
        self._gen_match_common(expr.subject, expr.arms, reg, is_expr=True)

    def gen_match_stmt(self, stmt: MatchStmt):
        self._gen_match_common(stmt.subject, stmt.arms, 'x9', is_expr=False)

    def _gen_match_common(self, subject, arms, reg, is_expr: bool):
        """match 编译为条件跳转链"""
        if not arms:
            if is_expr:
                self.emit(f'mov {reg}, #0')
            return
        self.gen_expr_to_reg(subject, 'x9')
        self.emit('str x9, [x29, #-128]')      # 保存 subject
        end_label = self.new_label("match_end")
        for arm in arms:
            next_label = self.new_label("match_next")
            self._gen_pattern_test(arm.pattern, next_label)
            if arm.body is not None:
                if is_expr:
                    self.gen_expr_to_reg(arm.body, reg)
                else:
                    self.gen_expr_to_reg(arm.body, 'x9')
            self.emit(f'b {end_label}')
            self.emit_raw(f'{next_label}:')
        # 无匹配:表达式结果为 0
        if is_expr:
            self.emit(f'mov {reg}, #0')
        self.emit_raw(f'{end_label}:')

    def _gen_pattern_test(self, pattern, nomatch_label: str):
        """生成模式测试:不匹配则跳转到 nomatch_label,匹配则顺序执行"""
        if isinstance(pattern, (WildcardPattern, BindPattern)):
            return  # 总是匹配
        if isinstance(pattern, LiteralPattern):
            self.emit('ldr x9, [x29, #-128]')   # subject
            self.gen_expr_to_reg(pattern.value, 'x10')
            self.emit('cmp x9, x10')
            self.emit(f'b.ne {nomatch_label}')
            return
        # Constructor/Struct/Tuple 模式:降级为总是匹配(不解构子字段)
        return

    # ---------- 解构绑定 ----------
    def gen_destructure_let(self, stmt: DestructureLet):
        """let (a, b) = expr:将元组元素依次赋给变量"""
        self.gen_expr_to_reg(stmt.initializer, 'x9')
        self.emit('str x9, [x29, #-128]')
        for i, name in enumerate(stmt.names):
            self.emit('ldr x0, [x29, #-128]')
            self.emit(f'mov x1, #{i}')
            self.emit('bl _aurora_array_get')
            self.emit('mov x9, x0')
            self.var_types[name] = self.var_types.get(name, 'int')
            self._store_reg_to_var('x9', name)
            if self._get_var_offset(name) is None and self._get_var_reg(name) is None:
                self._alloc_stack_var(name)
                self._store_reg_to_var('x9', name)

    # ============================================================
    # 编译期常量计算
    # ============================================================
    def _try_compile_time_eval(self, expr: CallExpr):
        """尝试编译期常量计算,成功返回整数值,失败返回 None"""
        if not isinstance(expr.callee, Identifier):
            return None
        func_name = expr.callee.name

        # 检查参数是否全是字面量
        const_args = []
        for arg in expr.args:
            if isinstance(arg, IntLiteral):
                const_args.append(int(arg.value))
            else:
                return None

        # 内置数学函数
        builtin = {
            'abs': lambda a: abs(a[0]),
            'min': lambda a: min(a),
            'max': lambda a: max(a),
            'gcd': lambda a: self._py_gcd(a[0], a[1]),
            'lcm': lambda a: abs(a[0] * a[1]) // self._py_gcd(a[0], a[1]) if a[1] != 0 else 0,
            'factorial': lambda a: self._py_factorial(a[0]),
            'fibonacci': lambda a: self._py_fibonacci(a[0]),
        }

        if func_name in builtin:
            try:
                return builtin[func_name](const_args)
            except:
                return None

        # 用户定义的函数(参数全为字面量时尝试编译期求值)
        if func_name in self.functions:
            # 检查函数是否适合编译期求值(无 IO 副作用、无循环)
            if self._is_compile_time_safe(self.functions[func_name]):
                try:
                    result = self._ct_eval_function(self.functions[func_name], const_args, {})
                    return result
                except:
                    return None

        return None

    def _is_compile_time_safe(self, fn_def, _visited=None) -> bool:
        """检测函数是否适合编译期求值(无 IO 副作用、无循环)
        递归函数允许,只要没有副作用(编译期求值器有深度限制和记忆化)"""
        if _visited is None:
            _visited = set()
        if id(fn_def) in _visited:
            return True  # 递归调用:假设安全(正在检查中)
        _visited.add(id(fn_def))

        pure_builtins = {'abs', 'min', 'max', 'gcd', 'lcm', 'factorial', 'fibonacci'}

        def check_expr(expr):
            if isinstance(expr, CallExpr):
                if isinstance(expr.callee, Identifier):
                    name = expr.callee.name
                    if name not in pure_builtins and name not in self.functions:
                        return False
                    if name in self.functions:
                        if not self._is_compile_time_safe(self.functions[name], _visited):
                            return False
                for arg in expr.args:
                    if not check_expr(arg):
                        return False
            elif isinstance(expr, BinaryOp):
                return check_expr(expr.left) and check_expr(expr.right)
            elif isinstance(expr, UnaryOp):
                return check_expr(expr.operand)
            return True

        def check_stmt(stmt):
            if isinstance(stmt, ExprStmt):
                return check_expr(stmt.expr)
            elif isinstance(stmt, ReturnStmt) and stmt.value:
                return check_expr(stmt.value)
            elif isinstance(stmt, IfStmt):
                if not check_expr(stmt.condition):
                    return False
                if stmt.then_body:
                    for s in stmt.then_body.statements:
                        if not check_stmt(s):
                            return False
                if stmt.else_body:
                    for s in stmt.else_body.statements:
                        if not check_stmt(s):
                            return False
                return True
            elif isinstance(stmt, (ForStmt, WhileStmt)):
                return False
            elif isinstance(stmt, (LetStmt, ConstStmt)) and stmt.initializer:
                return check_expr(stmt.initializer)
            elif isinstance(stmt, AssignStmt):
                return check_expr(stmt.value)
            return True

        if fn_def.body:
            for stmt in fn_def.body.statements:
                if not check_stmt(stmt):
                    return False
        return True

    @staticmethod
    def _py_gcd(a, b):
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

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

    def _ct_eval_function(self, fn_def, args, cache):
        """编译期递归求值器(带深度限制和记忆化)"""
        self._ct_depth = getattr(self, '_ct_depth', 0) + 1
        if self._ct_depth > 10000:
            self._ct_depth -= 1
            raise RuntimeError("compile-time eval recursion depth exceeded")
        cache_key = (fn_def.name, tuple(args))
        if cache_key in cache:
            self._ct_depth -= 1
            return cache[cache_key]

        env = {}
        for i, param in enumerate(fn_def.params):
            if i < len(args):
                env[param.name] = args[i]

        result = self._ct_eval_block(fn_def.body, env, cache) if fn_def.body else 0
        if isinstance(result, tuple) and result[0] == 'return':
            result = result[1]

        cache[cache_key] = result
        self._ct_depth -= 1
        return result

    def _ct_eval_block(self, block, env, cache):
        result = 0
        for stmt in block.statements:
            r = self._ct_eval_stmt(stmt, env, cache)
            if r is not None:
                if isinstance(r, tuple) and r[0] == 'return':
                    return r
                result = r
        return result

    def _ct_eval_stmt(self, stmt, env, cache):
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
        elif isinstance(stmt, (LetStmt, ConstStmt)):
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
        if isinstance(expr, IntLiteral):
            return int(expr.value)
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
                if func_name in self.functions:
                    args = [self._ct_eval_expr(a, env, cache) for a in expr.args]
                    return self._ct_eval_function(self.functions[func_name], args, cache)
            return 0
        return 0

    # ============================================================
    # 内置辅助函数(用汇编写的运行时)
    # ============================================================
    def _gen_builtin_helpers(self):
        """生成内置辅助函数"""
        self.emit_raw('')
        self.emit_raw('// ============================================================')
        self.emit_raw('// 内置辅助函数')
        self.emit_raw('// ============================================================')

        # _aurora_print_int: 打印 x0 中的整数(十进制)
        self.emit_raw('')
        self.emit_raw('_aurora_print_int:')
        self.emit('stp x29, x30, [sp, #-64]!')
        self.emit('mov x29, sp')
        self.emit('stp x19, x20, [sp, #16]')
        self.emit('stp x21, x22, [sp, #32]')
        self.emit('')
        self.emit('mov x19, x0          // 保存数字')
        self.emit('mov x20, #0          // 数字长度')
        self.emit('add x21, sp, #60     // 缓冲区末尾(栈上)')
        self.emit('mov w22, #10         // 除数')
        self.emit('')
        self.emit('// 处理负数')
        self.emit('cmp x19, #0')
        self.emit('b.ge _aurora_print_int_loop')
        self.emit('neg x19, x19')
        self.emit('mov w8, #45          // \'-\'')
        self.emit('strb w8, [x21, #-1]!')
        self.emit('add x20, x20, #1')
        self.emit('')
        self.emit_raw('_aurora_print_int_loop:')
        self.emit('cmp x19, #0')
        self.emit('b.eq _aurora_print_int_done')
        self.emit('sdiv x8, x19, x22')
        self.emit('msub x9, x8, x22, x19  // x9 = x19 % 10')
        self.emit('add w9, w9, #48       // 转 ASCII')
        self.emit('strb w9, [x21, #-1]!')
        self.emit('mov x19, x8')
        self.emit('add x20, x20, #1')
        self.emit('b _aurora_print_int_loop')
        self.emit('')
        self.emit_raw('_aurora_print_int_done:')
        self.emit('cmp x20, #0')
        self.emit('b.ne _aurora_print_int_write')
        self.emit('mov w8, #48          // 数字为0时输出"0"')
        self.emit('strb w8, [x21, #-1]!')
        self.emit('add x20, x20, #1')
        self.emit('')
        self.emit_raw('_aurora_print_int_write:')
        self.emit('mov x0, #1           // stdout')
        self.emit('mov x1, x21          // buffer')
        self.emit('mov x2, x20          // length')
        self.emit('mov x16, #4          // write')
        self.emit('svc #0')
        self.emit('')
        self.emit('ldp x19, x20, [sp, #16]')
        self.emit('ldp x21, x22, [sp, #32]')
        self.emit('ldp x29, x30, [sp], #64')
        self.emit('ret')

        # _aurora_pow_int: 整数幂运算 x0^x1
        self.emit_raw('')
        self.emit_raw('_aurora_pow_int:')
        self.emit('mov x2, #1           // result')
        self.emit('cmp x1, #0')
        self.emit('b.lt _aurora_pow_zero')
        self.emit_raw('_aurora_pow_loop:')
        self.emit('cmp x1, #0')
        self.emit('b.eq _aurora_pow_done')
        self.emit('mul x2, x2, x0')
        self.emit('sub x1, x1, #1')
        self.emit('b _aurora_pow_loop')
        self.emit_raw('_aurora_pow_zero:')
        self.emit('mov x2, #0')
        self.emit_raw('_aurora_pow_done:')
        self.emit('mov x0, x2')
        self.emit('ret')

        # 记忆化缓存(如果有需要记忆化的函数)
        if self._memoized_funcs:
            self.emit_raw('')
            self.emit_raw('// 记忆化缓存')
            for fn_name in self._memoized_funcs:
                label = f"_memo_{self.c_ident(fn_name)}"
                self.data_section.append(f'.align 3')
                self.data_section.append(f'{label}_cache: .zero 800000  // 100000 * 8 bytes')
                self.data_section.append(f'{label}_valid: .zero 100000  // 100000 bytes')

        # ============================================================
        # 内存分配器 (简单 bump allocator,静态堆)
        # ============================================================
        self.data_section.append('.align 4')
        self.data_section.append('_aurora_heap: .zero 1048576  // 1MB 静态堆')
        self.data_section.append('_aurora_heap_ptr: .quad _aurora_heap')

        self.emit_raw('')
        self.emit_raw('// _aurora_malloc: 分配 x0 字节内存,返回指针在 x0 (bump allocator)')
        self.emit_raw('_aurora_malloc:')
        self.emit('adrp x1, _aurora_heap_ptr@PAGE')
        self.emit('add x1, x1, _aurora_heap_ptr@PAGEOFF')
        self.emit('ldr x2, [x1]          // 当前堆指针')
        self.emit('mov x3, x2')
        self.emit('add x3, x3, x0        // 新指针')
        self.emit('str x3, [x1]          // 更新堆指针')
        self.emit('mov x0, x2            // 返回旧指针')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_free: 空操作(bump allocator 不释放)')
        self.emit_raw('_aurora_free:')
        self.emit('ret')

        # ============================================================
        # 浮点数辅助函数
        # ============================================================
        self.emit_raw('')
        self.emit_raw('// _aurora_print_float: 打印 d0 中的双精度浮点数')
        self.emit_raw('_aurora_print_float:')
        self.emit('stp x29, x30, [sp, #-128]!')
        self.emit('mov x29, sp')
        self.emit('stp x19, x20, [sp, #16]')
        self.emit('stp d8, d9, [sp, #32]')
        self.emit('fmov d8, d0            // 保存原始值')
        self.emit('')
        self.emit('// 处理负数')
        self.emit('fmov x19, d0')
        self.emit('cmp x19, #0')
        self.emit('b.ge _aurora_print_float_abs')
        self.emit('mov w8, #45            // \'-\'')
        self.emit('strb w8, [sp, #64]')
        self.emit('fneg d8, d8')
        self.emit('mov x20, #1            // 有负号')
        self.emit('b _aurora_print_float_start')
        self.emit_raw('_aurora_print_float_abs:')
        self.emit('mov x20, #0            // 无负号')
        self.emit_raw('_aurora_print_float_start:')
        self.emit('// 整数部分')
        self.emit('fcvtzs x19, d8         // x19 = (int)d8')
        self.emit('scvtf d9, x19          // d9 = (double)x19')
        self.emit('fsub d9, d8, d9        // d9 = 小数部分')
        self.emit('')
        self.emit('// 打印整数部分(复用整数打印逻辑)')
        self.emit('mov x0, x19')
        self.emit('bl _aurora_print_int')
        self.emit('')
        self.emit('// 打印小数点')
        self.emit('mov w8, #46            // \'.\'')
        self.emit('strb w8, [sp, #64]')
        self.emit('mov x0, #1')
        self.emit('add x1, sp, #64')
        self.emit('mov x2, #1')
        self.emit('mov x16, #4')
        self.emit('svc #0')
        self.emit('')
        self.emit('// 打印小数部分(6位)')
        self.emit('mov x19, #6            // 6位小数')
        self.emit_raw('_aurora_print_float_dec_loop:')
        self.emit('cmp x19, #0')
        self.emit('b.eq _aurora_print_float_dec_done')
        self.emit('fmov d10, #10.0')
        self.emit('fmul d9, d9, d10       // 小数部分 * 10')
        self.emit('fcvtzs x8, d9          // x8 = 整数位')
        self.emit('scvtf d10, x8')
        self.emit('fsub d9, d9, d10       // 剩余小数')
        self.emit('add w8, w8, #48        // 转 ASCII')
        self.emit('strb w8, [sp, #64]')
        self.emit('mov x0, #1')
        self.emit('add x1, sp, #64')
        self.emit('mov x2, #1')
        self.emit('mov x16, #4')
        self.emit('svc #0')
        self.emit('sub x19, x19, #1')
        self.emit('b _aurora_print_float_dec_loop')
        self.emit_raw('_aurora_print_float_dec_done:')
        self.emit('')
        self.emit('ldp x19, x20, [sp, #16]')
        self.emit('ldp d8, d9, [sp, #32]')
        self.emit('ldp x29, x30, [sp], #128')
        self.emit('ret')

        # ============================================================
        # 字符串辅助函数
        # ============================================================
        self.emit_raw('')
        self.emit_raw('// _aurora_strlen: x0 = 字符串指针,返回长度在 x0')
        self.emit_raw('_aurora_strlen:')
        self.emit('mov x1, #0')
        self.emit_raw('_aurora_strlen_loop:')
        self.emit('ldrb w2, [x0, x1]')
        self.emit('cmp w2, #0')
        self.emit('b.eq _aurora_strlen_done')
        self.emit('add x1, x1, #1')
        self.emit('b _aurora_strlen_loop')
        self.emit_raw('_aurora_strlen_done:')
        self.emit('mov x0, x1')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_str_concat: x0 = s1, x1 = s2,返回新字符串指针')
        self.emit_raw('_aurora_str_concat:')
        self.emit('stp x29, x30, [sp, #-48]!')
        self.emit('mov x29, sp')
        self.emit('stp x19, x20, [sp, #16]')
        self.emit('stp x21, x22, [sp, #32]')
        self.emit('mov x19, x0            // s1')
        self.emit('mov x20, x1            // s2')
        self.emit('bl _aurora_strlen')
        self.emit('mov x21, x0            // len1')
        self.emit('mov x0, x20')
        self.emit('bl _aurora_strlen')
        self.emit('mov x22, x0            // len2')
        self.emit('add x0, x21, x22')
        self.emit('add x0, x0, #1         // +1 for null terminator')
        self.emit('bl _aurora_malloc')
        self.emit('mov x1, x0             // dst')
        self.emit('// 复制 s1')
        self.emit('mov x2, #0')
        self.emit_raw('_aurora_str_concat_l1:')
        self.emit('cmp x2, x21')
        self.emit('b.ge _aurora_str_concat_l2')
        self.emit('ldrb w3, [x19, x2]')
        self.emit('strb w3, [x1, x2]')
        self.emit('add x2, x2, #1')
        self.emit('b _aurora_str_concat_l1')
        self.emit_raw('_aurora_str_concat_l2:')
        self.emit('// 复制 s2')
        self.emit('mov x3, #0')
        self.emit_raw('_aurora_str_concat_l3:')
        self.emit('cmp x3, x22')
        self.emit('b.ge _aurora_str_concat_done')
        self.emit('ldrb w4, [x20, x3]')
        self.emit('strb w4, [x1, x2]')
        self.emit('add x2, x2, #1')
        self.emit('add x3, x3, #1')
        self.emit('b _aurora_str_concat_l3')
        self.emit_raw('_aurora_str_concat_done:')
        self.emit('strb wzr, [x1, x2]     // null terminator')
        self.emit('ldp x19, x20, [sp, #16]')
        self.emit('ldp x21, x22, [sp, #32]')
        self.emit('ldp x29, x30, [sp], #48')
        self.emit('ret')

        # ============================================================
        # 数组辅助函数
        # ============================================================
        self.emit_raw('')
        self.emit_raw('// _aurora_array_new: x0 = 容量,返回数组指针(头部:8字节容量+8字节长度+数据)')
        self.emit_raw('_aurora_array_new:')
        self.emit('stp x29, x30, [sp, #-32]!')
        self.emit('mov x29, sp')
        self.emit('str x0, [sp, #16]      // 保存容量')
        self.emit('lsl x1, x0, #3         // 数据大小 = capacity * 8')
        self.emit('add x0, x1, #16        // +16 字节头部')
        self.emit('bl _aurora_malloc')
        self.emit('ldr x1, [sp, #16]')
        self.emit('str x1, [x0, #0]       // capacity')
        self.emit('str xzr, [x0, #8]      // length = 0')
        self.emit('ldp x29, x30, [sp], #32')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_array_push: x0 = 数组指针, x1 = 值')
        self.emit_raw('_aurora_array_push:')
        self.emit('ldr x2, [x0, #8]       // length')
        self.emit('ldr x3, [x0, #0]       // capacity')
        self.emit('cmp x2, x3')
        self.emit('b.ge _aurora_array_push_grow')
        self.emit('add x9, x0, #16         // data base (跳过 16 字节头)')
        self.emit('str x1, [x9, x2, lsl #3]  // data[length] = value')
        self.emit('add x2, x2, #1')
        self.emit('str x2, [x0, #8]       // length++')
        self.emit('ret')
        self.emit_raw('_aurora_array_push_grow:')
        self.emit('// 简单扩容: 容量翻倍(此处简化为直接返回,实际应重新分配)')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_array_get: x0 = 数组指针, x1 = 索引,返回值在 x0')
        self.emit_raw('_aurora_array_get:')
        self.emit('add x9, x0, #16         // data base (跳过 16 字节头)')
        self.emit('ldr x2, [x9, x1, lsl #3]')
        self.emit('mov x0, x2')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_array_set: x0 = 数组指针, x1 = 索引, x2 = 值')
        self.emit_raw('_aurora_array_set:')
        self.emit('add x9, x0, #16         // data base (跳过 16 字节头)')
        self.emit('str x2, [x9, x1, lsl #3]')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_array_len: x0 = 数组指针,返回长度在 x0')
        self.emit_raw('_aurora_array_len:')
        self.emit('ldr x0, [x0, #8]')
        self.emit('ret')

        # ============================================================
        # Map/字典辅助函数 (简单线性探测哈希表,整数键->整数值)
        # 布局: [0]=capacity, [8]=length, [16]=keys数组, [24]=values数组
        # ============================================================
        self.emit_raw('')
        self.emit_raw('// _aurora_map_new: x0 = 容量,返回 Map 指针')
        self.emit_raw('_aurora_map_new:')
        self.emit('stp x29, x30, [sp, #-32]!')
        self.emit('mov x29, sp')
        self.emit('str x0, [sp, #16]')
        self.emit('mov x0, #32          // 头部 32 字节')
        self.emit('bl _aurora_malloc')
        self.emit('mov x19, x0')
        self.emit('ldr x1, [sp, #16]')
        self.emit('str x1, [x19, #0]   // capacity')
        self.emit('str xzr, [x19, #8]  // length = 0')
        self.emit('// 分配 keys 数组')
        self.emit('lsl x0, x1, #3')
        self.emit('bl _aurora_malloc')
        self.emit('str x0, [x19, #16]')
        self.emit('// 分配 values 数组')
        self.emit('ldr x0, [sp, #16]')
        self.emit('lsl x0, x0, #3')
        self.emit('bl _aurora_malloc')
        self.emit('str x0, [x19, #24]')
        self.emit('// 初始化 keys 为 -1(空槽)')
        self.emit('ldr x2, [x19, #16]')
        self.emit('ldr x3, [sp, #16]')
        self.emit('mov x4, #0')
        self.emit('mov x5, #-1')
        self.emit_raw('_aurora_map_init_loop:')
        self.emit('cmp x4, x3')
        self.emit('b.ge _aurora_map_init_done')
        self.emit('str x5, [x2, x4, lsl #3]')
        self.emit('add x4, x4, #1')
        self.emit('b _aurora_map_init_loop')
        self.emit_raw('_aurora_map_init_done:')
        self.emit('mov x0, x19')
        self.emit('ldp x29, x30, [sp], #32')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_map_set: x0=map, x1=key, x2=value')
        self.emit_raw('_aurora_map_set:')
        self.emit('stp x29, x30, [sp, #-48]!')
        self.emit('mov x29, sp')
        self.emit('stp x19, x20, [sp, #16]')
        self.emit('stp x21, x22, [sp, #32]')
        self.emit('mov x19, x0')
        self.emit('mov x20, x1')
        self.emit('mov x21, x2')
        self.emit('ldr x22, [x19, #0]   // capacity')
        self.emit('// 哈希: key % capacity (处理负数)')
        self.emit('mov x8, x20')
        self.emit('cmp x8, #0')
        self.emit('b.ge _aurora_map_set_hash')
        self.emit('neg x8, x8')
        self.emit_raw('_aurora_map_set_hash:')
        self.emit('sdiv x9, x8, x22')
        self.emit('msub x9, x9, x22, x8  // x9 = key % cap')
        self.emit('ldr x10, [x19, #16]  // keys')
        self.emit('ldr x11, [x19, #24]  // values')
        self.emit_raw('_aurora_map_set_probe:')
        self.emit('ldr x12, [x10, x9, lsl #3]')
        self.emit('cmp x12, #-1')
        self.emit('b.eq _aurora_map_set_empty')
        self.emit('cmp x12, x20')
        self.emit('b.eq _aurora_map_set_update')
        self.emit('add x9, x9, #1')
        self.emit('cmp x9, x22')
        self.emit('b.lt _aurora_map_set_probe')
        self.emit('mov x9, #0')
        self.emit('b _aurora_map_set_probe')
        self.emit_raw('_aurora_map_set_empty:')
        self.emit('str x20, [x10, x9, lsl #3]')
        self.emit('str x21, [x11, x9, lsl #3]')
        self.emit('ldr x12, [x19, #8]')
        self.emit('add x12, x12, #1')
        self.emit('str x12, [x19, #8]')
        self.emit('b _aurora_map_set_done')
        self.emit_raw('_aurora_map_set_update:')
        self.emit('str x21, [x11, x9, lsl #3]')
        self.emit_raw('_aurora_map_set_done:')
        self.emit('ldp x19, x20, [sp, #16]')
        self.emit('ldp x21, x22, [sp, #32]')
        self.emit('ldp x29, x30, [sp], #48')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_map_get: x0=map, x1=key,返回 value(找不到返回0)')
        self.emit_raw('_aurora_map_get:')
        self.emit('stp x29, x30, [sp, #-32]!')
        self.emit('mov x29, sp')
        self.emit('str x19, [sp, #16]')
        self.emit('mov x19, x0')
        self.emit('ldr x2, [x19, #0]   // capacity')
        self.emit('mov x8, x1')
        self.emit('cmp x8, #0')
        self.emit('b.ge _aurora_map_get_hash')
        self.emit('neg x8, x8')
        self.emit_raw('_aurora_map_get_hash:')
        self.emit('sdiv x9, x8, x2')
        self.emit('msub x9, x9, x2, x8')
        self.emit('ldr x10, [x19, #16]')
        self.emit('ldr x11, [x19, #24]')
        self.emit_raw('_aurora_map_get_probe:')
        self.emit('ldr x12, [x10, x9, lsl #3]')
        self.emit('cmp x12, #-1')
        self.emit('b.eq _aurora_map_get_notfound')
        self.emit('cmp x12, x1')
        self.emit('b.eq _aurora_map_get_found')
        self.emit('add x9, x9, #1')
        self.emit('cmp x9, x2')
        self.emit('b.lt _aurora_map_get_probe')
        self.emit('mov x9, #0')
        self.emit('b _aurora_map_get_probe')
        self.emit_raw('_aurora_map_get_found:')
        self.emit('ldr x0, [x11, x9, lsl #3]')
        self.emit('b _aurora_map_get_done')
        self.emit_raw('_aurora_map_get_notfound:')
        self.emit('mov x0, #0')
        self.emit_raw('_aurora_map_get_done:')
        self.emit('ldr x19, [sp, #16]')
        self.emit('ldp x29, x30, [sp], #32')
        self.emit('ret')

        self.emit_raw('')
        self.emit_raw('// _aurora_map_len: x0=map,返回长度')
        self.emit_raw('_aurora_map_len:')
        self.emit('ldr x0, [x0, #8]')
        self.emit('ret')

        # ============================================================
        # 异常处理 (简化版 setjmp/longjmp)
        # _aurora_exception: 全局异常指针(0表示无异常)
        # _aurora_jmpbuf: 全局跳转缓冲区 [sp, pc]
        # ============================================================
        self.data_section.append('.align 3')
        self.data_section.append('_aurora_exception: .zero 8')
        self.data_section.append('_aurora_jmpbuf_sp: .zero 8')
        self.data_section.append('_aurora_jmpbuf_pc: .zero 8')

        self.emit_raw('')
        self.emit_raw('// _aurora_throw: x0 = 异常值,设置异常并 longjmp 到最近 catch')
        self.emit_raw('_aurora_throw:')
        self.emit('adrp x1, _aurora_exception@PAGE')
        self.emit('add x1, x1, _aurora_exception@PAGEOFF')
        self.emit('str x0, [x1]')
        self.emit('// 恢复 sp 和 pc')
        self.emit('adrp x1, _aurora_jmpbuf_sp@PAGE')
        self.emit('add x1, x1, _aurora_jmpbuf_sp@PAGEOFF')
        self.emit('ldr x2, [x1]')
        self.emit('cmp x2, #0')
        self.emit('b.eq _aurora_throw_no_catch')
        self.emit('mov sp, x2')
        self.emit('adrp x1, _aurora_jmpbuf_pc@PAGE')
        self.emit('add x1, x1, _aurora_jmpbuf_pc@PAGEOFF')
        self.emit('ldr x3, [x1]')
        self.emit('br x3')
        self.emit_raw('_aurora_throw_no_catch:')
        self.emit('// 无 catch,直接退出')
        self.emit('mov x0, #1')
        self.emit('mov x16, #1')
        self.emit('svc #0')


# ============================================================
# 便捷函数
# ============================================================
def generate_asm(program: Program) -> str:
    """从 AST 生成 ARM64 汇编代码"""
    gen = ARM64CodeGenerator()
    return gen.generate(program)


def compile_to_asm(source_path: str, output_path: str = None) -> tuple:
    """
    编译 Aurora 源代码为 ARM64 汇编,然后用 as/ld 生成可执行文件。
    不依赖 C 编译器和 C 运行时库。
    返回 (可执行文件路径, 编译输出)。
    """
    import subprocess

    # 读取源代码
    with open(source_path, "r") as f:
        source = f.read()

    # 解析
    from aurora.parser import Parser
    from aurora.lexer import Lexer
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    # 生成汇编
    asm_code = generate_asm(program)

    # 写入临时汇编文件
    with tempfile.NamedTemporaryFile(suffix=".s", mode="w", delete=False) as f:
        asm_path = f.name
        f.write(asm_code)

    # 确定输出路径
    if output_path is None:
        base = os.path.splitext(os.path.basename(source_path))[0]
        output_path = os.path.join(os.path.dirname(source_path) or '.', base)

    # 汇编
    obj_path = asm_path + ".o"
    as_cmd = ["as", "-o", obj_path, asm_path]
    result = subprocess.run(as_cmd, capture_output=True, text=True)
    compile_output = result.stdout + result.stderr

    if result.returncode != 0:
        try:
            os.unlink(asm_path)
        except:
            pass
        raise RuntimeError(f"汇编失败:\n{compile_output}\n\n汇编文件: {asm_path}")

    # 链接
    sdk_path = subprocess.run(["xcrun", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()
    ld_cmd = [
        "ld", "-o", output_path,
        obj_path,
        "-lSystem",
        "-syslibroot", sdk_path,
        "-arch", "arm64",
    ]
    result = subprocess.run(ld_cmd, capture_output=True, text=True)
    compile_output += result.stdout + result.stderr

    # 清理临时文件
    try:
        os.unlink(asm_path)
        os.unlink(obj_path)
    except:
        pass

    if result.returncode != 0:
        raise RuntimeError(f"链接失败:\n{compile_output}")

    return output_path, compile_output
