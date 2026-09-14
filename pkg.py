"""Aurora 包管理器 — 类 npm / cargo / pip 的依赖管理工具

提供:
  - LocalRegistry:   本地模拟包注册表(内置示例包)
  - PackageManager:  init / add / remove / install / list / search / publish / outdated
  - 语义化版本解析与匹配(^ ~ 精确 / >=)
  - 锁文件 aurora.lock(精确版本 + 内容哈希)
  - register_cli:     注册 `aurora pkg ...` 命令组

包存储位置默认: ~/.aurora/packages/<name>/<version>/
"""

import os
import re
import json
import shutil
import hashlib


# ── 语义化版本 ──────────────────────────────────────────────

def parse_version(v):
    """'1.2.3' → (1, 2, 3); 忽略预发布后缀。非法返回 None。"""
    if v is None:
        return None
    m = re.match(r'^\s*v?(\d+)\.(\d+)\.(\d+)', str(v).strip())
    if not m:
        return None
    return tuple(int(x) for x in m.groups())


def _cmp(a, b):
    return (a > b) - (a < b)


def _normalize_constraint(c):
    """把约束字符串拆成 (op, version_tuple)。"""
    if c is None or c == '' or c == '*' or c == 'latest':
        return ('>=', (0, 0, 0))
    c = str(c).strip()
    if c.startswith('^'):
        return ('^', parse_version(c[1:]))
    if c.startswith('~'):
        return ('~', parse_version(c[1:]))
    for op in ('>=', '<=', '==', '!=', '>', '<'):
        if c.startswith(op):
            v = parse_version(c[len(op):])
            return (op, v)
    return ('==', parse_version(c))


def satisfies(version, constraint):
    """version('1.2.3') 是否满足 constraint('^1.2.3' 等)。"""
    v = parse_version(version)
    if v is None:
        return False
    op, cv = _normalize_constraint(constraint)
    if cv is None:
        return False
    if op == '^':
        major, minor, _ = cv
        # caret 兼容: 同一 major(0.x 时同一 minor)内可升级
        if major == 0:
            return v >= cv and v < (0, minor + 1, 0)
        return v >= cv and v < (major + 1, 0, 0)
    if op == '~':
        major, minor, _ = cv
        return v >= cv and v < (major, minor + 1, 0)
    if op == '==':
        return v == cv
    if op == '!=':
        return v != cv
    if op == '>=':
        return v >= cv
    if op == '<=':
        return v <= cv
    if op == '>':
        return v > cv
    if op == '<':
        return v < cv
    return False


def pick_version(available, constraint):
    """从可用版本列表(字符串)中挑选满足约束的最高版本;没有则 None。"""
    ok = [v for v in available if satisfies(v, constraint)]
    if not ok:
        return None
    ok.sort(key=parse_version)
    return ok[-1]


# ── 本地模拟注册表 ──────────────────────────────────────────

