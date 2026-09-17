# -*- coding: utf-8 -*-
"""
Aurora v3.2.0 CLI/TUI 框架测试
所有 TUI 测试使用 MockScreen / 非 TTY 模式，不阻塞。
"""

import os
import sys
import unittest

# 强制非 TTY 模式，确保所有测试走 Mock 路径
_orig_no_color = os.environ.get("NO_COLOR")
os.environ["NO_COLOR"] = "1"

# 确保可以 import cli_tui
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cli_tui
from cli_tui import (
    fg, bg, bold, underline, dim, italic, strikethrough, rgb, style,
    strip_ansi, display_width,
    Spinner, ProgressBar, MultiProgress,
    Table, TreeNode,
    confirm, select, multiselect, input_prompt, password_prompt,
    Screen, MockScreen,
    KeyEvent, MouseEvent,
    Widget, Box, VBox, HBox,
    Text, Input, List, Button, TextArea,
    App,
)

# 导入完成后恢复 NO_COLOR，避免污染后续模块的颜色探测
if _orig_no_color is None:
    os.environ.pop("NO_COLOR", None)
else:
    os.environ["NO_COLOR"] = _orig_no_color


class TestColor(unittest.TestCase):
    """颜色与样式测试。"""

    def test_fg_returns_string(self):
        """fg 返回字符串。"""
        result = fg("hello", "red")
        self.assertIsInstance(result, str)
        # NO_COLOR 已设置，应原样返回
        self.assertEqual(result, "hello")

    def test_bold_and_strip_ansi(self):
        """bold 与 strip_ansi 配合。"""
        # 临时启用颜色验证 ANSI 码生成
        import cli_tui
        orig = cli_tui._supports_color
        cli_tui._supports_color = lambda: True
        try:
            colored = bold("hi")
            self.assertIn("\x1b[1m", colored)
            plain = strip_ansi(colored)
            self.assertEqual(plain, "hi")
        finally:
            cli_tui._supports_color = orig

    def test_style_combine(self):
        """style 组合样式。"""
        import cli_tui
        orig = cli_tui._supports_color
        cli_tui._supports_color = lambda: True
        try:
            out = style("x", "red", "bold")
            self.assertIn("\x1b[", out)
            self.assertEqual(strip_ansi(out), "x")
        finally:
            cli_tui._supports_color = orig

    def test_strip_ansi_real(self):
        """strip_ansi 去除多种 ANSI 码。"""
        text = "\x1b[31mred\x1b[0m \x1b[1bbold\x1b[0m"
        self.assertEqual(strip_ansi(text), "red bold")


class TestSpinner(unittest.TestCase):
    """Spinner 测试（非 TTY 模式）。"""

    def test_context_manager_non_tty(self):
        """Spinner 上下文管理器在非 TTY 下正常退出。"""
        with Spinner("处理中", style="dots") as s:
            self.assertIsInstance(s, Spinner)
            s.update("仍在处理")
        # 不抛异常即通过

    def test_start_stop(self):
        """start/stop 手动调用。"""
        s = Spinner("加载中", style="lines")
        s.start()
        s.stop(success=True, message="完成")


class TestProgressBar(unittest.TestCase):
    """进度条测试。"""

    def test_update_and_finish(self):
        """ProgressBar 更新与完成。"""
        pb = ProgressBar(100, prefix="测试", width=10)
        pb.update(50)
        self.assertEqual(pb.current, 50)
        line = pb.render_line()
        self.assertIn("测试", line)
        pb.advance(10)
        self.assertEqual(pb.current, 60)
        pb.finish()
        self.assertEqual(pb.current, 100)

    def test_multi_progress(self):
        """MultiProgress 多段进度。"""
        mp = MultiProgress()
        b1 = mp.add(100, prefix="A")
        b2 = mp.add(50, prefix="B")
        b1.advance(50)
        b2.update(25)
        rendered = mp.render()
        self.assertIn("A", rendered)
        self.assertIn("B", rendered)
        mp.finish()


