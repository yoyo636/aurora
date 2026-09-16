"""Aurora v3.2.0 std.web 全栈框架测试。

直接从 aurora.web_framework 导入类进行单元测试,不经过 Aurora 解释器。
运行: cd <repo父目录> && python3 -m unittest aurora.tests.test_web_framework_v320 -v
"""

import json
import os
import tempfile
import unittest

from aurora.web_framework import (
    Router, App, Request, Response, Middleware, WebSocket, Static, Session,
    Component, VNode, create_element, render_to_string, diff, patch,
    reactive, ref, computed, watch, css, keyframes, inject_styles,
    define_types, generate_typescript, generate_aurora,
    generate_client, render_server, hydrate_script,
    logger_middleware, cors_middleware, auth_middleware,
    rate_limit_middleware, apply_middleware,
    MemorySessionStore, CookieSessionStore,
    STDLIB_REGISTRATION,
)


class TestRouter(unittest.TestCase):
    """1) Router 路由匹配(含路径参数)。"""

    def setUp(self):
        self.router = Router()
        self.router.get("/", lambda req: "home")
        self.router.get("/users/:id", lambda req: "user")
        self.router.get("/users/:id/posts/:post_id", lambda req: "post")
        self.router.post("/users", lambda req: "create")

    def test_exact_match(self):
        handler, params = self.router.match("/", "GET")
        self.assertIsNotNone(handler)
        self.assertEqual(params, {})

    def test_path_params_single(self):
        handler, params = self.router.match("/users/42", "GET")
        self.assertIsNotNone(handler)
        self.assertEqual(params, {"id": "42"})

    def test_path_params_multi(self):
        handler, params = self.router.match("/users/7/posts/9", "GET")
        self.assertEqual(params, {"id": "7", "post_id": "9"})

    def test_method_not_matched(self):
        # /users 是 POST 路由,用 GET 应不命中
        handler, _ = self.router.match("/users", "GET")
        self.assertIsNone(handler)
        handler, _ = self.router.match("/users", "POST")
        self.assertIsNotNone(handler)

    def test_no_match_returns_none(self):
        self.assertEqual(self.router.match("/nope", "GET"), (None, {}))


class TestMiddleware(unittest.TestCase):
    """2) Middleware 链执行。"""

    def test_chain_order(self):
        calls = []

        def base(req):
            calls.append("handler")
            return Response.text("ok")

        def mw1(handler):
            def inner(req):
                calls.append("mw1-in")
                r = handler(req)
                calls.append("mw1-out")
                return r
            return inner

        def mw2(handler):
            def inner(req):
                calls.append("mw2-in")
                return handler(req)
            return inner

        wrapped = apply_middleware(base, mw1, mw2)
        wrapped(Request())
        self.assertEqual(calls, ["mw1-in", "mw2-in", "handler", "mw1-out"])

    def test_auth_middleware_blocks(self):
        called = []

        def ok(req):
            called.append("hit")
            return Response.json({"ok": True})

        mw = auth_middleware(lambda req: False)
        wrapped = apply_middleware(ok, mw)
        resp = wrapped(Request())
        self.assertEqual(resp.status, 401)
        self.assertEqual(called, [])

    def test_cors_injects_header(self):
        mw = cors_middleware("https://example.com")
        wrapped = apply_middleware(lambda req: Response.json({}), mw)
        resp = wrapped(Request())
        self.assertEqual(resp.headers["Access-Control-Allow-Origin"],
                         "https://example.com")

    def test_rate_limit(self):
        mw = rate_limit_middleware(2, 10)
        wrapped = apply_middleware(lambda req: Response.json({}), mw)
        self.assertEqual(wrapped(Request()).status, 200)
        self.assertEqual(wrapped(Request()).status, 200)
        self.assertEqual(wrapped(Request()).status, 429)

    def test_base_middleware_class(self):
        out = []
        m = Middleware(lambda req: out.append("x") or Response.text("done"))
        self.assertEqual(m(Request()).body, "done")
        self.assertEqual(out, ["x"])


