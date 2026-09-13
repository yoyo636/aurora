"""Aurora REPL — 交互式解释器"""

import sys
from .lexer import Lexer
from .parser import Parser, ParseError
from .interpreter import Interpreter
from .type_checker import TypeChecker
from .ownership import OwnershipChecker
from . import __version__


# Moonshot 暗黑极简风格 banner
BANNER = f"""
\033[90m        ╭──────────────────────────────────────╮\033[0m
\033[90m        │\033[0m                                      \033[90m│\033[0m
\033[90m        │\033[0m   \033[97m◡\033[0m  \033[1;97mAurora\033[0m \033[90mv{__version__}\033[0m                  \033[90m│\033[0m
\033[90m        │\033[0m   \033[37m寻求将代码转化为智能的最优解\033[0m        \033[90m│\033[0m
\033[90m        │\033[0m                                      \033[90m│\033[0m
\033[90m        ╰──────────────────────────────────────╯\033[0m

\033[90m  输入 \033[0m:help\033[90m 查看帮助 · \033[0m:quit\033[90m 退出\033[0m
"""

HELP_TEXT = """
\033[1;97m命令\033[0m
  \033[97m:help\033[0m          显示帮助
  \033[97m:quit / :exit\033[0m  退出
  \033[97m:type <expr>\033[0m   显示表达式类型
  \033[97m:ast <code>\033[0m    显示 AST 结构
  \033[97m:tokens <code>\033[0m 显示词法分析结果
  \033[97m:clear\033[0m         清屏
  \033[97m:env\033[0m           显示当前环境变量

\033[1;97m示例\033[0m
  \033[90m# 变量与函数\033[0m
  let x = 42
  fn greet(name) { println("Hello, {name}!") }
  greet("Aurora")

  \033[90m# 高效一行操作\033[0m
  write("/tmp/test.txt", "hello")
  read("/tmp/test.txt")
  json(r'{"a": 1}')
  unique([1,2,2,3])
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
                line = input("\033[90maurora\033[0m\033[37m>\033[0m ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\033[90m再见。\033[0m")
                break

            if not line:
                continue

            # 多行输入（遇到未闭合的 { 继续读取）
            while line.count('{') > line.count('}'):
                try:
                    cont = input("\033[90m    ...\033[0m ").strip()
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
                print(f"  \033[90m=>\033[0m \033[97m{result!r}\033[0m")
        except ParseError as e:
            print(f"  \033[91m解析错误\033[0m: {e}")
        except Exception as e:
            print(f"  \033[91m运行时错误\033[0m: {e}")

    def _handle_command(self, cmd: str):
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command in (':quit', ':exit', ':q'):
            print("\033[90m再见。\033[0m")
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
            print(f"  \033[90m未知命令: {command}，输入 :help 查看帮助\033[0m")

    def _show_type(self, code: str):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            errors = self.type_checker.check(program)
            if errors:
                for e in errors:
                    print(f"  \033[91m类型错误\033[0m: {e}")
                return
            # 显示最后一条语句的类型
            from .ast_nodes import ExprStmt
            last = None
            for stmt in program.statements:
                last = stmt
            if isinstance(last, ExprStmt):
                inferred = self.type_checker._infer_expr(
                    last.expr, self.type_checker.global_env)
                print(f"  \033[97m{inferred!r}\033[0m")
            elif last is not None:
                print(f"  \033[97m{last.__class__.__name__}\033[0m")
        except Exception as e:
            print(f"  \033[91m错误\033[0m: {e}")

    def _show_ast(self, code: str):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            self._print_ast(program, 0)
        except Exception as e:
            print(f"  \033[91m错误\033[0m: {e}")

    def _show_tokens(self, code: str):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            for tok in tokens:
                print(f"  \033[90m{tok}\033[0m")
        except Exception as e:
            print(f"  \033[91m错误\033[0m: {e}")

    def _show_env(self):
        env = self.interpreter.global_env
        for name, val in sorted(env.bindings.items()):
            if not name.startswith('_'):
                val_repr = repr(val)
                if len(val_repr) > 60:
                    val_repr = val_repr[:60] + "..."
                print(f"  \033[97m{name}\033[0m\033[90m:\033[0m {val_repr}")

    def _print_ast(self, node, indent):
        prefix = "  " * indent
        if hasattr(node, '__dataclass_fields__'):
            name = node.__class__.__name__
            print(f"{prefix}\033[97m{name}\033[0m")
            for field_name in node.__dataclass_fields__:
                val = getattr(node, field_name)
                if val is None or val == [] or val == "":
                    continue
                if hasattr(val, '__dataclass_fields__'):
                    print(f"{prefix}  \033[90m{field_name}:\033[0m")
                    self._print_ast(val, indent + 2)
                elif isinstance(val, list) and val and hasattr(val[0], '__dataclass_fields__'):
                    print(f"{prefix}  \033[90m{field_name}:\033[0m")
                    for item in val:
                        self._print_ast(item, indent + 2)
                else:
                    print(f"{prefix}  \033[90m{field_name}:\033[0m {val!r}")
        else:
            print(f"{prefix}{node!r}")
