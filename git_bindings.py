"""Aurora v3.2.0 Git 绑定模块（std.git）。

通过 subprocess 调用系统 git 命令并解析输出，不依赖 libgit2。
注册后在 Aurora 语言中以 ``std.git`` 内置模块使用。
"""

import os
import re
import subprocess


class GitError(Exception):
    """git 命令执行失败或环境不满足要求时抛出。"""
    pass


class Repo:
    """代表一个本地 git 仓库。"""

    # ------------------------------------------------------------------
    # 底层命令封装
    # ------------------------------------------------------------------
    @staticmethod
    def _run_git(args, cwd, check=True, capture=True):
        """在 ``cwd`` 目录下执行 ``git <args...>``。

        :param args: git 子命令参数列表（不含 ``git`` 本身）
        :param cwd:  工作目录
        :param check: 非零退出码时是否抛 GitError
        :param capture: True 返回 stdout 字符串；False 返回 CompletedProcess
        """
        cmd = ['git'] + [str(a) for a in args]
        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError:
            raise GitError('未找到 git 可执行文件，请先安装 git。')
        except OSError as exc:  # 其他 OS 级错误（如 cwd 不存在）
            raise GitError('执行 git 失败: %s' % exc)

        if check and proc.returncode != 0:
            raise GitError(
                "命令 'git %s' 失败: %s"
                % (' '.join(str(a) for a in args), (proc.stderr or '').strip())
            )
        if capture:
            return proc.stdout
        return proc

    # ------------------------------------------------------------------
    # 构造 / 静态工厂
    # ------------------------------------------------------------------
    def __init__(self, path='.'):
        """打开 ``path`` 处的仓库，自动定位仓库根目录并校验。"""
        self.path = os.path.abspath(path)
        # 普通工作区：定位仓库根目录
        try:
            out = self._run_git(['rev-parse', '--show-toplevel'], self.path)
            top = out.strip()
            if top:
                self.path = os.path.abspath(top)
                return
        except GitError:
            pass
        # 裸仓库没有工作区，退而校验 --git-dir 可用
        try:
            self._run_git(['rev-parse', '--git-dir'], self.path)
        except GitError:
            raise GitError("路径 '%s' 不是一个 git 仓库。" % path)

    @property
    def path(self):
        """仓库根目录。"""
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @staticmethod
    def is_git_repo(path='.'):
        """静态方法：判断 ``path`` 是否位于一个 git 工作区内。"""
        try:
            out = Repo._run_git(
                ['rev-parse', '--is-inside-work-tree'], path, check=True
            )
            return out.strip() == 'true'
        except GitError:
            return False

    @staticmethod
    def init(path='.', bare=False):
        """在 ``path`` 初始化新仓库并返回 Repo 实例。"""
        args = ['init']
        if bare:
            args.append('--bare')
        args.append(path)
        Repo._run_git(args, os.getcwd())
        return Repo(path)

    @staticmethod
    def clone(url, path=None, depth=None):
        """克隆 ``url`` 到 ``path``（缺省时从 url 推断目录名）。"""
        args = ['clone']
        if depth:
            args += ['--depth', str(depth)]
        args.append(url)
        if path is None:
            path = url.rstrip('/').split('/')[-1]
            if path.endswith('.git'):
                path = path[:-4]
        args.append(path)
        Repo._run_git(args, os.getcwd())
        return Repo(path)

    # ------------------------------------------------------------------
    # 工作区操作
    # ------------------------------------------------------------------
    def status(self):
        """解析 ``git status --porcelain -b``，返回工作区状态字典。"""
        out = self._run_git(
            ['status', '--porcelain=v1', '-b'], self.path, check=False
        )
        # check=False 时返回 CompletedProcess
        out = getattr(out, 'stdout', out) or ''

        result = {
            'branch': None,
            'ahead': 0,
            'behind': 0,
            'staged': [],
            'unstaged': [],
            'untracked': [],
        }

        for line in out.splitlines():
            if not line:
                continue
            # 分支信息行：## main...origin/main [ahead 1, behind 2]
            if line.startswith('##'):
                info = line[3:].strip()
                if info.startswith('HEAD (no branch)'):
                    result['branch'] = 'HEAD'
                else:
                    branch_part = info
                    if '...' in branch_part:
                        branch_part = branch_part.split('...', 1)[0]
                    branch_part = branch_part.split(' [', 1)[0].strip()
                    result['branch'] = branch_part or None
                    m = re.search(r'\[([^\]]*)\]', info)
                    if m:
                        contents = m.group(1)
                        am = re.search(r'ahead\s+(\d+)', contents)
                        bm = re.search(r'behind\s+(\d+)', contents)
                        if am:
                            result['ahead'] = int(am.group(1))
                        if bm:
                            result['behind'] = int(bm.group(1))
                continue

            xy = line[:2]
            rest = line[3:]
            x, y = xy[0], xy[1]

            # 处理重命名：R  old -> new
            if x == 'R' and ' -> ' in rest:
                rest = rest.split(' -> ', 1)[1]

            if x == '?' and y == '?':
                result['untracked'].append({'path': rest, 'status': '??'})
                continue

            if x not in (' ', '?'):
                result['staged'].append({'path': rest, 'status': x})
            if y not in (' ', '?'):
                result['unstaged'].append({'path': rest, 'status': y})

        return result

    def add(self, files):
        """暂存文件。``files`` 可以是路径字符串、列表，或 '.'。"""
        if isinstance(files, str):
            file_list = [files]
        else:
            file_list = list(files)
        self._run_git(['add', '--'] + file_list, self.path)

    def commit(self, message, author=None, allow_empty=False):
        """提交暂存区，返回新提交的完整 hash。支持多行 message。"""
        args = ['commit', '-m', message]
        if author:
            args.append('--author=%s' % author)
        if allow_empty:
            args.append('--allow-empty')
        self._run_git(args, self.path)
        return self._run_git(['rev-parse', 'HEAD'], self.path).strip()

    def reset(self, files=None, hard=False, mode='mixed'):
        """重置暂存区/工作区。``files`` 指定时取消这些文件的暂存。"""
        args = ['reset']
        if files:
            if isinstance(files, str):
                files = [files]
            args += ['HEAD', '--'] + list(files)
        else:
            if hard:
                args.append('--hard')
            elif mode == 'soft':
                args.append('--soft')
            else:
                args.append('--mixed')
        self._run_git(args, self.path)

    # ------------------------------------------------------------------
    # 远程操作
    # ------------------------------------------------------------------
    def _run_text(self, args):
        """执行会产生推送/拉取输出的命令，返回合并后的文本输出。"""
        proc = self._run_git(args, self.path, check=False, capture=False)
        out = ((proc.stdout or '') + (proc.stderr or '')).strip()
        if proc.returncode != 0:
            raise GitError("命令 'git %s' 失败: %s" % (' '.join(args), out))
        return out

    def push(self, remote='origin', branch=None, force=False, set_upstream=False):
        """推送到远程，返回输出文本。"""
        args = ['push']
        if force:
            args.append('--force')
        if set_upstream:
            args.append('-u')
        args.append(remote)
        if branch:
            args.append(branch)
        return self._run_text(args)

    def pull(self, remote='origin', branch=None, rebase=False):
        """从远程拉取，返回输出文本。"""
        args = ['pull']
        if rebase:
            args.append('--rebase')
        args.append(remote)
        if branch:
            args.append(branch)
        return self._run_text(args)

    def fetch(self, remote='origin', all_remotes=False):
        """从远程抓取，返回输出文本。"""
        args = ['fetch']
        if all_remotes:
            args.append('--all')
        else:
            args.append(remote)
        return self._run_text(args)

    # ------------------------------------------------------------------
    # 分支管理
    # ------------------------------------------------------------------
    def branch(self):
        """列出所有本地与远程分支。"""
        out = self._run_git(['branch', '-a'], self.path)
        result = []
        for line in out.splitlines():
            if not line.strip():
                continue
            is_current = line.startswith('*')
            name = line[2:].strip()
            # 跳过 remotes/origin/HEAD -> origin/main 这类指针行
            if ' -> ' in name:
                name = name.split(' -> ', 1)[0].strip()
            is_remote = name.startswith('remotes/')
            if is_remote:
                name = name[len('remotes/'):]
            result.append({
                'name': name,
                'current': is_current,
                'remote': is_remote,
            })
        return result

    def create_branch(self, name, start_point=None):
        """新建分支，返回分支名。"""
        args = ['branch', name]
        if start_point:
            args.append(start_point)
        self._run_git(args, self.path)
        return name

    def checkout(self, target, create_branch=False, b=False):
        """切换分支 / commit / tag；``create_branch`` 或 ``b`` 等价于 -b。"""
        args = ['checkout']
        if create_branch or b:
            args.append('-b')
        args.append(target)
        self._run_git(args, self.path)

    def delete_branch(self, name, force=False):
        """删除分支，``force=True`` 使用 -D。"""
        self._run_git(['branch', '-D' if force else '-d', name], self.path)

    def merge(self, branch, no_ff=False, message=None):
        """合并 ``branch``，返回 ``{'merged': bool, 'output': str}``。"""
        args = ['merge']
        if no_ff:
            args.append('--no-ff')
        if message:
            args += ['-m', message]
        args.append(branch)
        proc = self._run_git(args, self.path, check=False, capture=False)
        out = ((proc.stdout or '') + (proc.stderr or '')).strip()
        return {'merged': proc.returncode == 0, 'output': out}

    # ------------------------------------------------------------------
    # 历史
    # ------------------------------------------------------------------
    @staticmethod
    def _log_format():
        """构造一个带分隔符的 pretty format，便于稳健解析。

        注意：argv 不允许包含 NUL 字节，因此字段用 \\x1f（单元分隔符），
        记录用 \\x1e（记录分隔符）。
        """
        field_sep = '\x1f'
        record_sep = '\x1e'
        fields = ['%H', '%h', '%an <%ae>', '%ad', '%s']
        return record_sep + field_sep.join(fields)

    def log(self, max_count=20, oneline=False, author=None,
            since=None, until=None, grep=None):
        """返回提交列表，解析 ``git log --name-status``。"""
        fmt = self._log_format()
        args = ['log', '--pretty=format:%s' % fmt, '--date=short']
        if not oneline:
            args.append('--name-status')
        if max_count:
            args += ['-n', str(max_count)]
        if author:
            args += ['--author', author]
        if since:
            args += ['--since', since]
        if until:
            args += ['--until', until]
        if grep:
            args += ['--grep', grep]
        try:
            out = self._run_git(args, self.path)
        except GitError:
            # 仓库还没有任何提交
            return []

        result = []
        for chunk in out.split('\x1e'):
            chunk = chunk.strip('\n')
            if not chunk.strip():
                continue
            lines = chunk.split('\n')
            fields = lines[0].split('\x1f')
            if len(fields) < 5:
                continue
            files = []
            if not oneline:
                for ln in lines[1:]:
                    if not ln.strip():
                        continue
                    parts = ln.split('\t')
                    if len(parts) >= 2:
                        files.append({'path': parts[-1], 'status': parts[0][0]})
            result.append({
                'hash': fields[0],
                'short_hash': fields[1],
                'author': fields[2],
                'date': fields[3],
                'message': fields[4],
                'files': files,
            })
        return result

    def show(self, commit='HEAD'):
        """返回单个提交的详细信息（含 diff 与文件列表）。"""
        fmt = self._log_format()
        meta = self._run_git(
            ['show', '-s', '--pretty=format:%s' % fmt, '--date=short', commit],
            self.path,
        )
        chunk = meta.split('\x1e')[-1].strip()
        fields = chunk.split('\n', 1)[0].split('\x1f')
        diff = self._run_git(['show', '--format=', commit], self.path)
        ns = self._run_git(
            ['show', '--name-status', '--format=', commit], self.path
        )
        files = []
        for ln in ns.splitlines():
            if not ln.strip():
                continue
            parts = ln.split('\t')
            if len(parts) >= 2:
                files.append({'path': parts[-1], 'status': parts[0][0]})
        return {
            'hash': fields[0] if len(fields) > 0 else '',
            'short_hash': fields[1] if len(fields) > 1 else '',
            'author': fields[2] if len(fields) > 2 else '',
            'date': fields[3] if len(fields) > 3 else '',
            'message': fields[4] if len(fields) > 4 else '',
            'files': files,
            'diff': diff,
        }

    # ------------------------------------------------------------------
    # 差异
    # ------------------------------------------------------------------
    def diff(self, cached=False, target=None, base=None):
        """返回 ``git diff`` 的文本输出。"""
        args = ['diff']
        if cached:
            args.append('--cached')
        if target and base:
            args.append('%s..%s' % (base, target))
        elif target:
            args.append(target)
        return self._run_git(args, self.path)

    def diff_files(self, cached=False):
        """结合 ``--name-status`` 与 ``--numstat``，返回变更文件列表。"""
        base = ['diff']
        if cached:
            base.append('--cached')

        # 第一遍：name-status 给出真实的 A/M/D/R
        status_map = {}
        ns_out = self._run_git(base + ['--name-status'], self.path)
        for line in ns_out.splitlines():
            if not line.strip():
                continue
            parts = line.split('\t')
            status = parts[0][0]
            path = parts[-1]  # 重命名时取新路径
            status_map[path] = status

        # 第二遍：numstat 给出增删行数
        result = []
        num_out = self._run_git(base + ['--numstat'], self.path)
        for line in num_out.splitlines():
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            add_s, del_s = parts[0], parts[1]
            path = ' '.join(parts[2:])
            # 处理重命名形式: add del olddir/{old => newdir}/new
            if '=>' in path:
                m = re.search(r'=>\s*(.+)', path)
                if m:
                    path = m.group(1).strip()
            try:
                additions = int(add_s) if add_s != '-' else 0
                deletions = int(del_s) if del_s != '-' else 0
            except ValueError:
                additions, deletions = 0, 0
            result.append({
                'path': path,
                'status': status_map.get(path, 'M'),
                'additions': additions,
                'deletions': deletions,
            })
        return result

    # ------------------------------------------------------------------
    # 远程管理
    # ------------------------------------------------------------------
    def remote(self):
        """列出远程仓库。"""
        out = self._run_git(['remote', '-v'], self.path)
        remotes = {}
        order = []
        for line in out.splitlines():
            parts = line.split()
            if len(parts) < 3:
                continue
            name, url, kind = parts[0], parts[1], parts[2].strip('()')
            if name not in remotes:
                remotes[name] = {
                    'name': name, 'url': url, 'fetch': '', 'push': '',
                }
                order.append(name)
            if kind == 'fetch':
                remotes[name]['fetch'] = url
                remotes[name]['url'] = url
            elif kind == 'push':
                remotes[name]['push'] = url
        return [remotes[n] for n in order]

    def remote_add(self, name, url):
        """添加远程。"""
        self._run_git(['remote', 'add', name, url], self.path)

    def remote_remove(self, name):
        """删除远程。"""
        self._run_git(['remote', 'remove', name], self.path)

    def remote_set_url(self, name, url):
        """修改远程 URL。"""
        self._run_git(['remote', 'set-url', name, url], self.path)

    # ------------------------------------------------------------------
    # 标签
    # ------------------------------------------------------------------
    def tag(self):
        """列出所有标签名。"""
        out = self._run_git(['tag', '-l'], self.path)
        return [t for t in out.splitlines() if t.strip()]

    def create_tag(self, name, message=None, target=None):
        """创建轻量或附注标签，返回标签名。"""
        args = ['tag']
        if message:
            args += ['-a', name, '-m', message]
        else:
            args.append(name)
        if target:
            args.append(target)
        self._run_git(args, self.path)
        return name

    def delete_tag(self, name):
        """删除标签。"""
        self._run_git(['tag', '-d', name], self.path)

    # ------------------------------------------------------------------
    # 暂存（stash）
    # ------------------------------------------------------------------
    def stash(self, message=None):
        """保存工作区到 stash。"""
        args = ['stash', 'push']
        if message:
            args += ['-m', message]
        return self._run_git(args, self.path).strip()

    def stash_pop(self):
        """恢复最近一次 stash。"""
        return self._run_git(['stash', 'pop'], self.path).strip()

    def stash_list(self):
        """列出 stash 条目。"""
        out = self._run_git(['stash', 'list'], self.path)
        return [l for l in out.splitlines() if l.strip()]

    # ------------------------------------------------------------------
    # 其他工具
    # ------------------------------------------------------------------
    def rev_parse(self, rev):
        """把引用解析为完整 commit hash。"""
        return self._run_git(['rev-parse', rev], self.path).strip()

    def current_branch(self):
        """返回当前分支名（detached 或空仓库时回退到 'HEAD'）。"""
        # symbolic-ref 在尚未有任何提交的“unborn HEAD”上也能给出分支名
        try:
            return self._run_git(
                ['symbolic-ref', '--short', 'HEAD'], self.path
            ).strip()
        except GitError:
            return 'HEAD'

    def config_get(self, key):
        """读取 git 配置；未设置时返回 None。"""
        proc = self._run_git(
            ['config', '--get', key], self.path, check=False, capture=False
        )
        if proc.returncode != 0:
            return None
        return (proc.stdout or '').strip() or None

    def config_set(self, key, value):
        """写入 git 配置。"""
        self._run_git(['config', key, value], self.path)

    def clean(self, force=False, directories=False):
        """清理未跟踪文件。``force=False`` 时仅 dry-run。"""
        args = ['clean', '-f' if force else '-n']
        if directories:
            args.append('-d')
        return self._run_git(args, self.path).strip()


# ----------------------------------------------------------------------
# 模块注册信息（供 Aurora stdlib 加载器使用）
# ----------------------------------------------------------------------
STDLIB_REGISTRATION = {
    'std.git': {
        'Repo': Repo,
        'GitError': GitError,
        'init': Repo.init,
        'clone': Repo.clone,
        'is_git_repo': Repo.is_git_repo,
    }
}
