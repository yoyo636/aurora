# Aurora 编程语言 v3.3.0

> 融合 **Rust / Python / Go / TypeScript** 优势的通用编程语言 —— 纯 Python 实现，零第三方依赖。
> **v3.3.0 里程碑**:语言级原生增量计算——`source` / `live` / `transact` 三个关键字,`Source<T>` / `Live<T>` 两个类型,纯计算块用 `live` 标记后即成为可复算、可订阅的"活计算"(显式标记 + 自动依赖追踪,而非默认增量);拉模式惰性重算、哈希短路、事务、编译期纯度检查与循环依赖检测。
> **v3.2.0 里程碑**:全栈开发引擎——全栈 Web 框架、数据库 ORM、CLI/TUI 框架、Git 绑定、代码生成器五大模块;语言级增强(自动导入/属性简写/展开运算符/字典解构/解构默认值);测试增长到 **825+ 个全部通过**。
> **v3.1.0 里程碑**:全平台企业级引擎——性能革命(并行编译/NEON SIMD/逃逸分析)、模块化系统、AuroraUI 跨平台 GUI 框架、全平台打包(macOS/Windows/Linux/Web)、原生绑定;测试增长到 **509 个全部通过**。
> **v3.0.0 里程碑**:AI 原生引擎——张量计算、自动微分、神经网络、数据处理、Agent 框架、模型推理全部内置,不再依赖 Python / PyTorch / NumPy。
> 正式发布:语义化版本 + 完整规范(`docs/SPEC.md`)+ 版本策略(`docs/VERSIONING.md`)+ 变更日志(`CHANGELOG.md`)。

Aurora 是一个完整的语言工具链:词法分析 → 语法分析 → 类型检查 → 所有权检查 → 树遍历解释执行,外加 REPL、测试运行器、项目脚手架与生态桥接。

**[历史] v2.0.0 三大创新特性**:
- **ARM64 原生汇编后端** —— Aurora → ARM64 汇编 → 原生可执行文件,**不依赖 C 编译器**,直接使用系统调用
- **`@perf` 自适应性能注解** —— 五级优化策略,按函数自适应选择编译/优化级别
- **Result 类型与异常无缝互操作** —— `?` 操作符自动解包,`Result` 与 `try/catch` 双向贯通

**[历史] v2.2.0 生态互通大版本**:补齐 JavaScript/TypeScript/Java/WebAssembly 四大语言桥,构建 `std.interop` 统一多语言互操作层,FFI 增强结构体/回调/绑定代码自动生成,新增 `aurora interop`、`aurora gen-bindings`、`aurora wasm` 三个 CLI 命令。

**v3.2.0 全栈开发特性**:
- **全栈 Web 框架** —— `std.web` 扩展为 40 成员:路由、中间件、模板、静态资源、WebSocket
- **数据库 ORM** —— `std.db`:模型定义、迁移、查询构建器、种子数据、SQLite/PostgreSQL 驱动
- **CLI/TUI 框架** —— `std.cli`/`std.tui`:命令解析、子命令、参数校验、终端 UI(面板/列表/输入框)
- **Git 绑定** —— `std.git`:仓库初始化、提交、分支、差异、日志,纯 Python 实现
- **代码生成器** —— `aurora generate` 一键生成 controller/model/component/service 脚手架
- **语言级增强** —— 自动导入、属性简写 `User { name, age }`、展开运算符 `[...arr, 4]`/`{...obj, b: 2}`、字典解构 `let { name, age } = user`、解构默认值 `let { name = "Unknown" } = user`

**v3.3.0 增量计算特性**:
- **语言级原生增量计算** —— `source`(可变输入源)、`live`(活计算块)、`transact`(批量事务)三个关键字,无需手写订阅与失效逻辑
- **拉模式惰性重算** —— source 改动只标记下游 Dirty,真正读取时才深度优先重算,未读节点不浪费算力
- **哈希短路** —— 重算后结果哈希不变则不级联通知下游,避免无效刷新
- **类型** —— `Source<T>` / `Live<T>`,编译期纯度检查 + 循环依赖检测
- **可观测** —— 依赖图导出(Mermaid / DOT)、`get_stats()` 重算与缓存命中统计、`subscribe` 结果变化回调

**v3.1.0 企业级特性**:
- **性能革命** —— 并行编译、增量编译增强、图着色寄存器分配、指令调度、LICM、CSE、NEON SIMD、逃逸分析
- **模块化系统** —— `pub`/`import`/模块解析/循环依赖检测,支持超大型项目
- **构建系统** —— `#[cfg]` 条件编译、工作区 Monorepo、依赖图
- **AuroraUI** —— 跨平台 GUI 框架(20+ 控件),`aurora ui` 命令
- **全平台打包** —— `aurora package macos/windows/linux/web`,原生绑定 macOS/Windows/Web
- **LSP 企业级增强** —— 重构、跨文件跳转、语义高亮
- **调试器增强** —— 条件断点、时间旅行调试、远程调试

- **Rust 基因**:所有权/借用检查、`trait`/`impl`、`enum` + `match`、`Result`/`?`、`let`/`var` 绑定
- **Python 基因**:无分号压力、动态值、内置集合、`try/catch`、字符串插值
- **Go 基因**:`spawn` 协程、`chan` 通道、`select` 多路复用、`Mutex`、`defer`
- **TypeScript 基因**:渐进式类型推断、联合类型、管道 `|>`、可选链 `?.`、空合并 `??`
- **AI 基因 (v3.0.0)**:原生张量 `Tensor`、自动微分 `autograd`、神经网络 `nn`、数据处理 `data`、Agent 框架 `agent`、推理引擎 `inference`、Jupyter 内核 `kernel`

