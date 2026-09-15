"""Aurora v3.0.0 AI 引擎测试

覆盖六大 AI 原生模块:
- TestAuroraTensor:  张量创建 / 算术 / 矩阵乘法 / 广播 / 通用函数 / 形状 / 归约 / 类方法
- TestAuroraAutograd: Variable 反向传播 / 线性回归收敛 / Adam / matmul 梯度 / no_grad
- TestAuroraNN:      Linear / Sequential / 损失函数 / 模型存取 / Conv2d / LSTM
- TestAuroraData:    DataFrame / CSV IO / 清洗 / groupby / DataLoader / Scaler
- TestAuroraAgent:   PromptTemplate / 工具注册 / 对话记忆 / LLMChain(结构)
- TestAuroraInference: InferenceEngine / 模型存取 round-trip / 量化 / 推理服务器

直接从 ``aurora.ai`` 包导入(不依赖 stdlib 注册),确保测试独立可靠。
"""

import os
import sys
import json
import math
import tempfile
import unittest
import urllib.request

# 确保无论从哪个工作目录运行,都能把项目父目录加入 sys.path 以导入 aurora 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from aurora.ai.tensor import Tensor
from aurora.ai.autograd import Variable, SGD, Adam, no_grad
from aurora.ai import nn
from aurora.ai.data import (
    DataFrame, Dataset, DataLoader,
    StandardScaler, MinMaxScaler, LabelEncoder,
)
from aurora.ai.agent import (
    PromptTemplate, Tool, ToolRegistry, ConversationMemory,
    LLMChain, Agent,
)
from aurora.ai.inference import (
    SimpleAuroraModel, InferenceEngine, InferenceServer,
    Quantizer, save_model, load_model,
)


