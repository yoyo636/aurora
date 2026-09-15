"""Aurora v3.1.0 模块化系统核心。

提供与 Rust / ES Modules / Python import 对齐的模块基础设施:

  - ``Module``:               一个编译单元(文件即模块,或 ``module math { ... }`` 块)
  - ``ImportResolver``:       node_modules 风格的导入解析
                              (当前目录 → ``aurora_modules/`` → 标准库 → 全局路径)
  - ``ModuleRegistry``:       全局注册表:加载 / 缓存 / 查询模块
  - ``detect_cycles``:        编译期循环依赖检测(DFS)

支持的导入语法(源码层面):
  - ``import std.math``
  - ``import std.math as math2``
  - ``from std.math import add, sub``
  - ``module math { export fn add() {} }``(块级模块,当前作为命名标记处理)

可见性:``pub`` 关键字(或 ``export``)标记公开符号,其余为模块私有,
外部模块不可见。

本模块只做静态的符号/依赖提取与解析,不依赖词法/语法分析器,
保持与 pkg.py 相同的轻量风格,便于在构建期独立使用。
"""

from __future__ import annotations

import os
import re
from typing import Dict, List, Optional, Set, Tuple


# ── 源码级静态提取 ────────────────────────────────────────────

#: 匹配顶层符号定义:可选 ``pub``,再可选 ``export``,后跟 fn/struct/enum/const
_SYMBOL_RE = re.compile(
    r'^\s*(?P<pub>pub\s+)?(?P<export>export\s+)?'
    r'(?:fn|struct|enum|const|let|type)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)',
    re.MULTILINE,
)

#: ``import a.b.c`` 或 ``import a.b.c as alias``
_IMPORT_RE = re.compile(
    r'^\s*import\s+(?P<path>[A-Za-z_][A-Za-z0-9_.]*)'
    r'(?:\s+as\s+(?P<alias>[A-Za-z_][A-Za-z0-9_]*))?\s*$',
    re.MULTILINE,
)

#: ``from a.b.c import x, y, z``
_FROM_IMPORT_RE = re.compile(
    r'^\s*from\s+(?P<path>[A-Za-z_][A-Za-z0-9_.]*)\s+import\s+'
    r'(?P<names>[^#\n]+?)\s*$',
    re.MULTILINE,
)

#: 块级模块声明 ``module math { ... }``(取模块名,体在文件内展开)
_MODULE_DECL_RE = re.compile(
    r'^\s*module\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)',
    re.MULTILINE,
)


class ModuleError(Exception):
    """模块系统错误(解析失败、循环依赖、越权访问等)。"""


class CyclicDependencyError(ModuleError):
    """编译期检测到循环依赖。"""


class VisibilityError(ModuleError):
    """访问了模块私有(非 pub)符号。"""


# ── Module ──────────────────────────────────────────────────

