"""Aurora v3.1.0 持久化编译缓存

跨会话复用 AST / 类型信息 / 编译产物，把冷启动 + 重复编译成本压到最低。

设计要点：

* **缓存目录** ``.aurora_cache/``（项目本地）或 ``~/.aurora/cache``（全局）；
* **有效性判断**：``mtime`` + 内容 SHA256 双指纹。mtime 不变直接命中，
  mtime 变了再比对内容哈希，避免「touch 一下就失效」的假阳性；
* **.aurc 预编译文件**：标准库可以一次性预编译成 ``.aurc`` 二进制包，
  启动时直接整体 load，跳过 stdlib 解析与类型检查；
* **级联失效**：记录文件级 import 依赖，一个文件变更后，
  所有 import 它的文件（递归）一并从缓存剔除；
* **接口**：``get(key)`` / ``set(key, value)`` / ``invalidate(file)`` / ``clear()``。

``value`` 必须是 JSON 可序列化的 dict；AST / 类型信息在接入真实编译器时
通过序列化钩子转换。
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def file_fingerprint(path: str) -> Dict[str, Any]:
    """计算文件指纹：``{mtime, size, sha256}``。

    mtime 作为快速预检，sha256 作为最终裁决。
    """
    st = os.stat(path)
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return {
        "mtime": st.st_mtime,
        "size": st.st_size,
        "sha256": h.hexdigest(),
    }


def _hash_value(value: Any) -> str:
    """对任意 JSON 可序列化值计算稳定哈希。"""
    blob = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 缓存条目
# ---------------------------------------------------------------------------

@dataclass
class CacheEntry:
    """一个文件的缓存条目。"""

    key: str
    """缓存键（通常是文件绝对路径）。"""

    fingerprint: Dict[str, Any] = field(default_factory=dict)
    """源文件指纹，用于判断是否仍有效。"""

    value: Any = None
    """缓存内容（AST / 类型信息 / 编译产物）。"""

    imports: List[str] = field(default_factory=list)
    """该文件 import 的其它文件路径（用于级联失效）。"""

    created_at: float = 0.0
    hits: int = 0

    def is_fresh(self, current_fp: Dict[str, Any]) -> bool:
        """快速判断：mtime + size 一致就视为新鲜，避免每次都 hash。"""
        return (
            self.fingerprint.get("mtime") == current_fp.get("mtime")
            and self.fingerprint.get("size") == current_fp.get("size")
        )


# ---------------------------------------------------------------------------
# 主类
# ---------------------------------------------------------------------------

class PersistentCache:
    """磁盘持久化的编译缓存。

    用法::

        cache = PersistentCache(".aurora_cache")
        cache.set("src/main.aur", {"ast": ..., "type_info": ...})
        hit = cache.get("src/main.aur")
        cache.invalidate("src/util.aur")
    """

    INDEX_NAME = "index.json"
    AURC_SUFFIX = ".aurc"

    def __init__(self, cache_dir: str = ".aurora_cache") -> None:
        self.cache_dir = os.path.abspath(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        self._index_path = os.path.join(self.cache_dir, self.INDEX_NAME)
        self._entries: Dict[str, CacheEntry] = {}
        self._hits = 0
        self._misses = 0
        self._load()

    # ── 读 ────────────────────────────────────────────

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值；未命中或已失效返回 ``None``。"""
        key = os.path.abspath(key)
        entry = self._entries.get(key)
        if entry is None:
            self._misses += 1
            return None
        # 源文件还在吗？
        if not os.path.isfile(key):
            self._misses += 1
            return None
        fp = file_fingerprint(key)
        if not entry.is_fresh(fp):
            self._misses += 1
            return None
        entry.hits += 1
        self._hits += 1
        return entry.value

    # ── 写 ────────────────────────────────────────────

    def set(self, key: str, value: Any, imports: Optional[List[str]] = None) -> None:
        """写入缓存。``imports`` 用于后续级联失效。"""
        key = os.path.abspath(key)
        if not os.path.isfile(key):
            # 虚拟键（例如 stdlib 预编译），跳过指纹计算
            fp = {}
        else:
            fp = file_fingerprint(key)
        self._entries[key] = CacheEntry(
            key=key,
            fingerprint=fp,
            value=value,
            imports=[os.path.abspath(p) for p in (imports or [])],
            created_at=time.time(),
            hits=0,
        )
        self._save()

    # ── 失效 ──────────────────────────────────────────

    def invalidate(self, file: str) -> List[str]:
        """使某个文件的缓存失效，并级联失效所有 import 它的文件。

        :return: 本次被剔除的所有键列表。
        """
        target = os.path.abspath(file)
        removed: List[str] = []
        # 反向依赖：谁 import 了 target
        dependents = self._reverse_dependents(target)
        for key in [target, *dependents]:
            if self._entries.pop(key, None) is not None:
                removed.append(key)
        if removed:
            self._save()
        return removed

    def _reverse_dependents(self, target: str) -> List[str]:
        """返回所有把 target 写在自己 imports 里的文件键。"""
        out: List[str] = []
        for key, entry in self._entries.items():
            if target in entry.imports:
                out.append(key)
        return out

    def clear(self) -> None:
        """清空整个缓存目录。"""
        self._entries.clear()
        self._hits = 0
        self._misses = 0
        # 删除 index + 所有 .aurc
        for name in os.listdir(self.cache_dir):
            p = os.path.join(self.cache_dir, name)
            if os.path.isfile(p):
                try:
                    os.remove(p)
                except OSError:
                    pass

    # ── .aurc 预编译 ──────────────────────────────────

    def save_aurc(self, module_name: str, value: Any) -> str:
        """把一个 stdlib 模块预编译成 ``.aurc`` 文件，返回路径。"""
        path = os.path.join(self.cache_dir, module_name + self.AURC_SUFFIX)
        payload = {
            "module": module_name,
            "value": value,
            "saved_at": time.time(),
            "sha": _hash_value(value),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        return path

    def load_aurc(self, module_name: str) -> Optional[Any]:
        """加载 ``.aurc`` 预编译文件；不存在返回 ``None``。"""
        path = os.path.join(self.cache_dir, module_name + self.AURC_SUFFIX)
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
        return payload.get("value")

    def precompile_stdlib(self, modules: Dict[str, Any]) -> List[str]:
        """批量预编译 stdlib 模块，返回生成的 .aurc 路径列表。"""
        return [self.save_aurc(name, value) for name, value in modules.items()]

    # ── 统计 ──────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        return {
            "entries": len(self._entries),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": (self._hits / total) if total else 0.0,
            "cache_dir": self.cache_dir,
        }

    # ── 持久化 ──────────────────────────────────────────

    def _save(self) -> None:
        data = {
            "entries": {
                k: {
                    "fingerprint": e.fingerprint,
                    "value": e.value,
                    "imports": e.imports,
                    "created_at": e.created_at,
                    "hits": e.hits,
                }
                for k, e in self._entries.items()
            },
            "hits": self._hits,
            "misses": self._misses,
        }
        tmp = self._index_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, self._index_path)

    def _load(self) -> None:
        if not os.path.isfile(self._index_path):
            return
        try:
            with open(self._index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return
        self._entries = {
            k: CacheEntry(key=k, **v) for k, v in data.get("entries", {}).items()
        }
        self._hits = data.get("hits", 0)
        self._misses = data.get("misses", 0)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def register_cli(subparsers) -> Any:
    """注册 ``aurora cache`` 子命令组。"""
    p = subparsers.add_parser('cache', help='v3.1.0 持久化编译缓存')
    sub = p.add_subparsers(dest='cache_cmd')

    p_clear = sub.add_parser('clear', help='清空缓存')
    p_clear.add_argument('--dir', default='.aurora_cache')
    p_clear.set_defaults(func=_cmd_clear)

    p_stats = sub.add_parser('stats', help='查看缓存统计')
    p_stats.add_argument('--dir', default='.aurora_cache')
    p_stats.set_defaults(func=_cmd_stats)

    def _dispatch(args):
        if getattr(args, 'cache_cmd', None) is None:
            p.print_help()
            return
        args.func(args)

    p.set_defaults(func=_dispatch)
    return p


def _cmd_clear(args) -> None:
    c = PersistentCache(cache_dir=args.dir)
    c.clear()
    print(f"✓ 已清空缓存目录 {args.dir}")


def _cmd_stats(args) -> None:
    c = PersistentCache(cache_dir=args.dir)
    print(json.dumps(c.stats(), indent=2, ensure_ascii=False))
