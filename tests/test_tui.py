"""AuroraTUI 框架测试：样式 / 进度条 / 表格 / 树 / ANSI 解析 / 布局 / PTY / 事件循环"""

import os
import sys
import time
import unittest
from unittest import mock

import pytest

from aurora import tui


NEEDS_TTY = pytest.mark.skipif(
    not (sys.stdin.isatty() and sys.stdout.isatty()),
    reason="需要真实终端",
)


class TestStyle(unittest.TestCase):
    """终端样式与 ANSI 工具"""

    def test_strip_ansi(self):
        self.assertEqual(tui.strip_ansi("\x1b[31mhello\x1b[0m"), "hello")
        self.assertEqual(tui.strip_ansi("plain"), "plain")
        self.assertEqual(
            tui.strip_ansi("\x1b]0;title\x07hi\x1b[K"), "hi")

    def test_ansi_len(self):
        self.assertEqual(tui.ansi_len("abc"), 3)
        # 中文宽字符按 2 计
        self.assertEqual(tui.ansi_len("你好"), 4)
        # ANSI 序列不占可见宽度
        self.assertEqual(tui.ansi_len("\x1b[1;31mab\x1b[0m"), 2)

    def test_style_no_color(self):
        with mock.patch.object(tui, "COLOR_LEVEL", "no_color"):
            self.assertEqual(tui.style("hi", fg="red", bold=True), "hi")
            self.assertEqual(tui.color("hi", "red"), "hi")

    def test_style_truecolor(self):
        with mock.patch.object(tui, "COLOR_LEVEL", "truecolor"):
            out = tui.style("hi", fg="#ff0000", bold=True)
            self.assertIn("\x1b[1;38;2;255;0;0m", out)
            self.assertEqual(tui.strip_ansi(out), "hi")

    def test_style_16_named(self):
        with mock.patch.object(tui, "COLOR_LEVEL", "16"):
            out = tui.style("ok", fg="green", bg="black")
            self.assertIn("\x1b[32;40m", out)

    def test_style_256_palette(self):
        with mock.patch.object(tui, "COLOR_LEVEL", "256"):
            out = tui.style("x", fg=42)
            self.assertIn("38;5;42", out)


class TestProgressBar(unittest.TestCase):
    """进度条"""

    def test_update_and_percent(self):
        pb = tui.ProgressBar(200, width=10)
        pb.update(100)
        self.assertEqual(pb.current, 100)
        self.assertAlmostEqual(pb.percent, 50.0, places=1)

    def test_render_format(self):
        pb = tui.ProgressBar(100, width=10)
        pb.update(25)
        line = pb.render()
        self.assertIn("25/100", line)
        self.assertIn("25.0%", line)
        # 填充字符宽度 = 10
        plain = tui.strip_ansi(line)
        self.assertIn("█" * 2, plain)

    def test_done(self):
        pb = tui.ProgressBar(10)
        pb.done()
        self.assertEqual(pb.current, 10)
        self.assertIsNone(pb.eta())

    def test_clamp(self):
        pb = tui.ProgressBar(10)
        pb.update(999)
        self.assertEqual(pb.current, 10)
        pb.update(-5)
        self.assertEqual(pb.current, 0)


class TestTable(unittest.TestCase):
    """表格渲染"""

    def test_ascii_border(self):
        tbl = tui.Table(["Name", "Age"], [["Tom", "3"]], border_style="ascii")
        out = tbl.render()
        self.assertIn("+", out)
        self.assertIn("Name", out)
        self.assertIn("Tom", out)

    def test_unicode_border(self):
        tbl = tui.Table(["A"], [["1"]], border_style="unicode")
        out = tbl.render()
        self.assertIn("┌", out)
        self.assertIn("└", out)

    def test_no_border(self):
        tbl = tui.Table(["A", "B"], [["1", "2"]], border=False)
        out = tbl.render()
        self.assertNotIn("┌", out)
        self.assertIn("A", out)

    def test_col_width_auto(self):
        tbl = tui.Table(["S"], [["longcell"]], border=False)
        # 表头 S 列宽应被内容撑到 8
        self.assertEqual(tbl._col_widths(), [8])

    def test_align_right(self):
        tbl = tui.Table(["N"], [["x"]], border=False, align="right")
        line = tbl.render().splitlines()[1]
        self.assertTrue(line.rstrip().endswith("x"))


class TestTree(unittest.TestCase):
    """树渲染"""

    def test_siblings(self):
        t = tui.Tree("root")
        t.add("child1")
        t.add("child2")
        out = t.render().splitlines()
        self.assertEqual(out[0], "root")
        self.assertEqual(out[1], "├── child1")
        self.assertEqual(out[2], "└── child2")

    def test_nested(self):
        t = tui.Tree("root")
        a = t.add("a")
        t.add("a1", parent=a)
        out = t.render().splitlines()
        self.assertEqual(out[1], "├── a")
        self.assertEqual(out[2], "│   └── a1")

    def test_deep_last(self):
        t = tui.Tree("r")
        a = t.add("a")
        b = t.add("b", parent=a)
        t.add("c", parent=b)
        out = t.render().splitlines()
        self.assertEqual(out[-1], "    └── c")