## AI 原生引擎 (v3.0.0+,v3.1.0 增强)

Aurora v3.0.0 把 AI 工具链做进了语言本身:**张量计算、自动微分、神经网络、数据处理、LLM Agent、模型推理**全部内置为标准库模块,不再需要安装 Python + PyTorch + NumPy + pandas。同一个 `.aur` 文件既能训练模型,也能部署为 HTTP 推理服务。

**七大模块**:

- `std.tensor` — AuroraTensor:多维张量、广播、矩阵乘法、逐元素函数、NumPy 互操作
- `std.autograd` — AuroraAutograd:动态计算图反向自动微分,SGD / Adam 优化器
- `std.nn` — AuroraNN:`Linear` / `Conv2d` / `LSTM` / `Sequential` / 损失函数 / 模型保存
- `std.data` — AuroraData:类 Pandas `DataFrame`、CSV/JSON、清洗 / 转换 / `DataLoader`
- `std.agent` — AuroraAgent:ReAct 工具调用循环、记忆、RAG、PromptTemplate、Chain
- `std.inference` — AuroraInference:模型加载、批量推理、量化、HTTP 推理服务器
- `std.kernel` — AuroraKernel:Jupyter 内核,在 notebook 里直接写 Aurora AI 代码

**为什么 Aurora 比 Python 更适合 AI**:

- **原生性能**:ARM64 原生编译,张量循环比 Python 快 10–100 倍,不需要写 C 扩展
- **零依赖部署**:训练好的模型序列化为纯 JSON `.aur` 文件,推理服务是单可执行文件
- **类型安全**:编译期做张量形状检查(规划中),维度错误在编译期暴露而非训练中途崩溃
- **统一语言**:从数据清洗 → 训练 → 部署 → HTTP 服务,全栈 Aurora,不再需要 Python + Shell + Dockerfile 三件套

**最小示例** — 3 行完成张量运算:

```aurora
import std.tensor
let a = tensor.Tensor([[1.0, 2.0], [3.0, 4.0]])
print((a @ a.T).tolist())        # [[5.0, 11.0], [11.0, 25.0]]
```

完整文档与示例:

- 📖 AI 引擎完整文档:[`docs/AI_GUIDE.md`](docs/AI_GUIDE.md)
- 🚀 可运行示例:[`examples/ai/`](examples/ai/) — 线性回归 / MNIST MLP / LLM Agent / 数据流水线 / 推理服务器

## 全平台开发 (v3.1.0)

Aurora v3.1.0 把单语言扩展为**全平台企业级开发栈**:一套代码,同时构建桌面 GUI、Web 应用、AI 推理服务,并打包为各平台原生安装包。

### AuroraUI — 跨平台 GUI 框架

```aurora
import std.ui

let window = ui.Window(title: "Hello", width: 800, height: 600)
let label = ui.Label(text: "你好, Aurora!")
let button = ui.Button(text: "点击")
button.on_click(fn(e) { label.text = "已点击!" })
window.add(ui.VBox([label, button]))
window.run()
```

- **20+ 控件**:Button / Label / TextInput / Image / List / Table / Tree / Canvas / Menu / Dialog / ProgressBar / Slider / Checkbox / Radio / Tab / Splitter / StatusBar / Toolbar / Notification
- **跨平台**:原生窗口渲染(macOS Cocoa / Windows Win32 / Web WebAssembly)
- **事件系统**:on_click / on_change / on_key / on_resize

### 全平台打包

```bash
aurora package macos myapp.aur       # 打包为 .app / .pkg
aurora package windows myapp.aur     # 打包为 .exe
aurora package linux myapp.aur       # 打包为 ELF
aurora package web myapp.aur         # 编译为 WebAssembly,浏览器运行
```

### 原生绑定

- **macOS**:Cocoa/AppKit 绑定,可调用 Swift/Objective-C 框架
- **Windows**:Win32/COM 绑定,可调用 .NET / C# 组件
- **Web**:WebAssembly 绑定,直接操作 DOM / Web API
- `aurora gen-bindings` 自动从 C 头文件生成 Aurora 绑定代码

### 模块化系统

```aurora
// math.aur
pub fn add(a: int, b: int) -> int { a + b }
pub const VERSION = "1.0.0"
fn internal() { ... }              // 私有

// main.aur
import math
print(math.add(1, 2))               // 3
```

- `pub` 导出公开接口,未标注的成员模块内可见
- 编译器自动检测循环依赖并报告
- `aurora workspace` 管理 Monorepo 多项目
- `#[cfg(target: "macos")]` 条件编译平台特定代码

## 全栈开发 (v3.2.0)

Aurora v3.2.0 把单语言扩展为**全栈开发引擎**:一套语言覆盖 Web 后端、数据库、CLI 工具、TUI 应用与 Git 操作,配套代码生成器一键脚手架。

### 全栈 Web 框架 (std.web)

```aurora
import std.web

let app = web.App()

app.get("/", fn(req) {
    return web.html("<h1>你好, Aurora</h1>")
})

app.get("/api/users/:id", fn(req) {
    let id = req.params["id"]
    return {"id": id, "name": "用户 " + id}
})

app.use(web.logger())                  # 中间件
app.serve(8080)
```

- **路由**:`get/post/put/delete`,路径参数 `:id`,通配符 `*`
- **中间件**:日志、CORS、认证、错误处理,`app.use(middleware)`
- **模板**:`web.render(template, data)`,继承 v3.1.0 `std.html`
- **静态资源**:`app.static("/static", "./public")`
- **WebSocket**:`app.ws("/ws", on_message)`

### 数据库 ORM (std.db)

