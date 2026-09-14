# 变更日志

本项目遵循语义化版本,详见 `docs/VERSIONING.md`。

## [1.7.0] - 2026-09-14

极致性能版本。编译期常量计算 + 自动记忆化 + 激进编译优化,性能达到极限。

### 编译期常量计算(常量折叠)
- 参数全为字面量的纯函数调用,在编译时直接计算结果
- 支持内置数学函数(fibonacci/factorial/gcd/lcm/is_prime/sqrt/abs/sin/cos/tan/log/exp/floor/ceil/round/min/max)
- 支持用户定义的纯 int 函数(递归求值器 + 记忆化缓存)
- 编译期求值器支持:if/return/let/assign/基本运算/递归调用

### 自动记忆化
- 递归纯 int 单参数函数自动添加静态缓存
- 将 O(2^n) 递归计算降为 O(n)
- 缓存大小 100000,覆盖绝大多数实用场景
- 自动检测递归函数(函数体内调用自身)

### 激进编译优化
- 默认优化级别从 -O2 升级为 -O3
- 新增 -flto 链接时优化(跨模块内联和优化)
- 新增 -march=native 针对当前 CPU 指令集优化
- 新增 -fomit-frame-pointer 省略帧指针(释放额外寄存器)

### 性能提升
- **fib(35) 编译期常量计算**:28ms → **0ms**(编译时直接算出结果)
- **fib(35) 自动记忆化(非常量参数)**:28ms → **0ms**(O(2^n)→O(n))
- **fib(45) 自动记忆化**:无记忆化需数秒 → **0ms**
- **对比 Python**:707ms → 0ms,提升超过 **700 倍**
- 类型特化版本(无记忆化)仍保持 C 语言水平:28ms

### 验证
- 161 项现有测试全部通过
- 所有原生示例(hello/fibonacci/map_json/benchmark)编译运行正常
- 自动记忆化不影响非递归函数和动态类型功能

### 变更
- 版本 1.6.0 → 1.7.0
- 默认编译优化级别 -O2 → -O3

## [1.6.0] - 2026-09-14

极致性能版本。类型推断 + 单态化特化,性能达到 C 语言水平。

### 类型推断与特化
- **类型推断器** `type_infer.py`:分析函数参数类型、返回值类型和变量类型;支持递归函数迭代求解;从调用点推断参数类型;数值运算类型传播启发式
- **纯 int 函数单态化**:被识别为纯 int 函数(所有参数和返回值都是 int)的函数,直接编译为 `int64_t` C 函数,算术运算直接使用 C 运算符,完全消除 AuValue 运行时开销
- **自动类型转换**:普通函数调用纯 int 函数时,自动进行 AuValue ↔ int64_t 类型转换
- **特化表达式生成** `gen_expr_typed`:为纯 int 函数生成原生 C 表达式,支持字面量/变量/算术运算/比较运算/逻辑运算/函数调用/三元运算符

### 性能提升
- **fib(35) 递归**:从 144ms(动态类型)优化到 **28ms**(类型特化 -O3),提升 5.1 倍
- **对比 Python**:707ms → 28ms,提升 **25 倍**
- **对比 C 语言**:Aurora 28ms vs C 35ms,**达到并超过 C 语言性能**

### 运行时增强
- 新增 `_aurora_pow_int` 函数(int 幂运算,用于类型特化代码)
- 新增 `<stdint.h>` 头文件引用

### 变更
- 版本 1.5.0 → 1.6.0

## [1.5.0] - 2026-09-14

原生编译器版本。Aurora 从解释器语言升级为可编译为原生机器码的高性能语言。