# ===========================================================================
# 1. Tensor
# ===========================================================================
class TestAuroraTensor(unittest.TestCase):
    """AuroraTensor 原生张量计算库的单元测试。"""

    def test_tensor_creation(self):
        """从嵌套 list 创建张量,验证 shape / ndim / 扁平化 data。"""
        t = Tensor([[1, 2], [3, 4]])
        self.assertEqual(t.shape, (2, 2))
        self.assertEqual(t.ndim, 2)
        self.assertEqual(t.data, [1, 2, 3, 4])
        self.assertEqual(t.tolist(), [[1, 2], [3, 4]])
        # 标量
        s = Tensor(3.5)
        self.assertEqual(s.shape, ())
        self.assertEqual(s.item(), 3.5)

    def test_tensor_arithmetic(self):
        """add / sub / mul / div 逐元素运算。"""
        a = Tensor([[1.0, 2.0], [3.0, 4.0]])
        b = Tensor([[5.0, 6.0], [7.0, 8.0]])
        self.assertEqual(a.add(b).tolist(), [[6.0, 8.0], [10.0, 12.0]])
        self.assertEqual(a.sub(b).tolist(), [[-4.0, -4.0], [-4.0, -4.0]])
        self.assertEqual(a.mul(b).tolist(), [[5.0, 12.0], [21.0, 32.0]])
        div = a.div(b).tolist()
        self.assertAlmostEqual(div[0][0], 1.0 / 5.0)
        self.assertAlmostEqual(div[1][1], 4.0 / 8.0)
        # 运算符重载
        self.assertEqual((a + b).tolist(), [[6.0, 8.0], [10.0, 12.0]])
        # 标量广播
        self.assertEqual((a + 1.0).tolist(), [[2.0, 3.0], [4.0, 5.0]])

    def test_tensor_matmul(self):
        """2D 矩阵乘法:[[1,2],[3,4]] @ [[5,6],[7,8]] = [[19,22],[43,50]]。"""
        a = Tensor([[1.0, 2.0], [3.0, 4.0]])
        b = Tensor([[5.0, 6.0], [7.0, 8.0]])
        self.assertEqual(a.matmul(b).tolist(), [[19.0, 22.0], [43.0, 50.0]])
        self.assertEqual((a @ b).tolist(), [[19.0, 22.0], [43.0, 50.0]])

    def test_tensor_broadcast(self):
        """NumPy 风格广播:(2,3)+(3,) 与 (2,1)+(1,3)。"""
        a = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        b = Tensor([10.0, 20.0, 30.0])
        self.assertEqual((a + b).tolist(),
                         [[11.0, 22.0, 33.0], [14.0, 25.0, 36.0]])
        c = Tensor([[1.0], [2.0]])           # (2,1)
        d = Tensor([[10.0, 20.0, 30.0]])     # (1,3)
        self.assertEqual((c + d).tolist(),
                         [[11.0, 21.0, 31.0], [12.0, 22.0, 32.0]])

    def test_tensor_functions(self):
        """exp / log / sigmoid / relu / softmax 数值正确性。"""
        self.assertAlmostEqual(Tensor([0.0]).exp().tolist()[0], 1.0)
        self.assertAlmostEqual(Tensor([1.0]).log().tolist()[0], 0.0)
        self.assertAlmostEqual(Tensor([0.0]).sigmoid().tolist()[0], 0.5)
        self.assertEqual(Tensor([-1.0, 2.0]).relu().tolist(), [0.0, 2.0])
        # softmax 每行求和为 1,且最大元素概率最大
        sm = Tensor([1.0, 2.0, 3.0]).softmax().tolist()
        self.assertAlmostEqual(sum(sm), 1.0)
        self.assertEqual(sm.index(max(sm)), 2)

    def test_tensor_reshape_transpose(self):
        """reshape 与 transpose 形状 / 数值。"""
        t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        r = t.reshape(3, 2)
        self.assertEqual(r.shape, (3, 2))
        self.assertEqual(r.tolist(), [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        tr = t.transpose()
        self.assertEqual(tr.shape, (3, 2))
        self.assertEqual(tr.tolist(), [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]])
        self.assertEqual(t.T.tolist(), tr.tolist())

    def test_tensor_reduce(self):
        """sum / mean 归约。"""
        t = Tensor([[1.0, 2.0], [3.0, 4.0]])
        self.assertEqual(t.sum().item(), 10.0)
        self.assertAlmostEqual(t.mean().item(), 2.5)
        # 按列求和 -> [4,6]
        self.assertEqual(t.sum(axis=0).tolist(), [4.0, 6.0])

    def test_tensor_class_methods(self):
        """zeros / ones / eye / arange 工厂方法。"""
        self.assertEqual(Tensor.zeros((2, 2)).tolist(),
                         [[0.0, 0.0], [0.0, 0.0]])
        self.assertEqual(Tensor.ones(3).tolist(), [1.0, 1.0, 1.0])
        self.assertEqual(Tensor.eye(2).tolist(), [[1.0, 0.0], [0.0, 1.0]])
        self.assertEqual(Tensor.arange(4).tolist(), [0.0, 1.0, 2.0, 3.0])


# ===========================================================================
# 2. Autograd
# ===========================================================================
class TestAuroraAutograd(unittest.TestCase):
    """AuroraAutograd 自动微分引擎。"""

    def test_variable_backward(self):
        """f(x)=x^2, x=3 时梯度应为 6。"""
        x = Variable(Tensor(3.0), requires_grad=True)
        loss = x * x
        loss.backward()
        self.assertIsNotNone(x.grad)
        self.assertAlmostEqual(x.grad.data.item(), 6.0, places=5)

    def test_linear_regression_convergence(self):
        """用 Variable + SGD 训练 y=3x+2,验证 loss 显著下降。"""
        x = Variable(Tensor([[1.0], [2.0], [3.0], [4.0]]))
        y = Variable(Tensor([[5.0], [8.0], [11.0], [14.0]]))
        w = Variable(Tensor.randn((1, 1)), requires_grad=True)
        b = Variable(Tensor.zeros((1,)), requires_grad=True)
        opt = SGD([w, b], lr=0.1)
        first_loss = None
        last_loss = None
        for i in range(200):
            pred = x @ w + b
            loss = ((pred - y) * (pred - y)).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            if i == 0:
                first_loss = loss.item()
            last_loss = loss.item()
        self.assertLess(last_loss, first_loss / 10.0)

    def test_adam_optimizer(self):
        """Adam step 更新参数、zero_grad 清零梯度。"""
        p = Variable(Tensor([1.0, 2.0, 3.0]), requires_grad=True)
        opt = Adam([p], lr=0.1)
        loss = (p * p).sum()
        loss.backward()
        before = list(p.data.data)
        opt.step()
        after = list(p.data.data)
        self.assertNotEqual(before, after)
        self.assertIsNotNone(p.grad)
        opt.zero_grad()
        self.assertIsNone(p.grad)

    def test_matmul_gradient(self):
        """matmul 梯度:dA = grad @ B.T,dB = A.T @ grad。"""
        A = Variable(Tensor([[1.0, 2.0], [3.0, 4.0]]), requires_grad=True)
        B = Variable(Tensor([[5.0, 6.0], [7.0, 8.0]]), requires_grad=True)
        C = (A @ B).sum()
        C.backward()
        # dL/dA[i][j] = B 第 j 行和 -> A 第 0 列=11, 第 1 列=15
        self.assertEqual(A.grad.data.tolist(), [[11.0, 15.0], [11.0, 15.0]])
        # dB[j][k] = A 第 j 列和 -> [[4,4],[6,6]]
        self.assertEqual(B.grad.data.tolist(), [[4.0, 4.0], [6.0, 6.0]])

    def test_no_grad(self):
        """no_grad() 上下文中不记录梯度。"""
        with no_grad():
            x = Variable(Tensor([1.0]), requires_grad=True)
            out = x * 2.0
            self.assertFalse(out.requires_grad)


# ===========================================================================
# 3. NN
# ===========================================================================
class TestAuroraNN(unittest.TestCase):
    """AuroraNN 神经网络 DSL。"""

    def test_linear_forward(self):
        """Linear 层前向输出形状。"""
        layer = nn.Linear(4, 8)
        x = Variable(Tensor([[0.1, 0.2, 0.3, 0.4],
                             [0.5, 0.6, 0.7, 0.8]]))
        out = layer(x)
        self.assertEqual(out.shape, (2, 8))

    def test_sequential(self):
        """Sequential 多层串联输出形状与索引。"""
        model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))
        self.assertEqual(len(model), 3)
        self.assertIsInstance(model[1], nn.ReLU)
        x = Variable(Tensor([[0.1, 0.2, 0.3, 0.4],
                             [0.5, 0.6, 0.7, 0.8]]))
        out = model(x)
        self.assertEqual(out.shape, (2, 2))

    def test_loss_functions(self):
        """MSELoss 与 CrossEntropyLoss 数值 / 可运行。"""
        mse = nn.MSELoss()
        pred = Variable(Tensor([[1.0], [2.0], [3.0]]))
        target = Variable(Tensor([[1.0], [2.0], [4.0]]))
        loss = mse(pred, target)
        self.assertAlmostEqual(loss.item(), 1.0 / 3.0, places=5)

        ce = nn.CrossEntropyLoss()
        logits = Variable(Tensor([[2.0, 1.0, 0.1],
                                  [0.5, 2.0, 1.5]]))
        targets = Variable(Tensor([0.0, 1.0]))
        cl = ce(logits, targets)
        self.assertTrue(cl.item() > 0.0)

    def test_model_save_load(self):
        """模型保存为 .aur 再加载,相同输入预测一致。"""
        model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))
        x = Variable(Tensor([[0.1, 0.2, 0.3, 0.4],
                             [0.5, 0.6, 0.7, 0.8]]))
        out1 = model(x).data.tolist()
        with tempfile.TemporaryDirectory() as td:
            path = model.save(os.path.join(td, "mlp.aur"))
            model2 = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))
            model2.load(path)
            out2 = model2(x).data.tolist()
        self.assertEqual(out1, out2)

    def test_conv2d(self):
        """Conv2d 前向输出形状。"""
        conv = nn.Conv2d(1, 4, kernel_size=3)
        x = Variable(Tensor.zeros((2, 1, 5, 5)))
        out = conv(x)
        # (H - k)/stride + 1 = (5-3)/1 + 1 = 3
        self.assertEqual(out.shape, (2, 4, 3, 3))

    def test_lstm(self):
        """单层 LSTM 前向输出形状。"""
        lstm = nn.LSTM(3, 4, batch_first=True)
        x = Variable(Tensor.zeros((2, 5, 3)))
        out, (h, c) = lstm(x)
        self.assertEqual(out.shape, (2, 5, 4))
        self.assertEqual(h.shape, (2, 4))


