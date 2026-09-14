"""Aurora 语言服务器（LSP）— 基于 stdin/stdout 的 JSON-RPC 通信

提供 Aurora 编辑器集成所需的核心语言能力：
    initialize / initialized / shutdown / exit
    textDocument/didOpen | didChange | didClose
    textDocument/completion | hover | definition | references
    textDocument/documentSymbol | formatting
    textDocument/publishDiagnostics（内部推送）

CLI：
    aurora lsp            启动 LSP 服务器（stdin/stdout）
    aurora lsp --stdio    显式指定 stdio 传输（默认）
"""

import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

from .ast_nodes import (
    Program, FnDef, LetStmt, ConstStmt, Identifier, Param, NamedType,
)
from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .type_checker import TypeChecker
from .type_infer import infer_program_types
from .stdlib import BUILTIN_GLOBALS, STDLIB_MODULES


# LSP SymbolKind / CompletionItemKind 常量
KIND_FUNCTION = 12
KIND_VARIABLE = 13
KIND_KEYWORD = 14
KIND_FUNCTION_C = 3


KEYWORDS = [
    "let", "mut", "const", "fn", "if", "elif", "else", "while", "for", "in",
    "return", "break", "continue", "match", "try", "catch", "panic",
    "import", "struct", "enum",
]

# 点后方法补全
STRING_METHODS = [
    "len", "upper", "lower", "split", "trim", "contains", "replace",
    "starts_with", "ends_with", "clone",
]
ARRAY_METHODS = [
    "append", "push", "pop", "len", "map", "filter", "reduce", "join",
    "clone", "contains",
]
MAP_METHODS = ["get", "keys", "values", "items", "clone"]


def _collect_stdlib_names() -> List[str]:
    names = list(BUILTIN_GLOBALS.keys())
    for mod in STDLIB_MODULES.values():
        if isinstance(mod, dict):
            names.extend(k for k in mod.keys() if not k.startswith('_'))
    return sorted(set(names))


def _fmt_type(node) -> str:
    if node is None:
        return ""
    if isinstance(node, NamedType):
        return node.name
    return getattr(node, '__name__', str(node))


class LSPDocument:
    __slots__ = ('uri', 'source', 'version', 'ast', 'diagnostics',
                 'functions', 'variables', 'var_types')

    def __init__(self, uri: str, source: str, version: int = 1):
        self.uri = uri
        self.source = source
        self.version = version
        self.ast: Optional[Program] = None
        self.diagnostics: List[dict] = []
        self.functions: Dict[str, FnDef] = {}
        self.variables: Dict[str, dict] = {}
        self.var_types: Dict[str, str] = {}


