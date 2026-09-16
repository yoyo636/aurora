"""Aurora CLI — 命令行工具入口"""

import sys
import os
import argparse

# 确保能导入 aurora 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.lexer import Lexer, LexerError
from aurora.parser import Parser, ParseError
from aurora.type_checker import TypeChecker
from aurora.ownership import OwnershipChecker
from aurora.interpreter import Interpreter
from aurora.stdlib import AuroraError
from aurora.repl import REPL
from aurora import __version__

# P2/P3 工具链与生态模块（延迟导入以加快启动速度）
def _register_toolchain(subparsers):
    """注册 P2 工具链与 P3 生态的 CLI 子命令。"""
    from aurora import formatter, profiler, debugger, lsp, pkg
    formatter.register_cli(subparsers)
    profiler.register_cli(subparsers)
    debugger.register_cli(subparsers)
    lsp.register_cli(subparsers)
    pkg.register_cli(subparsers)
    # v3.0.0 AI 引擎：ai train/infer、serve、kernel [install]
    from aurora.ai import kernel as _aurora_kernel
    _aurora_kernel.register_cli(subparsers)
    # v3.1.0 性能革命：bench 基准测试
    from aurora import benchmark as _v310_benchmark
    _v310_benchmark.register_cli(subparsers)
    # v3.1.0 超大型项目基础设施：workspace / deps / index
    from aurora import workspace_manager as _v310_workspace
    _v310_workspace.register_cli(subparsers)
    from aurora import dep_graph as _v310_depgraph
    _v310_depgraph.register_cli(subparsers)
    from aurora import project_index as _v310_index
    _v310_index.register_cli(subparsers)
    # v3.1.0 全平台 GUI 与应用开发：ui / package / browser
    from aurora.ui import register_cli as _v310_ui_register
    _v310_ui_register(subparsers)
    from aurora import packaging as _v310_packaging
    _v310_packaging.register_cli(subparsers)
    from aurora import browser_engine as _v310_browser
    _v310_browser.register_cli(subparsers)
    # v3.2.0 全栈开发：web / db / codegen CLI 命令
    # 注意: db / generate / dev / docs 命令由 main() 中的 cmd_db 等实现,
    # 此处不再调用 db_orm / codegen 的 register_cli(它们会劫持 new、
    # 覆盖子命令绑定并与本文件实现冲突),避免子解析器冲突。
    _register_v320_cli(subparsers)

def _register_v320_cli(subparsers):
    """安全注册 v3.2.0 模块的 CLI 命令，模块缺失时静默跳过。"""
    v320_modules = [
        'aurora.web_framework',  # aurora webapp
    ]
    for mod_path in v320_modules:
        try:
            import importlib
            mod = importlib.import_module(mod_path)
            register_fn = getattr(mod, 'register_cli', None)
            if callable(register_fn):
                register_fn(subparsers)
        except Exception:
            pass

def cmd_run(args):
    """运行 .aur 文件"""
    path = args.file
    if path is None:
        # 无参数时读取项目清单 aurora.toml 的入口
        if os.path.exists('aurora.toml'):
            cfg = parse_toml('aurora.toml')
            entry = None
            for sec in (cfg.get('build') or {}):
                if sec == 'entry':
                    entry = cfg['build']['entry']
            if entry and os.path.exists(entry):
                path = entry
            else:
                print(f"错误: aurora.toml 入口 '{entry}' 不存在")
                sys.exit(1)
        else:
            print("错误: 未指定文件,且当前目录没有 aurora.toml 入口")
            sys.exit(1)
    if not os.path.exists(path):
        print(f"错误: 文件不存在 '{path}'")
        sys.exit(1)
    
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    _compile_and_run(source, args, file_path=path)

def cmd_eval(args):
    """执行一行代码"""
    _compile_and_run(args.code, args)

def cmd_interop(args):
    """多语言互操作工具:列出语言桥 / 测试连接"""
    from aurora.stdlib import AuroraInterop, AuroraJS, AuroraJava
    if args.test or args.lang:
        langs = [args.lang] if args.lang else AuroraInterop.languages()
        for lang in langs:
            try:
                if lang == 'python':
                    result = AuroraInterop.eval('python', '1 + 1')
                    status = 'OK' if result == 2 else 'FAIL'
                elif lang == 'js':
                    if not AuroraJS.available():
                        status = 'SKIP (node not found)'
                    else:
                        result = AuroraJS.eval('1 + 1')
                        status = 'OK' if result == 2 else 'FAIL'
                elif lang == 'java':
                    if not AuroraJava.available():
                        status = 'SKIP (java not found)'
                    else:
                        result = AuroraJava.eval('1 + 1')
                        status = 'OK' if result == 2 else 'FAIL'
                elif lang in ('c', 'cpp', 'rust', 'go'):
                    status = 'FFI (requires shared library)'
                else:
                    status = 'UNKNOWN'
            except Exception as e:
                status = f'ERROR: {e}'
            print(f'  {lang:10s} {status}')
    else:
        status = AuroraInterop.status()
        print('Aurora 多语言互操作层 — 可用语言桥:')
        print(f'{"语言":10s} {"调用方式":20s} {"状态"}')
        print('-' * 50)
        methods = {
            'python': '直连 (AuroraPython)',
            'js': 'Node.js 子进程',
            'java': 'java/jshell 子进程',
            'c': 'FFI (C ABI)',
            'cpp': 'FFI (C ABI)',
            'rust': 'FFI (C ABI)',
            'go': 'FFI (cgo C ABI)',
        }
        for lang in AuroraInterop.languages():
            st = status.get(lang, 'unknown')
            print(f'{lang:10s} {methods.get(lang, ""):20s} {st}')

def cmd_gen_bindings(args):
    """为 Rust/C++/Go 生成 FFI 绑定模板"""
    from aurora.stdlib import AuroraFFI
    import json
    lang = args.lang.lower()
    if lang not in ('rust', 'cpp', 'go'):
        print(f'错误: 不支持的语言 {lang},可用 rust / cpp / go')
        sys.exit(1)
    if args.functions:
        try:
            functions = json.loads(args.functions)
        except json.JSONDecodeError as e:
            print(f'错误: 函数签名 JSON 解析失败: {e}')
            sys.exit(1)
    else:
        functions = [
            {"name": "add", "args": ["i32", "i32"], "ret": "i32"},
            {"name": "multiply", "args": ["f64", "f64"], "ret": "f64"},
            {"name": "greet", "args": ["str"], "ret": "str"},
        ]
    code = AuroraFFI.gen_bindings(lang, functions)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f'绑定代码已写入: {args.output}')
    else:
        print(code)

