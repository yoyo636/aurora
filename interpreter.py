"""Aurora 树遍历解释器 — 直接执行 AST"""

import os
import re
import threading
from typing import Any, Dict, List, Optional

from .ast_nodes import *
from .lexer import Lexer
from .parser import Parser
from .stdlib import (
    AuroraChannel, AuroraMutex, AuroraFiber, AuroraResult, AuroraEnumVariant,
    AuroraError, BUILTIN_GLOBALS, STDLIB_MODULES, _CH_EMPTY,
)


# ── 返回值 / 控制流信号 ─────────────────────────────────

class ReturnValue:
    def __init__(self, value=None):
        self.value = value


class BreakSignal(Exception): pass
class ContinueSignal(Exception): pass
class ReturnSignal(Exception):
    def __init__(self, value=None):
        self.value = value


class ResultPropagateSignal(Exception):
    """? 操作符：遇到 Err 时从当前函数返回该 AuroraResult（Rust 风格错误传播）"""
    def __init__(self, result):
        self.result = result


# ── 环境 ────────────────────────────────────────────────

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings: Dict[str, Any] = {}
        self._mutable: Dict[str, bool] = {}

    def get(self, name: str):
        if name in self.bindings:
            return self.bindings[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def has(self, name: str) -> bool:
        if name in self.bindings:
            return True
        return self.parent.has(name) if self.parent else False

    def set(self, name: str, value):
        """赋值给已有的变量（向上查找）；let 绑定的不可变变量禁止重赋值"""
        if name in self.bindings:
            if not self._mutable.get(name, True):
                raise AuroraError(
                    "TypeError",
                    f"不可变绑定 '{name}' 不能被重新赋值(如需修改,请改用 var 声明)")
            self.bindings[name] = value
            return
        if self.parent and self.parent.has(name):
            self.parent.set(name, value)
            return
        self.bindings[name] = value
        self._mutable[name] = True  # 不存在则当前作用域新建

    def define(self, name: str, value, mutable: bool = True):
        self.bindings[name] = value
        self._mutable[name] = mutable

    def child(self):
        return Environment(parent=self)


# ── 解释器 ──────────────────────────────────────────────

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self._output: List[str] = []      # 捕获输出
        # impl 方法注册表：type_name -> {method_name: fn}
        self._impl_methods: Dict[str, Dict[str, Any]] = {}
        # trait 默认实现表：trait_name -> {method_name: fn}
        self._trait_defaults: Dict[str, Dict[str, Any]] = {}
        # 多文件模块系统
        self._module_cache: Dict[str, dict] = {}   # 绝对路径 -> 模块 dict
        self._file_stack: List[str] = []            # 当前执行的文件栈(循环导入检测)
        self._project_root: Optional[str] = None    # 项目根(含 aurora.toml 的目录)
        # Aurora 创新特性：@perf(trace) 调用统计
        self._perf_trace: Dict[str, dict] = {}
        # 标记：当前是否处于 `?` 操作数求值中（期间禁止自动解包 Result 返回值）
        self._no_unwrap: bool = False
        self._load_builtins()

    # ── 加载内建 ──────────────────────────────────────

    def _load_builtins(self):
        for name, val in BUILTIN_GLOBALS.items():
            self.global_env.define(name, val)

    def _get_cache(self):
        """惰性创建函数级增量编译缓存（进程内 + 磁盘持久化）"""
        if getattr(self, "_inc_cache", None) is None:
            from .incremental_cache import IncrementalCompilerCache
            self._inc_cache = IncrementalCompilerCache()
        return self._inc_cache

    def _register_function_cache(self, stmt: FnDef):
        """函数定义时计算内容哈希并接入增量编译缓存（未修改则命中）"""
        try:
            cache = self._get_cache()
            cached = cache.get(stmt)
            if cached is None:
                # 未命中：登记占位编译产物（树遍历解释器中即函数 AST 本身）
                from .incremental_cache import CompiledFunction
                cache.put(stmt, CompiledFunction(
                    name=stmt.name, func_hash=cache.function_hash(stmt),
                    machine_code="<interpreted>"))
        except Exception:
            # 缓存失败不应影响正常解释执行（保守降级）
            pass

    # ── 公共 API ──────────────────────────────────────

    def run(self, program: Program, file_path: str = None) -> Any:
        self._output = []
        if file_path:
            file_path = os.path.abspath(file_path)
            self._file_stack.append(file_path)
            if self._project_root is None:
                self._project_root = self._find_project_root(file_path)
        try:
            return self._exec_stmts(program.statements, self.global_env)
        except ResultPropagateSignal as s:
            # 顶层使用 `?` 遇到 Err：自动 panic（可被 try/catch 捕获）
            raise AuroraError("ResultError", str(s.result._err))
        finally:
            if file_path:
                self._file_stack.pop()

    def run_file(self, path: str) -> Any:
        """从文件路径运行 Aurora 程序(支持多文件 import)"""
        path = os.path.abspath(path)
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        return self.run(program, file_path=path)

    @staticmethod
    def _find_project_root(start_path: str) -> Optional[str]:
        """向上查找含 aurora.toml 的目录作为项目根"""
        cur = os.path.dirname(start_path)
        for _ in range(20):
            if os.path.isfile(os.path.join(cur, 'aurora.toml')):
                return cur
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
        return None

    def get_output(self) -> List[str]:
        return list(self._output)

    # ── 语句执行 ──────────────────────────────────────

    def _exec_stmts(self, stmts: List[Stmt], env: Environment) -> Any:
        result = None
        for stmt in stmts:
            result = self._exec_stmt(stmt, env)
            if isinstance(result, ReturnSignal):
                return result
        return result

    def _exec_stmt(self, stmt: Stmt, env: Environment) -> Any:
        if isinstance(stmt, LetStmt):
            val = self._eval(stmt.initializer, env) if stmt.initializer else None
            env.define(stmt.name, val, mutable=stmt.mutable)
            return val

        if isinstance(stmt, DestructureLet):
            val = self._eval(stmt.initializer, env)
            if isinstance(val, (tuple, list)):
                if len(val) < len(stmt.names):
                    raise AuroraError(
                        "ValueError",
                        f"解构绑定需要至少 {len(stmt.names)} 个元素,实际 {len(val)} 个")
                for i, name in enumerate(stmt.names):
                    env.define(name, val[i], mutable=stmt.mutable)
            elif isinstance(val, dict):
                for name in stmt.names:
                    if name not in val:
                        raise AuroraError(
                            "KeyError", f"解构绑定:字典缺少键 '{name}'")
                    env.define(name, val[name], mutable=stmt.mutable)
            else:
                raise AuroraError(
                    "TypeError",
                    f"无法解构类型 '{type(val).__name__}',仅支持元组/列表/字典")
            return val

        if isinstance(stmt, ConstStmt):
            val = self._eval(stmt.initializer, env)
            env.define(stmt.name, val)
            return val

        if isinstance(stmt, AssignStmt):
            val = self._eval(stmt.value, env)
            if isinstance(stmt.target, Identifier):
                if stmt.op != "=":
                    cur = env.get(stmt.target.name)
                    val = self._apply_binary(stmt.op.rstrip("="), cur, val)
                env.set(stmt.target.name, val)
            elif isinstance(stmt.target, MemberAccess):
                obj = self._eval(stmt.target.object, env)
                if isinstance(obj, dict):
                    obj[stmt.target.member] = val
                else:
                    setattr(obj, stmt.target.member, val)
            elif isinstance(stmt.target, IndexAccess):
                obj = self._eval(stmt.target.object, env)
                idx = self._eval(stmt.target.index, env)
                obj[idx] = val
            return val

        if isinstance(stmt, ReturnStmt):
            val = self._eval(stmt.value, env) if stmt.value else None
            return ReturnSignal(val)

        if isinstance(stmt, BreakStmt):
            raise BreakSignal()

        if isinstance(stmt, ContinueStmt):
            raise ContinueSignal()

        if isinstance(stmt, ExprStmt):
            return self._eval(stmt.expr, env)

        if isinstance(stmt, DeferStmt):
            # 注册到最近的函数根环境(循环/块内注册也统一在函数退出时 LIFO 执行)
            # 调用参数在注册时求值(Go 风格),退出时再执行调用
            stack = self._find_attr(env, "_defer_stack")
            if stack is None:
                stack = []
                env._defer_stack = stack
            if stmt.body is not None:
                stack.append(('block', stmt.body))
            elif isinstance(stmt.expr, CallExpr):
                fn = self._eval(stmt.expr.callee, env)
                args = [self._eval(a, env) for a in stmt.expr.args]
                named = {n: self._eval(v, env) for n, v in stmt.expr.named_args}
                stack.append(('call', fn, args, named))
            elif isinstance(stmt.expr, MethodCall):
                obj = self._eval(stmt.expr.object, env)
                args = [self._eval(a, env) for a in stmt.expr.args]
                method = self._get_method(obj, stmt.expr.method, env)
                stack.append(('method', method, args))
            else:
                stack.append(('eval', stmt.expr))
            return None

        if isinstance(stmt, YieldStmt):
            vals = self._find_attr(env, "_yield_values")
            if vals is None:
                vals = []
                env._yield_values = vals
            vals.append(self._eval(stmt.value, env) if stmt.value else None)
            return None

        if isinstance(stmt, IfStmt):
            return self._exec_if(stmt, env)

        if isinstance(stmt, ForStmt):
            return self._exec_for(stmt, env)

        if isinstance(stmt, WhileStmt):
            return self._exec_while(stmt, env)

        if isinstance(stmt, MatchStmt):
            return self._exec_match(stmt, env)

        if isinstance(stmt, FnDef):
            # 函数级增量编译缓存：计算内容哈希并尝试复用编译产物
            self._register_function_cache(stmt)
            env.define(stmt.name, self._make_function(stmt, env))
            return None

        if isinstance(stmt, TypeDef):
            env.define(stmt.name, self._make_type_constructor(stmt, env))
            return None

        if isinstance(stmt, EnumDef):
            self._register_enum(stmt, env)
            return None

        if isinstance(stmt, TraitDef):
            # trait 不产生运行时值；有函数体的方法注册为默认实现
            table = self._trait_defaults.setdefault(stmt.name, {})
            for m in stmt.methods:
                if m.body is not None:
                    table[m.name] = self._make_function(m, env, is_impl=True)
            return None

        if isinstance(stmt, ImplBlock):
            return self._exec_impl(stmt, env)

        if isinstance(stmt, ImportStmt):
            return self._exec_import(stmt, env)

        if isinstance(stmt, TryStmt):
            return self._exec_try(stmt, env)

        if isinstance(stmt, SpawnStmt):
            return self._exec_spawn(stmt, env)

        if isinstance(stmt, SelectStmt):
            return self._exec_select(stmt, env)

        if isinstance(stmt, TestBlock):
            return self._exec_test(stmt, env)

        if isinstance(stmt, Block):
            child_env = env.child()
            return self._exec_stmts(stmt.statements, child_env)

        return None

    # ── 控制流 ────────────────────────────────────────

    def _exec_if(self, stmt: IfStmt, env: Environment) -> Any:
        if self._truthy(self._eval(stmt.condition, env)):
            return self._exec_stmts(stmt.then_body.statements, env.child())
        for cond, body in stmt.elif_clauses:
            if self._truthy(self._eval(cond, env)):
                return self._exec_stmts(body.statements, env.child())
        if stmt.else_body:
            return self._exec_stmts(stmt.else_body.statements, env.child())
        return None

    def _exec_for(self, stmt: ForStmt, env: Environment) -> Any:
        iterable = self._eval(stmt.iterable, env)
        result = None
        if isinstance(iterable, dict) and len(stmt.variables) == 2:
            for k, v in iterable.items():
                child = env.child()
                child.define(stmt.variables[0], k)
                child.define(stmt.variables[1], v)
                try:
                    result = self._exec_stmts(stmt.body.statements, child)
                    if isinstance(result, ReturnSignal):
                        return result
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        elif len(stmt.variables) == 1:
            for item in iterable:
                child = env.child()
                child.define(stmt.variables[0], item)
                try:
                    result = self._exec_stmts(stmt.body.statements, child)
                    if isinstance(result, ReturnSignal):
                        return result
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        else:
            for item in iterable:
                child = env.child()
                if isinstance(item, (tuple, list)) and len(item) == len(stmt.variables):
                    for var, val in zip(stmt.variables, item):
                        child.define(var, val)
                else:
                    child.define(stmt.variables[0], item)
                try:
                    result = self._exec_stmts(stmt.body.statements, child)
                    if isinstance(result, ReturnSignal):
                        return result
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        return result

    def _exec_while(self, stmt: WhileStmt, env: Environment) -> Any:
        result = None
        while self._truthy(self._eval(stmt.condition, env)):
            try:
                result = self._exec_stmts(stmt.body.statements, env.child())
                if isinstance(result, ReturnSignal):
                    return result
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return result

    def _exec_match(self, stmt: MatchStmt, env: Environment) -> Any:
        subject = self._eval(stmt.subject, env)
        for arm in stmt.arms:
            bindings = self._match_pattern(arm.pattern, subject)
            if bindings is not None:
                child = env.child()
                for name, val in bindings.items():
                    child.define(name, val)
                return self._eval(arm.body, child)
        return None

    def _exec_try(self, stmt: TryStmt, env: Environment) -> Any:
        try:
            return self._exec_stmts(stmt.body.statements, env.child())
        except Exception as e:
            for catch in stmt.catches:
                child = env.child()
                child.define(catch.name, str(e))
                return self._exec_stmts(catch.body.statements, child)
        finally:
            if stmt.finally_body:
                self._exec_stmts(stmt.finally_body.statements, env.child())

    def _exec_spawn(self, stmt: SpawnStmt, env: Environment) -> Any:
        call = stmt.call
        if isinstance(call, CallExpr):
            fn = self._eval(call.callee, env)
            args = [self._eval(a, env) for a in call.args]
            fiber = AuroraFiber(fn, tuple(args))
            fiber.start()
            return fiber
        return None

    def _exec_select(self, stmt: SelectStmt, env: Environment) -> Any:
        import time as _time
        arms = [a for a in stmt.arms if not a.is_default]
        default = next((a for a in stmt.arms if a.is_default), None)

        if not arms:
            if default:
                return self._exec_stmts(default.body.statements, env.child())
            return None

        channels = []
        for arm in arms:
            ch_expr = arm.channel_expr
            # 支持 v = <-ch 绑定形式：从 ChannelRecv 中取出通道本身
            if isinstance(ch_expr, ChannelRecv):
                ch = self._eval(ch_expr.channel, env)
            else:
                ch = self._eval(ch_expr, env)
            channels.append((arm, ch))

        def _run_arm(arm, val):
            child = env.child()
            if arm.bind_name:
                child.define(arm.bind_name, val)
            return self._exec_stmts(arm.body.statements, child)

        # 第一轮：非阻塞尝试所有通道
        for arm, ch in channels:
            if isinstance(ch, AuroraChannel):
                val = ch.recv_nowait()
                if val is not _CH_EMPTY:
                    return _run_arm(arm, val)

        # 无立即就绪：有 default 则执行 default
        if default is not None:
            return self._exec_stmts(default.body.statements, env.child())

        # 无 default：阻塞等待任意通道就绪（短轮询）
        while True:
            for arm, ch in channels:
                if isinstance(ch, AuroraChannel):
                    val = ch.recv_nowait()
                    if val is not _CH_EMPTY:
                        return _run_arm(arm, val)
            # 所有通道均已关闭且为空 → 无值可取
            if all(isinstance(ch, AuroraChannel) and ch.is_closed()
                   for _, ch in channels):
                return None
            _time.sleep(0.02)

    def _exec_test(self, stmt: TestBlock, env: Environment) -> Any:
        child = env.child()
        try:
            self._exec_stmts(stmt.body.statements, child)
            self._capture_output(f"  ✓ {stmt.name}")
        except Exception as e:
            self._capture_output(f"  ✗ {stmt.name}: {e}")
        return None

    def _exec_import(self, stmt: ImportStmt, env: Environment) -> Any:
        path = '.'.join(stmt.path)
        module = STDLIB_MODULES.get(path)
        if module is None:
            # 尝试加载本地 .aur 模块
            module = self._load_local_module(stmt.path)
        if module is None:
            return None
        if stmt.names:
            if stmt.alias:
                # from x import a as b
                if stmt.names[0] in module:
                    env.define(stmt.alias, module[stmt.names[0]])
            else:
                for name in stmt.names:
                    if name in module:
                        env.define(name, module[name])
            return None

        # import std.io [as x]：同时建立 std.io.exists(...) 命名空间链
        root_name = stmt.path[0]
        existing = env.get(root_name)
        ns = existing if isinstance(existing, dict) else {}
        node = ns
        for seg in stmt.path[1:]:
            nxt = node.get(seg)
            if not isinstance(nxt, dict):
                nxt = {}
                node[seg] = nxt
            node = nxt
        node.update(module)
        env.define(root_name, ns)
        # 叶模块快捷方式：import std.io 后可直接 io.exists(...)
        mod_name = stmt.alias or stmt.path[-1]
        env.define(mod_name, module)
        return None

    # ── 多文件模块加载 ────────────────────────────────

    def _load_local_module(self, path_parts: List[str]) -> Optional[dict]:
        """加载本地 .aur 模块,返回模块导出 dict;找不到返回 None"""
        current_file = self._file_stack[-1] if self._file_stack else None
        resolved = self._resolve_module_path(path_parts, current_file)
        if resolved is None:
            return None
        abs_path = os.path.abspath(resolved)

        # 循环导入检测
        if abs_path in self._file_stack:
            raise AuroraError("ImportError",
                f"循环导入: {' -> '.join(os.path.basename(f) for f in self._file_stack)} -> {os.path.basename(abs_path)}")

        # 模块缓存
        if abs_path in self._module_cache:
            return self._module_cache[abs_path]

        # 读取并解析模块文件
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            raise AuroraError("ImportError", f"无法读取模块 {abs_path}: {e}")

        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        # 在子环境中执行模块,收集导出
        mod_env = Environment(parent=self.global_env)
        self._file_stack.append(abs_path)
        try:
            self._exec_stmts(program.statements, mod_env)
        finally:
            self._file_stack.pop()

        # 收集模块级定义(函数、变量、类型等)作为导出
        module = {}
        for name, value in mod_env.bindings.items():
            if name.startswith('_'):
                continue  # 下划线开头为模块私有
            module[name] = value

        self._module_cache[abs_path] = module
        return module

    def _resolve_module_path(self, path_parts: List[str],
                              current_file: Optional[str]) -> Optional[str]:
        """将点分模块路径解析为 .aur 文件绝对路径"""
        rel = os.path.join(*path_parts)
        candidates = [
            rel + '.aur',
            os.path.join(rel, '__init__.aur'),
        ]

        search_dirs = []
        if current_file:
            cur_dir = os.path.dirname(current_file)
            search_dirs.append(cur_dir)
            # 当前目录下的 src/
            src_in_cur = os.path.join(cur_dir, 'src')
            if os.path.isdir(src_in_cur):
                search_dirs.append(src_in_cur)
        if self._project_root:
            search_dirs.append(self._project_root)
            src_root = os.path.join(self._project_root, 'src')
            if os.path.isdir(src_root):
                search_dirs.append(src_root)
        # 兜底:当前工作目录
        search_dirs.append(os.getcwd())

        for d in search_dirs:
            for cand in candidates:
                full = os.path.join(d, cand)
                if os.path.isfile(full):
                    return full
        return None

    def _exec_impl(self, stmt: ImplBlock, env: Environment) -> Any:
        # 方法注册到解释器级 impl 方法表，按类型名索引
        table = self._impl_methods.setdefault(stmt.type_name, {})
        for method in stmt.methods:
            fn = self._make_function(method, env, is_impl=True)
            table[method.name] = fn
        # trait 默认实现：未覆盖的方法自动补齐
        if stmt.trait_name:
            defaults = self._trait_defaults.get(stmt.trait_name, {})
            for name, fn in defaults.items():
                if name not in table:
                    table[name] = fn
        return None

    # ── 表达式求值 ────────────────────────────────────

    def _eval(self, expr: Expr, env: Environment) -> Any:
        if expr is None:
            return None

        if isinstance(expr, IntLiteral):
            return expr.value
        if isinstance(expr, FloatLiteral):
            return expr.value
        if isinstance(expr, StringLiteral):
            if expr.raw:
                return expr.value
            return self._interpolate_string(expr.value, env)
        if isinstance(expr, BoolLiteral):
            return expr.value
        if isinstance(expr, NilLiteral):
            return None

        if isinstance(expr, Identifier):
            val = env.get(expr.name)
            if val is None and not env.has(expr.name):
                raise AuroraError("NameError", f"未定义的变量: '{expr.name}'")
            return val

        if isinstance(expr, ArrayLiteral):
            return [self._eval(e, env) for e in expr.elements]

        if isinstance(expr, MapLiteral):
            return {self._eval(k, env): self._eval(v, env) for k, v in expr.entries}

        if isinstance(expr, TupleLiteral):
            return tuple(self._eval(e, env) for e in expr.elements)

        if isinstance(expr, BinaryOp):
            left = self._eval(expr.left, env)
            right = self._eval(expr.right, env)
            return self._apply_binary(expr.op, left, right)

        if isinstance(expr, RangeExpr):
            # 区间 a..b:闭区间,含 b
            s = self._eval(expr.start, env)
            e = self._eval(expr.end, env)
            return list(range(int(s), int(e) + 1))

        if isinstance(expr, PipeExpr):
            # 管道:x |> f / x |> f(a) / x |> obj.m(a) —— 左侧值追加为最后一个参数
            left = self._eval(expr.left, env)
            call = expr.call
            if isinstance(call, CallExpr):
                fn = self._eval(call.callee, env)
                args = [self._eval(a, env) for a in call.args]
                named = {name: self._eval(v, env) for name, v in call.named_args}
                if not callable(fn):
                    raise AuroraError("TypeError", "管道右侧不可调用")
                try:
                    return fn(*args, left, **named)
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
            if isinstance(call, MethodCall):
                obj = self._eval(call.object, env)
                args = [self._eval(a, env) for a in call.args]
                method = self._get_method(obj, call.method, env)
                if not callable(method):
                    raise AuroraError("AttributeError",
                                      f"'{type(obj).__name__}' 没有方法 '{call.method}'")
                try:
                    return method(*args, left)
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
            if isinstance(call, Identifier):
                fn = self._eval(call, env)
                if not callable(fn):
                    raise AuroraError("TypeError", "管道右侧不可调用")
                return fn(left)
            raise AuroraError("TypeError", "管道右侧必须是函数名或函数调用")

        if isinstance(expr, UnaryOp):
            val = self._eval(expr.operand, env)
            if expr.op == '-':
                return -val
            if expr.op == '!':
                return not self._truthy(val)
            return val

        if isinstance(expr, CallExpr):
            fn = self._eval(expr.callee, env)
            args = [self._eval(a, env) for a in expr.args]
            named = {name: self._eval(v, env) for name, v in expr.named_args}
            if callable(fn):
                try:
                    if named and getattr(fn, '_aurora', False):
                        result = fn(*args, **named)
                    elif named:
                        result = fn(*args, **named)
                    else:
                        result = fn(*args)
                except AuroraError:
                    raise
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
                # Result 互操作：声明返回 Result[T,E] 的函数，调用点自动解包
                # （在 `?` 操作数求值期间不自动解包，交由 ? 处理 Err 传播）
                if (not self._no_unwrap
                        and getattr(fn, '_aurora_result_return', False)
                        and isinstance(result, AuroraResult)):
                    if result.is_err():
                        raise AuroraError("Panic", str(result._err))
                    return result._ok
                return result
            raise AuroraError("TypeError", f"'{expr.callee}' 不可调用")

        if isinstance(expr, MethodCall):
            obj = self._eval(expr.object, env)
            args = [self._eval(a, env) for a in expr.args]
            named = {name: self._eval(v, env) for name, v in expr.named_args}
            method = self._get_method(obj, expr.method, env)
            if callable(method):
                try:
                    if named and getattr(method, '_aurora', False):
                        return method(*args, **named)
                    if named:
                        return method(*args, **named)
                    return method(*args)
                except AuroraError:
                    raise
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
            raise AuroraError("AttributeError",
                              f"'{type(obj).__name__}' 没有方法 '{expr.method}'")

        if isinstance(expr, MemberAccess):
            obj = self._eval(expr.object, env)
            if isinstance(obj, dict):
                if expr.member.startswith('_'):
                    # 内部键（_type/_order）对用户隐藏
                    return None
                return obj.get(expr.member)
            try:
                return getattr(obj, expr.member, None)
            except AuroraError:
                raise

        if isinstance(expr, OptionalAccess):
            # 可选链：obj?.member，obj 为 nil 时整体为 nil
            obj = self._eval(expr.object, env)
            if obj is None:
                return None
            if isinstance(obj, dict):
                if expr.member.startswith('_'):
                    return None
                return obj.get(expr.member)
            try:
                return getattr(obj, expr.member, None)
            except AuroraError:
                raise

        if isinstance(expr, OptionalCall):
            # 可选链方法调用：obj?.method(args)，obj 为 nil 时整体为 nil
            obj = self._eval(expr.object, env)
            if obj is None:
                return None
            args = [self._eval(a, env) for a in expr.args]
            named = {name: self._eval(v, env) for name, v in expr.named_args}
            method = self._get_method(obj, expr.method, env)
            if callable(method):
                try:
                    if named and getattr(method, '_aurora', False):
                        return method(*args, **named)
                    if named:
                        return method(*args, **named)
                    return method(*args)
                except AuroraError:
                    raise
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
            raise AuroraError("AttributeError",
                              f"'{type(obj).__name__}' 没有方法 '{expr.method}'")

        if isinstance(expr, NullCoalesce):
            # 空合并：left ?? right，left 为 nil 时取 right
            left = self._eval(expr.left, env)
            if left is None:
                return self._eval(expr.right, env)
            return left

        if isinstance(expr, IndexAccess):
            obj = self._eval(expr.object, env)
            idx = self._eval(expr.index, env)
            try:
                return obj[idx]
            except (IndexError, KeyError):
                raise AuroraError("IndexError", "索引越界")

        if isinstance(expr, LambdaExpr):
            return self._make_lambda(expr, env)

        if isinstance(expr, IfExpr):
            if self._truthy(self._eval(expr.condition, env)):
                return self._exec_stmts(expr.then_body.statements, env.child())
            for cond, body in expr.elif_clauses:
                if self._truthy(self._eval(cond, env)):
                    return self._exec_stmts(body.statements, env.child())
            if expr.else_body:
                return self._exec_stmts(expr.else_body.statements, env.child())
            return None

        if isinstance(expr, MatchExpr):
            subject = self._eval(expr.subject, env)
            for arm in expr.arms:
                bindings = self._match_pattern(arm.pattern, subject)
                if bindings is not None:
                    child = env.child()
                    for name, val in bindings.items():
                        child.define(name, val)
                    return self._eval(arm.body, child)
            return None

        if isinstance(expr, SpawnExpr):
            call = expr.call
            fn = self._eval(call.callee if isinstance(call, CallExpr) else call, env)
            args = [self._eval(a, env) for a in (call.args if isinstance(call, CallExpr) else [])]
            fiber = AuroraFiber(fn, tuple(args))
            fiber.start()
            return fiber

        if isinstance(expr, ChannelSend):
            ch = self._eval(expr.channel, env)
            val = self._eval(expr.value, env)
            if isinstance(ch, AuroraChannel):
                ch.send(val)
            return None

        if isinstance(expr, ChannelRecv):
            ch = self._eval(expr.channel, env)
            if isinstance(ch, AuroraChannel):
                val = ch.recv_blocking()
                if val is _CH_EMPTY:
                    raise AuroraError("ChannelError", "从已关闭且为空的通道接收")
                return val
            raise AuroraError("TypeError", "'<-' 只能用于 channel")

        if isinstance(expr, OkExpr):
            return AuroraResult.Ok(self._eval(expr.value, env))

        if isinstance(expr, ErrExpr):
            return AuroraResult.Err(self._eval(expr.error, env))

        if isinstance(expr, TryExpr):
            # `expr?`：操作数求值期间禁止调用点自动解包，以便拿到原始 AuroraResult
            prev = self._no_unwrap
            self._no_unwrap = True
            try:
                val = self._eval(expr.expr, env)
            finally:
                self._no_unwrap = prev
            if isinstance(val, AuroraResult) and val.is_err():
                # Err：从当前函数返回该 Err（由函数包装层捕获）
                raise ResultPropagateSignal(val)
            if isinstance(val, AuroraResult):
                return val.unwrap()
            return val

        if isinstance(expr, RefExpr):
            # Python 没有真正的引用语义，这里简化处理
            return self._eval(expr.inner, env)

        if isinstance(expr, DerefExpr):
            val = self._eval(expr.inner, env)
            return val

        if isinstance(expr, StringInterpolation):
            parts = [str(self._eval(p, env)) for p in expr.parts]
            return ''.join(parts)

        return None

    # ── 辅助方法 ──────────────────────────────────────

    def _apply_binary(self, op: str, left, right) -> Any:
        ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else (_ for _ in ()).throw(AuroraError("MathError", "除以零")),
            '%': lambda a, b: a % b,
            '**': lambda a, b: a ** b,
            '<<': lambda a, b: int(a) << int(b),
            '>>': lambda a, b: int(a) >> int(b),
            '&': lambda a, b: int(a) & int(b),
            '|': lambda a, b: int(a) | int(b),
            '^': lambda a, b: int(a) ^ int(b),
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<': lambda a, b: a < b,
            '<=': lambda a, b: a <= b,
            '>': lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
            '&&': lambda a, b: self._truthy(a) and self._truthy(b),
            '||': lambda a, b: self._truthy(a) or self._truthy(b),
        }
        if op in ops:
            return ops[op](left, right)
        raise AuroraError("OperatorError", f"未知运算符: {op}")

    def _truthy(self, val) -> bool:
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            return len(val) > 0
        if isinstance(val, (list, dict, tuple)):
            return len(val) > 0
        return bool(val)

    def _interpolate_string(self, s: str, env: Environment) -> str:
        """字符串插值：将 {expr} 求值替换

        - `{{` / `}}` 转义为字面花括号
        - 支持任意表达式：{name}、{obj.field}、{fn(x)}、{a + b}
        - 表达式解析失败时保留原样（优雅降级）
        """
        out = []
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c == '{' and i + 1 < n and s[i + 1] == '{':
                out.append('{')
                i += 2
                continue
            if c == '}' and i + 1 < n and s[i + 1] == '}':
                out.append('}')
                i += 2
                continue
            if c == '{':
                depth = 1
                j = i + 1
                while j < n and depth > 0:
                    if s[j] == '{':
                        depth += 1
                    elif s[j] == '}':
                        depth -= 1
                    j += 1
                if depth == 0:
                    expr_str = s[i + 1:j - 1].strip()
                    out.append(self._eval_interp(expr_str, env))
                    i = j
                    continue
                out.append('{')
                i += 1
                continue
            out.append(c)
            i += 1
        return ''.join(str(x) for x in out)

    def _eval_interp(self, expr_str: str, env: Environment):
        if not expr_str:
            return ''
        # 简单标识符快速路径
        if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', expr_str) and env.has(expr_str):
            val = env.get(expr_str)
            return 'nil' if val is None else val
        # 完整表达式路径
        try:
            lexer = Lexer(expr_str)
            parser = Parser(lexer.tokenize())
            expr = parser.parse_expression()
            val = self._eval(expr, env)
            return 'nil' if val is None else val
        except Exception:
            return '{' + expr_str + '}'

    def _find_attr(self, env: Environment, attr: str):
        """沿父链向上查找第一个非空属性(用于函数根上的 defer 栈 / yield 收集)"""
        e = env
        while e is not None:
            v = getattr(e, attr, None)
            if v is not None:
                return v
            e = e.parent
        return None

    def _run_defers(self, fn_env: Environment):
        """按 LIFO 执行函数内注册的 defer"""
        stack = self._find_attr(fn_env, "_defer_stack")
        if not stack:
            return
        while stack:
            item = stack.pop()
            kind = item[0]
            if kind == 'block':
                self._exec_stmts(item[1].statements, fn_env)
            elif kind == 'call':
                _, fn, args, named = item
                try:
                    fn(*args, **named)
                except AuroraError:
                    raise
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
            elif kind == 'method':
                _, method, args = item
                try:
                    method(*args)
                except AuroraError:
                    raise
                except TypeError as e:
                    raise AuroraError("TypeError", str(e))
            else:
                self._eval(item[1], fn_env)

    def _make_function(self, fn_def: FnDef, closure_env: Environment,
                       is_impl: bool = False):
        def aurora_fn(*args, **kwargs):
            fn_env = closure_env.child()
            fn_env._defer_stack = []
            fn_env._yield_values = []
            param_map = {p.name: p for p in fn_def.params}

            if is_impl:
                # impl 方法：隐式绑定 self 为实例
                if not args:
                    raise AuroraError(
                        "TypeError",
                        f"impl 方法 '{fn_def.name}' 需要通过实例调用 (obj.{fn_def.name}(...))")
                fn_env.define('self', args[0])
                args = args[1:]

            # 绑定位置参数
            for i, arg in enumerate(args):
                if i < len(fn_def.params):
                    fn_env.define(fn_def.params[i].name, arg)
                else:
                    raise AuroraError(
                        "TypeError",
                        f"函数 '{fn_def.name}' 收到 {len(args)} 个位置参数，"
                        f"但最多接受 {len(fn_def.params)} 个")

            # 绑定命名参数
            for name, val in kwargs.items():
                if name not in param_map:
                    raise AuroraError(
                        "TypeError",
                        f"函数 '{fn_def.name}' 没有参数 '{name}'")
                if fn_env.has(name):
                    raise AuroraError(
                        "TypeError",
                        f"函数 '{fn_def.name}' 的参数 '{name}' 被重复指定")
                fn_env.define(name, val)

            # 处理未绑定参数：默认值或报错
            for p in fn_def.params:
                if not fn_env.has(p.name):
                    if p.default_value is not None:
                        fn_env.define(p.name, self._eval(p.default_value, closure_env))
                    else:
                        raise AuroraError(
                            "TypeError",
                            f"函数 '{fn_def.name}' 缺少必要参数 '{p.name}'")

            # @perf(trace)：自动记录调用次数与耗时
            trace_enabled = fn_def.get_perf_hints().get("trace", False)
            if trace_enabled:
                import time as _t
                _t0 = _t.perf_counter()

            try:
                result = self._exec_stmts(fn_def.body.statements, fn_env)
            except ResultPropagateSignal as s:
                # `?` 遇到 Err：直接从当前函数返回该 Err（传播错误）
                self._run_defers(fn_env)
                return s.result

            self._run_defers(fn_env)
            yields = getattr(fn_env, "_yield_values", None)
            if yields:
                return yields
            if isinstance(result, ReturnSignal):
                retval = result.value
            else:
                retval = result

            if trace_enabled:
                stat = self._perf_trace.setdefault(
                    fn_def.name, {"calls": 0, "total_time_ms": 0.0})
                stat["calls"] += 1
                stat["total_time_ms"] += (_t.perf_counter() - _t0) * 1000.0
            return retval

        # 返回类型为 Result[T, E]（泛型两参）的函数：调用点自动解包
        rt = fn_def.return_type
        returns_result = (isinstance(rt, GenericType) and rt.base == 'Result'
                           and len(rt.type_args) == 2)

        aurora_fn.__name__ = fn_def.name
        aurora_fn._ast = fn_def
        aurora_fn._aurora = True
        aurora_fn._aurora_result_return = returns_result
        return aurora_fn

    def _make_lambda(self, expr: LambdaExpr, closure_env: Environment):
        def aurora_lambda(*args, **kwargs):
            fn_env = closure_env.child()
            fn_env._defer_stack = []
            fn_env._yield_values = []
            param_map = {p.name: p for p in expr.params}
            for i, arg in enumerate(args):
                if i < len(expr.params):
                    fn_env.define(expr.params[i].name, arg)
                else:
                    raise AuroraError("TypeError", "lambda 收到过多位置参数")
            for name, val in kwargs.items():
                if name not in param_map:
                    raise AuroraError("TypeError", f"lambda 没有参数 '{name}'")
                if fn_env.has(name):
                    raise AuroraError("TypeError", f"lambda 参数 '{name}' 被重复指定")
                fn_env.define(name, val)
            for p in expr.params:
                if not fn_env.has(p.name):
                    if p.default_value is not None:
                        fn_env.define(p.name, self._eval(p.default_value, closure_env))
                    else:
                        raise AuroraError("TypeError", f"lambda 缺少必要参数 '{p.name}'")
            result = self._exec_stmts(expr.body.statements, fn_env)
            self._run_defers(fn_env)
            yields = getattr(fn_env, "_yield_values", None)
            if yields:
                return yields
            if isinstance(result, ReturnSignal):
                return result.value
            return result

        aurora_lambda._aurora = True
        return aurora_lambda

    def _make_type_constructor(self, type_def: TypeDef, closure_env: Environment = None):
        """为自定义类型生成构造函数（支持位置/命名参数、字段默认值）"""
        fields = type_def.fields
        names = [f[0] for f in fields]
        default_map = {f[0]: f[2] for f in fields if f[2] is not None}
        env = closure_env or self.global_env

        def constructor(*args, **kwargs):
            obj = {'_type': type_def.name, '_order': names}
            for i, a in enumerate(args):
                if i >= len(names):
                    raise AuroraError(
                        "TypeError",
                        f"类型 '{type_def.name}' 收到 {len(args)} 个位置参数，"
                        f"但只有 {len(names)} 个字段")
                obj[names[i]] = a
            for key in kwargs:
                if key not in names:
                    raise AuroraError(
                        "TypeError",
                        f"类型 '{type_def.name}' 没有字段 '{key}'")
            for name in names:
                if name in kwargs:
                    obj[name] = kwargs[name]
                elif name not in obj:
                    if name in default_map:
                        obj[name] = self._eval(default_map[name], env)
                    else:
                        obj[name] = None
            return obj

        constructor.__name__ = type_def.name
        constructor._aurora = True
        return constructor

    def _register_enum(self, enum_def: EnumDef, env: Environment):
        """注册枚举变体构造器，统一生成 AuroraEnumVariant 实例"""
        enum_dict = {}
        for variant in enum_def.variants:
            fields = [(f_name, f_type) for f_name, f_type in variant.fields]

            def make_constructor(v_name, v_fields):
                field_names = [f[0] for f in v_fields]

                def constructor(*args, **kwargs):
                    fdict = {}
                    for i, a in enumerate(args):
                        if i >= len(field_names):
                            raise AuroraError(
                                "TypeError",
                                f"变体 '{v_name}' 收到 {len(args)} 个位置参数，"
                                f"但只有 {len(field_names)} 个字段")
                        fdict[field_names[i]] = a
                    for key in kwargs:
                        if key not in field_names:
                            raise AuroraError(
                                "TypeError",
                                f"变体 '{v_name}' 没有字段 '{key}'")
                        fdict[key] = kwargs[key]
                    return AuroraEnumVariant(v_name, fdict)

                constructor.__name__ = v_name
                constructor._aurora = True
                return constructor

            enum_dict[variant.name] = make_constructor(variant.name, fields)
        env.define(enum_def.name, enum_dict)

    def _get_method(self, obj, method_name: str, env: Environment):
        """获取对象的方法（impl 注册方法 / 内建集合方法 / 原生方法）"""
        # 1) impl 注册的方法（按类型名查找）
        type_name = None
        if isinstance(obj, dict) and '_type' in obj:
            type_name = obj['_type']
        elif isinstance(obj, AuroraEnumVariant):
            type_name = obj._name
        if type_name:
            impl_methods = self._impl_methods.get(type_name, {})
            if method_name in impl_methods:
                fn = impl_methods[method_name]

                def bound(*a, **kw):
                    return fn(obj, *a, **kw)
                return bound

        # 2) dict 自定义键优先(模块成员;避免 std.http.get 命中 dict.get 内建方法)
        if isinstance(obj, dict) and method_name in obj:
            return obj[method_name]

        # 3) Python 原生方法
        method = getattr(obj, method_name, None)
        if method is not None:
            return method

        # 3) 集合特殊方法
        # 数组/列表/元组
        if isinstance(obj, (list, tuple)):
            if method_name == 'append' and isinstance(obj, list):
                return obj.append
            if method_name == 'len':
                return lambda: len(obj)
            if method_name == 'map':
                return lambda fn: [fn(x) for x in obj]
            if method_name == 'filter':
                return lambda fn: [x for x in obj if fn(x)]
            if method_name == 'reduce':
                def _reduce(*args):
                    # 统一参数序: reduce(init, fn); 兼容 reduce(fn) 经典写法
                    if len(args) == 1:
                        fn, init = args[0], None
                    elif len(args) >= 2:
                        init, fn = args[0], args[1]
                    else:
                        raise AuroraError("TypeError", "reduce 至少需要一个函数参数")
                    if not callable(fn):
                        raise AuroraError("TypeError", f"reduce 的第一个参数 '{init}' 不是函数")
                    if init is None:
                        if not obj:
                            return None
                        acc = obj[0]
                        rest = obj[1:]
                    else:
                        acc = init
                        rest = obj
                    for x in rest:
                        acc = fn(acc, x)
                    return acc
                return _reduce
            if method_name == 'join':
                return lambda sep='': sep.join(str(x) for x in obj)
            if method_name == 'clone':
                return lambda: list(obj)
            if method_name == 'contains':
                return lambda item: item in obj
            if method_name == 'push' and isinstance(obj, list):
                return obj.append
            if method_name == 'pop' and isinstance(obj, list):
                return obj.pop
        # 字符串
        if isinstance(obj, str):
            if method_name == 'len':
                return lambda: len(obj)
            if method_name == 'upper':
                return lambda: obj.upper()
            if method_name == 'lower':
                return lambda: obj.lower()
            if method_name == 'split':
                return lambda sep=None: obj.split(sep)
            if method_name == 'trim':
                return lambda: obj.strip()
            if method_name == 'contains':
                return lambda sub: sub in obj
            if method_name == 'replace':
                return lambda old, new='': obj.replace(old, new)
            if method_name == 'starts_with':
                return lambda prefix: obj.startswith(prefix)
            if method_name == 'ends_with':
                return lambda suffix: obj.endswith(suffix)
            if method_name == 'clone':
                return lambda: obj
        # dict
        if isinstance(obj, dict):
            if method_name in obj and callable(obj[method_name]):
                return obj[method_name]
            if method_name == 'get':
                return obj.get
            if method_name == 'keys':
                return lambda: [k for k in obj.keys() if not k.startswith('_')]
            if method_name == 'values':
                return lambda: [v for k, v in obj.items() if not k.startswith('_')]
            if method_name == 'items':
                return lambda: [(k, v) for k, v in obj.items() if not k.startswith('_')]
            if method_name == 'clone':
                return lambda: dict(obj)
        return None

    def _match_pattern(self, pattern: Pattern, value) -> Optional[Dict[str, Any]]:
        """模式匹配，返回绑定字典或 None"""
        if isinstance(pattern, WildcardPattern):
            return {}
        if isinstance(pattern, LiteralPattern):
            pat_val = pattern.value
            if isinstance(pat_val, IntLiteral) and value == pat_val.value:
                return {}
            if isinstance(pat_val, StringLiteral) and value == pat_val.value:
                return {}
            if isinstance(pat_val, BoolLiteral) and value == pat_val.value:
                return {}
            return None
        if isinstance(pattern, BindPattern):
            return {pattern.name: value}
        if isinstance(pattern, ConstructorPattern):
            # 枚举变体（AuroraEnumVariant）
            if isinstance(value, AuroraEnumVariant):
                if value._name == pattern.name:
                    bindings = {}
                    order = value._order
                    for i, field_pat in enumerate(pattern.fields):
                        key = order[i] if i < len(order) else None
                        field_bindings = self._match_pattern(
                            field_pat, value._fields.get(key))
                        if field_bindings is None:
                            return None
                        bindings.update(field_bindings)
                    return bindings
                return None
            # 自定义类型实例（dict 携带 _type）
            if isinstance(value, dict) and '_type' in value:
                if value['_type'] == pattern.name:
                    bindings = {}
                    order = value.get('_order', [])
                    for i, field_pat in enumerate(pattern.fields):
                        key = order[i] if i < len(order) else None
                        field_bindings = self._match_pattern(
                            field_pat, value.get(key))
                        if field_bindings is None:
                            return None
                        bindings.update(field_bindings)
                    return bindings
                return None
            # 旧格式 dict 枚举（兼容）
            if isinstance(value, dict) and '_variant' in value:
                if value['_variant'] == pattern.name:
                    bindings = {}
                    for i, field_pat in enumerate(pattern.fields):
                        field_bindings = self._match_pattern(field_pat, value.get(f'_{i}'))
                        if field_bindings is None:
                            return None
                        bindings.update(field_bindings)
                    return bindings
            # Ok / Err Result 匹配
            if isinstance(value, AuroraResult):
                if pattern.name == 'Ok' and value.is_ok():
                    if pattern.fields:
                        return self._match_pattern(pattern.fields[0], value._ok)
                    return {}
                if pattern.name == 'Err' and value.is_err():
                    if pattern.fields:
                        return self._match_pattern(pattern.fields[0], value._err)
                    return {}
            return None
        return None

    def _capture_output(self, text: str):
        self._output.append(text)
        print(text)