# ===========================================================================
# 4. Data
# ===========================================================================
class TestAuroraData(unittest.TestCase):
    """AuroraData 数据处理库。"""

    def _sample_df(self):
        return DataFrame([
            {"name": "Alice", "age": 25, "score": 88.0, "city": "BJ"},
            {"name": "Bob", "age": 30, "score": 92.5, "city": "SH"},
            {"name": "Carol", "age": None, "score": 79.0, "city": "BJ"},
            {"name": "Dave", "age": 25, "score": None, "city": "SZ"},
        ])

    def test_dataframe_creation(self):
        """DataFrame 构造,验证 shape / columns。"""
        df = self._sample_df()
        self.assertEqual(df.shape, (4, 4))
        self.assertEqual(df.columns, ["name", "age", "score", "city"])

    def test_dataframe_csv_io(self):
        """写入 CSV 再读取,数据一致。"""
        df = self._sample_df()
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "roundtrip.csv")
            df.to_csv(path, index=False)
            df2 = DataFrame.read_csv(path)
        self.assertEqual(df2.shape, df.shape)
        self.assertEqual(df2["name"], ["Alice", "Bob", "Carol", "Dave"])

    def test_dataframe_cleaning(self):
        """dropna / fillna / filter。"""
        df = self._sample_df()
        dropped = df.dropna()
        # 仅 Alice/Bob 两行无缺失
        self.assertEqual(dropped.shape[0], 2)
        # fillna(mean) 用均值填补缺失
        filled = df.fillna(method="mean")
        self.assertTrue(all(v is not None for v in filled["age"]))
        # filter 保留 city == BJ 的行
        bj = df.filter(lambda r: r["city"] == "BJ")
        self.assertEqual(bj.shape[0], 2)

    def test_dataframe_groupby(self):
        """groupby + mean / sum 聚合。"""
        df = self._sample_df().dropna()
        g = df.groupby("city").mean()
        rows = g.to_dict(orient="records")
        bj_row = [r for r in rows if r["city"] == "BJ"][0]
        # BJ 只有 Alice: score=88.0
        self.assertAlmostEqual(bj_row["score"], 88.0)
        self.assertEqual(g.shape[0], 2)

    def test_dataloader(self):
        """DataLoader 迭代,验证 batch 大小与 shuffle 可复现。"""
        feats = [[float(i), float(i) * 2.0] for i in range(10)]
        labels = [i % 2 for i in range(10)]
        ds = Dataset(feats, labels=labels)
        loader = DataLoader(ds, batch_size=3, shuffle=True, seed=42)
        self.assertEqual(len(loader), 4)  # ceil(10/3)
        batches = list(loader)
        sizes = [len(b["features"]) for b in batches]
        self.assertEqual(sizes, [3, 3, 3, 1])
        self.assertTrue(all("labels" in b for b in batches))
        # seed 可复现
        again = list(DataLoader(ds, batch_size=3, shuffle=True, seed=42))
        self.assertEqual(
            [b["features"] for b in batches],
            [b["features"] for b in again])

    def test_scalers(self):
        """StandardScaler / MinMaxScaler fit_transform。"""
        X = [[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]]
        std = StandardScaler().fit_transform(X)
        # 第一列均值为 0
        self.assertAlmostEqual(sum(r[0] for r in std) / 3.0, 0.0, places=5)
        mm = MinMaxScaler().fit_transform([[1.0], [5.0], [9.0]])
        self.assertAlmostEqual(mm[0][0], 0.0)
        self.assertAlmostEqual(mm[-1][0], 1.0)


