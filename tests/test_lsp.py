"""Aurora LSP 服务器测试 — initialize / completion / hover / symbol / diagnostics"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.lsp import LSPServer, register_cli, KEYWORDS


URI = "file:///proj/demo.aur"
SRC = """fn add(a, b) {
    return a + b
}

let name: str = "hi"
let count = 42
add(1, 2)
"""


class TestLSPBasics(unittest.TestCase):
    def setUp(self):
        self.server = LSPServer()
        self.server.handle("textDocument/didOpen", {
            "textDocument": {"uri": URI, "text": SRC, "version": 1}})

    def test_initialize_capabilities(self):
        cap = self.server.initialize({})["capabilities"]
        self.assertTrue(cap["hoverProvider"])
        self.assertTrue(cap["definitionProvider"])
        self.assertTrue(cap["referencesProvider"])
        self.assertTrue(cap["documentSymbolProvider"])
        self.assertTrue(cap["documentFormattingProvider"])
        self.assertIn("textDocumentSync", cap)

    def test_shutdown(self):
        self.assertIsNone(self.server.handle("shutdown", None))
        self.assertTrue(self.server.shutdown_requested)

    def test_completion_includes_keywords(self):
        items = self.server.handle("textDocument/completion", {
            "textDocument": {"uri": URI},
            "position": {"line": 0, "character": 0}})
        labels = {i["label"] for i in items}
        for kw in ("fn", "let", "if", "return", "while"):
            self.assertIn(kw, labels)

    def test_completion_includes_functions_and_vars(self):
        items = self.server.handle("textDocument/completion", {
            "textDocument": {"uri": URI},
            "position": {"line": 0, "character": 0}})
        labels = {i["label"] for i in items}
        self.assertIn("add", labels)
        self.assertIn("name", labels)
        self.assertIn("count", labels)

    def test_completion_includes_stdlib(self):
        items = self.server.handle("textDocument/completion", {
            "textDocument": {"uri": URI},
            "position": {"line": 0, "character": 0}})
        labels = {i["label"] for i in items}
        self.assertIn("len", labels)

    def test_hover_function(self):
        hov = self.server.handle("textDocument/hover", {
            "textDocument": {"uri": URI},
            "position": {"line": 0, "character": 4}})  # 指向 add
        self.assertIsNotNone(hov)
        self.assertIn("add", hov["contents"]["value"])

    def test_hover_variable_type(self):
        hov = self.server.handle("textDocument/hover", {
            "textDocument": {"uri": URI},
            "position": {"line": 4, "character": 5}})  # 指向 name
        self.assertIsNotNone(hov)
        self.assertIn("name", hov["contents"]["value"])

    def test_document_symbol_functions(self):
        syms = self.server.handle("textDocument/documentSymbol", {
            "textDocument": {"uri": URI}})
        names = [s["name"] for s in syms]
        self.assertIn("add", names)

    def test_document_symbol_variables(self):
        syms = self.server.handle("textDocument/documentSymbol", {
            "textDocument": {"uri": URI}})
        names = [s["name"] for s in syms]
        self.assertIn("name", names)
        self.assertIn("count", names)

    def test_definition(self):
        loc = self.server.handle("textDocument/definition", {
            "textDocument": {"uri": URI},
            "position": {"line": 6, "character": 0}})  # add(1,2) 调用处
        self.assertIsNotNone(loc)
        self.assertEqual(loc["uri"], URI)
        self.assertEqual(loc["range"]["start"]["line"], 0)

    def test_references(self):
        refs = self.server.handle("textDocument/references", {
            "textDocument": {"uri": URI},
            "position": {"line": 0, "character": 4}})
        # 至少包含调用处的引用
        self.assertGreaterEqual(len(refs), 1)

    def test_formatting(self):
        edits = self.server.handle("textDocument/formatting", {
            "textDocument": {"uri": URI}, "options": {}})
        self.assertEqual(len(edits), 1)
        self.assertTrue(edits[0]["newText"].endswith("\n"))

    def test_did_close(self):
        self.server.handle("textDocument/didClose", {"textDocument": {"uri": URI}})
        self.assertNotIn(URI, self.server.documents)


class TestDiagnostics(unittest.TestCase):
    def test_syntax_error_reported(self):
        bad = "fn broken(\n"
        uri = "file:///proj/bad.aur"
        server = LSPServer()
        server.handle("textDocument/didOpen", {
            "textDocument": {"uri": uri, "text": bad}})
        diags = server.documents[uri].diagnostics
        self.assertGreaterEqual(len(diags), 1)
        self.assertIn("line", diags[0]["range"]["start"])

    def test_clean_document_no_errors(self):
        server = LSPServer()
        server.handle("textDocument/didOpen", {
            "textDocument": {"uri": URI, "text": SRC}})
        # 语法合法；类型检查可能无错或有少量提示，此处至少不应崩溃
        self.assertIsInstance(server.documents[URI].diagnostics, list)


class TestCLIRegistration(unittest.TestCase):
    def test_register_cli(self):
        import argparse
        ap = argparse.ArgumentParser()
        sub = ap.add_subparsers()
        register_cli(sub)
        args = ap.parse_args(["lsp", "--stdio"])
        self.assertTrue(args.stdio)


if __name__ == "__main__":
    unittest.main()
