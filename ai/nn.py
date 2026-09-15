#!/usr/bin/env python3
# Aurora v3.0.0 AI Engine
"""nn.py — AuroraNN 神经网络 DSL.

在 :mod:`ai.autograd` 之上提供高层神经网络 API：``Module`` 基类、
常见层（Linear / Conv2d / LSTM / 激活 / Dropout / BatchNorm1d）、
``Sequential`` 容器、常用损失函数以及模型参数的 JSON 保存 / 加载。

所有层都是可调用对象，前向计算返回新的 :class:`~ai.autograd.Variable`，
训练时通过反向传播自动求导。
"""

import json
import math
import random

from .tensor import Tensor, _prod
from .autograd import Variable


# ---------------------------------------------------------------------------
# Module 基类
# ---------------------------------------------------------------------------
class Module:
    """所有神经网络层 / 模型的基类。

    子类应在 ``__init__`` 中通过 :meth:`register_parameter` 登记可训练参数，
    并实现 :meth:`forward`。调用实例本身即执行前向计算。
    """

    def __init__(self):
        self._params = []      # list[Variable]
        self._modules = []     # list[Module]
        self._training = True

    # ------------------------------------------------------------------ #
    # 注册
    # ------------------------------------------------------------------ #
    def register_parameter(self, p):
        """把一个 Variable 登记为可训练参数。"""
        self._params.append(p)
        return p

    def add_module(self, module):
        """把子模块加入本模块（其参数会自动纳入 parameters()）。"""
        self._modules.append(module)
        return module

    # ------------------------------------------------------------------ #
    # 参数收集
    # ------------------------------------------------------------------ #
    def parameters(self):
        """递归返回所有可训练参数列表。"""
        params = list(self._params)
        for m in self._modules:
            params.extend(m.parameters())
        return params

    # ------------------------------------------------------------------ #
    # 训练 / 评估模式
    # ------------------------------------------------------------------ #
    def train(self):
        """切换到训练模式（Dropout / BatchNorm 生效）。"""
        self._training = True
        for m in self._modules:
            m.train()

    def eval(self):
        """切换到评估模式。"""
        self._training = False
        for m in self._modules:
            m.eval()

    # ------------------------------------------------------------------ #
    # 前向
    # ------------------------------------------------------------------ #
    def forward(self, x):  # pragma: no cover - 抽象
        raise NotImplementedError

    def __call__(self, *args):
        return self.forward(*args)

    # ------------------------------------------------------------------ #
    # 保存 / 加载
    # ------------------------------------------------------------------ #
    def save(self, path):
        """把所有参数序列化为 JSON（.aur）。"""
        if not path.endswith(".aur"):
            path += ".aur"
        state = []
        for p in self.parameters():
            state.append({
                "shape": list(p.data.shape),
                "data": list(p.data.data),
            })
        with open(path, "w") as f:
            json.dump(state, f)
        return path

    def load(self, path):
        """从 JSON 文件按顺序读回参数。"""
        with open(path, "r") as f:
            state = json.load(f)
        params = self.parameters()
        if len(state) != len(params):
            raise ValueError(
                "保存的参数数量 (%d) 与当前模型 (%d) 不匹配"
                % (len(state), len(params)))
        for p, s in zip(params, state):
            p.data = Tensor._from_flat(s["data"], tuple(s["shape"]), "float32")


# ---------------------------------------------------------------------------
# 线性层
# ---------------------------------------------------------------------------
class Linear(Module):
    """全连接层：y = x @ W.T + b。

    Parameters
    ----------
    in_features, out_features : int
        输入 / 输出维度。weight 形状 (out_features, in_features)。
    bias : bool
        是否使用偏置。
    """

    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        # Xavier 初始化
        scale = math.sqrt(2.0 / (in_features + out_features))
        self.weight = self.register_parameter(
            Variable(Tensor.randn((out_features, in_features)) * scale,
                     requires_grad=True))
        if bias:
            self.bias = self.register_parameter(
                Variable(Tensor.zeros((out_features,)), requires_grad=True))
        else:
            self.bias = None

    def forward(self, x):
        out = x @ self.weight.T
        if self.bias is not None:
            out = out + self.bias
        return out


