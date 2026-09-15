"""Aurora v2.1.0 六大新特性测试 — 泛型/模式匹配/解构元组/推导式管道/可选空安全/struct命名参数"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora.lexer import Lexer
from aurora.parser import Parser
from aurora.interpreter import Interpreter, AuroraError


def run_source(src):
    tokens = Lexer(src).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    interp.run(program)
    return interp


def last_result(src):
    tokens = Lexer(src).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    interp.run(program)
    from aurora.ast_nodes import ExprStmt
    for stmt in reversed(program.statements):
        if isinstance(stmt, ExprStmt):
            return interp._eval(stmt.expr, interp.global_env)
    return None


# ============================================================
# 1. 泛型系统
# ============================================================
class TestGenerics(unittest.TestCase):
    def test_generic_function_map(self):
        src = '''
fn map<T, U>(arr, f) {
    var result = []
    for x in arr {
        result.append(f(x))
    }
    result
}
map([1, 2, 3], fn x => x * 2)
'''
        self.assertEqual(last_result(src), [2, 4, 6])

    def test_generic_function_identity(self):
        src = '''
fn identity<T>(x: T) -> T {
    x
}
identity(42)
'''
        self.assertEqual(last_result(src), 42)

    def test_generic_struct(self):
        src = '''
struct Pair<T> { first: T, second: T }
let p = Pair { first: 10, second: 20 }
p.first + p.second
'''
        self.assertEqual(last_result(src), 30)

    def test_generic_function_filter(self):
        src = '''
fn filter<T>(arr, pred) {
    var result = []
    for x in arr {
        if pred(x) {
            result.append(x)
        }
    }
    result
}
filter([1, 2, 3, 4, 5], fn x => x % 2 == 0)
'''
        self.assertEqual(last_result(src), [2, 4])

    def test_generic_enum(self):
        src = '''
enum Option<T> { Some(value: T), None() }
let v = Option.Some(value: 42)
let r = match v {
    Some(x) => x,
    None() => 0
}
r
'''
        self.assertEqual(last_result(src), 42)


# ============================================================
# 2. 模式匹配 + 代数数据类型
# ============================================================
class TestPatternMatching(unittest.TestCase):
    def test_enum_payload_match(self):
        src = '''
enum Shape { Circle(radius: float), Rect(w: float, h: float), Square(side: float) }
fn area(shape) {
    let r = match shape {
        Circle(r) => 3.14 * r * r,
        Rect(w, h) => w * h,
        Square(s) => s * s
    }
    r
}
area(Shape.Circle(radius: 2.0))
'''
        result = last_result(src)
        self.assertAlmostEqual(result, 12.56, places=1)

    def test_enum_struct_variant(self):
        src = '''
enum Shape { Circle(radius: float), Point { x: float, y: float } }
let p = Shape.Point(x: 1.0, y: 2.0)
let r = match p {
    Circle(r) => r,
    Point(x, y) => x + y
}
r
'''
        self.assertEqual(last_result(src), 3.0)

    def test_literal_pattern(self):
        src = '''
fn describe(x) {
    let r = match x {
        0 => "zero",
        1 => "one",
        _ => "other"
    }
    r
}
describe(1)
'''
        self.assertEqual(last_result(src), "one")

    def test_wildcard_pattern(self):
        src = '''
fn check(x) {
    let r = match x {
        42 => "answer",
        _ => "unknown"
    }
    r
}
check(99)
'''
        self.assertEqual(last_result(src), "unknown")

    def test_tuple_pattern_match(self):
        src = '''
let pair = (3, 4)
let r = match pair {
    (0, 0) => "origin",
    (x, 0) => "x-axis",
    (0, y) => "y-axis",
    (x, y) => x + y
}
r
'''
        self.assertEqual(last_result(src), 7)

    def test_struct_pattern_match(self):
        src = '''
struct Point { x: int, y: int }
let p = Point { x: 5, y: 12 }
let r = match p {
    Point { x: 0, y: 0 } => "origin",
    Point { x: a, y: b } => a + b
}
r
'''
        self.assertEqual(last_result(src), 17)

    def test_match_as_expression(self):
        src = '''
let x = 3
let result = match x {
    1 => "one",
    2 => "two",
    _ => "many"
}
result
'''
        self.assertEqual(last_result(src), "many")

    def test_nil_pattern_match(self):
        src = '''
fn unwrap_or(opt, default) {
    let r = match opt {
        nil => default,
        x => x
    }
    r
}
unwrap_or(nil, 42)
'''
        self.assertEqual(last_result(src), 42)


# ============================================================
# 3. 解构赋值 + 元组
# ============================================================
class TestDestructureAndTuples(unittest.TestCase):
    def test_tuple_literal(self):
        self.assertEqual(last_result('(1, "hello", 3.14)'), (1, "hello", 3.14))

    def test_tuple_index(self):
        src = '''
let tup = (10, 20, 30)
tup.0 + tup.1 + tup.2
'''
        self.assertEqual(last_result(src), 60)

    def test_destructure_let(self):
        src = '''
let (a, b, c) = (1, 2, 3)
a + b + c
'''
        self.assertEqual(last_result(src), 6)

    def test_nested_destructure(self):
        src = '''
let (x, (y, z)) = (1, (2, 3))
x + y + z
'''
        self.assertEqual(last_result(src), 6)

    def test_swap_variables(self):
        src = '''
var a = 1
var b = 2
a, b = b, a
a * 10 + b
'''
        self.assertEqual(last_result(src), 21)

    def test_function_return_tuple(self):
        src = '''
fn divmod(a, b) {
    (int(a / b), a % b)
}
let (q, r) = divmod(17, 5)
q * 10 + r
'''
        self.assertEqual(last_result(src), 32)

    def test_tuple_in_array(self):
        src = '''
let points = [(1, 2), (3, 4), (5, 6)]
points[1].0 + points[1].1
'''
        self.assertEqual(last_result(src), 7)


# ============================================================
# 4. 列表推导式 + 管道运算符
# ============================================================
class TestComprehensionsAndPipe(unittest.TestCase):
    def test_list_comprehension_basic(self):
        self.assertEqual(last_result('[x * 2 for x in [1, 2, 3]]'), [2, 4, 6])

    def test_list_comprehension_with_filter(self):
        self.assertEqual(
            last_result('[x * x for x in [1, 2, 3, 4, 5] if x % 2 == 0]'),
            [4, 16]
        )

    def test_set_comprehension(self):
        result = last_result('{x % 3 for x in [1, 2, 3, 4, 5]}')
        self.assertEqual(result, {0, 1, 2})

    def test_map_comprehension(self):
        result = last_result('{k: k * 2 for k in [1, 2, 3]}')
        self.assertEqual(result, {1: 2, 2: 4, 3: 6})

    def test_nested_comprehension(self):
        result = last_result('[a + b for a in [1, 2] for b in [10, 20]]')
        self.assertEqual(result, [11, 21, 12, 22])

    def test_pipe_operator(self):
        src = '''
fn double(x) { x * 2 }
fn add_one(x) { x + 1 }
5 |> double |> add_one
'''
        self.assertEqual(last_result(src), 11)

    def test_pipe_with_function_call(self):
        src = '''
[3, 1, 4, 1, 5] |> sorted |> len
'''
        self.assertEqual(last_result(src), 5)

    def test_lambda_shorthand(self):
        src = '''
let f = fn x => x * x
f(5)
'''
        self.assertEqual(last_result(src), 25)

    def test_lambda_shorthand_in_call(self):
        src = '''
fn apply(f, arr) {
    var r = []
    for x in arr { r.append(f(x)) }
    r
}
apply(fn x => x + 10, [1, 2, 3])
'''
        self.assertEqual(last_result(src), [11, 12, 13])

    def test_comprehension_with_pipe(self):
        src = '''
[x for x in 1..5] |> len
'''
        self.assertEqual(last_result(src), 5)


# ============================================================
# 5. 可选类型 + 空安全
# ============================================================
class TestOptionalAndNullSafety(unittest.TestCase):
    def test_optional_access_with_nil(self):
        src = '''
let obj = nil
obj?.name
'''
        self.assertIsNone(last_result(src))

    def test_optional_access_with_value(self):
        src = '''
struct User { name: str }
let user = User { name: "Alice" }
user?.name
'''
        self.assertEqual(last_result(src), "Alice")

    def test_null_coalesce_left_value(self):
        self.assertEqual(last_result('"hello" ?? "default"'), "hello")

    def test_null_coalesce_left_nil(self):
        self.assertEqual(last_result('nil ?? "default"'), "default")

    def test_forced_unwrap_value(self):
        src = '''
let x = "hello"
x!
'''
        self.assertEqual(last_result(src), "hello")

    def test_forced_unwrap_nil_panics(self):
        with self.assertRaises(AuroraError):
            last_result('nil!')

    def test_optional_chain(self):
        src = '''
struct Address { city: str }
struct User { name: str, address: Address }
let user = User { name: "Bob", address: Address { city: "NYC" } }
user?.address?.city
'''
        self.assertEqual(last_result(src), "NYC")

    def test_optional_chain_nil(self):
        src = '''
struct User { name: str, address: any }
let user = User { name: "Bob", address: nil }
user?.address?.city
'''
        self.assertIsNone(last_result(src))

    def test_null_coalesce_chain(self):
        src = '''
let x = nil
let y = nil
let z = "found"
x ?? y ?? z
'''
        self.assertEqual(last_result(src), "found")


# ============================================================
# 6. struct 数据类 + 命名参数/默认参数
# ============================================================
class TestStructAndNamedParams(unittest.TestCase):
    def test_struct_literal(self):
        src = '''
struct User { name: str, age: int }
let u = User { name: "Alice", age: 30 }
u.name
'''
        self.assertEqual(last_result(src), "Alice")

    def test_struct_default_field(self):
        src = '''
struct User { name: str, age: int = 0, active: bool = true }
let u = User { name: "Bob" }
u.age
'''
        self.assertEqual(last_result(src), 0)

    def test_struct_default_field_override(self):
        src = '''
struct User { name: str, age: int = 0, active: bool = true }
let u = User { name: "Carol", age: 25 }
u.age
'''
        self.assertEqual(last_result(src), 25)

    def test_named_params_function(self):
        src = '''
fn greet(name: str, greeting: str = "Hello") {
    greeting + ", " + name
}
greet(name: "Alice", greeting: "Hi")
'''
        self.assertEqual(last_result(src), "Hi, Alice")

    def test_default_params_function(self):
        src = '''
fn add(a, b = 1) {
    a + b
}
add(5)
'''
        self.assertEqual(last_result(src), 6)

    def test_variadic_params(self):
        src = '''
fn sum(...nums) {
    var total = 0
    for n in nums {
        total = total + n
    }
    total
}
sum(1, 2, 3, 4, 5)
'''
        self.assertEqual(last_result(src), 15)

    def test_variadic_with_fixed(self):
        src = '''
fn make_list(separator, ...parts) {
    parts
}
make_list(", ", "a", "b", "c")
'''
        self.assertEqual(last_result(src), ["a", "b", "c"])

    def test_struct_keyword_alias(self):
        src = '''
type Point { x: int, y: int }
let p = Point { x: 1, y: 2 }
p.x + p.y
'''
        self.assertEqual(last_result(src), 3)

    def test_struct_field_access(self):
        src = '''
struct Config { host: str = "localhost", port: int = 8080 }
let c = Config { host: "0.0.0.0" }
c.host
'''
        self.assertEqual(last_result(src), "0.0.0.0")


# ============================================================
# 集成测试：多特性组合
# ============================================================
class TestIntegration(unittest.TestCase):
    def test_generics_with_comprehensions(self):
        src = '''
fn transform<T, U>(arr, f) {
    [f(x) for x in arr]
}
transform([1, 2, 3], fn x => x * 10)
'''
        self.assertEqual(last_result(src), [10, 20, 30])

    def test_pattern_match_with_option(self):
        src = '''
fn unwrap_or(opt, default) {
    let r = match opt {
        nil => default,
        x => x
    }
    r
}
unwrap_or(nil, 42)
'''
        self.assertEqual(last_result(src), 42)

    def test_struct_with_pattern_match(self):
        src = '''
struct Point { x: int, y: int }
fn distance_from_origin(p) {
    let r = match p {
        Point { x: 0, y: 0 } => 0,
        Point { x: a, y: b } => a + b
    }
    r
}
distance_from_origin(Point { x: 3, y: 4 })
'''
        self.assertEqual(last_result(src), 7)

    def test_optional_with_comprehension(self):
        src = '''
struct User { name: str }
let users = [User { name: "Alice" }, nil, User { name: "Bob" }]
[u?.name for u in users if u != nil]
'''
        self.assertEqual(last_result(src), ["Alice", "Bob"])

    def test_named_params_with_defaults(self):
        src = '''
fn create_user(name, age = 18) {
    struct User { name: str, age: int }
    User { name: name, age: age }
}
let u = create_user(name: "Eve")
u.age
'''
        self.assertEqual(last_result(src), 18)

    def test_enum_with_generics_and_match(self):
        src = '''
enum Result<T, E> { Ok(value: T), Err(error: E) }
fn handle(r) {
    let msg = match r {
        Ok(v) => "success: " + v,
        Err(e) => "error: " + e
    }
    msg
}
handle(Result.Ok(value: "data"))
'''
        self.assertEqual(last_result(src), "success: data")

    def test_all_features_together(self):
        src = '''
struct Item { name: str, price: float = 0.0 }

fn total_price(...items) {
    var total = 0.0
    for item in items {
        total = total + item.price
    }
    total
}

let cart = [
    Item { name: "Phone", price: 699.0 },
    Item { name: "Book", price: 19.0 },
    Item { name: "Free" }
]

let expensive = [item.name for item in cart if item.price > 50]
expensive[0]
'''
        self.assertEqual(last_result(src), "Phone")

    def test_pipe_chain_with_lambda(self):
        src = '''
fn my_filter(pred, arr) {
    [x for x in arr if pred(x)]
}
fn my_map(f, arr) {
    [f(x) for x in arr]
}
[1, 2, 3, 4, 5] |> my_filter(fn x => x % 2 == 0) |> my_map(fn x => x * 10)
'''
        self.assertEqual(last_result(src), [20, 40])

    def test_struct_default_with_match(self):
        src = '''
struct Config { host: str = "localhost", port: int = 8080, debug: bool = false }
fn describe(c) {
    let r = match c.debug {
        true => c.host + " (debug)",
        false => c.host
    }
    r
}
describe(Config { host: "example.com" })
'''
        self.assertEqual(last_result(src), "example.com")

    def test_comprehension_with_destructure(self):
        src = '''
let pairs = [(1, 2), (3, 4), (5, 6)]
var sums = []
for (a, b) in pairs {
    sums.append(a + b)
}
sums
'''
        self.assertEqual(last_result(src), [3, 7, 11])


if __name__ == '__main__':
    unittest.main()
