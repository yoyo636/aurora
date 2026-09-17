# git-tools — Aurora Git 工具示例

基于 `std.git` 绑定的命令行 Git 小工具，在示例目录下自动创建一个 `demo-repo` 并完成一整套 Git 工作流。

## 功能介绍

| 演示项 | 用到的 API | 说明 |
| --- | --- | --- |
| 初始化仓库 | `git.init(path)` / `git.is_git_repo(path)` | 不存在则 `git init`，存在则直接打开 |
| 打开仓库 | `git.Repo(path)` | 已有仓库路径上构造 Repo 对象 |
| 配置身份 | `repo.config_set(key, value)` | 本地设置 user.name / user.email |
| 查看状态 | `repo.status()` | 返回 `{staged, unstaged, untracked, ahead}`，每项为 `{path: ...}` 列表 |
| 暂存文件 | `repo.add(path)` | `git add` |
| 提交 | `repo.commit(message)` | 返回 40 位 commit hash |
| 提交日志 | `repo.log(max_count=N)` | 每条含 `short_hash / author / message / files` |
| 分支操作 | `repo.branch()` / `create_branch(name)` / `checkout(name)` / `current_branch()` | 列出、创建、切换分支 |

## 前置条件

本机需要安装 `git` 命令行工具：

```bash
git --version    # 能打印版本号即可
```

## 运行命令

```bash
cd examples/git-tools
../../aurora-run run git_tools.aur
```

脚本会在当前目录创建 `demo-repo/`（已是仓库则复用），自动完成两次提交、查看状态与日志、创建并切换 `demo-branch` 分支。运行结束后可手动进入仓库验证：

```bash
cd demo-repo && git log --oneline && git branch
```

> 只做语法检查：`../../aurora-run check git_tools.aur`

## 注意事项

- 示例仓库是**本地**操作，不涉及远程推送（`remote_add` / `push` 未在本示例演示）。
- 脚本通过 `config_set` 只在该仓库内设置提交身份，不会修改你的全局 `~/.gitconfig`。
- 重复运行是安全的：会在已有提交之上继续追加新提交。
- 若想从零开始，先 `rm -rf demo-repo` 再运行即可。

## 代码结构

```
git_tools.aur
└── main()
    ├── io.mkdir + git.init / git.Repo     # 1. 初始化或打开仓库
    ├── repo.config_set(user.*)            #    本地提交身份
    ├── io.write_file + repo.add + commit  # 2. 两次提交
    ├── repo.status() → 遍历三段列表       # 3. 打印工作区状态
    ├── repo.log(max_count=10)             # 4. 打印提交日志
    └── create_branch / checkout / branch  # 5. 分支演示后切回主分支
```
