# -*- coding: utf-8 -*-
"""Aurora IDE 执行子进程。

由 server.py 以子进程方式调用,实现运行隔离 + 超时控制 + 标准输入注入。

用法:
    python3 worker.py <run|check> <src_path> <result_path> <project_root>

结果写入 result_path(JSON):
    run:   {"kind": "ok"|"error", "output": "...", "errors": [{"kind","message"}]}
    check: {"errors": [{"kind","message"}]}
"""

import io
import json
import sys


def load_code(src_path):
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


def report(result_path, payload):
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


def parse_errors():
    """词法/语法/类型/所有权检查,返回结构化错误列表。"""
    from aurora.lexer import Lexer, LexerError
    from aurora.parser import Parser, ParseError
    from aurora.type_checker import TypeChecker
    from aurora.ownership import OwnershipChecker

    errors = []
    try:
        tokens = Lexer(code).tokenize()
        program = Parser(tokens).parse()
        for err in TypeChecker().check(program):
            errors.append({"kind": "TypeError", "message": err})
        for err in OwnershipChecker().check(program):
            errors.append({"kind": "OwnershipError", "message": err})
    except LexerError as e:
        errors.append({"kind": "LexerError", "message": str(e)})
    except ParseError as e:
        errors.append({"kind": "ParseError", "message": str(e)})
    return errors


def run_program():
    """词法→语法→解释执行,捕获输出与运行时错误。"""
    from aurora.lexer import Lexer, LexerError
    from aurora.parser import Parser, ParseError
    from aurora.interpreter import Interpreter, AuroraError

    out = io.StringIO()
    errors = []
    kind = "ok"
    try:
        tokens = Lexer(code).tokenize()
        program = Parser(tokens).parse()
        old_stdout = sys.stdout
        sys.stdout = out
        try:
            Interpreter().run(program)
        finally:
            sys.stdout = old_stdout
    except (LexerError, ParseError, AuroraError) as e:
        kind = "error"
        errors.append({"kind": type(e).__name__, "message": str(e)})
    except RecursionError:
        kind = "error"
        errors.append({"kind": "RecursionError", "message": "递归过深,栈溢出(检查递归出口)"})
    except Exception as e:  # 解释器自身防御
        kind = "error"
        errors.append({"kind": "RuntimeError", "message": f"{type(e).__name__}: {e}"})
    return {"kind": kind, "output": out.getvalue(), "errors": errors}


def main():
    mode, src_path, result_path, project_root = sys.argv[1:]
    sys.path.insert(0, project_root)
    global code
    code = load_code(src_path)

    if mode == "run":
        payload = run_program()
    else:
        payload = {"errors": parse_errors()}
    report(result_path, payload)


if __name__ == "__main__":
    main()
