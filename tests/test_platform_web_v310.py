"""Aurora v3.1.0 平台原生绑定 / 全平台打包 / Web 运行时 / 浏览器引擎测试

覆盖：
* native_bindings: CocoaBridge、Win32 结构体、注册表、通知接口
* packaging: macOS .app / Info.plist、NSIS、deb control、PWA manifest
* web_runtime: DOM 操作、JS 编译、组件渲染、路由、扩展模板
* browser_engine: HTML 解析、CSS 解析、样式级联、布局盒模型

所有测试不依赖显示环境；外部工具（emcc/codesign/dpkg-deb 等）不可用时
验证接口与产物文件，而非实际调用。
"""

import json
import os
import sys
import tempfile
import unittest

# 让 `import aurora.*` 在 pytest 与直接运行下都可解析
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 同时支持 `from aurora.xxx import ...`
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from aurora import native_bindings as nb          # noqa: E402
from aurora import packaging as pk                # noqa: E402
from aurora import web_runtime as wr              # noqa: E402
from aurora import browser_engine as be           # noqa: E402
from aurora.ast_nodes import (                    # noqa: E402
    Program, Block, FnDef, Param, ReturnStmt, LetStmt, ConstStmt,
    BinaryOp, Identifier, IntLiteral, IfStmt, ForStmt, ImportStmt,
    NamedType,
)


# ===========================================================================
# native_bindings
# ===========================================================================

class TestNativeBindings(unittest.TestCase):
    """平台原生绑定：跨平台可导入、优雅降级。"""

    def test_cocoa_bridge_constructible(self):
        """CocoaBridge 可创建；available() 是布尔值，非 macOS 上为 False。"""
        bridge = nb.CocoaBridge()
        self.assertIsInstance(bridge.available(), bool)
        if not nb.IS_MACOS:
            self.assertFalse(bridge.available())
            self.assertIsNone(bridge.objc_get_class("NSApplication"))
        else:
            # macOS 上应能拿到真实类句柄（int）
            self.assertIsInstance(bridge.objc_get_class("NSApplication"), int)
        # 任意平台 msg_send 都不抛异常
        bridge.msg_send(None, "run")

    def test_cocoa_proxy_chainable_off_platform(self):
        """非 macOS 上 CocoaClass 链式调用不崩溃。"""
        if nb.IS_MACOS:
            self.skipTest("仅在非 macOS 平台验证降级")
        cls = nb.CocoaClass("NSWindow")
        self.assertEqual(cls.name, "NSWindow")
        # 不抛异常即可
        win = nb.MacIntegration()
        self.assertFalse(win.send_notification("t", "b"))
        self.assertFalse(win.bounce_dock())

    def test_win32_structures_defined(self):
        """Win32 结构体在任意平台都可引用。"""
        bridge = nb.Win32Bridge()
        for name in ("RECT", "POINT", "MSG", "WNDCLASSEX"):
            self.assertTrue(hasattr(bridge, name), name)
            struct = getattr(bridge, name)
            self.assertTrue(hasattr(struct, "_fields_"), name)

    def test_win32_window_off_platform(self):
        """非 Windows 上 Win32Window 可实例化且方法为 no-op。"""
        win = nb.Win32Window("hello", 400, 300)
        self.assertEqual(win.title, "hello")
        self.assertEqual((win.width, win.height), (400, 300))
        win.set_title("changed")
        win.resize(800, 600)
        self.assertEqual(win.title, "changed")
        self.assertEqual((win.width, win.height), (800, 600))
        win.show(); win.hide(); win.destroy()  # 不抛异常

    def test_registry_off_platform_returns_false(self):
        """非 Windows 上注册表读写返回 None / False。"""
        integ = nb.WindowsIntegration()
        self.assertIsNone(integ.reg_read("SOFTWARE\\Aurora", "Version"))
        self.assertFalse(integ.reg_write("SOFTWARE\\Aurora", "Version", "1.0"))
        self.assertFalse(integ.reg_delete("SOFTWARE\\Aurora", "Version"))
        # 事件日志同样降级
        self.assertFalse(integ.write_event_log("src", "msg"))

    def test_notification_interface(self):
        """通知接口签名正确，非 macOS 返回 False。"""
        mac = nb.MacIntegration()
        result = mac.send_notification("标题", "正文", subtitle="副标题")
        self.assertIsInstance(result, bool)
        if not nb.IS_MACOS:
            self.assertFalse(result)

    def test_systray_and_winui(self):
        """托盘 / WinUI 接口在非 Windows 上降级。"""
        tray = nb.SysTrayIcon("icon.png", "tip")
        tray.add_menu_item("打开", lambda: None)
        self.assertFalse(tray.show())
        self.assertFalse(tray.notify("t", "b"))
        ui = nb.WinUIBridge()
        self.assertFalse(ui.activate("main.xaml"))


