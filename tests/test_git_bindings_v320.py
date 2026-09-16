"""Aurora v3.2.0 std.git 绑定模块测试。

在临时目录中执行真实 git 命令验证 Repo 的主要 API。
若系统未安装 git，则整体跳过。
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

# 保证能从项目根目录导入 git_bindings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from git_bindings import Repo, GitError, STDLIB_REGISTRATION


def _git_available():
    """探测系统是否有 git。"""
    try:
        subprocess.run(['git', '--version'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except OSError:
        return False


@unittest.skipUnless(_git_available(), '系统未安装 git，跳过 std.git 测试')
class TestGitBindingsV320(unittest.TestCase):
    """std.git 核心 API 端到端测试。"""

    def setUp(self):
        """每个用例在独立临时目录中初始化一个干净仓库。"""
        self.tmp = tempfile.TemporaryDirectory()
        self.work = self.tmp.name
        self.repo = Repo.init(self.work)
        # 本地配置提交身份，避免依赖全局 gitconfig
        self.repo.config_set('user.name', 'Aurora Tester')
        self.repo.config_set('user.email', 'aurora@example.com')

    def tearDown(self):
        self.tmp.cleanup()

    # ------------------------------------------------------------------
    # 辅助
    # ------------------------------------------------------------------
    def _write(self, name, content):
        path = os.path.join(self.work, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    # ------------------------------------------------------------------
    # 1. init 创建新仓库并验证
    # ------------------------------------------------------------------
    def test_init_creates_repo(self):
        # Repo.init 已在 setUp 中调用，这里验证状态
        self.assertTrue(Repo.is_git_repo(self.work))
        self.assertTrue(os.path.isdir(os.path.join(self.work, '.git')))
        # 当前分支非空（git init 默认分支名因配置而异，不写死）
        self.assertIsNotNone(self.repo.current_branch())
        # 非仓库路径应返回 False
        outside = tempfile.mkdtemp()
        try:
            self.assertFalse(Repo.is_git_repo(outside))
        finally:
            shutil.rmtree(outside)

    # ------------------------------------------------------------------
    # 2. add + commit 工作流
    # ------------------------------------------------------------------
    def test_add_commit_workflow(self):
        self._write('hello.txt', 'hello aurora\n')
        self.repo.add('hello.txt')
        h = self.repo.commit('first commit')
        self.assertEqual(len(h), 40, 'commit hash 应为 40 位')
        # 再做一次多行 message 提交
        self._write('second.txt', 'second\n')
        self.repo.add('.')
        h2 = self.repo.commit('second line\nbody line')
        self.assertEqual(len(h2), 40)
        self.assertNotEqual(h, h2)

    # ------------------------------------------------------------------
    # 3. status 解析（暂存 / 未暂存 / 未跟踪）
    # ------------------------------------------------------------------
    def test_status_parsing(self):
        # 先有一个干净基线
        self._write('tracked.txt', 'v1\n')
        self.repo.add('tracked.txt')
        self.repo.commit('init tracked')

        # 未跟踪文件
        self._write('untracked.txt', 'new\n')
        s = self.repo.status()
        paths = [e['path'] for e in s['untracked']]
        self.assertIn('untracked.txt', paths)
        self.assertEqual(s['ahead'], 0)

        # 已跟踪文件修改后进入 unstaged
        self._write('tracked.txt', 'v2\n')
        s = self.repo.status()
        unstaged_paths = [e['path'] for e in s['unstaged']]
        self.assertIn('tracked.txt', unstaged_paths)

        # add 后进入 staged
        self.repo.add('tracked.txt')
        s = self.repo.status()
        staged_paths = [e['path'] for e in s['staged']]
        self.assertIn('tracked.txt', staged_paths)
        # 提交后清理掉之前的未跟踪文件，再验证工作区干净
        self.repo.commit('modify tracked')
        os.remove(os.path.join(self.work, 'untracked.txt'))
        s = self.repo.status()
        self.assertEqual(s['staged'], [])
        self.assertEqual(s['unstaged'], [])
        self.assertEqual(s['untracked'], [])

    # ------------------------------------------------------------------
    # 4. branch 创建和切换
    # ------------------------------------------------------------------
    def test_branch_create_and_checkout(self):
        self._write('a.txt', 'a\n')
        self.repo.add('a.txt')
        self.repo.commit('base')

        main = self.repo.current_branch()
        self.repo.create_branch('feature-x')
        self.repo.checkout('feature-x')
        self.assertEqual(self.repo.current_branch(), 'feature-x')

        # 在新分支上提交
        self._write('b.txt', 'b\n')
        self.repo.add('b.txt')
        self.repo.commit('on feature')

        # 切回主分支看不到 b.txt
        self.repo.checkout(main)
        self.assertFalse(os.path.exists(os.path.join(self.work, 'b.txt')))

        names = [b['name'] for b in self.repo.branch()]
        self.assertIn('feature-x', names)

    # ------------------------------------------------------------------
    # 5. log 解析
    # ------------------------------------------------------------------
    def test_log_parsing(self):
        self._write('f1.txt', '1\n')
        self.repo.add('f1.txt')
        h1 = self.repo.commit('alpha commit')

        self._write('f2.txt', '2\n')
        self.repo.add('f2.txt')
        h2 = self.repo.commit('beta commit')

        entries = self.repo.log(max_count=10)
        # 最新的在前
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]['hash'], h2)
        self.assertEqual(entries[0]['short_hash'], h2[:7])
        self.assertEqual(entries[0]['message'], 'beta commit')
        self.assertIn('Aurora Tester', entries[0]['author'])
        self.assertEqual(entries[1]['hash'], h1)
        # 每个提交都带文件列表
        self.assertTrue(any(e['path'] == 'f2.txt' for e in entries[0]['files']))

        # 过滤：grep
        filtered = self.repo.log(grep='alpha')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['message'], 'alpha commit')

        # oneline 模式不带文件
        oneline = self.repo.log(oneline=True)
        self.assertEqual(oneline[0]['files'], [])

    # ------------------------------------------------------------------
    # 6. diff 输出
    # ------------------------------------------------------------------
    def test_diff_output(self):
        self._write('d.txt', 'line1\n')
        self.repo.add('d.txt')
        self.repo.commit('add d')

        # 修改文件，未暂存 -> diff 应有内容
        self._write('d.txt', 'line1\nline2\n')
        d = self.repo.diff()
        self.assertIn('diff --git', d)
        self.assertIn('line2', d)

        # 暂存后 diff_files 报告新增行数
        self.repo.add('d.txt')
        files = self.repo.diff_files(cached=True)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['path'], 'd.txt')
        self.assertEqual(files[0]['status'], 'M')
        self.assertGreater(files[0]['additions'], 0)

    # ------------------------------------------------------------------
    # 7. tag 创建和列出
    # ------------------------------------------------------------------
    def test_tag_create_and_list(self):
        self._write('t.txt', 't\n')
        self.repo.add('t.txt')
        self.repo.commit('tag base')

        self.repo.create_tag('v0.1.0', message='initial release')
        self.repo.create_tag('v0.1.1')  # 轻量标签

        tags = self.repo.tag()
        self.assertIn('v0.1.0', tags)
        self.assertIn('v0.1.1', tags)

        # show 一个 tag
        info = self.repo.show('v0.1.1')
        self.assertEqual(info['message'], 'tag base')

        # 删除标签
        self.repo.delete_tag('v0.1.1')
        self.assertNotIn('v0.1.1', self.repo.tag())

    # ------------------------------------------------------------------
    # 8. remote_add / remote 列表（用本地裸仓库做远程，不触网）
    # ------------------------------------------------------------------
    def test_remote_add_list(self):
        # 用另一个临时目录建一个裸仓库作为“远程”
        remote_dir = tempfile.mkdtemp()
        bare = Repo.init(remote_dir, bare=True)
        try:
            self.repo.remote_add('origin', bare.path)
            remotes = self.repo.remote()
            self.assertEqual(len(remotes), 1)
            self.assertEqual(remotes[0]['name'], 'origin')
            self.assertEqual(remotes[0]['fetch'], bare.path)
            self.assertEqual(remotes[0]['push'], bare.path)

            # set_url 改地址
            new_url = bare.path + '.new'
            self.repo.remote_set_url('origin', new_url)
            self.assertEqual(self.repo.remote()[0]['url'], new_url)

            # 删除远程
            self.repo.remote_remove('origin')
            self.assertEqual(self.repo.remote(), [])
        finally:
            shutil.rmtree(remote_dir)

    # ------------------------------------------------------------------
    # 9. rev_parse / config / clean 等小工具
    # ------------------------------------------------------------------
    def test_rev_parse_and_config(self):
        self._write('c.txt', 'c\n')
        self.repo.add('c.txt')
        h = self.repo.commit('config test')

        self.assertEqual(self.repo.rev_parse('HEAD'), h)
        self.assertEqual(self.repo.rev_parse('HEAD'),
                         self.repo.rev_parse(h[:7]))

        # config 读写
        self.repo.config_set('user.name', 'Another')
        self.assertEqual(self.repo.config_get('user.name'), 'Another')
        self.assertIsNone(self.repo.config_get('nonexistent.key.xyz'))

    # ------------------------------------------------------------------
    # 10. GitError 对非仓库抛出
    # ------------------------------------------------------------------
    def test_open_non_repo_raises(self):
        empty = tempfile.mkdtemp()
        try:
            with self.assertRaises(GitError):
                Repo(empty)
        finally:
            shutil.rmtree(empty)


if __name__ == '__main__':
    unittest.main()
