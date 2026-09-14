# Aurora Language — VSCode 扩展 (v2.0.0)

在 VSCode 中完整支持 **Aurora** 编程语言(`.aur` 文件)。

## 安装

```bash
# 方式一:命令行安装
code --install-extension /Users/wuyuanduo/aurora/vscode-aurora

# 方式二:复制到扩展目录后重启 VSCode
cp -r /Users/wuyuanduo/aurora/vscode-aurora ~/.vscode/extensions/aurora-ide-2.0.0
```

> 安装后**重启 VSCode**,打开任意 `.aur` 文件即自动激活。

## 功能

| 功能 | 触发方式 | 说明 |
| --- | --- | --- |
| ▶ 运行当前文件 | 编辑器标题栏 ▶ 按钮 / 右键菜单 / `⌘⌥R`(Win: `Ctrl+Alt+R`) | 在集成终端中执行,支持 `read_int` 等 stdin 交互输入 |
| 运行选中代码 | 右键菜单「Aurora: 运行选中代码」 | 选中片段写入临时文件后执行 |
| 静态检查 | 标题栏 ✓ 按钮 / 右键菜单 / `⌘⌥K`(Win: `Ctrl+Alt+K`) | 类型检查 + 所有权检查,错误**行内波浪线**标出,点击跳转 |
| 语法高亮 | 自动 | 关键字 / 内建函数 / 字符串(含插值)/ 数字 / 注释(`//` 与 `#`)/ 运算符 |
| 自动配对 | 自动 | 括号与引号自动闭合、缩进/折叠规则 |

### v2.0.0 新特性

| 功能 | 命令 | 对应 CLI |
| --- | --- | --- |
| 格式化 | `Aurora: 格式化当前文件` | `aurora fmt <file> [--check]` |
| 性能分析 | `Aurora: 性能分析当前文件` | `aurora profile <file> [--json] [--flamegraph] [--top N]` |
| 调试 | `Aurora: 调试当前文件` | `aurora debug <file> [--break N] [--cmd]` |
| LSP 语言服务器 | `Aurora: 启动 LSP 语言服务器` | `aurora lsp [--stdio]` |
| 包管理 | `Aurora: 包管理 (aurora pkg)` | `aurora pkg {init,add,remove,install,list,search,publish,outdated}` |

语法高亮同步增强:

- `@perf(critical|hot|cold|size|trace)` 注解及其参数
- `Result[T,E]` 类型与 `Ok()` / `Err()` 构造
- `?` 问号操作符、`try` / `catch` 错误处理

## 配置

设置项(设置面板搜索 `aurora`):

- `aurora.auroraDir`:Aurora 项目根目录,默认 `/Users/wuyuanduo/aurora`
- `aurora.pythonPath`:执行用的 Python,默认 `python3`

## 目录结构

```
vscode-aurora/
├── package.json                # 扩展清单(命令/语言/键位/菜单/配置)
├── extension.js                # 运行 / 检查 / 诊断逻辑
├── language-configuration.json # 注释、括号、缩进、折叠
├── syntaxes/aurora.tmLanguage.json  # TextMate 语法高亮
└── icons/aurora.png            # 扩展图标
```

## 说明

- 运行依赖 Aurora 语言项目(默认 `/Users/wuyuanduo/aurora`),通过 `aurora-run` 执行
- 检查结果输出到「输出」面板(Aurora 通道),错误同时写入诊断区
- 无需任何构建步骤,纯 Node.js 实现
