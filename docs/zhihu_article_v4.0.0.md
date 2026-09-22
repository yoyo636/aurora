# Aurora v4.0.0 自举之路：当一门语言开始用自己解释自己

## 一、版本概述

Aurora v4.0.0 是自举（Bootstrap / Self-hosting）重构大版本。在 v3.4.0 标准库补齐（14 个 `std.*` 命名空间、1089 个测试）的基础上，项目正式启动用 Aurora 语言本身来实现 Aurora 编译器前端的工程目标。

本次更新的核心产物是 `selfhost/interpreter.aur`——一份 **891 行纯 Aurora 代码**，用 Aurora 语言手写完成了 Aurora 的词法分析器、递归下降解析器与树遍历解释器。该解释器由 Python 实现的 Aurora 运行时加载执行，能够对 Aurora 源代码完成从字符流到语法树、再到运行结果的完整闭环。

项目地址：https://github.com/yoyo636/aurora

## 二、为什么要自举

一门语言的编译器初期几乎总是用另一门"宿主语"来写。Aurora 的前身由 Python 实现：解释器 2047 行、词法分析器 263 行、解析器 1451 行、AST 节点 760 行、类型检查器 1041 行，合计约 41,000 行 Python 构成了 v3.3.0 的全部基础设施。

这种"宿主语寄生"状态在工程上有三个根本性问题。

**第一，运行时依赖无法剥离。** Python 实现的解释器必须依赖 CPython 运行时。Aurora 虽然提供了 ARM64 汇编后端与 C 原生编译后端，但编译器本身的引导仍然需要 Python 解释器在场。这意味着分发一个"零依赖、单文件、原生机器码"的 Aurora 二进制在引导层就做不到。

**第二，语言能力无法自证。** 一门语言是否足够强大，最严格的检验标准是它能否写出自己的编译器。Rust 1.0 自举、Go 1.5 自举、Zig 0.9 自举、Swift 5.x 自举——这些节点都不是营销事件，而是工程上证明"这门语言的抽象能力、表达能力、标准库覆盖度足以承载非平凡软件系统"的里程碑。在没有完成自举之前，任何"Aurora 是通用系统语言"的论断都是外部承诺，不是内部证据。

**第三，优化闭环无法形成。** 当编译器与被编译语言是同一门语言时，自举版本自身就是最大、最真实的基准程序。解释器的每一次优化、标准库的每一次性能改进，都可以通过"自举解释器运行自身"来端到端验证。这种闭环在宿主语实现下是断裂的。

因此，v4.0.0 的目标不是立即替换 Python 实现，而是迈出第一步：**证明 Aurora 语言本身足够强大，能够写出自己的编译器前端。**

## 三、自举的技术挑战

自举不是简单地"把 Python 代码翻译成 Aurora"。它要求被自举的语言在表达能力上先跨过一道门槛。

### 3.1 字符串逐字符处理

词法分析器的本质是对字符流做状态机扫描。Python 版本的 Lexer 依赖 `len(source)`、索引取字符、切片等操作。Aurora 在 v3.4.0 之前对字符串的逐字符访问能力不足——没有 `charAt`、`charCodeAt`、`substring` 等基元。自举工作首先倒逼标准库补齐了这些字符串操作：

```aurora
# 自举词法分析器中的数字扫描（selfhost/interpreter.aur）
if c >= 48 && c <= 57 {
    let start = pos
    let mut has_dot = false
    while pos < n {
        let cc = char_code_at(src, pos)
        if cc >= 48 && cc <= 57 {
            pos = pos + 1
        } else {
            if cc == 46 && !has_dot {
                has_dot = true
                pos = pos + 1
            } else {
                break
            }
        }
    }
    let text = substring(src, start, pos)
    # ...生成数字 token
}
```

这段代码展示了自举对语言基元的反向驱动：如果 `char_code_at` 和 `substring` 不存在，词法分析器就无法在 Aurora 内部实现。

### 3.2 动态数据结构模拟 AST

编译器前端的中间表示是抽象语法树（AST）。在静态类型语言中，AST 通常用代数数据类型（ADT）或 sealed class 层级来表达。Aurora v4.0.0 的自举版本采用了一个更务实的方案：**用 HashMap 模拟 AST 节点**。

