# Aurora 语言 AI 开发指南

> 本文档专为 AI 助手设计,阅读后即可编写、解释和调试 Aurora 代码。
> 版本:v1.2.0 | 实现:纯 Python 解释器(零依赖)| CLI:`aurora run file.aur`

---

## 0. 一句话定位

Aurora 是一门**表达式导向、静态检查、生态互通**的现代编程语言。语法类似 Rust/Python 混合,运行方式为解释执行或 AOT 编译为 Python。

```bash
aurora run main.aur      # 解释执行
aurora build             # AOT 编译为 Python(输出 dist/)
aurora repl              # 交互式
aurora new myapp         # 脚手架(src/ + tests/ + aurora.toml)
```

---

## 1. 语法速查

### 1.1 变量

| 写法 | 语义 | 示例 |
|---|---|---|
| `let x = 5` | 不可变绑定 | `let pi = 3.14` |
| `var x = 5` | 可变绑定 | `var count = 0` |
| `let x: i32 = 5` | 带类型标注(可选) | |
| `const x = 5` | 编译期常量 | |

**规则**:let 绑定不可重新赋值,否则报 `不可变绑定` 错误。需要修改用 var。

### 1.2 函数

```rust
fn add(a, b) {
    a + b                    // 最后一个表达式即返回值
}

fn greet(name: string) -> string {
    return "Hello, " + name   // return 仅用于提前退出
}

fn multi(a, b) {
    let sum = a + b
    let prod = a * b
    sum + prod                // 返回最后一个表达式
}

// 调用
add(3, 4)                     // 7
```

### 1.3 控制流

```rust
// if 是表达式,有值
let x = if score >= 60 { "pass" } else { "fail" }

// for 循环
for i in range(5) {
    println(i)
}
for item in arr {
    println(item)
}
for i, item in enumerate(arr) {
    println(str(i) + ": " + str(item))
}

// while
while n > 0 {
    n = n - 1
}

// loop + break/continue
loop {
    if done { break }
}
```

### 1.4 数据结构

```rust
// 数组(动态)
let arr = [1, 2, 3]
arr.push(4)
arr.len()                     // 4
arr[0]                        // 1
arr.contains(2)               // true

// Map(字典)
let m = {"name": "Aurora", "version": 1.2}
m["name"]                     // "Aurora"
m["new"] = "value"
m.keys()                      // ["name", "version", "new"]
m.values()

// 元组
let t = (1, "hello", true)
t.0                           // 1
t.1                           // "hello"
```

### 1.5 字符串

```rust
let s = "hello"
s + " world"                  // 拼接
s.len()                       // 5
s.upper()                     // "HELLO"
s.trim()
s.split(",")                  // 数组
s.replace("a", "b")
s.contains("ell")             // true
s.starts_with("he")           // true

// 插值
let name = "world"
"hello {name}"                // "hello world"
"sum={1 + 2}"                 // "sum=3"

// 原始字符串(不插值、不转义)——JSON/正则/外部代码必须用
let json = r'{"key": "value"}'
```

### 1.6 现代语法糖

```rust
// 管道 |> (左边结果作为右边函数的最后一个参数)
let result = [1, 2, 3] |> sum |> str
// 等价于 str(sum([1, 2, 3]))

// 区间 a..b
for i in 0..5 {
    println(i)                // 0,1,2,3,4
}

// 可选链 ?. 和空合并 ??
let v = obj?.field ?? "default"

// 模式解构
let (a, b) = (1, 2)
let [first, ...rest] = arr

// defer(函数返回前执行)
fn process() {
    let f = std.io.read_file("data.txt")
    defer println("清理资源")
    // ... 使用 f
}

// yield 生成器
fn gen() {
    yield 1
    yield 2
    yield 3
}
```

### 1.7 类型系统