```aurora
import std.db

type User {
    db.table("users")
    db.field("id", type: "int", primary: true)
    db.field("name", type: "str")
    db.field("email", type: "str")
}

db.connect("sqlite://blog.db")
db.migrate()                           # 自动建表

let user = User(name: "Aurora", email: "hi@aurora.dev")
user.save()

let admins = db.query("User").where("name", "==", "Aurora").all()
```

- **模型定义**:`db.table` / `db.field`,自动映射数据库表
- **迁移**:`aurora db migrate` 自动生成 SQL,`aurora db rollback` 回滚
- **查询构建器**:`where / order_by / limit / join / first / all / count`
- **种子数据**:`aurora db seed` 填充测试数据
- **驱动**:SQLite(内置)、PostgreSQL(扩展)

### CLI/TUI 框架 (std.cli / std.tui)

```aurora
import std.cli
import std.tui

// CLI 应用
let app = cli.App(name: "mycli", version: "1.0.0")
app.command("greet", fn(args) {
    cli.print("你好, " + args.get("name", "世界"))
})
app.run()

// TUI 应用
let t = tui.Terminal()
let panel = tui.Panel(title: "任务列表")
panel.add(tui.List(["写文档", "跑测试", "发布"]))
t.render(panel)
```

- **std.cli**:子命令解析、位置/选项参数、类型校验、`--help` 自动生成
- **std.tui**:Panel / List / Input / ProgressBar / Table / Box 布局,键盘事件

### Git 绑定 (std.git)

```aurora
import std.git

let repo = git.Repository.init("./myproject")
repo.config(user_name: "Aurora", user_email: "hi@aurora.dev")

repo.add("src/main.aur")
repo.commit("feat: 初始化项目")

let feature = repo.branch("feature/login")
feature.checkout()
```

- **纯 Python 实现**,无外部 git 依赖
- 支持:init / clone / add / commit / branch / checkout / diff / log / status
- 可用 `aurora new` 创建的项目自动 `git init`

### 代码生成器

```bash
aurora generate controller UserController   # 生成 HTTP 控制器
aurora generate model User                  # 生成 ORM 模型
aurora generate component Header            # 生成 UI 组件
aurora generate service AuthService          # 生成业务服务类
```

### 新建项目模板

```bash
aurora new myblog --template fullstack      # 全栈 Web 项目
aurora new mytool --template cli            # CLI 工具项目
aurora new myeditor --template tui          # TUI 终端应用
aurora new mysvc --template microservice    # 微服务项目
aurora new mysite --template webapp         # 纯前端 Web 应用
```

### v3.2.0 语言级增强

```aurora
// 属性简写:变量名与字段名相同时省略 value
let name = "Aurora"
let age = 3
let user = User { name, age }              // 等价 User { name: name, age: age }

// 展开运算符:数组
let arr = [1, 2, 3]
let extended = [...arr, 4, 5]              // [1, 2, 3, 4, 5]
let merged = [...arr, ...[6, 7]]           // [1, 2, 3, 6, 7]

// 展开运算符:字典
let base = { port: 8080, host: "0.0.0.0" }
let config = { ...base, debug: true }      // { port: 8080, host: "0.0.0.0", debug: true }

// 字典解构
let { name, age } = user                   // name="Aurora", age=3
let { name: n, age: a } = user             // 重命名:n="Aurora"

// 解构默认值
let { title = "未命名" } = user            // 缺失键时取默认值 "未命名"

// 自动导入:std.web / std.db / std.cli / std.tui / std.git 等常用模块无需手动 import
let app = web.App()                        // web 自动可用
```

### v3.2.0 示例项目

| 示例 | 路径 | 说明 |
| --- | --- | --- |
| 全栈博客 | `examples/fullstack-blog/` | Web 框架 + ORM + 模板,完整博客应用 |
| CLI 工具 | `examples/cli-tool/` | std.cli 子命令 + 参数校验,完整 CLI 工具 |
| TUI 编辑器 | `examples/tui-editor/` | std.tui 面板/列表/键盘事件,终端文本编辑器 |
| Claude Code 风格 | `examples/claude-code-like/` | 全栈:CLI 交互 + AI Agent + TUI 界面 |

## 增量计算 (v3.3.0)

Aurora v3.3.0 的**杀手级特性**:**把纯计算块用 `live` 关键字显式标记为"活计算"**——标记后自动追踪依赖、可复算、可订阅。注意这不是"所有函数默认增量":普通 `let` 定义的计算不参与增量图,只有被 `live` 包裹的块才会按需重算。你只需用 `source` 标出"输入会变",用 `live { ... }` 包住一段纯计算,Aurora 就自动追踪依赖、按需重算,再也不用手写"监听 → 失效 → 重新渲染"的样板代码。

```aurora
# 唯一的输入变化点:source
let mut count = source(0)

# live 块自动追踪它读到的 source/live
let doubled = live { count * 2 }
let tripled  = live { count * 3 }

println("初始:", doubled, tripled)     # 0  0

# 修改 source —— 下游只是被标记,不会立刻重算
count = 5

# 真正读取时才惰性重算:只算被读到的节点
println("doubled =", doubled)          # 10
println("tripled =", tripled)          # 15
```

**三个核心概念**:

- **`source(value)` 是唯一的输入变化点** —— 只有写进 `source` 的值才会"变"。普通变量保持编译期常量语义,不会触发任何重算。
- **`live { ... }` 自动追踪依赖** —— 块内读了哪个 source/live,运行时就记下它作为依赖;source 一改,这些 live 自动变脏,读取时才重算。
- **`transact { ... }` 批量更新** —— 块内多次写 source 只累积、不传播,块结束时统一重算一次,避免中间态触发多次刷新。

**关键特性**:

