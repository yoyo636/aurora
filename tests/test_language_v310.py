"""Aurora v3.1.0 语言级增强测试。

覆盖:
  - pub 关键字:模块可见性 / 导出表
  - #[cfg(...)] 属性:条件编译(target_os / target_arch / feature / not/and/or)
  - extern "C" 块:外部函数声明与注册
  - unsafe 块:原始指针读写;safe 上下文报错
  - async/await:协程对象、await、EventLoop.run/gather/sleep
  - defer:Go 风格 LIFO 延迟执行,正常返回与异常时均执行
"""

import os
import platform

import pytest

from aurora.lexer import Lexer
from aurora.parser import Parser
from aurora.interpreter import (
    Interpreter, Memory, Coroutine, AuroraEventLoop,
    InterpCfgEvaluator,
)
from aurora.ast_nodes import (
    Attribute, ExternBlock, ExternFn, UnsafeBlock, AwaitExpr,
)
from aurora.stdlib import AuroraError
from aurora.interpreter import ReturnSignal


def run(src):
    """编译并执行源码,返回 (解释器, 顶层返回值)。"""
    program = Parser(Lexer(src).tokenize()).parse()
    interp = Interpreter()
    result = interp.run(program)
    if isinstance(result, ReturnSignal):
        result = result.value
    return interp, result


# ════════════════════════════════════════════════════════════
# 1. pub —— 模块可见性
# ════════════════════════════════════════════════════════════

class TestPubVisibility:

    def test_pub_function_marked_public(self):
        interp, _ = run(
            'pub fn add(a, b) { return a + b }\n'
            'fn private_fn(x) { return x }\n')
        assert interp.export_table['add'] is True
        assert interp.export_table['private_fn'] is False

    def test_pub_const_and_let(self):
        interp, _ = run(
            'pub const VERSION = "3.1.0"\n'
            'const INTERNAL = 1\n'
            'pub let PUBLIC_VAR = 10\n')
        assert interp.export_table['VERSION'] is True
        assert interp.export_table['INTERNAL'] is False
        assert interp.export_table['PUBLIC_VAR'] is True

    def test_pub_callable_from_same_module(self):
        interp, result = run(
            'pub fn add(a, b) { return a + b }\n'
            'return add(2, 3)\n')
        assert result == 5

    def test_non_pub_not_exported(self):
        """非 pub 符号不进入导出表(True/False 记录)。"""
        interp, _ = run(
            'pub fn exported() { return 1 }\n'
            'fn hidden() { return 2 }\n')
        assert interp.export_table['exported'] is True
        assert interp.export_table['hidden'] is False


# ════════════════════════════════════════════════════════════
# 2. #[cfg(...)] —— 条件编译
# ════════════════════════════════════════════════════════════

class TestCfg:

    def test_cfg_evaluator_basic(self):
        ev = InterpCfgEvaluator({'target_os': 'macos',
                                 'target_arch': 'arm64',
                                 'features': {'gui'}})
        assert ev.evaluate('target_os = "macos"') is True
        assert ev.evaluate('target_os = "windows"') is False
        assert ev.evaluate('feature = "gui"') is True
        assert ev.evaluate('feature = "cli"') is False

    def test_cfg_logic_combinators(self):
        ev = InterpCfgEvaluator({'target_os': 'macos', 'features': set()})
        assert ev.evaluate('not(target_os = "windows")') is True
        assert ev.evaluate('or(target_os = "linux", target_os = "macos")') is True
        assert ev.evaluate('and(target_os = "macos", feature = "x")') is False

    def test_cfg_mac_on_mac_executed(self):
        """当前为 macOS(darwin) 时,cfg(macos) 函数应被执行。"""
        os_name = platform.system().lower()
        expected_present = os_name in ('darwin', 'macos')
        interp, _ = run(
            '#[cfg(target_os = "macos")]\n'
            'pub fn on_mac() { return 1 }\n'
            '#[cfg(target_os = "windows")]\n'
            'pub fn on_win() { return 2 }\n')
        assert ('on_mac' in interp.export_table) == expected_present
        assert 'on_win' not in interp.export_table

    def test_cfg_not_and_or_skipped(self):
        interp, _ = run(
            '#[cfg(not(target_os = "windows"))]\n'
            'pub fn not_win() { return 1 }\n'
            '#[cfg(and(target_os = "macos", feature = "nonexistent_xyz"))]\n'
            'pub fn and_false() { return 2 }\n'
            '#[cfg(or(target_os = "macos", target_os = "linux"))]\n'
            'pub fn or_true() { return 3 }\n')
        assert 'not_win' in interp.export_table
        assert 'and_false' not in interp.export_table
        assert 'or_true' in interp.export_table

    def test_cfg_feature_from_env(self, monkeypatch):
        monkeypatch.setenv('AURORA_FEATURES', 'gui,debug')
        ev = InterpCfgEvaluator()
        assert ev.evaluate('feature = "gui"') is True
        assert ev.evaluate('feature = "debug"') is True
        assert ev.evaluate('feature = "cli"') is False

    def test_attribute_node_parsed(self):
        program = Parser(Lexer(
            '#[cfg(target_os = "macos")]\n'
            'pub fn f() { return 1 }\n').tokenize()).parse()
        fn = program.statements[0]
        assert len(fn.attributes) == 1
        assert fn.attributes[0].name == 'cfg'
        assert 'target_os' in fn.attributes[0].raw