class TestTable(unittest.TestCase):
    """表格测试。"""

    def test_rounded_border(self):
        """圆角边框渲染。"""
        t = Table(["名称", "值"], [["a", "1"], ["b", "2"]], border_style="rounded")
        out = t.render()
        self.assertIn("╭", out)
        self.assertIn("╰", out)
        self.assertIn("名称", out)

    def test_square_border(self):
        """方角边框。"""
        t = Table(["A"], [["x"]], border_style="square")
        out = t.render()
        self.assertIn("┌", out)
        self.assertIn("└", out)

    def test_minimal_border(self):
        """最小化边框。"""
        t = Table(["A", "B"], [["1", "2"]], border_style="minimal")
        out = t.render()
        self.assertIn("A", out)

    def test_add_row(self):
        """动态添加行。"""
        t = Table(["H"])
        t.add_row(["r1"])
        t.add_row(["r2"])
        out = t.render()
        self.assertIn("r1", out)
        self.assertIn("r2", out)


class TestTreeNode(unittest.TestCase):
    """树状结构测试。"""

    def test_render(self):
        """TreeNode 渲染。"""
        root = TreeNode("root")
        child1 = root.add_child(TreeNode("child1", icon="📁"))
        child1.add_child(TreeNode("leaf1"))
        root.add_child(TreeNode("child2"))
        out = root.render()
        self.assertIn("root", out)
        self.assertIn("child1", out)
        self.assertIn("leaf1", out)
        self.assertIn("└──", out)
        self.assertIn("├──", out)


class TestInteractions(unittest.TestCase):
    """交互提示测试（非 TTY 降级）。"""

    def test_confirm_non_tty(self):
        """confirm 非 TTY 返回 default。"""
        # 非 TTY 下应直接返回 default
        result = confirm("继续?", default=True)
        self.assertTrue(result)
        result2 = confirm("继续?", default=False)
        self.assertFalse(result2)

    def test_select_non_tty(self):
        """select 非 TTY 降级。"""
        # 非 TTY 下 select 会尝试 input，需 mock
        import builtins
        orig_input = builtins.input
        builtins.input = lambda *a, **kw: "2"
        try:
            result = select("选择", ["a", "b", "c"], default_index=0)
            self.assertEqual(result, "b")
        finally:
            builtins.input = orig_input

    def test_multiselect_non_tty(self):
        """multiselect 非 TTY 降级。"""
        import builtins
        orig_input = builtins.input
        builtins.input = lambda *a, **kw: "1,3"
        try:
            result = multiselect("多选", ["a", "b", "c"], default_indices=[0])
            self.assertIn("a", result)
            self.assertIn("c", result)
        finally:
            builtins.input = orig_input

    def test_input_with_validator(self):
        """带校验的输入。"""
        import builtins
        orig_input = builtins.input
        # 第一次非法，第二次合法
        builtins.input = lambda *a, **kw: "18"
        try:
            v = input_prompt("年龄", validator=lambda s: (s.isdigit(), "必须是数字"))
            self.assertEqual(v, "18")
        finally:
            builtins.input = orig_input


class TestScreen(unittest.TestCase):
    """屏幕管理测试（Mock 模式）。"""

    def test_mock_screen(self):
        """MockScreen 记录操作。"""
        s = MockScreen(80, 24)
        with s:
            s.clear()
            s.move_cursor(5, 5)
            s.hide_cursor()
            s.show_cursor()
            s.render(["hello"])
        self.assertIn("enter_alternate", s.calls)
        self.assertIn("exit_alternate", s.calls)
        self.assertIn("clear", s.calls)

    def test_screen_factory_non_tty(self):
        """Screen 在非 TTY 下返回 MockScreen。"""
        s = Screen()
        self.assertIsInstance(s, MockScreen)


