#!/usr/bin/env python3
# Aurora v3.0.0 AI Engine
"""autograd.py — AuroraAutograd 自动微分引擎.

基于动态计算图的反向自动微分。每个 :class:`Variable` 包装一个底层
:class:`~ai.tensor.Tensor`，并在需要时记录它的父节点与 ``grad_fn``。
调用 :meth:`Variable.backward` 时，先对参与运算的节点做拓扑排序，
再按依赖反序执行每个节点的局部反向函数，沿链式法则累积梯度。

优化器提供 SGD（带动量）与 Adam 两种标准实现，并通过 ``no_grad``
上下文管理器在推理时关闭梯度追踪。
"""

import math

from .tensor import Tensor, _prod


# ---------------------------------------------------------------------------
# no_grad 上下文：全局计数器，嵌套安全
# ---------------------------------------------------------------------------
_no_grad_depth = 0


class no_grad:
    """推理时使用的上下文管理器，关闭梯度追踪。"""

    def __enter__(self):
        global _no_grad_depth
        _no_grad_depth += 1
        return self

    def __exit__(self, *args):
        global _no_grad_depth
        _no_grad_depth -= 1
        return False


def _grad_enabled():
    return _no_grad_depth == 0


# ---------------------------------------------------------------------------
# 工具：把上游梯度“广播回去”
# ---------------------------------------------------------------------------
def _unbroadcast(grad, target_shape):
    """把从广播运算得到的 grad 规约回 target_shape。

    规则：先把多出的前导维按 axis=0 求和；再对 target 中大小为 1 的维度求和。
    """
    grad = grad
    while len(grad.shape) > len(target_shape):
        grad = grad.sum(axis=0)
    for i in range(len(target_shape)):
        if target_shape[i] == 1 and grad.shape[i] != 1:
            grad = grad.sum(axis=i, keepdims=True)
    return grad


def _ones(shape):
    return Tensor.ones(shape)


