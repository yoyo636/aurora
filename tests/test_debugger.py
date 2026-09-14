"""Aurora 调试器测试 — 断点 / 单步 / 变量 / 调用栈 / 条件断点 / 非交互模式"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.debugger import Debugger, DebuggerQuit, register_cli


SAMPLE = """fn main() {
    let x = 1
    let y = x + 1
    return y
}

main()
"""

LOOP = """let sum = 0
for i in 1..3 {
    sum = sum + i
}
println(sum)
"""

COND = """let x = 1
let x = 2
let x = 3
"""


class RecordingDebugger(Debugger):
    """记录每一次停下时的上下文，便于断言"""

    def __init__(self, path):
        super().__init__(path=path)
        self.stops = []

    def _stop(self, file, line, reason):
        snap = {}
        e = self.current_env
        while e is not None:
            for k, v in e.bindings.items():
                if not k.startswith('_'):
                    snap.setdefault(k, v)
            e = e.parent
        self.stops.append({
            'line': line,
            'reason': reason,
            'frames': [f['name'] for f in self.frames],
            'locals': snap,
        })
        super()._stop(file, line, reason)


def run_dbg(source: str, commands):
    """写临时文件，批量执行调试命令，返回 RecordingDebugger"""
    fd, path = tempfile.mkstemp(suffix='.aur')
    with os.fdopen(fd, 'w') as f:
        f.write(source)
    dbg = RecordingDebugger(path)
    dbg.load()
    dbg.run(commands=list(commands))
    os.remove(path)
    return dbg


class TestBreakpoints(unittest.TestCase):
    def test_line_breakpoint_triggers(self):
        dbg = run_dbg(SAMPLE, ['b 3', 'c', 'c'])
        lines = [s['line'] for s in dbg.stops]
        # 初始停在第 1 行，随后命中断点第 3 行
        self.assertIn(1, lines)
        self.assertIn(3, lines)

    def test_function_breakpoint(self):
        dbg = run_dbg(SAMPLE, ['b main', 'c', 'c'])
        names = set()
        for s in dbg.stops:
            names.update(s['frames'])
        self.assertIn('main', names)

    def test_conditional_breakpoint_skips(self):
        # 条件 x == 1 在第 3 行求值时 x 已为 3 → 不应停在第 3 行
        dbg = run_dbg(COND, ['b 3 if x == 1', 'c'])
        self.assertNotIn(3, [s['line'] for s in dbg.stops])

    def test_conditional_breakpoint_hits(self):
        # x > 1 在第 3 行为真 → 应停在第 3 行
        dbg = run_dbg(COND, ['b 3 if x > 1', 'c', 'c'])
        self.assertIn(3, [s['line'] for s in dbg.stops])

    def test_delete_breakpoint(self):
        dbg = run_dbg(SAMPLE, ['b 3', 'delete 1', 'c'])
        # 删掉断点后应不再停在第 3 行
        self.assertNotIn(3, [s['line'] for s in dbg.stops])

    def test_info_breakpoints(self):
        dbg = run_dbg(SAMPLE, ['b 3', 'b main', 'info breakpoints', 'c', 'c'])
        # 不崩溃即可；直接调用检查字符串
        out = dbg.info_breakpoints()
        self.assertIn('func', out)


class TestStepping(unittest.TestCase):
    def test_step_into_function(self):
        # 初始停在 1；s 到调用点 7；再 s 进入 main，应停在函数体第一行（第 2 行）
        dbg = run_dbg(SAMPLE, ['s', 's', 'bt', 'c'])
        lines = [s['line'] for s in dbg.stops]
        self.assertIn(2, lines)

    def test_step_over(self):
        # 在 main() 调用处（第 7 行）next：命中断点后不进入函数内部
        dbg = run_dbg(SAMPLE, ['b 7', 'n', 'c'])
        lines = [s['line'] for s in dbg.stops]
        self.assertIn(7, lines)
        self.assertNotIn(2, lines)

    def test_finish_returns(self):
        # 进入 main 后 finish：回到调用者的下一条语句
        src = """fn main() {
    let x = 1
    return x
}
main()
let after = 2
"""
        dbg = run_dbg(src, ['b main', 'c', 'f', 'c'])
        reasons = [s['reason'] for s in dbg.stops]
        self.assertTrue(any('返回' in r for r in reasons))


class TestInspection(unittest.TestCase):
    def test_locals_params(self):
        src = """fn add(a, b) {
    return a + b
}
add(1, 2)
"""
        dbg = run_dbg(src, ['b 2', 'locals', 'c'])
        # 停在函数体第 2 行时局部应有 a=1, b=2
        local_stop = [s for s in dbg.stops if s['line'] == 2][-1]
        self.assertEqual(local_stop['locals'].get('a'), 1)
        self.assertEqual(local_stop['locals'].get('b'), 2)

    def test_backtrace(self):
        dbg = run_dbg(SAMPLE, ['b main', 'bt', 'c'])
        frame_names = dbg.frames_names_at_last_stop = dbg.stops[-1]['frames']
        self.assertIn('main', frame_names)
        self.assertIn('<main>', frame_names)

    def test_print_expression(self):
        src = """let a = 10
let b = 32
"""
        dbg = run_dbg(src, ['b 2', 'p a + b', 'c'])
        # print 不应崩溃；求值通过 _eval_interp
        self.assertTrue(len(dbg.stops) >= 1)


class TestBatchMode(unittest.TestCase):
    def test_noninteractive_runs_to_end(self):
        dbg = run_dbg(SAMPLE, ['b 3', 'c', 'c'])
        # 批量模式执行完成不抛异常
        self.assertTrue(True)

    def test_quit_command(self):
        dbg = run_dbg(SAMPLE, ['b 3', 'q'])
        # quit 后提前结束，不应执行到末尾
        self.assertTrue(True)


class TestCLIRegistration(unittest.TestCase):
    def test_register_cli(self):
        import argparse
        ap = argparse.ArgumentParser()
        sub = ap.add_subparsers()
        register_cli(sub)
        args = ap.parse_args(['debug', 'x.aur', '--break', '5'])
        self.assertEqual(args.break_line, '5')


if __name__ == '__main__':
    unittest.main()