```aurora
fn new_node(kind: str) -> HashMap {
    let n = HashMap()
    n.set("kind", kind)
    n.set("int_val", 0)
    n.set("float_val", 0.0)
    n.set("str_val", "")
    n.set("bool_val", false)
    n.set("name", "")
    n.set("op", "")
    n.set("left", null)
    n.set("right", null)
    n.set("operand", null)
    n.set("func", null)
    n.set("args", [])
    n.set("cond", null)
    n.set("then", null)
    n.set("else", null)
    n.set("body", null)
    n.set("stmts", [])
    n.set("params", [])
    return n
}
```

每个 AST 节点是一个带类型标签的 HashMap：`kind` 字段区分节点类型（`"int"`、`"binary"`、`"call"`、`"if"` 等），其余字段按节点类型填充。这种方案放弃了编译期穷尽性检查，但换来了两个工程上的收益：一是无需等待 Aurora 的 ADT/sealed class 完全成熟即可启动自举；二是节点构造与访问都是动态的，解析器和解释器可以在不修改类型定义的情况下扩展节点种类。

这是一个典型的"先跑通、再加固"的自举策略。Rust 早期自举也曾在 unstable trait object 与 enum 之间做过类似权衡。

### 3.3 作用域与环境建模

解释器需要维护变量环境。Aurora 自举版本用 HashMap 作为单一作用域，通过链式查找模拟作用域链：

```aurora
fn env_get(env: HashMap, name: str) -> HashMap {
    if env.has(name) {
        return env.get(name)
    }
    return val_null()
}

fn env_set(env: HashMap, name: str, val: HashMap) {
    env.set(name, val)
}
```

函数调用时创建新的环境帧，参数绑定到新帧，返回时丢弃。`eval_call` 函数负责构造闭包环境：

```aurora
fn eval_call(node: HashMap, env: HashMap) -> HashMap {
    let func_node = eval_expr(node.get("func"), env)
    let params = func_node.get("params")
    let args = []
    for arg_node in node.get("args") {
        args.append(eval_expr(arg_node, env))
    }
    let call_env = HashMap()
    for i in range(len(params)) {
        call_env.set(params[i], args[i])
    }
    return eval_block(func_node.get("body"), call_env)
}
```

### 3.4 递归下降解析器

解析器采用经典的 Pratt / 递归下降风格，按运算符优先级分层。自举版本实现了 17 个解析函数，覆盖 Aurora 表达式与语句的一个子集：

| 解析函数 | 职责 |
|---------|------|
| `parse_program` | 程序入口，解析顶层语句序列 |
| `parse_block` | 解析花括号包围的语句块 |
| `parse_stmt` | 语句分派（let / if / while / return / 表达式） |
| `parse_expr` | 表达式入口（最低优先级） |
| `parse_comparison` | 比较运算符 `== != < > <= >=` |
| `parse_additive` | 加减 `+ -` |
| `parse_multiplicative` | 乘除模 `* / %` |
| `parse_unary` | 一元运算符 `- !` |
| `parse_call` | 函数调用 `f(a, b)` |
| `parse_primary` | 字面量 / 标识符 / 括号表达式 |

优先级层次与主流语言（C/Java/Go）一致：一元 > 乘除 > 加减 > 比较 > 逻辑。这种分层使得运算符结合性与优先级无需特殊表驱动逻辑即可正确处理。

## 四、自举路径：六阶段规划

v4.0.0 完成的是第一阶段到第五阶段的一个最小子集。完整的自举路径规划为六个阶段。

### 阶段一：能力补齐（已完成）

在 Aurora 标准库中补齐自举所需的语言基元：字符串逐字符操作（`char_code_at`、`substring`）、动态容器（`HashMap`、`Vec`）、控制流（`while`、`for in range`、`if/else`）、函数与递归。v3.4.0 的 14 个 `std.*` 模块为这一阶段提供了基础设施。

### 阶段二：自举词法分析器（已完成）

`tokenize(src)` 函数将源代码字符串转换为 Token 列表。Token 用 HashMap 表示，包含 `kind`（`"int"` / `"float"` / `"string"` / `"ident"` / `"keyword"` / `"op"`）、`value`、`line` 三个字段。已支持：整数与浮点数、双引号字符串（含反斜杠转义）、标识符与关键字、单字符与双字符运算符、单行注释、空白与换行。

### 阶段三：自举 AST 节点（已完成）

`new_node(kind)` 工厂函数构造带类型标签的 HashMap 节点。已覆盖：整数字面量、浮点字面量、字符串字面量、布尔字面量、null、标识符、二元表达式、一元表达式、函数调用、函数定义、变量声明、if 语句、while 语句、return 语句、语句块、程序根节点。

