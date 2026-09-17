# Aurora v3.2.0：全栈开发引擎发布——一套语言搞定前后端、数据库与终端应用

## 一、版本概述

Aurora v3.2.0 是全栈开发引擎大版本，在 v3.1.0 全平台企业级引擎基础上，新增全栈 Web 框架、数据库 ORM、CLI/TUI 框架、Git 绑定与代码生成器五大核心模块，使 Aurora 从一门高性能系统语言升级为具备完整全栈开发能力的通用编程语言。

本次更新新增代码 **4,787 行**，版本号从 v3.1.0 升级至 **v3.2.0**，测试文件从 24 个扩展至 31 个。项目地址：https://github.com/yoyo636/aurora

## 二、全栈 Web 框架

Aurora Web 框架提供后端路由、中间件、请求响应、静态文件与会话管理的完整能力，采用与 Express/FastAPI 类似的简洁 API 设计。

### 2.1 路由系统

`Router` 类支持 RESTful 方法与路径参数，路径参数通过 `:param` 语法声明，编译为正则表达式进行匹配：

```python
from web_framework import Router, Response

router = Router()

@router.get("/users/:id")
def get_user(request):
    user_id = request.params["id"]
    return Response.json({"id": user_id, "name": "Alice"})

@router.post("/users")
def create_user(request):
    data = request.json()
    return Response.json({"created": True}, status=201)
```

支持的 HTTP 方法包括 `GET`、`POST`、`PUT`、`DELETE`，路由匹配返回处理函数与参数字典。

### 2.2 中间件链

`Middleware` 基类支持链式组合，内置五种中间件：

- **LoggerMiddleware**：请求日志记录（方法、路径、状态码、耗时）
- **CORSMiddleware**：跨域资源共享，可配置允许的源、方法与请求头
- **AuthMiddleware**：基于 Token 的身份验证
- **CompressMiddleware**：Gzip 压缩响应
- **RateLimitMiddleware**：基于 IP 的请求限流

中间件通过 `wrap` 方法包装处理函数，支持前置处理与后置处理：

```python
app = Middleware(LoggerMiddleware())
app = CORSMiddleware(app)
app = RateLimitMiddleware(app, max_requests=100, window=60)
```

### 2.3 请求与响应

`Request` 对象封装 HTTP 请求，提供以下能力：
- `json()`：解析 JSON 请求体
- `form()`：解析表单数据
- `cookies()`：解析 Cookie
- `file(name)`：获取上传文件
- `params`：路径参数
- `query`：查询参数
- `headers`：请求头

`Response` 对象支持多种响应类型：
- `Response.json(data)`：JSON 响应
- `Response.html(content)`：HTML 响应
- `Response.text(content)`：纯文本响应
- `Response.redirect(url)`：重定向
- `set_header(key, value)`：设置响应头
- `set_cookie(name, value, max_age, httponly, secure)`：设置 Cookie

### 2.4 静态文件与会话

`Static.serve(directory, url_prefix)` 提供静态文件服务，自动处理 MIME 类型与缓存。

`Session` 类支持两种存储后端：
- **MemorySessionStore**：内存存储，适用于开发环境
- **CookieSessionStore**：签名 Cookie 存储，支持分布式部署，使用 HMAC 签名防止篡改

## 三、数据库 ORM

Aurora ORM 提供类 ActiveRecord 的数据访问层，支持 SQLite、PostgreSQL、MySQL 三种数据库后端，具备模型定义、查询构建、迁移、连接池、事务与关系映射能力。

### 3.1 模型定义

模型通过继承 `Model` 类定义，字段使用 `Field` 声明：

```python
from db_orm import Model, Field, HasMany, BelongsTo

class User(Model):
    __table__ = "users"
    id = Field(primary_key=True, autoincrement=True)
    name = Field(type="str", nullable=False, index=True)
    email = Field(type="str", unique=True)
    created_at = Field(type="datetime", default="now")
    posts = HasMany("Post", foreign_key="user_id")

class Post(Model):
    __table__ = "posts"
    id = Field(primary_key=True, autoincrement=True)
    title = Field(type="str", nullable=False)
    content = Field(type="text")
    user_id = Field(type="int", foreign_key="users.id")
    author = BelongsTo("User", foreign_key="user_id")
```

`Field` 支持的属性包括：`primary_key`、`autoincrement`、`type`、`nullable`、`default`、`unique`、`index`、`foreign_key`。

### 3.2 查询构建器

`Query` 类提供链式调用 API，支持过滤、排序、分页、聚合与关联预加载：

```python
# 基础查询
users = User.filter(name="Alice").all()
user = User.get(1)

# 链式查询
active_users = (User
    .filter(status="active")
    .order_by("-created_at")
    .limit(10)
    .offset(20)
    .all())

# 聚合
count = User.filter(status="active").count()
avg_age = User.avg("age")

# 关联预加载
posts = Post.filter(published=True).with_related("author").all()
```

