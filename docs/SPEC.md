# Aurora 语言规范 v3.1.0

> 状态: **Stable(稳定)** — 自 v2.0.0 起,本规范描述的语言行为受语义化版本约束,破坏性变更须进入下一主版本。
> 实现: ARM64 原生汇编后端 + 解释器双模式 + AI 原生引擎 + 全平台企业级引擎,位于 `aurora/` 包;CLI 入口 `aurora`。

---

## 1. 设计目标

Aurora 是一门**融合现代语言优势的可学习编程语言**,面向教育、脚本与生态集成:

- **消除歧义**:C++ "同一件事多种写法"的歧义(声明、初始化、解析)被统一消灭;
- **表达式导向**:`if` / `match` / `loop` / 代码块都有值,函数体最后一个表达式即返回值;
- **安全默认**:类型检查器 + 所有权检查器在运行前静态检查,运行时错误带 `L行:C列` 定位;
- **生态链**:内置标准库模块与 FFI,可与 JSON / Python / Rust / C++ / HTML / VEX / HTTP 互通;
- **工具完备**:REPL、测试运行器、静态检查、脚手架、IDE(.app)、VSCode 插件。

## 2. 词法

### 2.1 注释
- `//` 行注释(推荐)
- `#` 行注释

### 2.2 字面量

| 类别 | 写法 | 示例 |
| --- | --- | --- |
| 整数 | 十进制 | `42`, `-17` |
| 浮点 | 十进制小数点 | `3.14`, `1e3` |
| 布尔 | `true` / `false` | |
| 空值 | `nil` | |
| 字符串 | `"..."` 或 `'...'` | `"hi"`, `'hi'` |
| 原始字符串 | `r"..."` 或 `r'...'` | `r'{"a": 1}'`(不插值、反斜杠保留) |
| 字符/字节 | 字符串中的转义 | `\n \t \r \\ \" \' \0` |

### 2.3 字符串插值
普通字符串中 `{expr}` 求值替换,`{{`/`}}` 转义为字面花括号:

```python
let name = "aurora"
"hello {name}"          # hello aurora
"sum={1 + 2 * 3}"       # sum=7
"literal {{braces}}"    # literal {braces}
```

原始字符串 `r'...'` 不做任何插值与转义处理,用于 JSON、正则、路径、外部代码片段。

### 2.4 标识符与关键字

标识符: `[A-Za-z_][A-Za-z0-9_]*`。

关键字:
`fn let var const if elif else for while return type enum impl match trait true false nil in break continue import from as spawn chan select default try catch finally panic self std and or not loop pub mut defer yield async await unsafe extern`

### 2.5 运算符

```
算术   +  -  *  /  %  **
比较   ==  !=  <  <=  >  >=
逻辑   and  or  not  &&  ||  !
位     &  |  ^  ~  <<  >>
赋值   =  +=  -=  *=  /=  %=
其他   |>  ..  ?.  ??  ->  =>
区间   a..b(闭区间)
管道   x |> f(args)  左侧值作为右侧调用的最后一个参数
可选链 obj?.m / obj ?? 默认
```

## 3. 类型系统

### 3.1 基本类型(运行时动态,静态检查可选)
整数 / 浮点 / 布尔 / 字符串 / nil;`type(x)` 返回类型名。

### 3.2 复合类型
- 列表: `[1, 2, 3]` — 方法 `push pop map filter reduce(init, fn) contains len join clone append`
- 字典: `{"k": "v"}` — 方法 `keys values items get clone`
- 元组: `(1, "x")` — 可解构
- 区间: `1..5` → `[1, 2, 3, 4, 5]`(闭区间)

### 3.3 自定义类型
```python
type Point { x, y }            # 结构体
type Shape {
    Circle(radius),            # 标签联合(替代继承建模)
    Rect(w, h),
}
impl Shape {
    fn area(self) {
        match self {
            Circle(r) => 3.14 * r * r,
            Rect(w, h) => w * h,
        }
    }
}
```

### 3.4 空值安全
无空指针;可空值用 `nil` 表示,可选链 `obj?.field` 与空合并 `a ?? b` 提供安全访问。

## 4. 声明与绑定

```python
let x = 1          # 不可变绑定(赋值报错)
var y = 1          # 可变绑定
let mut z = 1      # 兼容写法(可变)
y = y + 1

fn add(a, b) { a + b }           # 函数,末表达式即返回值
fn greet(name, punct: "!") { }   # 默认参数
fn draw(w, h, color) { }         # 具名调用 draw(color: "red", w: 1, h: 2)

type T { f }                     # 类型
enum E { A, B }                  # 枚举
```

