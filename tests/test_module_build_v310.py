"""Aurora v3.1.0 模块化系统与构建基础设施测试。

覆盖:
  - module_system:     模块加载 / 导入解析 / 循环依赖检测 / pub 可见性
  - build_engine:      条件编译评估 / 多入口 / 资源打包 / 增量构建 /
                        compile_commands.json 生成
  - workspace_manager: 工作区初始化 / 成员管理 / 统一构建
  - dep_graph:         图构建 / 传递依赖 / 冲突检测 / DOT & Mermaid 输出
"""

import json
import os

import pytest

from aurora.module_system import (
    Module, ImportResolver, ModuleRegistry,
    detect_cycles, assert_no_cycles,
    CyclicDependencyError, VisibilityError, ModuleError,
)
from aurora.build_engine import CfgEvaluator, BuildEngine
from aurora.workspace_manager import Workspace
from aurora.dep_graph import DependencyGraph


# ── 临时项目骨架工具 ──────────────────────────────────────────

def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return path


# ══ module_system ══════════════════════════════════════════

class TestModuleSystem:

    def test_module_load_and_exports(self, tmp_path):
        """文件即模块:加载后应正确提取 pub / 私有符号。"""
        src = _write(str(tmp_path / "math.aur"),
                     'pub fn add(a, b) { return a + b }\n'
                     'fn internal(x) { return x }\n'
                     'pub const VERSION = "1.0"\n')
        mod = Module.from_source('math', open(src).read(), path=src)
        assert 'add' in mod.exports
        assert 'VERSION' in mod.exports
        assert 'internal' in mod.private
        assert mod.is_exported('add')
        assert not mod.is_exported('internal')

    def test_import_resolution_order(self, tmp_path):
        """ImportResolver:当前目录 → aurora_modules → 标准库路径。"""
        # 标准库路径下放 std/math.aur
        stdlib = tmp_path / "stdlib"
        _write(str(stdlib / "std" / "math.aur"),
               'pub fn add(a, b) { return a + b }\n')
        # 项目目录下放另一个同名模块,当前目录优先
        proj = tmp_path / "proj"
        _write(str(proj / "std" / "math.aur"),
               'pub fn local_marker() {}\n')
        resolver = ImportResolver(stdlib_paths=[str(stdlib)])

        here = resolver.resolve('std.math', current_module_path=str(proj / "main.aur"))
        assert here == os.path.abspath(str(proj / "std" / "math.aur"))

        # 换到一个不含 std/math 的目录,应落到标准库
        other = tmp_path / "other"
        os.makedirs(str(other / "src"), exist_ok=True)
        there = resolver.resolve('std.math', current_module_path=str(other / "src" / "x.aur"))
        assert there == os.path.abspath(str(stdlib / "std" / "math.aur"))

    def test_registry_load_and_resolve_import(self, tmp_path):
        """ModuleRegistry 缓存 + resolve_import 支持三种语法。"""
        _write(str(tmp_path / "std" / "math.aur"),
               'pub fn add(a, b) { return a + b }\n')
        reg = ModuleRegistry(ImportResolver(search_paths=[str(tmp_path)]))

        m1 = reg.resolve_import('import std.math', current_module=None)
        assert m1.name == 'std.math'
        # 二次加载走缓存
        m1b = reg.load_module('std.math')
        assert m1b is m1

        m2 = reg.resolve_import('from std.math import add')
        # from-import 解析到的目标模块应公开 add
        assert 'add' in m2.exports
        # 源码级提取:模块里写了 from X import y 时记录 reexports
        src_mod = Module.from_source('user', 'from std.math import add\nimport std.math as sm\n')
        assert src_mod.reexports == {'add': 'std.math'}
        assert src_mod.aliases == {'sm': 'std.math'}

        with pytest.raises(ModuleError):
            reg.resolve_import('import no.such.module')

    def test_cyclic_dependency_detection(self):
        """A→B→A 应被 DFS 检测为环。"""
        a = Module('a', deps=['b'])
        b = Module('b', deps=['a'])
        cycles = detect_cycles({'a': a, 'b': b})
        assert cycles, "应检测到 a↔b 环"
        flat = set(cycles[0])
        assert {'a', 'b'} <= flat

        # 无环图
        ok = detect_cycles({'a': Module('a', deps=['b']),
                            'b': Module('b', deps=[])})
        assert ok == []

        # assert_no_cycles 抛异常
        with pytest.raises(CyclicDependencyError):
            assert_no_cycles({'a': a, 'b': b})

    def test_pub_visibility(self):
        """非 pub 符号外部访问必须抛 VisibilityError。"""
        mod = Module('math', exports={'add'}, private={'internal'})
        assert mod.lookup('add') == 'add'
        with pytest.raises(VisibilityError):
            mod.lookup('internal')
        with pytest.raises(VisibilityError):
            mod.lookup('ghost')


# ══ build_engine ═══════════════════════════════════════════

