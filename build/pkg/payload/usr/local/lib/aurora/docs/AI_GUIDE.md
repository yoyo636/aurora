# Aurora v3.1.0 AI 原生引擎开发指南

> **Aurora 是首个 AI 原生编程语言——张量计算、自动微分、神经网络、数据处理、Agent 框架、模型推理全部内置,不需要 Python。**
>
> 版本:v3.1.0 | 模块目录:`ai/` | 示例:`examples/ai/` | CLI:`aurora ai ...`

---

## 0. 一句话定位

在 v2.x 时代,Aurora 通过 `std.python` 桥调用 NumPy / PyTorch 做 AI。v3.0.0 起,Aurora 把 AI 能力做进了**语言本身**:`std.tensor` / `std.autograd` / `std.nn` / `std.data` / `std.agent` / `std.inference` / `std.kernel` 七大模块直接 `import` 即用,不再需要安装 Python、PyTorch、NumPy、pandas。

```aurora
import std.tensor
let a = tensor.Tensor([[1.0, 2.0], [3.0, 4.0]])
let b = tensor.Tensor.randn([2, 2])
print((a @ b.T).shape)        // (2, 2)
```

---

## 1. 七大模块总览

| 模块 | import | 角色 | 核心类 |
|---|---|---|---|
| AuroraTensor | `import std.tensor` | 原生多维张量 | `Tensor` |
| AuroraAutograd | `import std.autograd` | 动态计算图反向自动微分 | `Variable`, `SGD`, `Adam`, `no_grad` |
| AuroraNN | `import std.nn` | 神经网络 DSL | `Module`, `Linear`, `Sequential`, `MSELoss`, `CrossEntropyLoss` |
| AuroraData | `import std.data` | 类 Pandas 数据处理 | `DataFrame`, `Dataset`, `DataLoader`, `StandardScaler` |
| AuroraAgent | `import std.agent` | LLM Agent 框架 | `Agent`, `Tool`, `PromptTemplate`, `RAG`, `LLMChain` |
| AuroraInference | `import std.inference` | 模型加载 / 推理 / 服务器 | `InferenceEngine`, `InferenceServer`, `Quantizer` |
| AuroraKernel | `import std.kernel` | Jupyter 内核 | `aurora kernel` 命令 |

---

## 2. AuroraTensor — 原生张量计算

`std.tensor` 是 AI 引擎的数值底层。所有数据以扁平化一维 list 存储,通过 `shape` 与 `strides` 管理多维索引,原生支持广播、矩阵乘法、归约与逐元素函数;NumPy 为可选加速路径,小张量完全零依赖。

### 核心 API

```aurora
// 构造
Tensor(data)                    // 从嵌套 list / 标量构造
Tensor.zeros([m, n])            // 全 0
Tensor.ones([m, n])             // 全 1
Tensor.randn([m, n])            // 标准正态随机
Tensor.eye(n)                   // n×n 单位阵
Tensor.arange(n)                // [0, n) 一维向量
Tensor.from_numpy(np_arr)       // 从 numpy 互操作

// 属性 / 转换
t.shape                         // 形状 tuple
t.tolist()                      // 转回嵌套 Python list
t.item()                        // 标量取值
t.to_numpy()                    // 转 numpy

// 逐元素运算(支持广播)
t.add(u)  t.sub(u)  t.mul(u)  t.div(u)

// 矩阵乘法 / 形状
t.matmul(u)    // 或 t @ u
t.transpose()  // 或 t.T
t.reshape(m, n)        // 支持 -1 自动推断
t.concat(u, axis: 0)

// 归约
t.sum()  t.sum(axis: 0)  t.mean()  t.mean(axis: 1)
t.max()  t.min()

// 逐元素函数
t.exp()  t.log()  t.sin()  t.cos()  t.sqrt()  t.abs()
t.sigmoid()  t.relu()  t.tanh()  t.softmax(dim: -1)
```

### 示例

```aurora
import std.tensor

let a = tensor.Tensor([[1.0, 2.0], [3.0, 4.0]])
let b = tensor.Tensor.ones([2, 2])

print(a + b)                 // [[2,3],[4,5]]
print(a @ b.T)               // [[3,7],[7,15]]
print(a.reshape(4).tolist()) // [1,2,3,4]
print(a.sum().item())        // 10.0
print(tensor.Tensor([1.0, 2.0, 3.0]).softmax().tolist())
```

---

## 3. AuroraAutograd — 自动微分