```rust
// 自定义类型(type = struct)
type Point {
    x: f64
    y: f64
}

// 枚举
type Color = enum {
    Red
    Green
    Blue
    Rgb(r: u8, g: u8, b: u8)
}

// trait(接口)
trait Drawable {
    fn draw(self)
}

// impl(为类型实现 trait 或方法)
impl Point {
    fn distance(self, other: Point) -> f64 {
        std.math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    }
}

// match 模式匹配
match color {
    Color.Red => println("red")
    Color.Rgb(r, g, b) => println("rgb({r},{g},{b})")
    _ => println("other")
}
```

### 1.8 错误处理

```rust
// 断言
assert x > 0, "x 必须为正"

// panic(不可恢复错误)
panic("发生了严重错误")

// Result 类型(可恢复错误)
from std.result import Ok, Err

fn divide(a, b) {
    if b == 0 { return Err("除数为零") }
    Ok(a / b)
}

let r = divide(10, 2)
if r.is_ok() {
    println("结果: " + str(r.unwrap()))
}
```

### 1.9 并发

```rust
// 通道
let ch = std.sync.Channel()

// 轻量线程(Fiber)
spawn {
    ch.send("hello from fiber")
}

let msg = ch.recv()
println(msg)

// Mutex
let mtx = std.sync.Mutex(0)
// ...
```

### 1.10 模块与导入

```rust
// 标准库
import std.io
import std.math as m
from std.json import parse, stringify

// 本地模块(同目录或 src/ 下的 .aur 文件)
import utils                    // 加载 utils.aur
from utils import helper        // 导入指定函数
import services.task_service    // 加载 services/task_service.aur

// 模块内函数通过命名空间访问
std.io.read_file("data.txt")
m.sqrt(16)
```

---

## 2. 标准库完整清单

### std.io — 文件与输入输出
| 函数 | 说明 |
|---|---|
| `read_file(path)` | 读取文件全部内容为字符串 |
| `write_file(path, content)` | 写入文件 |
| `append_file(path, content)` | 追加写入 |
| `exists(path)` | 文件/目录是否存在 |
| `is_dir(path)` | 是否为目录 |
| `list_dir(path)` | 列出目录内容(数组) |
| `mkdir(path)` | 创建目录 |
| `files(dir, ext)` | 列出指定扩展名文件 |
| `read_line(prompt)` | 读取一行输入 |

### std.math
| 函数 | 说明 |
|---|---|
| `sqrt(x)`, `pow(a,b)`, `floor(x)`, `ceil(x)`, `round(x)` | 基础数学 |
| `abs(x)`, `min(a,b)`, `max(a,b)` | |
| `sin(x)`, `cos(x)`, `tan(x)`, `log(x)` | 三角/对数 |
| `random()`, `randint(a,b)` | 随机数 |
| `PI`, `E` | 常量 |

### std.str — 字符串工具
| 函数 | 说明 |
|---|---|
| `split(s, sep)`, `join(arr, sep)`, `replace(s, old, new)` | |
| `contains(s, sub)`, `starts_with(s, p)`, `ends_with(s, p)` | |
| `trim(s)`, `upper(s)`, `lower(s)` | |
| `find(s, sub, start)`, `substring(s, start, end)`, `len(s)`, `char_at(s, i)` | |

### std.json
| 函数 | 说明 |
|---|---|
| `parse(s)` | JSON 字符串 → Aurora 值 |
| `stringify(v)` | Aurora 值 → JSON 字符串 |
| `load(path)` | 从文件加载 JSON |
| `save(path, v)` | 保存 JSON 到文件 |

### std.http — HTTP 请求
| 函数 | 说明 |
|---|---|
| `get(url, timeout)` | GET 请求,返回响应文本(自动带浏览器 UA) |
| `get_json(url)` | GET + 自动解析 JSON |
| `post(url, data, content_type)` | POST 请求 |

### std.web — Web 后端
| 函数 | 说明 |
|---|---|
| `serve(port, handler)` | 启动 HTTP 服务;handler 返回 dict→JSON、str→HTML、[status,body] |
| `static(port, dir)` | 静态文件服务 |
| `wait()` | 常驻服务 |

