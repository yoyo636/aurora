# Aurora 版本策略

本文档定义 Aurora 语言的版本管理与兼容性承诺。自 v1.0.0 起生效,v2.0.0 起纳入 ARM64 后端与新特性稳定性承诺。

## 语义化版本

版本号 `MAJOR.MINOR.PATCH`:

| 段 | 何时递增 | 示例 |
| --- | --- | --- |
| MAJOR | 破坏性变更:语法移除、语义变更(如绑定可变性)、标准库签名不兼容 | 1.0.0 → 2.0.0 |
| MINOR | 向后兼容的新特性、新模块、新命令 | 1.0.0 → 1.1.0 |
| PATCH | 向后兼容的缺陷修复 | 1.0.0 → 1.0.1 |

## 稳定性分级

| 级别 | 含义 | 变更许可 |
| --- | --- | --- |
| stable | v2.0.0 规范承诺的行为 | 仅 MAJOR 版本可破坏 |
| experimental | 新特性(带 `@` 或文档标注) | 任意版本可调整 |
| deprecated | 已标记弃用 | 下一 MAJOR 移除 |

## 兼容性承诺(v3.x)

1. 按 `docs/SPEC.md` 编写的程序,在相同平台使用相同版本运行,行为一致;
2. 新特性只做**加法**:新语法、新模块、新命令不改变既有程序结果;
3. 错误消息文本可改进,但 `L行:C列: [类别]` 的格式不变;
4. `aurora.toml` 清单格式向后兼容(新增键不破坏旧清单);
5. 测试运行器、脚手架等工具行为的既有用法保持可用。

## v2.0.0 稳定性承诺

v2.0.0 是里程碑大版本,P0–P3 全部规划完成,包含三大创新特性:ARM64 原生汇编后端、@perf 自适应性能注解、Result 与异常无缝互操作,以及函数级增量编译缓存。

自 v2.0.0 起,以下内容纳入 stable 承诺:
- ARM64 原生汇编后端(asmgen.py)及其优化 Pass 链(内联、循环展开、强度削减、TCO、DCE、常量传播等);
- @perf 五级注解语法与编译器行为;
- `Result[T, E]` 类型标注、`?` 操作符、自动解包规则、try/catch 互操作语义;
- P2 工具链:`aurora fmt`、`aurora profile`、`aurora debug`、`aurora lsp`;
- P3 生态:`aurora pkg` 包管理器、扩充标准库(正则/日期时间/加密/文件系统/网络);
- 函数级增量编译缓存的磁盘格式与失效语义。

## 版本历史

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0.0 | — | 首个稳定版本,核心语法与解释器 |
| v2.0.0 | 2026-09-14 | 里程碑大版本:P0–P3 全部完成;三大创新特性(ARM64 后端、@perf 注解、Result 互操作);增量编译缓存;测试 161→306 全通过 |
| v3.0.0 | 2026-09-15 | AI 原生引擎:七大 AI 模块(std.tensor/autograd/nn/data/agent/inference/kernel);@ai 注解;aurora ai train/infer、aurora serve、aurora kernel;测试 364→400+ 全通过 |
| v3.1.0 | 2026-09-15 | 全平台企业级引擎:性能革命(并行编译/增量编译增强/图着色寄存器分配/指令调度/LICM/CSE/NEON SIMD/逃逸分析);模块化系统(pub/import/循环依赖检测);构建系统(#[cfg]/工作区 Monorepo/依赖图);LSP 企业级增强;调试器增强;AuroraUI 跨平台 GUI 框架;macOS/Windows/Web 原生绑定;全平台打包;新关键字 pub/async/await/defer/unsafe/extern "C"/#[cfg];测试 400+→509 全通过 |

## 发布流程

1. 所有变更必须通过测试套件:`python3 -m unittest discover -s aurora/tests`(当前 509 项);
2. 破坏性变更须同时更新 `docs/SPEC.md`、`CHANGELOG.md` 与示例;
3. 版本号同步更新于:`aurora/__init__.py`、`ide/static/index.html`(状态栏)、`vscode-aurora/package.json`、`pyproject.toml`、`build-pkg.sh`、`build-vsix.py`;
4. 发布同时产出:CLI 安装脚本 `install.sh`、VSCode 插件 `.vsix`、`.app`。

## 变更记录

每次发布在 `CHANGELOG.md` 中追加条目,格式:

```
## [版本] - 日期
### 新增 / 变更 / 修复 / 移除
- 描述
```