# ---------------------------------------------------------------------------
# 激活函数层
# ---------------------------------------------------------------------------
class ReLU(Module):
    """ReLU 激活层。"""

    def forward(self, x):
        return x.relu()


class Sigmoid(Module):
    """Sigmoid 激活层。"""

    def forward(self, x):
        return x.sigmoid()


class Tanh(Module):
    """Tanh 激活层。"""

    def forward(self, x):
        return x.tanh()


class LeakyReLU(Module):
    """Leaky ReLU：x>0 时为 x，否则为 ``negative_slope * x``。"""

    def __init__(self, negative_slope=0.01):
        super().__init__()
        self.negative_slope = negative_slope

    def forward(self, x):
        # max(0,x) + slope * max(0,-x)
        return x.relu() + (-x).relu() * self.negative_slope


class Softmax(Module):
    """沿 ``dim`` 的 softmax（常用于输出层）。"""

    def __init__(self, dim=-1):
        super().__init__()
        self.dim = dim

    def forward(self, x):
        return Variable(x.data.softmax(dim=self.dim), requires_grad=x.requires_grad)


# ---------------------------------------------------------------------------
# Dropout / Flatten / BatchNorm
# ---------------------------------------------------------------------------
class Dropout(Module):
    """训练时以概率 ``p`` 随机置零，评估时直通。"""

    def __init__(self, p=0.5):
        super().__init__()
        self.p = p

    def forward(self, x):
        if not self._training or self.p <= 0.0:
            return x
        mask = [1.0 if random.random() > self.p else 0.0 for _ in range(x.data.size)]
        mask_t = Variable(Tensor._from_flat(mask, x.data.shape, "float32"))
        return x * mask_t / (1.0 - self.p)


class Flatten(Module):
    """把除 batch 维之外的所有维展平。"""

    def forward(self, x):
        batch = x.shape[0]
        return x.reshape(batch, -1)


class BatchNorm1d(Module):
    """简化版 1D 批归一化。

    训练时使用当前 batch 的均值 / 方差并滑动更新 running 统计量；
    评估时使用 running 均值 / 方差。
    """

    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super().__init__()
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum
        self.gamma = self.register_parameter(
            Variable(Tensor.ones((num_features,)), requires_grad=True))
        self.beta = self.register_parameter(
            Variable(Tensor.zeros((num_features,)), requires_grad=True))
        self.registered_mean = Tensor.zeros((num_features,))
        self.registered_var = Tensor.ones((num_features,))

    def forward(self, x):
        if self._training:
            mean = x.mean(axis=0)
            centered = x - mean
            var = (centered * centered).mean(axis=0)
            # 更新 running 统计量（用纯 Tensor，不进图）
            self.registered_mean = (
                self.registered_mean * (1 - self.momentum)
                + mean.data * self.momentum)
            self.registered_var = (
                self.registered_var * (1 - self.momentum)
                + var.data * self.momentum)
        else:
            mean = Variable(self.registered_mean, requires_grad=False)
            var = Variable(self.registered_var, requires_grad=False)
        x_hat = (x - mean) / (var + self.eps).sqrt()
        return self.gamma * x_hat + self.beta