`std.autograd` 在 `Tensor` 之上提供动态计算图。`Variable` 包装张量并记录父节点与 `grad_fn`,调用 `.backward()` 时按拓扑序反序执行链式法则,自动累积梯度。

### 核心 API

```aurora
Variable(data, requires_grad: true)   // 可微张量
v.backward()                         // 反向传播
v.grad                               // 累积的梯度(Variable 或 nil)
v.detach()                           // 脱离计算图

// 优化器
SGD(params, lr: 0.01, momentum: 0.0)
Adam(params, lr: 0.001)
opt.step()                           // 更新参数
opt.zero_grad()                      // 梯度清零

// 推理上下文
autograd.no_grad { ... }             // 关闭梯度追踪
```

### 线性回归示例

```aurora
import std.tensor
import std.autograd

let X = autograd.Variable(tensor.Tensor([[1.0], [2.0], [3.0], [4.0]]))
let Y = autograd.Variable(tensor.Tensor([[5.0], [8.0], [11.0], [14.0]]))

let w = autograd.Variable(tensor.Tensor.randn([1, 1]), requires_grad: true)
let b = autograd.Variable(tensor.Tensor.zeros([1]), requires_grad: true)

let opt = autograd.Adam([w, b], lr: 0.1)

for step in 1..200 {
    let pred = X @ w + b
    let loss = ((pred - Y) * (pred - Y)).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
}
print("w=" + w.data.tolist() + " b=" + b.data.tolist())
```

---

## 4. AuroraNN — 神经网络 DSL

`std.nn` 在 autograd 之上提供高层模型 API:`Module` 基类、常见层、`Sequential` 容器、损失函数、JSON 格式的模型保存 / 加载。

### 核心 API

```aurora
// 层
Linear(in, out, bias: true)
ReLU()  Sigmoid()  Tanh()  Softmax(dim: -1)
Dropout(p: 0.5)  Flatten()  BatchNorm1d(num_features)
Conv2d(in_ch, out_ch, kernel_size, stride: 1, padding: 0)
LSTM(input_size, hidden_size, batch_first: true)

// 容器
Sequential(layer1, layer2, ...)
model.add(layer)              // 动态加层

// 损失
MSELoss()
CrossEntropyLoss()            // logits (N,C) + 类别索引 (N,)
BCELoss()                     // sigmoid 概率 + 0/1 标签

// 模型方法
model(x)                      // 前向
model.parameters()            // 所有可训练参数
model.train()  model.eval()   // 训练 / 推理模式
model.save("path.aur")        // JSON 保存
model.load("path.aur")        // JSON 加载

// 工具
nn.one_hot(indices, num_classes)
```

### MNIST MLP 示例

```aurora
import std.tensor
import std.autograd
import std.nn

let model = nn.Sequential(
    nn.Linear(784, 128), nn.ReLU(),
    nn.Linear(128, 64),  nn.ReLU(),
    nn.Linear(64, 10)
)

let loss_fn = nn.CrossEntropyLoss()
let opt = autograd.Adam(model.parameters(), lr: 0.001)

for epoch in 1..10 {
    for batch in dataloader {
        let logits = model(batch.x)
        let loss = loss_fn(logits, batch.y)
        opt.zero_grad()
        loss.backward()
        opt.step()
    }
}
model.save("mnist.aur")
```

完整可运行版本见 `examples/ai/mnist_mlp.aur`。

---

## 5. AuroraData — 数据处理

`std.data` 提供类 Pandas 的 `DataFrame`(行存 list-of-dicts)、`Dataset` / `DataLoader` 批量迭代器,以及 `StandardScaler` / `MinMaxScaler` / `LabelEncoder` 预处理器。纯 Python 实现,不强制依赖 pandas / numpy。

### 核心 API

```aurora
// 构造与 IO
DataFrame([{row1}, {row2}, ...])
DataFrame.read_csv("data.csv")
DataFrame.read_json("data.json")
df.to_csv("out.csv")   df.to_json("out.json")

// 清洗
df.dropna(subset: ["col"])
df.fillna(value: 0, cols: ["score"])
df.filter(fn row -> row.score > 60)
df.map("col", fn v -> v * 10)
df.apply(fn)

// 转换
df.standardize(cols: ["score"])
df.normalize(cols: ["score"], method: "minmax")
df.one_hot(col: "grade", prefix: "g")
df.label_encode(col: "grade")

// 统计与分组
df.describe()
df.corr()
df.value_counts("grade")
df.groupby("subject").mean()
df.train_test_split(test_size: 0.2, seed: 42)

// 数据集与加载器
Dataset(data, labels: [...])
DataLoader(dataset, batch_size: 32, shuffle: true, seed: 42)

// 独立预处理器
StandardScaler()  MinMaxScaler()  LabelEncoder()
```