### 4.1 @perf 性能注解(v2.0.0)

函数级自适应性能注解,放在函数声明前一行:

```python
@perf(critical)
fn hot_path(a, b) { a * b + loop_sum(10000) }

@perf(hot)
fn frequent(x) { ... }

@perf(cold)
fn error_handler(msg) { ... }

@perf(size)
fn utility() { ... }

@perf(trace)
fn monitored() { ... }
```

| level | 编译器策略 |
| --- | --- |
| `critical` | 内联 + 循环展开4次 + 向量化提示 + 寄存器全分配 |
| `hot` | 内联 + 循环展开2次 |
| `cold` | 不优化,最小化体积 |
| `size` | 优化代码大小 |
| `trace` | 自动插入性能追踪(计时/调用计数) |

未标注 `@perf` 的函数采用默认优化策略。

## 5. 语句与控制流

```python
if score >= 90 { "A" } elif score >= 60 { "B" } else { "C" }   # 有值
for i in 1..5 { print(i) }       # 区间迭代(含 5)
for x in items { }               # 集合迭代
while cond { }
match v { 1 => "one", _ => "other" }

return            # 仅提前退出用
defer println("cleanup")   # 函数退出 LIFO;参数注册时求值;支持 { } 块
yield v           # 生成器:函数含 yield 即生成器,调用返回收集列表
break / continue
```

## 6. 模块系统

- **文件即模块**,`import` 引入,无头文件 / 前向声明 / include guard;
- 标准库注册表 `std.*`:

```
std.io      read_file write_file append_file exists read_line list_dir mkdir is_dir files
std.math    PI E abs sqrt pow floor ceil round min max sin cos tan log random randint
std.str     split join replace contains starts_with ends_with trim upper lower format
std.time    now sleep timestamp format
std.json    parse stringify load save
std.sync    Channel Mutex Fiber
std.result  Ok Err Result
std.python  eval exec import call version        # Python 生态桥
std.ffi     load func cstr                        # C ABI 共享库(Rust/C++)
std.html    escape render page write open link list json_script   # HTML 前端组件
std.proc    run call spawn run_args call_args     # 进程编排(多程序协同)
std.http    get get_json post                     # HTTP/API
std.vex     export python cpp                     # VEXcode 工程导出
std.web     serve static wait                     # Web 后端(HTTP 服务)
std.ai      configure chat messages agent         # AI Agent(大模型对话/工具调用)
```

- **`std.web`**:`serve(port, handler, host)` 启动 HTTP 服务(后台线程),handler 返回 `dict`→JSON、`str`→HTML、`[status, body]` 或 `[status, headers, body]`;`static(port, dir)` 静态文件服务;`wait()` 阻塞保持服务常驻。
- **`std.ai`**:OpenAI 兼容协议。`configure(base_url, api_key, model)`(默认火山方舟 / 豆包);`chat(prompt, system)`、`messages(msgs)` 对话;`agent(system, tools, prompt, max_steps)` 工具调用式 Agent——大模型决策→调用 Aurora 函数→结果回填→收敛,返回 `{answer, steps, tool_calls}`。Key 从 `AURORA_AI_API_KEY` / `DOUBAO_API_KEY` / `OPENAI_API_KEY` 读取或显式配置。

导入语法:
```python
import std.io                     # std.io.exists(...)
import std.math as m              # m.sqrt(16)
from std.json import parse        # parse(...)
```

### 6.1 模块化系统增强(v3.1.0)

**`pub` 关键字**:导出模块内的函数、类型、常量为公开接口,供其他模块导入使用。未标注 `pub` 的成员仅模块内可见。

```python
// math_utils.aur
pub fn add(a: int, b: int) -> int { a + b }
pub const PI = 3.14159
fn internal_helper(x) { ... }     // 私有,外部不可导入
```

```python
// main.aur
import math_utils
math_utils.add(1, 2)              // 可用
// math_utils.internal_helper()   // 编译错误:私有成员
```

**模块解析**:编译器按以下顺序搜索模块:当前目录 → `src/` → 项目根目录;支持嵌套目录 `import services.task_service`。

**循环依赖检测**:编译器在构建依赖图时自动检测循环 import,检测到时报告具体循环路径并终止编译。

