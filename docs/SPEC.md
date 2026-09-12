# Aurora 语言规范 v1.0.0

> 状态: **Stable(稳定)** — 自 v1.0.0 起,本规范描述的语言行为受语义化版本约束,破坏性变更须进入下一主版本。
> 实现: 纯 Python 解释器(零第三方依赖),位于 `aurora/` 包;CLI 入口 `aurora`。

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
`fn let var const if elif else for while return type enum impl match trait true false nil in break continue import from as spawn chan select default try catch finally panic self std and or not loop pub mut defer yield`

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

## 7. 并发

```python
spawn(fn, *args)              # 协程
chan(capacity)                # 通道
ch.send(v) / ch.recv()        # 收发
select { case x => ch1.recv(), ... }
```

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

## 9. 静态检查

```bash
aurora check main.aur
```
运行类型检查器与所有权检查器(不执行);`aurora run --strict` 在检查失败时终止。

## 10. 工具链

```
aurora repl            交互式 REPL
aurora run [file]     运行 .aur 或读 aurora.toml 入口
aurora eval 'code'    执行一行
aurora check file     类型/所有权静态检查
aurora new name       创建项目(脚手架 + 清单)
aurora test [path]    测试运行器(*_test.aur / *_tests.aur 整体运行;test_* 函数逐项运行)
aurora tokens file    词法分析
aurora ast file       AST 结构
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
- 破坏性变更(如 `let` 语义)仅允许在 MAJOR 版本发布;
- 详细策略见 `VERSIONING.md`,历史见 `CHANGELOG.md`。

## 13. 已知限制(roadmap)

以下特性不属于 v1.0.0 稳定承诺,计划在未来主版本演进:
- 编译后端(LLVM/JIT)与 AOT 产物;
- 泛型单态化、trait 约束求解;
- 定宽整数 `i32`/`u64` 等显式类型;
- 所有权/借用作为强制的编译期语义;
- 包管理器与依赖解析、注册表。

## 14. 生态示例

见 `examples/interop/`:与 Rust、C++、Python、JSON、HTML、VEX、HTTP、多进程协同的可运行示例。