### std.ai — AI Agent
| 函数 | 说明 |
|---|---|
| `configure(base_url, model, api_key)` | 配置 OpenAI 兼容端点 |
| `chat(prompt)` | 单轮对话 |
| `messages(history)` | 多轮对话 |
| `agent(system, tools, prompt)` | 工具调用式 Agent 循环 |

### std.python — Python 互操作
| 函数 | 说明 |
|---|---|
| `eval(code)` | 执行 Python 表达式,返回结果 |
| `exec(code)` | 执行 Python 语句 |
| `import(module)` | 导入 Python 模块 |
| `call(fn, args)` | 调用 Python 函数 |

### std.ffi — C ABI 互操作(Rust/C++)
| 函数 | 说明 |
|---|---|
| `load(path)` | 加载 .so/.dylib/.dll 共享库 |
| `func(lib, name, argtypes, restype)` | 获取函数 |
| `cstr(s)` | 字符串 → C 字符串 |

### std.html — HTML 生成
| 函数 | 说明 |
|---|---|
| `escape(s)`, `page(title, body)`, `render(template, data)` | |
| `write(path, content)`, `link(href, text)`, `list(items)`, `json_script(data, id)` | |

### std.collections — 集合类型
| 类型/函数 | 说明 |
|---|---|
| `HashMap` | 哈希表:get/put/contains/remove/keys/values/len |
| `HashSet` | 哈希集合:add/contains/remove/len |
| `Vec` | 动态数组:push/pop/get/len/iter |
| `hash_map()`, `hash_set()`, `vec()` | 工厂函数 |

### 其他模块
- `std.time`: `now()`, `sleep(ms)`, `timestamp()`, `format()`
- `std.sync`: `Channel`, `Mutex`, `Fiber`
- `std.result`: `Ok`, `Err`, `Result`
- `std.proc`: `run(cmd)`, `call(cmd)`, `spawn(cmd)`(子进程)
- `std.vex`: `export()`, `python()`, `cpp()`(VEXcode 工程导出)

---

## 3. 常用编程模式

### 3.1 深度优先搜索(DFS)

```rust
fn dfs(graph, node, visited) {
    if visited.contains(node) { return }
    visited.push(node)
    println("访问: " + str(node))
    for neighbor in graph[node] {
        dfs(graph, neighbor, visited)
    }
}

let graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"]
}
dfs(graph, "A", [])
```

### 3.2 斐波那契(递归 + 记忆化)

```rust
fn fib(n, memo) {
    if n < 2 { return n }
    if memo.keys().contains(n) { return memo[n] }
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    memo[n]
}

let memo = {}
println(str(fib(10, memo)))   // 55
```

### 3.3 HTTP + JSON API 调用

```rust
import std.http
import std.json

let data = std.http.get_json("https://api.example.com/users")
for user in data {
    println(user["name"])
}
```

### 3.4 Web 服务(一个文件全栈)

```rust
import std.web
import std.json

fn handler(req) {
    let path = req["path"]
    if path == "/" {
        return "<h1>Hello Aurora</h1>"
    }
    if path == "/api/data" {
        return {"status": "ok", "data": [1, 2, 3]}
    }
    return [404, "Not Found"]
}

std.web.serve(8080, handler)
std.web.wait()
```

### 3.5 调用 Rust/C++ 共享库

```rust
import std.ffi

let lib = std.ffi.load("librust_math.dylib")
let add = std.ffi.func(lib, "add", ["int32", "int32"], "int32")
println(str(add(3, 4)))   // 7
```

### 3.6 调用 Python 库

```rust
import std.python

let np = std.python.import("numpy")
let arr = np.array([1, 2, 3])
println(str(np.mean(arr)))   // 2.0
```

### 3.7 读写 JSON 文件

```rust
import std.json

let config = std.json.load("config.json")
config["version"] = "2.0"
std.json.save("config.json", config)
```

### 3.8 多文件项目结构

```
myapp/
├── aurora.toml          # [project] name/version, [build] entry, [dependencies]
├── src/
│   ├── main.aur         # 入口
│   ├── models/
│   │   └── user.aur     # import models.user
│   └── utils.aur        # import utils
└── tests/
    └── user_test.aur    # aurora test
```