def cmd_wasm(args):
    """WASM 操作:列出导出函数 / 调用导出函数"""
    from aurora.stdlib import AuroraWASM
    import json
    if not AuroraWASM.available():
        print('错误: Node.js 不可用,WASM 功能需要 Node.js 环境')
        sys.exit(1)
    path = args.file
    if not os.path.exists(path):
        print(f'错误: 文件不存在 {path}')
        sys.exit(1)
    if args.call:
        try:
            wasm_args = json.loads(args.args) if args.args else []
        except json.JSONDecodeError:
            print('错误: --args 必须是 JSON 数组')
            sys.exit(1)
        module = AuroraWASM.load(path)
        result = AuroraWASM.call(module, args.call, *wasm_args)
        print(f'{args.call}({", ".join(map(str, wasm_args))}) = {result}')
    else:
        info = AuroraWASM.load(path)
        exports = info.get('exports', {})
        print(f'WASM 模块: {path}')
        print(f'导出函数 ({len(exports)} 个):')
        for name, typ in exports.items():
            print(f'  {name}: {typ}')

def parse_toml(path: str) -> dict:
    """解析 TOML 子集([section] 与 key = value)"""
    cfg: dict = {}
    section = None
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1].strip()
                cfg.setdefault(section, {})
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            k, v = k.strip(), v.strip()
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            else:
                try:
                    v = int(v)
                except ValueError:
                    pass
            if section:
                cfg[section][k] = v
            else:
                cfg[k] = v
    return cfg

def _template_main_source(template: str, name: str) -> str:
    """按模板返回 src/main.aur 的示例源码"""
    if template == 'api':
        return (
            '# ' + name + ' — REST API 项目入口(src/main.aur)\n'
            '# web 路由 + JSON 响应示例\n\n'
            'import std.web\n\n'
            'fn main() {\n'
            '    let app = web.App()\n'
            '    app.get("/", fn(ctx) { return ctx.json({"hello": "' + name + '"}) })\n'
            '    app.get("/api/items", fn(ctx) { return ctx.json({"items": []}) })\n'
            '    app.get("/api/items/:id", fn(ctx) { return ctx.json({"id": ctx.params.id}) })\n'
            '    app.serve(8000)\n'
            '}\n\n'
            'main()\n'
        )
    if template == 'cli':
        return (
            '# ' + name + ' — CLI 工具项目入口(src/main.aur)\n'
            '# 使用 std.cli 定义子命令\n\n'
            'import std.cli\n\n'
            'fn main() {\n'
            '    let app = cli.App(name="' + name + '")\n'
            '    app.command("greet", fn(args) {\n'
            '        let who = args.get(0, "世界")\n'
            '        println("你好, " + who)\n'
            '    })\n'
            '    app.command("version", fn(args) { println("' + name + ' v0.1.0") })\n'
            '    app.run()\n'
            '}\n\n'
            'main()\n'
        )
    if template == 'tui':
        return (
            '# ' + name + ' — TUI 应用项目入口(src/main.aur)\n'
            '# 使用 std.tui 构建终端界面\n\n'
            'import std.tui\n\n'
            'fn main() {\n'
            '    let ui = tui.App()\n'
            '    ui.title("' + name + '")\n'
            '    ui.box("按 q 退出")\n'
            '    ui.run()\n'
            '}\n\n'
            'main()\n'
        )
    if template == 'agent':
        return (
            '# ' + name + ' — AI Agent 项目入口(src/main.aur)\n'
            '# 使用 std.ai 调用大模型\n\n'
            'import std.ai\n'
            'import std.io\n\n'
            'fn main() {\n'
            '    let agent = ai.Agent(model="default")\n'
            '    agent.system("你是 ' + name + ' 的助手")\n'
            '    loop {\n'
            '        let msg = io.readline("you> ")\n'
            '        if msg == "exit" { break }\n'
            '        println("agent> " + agent.chat(msg))\n'
            '    }\n'
            '}\n\n'
            'main()\n'
        )
    # basic（默认）
    return (
        '# ' + name + ' — 项目入口(src/main.aur)\n\n'
        'import lib\n\n'
        'fn main() {\n'
        '    println(lib.greet("Aurora"))\n'
        '    println("2 + 3 = " + str(lib.add(2, 3)))\n'
        '}\n\n'
        'main()\n'
    )

