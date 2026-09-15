#!/usr/bin/env python3
# Aurora v3.0.0 AI Engine
"""decorators.py — 运行时装饰器（编译器优化提示接口）。

本模块刻意保持为叶子模块：不依赖 stdlib / interpreter / kernel，
因此 stdlib.py 可以安全地在此处导入 ``ai`` 装饰器，而不会引入循环依赖。

未来 Aurora 编译器可在 AST / 字节码阶段检测被 ``@ai`` 标记的函数，
自动做张量向量化、算子融合与图优化。
"""

from typing import Callable, Any


def ai(fn: Callable) -> Callable:
    """标记函数为 AI 相关，编译器可据此优化张量运算。

    用法::

        @ai
        def forward(x):
            return x @ W + b

    目前作为运行时元数据标记：在函数对象上写入 ``_aurora_ai = True``。
    未来的编译器 / JIT 会读取该属性，对函数体内的张量运算做自动向量化。
    """
    fn._aurora_ai = True
    return fn


def is_ai(fn: Any) -> bool:
    """判断一个函数是否被 ``@ai`` 标记。"""
    return getattr(fn, '_aurora_ai', False) is True


__all__ = ['ai', 'is_ai']