class TestBuildEngine:

    def test_cfg_evaluator_expressions(self):
        """条件编译:target_os / feature / not / and / or 组合。"""
        ev = CfgEvaluator({
            'target_os': 'macos',
            'target_arch': 'arm64',
            'features': {'gui', 'debug'},
        })
        assert ev.evaluate('target_os = "macos"') is True
        assert ev.evaluate('target_os = "windows"') is False
        assert ev.evaluate('target_arch = "arm64"') is True
        assert ev.evaluate('feature = "gui"') is True
        assert ev.evaluate('feature = "cli"') is False
        assert ev.evaluate('not(target_os = "windows")') is True
        assert ev.evaluate('and(target_os = "macos", feature = "gui")') is True
        assert ev.evaluate('and(target_os = "macos", feature = "cli")') is False
        assert ev.evaluate('or(feature = "gui", feature = "cli")') is True
        # 空条件恒真
        assert ev.evaluate('') is True

    def test_cfg_source_filtering(self):
        """filter_source 按条件裁剪行级 cfg 标注。"""
        src = (
            'pub fn main() {}\n'
            '#[cfg(target_os = "macos")]\n'
            'fn mac_only() {}\n'
            '#[cfg(target_os = "windows")]\n'
            'fn win_only() {}\n'
        )
        mac = CfgEvaluator({'target_os': 'macos'})
        out = mac.filter_source(src)
        assert 'mac_only' in out
        assert 'win_only' not in out

    def test_multi_entry_and_resource_packaging(self, tmp_path):
        """多入口构建 + 资源文件复制到 dist/。"""
        _write(str(tmp_path / "src" / "main.aur"), 'pub fn main() {}\n')
        _write(str(tmp_path / "src" / "cli.aur"), 'pub fn cli() {}\n')
        _write(str(tmp_path / "assets" / "logo.png"), '\x89PNG fake')
        _write(str(tmp_path / "config.toml"), 'name = "demo"\n')

        eng = BuildEngine(project_root=str(tmp_path))
        result = eng.build({
            'entries': ['src/main.aur', 'src/cli.aur'],
            'resources': ['assets', 'config.toml'],
        })
        assert set(result['all_entries']) == {'src/main.aur', 'src/cli.aur'}
        # 产物落盘
        assert os.path.isfile(str(tmp_path / "dist" / "src" / "main.auro"))
        assert os.path.isfile(str(tmp_path / "dist" / "src" / "cli.auro"))
        # 资源复制
        assert os.path.isfile(str(tmp_path / "dist" / "assets" / "logo.png"))
        assert os.path.isfile(str(tmp_path / "dist" / "config.toml"))

    def test_incremental_build(self, tmp_path):
        """未变更文件第二次构建应被增量跳过。"""
        entry = _write(str(tmp_path / "src" / "main.aur"), 'pub fn main() {}\n')
        eng = BuildEngine(project_root=str(tmp_path))
        r1 = eng.build({'entries': ['src/main.aur']})
        assert r1['changed'] == ['src/main.aur']

        # 内容未变 → 增量跳过
        r2 = eng.build({'entries': ['src/main.aur']})
        assert r2['changed'] == []
        assert r2['incremental_skipped'] == 1

        # 修改文件 → 重新构建
        with open(entry, 'a') as f:
            f.write('fn second() {}\n')
        r3 = eng.build({'entries': ['src/main.aur']})
        assert r3['changed'] == ['src/main.aur']

    def test_compile_commands_generation(self, tmp_path):
        """构建后应生成 compile_commands.json(LSP 可用)。"""
        _write(str(tmp_path / "src" / "main.aur"), 'pub fn main() {}\n')
        eng = BuildEngine(project_root=str(tmp_path))
        eng.build({'entries': ['src/main.aur']})
        db_path = str(tmp_path / "build" / "compile_commands.json")
        assert os.path.isfile(db_path)
        with open(db_path) as f:
            db = json.load(f)
        assert isinstance(db, list)
        assert db and db[0]['file'].endswith('main.aur')
        assert 'command' in db[0]

    def test_clean(self, tmp_path):
        """clean 应删除 dist/ 与 build/。"""
        _write(str(tmp_path / "src" / "main.aur"), 'pub fn main() {}\n')
        eng = BuildEngine(project_root=str(tmp_path))
        eng.build({'entries': ['src/main.aur']})
        assert os.path.isdir(str(tmp_path / "dist"))
        eng.clean()
        assert not os.path.exists(str(tmp_path / "dist"))
        assert not os.path.exists(str(tmp_path / "build"))


# ══ workspace_manager ═══════════════════════════════════════