def cmd_new(args):
    """创建新 Aurora 项目(脚手架 + 清单),支持 --template 选择模板"""
    name = args.name
    import re
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
        print(f"错误: 项目名 '{name}' 不合法(须以字母/下划线开头,仅字母数字下划线)")
        sys.exit(1)
    if os.path.exists(name):
        print(f"错误: 目录 '{name}' 已存在")
        sys.exit(1)

    template = getattr(args, 'template', 'basic')

    # fullstack 模板: 复用 fullstack.Scaffold 生成一体化全栈项目
    if template == 'fullstack':
        try:
            from aurora.fullstack import Scaffold
        except Exception as e:
            print(f"错误: fullstack 模板依赖模块加载失败: {e}")
            sys.exit(1)
        root = Scaffold().create_project(name, template='fullstack')
        print(f"创建全栈项目 {root}/")
        print(f"  ├─ api/        后端路由")
        print(f"  ├─ web/        前端页面")
        print(f"  ├─ shared/     共享类型")
        print(f"  ├─ migrations/ 数据库迁移")
        print(f"  └─ main.aurora 入口")
        print(f"下一步: cd {name} && aurora dev")
        return

    os.makedirs(name)
    os.makedirs(os.path.join(name, 'src'))
    os.makedirs(os.path.join(name, 'tests'))
    manifest = (
        f'[project]\n'
        f'name = "{name}"\n'
        f'version = "0.1.0"\n'
        f'description = "Aurora 项目(模板: {template})"\n'
        f'author = ""\n\n'
        f'[build]\n'
        f'entry = "src/main.aur"\n\n'
        f'[dependencies]\n'
        f'# 本地路径依赖示例:\n'
        f'# mylib = {{ path = "../mylib" }}\n'
    )
    main_src = _template_main_source(template, name)
    lib_src = (
        '# ' + name + ' — 库模块(src/lib.aur)\n'
        '# 可被 main.aur 通过 import lib 引用\n\n'
        'fn greet(name) {\n'
        '    return "你好, " + name + "!"\n'
        '}\n\n'
        'fn add(a, b) {\n'
        '    return a + b\n'
        '}\n'
    )
    test_src = (
        '# ' + name + ' — 测试(tests/' + name + '_test.aur)\n\n'
        'import lib\n\n'
        'fn test_add() {\n'
        '    assert lib.add(2, 3) == 5\n'
        '    println("test_add 通过")\n'
        '}\n\n'
        'fn test_greet() {\n'
        '    assert lib.greet("x") == "你好, x!"\n'
        '    println("test_greet 通过")\n'
        '}\n'
    )
    readme = (
        f'# {name}\n\n'
        f'Aurora 项目(语言 v1.1.0,模板: {template})。\n\n'
        f'## 项目结构\n\n'
        f'```\n'
        f'{name}/\n'
        f'├── aurora.toml      项目清单\n'
        f'├── src/\n'
        f'│   ├── main.aur    入口程序\n'
        f'│   └── lib.aur     库模块(可被 import)\n'
        f'├── tests/\n'
        f'│   └── {name}_test.aur  测试\n'
        f'└── README.md\n'
        f'```\n\n'
        f'## 运行\n\n'
        f'```bash\n'
        f'aurora run          # 读取 aurora.toml 入口(src/main.aur)\n'
        f'aurora build        # AOT 编译为 Python(输出 dist/)\n'
        f'```\n\n'
        f'## 测试\n\n'
        f'```bash\n'
        f'aurora test\n'
        f'```\n'
    )
    with open(os.path.join(name, 'aurora.toml'), 'w', encoding='utf-8') as f:
        f.write(manifest)
    with open(os.path.join(name, 'src', 'main.aur'), 'w', encoding='utf-8') as f:
        f.write(main_src)
    with open(os.path.join(name, 'src', 'lib.aur'), 'w', encoding='utf-8') as f:
        f.write(lib_src)
    with open(os.path.join(name, 'tests', name + '_test.aur'), 'w', encoding='utf-8') as f:
        f.write(test_src)
    with open(os.path.join(name, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)
    print(f"创建项目 {name}/  (模板: {template})")
    print(f"  ├─ aurora.toml      项目清单")
    print(f"  ├─ src/main.aur     入口程序")
    print(f"  ├─ src/lib.aur      库模块")
    print(f"  ├─ tests/           测试")
    print(f"  └─ README.md")
    print(f"下一步: cd {name} && aurora run")

def _needs_compile(src: str, dst: str) -> bool:
    """检查源文件是否需要重新编译(产物不存在或源文件更新)"""
    if not os.path.exists(dst):
        return True
    return os.path.getmtime(src) > os.path.getmtime(dst)

def cmd_build(args):
    """AOT 编译:将 .aur 项目编译为 Python 源码"""
    entry = getattr(args, 'file', None)
    if entry is None:
        if os.path.exists('aurora.toml'):
            cfg = parse_toml('aurora.toml')
            entry = (cfg.get('build') or {}).get('entry')
            if not entry:
                for cand in ('src/main.aur', 'main.aur'):
                    if os.path.exists(cand):
                        entry = cand
                        break
        if not entry:
            print("错误: 未指定入口文件,且未找到 aurora.toml 或 src/main.aur")
            sys.exit(1)
    if not os.path.exists(entry):
        print(f"错误: 入口文件不存在 '{entry}'")
        sys.exit(1)

    out_dir = getattr(args, 'out', 'dist')
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(entry))[0]
    out_path = os.path.join(out_dir, base + '.py')
    force = getattr(args, 'force', False)
    try:
        if force or _needs_compile(entry, out_path):
            compile_file(entry, out_path)
            print(f"✓ 编译: {entry} → {out_path}")
        else:
            print(f"⏭ 跳过(未变化): {entry}")
    except (LexerError, ParseError) as e:
        print(f"编译错误: {e}")
        sys.exit(1)
    except Exception as e:
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        else:
            print(f"编译错误: {e}")
        sys.exit(1)

    _build_local_modules(entry, out_dir, args, force)
    print(f"\n编译完成!运行: python3 {out_path}")

def cmd_build_native(args):
    """原生编译:将 .aur 文件编译为 C,然后用 gcc/clang 编译为原生机器码"""
    entry = getattr(args, 'file', None)
    if entry is None:
        if os.path.exists('aurora.toml'):
            cfg = parse_toml('aurora.toml')
            entry = (cfg.get('build') or {}).get('entry')
            if not entry:
                for cand in ('src/main.aur', 'main.aur'):
                    if os.path.exists(cand):
                        entry = cand
                        break
        if not entry:
            print("错误: 未指定入口文件,且未找到 aurora.toml 或 src/main.aur")
            sys.exit(1)
    if not os.path.exists(entry):
        print(f"错误: 入口文件不存在 '{entry}'")
        sys.exit(1)

    # 确定输出路径
    out_path = getattr(args, 'out', None)
    if out_path is None:
        base = os.path.splitext(os.path.basename(entry))[0]
        out_path = os.path.join(os.path.dirname(entry) or '.', base)

    optimize = getattr(args, 'optimize', '-O2')
    cc = getattr(args, 'cc', 'cc')
    keep_c = getattr(args, 'keep_c', False)
    verbose = getattr(args, 'verbose', False)

    print(f"\033[97m◡ Aurora 原生编译器\033[0m v{__version__}")
    print(f"  源文件: {entry}")
    print(f"  输出:   {out_path}")
    print(f"  优化:   {optimize}")
    print(f"  编译器: {cc}")
    print()

    try:
        from aurora.codegen import compile_to_binary
        binary_path, compile_output = compile_to_binary(
            entry, out_path,
            optimize=optimize, cc=cc
        )
        if verbose and compile_output:
            print(compile_output)

        # 显示文件大小
        if os.path.exists(binary_path):
            size = os.path.getsize(binary_path)
            if size > 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.2f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} B"
            print(f"\033[92m✓ 编译成功!\033[0m {binary_path} ({size_str})")
            print(f"\n运行: ./{binary_path}")
        else:
            print(f"\033[92m✓ 编译成功!\033[0m")

    except Exception as e:
        if verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"\033[91m✗ 编译失败:\033[0m {e}")
        sys.exit(1)

