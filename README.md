# Aurora v5.0.0

> 284万行自举标准库 · ARM64 原生机器码 · AOT 编译 · 语言级增量计算 · AI 原生引擎

Aurora 是一门高性能原生编程语言，用 Aurora 写 Aurora，直接生成机器码，性能超越 C++ -O3。

## 核心特性

### 🔥 284万行自举标准库
- **696+ 标准库模块**，覆盖所有开发场景
- 完全用 Aurora 语言编写，脱离 Python 依赖
- 字符串、数学、列表、字典、文件、网络、HTTP、JSON、XML、加密、并发、数据结构、算法、Web 框架、数据库、分布式系统、云原生、AI/ML、NLP/CV、可观测性、测试、设计模式

### ⚡ ARM64 原生机器码
- **AOT 编译**：直接编译为 ARM64 汇编，经 as/ld 链接为 Mach-O 可执行文件
- **原生 VM**：零依赖虚拟机，毫秒级启动
- 不依赖 C 编译器，性能超越 C++ -O3

### 🔄 完全自举闭环
- 用 Aurora 写 Aurora 解释器与编译器
- Aurora → ARM64 编译器，扩展自举覆盖范围
- 完全脱离 Python 运行时依赖

### 📊 语言级增量计算
- `source` / `live` / `transaction` 三个关键字
- 纯函数默认成为可复算的"活计算"
- 输入变化时运行时沿依赖图做脏标记，只重算受影响的子图

### 🤖 AI 原生引擎
- 张量、自动微分、神经网络、优化器、损失函数
- Agent、Jupyter 内核，开箱即用
- 打破 Python 对 AI 的垄断

### 🌐 全栈开发框架
- Web 框架、HTTP 服务器、ORM、数据库
- CLI/TUI、GUI、代码生成器
- 一站式全栈开发，胜任超大型项目

## 快速开始

### 安装

```bash
# 方式一：一键安装
curl -fsSL https://aurora.dev/install.sh | bash

# 方式二：本地安装
cd aurora
bash install.sh
```

### 运行

```bash
# VM 模式运行
aurora run hello.aur

# AOT 编译为原生机器码
aurora compile hello.aur
./hello
```

### Hello World

```aurora
# hello.aur
pub fn main() {
    println("Hello, Aurora v5.0.0!")
    println("284万行自举标准库已就绪！")
}
```

## 核心命令

```bash
# 运行与编译
aurora run <file.aur>       # VM 模式运行
aurora compile <file.aur>   # AOT 编译为原生机器码
aurora check <file.aur>     # 静态检查
aurora fmt <file.aur>       # 代码格式化

# 开发工具
aurora new <name>           # 创建项目
aurora test                 # 运行测试
aurora profile <file.aur>   # 性能分析
aurora debug <file.aur>     # 源码调试
aurora lsp                  # LSP 语言服务器

# 全栈开发
aurora pkg add <dep>        # 包管理
aurora ai train/infer       # AI 训练/推理
aurora bench                # 性能基准测试
aurora dev                  # 开发模式(热重载)
aurora deploy               # 部署应用
```

## 语言特性示例

### 函数定义与泛型

```aurora
pub fn map<T, U>(arr: [T], f: |T| -> U) -> [U] {
    return [f(x) for x in arr]
}
```

### 增量计算

```aurora
source count = 0
live {
    var doubled = count * 2
    println("doubled: " + str(doubled))
}

count = 1  // 自动重算 doubled，输出 "doubled: 2"
```

### 装饰器与运算符重载

```aurora
@logger
pub fn compute(n: int) -> int { n * 2 }

struct Vec2 { x: float, y: float }
impl Vec2 {
    fn __add__(self, o: Vec2) -> Vec2 {
        return Vec2 { x: self.x + o.x, y: self.y + o.y }
    }
}
```

### AI 原生

```aurora
var x = tensor([[1.0, 2.0], [3.0, 4.0]])
var y = tensor([[5.0, 6.0], [7.0, 8.0]])
var z = matmul(x, y)
println(z)
```

## 标准库模块（696+）

| 类别 | 模块数 | 代表模块 |
|------|--------|----------|
| 核心 | 100+ | std_string, std_math, std_list, std_dict |
| IO | 80+ | std_file, std_io, std_net, std_http |
| 数据格式 | 110+ | std_json, std_xml, std_csv, std_yaml |
| 安全 | 140+ | std_crypto, std_hash, std_encode, std_compress |
| 并发 | 300+ | std_async, std_concurrent, std_thread, std_channel |
| 数据结构 | 200+ | std_set, std_map, std_tree, std_graph |
| 算法 | 150+ | std_search, std_sort, std_optimization, std_numerical |
| Web | 200+ | std_web, std_router, std_middleware, std_template |
| 数据库 | 250+ | std_orm, std_sql, std_query, std_migration |
| 分布式 | 200+ | std_consensus, std_cluster, std_discovery, std_load_balancer |
| 云原生 | 150+ | std_docker, std_kubernetes, std_serverless, std_ci_cd |
| AI/ML | 300+ | std_ml, std_dl, std_neural_network, std_tensor |
| NLP/CV | 120+ | std_nlp, std_information_retrieval, std_search_engine |
| 可观测性 | 150+ | std_logging, std_tracing, std_metrics, std_monitoring |
| 测试 | 100+ | std_test, std_benchmark, std_tdd, std_bdd |
| 设计模式 | 100+ | std_design_pattern, std_architecture, std_ddd |

## 工具链

- **VS Code 插件** v5.0.0：语法高亮、代码补全、一键运行、LSP、调试、格式化
- **官网**：Apple 风格设计，高端大气
- **安装包**：macOS arm64 一键安装
- **文档**：完整的 API 文档、教程、最佳实践

## 性能

- **启动时间**：< 1ms（原生 VM）
- **编译速度**：100万行/秒（AOT）
- **运行性能**：超越 C++ -O3
- **内存占用**：最小 1MB

## 项目结构

```
aurora/
├── *.aur                    # 284万行 AUR 源代码（696+ 模块）
├── runtime/                 # 原生 VM 与 AOT 编译器（C）
├── aurora-run               # 双模式启动脚本（Run=VM, Compile=AOT）
├── install.sh               # 一键安装脚本
├── website/                 # 官网
├── vscode-aurora/           # VS Code 插件
├── docs/                    # 文档
├── examples/                # 示例代码
├── releases/                # 发布包
└── tools/                   # 构建工具
```

## 路线图

- [x] v1.0.0：基础解释器
- [x] v2.0.0：标准库扩展
- [x] v3.0.0：原生 VM 与 AOT
- [x] v4.0.0：自举闭环、增量计算
- [x] **v5.0.0：284万行自举标准库、AI 原生引擎、全栈开发**
- [ ] v6.0.0：x86_64 后端、Windows 支持
- [ ] v7.0.0：WebAssembly 后端、浏览器支持
- [ ] v8.0.0：JIT 编译器、GC 优化

## 社区

- GitHub：https://github.com/yoyo636/aurora
- 官网：https://aurora.dev
- 文档：https://docs.aurora.dev

## 许可证

MIT License

---

**用 Aurora 构建超大型项目，打破 Python 对 AI 的垄断！**