- **惰性重算**:拉模式,只有被读取的节点才重算,没读的分支零开销
- **哈希短路**:重算后结果没变(结构化哈希相同)就不通知下游,UI 不会白刷新
- **编译期纯度检查**:`live` 块必须是纯函数,块内赋值/副作用在编译期报错
- **循环依赖检测**:运行时检测到环立即报错,不让程序进入无限重算
- **依赖图可视化**:`export_graph("mermaid")` / `export_graph("dot")` 导出依赖图
- **结果订阅**:`node.subscribe(fn(new, old) { ... })`,结果真正变化时回调

完整指南:[`docs/INCREMENTAL_GUIDE.md`](docs/INCREMENTAL_GUIDE.md) · 可运行示例:[`examples/incremental/`](examples/incremental/)

## 安装

```bash
# macOS 一键安装器(推荐,自动配置运行时 / VSCode 插件 / 环境变量)
curl -L -o Aurora-Installer-v3.2.0.pkg https://github.com/yoyo636/aurora/releases/download/v3.2.0/Aurora-Installer-v3.2.0.pkg
installer -pkg Aurora-Installer-v3.2.0.pkg -target /

# 或直接使用源码
bash install.sh          # 安装 aurora 命令到用户 PATH(推荐)
./aurora-run repl
```

## 快速开始

```bash
aurora repl                        # 交互式 REPL
aurora run hello.aur               # 运行 .aur 文件
aurora check hello.aur             # 类型/所有权静态检查
aurora new myapp && cd myapp       # 创建项目(脚手架 + aurora.toml)
aurora run                         # 运行项目(读清单入口)
aurora test                        # 运行测试(*_test.aur / test_* 函数)
aurora fmt .                       # 格式化整个项目(P2 工具链)
aurora eval 'println(1 + 2)'       # 执行一行
aurora --version                   # Aurora v3.2.0
```

`hello.aur`：

```python
fn greet(name: str) -> str {
    return "Hello, {name}!"
}

let msg = greet("Aurora")
println(msg)            # Hello, Aurora!
assert msg.len() > 0
```

## 语言指南

### 变量与常量

```python
let x = 42              # 可变变量（let 默认 mutable）
let mut y = 1           # 显式 mutable
y = y + 1
const MAX = 100         # 常量（不可变）
let typed: int = 5      # 类型注解可选
```

### 函数

```python
fn add(a: int, b: int = 10) -> int {
    return a + b
}

add(5)                  # 15（默认参数）
add(5, 6)               # 11
add(a: 5, b: 6)         # 命名参数
add(5, b: 6)            # 位置 + 命名混用

# lambda 与高阶函数
let double = |x| x * 2
[1, 2, 3].map(|x| x * 2)        # [2, 4, 6]
[1, 2, 3, 4].filter(|x| x % 2 == 0)  # [2, 4]
[1, 2, 3, 4].reduce(|a, b| a + b)    # 10
```

### 控制流

```python
# if / elif / else（也是表达式）
let grade = if score >= 90 { "A" } elif score >= 60 { "B" } else { "C" }

# for：range、集合、字典、通道
for i in range(5) { println(i) }
for k, v in {"a": 1} { println("{k}={v}") }
for item in ch { ... }          # 通道迭代直到 close

# while / break / continue
while true { if done { break } }
```

### 自定义类型

```python
type Point {
    x: float,
    y: float
}

type Rect {
    w: float = 1.0,      # 字段默认值
    h: float = 1.0
}

let p = Point(x: 3.0, y: 4.0)   # 命名参数
let r = Rect(5.0, 2.0)          # 位置参数
println(p.x)                    # 字段访问
p.y = 9.0                       # 字段赋值

# match 构造器模式绑定
match p {
    Point(x, y) => println("{x},{y}"),
    _ => println("other")
}
```

### 枚举与模式匹配

```python
enum Shape {
    Circle(radius: float),
    Rect(w: float, h: float),
    Dot
}

let c = Shape.Circle(radius: 2.5)
println(c.radius)                       # 字段访问
c == Shape.Circle(radius: 2.5)          # 值比较

fn area(s) -> float {
    match s {
        Circle(r) => 3.14159 * r * r,
        Rect(w, h) => w * h,
        Dot => 0.0,
        _ => -1.0
    }
}
```

### trait 与 impl

```python
trait Greeter {
    fn greet() -> str          # 纯声明
    fn farewell() -> str { return "bye" }  # 默认实现
}

type Person { name: str }

impl Greeter for Person {
    fn greet() -> str { return "hi, {self.name}" }
}

let me = Person(name: "aurora")
me.greet()          # "hi, aurora"
me.farewell()       # "bye"（默认实现自动补齐）
```

### 错误处理(v2.0.0:Result 与异常无缝互操作)

```python
# try / catch / finally
try {
    panic("boom")
} catch e: str {
    println("caught: {e}")
} finally {
    println("cleanup")
}

# Result / ? —— v2.0.0 起与异常无缝互操作
# ? 自动解包 Ok;遇 Err 自动转为 ResultError 抛出,可被 try/catch 捕获
from std.result import Ok, Err

fn read_config(path: str) -> Result {
    if not exists(path) { return Err("missing: {path}") }
    return Ok(read_file(path))
}

fn bootstrap() -> str {
    let cfg = read_config("app.conf")?      # 自动解包;Err 时抛出 ResultError
    return parse(cfg)?.get("name", "default")?
}

# match 模式匹配仍完全可用
match safe_div(1, 0) {
    Ok(x) => println(x),
    Err(e) => println("failed: {e}")
}

# ResultError 与原生异常双向贯通
try {
    bootstrap()
} catch e {
    println("err: {e}")        # ResultError 携带原始 Err 值
}
```

### 并发