def cmd_build_asm(args):
    """ARM64 汇编编译命令"""
    entry = args.file
    if entry is None:
        entry = _resolve_project_entry()
    if not entry or not os.path.exists(entry):
        print(f"\033[91m✗ 文件不存在:\033[0m {entry}")
        sys.exit(1)

    out_path = args.out
    if out_path is None:
        base = os.path.splitext(os.path.basename(entry))[0]
        out_path = os.path.join(os.path.dirname(entry) or '.', base)

    verbose = getattr(args, 'verbose', False)

    print(f"\033[97m◡ Aurora ARM64 汇编编译器\033[0m v{__version__}")
    print(f"  源文件: {entry}")
    print(f"  输出:   {out_path}")
    print(f"  后端:   Aurora → ARM64 汇编 → as/ld → 原生可执行文件")
    print()

    try:
        from aurora.asmgen import compile_to_asm
        binary_path, compile_output = compile_to_asm(entry, out_path)
        if verbose and compile_output:
            print(compile_output)

        if os.path.exists(binary_path):
            size = os.path.getsize(binary_path)
            if size > 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.2f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} B"
            print(f"\033[92m✓ 编译成功!\033[0m {binary_path} ({size_str})")
            print(f"\n运行: ./{binary_path}")
        else:
            print(f"\033[92m✓ 编译成功!\033[0m")

    except Exception as e:
        if verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"\033[91m✗ 编译失败:\033[0m {e}")
        sys.exit(1)

def _build_local_modules(entry, out_dir, args, force=False):
    """扫描并编译 import 的本地模块(带缓存)"""
    import re
    with open(entry, 'r', encoding='utf-8') as f:
        source = f.read()
    entry_dir = os.path.dirname(os.path.abspath(entry))
    imports = re.findall(r'^\s*import\s+([a-zA-Z_][\w.]*)\s*(?:as\s+\w+)?\s*$', source, re.M)
    from_imports = re.findall(r'^\s*from\s+([a-zA-Z_][\w.]*)\s+import', source, re.M)
    for mod in set(imports) | set(from_imports):
        if mod.startswith('std.'):
            continue
        mod_path = mod.replace('.', os.sep)
        for cand in (mod_path + '.aur', os.path.join(mod_path, '__init__.aur')):
            full = os.path.join(entry_dir, cand)
            if os.path.exists(full):
                out = os.path.join(out_dir, mod.replace('.', '_') + '.py')
                try:
                    if force or _needs_compile(full, out):
                        compile_file(full, out)
                        print(f"✓ 编译模块: {mod} → {out}")
                    else:
                        print(f"⏭ 跳过模块(未变化): {mod}")
                except Exception as e:
                    print(f"  ⚠ 模块 {mod} 编译失败: {e}")
                break

def cmd_watch(args):
    """监听文件变化,自动运行(开发模式热重载)"""
    import time
    entry = getattr(args, 'file', None)
    if entry is None:
        if os.path.exists('aurora.toml'):
            cfg = parse_toml('aurora.toml')
            entry = (cfg.get('build') or {}).get('entry')
        if not entry:
            for cand in ('src/main.aur', 'main.aur'):
                if os.path.exists(cand):
                    entry = cand
                    break
    if not entry or not os.path.exists(entry):
        print("错误: 未找到入口文件")
        sys.exit(1)

    interval = getattr(args, 'interval', 0.5)
    print(f"👁  Aurora Watch — 监听 {entry} 及 src/ 目录")
    print(f"   间隔 {interval}s,Ctrl+C 退出")
    print("   首次运行...")

    def collect_files():
        files = {os.path.abspath(entry)}
        for root, dirs, fnames in os.walk('src'):
            for fn in fnames:
                if fn.endswith('.aur'):
                    files.add(os.path.abspath(os.path.join(root, fn)))
        return files

    def get_mtimes(files):
        return {f: os.path.getmtime(f) for f in files if os.path.exists(f)}

    def run_entry():
        print(f"\n{'─'*50}")
        print(f"▶ 运行 {entry} ({time.strftime('%H:%M:%S')})")
        print('─'*50)
        try:
            source = open(entry, 'r', encoding='utf-8').read()
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interp = Interpreter()
            interp.run(program, file_path=os.path.abspath(entry))
        except (LexerError, ParseError) as e:
            print(f"编译错误: {e}")
        except Exception as e:
            print(f"运行错误: {e}")

    run_entry()
    last_mtimes = get_mtimes(collect_files())

    try:
        while True:
            time.sleep(interval)
            files = collect_files()
            current = get_mtimes(files)
            changed = [f for f in current if f not in last_mtimes or current[f] != last_mtimes.get(f)]
            removed = [f for f in last_mtimes if f not in current]
            if changed or removed:
                for f in changed:
                    print(f"\n📝 变化: {os.path.relpath(f)}")
                run_entry()
                last_mtimes = current
    except KeyboardInterrupt:
        print("\n\n👋 Watch 已退出")

def _collect_test_fns(source: str) -> list:
    """收集源码中顶层 test_* 函数名"""
    import re
    return re.findall(r'^\s*fn\s+(test_\w+)\s*\(', source, re.M)

def _run_test_source(source: str, label: str):
    """运行测试源码;返回 (ok, message)"""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interp = Interpreter()
        interp.run(program)
        return True, "通过"
    except AuroraError as e:
        if e.kind == 'AssertError':
            return False, f"断言失败: {e}"
        return False, f"{e.kind}: {e}"
    except (LexerError, ParseError) as e:
        return False, f"解析错误: {e}"
    except Exception as e:
        return False, f"异常: {e}"

def cmd_test(args):
    """测试运行器:收集 *_test.aur 文件与 test_* 函数并运行"""
    root = args.path or '.'
    if os.path.isfile(root):
        files = [os.path.abspath(root)]
    else:
        files = []
        skip = {'.git', '__pycache__', 'node_modules', '.venv', 'target', '.app'}
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip]
            for n in filenames:
                if n.endswith('.aur'):
                    files.append(os.path.join(dirpath, n))
        files.sort()

    if not files:
        print("未找到 .aur 文件")
        return

    passed = failed = 0
    skipped = 0
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                src = fh.read()
        except OSError as e:
            print(f"[ERR]  {f}: 读取失败 {e}")
            failed += 1
            continue

        is_test_file = (os.path.basename(f).endswith('_test.aur')
                        or os.path.basename(f).endswith('_tests.aur'))
        tests = _collect_test_fns(src)

        if is_test_file:
            ok, msg = _run_test_source(src, f)
            if ok:
                print(f"[PASS] {f}"); passed += 1
            else:
                print(f"[FAIL] {f}: {msg}"); failed += 1
        elif tests:
            for tname in tests:
                ok, msg = _run_test_source(src + f"\n{tname}()\n", f)
                if ok:
                    print(f"[PASS] {f} :: {tname}"); passed += 1
                else:
                    print(f"[FAIL] {f} :: {tname}: {msg}"); failed += 1
        else:
            skipped += 1

    print()
    print(f"共 {passed + failed + skipped} 个文件: {passed} 通过, {failed} 失败, {skipped} 跳过(无测试)")
    if failed:
        sys.exit(1)