# ===========================================================================
# 5. Agent
# ===========================================================================
class _FakeLLM:
    """不发网络请求的假 LLM,仅用于测试 Chain 结构。"""
    provider = "fake"

    def chat(self, prompt, system=None, temperature=None):
        return "ECHO:" + prompt


class TestAuroraAgent(unittest.TestCase):
    """AuroraAgent LLM Agent 框架(仅结构测试,不调用真实 API)。"""

    def test_prompt_template(self):
        """PromptTemplate 变量替换。"""
        t = PromptTemplate("你好,{name}!今天是{day}。",
                            variables=["name", "day"])
        self.assertEqual(t.format(name="元铎", day="周二"),
                         "你好,元铎!今天是周二。")
        # 自动提取变量
        t2 = PromptTemplate("值是 {v}")
        self.assertEqual(t2.variables, ["v"])

    def test_tool_registry(self):
        """Tool 注册与查找。"""
        reg = ToolRegistry()

        def add(a: int, b: int) -> int:
            """两数相加"""
            return a + b

        tool = Tool("add", add, "两数相加")
        reg.register(tool)
        found = reg.lookup("add")
        self.assertIsNotNone(found)
        self.assertEqual(found.run(a=1, b=2), 3)
        self.assertIsNone(reg.lookup("nonexistent"))

    def test_conversation_memory(self):
        """ConversationMemory add / get_recent。"""
        mem = ConversationMemory()
        mem.add("user", "你好")
        mem.add("assistant", "你好呀")
        self.assertEqual(len(mem), 2)
        recent = mem.get_recent(1)
        self.assertEqual(recent[0]["role"], "assistant")
        self.assertEqual(recent[0]["content"], "你好呀")

    def test_llm_chain(self):
        """LLMChain 基本结构(用假 LLM,不调真实 API)。"""
        chain = LLMChain("问题: {q}", llm=_FakeLLM())
        out = chain.run(q="1+1=?")
        self.assertTrue(out.startswith("ECHO:"))
        # Agent 可注册工具且不触发网络调用
        agent = Agent(tools=[Tool("echo", lambda msg: msg, "回显")],
                      llm=_FakeLLM())
        self.assertIn("echo", agent.tools)