```python
fn worker(ch, items) {
    for item in items {
        ch <- item              # 发送
    }
    ch.close()
}

let ch = chan(10)
spawn worker(ch, [1, 2, 3])

let first = <-ch                # 前缀接收（阻塞）
let rest = ch.recv()            # 方法接收

select {
    v = <-ch => { println("got {v}") },   # 接收并绑定变量
    ch2 => { println("data on ch2") },
    default => { println("no data yet") }
}
```

### 模块与标准库

```python
import std.io                     # 命名空间访问：std.io.exists(...)
import std.math as m              # 别名：m.sqrt(16)
from std.math import sqrt, PI     # 直接导入
from std.result import Ok as ROk  # 别名导入

import std.json
std.json.stringify({"k": [1, 2]})   # '{"k": [1, 2]}'

# 多文件模块：import 本地 .aur 文件(自动搜索当前目录/src/项目根)
import utils                      # 加载 utils.aur 或 utils/__init__.aur
from utils import helper          # 从本地模块导入指定函数
import services.task_service      # 加载 services/task_service.aur

# 集合类型
import std.collections
let map = std.collections.hash_map()
map.put("key", "value")
map.get("key")                     # "value"

# 可用模块
# std.io          read_file / write_file / append_file / exists / read_line / list_dir / mkdir / is_dir / files
# std.math        sqrt / pow / floor / ceil / round / sin / cos / log / random ...
# std.str         split / join / replace / contains / upper / lower / trim / format
# std.time        now / sleep / timestamp / format
# std.json        parse / stringify / load / save
# std.sync        Channel / Mutex / Fiber
# std.result      Ok / Err / Result
# std.collections HashMap / HashSet / Vec / hash_map / hash_set / vec
# std.web         40 成员:路由/中间件/模板/静态/WebSocket/serve/static/wait(v3.2.0 扩展)
# std.db          Model/Migration/QueryBuilder/Seed/数据库驱动(v3.2.0)
# std.cli         命令解析/子命令/参数校验(v3.2.0)
# std.tui         面板/列表/输入框/终端UI(v3.2.0)
# std.git         仓库/提交/分支/差异/日志(v3.2.0)
# std.ai          configure / chat / messages / agent(AI Agent)
# std.tensor      Tensor 原生张量计算(v3.0.0)
# std.autograd    Variable / backward / SGD / Adam(v3.0.0)
# std.nn          Linear / Sequential / ReLU / CrossEntropyLoss(v3.0.0)
# std.data        DataFrame / Dataset / DataLoader / Scaler(v3.0.0)
# std.agent       Agent / Tool / PromptTemplate / RAG(v3.0.0)
# std.inference   InferenceEngine / InferenceServer / Quantizer(v3.0.0)
# std.kernel      Jupyter 内核(v3.0.0)
# std.ui          AuroraUI 跨平台 GUI 框架(v3.1.0)
# std.ffi         load / func / cstr(C ABI 互操作)
# std.python      eval / exec / import / call(Python 互操作)
# std.js          eval / call / require / run_file(JavaScript/TypeScript 互操作)
# std.java        call / run / eval / compile(Java 互操作)
# std.interop     call / import / eval / languages / status(统一多语言互操作层)
# std.wasm        load / call / exports(WebAssembly 互操作)
# std.html        escape / page / render / write / link / list / json_script
# std.proc        run / call / spawn(子进程)
# std.http        get / get_json / post
# std.vex         export / python / cpp(VEX 导出)
# std.regex       match / search / replace / groups(v2.0.0 P3 扩充)
# std.date        now / parse / format / add / diff(v2.0.0 P3 扩充)
# std.crypto      md5 / sha256 / hmac / random(v2.0.0 P3 扩充)
# std.fs          read_dir / walk / stat / remove / copy(v2.0.0 P3 扩充)
# std.net         tcp / udp / listen / dial(v2.0.0 P3 扩充)
```

### 大型项目:多文件模块 + AOT 编译

Aurora 支持真正的大型项目开发:分层模块、标准工程结构、AOT 编译为可部署产物。

```bash
# 创建标准工程结构
aurora new myapp
# myapp/
# ├── aurora.toml      项目清单(入口/依赖)
# ├── src/
# │   ├── main.aur     入口
# │   └── lib.aur      库模块
# └── tests/           测试

# 运行(读 aurora.toml 入口)
cd myapp && aurora run

# AOT 编译为 Python(输出 dist/,可直接部署)
aurora build
python3 dist/main.py
```

完整分层架构示例见 `examples/largeapp/`(models/services/utils/storage 四层,7 个模块文件)。

### v3.1.0 性能革命

v3.1.0 在 v2.0.0 ARM64 原生后端基础上,新增多项编译优化 Pass:

- **并行编译**:多模块并行编译,大型项目构建速度提升 3–5x
- **增量编译增强**:跨函数依赖追踪,仅重编译受影响模块
- **图着色寄存器分配**:线性扫描 → 图着色,减少寄存器溢出
- **指令调度**:重排指令减少流水线停顿
- **LICM**(循环不变量代码移动):把循环内不变计算提到循环外
- **CSE**(公共子表达式消除):消除重复计算
- **NEON SIMD**:自动向量化浮点循环,ARM NEON 指令
- **逃逸分析**:栈分配优先,减少堆分配与 GC 压力

**ARM64 原生汇编后端**:`aurora build-asm` 直接把 Aurora 编译成 ARM64 机器码,**不依赖 C 编译器**,直接发起系统调用。

**函数级增量编译缓存**:只重编译改动过的函数,大型项目二次构建从秒级降到毫秒级;缓存键基于函数源码哈希,跨会话生效。

**`@perf` 自适应性能注解**:五级优化策略,标注后编译器按级别自动选择内联、循环展开、常量折叠、逃逸分析等 Pass:

```python
# @perf level 0..4,自适应选择优化强度
@perf(3)
fn count_primes(n: int) -> int {
    let count = 0
    for i in 2..n {
        if is_prime(i) { count = count + 1 }
    }
    return count
}

# @perf(auto):编译器按函数复杂度自动定级
@perf(auto)
fn fib(n: int) -> int {
    if n < 2 { return n }
    return fib(n - 1) + fib(n - 2)
}
```

**基准性能(ARM64,对比 C++ -O3)**:

| 基准 | Aurora v3.1.0 | C++ -O3 | 说明 |
|---|---|---|---|
| `count_primes` (1e6) | **9.3 ms** | ~10 ms | **超越 C++ -O3** |
| `fib` (28) | **6.3 ms** | ~35 ms | **比 C++ 快 5.5x** |
| `loop_sum` (1e8) | **10.1 ms** | — | 原生汇编后端 + NEON SIMD |
| 启动时间 | **2 ms** | — | 零运行时预热 |
| 并行编译(100 模块) | **~0.3s** | — | v3.1.0 并行编译 |

### 全栈:HTML 前端 + Web 后端 + AI Agent

Aurora 一个文件即可提供完整 Web 应用:**HTML 前端由 Aurora 生成,HTTP 服务由 Aurora 启动,后端计算可调用 Rust / C++ / Python,AI Agent 自动调用工具**。完整示例见 `examples/fullstack/`。

```python
import std.web
import std.json

fn handle(path, method, query, body) {
    if path == "/" {
        return std.html.page("首页", "<h1>你好, Aurora</h1>")
    }
    if path == "/api/hello" {
        return {"message": "hello", "query": query}   # dict → JSON
    }
    return [404, "not found"]
}

let info = std.web.serve(8977, handle)   # 启动 HTTP 服务
println("服务: " + info["url"])
std.web.wait()                            # 常驻,直到 Ctrl-C
```

```python
import std.ai

# AI Agent:大模型决策,自动调用你写的 Aurora 函数
std.ai.configure(api_key: "你的密钥")     # 或环境变量 AURORA_AI_API_KEY

fn double(x) { x * 2 }

let r = std.ai.agent(
    "你是数学助手",
    {"double": {"fn": double, "desc": "把数字翻倍"}},
    "21 的两倍是多少?",
)
println(r["answer"])       # 模型调用 double(21) → 42 → 给出最终答案
```

- **`std.web`**:`serve(port, handler)`(dict→JSON / str→HTML / [status, body] 响应)、`static(port, dir)`、`wait()`
- **`std.ai`**:`configure(base_url, api_key, model)`(默认火山方舟/豆包)、`chat(prompt, system)`、`messages(msgs)`、`agent(system, tools, prompt)`(工具调用循环,返回 `{answer, steps, tool_calls}`)
- **`std.html`**:`escape / render / page / write / open / link / list / json_script`(数据嵌入页面)
- 支持任意 OpenAI 兼容服务:`AURORA_AI_BASE_URL` 可指向 Ollama 等本地模型

### 生态链:与外部世界互通

Aurora 是"有生态链"的语言:可编排多个程序协同,可连接各种库与语言。

```python
# ── JSON:与数据格式打通 ──
import std.json
let d = std.json.parse(r'{"a": 1, "b": [1, 2, 3]}')   # 原始字符串 r'...' 不插值
std.json.save("/tmp/d.json", d)                        # 文件读写
let back = std.json.load("/tmp/d.json")

# ── Python 桥:导入任意已安装库 ──
import std.python
let np = std.python.import("numpy")
println(np.__version__)
let m = std.python.import("math")
println(m.sqrt(81))                                    # 9.0
println(std.python.eval("1 + 2 * 3"))                  # 7

# ── FFI:与 Rust / C++ 打通 ──
import std.ffi
let lib = std.ffi.load("path/to/librust_math.dylib")   # Rust #[no_mangle] extern "C"
let add = std.ffi.func(lib, "add", ["i32", "i32"], "i32")
println(add(3, 4))                                     # 7

# ── HTML:数据渲染成网页 ──
import std.html
let doc = std.html.page("标题", std.html.render(
    r'<h1>{{title}}</h1>', {"title": "你好"}))
std.html.open("/tmp/page.html", doc)                   # 写入并在浏览器打开

# ── 多程序协同:一个 Aurora 程序编排其它程序 ──
import std.proc
let out = std.proc.call(
    r'python3 -m aurora.cli run worker.aur',           # 启动另一个 Aurora 程序
    r'{"nums": [1, 2, 3]}')                            # 经 stdin 传 JSON
let result = std.json.parse(out)                       # 经 stdout 收 JSON

# ── HTTP / Web API ──
import std.http
let data = std.http.get_json("https://api.example.com/data")

# ── VEX 机器人:导出 VEXcode 工程 ──
import std.vex
std.vex.python("/tmp", "my_robot", code_string)        # 生成 VEXcode Python 工程
std.vex.cpp("/tmp", "my_robot_cpp", cpp_string)        # 生成 VEXcode C++ 工程

# ── JavaScript/TypeScript 桥:Node.js 生态 ──
import std.js
std.js.eval("1 + 2 * 3")                       # 7
std.js.call("Math.sqrt", 81)                    # 9
std.js.require("os")                             # {"platform": "darwin", ...}
std.js.run_file("script.ts")                     # 运行 TypeScript

# ── Java 桥:JVM 生态 ──
import std.java
std.java.eval("1 + 2 * 3")                      # 7 (jshell)
std.java.call("java.lang.Math", "sqrt", 81.0)   # 9.0
std.java.call("java.lang.Integer", "parseInt", "100")  # 100

# ── WebAssembly 桥:Rust/Go/C++ 编译为 WASM ──
import std.wasm
let wasm_mod = std.wasm.load("math.wasm")
std.wasm.call(wasm_mod, "add", 3, 4)           # 7
std.wasm.exports("math.wasm")                    # 列出导出函数

# ── 统一互操作层:一个 API 调用所有语言 ──
import std.interop
std.interop.eval("python", "1 + 1")              # 2 (直连)
std.interop.eval("js", "1 + 1")                   # 2 (Node.js)
std.interop.eval("java", "1 + 1")                 # 2 (JVM)
std.interop.call("js", "parseInt", "42")          # 42
std.interop.languages()                            # 支持的语言列表
std.interop.status()                               # 各语言桥状态
```