class TestHighlight(unittest.TestCase):
    """代码高亮"""

    def test_python_keyword(self):
        out = tui.highlight("def foo(): return 1", "python")
        self.assertIn("def", tui.strip_ansi(out))
        self.assertNotEqual(out, "def foo(): return 1")

    def test_json(self):
        out = tui.highlight('{"a": 1}', "json")
        self.assertIn('"a"', tui.strip_ansi(out))

    def test_unknown_language(self):
        self.assertEqual(tui.highlight("code", "cobol"), "code")


class TestAnsiParser(unittest.TestCase):
    """ANSI 解析与虚拟终端"""

    def test_cursor_move(self):
        evs = tui.AnsiParser().parse("\x1b[5;10H")
        self.assertEqual(len(evs), 1)
        self.assertIsInstance(evs[0], tui.CursorMoveEvent)
        self.assertEqual((evs[0].row, evs[0].col), (5, 10))

    def test_relative_move(self):
        evs = tui.AnsiParser().parse("\x1b[A\x1b[C")
        self.assertTrue(all(isinstance(e, tui.CursorMoveEvent) for e in evs))
        self.assertTrue(evs[0].relative)
        self.assertEqual(evs[0].row, -1)
        self.assertEqual(evs[1].col, 1)

    def test_sgr(self):
        evs = tui.AnsiParser().parse("\x1b[1;31mhi\x1b[0m")
        colors = [e for e in evs if isinstance(e, tui.ColorEvent)]
        self.assertEqual(colors[0].params, [1, 31])
        texts = [e.text for e in evs if isinstance(e, tui.TextEvent)]
        self.assertEqual(texts, ["hi"])

    def test_clear(self):
        evs = tui.AnsiParser().parse("\x1b[2J\x1b[K")
        kinds = [(e.what, e.mode) for e in evs if isinstance(e, tui.ClearEvent)]
        self.assertEqual(kinds, [("screen", 2), ("line", 0)])

    def test_mouse_mode(self):
        evs = tui.AnsiParser().parse("\x1b[?1000h\x1b[?1000l")
        modes = [(e.mode, e.on) for e in evs if isinstance(e, tui.ModeEvent)]
        self.assertEqual(modes, [(1000, True), (1000, False)])

    def test_terminal_buffer(self):
        buf = tui.TerminalBuffer(rows=3, cols=10)
        buf.feed("hello\nworld")
        rendered = buf.render()
        self.assertIn("hello", rendered)
        self.assertIn("world", rendered)
        self.assertEqual(buf.cursor_row, 1)
        buf.feed("\x1b[2J")
        self.assertNotIn("hello", buf.render())


class TestLayout(unittest.TestCase):
    """Flexbox 布局计算"""

    def test_hbox_flex_grow(self):
        box = tui.HBox(children=[tui.Widget(), tui.Widget()])
        box.children[0].flex_grow = 1
        box.children[1].flex_grow = 2
        rects = box.compute(30, 5)
        self.assertEqual([r.w for _, r in rects], [10, 20])

    def test_vbox(self):
        box = tui.VBox(children=[tui.Widget(), tui.Widget()])
        box.children[0].flex_grow = 1
        box.children[1].flex_grow = 1
        rects = box.compute(10, 20)
        self.assertEqual([r.h for _, r in rects], [10, 10])

    def test_justify_center(self):
        box = tui.HBox(children=[tui.Widget()], justify_content="center")
        box.children[0].flex_basis = 10
        rect = box.compute(40, 5)[0][1]
        self.assertEqual(rect.x, 15)

    def test_align_center_cross(self):
        box = tui.HBox(children=[tui.Widget()], align_items="center")
        box.children[0].flex_basis = 10
        box.children[0].min_height = 2
        rect = box.compute(40, 10)[0][1]
        self.assertEqual(rect.y, 4)