class Module:
    """表示一个 Aurora 模块。

    Attributes:
        name:     全限定模块名,如 ``std.math``(文件即模块时由路径推导)。
        path:     模块对应的源文件绝对路径(内存模块可为 ``<builtin:xxx>``)。
        source:   模块原始源码文本。
        exports:  公开符号名集合(``pub`` / ``export`` 标记)。
        private:  模块私有符号名集合。
        deps:     本模块直接依赖的模块名列表(去重、保持声明顺序)。
        aliases:  ``import x as y`` 形式的别名映射 {alias: module}。
        reexports: ``from a import b`` 导入的符号 {symbol: source_module}。
    """

    def __init__(
        self,
        name: str,
        path: str = '',
        source: str = '',
        exports: Optional[Set[str]] = None,
        private: Optional[Set[str]] = None,
        deps: Optional[List[str]] = None,
    ) -> None:
        self.name: str = name
        self.path: str = path
        self.source: str = source
        self.exports: Set[str] = set(exports or ())
        self.private: Set[str] = set(private or ())
        self.deps: List[str] = list(deps or [])
        self.aliases: Dict[str, str] = {}
        self.reexports: Dict[str, str] = {}

    # ── 静态提取 ──

    @staticmethod
    def extract_symbols(source: str) -> Tuple[Set[str], Set[str]]:
        """从源码中提取 (公开符号集, 私有符号集)。

        ``pub`` 或 ``export``(或两者)修饰的符号计入 exports,否则计入 private。
        """
        exported: Set[str] = set()
        private: Set[str] = set()
        for m in _SYMBOL_RE.finditer(source):
            name = m.group('name')
            is_pub = bool(m.group('pub') or m.group('export'))
            (exported if is_pub else private).add(name)
        return exported, private

    @staticmethod
    def extract_imports(source: str) -> List[Tuple[str, List[str], Optional[str]]]:
        """提取源码中的导入语句。

        Returns:
            三元组列表 ``(module_path, imported_names, alias)``:
              - ``import a.b``          → ('a.b', [], None)
              - ``import a.b as c``     → ('a.b', [], 'c')
              - ``from a.b import x,y`` → ('a.b', ['x', 'y'], None)
        """
        out: List[Tuple[str, List[str], Optional[str]]] = []
        for m in _IMPORT_RE.finditer(source):
            out.append((m.group('path'), [], m.group('alias')))
        for m in _FROM_IMPORT_RE.finditer(source):
            names = [n.strip() for n in m.group('names').split(',') if n.strip()]
            out.append((m.group('path'), names, None))
        return out

    @classmethod
    def from_source(cls, name: str, source: str, path: str = '') -> 'Module':
        """从源码文本构建 Module(自动提取符号与导入依赖)。"""
        exports, private = cls.extract_symbols(source)
        deps: List[str] = []
        mod = cls(name=name, path=path, source=source,
                  exports=exports, private=private)
        for imp_path, names, alias in cls.extract_imports(source):
            if imp_path not in deps:
                deps.append(imp_path)
            if alias:
                mod.aliases[alias] = imp_path
            for n in names:
                mod.reexports[n] = imp_path
        mod.deps = deps
        return mod

    # ── 可见性 ──

    def is_exported(self, symbol: str) -> bool:
        """``symbol`` 是否为本模块公开符号。"""
        return symbol in self.exports

    def lookup(self, symbol: str) -> str:
        """按可见性解析本模块内的符号。

        Returns:
            若符号公开,返回其名字(调用方可通过模块限定访问)。

        Raises:
            VisibilityError: 符号是模块私有的。
        """
        if symbol in self.exports:
            return symbol
        if symbol in self.private or symbol in self.reexports:
            raise VisibilityError(
                f"模块 '{self.name}' 的符号 '{symbol}' 不是 pub,外部不可访问")
        raise VisibilityError(
            f"模块 '{self.name}' 中不存在符号 '{symbol}'")

    def __repr__(self) -> str:  # pragma: no cover - 调试用
        return (f"Module(name={self.name!r}, exports={sorted(self.exports)}, "
                f"deps={self.deps})")


# ── ImportResolver ──────────────────────────────────────────

