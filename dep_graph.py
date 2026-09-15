"""Aurora v3.1.0 依赖图分析与可视化。

提供:
  - ``DependencyGraph``:      构建模块/包依赖图,传递依赖计算、冲突与未使用检测
  - DOT / Mermaid 两种可视化输出
  - ``register_cli``:         注册 `aurora deps ...` 命令组

冲突检测复用 pkg.py 的语义化版本 ``satisfies``;图算法为标准 DFS/BFS,
保持零外部依赖。
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional, Set, Tuple

try:
    from aurora.pkg import satisfies, parse_version
except Exception:  # pragma: no cover - 兜底,保证模块独立可导入
    def satisfies(version: str, constraint: str) -> bool:
        return str(version) == str(constraint).lstrip('^~><=! ')

    def parse_version(v):
        return (0, 0, 0)


class DependencyError(Exception):
    """依赖图分析错误。"""


# ── DependencyGraph ────────────────────────────────────────

class DependencyGraph:
    """包依赖有向图。

    节点:``{包名: {'version': str, 'deps': {依赖名: 版本约束}}}``。
    边:A 依赖 B → 有向边 A → B。

    Example::

        g = DependencyGraph()
        g.build({
            'app': {'version': '1.0.0', 'deps': {'lib': '^1.0.0'}},
            'lib': {'version': '1.2.0', 'deps': {}},
        })
    """

    def __init__(self) -> None:
        #: 节点表 {包名: {'version', 'deps'}}
        self.packages: Dict[str, Dict[str, object]] = {}

    # ── 构建 ──

    def build(self, packages: Dict[str, Dict[str, object]]) -> 'DependencyGraph':
        """从包描述字典构建图(会覆盖已有内容)。"""
        self.packages = {
            name: {
                'version': str(meta.get('version', '0.0.0')),
                'deps': dict(meta.get('deps') or {}),
            }
            for name, meta in packages.items()
        }
        return self

    # ── 查询 ──

    def nodes(self) -> List[str]:
        return list(self.packages.keys())

    def direct_deps(self, pkg: str) -> Dict[str, str]:
        """直接依赖 {依赖名: 约束}。"""
        return dict((self.packages.get(pkg) or {}).get('deps') or {})

    def transitive_deps(self, pkg: str) -> List[str]:
        """BFS 列出 ``pkg`` 的全部传递依赖(不含自身,拓扑序去重)。"""
        if pkg not in self.packages:
            raise DependencyError(f"未知包: {pkg}")
        seen: Set[str] = set()
        order: List[str] = []
        queue: List[str] = [pkg]
        while queue:
            cur = queue.pop(0)
            for dep in self.direct_deps(cur):
                if dep in seen or dep == pkg:
                    continue
                seen.add(dep)
                order.append(dep)
                if dep in self.packages:
                    queue.append(dep)
        return order

    # ── 冲突检测 ──

    def detect_conflicts(self) -> List[Dict[str, object]]:
        """检测同一包被多个上游以不兼容版本约束引用的情况。

        Returns:
            冲突列表,每项::

                {'package': 'lib',
                 'required_by': {'app': '^2.0.0', 'cli': '~1.0.0'},
                 'resolved': '1.5.0' or None}
        """
        # 收集每个被依赖包: {被依赖包: {上游: 约束}}
        required_by: Dict[str, Dict[str, str]] = {}
        for name, meta in self.packages.items():
            for dep, constraint in (meta.get('deps') or {}).items():
                required_by.setdefault(dep, {})[name] = str(constraint)

        conflicts: List[Dict[str, object]] = []
        for dep, upstreams in required_by.items():
            resolved = (self.packages.get(dep) or {}).get('version')
            incompatible = {
                up: c for up, c in upstreams.items()
                if resolved and not satisfies(str(resolved), c)
            }
            # 多个不同约束且没有一个统一可满足版本 → 冲突
            constraints = set(upstreams.values())
            if len(constraints) > 1 and incompatible:
                conflicts.append({
                    'package': dep,
                    'required_by': upstreams,
                    'resolved': resolved,
                    'incompatible': incompatible,
                })
        return conflicts

    # ── 未使用依赖检测 ──

    def detect_unused(self, actually_used: Optional[Set[str]] = None
                      ) -> Dict[str, List[str]]:
        """对比"声明依赖"与"实际 import",找出每个包声明但未使用的依赖。

        Args:
            actually_used: {包名: 实际被导入的依赖集合};缺省则每个包认为
                           只使用自身直接依赖的一半(用于演示)。

        Returns:
            {包名: [未使用的依赖名]}。
        """
        actually_used = actually_used or {}
        out: Dict[str, List[str]] = {}
        for name, meta in self.packages.items():
            declared = set((meta.get('deps') or {}).keys())
            used = set(actually_used.get(name, set()))
            unused = sorted(declared - used)
            if unused:
                out[name] = unused
        return out

    # ── 可视化 ──

    def edges(self) -> List[Tuple[str, str]]:
        """全部有向边 (源, 目标)。"""
        out = []
        for name, meta in self.packages.items():
            for dep in (meta.get('deps') or {}):
                out.append((name, dep))
        return out

    def to_dot(self) -> str:
        """输出 Graphviz DOT 格式依赖图。"""
        lines = ['digraph aurora_deps {', '  rankdir=LR;']
        for name, meta in self.packages.items():
            ver = meta.get('version', '?')
            lines.append(f'  "{name}" [label="{name}\\nv{ver}"];')
        for src, dst in self.edges():
            lines.append(f'  "{src}" -> "{dst}";')
        lines.append('}')
        return '\n'.join(lines)

    def to_mermaid(self) -> str:
        """输出 Mermaid flowchart 格式依赖图。"""
        lines = ['graph LR']
        for src, dst in self.edges():
            # Mermaid 节点 ID 不能含点,替换为下划线
            lines.append(f'  {src.replace(".", "_")} --> {dst.replace(".", "_")}')
        for name, meta in self.packages.items():
            ver = meta.get('version', '?')
            nid = name.replace('.', '_')
            lines.append(f'  {nid}["{name} v{ver}"]')
        return '\n'.join(lines)

    # ── 序列化 ──

    def to_json(self) -> str:
        return json.dumps(self.packages, indent=2, ensure_ascii=False)


# ── CLI 注册 ────────────────────────────────────────────────

def _cmd_deps(ns):
    """``aurora deps [--graph=dot|mermaid] [--transitive PKG] [--from file.json]``。"""
    graph: DependencyGraph = DependencyGraph()
    src = getattr(ns, 'from_file', None)
    if src:
        with open(src, 'r', encoding='utf-8') as f:
            graph.build(json.load(f))
    else:
        print("  提示:用 --from packages.json 加载依赖数据")
        return

    if getattr(ns, 'transitive', None):
        for d in graph.transitive_deps(ns.transitive):
            print(f"  {d}")
        return

    fmt = getattr(ns, 'graph', None)
    if fmt == 'mermaid':
        print(graph.to_mermaid())
    elif fmt == 'dot' or fmt:
        print(graph.to_dot())
    else:
        conflicts = graph.detect_conflicts()
        unused = graph.detect_unused()
        print(f"  节点: {len(graph.nodes())}  边: {len(graph.edges())}")
        if conflicts:
            print("  冲突:")
            for c in conflicts:
                print(f"    ! {c['package']}: {c['required_by']}")
        else:
            print("  无版本冲突")
        if unused:
            print("  未使用依赖:")
            for pkg, deps in unused.items():
                print(f"    - {pkg}: {deps}")


def register_cli(subparsers):
    """在主 CLI 上注册 `aurora deps ...` 命令组。"""
    p = subparsers.add_parser('deps', help='依赖图分析与可视化')
    p.add_argument('--graph', choices=['dot', 'mermaid'],
                   help='输出可视化格式')
    p.add_argument('--transitive', metavar='PKG',
                   help='列出某包的全部传递依赖')
    p.add_argument('--from', dest='from_file', metavar='FILE',
                   help='从 JSON 文件加载包依赖数据')
    p.set_defaults(func=_cmd_deps)
    return p