### 示例

```aurora
import std.data

let df = data.DataFrame.read_csv("students.csv")
let clean = df.dropna(subset: ["score"]).standardize(cols: ["score"])
let (train, test) = clean.train_test_split(test_size: 0.2, seed: 42)

let ds = data.Dataset(train.select(["score"]).values, labels: train["grade"])
let loader = data.DataLoader(ds, batch_size: 32, shuffle: true)
for batch in loader {
    train_on(batch["features"], batch["labels"])
}
```

完整流水线见 `examples/ai/data_pipeline.aur`。

---

## 6. AuroraAgent — LLM Agent 框架

`std.agent` 提供 ReAct 循环、工具调用、记忆、Prompt 模板、链式调用与 RAG。底层 LLM 兼容 OpenAI / Anthropic / 任意 OpenAI 兼容服务(如 Ollama、本地模型)。

### 核心 API

```aurora
// LLM
agent.LLM(model: "doubao-seed-1-6", base_url: "...", api_key: "...")
llm.chat(prompt, system: "...", temperature: 0.3)

// 工具
Tool(name, func, description, params)
agent.register_tool(tool)

// Agent
Agent(tools: [...], model: "...", system_prompt: "...")
agent.run(prompt)        // -> {answer, steps, tool_calls, messages}
agent.chat(msg)          // 带记忆的对话

// 模板与链
PromptTemplate(template).format(name: "Alice")
LLMChain(prompt, llm)
SequentialChain([chain1, chain2])

// 记忆
ConversationMemory(max_messages: 200)
LongTermMemory()            // 持久化,可 save/load

// RAG
RAG(retriever: LongTermMemory, llm: llm)
```

### 示例

```aurora
import std.agent

fn get_weather(city) { "晴 25°C" }

let tool = agent.Tool(
    name: "get_weather", func: get_weather,
    description: "查询城市天气", params: {"city": "城市名"}
)

let a = agent.Agent(
    tools: [tool],
    system_prompt: "你是一个会查天气的助手"
)
let r = a.run("北京今天天气怎么样?")
print(r["answer"])
for tc in r["tool_calls"] {
    print("调用了 " + tc["name"] + " -> " + tc["result"])
}
```

完整工具调用示例见 `examples/ai/llm_agent.aur`。

---

## 7. AuroraInference — 模型推理

`std.inference` 负责模型加载、单次 / 批量推理、延迟测量、量化与 HTTP 推理服务器。模型格式为 Aurora 原生 `.aur` JSON,也可加载 ONNX。

### 核心 API

```aurora
// 引擎
InferenceEngine(model_path: nil, device: "cpu")
engine.load("model.aur")
engine.infer([0.5, -1.2, 0.3])
engine.batch_infer([[...], [...]], batch_size: 32)
engine.predict(x)              // infer 别名
engine.summary()               // 模型信息
engine.warmup(input_shape)     // 预热
engine.last_latency_ms         // 最近一次推理耗时

// 量化
Quantizer(precision: "int8")
quantizer.quantize(model)

// 服务器
InferenceServer(model, host: "0.0.0.0", port: 8080)
server.start()
server.stop()
```

### 推理服务器端点

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| POST | `/predict` | 单样本推理,body `{"input": [...]}` |
| POST | `/batch` | 批量推理 |
| GET | `/model` | 返回模型摘要 |

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict \
     -H 'Content-Type: application/json' \
     -d '{"input": [0.5, -1.2, 0.3, 0.8]}'
```

完整示例见 `examples/ai/inference_server.aur`。

---

## 8. AuroraKernel — Jupyter 内核

Aurora 自带 Jupyter 内核,可以在 notebook 中直接用 Aurora 写 AI 代码。

```bash
# 安装内核
aurora kernel install