class ImportResolver:
    """node_modules 风格的导入解析器。

    解析顺序(对给定模块名 ``std.math``):
      1. 当前模块所在目录(相对导入): ``./std/math.aur``
      2. 项目内 ``aurora_modules/<name>/...``(node_modules 镜像)
      3. 标准库搜索路径
      4. 额外的全局搜索路径

    一个模块名 ``a.b.c`` 会被映射成候选文件:
      - ``a/b/c.aur``
      - ``a/b/c/index.aur``
    """

    #: 项目内镜像 node_modules 的目录名
    VENDOR_DIR = 'aurora_modules'
    #: 源文件扩展名
    EXT = '.aur'

    def __init__(self, search_paths: Optional[List[str]] = None,
                 stdlib_paths: Optional[List[str]] = None) -> None:
        self.search_paths: List[str] = [os.path.abspath(p) for p in (search_paths or [])]
        self.stdlib_paths: List[str] = [os.path.abspath(p) for p in (stdlib_paths or [])]

    # ── 候选文件 ──

    @staticmethod
    def _candidates(modname: str) -> List[str]:
        """把点分隔模块名展开为相对路径候选。"""
        rel = modname.replace('.', os.sep)
        return [
            rel + ImportResolver.EXT,
            os.path.join(rel, 'index' + ImportResolver.EXT),
        ]

    def resolve(self, modname: str, current_module_path: str = '') -> Optional[str]:
        """把模块名解析为源文件绝对路径;找不到返回 None。

        Args:
            modname:             点分隔模块名,如 ``std.math``。
            current_module_path: 发起导入的模块文件路径(用于相对查找)。
        """
        candidates = self._candidates(modname)

        # 1) 当前目录 / 当前模块所在目录
        bases: List[str] = [os.getcwd()]
        if current_module_path:
            bases.append(os.path.dirname(os.path.abspath(current_module_path)))
        # 2) aurora_modules 镜像目录
        for base in list(bases):
            bases.append(os.path.join(base, self.VENDOR_DIR))
        # 3) 标准库
        bases.extend(self.stdlib_paths)
        # 4) 额外搜索路径
        bases.extend(self.search_paths)

        for base in bases:
            for cand in candidates:
                full = os.path.normpath(os.path.join(base, cand))
                if os.path.isfile(full):
                    return full
        return None

    def module_name_from_path(self, path: str, root: str) -> str:
        """把文件路径反推成点分隔模块名(相对 root)。

        例如 ``root/std/math.aur`` → ``std.math``;
        ``root/std/math/index.aur`` → ``std.math``。
        """
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root))
        rel = rel.replace(os.sep, '/')
        if rel.endswith('/index.aur'):
            rel = rel[:-len('/index.aur')]
        elif rel.endswith('.aur'):
            rel = rel[:-len('.aur')]
        return rel.replace('/', '.')


# ── ModuleRegistry ───────────────────────────────────────────

class ModuleRegistry:
    """全局模块注册表:加载、缓存、查询模块。

    负责按解析路径加载源文件、缓存 Module 对象、维护模块依赖边,
    并对外提供统一的导入入口。
    """

    def __init__(self, resolver: Optional[ImportResolver] = None) -> None:
        self.resolver: ImportResolver = resolver or ImportResolver()
        self._modules: Dict[str, Module] = {}

    # ── 注册 / 查询 ──

    def register(self, module: Module) -> None:
        """直接注册一个已构建的模块(内存模块或测试桩)。"""
        self._modules[module.name] = module

    def get(self, name: str) -> Optional[Module]:
        """按名查询已加载模块(未加载返回 None)。"""
        return self._modules.get(name)

    def all(self) -> Dict[str, Module]:
        """返回 {模块名: Module} 副本。"""
        return dict(self._modules)

    def has(self, name: str) -> bool:
        return name in self._modules

    # ── 加载 ──

    def load_file(self, path: str, name: Optional[str] = None,
                   root: Optional[str] = None) -> Module:
        """从磁盘加载一个 .aur 文件并注册。

        Args:
            path: 源文件路径。
            name: 显式模块名(缺省由路径推导)。
            root: 推导模块名时的根目录(缺省用文件所在目录)。
        """
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        if name is None:
            root = root or os.path.dirname(os.path.abspath(path))
            name = self.resolver.module_name_from_path(path, root)
        mod = Module.from_source(name, source, path=os.path.abspath(path))
        self._modules[name] = mod
        return mod

    def load_module(self, name: str,
                    search_paths: Optional[List[str]] = None) -> Module:
        """按模块名加载(带缓存)。找不到抛 ModuleError。"""
        if name in self._modules:
            return self._modules[name]
        if search_paths:
            self.resolver.search_paths.extend(
                os.path.abspath(p) for p in search_paths)
        path = self.resolver.resolve(name)
        if path is None:
            raise ModuleError(f"无法解析模块 '{name}':搜索路径 {self.resolver.search_paths}")
        return self.load_file(path, name=name)

    # ── 导入语句解析 ──

    def resolve_import(self, import_stmt: str,
                       current_module: Optional[Module] = None) -> Module:
        """解析一条导入语句文本,返回目标 Module(并完成加载)。

        支持:``import a.b``、``import a.b as c``、``from a.b import x``。
        """
        stmt = import_stmt.strip().rstrip(';')
        m = _IMPORT_RE.match(stmt + '\n')
        if m:
            path = m.group('path')
        else:
            m = _FROM_IMPORT_RE.match(stmt + '\n')
            if m:
                path = m.group('path')
            else:
                raise ModuleError(f"无法识别的导入语句: {import_stmt!r}")
        cur_path = current_module.path if current_module else ''
        resolved = self.resolver.resolve(path, current_module_path=cur_path)
        if resolved is None:
            raise ModuleError(f"导入失败:无法定位模块 '{path}'")
        return self.load_file(resolved, name=path)


