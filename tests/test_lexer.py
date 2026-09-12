"""词法分析器测试"""

import unittest

from aurora.lexer import Lexer, LexerError
from aurora.tokens import TokenType


def toks(src):
    return Lexer(src).tokenize()


class TestLexerBasics(unittest.TestCase):
    def test_literals(self):
        ts = toks('42 3.14 "hi" true false nil')
        types = [t.type for t in ts]
        self.assertEqual(types[:6], [
            TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING,
            TokenType.BOOLEAN, TokenType.BOOLEAN, TokenType.NIL,
        ])

    def test_keywords(self):
        ts = toks('let const fn if else for while match type enum trait impl as')
        kinds = {t.value: t.type for t in ts}
        self.assertEqual(kinds['let'], TokenType.LET)
        self.assertEqual(kinds['fn'], TokenType.FN)
        self.assertEqual(kinds['impl'], TokenType.IMPL)
        self.assertEqual(kinds['as'], TokenType.AS)  # 新关键字

    def test_operators(self):
        ts = toks('+ - * / % ** == != <= >= && || -> => <- & &mut ?')
        values = [t.value for t in ts if t.value]
        self.assertIn('**', values)
        self.assertIn('->', values)
        self.assertIn('=>', values)
        self.assertIn('<-', values)
        self.assertIn('&', values)
        # &mut 拆分为 & 和 mut 关键字
        kinds = {t.type for t in ts}
        self.assertIn(TokenType.MUT, kinds)

    def test_comments_skipped(self):
        ts = toks('# 这是一行注释\nlet x = 1')
        types = [t.type for t in ts]
        self.assertNotIn(TokenType.COMMENT, types)
        self.assertIn(TokenType.LET, types)

    def test_identifier_and_keyword(self):
        ts = toks('hello world _private x1')
        self.assertTrue(all(t.type == TokenType.IDENTIFIER for t in ts[:-1]))

    def test_escape_in_string(self):
        # \" 转义为字面引号(不再保留反斜杠)
        ts = toks(r'"a\"b"')
        self.assertEqual(ts[0].value, 'a"b')

    def test_escape_sequences(self):
        ts = toks(r'"a\nb\tc\\d"')
        self.assertEqual(ts[0].value, 'a\nb\tc\\d')

    def test_unclosed_string_raises(self):
        with self.assertRaises(LexerError):
            toks('"oops')

    def test_unknown_char_raises(self):
        with self.assertRaises(LexerError):
            toks('@')

    def test_position(self):
        ts = toks('let x = 1\nlet y = 2')
        line2 = [t for t in ts if t.line == 2]
        self.assertTrue(line2)


if __name__ == '__main__':
    unittest.main()