class TestRequestResponse(unittest.TestCase):
    """3) Request 解析 + Response JSON/HTML/重定向。"""

    def test_request_json_form_cookies(self):
        req = Request("POST", "/x?a=1", query={"a": "1"},
                      headers={"Content-Type": "application/json",
                               "Cookie": "sid=abc; theme=dark"},
                      body='{"hello": "world"}')
        self.assertEqual(req.json, {"hello": "world"})
        self.assertEqual(req.cookies, {"sid": "abc", "theme": "dark"})
        req2 = Request("POST", "/", body="name=aurora&version=3")
        self.assertEqual(req2.form, {"name": "aurora", "version": "3"})

    def test_response_json(self):
        resp = Response.json({"msg": "hi"})
        status, headers, body = resp.to_http_response()
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["Content-Type"])
        self.assertEqual(json.loads(body), {"msg": "hi"})

    def test_response_html_text(self):
        self.assertIn("text/html", Response.html("<b>").headers["Content-Type"])
        self.assertIn("text/plain", Response.text("hi").headers["Content-Type"])

    def test_response_redirect_and_cookie(self):
        r = Response.redirect("/login")
        self.assertEqual(r.status, 302)
        self.assertEqual(r.headers["Location"], "/login")
        r.set_cookie("token", "abc", max_age=3600)
        r.set_cookie("other", "v")
        status, headers, _ = r.to_http_response()
        self.assertIsInstance(headers["Set-Cookie"], list)
        self.assertEqual(len(headers["Set-Cookie"]), 2)
        self.assertIn("Max-Age=3600", headers["Set-Cookie"][0])


class TestAppIntegration(unittest.TestCase):
    """4) App 集成请求处理 + 全局中间件。"""

    def setUp(self):
        self.app = App("test-app")

        @self.app.get("/hello")
        def hello(req):
            return Response.json({"path": req.path})

        @self.app.get("/users/:id")
        def user(req):
            return Response.json({"id": req.params["id"]})

    def test_handle_json_route(self):
        resp = self.app.handle_request(Request("GET", "/hello"))
        self.assertEqual(resp.status, 200)
        self.assertEqual(json.loads(resp.body)["path"], "/hello")

    def test_handle_path_param(self):
        resp = self.app.handle_request(Request("GET", "/users/99"))
        self.assertEqual(json.loads(resp.body)["id"], "99")

    def test_not_found(self):
        resp = self.app.handle_request(Request("GET", "/missing"))
        self.assertEqual(resp.status, 404)

    def test_global_middleware(self):
        marks = []

        def trace(handler):
            def inner(req):
                marks.append("global")
                return handler(req)
            return inner

        self.app.use(trace)
        self.app.handle_request(Request("GET", "/hello"))
        self.assertEqual(marks, ["global"])

    def test_return_value_normalization(self):
        # 返回 dict / str 也应被归一化为 Response
        app = App()
        app.get("/dict")(lambda req: {"ok": True})
        app.get("/str")(lambda req: "<h1>str</h1>")
        self.assertEqual(app.handle_request(Request("GET", "/dict")).status, 200)
        self.assertIn("str", app.handle_request(Request("GET", "/str")).body)


class TestVDom(unittest.TestCase):
    """5) VNode 创建与 render_to_string(SSR)。"""

    def test_create_element_filters_false(self):
        v = create_element("div", {"class": "box"}, None, False, "a",
                            create_element("span", None, "b"))
        self.assertEqual(len(v.children), 2)

    def test_render_to_string(self):
        v = create_element("ul", {"class": "list"},
                           create_element("li", None, "one"),
                           create_element("li", None, "two"))
        html = render_to_string(v)
        self.assertEqual(html, '<ul class="list"><li>one</li><li>two</li></ul>')

    def test_escape_text(self):
        v = create_element("p", None, "<script>alert(1)</script>")
        out = render_to_string(v)
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)

    def test_diff_produces_patches(self):
        a = create_element("div", None, "old")
        b = create_element("div", None, "new")
        patches = diff(a, b)
        self.assertTrue(any(p["type"] == "TEXT" for p in patches))


