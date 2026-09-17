"""AuroraGit — Aurora 语言 v3.2.0 标准库扩展：Git 绑定与仓库操作。

通过 subprocess 调用系统安装的 ``git`` 命令行，把常用的版本控制工作流
封装为 Pythonic、结构化、可在 Aurora 解释器中直接调用的 API。所有返回值
均为数据类对象，错误统一抛 :class:`GitError`（携带原始命令、退出码与 stderr）。

依赖：仅系统 ``git`` 可执行文件（无需任何第三方 Python 包）。
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ── 异常 ────────────────────────────────────────────────────────────

class GitError(Exception):
    """git 命令执行失败时抛出。

    Attributes:
        command: 失败的完整命令参数列表。
        returncode: git 进程退出码。
        stderr:   git 输出到 stderr 的内容。
    """

    def __init__(self, command: List[str], returncode: int, stderr: str):
        self.command: List[str] = list(command)
        self.returncode: int = returncode
        self.stderr: str = stderr
        super().__init__(f"git {' '.join(command)} failed (exit {returncode}): {stderr.strip()}")


# ── 数据类 ──────────────────────────────────────────────────────────

@dataclass
class Commit:
    """一次 git 提交的结构化表示。"""
    hash: str
    short_hash: str
    author: str
    author_email: str
    date: str
    message: str
    subject: str
    parents: List[str] = field(default_factory=list)

    def __repr__(self) -> str:  # pragma: no cover - 调试用
        return f"<Commit {self.short_hash} {self.subject!r}>"


@dataclass
class Diff:
    """单个文件的 diff 结果。"""
    path: str
    additions: int = 0
    deletions: int = 0
    content: str = ""

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Diff {self.path} +{self.additions}/-{self.deletions}>"


@dataclass
class Status:
    """工作区状态：按 staged / unstaged / untracked 三桶分类。"""
    staged: List[str] = field(default_factory=list)        # 已暂存（新增/修改/删除/重命名）
    unstaged: List[str] = field(default_factory=list)      # 未暂存的修改
    untracked: List[str] = field(default_factory=list)     # 未跟踪文件
    unmerged: List[str] = field(default_factory=list)     # 冲突中

    @property
    def dirty(self) -> bool:
        """工作区是否有任何变更。"""
        return bool(self.staged or self.unstaged or self.untracked or self.unmerged)


@dataclass
class BlameHunk:
    """单行 blame 信息。"""
    line_no: int
    commit: str
    short_hash: str
    author: str
    author_email: str
    time: str
    text: str


@dataclass
class MergeResult:
    """merge / rebase 的结构化结果。"""
    success: bool
    output: str
    conflicts: List[str] = field(default_factory=list)


# ── 内部工具 ────────────────────────────────────────────────────────

def _run_git(args: List[str], cwd: str, check: bool = True) -> subprocess.CompletedProcess:
    """在 ``cwd`` 下执行 ``git <args>``，返回 CompletedProcess。

    若 ``check=True`` 且退出码非 0，抛 :class:`GitError`。
    """
    cmd = ["git"] + list(args)
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if check and proc.returncode != 0:
        raise GitError(cmd, proc.returncode, proc.stderr or proc.stdout)
    return proc


def _parse_log(stdout: str) -> List[Commit]:
    """解析自定义分隔符的 log 输出。"""
    sep = "\x1f"
    commits: List[Commit] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split(sep)
        if len(parts) < 7:
            continue
        h, sh, author, email, date, subject, parents_raw = parts[:7]
        parents = [p for p in parents_raw.split() if p]
        commits.append(Commit(
            hash=h,
            short_hash=sh,
            author=author,
            author_email=email,
            date=date,
            message=subject,
            subject=subject,
            parents=parents,
        ))
    return commits


_LOG_FMT = "%H%x1f%h%x1f%an%x1f%ae%x1f%aI%x1f%s%x1f%P"


# ── Repository ──────────────────────────────────────────────────────

class Repository:
    """一个 git 仓库的 Pythonic 句柄。

    不要直接构造，请使用 :meth:`open` / :meth:`init` / :meth:`clone`。
    """

    def __init__(self, path: str):
        self.path: str = os.path.abspath(path)

    # ── 构造 ────────────────────────────────────────────────────

    @staticmethod
    def open(path: str) -> "Repository":
        """打开已有仓库，校验其确实是 git 仓库。"""
        repo = Repository(path)
        if not repo.is_git_repo():
            raise GitError(["rev-parse", "--is-inside-work-tree"], 1,
                           f"{path} 不是一个 git 仓库")
        return repo

    @staticmethod
    def init(path: str, bare: bool = False) -> "Repository":
        """在 ``path`` 初始化（或复用）一个新仓库。"""
        os.makedirs(path, exist_ok=True)
        args = ["init"]
        if bare:
            args.append("--bare")
        args.append(path)
        _run_git(args, cwd=os.path.abspath(path))
        return Repository(path)

    @staticmethod
    def clone(url: str, path: str, depth: Optional[int] = None,
              branch: Optional[str] = None) -> "Repository":
        """克隆 ``url`` 到 ``path``，可选浅克隆 / 指定分支。"""
        args = ["clone"]
        if depth is not None:
            args += ["--depth", str(depth)]
        if branch:
            args += ["--branch", branch]
        args += [url, path]
        parent = os.path.dirname(os.path.abspath(path)) or "."
        _run_git(args, cwd=parent)
        return Repository(path)

    # ── 基础属性 ─────────────────────────────────────────────────

    @property
    def git_dir(self) -> str:
        """.git 目录的绝对路径（bare 仓库则为仓库根）。"""
        proc = _run_git(["rev-parse", "--git-dir"], cwd=self.path)
        return os.path.abspath(os.path.join(self.path, proc.stdout.strip()))

    def is_git_repo(self) -> bool:
        """当前路径是否位于一个 git 工作树内。"""
        try:
            _run_git(["rev-parse", "--is-inside-work-tree"], cwd=self.path)
            return True
        except GitError:
            return False

    # ── config ───────────────────────────────────────────────────

    def config_get(self, key: str) -> Optional[str]:
        """读取配置项；不存在返回 None。"""
        try:
            proc = _run_git(["config", "--get", key], cwd=self.path)
            return proc.stdout.strip() or None
        except GitError:
            return None

    def config_set(self, key: str, value: str) -> None:
        """写入（仓库级）配置项。"""
        _run_git(["config", key, value], cwd=self.path)

    # ── 提交 / 暂存 ──────────────────────────────────────────────

    def add(self, paths) -> None:
        """把 ``paths`` 加入暂存区。

        ``paths`` 可以是：

        - 字符串 ``"."`` 或 ``"-A"`` → 添加所有变更；
        - 单个字符串 → 添加该路径；
        - 字符串列表 → 批量添加。
        """
        if isinstance(paths, str):
            if paths == "-A":
                args = ["add", "-A"]
            else:
                args = ["add", paths]
        else:
            args = ["add"] + list(paths)
        _run_git(args, cwd=self.path)

    def stage_all(self) -> None:
        """等价于 ``git add -A``。"""
        self.add("-A")

    def unstage(self, paths) -> None:
        """从暂存区移除（``git restore --staged``）。"""
        if isinstance(paths, str):
            paths = [paths]
        _run_git(["restore", "--staged"] + list(paths), cwd=self.path)

    def commit(self, message: str, author: Optional[str] = None,
               allow_empty: bool = False) -> Commit:
        """创建一次提交，返回新提交的 :class:`Commit`。

        ``author`` 形如 ``"Name <email@x.y>"``；``allow_empty`` 对应 ``--allow-empty``。
        """
        args = ["commit", "-m", message]
        if author:
            args += ["--author", author]
        if allow_empty:
            args.append("--allow-empty")
        _run_git(args, cwd=self.path)
        return self.head()

    def head(self) -> Commit:
        """当前 HEAD 提交。"""
        return self.log(n=1)[0]

    def status(self) -> Status:
        """解析工作区状态。"""
        proc = _run_git(["status", "--porcelain"], cwd=self.path)
        s = Status()
        for line in proc.stdout.splitlines():
            if not line:
                continue
            code, rest = line[:2], line[3:]
            name = rest.strip()
            if not name:
                continue
            # 处理 rename: "R  old -> new"
            if " -> " in name:
                name = name.split(" -> ", 1)[1]
            x, y = code[0], code[1]
            if x == "?" and y == "?":
                s.untracked.append(name)
            elif x == "U" or y == "U":
                s.unmerged.append(name)
            elif x != " ":
                s.staged.append(name)
            elif y != " ":
                s.unstaged.append(name)
        return s

    def is_dirty(self) -> bool:
        """工作区是否有未提交变更（含未跟踪文件）。"""
        return self.status().dirty

    def is_clean(self) -> bool:
        """工作区是否干净。"""
        return not self.is_dirty()

    def diff(self, cached: bool = False, target: Optional[str] = None) -> List[Diff]:
        """返回文件级 diff 列表。

        - ``cached=True`` → 比较暂存区与 HEAD；
        - ``target`` → 与指定 ref 比较；
        - 否则比较工作区与暂存区。
        """
        args = ["diff", "--numstat"]
        if cached:
            args.append("--cached")
        if target:
            args.append(target)
        stat = _run_git(args, cwd=self.path).stdout

        # 取完整 diff 内容
        full_args = ["diff"]
        if cached:
            full_args.append("--cached")
        if target:
            full_args.append(target)
        full = _run_git(full_args, cwd=self.path).stdout

        # 按文件切分完整 diff
        chunks: Dict[str, str] = {}
        current: Optional[str] = None
        for line in full.splitlines():
            m = re.match(r"^diff --git a/(.+?) b/", line)
            if m:
                current = m.group(1)
                chunks[current] = line + "\n"
            elif current is not None:
                chunks[current] += line + "\n"

        result: List[Diff] = []
        for line in stat.splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            added, deleted, name = parts[0], parts[1], parts[2]
            # rename: name may be "old -> new"
            if " -> " in name:
                name = name.split(" -> ", 1)[1]
            try:
                a = 0 if added == "-" else int(added)
                d = 0 if deleted == "-" else int(deleted)
            except ValueError:
                a, d = 0, 0
            result.append(Diff(
                path=name,
                additions=a,
                deletions=d,
                content=chunks.get(name, ""),
            ))
        return result

    # ── 分支 ─────────────────────────────────────────────────────

    def branches(self) -> List[str]:
        """列出所有分支（本地 + 远程，去掉前导 ``remotes/`` 前缀展示名）。"""
        proc = _run_git(["branch", "-a"], cwd=self.path)
        out: List[str] = []
        for line in proc.stdout.splitlines():
            name = line.strip().lstrip("* ").strip()
            if not name or "HEAD" in name:
                continue
            out.append(name)
        return out

    def current_branch(self) -> Optional[str]:
        """当前分支名；detached HEAD 时返回 None。"""
        proc = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=self.path,
                        check=False)
        name = proc.stdout.strip()
        if proc.returncode != 0 or name in ("", "HEAD"):
            return None
        return name

    def branch_create(self, name: str, from_branch: Optional[str] = None) -> None:
        """创建分支。"""
        args = ["branch", name]
        if from_branch:
            args.append(from_branch)
        _run_git(args, cwd=self.path)

    def branch_delete(self, name: str, force: bool = False) -> None:
        """删除分支；``force=True`` 等价 ``-D``。"""
        flag = "-D" if force else "-d"
        _run_git(["branch", flag, name], cwd=self.path)

    def checkout(self, target: str, create_branch: bool = False) -> None:
        """切换到分支或 commit；``create_branch=True`` 时新建并切换。"""
        args = ["checkout"]
        if create_branch:
            args.append("-b")
        args.append(target)
        _run_git(args, cwd=self.path)

    def rename_branch(self, old: str, new: str) -> None:
        """重命名分支。"""
        _run_git(["branch", "-m", old, new], cwd=self.path)

    def merge(self, branch: str, no_ff: bool = False,
              message: Optional[str] = None) -> MergeResult:
        """合并 ``branch`` 到当前分支。"""
        args = ["merge", "--no-edit"]
        if no_ff:
            args.append("--no-ff")
        if message:
            args += ["-m", message]
        args.append(branch)
        proc = _run_git(args, cwd=self.path, check=False)
        conflicts: List[str] = []
        if proc.returncode != 0:
            # 列出冲突文件
            ls = _run_git(["diff", "--name-only", "--diff-filter=U"],
                          cwd=self.path, check=False)
            conflicts = [f for f in ls.stdout.splitlines() if f.strip()]
        return MergeResult(
            success=proc.returncode == 0,
            output=(proc.stdout or "") + (proc.stderr or ""),
            conflicts=conflicts,
        )

    def rebase(self, upstream: str, branch: Optional[str] = None,
               interactive: bool = False) -> MergeResult:
        """变基到 ``upstream``。"""
        args = ["rebase"]
        if interactive:
            args.append("-i")
        args.append(upstream)
        if branch:
            args.append(branch)
        proc = _run_git(args, cwd=self.path, check=False)
        conflicts: List[str] = []
        if proc.returncode != 0:
            ls = _run_git(["diff", "--name-only", "--diff-filter=U"],
                          cwd=self.path, check=False)
            conflicts = [f for f in ls.stdout.splitlines() if f.strip()]
        return MergeResult(
            success=proc.returncode == 0,
            output=(proc.stdout or "") + (proc.stderr or ""),
            conflicts=conflicts,
        )

    # ── 远程 ─────────────────────────────────────────────────────

    def remotes(self) -> Dict[str, str]:
        """返回 ``{name: url}`` 映射。"""
        proc = _run_git(["remote", "-v"], cwd=self.path)
        out: Dict[str, str] = {}
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and "(fetch)" in line:
                out[parts[0]] = parts[1]
        return out

    def remote_add(self, name: str, url: str) -> None:
        """添加远程。"""
        _run_git(["remote", "add", name, url], cwd=self.path)

    def remote_remove(self, name: str) -> None:
        """删除远程。"""
        _run_git(["remote", "remove", name], cwd=self.path)

    def remote_set_url(self, name: str, url: str) -> None:
        """修改远程 URL。"""
        _run_git(["remote", "set-url", name, url], cwd=self.path)

    def fetch(self, remote: str = "origin", branch: Optional[str] = None,
              all_: bool = False) -> None:
        """拉取远程引用。"""
        args = ["fetch"]
        if all_:
            args.append("--all")
        else:
            args.append(remote)
            if branch:
                args.append(branch)
        _run_git(args, cwd=self.path)

    def pull(self, remote: str = "origin", branch: Optional[str] = None,
             rebase: bool = False) -> None:
        """拉取并合并。"""
        args = ["pull"]
        if rebase:
            args.append("--rebase")
        args.append(remote)
        if branch:
            args.append(branch)
        _run_git(args, cwd=self.path)

    def push(self, remote: str = "origin", branch: Optional[str] = None,
             force: bool = False, tags: bool = False) -> None:
        """推送。"""
        args = ["push"]
        if force:
            args.append("--force-with-lease")
        if tags:
            args.append("--tags")
        args.append(remote)
        if branch:
            args.append(branch)
        _run_git(args, cwd=self.path)

    # ── 日志 / 查看 ─────────────────────────────────────────────

    def log(self, n: int = 10, branch: Optional[str] = None,
            since: Optional[str] = None, until: Optional[str] = None,
            author: Optional[str] = None, grep: Optional[str] = None) -> List[Commit]:
        """返回提交历史，最新在前。"""
        args = ["log", f"-n{n}", f"--pretty=format:{_LOG_FMT}", "--no-color"]
        if branch:
            args.append(branch)
        if since:
            args += ["--since", since]
        if until:
            args += ["--until", until]
        if author:
            args += ["--author", author]
        if grep:
            args += ["--grep", grep]
        proc = _run_git(args, cwd=self.path, check=False)
        if proc.returncode != 0 and not proc.stdout.strip():
            return []
        return _parse_log(proc.stdout)

    def show(self, commit_or_ref: str) -> Commit:
        """返回指定 ref 的 Commit 详情（subject + parents）。"""
        args = ["show", "-s", f"--pretty=format:{_LOG_FMT}", "--no-color", commit_or_ref]
        proc = _run_git(args, cwd=self.path)
        commits = _parse_log(proc.stdout)
        if not commits:
            raise GitError(args, 1, f"无法解析 {commit_or_ref}")
        c = commits[0]
        # 附带 diff 内容到 message 之后的字段（这里只回填基础元数据）
        return c

    def blame(self, file_path: str, revision: Optional[str] = None) -> List[BlameHunk]:
        """逐行 blame，返回 :class:`BlameHunk` 列表。"""
        args = ["blame", "-w", "--porcelain"]
        if revision:
            args.append(revision)
        args.append("--", file_path)
        proc = _run_git(args, cwd=self.path)
        hunks: List[BlameHunk] = []
        cur: Dict[str, str] = {}
        line_no = 0
        for line in proc.stdout.splitlines():
            if re.match(r"^[0-9a-f]{40} \d+ (\d+)$", line):
                # 新 hunk 起始
                parts = line.split()
                if cur and line_no:
                    hunks.append(BlameHunk(
                        line_no=line_no,
                        commit=cur.get("sha", ""),
                        short_hash=cur.get("sha", "")[:7],
                        author=cur.get("author", ""),
                        author_email=cur.get("author-mail", "").strip("<>"),
                        time=cur.get("author-time", ""),
                        text=cur.get("text", ""),
                    ))
                line_no = int(parts[2])
                cur = {"sha": parts[0]}
            elif line.startswith("author "):
                cur["author"] = line[len("author "):]
            elif line.startswith("author-mail "):
                cur["author-mail"] = line[len("author-mail "):]
            elif line.startswith("author-time "):
                cur["author-time"] = line[len("author-time "):]
            elif line.startswith("\t"):
                cur["text"] = line[1:]
                if cur.get("sha"):
                    hunks.append(BlameHunk(
                        line_no=line_no,
                        commit=cur["sha"],
                        short_hash=cur["sha"][:7],
                        author=cur.get("author", ""),
                        author_email=cur.get("author-mail", "").strip("<>"),
                        time=cur.get("author-time", ""),
                        text=cur["text"],
                    ))
                    line_no += 1
        return hunks

    # ── 标签 ────────────────────────────────────────────────────

    def tags(self) -> List[str]:
        """列出所有标签。"""
        proc = _run_git(["tag"], cwd=self.path, check=False)
        return [t for t in proc.stdout.splitlines() if t.strip()]

    def tag_create(self, name: str, target: Optional[str] = None,
                   message: Optional[str] = None) -> None:
        """打标签；``message`` 非空则创建 annotated tag。"""
        args = ["tag"]
        if message:
            args += ["-a", "-m", message, name]
        else:
            args.append(name)
        if target:
            args.append(target)
        _run_git(args, cwd=self.path)

    def tag_delete(self, name: str) -> None:
        """删除本地标签。"""
        _run_git(["tag", "-d", name], cwd=self.path)

    # ── stash / reset / revert / clean ───────────────────────────

    def stash(self, message: Optional[str] = None) -> None:
        """保存工作区到 stash。"""
        args = ["stash", "push"]
        if message:
            args += ["-m", message]
        _run_git(args, cwd=self.path, check=False)

    def stash_pop(self) -> None:
        """恢复最近一条 stash。"""
        _run_git(["stash", "pop"], cwd=self.path, check=False)

    def stash_list(self) -> List[str]:
        """列出 stash 条目。"""
        proc = _run_git(["stash", "list"], cwd=self.path, check=False)
        return [l for l in proc.stdout.splitlines() if l.strip()]

    def reset(self, hard: bool = False, mixed: bool = True,
              target: str = "HEAD") -> None:
        """重置当前分支到 ``target``。

        默认 mixed（仅取消暂存）；``hard=True`` 会同时丢弃工作区改动。
        """
        args = ["reset"]
        if hard:
            args.append("--hard")
        elif mixed:
            args.append("--mixed")
        args.append(target)
        _run_git(args, cwd=self.path)

    def revert(self, commit: str) -> MergeResult:
        """反转指定提交。"""
        proc = _run_git(["revert", "--no-edit", commit], cwd=self.path, check=False)
        conflicts: List[str] = []
        if proc.returncode != 0:
            ls = _run_git(["diff", "--name-only", "--diff-filter=U"],
                          cwd=self.path, check=False)
            conflicts = [f for f in ls.stdout.splitlines() if f.strip()]
        return MergeResult(
            success=proc.returncode == 0,
            output=(proc.stdout or "") + (proc.stderr or ""),
            conflicts=conflicts,
        )

    def clean(self, force: bool = False, directories: bool = False) -> List[str]:
        """清理未跟踪文件，返回被删除的文件列表（dry-run 模式先列出）。"""
        args = ["clean", "-n"]
        if directories:
            args.append("-d")
        listed = _run_git(args, cwd=self.path, check=False).stdout
        removed = []
        for line in listed.splitlines():
            m = re.match(r"^Would remove (.*)$", line.strip())
            if m:
                removed.append(m.group(1))
        if force:
            do_args = ["clean", "-f"]
            if directories:
                do_args.append("-d")
            _run_git(do_args, cwd=self.path, check=False)
        return removed


__all__ = [
    "GitError",
    "Repository",
    "Commit",
    "Diff",
    "Status",
    "BlameHunk",
    "MergeResult",
]