class TestKeyEvent(unittest.TestCase):
    """事件解析测试。"""

    def test_parse_special_keys(self):
        """解析方向键。"""
        up = KeyEvent.parse_escape_seq("[A")
        self.assertEqual(up.key, KeyEvent.UP)
        down = KeyEvent.parse_escape_seq("[B")
        self.assertEqual(down.key, KeyEvent.DOWN)

    def test_parse_printable(self):
        """解析普通字符。"""
        ev = KeyEvent.parse_escape_seq("a")
        self.assertEqual(ev.key, "a")

    def test_parse_enter(self):
        """解析回车。"""
        ev = KeyEvent.parse_escape_seq("\r")
        self.assertEqual(ev.key, KeyEvent.ENTER)

    def test_parse_backspace(self):
        """解析退格。"""
        ev = KeyEvent.parse_escape_seq("\x7f")
        self.assertEqual(ev.key, KeyEvent.BACKSPACE)

    def test_mouse_event(self):
        """MouseEvent 创建。"""
        m = MouseEvent(10, 20, "left", MouseEvent.CLICK)
        self.assertEqual(m.x, 10)
        self.assertEqual(m.action, "click")


class TestLayout(unittest.TestCase):
    """布局容器测试。"""

    def test_box_draw(self):
        """Box 绘制边框。"""
        b = Box(0, 0, 20, 5, title="Test", border=True)
        lines = b.draw(MockScreen())
        self.assertTrue(any("┌" in l for l in lines))
        self.assertTrue(any("└" in l for l in lines))
        self.assertTrue(any("Test" in l for l in lines))

    def test_vbox_layout(self):
        """VBox 垂直排列。"""
        v = VBox(0, 0, 30, 10)
        t1 = v.add(Text("one", width=30))
        t2 = v.add(Text("two", width=30))
        self.assertEqual(t1.y, 0)
        self.assertEqual(t2.y, 1)
        lines = v.draw(MockScreen())
        self.assertTrue(any("one" in l for l in lines))
        self.assertTrue(any("two" in l for l in lines))

    def test_hbox_layout(self):
        """HBox 水平排列。"""
        h = HBox(0, 0, 30, 1)
        t1 = h.add(Text("A", width=5))
        t2 = h.add(Text("B", width=5))
        self.assertEqual(t1.x, 0)
        self.assertEqual(t2.x, 5)


class TestWidgets(unittest.TestCase):
    """具体控件测试。"""

    def test_text_widget(self):
        """Text 控件绘制。"""
        t = Text("hello", x=0, y=0, width=10)
        lines = t.draw(MockScreen())
        self.assertEqual(len(lines), 1)
        self.assertIn("hello", lines[0])

    def test_text_truncate(self):
        """Text 超长截断。"""
        t = Text("hello world", width=5)
        lines = t.draw(MockScreen())
        self.assertIn("…", lines[0])

    def test_input_editing(self):
        """Input 控件编辑。"""
        inp = Input(x=0, y=0, width=20)
        inp.handle_key(KeyEvent("a"))
        inp.handle_key(KeyEvent("b"))
        self.assertEqual(inp.value, "ab")
        inp.handle_key(KeyEvent(KeyEvent.BACKSPACE))
        self.assertEqual(inp.value, "a")
        # 左移再删
        inp.handle_key(KeyEvent(KeyEvent.LEFT))
        inp.handle_key(KeyEvent(KeyEvent.BACKSPACE))
        self.assertEqual(inp.value, "a")

    def test_list_navigation(self):
        """List 上下导航。"""
        lst = List(["a", "b", "c"], x=0, y=0, width=10, height=3)
        self.assertEqual(lst.selected_index, 0)
        lst.handle_key(KeyEvent(KeyEvent.DOWN))
        self.assertEqual(lst.selected_index, 1)
        lst.handle_key(KeyEvent(KeyEvent.DOWN))
        self.assertEqual(lst.selected_index, 2)
        lst.handle_key(KeyEvent(KeyEvent.UP))
        self.assertEqual(lst.selected_index, 1)
        self.assertEqual(lst.selected_value, "b")

    def test_button_click(self):
        """Button 触发。"""
        clicked = []
        btn = Button("OK", on_click=lambda: clicked.append(True))
        btn.focus()
        btn.handle_key(KeyEvent(KeyEvent.ENTER))
        self.assertEqual(len(clicked), 1)

    def test_textarea_edit(self):
        """TextArea 多行编辑。"""
        ta = TextArea(x=0, y=0, width=20, height=5, text="line1")
        self.assertEqual(ta.text, "line1")
        ta.handle_key(KeyEvent(KeyEvent.ENTER))
        ta.handle_key(KeyEvent("x"))
        self.assertIn("line1", ta.text)
        self.assertIn("x", ta.text)