完整示例见 `examples/interop/`(含 Rust/C++ 库源码与构建命令)。

### 字符串插值

```python
let name = "aurora"
println("hello {name}")                 # 变量
println("sum={1 + 2 * 3}")              # 任意表达式
println("len={[1,2,3].len()}")          # 方法调用
println("literal {{braces}}")           # 转义为 {braces}

# 原始字符串 r'...' / r"..." :不插值、反斜杠保留
# 适合书写 JSON、正则、Windows 路径、外部代码片段
let raw = r'{"a": 1}   # 不会触发 {a} 插值
let re  = r'\.\d+'
```

### 现代语法糖

```python
# 可选链 ?.:左侧为 nil 时整体安全得到 nil
let user = { "name": "Aurora" }
println(user?.name)      # Aurora
println(user?.email)     # nil
println(nil?.name)       # nil

# 空合并 ??:左侧为 nil 时取右侧默认值
let port = nil ?? 8697            # 8697
let name = user?.name ?? "无名"    # Aurora

# 可选链方法调用
println([1, 2, 3]?.len())  # 3

# if / match / 代码块都是表达式,可直接作为值
let grade = if score >= 90 { "A" } else { "B" }

# 换行是语句边界:新一行以 ( 开头不会当作上一行的调用参数
let s = 1 + 2
(s * 2)          # 独立语句,不是 1 + 2(s*2)

# 注释支持 // 与 #;nil 打印为 nil
```

### ZL 设计特性(v0.3.0)

```python
# let 不可变绑定 / var 可变绑定(赋值给 let 会报错)
let max_retry = 3
var count = 0
count = count + 1

# 管道 |>:左侧值作为右侧调用的最后一个参数,数据流式书写
fn double(x) { x * 2 }
fn add(a, b) { a + b }
10 |> double |> add(1)     # 21
[1, 2, 3] |> len           # 3

# 区间 a..b:闭区间(含 b),可直接迭代
for i in 1..5 { print(i) }   # 12345
1..3 |> len                  # 3

# 模式解构:let (a, b) = ... / let [x, y] = ... / let (k, v) = dict
let (x, y) = (3, 4)
let [a, b, c] = [1, 2, 3]
let p = {"name": "A", "age": 1}
let (name, age) = p

# defer:函数退出时按 LIFO 执行;调用参数在注册时求值
fn work() {
    defer println("cleanup")
    defer { save_state() }
    # ... 提前 return 也会执行 defer
}

# yield:生成器,函数调用返回收集的列表
fn squares(n) { for i in 1..n { yield i * i } }
squares(4)     # [1, 4, 9, 16]
```

### 测试与断言

```python
test "addition" {
    assert 1 + 1 == 2
}

assert 2 > 1, "custom message"
```

## Aurora IDE(macOS 应用)

Aurora 自带一个 **VSCode 风格**的原生 macOS 编程 IDE,以代码编辑为核心:文件浏览器、多标签编辑器、运行、静态检查、问题面板一应俱全。

```bash
# 方式一:双击启动(Finder 中双击即可,推荐)
open "aurora/Aurora IDE.app"

# 方式二:命令行启动(自动打开浏览器)
./aurora/ide/aurora-ide
```

应用特点:

- **原生窗口**:基于 pywebview 的内嵌 WebView 窗口(非浏览器标签),Dock 图标 + 应用菜单栏;启动时自动拉起本地服务,退出自动回收
- **活动栏 + 侧边栏**:文件资源管理器(工作区 = aurora 项目根,自动忽略 .git/__pycache__ 等)
- **多标签编辑器**:语法高亮、行号、Tab 缩进、错误行标红、脏标记;`⌘N` 新建、`⌘S` 保存、`⌘W` 关闭标签、`⌘B` 折叠侧边栏
- **▶ 运行**(`⌘R`):结果输出到底部「输出」面板,支持 stdin 输入;超时/错误自动进入「问题」面板,点击可跳转到出错行
- **检查**(`⌘K`):类型检查 + 所有权检查,错误列表点击定位
- **状态栏**:光标行列、错误计数、编码、端口状态

语言能力完整保留:输入输出、位运算、函数与闭包、递归与深度优先搜索、集合与高阶函数、类型/枚举/match、协程与通道、可选链与空合并。

手动启动服务:

```bash
cd aurora/ide && python3 server.py --open
```

## 命令行工具

