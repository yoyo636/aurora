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

def cmd_new(args):
    """创建新 Aurora 项目(脚手架 + 清单)"""
    name = args.name
    import re
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
        print(f"错误: 项目名 '{name}' 不合法(须以字母/下划线开头,仅字母数字下划线)")
        sys.exit(1)
    if os.path.exists(name):
        print(f"错误: 目录 '{name}' 已存在")
        sys.exit(1)

    os.makedirs(name)
    os.makedirs(os.path.join(name, 'src'))
    os.makedirs(os.path.join(name, 'tests'))
    manifest = (
        f'[project]\n'
        f'name = "{name}"\n'
        f'version = "0.1.0"\n'
        f'description = "Aurora 项目"\n'
        f'author = ""\n\n'
        f'[build]\n'
        f'entry = "src/main.aur"\n\n'
        f'[dependencies]\n'
        f'# 本地路径依赖示例:\n'
        f'# mylib = {{ path = "../mylib" }}\n'
    )
    main_src = (
        '# ' + name + ' — 项目入口(src/main.aur)\n\n'
        'import lib\n\n'
        'fn main() {\n'
        '    println(lib.greet("Aurora"))\n'
        '    println("2 + 3 = " + str(lib.add(2, 3)))\n'
        '}\n\n'
        'main()\n'
    )
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
        f'Aurora 项目(语言 v1.1.0)。\n\n'
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
    print(f"创建项目 {name}/")
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
        from .codegen import compile_to_binary
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

    # watch
    p_watch = subparsers.add_parser('watch', help='监听文件变化,自动运行(开发模式)')
    p_watch.add_argument('file', nargs='?', default=None, help='入口 .aur 文件(默认读 aurora.toml)')
    p_watch.add_argument('-i', '--interval', type=float, default=0.5, help='检查间隔秒数(默认 0.5)')
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    
    if not args.command:
        # 默认启动 REPL
        cmd_repl(args)
    else:
        args.func(args)

if __name__ == '__main__':
    main()