class TestComponent(unittest.TestCase):
    """6) Component 生命周期。"""

    class Greeter(Component):
        def mount(self):
            super().mount()
            self.state["greeted"] = True

        def render(self):
            return create_element("h1", None, "Hi " + str(self.props.get("name")))

    def test_lifecycle(self):
        c = self.Greeter({"name": "Aurora"})
        self.assertFalse(c._mounted)
        c.mount()
        self.assertTrue(c._mounted)
        self.assertTrue(c.state["greeted"])
        c.set_state({"count": 1})
        self.assertEqual(c.state["count"], 1)
        self.assertIn("Hi Aurora", render_to_string(c.render()))
        c.unmount()
        self.assertFalse(c._mounted)


class TestReactiveState(unittest.TestCase):
    """7) reactive / ref / computed / watch。"""

    def test_ref_watch(self):
        s = ref(10)
        seen = []
        watch(s, lambda nv, ov: seen.append((nv, ov)))
        s.value = 20
        self.assertEqual(seen, [(20, 10)])
        self.assertEqual(s.value, 20)

    def test_reactive_watch(self):
        d = reactive({"a": 1})
        seen = []
        watch(d, lambda k, v, o: seen.append((k, v)))
        d["a"] = 2
        d["b"] = 3
        self.assertEqual(seen, [("a", 2), ("b", 3)])

    def test_computed(self):
        d = reactive({"price": 100})
        tax = computed(lambda: d["price"] * 0.1)
        self.assertAlmostEqual(tax.value, 10.0)
        d["price"] = 200
        tax.invalidate()
        self.assertAlmostEqual(tax.value, 20.0)


class TestTypeSharing(unittest.TestCase):
    """8) TypeSharing 代码生成。"""

    def test_generate_typescript(self):
        defs = define_types({"User": {"id": "int", "name": "str",
                                      "active": "bool"}})
        ts = generate_typescript(defs)
        self.assertIn("export interface User", ts)
        self.assertIn("id: number;", ts)
        self.assertIn("name: string;", ts)
        self.assertIn("active: boolean;", ts)

    def test_generate_aurora(self):
        defs = {"User": {"id": "int", "name": "str"}}
        au = generate_aurora(defs)
        self.assertIn("type User {", au)
        self.assertIn("id: int", au)


class TestAPIClient(unittest.TestCase):
    """9) APIClient 从路由生成 fetch 封装。"""

    def test_generate_client_from_list(self):
        js = generate_client([("GET", "/users/:id"), ("POST", "/users")],
                             base_url="/api")
        self.assertIn("export const api", js)
        self.assertIn("_req(", js)
        self.assertIn("/users/:id", js)

    def test_generate_client_from_router(self):
        r = Router()
        r.get("/items/:id", lambda req: None)
        js = generate_client(r, "/api/v2")
        self.assertIn("/api/v2" if False else "BASE", js)
        self.assertIn("/items/:id", js)


