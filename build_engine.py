"""Aurora v3.1.0 构建系统增强。

提供:
  - ``CfgEvaluator``:     ``#[cfg(target_os = "macos")]`` 条件编译属性求值
  - ``BuildEngine``:      完整构建流程编排:多入口 / 资源打包 / 构建脚本钩子 /
                          增量构建(文件哈希 + 依赖图)/ compile_commands.json 生成
  - CLI:                  ``aurora build ...``(多入口、清理、生成编译数据库)

设计原则与 pkg.py 一致:不依赖外部工具链,所有"编译"动作以确定性的
文件落盘/哈希记录表示,便于在 CI 与测试中复现。
"""

from __future__ import annotations

import os
import re
import json
import shutil
import hashlib
import platform
from typing import Any, Dict, List, Optional, Set


class BuildError(Exception):
    """构建过程错误。"""


# ── 条件编译 ────────────────────────────────────────────────

class CfgEvaluator:
    """评估 ``#[cfg(...)]`` 条件编译属性。

    支持的谓词:
      - ``target_os = "macos"`` / ``target_arch = "x86_64"``
      - ``feature = "gui"``
      - ``not(...)``、``and(...)``、``or(...)``(可嵌套)

    Example:
        >>> ctx = {"target_os": "macos", "target_arch": "arm64",
        ...        "features": {"gui", "debug"}}
        >>> ev = CfgEvaluator(ctx)
        >>> ev.evaluate('target_os = "macos"')
        True
        >>> ev.evaluate('and(target_os = "macos", feature = "cli")')
        False
        >>> ev.evaluate('or(feature = "gui", feature = "cli")')
        True
        >>> ev.evaluate('not(target_os = "windows")')
        True
    """

    def __init__(self, context: Optional[Dict[str, Any]] = None) -> None:
        #: 求值上下文:``target_os`` / ``target_arch`` 为标量,``features`` 为集合
        self.context: Dict[str, Any] = dict(context or {})
        self.context.setdefault('target_os', platform.system().lower())
        self.context.setdefault('target_arch', platform.machine().lower())
        self.context.setdefault('features', set())

    # ── token 级解析 ──

    @staticmethod
    def _tokenize(expr: str) -> List[str]:
        """把 cfg 表达式切成 token:括号、标识符、字符串、=。"""
        tokens = re.findall(r'\s*(?:\(|\)|[A-Za-z_][A-Za-z0-9_]*|"[^"]*"|=)', expr)
        return [t.strip() for t in tokens if t.strip()]

    def _parse_primary(self, tokens: List[str], i: int) -> (bool, int):
        """解析一个 primary 表达式,返回 (布尔值, 新下标)。"""
        tok = tokens[i]
        if tok == 'not':
            # not(inner)
            assert tokens[i + 1] == '(', "cfg: not 后必须跟 ("
            val, j = self._parse(tokens, i + 2)
            assert tokens[j] == ')', "cfg: not 缺少 )"
            return (not val), j + 1
        if tok in ('and', 'or'):
            assert tokens[i + 1] == '(', f"cfg: {tok} 后必须跟 ("
            op = tok
            j = i + 2
            results: List[bool] = []
            while tokens[j] != ')':
                v, j = self._parse(tokens, j)
                results.append(v)
                if tokens[j] == ',':
                    j += 1
            combined = results[0]
            for r in results[1:]:
                combined = (combined and r) if op == 'and' else (combined or r)
            return combined, j + 1
        # 普通谓词: name = "value"
        assert tok in ('target_os', 'target_arch', 'feature'), \
            f"cfg: 未知谓词 '{tok}'"
        assert tokens[i + 1] == '=', "cfg: 谓词后需 = \"...\""
        literal = tokens[i + 2].strip('"')
        if tok == 'feature':
            result = literal in (self.context.get('features') or set())
        else:
            result = self.context.get(tok) == literal
        return result, i + 3

    def _parse(self, tokens: List[str], i: int) -> (bool, int):
        if tokens[i] == '(':
            v, j = self._parse(tokens, i + 1)
            assert tokens[j] == ')', "cfg: 括号不匹配"
            return v, j + 1
        return self._parse_primary(tokens, i)

    def evaluate(self, attribute: str) -> bool:
        """评估一个 ``cfg(...)`` 属性内容(不含外层括号)。

        形如 ``target_os = "macos"`` 或 ``not(feature = "cli")``。
        空串视为恒真。
        """
        expr = attribute.strip()
        if expr.startswith('cfg('):
            expr = expr[4:]
            if expr.endswith(')'):
                expr = expr[:-1]
        expr = expr.strip()
        if not expr:
            return True
        tokens = self._tokenize(expr)
        try:
            val, j = self._parse(tokens, 0)
        except (AssertionError, IndexError) as e:
            raise BuildError(f"无法解析 cfg 表达式 {attribute!r}: {e}")
        if j != len(tokens):
            raise BuildError(f"cfg 表达式有多余 token: {attribute!r}")
        return bool(val)

    def filter_source(self, source: str) -> str:
        """按上下文裁剪源码中被 ``#[cfg(...)]`` 标注的代码块。

        约定:行首 ``#[cfg(...)]`` 之后紧跟的一行代码,若条件为假则删除该行。
        这是构建引擎支持的子集语法,完整块级裁剪由编译器完成。
        """
        out: List[str] = []
        pending_cfg: Optional[str] = None
        for line in source.splitlines():
            stripped = line.strip()
            m = re.match(r'^#\[cfg\((.*)\)\]\s*$', stripped)
            if m:
                pending_cfg = m.group(1)
                continue
            if pending_cfg is not None:
                if self.evaluate(pending_cfg):
                    out.append(line)
                pending_cfg = None
                continue
            out.append(line)
        return '\n'.join(out)


