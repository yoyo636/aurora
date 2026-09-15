#!/usr/bin/env python3
# Aurora v3.0.0 AI Engine
"""tensor.py — AuroraTensor 原生张量计算库.

Aurora AI 引擎的底层数值计算核心。所有数据以扁平化一维 list 存储，
通过 ``shape`` 与由此推导出的 ``strides`` 管理多维索引，避免依赖 numpy
即可完成广播、矩阵乘法、归约与逐元素函数运算。

设计要点
--------
* 内部存储：``self.data`` 始终是一个一维 list（行主序 / C-order）。
* strides[i] = prod(shape[i+1:])，即第 i 维上走一步需要跨越的元素数。
* 广播：两 shape 右对齐后逐维比较，相等或其一为 1 即可广播。
* numpy 为可选加速路径：``to_numpy`` / ``from_numpy`` 在可用时启用，
  小张量路径完全不依赖第三方库。
"""

import math
import random

try:  # 可选加速依赖；缺失时不影响纯 Python 路径
    import numpy as _np  # type: ignore
    _HAS_NUMPY = True
except Exception:  # pragma: no cover - numpy 可选
    _np = None
    _HAS_NUMPY = False


# ---------------------------------------------------------------------------
# 内部工具函数
# ---------------------------------------------------------------------------
def _prod(seq):
    """返回序列中所有元素的乘积（空序列返回 1）。"""
    out = 1
    for x in seq:
        out *= x
    return out


def _strides(shape):
    """根据 shape 计算行主序 strides：strides[i] = prod(shape[i+1:])。"""
    n = len(shape)
    strides = [1] * n
    for i in range(n - 2, -1, -1):
        strides[i] = strides[i + 1] * shape[i + 1]
    return tuple(strides)


def _list_shape(lst):
    """从嵌套 list 递归推断 shape。"""
    if isinstance(lst, (list, tuple)):
        if len(lst) == 0:
            return (0,)
        return (len(lst),) + _list_shape(lst[0])
    return ()


def _flatten(lst):
    """把嵌套 list 递归拍平成一维 list。"""
    out = []

    def rec(x):
        if isinstance(x, (list, tuple)):
            for y in x:
                rec(y)
        else:
            out.append(x)

    rec(lst)
    return out


def _nest(flat, shape):
    """把一维 flat 数据按 shape 重新组装成嵌套 list。"""
    if len(shape) == 0:
        return flat[0]
    if len(shape) == 1:
        return list(flat)
    size = _prod(shape[1:])
    return [_nest(flat[i * size:(i + 1) * size], shape[1:]) for i in range(shape[0])]


def _broadcast_shapes(s1, s2):
    """返回两个 shape 广播后的结果 shape，不可广播则抛 ValueError。"""
    n = max(len(s1), len(s2))
    a = (1,) * (n - len(s1)) + tuple(s1)
    b = (1,) * (n - len(s2)) + tuple(s2)
    out = []
    for i in range(n):
        if a[i] == b[i] or a[i] == 1 or b[i] == 1:
            out.append(max(a[i], b[i]))
        else:
            raise ValueError("无法广播的张量形状: %s 与 %s" % (s1, s2))
    return tuple(out)


def _bc_strides(input_shape, output_shape):
    """计算 input 到 output 广播时，每个输出维对应在 input flat 空间的步长。

    若 input 某维为 1（或该维缺失，视作 1），广播时该维不前进，步长为 0。
    """
    pad = len(output_shape) - len(input_shape)
    ishape = (1,) * pad + tuple(input_shape)
    istrides = _strides(ishape)
    result = []
    for k in range(len(output_shape)):
        result.append(0 if ishape[k] == 1 else istrides[k])
    return result


def _infer_dtype(flat):
    """根据扁平数据推断 dtype：含 float -> float32，否则 int64。"""
    for v in flat:
        if isinstance(v, float):
            return "float32"
    return "int64"


