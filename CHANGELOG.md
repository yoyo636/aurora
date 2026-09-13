# 变更日志

本项目遵循语义化版本,详见 `docs/VERSIONING.md`。

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
