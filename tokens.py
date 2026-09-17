"""Aurora 词法分析 — Token 定义"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


class TokenType(Enum):
    # 字面量
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    RAW_STRING = auto()
    BOOLEAN = auto()
    NIL = auto()
    
    # 标识符
    IDENTIFIER = auto()
    
    # 关键字
    LET = auto()
    VAR = auto()
    CONST = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    MATCH = auto()
    TYPE = auto()
    STRUCT = auto()    # struct (type 别名)
    ENUM = auto()
    TRAIT = auto()
    IMPL = auto()
    IMPORT = auto()
    FROM = auto()
    PUB = auto()
    MUT = auto()
    SPAWN = auto()
    SELECT = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    TEST = auto()
    ASSERT = auto()
    DEFER = auto()
    YIELD = auto()
    # ── v3.1.0 语言级增强 ──
    EXTERN = auto()    # extern "C" { ... } 外部函数声明
    UNSAFE = auto()    # unsafe { ... } / unsafe fn
    ASYNC = auto()     # async fn
    AWAIT = auto()     # await expr
    AS = auto()        # as (import 别名)
    PERF = auto()      # @perf 性能注解
    # ── v3.3.0 增量计算 ──
    SOURCE = auto()    # source(...) 可变增量源
    LIVE = auto()      # live { ... } 活计算块
    TRANSACT = auto()  # transact { ... } 批量事务
    PURE = auto()      # extern "C" { pure fn ... } 纯函数标注

    # 运算符
    PLUS = auto()      # +
    MINUS = auto()     # -
    STAR = auto()      # *
    SLASH = auto()     # /
    PERCENT = auto()   # %
    POWER = auto()     # **
    
    # 比较
    EQ = auto()        # ==
    NE = auto()        # !=
    LT = auto()        # <
    LE = auto()        # <=
    GT = auto()        # >
    GE = auto()        # >=
    
    # 逻辑
    AND = auto()       # &&
    OR = auto()        # ||
    NOT = auto()       # !
    
    # 赋值
    ASSIGN = auto()    # =
    PLUS_EQ = auto()   # +=
    MINUS_EQ = auto()  # -=
    STAR_EQ = auto()   # *=
    SLASH_EQ = auto()  # /=

    # 位运算
    SHIFT_LEFT = auto()   # <<
    SHIFT_RIGHT = auto()  # >>
    CARET = auto()        # ^ (异或)
    
    # 箭头与通道
    ARROW = auto()     # ->
    FAT_ARROW = auto() # =>
    CHANNEL_SEND = auto()  # <-
    PIPE_OP = auto()   # |> (管道)
    RANGE = auto()     # .. (区间)
    VARIADIC = auto()  # ... (可变参数)
    
    # 引用
    AMP = auto()       # &
    AMP_MUT = auto()   # &mut (特殊处理)
    QUESTION = auto()  # ? (错误传播)
    OPTIONAL_DOT = auto()  # ?. (可选链, nil 安全访问)
    NULL_COALESCE = auto() # ?? (空合并, 左侧 nil 时取右侧)
    
    # 分隔符
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    LBRACE = auto()    # {
    RBRACE = auto()    # }
    COMMA = auto()     # ,
    COLON = auto()     # :
    SEMICOLON = auto() # ; (可选)
    DOT = auto()       # .
    PIPE = auto()      # | (lambda)
    
    # 特殊
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    COMMENT = auto()
    AT = auto()        # @ (性能注解前缀)
    POUND = auto()     # # (属性前缀 #[...])


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"


# 关键字映射
KEYWORDS = {
    'let': TokenType.LET,
    'var': TokenType.VAR,
    'const': TokenType.CONST,
    'fn': TokenType.FN,
    'return': TokenType.RETURN,
    'if': TokenType.IF,
    'elif': TokenType.ELIF,
    'else': TokenType.ELSE,
    'for': TokenType.FOR,
    'while': TokenType.WHILE,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'match': TokenType.MATCH,
    'type': TokenType.TYPE,
    'struct': TokenType.STRUCT,
    'enum': TokenType.ENUM,
    'trait': TokenType.TRAIT,
    'impl': TokenType.IMPL,
    'import': TokenType.IMPORT,
    'from': TokenType.FROM,
    'pub': TokenType.PUB,
    'mut': TokenType.MUT,
    'spawn': TokenType.SPAWN,
    'select': TokenType.SELECT,
    'try': TokenType.TRY,
    'catch': TokenType.CATCH,
    'finally': TokenType.FINALLY,
    'test': TokenType.TEST,
    'assert': TokenType.ASSERT,
    'defer': TokenType.DEFER,
    'yield': TokenType.YIELD,
    'extern': TokenType.EXTERN,
    'unsafe': TokenType.UNSAFE,
    'async': TokenType.ASYNC,
    'await': TokenType.AWAIT,
    'as': TokenType.AS,
    'perf': TokenType.PERF,
    'true': TokenType.BOOLEAN,
    'false': TokenType.BOOLEAN,
    'nil': TokenType.NIL,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'source': TokenType.SOURCE,
    'live': TokenType.LIVE,
    'transact': TokenType.TRANSACT,
    'pure': TokenType.PURE,
}