class LocalRegistry:
    """内存中的模拟包注册表。内置若干示例包,支持 search / get / download。"""

    def __init__(self):
        # name -> { version -> {description, content} }
        self._packages = {
            'aurora-json': {
                'description': 'JSON 编解码增强库,支持流式解析与格式化',
                'versions': {
                    '1.0.0': '// aurora-json 1.0.0\nexport fn parse(s) { return s }\n',
                    '1.2.0': '// aurora-json 1.2.0\nexport fn parse(s) { return s }\nexport fn stringify(o) { return o }\n',
                    '2.0.0': '// aurora-json 2.0.0\nexport fn parse(s) { return s }\nexport fn stream(s) { return s }\n',
                },
            },
            'aurora-http': {
                'description': 'HTTP 客户端工具集,带重试与超时',
                'versions': {
                    '1.0.0': '// aurora-http 1.0.0\nexport fn get(u) { return u }\n',
                    '1.1.0': '// aurora-http 1.1.0\nexport fn get(u) { return u }\nexport fn post(u, b) { return b }\n',
                    '1.2.0': '// aurora-http 1.2.0\nexport fn get(u) { return u }\nexport fn retry(u, n) { return n }\n',
                },
            },
            'aurora-math': {
                'description': '数学与统计函数库(均值/方差/插值)',
                'versions': {
                    '1.0.0': '// aurora-math 1.0.0\nexport fn mean(xs) { return xs }\n',
                    '1.0.5': '// aurora-math 1.0.5\nexport fn mean(xs) { return xs }\nexport fn median(xs) { return xs }\n',
                    '1.1.0': '// aurora-math 1.1.0\nexport fn mean(xs) { return xs }\nexport fn stddev(xs) { return xs }\n',
                },
            },
        }

    def list_packages(self):
        return dict(self._packages)

    def has(self, name):
        return name in self._packages

    def versions(self, name):
        pkg = self._packages.get(name)
        if not pkg:
            return []
        vs = list(pkg['versions'].keys())
        vs.sort(key=parse_version)
        return vs

    def latest(self, name):
        vs = self.versions(name)
        return vs[-1] if vs else None

    def search(self, keyword):
        """按关键字搜索,返回 [{name, description, latest}]。"""
        kw = (keyword or '').lower()
        out = []
        for name, meta in self._packages.items():
            if kw and kw not in name.lower() and kw not in meta['description'].lower():
                continue
            out.append({
                'name': name,
                'description': meta['description'],
                'latest': self.latest(name),
            })
        out.sort(key=lambda x: x['name'])
        return out

    def get(self, name, version=None):
        """获取包某版本的内容;version 缺省取最新。返回 (version, content, description)。"""
        pkg = self._packages.get(name)
        if not pkg:
            raise KeyError(f"包不存在: {name}")
        if version is None:
            version = self.latest(name)
        if version not in pkg['versions']:
            raise KeyError(f"包 {name} 没有版本 {version}")
        return version, pkg['versions'][version], pkg['description']

    def publish(self, name, version, description=''):
        """模拟发布:注册一个新版本到内存注册表。"""
        self._packages.setdefault(name, {'description': description, 'versions': {}})
        if not self._packages[name]['description']:
            self._packages[name]['description'] = description
        self._packages[name]['versions'][version] = f'// {name} {version}(published)\n'
        return True


# ── TOML 子集读写(与 cli.parse_toml 保持一致的子集)──────────

def _read_toml(path):
    cfg = {}
    if not os.path.exists(path):
        return cfg
    section = None
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line.strip()
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
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
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