# ---------------------------------------------------------------------------
# Conv2d（im2col + matmul）
# ---------------------------------------------------------------------------
class Conv2d(Module):
    """简化版 2D 卷积，使用 im2col 展开后做矩阵乘法。

    Parameters
    ----------
    in_channels, out_channels : int
    kernel_size : int
        卷积核边长（正方形）。
    stride, padding : int
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.k = kernel_size
        self.stride = stride
        self.padding = padding
        scale = math.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        self.weight = self.register_parameter(
            Variable(Tensor.randn((out_channels, in_channels, kernel_size,
                                   kernel_size)) * scale, requires_grad=True))
        self.bias = self.register_parameter(
            Variable(Tensor.zeros((out_channels,)), requires_grad=True))

    def forward(self, x):
        # x: (N, C, H, W)
        N, C, H, W = x.shape
        k = self.k
        pad = self.padding
        stride = self.stride
        oh = (H + 2 * pad - k) // stride + 1
        ow = (W + 2 * pad - k) // stride + 1

        # im2col：构造 (C*k*k, N*oh*ow) 的列矩阵
        col_len = C * k * k
        n_col = N * oh * ow
        cols = [[0.0] * n_col for _ in range(col_len)]
        out_idx = 0
        d = x.data.data  # 底层扁平 list
        for n in range(N):
            for i in range(oh):
                for j in range(ow):
                    ii = i * stride - pad
                    jj = j * stride - pad
                    row = 0
                    for c in range(C):
                        for di in range(k):
                            for dj in range(k):
                                h = ii + di
                                w = jj + dj
                                if 0 <= h < H and 0 <= w < W:
                                    cols[row][out_idx] = d[
                                        ((n * C + c) * H + h) * W + w]
                                row += 1
                    out_idx += 1
        col_tensor = Tensor(cols)  # (col_len, n_col)
        w_mat = self.weight.reshape(self.out_channels, col_len)  # (out, col_len)
        out_mat = w_mat @ col_tensor  # (out, n_col)

        # 把 (out, n_col) 重排回 (N, out, oh, ow)
        out_flat = out_mat.data.data
        final = [0.0] * (N * self.out_channels * oh * ow)
        n_col_total = n_col
        for oc in range(self.out_channels):
            for kk in range(n_col_total):
                n = kk // (oh * ow)
                rem = kk % (oh * ow)
                i = rem // ow
                j = rem % ow
                final[((n * self.out_channels + oc) * oh + i) * ow + j] = (
                    out_flat[oc * n_col_total + kk] + self.bias.data.data[oc])
        return Variable(
            Tensor._from_flat(final, (N, self.out_channels, oh, ow), "float32"),
            requires_grad=x.requires_grad)


# ---------------------------------------------------------------------------
# LSTM（单层）
# ---------------------------------------------------------------------------
class LSTM(Module):
    """简化版单层 LSTM（四个门：i/f/o/g）。

    Parameters
    ----------
    input_size, hidden_size : int
    batch_first : bool
        若为 True，输入形状为 (N, L, input_size)；否则 (L, N, input_size)。
    """

    def __init__(self, input_size, hidden_size, num_layers=1, batch_first=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.batch_first = batch_first
        H = hidden_size
        # 输入隐藏门 / 隐藏隐藏门：一次计算四个门
        self.W_ih = self.register_parameter(
            Variable(Tensor.randn((4 * H, input_size)) * math.sqrt(1.0 / input_size),
                     requires_grad=True))
        self.W_hh = self.register_parameter(
            Variable(Tensor.randn((4 * H, H)) * math.sqrt(1.0 / H),
                     requires_grad=True))
        self.b_ih = self.register_parameter(
            Variable(Tensor.zeros((4 * H,)), requires_grad=True))
        self.b_hh = self.register_parameter(
            Variable(Tensor.zeros((4 * H,)), requires_grad=True))

    def forward(self, x, hidden=None):
        if self.batch_first:
            # x: (N, L, F) -> (L, N, F)
            x = x.transpose((1, 0, 2))
        L, N, F = x.shape
        H = self.hidden_size
        if hidden is None:
            h = Variable(Tensor.zeros((N, H)), requires_grad=False)
            c = Variable(Tensor.zeros((N, H)), requires_grad=False)
        else:
            h, c = hidden

        outputs = []
        for t in range(L):
            x_t = x[t]  # (N, F)
            gates = x_t @ self.W_ih.T + self.b_ih + h @ self.W_hh.T + self.b_hh
            i = gates[:, 0:H].sigmoid()
            f = gates[:, H:2 * H].sigmoid()
            g = gates[:, 2 * H:3 * H].tanh()
            o = gates[:, 3 * H:4 * H].sigmoid()
            c = f * c + i * g
            h = o * c.tanh()
            outputs.append(h)
        # 沿时间维堆叠：(L, N, H)
        stacked = outputs[0].reshape(1, N, H)
        for t in range(1, L):
            stacked = stacked.concat(outputs[t].reshape(1, N, H), axis=0)
        if self.batch_first:
            stacked = stacked.transpose((1, 0, 2))
        return stacked, (h, c)


# ---------------------------------------------------------------------------
# Sequential 容器
# ---------------------------------------------------------------------------
class Sequential(Module):
    """按顺序执行各层的容器。"""

    def __init__(self, *layers):
        super().__init__()
        self._layers = []
        for layer in layers:
            self.add(layer)

    def add(self, layer):
        """动态添加一层。"""
        self._layers.append(layer)
        self.add_module(layer)
        return layer

    def forward(self, x):
        for layer in self._layers:
            x = layer(x)
        return x

    def __getitem__(self, idx):
        return self._layers[idx]

    def __len__(self):
        return len(self._layers)


# ---------------------------------------------------------------------------
# 损失函数
# ---------------------------------------------------------------------------
class MSELoss(Module):
    """均方误差：mean((pred - target)^2)。"""

    def forward(self, pred, target):
        return ((pred - target) * (pred - target)).mean()


class CrossEntropyLoss(Module):
    """交叉熵损失：输入 logits (N, C) 与类别索引 (N,)。"""

    def forward(self, logits, targets):
        # 数值稳定 log_softmax（纯 Python 范围下不减去最大值也可接受）
        shifted = logits - logits.max(axis=1, keepdims=True)
        log_sum_exp = shifted.exp().sum(axis=1, keepdims=True).log()
        log_probs = shifted - log_sum_exp  # (N, C)
        # 用 one-hot 选择对应类别，全程保持可微
        N, C = logits.shape
        one_hot_t = Variable(one_hot(targets.tolist(), C))
        nll = -(log_probs * one_hot_t).sum()
        return nll / float(N)


class BCELoss(Module):
    """二元交叉熵：pred 已为 sigmoid 概率，target 为 0/1。"""

    def forward(self, pred, target):
        # 全程用 Variable 运算保持可微
        eps = 1e-9
        loss = -(target * pred.log() + (1.0 - target) * (1.0 - pred + eps).log())
        return loss.mean()


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def one_hot(indices, num_classes):
    """把类别索引转成 one-hot 张量。"""
    flat = []
    for idx in indices:
        row = [0.0] * num_classes
        row[int(idx)] = 1.0
        flat.extend(row)
    return Tensor._from_flat(flat, (len(indices), num_classes), "float32")


def init_weights(model):
    """对模型中所有二维参数做 Xavier 风格初始化。"""
    for p in model.parameters():
        if p.data.ndim == 2:
            out_f, in_f = p.data.shape
            scale = math.sqrt(2.0 / (in_f + out_f))
            p.data = Tensor.randn((out_f, in_f)) * scale
        elif p.data.ndim == 1:
            p.data = Tensor.zeros(p.data.shape)


# ---------------------------------------------------------------------------
# 冒烟测试
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from .autograd import SGD

    # 用 MSELoss 演示端到端训练
    X = Tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    model2 = Sequential(Linear(2, 8), ReLU(), Linear(8, 1))
    mse = MSELoss()
    opt2 = SGD(model2.parameters(), lr=0.05)
    targets = Variable(Tensor([[0.0], [1.0], [1.0], [0.0]]))
    for step_i in range(300):
        pred = model2(Variable(X))
        loss = mse(pred, targets)
        opt2.zero_grad()
        loss.backward()
        opt2.step()
    print("final MSE loss =", loss.item())
    print("predictions =", model2(Variable(X)).data.tolist())

    # save / load
    path = model2.save("/tmp/aurora_test.aur")
    model2b = Sequential(Linear(2, 8), ReLU(), Linear(8, 1))
    model2b.load(path)
    print("after load predictions =", model2b(Variable(X)).data.tolist())

    # one_hot
    print("one_hot =", one_hot([0, 2, 1], 3).tolist())

    print("OK nn.py")
