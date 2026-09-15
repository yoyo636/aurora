"""Aurora AI 原生引擎 — 数据处理库 (AuroraData)

提供类 Pandas 的 DataFrame、数据集封装 Dataset、批量迭代器 DataLoader，
以及 StandardScaler / MinMaxScaler / LabelEncoder 等预处理工具。

设计目标：
    - 纯 Python 实现，不强制依赖 pandas / numpy；
    - 内部采用 list-of-dicts 行存储，对 filter / map / groupby 最自然；
    - 缺失值统一用 None 表示；
    - CSV 解析委托标准库 csv，天然处理引号与转义逗号。

典型用法::

    from ai.data import DataFrame, Dataset, DataLoader, StandardScaler

    df = DataFrame.read_csv("data.csv")
    df = df.dropna()
    train, test = df.train_test_split(test_size=0.2, seed=42)
    ds = Dataset(df, labels=df["label"])
    loader = DataLoader(ds, batch_size=32, shuffle=True, seed=42)
    for batch in loader:
        ...
"""

# Aurora v3.0.0 AI Engine - Data

from __future__ import annotations

import csv
import json
import math
import os
import random
import statistics
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple, Union

# ---------------------------------------------------------------------------
# 可选加速：检测到 numpy 时使用其向量化实现（保持 API 不变）
# ---------------------------------------------------------------------------
try:  # pragma: no cover - 环境探测
    import numpy as _np  # type: ignore

    _HAS_NUMPY = True
except Exception:  # noqa: BLE001
    _np = None
    _HAS_NUMPY = False


# ===========================================================================
# 内部工具函数
# ===========================================================================
def _is_missing(v: Any) -> bool:
    """判断一个值是否为缺失（None 或 NaN）。"""
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    return False


def _is_numeric(v: Any) -> bool:
    """判断单个值是否为数值（bool 在统计中视为数值）。"""
    return isinstance(v, (int, float)) and not isinstance(v, bool) and not (
        isinstance(v, float) and math.isnan(v)
    )


def _numeric_values(series: List[Any]) -> List[float]:
    """从一列中取出所有非缺失数值，转成 float。"""
    out: List[float] = []
    for v in series:
        if _is_missing(v):
            continue
        if isinstance(v, bool):
            out.append(1.0 if v else 0.0)
        elif isinstance(v, (int, float)):
            out.append(float(v))
    return out


def _mean(xs: List[float]) -> float:
    return statistics.fmean(xs) if xs else float("nan")


def _std(xs: List[float]) -> float:
    """样本标准差（ddof=1）；样本不足时返回 0。"""
    if len(xs) < 2:
        return 0.0
    return statistics.stdev(xs)


def _median(xs: List[float]) -> float:
    return statistics.median(xs) if xs else float("nan")