# ===========================================================================
# packaging
# ===========================================================================

class TestPackaging(unittest.TestCase):
    """打包工具：验证产物文件结构与文本内容。"""

    def test_macos_app_structure_and_info_plist(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.MacOSPackager("MyApp", "1.2.3", "com.test.myapp")
            app = pkger.build_app_structure(d, executable="/bin/ls")
            self.assertTrue(os.path.isdir(app))
            for sub in ("Contents/MacOS", "Contents/Resources", "Contents/Frameworks"):
                self.assertTrue(os.path.isdir(os.path.join(app, sub)), sub)
            plist = os.path.join(app, "Contents", "Info.plist")
            self.assertTrue(os.path.exists(plist))
            text = open(plist, encoding="utf-8").read()
            self.assertIn("CFBundleName", text)
            self.assertIn("MyApp", text)
            self.assertIn("com.test.myapp", text)
            self.assertIn("1.2.3", text)

    def test_macos_info_plist_lsuielement(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.MacOSPackager("Agent", "1.0", "com.agent")
            app = pkger.build_app_structure(d, executable="", ls_ui_element=True)
            text = open(os.path.join(app, "Contents", "Info.plist")).read()
            self.assertIn("LSUIElement", text)

    def test_windows_nsis_script(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.WindowsPackager("WinApp", "2.0", "com.win")
            pkger.build_exe("/bin/ls", d)
            nsi = pkger.generate_nsis_script("WinApp.exe", d)
            self.assertTrue(os.path.exists(nsi))
            text = open(nsi, encoding="utf-8").read()
            self.assertIn("Name", text)
            self.assertIn("CreateShortCut", text)
            self.assertIn("WriteRegStr", text)
            self.assertIn("Uninstall", text)

    def test_windows_wxs_msi(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.WindowsPackager("WinApp", "2.0", "com.win")
            wxs = pkger.generate_wxs("WinApp.exe", d)
            text = open(wxs, encoding="utf-8").read()
            self.assertIn("Wix", text)
            self.assertIn("Product", text)

    def test_linux_deb_control(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.LinuxPackager("LxApp", "0.9", "com.lx")
            root = pkger.build_deb("/bin/ls", d)
            control = os.path.join(root, "DEBIAN", "control")
            self.assertTrue(os.path.exists(control))
            text = open(control, encoding="utf-8").read().lower()
            self.assertIn("package: lxapp", text)
            self.assertIn("version: 0.9", text)

    def test_linux_rpm_spec_and_appimage(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.LinuxPackager("RpmApp", "1.0", "com.rpm")
            spec = pkger.build_rpm("/bin/ls", d)
            self.assertIn("Name:", open(spec).read())
            ai = pkger.build_appimage("/bin/ls", d)
            self.assertTrue(os.path.exists(os.path.join(ai, "AppRun")))
            self.assertTrue(os.path.exists(os.path.join(ai, "RpmApp.desktop")))

    def test_web_pwa_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.WebPackager("WebApp", "3.0", "com.web")
            pkger.build_pwa(d)
            self.assertTrue(os.path.exists(os.path.join(d, "index.html")))
            manifest = json.load(open(os.path.join(d, "manifest.json")))
            self.assertEqual(manifest["name"], "WebApp")
            self.assertEqual(manifest["display"], "standalone")
            self.assertGreaterEqual(len(manifest["icons"]), 1)
            self.assertTrue(os.path.exists(os.path.join(d, "service-worker.js")))

    def test_mobile_skeletons(self):
        with tempfile.TemporaryDirectory() as d:
            mp = pk.MobilePackager("MobApp", "1.0", "com.mob")
            ios = mp.build_ios(".", d)
            self.assertTrue(os.path.exists(os.path.join(ios, "Info.plist")))
            andr = mp.build_android(".", d)
            self.assertTrue(os.path.exists(
                os.path.join(andr, "app", "src", "main", "AndroidManifest.xml")))
            self.assertTrue(os.path.exists(os.path.join(andr, "app", "build.gradle")))

    def test_notarize_script_generated(self):
        with tempfile.TemporaryDirectory() as d:
            pkger = pk.MacOSPackager("App", "1.0", "com.x")
            script = pkger.notarize(os.path.join(d, "App.app"),
                                    "me@x.com", "abcd-efgh-ijkl")
            self.assertTrue(os.path.exists(script))
            self.assertIn("notarytool", open(script).read())


# ===========================================================================
# web_runtime
# ===========================================================================

class TestWebRuntime(unittest.TestCase):
    """DOM / JS 编译 / 框架 / 扩展。"""

    def setUp(self):
        self.dom = wr.DOMBridge()

    def _make_tree(self):
        root = self.dom.create_element("div")
        root.set_attribute("id", "app")
        self.dom.document.append_child(root)
        self.dom.register_id(root)
        h = self.dom.create_element("h1")
        h.text_content = "Hello"
        root.append_child(h)
        btn = self.dom.create_element("button")
        btn.add_class("primary")
        root.append_child(btn)
        return root, h, btn

    def test_dom_element_operations(self):
        root, h, btn = self._make_tree()
        self.assertIs(self.dom.get_element_by_id("app"), root)
        self.assertEqual(h.text_content, "Hello")
        self.assertIn("primary", btn.get_attribute("class"))
        btn.remove_class("primary")
        self.assertNotIn("primary", btn.get_attribute("class") or "")
        # 属性
        root.set_attribute("data-x", "1")
        self.assertEqual(root.get_attribute("data-x"), "1")
        root.remove_attribute("data-x")
        self.assertIsNone(root.get_attribute("data-x"))
        # 样式
        root.set_style("color", "red")
        self.assertIn("color:red", root.get_attribute("style"))
        # 查询
        self.assertEqual(len(self.dom.query_selector_all("h1")), 1)

    def test_dom_event(self):
        _, _, btn = self._make_tree()
        calls = []
        btn.add_event_listener("click", lambda e: calls.append(1))
        ev = wr.DOMEvent("click", btn, client_x=10, client_y=20)
        btn.dispatch_event(ev)
        self.assertEqual(len(calls), 1)
        self.assertEqual((ev.client_x, ev.client_y), (10, 20))
        ev.prevent_default()
        self.assertTrue(ev._default_prevented)

    def test_js_compiler_function(self):
        """编译一个含参数、返回、JSDoc 的函数。"""
        prog = Program(statements=[
            FnDef(name="add",
                  params=[Param(name="a"), Param(name="b")],
                  return_type=NamedType(name="int"),
                  body=Block(statements=[
                      ReturnStmt(value=BinaryOp(
                          left=Identifier(name="a"), op="+",
                          right=Identifier(name="b")))])),
            LetStmt(name="x",
                    initializer=BinaryOp(left=IntLiteral(value=1), op="+",
                                         right=IntLiteral(value=2))),
            ImportStmt(path=["net", "http"]),
        ])
        js = wr.JSCompiler().compile(prog, "main")
        self.assertIn("function add(a, b)", js)
        self.assertIn("return (a + b);", js)
        self.assertIn("@returns", js)          # 类型擦除为 JSDoc
        self.assertIn("const x = (1 + 2);", js)
        self.assertIn("import", js)            # ES6 import

    def test_js_compiler_control_flow(self):
        prog = Program(statements=[
            IfStmt(condition=BinaryOp(left=Identifier(name="x"), op=">",
                                      right=IntLiteral(value=0)),
                   then_body=Block(statements=[
                       ConstStmt(name="y",
                                 initializer=IntLiteral(value=1))])),
            ForStmt(variables=["i"], iterable=Identifier(name="arr"),
                    body=Block(statements=[])),
        ])
        js = wr.JSCompiler().compile(prog)
        self.assertIn("if", js)
        self.assertIn("for (const i of arr)", js)

    def test_component_render_and_lifecycle(self):
        class Hello(wr.Component):
            def render(self):
                return wr.VNode("div", {"class": "greeting"},
                                [wr.VNode("span", {}, ["hi"])])

        c = Hello({"name": "Aurora"})
        c.on_mount()
        self.assertTrue(c._mounted)
        v = c.render()
        self.assertEqual(v.tag, "div")
        self.assertEqual(v.props["class"], "greeting")
        c.set_state({"n": 1})
        self.assertEqual(c.state["n"], 1)
        c.on_unmount()
        self.assertFalse(c._mounted)

    def test_virtual_dom_diff(self):
        old = wr.VNode("div", {"a": "1"}, [wr.VNode("span")])
        new = wr.VNode("div", {"a": "2"}, [wr.VNode("span")])
        patches = wr.diff(old, new)
        self.assertTrue(any(p["type"] == "props" for p in patches))
        # 结构替换
        patches2 = wr.diff(wr.VNode("div"), wr.VNode("p"))
        self.assertTrue(any(p["type"] == "replace" for p in patches2))

    def test_router_match_and_navigate(self):
        class A(wr.Component):
            pass
        class B(wr.Component):
            pass
        router = wr.Router([wr.Route("/home", A), wr.Route("/about", B)])
        self.assertEqual(router.match("/home").component, A)
        self.assertIsNone(router.match("/nope"))
        seen = []
        router.on_change(lambda p: seen.append(p))
        route = router.navigate("/about")
        self.assertEqual(route.component, B)
        self.assertEqual(router.current, "/about")
        self.assertEqual(seen, ["/about"])

    def test_store_redux(self):
        store = wr.Store(lambda s, a: s + 1 if a["type"] == "inc" else s, 0)
        notified = []
        store.subscribe(lambda: notified.append(store.get_state()))
        store.dispatch({"type": "inc"})
        store.dispatch({"type": "inc"})
        self.assertEqual(store.get_state(), 2)
        self.assertEqual(notified, [1, 2])

    def test_extension_template_chrome(self):
        with tempfile.TemporaryDirectory() as d:
            eg = wr.ExtensionGenerator("MyExt", "demo", "1.0")
            root = eg.generate("chrome", d)
            manifest = json.load(open(os.path.join(root, "manifest.json")))
            self.assertEqual(manifest["manifest_version"], 3)
            self.assertEqual(manifest["name"], "MyExt")
            for f in ("background.js", "content.js", "popup.html", "options.html"):
                self.assertTrue(os.path.exists(os.path.join(root, f)), f)

    def test_extension_template_firefox(self):
        with tempfile.TemporaryDirectory() as d:
            root = wr.ExtensionGenerator("FxExt").generate("firefox", d)
            manifest = json.load(open(os.path.join(root, "manifest.json")))
            self.assertEqual(manifest["manifest_version"], 3)
            self.assertIn("browser_specific_settings", manifest)

    def test_generate_web_project(self):
        with tempfile.TemporaryDirectory() as d:
            root = wr.generate_web_project("myweb", d)
            self.assertTrue(os.path.exists(os.path.join(root, "index.html")))
            self.assertTrue(os.path.exists(os.path.join(root, "src", "app.js")))


# ===========================================================================
# browser_engine
# ===========================================================================

class TestBrowserEngine(unittest.TestCase):
    """HTML / CSS / 样式级联 / 布局。"""

    def test_html_parser_tags_and_attrs(self):
        html = ('<html><body><h1 class="title" id="main">Hi</h1>'
                '<div class="card"><p>text</p></div>'
                '<img src="a.png"/><br></body></html>')
        root = be.HTMLParser().parse(html)
        # 找到 h1
        h1 = next(n for n in root.walk() if n.tag == "h1")
        self.assertEqual(h1.attrs["class"], "title")
        self.assertEqual(h1.id, "main")
        self.assertIn("Hi", h1.text_content)
        # 自闭合 img / br 不产生未闭合栈
        tags = [n.tag for n in root.walk()]
        self.assertIn("img", tags)
        self.assertIn("br", tags)

    def test_html_entities_and_fault_tolerance(self):
        text = be.decode_entities("a &lt; b &amp; c &#65;")
        self.assertEqual(text, "a < b & c A")
        # 未闭合标签容错
        root = be.HTMLParser().parse("<div><p>x<p>y")
        div = next(n for n in root.walk() if n.tag == "div")
        self.assertEqual(len([c for c in div.walk() if c.tag == "p"]), 2)

    def test_css_parser_rules(self):
        css = "h1.title { color: red; font-size: 20px; } .card { margin: 10px; }"
        sheet = be.CSSParser().parse(css)
        self.assertEqual(len(sheet.rules), 2)
        r0 = sheet.rules[0]
        self.assertEqual(r0.selectors[0].tag, "h1")
        self.assertEqual(r0.selectors[0].classes, ["title"])
        props = {d.prop: d.value for d in r0.declarations}
        self.assertEqual(props["color"], "red")
        self.assertEqual(props["font-size"], "20px")

    def test_selector_specificity(self):
        self.assertEqual(be.Selector(raw="#a.b", ids=["a"], classes=["b"]).specificity(),
                         (1, 1, 0))
        self.assertEqual(be.Selector(raw="div", tag="div").specificity(),
                         (0, 0, 1))

    def test_style_cascade_and_inheritance(self):
        html = '<div><p class="lead">hi</p></div>'
        css = "p { color: blue; } .lead { font-size: 18px; }"
        root = be.HTMLParser().parse(html)
        sheet = be.CSSParser().parse(css)
        engine = be.StyleEngine(sheet)
        engine.apply(root)
        p = next(n for n in root.walk() if n.tag == "p")
        self.assertEqual(p.styles["color"], "blue")
        self.assertEqual(p.styles["font-size"], "18px")
        # 继承：父 div 未设置 color，p 仍匹配了自身规则
        # 初始值生效
        self.assertEqual(p.styles["margin"], "0")

    def test_layout_box_model(self):
        root = be.HTMLParser().parse('<div><p>x</p></div>')
        sheet = be.CSSParser().parse(
            "div { padding: 5px; border-width: 2px; margin: 3px; }")
        be.StyleEngine(sheet).apply(root)
        div = next(n for n in root.walk() if n.tag == "div")
        engine = be.LayoutEngine(400, 300)
        box = engine.layout(div)
        # margin/padding/border 被解析
        self.assertEqual(box.padding, 5)
        self.assertEqual(box.border, 2)
        self.assertEqual(box.margin, 3)
        # content_box 扣掉 padding+border
        cx, cy, cw, ch = box.content_box
        self.assertEqual(cx, box.x + box.padding + box.border)
        # margin_box 向外扩 margin
        mx, my, mw, mh = box.margin_box
        self.assertEqual(mx, box.x - box.margin)

    def test_renderer_draw_order(self):
        root = be.HTMLParser().parse('<div>hi</div>')
        sheet = be.CSSParser().parse("div { background-color: red; border-width: 1px; }")
        be.StyleEngine(sheet).apply(root)
        box = be.LayoutEngine(200, 100).layout(root)
        commands = be.Renderer().render(box)
        kinds = [c[0] for c in commands]
        # 背景先于内容
        if "fill_rect" in kinds and "draw_text" in kinds:
            self.assertLess(kinds.index("fill_rect"), kinds.index("draw_text"))

    def test_js_engine_binding_interface(self):
        binding = be.QuickJSBinding("/nonexistent.dylib")
        self.assertFalse(binding.available())
        with self.assertRaises(NotImplementedError):
            binding.evaluate("1+1")
        v8 = be.V8Binding("/also-missing.dylib")
        self.assertFalse(v8.available())


if __name__ == "__main__":
    unittest.main()
