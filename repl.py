"""Aurora REPL — 交互式解释器"""

import sys
from .lexer import Lexer
from .parser import Parser, ParseError
from .interpreter import Interpreter
from .type_checker import TypeChecker
from .ownership import OwnershipChecker
from . import __version__


BANNER = f"""
    ___                   __
   /   | __  __________  / /__________ _
  / /| |/ / / / ___/ _ \\/ __/ ___/ _ `/
 / ___ / /_/ / /  /  __/ /_/ /  / /_/ /
/_/  |_\\__,_/_/   \\___/\\__/_/   \\__,_/

 Aurora v{__version__} — 融合 Rust / Python / Go / TypeScript
 输入 :help 查看帮助，:quit 退出
"""

HELP_TEXT = """
命令:
  :help          显示帮助
  :quit / :exit  退出
  :type <expr>   显示表达式类型
  :ast <code>    显示 AST 结构
  :tokens <code> 显示词法分析结果
  :clear         清屏
  :env           显示当前环境变量

示例:
  let x = 42
  fn greet(name: str) { println("Hello, {name}!") }
  greet("Aurora")
"""


class REPL:
    def __init__(self):
        self.interpreter = Interpreter()
        self.type_checker = TypeChecker()
        self.ownership_checker = OwnershipChecker()
    
    def run(self):
        print(BANNER)
        while True:
            try:
                line = input("aurora> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见！")
                break
            
            if not line:
                continue
            
            # 多行输入（遇到未闭合的 { 继续读取）
            while line.count('{') > line.count('}'):
                try:
                    cont = input("    ... ").strip()
                    line += '\n' + cont
                except (EOFError, KeyboardInterrupt):
                    break
            
            self._process(line)
    
    def _process(self, line: str):
        # 命令处理
        if line.startswith(':'):
            self._handle_command(line)
            return
        
        try:
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            result = self.interpreter.run(program)
            if result is not None:
                print(f"  => {result!r}")
        except ParseError as e:
            print(f"  解析错误: {e}")
        except Exception as e:
            print(f"  运行时错误: {e}")
    
    def _handle_command(self, cmd: str):
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if command in (':quit', ':exit', ':q'):
            print("再见！")
            sys.exit(0)
        elif command == ':help':
            print(HELP_TEXT)
        elif command == ':type':
            self._show_type(arg)
        elif command == ':ast':
            self._show_ast(arg)
        elif command == ':tokens':
            self._show_tokens(arg)
        elif command == ':env':
            self._show_env()
        elif command == ':clear':
            print('\033[2J\033[H', end='')
        else:
            print(f"  未知命令: {command}，输入 :help 查看帮助")
    
    def _show_type(self, code: str):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            errors = self.type_checker.check(program)
            if errors:
                for e in errors:
                    print(f"  类型错误: {e}")
                return
            # 显示最后一条语句的类型
            from .ast_nodes import ExprStmt
            last = None
            for stmt in program.statements:
                last = stmt
            if isinstance(last, ExprStmt):
                inferred = self.type_checker._infer_expr(
                    last.expr, self.type_checker.global_env)
                print(f"  {inferred!r}")
            elif last is not None:
                print(f"  {last.__class__.__name__}")
        except Exception as e:
            print(f"  错误: {e}")
    
    def _show_ast(self, code: str):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            self._print_ast(program, 0)
        except Exception as e:
            print(f"  错误: {e}")
    
    def _show_tokens(self, code: str):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            for tok in tokens:
                print(f"  {tok}")
        except Exception as e:
            print(f"  错误: {e}")
    
    def _show_env(self):
        env = self.interpreter.global_env
        for name, val in sorted(env.bindings.items()):
            if not name.startswith('_'):
                val_repr = repr(val)
                if len(val_repr) > 60:
                    val_repr = val_repr[:60] + "..."
                print(f"  {name}: {val_repr}")
    
    def _print_ast(self, node, indent):
        prefix = "  " * indent
        if hasattr(node, '__dataclass_fields__'):
            name = node.__class__.__name__
            print(f"{prefix}{name}")
            for field_name in node.__dataclass_fields__:
                val = getattr(node, field_name)
                if val is None or val == [] or val == "":
                    continue
                if hasattr(val, '__dataclass_fields__'):
                    print(f"{prefix}  {field_name}:")
                    self._print_ast(val, indent + 2)
                elif isinstance(val, list) and val and hasattr(val[0], '__dataclass_fields__'):
                    print(f"{prefix}  {field_name}:")
                    for item in val:
                        self._print_ast(item, indent + 2)
                else:
                    print(f"{prefix}  {field_name}: {val!r}")
        else:
            print(f"{prefix}{node!r}")