def cmd_check(args):
    """类型检查与所有权检查（不执行）"""
    path = args.file
    if not os.path.exists(path):
        print(f"错误: 文件不存在 '{path}'")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()

    print(f"检查: {path}")

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
    except (LexerError, ParseError) as e:
        print(f"  解析错误: {e}")
        sys.exit(1)

    tc = TypeChecker()
    type_errors = tc.check(program)
    if type_errors:
        print(f"  类型错误 {len(type_errors)} 个:")
        for err in type_errors:
            print(f"    - {err}")
        sys.exit(1)
    print("  类型检查通过 ✓")

    oc = OwnershipChecker()
    own_errors = oc.check(program)
    if own_errors:
        print(f"  所有权错误 {len(own_errors)} 个:")
        for err in own_errors:
            print(f"    - {err}")
        sys.exit(1)
    print("  所有权检查通过 ✓")


def cmd_repl(args):
    """启动交互式 REPL"""
    repl = REPL()
    repl.run()

def cmd_tokens(args):
    """显示词法分析结果"""
    path = args.file
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    for tok in tokens:
        print(tok)

def cmd_ast(args):
    """显示 AST 结构"""
    path = args.file
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    _print_tree(program)

def _compile_and_run(source, args, file_path=None):
    """编译并运行源码"""
    try:
        # 词法分析
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # 语法分析
        parser = Parser(tokens)
        program = parser.parse()
        
        # 类型检查（警告模式，不阻塞执行）
        if not getattr(args, 'no_type_check', False):
            tc = TypeChecker()
            type_errors = tc.check(program)
            if type_errors and getattr(args, 'strict', False):
                print("类型错误:")
                for err in type_errors:
                    print(f"  - {err}")
                sys.exit(1)
        
        # 所有权检查
        if not getattr(args, 'no_ownership_check', False):
            oc = OwnershipChecker()
            own_errors = oc.check(program)
            if own_errors and getattr(args, 'strict', False):
                print("所有权错误:")
                for err in own_errors:
                    print(f"  - {err}")
                sys.exit(1)
        
        # 执行
        interpreter = Interpreter()
        interpreter.run(program, file_path=file_path)
        
    except LexerError as e:
        print(f"词法错误: {e}")
        sys.exit(1)
    except ParseError as e:
        print(f"解析错误: {e}")
        sys.exit(1)
    except Exception as e:
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        else:
            print(f"运行时错误: {e}")
        sys.exit(1)

def _print_tree(node, indent=0, prefix=""):
    """递归打印 AST 树"""
    pad = "  " * indent
    cls_name = node.__class__.__name__
    
    if hasattr(node, '__dataclass_fields__'):
        # 获取关键字段
        key_fields = {}
        for f in node.__dataclass_fields__:
            v = getattr(node, f)
            if v is not None and v != [] and v != "" and f not in ('line', 'column'):
                key_fields[f] = v
        
        if key_fields:
            print(f"{pad}{prefix}{cls_name}")
            for fname, fval in key_fields.items():
                if isinstance(fval, list):
                    if fval and hasattr(fval[0], '__dataclass_fields__'):
                        print(f"{pad}  {fname}:")
                        for item in fval:
                            _print_tree(item, indent + 2)
                    else:
                        print(f"{pad}  {fname}: {fval!r}")
                elif hasattr(fval, '__dataclass_fields__'):
                    print(f"{pad}  {fname}:")
                    _print_tree(fval, indent + 2)
                else:
                    print(f"{pad}  {fname}: {fval!r}")
        else:
            print(f"{pad}{prefix}{cls_name}")
    else:
        print(f"{pad}{prefix}{node!r}")

# ─────────────────────────────────────────────────────────────────────
# v3.2.0 开发效率命令: generate / dev / docs / db
# ─────────────────────────────────────────────────────────────────────

def _write_file(path: str, content: str) -> None:
    """写入文本文件,自动创建父目录"""
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def _to_snake(name: str) -> str:
    """PascalCase/camelCase -> snake_case"""
    import re
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def _to_camel(name: str) -> str:
    """任意命名 -> PascalCase 类名(保留原有大小写)"""
    import re
    parts = re.split(r'[_\-\s]+', name)
    return ''.join(p[:1].upper() + p[1:] for p in parts if p)

def cmd_generate(args):
    """代码生成器: model / controller / migration / component / service"""
    sub = getattr(args, 'gen_command', None)
    if not sub:
        print("用法: aurora generate <model|controller|migration|component|service> [参数]")
        print("示例:")
        print("  aurora generate model User name:str email:str age:int")
        print("  aurora generate controller User")
        print("  aurora generate migration add_users_table")
        print("  aurora generate component UserCard")
        print("  aurora generate service User")
        sys.exit(1)

    os.makedirs('src', exist_ok=True)

    if sub == 'model':
        cls = _to_camel(args.name)
        path = os.path.join('src', 'models', _to_snake(cls) + '.aur')
        fields = args.fields or ['id:int', 'name:str']
        lines = [f'// 自动生成的 ORM 模型 — {cls}', 'import std.db', '', f'class {cls}(Model) {{']
        for fdef in fields:
            if ':' in fdef:
                fn_, ft_ = fdef.split(':', 1)
            else:
                fn_, ft_ = fdef, 'str'
            if fn_ == 'id':
                lines.append(f'    {fn_} = Field(type="{ft_}", primary_key=true, autoincrement=true)')
            else:
                lines.append(f'    {fn_} = Field(type="{ft_}")')
        lines.append('}')
        _write_file(path, '\n'.join(lines) + '\n')
        print(f'✓ 生成模型: {path}')

    elif sub == 'controller':
        cls = _to_camel(args.name)
        path = os.path.join('src', 'controllers', _to_snake(cls) + '_controller.aur')
        code = (
            f'// 自动生成的控制器 — {cls}Controller\n'
            'import std.web\n\n'
            f'// {cls} 资源的 CRUD 路由处理\n'
            'fn list(req)   { return req.json({"items": []}) }\n'
            'fn get(req)    { return req.json({"id": req.params.id}) }\n'
            'fn create(req) { return req.json({"created": true, "data": req.body}) }\n'
            'fn update(req) { return req.json({"updated": true, "id": req.params.id}) }\n'
            'fn remove(req)  { return req.json({"deleted": true, "id": req.params.id}) }\n\n'
            'fn register(r) {\n'
            '    r.get("/", list)\n'
            '    r.get("/:id", get)\n'
            '    r.post("/", create)\n'
            '    r.put("/:id", update)\n'
            '    r.delete("/:id", remove)\n'
            '}\n'
        )
        _write_file(path, code)
        print(f'✓ 生成控制器: {path}')

    elif sub == 'migration':
        import re
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', args.name)
        existing = []
        if os.path.isdir('migrations'):
            for fn in os.listdir('migrations'):
                m = re.match(r'^(\d+)_.+\.py$', fn)
                if m:
                    existing.append(int(m.group(1)))
        version = f'{(max(existing) if existing else 0) + 1:04d}'
        path = os.path.join('migrations', f'{version}_{safe}.py')
        code = (
            f'"""自动生成的迁移文件 — {version}_{safe}"""\n\n'
            'def up(conn):\n'
            '    """向上迁移: 在此编写建表/改表 SQL"""\n'
            '    # conn.execute("CREATE TABLE ...")\n'
            '    pass\n\n\n'
            'def down(conn):\n'
            '    """向下迁移(回滚)"""\n'
            '    # conn.execute("DROP TABLE ...")\n'
            '    pass\n'
        )
        _write_file(path, code)
        print(f'✓ 生成迁移: {path}')

    elif sub == 'component':
        cls = _to_camel(args.name)
        path = os.path.join('src', 'components', _to_snake(cls) + '.aur')
        code = (
            f'// 自动生成的前端组件 — {cls}\n'
            'import std.web.ui\n\n'
            f'fn {cls}(props) {{\n'
            f'    return ui.div({{"class": "{_to_snake(cls)}"}}, [\n'
            f'        ui.h1({{}}, props.get("title", "{cls}")),\n'
            f'        ui.p({{}}, props.get("body", "组件内容")),\n'
            f'    ])\n'
            f'}}\n'
        )
        _write_file(path, code)
        print(f'✓ 生成组件: {path}')

    elif sub == 'service':
        cls = _to_camel(args.name)
        path = os.path.join('src', 'services', _to_snake(cls) + '_service.aur')
        code = (
            f'// 自动生成的服务层 — {cls}Service\n'
            '// 业务逻辑层: 与控制器解耦\n\n'
            'fn get_all()    { return [] }\n'
            'fn get_by_id(id) { return null }\n'
            'fn create(data) { return data }\n'
            'fn update(id, data) { return data }\n'
            'fn delete(id)   { return true }\n'
        )
        _write_file(path, code)
        print(f'✓ 生成服务: {path}')