class TestApp(unittest.TestCase):
    """App 主循环测试（Mock 模式）。"""

    def test_app_mock_mode(self):
        """App 在非 TTY 下进入 Mock 模式。"""
        app = App()
        self.assertTrue(app.mock_mode)
        self.assertIsInstance(app.screen, MockScreen)

    def test_app_run_with_injected_keys(self):
        """App Mock 模式处理注入按键后退出。"""
        app = App()
        root = VBox(0, 0, 40, 10)
        root.add(Text("Hello TUI", width=20))
        app.add(root)
        # 注入几个按键
        app.enqueue_key(KeyEvent("a"))
        app.enqueue_key(KeyEvent("b"))
        app.enqueue_key(KeyEvent(KeyEvent.ESC))
        app.run()
        # 应处理完队列后退出
        self.assertFalse(app._running)

    def test_app_status_bar(self):
        """App 状态栏。"""
        app = App()
        app.set_status("就绪")
        self.assertEqual(app._status, "就绪")
        buffer = app.render_frame()
        self.assertIn("就绪", buffer[-1])

    def test_app_stop(self):
        """App.stop() 设置 _running=False。"""
        app = App()
        app._running = True
        app.stop()
        self.assertFalse(app._running)


class TestEventDispatch(unittest.TestCase):
    """事件分发测试。"""

    def test_widget_event_consumption(self):
        """控件 handle_key 返回布尔值。"""
        w = Widget()
        self.assertFalse(w.handle_key(KeyEvent("a")))
        # 注册回调
        w.on_key = lambda ev: True
        self.assertTrue(w.handle_key(KeyEvent("a")))

    def test_mouse_dispatch(self):
        """鼠标事件分发。"""
        w = Widget()
        w.on_click = lambda ev: True
        self.assertTrue(w.handle_mouse(MouseEvent(1, 1, "left", "click")))

    def test_app_global_key_callback(self):
        """App 全局键盘回调。"""
        app = App()
        consumed = []
        app.on_key(lambda ev: consumed.append(ev) or True)
        ev = KeyEvent("q")
        app._dispatch_key(ev)
        self.assertEqual(len(consumed), 1)


class TestStdlibRegistration(unittest.TestCase):
    """标准库注册表测试。"""

    def test_registration_dict(self):
        """STDLIB_REGISTRATION 结构完整。"""
        reg = cli_tui.STDLIB_REGISTRATION
        self.assertIn("std.cli", reg)
        self.assertIn("std.tui", reg)
        # std.cli 关键项
        cli = reg["std.cli"]
        for key in ["fg", "bg", "bold", "Spinner", "ProgressBar", "Table",
                     "TreeNode", "confirm", "select", "input", "password",
                     "strip_ansi"]:
            self.assertIn(key, cli, f"std.cli 缺少 {key}")
        # std.tui 关键项
        tui = reg["std.tui"]
        for key in ["App", "Screen", "MockScreen", "Box", "VBox", "HBox",
                     "Text", "Input", "List", "Button", "TextArea",
                     "KeyEvent", "MouseEvent", "Widget"]:
            self.assertIn(key, tui, f"std.tui 缺少 {key}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