# ---------------------------------------------------------------------------
# Variable：可微张量
# ---------------------------------------------------------------------------
class Variable:
    """可微张量：包装 :class:`Tensor`，并记录计算图中的边。

    Parameters
    ----------
    data : Tensor
        底层数值张量。
    requires_grad : bool
        是否需要在反向传播时累积梯度。
    """

    def __init__(self, data, requires_grad=False):
        if not isinstance(data, Tensor):
            data = Tensor(data)
        self.data = data
        self.requires_grad = requires_grad
        self.grad = None  # Variable 或 None
        self._parents = []  # list[Variable]
        self._backward_fn = None  # callable(grad_out: Tensor) -> list[Tensor]

    # ------------------------------------------------------------------ #
    # 构造辅助：前向计算后登记边
    # ------------------------------------------------------------------ #
    @classmethod
    def _build(cls, out_tensor, parents, backward_fn):
        requires_grad = _grad_enabled() and any(p.requires_grad for p in parents)
        out = cls(out_tensor, requires_grad=requires_grad)
        if requires_grad:
            out._parents = list(parents)
            out._backward_fn = backward_fn
        return out

    def detach(self):
        """返回脱离当前计算图的新 Variable（不共享梯度）。"""
        return Variable(self.data, requires_grad=False)

    # ------------------------------------------------------------------ #
    # 梯度累积
    # ------------------------------------------------------------------ #
    def _accumulate(self, g):
        if self.grad is None:
            self.grad = Variable(g, requires_grad=False)
        else:
            self.grad = Variable(self.grad.data + g, requires_grad=False)

    # ------------------------------------------------------------------ #
    # 反向传播
    # ------------------------------------------------------------------ #
    def backward(self, grad=None):
        """从当前节点反向传播，计算所有 ``requires_grad=True`` 节点的梯度。

        Parameters
        ----------
        grad : Tensor, optional
            上游梯度。若当前节点是标量（shape==()）且未提供，则默认为 1.0。
        """
        # 1. 拓扑排序：DFS
        topo = []
        visited = set()

        def visit(v):
            if id(v) in visited:
                return
            visited.add(id(v))
            for p in v._parents:
                visit(p)
            topo.append(v)

        visit(self)

        # 2. 初始梯度
        if grad is None:
            if self.shape != ():
                raise RuntimeError("对非标量 Variable 调用 backward 必须传入 grad")
            grad = Tensor(1.0)
        else:
            if not isinstance(grad, Tensor):
                grad = Tensor(grad)
        self._accumulate(grad)

        # 3. 反序执行每个节点的反向函数
        for v in reversed(topo):
            if v._backward_fn is None:
                continue
            upstream = v.grad.data  # Tensor
            parent_grads = v._backward_fn(upstream)
            for p, pg in zip(v._parents, parent_grads):
                if pg is not None and p.requires_grad:
                    p._accumulate(pg)

    # ------------------------------------------------------------------ #
    # 只读属性转发
    # ------------------------------------------------------------------ #
    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    # ------------------------------------------------------------------ #
    # 逐元素二元运算
    # ------------------------------------------------------------------ #
    def _coerce(self, other):
        if isinstance(other, Variable):
            return other
        if isinstance(other, Tensor):
            return Variable(other, requires_grad=False)
        return Variable(Tensor(other), requires_grad=False)

    def __add__(self, other):
        other = self._coerce(other)
        out = self.data + other.data

        def backward(grad):
            return [_unbroadcast(grad, self.shape), _unbroadcast(grad, other.shape)]

        return self._build(out, [self, other], backward)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._coerce(other)
        out = self.data - other.data

        def backward(grad):
            return [_unbroadcast(grad, self.shape),
                    _unbroadcast(grad.mul(-1.0), other.shape)]

        return self._build(out, [self, other], backward)

    def __rsub__(self, other):
        other = self._coerce(other)
        out = other.data - self.data

        def backward(grad):
            return [_unbroadcast(grad.mul(-1.0), self.shape),
                    _unbroadcast(grad, other.shape)]

        return self._build(out, [self, other], backward)

    def __mul__(self, other):
        other = self._coerce(other)
        out = self.data * other.data

        def backward(grad):
            g_a = _unbroadcast(grad * other.data, self.shape)
            g_b = _unbroadcast(grad * self.data, other.shape)
            return [g_a, g_b]

        return self._build(out, [self, other], backward)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._coerce(other)
        a, b = self.data, other.data
        out = a / b

        def backward(grad):
            g_a = _unbroadcast(grad / b, self.shape)
            g_b = _unbroadcast(grad * a / (b * b) * -1.0, other.shape)
            return [g_a, g_b]

        return self._build(out, [self, other], backward)

    def __matmul__(self, other):
        other = self._coerce(other)
        A, B = self.data, other.data
        out = A @ B

        def backward(grad):
            # dA = grad @ B.T, dB = A.T @ grad
            g_a = grad @ B.T
            g_b = A.T @ grad
            # 若输入是一维向量，输出也会被 squeeze，需要把梯度形状补回去
            if A.ndim == 1 and g_a.shape != A.shape:
                g_a = g_a.reshape(A.shape) if _prod(g_a.shape) == A.size else g_a
            if B.ndim == 1 and g_b.shape != B.shape:
                g_b = g_b.reshape(B.shape) if _prod(g_b.shape) == B.size else g_b
            return [g_a, g_b]

        return self._build(out, [self, other], backward)

    def __neg__(self):
        out = self.data * -1.0

        def backward(grad):
            return [grad * -1.0]

        return self._build(out, [self], backward)

    # ------------------------------------------------------------------ #
    # 一元函数
    # ------------------------------------------------------------------ #
    def exp(self):
        x = self.data
        s = x.exp()

        def backward(grad):
            return [grad * s]

        return self._build(s, [self], backward)

    def log(self):
        x = self.data
        out = x.log()

        def backward(grad):
            return [grad / x]

        return self._build(out, [self], backward)

    def sin(self):
        x = self.data
        out = x.sin()

        def backward(grad):
            return [grad * x.cos()]

        return self._build(out, [self], backward)

    def cos(self):
        x = self.data
        out = x.cos()

        def backward(grad):
            return [grad * x.sin() * -1.0]

        return self._build(out, [self], backward)

    def sigmoid(self):
        x = self.data
        s = x.sigmoid()

        def backward(grad):
            return [grad * s * (1.0 - s)]

        return self._build(s, [self], backward)

    def relu(self):
        x = self.data
        out = x.relu()

        def backward(grad):
            mask = Tensor._from_flat(
                [1.0 if v > 0 else 0.0 for v in x.data], x.shape, "float32"
            )
            return [grad * mask]

        return self._build(out, [self], backward)

    def tanh(self):
        x = self.data
        t = x.tanh()

        def backward(grad):
            return [grad * (1.0 - t * t)]

        return self._build(t, [self], backward)

    def sqrt(self):
        x = self.data
        s = x.sqrt()

        def backward(grad):
            return [grad / (s * 2.0)]

        return self._build(s, [self], backward)

    # ------------------------------------------------------------------ #
    # 归约
    # ------------------------------------------------------------------ #
    def sum(self, axis=None, keepdims=False):
        x = self.data
        out = x.sum(axis=axis, keepdims=keepdims)

        def backward(grad):
            if axis is None:
                # 标量梯度广播到全体
                return [grad * _ones(x.shape)]
            axes = axis if isinstance(axis, (tuple, list)) else (axis,)
            axes = tuple(a + x.ndim if a < 0 else a for a in axes)
            view_shape = [1 if i in axes else x.shape[i] for i in range(x.ndim)]
            g = grad.reshape(view_shape)
            return [g * _ones(x.shape)]

        return self._build(out, [self], backward)

    def mean(self, axis=None, keepdims=False):
        x = self.data
        out = x.mean(axis=axis, keepdims=keepdims)
        if axis is None:
            n = x.size
        else:
            axes = axis if isinstance(axis, (tuple, list)) else (axis,)
            n = 1
            for a in axes:
                n *= x.shape[a]

        def backward(grad):
            if axis is None:
                return [grad * _ones(x.shape) / float(n)]
            axes_t = tuple(a + x.ndim if a < 0 else a for a in axes)
            view_shape = [1 if i in axes_t else x.shape[i] for i in range(x.ndim)]
            g = grad.reshape(view_shape)
            return [g * _ones(x.shape) / float(n)]

        return self._build(out, [self], backward)

    def max(self, axis=None, keepdims=False):
        """沿 axis 取最大值（用于数值稳定的 log_softmax）。"""
        x = self.data
        out = x.max(axis=axis, keepdims=keepdims)

        def backward(grad):
            g = [0.0] * x.size
            if axis is None:
                flat = x.data
                idx = max(range(len(flat)), key=lambda i: flat[i])
                g[idx] = grad.item()
                return [Tensor._from_flat(g, x.shape, "float32")]
            axes = (axis,) if isinstance(axis, int) else tuple(axis)
            axes = tuple(a + x.ndim if a < 0 else a for a in axes)
            from .tensor import _strides
            x_strides = _strides(x.shape)
            out_strides = _strides(out.shape)
            # 遍历每个输出元素，定位其在输入中的 argmax 位置
            for oflat in range(out.size):
                rem = oflat
                ocoords = []
                for k in range(len(out.shape)):
                    ocoords.append(rem // out_strides[k])
                    rem %= out_strides[k]
                # 在被规约的轴上枚举，找最大值
                best_val = float("-inf")
                best_input_flat = -1
                def enum(dim, base):
                    nonlocal best_val, best_input_flat
                    if dim == x.ndim:
                        v = x.data[base]
                        if v > best_val:
                            best_val = v
                            best_input_flat = base
                        return
                    if dim in axes:
                        for v in range(x.shape[dim]):
                            enum(dim + 1, base + v * x_strides[dim])
                    else:
                        # 非规约轴：固定为输出坐标
                        coord = ocoords[dim] if keepdims else \
                            ocoords[sum(1 for a in axes if a < dim)]
                        enum(dim + 1, base + coord * x_strides[dim])
                enum(0, 0)
                g[best_input_flat] += grad.data[oflat]
            return [Tensor._from_flat(g, x.shape, "float32")]

        return self._build(out, [self], backward)
    def transpose(self, axes=None):
        x = self.data
        out = x.transpose(axes=axes)
        n = x.ndim
        if axes is None:
            axes_inv = list(range(n - 1, -1, -1))
        else:
            inv = [0] * n
            for i, a in enumerate(axes):
                inv[a] = i
            axes_inv = inv

        def backward(grad):
            return [grad.transpose(axes_inv)]

        return self._build(out, [self], backward)

    @property
    def T(self):
        return self.transpose()

    def reshape(self, *shape):
        x = self.data
        out = x.reshape(*shape)

        def backward(grad):
            return [grad.reshape(x.shape)]

        return self._build(out, [self], backward)

    def concat(self, other, axis=0):
        """沿 axis 拼接两个 Variable。"""
        other = self._coerce(other)
        out = self.data.concat(other.data, axis=axis)
        self_len = self.data.shape[axis]

        def backward(grad):
            # 按 axis 切分梯度
            sl = [slice(None)] * grad.ndim
            sl[axis] = slice(0, self_len)
            g_self = grad[tuple(sl)]
            sl[axis] = slice(self_len, None)
            g_other = grad[tuple(sl)]
            return [g_self, g_other]

        return self._build(out, [self, other], backward)

    # ------------------------------------------------------------------ #
    # 其它
    # ------------------------------------------------------------------ #
    def __getitem__(self, key):
        """索引 / 切片。简化实现：返回不带梯度追踪的视图。"""
        return Variable(self.data[key], requires_grad=False)

    def item(self):
        """标量取值。"""
        return self.data.item()

    def tolist(self):
        return self.data.tolist()

    def __repr__(self):
        return "Variable(data=%r, requires_grad=%s)" % (
            self.data.tolist(), self.requires_grad)


# ---------------------------------------------------------------------------
# 优化器
# ---------------------------------------------------------------------------
class Optimizer:
    """优化器基类，定义通用接口。"""

    def __init__(self, params):
        self.params = list(params)

    def zero_grad(self):
        """把所有参数的梯度清零。"""
        for p in self.params:
            p.grad = None

    def step(self):  # pragma: no cover - 抽象
        raise NotImplementedError


class SGD(Optimizer):
    """随机梯度下降优化器（带动量）。

    Parameters
    ----------
    params : list[Variable]
        待优化参数。
    lr : float
        学习率。
    momentum : float
        动量系数，0 表示不使用动量。
    """

    def __init__(self, params, lr=0.01, momentum=0.0):
        super().__init__(params)
        self.lr = lr
        self.momentum = momentum
        self._velocity = {}

    def step(self):
        for p in self.params:
            if p.grad is None:
                continue
            g = p.grad.data
            if self.momentum > 0:
                v_prev = self._velocity.get(id(p), None)
                if v_prev is None:
                    v = g.mul(-self.lr)
                else:
                    v = v_prev.mul(self.momentum) - g.mul(self.lr)
                self._velocity[id(p)] = v
                p.data = p.data + v
            else:
                p.data = p.data - g.mul(self.lr)


class Adam(Optimizer):
    """Adam 优化器（带偏差修正）。

    Parameters
    ----------
    params : list[Variable]
        待优化参数。
    lr : float
        学习率。
    betas : (float, float)
        一阶 / 二阶矩衰减系数。
    eps : float
        数值稳定小量。
    """

    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8):
        super().__init__(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.t = 0
        self._m = {}
        self._v = {}

    def step(self):
        self.t += 1
        for p in self.params:
            if p.grad is None:
                continue
            g = p.grad.data
            pid = id(p)
            m_prev = self._m.get(pid)
            v_prev = self._v.get(pid)
            if m_prev is None:
                m = g.mul(1.0 - self.beta1)
                v = (g * g).mul(1.0 - self.beta2)
            else:
                m = m_prev.mul(self.beta1) + g.mul(1.0 - self.beta1)
                v = v_prev.mul(self.beta2) + (g * g).mul(1.0 - self.beta2)
            self._m[pid] = m
            self._v[pid] = v
            # 偏差修正
            m_hat = m / (1.0 - self.beta1 ** self.t)
            v_hat = v / (1.0 - self.beta2 ** self.t)
            # 更新：p = p - lr * m_hat / (sqrt(v_hat) + eps)
            update = m_hat / (v_hat.sqrt() + self.eps)
            p.data = p.data - update.mul(self.lr)


# ---------------------------------------------------------------------------
# 冒烟测试
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 简单线性回归：y = 3x + 2，验证反向传播
    x = Variable(Tensor([[1.0], [2.0], [3.0], [4.0]]))
    y = Variable(Tensor([[5.0], [8.0], [11.0], [14.0]]))
    w = Variable(Tensor.randn((1, 1)), requires_grad=True)
    b = Variable(Tensor.zeros((1,)), requires_grad=True)

    opt = Adam([w, b], lr=0.1)
    for step_i in range(200):
        pred = x @ w + b
        loss = ((pred - y) * (pred - y)).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()

    print("w =", w.data.tolist(), " b =", b.data.tolist())
    print("loss =", loss.item())

    # 验证 sigmoid 梯度
    z = Variable(Tensor([0.0]), requires_grad=True)
    s = z.sigmoid().sum()
    s.backward()
    print("sigmoid'(0) =", z.grad.item(), "(期望 0.25)")

    # no_grad
    with no_grad():
        z2 = Variable(Tensor([1.0]), requires_grad=True)
        out = z2 * 2
        print("no_grad out.requires_grad =", out.requires_grad, "(期望 False)")

    print("OK autograd.py")