class TestWorkspace:

    def test_workspace_init_and_member_management(self, tmp_path):
        """init → add_member → list_members → remove_member。"""
        root = tmp_path / "mono"
        ws = Workspace.init(str(root), name='mono')

        # 建两个子包
        for name in ('pkg-a', 'pkg-b'):
            _write(str(root / "packages" / name / "aurora.toml"),
                  f'[project]\nname = "{name}"\nversion = "0.1.0"\n')
            _write(str(root / "packages" / name / "src" / "lib.aur"),
                   'pub fn lib() {}\n')

        # members 用 glob
        ws._write_members(['packages/*'])

        members = ws.list_members()
        assert len(members) == 2
        assert all(os.path.isdir(m) for m in members)

        # 跨包依赖解析
        resolved = ws.resolve_dependency('pkg-a')
        assert resolved is not None and resolved.endswith('pkg-a')

        # 移除
        assert ws.remove_member('pkg-a') is True
        assert len(ws.list_members()) == 1
        assert ws.remove_member('pkg-a') is False

    def test_workspace_add_member(self, tmp_path):
        """add_member 把已有目录登记进 members。"""
        root = tmp_path / "mono2"
        ws = Workspace.init(str(root), name='mono2')
        _write(str(root / "packages" / "pkg-c" / "aurora.toml"),
              '[project]\nname = "pkg-c"\nversion = "0.1.0"\n')
        abs_pkg = ws.add_member('packages/pkg-c')
        assert abs_pkg.endswith('pkg-c')
        members = [os.path.basename(m) for m in ws.list_members()]
        assert 'pkg-c' in members

    def test_workspace_build_all(self, tmp_path):
        """build_all 应构建工作区内全部子包。"""
        root = tmp_path / "mono3"
        ws = Workspace.init(str(root), name='mono3')
        for name in ('a', 'b'):
            _write(str(root / "packages" / name / "aurora.toml"),
                  f'[project]\nname = "{name}"\n')
            _write(str(root / "packages" / name / "src" / "main.aur"),
                   'pub fn main() {}\n')
        ws._write_members(['packages/*'])
        results = ws.build_all()
        assert results == {'a': True, 'b': True}
        # 产物落盘到各子包 dist/
        assert os.path.isfile(str(root / "packages" / "a" / "dist" / "src" / "main.auro"))


# ══ dep_graph ═══════════════════════════════════════════════

class TestDepGraph:

    def _graph(self):
        return DependencyGraph().build({
            'app':  {'version': '1.0.0', 'deps': {'lib': '^1.0.0', 'util': '1.0.0'}},
            'lib':  {'version': '1.2.0', 'deps': {'util': '^1.0.0'}},
            'util': {'version': '1.1.0', 'deps': {}},
        })

    def test_build_and_nodes(self):
        g = self._graph()
        assert set(g.nodes()) == {'app', 'lib', 'util'}
        assert ('app', 'lib') in g.edges()
        assert ('lib', 'util') in g.edges()

    def test_transitive_deps(self):
        g = self._graph()
        td = g.transitive_deps('app')
        # app → lib, util;lib → util(去重)
        assert set(td) == {'lib', 'util'}
        assert g.transitive_deps('lib') == ['util']
        assert g.transitive_deps('util') == []
        with pytest.raises(Exception):
            g.transitive_deps('ghost')

    def test_conflict_detection(self):
        """同一包被两个上游以不兼容约束引用 → 冲突。"""
        g = DependencyGraph().build({
            'app': {'version': '1.0.0', 'deps': {'lib': '^2.0.0'}},
            'cli': {'version': '1.0.0', 'deps': {'lib': '~1.0.0'}},
            'lib': {'version': '1.5.0', 'deps': {}},   # 不满足 ^2.0.0
        })
        conflicts = g.detect_conflicts()
        assert conflicts, '应检测到 lib 版本冲突'
        assert conflicts[0]['package'] == 'lib'
        assert set(conflicts[0]['required_by']) == {'app', 'cli'}

        # 无冲突图
        ok = DependencyGraph().build({
            'app': {'version': '1.0.0', 'deps': {'lib': '^1.0.0'}},
            'lib': {'version': '1.2.0', 'deps': {}},
        })
        assert ok.detect_conflicts() == []

    def test_unused_detection(self):
        g = DependencyGraph().build({
            'app': {'version': '1.0.0',
                    'deps': {'lib': '1.0.0', 'unused-lib': '1.0.0'}},
            'lib': {'version': '1.0.0', 'deps': {}},
            'unused-lib': {'version': '1.0.0', 'deps': {}},
        })
        unused = g.detect_unused({'app': {'lib'}})
        assert unused.get('app') == ['unused-lib']

    def test_dot_and_mermaid(self):
        g = self._graph()
        dot = g.to_dot()
        assert dot.startswith('digraph')
        assert 'app -> lib' in dot.replace('"', '') or 'app ->' in dot
        mermaid = g.to_mermaid()
        assert mermaid.startswith('graph LR')
        assert ' --> ' in mermaid


# ══ CLI 注册自检 ═══════════════════════════════════════════

class TestCliRegistration:

    def test_register_cli_callable(self):
        """四个模块都应提供 register_cli 且可挂到 argparse。"""
        import argparse
        from aurora.module_system import register_cli as reg_mod
        from aurora.build_engine import register_cli as reg_build
        from aurora.workspace_manager import register_cli as reg_ws
        from aurora.dep_graph import register_cli as reg_deps

        parser = argparse.ArgumentParser()
        subs = parser.add_subparsers()
        reg_mod(subs)
        reg_build(subs)
        reg_ws(subs)
        reg_deps(subs)
        ns = parser.parse_args(['deps'])
        assert hasattr(ns, 'func')