class LSPServer:
    """Aurora 语言服务器"""

    def __init__(self):
        self.documents: Dict[str, LSPDocument] = {}
        self.stdlib_names = _collect_stdlib_names()
        self.shutdown_requested = False
        self._req_id = 0

    # ── 文档解析 ─────────────────────────────────

    def _parse(self, source: str):
        """返回 (ast_or_None, diagnostics)"""
        diags: List[dict] = []
        ast = None
        try:
            tokens = Lexer(source).tokenize()
            ast = Parser(tokens).parse()
        except (LexerError, ParseError) as e:
            line = getattr(e, 'line', 1) or 1
            col = getattr(e, 'column', 1) or 1
            tok = getattr(e, 'token', None)
            if tok is not None:
                line, col = tok.line, tok.column
            diags.append(self._make_diag(line - 1, col - 1, str(e)))
            return None, diags
        # 类型检查诊断
        try:
            errs = TypeChecker().check(ast)
            for err in errs:
                node = getattr(err, 'node', None)
                l = (getattr(node, 'line', 1) or 1) - 1
                c = (getattr(node, 'column', 1) or 1) - 1
                diags.append(self._make_diag(l, c, str(err)))
        except Exception:
            pass
        return ast, diags

    @staticmethod
    def _make_diag(line0: int, char0: int, message: str) -> dict:
        return {
            "range": {
                "start": {"line": max(line0, 0), "character": max(char0, 0)},
                "end": {"line": max(line0, 0), "character": max(char0, 0) + 1},
            },
            "severity": 1,
            "source": "aurora",
            "message": message,
        }

    def _reanalyze(self, doc: LSPDocument):
        ast, diags = self._parse(doc.source)
        doc.ast = ast
        doc.diagnostics = diags
        doc.functions = {}
        doc.variables = {}
        doc.var_types = {}
        if ast is not None:
            for stmt in ast.statements:
                if isinstance(stmt, FnDef):
                    doc.functions[stmt.name] = stmt
                    sig = self._signature(stmt)
                    doc.var_types[stmt.name] = sig
                elif isinstance(stmt, (LetStmt, ConstStmt)):
                    doc.variables[stmt.name] = stmt
                    ann = _fmt_type(stmt.type_annotation)
                    doc.var_types[stmt.name] = ann or "unknown"

    # ── LSP 主分发 ──────────────────────────────

    def handle(self, method: str, params: Optional[dict]) -> Any:
        if method == "initialize":
            return self.initialize(params or {})
        if method == "initialized":
            return None
        if method == "shutdown":
            self.shutdown_requested = True
            return None
        if method == "exit":
            return None
        if method == "textDocument/didOpen":
            return self._did_open(params)
        if method == "textDocument/didChange":
            return self._did_change(params)
        if method == "textDocument/didClose":
            return self._did_close(params)
        if method == "textDocument/completion":
            return self.completion(params)
        if method == "textDocument/hover":
            return self.hover(params)
        if method == "textDocument/definition":
            return self.definition(params)
        if method == "textDocument/references":
            return self.references(params)
        if method == "textDocument/documentSymbol":
            return self.document_symbol(params)
        if method == "textDocument/formatting":
            return self.formatting(params)
        return None

    # ── 生命周期 ──────────────────────────────

    def initialize(self, params: dict) -> dict:
        return {
            "capabilities": {
                "textDocumentSync": 1,
                "completionProvider": {"triggerCharacters": [".", " "]},
                "hoverProvider": True,
                "definitionProvider": True,
                "referencesProvider": True,
                "documentSymbolProvider": True,
                "documentFormattingProvider": True,
            }
        }

    # ── 文档同步 ────────────────────────────────

    def _doc_of(self, params: dict) -> Optional[LSPDocument]:
        td = params.get("textDocument", {}) or {}
        uri = td.get("uri")
        return self.documents.get(uri)

    def _did_open(self, params: dict):
        td = params["textDocument"]
        doc = LSPDocument(td["uri"], td["text"], td.get("version", 1))
        self._reanalyze(doc)
        self.documents[doc.uri] = doc
        return None

    def _did_change(self, params: dict):
        doc = self._doc_of(params)
        if doc is None:
            return None
        changes = params.get("contentChanges", [])
        if changes:
            doc.source = changes[-1].get("text", doc.source)
            doc.version += 1
        self._reanalyze(doc)
        return None

    def _did_close(self, params: dict):
        doc = self._doc_of(params)
        if doc is not None:
            self.documents.pop(doc.uri, None)
        return None

    def publish_diagnostics(self, uri: str) -> Optional[dict]:
        doc = self.documents.get(uri)
        if doc is None:
            return None
        return {
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {"uri": uri, "diagnostics": doc.diagnostics},
        }

    # ── 辅助：位置 → 词 ─────────────────────────

    @staticmethod
    def _word_at(source_lines: List[str], line0: int, char0: int) -> Optional[str]:
        if line0 < 0 or line0 >= len(source_lines):
            return None
        line_text = source_lines[line0]
        if char0 > len(line_text):
            char0 = len(line_text)
        start = char0
        while start > 0 and (line_text[start - 1].isalnum() or line_text[start - 1] == '_'):
            start -= 1
        end = char0
        while end < len(line_text) and (line_text[end].isalnum() or line_text[end] == '_'):
            end += 1
        return line_text[start:end] or None

    def _dot_prefix(self, source_lines: List[str], line0: int, char0: int):
        """返回 (对象名, 已输入成员前缀)；非点后补全返回 None"""
        if line0 < 0 or line0 >= len(source_lines):
            return None
        text = source_lines[line0][:char0]
        m = re.search(r'([A-Za-z_]\w*)\.(\w*)$', text)
        if m:
            return m.group(1), m.group(2)
        return None

    # ── 补全 ────────────────────────────────────

    def completion(self, params: dict):
        doc = self._doc_of(params)
        if doc is None:
            return []
        pos = params["position"]
        lines = doc.source.splitlines()
        items: List[dict] = []

        dot = self._dot_prefix(lines, pos["line"], pos["character"])
        if dot is not None:
            obj_name, member_prefix = dot
            methods = self._methods_for_object(doc, obj_name)
            for name in methods:
                if name.startswith(member_prefix):
                    items.append(self._item(name, KIND_METHOD, "method"))
            return items

        # 关键字
        for kw in KEYWORDS:
            items.append(self._item(kw, KIND_KEYWORD, "keyword"))
        # 文档内函数
        for name, fn in doc.functions.items():
            items.append(self._item(name, KIND_FUNCTION, self._signature(fn)))
        # 文档内变量
        for name in doc.variables:
            items.append(self._item(name, KIND_VARIABLE,
                                    doc.var_types.get(name, "unknown")))
        # 标准库函数
        for name in self.stdlib_names:
            items.append(self._item(name, KIND_FUNCTION_C, "stdlib"))
        return items

    @staticmethod
    def _item(label: str, kind: int, detail: str = "") -> dict:
        return {"label": label, "kind": kind, "detail": detail}

    @staticmethod
    def _signature(fn: FnDef) -> str:
        params = ", ".join(p.name for p in fn.params)
        ret = f" -> {_fmt_type(fn.return_type)}" if fn.return_type else ""
        return f"fn {fn.name}({params}){ret}"

    def _methods_for_object(self, doc: LSPDocument, obj_name: str) -> List[str]:
        # 优先按变量类型注解推断
        ann = doc.var_types.get(obj_name, "")
        if ann in ("string", "str"):
            return STRING_METHODS
        if ann in ("array", "[int]", "[str]", "list"):
            return ARRAY_METHODS
        if ann in ("map", "dict"):
            return MAP_METHODS
        # 无法确定类型时给出全部
        return STRING_METHODS + ARRAY_METHODS + MAP_METHODS

    # ── hover ───────────────────────────────────

    def hover(self, params: dict):
        doc = self._doc_of(params)
        if doc is None:
            return None
        pos = params["position"]
        lines = doc.source.splitlines()
        word = self._word_at(lines, pos["line"], pos["character"])
        if not word:
            return None
        content = None
        if word in doc.functions:
            content = "```aurora\n" + self._signature(doc.functions[word]) + "\n```"
        elif word in doc.var_types:
            content = f"**{word}**: {doc.var_types[word]}"
        elif word in self.stdlib_names:
            content = f"`{word}` — 标准库函数"
        if content is None:
            return None
        return {"contents": {"kind": "markdown", "value": content}}

    # ── definition ──────────────────────────────

    def definition(self, params: dict):
        doc = self._doc_of(params)
        if doc is None or doc.ast is None:
            return None
        pos = params["position"]
        lines = doc.source.splitlines()
        word = self._word_at(lines, pos["line"], pos["character"])
        if not word:
            return None
        target = doc.functions.get(word) or doc.variables.get(word)
        if target is None:
            return None
        line = getattr(target, 'line', 1) or 1
        col = getattr(target, 'column', 1) or 1
        return self._loc(doc.uri, line - 1, col - 1)

    # ── references ──────────────────────────────

    def references(self, params: dict):
        doc = self._doc_of(params)
        if doc is None or doc.ast is None:
            return []
        pos = params["position"]
        lines = doc.source.splitlines()
        word = self._word_at(lines, pos["line"], pos["character"])
        if not word:
            return []
        out = []
        self._walk_idents(doc.ast, word, out, doc.uri)
        return out

    def _walk_idents(self, node, name: str, out: List[dict], uri: str):
        if isinstance(node, Identifier) and node.name == name:
            out.append(self._loc(uri, node.line - 1, node.column - 1))
        for v in vars(node).values():
            if isinstance(v, list):
                for it in v:
                    if hasattr(it, '__dict__'):
                        self._walk_idents(it, name, out, uri)
            elif hasattr(v, '__dict__') and not isinstance(v, type):
                self._walk_idents(v, name, out, uri)

    @staticmethod
    def _loc(uri: str, line0: int, char0: int) -> dict:
        return {
            "uri": uri,
            "range": {
                "start": {"line": line0, "character": char0},
                "end": {"line": line0, "character": char0 + 1},
            },
        }

    # ── documentSymbol ──────────────────────────

    def document_symbol(self, params: dict):
        doc = self._doc_of(params)
        if doc is None or doc.ast is None:
            return []
        out = []
        for stmt in doc.ast.statements:
            line = getattr(stmt, 'line', 0) or 0
            if isinstance(stmt, FnDef):
                out.append({
                    "name": stmt.name,
                    "kind": KIND_FUNCTION,
                    "detail": self._signature(stmt),
                    "range": {"start": {"line": line - 1, "character": 0},
                              "end": {"line": line - 1, "character": 0}},
                    "selectionRange": {"start": {"line": line - 1, "character": 0},
                                       "end": {"line": line - 1, "character": 0}},
                })
            elif isinstance(stmt, (LetStmt, ConstStmt)):
                out.append({
                    "name": stmt.name,
                    "kind": KIND_VARIABLE,
                    "detail": doc.var_types.get(stmt.name, "unknown"),
                    "range": {"start": {"line": line - 1, "character": 0},
                              "end": {"line": line - 1, "character": 0}},
                    "selectionRange": {"start": {"line": line - 1, "character": 0},
                                       "end": {"line": line - 1, "character": 0}},
                })
        return out

    # ── formatting ──────────────────────────────

    def formatting(self, params: dict):
        doc = self._doc_of(params)
        if doc is None:
            return []
        new_text = format_code(doc.source)
        lines = doc.source.splitlines()
        last_line = max(len(lines) - 1, 0)
        return [{
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": last_line,
                        "character": len(lines[last_line]) if lines else 0},
            },
            "newText": new_text,
        }]

    # ── stdio 主循环 ────────────────────────────

    def run(self):
        """从 stdin 读取 JSON-RPC 帧，向 stdout 写入响应"""
        while True:
            try:
                header = self._read_headers()
            except (EOFError, OSError):
                return
            if not header:
                continue
            length = header.get('Content-Length')
            if not length:
                continue
            body = sys.stdin.read(int(length))
            try:
                msg = json.loads(body)
            except json.JSONDecodeError:
                continue
            method = msg.get('method')
            msgid = msg.get('id')
            if method and msgid is not None:
                result = self.handle(method, msg.get('params'))
                self._write({'jsonrpc': '2.0', 'id': msgid, 'result': result})
            elif method:
                # 通知
                if method == 'textDocument/didOpen':
                    self.handle(method, msg.get('params'))
                    diag = self.publish_diagnostics(msg['params']['textDocument']['uri'])
                    if diag:
                        self._write(diag)
                elif method == 'textDocument/didChange':
                    self.handle(method, msg.get('params'))
                    diag = self.publish_diagnostics(msg['params']['textDocument']['uri'])
                    if diag:
                        self._write(diag)
                else:
                    self.handle(method, msg.get('params'))
                if method == 'exit':
                    return

    @staticmethod
    def _read_headers() -> dict:
        headers = {}
        while True:
            line = sys.stdin.readline()
            if line == '' or line == '\n':
                break
            if ':' in line:
                k, v = line.split(':', 1)
                headers[k.strip()] = v.strip()
        return headers

    @staticmethod
    def _write(msg: dict):
        body = json.dumps(msg)
        sys.stdout.write(f"Content-Length: {len(body)}\r\n\r\n{body}")
        sys.stdout.flush()


# ── 简易格式化（formatter.py 不可用时的内置回退） ──

def format_code(source: str) -> str:
    """最小可用格式化：去除行尾空白、保证文件末尾一个换行"""
    out = [ln.rstrip() for ln in source.splitlines()]
    text = '\n'.join(out)
    if not text.endswith('\n'):
        text += '\n'
    return text


# ── CLI 注册 ──────────────────────────────────────────

def cmd_lsp(args):
    """aurora lsp 命令实现"""
    server = LSPServer()
    server.run()


def register_cli(subparsers):
    """把 lsp 子命令注册到全局 argparse"""
    p = subparsers.add_parser('lsp', help='启动 Aurora 语言服务器（stdio）')
    p.add_argument('--stdio', action='store_true', default=True,
                  help='使用 stdin/stdout 传输（默认）')
    p.set_defaults(func=cmd_lsp)
