"""AuroraGit 测试 — 全部在临时目录中操作，不影响项目仓库本身。"""

import os
import shutil
import tempfile
import unittest

from aurora.git import Repository, GitError


def _make_repo() -> Repository:
    """在临时目录创建一个已配置 user 信息的空仓库。"""
    d = tempfile.mkdtemp(prefix="aurora-git-test-")
    repo = Repository.init(d)
    repo.config_set("user.email", "aurora-test@example.com")
    repo.config_set("user.name", "Aurora Test")
    return repo


def _write(repo: Repository, rel: str, content: str) -> None:
    with open(os.path.join(repo.path, rel), "w", encoding="utf-8") as f:
        f.write(content)


class TestGitInit(unittest.TestCase):
    """仓库初始化与基本属性。"""

    def setUp(self):
        self.repo = _make_repo()
        self.addCleanup(shutil.rmtree, self.repo.path, ignore_errors=True)

    def test_init_creates_git_dir(self):
        self.assertTrue(self.repo.is_git_repo())
        self.assertTrue(os.path.isdir(self.repo.git_dir))

    def test_open_existing_repo(self):
        reopened = Repository.open(self.repo.path)
        self.assertEqual(os.path.normcase(reopened.path),
                         os.path.normcase(self.repo.path))

    def test_open_non_repo_raises(self):
        empty = tempfile.mkdtemp(prefix="aurora-git-nope-")
        self.addCleanup(shutil.rmtree, empty, ignore_errors=True)
        with self.assertRaises(GitError):
            Repository.open(empty)

    def test_config_get_set(self):
        self.repo.config_set("core.ignorecase", "true")
        self.assertEqual(self.repo.config_get("core.ignorecase"), "true")
        self.assertIsNone(self.repo.config_get("nonexistent.key.xyz"))


class TestGitAddCommitStatus(unittest.TestCase):
    """add / commit / status 工作流。"""

    def setUp(self):
        self.repo = _make_repo()
        self.addCleanup(shutil.rmtree, self.repo.path, ignore_errors=True)

    def test_add_and_commit(self):
        _write(self.repo, "hello.txt", "hello\n")
        self.repo.add("hello.txt")
        c = self.repo.commit("first commit")
        self.assertEqual(c.subject, "first commit")
        self.assertEqual(len(c.parents), 0)
        self.assertTrue(self.repo.is_clean())

    def test_status_classifies(self):
        _write(self.repo, "a.txt", "a\n")
        self.repo.add(".")
        self.repo.commit("c1")
        # 修改已跟踪文件
        _write(self.repo, "a.txt", "a v2\n")
        # 新增未跟踪文件
        _write(self.repo, "b.txt", "b\n")
        st = self.repo.status()
        self.assertIn("a.txt", st.unstaged)
        self.assertIn("b.txt", st.untracked)

    def test_stage_all_and_unstage(self):
        # 先有一次初始提交，否则没有 HEAD 可 restore
        _write(self.repo, "seed.txt", "seed\n")
        self.repo.add(".")
        self.repo.commit("seed")
        _write(self.repo, "x.txt", "x\n")
        self.repo.stage_all()
        st = self.repo.status()
        self.assertIn("x.txt", st.staged)
        self.repo.unstage("x.txt")
        st = self.repo.status()
        self.assertIn("x.txt", st.untracked)


class TestGitBranchCheckout(unittest.TestCase):
    """分支创建 / 切换 / 列表。"""

    def setUp(self):
        self.repo = _make_repo()
        self.addCleanup(shutil.rmtree, self.repo.path, ignore_errors=True)
        _write(self.repo, "main.txt", "m\n")
        self.repo.add(".")
        self.repo.commit("on main")

    def test_branch_create_and_list(self):
        self.repo.branch_create("feature")
        branches = self.repo.branches()
        self.assertIn("main", branches)
        self.assertIn("feature", branches)

    def test_checkout_switches_branch(self):
        self.repo.branch_create("dev")
        self.repo.checkout("dev")
        self.assertEqual(self.repo.current_branch(), "dev")
        _write(self.repo, "dev.txt", "d\n")
        self.repo.add(".")
        self.repo.commit("on dev")
        # 切回 main 不应看到 dev.txt
        self.repo.checkout("main")
        self.assertFalse(os.path.exists(os.path.join(self.repo.path, "dev.txt")))


class TestGitLogAndDiff(unittest.TestCase):
    """提交历史与 diff。"""

    def setUp(self):
        self.repo = _make_repo()
        self.addCleanup(shutil.rmtree, self.repo.path, ignore_errors=True)
        _write(self.repo, "file.txt", "v1\n")
        self.repo.add(".")
        self.repo.commit("first", author="Aurora Tester <t@example.com>")
        _write(self.repo, "file.txt", "v2\n")
        self.repo.add(".")
        self.repo.commit("second")

    def test_log_returns_commits(self):
        history = self.repo.log(n=10)
        self.assertEqual(len(history), 2)
        # 最新在前
        self.assertEqual(history[0].subject, "second")
        self.assertEqual(history[1].subject, "first")
        # 第一条应是第二条的子提交
        self.assertIn(history[1].hash, history[0].parents)
        self.assertEqual(history[1].author_email, "t@example.com")

    def test_diff_after_edit(self):
        _write(self.repo, "file.txt", "v3\nplus\n")
        diffs = self.repo.diff()
        paths = [d.path for d in diffs]
        self.assertIn("file.txt", paths)
        d = next(x for x in diffs if x.path == "file.txt")
        self.assertGreaterEqual(d.additions, 1)
        self.assertIn("-v2", d.content)


class TestGitErrors(unittest.TestCase):
    """GitError 携带命令 / 退出码 / stderr。"""

    def setUp(self):
        self.repo = _make_repo()
        self.addCleanup(shutil.rmtree, self.repo.path, ignore_errors=True)

    def test_bad_command_raises(self):
        with self.assertRaises(GitError) as cm:
            self.repo.branch_delete("nonexistent-branch")
        self.assertNotEqual(cm.exception.returncode, 0)
        self.assertTrue(cm.exception.command)
        self.assertTrue(cm.exception.stderr)


if __name__ == "__main__":
    unittest.main()
