# Aurora 全栈示例

一个 `.aur` 文件同时演示 **HTML 前端 + Web 后端 + Rust/C++/Python/JSON 后端 + AI Agent**。

## 前置构建(共享库)

```bash
cd ../interop/rust_math && cargo build --release
cd ../interop && clang++ -shared -fPIC -O2 cpp_math.cpp -o libcpp_math.dylib
```

## 运行

```bash
cd examples/fullstack
../../aurora-run run app.aur
```

浏览器打开 http://127.0.0.1:8988/

## 页面能力

| 卡片 | 后端 | 说明 |
| --- | --- | --- |
| 计算后端 | Rust `add/fib` + C++ `gcd/ipow`(FFI) | `/api/calc` JSON API |
| Python 后端 | `std.python` 导入 math / 列表推导 | `/api/py` JSON API |
| AI Agent | `std.ai.agent` 工具调用循环 | `/api/ai`,大模型调用 Aurora 函数 |

## AI Agent 配置

`std.ai` 走 OpenAI 兼容协议,三种配置方式(优先级从高到低):

```bash
# 1. 环境变量
export AURORA_AI_API_KEY=你的密钥
export AURORA_AI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3   # 默认火山方舟
export AURORA_AI_MODEL=doubao-seed-1-6-250615                        # 默认豆包模型

# 2. 代码内配置(可直接写在 app.aur 顶部)
# std.ai.configure(api_key: "...", base_url: "...", model: "...")

# 3. 通用 OpenAI 兼容服务 / 本地模型均可
# export AURORA_AI_BASE_URL=http://localhost:11434/v1  # Ollama 本地
```

未配置 Key 时,Agent 相关接口会给出明确提示,其余功能不受影响。

## 请求示例

```bash
curl -s -X POST http://127.0.0.1:8988/api/calc -d '{"a": 48, "b": 36, "n": 10}'
# {"add": 84, "gcd": 12, "fib": 55, "ipow": 1024, "backend": "Rust + C++ (FFI)"}

curl -s -X POST http://127.0.0.1:8988/api/py -d '{"n": 81}'
# {"sqrt": 9.0, "floor_pi": 314, "prime_less_20": [2, 3, 5, 7, 11, 13, 17, 19], "backend": "Python"}
```