# ════════════════════════════════════════════════════════════
# 3. extern "C" —— 外部函数声明
# ════════════════════════════════════════════════════════════

class TestExtern:

    def test_extern_block_parses(self):
        program = Parser(Lexer(
            'extern "C" {\n'
            '  fn printf(fmt: *u8) -> i32;\n'
            '  fn malloc(size: usize) -> *void;\n'
            '}\n').tokenize()).parse()
        block = program.statements[0]
        assert isinstance(block, ExternBlock)
        assert block.abi == 'C'
        names = [d.name for d in block.declarations]
        assert names == ['printf', 'malloc']
        assert block.declarations[0].return_type is not None

    def test_extern_declarations_registered(self):
        interp, _ = run(
            'extern "C" {\n'
            '  fn printf(fmt: *u8) -> i32;\n'
            '  fn malloc(size: usize) -> *void;\n'
            '}\n')
        assert 'printf' in interp.extern_registry
        assert 'malloc' in interp.extern_registry
        # 注册的是外部调用占位
        assert getattr(interp.extern_registry['printf'], '_extern', False)

    def test_extern_call_missing_symbol_raises(self):
        interp, _ = run(
            'extern "C" { fn aurora_nonexistent_sym_xyz() -> i32; }\n'
            'fn caller() { return aurora_nonexistent_sym_xyz() }\n')
        with pytest.raises(AuroraError) as exc:
            interp.global_env.get('caller')()
        assert 'extern function' in str(exc.value)


# ════════════════════════════════════════════════════════════
# 4. unsafe —— 原始指针 / 内存操作
# ════════════════════════════════════════════════════════════

class TestUnsafe:

    def test_unsafe_block_parses(self):
        program = Parser(Lexer('unsafe { let x = 1 }\n').tokenize()).parse()
        assert isinstance(program.statements[0], UnsafeBlock)

    def test_unsafe_pointer_read_write(self):
        _, result = run(
            'let n = 100\n'
            'unsafe {\n'
            '  let addr = &n\n'
            '  *addr = 999\n'
            '  return *addr\n'
            '}\n')
        assert result == 999

    def test_safe_deref_raises(self):
        with pytest.raises(AuroraError) as exc:
            run('let p = 5\nreturn *p\n')
        assert 'UnsafeError' in str(exc.value)

    def test_safe_pointer_write_raises(self):
        with pytest.raises(AuroraError):
            run('let p = 5\n*p = 1\n')

    def test_unsafe_fn_callable_in_unsafe_block(self):
        _, result = run(
            'unsafe fn danger() { return 42 }\n'
            'unsafe { return danger() }\n')
        assert result == 42

    def test_unsafe_fn_call_in_safe_context_raises(self):
        with pytest.raises(AuroraError) as exc:
            run('unsafe fn danger() { return 42 }\nreturn danger()\n')
        assert 'UnsafeError' in str(exc.value)

    def test_memory_class(self):
        mem = Memory()
        addr = mem.allocate(10)
        assert mem.read(addr) == 10
        mem.write(addr, 99)
        assert mem.read(addr) == 99
        with pytest.raises(AuroraError):
            mem.read(0xDEAD)