# ── 顶层便捷函数 ─────────────────────────────────────────────

def load_module(name: str, search_paths: Optional[List[str]] = None,
                registry: Optional[ModuleRegistry] = None) -> Module:
    """加载模块(顶层便捷函数,使用独立注册表时可传入)。"""
    reg = registry or ModuleRegistry()
    return reg.load_module(name, search_paths=search_paths)


def resolve_import(import_stmt: str, current_module: Optional[Module] = None,
                   registry: Optional[ModuleRegistry] = None) -> Module:
    """解析导入语句(顶层便捷函数)。"""
    reg = registry or ModuleRegistry()
    return reg.resolve_import(import_stmt, current_module)


def detect_cycles(modules: Dict[str, Module]) -> List[List[str]]:
    """对模块图做 DFS 环检测。

    Args:
        modules: {模块名: Module}。

    Returns:
        找到的环列表,每个环是按访问顺序排列的模块名列表
        (首尾相同,如 ``['a', 'b', 'a']``);无环时返回 []。
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[str, int] = {name: WHITE for name in modules}
    cycles: List[List[str]] = []
    stack: List[str] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        stack.append(node)
        mod = modules.get(node)
        for dep in (mod.deps if mod else []):
            if dep not in modules:
                continue  # 外部依赖不参与环检测
            if color[dep] == GRAY:
                idx = stack.index(dep)
                cycle = stack[idx:] + [dep]
                cycles.append(cycle)
            elif color[dep] == WHITE:
                dfs(dep)
        stack.pop()
        color[node] = BLACK

    for name in modules:
        if color[name] == WHITE:
            dfs(name)
    return cycles


def assert_no_cycles(modules: Dict[str, Module]) -> None:
    """若存在循环依赖,抛出 CyclicDependencyError(带环路径)。"""
    cycles = detect_cycles(modules)
    if cycles:
        rendered = ' ; '.join(' → '.join(c) for c in cycles)
        raise CyclicDependencyError(f"检测到循环依赖: {rendered}")


# ── CLI 注册 ────────────────────────────────────────────────

def _cmd_modules_list(ns):
    """``aurora modules list``:列出已加载缓存中的模块(演示/调试用)。"""
    reg = ModuleRegistry()
    # 扫描 --path 下的 .aur 文件作为可发现模块
    root = getattr(ns, 'path', '.') or '.'
    found = []
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            if fn.endswith('.aur'):
                found.append(os.path.join(dirpath, fn))
    if not found:
        print("  未发现 .aur 模块文件")
        return
    for f in sorted(found):
        print(f"  {f}")


def register_cli(subparsers):
    """在主 CLI 上注册 `aurora modules ...` 命令组。"""
    mp = subparsers.add_parser('modules', help='模块化系统(模块加载 / 导入解析 / 环检测)')
    sub = mp.add_subparsers(dest='modules_cmd', help='modules 子命令')

    p = sub.add_parser('list', help='列出目录下可发现的 .aur 模块')
    p.add_argument('--path', default='.', help='扫描根目录(默认当前目录)')
    p.set_defaults(func=_cmd_modules_list)

    def _dispatch(args):
        if getattr(args, 'modules_cmd', None) is None:
            mp.print_help()
            return
        args.func(args)

    mp.set_defaults(func=_dispatch)
    return mp