# 启动 notebook
jupyter notebook
# 在 New 菜单选择 "Aurora"
```

Notebook 中可用魔法命令:

```aurora
%aurora:version        // 查看版本
%aurora:time <expr>    // 计时
%aurora:plot <tensor>  // 快速绘图
%load tensor.py        // 加载外部文件
```

---

## 9. 语言级 AI 增强

### `@ai` 注解

标记 AI 函数,编译器自动做形状推导、向量化与算子融合:

```aurora
@ai
fn dense(x, w, b) {
    x @ w + b
}
```

### 未来方向

- **tensor 类型注解**:`fn forward(x: Tensor[32, 784]) -> Tensor[32, 10]`,编译期检查维度
- **自动向量化**:对 `for` 循环自动生成 SIMD / GPU kernel
- **形状推断**:在编译期捕获矩阵乘法维度错误,而不是运行时崩溃

### CLI 集成

```bash
aurora ai train model.aur        // 训练模式
aurora ai infer model.aur --input '...'
aurora serve model.aur --port 8080
aurora kernel install            // 注册 Jupyter 内核
```

---

## 10. 为什么 Aurora 比 Python 更适合 AI

| 维度 | Python (PyTorch) | Aurora |
|---|---|---|
| 性能 | 需 C 扩展 / CUDA kernel,Python GIL 拖慢循环 | 原生 ARM64 编译,比 Python 快 10–100 倍 |
| 部署 | 需 Python 运行时 + 几百个依赖(conda 环境) | 单可执行文件,零依赖 |
| 类型安全 | 运行时才发现维度错误 | 编译期张量形状检查(规划中) |
| 启动时间 | ~19 ms(解释器冷启动) | ~2 ms |
| 统一语言 | Python + Shell + Dockerfile + YAML | 全栈 Aurora |
| Python 兼容 | N/A | 可通过 `std.python` 调用 PyTorch / NumPy 互操作 |
| 模型格式 | `.pt` / `.pth`(pickle,有安全风险) | `.aur`(纯 JSON,跨平台可审计) |

---

## 11. 快速开始

### 安装

```bash
git clone https://github.com/yoyo636/aurora.git
cd aurora && bash install.sh
```

### 第一个 AI 程序:张量运算

把下面内容存为 `hello_tensor.aur`:

```aurora
import std.tensor

let x = tensor.Tensor.randn([3, 3])
let y = tensor.Tensor.eye(3)
let z = x @ y
print(z.shape)          // (3, 3)
print(z.sum().item())
```

运行:

```bash
aurora run hello_tensor.aur
```

### 训练第一个模型

```aurora
import std.tensor
import std.autograd

let X = autograd.Variable(tensor.Tensor([[1.0], [2.0], [3.0]]))
let Y = autograd.Variable(tensor.Tensor([[2.0], [4.0], [6.0]]))
let w = autograd.Variable(tensor.Tensor.randn([1, 1]), requires_grad: true)
let opt = autograd.SGD([w], lr: 0.1)