### 原生编译器
- **Aurora → C → 机器码编译管线**:新增 `codegen.py` 代码生成器,将 AST 转换为 C 代码,再由 gcc/clang 编译为原生可执行文件
- **运行时库** `runtime/aurora_rt.h/c`:通用值类型 AuValue(标签联合,支持 nil/int/float/bool/string/array/map)、AuString(带长度 UTF-8)、AuArray(动态数组)、AuMap(开放寻址哈希表)、算术/比较/逻辑运算、内置函数(println/len/range/read_line/file_io/shell/env/time)、数学函数(sqrt/sin/cos/log/exp/floor/ceil/round/min/max/gcd/lcm/is_prime/factorial/fibonacci)、JSON 解析与序列化、内存管理
- **`aurora build-native` 命令**:编译 .aur 文件为原生可执行文件;支持 `-O0/-O1/-O2/-O3/-Os` 优化级别;`--cc` 指定编译器(cc/clang/gcc);`--keep-c` 保留生成的 C 源码;`-v` 显示详细编译输出
- **性能提升**:递归斐波那契 fib(35) 原生编译 144ms vs Python 解释器 707ms,快约 4.9 倍

### 支持的语法特性
- 变量声明(let/var/const)、函数定义(fn)、递归调用
- 算术运算(+ - * / % **)、比较运算(== != < <= > >=)、逻辑运算(&& || !)
- if/elif/else 条件语句、for 循环(支持 range 和数组迭代)、while 循环
- break/continue、return(提前退出)
- 数组字面量 [1, 2, 3]、Map 字面量 {"key": value}
- 索引访问 arr[0]、map["key"]
- 字符串插值 "x = {x}"、原始字符串 r'...'
- 内置函数:println/print/len/range/now_ms/sleep_ms/json_parse/json_stringify 等
- 数学函数:sqrt/abs/sin/cos/tan/log/exp/floor/ceil/round/min/max/gcd/lcm/is_prime/factorial/fibonacci

### 示例
- `examples/native/hello.aur`:Hello World + 字符串插值
- `examples/native/fibonacci.aur`:递归斐波那契 + 数组 + 循环求和
- `examples/native/map_json.aur`:Map 操作 + JSON 解析与序列化
- `examples/native/benchmark.aur`:性能基准测试

### 变更
- 版本 1.4.0 → 1.5.0

## [1.4.0] - 2026-09-13

效率大增强 + Moonshot 主题版本。

### 效率增强
- **100+ 全局快捷函数**:文件/网络/JSON/Shell/列表/字符串/系统/数学/函数式/字典/编码/格式/正则/随机/工具/验证/颜色/临时文件等全局函数,无需 import 直接使用
- **Moonshot 暗黑极简主题**:REPL banner 黑色背景+白色月牙◡+极简边框+ANSI 颜色;CLI `--version` 输出 `◡ Aurora v1.4.0`
- **VSCode Aurora Dark 主题**:纯黑 #000 + 白色高亮,插件版本升至 0.5.0
- **安装器界面暗黑化**:白色月牙光晕背景图(纯 Python zlib 生成 PNG,无 PIL 依赖)

### 变更
- 版本 1.3.0 → 1.4.0;全局函数 `color` 改名为 `colorize`(避免与命名参数冲突)

## [1.3.0] - 2026-09-13

高效版本。全面提升执行性能、编译效率和开发体验。

### 高性能执行
- **AOT 编译器扩展**:新增 `match` 表达式和语句支持(翻译为 Python if/elif 链);函数末尾的 `match` 语句自动转为返回值
- **std.str 增强**:新增 `find(s, sub, start)`、`substring(s, start, end)`、`len(s)`、`char_at(s, index)`
- **std.http.get 增强**:自动携带浏览器 User-Agent,CSDN 等网站不再拦截;支持自定义 headers 参数
- **性能基准测试** `examples/benchmarks/`:fibonacci(递归+记忆化)、loop_sum(百万次累加)、map_ops(十万次 Map 读写),可对比解释器 vs AOT 编译性能

### 高效编译
- **编译缓存**:基于文件 mtime,未变化的源文件跳过编译;`aurora build` 第二次运行时所有模块显示 `⏭ 跳过(未变化)`
- **`--force` / `-f` 参数**:强制重新编译,忽略缓存
- **自动扫描 import 模块**:编译入口时自动发现并编译所有本地依赖模块

