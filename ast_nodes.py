"""Aurora 抽象语法树（AST）节点定义"""

from dataclasses import dataclass, field
from typing import List, Optional, Union


# ============================================================
# 基础节点
# ============================================================

@dataclass
class Node:
    """所有 AST 节点的基类"""
    line: int = 0
    column: int = 0


# ============================================================
# 类型表达式
# ============================================================

@dataclass
class TypeNode(Node):
    """类型节点基类"""
    pass


@dataclass
class NamedType(TypeNode):
    """命名类型，如 int, str, float"""
    name: str = ""


@dataclass
class ArrayType(TypeNode):
    """数组类型，如 [int], [str]"""
    element_type: TypeNode = None


@dataclass
class MapType(TypeNode):
    """映射类型，如 map<str, int>"""
    key_type: TypeNode = None
    value_type: TypeNode = None


@dataclass
class TupleType(TypeNode):
    """元组类型，如 (int, str)"""
    element_types: List[TypeNode] = field(default_factory=list)


@dataclass
class FunctionType(TypeNode):
    """函数类型，如 (int) -> str"""
    param_types: List[TypeNode] = field(default_factory=list)
    return_type: TypeNode = None


@dataclass
class GenericType(TypeNode):
    """泛型类型，如 Result<T>"""
    base: str = ""
    type_args: List[TypeNode] = field(default_factory=list)


@dataclass
class UnionType(TypeNode):
    """联合类型，如 Ok<T> | Err<str>"""
    variants: List[TypeNode] = field(default_factory=list)


@dataclass
class RefType(TypeNode):
    """引用类型，如 &int, &mut [int]"""
    inner: TypeNode = None
    mutable: bool = False


# ============================================================
# 表达式
# ============================================================

@dataclass
class Expr(Node):
    """表达式节点基类"""
    inferred_type: Optional[TypeNode] = None  # 类型推断结果


@dataclass
class IntLiteral(Expr):
    value: int = 0


@dataclass
class FloatLiteral(Expr):
    value: float = 0.0


@dataclass
class StringLiteral(Expr):
    value: str = ""
    raw: bool = False  # 原始字符串:不做插值、不处理转义


@dataclass
class BoolLiteral(Expr):
    value: bool = False


@dataclass
class NilLiteral(Expr):
    pass


@dataclass
class Identifier(Expr):
    name: str = ""


@dataclass
class ArrayLiteral(Expr):
    elements: List[Expr] = field(default_factory=list)


@dataclass
class MapLiteral(Expr):
    entries: List[tuple] = field(default_factory=list)  # [(key, value), ...]


@dataclass
class TupleLiteral(Expr):
    elements: List[Expr] = field(default_factory=list)


@dataclass
class BinaryOp(Expr):
    left: Expr = None
    op: str = ""
    right: Expr = None


@dataclass
class RangeExpr(Expr):
    """区间 a..b(闭区间,含 b)"""
    start: Expr = None
    end: Expr = None


@dataclass
class PipeExpr(Expr):
    """管道 x |> f / x |> f(args):左侧值作为最后一个参数传给右侧调用"""
    left: Expr = None
    call: Expr = None


@dataclass
class UnaryOp(Expr):
    op: str = ""
    operand: Expr = None


@dataclass
class CallExpr(Expr):
    """函数调用：func(args...)，支持命名参数 func(name: value)"""
    callee: Expr = None
    args: List[Expr] = field(default_factory=list)
    named_args: List[tuple] = field(default_factory=list)  # [(name, expr), ...]


@dataclass
class MethodCall(Expr):
    """方法调用：obj.method(args...)，支持命名参数"""
    object: Expr = None
    method: str = ""
    args: List[Expr] = field(default_factory=list)
    named_args: List[tuple] = field(default_factory=list)


@dataclass
class MemberAccess(Expr):
    """成员访问：obj.field"""
    object: Expr = None
    member: str = ""


@dataclass
class IndexAccess(Expr):
    """索引访问：arr[i], map[key]"""
    object: Expr = None
    index: Expr = None