**工作区 Monorepo**:`aurora workspace` 管理多项目工作区,`aurora deps` 解析跨项目依赖图。

### 6.2 条件编译(v3.1.0)

`#[cfg(...)]` 属性按目标平台 / 配置条件编译代码块:

```python
#[cfg(target: "macos")]
fn platform_specific() { ... }    // 仅 macOS 编译

#[cfg(target: "windows")]
fn platform_specific() { ... }    // 仅 Windows 编译

#[cfg(debug)]
fn debug_log(msg) { ... }         // 仅 Debug 构建编译
```

支持的 cfg 谓词:`target: "macos" | "windows" | "linux" | "web"`, `debug`, `release`, `feature: "..."`。

## 7. 并发

```python
spawn(fn, *args)              # 协程
chan(capacity)                # 通道
ch.send(v) / ch.recv()        # 收发
select { case x => ch1.recv(), ... }
```

### 7.1 async/await(v3.1.0)

`async fn` 声明异步函数,调用返回协程;`await` 等待异步操作完成:

```python
async fn fetch_data(url: str) -> str {
    let resp = await http_get(url)
    return resp.body
}

async fn main() {
    let a = await fetch_data("https://a.example.com")
    let b = await fetch_data("https://b.example.com")
    print(a + b)
}
```

- `async fn` 可在内部使用 `await`;普通函数不可使用 `await`
- 并发执行多个异步操作用 `spawn` + `await` 组合
- 事件循环由运行时自动管理,无需手动驱动

### 7.2 defer(v3.1.0 正式化)

`defer` 语句注册函数退出时按 LIFO 顺序执行的清理动作,参数在注册时求值:

```python
fn process() {
    let f = open("file.txt")
    defer f.close()
    // ... 提前 return 或异常退出,defer 仍会执行
}
```

### 7.3 unsafe 与 extern "C"(v3.1.0)

`unsafe` 块标记不安全操作区域(FFI 调用、裸指针操作),编译器对 unsafe 块内不做安全检查:

```python
unsafe {
    let lib = std.ffi.load("libmylib.dylib")
    let add = std.ffi.func(lib, "add", ["i32", "i32"], "i32")
    println(add(3, 4))
}
```

`extern "C"` 声明 C ABI 外部函数,用于与 C/Rust/C++ 共享库互操作:

```python
extern "C" {
    fn puts(s: str) -> int
    fn malloc(size: int) -> rawptr
    fn free(ptr: rawptr)
}
```

- `extern "C"` 块内的函数声明不生成实现,链接时从共享库解析
- `rawptr` 类型仅在 unsafe 块内可用
- FFI 调用必须在 `unsafe` 块中

## 8. 错误处理

```python
try {
    risk_call()
} catch e {
    println("出错: " + str(e))
} finally { }

assert(cond, "消息")     # 断言,失败抛 AssertError
panic("消息")            # 主动终止
```

错误消息统一格式:`L<行>:C<列>: [<类别>] <描述>`,类别含 `AuroraError TypeError NameError ValueError KeyError IndexError MathError AssertError TimeoutError JsonError PythonError FFIError ProcError HttpError VexError ...`。

### 8.1 Result 类型与互操作(v2.0.0)

**Result 类型标注**:函数可声明返回 `Result[T, E]`:

```python
fn divide(a: int, b: int) -> Result[int, str] {
    if b == 0 { return Err("除数为零") }
    return Ok(a / b)
}
```

**构造**:`Ok(value)` 包装成功值,`Err(error)` 包装错误。

**`?` 操作符**:仅在返回 `Result` 的函数体中可用。作用于 `Result` 值时,若为 `Ok(v)` 自动解包为 `v`;若为 `Err(e)`,自动 `return Err(e)` 传播:

```python
fn safe_divide(a, b) -> Result[int, str] {
    let r = divide(a, b)?    # b==0 时自动 return Err("除数为零")
    Ok(r * 2)
}
```

**自动解包规则**:声明 `-> Result[T, E]` 的函数,其返回值在调用处自动解包为裸值 `T`(或在 `Err` 时传播);未声明 `-> Result` 的旧式 `Result` 返回保持兼容,需手动 `.unwrap()`。

**try/catch 与 Result 互操作**:`try/catch` 可捕获 `?` 操作符传播的 `Err` 异常,`catch` 绑定到异常对象:

```python
try {
    divide(10, 0)
} catch e {
    println("捕获到: " + str(e))   # Err 传播的错误
}
```

## 9. 静态检查

```bash
aurora check main.aur
```
运行类型检查器与所有权检查器(不执行);`aurora run --strict` 在检查失败时终止。

## 10. 工具链

```
aurora repl            交互式 REPL
aurora run [file]     运行 .aur 或读 aurora.toml 入口(自动选择解释器/ARM64 后端)
aurora eval 'code'    执行一行
aurora check file     类型/所有权静态检查
aurora new name       创建项目(脚手架 + 清单)
aurora test [path]    测试运行器(*_test.aur / *_tests.aur 整体运行;test_* 函数逐项运行)
aurora tokens file    词法分析
aurora ast file       AST 结构
aurora fmt file       代码格式化(v2.0.0)
aurora profile file   性能分析(v2.0.0)
aurora debug file     调试器(v2.0.0)
aurora lsp            LSP 语言服务器(v2.0.0)
aurora pkg install X  包管理器(v2.0.0)
aurora ai train/infer    AI 训练/推理(v3.0.0)
aurora serve model.aur   推理服务(v3.0.0)
aurora kernel install    Jupyter 内核(v3.0.0)
aurora bench             性能基准测试(v3.1.0)
aurora workspace         工作区管理(v3.1.0)
aurora deps              依赖管理(v3.1.0)
aurora ui                GUI 应用(v3.1.0)
aurora package           跨平台打包(v3.1.0)
aurora interop           语言互操作(v2.2.0)
aurora gen-bindings      绑定代码生成(v2.2.0)
aurora wasm              WebAssembly(v2.2.0)
aurora --version      版本
```

### 项目清单 aurora.toml
```toml
[project]
name = "myapp"
version = "0.1.0"
description = "Aurora 项目"
author = ""

[build]
entry = "main.aur"
```

## 11. 内存与安全模型

- **值语义**:无手动 `free`/`delete`,无 GC(解释器托管);
- **所有权检查器**:静态检查借用/所有权冲突(可选启用);
- **无未定义行为**:越界、除零、空值访问均产生带定位的运行时错误;
- **整型溢出**在 Debug 路径检查。

## 12. 版本与稳定性

- 语义化版本 `MAJOR.MINOR.PATCH`;
- **Stable** 特性:本规范第 2–11 章描述的全部语法与标准库;
- v2.0.0 新增稳定内容:ARM64 原生汇编后端、@perf 性能注解、Result[T,E]/`?` 互操作、函数级增量编译缓存、P2 工具链(fmt/profile/debug/lsp)、P3 包管理器与标准库扩充;
- v3.0.0 新增稳定内容:AI 原生引擎七模块(std.tensor/autograd/nn/data/agent/inference/kernel)、@ai 注解、aurora ai/serve/kernel 命令;
- v3.1.0 新增稳定内容:并行编译、增量编译增强、图着色寄存器分配、指令调度、LICM、CSE、NEON SIMD、逃逸分析、模块化系统(pub/import/循环依赖检测)、#[cfg] 条件编译、工作区 Monorepo、LSP 企业级增强、调试器增强、AuroraUI 跨平台 GUI 框架、macOS/Windows/Web 原生绑定、全平台打包、新关键字 pub/async/await/defer/unsafe/extern "C";
- 破坏性变更(如 `let` 语义)仅允许在 MAJOR 版本发布;
- 详细策略见 `VERSIONING.md`,历史见 `CHANGELOG.md`。

## 13. 已知限制(roadmap)

以下特性已在 v2.0.0 纳入稳定承诺:
- ✅ ARM64 原生汇编后端(asmgen.py),不依赖 C 编译器;
- ✅ 包管理器 `aurora pkg` 与依赖解析;
- ✅ @perf 自适应性能注解(五级);
- ✅ Result[T,E] 类型标注、`?` 操作符、自动解包、try/catch 互操作;
- ✅ 函数级增量编译缓存(AST 哈希 + 磁盘持久化 + 调用图依赖跟踪)。

以下特性仍属 roadmap,计划在未来主版本演进:
- 泛型单态化、trait 约束求解;
- 定宽整数 `i32`/`u64` 等显式类型;
- 所有权/借用作为强制的编译期语义。

## 14. 生态示例

见 `examples/interop/`:与 Rust、C++、Python、JSON、HTML、VEX、HTTP、多进程协同的可运行示例。