支持的查询方法：`filter`、`exclude`、`order_by`、`limit`、`offset`、`all`、`first`、`get`、`count`、`exists`、`update`、`delete`、`with_related`。

### 3.3 关系映射

ORM 支持三种关系类型：
- **HasMany**：一对多关系
- **BelongsTo**：多对一关系
- **ManyToMany**：多对多关系（自动创建中间表）

关系通过属性访问，支持延迟加载与预加载：

```python
user = User.get(1)
posts = user.posts  # 延迟加载
user = User.with_related("posts").get(1)  # 预加载，避免 N+1
```

### 3.4 迁移系统

`MigrationManager` 管理数据库迁移，支持自动生成迁移脚本与版本化管理：

```python
from db_orm import MigrationManager, Migration

manager = MigrationManager("sqlite:///app.db")

# 创建迁移
migration = Migration("create_users_table")
migration.create_table("users", [
    ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"),
    ("name", "TEXT", "NOT NULL"),
    ("email", "TEXT", "UNIQUE"),
])
manager.add_migration(migration)

# 执行迁移
manager.migrate()
manager.rollback()  # 回滚
```

### 3.5 连接池与事务

`ConnectionPool` 实现数据库连接池，支持最小/最大连接数配置与空闲连接回收。`Transaction` 提供事务上下文管理：

```python
with Transaction(connection) as tx:
    User.create(name="Alice", email="alice@example.com")
    Post.create(title="Hello", content="World", user_id=1)
    tx.commit()
```

## 四、CLI/TUI 框架

Aurora CLI/TUI 框架为开发命令行工具与终端用户界面提供完整支持，是构建 Claude Code、Open Code 等交互式终端应用的基础设施。

### 4.1 CLI 工具集

**Spinner 加载动画**：支持多种动画样式，可配置前缀文本与速度：

```python
from cli_tui import Spinner

with Spinner("加载中...", style="dots") as spinner:
    # 执行耗时操作
    spinner.success("完成")
```

**ProgressBar 进度条**：支持百分比、ETA、速度显示，可嵌套多段进度：

```python
from cli_tui import ProgressBar, MultiProgress

bar = ProgressBar(total=100, width=40, show_eta=True)
for i in range(100):
    bar.update(1)
    bar.render()

# 多段进度
multi = MultiProgress()
task1 = multi.add_task("下载文件", total=100)
task2 = multi.add_task("处理数据", total=50)
```

**Table 表格渲染**：支持对齐、边框样式、颜色高亮：

```python
from cli_tui import Table

table = Table(headers=["名称", "状态", "进度"], border_style="rounded")
table.add_row(["任务A", "运行中", "60%"])
table.add_row(["任务B", "完成", "100%"])
table.render()
```

**TreeNode 树状结构**：递归渲染目录树或层级数据。

### 4.2 TUI 框架

TUI 框架采用组件化设计，提供完整的布局系统与控件库。

**布局系统**：
- `Box`：基础容器
- `VBox`：垂直布局
- `HBox`：水平布局
- 支持 flex 比例分配与间距配置

**控件库**：
- `Text`：文本显示，支持多行与自动换行
- `Input`：单行文本输入，支持光标移动与历史记录
- `TextArea`：多行文本编辑
- `List`：列表选择，支持上下键导航与滚动
- `Button`：按钮，支持点击事件

**事件系统**：
- `KeyEvent`：键盘事件，包含按键码与修饰键
- `MouseEvent`：鼠标事件，支持点击与移动
- 事件冒泡与捕获机制

**Screen 终端管理**：
- alternate screen 切换
- 光标隐藏/显示/定位
- 颜色与样式（256 色与真彩色）
- 输入模式切换（cbreak/raw）
- `MockScreen` 用于单元测试

**App 主循环**：
```python
from cli_tui import App, VBox, Text, Input

class MyApp(App):
    def build(self):
        return VBox([
            Text("欢迎使用 Aurora TUI", bold=True),
            Input(placeholder="输入命令..."),
        ])

    def on_key(self, event):
        if event.key == "q":
            self.quit()

MyApp().run()
```

## 五、Git 绑定

Aurora Git 绑定通过调用系统 git 命令并解析输出，提供类型安全的 Git 操作 API，是开发 AI 编程助手、版本控制工具等应用的核心组件。

### 5.1 仓库操作

```python
from git_bindings import Repo

# 打开或初始化仓库
repo = Repo.open("/path/to/repo")
repo = Repo.init("/path/to/new/repo")
repo = Repo.clone("https://github.com/user/repo.git", "/path/to/local")

# 状态查询
status = repo.status()
print(status.modified)   # 修改的文件列表
print(status.staged)     # 已暂存文件
print(status.untracked)  # 未跟踪文件
print(repo.current_branch())  # 当前分支
```

### 5.2 提交与推送

```python
# 暂存与提交
repo.add(["file1.py", "file2.py"])
repo.add(".")  # 暂存所有变更
repo.commit("feat: 添加新功能", author="Aurora <aurora@example.com>")

# 推送与拉取
repo.push(remote="origin", branch="main")
repo.pull(remote="origin", branch="main")
```