def cmd_dev(args):
    """开发服务器: 监听文件变化,自动重启后端 + 前端 HMR"""
    import time
    entry = getattr(args, 'file', None)
    if entry is None:
        if os.path.exists('aurora.toml'):
            cfg = parse_toml('aurora.toml')
            entry = (cfg.get('build') or {}).get('entry')
        if not entry:
            for cand in ('src/main.aur', 'main.aur'):
                if os.path.exists(cand):
                    entry = cand
                    break
    if not entry or not os.path.exists(entry):
        print("错误: 未找到入口文件")
        sys.exit(1)

    port = getattr(args, 'port', 3000)
    interval = getattr(args, 'interval', 0.5)
    watch_dirs = [d for d in ('src', 'api', 'web') if os.path.isdir(d)]

    print(f"🛠  Aurora Dev Server  v{__version__}")
    print(f"   入口: {entry}")
    print(f"   端口: {port}  (前端 HMR)")
    print(f"   监听: {', '.join(watch_dirs) or '.'}  Ctrl+C 退出")

    # 尝试接入 fullstack.HotReloader;失败则回退到内置轮询
    changed = []
    reloader = None
    try:
        from aurora.fullstack import HotReloader
        reloader = HotReloader(debounce_ms=200)
        reloader.watch(watch_dirs or ['.'],
                       extensions=['.aur', '.aurora', '.html', '.css', '.js'],
                       on_change=lambda p: changed.append(p),
                       poll_interval=interval,
                       ignore_patterns=['.git', '__pycache__', 'dist', 'node_modules'])
        hmr_js = HotReloader.generate_hmr_client(port)
        print(f"   HMR 客户端: 已生成(可注入前端页面)")
    except Exception as e:
        print(f"   (提示: HotReloader 不可用,使用内置轮询监听: {e})")
        hmr_js = None

    def collect_files():
        files = {os.path.abspath(entry)}
        for d in watch_dirs or ['.']:
            for root, dirs_, fnames in os.walk(d):
                for fn in fnames:
                    if fn.endswith(('.aur', '.aurora', '.html', '.css', '.js')):
                        files.add(os.path.abspath(os.path.join(root, fn)))
        return files

    def run_entry():
        print(f"\n{'─'*50}")
        print(f"▶ 运行 {entry} ({time.strftime('%H:%M:%S')})")
        print('─'*50)
        try:
            source = open(entry, 'r', encoding='utf-8').read()
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interp = Interpreter()
            interp.run(program, file_path=os.path.abspath(entry))
        except (LexerError, ParseError) as e:
            print(f"编译错误: {e}")
        except Exception as e:
            print(f"运行错误: {e}")

    run_entry()
    last_mtimes = {f: os.path.getmtime(f) for f in collect_files()}

    try:
        while True:
            time.sleep(interval)
            if reloader is not None and changed:
                for p in changed:
                    print(f"\n📝 变化: {os.path.relpath(p)}")
                changed.clear()
                run_entry()
                last_mtimes = {f: os.path.getmtime(f) for f in collect_files()}
                continue
            current = {f: os.path.getmtime(f) for f in collect_files() if os.path.exists(f)}
            diff = [f for f in current if current[f] != last_mtimes.get(f)]
            if diff:
                for f in diff:
                    print(f"\n📝 变化: {os.path.relpath(f)}")
                run_entry()
                last_mtimes = current
    except KeyboardInterrupt:
        if reloader is not None:
            reloader.stop()
        print("\n\n👋 Dev Server 已退出")