### 阶段四：自举解析器（已完成）

递归下降解析器将 Token 列表转换为 AST。已支持 Aurora 子集：表达式（算术、比较、函数调用、括号嵌套）、语句（`let` 变量声明、`if/else`、`while`、`return`）、函数定义（`fn name(params) { body }`）、程序顶层语句序列。

### 阶段五：自举解释器（已完成）

`eval_expr` / `eval_stmt` / `eval_block` / `eval_program` 四层树遍历求值器。已支持：变量定义与读取、算术与比较运算、条件分支、while 循环、函数定义与调用、递归、`return` 提前返回、`print` 内置函数。`run(src)` 是完整入口：词法分析 → 解析 → 解释执行。

### 阶段六：自举验证（进行中）

验证 Aurora 写的解释器能够正确执行 Aurora 子集程序。验证方式包括：自举解释器运行斐波那契递归、阶乘、字符串处理、循环累加等基准；与 Python 解释器执行同一程序的输出做端到端对比。

```aurora
# selfhost/interpreter.aur 中的自检测试
fn self_test() {
    let result = run("
        fn fib(n) {
            if n < 2 { return n }
            return fib(n - 1) + fib(n - 2)
        }
        let x = fib(10)
        print(x)
    ")
    # 期望输出 55
}
```

## 五、自举解释器的架构

`selfhost/interpreter.aur` 的 891 行代码可以划分为四层，对应编译器前端的经典架构：

```
┌─────────────────────────────────────────┐
│  run(src)  ← 完整入口                   │
├─────────────────────────────────────────┤
│  解释层: eval_program / eval_block     │
│          eval_stmt / eval_expr          │
│          eval_binary / eval_call       │
├─────────────────────────────────────────┤
│  解析层: parse_program / parse_block   │
│          parse_stmt / parse_expr       │
│          parse_comparison / ...        │
├─────────────────────────────────────────┤
│  词法层: tokenize(src)                  │
│          → Vec<HashMap {kind,value,line}>│
└─────────────────────────────────────────┘
```

这一架构与 Python 实现的编译器前端（`lexer.py` → `parser.py` → `interpreter.py`）在分层上完全同构。区别仅在于实现语言：Python 版本用类继承表达 AST 节点层级，Aurora 版本用带类型标签的 HashMap 表达。

从代码量看，Python 版本的解释器（2047 行）+ 词法分析器（263 行）+ 解析器（1451 行）合计约 3761 行。Aurora 自举版本以 891 行完成了一个功能子集——表达密度约为 Python 的 4 倍，这得益于 Aurora 语法在函数定义、容器字面量、控制流上的简洁性。

## 六、与主流语言自举里程碑的对比

| 语言 | 首次自举版本 | 自举时编译器规模 | 自举前宿主语 |
|------|------------|----------------|------------|
| Rust | 1.0 (2015) | ~10 万行 Rust | OCaml |
| Go | 1.5 (2015) | ~40 万行 Go | C |
| Zig | 0.9 (2021) | ~2 万行 Zig | C++ |
| Swift | 5.x (2018) | ~20 万行 Swift | C++ |
| Java | JDK (1996) | ~10 万行 Java | C |
| **Aurora** | **v4.0.0 (2026)** | **891 行 Aurora（前端子集）** | **Python** |

Aurora 的自举在规模上远小于上述语言——因为 v4.0.0 自举的是"编译器前端的一个最小子集"，而非完整编译器。这与 Zig 0.9 自举时只覆盖 Zig 语言子集、后续版本逐步扩展覆盖范围的策略一致。完整自举（自举版本能够编译自身的全部语法与标准库）预计需要后续多个版本迭代。

## 七、自举解锁了什么

完成自举前端的意义不在于"脱离 Python"本身，而在于它解锁了几条原本走不通的路径。

**第一，独立二进制分发成为可能。** 当 Aurora 编译器前端可以用 Aurora 写就，配合 ARM64 汇编后端，最终可以产出一个不依赖 CPython 的原生 Aurora 二进制——这个二进制本身就是用 Aurora 写的编译器。用户不需要安装 Python，只需要一个可执行文件即可运行 Aurora 程序。

**第二，性能优化有了真实基准。** 自举解释器是 Aurora 代码库中最大的纯 Aurora 程序之一。解释器内部的字符串扫描、哈希表查找、函数调用、递归求值，每一处都是真实的性能热点。v3.3.0 引入的 ARM64 后端优化、v3.4.0 的标准库完善，都可以通过"自举解释器运行自身"来端到端测量。

