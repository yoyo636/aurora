# -*- coding: utf-8 -*-
"""Aurora 教学课程数据 —— 8 章渐进式课程,覆盖输入输出、函数、递归、DFS 等。

每节结构:
  id         唯一标识
  chapter    章名
  title      节标题
  objective  讲解正文(支持 ``` 代码块,其余为段落)
  example    可运行示例代码
  exercise   练习 { task, hint, solution, expected }
  concepts   概念标签
"""

LESSONS = [
    # ───────────────────────── 第 1 章 ─────────────────────────
    {
        "id": "l01_hello",
        "chapter": "第 1 章 · 从输出开始",
        "title": "你好,Aurora",
        "objective": [
            "每一个程序员的第一行代码,都是从『向世界打个招呼』开始的。Aurora 用 `println(内容)` 输出一行文字。",
            "```\nprintln(\"你好,Aurora!\")\n```",
            "字符串要放在双引号 `\"` 里。`println` 会自动在结尾换行;不想换行可以用 `print`。",
            "更强大的技巧是**字符串插值**:把变量或表达式用 `{ }` 包起来,直接嵌入字符串。",
            "```\nlet name = \"小明\"\nlet score = 95\nprintln(\"你好,{name},你得了 {score} 分\")\n```",
            "试试运行下面的示例,然后修改它输出你自己的问候语。",
        ],
        "example": 'println("Hello, Aurora!")\nprintln("这是你的第一行代码")\nlet name = "学习者"\nlet score = 100\nprintln("欢迎,{name}! 练习 +{score} 分")',
        "exercise": {
            "task": "输出两行文字:第一行是你的名字,第二行用插值输出『我 2026 岁』(用变量 age=2026)。",
            "hint": "let age = 2026 后,写 println(\"我 {age} 岁\")。注意中文引号要用英文的。",
            "solution": 'let age = 2026\nprintln("我叫 Aurora")\nprintln("我 {age} 岁")',
            "expected": None,
        },
        "concepts": ["println", "字符串", "插值"],
    },
    # ───────────────────────── 第 2 章 ─────────────────────────
    {
        "id": "l02_vars_input",
        "chapter": "第 2 章 · 变量与输入输出",
        "title": "变量、类型与键盘输入",
        "objective": [
            "`let 名字 = 值` 定义变量。Aurora 能自动推断类型,常用类型有:`int`(整数)、`float`(小数)、`str`(字符串)、`bool`(布尔 true/false)。",
            "```\nlet a: int = 10\nlet pi: float = 3.14\nlet ok: bool = true\n```",
            "程序要和人交互,就需要**输入**。Aurora 提供了像 C 语言 scanf 一样的读取函数:",
            "```\nlet name = read_line(\"请输入名字: \")\nlet age  = read_int(\"请输入年龄: \")\nprintln(\"{name} 明年 {age + 1} 岁\")\n```",
            "`read_int` 读整数、`read_float` 读小数、`read_line` 读整行文本。注意:程序运行时,要把输入内容填写在右侧的『程序输入』框里,一行一个。",
            "在 WebUI 里运行这个示例时,先在右侧输入框里填写 `小明` 和 `12`(各占一行),再点运行。",
        ],
        "example": 'let name = read_line("你的名字: ")\nlet age = read_int("你的年龄: ")\nlet height = read_float("你的身高: ")\nprintln("你好,{name}!")\nprintln("明年你 {age + 1} 岁,身高 {height} 米")',
        "exercise": {
            "task": "读取两个整数 a 和 b,输出它们的和与平均值。输入为 10 和 4,应输出 sum=14 与 avg=7。",
            "hint": "avg = (a + b) / 2 结果是 float,println 会自动转换。",
            "solution": "let a = read_int()\nlet b = read_int()\nlet sum = a + b\nlet avg = (a + b) / 2\nprintln(\"sum={sum}, avg={avg}\")",
            "expected": "sum=14, avg=7.0",
        },
        "concepts": ["let", "int/float/str", "read_int", "read_line"],
    },
    # ───────────────────────── 第 3 章 ─────────────────────────
    {
        "id": "l03_condition_loop",
        "chapter": "第 3 章 · 逻辑与流程控制",
        "title": "条件判断与循环",
        "objective": [
            "程序的核心能力是**做决定**和**重复执行**。`if / else if / else` 做条件判断,`for` 和 `while` 做循环。",
            "```\nlet score = read_int(\"分数: \")\nif score >= 90 {\n    println(\"优秀\")\n} else if score >= 60 {\n    println(\"及格\")\n} else {\n    println(\"不及格\")\n}\n```",
            "`for i in range(n)` 循环 n 次,`for x in 数组` 遍历元素,`while 条件` 在条件为真时持续执行。",
            "```\nlet total = 0\nfor i in range(5) { total = total + i }   // 0+1+2+3+4=10\nprintln(total)\n```",
            "循环里可以 `break` 提前结束,`continue` 跳到下一次。这和 C 语言完全一致。",
        ],
        "example": 'let total = 0\nfor i in range(1, 11) { total = total + i }\nprintln("1..10 的和 = {total}")\n\nlet n = 5\nlet fact = 1\nwhile n > 1 { fact = fact * n; n = n - 1 }\nprintln("5! = {fact}")',
        "exercise": {
            "task": "打印 1 到 20 之间所有 3 的倍数(每个占一行)。",
            "hint": "for i in range(1, 21) { if i % 3 == 0 { println(i) } }",
            "solution": "for i in range(1, 21) {\n    if i % 3 == 0 {\n        println(i)\n    }\n}",
            "expected": "3\n6\n9\n12\n15\n18",
        },
        "concepts": ["if", "for", "while", "range", "break/continue"],
    },
    # ───────────────────────── 第 4 章 ─────────────────────────
    {
        "id": "l04_functions",
        "chapter": "第 4 章 · 函数",
        "title": "函数:把代码组织成积木",
        "objective": [
            "函数是组织代码的积木。用 `fn 名字(参数) -> 返回类型 { ... }` 定义,用 `return` 返回结果。",
            "```\nfn add(a: int, b: int) -> int {\n    return a + b\n}\nprintln(add(3, 5))    // 8\n```",
            "参数可以有**默认值**,调用时可以省略;也可以使用**命名参数**,让调用更清晰。",
            "```\nfn greet(name: str, prefix: str = \"你好\") -> str {\n    return prefix + \", \" + name\n}\nprintln(greet(\"小明\"))            // 你好, 小明\nprintln(greet(\"小红\", prefix: \"晚上好\"))\n```",
            "Aurora 还支持**匿名函数(λambda)**:`|参数| 表达式`。它常和集合方法一起用:",
            "```\nlet squares = [1, 2, 3, 4].map(|x| x * x)\nprintln(squares)      // [1, 4, 9, 16]\n```",
            "函数是递归的基础——下一章我们就要用它做深度优先搜索了。",
        ],
        "example": 'fn fib(n: int) -> int {\n    if n <= 1 { return n }\n    return fib(n - 1) + fib(n - 2)\n}\n\nfor i in range(10) { println("fib({i}) = {fib(i)}") }',
        "exercise": {
            "task": "写一个函数 is_prime(n) 判断质数,并打印 2 到 30 之间的所有质数。",
            "hint": "质数:大于 1 且只能被 1 和自身整除。for i in range(2, n) 里若 n % i == 0 则不是质数。",
            "solution": "fn is_prime(n: int) -> bool {\n    if n < 2 { return false }\n    for i in range(2, n) {\n        if n % i == 0 { return false }\n    }\n    return true\n}\n\nfor n in range(2, 31) {\n    if is_prime(n) { println(n) }\n}",
            "expected": "2\n3\n5\n7\n11\n13\n17\n19\n23\n29",
        },
        "concepts": ["fn", "return", "默认参数", "命名参数", "lambda"],
    },
    # ───────────────────────── 第 5 章 ─────────────────────────
    {
        "id": "l05_collections",
        "chapter": "第 5 章 · 数组与字典",
        "title": "数组与字典:批量数据",
        "objective": [
            "数组 `[1, 2, 3]` 存有序列表,字典 `{\"键\": 值}` 存键值对。它们和 C 的数组、结构体一样,是组织数据的基础。",
            "```\nlet nums = [10, 20, 30]\nprintln(nums[0])          // 10\nnums.push(40)             // 追加\nprintln(nums.len())       // 4\n```",
            "字典用 `{ }` 创建,用键取值、修改、添加:",
            "```\nlet scores = {\"语文\": 90, \"数学\": 85}\nscores[\"英语\"] = 88\nprintln(scores[\"数学\"])\n```",
            "集合方法让数据处理很优雅:`map`(映射)、`filter`(过滤)、`reduce`(归约)、`contains`(包含)、`sort`(排序)。",
            "```\nlet nums = [5, 1, 4, 2, 3]\nlet evens = nums.filter(|x| x % 2 == 0)     // [4, 2]\nlet total = nums.reduce(0, |acc, x| acc + x)  // 15\nprintln(nums.sort())\n```",
            "字符串也是『字符数组』,支持下标、切片和 `.len()`、`.upper()`、`.split()` 等方法。",
        ],
        "example": 'let scores = {"语文": 90, "数学": 85, "英语": 88}\nlet total = 0\nlet names = scores.keys()\nfor k in names { total = total + scores[k] }\nprintln("平均分 = {total / scores.len()}")\n\nlet words = "aurora is a language".split(" ")\nprintln(words)\nprintln(words.map(|w| w.upper()))',
        "exercise": {
            "task": "给一个数组 [7, 3, 9, 1, 6, 4],用 filter 选出大于 4 的元素并求和。",
            "hint": "filter(|x| x > 4) 得 [7, 9, 6],再用 reduce 求和。",
            "solution": "let nums = [7, 3, 9, 1, 6, 4]\nlet big = nums.filter(|x| x > 4)\nlet sum = big.reduce(0, |acc, x| acc + x)\nprintln(\"选出的数: {big}\")\nprintln(\"和: {sum}\")",
            "expected": "选出的数: [7, 9, 6]\n和: 22",
        },
        "concepts": ["数组", "字典", "map/filter/reduce", "方法"],
    },
    # ───────────────────────── 第 6 章 ─────────────────────────
    {
        "id": "l06_recursion_dfs",
        "chapter": "第 6 章 · 递归与深度优先搜索",
        "title": "递归与深度优先搜索(DFS)",
        "objective": [
            "**递归**是函数调用自己。写递归要抓住两件事:① 递归出口(不再调用自己的条件);② 递归公式(把问题缩小)。",
            "```\nfn factorial(n: int) -> int {\n    if n <= 1 { return 1 }      // 出口\n    return n * factorial(n - 1) // 公式\n}\n```",
            "**深度优先搜索(DFS)** 是沿着一条路走到黑、再回头换路的搜索策略,常用于走迷宫、遍历图、数独等。核心模板:",
            "```\nfn dfs(graph, node, visited) {\n    visited.push(node)              // ① 标记已访问\n    for nb in graph[node] {         // ② 逐个访问邻居\n        if !visited.contains(nb) {  // ③ 没走过的才走\n            dfs(graph, nb, visited) // ④ 递归深入\n        }\n    }\n}\n```",
            "下面用邻接表(字典)表示一张图,A 出发的 DFS 会按深度优先顺序访问全部节点。",
            "二叉树是递归的天然舞台:一棵树 = 根 + 左子树 + 右子树。求树的最大深度只需递归地比较左右子树。",
        ],
        "example": '# 图的深度优先搜索(邻接表)\nlet graph = {\n    "A": ["B", "C"],\n    "B": ["A", "D", "E"],\n    "C": ["A", "F"],\n    "D": ["B"],\n    "E": ["B", "F"],\n    "F": ["C", "E"],\n}\n\nfn dfs(graph, node, visited) {\n    visited.push(node)\n    for nb in graph[node] {\n        if !visited.contains(nb) {\n            dfs(graph, nb, visited)\n        }\n    }\n}\n\nlet visited = []\ndfs(graph, "A", visited)\nprintln("DFS 顺序: {visited}")\n\n# 二叉树的最大深度(递归)\ntype TreeNode { val: int, left: TreeNode, right: TreeNode }\n\nfn maxDepth(node) -> int {\n    if node == nil { return 0 }\n    let l = maxDepth(node.left)\n    let r = maxDepth(node.right)\n    if l > r { return l + 1 }\n    return r + 1\n}\n\nlet root = TreeNode(val: 1)\nroot.left = TreeNode(val: 2)\nroot.right = TreeNode(val: 3)\nroot.left.left = TreeNode(val: 4)\nprintln("树的最大深度: {maxDepth(root)}")',
        "exercise": {
            "task": "给定邻接表 graph,从 \"D\" 出发做 DFS,输出访问顺序。",
            "hint": "复用示例的 dfs 函数,把起点改成 \"D\"。注意 visited.contains 判断。",
            "solution": 'let graph = {\n    "A": ["B", "C"],\n    "B": ["A", "D", "E"],\n    "C": ["A", "F"],\n    "D": ["B"],\n    "E": ["B", "F"],\n    "F": ["C", "E"],\n}\n\nfn dfs(graph, node, visited) {\n    visited.push(node)\n    for nb in graph[node] {\n        if !visited.contains(nb) {\n            dfs(graph, nb, visited)\n        }\n    }\n}\n\nlet visited = []\ndfs(graph, "D", visited)\nprintln("DFS 顺序: {visited}")',
            "expected": "DFS 顺序: ['D', 'B', 'A', 'C', 'F', 'E']",
        },
        "concepts": ["递归", "DFS", "邻接表", "二叉树"],
    },
    # ───────────────────────── 第 7 章 ─────────────────────────
    {
        "id": "l07_type_enum",
        "chapter": "第 7 章 · 类型与模式匹配",
        "title": "自定义类型、方法与枚举",
        "objective": [
            "用 `type` 定义自己的数据类型(类似 C 的 struct),字段就是你要保存的数据:",
            "```\ntype Point { x: float, y: float }\nlet p = Point(x: 3.0, y: 4.0)\nprintln(p.x)      // 3.0\n```",
            "用 `impl` 给类型加方法。注意方法里通过 `self` 访问当前对象:",
            "```\ntype Circle { r: float }\nimpl Circle {\n    fn area() -> float { return 3.14159 * self.r * self.r }\n}\nlet c = Circle(r: 2.0)\nprintln(c.area())\n```",
            "`enum` 定义一组可能的形式(类似 C 的 union + 标签)。配合 `match` 模式匹配,可以安全地分别处理每种情况:",
            "```\nenum Shape { Circle(radius: float), Rect(w: float, h: float) }\nfn area(s) -> float {\n    match s {\n        Circle(r) => 3.14159 * r * r,\n        Rect(w, h) => w * h,\n        _ => 0.0,\n    }\n}\n```",
            "match 的 `_` 是兜底分支,匹配所有没写的情况。这是类型系统最优雅的部分。",
        ],
        "example": 'type Point { x: float, y: float }\nimpl Point {\n    fn dist() -> float {\n        return (self.x * self.x + self.y * self.y) ** 0.5\n    }\n}\nlet p = Point(x: 3.0, y: 4.0)\nprintln("p 到原点的距离: {p.dist()}")\n\nenum Shape { Circle(radius: float), Rect(w: float, h: float) }\nfn area(s) -> float {\n    match s {\n        Circle(r) => 3.14159 * r * r,\n        Rect(w, h) => w * h,\n        _ => 0.0,\n    }\n}\nlet s = Shape.Rect(w: 5.0, h: 4.0)\nprintln("矩形面积: {area(s)}")',
        "exercise": {
            "task": "定义一个 Rectangle 类型(宽 w、高 h)和方法 area(),再定义一个方法 scale(k) 把宽高都放大 k 倍,输出放大后的面积。",
            "hint": "type Rectangle { w: float, h: float };impl 里 area() 返回 self.w * self.h;scale(k) 里 self.w = self.w * k。",
            "solution": 'type Rectangle { w: float, h: float }\nimpl Rectangle {\n    fn area() -> float { return self.w * self.h }\n    fn scale(k: float) {\n        self.w = self.w * k\n        self.h = self.h * k\n    }\n}\nlet r = Rectangle(w: 3.0, h: 4.0)\nr.scale(2.0)\nprintln("放大后面积: {r.area()}")',
            "expected": "放大后面积: 48.0",
        },
        "concepts": ["type", "impl", "enum", "match", "模式匹配"],
    },
    # ───────────────────────── 第 8 章 ─────────────────────────
    {
        "id": "l08_concurrency",
        "chapter": "第 8 章 · 并发与错误处理",
        "title": "通道并发与异常处理",
        "objective": [
            "Aurora 有 Go 风格的**协程与通道**:`spawn` 启动一个轻量任务,`chan(n)` 创建带缓冲的通道,`<-ch` 接收、`ch <- v` 发送。",
            "```\nfn worker(ch) {\n    ch <- 42\n    ch.close()\n}\nlet ch = chan(1)\nspawn worker(ch)\nprintln(<-ch)     // 42\n```",
            "`select` 可以同时等待多个通道,谁先有数据就处理谁:",
            "```\nselect {\n    v = <-ch1 => println(\"ch1: {v}\"),\n    v = <-ch2 => println(\"ch2: {v}\"),\n    default => println(\"两个通道都暂时没数据\"),\n}\n```",
            "错误处理用 `try / catch / finally`,像 Python 一样捕获运行时错误:",
            "```\ntry {\n    let x = 1 / 0\n} catch e: str {\n    println(\"出错了: {e}\")\n} finally {\n    println(\"无论是否出错都会执行\")\n}\n```",
            "到这一章,你已经掌握了 Aurora 的全部核心能力。去右侧编辑器里写你自己的程序吧!",
        ],
        "example": 'fn producer(ch) {\n    for i in range(5) {\n        ch <- i * i\n    }\n    ch.close()\n}\n\nlet ch = chan(5)\nspawn producer(ch)\nfor v in ch {\n    println("收到: {v}")\n}\n\nprintln("--- 错误处理 ---")\ntry {\n    let a = read_int("输入一个数: ")\n    println("100 / a = {100 / a}")\n} catch e: str {\n    println("出错了: {e}")\n} finally {\n    println("结束")\n}',
        "exercise": {
            "task": "启动两个 worker,分别发送 10 和 20 到一个通道,主程序用两次 <-ch 接收并输出总和。",
            "hint": "两个 spawn 往同一个通道发送;主程序 let a = <-ch; let b = <-ch。",
            "solution": 'fn worker(ch, v) {\n    ch <- v\n}\nlet ch = chan(2)\nspawn worker(ch, 10)\nspawn worker(ch, 20)\nlet a = <-ch\nlet b = <-ch\nprintln("总和: {a + b}")',
            "expected": "总和: 30",
        },
        "concepts": ["spawn", "chan", "select", "try/catch"],
    },
    # ───────────────────────── 第 9 章 ─────────────────────────
    {
        "id": "l09_modern_syntax",
        "chapter": "第 9 章 · 现代语法糖",
        "title": "可选链、空合并与表达式",
        "objective": [
            "Aurora 融合了现代语言的安全访问语法,让代码**更短、更不容易出错**。",
            "**可选链 `?.`**:当左侧是 `nil` 时,整个表达式安全地得到 `nil`,不会报错。适合访问可能不存在的字段:",
            "```\nlet user = { \"name\": \"Aurora\", \"age\": 2 }\nprintln(user?.name)     // Aurora\nprintln(user?.email)    // nil(字段不存在,不报错)\nlet guest = nil\nprintln(guest?.name)    // nil(nil 上访问也不报错)\n```",
            "**空合并 `??`**:左侧是 `nil` 时取右侧作为默认值,一行代替整个 if-else:",
            "```\nlet nickname = user?.name ?? \"无名\"\nprintln(nickname)       // Aurora\nlet port = nil ?? 8697\nprintln(port)           // 8697\n```",
            "**表达式即值**:`if`、`match`、代码块 `{}` 都可以作为值赋给变量,函数体最后一个表达式自动成为返回值:",
            "```\nlet score = 85\nlet grade = if score >= 90 { \"A\" } elif score >= 80 { \"B\" } else { \"C\" }\nprintln(grade)          // B\n\nfn sign(x: int) -> str {\n    if x > 0 { \"正数\" } elif x < 0 { \"负数\" } else { \"零\" }\n}\nprintln(sign(-5))       // 负数\n```",
            "注释两种写法都支持:`// 行注释` 与 `# 行注释`;`nil` 打印出来就是 `nil`。",
        ],
        "example": '// 9 章 · 现代语法糖\nlet config = {\n    "host": "localhost",\n    "port": nil,\n}\n\nlet host = config?.host ?? "127.0.0.1"\nlet port = config?.port ?? 8080\nprintln("连接 {host}:{port}")\n\nlet items = [3, 1, 2]\nlet first = items?.len() ?? 0\nprintln("元素个数: {first}")',
        "exercise": {
            "task": "用 `?.` 与 `??` 写一段代码:person 的 name 存在就打印它,不存在就打印“游客”;再定义一个函数 classify(n),n 大于 0 返回“正”,小于 0 返回“负”,否则返回“零”,并打印 classify(-3) 的结果。",
            "hint": "let name = person?.name ?? \"游客\";函数体里用 if 表达式作为返回值。",
            "solution": 'let person = { "name": "小明" }\nlet who = person?.name ?? "游客"\nprintln(who)\n\nlet nobody = nil\nlet stranger = nobody?.name ?? "游客"\nprintln(stranger)\n\nfn classify(n: int) -> str {\n    if n > 0 { "正" } elif n < 0 { "负" } else { "零" }\n}\nprintln(classify(-3))',
            "expected": "小明\n游客\n负",
        },
        "concepts": ["可选链 ?.", "空合并 ??", "if 表达式", "// 注释"],
    },
]

LESSON_MAP = {lesson["id"]: lesson for lesson in LESSONS}
