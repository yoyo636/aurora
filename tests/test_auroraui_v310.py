"""AuroraUI v3.1.0 — 跨平台 GUI 框架测试。

所有测试都使用 Mock 后端，无需显示环境。需要真实窗口/显示的测试
用 ``@pytest.mark.skipif`` 跳过。
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.ui import (  # noqa: E402
    ALIGN_STRETCH,
    Application,
    Backend,
    BackendFactory,
    Button,
    Canvas,
    ChangeEvent,
    CheckBox,
    ComboBox,
    Dialog,
    Event,
    EventDispatcher,
    FileDialog,
    Grid,
    GraphicsContext,
    HBox,
    INLINE_SPECIFICITY,
    InputDialog,
    KeyEvent,
    Label,
    LayoutParams,
    ListView,
    Matrix,
    Menu,
    MenuItem,
    MessageDialog,
    MockBackend,
    MouseEvent,
    PaintEvent,
    ProgressBar,
    RadioButton,
    Slider,
    Stack,
    StatusBar,
    StyleEngine,
    StyleSheet,
    TableView,
    TabView,
    TextArea,
    TextField,
    Toolbar,
    TreeView,
    VBox,
    Window,
    WindowHandle,
    apply_style,
    on,
)
from aurora.ui.backends.cocoa import CocoaBackend
from aurora.ui.backends.gtk import GtkBackend
from aurora.ui.backends.web import WebBackend
from aurora.ui.backends.win32 import Win32Backend


# ---------------------------------------------------------------------------
# 夹具
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_application():
    """每个测试前后清空 Application 单例，避免窗口互相污染。"""
    Application.reset()
    BackendFactory._cache.clear()
    yield
    Application.reset()
    BackendFactory._cache.clear()


@pytest.fixture
def mock_backend():
    return MockBackend()


# ===========================================================================
# 1) backend
# ===========================================================================

class TestBackendFactory:
    def test_factory_returns_backend_instance(self):
        backend = BackendFactory.get_backend("mock")
        assert isinstance(backend, Backend)
        assert backend.get_platform() == "mock"

    def test_factory_auto_detect_platform(self):
        # 在 macOS 上应返回 "cocoa" 或降级 "mock"，绝不为 None
        backend = BackendFactory.get_backend()
        assert backend.get_platform() in {"cocoa", "win32", "gtk", "mock"}

    def test_unknown_platform_falls_back_to_mock(self):
        backend = BackendFactory.get_backend("plan9")
        assert isinstance(backend, MockBackend)

    def test_mock_creates_window_and_control(self, mock_backend):
        win = mock_backend.create_window("hi", 400, 300)
        assert isinstance(win, WindowHandle)
        assert win.title == "hi" and win.width == 400
        ctrl = mock_backend.create_control(win, "button", text="OK")
        assert ctrl.control_type == "button"
        assert ctrl.properties["text"] == "OK"
        assert ctrl in mock_backend.controls

    def test_mock_show_hide_destroy(self, mock_backend):
        win = mock_backend.create_window("t", 100, 100)
        mock_backend.show_window(win)
        assert win.visible is True
        mock_backend.hide_window(win)
        assert win.visible is False
        mock_backend.destroy_window(win)
        assert win not in mock_backend.windows

    def test_mock_set_get_property(self, mock_backend):
        ctrl = mock_backend.create_control(None, "label")
        mock_backend.set_control_property(ctrl, "text", "hello")
        assert mock_backend.get_control_property(ctrl, "text") == "hello"

    def test_mock_connect_and_simulate_click(self, mock_backend):
        calls = []
        btn = mock_backend.create_control(None, "button")
        mock_backend.connect_event(btn, "clicked", lambda h: calls.append(h))
        mock_backend.simulate_click(btn)
        assert calls == [btn]


# ===========================================================================
# 2) events
# ===========================================================================

class TestEvents:
    def test_mouse_event_fields(self):
        ev = MouseEvent(type="mouse_down", x=10, y=20, button=1)
        assert ev.x == 10 and ev.y == 20 and ev.button == 1
        assert isinstance(ev.timestamp, float)

    def test_key_event_fields(self):
        ev = KeyEvent(type="key_down", key="Enter", code="Enter", text="\r")
        assert ev.key == "Enter" and ev.code == "Enter"

    def test_stop_propagation(self):
        ev = Event(type="x")
        ev.stop_propagation()
        assert ev.propagation_stopped is True

    def test_dispatcher_dispatch_to_target(self):
        owner = object()
        d = EventDispatcher(owner)
        seen = []
        d.on("click", lambda e: seen.append(e))
        ev = d.dispatch(Event(type="click"))
        assert seen and seen[0] is ev

    def test_dispatcher_bubbling(self):
        root = object()
        child = object()
        root_d = EventDispatcher(root)
        child_d = EventDispatcher(child)
        child_d.attach_parent(root_d)

        order = []
        root_d.on("click", lambda e: order.append("root"))
        child_d.on("click", lambda e: order.append("child"))
        child_d.dispatch(Event(type="click"))
        # 冒泡：child 先，root 后
        assert order == ["child", "root"]

    def test_dispatcher_capture_phase(self):
        root = object()
        child = object()
        root_d = EventDispatcher(root)
        child_d = EventDispatcher(child)
        child_d.attach_parent(root_d)

        order = []
        root_d.on("click", lambda e: order.append("root-capture"), capture=True)
        root_d.on("click", lambda e: order.append("root-bubble"))
        child_d.on("click", lambda e: order.append("child"))
        child_d.dispatch(Event(type="click"))
        assert order == ["root-capture", "child", "root-bubble"]

    def test_dispatcher_propagation_stops(self):
        root = object()
        child = object()
        root_d = EventDispatcher(root)
        child_d = EventDispatcher(child)
        child_d.attach_parent(root_d)

        root_d.on("click", lambda e: None)
        child_d.on("click", lambda e: e.stop_propagation())
        # 不应抛错，root 也不应被调用 —— 用一个会抛错的回调验证
        root_d._handlers.clear()
        root_d.on("click", lambda e: (_ for _ in ()).throw(AssertionError("root should not fire")))
        child_d.dispatch(Event(type="click"))

    def test_on_decorator_registers_handler(self):
        class MyWidget:
            def __init__(self):
                self.d = EventDispatcher(self)
                install_event_handlers(self, self.d)
                self.got = None

            @on("click")
            def handle(self, event):
                self.got = event

        from aurora.ui.events import install_event_handlers  # noqa: WPS433

        w = MyWidget()
        ev = Event(type="click")
        w.d.dispatch(ev)
        assert w.got is ev


# ===========================================================================
# 3) window
# ===========================================================================

class TestWindow:
    def test_window_creation(self, mock_backend):
        app = Application.instance(backend=mock_backend)
        win = Window("Hello", 400, 300, backend=mock_backend)
        assert win.title == "Hello"
        assert win.width == 400 and win.height == 300
        assert win in app.open_windows

    def test_window_setters(self, mock_backend):
        win = Window(backend=mock_backend)
        win.set_title("New Title")
        assert win.title == "New Title"
        win.resize(640, 480)
        assert (win.width, win.height) == (640, 480)
        win.move(200, 150)
        assert (win.x, win.y) == (200, 150)

    def test_window_show_hide_close(self, mock_backend):
        win = Window(backend=mock_backend)
        win.show()
        assert win.visible is True
        win.hide()
        assert win.visible is False
        win.close()
        assert win not in Application.instance().open_windows

    def test_window_event_callbacks(self, mock_backend):
        win = Window(backend=mock_backend)
        events = []
        win.on_resize = lambda w: events.append(("resize", w.width, w.height))
        win.on_move = lambda w: events.append(("move", w.x, w.y))
        win.resize(500, 400)
        win.move(10, 20)
        assert ("resize", 500, 400) in events
        assert ("move", 10, 20) in events

    def test_application_run_quit(self, mock_backend):
        app = Application.instance(backend=mock_backend)
        app.set_app_name("TestApp")
        assert app.app_name == "TestApp"
        app.run()
        assert "run_loop" in mock_backend.call_log
        app.quit()
        assert mock_backend.quit_requested is True

    def test_window_set_content(self, mock_backend):
        win = Window(backend=mock_backend)
        btn = Button("x")
        win.set_content(btn)
        assert win.content is btn
        assert btn.backend_handle is not None


# ===========================================================================
# 4) controls
# ===========================================================================

class TestControls:
    def test_button_creation(self, mock_backend):
        clicks = []
        btn = Button("Click me", on_click=lambda e: clicks.append(1))
        assert btn.text == "Click me"
        btn.create(mock_backend, None)
        assert btn.backend_handle.control_type == "button"
        assert btn.backend_handle.properties["text"] == "Click me"

    def test_label_textfield_textarea(self):
        lbl = Label("Hello")
        tf = TextField("init", placeholder="type here")
        ta = TextArea("multi", rows=5, cols=30)
        assert lbl.text == "Hello"
        assert tf.placeholder == "type here"
        assert (ta.rows, ta.cols) == (5, 30)

    def test_checkbox_toggle(self):
        cb = CheckBox("Agree", checked=False)
        changes = []
        cb.on_event("toggled", lambda e: changes.append(e.new_value))
        cb.toggle()
        assert cb.checked is True
        assert changes == [True]

    def test_radio_button_group(self):
        a = RadioButton("A", group="g1", checked=True)
        b = RadioButton("B", group="g1")
        assert a.group == b.group == "g1"
        assert a.checked and not b.checked

    def test_combobox_selected(self):
        cb = ComboBox(["a", "b", "c"], selected_index=1)
        assert cb.selected_text == "b"

    def test_slider_progressbar(self):
        s = Slider(min=0, max=200, value=50)
        p = ProgressBar(value=30, maximum=100)
        assert (s.min, s.max, s.value) == (0, 200, 50)
        assert p.value == 30 and p.maximum == 100

    def test_listview_treeview_tableview(self):
        lv = ListView(["a", "b", "c"])
        tv = TreeView([{"label": "root", "children": []}])
        tb = TableView(columns=["A", "B"], rows=[[1, 2], [3, 4]])
        assert lv.items == ["a", "b", "c"]
        assert tv.nodes[0]["label"] == "root"
        assert tb.columns == ["A", "B"] and tb.rows == [[1, 2], [3, 4]]

    def test_tabview(self):
        tab = TabView([("One", Label("1")), ("Two", Label("2"))])
        assert len(tab.tabs) == 2
        assert tab.active_index == 0

    def test_dialog_creation(self):
        dlg = Dialog("My Dialog")
        dlg.close(42)
        assert dlg.result == 42
        md = MessageDialog("Hi", "Body", buttons=["OK", "Cancel"])
        assert md.buttons == ["OK", "Cancel"]
        fd = FileDialog("open")
        assert fd.mode == "open"
        idlg = InputDialog("Title", "Your name?")
        assert idlg.prompt == "Your name?"

    def test_menu_toolbar_statusbar(self):
        mi = MenuItem("Open", "Ctrl+O")
        menu = Menu("File", [mi])
        tb = Toolbar([mi])
        sb = StatusBar("Ready")
        assert menu.title == "File"
        assert tb.items == [mi]
        assert sb.text == "Ready"

    def test_widget_tree_traversal(self):
        # 用 Stack 当容器
        s = Stack()
        b1 = Button("1"); b2 = Button("2")
        s.add(b1); s.add(b2)
        assert s.children == [b1, b2]
        b1.id = "b1"
        assert s.find_by_id("b1") is b1


# ===========================================================================
# 5) layout
# ===========================================================================

class TestLayout:
    def test_vbox_stacks_vertically(self):
        box = VBox(spacing=10)
        c1, c2 = Button("A"), Button("B")
        c1.preferred_height = 20; c2.preferred_height = 30
        box.add(c1); box.add(c2)
        box.layout(None, 100, 200)
        x1, y1, w1, h1 = c1.bounds
        x2, y2, w2, h2 = c2.bounds
        assert y1 == 0 and h1 == 20
        assert y2 == 20 + 10 and h2 == 30
        assert w1 == w2 == 100

    def test_hbox_stacks_horizontally(self):
        box = HBox(spacing=5)
        c1, c2 = Button("A"), Button("B")
        c1.preferred_width = 40; c2.preferred_width = 60
        box.add(c1); box.add(c2)
        box.layout(None, 200, 50)
        x1, y1, w1, h1 = c1.bounds
        x2, y2, w2, h2 = c2.bounds
        assert x1 == 0 and w1 == 40
        assert x2 == 40 + 5 and w2 == 60

    def test_grid_layout(self):
        g = Grid(rows=2, cols=2, row_spacing=2, col_spacing=2)
        a, b = Button("a"), Button("b")
        g.add(a, row=0, col=0)
        g.add(b, row=1, col=1)
        g.layout(None, 100, 100)
        ax, ay, aw, ah = a.bounds
        bx, by, bw, bh = b.bounds
        assert (ax, ay) == (0, 0)
        assert aw == bh == pytest.approx(49)  # (100 - 2)/2

    def test_layout_params_stretch(self):
        lp = LayoutParams(stretch=2, min_width=10)
        w, h = lp.clamped_size(5, 20)
        assert w == 10  # 被 min_width 夹紧
        assert lp.stretch == 2

    def test_layout_add_remove(self):
        box = VBox()
        b = Button("x")
        box.add(b)
        assert b in box.children
        box.remove(b)
        assert b not in box.children

    def test_stack_layout_overlaps(self):
        st = Stack()
        a, b = Button("a"), Button("b")
        st.add(a); st.add(b)
        st.layout.layout(None, 300, 200)
        assert a.bounds == (0, 0, 300, 200)
        assert b.bounds == (0, 0, 300, 200)


# ===========================================================================
# 6) style
# ===========================================================================

class TestStyle:
    def test_parse_type_class_id_selectors(self):
        sheet = StyleSheet(
            "Button { color: red; } "
            ".primary { background-color: blue; } "
            "#submit { font-size: 14px; }"
        )
        assert len(sheet.rules) == 3

    def test_apply_style_to_widget(self):
        sheet = StyleSheet("Button { color: red; font-size: 14px; }")
        btn = Button("OK")
        result = apply_style(btn, sheet)
        assert result["color"] == "red"
        assert result["font-size"] == "14px"
        assert btn._computed_style["color"] == "red"

    def test_class_selector_matches(self):
        sheet = StyleSheet(".primary { color: blue; }")
        btn = Button("OK", style_class="primary")
        result = apply_style(btn, sheet)
        assert result.get("color") == "blue"

    def test_id_selector_matches(self):
        sheet = StyleSheet("#submit { background-color: yellow; }")
        btn = Button("Go", id="submit")
        result = apply_style(btn, sheet)
        assert result["background-color"] == "yellow"

    def test_specificity_priority(self):
        # 类型选择器 specificity=1；类选择器 specificity=10
        sheet = StyleSheet(
            "Button { color: red; }"
            ".primary { color: blue; }"
        )
        btn = Button("OK", style_class="primary")
        engine = StyleEngine(sheet)
        result = engine.compute_style(btn)
        assert result["color"] == "blue"  # 类选择器胜出

    def test_inline_style_overrides_everything(self):
        sheet = StyleSheet(
            "Button { color: red; }"
            ".primary { color: blue; }"
        )
        btn = Button("OK", style_class="primary")
        btn.style = "color: green;"
        engine = StyleEngine(sheet)
        result = engine.compute_style(btn)
        assert result["color"] == "green"
        assert INLINE_SPECIFICITY > 1000

    def test_descendant_selector(self):
        sheet = StyleSheet("Dialog Label { color: gray; }")
        dlg = Dialog()
        lbl = Label("inner")
        lbl.parent = dlg
        result = apply_style(lbl, sheet)
        assert result["color"] == "gray"

    def test_pseudo_class_disabled(self):
        sheet = StyleSheet("Button:disabled { opacity: 0.5; }")
        btn = Button("OK", enabled=False)
        btn._hovered = btn._pressed = btn._focused = False
        result = apply_style(btn, sheet)
        assert result["opacity"] == "0.5"


# ===========================================================================
# 7) canvas
# ===========================================================================

class TestCanvas:
    def test_graphics_context_path_commands(self):
        ctx = GraphicsContext(100, 100)
        ctx.begin_path()
        ctx.move_to(0, 0)
        ctx.line_to(10, 10)
        ctx.bezier_curve_to(0, 10, 10, 0, 10, 10)
        ctx.arc(50, 50, 10, 0, 3.14)
        ctx.rect(0, 0, 20, 20)
        ctx.close_path()
        ctx.fill()
        cmds = [c[0] for c in ctx.command_log]
        assert cmds == [
            "begin_path", "move_to", "line_to", "bezier_curve_to",
            "arc", "rect", "close_path", "fill",
        ]

    def test_transform_stack_save_restore(self):
        ctx = GraphicsContext()
        ctx.save()
        ctx.translate(10, 20)
        ctx.rotate(0.5)
        ctx.scale(2, 2)
        mid = ctx.current_transform
        ctx.restore()
        after = ctx.current_transform
        # restore 后应回到单位矩阵
        assert after.a == 1 and after.b == 0 and after.e == 0
        assert mid.e != 0  # translate 生效过

    def test_matrix_multiply(self):
        m = Matrix().translate(5, 0).translate(0, 5)
        x, y = m.transform_point(0, 0)
        assert (x, y) == (5, 5)

    def test_canvas_paint_callback(self):
        canvas = Canvas(width=100, height=100)
        @canvas.on_paint
        def draw(ctx):
            ctx.fill_style = "red"
            ctx.rect(0, 0, 50, 50)
            ctx.fill()
        ctx = canvas.repaint()
        assert ctx.width == 100 and ctx.height == 100
        assert any(c[0] == "fill" for c in ctx.command_log)

    def test_canvas_draw_text_and_image(self):
        ctx = GraphicsContext(200, 200)
        ctx.fill_text("hello", 10, 10)
        ctx.draw_image(object(), 0, 0, 50, 50)
        ctx.clear_rect(0, 0, 10, 10)
        names = [c[0] for c in ctx.command_log]
        assert "fill_text" in names and "draw_image" in names and "clear_rect" in names


# ===========================================================================
# 8) backends
# ===========================================================================

class TestBackends:
    def test_cocoa_is_available_boolean(self):
        assert isinstance(CocoaBackend.is_available(), bool)

    def test_win32_is_available_boolean(self):
        assert isinstance(Win32Backend.is_available(), bool)
        # 在 macOS 上必然 False
        assert Win32Backend.is_available() is False

    def test_gtk_is_available_boolean(self):
        assert isinstance(GtkBackend.is_available(), bool)

    def test_web_is_available_in_python(self):
        # CPython 上永远 False
        assert WebBackend.is_available() is False

    def test_unavailable_backend_falls_back(self, monkeypatch):
        # 直接请求 web 后端 —— 在 CPython 上不可用，应降级到 Mock
        backend = BackendFactory.get_backend("web")
        assert isinstance(backend, MockBackend)

    def test_backends_subclass_mock(self):
        # 不可用时仍能实例化（不抛错）
        wb = Win32Backend()
        wb.show_window(wb.create_window("x", 10, 10))
        assert wb.windows[0].visible is True


# ===========================================================================
# 9) 需要真实显示的测试（默认跳过）
# ===========================================================================

DISPLAY_AVAILABLE = bool(
    os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
)


@pytest.mark.skipif(not DISPLAY_AVAILABLE, reason="需要图形显示环境")
class TestRealDisplay:
    def test_real_cocoa_window(self):
        backend = BackendFactory.get_backend("cocoa")
        win = backend.create_window("real", 200, 200)
        backend.show_window(win)
        assert win is not None

    def test_real_event_loop(self):
        backend = BackendFactory.get_backend("cocoa")
        backend.run_loop()
        backend.quit()
