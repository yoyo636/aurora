"""全栈能力测试:Web 后端 / AI Agent / HTML 前端组件 / IO 增强"""

import json
import os
import tempfile
import threading
import unittest
import urllib.request

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from helpers import eval_expr
from aurora.stdlib import (
    AuroraError, AuroraWeb, AuroraAI, AuroraHtml, AuroraIO,
)


class TestWebServer(unittest.TestCase):
    def setUp(self):
        def handler(path, method, query, body):
            if path == "/":
                return "<h1>hi</h1>"
            if path == "/api/hello":
                return {"msg": "ok", "q": query}
            if path == "/api/echo" and method == "POST":
                return {"got": json.loads(body)}
            return [404, "not found"]
        self.info = AuroraWeb.serve(0, handler)

    def _get(self, path):
        url = f"http://127.0.0.1:{self.info['port']}{path}"
        with urllib.request.urlopen(url) as r:
            return r.status, r.read().decode('utf-8')

    def test_html_route(self):
        status, body = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn("<h1>hi</h1>", body)

    def test_json_route_with_query(self):
        status, body = self._get("/api/hello?x=1")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"msg": "ok", "q": {"x": "1"}})

    def test_post_echo(self):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.info['port']}/api/echo",
            data=json.dumps({"k": [1, 2]}).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            self.assertEqual(json.loads(r.read()), {"got": {"k": [1, 2]}})

    def test_404(self):
        try:
            self._get("/nope")
            self.fail("应 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)


class MockLLM:
    """可编程的 OpenAI 兼容 mock:
    请求带 tools 且尚未给过工具调用 → 返回 double 工具调用;
    否则 → 返回最终答案。"""

    def __init__(self):
        self.answered_tool = False
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), self._handler())
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.port = self.server.server_address[1]

    def _handler(self):
        def make(server):
            class H(BaseHTTPRequestHandler):
                def do_POST(self):
                    length = int(self.headers.get('Content-Length') or 0)
                    req = json.loads(self.rfile.read(length))
                    body_str = json.dumps(req)
                    if 'tools' in body_str and not server.answered_tool:
                        server.answered_tool = True
                        msg = {'role': 'assistant', 'content': None,
                               'tool_calls': [{
                                   'id': 'call_1', 'type': 'function',
                                   'function': {'name': 'double',
                                                'arguments': '{"x": 21}'}}]}
                    else:
                        msg = {'role': 'assistant',
                               'content': '21 的两倍是 42'}
                    body = json.dumps({'choices': [{'message': msg}]}).encode()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Length', str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)

                def log_message(self, *a):
                    pass
            return H
        return make(self)

    def url(self):
        return f"http://127.0.0.1:{self.port}"


class TestAIAgent(unittest.TestCase):
    def setUp(self):
        self.mock = MockLLM()
        AuroraAI.configure(base_url=self.mock.url(), api_key="test", model="mock")

    def tearDown(self):
        self.mock.server.shutdown()

    def test_agent_tool_loop(self):
        src = (
            'import std.ai\n'
            'fn double(x) { x * 2 }\n'
            'let r = std.ai.agent("助手", '
            '{"double": {"fn": double, "desc": "翻倍", '
            '"params": {"type": "object", "properties": {"x": {"type": "integer"}}}}},'
            '"21 的两倍?")\n'
            'r'
        )
        result = eval_expr(src)
        self.assertEqual(result["answer"], "21 的两倍是 42")
        self.assertEqual(result["steps"], 2)
        self.assertEqual(result["tool_calls"][0]["name"], "double")
        self.assertEqual(result["tool_calls"][0]["args"], {"x": 21})
        self.assertEqual(result["tool_calls"][0]["result"], 42)

    def test_chat(self):
        self.assertEqual(AuroraAI.chat("hi"), "21 的两倍是 42")

    def test_agent_plain_no_tools(self):
        AuroraAI.configure(base_url=self.mock.url(), api_key="test")
        r = AuroraAI.agent("", {}, "q")
        self.assertEqual(r["answer"], "21 的两倍是 42")
        self.assertEqual(r["steps"], 1)

    def test_no_key_raises(self):
        AuroraAI._api_key = ""
        with self.assertRaises(AuroraError) as ctx:
            AuroraAI.chat("hi")
        self.assertEqual(ctx.exception.kind, "AIError")
        self.assertIn("API Key", str(ctx.exception))


class TestHtmlComponents(unittest.TestCase):
    def test_link(self):
        self.assertEqual(AuroraHtml.link("https://a.b", "A&B"),
                         '<a href="https://a.b">A&amp;B</a>')

    def test_list(self):
        self.assertEqual(AuroraHtml.list([1, 2]),
                         "<ul><li>1</li><li>2</li></ul>")
        self.assertIn("<ol>", AuroraHtml.list(["a"], ordered=True))

    def test_json_script(self):
        out = AuroraHtml.json_script({"a": 1}, "d")
        self.assertIn('id="d"', out)
        self.assertIn('{"a": 1}', out)


class TestIOEnhance(unittest.TestCase):
    def test_mkdir_list_is_dir_files(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(AuroraIO.mkdir(os.path.join(d, "sub")))
            self.assertFalse(AuroraIO.mkdir(os.path.join(d, "sub")))
            with open(os.path.join(d, "sub", "a.aur"), 'w') as f:
                f.write("x")
            self.assertTrue(AuroraIO.is_dir(os.path.join(d, "sub")))
            self.assertEqual(AuroraIO.list_dir(d), ["sub"])
            self.assertEqual(AuroraIO.files(os.path.join(d, "sub"), ".aur"),
                             ["a.aur"])


if __name__ == '__main__':
    unittest.main()