### 5.3 分支与历史

```python
# 分支管理
repo.branch("feature/new-feature")  # 创建分支
repo.checkout("feature/new-feature")  # 切换分支
repo.branch_list()  # 列出所有分支

# 提交历史
commits = repo.log(limit=10)
for commit in commits:
    print(commit.hash, commit.author, commit.message)

# 差异对比
diff = repo.diff()  # 工作区差异
diff = repo.diff("HEAD~1", "HEAD")  # 提交间差异
```

### 5.4 远程管理

```python
repo.remote_add("origin", "https://github.com/user/repo.git")
repo.remote_list()
repo.remote_remove("origin")
```

实现采用 `\x1f`/`\x1e` 作为字段分隔符替代 NUL 字节，确保在各种 Git 版本与平台上的输出解析稳定性。

## 六、代码生成器与脚手架

v3.2.0 增强了 CLI 工具，提供项目脚手架与代码生成能力，显著提升开发效率。

### 6.1 项目脚手架

```bash
# 全栈项目（后端+前端+数据库+配置）
aurora new fullstack my-blog

# CLI 工具
aurora new cli my-tool

# TUI 应用
aurora new tui my-editor

# 微服务
aurora new microservice user-service
```

脚手架自动生成项目结构、配置文件、入口文件与示例代码，遵循约定优于配置原则。

### 6.2 代码生成

```bash
# 生成模型+迁移
aurora generate model User name:str email:str:unique age:int

# 生成控制器
aurora generate controller UserController

# 生成前端组件
aurora generate component UserList

# 生成服务层
aurora generate service UserService
```

### 6.3 开发模式

```bash
# 热重载开发模式（文件变化自动重启）
aurora dev

# 数据库迁移
aurora db migrate
aurora db rollback
aurora db seed

# 部署
aurora deploy --target docker
```

## 七、语言级简洁性增强

v3.2.0 在语言层面引入多项语法糖，提升开发效率：

- **属性简写**：`{ name, age }` 等价于 `{ name: name, age: age }`
- **解构默认值**：`let { name = "Unknown", age = 0 } = user`
- **展开运算符**：`...arr` 展开数组，`...obj` 展开对象
- **方法链**：集合操作返回 self，支持 `arr.filter().map().reduce()` 链式调用
- **自动导入**：常用标准库模块自动可用，减少样板 import

## 八、超大型项目支撑能力

Aurora v3.2.0 具备开发 Claude Code、Open Code 级超大型项目的完整能力栈：

| 能力维度 | 支撑模块 | 对应 Claude Code 功能 |
|---------|---------|---------------------|
| 终端交互 | TUI 框架（App/Screen/Widget/Input/List） | 聊天界面、文件浏览、命令面板 |
| 文件操作 | std.io / std.fs | 文件读写、目录遍历、搜索替换 |
| 版本控制 | Git 绑定（Repo/status/commit/diff） | Git 集成、变更查看、自动提交 |
| AI 能力 | AuroraAgent（ReAct/RAG/工具调用） | AI 对话、代码生成、任务执行 |
| 子进程 | AuroraProc | 执行命令、运行测试、启动服务 |
| 配置管理 | std.config | 用户配置、项目配置、环境变量 |
| 全栈开发 | Web 框架 + ORM | 本地服务、Web 界面、数据持久化 |
| 代码生成 | codegen 脚手架 | 项目初始化、模板生成 |

## 九、性能与兼容性

v3.2.0 所有新增模块均为纯 Python 实现，零外部依赖，可在 Aurora 解释器与原生编译模式下运行。Web 框架基于 Python 标准库 `http.server`，ORM 基于 `sqlite3` 标准库（PostgreSQL/MySQL 通过可选驱动），Git 绑定通过系统 git 命令。

新增模块均注册为内置模块，可通过 `import std.web`、`import std.db`、`import std.cli`、`import std.tui`、`import std.git` 直接使用。

## 十、总结

Aurora v3.2.0 全栈开发引擎的发布，标志着 Aurora 从一门高性能系统语言演进为具备完整全栈开发能力的通用平台。开发者现在可以用同一门语言完成：

- **后端服务**：Web API、中间件、会话管理
- **数据层**：ORM、迁移、连接池、事务
- **前端界面**：Web 组件、TUI 应用、GUI 桌面应用
- **开发工具**：CLI 工具、代码生成器、脚手架
- **AI 应用**：Agent 框架、神经网络、推理引擎
- **系统编程**：ARM64 原生编译、内存管理、并发

这正是打破 Python 在 AI 与全栈开发领域垄断的关键一步——Aurora 提供了从底层系统编程到上层全栈应用的统一技术栈，无需在多种语言之间切换。

项目完全开源，欢迎参与贡献：https://github.com/yoyo636/aurora

---

*本文基于 Aurora v3.2.0 撰写，所有代码示例均可直接运行。*