@dataclass
class LambdaExpr(Expr):
    """Lambda 表达式：|params| -> type { body }"""
    params: List['Param'] = field(default_factory=list)
    return_type: Optional[TypeNode] = None
    body: 'Block' = None
    is_expression: bool = True  # |x| x * 2 形式


@dataclass
class IfExpr(Expr):
    """if 表达式（可作为值）"""
    condition: Expr = None
    then_body: 'Block' = None
    elif_clauses: List[tuple] = field(default_factory=list)  # [(cond, body), ...]
    else_body: Optional['Block'] = None


@dataclass
class MatchExpr(Expr):
    """模式匹配表达式"""
    subject: Expr = None
    arms: List['MatchArm'] = field(default_factory=list)


@dataclass
class SpawnExpr(Expr):
    """spawn 表达式，启动协程"""
    call: Expr = None


@dataclass
class ChannelSend(Expr):
    """通道发送：ch <- value"""
    channel: Expr = None
    value: Expr = None


@dataclass
class ChannelRecv(Expr):
    """通道接收：<-ch"""
    channel: Expr = None


@dataclass
class SelectExpr(Expr):
    """select 多路复用"""
    arms: List['SelectArm'] = field(default_factory=list)


@dataclass
class TryExpr(Expr):
    """? 错误传播"""
    expr: Expr = None


@dataclass
class OptionalAccess(Expr):
    """可选链访问：obj?.member（obj 为 nil 时结果为 nil）"""
    object: Expr = None
    member: str = None


@dataclass
class OptionalCall(Expr):
    """可选链方法调用：obj?.method(args)（obj 为 nil 时结果为 nil）"""
    object: Expr = None
    method: str = None
    args: List['Expr'] = field(default_factory=list)
    named_args: List[tuple] = field(default_factory=list)


@dataclass
class NullCoalesce(Expr):
    """空合并：left ?? right（left 为 nil 时取 right）"""
    left: Expr = None
    right: Expr = None


@dataclass
class RefExpr(Expr):
    """引用表达式：&x, &mut x"""
    inner: Expr = None
    mutable: bool = False


@dataclass
class DerefExpr(Expr):
    """解引用表达式：*x"""
    inner: Expr = None


@dataclass
class StringInterpolation(Expr):
    """字符串插值："hello {name}" """
    parts: List[Expr] = field(default_factory=list)


# ============================================================
# 模式（用于 match）
# ============================================================

@dataclass
class Pattern(Node):
    pass


@dataclass
class LiteralPattern(Pattern):
    value: Expr = None


@dataclass
class BindPattern(Pattern):
    """绑定模式：x => ..."""
    name: str = ""


@dataclass
class ConstructorPattern(Pattern):
    """构造器模式：Ok(val), Err(msg)"""
    name: str = ""
    fields: List[Pattern] = field(default_factory=list)


@dataclass
class WildcardPattern(Pattern):
    """通配符：_"""
    pass


@dataclass
class MatchArm(Node):
    pattern: Pattern = None
    body: Expr = None


@dataclass
class SelectArm(Node):
    channel_expr: Expr = None
    bind_name: Optional[str] = None
    body: 'Block' = None
    is_default: bool = False


# ============================================================
# 语句
# ============================================================

@dataclass
class Stmt(Node):
    pass


@dataclass
class Block(Node):
    statements: List[Stmt] = field(default_factory=list)


@dataclass
class LetStmt(Stmt):
    """变量声明：let x = expr 或 let x: Type = expr"""
    name: str = ""
    mutable: bool = False  # let 不可变;var 可变
    type_annotation: Optional[TypeNode] = None
    initializer: Optional[Expr] = None


@dataclass
class DestructureLet(Stmt):
    """模式解构绑定：let (a, b) = expr / let [a, b] = expr"""
    names: List[str] = field(default_factory=list)
    mutable: bool = False
    initializer: Expr = None


@dataclass
class ConstStmt(Stmt):
    """常量声明：const X = expr"""
    name: str = ""
    type_annotation: Optional[TypeNode] = None
    initializer: Expr = None