class TestEventLoop(unittest.TestCase):
    """事件总线与定时器（mock 时钟）"""

    def setUp(self):
        self.loop = tui.EventLoop()
        self.clock = [0.0]
        self.loop.now_func = lambda: self.clock[0]

    def test_emit(self):
        seen = []
        self.loop.on("tick", seen.append)
        self.loop.emit("tick", 42)
        self.assertEqual(seen, [42])

    def test_off(self):
        seen = []
        self.loop.on("e", seen.append)
        self.loop.off("e", seen.append)
        self.loop.emit("e", 1)
        self.assertEqual(seen, [])

    def test_set_timeout(self):
        called = []
        self.loop.set_timeout(lambda: called.append("a"), 100)
        self.clock[0] = 50
        self.assertEqual(self.loop.pump(), 0)
        self.clock[0] = 150
        self.assertEqual(self.loop.pump(), 1)
        self.assertEqual(called, ["a"])
        # 一次性定时器已被移除
        self.clock[0] = 300
        self.assertEqual(self.loop.pump(), 0)

    def test_set_interval(self):
        count = [0]
        self.loop.set_interval(lambda: count.__setitem__(0, count[0] + 1), 100)
        for t in (100, 200, 300):
            self.clock[0] = t
            self.loop.pump()
        self.assertEqual(count[0], 3)

    def test_cancel(self):
        called = []
        h = self.loop.set_timeout(lambda: called.append("x"), 10)
        self.loop.cancel(h)
        self.clock[0] = 1000
        self.assertEqual(self.loop.pump(), 0)
        self.assertEqual(called, [])


class TestWidgets(unittest.TestCase):
    """Widget 基类交互"""

    def test_listbox_keys(self):
        lb = tui.ListBox(["a", "b", "c"])
        self.assertEqual(lb.selected, 0)
        self.assertTrue(lb.handle_key(tui.Key(b"\x1b[B")))
        self.assertEqual(lb.selected, 1)
        lb.handle_key(tui.Key(b"\x1b[B"))
        lb.handle_key(tui.Key(b"\x1b[A"))
        self.assertEqual(lb.selected, 1)

    def test_textbox_insert_and_backspace(self):
        tb = tui.TextBox()
        self.assertTrue(tb.handle_key(tui.Key(b"h")))
        self.assertTrue(tb.handle_key(tui.Key(b"i")))
        self.assertEqual(tb.text, "hi")
        tb.handle_key(tui.Key(b"\x7f"))
        self.assertEqual(tb.text, "h")

    def test_button_click(self):
        clicked = []
        btn = tui.Button("Go", on_click=lambda: clicked.append(1))
        btn.handle_key(tui.Key(b"\r"))
        self.assertEqual(clicked, [1])

    def test_tabs_switch(self):
        tabs = tui.Tabs(["One", "Two", "Three"])
        tabs.handle_key(tui.Key(b"\x1b[C"))
        self.assertEqual(tabs.active, 1)
        tabs.handle_key(tui.Key(b"\x1b[D"))
        tabs.handle_key(tui.Key(b"\x1b[D"))
        self.assertEqual(tabs.active, 2)  # 循环

    def test_key_parse(self):
        keys = tui.Key.parse(b"\x1b[B")
        self.assertEqual(keys[0].name, "down")
        keys = tui.Key.parse(b"a\r")
        self.assertEqual(keys[0].char, "a")
        self.assertEqual(keys[1].name, "enter")


@unittest.skipUnless(os.name == "posix", "PTY 仅支持 POSIX")
class TestPTY(unittest.TestCase):
    """伪终端"""

    def test_spawn_echo(self):
        p = tui.PTY()
        p.spawn(["/bin/echo", "-n", "aurora"])
        p.set_size(24, 80)
        chunks = []
        deadline = time.time() + 3
        while time.time() < deadline:
            try:
                data = p.read(timeout=0.2)
            except OSError:
                break
            if not data:
                break
            chunks.append(data)
            if p.poll() is not None:
                break
        out = b"".join(chunks).decode("utf-8", "replace")
        p.wait()
        p.close()
        self.assertIn("aurora", out)

    def test_terminate(self):
        p = tui.PTY()
        p.spawn(["/bin/sleep", "30"])
        self.assertIsNone(p.poll())
        p.terminate()
        self.assertNotEqual(p.wait(), 0)
        p.close()


class TestPromptDegrade(unittest.TestCase):
    """非终端环境的降级行为"""

    def test_confirm_degrade(self):
        with mock.patch.object(tui, "_is_interactive", return_value=False):
            self.assertTrue(tui.prompt_confirm("ok?", default=True))
            self.assertFalse(tui.prompt_confirm("ok?", default=False))

    def test_input_degrade(self):
        with mock.patch.object(tui, "_is_interactive", return_value=False):
            self.assertEqual(tui.prompt_input("name", default="x"), "x")
            self.assertEqual(tui.prompt_input("name"), "")

    def test_select_degrade(self):
        with mock.patch.object(tui, "_is_interactive", return_value=False):
            self.assertEqual(tui.prompt_select("pick", ["a", "b"], default=1), 1)

    def test_multiselect_degrade(self):
        with mock.patch.object(tui, "_is_interactive", return_value=False):
            self.assertEqual(tui.prompt_multiselect("pick", ["a", "b"],
                                                    defaults=[1]), [1])


class TestPanel(unittest.TestCase):
    """面板"""

    def test_panel_render(self):
        out = tui.Panel("hello", title="T", border_style="rounded")
        self.assertIn("╭", out)
        self.assertIn("╰", out)
        self.assertIn("hello", out)


if __name__ == "__main__":
    unittest.main()