def _toml_str(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return '"' + str(value).replace('"', '\\"') + '"'


# ── 包管理器 ──────────────────────────────────────────────

class PackageManager:
    """Aurora 包管理器。

    project_dir   : 项目根目录(含 aurora.toml)
    packages_dir   : 已安装包缓存根目录(默认 ~/.aurora/packages)
    registry       : 包注册表(默认 LocalRegistry)
    """

    LOCK_NAME = 'aurora.lock'
    MANIFEST = 'aurora.toml'

    def __init__(self, project_dir='.', packages_dir=None, registry=None):
        self.project_dir = os.path.abspath(project_dir)
        self.packages_dir = os.path.abspath(
            packages_dir or os.path.expanduser('~/.aurora/packages'))
        self.registry = registry or LocalRegistry()

    # ── 路径 / 配置 ──

    @property
    def manifest_path(self):
        return os.path.join(self.project_dir, self.MANIFEST)

    @property
    def lock_path(self):
        return os.path.join(self.project_dir, self.LOCK_NAME)

    def _read_config(self):
        return _read_toml(self.manifest_path)

    def _dependencies(self):
        cfg = self._read_config()
        deps = cfg.get('dependencies')
        return dict(deps) if isinstance(deps, dict) else {}

    def _write_config(self, cfg):
        """把 cfg 字典序列化为 aurora.toml(保持 project/build/dependencies 结构)。"""
        lines = []
        proj = cfg.get('project', {})
        if proj:
            lines.append('[project]')
            for k in ('name', 'version', 'description', 'author', 'license'):
                if k in proj:
                    lines.append(f'{k} = {_toml_str(proj[k])}')
            lines.append('')
        build = cfg.get('build')
        if build:
            lines.append('[build]')
            for k, v in build.items():
                lines.append(f'{k} = {_toml_str(v)}')
            lines.append('')
        deps = cfg.get('dependencies')
        if deps:
            lines.append('[dependencies]')
            for k, v in deps.items():
                lines.append(f'{k} = {_toml_str(v)}')
            lines.append('')
        os.makedirs(self.project_dir, exist_ok=True)
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines).rstrip() + '\n')

    # ── init ──

    def init(self, name):
        """在 project_dir 初始化新项目(aurora.toml / src/main.aur / .gitignore)。"""
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*', name):
            raise ValueError(f"项目名 '{name}' 不合法")
        src_dir = os.path.join(self.project_dir, 'src')
        os.makedirs(src_dir, exist_ok=True)
        cfg = {
            'project': {
                'name': name,
                'version': '0.1.0',
                'description': f'{name} — Aurora 项目',
                'author': '',
                'license': 'MIT',
            },
            'build': {'entry': 'src/main.aur'},
            'dependencies': {},
        }
        self._write_config(cfg)
        main_path = os.path.join(src_dir, 'main.aur')
        if not os.path.exists(main_path):
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(f'// {name} — 项目入口\n\nfn main() {{\n    println("Hello, Aurora!")\n}}\n\nmain()\n')
        gitignore = os.path.join(self.project_dir, '.gitignore')
        if not os.path.exists(gitignore):
            with open(gitignore, 'w', encoding='utf-8') as f:
                f.write('# Aurora 构建产物\ndist/\nbuild/\n.aurora/\n')
        return True

    # ── 依赖增删 ──

    def add(self, package_name, version=None):
        """添加依赖到 aurora.toml 并下载安装。返回实际安装的版本。"""
        if not self.registry.has(package_name):
            raise KeyError(f"包不存在: {package_name}")
        constraint = version or self.registry.latest(package_name)
        if constraint is None:
            raise KeyError(f"包 {package_name} 无可安装版本")
        cfg = self._read_config()
        cfg.setdefault('dependencies', {})
        cfg['dependencies'][package_name] = constraint
        self._write_config(cfg)
        self._install_one(package_name, constraint)
        self._write_lock()
        return self._installed_version(package_name)

    def remove(self, package_name):
        """从 aurora.toml 移除依赖,并更新锁文件。返回是否移除了。"""
        cfg = self._read_config()
        deps = cfg.get('dependencies', {})
        if package_name not in deps:
            return False
        del deps[package_name]
        cfg['dependencies'] = deps
        self._write_config(cfg)
        lock = self._read_lock()
        lock.pop(package_name, None)
        self._write_lock_data(lock)
        return True

    # ── 安装 ──

    def _installed_version(self, package_name):
        lock = self._read_lock()
        entry = lock.get(package_name)
        return entry['version'] if entry else None

    def _install_one(self, package_name, constraint):
        available = self.registry.versions(package_name)
        version = pick_version(available, constraint)
        if version is None:
            raise RuntimeError(
                f"无法为 {package_name} 找到满足 '{constraint}' 的版本;可用: {available}")
        _, content, _ = self.registry.get(package_name, version)
        dest = os.path.join(self.packages_dir, package_name, version)
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, 'index.aur'), 'w', encoding='utf-8') as f:
            f.write(content)
        return version, hashlib.sha256(content.encode('utf-8')).hexdigest()

    def install(self):
        """安装 aurora.toml 中所有依赖,生成 aurora.lock。"""
        deps = self._dependencies()
        installed = {}
        for name, constraint in deps.items():
            if not self.registry.has(name):
                raise KeyError(f"包不存在: {name}")
            version, digest = self._install_one(name, constraint)
            installed[name] = {'version': version, 'hash': digest}
        self._write_lock_data(installed)
        return installed

    # ── 锁文件 ──

    def _read_lock(self):
        if not os.path.exists(self.lock_path):
            return {}
        try:
            with open(self.lock_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('packages', {})
        except Exception:
            return {}

    def _write_lock_data(self, packages):
        data = {'version': 1, 'packages': packages}
        with open(self.lock_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)

    def _write_lock(self):
        """根据当前 aurora.toml 与本地缓存重建锁文件。"""
        lock = {}
        for name, constraint in self._dependencies().items():
            v = self._installed_version(name)
            if v is None:
                try:
                    v, digest = self._install_one(name, constraint)
                except Exception:
                    continue
            else:
                pkg_dir = os.path.join(self.packages_dir, name, v)
                idx = os.path.join(pkg_dir, 'index.aur')
                with open(idx, 'rb') as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
            lock[name] = {'version': v, 'hash': digest}
        self._write_lock_data(lock)

    # ── 查询 ──

    def list(self):
        """返回 {name: {'require': constraint, 'installed': version|None}}。"""
        deps = self._dependencies()
        lock = self._read_lock()
        out = {}
        for name, constraint in deps.items():
            out[name] = {
                'require': constraint,
                'installed': (lock.get(name) or {}).get('version'),
            }
        return out

    def search(self, keyword):
        return self.registry.search(keyword)

    def outdated(self):
        """检查过时依赖,返回 [{name, installed, latest}]。"""
        out = []
        for name, info in self.list().items():
            latest = self.registry.latest(name)
            installed = info['installed']
            if latest and installed and parse_version(installed) < parse_version(latest):
                out.append({'name': name, 'installed': installed, 'latest': latest})
        return out

    # ── 发布 ──

    def publish(self):
        """模拟发布:校验 aurora.toml 完整性。返回项目元信息。"""
        cfg = self._read_config()
        proj = cfg.get('project', {})
        missing = [k for k in ('name', 'version', 'description') if not proj.get(k)]
        if missing:
            raise RuntimeError(f"aurora.toml 缺少必填字段: {', '.join(missing)}")
        entry = (cfg.get('build') or {}).get('entry')
        if not entry:
            raise RuntimeError("aurora.toml 缺少 [build].entry")
        info = {
            'name': proj['name'],
            'version': proj['version'],
            'description': proj['description'],
            'author': proj.get('author', ''),
            'license': proj.get('license', ''),
            'entry': entry,
        }
        # 模拟注册到注册表
        self.registry.publish(info['name'], info['version'], info['description'])
        return info


# ── CLI 注册 ────────────────────────────────────────────────

def _cmd_pkg_init(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    pm.init(ns.name)
    print(f"✓ 初始化项目 {ns.name}/")
    print(f"  ├─ aurora.toml")
    print(f"  ├─ src/main.aur")
    print(f"  └─ .gitignore")


def _cmd_pkg_add(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    v = pm.add(ns.name, getattr(ns, 'version', None))
    print(f"✓ 添加依赖 {ns.name}@{v}")


def _cmd_pkg_remove(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    if pm.remove(ns.name):
        print(f"✓ 移除依赖 {ns.name}")
    else:
        print(f"  {ns.name} 不在依赖列表中")


def _cmd_pkg_install(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    installed = pm.install()
    if not installed:
        print("  没有需要安装的依赖")
        return
    for name, info in installed.items():
        print(f"✓ {name}@{info['version']}")


def _cmd_pkg_list(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    items = pm.list()
    if not items:
        print("  无依赖")
        return
    for name, info in items.items():
        print(f"  {name:<16} {info['require']:<10} (安装: {info['installed'] or '未安装'})")


def _cmd_pkg_search(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    results = pm.search(ns.keyword)
    if not results:
        print("  无匹配包")
        return
    for r in results:
        print(f"  {r['name']:<16} v{r['latest']:<8} {r['description']}")


def _cmd_pkg_publish(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    info = pm.publish()
    print(f"✓ 发布 {info['name']}@{info['version']}")


def _cmd_pkg_outdated(ns):
    pm = PackageManager(project_dir=getattr(ns, 'path', '.') or '.')
    items = pm.outdated()
    if not items:
        print("✓ 所有依赖均为最新")
        return
    for it in items:
        print(f"  {it['name']}: {it['installed']} → {it['latest']}")


def register_cli(subparsers):
    """在主 CLI 上注册 `aurora pkg ...` 命令组。"""
    pkg = subparsers.add_parser('pkg', help='包管理器(aurora.toml 依赖管理)')
    sub = pkg.add_subparsers(dest='pkg_cmd', help='pkg 子命令')

    p = sub.add_parser('init', help='初始化新项目')
    p.add_argument('name', help='项目名')
    p.add_argument('--path', default='.', help='项目目录(默认当前目录)')
    p.set_defaults(func=_cmd_pkg_init)

    p = sub.add_parser('add', help='添加依赖')
    p.add_argument('name', help='包名')
    p.add_argument('version', nargs='?', default=None, help='版本/约束(默认最新)')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_add)

    p = sub.add_parser('remove', help='移除依赖')
    p.add_argument('name', help='包名')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_remove)

    p = sub.add_parser('install', help='安装所有依赖')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_install)

    p = sub.add_parser('list', help='列出依赖')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_list)

    p = sub.add_parser('search', help='搜索包')
    p.add_argument('keyword', help='关键字')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_search)

    p = sub.add_parser('publish', help='发布当前包')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_publish)

    p = sub.add_parser('outdated', help='检查过时依赖')
    p.add_argument('--path', default='.')
    p.set_defaults(func=_cmd_pkg_outdated)

    # 把分发逻辑挂到 pkg 本身(主 CLI 已用 func 分发到 cmd 级)
    def _dispatch(args):
        if getattr(args, 'pkg_cmd', None) is None:
            pkg.print_help()
            return
        args.func(args)

    pkg.set_defaults(func=_dispatch)
    return pkg