@dataclass
class ExprStmt(Stmt):
    """表达式语句"""
    expr: Expr = None


@dataclass
class ReturnStmt(Stmt):
    value: Optional[Expr] = None


@dataclass
class DeferStmt(Stmt):
    """defer:函数退出时(LIFO)执行"""
    expr: Optional[Expr] = None
    body: Optional[Block] = None


@dataclass
class YieldStmt(Stmt):
    """yield:生成器收集一个值(调用函数返回收集列表)"""
    value: Expr = None


@dataclass
class BreakStmt(Stmt):
    pass


@dataclass
class ContinueStmt(Stmt):
    pass


@dataclass
class IfStmt(Stmt):
    condition: Expr = None
    then_body: Block = None
    elif_clauses: List[tuple] = field(default_factory=list)
    else_body: Optional[Block] = None


@dataclass
class ForStmt(Stmt):
    """for 循环"""
    variables: List[str] = field(default_factory=list)  # 支持 for key, value in ...
    iterable: Expr = None
    body: Block = None


@dataclass
class WhileStmt(Stmt):
    condition: Expr = None
    body: Block = None


@dataclass
class MatchStmt(Stmt):
    subject: Expr = None
    arms: List[MatchArm] = field(default_factory=list)


@dataclass
class TryStmt(Stmt):
    """try-catch-finally"""
    body: Block = None
    catches: List['CatchClause'] = field(default_factory=list)
    finally_body: Optional[Block] = None


@dataclass
class CatchClause(Node):
    name: str = ""
    error_type: Optional[TypeNode] = None
    body: Block = None


@dataclass
class SpawnStmt(Stmt):
    """spawn 语句"""
    call: Expr = None


@dataclass
class SelectStmt(Stmt):
    """select 语句"""
    arms: List[SelectArm] = field(default_factory=list)


@dataclass
class AssignStmt(Stmt):
    """赋值语句：target = value"""
    target: Expr = None
    value: Expr = None
    op: str = "="  # =, +=, -=, *=, /=


# ============================================================
# 定义
# ============================================================

@dataclass
class Param(Node):
    """函数参数"""
    name: str = ""
    type_annotation: Optional[TypeNode] = None
    default_value: Optional[Expr] = None


@dataclass
class FnDef(Stmt):
    """函数定义"""
    name: str = ""
    params: List[Param] = field(default_factory=list)
    return_type: Optional[TypeNode] = None
    body: Block = None
    is_pub: bool = False
    is_test: bool = False


@dataclass
class TypeDef(Stmt):
    """自定义类型定义"""
    name: str = ""
    fields: List[tuple] = field(default_factory=list)  # [(name, type, optional_default), ...]
    is_pub: bool = False
    type_params: List[str] = field(default_factory=list)  # 泛型参数


@dataclass
class EnumDef(Stmt):
    """枚举定义"""
    name: str = ""
    variants: List['EnumVariant'] = field(default_factory=list)
    is_pub: bool = False
    type_params: List[str] = field(default_factory=list)


@dataclass
class EnumVariant(Node):
    name: str = ""
    fields: List[tuple] = field(default_factory=list)  # [(name, type), ...]


@dataclass
class TraitDef(Stmt):
    """trait 定义（类似 Rust trait / Go interface）"""
    name: str = ""
    methods: List['FnDef'] = field(default_factory=list)
    is_pub: bool = False


@dataclass
class ImplBlock(Stmt):
    """impl 实现块"""
    trait_name: Optional[str] = None
    type_name: str = ""
    methods: List[FnDef] = field(default_factory=list)


@dataclass
class ImportStmt(Stmt):
    """导入语句"""
    path: List[str] = field(default_factory=list)  # import net.http
    alias: Optional[str] = None                    # as http
    names: List[str] = field(default_factory=list)  # from x import a, b


@dataclass
class TestBlock(Stmt):
    """测试块"""
    name: str = ""
    body: Block = None


# ============================================================
# 顶层
# ============================================================

@dataclass
class Program(Node):
    """程序顶层节点"""
    statements: List[Stmt] = field(default_factory=list)