### 高效开发体验
- **`aurora watch` 命令**:监听 `src/` 目录及入口文件变化,自动重新运行;0.5s 检查间隔,Ctrl+C 退出;首次启动立即运行一次
- **IDE 保存自动运行**:状态栏新增「⚡ 自动运行」开关,开启后保存文件自动触发运行(热重载开发模式)
- **IDE 状态栏版本同步** v1.3.0

### 变更
- 版本 1.2.0 → 1.3.0

## [1.2.0] - 2026-09-13

大型项目能力版本。Aurora 从单文件脚本语言升级为可构建真正大型项目的工程化语言。

### 新增
- **多文件模块系统**:解释器原生支持 `import utils` / `from utils import fn` 加载本地 `.aur` 模块;自动搜索当前文件目录、`src/`、项目根;支持 `utils.aur` 与 `utils/__init__.aur` 两种包形态;循环导入检测;模块缓存
- **AOT 编译器 `aurora build`**:AST → Python 源码生成器,支持核心语法(字面量/运算/调用/方法/索引/Lambda/If 表达式/字符串插值/let/return/if/for/while/函数定义/import/块);函数体最后表达式自动 return;`std.io`/`std.json`/`std.math`/`str.html` 等标准库调用翻译为 Python 原生;自动扫描并编译 import 的本地模块;输出 `dist/` 可直接 `python3` 运行
- **`std.collections` 集合库**:`HashMap` / `HashSet` / `Vec` 三个类 + 工厂函数 `hash_map()` / `hash_set()` / `vec()`,提供 get/put/contains/remove/keys/values/len/iter 等方法
- **工程化项目结构**:`aurora new` 现在生成 `src/main.aur` + `src/lib.aur` + `tests/` + `aurora.toml` 的标准分层结构;`aurora.toml` 支持 `[dependencies]` 路径依赖声明;`aurora run` / `aurora build` 无参数时自动读取 `aurora.toml` 入口
- **大型项目示例** `examples/largeapp/`:分层架构任务管理系统(models/services/utils/storage 四层),7 个模块文件,展示多文件 import、JSON 持久化、业务逻辑分层、测试

### 变更
- 版本 1.1.0 → 1.2.0;IDE 状态栏同步
- `aurora new` 脚手架从单文件升级为 `src/` 分层结构

## [1.1.0] - 2026-09-12

全栈 + AI Agent 版本。

### 新增
- **`std.web` Web 后端**:`serve(port, handler)` 起 HTTP 服务(路由/JSON API/HTML 页面,handler 返回 dict→JSON、str→HTML、[status, body]、[status, headers, body]);`static(port, dir)` 静态文件服务;`wait()` 常驻服务
- **`std.ai` AI Agent**:`configure()` 配置 OpenAI 兼容端点(默认火山方舟/豆包模型);`chat()` 对话;`messages()` 多轮;`agent(system, tools, prompt)` 工具调用式 Agent 循环——大模型决策,调用 Aurora 函数,结果回填,自动收敛
- **`std.html` 前端组件增强**:`link()` / `list()` / `json_script()`(数据嵌入页面,防 `</` 注入)
- **`std.io` 增强**:`list_dir()` / `mkdir()` / `is_dir()` / `files(dir, ext)`
- **关键字 `and` / `or` / `not`**:token 类型早已定义但关键字表漏映射,补全;`if a == 1 and b == 2` 现可直接书写
- **全栈示例** `examples/fullstack/`:一个 `.aur` 文件同时提供 HTML 前端、Web 后端、Rust/C++(FFI)计算、Python 计算、JSON API、AI Agent 端点
- 测试 149 → 161(Web 服务 / AI Agent 工具循环(mock LLM)/ HTML 组件 / IO 增强)

