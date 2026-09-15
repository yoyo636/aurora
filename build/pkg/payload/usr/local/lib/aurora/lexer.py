"""Aurora 词法分析器 — 将源码转换为 Token 流"""

from typing import List
from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"L{line}:C{column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def tokenize(self) -> List[Token]:
        """词法分析主函数"""
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break
                
            char = self.source[self.pos]

            # 属性前缀 #[...]：v3.1.0 条件编译/属性语法
            if char == '#' and self.pos + 1 < len(self.source) \
                    and self.source[self.pos + 1] == '[':
                self.tokens.append(Token(TokenType.POUND, '#', self.line, self.column))
                self._advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column))
                self._advance()
                continue

            # 注释
            if char == '#':
                self._skip_comment()
                continue
            if char == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                self._skip_comment()
                continue
            
            # 数字
            if char.isdigit():
                self._read_number()
                continue
            
            # 字符串
            if char in '"\'':
                self._read_string()
                continue

            # 原始字符串 r'...' / r"..."(不插值,反斜杠保留)
            if (char in 'rR' and self.pos + 1 < len(self.source)
                    and self.source[self.pos + 1] in '"\''):
                self._read_raw_string()
                continue
            
            # 标识符/关键字
            if char.isalpha() or char == '_':
                self._read_identifier()
                continue
            
            # 运算符和分隔符
            self._read_symbol()
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """跳过空白字符（保留换行）"""
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char in ' \t\r':
                self._advance()
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self._advance()
                self.line += 1
                self.column = 1
            else:
                break
    
    def _skip_comment(self):
        """跳过注释"""
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self._advance()
    
    def _read_number(self):
        """读取数字（整数或浮点数）"""
        start = self.pos
        has_dot = False
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isdigit():
                self._advance()
            elif char == '.' and not has_dot:
                # 小数点：但 `1..5` 中 `..` 是区间运算符，不是小数
                if self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '.':
                    break
                has_dot = True
                self._advance()
            else:
                break
        
        value = self.source[start:self.pos]
        token_type = TokenType.FLOAT if has_dot else TokenType.INTEGER
        self.tokens.append(Token(token_type, value, self.line, self.column))
    
    def _read_string(self):
        """读取字符串,处理转义序列 \\n \\t \\r \\\\ \\\" \\' 等"""
        quote = self.source[self.pos]
        self._advance()
        chars = []
        escapes = {'n': '\n', 't': '\t', 'r': '\r', '0': '\0',
                   '\\': '\\', '"': '"', "'": "'", '/': '/'}

        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char == quote:
                value = ''.join(chars)
                self.tokens.append(Token(TokenType.STRING, value, self.line, self.column))
                self._advance()
                return
            elif char == '\\':
                self._advance()  # 跳过反斜杠
                if self.pos >= len(self.source):
                    break
                esc = self.source[self.pos]
                self._advance()
                chars.append(escapes.get(esc, esc))
            else:
                chars.append(char)
                self._advance()

        raise LexerError("未闭合的字符串", self.line, self.column)
    
    def _read_raw_string(self):
        """读取原始字符串 r'...' / r"..."：不做插值、不处理转义"""
        self._advance()  # 跳过 r
        quote = self.source[self.pos]
        self._advance()
        start = self.pos
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char == quote:
                value = self.source[start:self.pos]
                self.tokens.append(Token(TokenType.RAW_STRING, value, self.line, self.column))
                self._advance()
                return
            self._advance()
        raise LexerError("未闭合的原始字符串", self.line, self.column)

    def _read_identifier(self):
        """读取标识符或关键字"""
        start = self.pos
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isalnum() or char == '_':
                self._advance()
            else:
                break
        
        value = self.source[start:self.pos]
        
        # 宏标识符: 以 ! 结尾(但 != 是不相等运算符)
        if self.pos < len(self.source) and self.source[self.pos] == '!':
            if self.pos + 1 >= len(self.source) or self.source[self.pos + 1] != '=':
                self._advance()
                value = self.source[start:self.pos]
        
        token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, value, self.line, self.column))
    
    def _read_symbol(self):
        """读取运算符和分隔符"""
        char = self.source[self.pos]
        next_char = self.source[self.pos + 1] if self.pos + 1 < len(self.source) else ''
        next_next_char = self.source[self.pos + 2] if self.pos + 2 < len(self.source) else ''

        # 三字符运算符
        if char == '.' and next_char == '.' and next_next_char == '.':
            self.tokens.append(Token(TokenType.VARIADIC, '...', self.line, self.column))
            self._advance()
            self._advance()
            self._advance()
            return
        
        # 双字符运算符
        two_char = char + next_char
        two_char_map = {
            '==': TokenType.EQ,
            '!=': TokenType.NE,
            '<=': TokenType.LE,
            '>=': TokenType.GE,
            '&&': TokenType.AND,
            '||': TokenType.OR,
            '<<': TokenType.SHIFT_LEFT,
            '>>': TokenType.SHIFT_RIGHT,
            '->': TokenType.ARROW,
            '=>': TokenType.FAT_ARROW,
            '<-': TokenType.CHANNEL_SEND,
            '+=': TokenType.PLUS_EQ,
            '-=': TokenType.MINUS_EQ,
            '*=': TokenType.STAR_EQ,
            '/=': TokenType.SLASH_EQ,
            '**': TokenType.POWER,
            '?.': TokenType.OPTIONAL_DOT,
            '??': TokenType.NULL_COALESCE,
            '|>': TokenType.PIPE_OP,
            '..': TokenType.RANGE,
        }
        
        if two_char in two_char_map:
            self.tokens.append(Token(two_char_map[two_char], two_char, self.line, self.column))
            self._advance()
            self._advance()
            return
        
        # 单字符运算符
        single_char_map = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '%': TokenType.PERCENT,
            '<': TokenType.LT,
            '>': TokenType.GT,
            '!': TokenType.NOT,
            '=': TokenType.ASSIGN,
            '&': TokenType.AMP,
            '^': TokenType.CARET,
            '?': TokenType.QUESTION,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
            '.': TokenType.DOT,
            '|': TokenType.PIPE,
            '@': TokenType.AT,
        }
        
        if char in single_char_map:
            self.tokens.append(Token(single_char_map[char], char, self.line, self.column))
            self._advance()
        else:
            raise LexerError(f"未知字符: {char!r}", self.line, self.column)
    
    def _advance(self):
        """前进一个字符"""
        self.pos += 1
        self.column += 1
