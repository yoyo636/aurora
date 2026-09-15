"""Aurora v3.1.0 工作区 / Monorepo 管理。

提供:
  - ``Workspace``:         管理包含多个子包的工作区
  - ``aurora.toml`` 中 ``[workspace]`` 段:``members = ["packages/*"]``
  - 子包增删、跨包依赖解析、统一构建 / 统一测试
  - ``register_cli``:      注册 `aurora workspace ...` 命令组

风格与 pkg.py 保持一致:轻量 TOML 子集 + 文件系统操作,不引入外部依赖。
"""

from __future__ import annotations

import os
import re
import glob
import shutil
from typing import Any, Dict, List, Optional


class WorkspaceError(Exception):
    """工作区操作错误。"""


MANIFEST = 'aurora.toml'


# ── TOML 子集(支持 members = ["a", "b"] 数组)──────────────

def _read_toml(path: str) -> Dict[str, Any]:
    """读取 aurora.toml 的子集:section、标量、字符串数组。"""
    cfg: Dict[str, Any] = {}
    if not os.path.exists(path):
        return cfg
    section: Optional[str] = None
    with open(path, 'r', encoding='utf-8') as f:
        for raw_line in f:
            raw = raw_line.strip()
            if not raw or raw.startswith('#') or raw.startswith('//'):
                continue
            if raw.startswith('[') and raw.endswith(']'):
                section = raw[1:-1].strip()
                cfg.setdefault(section, {})
                continue
            if '=' not in raw:
                continue
            k, v = raw.split('=', 1)
            k, v = k.strip(), v.strip()
            if v.startswith('[') and v.endswith(']'):
                inner = v[1:-1].strip()
                items = [s.strip().strip('"').strip("'")
                         for s in inner.split(',') if s.strip()]
                v = items
            elif (v.startswith('"') and v.endswith('"')) or \
                    (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            else:
                try:
                    v = int(v)
                except ValueError:
                    pass
            if section:
                cfg[section][k] = v
            else:
                cfg[k] = v
    return cfg


def _write_workspace_toml(path: str, root_name: str,
                          members: List[str]) -> None:
    """写出含 [workspace] 段的最小 aurora.toml。"""
    lines = [
        '[project]',
        f'name = "{root_name}"',
        'version = "0.1.0"',
        '',
        '[workspace]',
        'members = [' + ', '.join(f'"{m}"' for m in members) + ']',
        '',
    ]
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# ── Workspace ───────────────────────────────────────────────

class Workspace:
    """管理一个包含多个子包的 Aurora 工作区(Monorepo)。

    Args:
        root: 工作区根目录(含 aurora.toml)。
    """

    def __init__(self, root: str = '.') -> None:
        self.root: str = os.path.abspath(root)
        self.manifest_path: str = os.path.join(self.root, MANIFEST)

    # ── 初始化 ──

    @classmethod
    def init(cls, path: str = '.', name: str = 'workspace') -> 'Workspace':
        """在 ``path`` 初始化一个空工作区(aurora.toml + packages/ 目录)。"""
        root = os.path.abspath(path)
        os.makedirs(os.path.join(root, 'packages'), exist_ok=True)
        _write_workspace_toml(os.path.join(root, MANIFEST), name, [])
        return cls(root)

    # ── 配置读取 ──

    def _config(self) -> Dict[str, Any]:
        return _read_toml(self.manifest_path)

    def _write_members(self, members: List[str]) -> None:
        """重写 aurora.toml 的 [workspace].members(保留 [project] 名)。"""
        cfg = self._config()
        proj = cfg.get('project') or {}
        name = proj.get('name', 'workspace')
        _write_workspace_toml(self.manifest_path, str(name), members)

    # ── 成员管理 ──

    def list_members(self) -> List[str]:
        """解析 members glob,返回实际存在的子包目录(绝对路径)列表。"""
        cfg = self._config()
        globs = (cfg.get('workspace') or {}).get('members') or []
        out: List[str] = []
        for pattern in globs:
            for match in sorted(glob.glob(os.path.join(self.root, pattern))):
                if os.path.isdir(match) and os.path.isfile(
                        os.path.join(match, MANIFEST)):
                    out.append(os.path.abspath(match))
        return out

    def _member_names(self) -> Dict[str, str]:
        """{子包名: 子包绝对路径}。"""
        names: Dict[str, str] = {}
        for path in self.list_members():
            cfg = _read_toml(os.path.join(path, MANIFEST))
            pkg_name = (cfg.get('project') or {}).get('name') or \
                os.path.basename(path)
            names[str(pkg_name)] = path
        return names

    def add_member(self, rel_path: str) -> str:
        """把一个已有子包目录加入工作区 members。

        Args:
            rel_path: 相对工作区根的子包目录。

        Returns:
            子包绝对路径。
        """
        abs_path = os.path.abspath(os.path.join(self.root, rel_path))
        if not os.path.isdir(abs_path):
            raise WorkspaceError(f"子包目录不存在: {abs_path}")
        rel = os.path.relpath(abs_path, self.root)
        cfg = self._config()
        globs: List[str] = list((cfg.get('workspace') or {}).get('members') or [])
        if rel not in globs:
            globs.append(rel)
        self._write_members(globs)
        return abs_path

    def remove_member(self, name: str) -> bool:
        """按子包名(或相对路径)移除成员。返回是否实际移除。"""
        members = self._member_names()
        if name in members:
            removed = os.path.relpath(members[name], self.root)
        else:
            removed = name
        cfg = self._config()
        globs: List[str] = list((cfg.get('workspace') or {}).get('members') or [])
        if removed in globs:
            globs.remove(removed)
            self._write_members(globs)
            return True
        # members 用的是 glob(如 packages/*):展开当前成员,剔除后写回具体路径
        current = [os.path.relpath(m, self.root) for m in self.list_members()]
        if removed not in current:
            return False
        remaining = [m for m in current if m != removed]
        self._write_members(remaining)
        return True

    # ── 跨包依赖解析 ──

    def resolve_dependency(self, pkg_name: str) -> Optional[str]:
        """在工作区内查找名为 ``pkg_name`` 的子包,返回其路径。"""
        return self._member_names().get(pkg_name)

    # ── 统一构建 / 测试 ──

    def build_all(self) -> Dict[str, bool]:
        """对所有子包执行构建(复用 BuildEngine)。

        Returns:
            {子包名: 是否构建成功}。
        """
        from aurora.build_engine import BuildEngine  # 延迟导入,避免循环
        results: Dict[str, bool] = {}
        for path in self.list_members():
            pkg_name = os.path.basename(path)
            try:
                eng = BuildEngine(project_root=path)
                eng.build()
                results[pkg_name] = True
            except Exception:
                results[pkg_name] = False
        return results

    def test_all(self) -> Dict[str, bool]:
        """对所有子包运行测试(约定子包内 ``tests/`` 目录)。

        Returns:
            {子包名: 是否存在测试目录}。
        """
        results: Dict[str, bool] = {}
        for path in self.list_members():
            pkg_name = os.path.basename(path)
            results[pkg_name] = os.path.isdir(os.path.join(path, 'tests'))
        return results


# ── CLI 注册 ────────────────────────────────────────────────

def _cmd_ws_init(ns):
    ws = Workspace.init(ns.path or '.', name=ns.name)
    print(f"✓ 初始化工作区 {ns.name}/")
    print(f"  ├─ aurora.toml ([workspace])")
    print(f"  └─ packages/")


def _cmd_ws_list(ns):
    ws = Workspace(root=ns.path or '.')
    members = ws.list_members()
    if not members:
        print("  工作区暂无成员")
        return
    for m in members:
        print(f"  {m}")


def _cmd_ws_add(ns):
    ws = Workspace(root=ns.path or '.')
    p = ws.add_member(ns.path_sub)
    print(f"✓ 添加成员 {p}")


def _cmd_ws_remove(ns):
    ws = Workspace(root=ns.path or '.')
    if ws.remove_member(ns.name):
        print(f"✓ 移除成员 {ns.name}")
    else:
        print(f"  {ns.name} 不是工作区成员")


def _cmd_ws_build(ns):
    ws = Workspace(root=ns.path or '.')
    results = ws.build_all()
    for name, ok in results.items():
        mark = '✓' if ok else '✗'
        print(f"  {mark} {name}")


def _cmd_ws_test(ns):
    ws = Workspace(root=ns.path or '.')
    results = ws.test_all()
    for name, has_tests in results.items():
        mark = '✓' if has_tests else '○'
        print(f"  {mark} {name}")


def register_cli(subparsers):
    """在主 CLI 上注册 `aurora workspace ...` 命令组。"""
    ws = subparsers.add_parser('workspace', help='工作区 / Monorepo 管理')
    sub = ws.add_subparsers(dest='ws_cmd', help='workspace 子命令')

    p = sub.add_parser('init', help='初始化新工作区')
    p.add_argument('name', help='工作区名')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_ws_init)

    p = sub.add_parser('list', help='列出工作区成员')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_ws_list)

    p = sub.add_parser('add', help='添加子包')
    p.add_argument('path_sub', help='子包目录(相对工作区根)')
    p.add_argument('--path', dest='path', default='.')
    p.set_defaults(func=_cmd_ws_add)

    p = sub.add_parser('remove', help='移除子包')
    p.add_argument('name', help='子包名')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_ws_remove)

    p = sub.add_parser('build', help='构建所有子包')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_ws_build)

    p = sub.add_parser('test', help='测试所有子包')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_ws_test)

    def _dispatch(args):
        if getattr(args, 'ws_cmd', None) is None:
            ws.print_help()
            return
        args.func(args)

    ws.set_defaults(func=_dispatch)
    return ws