---

## 4. 与其他语言对比

| 概念 | Aurora | Python | Rust | JavaScript |
|---|---|---|---|---|
| 不可变变量 | `let x = 5` | `x = 5`(约定) | `let x = 5` | `const x = 5` |
| 可变变量 | `var x = 5` | `x = 5` | `let mut x = 5` | `let x = 5` |
| 函数 | `fn f(a) { a }` | `def f(a): return a` | `fn f(a: i32) -> i32 { a }` | `const f = (a) => a` |
| 返回值 | 最后表达式 | `return` | 最后表达式 | `return` |
| 数组 | `[1,2,3]` | `[1,2,3]` | `vec![1,2,3]` | `[1,2,3]` |
| Map | `{"k": v}` | `{"k": v}` | `HashMap::new()` | `{k: v}` |
| 空值 | `nil` | `None` | `Option<T>` | `null/undefined` |
| 模块 | `import std.io` | `import io` | `use std::io` | `import io` |
| 字符串插值 | `"hi {name}"` | f-string | `format!("hi {name}")` | `` `hi ${name}` `` |
| 管道 | `x \|> f` | 无 | 无(方法链) | 无(方法链) |
| 错误处理 | `Result` + `?` | 异常 | `Result<T,E>` | try/catch |

---

## 5. 常见陷阱

1. **let 不可变**:循环计数器、累加器必须用 `var`,不是 `let`。
2. **函数返回值**:函数体最后一个表达式自动返回,不需要 `return`。但如果最后是语句(如 println),函数返回 nil。
3. **原始字符串**:JSON、正则、路径、外部代码片段必须用 `r'...'`,否则 `{` 会被当作插值。
4. **import 本地模块**:模块文件必须在当前目录、`src/` 或项目根下;文件名对应模块名。
5. **Map 键是字符串**:`{"key": value}`,访问用 `m["key"]`,不是 `m.key`(除非是对象方法)。
6. **std.http.get 自动带 UA**:不需要手动设置 User-Agent。
7. **AOT 编译限制**:`aurora build` 支持核心语法,高级语法(match/spawn/trait/impl 等)暂不支持编译,请用解释器运行。

---

## 6. 调试与错误信息

错误格式:`L<行>:C<列>: [<类别>] 描述`

| 类别 | 含义 |
|---|---|
| `ParseError` | 语法错误 |
| `TypeError` | 类型错误(含不可变绑定赋值) |
| `NameError` | 未定义变量 |
| `RuntimeError` | 运行时错误 |
| `ImportError` | 模块导入失败 |
| `HttpError` | HTTP 请求失败 |
| `OwnershipError` | 所有权/借用冲突 |

调试技巧:
- `println(str(x))` 打印任意值
- `aurora check file.aur` 只做静态检查不运行
- `aurora tokens file.aur` 看词法分析结果
- `aurora ast file.aur` 看 AST 结构

---

## 7. 完整示例:命令行待办应用

```rust
import std.json
import std.io

let DATA_FILE = "todos.json"

fn load() {
    if std.io.exists(DATA_FILE) {
        return std.json.load(DATA_FILE)
    }
    return []
}

fn save(todos) {
    std.json.save(DATA_FILE, todos)
}

fn add(todos, title) {
    todos.push({"id": todos.len() + 1, "title": title, "done": false})
    save(todos)
    println("已添加: " + title)
}

fn list(todos) {
    for t in todos {
        let mark = if t["done"] { "[x]" } else { "[ ]" }
        println(mark + " #" + str(t["id"]) + " " + t["title"])
    }
}

fn main() {
    let todos = load()
    add(todos, "学习 Aurora")
    add(todos, "写一个项目")
    todos[0]["done"] = true
    save(todos)
    list(todos)
}

main()
```

---

*本文档随 Aurora v1.2.0 发布。最新版本见 `docs/SPEC.md` 和 `CHANGELOG.md`。*