def cmd_docs(args):
    """API 文档服务器: 从项目路由生成 OpenAPI 3.0 并展示 Swagger UI"""
    import re
    import json as _json
    port = getattr(args, 'port', 8080)

    # 1. 扫描项目中的路由定义
    routes = []
    for cand in ('src/routes.aur', 'api/routes.aur', 'main.aurora', 'src/main.aur'):
        if not os.path.exists(cand):
            continue
        with open(cand, 'r', encoding='utf-8') as f:
            text = f.read()
        found = re.findall(
            r'(get|post|put|patch|delete)\s*\(?\s*["\'`]([^"\'`]+)["\'`]',
            text, re.IGNORECASE)
        if found:
            print(f"   从 {cand} 发现 {len(found)} 条路由")
        routes.extend((m.upper(), p) for m, p in found)

    # 2. 生成 OpenAPI 3.0 文档 (优先复用 fullstack.ApiGenerator)
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "Aurora API", "version": "1.0.0"},
        "paths": {},
    }
    try:
        from aurora.fullstack import ApiGenerator
        gen = ApiGenerator()
        for method, path in routes:
            gen.register_route(method, path, handler=path)
        spec_text = gen.generate_api_docs(gen.routes, '.aurora/openapi.json')
        spec = _json.loads(spec_text)
    except Exception as e:
        print(f"   (提示: ApiGenerator 不可用,使用内置 OpenAPI 生成: {e})")
        for method, path in routes:
            spec["paths"].setdefault(path, {})[method.lower()] = {
                "summary": path,
                "responses": {"200": {"description": "OK"}},
            }

    out = getattr(args, 'output', None)
    if out:
        _write_file(out, _json.dumps(spec, indent=2, ensure_ascii=False))
        print(f"   OpenAPI 文档已导出: {out}")

    spec_bytes = _json.dumps(spec, indent=2, ensure_ascii=False).encode('utf-8')
    html_page = """<!doctype html>
<html><head>
<meta charset="utf-8">
<title>Aurora API Docs</title>
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head><body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
<script>
window.onload = () => SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger-ui" });
</script></body></html>"""
    html_bytes = html_page.encode('utf-8')

    from http.server import BaseHTTPRequestHandler, HTTPServer

    class _DocsHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.split('?')[0] == '/openapi.json':
                body, ctype = spec_bytes, 'application/json; charset=utf-8'
            else:
                body, ctype = html_bytes, 'text/html; charset=utf-8'
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *a):
            pass

    print(f"\n📚  Aurora API 文档服务器")
    print(f"   路由数: {len(routes)}")
    print(f"   文档地址:    http://127.0.0.1:{port}/")
    print(f"   OpenAPI JSON: http://127.0.0.1:{port}/openapi.json")
    print(f"   Ctrl+C 退出\n")
    try:
        HTTPServer(('0.0.0.0', port), _DocsHandler).serve_forever()
    except KeyboardInterrupt:
        print("\n👋 文档服务器已退出")

def cmd_db(args):
    """数据库管理: migrate / seed / status"""
    sub = getattr(args, 'db_command', None)
    if not sub:
        print("用法: aurora db <migrate|seed|status>")
        sys.exit(1)
    try:
        from aurora import db_orm
    except Exception as e:
        print(f"错误: 数据库模块 db_orm 加载失败: {e}")
        sys.exit(1)

    db_url = getattr(args, 'database', None) or 'sqlite:///./aurora.db'
    try:
        conn = db_orm.Connection(db_url)
        conn.connect()
    except Exception as e:
        print(f"错误: 数据库连接失败 ({db_url}): {e}")
        sys.exit(1)
    migration = db_orm.Migration(conn, 'migrations')

    if sub == 'migrate':
        print(f"🗄  数据库迁移 ({db_url})")
        migration.migrate()
        print("✓ 迁移完成")
    elif sub == 'seed':
        print("🌱  种子数据")
        seed = db_orm.Seed(conn)
        print("   内置假数据生成器: fake_name / fake_email / fake_text / fake_number")
        print("   提示: 在项目 seeder 中调用 seed.run([(Model, count), ...]) 填充数据")
    elif sub == 'status':
        applied = set(migration.status())
        files = migration._list_migration_files()
        print(f"🗄  迁移状态 ({db_url})")
        if not files:
            print("   migrations/ 目录为空 — 用 aurora generate migration <name> 创建")
        for version, name, fname in files:
            mark = "✓ 已应用" if version in applied else "· 待执行"
            print(f"   {version}_{name}  {mark}")
        cur = migration.manager.get_current_version()
        print(f"   当前版本: {cur or '(无)'}")

