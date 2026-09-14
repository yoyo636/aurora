"""Aurora 格式化器测试"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.formatter import format_code, format_file, register_cli  # noqa: E402


class TestFormatterBasics(unittest.TestCase):
    def test_operator_spacing(self):
        self.assertEqual(format_code("let x=1+2*3"),
                         "let x = 1 + 2 * 3\n")

    def test_power_no_space(self):
        out = format_code("let y=a**2")
        self.assertIn("a**2", out)
        self.assertNotIn("a ** 2", out)

    def test_comma_space(self):
        self.assertEqual(format_code("fn add(a,b,c){return a+b+c}"),
                         "fn add(a, b, c) {\n    return a + b + c\n}\n")

    def test_colon_annotation(self):
        out = format_code("let x:int=5")
        self.assertIn("let x: int = 5", out)

    def test_function_indent(self):
        src = "fn f(){\nreturn 1\n}"
        out = format_code(src)
        self.assertIn("    return 1", out)

    def test_if_else_blocks(self):
        src = "fn f(x){\nif x>0{\nreturn 1\n} else {\nreturn 0\n}\n}"
        out = format_code(src)
        self.assertIn("if x > 0 {", out)
        self.assertIn("    return 1", out)
        self.assertIn("} else {", out)
        self.assertIn("        return 0", out)

    def test_4_space_indent(self):
        src = "fn f(){\nif true {\nreturn 1\n}\n}"
        out = format_code(src)
        # 函数体一级缩进 = 4 空格；if 内二级 = 8 空格
        self.assertIn("    if true {", out)
        self.assertIn("        return 1", out)

    def test_no_trailing_whitespace(self):
        src = "fn f(){\nlet x=1   \n}"
        out = format_code(src)
        for line in out.splitlines():
            self.assertEqual(line, line.rstrip(), f"行尾有空白: {line!r}")

    def test_string_preserved(self):
        src = 'fn f(){return "hello #not a comment"}'
        out = format_code(src)
        self.assertIn('"hello #not a comment"', out)

    def test_single_quote_preserved(self):
        src = "fn f(){return 'single'}"
        out = format_code(src)
        self.assertIn("'single'", out)


class TestFormatterIdempotent(unittest.TestCase):
    def test_idempotent(self):
        src = """
fn add(a,b){
return a+b
}

fn main(){
let x: int=add(1,2)
if x>2 {
println("big")
} else {
println("small")
}
}
"""
        once = format_code(src)
        twice = format_code(once)
        self.assertEqual(once, twice)


class TestFormatterComments(unittest.TestCase):
    def test_standalone_comment_preserved(self):
        src = "// 顶部注释\nfn f(){\nreturn 1\n}"
        out = format_code(src)
        self.assertIn("// 顶部注释", out)

    def test_hash_comment_preserved(self):
        src = "fn f(){\n# 内部注释\nreturn 1\n}"
        out = format_code(src)
        self.assertIn("# 内部注释", out)

    def test_trailing_comment(self):
        src = "let x=5 # 赋值"
        out = format_code(src)
        self.assertIn("# 赋值", out)
        self.assertIn("let x = 5", out)


class TestFormatterComplex(unittest.TestCase):
    def test_while_for(self):
        src = "fn f(n){\nvar i=0\nwhile i<n {\nprintln(i)\ni=i+1\n}\nfor k in 1..10 {\nprintln(k)\n}\n}"
        out = format_code(src)
        self.assertIn("while i < n {", out)
        self.assertIn("for k in 1..10 {", out)
        self.assertIn("        println(i)", out)

    def test_match(self):
        src = "fn f(x){\nmatch x {\n1 => \"a\",\n_ => \"b\"\n}\n}"
        out = format_code(src)
        self.assertIn("match x {", out)
        self.assertIn('1 => "a"', out)

    def test_function_blank_line(self):
        src = "fn a(){return 1}\nfn b(){return 2}"
        out = format_code(src)
        self.assertEqual(out, "fn a() {\n    return 1\n}\n\nfn b() {\n    return 2\n}\n")

    def test_const_and_type_annotation(self):
        src = "const MAX:int=100"
        out = format_code(src)
        self.assertIn("const MAX: int = 100", out)


class TestFormatFile(unittest.TestCase):
    def test_format_file_inplace(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.aur")
            with open(path, "w", encoding="utf-8") as f:
                f.write("fn f(){return 1+1}\n")
            changed = format_file(path)
            self.assertTrue(changed)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("fn f() {", content)

    def test_format_file_no_change(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.aur")
            formatted = "fn f() {\n    return 1 + 1\n}\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(formatted)
            changed = format_file(path)
            self.assertFalse(changed)


class TestCli(unittest.TestCase):
    def test_register_cli(self):
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers()
        register_cli(sub)
        args = parser.parse_args(["fmt", "some.aur", "--check"])
        self.assertEqual(args.path, "some.aur")
        self.assertTrue(args.check)


if __name__ == "__main__":
    unittest.main()