| 命令 | 说明 |
|---|---|
| `aurora repl` | 交互式 REPL（`:help` 查看命令） |
| `aurora run [<file>]` | 运行 .aur 文件；无参数时读取 `aurora.toml` 入口 |
| `aurora build [<file>] [-o dist]` | AOT 编译为 Python 源码，输出到 `dist/`，可直接 `python3` 运行 |
| `aurora build-native <file> [-o out] [-O -O3]` | 原生编译为机器码（Aurora → C → 原生可执行文件），需系统 C 编译器 |
| `aurora build-asm <file> [-o out]` | ARM64 汇编编译（Aurora → 汇编 → 原生可执行文件），**不依赖 C 编译器**，直接使用系统调用 |
| `aurora check <file>` | 类型检查 + 所有权检查（不执行） |
| `aurora fmt [path]` | **(P2)** 代码格式化：统一缩进 / 换行 / 引号 / 管道链风格 |
| `aurora profile <file>` | **(P2)** 性能分析：函数级耗时火焰图 + 热点报告 |
| `aurora debug <file>` | **(P2)** 调试器：断点 / 单步 / 变量查看 / 调用栈 |
| `aurora lsp` | **(P2)** LSP 语言服务器：补全 / 跳转定义 / 悬停文档 / 诊断（VSCode 插件对接） |
| `aurora pkg` | **(P3)** 包管理器：依赖解析、版本锁定、发布到本地 registry |
| `aurora eval '<code>'` | 执行一行代码 |
| `aurora new <name>` | 创建工程化脚手架（`aurora.toml` + `src/main.aur` + `src/lib.aur` + `tests/`） |
| `aurora test [path]` | 测试运行器：`*_test.aur`/`*_tests.aur` 整体运行，`test_*` 函数逐项运行 |
| `aurora tokens <file>` | 显示词法分析结果 |
| `aurora ast <file>` | 显示 AST 结构 |
| `aurora ai train <file>` | **(v3.0.0)** AI 训练模式 |
| `aurora ai infer <file>` | **(v3.0.0)** AI 推理模式 |
| `aurora serve <model.aur>` | **(v3.0.0)** 启动 HTTP 推理服务 |
| `aurora kernel install` | **(v3.0.0)** 注册 Jupyter 内核 |
| `aurora bench [path]` | **(v3.1.0)** 性能基准测试 |
| `aurora workspace` | **(v3.1.0)** 工作区 Monorepo 管理 |
| `aurora deps` | **(v3.1.0)** 依赖图解析与管理 |
| `aurora ui <file>` | **(v3.1.0)** 启动 AuroraUI GUI 应用 |
| `aurora package <target> <file>` | **(v3.1.0)** 跨平台打包(macos/windows/linux/web) |
| `aurora interop` | **(v2.2.0)** 语言互操作 |
| `aurora gen-bindings <header.h>` | **(v2.2.0)** 自动生成 FFI 绑定代码 |
| `aurora wasm <file>` | **(v2.2.0)** 编译为 WebAssembly |
| `aurora new {fullstack,cli,tui,microservice,webapp}` | **(v3.2.0)** 按模板创建全栈/CLI/TUI/微服务/Web 应用脚手架 |
| `aurora generate {controller,model,component,service}` | **(v3.2.0)** 代码生成器:生成 controller/model/component/service |
| `aurora db {migrate,rollback,seed}` | **(v3.2.0)** 数据库迁移/回滚/种子数据 |
| `aurora dev` | **(v3.2.0)** 开发服务器:热重载 + 自动重启 |
| `aurora deploy` | **(v3.2.0)** 一键部署到生产环境 |
| `aurora --version` | 版本信息 |

REPL 内建命令：`:type <expr>` 显示类型、`:ast <code>`、`:tokens <code>`、`:env` 查看环境、`:clear`、`:quit`。

## 正式文档

- **语言规范** `docs/SPEC.md` — 词法 / 类型 / 语义 / 模块 / 生态 / 工具链完整定义
- **版本策略** `docs/VERSIONING.md` — 语义化版本、稳定性分级、兼容承诺
- **变更日志** `CHANGELOG.md` — 逐版本变更记录

## 目录结构

```
aurora/
├── __init__.py        包定义与版本
├── __main__.py        python -m aurora 入口
├── cli.py             命令行工具
├── repl.py            交互式 REPL
├── lexer.py           词法分析器
├── tokens.py          Token 定义
├── parser.py          递归下降 + Pratt 解析器
├── ast_nodes.py       AST 节点定义
├── type_checker.py    渐进式类型推断与检查
├── ownership.py       Rust 风格所有权/借用检查
├── interpreter.py     树遍历解释器
├── stdlib.py          标准库（io/math/str/time/json/sync/result）
├── tests/             单元测试套件
├── pyproject.toml     打包配置
└── ide/               教学工坊 WebIDE（lessons/server/worker/static）
```

## 测试

```bash
python3 -m unittest discover -s aurora/tests -v
# 825+ 个用例全部通过,覆盖词法、语法、解释器、类型检查、所有权检查、
# ARM64 后端、@perf 优化 Pass、Result 互操作、增量编译缓存,
# v3.0.0 AI 引擎(tensor / autograd / nn / data / agent / inference),
# v3.1.0 企业级特性(并行编译 / 模块化 / AuroraUI / 打包 / LSP / 调试器),
# 以及 v3.2.0 全栈开发特性(Web 框架 / ORM / CLI / TUI / Git 绑定 / 代码生成器 / 语言级增强)
```

## 已知限制

- 类型检查与所有权检查是编译期"把关者"：`run` 默认以警告模式运行，`--strict` 可强制拦截
- 所有权检查聚焦不可变变量与借用冲突；函数参数移动语义暂按简化处理
- 引用 `&x` 在运行时是值语义的简化实现（不做真实别名追踪）
- `select` 采用短轮询调度，适用于教学与原型场景
- trait 泛型约束（`T: Trait`）尚未接入类型检查器
- `reduce` 参数序约定为 `reduce(初始值, 函数)`，同时兼容经典写法 `reduce(函数)`
- 位与 `&` 优先级低于 `==`（与 C 相反），逻辑链 `&&` 位于最低优先级——这是当前固定的语义，教学按此讲授

## License

MIT