def main():
    parser = argparse.ArgumentParser(
        prog='aurora',
        description='\033[97m◡ Aurora\033[0m — 寻求将代码转化为智能的最优解',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='\033[90m示例: aurora new myapp && cd myapp && aurora run\033[0m'
    )
    parser.add_argument('--version', action='version', version=f'\033[97m◡ Aurora\033[0m v{__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # run
    p_run = subparsers.add_parser('run', help='运行 .aur 文件(无参数时读取 aurora.toml 入口)')
    p_run.add_argument('file', nargs='?', help='源文件路径')
    p_run.add_argument('--strict', action='store_true', help='严格模式（类型/所有权错误时终止）')
    p_run.add_argument('--no-type-check', action='store_true', help='跳过类型检查')
    p_run.add_argument('--no-ownership-check', action='store_true', help='跳过所有权检查')
    p_run.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    p_run.set_defaults(func=cmd_run)
    
    # eval
    p_eval = subparsers.add_parser('eval', help='执行一行代码')
    p_eval.add_argument('code', help='要执行的代码')
    p_eval.add_argument('-v', '--verbose', action='store_true')
    p_eval.set_defaults(func=cmd_eval)
    
    # check
    p_check = subparsers.add_parser('check', help='类型检查与所有权检查')
    p_check.add_argument('file', help='源文件路径')
    p_check.set_defaults(func=cmd_check)
    
    # repl
    p_repl = subparsers.add_parser('repl', help='启动交互式 REPL')
    p_repl.set_defaults(func=cmd_repl)
    
    # tokens
    p_tokens = subparsers.add_parser('tokens', help='显示词法分析结果')
    p_tokens.add_argument('file', help='源文件路径')
    p_tokens.set_defaults(func=cmd_tokens)
    
    # ast
    p_ast = subparsers.add_parser('ast', help='显示 AST 结构')
    p_ast.add_argument('file', help='源文件路径')
    p_ast.set_defaults(func=cmd_ast)

    # new
    p_new = subparsers.add_parser('new', help='创建新 Aurora 项目(脚手架 + aurora.toml 清单)')
    p_new.add_argument('name', help='项目名')
    p_new.add_argument('-t', '--template', default='basic',
                       choices=['basic', 'fullstack', 'api', 'cli', 'tui', 'agent'],
                       help='项目模板 (默认 basic)')
    p_new.set_defaults(func=cmd_new)

    # test
    p_test = subparsers.add_parser('test', help='运行测试(*_test.aur 文件与 test_* 函数)')
    p_test.add_argument('path', nargs='?', default='.', help='目录或文件(默认当前目录)')
    p_test.set_defaults(func=cmd_test)

    # build
    p_build = subparsers.add_parser('build', help='AOT 编译为 Python 源码')
    p_build.add_argument('file', nargs='?', default=None, help='入口 .aur 文件(默认读 aurora.toml)')
    p_build.add_argument('-o', '--out', default='dist', help='输出目录(默认 dist)')
    p_build.add_argument('-f', '--force', action='store_true', help='强制重新编译(忽略缓存)')
    p_build.add_argument('-v', '--verbose', action='store_true', help='显示详细错误')
    p_build.set_defaults(func=cmd_build)

    # build-native
    p_build_native = subparsers.add_parser('build-native', help='原生编译为机器码(Aurora → C → 原生可执行文件)')
    p_build_native.add_argument('file', nargs='?', default=None, help='入口 .aur 文件(默认读 aurora.toml)')
    p_build_native.add_argument('-o', '--out', default=None, help='输出可执行文件路径')
    p_build_native.add_argument('-O', '--optimize', default='-O2', choices=['-O0', '-O1', '-O2', '-O3', '-Os'], help='优化级别(默认 -O2)')
    p_build_native.add_argument('--cc', default='cc', help='C 编译器(默认 cc,可用 clang/gcc)')
    p_build_native.add_argument('--keep-c', action='store_true', help='保留生成的 C 源文件')
    p_build_native.add_argument('-v', '--verbose', action='store_true', help='显示详细编译输出')
    p_build_native.set_defaults(func=cmd_build_native)

    # build-asm
    p_build_asm = subparsers.add_parser('build-asm', help='ARM64 汇编编译(Aurora → 汇编 → 原生可执行文件,不依赖 C 编译器)')
    p_build_asm.add_argument('file', nargs='?', default=None, help='入口 .aur 文件(默认读 aurora.toml)')
    p_build_asm.add_argument('-o', '--out', default=None, help='输出可执行文件路径')
    p_build_asm.add_argument('-v', '--verbose', action='store_true', help='显示详细编译输出')
    p_build_asm.set_defaults(func=cmd_build_asm)

    # watch
    p_watch = subparsers.add_parser('watch', help='监听文件变化,自动运行(开发模式)')
    p_watch.add_argument('file', nargs='?', default=None, help='入口 .aur 文件(默认读 aurora.toml)')
    p_watch.add_argument('-i', '--interval', type=float, default=0.5, help='检查间隔秒数(默认 0.5)')
    p_watch.set_defaults(func=cmd_watch)

    # interop
    p_interop = subparsers.add_parser('interop', help='多语言互操作工具（列出语言桥/测试连接）')
    p_interop.add_argument('--list', action='store_true', help='列出所有可用语言桥')
    p_interop.add_argument('--test', action='store_true', help='测试所有语言桥连接')
    p_interop.add_argument('--lang', type=str, default=None, help='仅测试指定语言')
    p_interop.set_defaults(func=cmd_interop)

    # gen-bindings
    p_gen = subparsers.add_parser('gen-bindings', help='为 Rust/C++/Go 生成 FFI 绑定模板')
    p_gen.add_argument('lang', help='目标语言: rust / cpp / go')
    p_gen.add_argument('-f', '--functions', type=str, default=None, help='函数签名 JSON 数组')
    p_gen.add_argument('-o', '--output', type=str, default=None, help='输出文件路径')
    p_gen.add_argument('--lib', type=str, default='aurora_ffi', help='库名')
    p_gen.set_defaults(func=cmd_gen_bindings)

    # wasm
    p_wasm = subparsers.add_parser('wasm', help='WebAssembly 操作（列出导出/调用函数）')
    p_wasm.add_argument('file', help='.wasm 文件路径')
    p_wasm.add_argument('--exports', action='store_true', help='列出导出函数（默认）')
    p_wasm.add_argument('--call', type=str, default=None, help='调用指定导出函数')
    p_wasm.add_argument('--args', type=str, default=None, help='调用参数 JSON 数组')
    p_wasm.set_defaults(func=cmd_wasm)

    # generate (v3.2.0 代码生成器)
    p_generate = subparsers.add_parser('generate',
        help='代码生成器: model/controller/migration/component/service')
    gen_sub = p_generate.add_subparsers(dest='gen_command')
    g_model = gen_sub.add_parser('model', help='生成 ORM 模型')
    g_model.add_argument('name', help='模型名 (PascalCase, 如 User)')
    g_model.add_argument('fields', nargs='*', help='字段定义 field:type (如 name:str age:int)')
    g_ctrl = gen_sub.add_parser('controller', help='生成控制器(web 路由处理)')
    g_ctrl.add_argument('name', help='资源名 (如 User)')
    g_mig = gen_sub.add_parser('migration', help='生成数据库迁移文件')
    g_mig.add_argument('name', help='迁移名 (如 add_users_table)')
    g_comp = gen_sub.add_parser('component', help='生成前端组件')
    g_comp.add_argument('name', help='组件名 (PascalCase, 如 UserCard)')
    g_svc = gen_sub.add_parser('service', help='生成服务层')
    g_svc.add_argument('name', help='服务名 (如 User)')
    p_generate.set_defaults(func=cmd_generate)

    # dev (v3.2.0 开发服务器)
    p_dev = subparsers.add_parser('dev', help='开发服务器: 文件监听 + 自动重启 + 前端 HMR')
    p_dev.add_argument('file', nargs='?', default=None, help='入口 .aur 文件(默认读 aurora.toml)')
    p_dev.add_argument('-p', '--port', type=int, default=3000, help='开发服务器端口(默认 3000)')
    p_dev.add_argument('-i', '--interval', type=float, default=0.5, help='文件检查间隔秒数(默认 0.5)')
    p_dev.set_defaults(func=cmd_dev)

    # docs (v3.2.0 API 文档服务器)
    p_docs = subparsers.add_parser('docs', help='API 文档服务器: OpenAPI 3.0 + Swagger UI')
    p_docs.add_argument('-p', '--port', type=int, default=8080, help='文档服务器端口(默认 8080)')
    p_docs.add_argument('-o', '--output', default=None, help='额外导出 openapi.json 到指定路径')
    p_docs.set_defaults(func=cmd_docs)

    # db (v3.2.0 数据库管理)
    p_db = subparsers.add_parser('db', help='数据库管理: migrate / seed / status')
    p_db.add_argument('-d', '--database', default=None,
                      help='数据库 URL (默认 sqlite:///./aurora.db)')
    db_sub = p_db.add_subparsers(dest='db_command')
    db_sub.add_parser('migrate', help='执行待应用迁移')
    db_sub.add_parser('seed', help='运行种子数据')
    db_sub.add_parser('status', help='显示迁移状态')
    p_db.set_defaults(func=cmd_db)

    # P2 工具链 + P3 生态命令（fmt/profile/debug/lsp/pkg）
    _register_toolchain(subparsers)

    args = parser.parse_args()
    
    if not args.command:
        # 默认启动 REPL
        cmd_repl(args)
    else:
        args.func(args)

if __name__ == '__main__':
    main()