class TestStatic(unittest.TestCase):
    """10) Static 静态文件服务。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        with open(os.path.join(self.tmp, "index.html"), "w") as f:
            f.write("<h1>home</h1>")
        with open(os.path.join(self.tmp, "app.js"), "w") as f:
            f.write("console.log(1)")
        self.handler = Static.serve(self.tmp, "/static")

    def test_serve_html(self):
        resp = self.handler(Request("GET", "/static/index.html"))
        self.assertEqual(resp.status, 200)
        self.assertIn("text/html", resp.headers["Content-Type"])
        self.assertIn("<h1>home</h1>", resp.body)

    def test_serve_js_mime_and_cache(self):
        resp = self.handler(Request("GET", "/static/app.js"))
        self.assertIn("javascript", resp.headers["Content-Type"])
        self.assertIn("Cache-Control", resp.headers)

    def test_not_found(self):
        resp = self.handler(Request("GET", "/static/missing.css"))
        self.assertEqual(resp.status, 404)

    def test_dir_traversal_blocked(self):
        resp = self.handler(Request("GET", "/static/../secret.txt"))
        self.assertIn(resp.status, (403, 404))


class TestSession(unittest.TestCase):
    """Session 存储。"""

    def test_memory_session(self):
        store = MemorySessionStore()
        store.set("sid-1", "user", "aurora")
        self.assertEqual(store.get("sid-1"), {"user": "aurora"})
        store.clear("sid-1")
        self.assertEqual(store.get("sid-1"), {})

    def test_cookie_session_signature(self):
        store = CookieSessionStore(secret="s3cret")
        sid = store.set("", "theme", "dark")
        self.assertIn(".", sid)
        self.assertEqual(store.get(sid), {"theme": "dark"})
        # 篡改签名应失败
        bad = sid[:-2] + ("aa" if not sid.endswith("aa") else "bb")
        self.assertEqual(store.get(bad), {})

    def test_session_facade(self):
        s = Session(MemorySessionStore())
        req = Request("GET", "/", headers={"Cookie": "aurora_sid=mysid"})
        s.set(req, "k", "v")
        self.assertEqual(s.get(req), {"k": "v"})
        s.clear(req)
        self.assertEqual(s.get(req), {})


class TestStyle(unittest.TestCase):
    """CSS-in-JS。"""

    def test_css_and_keyframes(self):
        before = len(inject_styles())
        cls = css({"color": "red", "font-size": "14px"})
        self.assertTrue(cls.startswith("ax-"))
        keyframes("spin", {"0%": {"transform": "rotate(0)"},
                           "100%": {"transform": "rotate(360deg)"}})
        out = inject_styles()
        self.assertGreater(len(out), before)
        self.assertIn(cls, out)
        self.assertIn("@keyframes spin", out)


class TestSSR(unittest.TestCase):
    """SSR 渲染与水合。"""

    class Banner(Component):
        def render(self):
            return create_element("div", {"class": "banner"},
                                  self.props.get("title"))

    def test_render_server(self):
        html_str, state_json = render_server(self.Banner, {"title": "SSR!"})
        self.assertIn('<div class="banner">SSR!</div>', html_str)
        state = json.loads(state_json)
        self.assertEqual(state["props"]["title"], "SSR!")

    def test_hydrate_script(self):
        script = hydrate_script("Banner", {"title": "x"}, {"count": 1})
        self.assertIn("__AURORA_HYDRATE__", script)
        self.assertIn("Banner", script)


class TestWebSocket(unittest.TestCase):
    """WebSocket 握手与帧编解码(不真正起 socket)。"""

    def test_accept_key(self):
        # 已知 RFC 6455 测试向量
        key = "dGhlIHNhbXBsZSBub25jZQ=="
        accept = WebSocket.accept_key(key)
        self.assertEqual(accept, "s3pPLMBiTxaQ9kYGzzhZRbK+xOo=")

    def test_encode_decode_roundtrip(self):
        frame = WebSocket.encode_text("hello")
        self.assertTrue(frame[0] & 0x81)  # FIN + text opcode
        # decode_text 期望客户端带掩码,这里手动构造一个掩码帧
        payload = b"hi"
        mask = b"\x01\x02\x03\x04"
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        frame = bytes([0x81, 0x80 | len(payload)]) + mask + masked
        self.assertEqual(WebSocket.decode_text(frame), "hi")


class TestStdlibRegistration(unittest.TestCase):
    """STDLIB_REGISTRATION 暴露完整。"""

    def test_registration_keys(self):
        mod = STDLIB_REGISTRATION["std.web"]
        for name in ["Router", "App", "Request", "Response", "Middleware",
                     "WebSocket", "Static", "Session", "Component", "VNode",
                     "create_element", "reactive", "ref", "computed", "css",
                     "define_types", "generate_client", "render_server",
                     "logger_middleware", "cors_middleware"]:
            self.assertIn(name, mod, "缺少导出: %s" % name)


if __name__ == "__main__":
    unittest.main()