def _quantile(sorted_xs: List[float], q: float) -> float:
    """对已排序升序列表计算分位数（线性插值法，与 pandas 默认一致）。

    q ∈ [0, 1]。空列表返回 nan。
    """
    if not sorted_xs:
        return float("nan")
    if len(sorted_xs) == 1:
        return float(sorted_xs[0])
    pos = q * (len(sorted_xs) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(sorted_xs[lo])
    frac = pos - lo
    return float(sorted_xs[lo]) * (1.0 - frac) + float(sorted_xs[hi]) * frac


def _auto_dtype(values: List[Any]) -> str:
    """根据一列的值推断类型名：int / float / bool / object。"""
    seen_numeric = False
    has_int = False
    has_float = False
    has_bool = False
    has_other = False
    for v in values:
        if _is_missing(v):
            continue
        if isinstance(v, bool):
            has_bool = True
        elif isinstance(v, int):
            has_int = True
            seen_numeric = True
        elif isinstance(v, float):
            has_float = True
            seen_numeric = True
        else:
            has_other = True
    if has_other or not seen_numeric and not has_bool:
        if has_bool and not seen_numeric:
            return "bool"
        if has_other:
            return "object"
    if has_float:
        return "float"
    if has_int:
        return "int"
    if has_bool:
        return "bool"
    return "object"


# ===========================================================================
# GroupBy 结果对象
# ===========================================================================
class GroupBy:
    """``DataFrame.groupby(col)`` 返回的分组聚合对象。

    支持链式聚合：.sum() / .mean() / .count() / .max() / .min() / .agg(fn)，
    返回新的 DataFrame（索引列名为分组列名）。
    """

    def __init__(self, df: "DataFrame", by: str):
        self._df = df
        self._by = by
        # groups: {group_value: [row_index, ...]}
        self._groups: Dict[Any, List[int]] = {}
        for i, row in enumerate(df._rows):
            key = row.get(by, None)
            self._groups.setdefault(key, []).append(i)

    # ---- 聚合辅助 ----
    def _numeric_cols(self) -> List[str]:
        """聚合时参与运算的列：排除分组列本身，且至少在一组里有数值。"""
        cols = [c for c in self._df._columns if c != self._by]
        usable: List[str] = []
        for c in cols:
            for idxs in self._groups.values():
                if any(_is_numeric(self._df._rows[i].get(c)) for i in idxs):
                    usable.append(c)
                    break
        return usable

    def _build(self, stat_fn: Callable[[List[float]], float], cols: List[str]) -> "DataFrame":
        rows_out: List[Dict[str, Any]] = []
        # 保持分组键首次出现的顺序
        seen_order: List[Any] = []
        seen_set = set()
        for row in self._df._rows:
            k = row.get(self._by, None)
            if k not in seen_set:
                seen_set.add(k)
                seen_order.append(k)

        for key in seen_order:
            idxs = self._groups[key]
            rec: Dict[str, Any] = {self._by: key}
            for c in cols:
                vals = []
                for i in idxs:
                    v = self._df._rows[i].get(c)
                    if not _is_missing(v):
                        vals.append(float(v))
                rec[c] = stat_fn(vals)
            rows_out.append(rec)
        return DataFrame(rows_out)

    def sum(self) -> "DataFrame":
        """对每组数值列求和。"""
        cols = self._numeric_cols()
        return self._build(lambda xs: sum(xs) if xs else 0.0, cols)

    def mean(self) -> "DataFrame":
        """对每组数值列求均值。"""
        cols = self._numeric_cols()
        return self._build(_mean, cols)

    def count(self) -> "DataFrame":
        """对每组统计各列非缺失值数量。"""
        cols = [c for c in self._df._columns if c != self._by]

        def _cnt(xs: List[float]) -> float:  # 这里传入的是非缺失数值数；为通用计数列另行处理
            return float(len(xs))

        rows_out: List[Dict[str, Any]] = []
        seen_order: List[Any] = []
        seen_set = set()
        for row in self._df._rows:
            k = row.get(self._by, None)
            if k not in seen_set:
                seen_set.add(k)
                seen_order.append(k)
        for key in seen_order:
            idxs = self._groups[key]
            rec: Dict[str, Any] = {self._by: key}
            for c in cols:
                rec[c] = float(sum(1 for i in idxs if not _is_missing(self._df._rows[i].get(c))))
            rows_out.append(rec)
        return DataFrame(rows_out)

    def max(self) -> "DataFrame":
        """对每组数值列求最大值。"""
        cols = self._numeric_cols()
        return self._build(lambda xs: max(xs) if xs else float("nan"), cols)

    def min(self) -> "DataFrame":
        """对每组数值列求最小值。"""
        cols = self._numeric_cols()
        return self._build(lambda xs: min(xs) if xs else float("nan"), cols)

    def agg(self, fn: Callable[[List[float]], float]) -> "DataFrame":
        """对每组数值列应用自定义聚合函数 fn(numeric_list) -> float。"""
        cols = self._numeric_cols()
        return self._build(fn, cols)

    # 让 dir()/help() 友好
    def __repr__(self) -> str:  # pragma: no cover
        return f"GroupBy(by={self._by!r}, n_groups={len(self._groups)})"


# ===========================================================================
# DataFrame
# ===========================================================================
class _ILocIndexer:
    """``df.iloc`` 访问器：按行号（整数位置）取值。"""

    def __init__(self, df: "DataFrame"):
        self._df = df

    def __getitem__(self, key: Union[int, slice]) -> Any:
        rows = self._df._rows
        n = len(rows)
        if isinstance(key, slice):
            sl = rows[key]
            idxs = list(range(*key.indices(n)))
            idx_labels = [self._df._index[i] for i in idxs]
            return DataFrame([dict(r) for r in sl], columns=list(self._df._columns), index=idx_labels)
        # 单个整数行号，返回 dict（行副本）
        if key < 0:
            key += n
        if not (0 <= key < n):
            raise IndexError(f"iloc 行索引越界: {key}（共 {n} 行）")
        return dict(rows[key])


class _LocIndexer:
    """``df.loc`` 访问器：按行索引标签取值。"""

    def __init__(self, df: "DataFrame"):
        self._df = df

    def __getitem__(self, key: Any) -> Any:
        # 建立 label -> position 映射
        for i, label in enumerate(self._df._index):
            if label == key:
                return dict(self._df._rows[i])
        raise KeyError(f"loc 未找到索引标签: {key!r}")


class DataFrame:
    """类 Pandas 的二维数据表。

    内部以 list-of-dicts 存储行，列名按插入顺序保存在 ``self._columns``。

    Parameters
    ----------
    data :
        支持四种输入形态：
          - ``list[dict]``：每行一个字典；
          - ``dict[list]``：每个键对应一列；
          - ``list[list]``：二维数组，配合 ``columns`` 使用；
          - ``list[list]`` 之外的一维 list 会被当作单列。
    columns : list[str], optional
        列名。未提供时自动推断。
    index : list, optional
        行索引标签，默认 ``0..n-1``。
    """

    # ------------------------------------------------------------------ #
    # 构造
    # ------------------------------------------------------------------ #
    def __init__(
        self,
        data: Any = None,
        columns: Optional[List[str]] = None,
        index: Optional[List[Any]] = None,
    ) -> None:
        self._rows: List[Dict[str, Any]] = []
        self._columns: List[str] = []
        self._index: List[Any] = []
        self.iloc = _ILocIndexer(self)
        self.loc = _LocIndexer(self)

        if data is None:
            data = []
        self._init_from(data, columns=columns, index=index)

    def _init_from(
        self,
        data: Any,
        columns: Optional[List[str]],
        index: Optional[List[Any]],
    ) -> None:
        # dict of lists
        if isinstance(data, dict):
            cols = list(columns) if columns else list(data.keys())
            lens = [len(v) for v in data.values() if isinstance(v, list)]
            n = lens[0] if lens else 0
            for i in range(n):
                rec = {c: (data[c][i] if i < len(data[c]) else None) for c in cols}
                self._rows.append(rec)
            self._columns = cols
        # list of dicts
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            cols: List[str] = []
            seen = set()
            for rec in data:
                for k in rec.keys():
                    if k not in seen:
                        seen.add(k)
                        cols.append(k)
            if columns:
                # 用户显式指定列顺序 / 子集
                cols = list(columns)
            self._columns = cols
            for rec in data:
                self._rows.append({c: rec.get(c, None) for c in cols})
        # list of lists (2D) / list of scalars (1D)
        elif isinstance(data, list):
            if data and not isinstance(data[0], (list, tuple)):
                # 一维 list -> 单列
                col = columns[0] if columns else "value"
                self._columns = [col]
                self._rows = [{col: v} for v in data]
            else:
                rows_2d: List[List[Any]] = data
                if not columns:
                    # 自动命名 col0, col1, ...
                    ncol = max((len(r) for r in rows_2d), default=0)
                    columns = [f"col{i}" for i in range(ncol)]
                self._columns = list(columns)
                for r in rows_2d:
                    rec = {}
                    for i, c in enumerate(self._columns):
                        rec[c] = r[i] if i < len(r) else None
                    self._rows.append(rec)
        else:
            raise TypeError(f"不支持的 DataFrame 数据类型: {type(data).__name__}")

        # index
        n = len(self._rows)
        if index is not None:
            if len(index) != n:
                raise ValueError(f"index 长度 {len(index)} 与数据行数 {n} 不一致")
            self._index = list(index)
        else:
            self._index = list(range(n))

    # ------------------------------------------------------------------ #
    # 基础属性
    # ------------------------------------------------------------------ #
    @property
    def shape(self) -> Tuple[int, int]:
        """``(行数, 列数)``。"""
        return (len(self._rows), len(self._columns))

    @property
    def columns(self) -> List[str]:
        """列名列表。"""
        return list(self._columns)

    @columns.setter
    def columns(self, new_cols: List[str]) -> None:
        if len(new_cols) != len(self._columns):
            raise ValueError("新列名数量与现有列数不一致")
        # 同时重命名行字典里的键
        mapping = {old: new for old, new in zip(self._columns, new_cols)}
        self._rows = [{mapping.get(k, k): v for k, v in r.items()} for r in self._rows]
        self._columns = list(new_cols)

    @property
    def index(self) -> List[Any]:
        """行索引列表。"""
        return list(self._index)

    @property
    def dtypes(self) -> Dict[str, str]:
        """每列推断出的类型名。"""
        out: Dict[str, str] = {}
        for c in self._columns:
            out[c] = _auto_dtype([r.get(c) for r in self._rows])
        return out

    @property
    def values(self) -> List[List[Any]]:
        """二维 list 形式的数据（按列顺序）。"""
        return [[r.get(c) for c in self._columns] for r in self._rows]

    # ------------------------------------------------------------------ #
    # 数据访问
    # ------------------------------------------------------------------ #
    def __getitem__(self, key: Any) -> Any:
        # 多列：list of str
        if isinstance(key, list):
            for c in key:
                if c not in self._columns:
                    raise KeyError(f"列不存在: {c!r}")
            rows_out = [{c: r.get(c) for c in key} for r in self._rows]
            return DataFrame(rows_out, columns=list(key), index=self._index)
        # 单列
        if key not in self._columns:
            raise KeyError(f"列不存在: {key!r}")
        return [r.get(key) for r in self._rows]

    def __setitem__(self, key: str, value: Any) -> None:
        # 标量 -> 整列填充；list -> 逐行赋值
        if isinstance(value, list):
            if len(value) != len(self._rows):
                raise ValueError(f"赋值长度 {len(value)} 与行数 {len(self._rows)} 不一致")
            for r, v in zip(self._rows, value):
                r[key] = v
        else:
            for r in self._rows:
                r[key] = value
        if key not in self._columns:
            self._columns.append(key)

    def __len__(self) -> int:
        return len(self._rows)

    def __contains__(self, key: str) -> bool:
        return key in self._columns

    def __iter__(self) -> Iterator[str]:
        return iter(self._columns)

    def __repr__(self) -> str:  # pragma: no cover
        rows, cols = self.shape
        head = self.head(5)
        lines = [f"<DataFrame {rows}x{cols}>"]
        lines.append("  " + " | ".join(str(c) for c in head._columns))
        for i, r in enumerate(head._rows):
            lines.append(
                f"  {head._index[i]}: "
                + " | ".join(str(r.get(c)) for c in head._columns)
            )
        if rows > 5:
            lines.append(f"  ... ({rows - 5} more rows)")
        return "\n".join(lines)

    def head(self, n: int = 5) -> "DataFrame":
        """返回前 ``n`` 行。"""
        rows = self._rows[:n]
        idx = self._index[:n]
        return DataFrame([dict(r) for r in rows], columns=list(self._columns), index=idx)

    def tail(self, n: int = 5) -> "DataFrame":
        """返回后 ``n`` 行。"""
        rows = self._rows[-n:] if n > 0 else []
        idx = self._index[-n:] if n > 0 else []
        return DataFrame([dict(r) for r in rows], columns=list(self._columns), index=idx)

    def iterrows(self) -> Iterator[Tuple[Any, Dict[str, Any]]]:
        """逐行迭代 ``(index_label, row_dict)``。"""
        for i, r in enumerate(self._rows):
            yield self._index[i], dict(r)

    # ------------------------------------------------------------------ #
    # 数据清洗
    # ------------------------------------------------------------------ #
    def dropna(self, axis: int = 0, how: str = "any") -> "DataFrame":
        """删除含缺失值的行（axis=0）或列（axis=1）。

        how='any'：任意一个缺失即删；how='all'：全部缺失才删。
        """
        if axis == 0:
            kept_rows: List[Dict[str, Any]] = []
            kept_idx: List[Any] = []
            for i, r in enumerate(self._rows):
                flags = [_is_missing(r.get(c)) for c in self._columns]
                if how == "all":
                    drop = all(flags)
                else:
                    drop = any(flags)
                if not drop:
                    kept_rows.append(dict(r))
                    kept_idx.append(self._index[i])
            return DataFrame(kept_rows, columns=list(self._columns), index=kept_idx)
        elif axis == 1:
            kept_cols: List[str] = []
            for c in self._columns:
                flags = [_is_missing(r.get(c)) for r in self._rows]
                drop = all(flags) if how == "all" else any(flags)
                if not drop:
                    kept_cols.append(c)
            rows_out = [{c: r.get(c) for c in kept_cols} for r in self._rows]
            return DataFrame(rows_out, columns=kept_cols, index=self._index)
        else:
            raise ValueError("axis 只能是 0 或 1")

    def fillna(self, value: Any = None, method: Optional[str] = None) -> "DataFrame":
        """填充缺失值。

        Parameters
        ----------
        value :
            固定填充值。
        method :
            'ffill' 前向填充 / 'bfill' 后向填充 /
            'mean' 列均值 / 'median' 列中位数。
        """
        rows_out = [dict(r) for r in self._rows]
        cols = list(self._columns)

        if method is None:
            for r in rows_out:
                for c in cols:
                    if _is_missing(r.get(c)):
                        r[c] = value
            return DataFrame(rows_out, columns=cols, index=self._index)

        # 按列处理
        for c in cols:
            series = [r.get(c) for r in rows_out]
            if method == "ffill":
                last = None
                for i, v in enumerate(series):
                    if _is_missing(v):
                        series[i] = last
                    else:
                        last = v
            elif method == "bfill":
                nxt = None
                for i in range(len(series) - 1, -1, -1):
                    v = series[i]
                    if _is_missing(v):
                        series[i] = nxt
                    else:
                        nxt = v
            elif method == "mean":
                nums = _numeric_values(series)
                m = _mean(nums) if nums else 0
                for i, v in enumerate(series):
                    if _is_missing(v):
                        series[i] = m
            elif method == "median":
                nums = sorted(_numeric_values(series))
                m = _median(nums) if nums else 0
                for i, v in enumerate(series):
                    if _is_missing(v):
                        series[i] = m
            else:
                raise ValueError(f"未知 fillna method: {method!r}")
            for i, r in enumerate(rows_out):
                r[c] = series[i]
        return DataFrame(rows_out, columns=cols, index=self._index)

    def drop_duplicates(self, subset: Optional[List[str]] = None) -> "DataFrame":
        """基于 ``subset`` 列去重，保留首次出现的行。"""
        subset = subset or list(self._columns)
        seen = set()
        kept_rows: List[Dict[str, Any]] = []
        kept_idx: List[Any] = []
        for i, r in enumerate(self._rows):
            key = tuple(r.get(c) for c in subset)
            if key in seen:
                continue
            seen.add(key)
            kept_rows.append(dict(r))
            kept_idx.append(self._index[i])
        return DataFrame(kept_rows, columns=list(self._columns), index=kept_idx)

    def rename(self, columns: Dict[str, str]) -> "DataFrame":
        """按字典重命名列，返回新 DataFrame。"""
        new_cols = [columns.get(c, c) for c in self._columns]
        rows_out = []
        for r in self._rows:
            rec = {}
            for old, new in zip(self._columns, new_cols):
                rec[new] = r.get(old)
            rows_out.append(rec)
        return DataFrame(rows_out, columns=new_cols, index=self._index)

    def filter(self, condition_fn: Callable[[Dict[str, Any]], bool]) -> "DataFrame":
        """按行过滤：``condition_fn(row_dict)`` 为 True 才保留。"""
        kept_rows: List[Dict[str, Any]] = []
        kept_idx: List[Any] = []
        for i, r in enumerate(self._rows):
            if bool(condition_fn(dict(r))):
                kept_rows.append(dict(r))
                kept_idx.append(self._index[i])
        return DataFrame(kept_rows, columns=list(self._columns), index=kept_idx)

    def map(self, col_name: str, fn: Callable[[Any], Any]) -> "DataFrame":
        """对 ``col_name`` 列逐元素应用 ``fn``，返回新 DataFrame。"""
        if col_name not in self._columns:
            raise KeyError(f"列不存在: {col_name!r}")
        rows_out = []
        for r in self._rows:
            rec = dict(r)
            rec[col_name] = fn(rec.get(col_name))
            rows_out.append(rec)
        return DataFrame(rows_out, columns=list(self._columns), index=self._index)

    def apply(self, fn: Callable, axis: int = 0) -> Union[List[Any], "DataFrame"]:
        """对行（axis=1）或列（axis=0）应用函数。

        axis=0：``fn(series: list) -> scalar``，返回 list（按列顺序）；
        axis=1：``fn(row_dict) -> scalar``，返回新单列 DataFrame。
        """
        if axis == 0:
            return [fn([r.get(c) for r in self._rows]) for c in self._columns]
        elif axis == 1:
            out = [fn(dict(r)) for r in self._rows]
            col = "apply"
            rows_out = [{col: v} for v in out]
            return DataFrame(rows_out, columns=[col], index=self._index)
        else:
            raise ValueError("axis 只能是 0 或 1")

    def groupby(self, col_name: str) -> GroupBy:
        """按 ``col_name`` 分组，返回 :class:`GroupBy`。"""
        if col_name not in self._columns:
            raise KeyError(f"列不存在: {col_name!r}")
        return GroupBy(self, col_name)

    # ------------------------------------------------------------------ #
    # 数据转换
    # ------------------------------------------------------------------ #
    def _numeric_columns(self, cols: Optional[List[str]]) -> List[str]:
        if cols is not None:
            for c in cols:
                if c not in self._columns:
                    raise KeyError(f"列不存在: {c!r}")
            return list(cols)
        # 自动选择数值列
        out = []
        for c in self._columns:
            vals = _numeric_values([r.get(c) for r in self._rows])
            if vals:
                out.append(c)
        return out

    def standardize(self, cols: Optional[List[str]] = None) -> "DataFrame":
        """Z-score 标准化：``(x - mean) / std``。None 值保持 None。"""
        target = self._numeric_columns(cols)
        rows_out = [dict(r) for r in self._rows]
        for c in target:
            nums = _numeric_values([r.get(c) for r in rows_out])
            if not nums:
                continue
            m = _mean(nums)
            s = _std(nums) or 1.0
            for r in rows_out:
                v = r.get(c)
                if not _is_missing(v) and isinstance(v, (int, float)):
                    r[c] = (float(v) - m) / s
        return DataFrame(rows_out, columns=list(self._columns), index=self._index)

    def normalize(self, cols: Optional[List[str]] = None, method: str = "minmax") -> "DataFrame":
        """归一化。method='minmax' 映射到 [0, 1]；method='l2' 做 L2 范数归一化。"""
        target = self._numeric_columns(cols)
        rows_out = [dict(r) for r in self._rows]
        if method == "minmax":
            for c in target:
                nums = _numeric_values([r.get(c) for r in rows_out])
                if not nums:
                    continue
                lo, hi = min(nums), max(nums)
                rng = hi - lo
                if rng == 0:
                    rng = 1.0
                for r in rows_out:
                    v = r.get(c)
                    if not _is_missing(v) and isinstance(v, (int, float)):
                        r[c] = (float(v) - lo) / rng
        elif method == "l2":
            for c in target:
                sq = 0.0
                for r in rows_out:
                    v = r.get(c)
                    if not _is_missing(v) and isinstance(v, (int, float)):
                        sq += float(v) ** 2
                norm = math.sqrt(sq) or 1.0
                for r in rows_out:
                    v = r.get(c)
                    if not _is_missing(v) and isinstance(v, (int, float)):
                        r[c] = float(v) / norm
        else:
            raise ValueError(f"未知 normalize method: {method!r}")
        return DataFrame(rows_out, columns=list(self._columns), index=self._index)

    def one_hot(self, col_name: str, prefix: Optional[str] = None) -> "DataFrame":
        """对 ``col_name`` 做 one-hot 编码：为每个唯一值生成 ``{prefix}{值}`` 0/1 列，删除原列。"""
        if col_name not in self._columns:
            raise KeyError(f"列不存在: {col_name!r}")
        prefix = prefix if prefix is not None else f"{col_name}_"
        # 收集唯一值，保持首次出现顺序
        uniques: List[Any] = []
        seen = set()
        for r in self._rows:
            v = r.get(col_name)
            if v not in seen:
                seen.add(v)
                uniques.append(v)

        new_cols: List[str] = []
        new_names: List[str] = []
        for u in uniques:
            name = f"{prefix}{u}"
            new_names.append(name)
            new_cols.append(name)

        rows_out: List[Dict[str, Any]] = []
        for r in self._rows:
            rec = {k: v for k, v in r.items() if k != col_name}
            v = r.get(col_name)
            for name, u in zip(new_names, uniques):
                rec[name] = 1 if v == u else 0
            rows_out.append(rec)

        cols = [c for c in self._columns if c != col_name] + new_names
        return DataFrame(rows_out, columns=cols, index=self._index)

    def label_encode(self, col_name: str) -> "DataFrame":
        """对 ``col_name`` 做整数标签编码（按首次出现顺序 0,1,2,...），返回新 DataFrame。"""
        if col_name not in self._columns:
            raise KeyError(f"列不存在: {col_name!r}")
        mapping: Dict[Any, int] = {}
        for r in self._rows:
            v = r.get(col_name)
            if v not in mapping:
                mapping[v] = len(mapping)
        rows_out = [dict(r) for r in self._rows]
        for r in rows_out:
            r[col_name] = mapping[r.get(col_name)]
        return DataFrame(rows_out, columns=list(self._columns), index=self._index)

    def train_test_split(
        self,
        test_size: float = 0.2,
        shuffle: bool = True,
        seed: Optional[int] = None,
    ) -> Tuple["DataFrame", "DataFrame"]:
        """按行划分训练/测试集，返回 ``(train_df, test_df)``。"""
        n = len(self._rows)
        idx = list(range(n))
        if shuffle:
            rng = random.Random(seed)
            rng.shuffle(idx)
        n_test = int(round(n * test_size))
        test_idx = idx[:n_test]
        train_idx = idx[n_test:]
        train_df = DataFrame(
            [dict(self._rows[i]) for i in train_idx],
            columns=list(self._columns),
            index=[self._index[i] for i in train_idx],
        )
        test_df = DataFrame(
            [dict(self._rows[i]) for i in test_idx],
            columns=list(self._columns),
            index=[self._index[i] for i in test_idx],
        )
        return train_df, test_df

    # ------------------------------------------------------------------ #
    # 合并 / 连接
    # ------------------------------------------------------------------ #
    def concat(self, other: "DataFrame", axis: int = 0) -> "DataFrame":
        """沿行（axis=0）或列（axis=1）拼接另一个 DataFrame。"""
        if axis == 0:
            cols = list(self._columns)
            for c in other._columns:
                if c not in cols:
                    cols.append(c)
            rows_out = []
            for r in self._rows:
                rows_out.append({c: r.get(c) for c in cols})
            for r in other._rows:
                rows_out.append({c: r.get(c) for c in cols})
            base_idx = list(self._index)
            offset = max(base_idx) + 1 if base_idx and all(isinstance(x, int) for x in base_idx) else 0
            if all(isinstance(x, int) for x in list(self._index) + list(other._index)):
                idx = list(self._index) + [i + offset for i in other._index]
            else:
                idx = list(self._index) + list(other._index)
            return DataFrame(rows_out, columns=cols, index=idx)
        elif axis == 1:
            # 列拼接：按行位置对齐
            n = max(len(self._rows), len(other._rows))
            cols = list(self._columns) + list(other._columns)
            rows_out = []
            for i in range(n):
                rec = {}
                if i < len(self._rows):
                    rec.update({c: self._rows[i].get(c) for c in self._columns})
                if i < len(other._rows):
                    rec.update({c: other._rows[i].get(c) for c in other._columns})
                rows_out.append(rec)
            return DataFrame(rows_out, columns=cols)
        else:
            raise ValueError("axis 只能是 0 或 1")

    def merge(
        self,
        other: "DataFrame",
        on: Optional[str] = None,
        how: str = "inner",
    ) -> "DataFrame":
        """类 SQL 连接。``how`` ∈ {'inner', 'left', 'right', 'outer'}。

        采用 hash join：先把 ``other`` 按 ``on`` 列建索引，再扫描 ``self``。
        """
        if on is None:
            raise ValueError("merge 必须指定 on 列")
        if on not in self._columns or on not in other._columns:
            raise KeyError(f"on 列 {on!r} 在两侧都必须存在")

        right_cols = [c for c in other._columns if c != on]
        left_cols = list(self._columns)

        # 构建 right 的 hash 索引
        right_index: Dict[Any, List[Dict[str, Any]]] = {}
        for r in other._rows:
            key = r.get(on)
            right_index.setdefault(key, []).append(r)

        out_cols = left_cols + right_cols
        rows_out: List[Dict[str, Any]] = []
        matched_right_keys: set = set()

        def _emit(left_row: Optional[Dict[str, Any]], right_row: Optional[Dict[str, Any]]) -> None:
            rec: Dict[str, Any] = {}
            for c in left_cols:
                rec[c] = left_row.get(c) if left_row else None
            for c in right_cols:
                rec[c] = right_row.get(c) if right_row else None
            rows_out.append(rec)

        # inner / left：扫描 left
        for lrow in self._rows:
            key = lrow.get(on)
            matches = right_index.get(key, [])
            if matches:
                for rrow in matches:
                    matched_right_keys.add(key)
                    _emit(lrow, rrow)
            else:
                if how in ("left", "outer"):
                    _emit(lrow, None)

        # right / outer：扫描未匹配的 right 行
        if how in ("right", "outer"):
            for key, rrows in right_index.items():
                if key in matched_right_keys:
                    continue
                for rrow in rrows:
                    _emit(None, rrow)

        return DataFrame(rows_out, columns=out_cols)

    # ------------------------------------------------------------------ #
    # IO
    # ------------------------------------------------------------------ #
    @classmethod
    def read_csv(
        cls,
        path: str,
        delimiter: str = ",",
        header: bool = True,
        encoding: str = "utf-8",
    ) -> "DataFrame":
        """从 CSV 文件读取，返回 DataFrame。

        底层使用标准库 ``csv`` 模块，自动处理引号包裹与字段内转义逗号。
        """
        rows: List[List[str]] = []
        with open(path, "r", encoding=encoding, newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            for r in reader:
                rows.append(r)
        if not rows:
            return cls([])
        if header:
            columns = [c.strip() for c in rows[0]]
            body = rows[1:]
        else:
            ncol = max((len(r) for r in rows), default=0)
            columns = [f"col{i}" for i in range(ncol)]
            body = rows
        # 尝试把数值字符串转成 int / float；空串视为 None
        parsed: List[List[Any]] = []
        for r in body:
            rec: List[Any] = []
            for cell in r:
                s = cell.strip() if isinstance(cell, str) else cell
                if s == "" or s is None:
                    rec.append(None)
                else:
                    rec.append(_coerce_number(s))
            parsed.append(rec)
        return cls(parsed, columns=columns)

    def to_csv(
        self,
        path: str,
        delimiter: str = ",",
        index: bool = True,
        encoding: str = "utf-8",
    ) -> None:
        """写入 CSV 文件。``index=True`` 时在首列写出行索引。"""
        with open(path, "w", encoding=encoding, newline="") as f:
            writer = csv.writer(f, delimiter=delimiter)
            header = (["index"] if index else []) + list(self._columns)
            writer.writerow(header)
            for i, r in enumerate(self._rows):
                row = ([self._index[i]] if index else [])
                row += [_stringify(r.get(c)) for c in self._columns]
                writer.writerow(row)

    @classmethod
    def read_json(cls, path: str) -> "DataFrame":
        """从 JSON 文件读取（list-of-dicts 格式）。"""
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        return cls(obj)

    def to_json(self, path: str, indent: int = 2) -> None:
        """写入 JSON 文件（list-of-dicts）。"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(orient="records"), f, ensure_ascii=False, indent=indent, default=_json_default)

    def to_dict(self, orient: str = "records") -> Any:
        """转 Python 对象。``orient='records'`` 返回 list[dict]。"""
        if orient == "records":
            return [dict(r) for r in self._rows]
        elif orient == "list":
            return {c: [r.get(c) for r in self._rows] for c in self._columns}
        else:
            raise ValueError(f"未知 orient: {orient!r}")

    # ------------------------------------------------------------------ #
    # 统计
    # ------------------------------------------------------------------ #
    def describe(self) -> "DataFrame":
        """对数值列生成 count / mean / std / min / 25% / 50% / 75% / max 摘要。"""
        rows_out: List[Dict[str, Any]] = []
        stats_names = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
        for c in self._columns:
            nums = sorted(_numeric_values([r.get(c) for r in self._rows]))
            if not nums:
                continue
            row = {"stat": c}
            row["count"] = float(len(nums))
            row["mean"] = _mean(nums)
            row["std"] = _std(nums)
            row["min"] = nums[0]
            row["25%"] = _quantile(nums, 0.25)
            row["50%"] = _quantile(nums, 0.50)
            row["75%"] = _quantile(nums, 0.75)
            row["max"] = nums[-1]
            rows_out.append(row)
        if not rows_out:
            return DataFrame([])
        return DataFrame(rows_out, columns=["stat"] + stats_names)

    def corr(self) -> "DataFrame":
        """计算数值列之间的 Pearson 相关系数矩阵。"""
        numeric_cols = [
            c for c in self._columns if _numeric_values([r.get(c) for r in self._rows])
        ]
        n = len(numeric_cols)
        matrix: List[List[Any]] = [[0.0] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 1.0
            for j in range(i + 1, n):
                a = [r.get(numeric_cols[i]) for r in self._rows]
                b = [r.get(numeric_cols[j]) for r in self._rows]
                # 只取两侧都非缺失的位置
                pairs = [
                    (float(x), float(y))
                    for x, y in zip(a, b)
                    if not _is_missing(x) and not _is_missing(y)
                    and isinstance(x, (int, float)) and isinstance(y, (int, float))
                ]
                if len(pairs) < 2:
                    r = float("nan")
                else:
                    xs = [p[0] for p in pairs]
                    ys = [p[1] for p in pairs]
                    mx = _mean(xs)
                    my = _mean(ys)
                    num = sum((x - mx) * (y - my) for x, y in pairs)
                    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
                    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
                    r = num / (dx * dy) if dx > 0 and dy > 0 else float("nan")
                matrix[i][j] = r
                matrix[j][i] = r
        rows_out = []
        for i, c in enumerate(numeric_cols):
            rec: Dict[str, Any] = {"index": c}
            for j, c2 in enumerate(numeric_cols):
                rec[c2] = matrix[i][j]
            rows_out.append(rec)
        return DataFrame(rows_out, columns=["index"] + numeric_cols)

    def value_counts(self, col_name: str) -> "DataFrame":
        """统计某列各值出现次数，按频次降序。"""
        if col_name not in self._columns:
            raise KeyError(f"列不存在: {col_name!r}")
        counter: Dict[Any, int] = {}
        order: List[Any] = []
        for r in self._rows:
            v = r.get(col_name)
            if v not in counter:
                counter[v] = 0
                order.append(v)
            counter[v] += 1
        rows_out = [{"value": v, "count": counter[v]} for v in order]
        rows_out.sort(key=lambda x: -x["count"])
        return DataFrame(rows_out, columns=["value", "count"])


# ===========================================================================
# 数值转换辅助
# ===========================================================================
def _coerce_number(s: str) -> Any:
    """尝试把字符串转成 int / float；失败则原样返回。"""
    try:
        return int(s)
    except (ValueError, TypeError):
        pass
    try:
        return float(s)
    except (ValueError, TypeError):
        return s


def _stringify(v: Any) -> str:
    """把任意值转成 CSV/JSON 友好的字符串。"""
    if v is None:
        return ""
    if isinstance(v, float) and math.isnan(v):
        return ""
    return str(v)


def _json_default(o: Any) -> Any:
    """JSON 序列化兜底：NaN 转 None。"""
    if isinstance(o, float) and math.isnan(o):
        return None
    return str(o)


# ===========================================================================
# Dataset
# ===========================================================================
class Dataset:
    """封装特征与标签的数据集。

    Parameters
    ----------
    data : list[list] | DataFrame
        特征矩阵。
    labels : list, optional
        标签向量，长度需与 data 行数一致。
    transform : callable, optional
        对每个特征样本的预处理函数。
    """

    def __init__(
        self,
        data: Any,
        labels: Optional[List[Any]] = None,
        transform: Optional[Callable[[Any], Any]] = None,
    ) -> None:
        if isinstance(data, DataFrame):
            self._features: List[List[Any]] = data.values
        elif isinstance(data, list):
            self._features = [list(row) for row in data]
        else:
            raise TypeError("Dataset.data 必须是 list[list] 或 DataFrame")
        if labels is not None and len(labels) != len(self._features):
            raise ValueError(f"labels 长度 {len(labels)} 与样本数 {len(self._features)} 不一致")
        self._labels: Optional[List[Any]] = list(labels) if labels is not None else None
        self._transform = transform

    def __len__(self) -> int:
        return len(self._features)

    def __getitem__(self, idx: Union[int, slice]) -> Any:
        if isinstance(idx, slice):
            # 切片返回新 Dataset
            feats = self._features[idx]
            labels = self._labels[idx] if self._labels is not None else None
            return Dataset(feats, labels=labels, transform=self._transform)
        feat = self._features[idx]
        if self._transform is not None:
            feat = self._transform(feat)
        if self._labels is not None:
            return feat, self._labels[idx]
        return feat

    def map(self, fn: Callable[[Any], Any]) -> "Dataset":
        """对所有特征样本应用 ``fn``，返回新 Dataset。"""
        new_feats = [fn(list(f)) for f in self._features]
        return Dataset(new_feats, labels=self._labels, transform=self._transform)

    @property
    def features(self) -> List[List[Any]]:
        return [list(f) for f in self._features]

    @property
    def labels(self) -> Optional[List[Any]]:
        return list(self._labels) if self._labels is not None else None

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Dataset n={len(self)} has_labels={self._labels is not None}>"


# ===========================================================================
# DataLoader
# ===========================================================================
class DataLoader:
    """批量迭代器。

    Parameters
    ----------
    dataset : Dataset
        数据源。
    batch_size : int
        批大小。
    shuffle : bool
        是否每个 epoch 打乱。
    seed : int, optional
        随机种子。
    """

    def __init__(
        self,
        dataset: Dataset,
        batch_size: int = 32,
        shuffle: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size 必须 > 0")
        self._ds = dataset
        self._bs = batch_size
        self._shuffle = shuffle
        self._rng = random.Random(seed)

    def __len__(self) -> int:
        n = len(self._ds)
        return (n + self._bs - 1) // self._bs

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        n = len(self._ds)
        idx = list(range(n))
        if self._shuffle:
            self._rng.shuffle(idx)
        for start in range(0, n, self._bs):
            chunk = idx[start:start + self._bs]
            feats: List[List[Any]] = []
            labels: List[Any] = []
            has_labels = self._ds.labels is not None
            for i in chunk:
                item = self._ds[i]
                if has_labels:
                    f, y = item
                    feats.append(list(f))
                    labels.append(y)
                else:
                    feats.append(list(item))
            batch: Dict[str, Any] = {"features": feats}
            if has_labels:
                batch["labels"] = labels
            yield batch


# ===========================================================================
# 预处理器（Scaler / Encoder）
# ===========================================================================
class StandardScaler:
    """Z-score 标准化器：``(x - mean) / std``，按列拟合。"""

    def __init__(self) -> None:
        self.mean_: Optional[List[float]] = None
        self.std_: Optional[List[float]] = None

    def fit(self, X: Sequence[Sequence[float]]) -> "StandardScaler":
        """对二维样本列表按列拟合均值与标准差。"""
        cols = list(zip(*X)) if X else []
        self.mean_ = []
        self.std_ = []
        for col in cols:
            nums = [float(v) for v in col if not _is_missing(v)]
            self.mean_.append(_mean(nums) if nums else 0.0)
            self.std_.append(_std(nums) or 1.0)
        return self

    def transform(self, X: Sequence[Sequence[float]]) -> List[List[float]]:
        """应用已拟合的标准化。"""
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("StandardScaler 尚未 fit")
        out = []
        for row in X:
            out.append(
                [(float(v) - m) / s if not _is_missing(v) else float("nan")
                 for v, m, s in zip(row, self.mean_, self.std_)]
            )
        return out

    def fit_transform(self, X: Sequence[Sequence[float]]) -> List[List[float]]:
        """等价于 ``fit(X).transform(X)``。"""
        return self.fit(X).transform(X)


class MinMaxScaler:
    """Min-Max 归一化器：映射到 [0, 1]，按列拟合。"""

    def __init__(self, feature_range: Tuple[float, float] = (0.0, 1.0)) -> None:
        self.lo_: Optional[List[float]] = None
        self.hi_: Optional[List[float]] = None
        self.range_ = feature_range

    def fit(self, X: Sequence[Sequence[float]]) -> "MinMaxScaler":
        """对二维样本列表按列拟合 min/max。"""
        cols = list(zip(*X)) if X else []
        self.lo_ = []
        self.hi_ = []
        for col in cols:
            nums = [float(v) for v in col if not _is_missing(v)]
            self.lo_.append(min(nums) if nums else 0.0)
            self.hi_.append(max(nums) if nums else 1.0)
        return self

    def transform(self, X: Sequence[Sequence[float]]) -> List[List[float]]:
        if self.lo_ is None or self.hi_ is None:
            raise RuntimeError("MinMaxScaler 尚未 fit")
        out_lo, out_hi = self.range_
        out = []
        for row in X:
            rec = []
            for v, lo, hi in zip(row, self.lo_, self.hi_):
                if _is_missing(v):
                    rec.append(float("nan"))
                    continue
                rng = (hi - lo) or 1.0
                rec.append(out_lo + (float(v) - lo) / rng * (out_hi - out_lo))
            out.append(rec)
        return out

    def fit_transform(self, X: Sequence[Sequence[float]]) -> List[List[float]]:
        return self.fit(X).transform(X)


class LabelEncoder:
    """标签编码器：把类别值映射为 0..n-1 整数。"""

    def __init__(self) -> None:
        self.classes_: List[Any] = []
        self._map: Dict[Any, int] = {}

    def fit(self, y: Sequence[Any]) -> "LabelEncoder":
        """从序列学习类别集合（按首次出现顺序）。"""
        self.classes_ = []
        self._map = {}
        for v in y:
            if v not in self._map:
                self._map[v] = len(self.classes_)
                self.classes_.append(v)
        return self

    def transform(self, y: Sequence[Any]) -> List[int]:
        if not self._map:
            raise RuntimeError("LabelEncoder 尚未 fit")
        return [self._map[v] for v in y]

    def fit_transform(self, y: Sequence[Any]) -> List[int]:
        return self.fit(y).transform(y)

    def inverse_transform(self, y: Sequence[int]) -> List[Any]:
        return [self.classes_[i] for i in y]


# ===========================================================================
# 顶层快捷函数
# ===========================================================================
def read_csv(path: str, **kwargs: Any) -> DataFrame:
    """``DataFrame.read_csv`` 的快捷函数。"""
    return DataFrame.read_csv(path, **kwargs)


def train_test_split(
    X: Sequence[Sequence[Any]],
    y: Optional[Sequence[Any]] = None,
    test_size: float = 0.2,
    shuffle: bool = True,
    seed: Optional[int] = None,
) -> Tuple[Any, ...]:
    """数组版训练/测试划分。

    返回 ``(X_train, X_test)`` 或 ``(X_train, X_test, y_train, y_test)``。
    """
    n = len(X)
    idx = list(range(n))
    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(idx)
    n_test = int(round(n * test_size))
    test_idx = idx[:n_test]
    train_idx = idx[n_test:]
    X_train = [list(X[i]) for i in train_idx]
    X_test = [list(X[i]) for i in test_idx]
    if y is None:
        return X_train, X_test
    y = list(y)
    y_train = [y[i] for i in train_idx]
    y_test = [y[i] for i in test_idx]
    return X_train, X_test, y_train, y_test


# ===========================================================================
# 冒烟测试
# ===========================================================================
if __name__ == "__main__":
    import tempfile

    print("== AuroraData 冒烟测试 ==")

    # 1) 创建 DataFrame（list of dicts）
    df = DataFrame(
        [
            {"name": "Alice", "age": 25, "score": 88.0, "city": "BJ"},
            {"name": "Bob", "age": 30, "score": 92.5, "city": "SH"},
            {"name": "Carol", "age": None, "score": 79.0, "city": "BJ"},
            {"name": "Dave", "age": 25, "score": None, "city": "SZ"},
            {"name": "Eve", "age": 35, "score": 95.0, "city": "SH"},
        ]
    )
    print("[1] shape:", df.shape)
    assert df.shape == (5, 4)
    print("    columns:", df.columns)
    print("    dtypes :", df.dtypes)

    # 2) 访问
    print("[2] df['age']:", df["age"])
    row = df.iloc[1]
    print("    iloc[1]:", row)
    print("    head(2):\n", df.head(2))

    # 3) 清洗
    df_clean = df.dropna()
    print("[3] dropna 后 shape:", df_clean.shape)
    df_filled = df.fillna(method="mean")
    print("    fillna(mean) age:", df_filled["age"])

    # 4) groupby
    g = df_clean.groupby("city").mean()
    print("[4] groupby(city).mean():\n", g)

    # 5) 统计
    print("[5] describe:\n", df.describe())
    print("    value_counts(city):\n", df.value_counts("city"))

    # 6) one-hot / label encode
    oh = df.one_hot("city")
    print("[6] one_hot(city) columns:", oh.columns)
    le = df.label_encode("name")
    print("    label_encode(name):", le["name"])

    # 7) 读写 CSV（round-trip 用 index=False，避免 index 列回流）
    with tempfile.TemporaryDirectory() as td:
        csv_path = os.path.join(td, "t.csv")
        df.to_csv(csv_path, index=False)
        df2 = DataFrame.read_csv(csv_path)
        print("[7] read_csv shape:", df2.shape, "columns:", df2.columns)
        assert df2.shape == df.shape

        json_path = os.path.join(td, "t.json")
        df.to_json(json_path)
        df3 = DataFrame.read_json(json_path)
        print("    read_json shape:", df3.shape)
        assert df3.shape == df.shape

    # 8) train_test_split
    train, test = df.train_test_split(test_size=0.4, shuffle=True, seed=42)
    print("[8] train size:", train.shape, "test size:", test.shape)

    # 9) Dataset + DataLoader
    ds = Dataset(df.values, labels=df["age"])
    loader = DataLoader(ds, batch_size=2, shuffle=True, seed=1)
    print("[9] batches:", len(loader))
    for i, batch in enumerate(loader):
        print(f"    batch[{i}] features={len(batch['features'])} labels={batch['labels']}")

    # 10) Scalers
    scaler = StandardScaler().fit_transform([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    print("[10] StandardScaler:", scaler)
    mm = MinMaxScaler().fit_transform([[1.0], [5.0], [9.0]])
    print("     MinMaxScaler:", mm)
    enc = LabelEncoder().fit_transform(["a", "b", "a", "c"])
    print("     LabelEncoder:", enc)

    # 11) merge
    left = DataFrame([{"id": 1, "x": "a"}, {"id": 2, "x": "b"}])
    right = DataFrame([{"id": 1, "y": 10}, {"id": 3, "y": 30}])
    print("[11] merge inner:\n", left.merge(right, on="id", how="inner"))
    print("     merge left:\n", left.merge(right, on="id", how="left"))

    print("== 冒烟测试全部通过 ==")