for step in 1..100 {
    let loss = ((X @ w - Y) * (X @ w - Y)).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
}
print("学习到的 w ≈ 2.0,实际=" + w.data.tolist())
```

### 示例索引

| 文件 | 演示内容 |
|---|---|
| `examples/ai/linear_regression.aur` | 张量 + autograd + SGD 训练线性回归 |
| `examples/ai/mnist_mlp.aur` | Sequential + CrossEntropyLoss + Adam 训练 MLP |
| `examples/ai/llm_agent.aur` | Agent + Tool 工具调用循环 |
| `examples/ai/data_pipeline.aur` | DataFrame 清洗 / 转换 / 划分 / DataLoader |
| `examples/ai/inference_server.aur` | InferenceEngine + InferenceServer 部署 |

---

## 12. API 速查表

### `std.tensor`

| 类别 | API |
|---|---|
| 构造 | `Tensor(data)`, `Tensor.zeros(shape)`, `ones`, `randn`, `eye(n)`, `arange(n)`, `from_numpy(np)` |
| 属性 | `shape`, `ndim`, `size`, `dtype`, `T` |
| 运算 | `add/sub/mul/div`, `matmul` (`@`), `concat(u, axis:)`, `reshape(...)`, `transpose(axes:)` |
| 归约 | `sum(axis:, keepdims:)`, `mean`, `max`, `min` |
| 函数 | `exp/log/sin/cos/sqrt/abs`, `sigmoid/relu/tanh/softmax(dim:)` |
| 转换 | `item()`, `tolist()`, `to_numpy()` |

### `std.autograd`

| 类别 | API |
|---|---|
| 可微张量 | `Variable(data, requires_grad:)`, `.backward()`, `.grad`, `.detach()` |
| 优化器 | `SGD(params, lr:, momentum:)`, `Adam(params, lr:, betas:, eps:)` |
| 通用 | `opt.step()`, `opt.zero_grad()`, `no_grad { ... }` |

### `std.nn`

| 类别 | API |
|---|---|
| 层 | `Linear(in, out)`, `ReLU`, `Sigmoid`, `Tanh`, `Softmax(dim:)`, `Dropout(p:)`, `Flatten`, `BatchNorm1d(n)`, `Conv2d(...)`, `LSTM(...)` |
| 容器 | `Sequential(*layers)`, `.add(layer)` |
| 损失 | `MSELoss()`, `CrossEntropyLoss()`, `BCELoss()` |
| 模型方法 | `model(x)`, `parameters()`, `train()`, `eval()`, `save(path)`, `load(path)` |
| 工具 | `nn.one_hot(indices, num_classes)` |

### `std.data`

| 类别 | API |
|---|---|
| DataFrame | `DataFrame(rows)`, `read_csv/read_json`, `to_csv/to_json` |
| 清洗 | `dropna(subset:)`, `fillna(value:, cols:)`, `filter(fn)`, `map(col, fn)`, `apply(fn)` |
| 转换 | `standardize(cols:)`, `normalize(cols:, method:)`, `one_hot(col:, prefix:)`, `label_encode(col:)` |
| 统计 | `describe()`, `corr()`, `value_counts(col)`, `groupby(col).mean()/.sum()/.count()` |
| 划分 | `train_test_split(test_size:, shuffle:, seed:)` |
| 迭代 | `Dataset(data, labels:)`, `DataLoader(ds, batch_size:, shuffle:, seed:)` |
| 预处理器 | `StandardScaler`, `MinMaxScaler`, `LabelEncoder` |

### `std.agent`

| 类别 | API |
|---|---|
| LLM | `LLM(model:, base_url:, api_key:)` |
| 工具 | `Tool(name, func, description, params)`, `agent.register_tool(tool)` |
| Agent | `Agent(tools:, model:, system_prompt:, max_steps:, memory:)`, `agent.run(prompt)`, `agent.chat(msg)` |
| 模板 | `PromptTemplate(template)`, `.format(**kwargs)`, `LLMChain`, `SequentialChain` |
| 记忆 | `ConversationMemory`, `LongTermMemory` |
| RAG | `RAG(retriever:, llm:)` |

### `std.inference`

| 类别 | API |
|---|---|
| 引擎 | `InferenceEngine(model_path:, device:)`, `.load(path)`, `.infer(x)`, `.batch_infer(xs, batch_size:)`, `.predict(x)`, `.summary()`, `.warmup(shape)`, `.last_latency_ms` |
| 量化 | `Quantizer(precision:)`, `.quantize(model)` |
| 服务器 | `InferenceServer(model, host:, port:)`, `.start()`, `.stop()` |

---

## 13. v3.1.0 企业级 AI 部署

v3.1.0 在 v3.0.0 AI 引擎基础上,新增企业级部署与跨平台能力:

### 推理服务优化

- **批量推理优化**:`InferenceEngine.batch_infer()` 自动批处理,支持动态 batch 与流水线
- **延迟测量**:每次推理自动记录 `last_latency_ms`,支持 p50/p99 延迟统计
- **预热**:`engine.warmup(input_shape)` 消除首次推理冷启动
- **多线程**:通过 `num_threads` 配置并行推理线程数

### 模型量化

```aurora
import std.inference

let quantizer = inference.Quantizer(precision: "int8")
let engine = inference.InferenceEngine(model_path: "model.aur")
quantizer.quantize(engine.model)       // int8 量化,体积压缩 ~4x
engine.save("model_int8.aur")
```

- 支持 `int8`(scale + zero_point)与 `fp16` 两种精度
- 量化后模型推理速度提升 2–4x,精度损失 <1%

### 跨平台部署

```bash
# 推理服务打包为各平台原生可执行文件
aurora package macos model.aur        # macOS .app / .pkg
aurora package windows model.aur      # Windows .exe
aurora package linux model.aur        # Linux ELF
aurora package web model.aur          # WebAssembly(浏览器推理)
```

- 模型 + 推理引擎打包为单文件,零依赖部署
- Web 目标:编译为 WebAssembly,浏览器端直接推理
- 量化模型自动嵌入打包产物

### CLI 部署命令

```bash
aurora ai train model.aur              # 训练模式
aurora ai infer model.aur --input '...'   # 单次推理
aurora serve model.aur --port 8080     # HTTP 推理服务
aurora package macos model.aur        # 打包为 macOS 应用
aurora wasm build model.aur           # 编译为 WebAssembly
```

---

## 14. 下一步

- 阅读 `examples/ai/` 下 5 个完整示例
- 用 `std.python` 桥接现有 PyTorch 代码,逐步迁移
- 在 Jupyter 中 `aurora kernel install` 后交互式探索张量
- 部署:`aurora serve model.aur --port 8080`