# ===========================================================================
# 6. Inference
# ===========================================================================
def _make_simple_model():
    """构造 3 -> 4(relu) -> 2 的简单模型。"""
    layer1 = {
        "type": "linear", "in": 3, "out": 4, "activation": "relu",
        "W": [[0.1, 0.2, 0.3],
              [0.4, 0.5, 0.6],
              [-0.1, -0.2, -0.3],
              [0.7, 0.8, 0.9]],
        "b": [0.0] * 4,
    }
    layer2 = {
        "type": "linear", "in": 4, "out": 2, "activation": None,
        "W": [[1.0, 0.0, 0.5, 0.2],
              [0.2, 0.3, 0.1, -0.4]],
        "b": [0.0] * 2,
    }
    return SimpleAuroraModel([layer1, layer2],
                             hyperparams={"lr": 0.01},
                             metadata={"name": "demo"})


class TestAuroraInference(unittest.TestCase):
    """AuroraInference 模型推理引擎。"""

    def test_inference_engine(self):
        """创建引擎、加载模型、推理并记录延迟。"""
        m = _make_simple_model()
        out = m.infer([1.0, 1.0, 1.0])
        self.assertEqual(len(out), 2)
        with tempfile.TemporaryDirectory() as td:
            path = save_model(m, os.path.join(td, "demo.aur"))
            engine = InferenceEngine(path)
            self.assertEqual(engine.model_format, "aur")
            pred = engine.predict([1.0, 1.0, 1.0])
            self.assertEqual(len(pred), 2)
            self.assertGreaterEqual(engine.last_latency_ms, 0.0)
            summary = engine.summary()
            self.assertEqual(summary["total_params"], (3 * 4 + 4) + (4 * 2 + 2))

    def test_model_save_load(self):
        """save_model / load_model round-trip 预测一致。"""
        m = _make_simple_model()
        expected = m.infer([1.0, 1.0, 1.0])
        with tempfile.TemporaryDirectory() as td:
            path = save_model(m, os.path.join(td, "demo.aur"))
            loaded = load_model(path)
            actual = loaded.infer([1.0, 1.0, 1.0])
        for a, b in zip(expected, actual):
            self.assertAlmostEqual(a, b, places=6)

    def test_quantizer(self):
        """int8 量化,精度损失在可接受范围。"""
        m = _make_simple_model()
        expected = m.infer([1.0, 1.0, 1.0])
        qmodel = Quantizer(precision="int8").quantize(m)
        qout = qmodel.infer([1.0, 1.0, 1.0])
        max_err = max(abs(a - b) for a, b in zip(expected, qout))
        self.assertLess(max_err, 0.5)

    def test_inference_server(self):
        """启动临时端口服务器,测试 /health 端点后关闭。"""
        m = _make_simple_model()
        with tempfile.TemporaryDirectory() as td:
            path = save_model(m, os.path.join(td, "demo.aur"))
            engine = InferenceEngine(path)
            server = InferenceServer(engine, host="127.0.0.1", port=0)
            addr = server.start()
            try:
                with urllib.request.urlopen(addr + "/health", timeout=5) as r:
                    hb = json.loads(r.read().decode("utf-8"))
                self.assertEqual(hb["status"], "ok")
            finally:
                server.stop()


if __name__ == "__main__":
    unittest.main(verbosity=2)