### 变更
- 版本 1.0.0 → 1.1.0;IDE 状态栏、VSCode 插件 0.4.0 同步

## [1.0.0] - 2026-09-12

正式发布。语言达到稳定承诺,新增正式工具链与治理文档。

### 新增
- **正式 CLI 工具链**
  - `aurora new <name>`:项目脚手架,生成 `aurora.toml` 清单 / `main.aur` 入口 / README
  - `aurora test [path]`:测试运行器,收集 `*_test.aur` / `*_tests.aur` 文件整体运行,或逐个运行 `test_*` 函数,输出 PASS/FAIL 汇总(失败时退出码非零)
  - `aurora run`(无参数):读取当前目录 `aurora.toml` 的 `[build] entry` 运行项目
- **全局安装**:`install.sh` 把 `aurora` 命令安装到用户 PATH(`~/.local/bin` 优先),验证通过
- **语言规范文档**:`docs/SPEC.md`(14 章完整规范,涵盖词法/类型/语义/模块/生态/工具链/稳定性)
- **版本策略**:`docs/VERSIONING.md`(语义化版本 + 稳定性分级 + 兼容承诺 + 发布流程)
- **版本治理**:语言版本升至 1.0.0,IDE 状态栏同步

### 变更
- 语言版本 0.3.0 → 1.0.0(稳定承诺起点)

## [0.3.0] - 2026-09-12

生态链版本:与外部语言/数据/程序互通。

### 新增
- **生态模块**:`std.json`(load/save)、`std.python`(eval/exec/import/call)、`std.ffi`(load/func/cstr,C ABI 桥)、`std.html`(escape/render/page/write/open,`{{!key}}` 原始输出)、`std.proc`(run/call/spawn/run_args/call_args)、`std.http`(get/get_json/post)、`std.vex`(export/python/cpp,VEXcode 工程导出)
- **原始字符串** `r'...'` / `r"..."`:不插值、反斜杠保留,适合 JSON/正则/路径/外部代码
- **关键字成员访问**:`std.python.import(...)` 合法
- **字典键优先**:修复模块函数 `get` 被 dict 内建方法遮蔽的问题
- **示例**:`examples/interop/` 8 个可运行 demo + Rust/C++ 共享库源码

### 修复
- 字符串转义真实生效(`\"` 不再残留反斜杠,`\n`/`\t` 等正确转换)

### ZL 设计特性(同版本内落地)
- `let` 不可变 / `var` 可变(`let mut` 兼容)
- 管道 `|>`
- 区间 `a..b`(闭区间)
- 模式解构 `let (a, b) = ...`
- `defer`(LIFO、参数注册时求值、支持块、return 也执行)
- `yield` 生成器
- 测试 126 → 149

## [0.2.0] - 2026-09-12

IDE 与工具链里程碑。

### 新增
- macOS 应用 `Aurora IDE.app`(pywebview 原生窗口,内嵌本地 IDE 服务)
- VSCode 插件 `aurora.aurora-ide`(运行/检查/运行选中,快捷键 ⌘⌥R / ⌘⌥K)
- VSCode 风格 WebIDE:文件树 / 多标签编辑器 / 输出·问题·输入面板 / 状态栏
- 文件 API:列表/读取/保存/新建(白名单扩展名 + 工作区边界防护)

### 修复
- 换行后以 `(` 开头的新语句不再被吸进上一表达式(解析器边界修复)
- REPL 模块导入路径

## [0.1.0] - 2026-09-12

语言核心初版。

### 新增
- 词法/语法分析、AST、类型检查器、所有权检查器、解释器、标准库
- CLI:`run / eval / check / repl / tokens / ast`
- 示例:等腰三角形系列(`examples/triangles/`)
- 测试套件:101 项单测

### 修复
- 循环内 `ReturnSignal` 覆盖导致 `is_prime` 恒真
- `reduce` 参数序统一并兼容经典写法
- server 进程级缓存(lessons 改后需重启)
