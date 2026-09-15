# large-app — 大型项目结构示例

展示 Aurora v3.1.0 如何组织一个超大型多模块项目：模块划分、`pub` 可见性、
`#[cfg(...)]` 条件编译、`async/await`、`defer` 资源管理与错误处理。

## 目录结构

```
large-app/
├── aurora.toml              # workspace / dependencies / features 配置
└── src/
    ├── main.aur             # 入口：组合各模块
    ├── utils/module.aur     # 通用工具（pub 导出常量与函数）
    ├── auth/module.aur     # 认证：pub 结构体 + 私有会话表
    ├── db/module.aur        # 数据库：按 target_os 选择路径
    └── api/module.aur       # HTTP 层：async/await 组合
```

## 关键语言特性

| 特性 | 示例位置 | 说明 |
| --- | --- | --- |
| `pub` 可见性 | `utils/`, `auth/` | 仅 `pub` 符号进入模块导出表；私有符号不可跨模块访问 |
| `#[cfg(...)]` | `db/module.aur` | 按 `target_os` 选择数据库路径，`not`/`or` 组合 |
| `async/await` | `api/module.aur` | `async fn` 返回协程，`await` 取结果 |
| `defer` | `main.aur`, `db/` | LIFO 顺序在函数返回前释放连接 |
| `extern "C"` | `auth/module.aur` | 声明本地 C 库符号 |
| workspace | `aurora.toml` | `[workspace] members` + `[features]` 按需裁剪 |

## 构建命令

```bash
aurora build            # 构建默认入口
aurora build --workspace # 构建整个 workspace
aurora deps             # 查看依赖树
aurora index            # 重建项目符号索引（跨模块跳转/补全）
```

启用 features：

```bash
AURORA_FEATURES=debug,server aurora build
```