# ════════════════════════════════════════════════════════════
# 5. async / await —— 异步编程
# ════════════════════════════════════════════════════════════

class TestAsync:

    def test_async_fn_returns_coroutine(self):
        interp, _ = run('async fn work() { return 1 }\n')
        coro = interp.global_env.get('work')()
        assert isinstance(coro, Coroutine)

    def test_await_unwraps_result(self):
        _, result = run(
            'async fn double(x) { return x * 2 }\n'
            'return await double(21)\n')
        assert result == 42

    def test_await_expr_node(self):
        program = Parser(Lexer('return await f(x)\n').tokenize()).parse()
        ret = program.statements[0]
        assert isinstance(ret.value, AwaitExpr)

    def test_event_loop_run(self):
        interp, _ = run('async fn one() { return 1 }\n')
        coro = interp.global_env.get('one')()
        assert interp.event_loop.run(coro) == 1

    def test_event_loop_gather(self):
        _, result = run(
            'async fn a() { return 1 }\n'
            'async fn b() { return 2 }\n'
            'let c1 = a()\n'
            'let c2 = b()\n'
            'return event_loop.gather(c1, c2)\n')
        assert result == [1, 2]

    def test_event_loop_sleep_runs(self):
        # sleep 不应抛错(允许 0 秒以加速测试)
        interp, _ = run('return event_loop.sleep(0)\n')
        assert isinstance(interp.event_loop, AuroraEventLoop)

    def test_async_nested_await(self):
        _, result = run(
            'async fn base() { return 10 }\n'
            'async fn add_two() { let v = await base(); return v + 2 }\n'
            'return await add_two()\n')
        assert result == 12


# ════════════════════════════════════════════════════════════
# 6. defer —— Go 风格延迟执行
# ════════════════════════════════════════════════════════════

class TestDefer:

    def test_defer_lifo_order(self):
        _, result = run(
            'let log = []\n'
            'fn f() {\n'
            '  defer { log.append("first") }\n'
            '  defer { log.append("second") }\n'
            '  return 1\n'
            '}\n'
            'f()\n'
            'return log\n')
        assert result == ['second', 'first']

    def test_defer_runs_before_return(self):
        _, result = run(
            'var ran = false\n'
            'fn f() {\n'
            '  defer { ran = true }\n'
            '  return 1\n'
            '}\n'
            'f()\n'
            'return ran\n')
        assert result is True

    def test_defer_expr_call(self):
        _, result = run(
            'let log = []\n'
            'fn push(x) { log.append(x) }\n'
            'fn f() {\n'
            '  defer push(42)\n'
            '  return 1\n'
            '}\n'
            'f()\n'
            'return log\n')
        assert result == [42]

    def test_defer_runs_on_panic(self):
        _, result = run(
            'let log = []\n'
            'fn boom() {\n'
            '  defer { log.append("cleanup") }\n'
            '  panic("oops")\n'
            '}\n'
            'var outcome = "none"\n'
            'try { boom() } catch e { outcome = "caught" }\n'
            'return (outcome, log)\n')
        assert result == ('caught', ['cleanup'])


# ════════════════════════════════════════════════════════════
# 综合:多特性共存
# ════════════════════════════════════════════════════════════

class TestIntegration:

    def test_pub_async_cfg_together(self):
        interp, result = run(
            '#[cfg(target_os = "macos")]\n'
            'pub async fn fetch() { return 7 }\n'
            'return await fetch()\n')
        assert result == 7
        assert interp.export_table['fetch'] is True

    def test_extern_does_not_block(self):
        interp, _ = run(
            'extern "C" { fn getpid() -> i32; }\n'
            'pub fn real() { return 1 }\n')
        assert 'getpid' in interp.extern_registry
        assert interp.export_table['real'] is True