# ── 增量构建哈希 ────────────────────────────────────────────

def _file_hash(path: str) -> str:
    """计算文件内容 SHA-256(用于增量构建判定)。"""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


# ── BuildEngine ─────────────────────────────────────────────

class BuildEngine:
    """Aurora 构建引擎:管理完整构建流程。

    典型用法::

        eng = BuildEngine(project_root='.')
        eng.build({'entries': ['src/main.aur'], 'resources': ['assets/']})

    Attributes:
        project_root:  项目根目录。
        build_dir:     构建中间产物目录(默认 ``build/``)。
        out_dir:       最终输出目录(默认 ``dist/``)。
        evaluator:     条件编译求值器(共享构建上下文)。
    """

    STATE_NAME = '.build_state.json'

    def __init__(self, project_root: str = '.',
                 build_dir: str = 'build',
                 out_dir: str = 'dist') -> None:
        self.project_root = os.path.abspath(project_root)
        self.build_dir = os.path.join(self.project_root, build_dir)
        self.out_dir = os.path.join(self.project_root, out_dir)
        self.evaluator = CfgEvaluator()
        self._hooks_run: List[tuple] = []
        #: 上一次构建的 {文件: 哈希} 记录,增量判定依据
        self._state: Dict[str, str] = {}
        self._load_state()

    # ── 状态持久化 ──

    @property
    def _state_path(self) -> str:
        return os.path.join(self.build_dir, self.STATE_NAME)

    def _load_state(self) -> None:
        if os.path.exists(self._state_path):
            try:
                with open(self._state_path, 'r', encoding='utf-8') as f:
                    self._state = json.load(f)
            except Exception:
                self._state = {}

    def _save_state(self) -> None:
        os.makedirs(self.build_dir, exist_ok=True)
        with open(self._state_path, 'w', encoding='utf-8') as f:
            json.dump(self._state, f, indent=2, sort_keys=True)

    # ── 构建脚本钩子 ──

    def _run_hook(self, script_name: str, phase: str) -> None:
        """执行 build.aur 中给定阶段的钩子(模拟:存在即记录,不真正执行)。

        约定:``build.aur`` 中出现 ``# hook: pre-build`` / ``# hook: post-build``
        标记表示该阶段钩子存在。
        """
        path = os.path.join(self.project_root, script_name)
        if not os.path.isfile(path):
            return
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        marker = f'# hook: {phase}'
        if marker in text:
            self._hooks_run.append((phase, script_name))

    # ── 资源打包 ──

    def _copy_resources(self, resources: List[str]) -> List[str]:
        """把非代码资源(目录或文件)复制到输出目录。"""
        copied: List[str] = []
        for res in resources:
            src = os.path.join(self.project_root, res)
            if not os.path.exists(src):
                continue
            dst = os.path.join(self.out_dir, os.path.basename(src.rstrip('/')))
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
                shutil.copy2(src, dst)
            copied.append(dst)
        return copied

    # ── 编译单文件(模拟)──

    def _compile_one(self, entry: str) -> str:
        """对单个入口做条件编译裁剪并落盘到 out_dir,返回产物路径。"""
        src_path = os.path.join(self.project_root, entry)
        if not os.path.isfile(src_path):
            raise BuildError(f"入口文件不存在: {src_path}")
        with open(src_path, 'r', encoding='utf-8') as f:
            source = f.read()
        compiled = self.evaluator.filter_source(source)
        rel = entry.replace(os.sep, '/')
        out_rel = rel[:-4] + '.auro' if rel.endswith('.aur') else rel + '.o'
        out_path = os.path.join(self.out_dir, out_rel)
        os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(compiled)
        return out_path

    # ── 主构建流程 ──

    def build(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行一次构建。

        Args:
            config: 构建配置,支持键:
                - ``entries``:    入口文件列表(多入口)
                - ``resources``:  资源文件/目录列表
                - ``features``:   启用的特性集合(合并进 cfg 上下文)
                - ``build_script``: 构建脚本文件名(默认 ``build.aur``)

        Returns:
            构建结果摘要 {entries, resources, incremental, hooks, changed}。
        """
        config = dict(config or {})
        entries: List[str] = list(config.get('entries') or ['src/main.aur'])
        resources: List[str] = list(config.get('resources') or [])
        features: Set[str] = set(config.get('features') or [])
        script: str = config.get('build_script', 'build.aur')

        # 合并特性到 cfg 上下文
        self.evaluator.context['features'] = set(
            self.evaluator.context.get('features') or set()) | features

        self._hooks_run: List[tuple] = []
        os.makedirs(self.out_dir, exist_ok=True)

        # pre-build 钩子
        self._run_hook(script, 'pre-build')

        changed: List[str] = []
        outputs: List[str] = []
        for entry in entries:
            abs_entry = os.path.join(self.project_root, entry)
            if not os.path.isfile(abs_entry):
                continue
            digest = _file_hash(abs_entry)
            if self._state.get(entry) == digest:
                continue  # 增量:未变更,跳过
            self._compile_one(entry)
            self._state[entry] = digest
            changed.append(entry)
            outputs.append(entry)

        copied = self._copy_resources(resources)

        # post-build 钩子
        self._run_hook(script, 'post-build')

        self._save_state()
        self.generate_compile_commands()
        return {
            'entries': outputs,
            'all_entries': entries,
            'resources': copied,
            'changed': changed,
            'incremental_skipped': len(entries) - len(changed),
            'hooks': self._hooks_run,
            'output_dir': self.out_dir,
        }

    # ── 清理 ──

    def clean(self) -> None:
        """删除输出目录与构建状态(下次全量重建)。"""
        for d in (self.out_dir, self.build_dir):
            if os.path.isdir(d):
                shutil.rmtree(d)
        self._state = {}

    # ── 编译数据库 ──

    def generate_compile_commands(self, path: Optional[str] = None) -> str:
        """生成 ``compile_commands.json``(供 LSP / 工具链使用)。

        Returns:
            写入的文件路径。
        """
        entries = [k for k in self._state] or ['src/main.aur']
        db = []
        for entry in entries:
            abs_src = os.path.join(self.project_root, entry)
            db.append({
                'directory': self.project_root,
                'file': abs_src,
                'command': f'aurora build --entry {entry}',
            })
        out_path = path or os.path.join(self.build_dir, 'compile_commands.json')
        os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        return out_path


# ── CLI 注册 ────────────────────────────────────────────────

def _cmd_build(ns):
    """``aurora build [--entry ...] [--clean] [--compile-commands]``。"""
    eng = BuildEngine(project_root=getattr(ns, 'path', '.') or '.')
    if getattr(ns, 'clean', False):
        eng.clean()
        print("✓ 已清理 build/ 与 dist/")
        return
    entries = list(getattr(ns, 'entry', None) or [])
    features = list(getattr(ns, 'feature', None) or [])
    result = eng.build({'entries': entries, 'features': features})
    print(f"✓ 构建完成 → {result['output_dir']}")
    for e in result['entries']:
        print(f"  ├─ {e}")
    if getattr(ns, 'compile_commands', False):
        p = eng.generate_compile_commands()
        print(f"✓ 编译数据库 → {p}")


def register_cli(subparsers):
    """在主 CLI 上注册 `aurora build ...` 命令组。"""
    p = subparsers.add_parser('build', help='构建项目(多入口 / 条件编译 / 增量)')
    p.add_argument('--entry', action='append', help='入口文件(可多次指定)')
    p.add_argument('--feature', action='append', help='启用特性(可多次指定)')
    p.add_argument('--clean', action='store_true', help='清理后重新构建')
    p.add_argument('--compile-commands', action='store_true',
                   help='生成 compile_commands.json')
    p.add_argument('--path', default='.', help='项目根目录')
    p.set_defaults(func=_cmd_build)
    return p