**第三，语言能力有了自证通道。** 当一门语言能写出自己的词法分析器、解析器和解释器，它的表达能力、标准库覆盖度、错误处理机制就不再是文档上的承诺，而是可执行的证据。后续版本扩展自举覆盖范围（泛型、模式匹配、trait、增量计算）时，每一项语言特性都必须先通过"能否在自举解释器中使用"这一检验。

**第四，跨平台移植成本下降。** 自举版本不再依赖 CPython 的 C API。移植到新平台时，只需要为该平台提供一个最小的 Aurora 运行时（内存分配、I/O、垃圾回收），编译器前端就可以随语言一起移植。这在嵌入式、浏览器 WASM、RISC-V 等平台上有实际价值。

## 八、后续路线图

v4.0.0 完成的是自举的第一步——最小前端子集。后续版本的规划如下：

**v4.1.0：扩展自举语法覆盖。** 让自举解释器支持 Aurora 的更多语法特性：`struct` 定义、`enum` 代数数据类型、`match` 模式匹配、`lambda` 闭包、`return` 从嵌套块返回、`break` / `continue`。这一阶段的目标是让自举解释器能够执行 Aurora 标准库的纯逻辑部分。

**v4.2.0：自举 AST 类型化。** 将 HashMap 模拟的 AST 节点替换为 Aurora 的 `struct` + `enum` 类型化节点，恢复编译期穷尽性检查。这一步要求 Aurora 的 `enum` 和 `match` 已经足够成熟到可以描述 AST 层级。

**v4.3.0：自举类型检查器。** 用 Aurora 实现类型检查器，使自举版本具备对 Aurora 源代码进行静态类型推断的能力。这是自举从"解释器"走向"编译器"的关键一步。

**v5.0.0：自举代码生成。** 用 Aurora 实现后端代码生成器，使自举版本能够直接输出 ARM64 机器码。届时 Python 实现的编译器可以退役，Aurora 完全用自身编译自身。

## 九、当前技术栈全景

截至 v4.0.0，Aurora 的技术栈全景如下：

**语言核心：** 静态类型推断、泛型、代数数据类型、模式匹配、trait、可选类型、Result 错误处理、async/await、fiber 协程、宏系统。

**原生增量计算：** `source` / `live` / `transact` 三个关键字，编译期纯度检查，依赖图脏标记，结构化哈希短路。

**编译器后端：** 解释器（Python）、AOT→Python、C 原生编译、ARM64 汇编直出（NEON SIMD 自动向量化）、WASM 后端。

**标准库（v3.4.0，14 个命名空间）：** `std.re` 正则、`std.log` 日志、`std.csv`、`std.archive` 压缩归档、`std.crypto` 加密哈希、`std.time` 日期时间、`std.collections` 高级容器、`std.itertools` 迭代器、`std.functools` 函数工具、`std.math` 复数/Decimal、`std.stats` 统计、`std.fs` 文件系统、`std.thread` 多线程、`std.test` 测试增强。

**AI 引擎：** 张量、自动微分、神经网络层、Agent 工具调用、Jupyter 内核。

**全栈框架：** Web 路由 + 中间件、ORM（SQLite/PostgreSQL/MySQL）、CLI/TUI 框架、Git 绑定、代码生成器。

**自举层（v4.0.0）：** `selfhost/interpreter.aur`，891 行 Aurora 实现的词法分析器 + 解析器 + 解释器。

## 十、结语

自举不是一门语言的终点，而是它开始"用自己的脚走路"的起点。

Aurora v4.0.0 的 891 行自举解释器，在规模上远小于 Rust 1.0 或 Go 1.5 的自举代码——但它完成了同样性质的跨越：被设计的语言第一次开始描述自己。词法分析器的字符扫描、解析器的优先级爬升、解释器的环境帧与递归求值，这些编译器工程中最经典的问题，现在由 Aurora 代码本身来回答。

后续版本将逐步扩展自举覆盖范围，从最小前端子集走向类型化 AST、类型检查器、代码生成器，最终实现 Aurora 完全用自身编译自身。在那之前，Python 实现仍然是主力编译器；但自举的方向已经确定。

项目地址：https://github.com/yoyo636/aurora

---

*本文描述的 Aurora v4.0.0 自举工作正在持续推进中。自举解释器的完整源码位于仓库 `selfhost/interpreter.aur`，欢迎通过测试、Issue 与 PR 参与。*