# ---------------------------------------------------------------------------
# Tensor 主体
# ---------------------------------------------------------------------------
class Tensor:
    """AuroraTensor：原生多维张量。

    Parameters
    ----------
    data : 嵌套 list 或扁平化 list
        张量数据。若同时传入 ``shape``，则 ``data`` 被视为已经拍平的一维序列。
    dtype : str, optional
        数据类型标记，如 ``'float32'`` / ``'int64'``。缺省时自动推断。
    shape : tuple, optional
        显式给出的形状；传入时 ``data`` 必须是一维 list 且长度等于 prod(shape)。
    """

    def __init__(self, data, dtype=None, *, shape=None):
        if shape is not None:
            self.shape = tuple(shape)
            self.data = list(data)
        else:
            if isinstance(data, (int, float)):
                self.shape = ()
                self.data = [data]
            else:
                self.shape = _list_shape(data)
                self.data = _flatten(data)
        if dtype is None:
            dtype = _infer_dtype(self.data)
        self.dtype = dtype
        self.ndim = len(self.shape)
        # 基本校验
        if self.data and _prod(self.shape) != len(self.data):
            raise ValueError(
                "shape %s 与元素数 %d 不匹配" % (self.shape, len(self.data))
            )

    # ------------------------------------------------------------------ #
    # 内部工厂：直接用 flat data + shape 构造（不重新推断）
    # ------------------------------------------------------------------ #
    @classmethod
    def _from_flat(cls, flat, shape, dtype=None):
        obj = cls.__new__(cls)
        obj.data = list(flat)
        obj.shape = tuple(shape)
        obj.ndim = len(obj.shape)
        obj.dtype = dtype or _infer_dtype(flat)
        return obj

    # ------------------------------------------------------------------ #
    # 构造类方法
    # ------------------------------------------------------------------ #
    @classmethod
    def zeros(cls, shape):
        """创建全 0 张量。"""
        shape = tuple(shape) if isinstance(shape, (list, tuple)) else (shape,)
        return cls._from_flat([0.0] * _prod(shape), shape, "float32")

    @classmethod
    def ones(cls, shape):
        """创建全 1 张量。"""
        shape = tuple(shape) if isinstance(shape, (list, tuple)) else (shape,)
        return cls._from_flat([1.0] * _prod(shape), shape, "float32")

    @classmethod
    def randn(cls, shape):
        """创建标准正态分布随机张量。"""
        shape = tuple(shape) if isinstance(shape, (list, tuple)) else (shape,)
        flat = [random.gauss(0.0, 1.0) for _ in range(_prod(shape))]
        return cls._from_flat(flat, shape, "float32")

    @classmethod
    def eye(cls, n):
        """创建 n×n 单位矩阵。"""
        flat = [0.0] * (n * n)
        for i in range(n):
            flat[i * n + i] = 1.0
        return cls._from_flat(flat, (n, n), "float32")

    @classmethod
    def arange(cls, n):
        """创建 [0, n) 的一维张量。"""
        return cls._from_flat([float(i) for i in range(n)], (n,), "float32")

    # ------------------------------------------------------------------ #
    # 转换接口
    # ------------------------------------------------------------------ #
    def item(self):
        """标量张量转为 Python number。"""
        if self.size != 1:
            raise ValueError("只有标量张量才能调用 item()，当前 shape=%s" % (self.shape,))
        return self.data[0]

    def tolist(self):
        """转回嵌套 Python list。"""
        return _nest(self.data, self.shape)

    @property
    def size(self):
        """元素总数。"""
        return len(self.data)

    @property
    def T(self):
        """2D 转置。"""
        return self.transpose()

    # ------------------------------------------------------------------ #
    # NumPy 互操作
    # ------------------------------------------------------------------ #
    @classmethod
    def from_numpy(cls, np_arr):
        """从 numpy ndarray 创建 Tensor（会拷贝数据）。"""
        if not _HAS_NUMPY:
            raise RuntimeError("当前环境没有安装 numpy")
        arr = _np.ascontiguousarray(np_arr)
        flat = arr.flatten().tolist()
        return cls._from_flat(flat, tuple(arr.shape), "float32")

    def to_numpy(self):
        """转为 numpy ndarray。"""
        if not _HAS_NUMPY:
            raise RuntimeError("当前环境没有安装 numpy")
        return _np.array(self.data, dtype=_np.float32).reshape(self.shape)

    # ------------------------------------------------------------------ #
    # 内部：把标量 / Tensor 统一成 Tensor
    # ------------------------------------------------------------------ #
    def _coerce(self, other):
        if isinstance(other, Tensor):
            return other
        if isinstance(other, (int, float)):
            return Tensor._from_flat([other], (), "float32")
        raise TypeError("不支持与 %s 运算" % type(other))

    # ------------------------------------------------------------------ #
    # 逐元素二元运算（支持广播）
    # ------------------------------------------------------------------ #
    def _elementwise_binary(self, other, op):
        other = self._coerce(other)
        out_shape = _broadcast_shapes(self.shape, other.shape)
        bc1 = _bc_strides(self.shape, out_shape)
        bc2 = _bc_strides(other.shape, out_shape)
        os = _strides(out_shape)
        out_size = _prod(out_shape)
        out = [0.0] * out_size
        d1 = self.data
        d2 = other.data
        for flat in range(out_size):
            idx = flat
            a_idx = 0
            b_idx = 0
            for k in range(len(out_shape)):
                s = os[k]
                d = idx // s
                idx %= s
                a_idx += d * bc1[k]
                b_idx += d * bc2[k]
            out[flat] = op(d1[a_idx], d2[b_idx])
        return Tensor._from_flat(out, out_shape, "float32")

    def add(self, other):
        """逐元素加法（支持标量与广播）。"""
        return self._elementwise_binary(other, lambda x, y: x + y)

    def sub(self, other):
        """逐元素减法（支持标量与广播）。"""
        return self._elementwise_binary(other, lambda x, y: x - y)

    def mul(self, other):
        """逐元素乘法（支持标量与广播）。"""
        return self._elementwise_binary(other, lambda x, y: x * y)

    def div(self, other):
        """逐元素除法（支持标量与广播）。"""
        return self._elementwise_binary(other, lambda x, y: x / y)

    # ------------------------------------------------------------------ #
    # 矩阵乘法
    # ------------------------------------------------------------------ #
    def matmul(self, other):
        """矩阵乘法 / 向量点积。

        支持：
        * 2D @ 2D：(M,K) @ (K,N) -> (M,N)
        * 1D @ 1D：(K,) @ (K,) -> 标量 ()
        * 2D @ 1D：(M,K) @ (K,) -> (M,)
        * 1D @ 2D：(K,) @ (K,N) -> (N,)
        """
        other = self._coerce(other)
        a, b = self, other

        # 处理一维向量情形
        if a.ndim == 1 and b.ndim == 1:
            if a.shape[0] != b.shape[0]:
                raise ValueError("向量点积维度不匹配")
            s = 0.0
            for i in range(a.shape[0]):
                s += a.data[i] * b.data[i]
            return Tensor._from_flat([s], (), "float32")

        squeeze_left = False
        squeeze_right = False
        if a.ndim == 2 and b.ndim == 1:
            # (M,K) @ (K,) -> (M,)
            M, K = a.shape
            if K != b.shape[0]:
                raise ValueError("matmul 维度不匹配")
            out = [0.0] * M
            for i in range(M):
                acc = 0.0
                for k in range(K):
                    acc += a.data[i * K + k] * b.data[k]
                out[i] = acc
            return Tensor._from_flat(out, (M,), "float32")
        if a.ndim == 1 and b.ndim == 2:
            # (K,) @ (K,N) -> (N,)
            K, N = b.shape
            if K != a.shape[0]:
                raise ValueError("matmul 维度不匹配")
            out = [0.0] * N
            for j in range(N):
                acc = 0.0
                for k in range(K):
                    acc += a.data[k] * b.data[k * N + j]
                out[j] = acc
            return Tensor._from_flat(out, (N,), "float32")

        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("matmul 目前只支持 1D/2D 张量")
        M, K = a.shape
        K2, N = b.shape
        if K != K2:
            raise ValueError("matmul 维度不匹配: %s vs %s" % (a.shape, b.shape))
        out = [0.0] * (M * N)
        da = a.data
        db = b.data
        for i in range(M):
            row_base = i * K
            out_base = i * N
            for k in range(K):
                aik = da[row_base + k]
                bk_base = k * N
                for j in range(N):
                    out[out_base + j] += aik * db[bk_base + j]
        return Tensor._from_flat(out, (M, N), "float32")

    # ------------------------------------------------------------------ #
    # 形状操作
    # ------------------------------------------------------------------ #
    def transpose(self, axes=None):
        """转置 / 轴重排。

        2D 不带 axes 时交换两轴；高维可传入 ``axes`` 元组指定新轴序。
        """
        n = self.ndim
        if axes is None:
            if n == 0:
                return self._from_flat(self.data, (), self.dtype)
            axes = list(range(n - 1, -1, -1))
        else:
            axes = list(axes)
        # 新 shape：new_shape[i] = old_shape[axes[i]]
        new_shape = tuple(self.shape[a] for a in axes)
        old_strides = _strides(self.shape)
        new_strides = _strides(new_shape)
        out_size = _prod(new_shape)
        out = [0.0] * out_size
        for flat in range(out_size):
            idx = flat
            new_idx = []
            rem = flat
            for k in range(n):
                s = new_strides[k]
                new_idx.append(rem // s)
                rem %= s
            # new_idx[i] 是第 i 个新轴上的坐标；对应旧轴 axes[i]
            old_flat = 0
            for i in range(n):
                old_flat += new_idx[i] * old_strides[axes[i]]
            out[flat] = self.data[old_flat]
        return Tensor._from_flat(out, new_shape, self.dtype)

    def reshape(self, *shape):
        """改变形状。支持单个 -1 自动推断维度。"""
        if len(shape) == 1 and isinstance(shape[0], (tuple, list)):
            shape = tuple(shape[0])
        else:
            shape = tuple(shape)
        if -1 in shape:
            known = 1
            auto_idx = -1
            for i, s in enumerate(shape):
                if s == -1:
                    auto_idx = i
                else:
                    known *= s
            if known == 0:
                raise ValueError("reshape 中不能出现 0 维配合 -1")
            inferred = self.size // known
            shape = tuple(inferred if s == -1 else s for s in shape)
        if _prod(shape) != self.size:
            raise ValueError("reshape: 无法把 size=%d 重塑为 %s" % (self.size, shape))
        return Tensor._from_flat(self.data, shape, self.dtype)

    def concat(self, other, axis=0):
        """沿 ``axis`` 拼接另一个张量。"""
        other = self._coerce(other)
        if self.ndim != other.ndim:
            raise ValueError("concat 要求两个张量维度一致")
        if axis < 0:
            axis += self.ndim
        for i in range(self.ndim):
            if i == axis:
                continue
            if self.shape[i] != other.shape[i]:
                raise ValueError("concat 非拼接轴形状必须一致")
        out_shape = list(self.shape)
        out_shape[axis] = self.shape[axis] + other.shape[axis]
        out_shape = tuple(out_shape)

        a_strides = _strides(self.shape)
        b_strides = _strides(other.shape)
        out_strides = _strides(out_shape)
        out = [0.0] * _prod(out_shape)

        def _write(tensor, strides, offset):
            t_strides = strides
            base_sizes = list(tensor.shape)
            # 递归按维写
            def rec(dim, flat_out, flat_in):
                if dim == self.ndim:
                    out[flat_out] = tensor.data[flat_in]
                    return
                for v in range(tensor.shape[dim]):
                    rec(dim + 1, flat_out + v * out_strides[dim],
                        flat_in + v * t_strides[dim])
            rec(0, offset, 0)

        # self 在前，other 在后
        _write(self, a_strides, 0)
        # other 起点：拼接轴上前进 self.shape[axis] 步
        other_offset = self.shape[axis] * out_strides[axis]
        _write(other, b_strides, other_offset)
        return Tensor._from_flat(out, out_shape, self.dtype)

    # ------------------------------------------------------------------ #
    # 索引
    # ------------------------------------------------------------------ #
    def _get_index(self, multi_idx):
        """根据多维索引（int 或 slice）取值或切片，返回新 Tensor。"""
        if not isinstance(multi_idx, tuple):
            multi_idx = (multi_idx,)
        src_strides = _strides(self.shape)
        fixed_offset = 0
        new_shape = []
        dim_offsets = []  # 每个输出维对应的 (起点偏移, 每步偏移)

        for axis in range(self.ndim):
            if axis < len(multi_idx):
                sl = multi_idx[axis]
            else:
                sl = slice(None)
            if isinstance(sl, slice):
                start = sl.start if sl.start is not None else 0
                stop = sl.stop if sl.stop is not None else self.shape[axis]
                step = sl.step if sl.step is not None else 1
                if start < 0:
                    start += self.shape[axis]
                if stop < 0:
                    stop += self.shape[axis]
                length = max(0, (stop - start + (step - 1)) // step) if step > 0 else 0
                new_shape.append(length)
                dim_offsets.append((start * src_strides[axis],
                                    step * src_strides[axis]))
            else:
                if sl < 0:
                    sl += self.shape[axis]
                fixed_offset += sl * src_strides[axis]

        out_size = _prod(new_shape) if new_shape else 1
        out = [0.0] * out_size
        out_strides = _strides(new_shape) if new_shape else ()
        for flat in range(out_size):
            rem = flat
            old_flat = fixed_offset
            for k in range(len(new_shape)):
                s = out_strides[k] if new_shape else 0
                d = rem // s
                rem %= s
                old_flat += dim_offsets[k][0] + d * dim_offsets[k][1]
            out[flat] = self.data[old_flat]
        if not new_shape:
            return Tensor._from_flat([out[0]], (), self.dtype)
        return Tensor._from_flat(out, tuple(new_shape), self.dtype)

    def __getitem__(self, key):
        """支持 tensor[i]、tensor[i,j]、tensor[start:end]。"""
        return self._get_index(key)

    # ------------------------------------------------------------------ #
    # 归约
    # ------------------------------------------------------------------ #
    def _reduce(self, axis, keepdims, reduce_fn, identity):
        if axis is None:
            s = identity
            for v in self.data:
                s = reduce_fn(s, v)
            if keepdims:
                shape = tuple(1 for _ in range(self.ndim))
                return Tensor._from_flat([s], shape, self.dtype)
            return Tensor._from_flat([s], (), self.dtype)

        if isinstance(axis, int):
            axis = (axis,)
        axis = tuple(a + self.ndim if a < 0 else a for a in axis)
        out_shape = list(self.shape)
        for a in axis:
            out_shape[a] = 1
        # 先按 keepdims 保留 1，再按需 squeeze
        out_shape = tuple(out_shape)
        out = [identity] * _prod(out_shape)
        out_strides = _strides(out_shape)
        in_strides = _strides(self.shape)

        for flat in range(self.size):
            rem = flat
            out_flat = 0
            for k in range(self.ndim):
                s = in_strides[k]
                d = rem // s
                rem %= s
                if k in axis:
                    d = 0
                out_flat += d * out_strides[k]
            out[out_flat] = reduce_fn(out[out_flat], self.data[flat])

        if keepdims:
            return Tensor._from_flat(out, out_shape, self.dtype)
        # squeeze 掉被规约的轴
        squeezed = [s for i, s in enumerate(out_shape) if i not in axis]
        return Tensor._from_flat(out, tuple(squeezed), self.dtype)

    def sum(self, axis=None, keepdims=False):
        """求和。axis 为 None 时对全部元素求和。"""
        return self._reduce(axis, keepdims, lambda a, b: a + b, 0.0)

    def mean(self, axis=None, keepdims=False):
        """算术平均。"""
        total = self.sum(axis=axis, keepdims=keepdims)
        if axis is None:
            n = self.size
        else:
            if isinstance(axis, int):
                axis = (axis,)
            n = 1
            for a in axis:
                n *= self.shape[a]
        return total.div(float(n))

    def max(self, axis=None, keepdims=False):
        """最大值。"""
        return self._reduce(axis, keepdims, lambda a, b: a if a > b else b,
                            float("-inf"))

    def min(self, axis=None, keepdims=False):
        """最小值。"""
        return self._reduce(axis, keepdims, lambda a, b: a if a < b else b,
                            float("inf"))

    # ------------------------------------------------------------------ #
    # 逐元素一元函数
    # ------------------------------------------------------------------ #
    def _unary(self, fn):
        out = [fn(v) for v in self.data]
        return Tensor._from_flat(out, self.shape, "float32")

    def exp(self):
        """逐元素 e^x。"""
        return self._unary(math.exp)

    def log(self):
        """逐元素自然对数。"""
        return self._unary(math.log)

    def sin(self):
        """逐元素 sin。"""
        return self._unary(math.sin)

    def cos(self):
        """逐元素 cos。"""
        return self._unary(math.cos)

    def sqrt(self):
        """逐元素平方根。"""
        return self._unary(math.sqrt)

    def abs(self):
        """逐元素绝对值。"""
        return self._unary(abs)

    def sigmoid(self):
        """逐元素 sigmoid(x) = 1/(1+e^-x)。"""
        def f(x):
            if x >= 0:
                z = math.exp(-x)
                return 1.0 / (1.0 + z)
            z = math.exp(x)
            return z / (1.0 + z)
        return self._unary(f)

    def relu(self):
        """逐元素 ReLU(x) = max(0, x)。"""
        return self._unary(lambda x: x if x > 0 else 0.0)

    def tanh(self):
        """逐元素 tanh。"""
        return self._unary(math.tanh)

    def softmax(self, dim=-1):
        """沿 ``dim`` 做 softmax（数值稳定版：减去最大值）。"""
        n = self.ndim
        if n == 0:
            return Tensor._from_flat([1.0], (), "float32")
        if dim < 0:
            dim += n
        # 把 dim 提到最后维，按行计算
        # 简化：迭代所有非 dim 维，每个 dim 行内做 softmax
        other_dims = [i for i in range(n) if i != dim]
        # 计算每个“行”的长度 = shape[dim]
        row_len = self.shape[dim]
        outer_size = self.size // row_len
        out = [0.0] * self.size
        # 把数据按行重排到连续（dim 在最后）
        perm = other_dims + [dim]
        # 构造索引映射：flat -> 按 perm 排列后的位置
        src_strides = _strides(self.shape)
        perm_strides = _strides(tuple(self.shape[p] for p in perm))
        # perm 后的连续索引：outer_idx * row_len + j
        for outer in range(outer_size):
            # 计算 outer 在原 shape 中的多维坐标（除 dim 外）
            rem = outer
            coords = [0] * n
            for rank, d in enumerate(other_dims):
                stride = 1
                for dd in other_dims[rank + 1:]:
                    stride *= self.shape[dd]
                coords[d] = rem // stride
                rem %= stride
            # 取出该行
            row_vals = []
            for j in range(row_len):
                coords[dim] = j
                flat = sum(coords[k] * src_strides[k] for k in range(n))
                row_vals.append(self.data[flat])
            m = max(row_vals)
            exps = [math.exp(v - m) for v in row_vals]
            s = sum(exps)
            for j in range(row_len):
                coords[dim] = j
                flat = sum(coords[k] * src_strides[k] for k in range(n))
                out[flat] = exps[j] / s
        return Tensor._from_flat(out, self.shape, "float32")

    # ------------------------------------------------------------------ #
    # 运算符重载
    # ------------------------------------------------------------------ #
    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __rsub__(self, other):
        return self._coerce(other).sub(self)

    def __mul__(self, other):
        return self.mul(other)

    def __rmul__(self, other):
        return self.mul(other)

    def __truediv__(self, other):
        return self.div(other)

    def __rtruediv__(self, other):
        return self._coerce(other).div(self)

    def __matmul__(self, other):
        return self.matmul(other)

    def __neg__(self):
        return self.mul(-1.0)

    def __repr__(self):
        data_preview = self.tolist()
        return "Tensor(shape=%s, dtype=%s, data=%r)" % (
            self.shape, self.dtype, data_preview)


# ---------------------------------------------------------------------------
# 冒烟测试
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    a = Tensor([[1, 2], [3, 4]])
    b = Tensor([[5, 6], [7, 8]])
    print("a:", a)
    print("a+b:", a + b)
    print("a*b:", a * b)
    print("a@b:", a @ b)
    print("a.T:", a.T)
    print("a.sum():", a.sum())
    print("a.sum(axis=0):", a.sum(axis=0))
    print("a.reshape(4):", a.reshape(4))
    print("softmax:", Tensor([1.0, 2.0, 3.0]).softmax())
    print("zeros:", Tensor.zeros((2, 2)))
    print("eye:", Tensor.eye(3))
    # 广播
    c = Tensor([1, 2, 3])
    print("broadcast a + c:", Tensor([[1], [2]]) + c)
    print("OK tensor.py")
