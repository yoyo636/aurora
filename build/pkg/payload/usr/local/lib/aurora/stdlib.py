"""Aurora 标准库 — 核心内建模块"""

import time
import math
import json
import os
import sys
import random
import ctypes
import subprocess
import html
import webbrowser
import shlex
import threading
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Callable

# ── Aurora AI 引擎集成（v3.0.0）──────────────────────────────────────
# 以延迟/容错方式导入 AI 模块。ai/ 不依赖 stdlib，正常情况下可直接导入；
# 若未来出现循环依赖或可选依赖缺失，这里的 try/except 保证 stdlib 仍可加载，
# 对应 std.* AI 模块在 STDLIB_MODULES 中退化为空占位（不影响其他功能）。
try:
    from aurora.ai.tensor import Tensor as _AuroraTensor
    from aurora.ai.autograd import (
        Variable as _AuroraVariable,
        SGD as _AuroraSGD,
        Adam as _AuroraAdam,
    )
    from aurora.ai import nn as _aurora_nn
    from aurora.ai.data import (
        DataFrame as _AuroraDataFrame,
        Dataset as _AuroraDataset,
        DataLoader as _AuroraDataLoader,
    )
    from aurora.ai.agent import (
        Agent as _AuroraAgent,
        LLM as _AuroraLLM,            # 工厂函数：根据 provider 创建 OpenAI/Anthropic/local 后端
        PromptTemplate as _AuroraPromptTemplate,
        LLMChain as _AuroraLLMChain,
    )
    from aurora.ai.inference import (
        InferenceEngine as _AuroraInferenceEngine,
        InferenceServer as _AuroraInferenceServer,
    )
    from aurora.ai.decorators import ai as _AuroraAIDecorator
    _AURORA_AI_AVAILABLE = True
except Exception as _ai_import_err:  # pragma: no cover - 容错降级
    _AURORA_AI_AVAILABLE = False
    _ai_import_err = _ai_import_err


class AuroraError(Exception):
    """Aurora 运行时异常基类"""
    def __init__(self, kind: str, message: str, line: int = 0, column: int = 0):
        self.kind = kind
        self.line = line
        self.column = column
        loc = f"L{line}:C{column}: " if line else ""
        super().__init__(f"{loc}[{kind}] {message}")


# 通道"空"哨兵（区别于合法的 None 值）
_CH_EMPTY = object()


class AuroraChannel:
    """通道 — Go 风格 channel 实现"""
    def __init__(self, capacity: int = 0):
        import threading
        import queue
        self.capacity = capacity
        self._queue = queue.Queue(maxsize=capacity if capacity > 0 else 0)
        self._closed = False
        self._lock = threading.Lock()

    def send(self, value):
        if self._closed:
            raise AuroraError("ChannelError", "向已关闭的通道发送数据")
        self._queue.put(value)

    def recv(self):
        try:
            return self._queue.get(timeout=0.1)
        except Exception:
            return _CH_EMPTY

    def recv_nowait(self):
        """非阻塞接收；通道为空时返回哨兵"""
        try:
            return self._queue.get_nowait()
        except Exception:
            return _CH_EMPTY

    def recv_blocking(self):
        """阻塞接收，直到通道有值或通道已关闭且为空"""
        while True:
            val = self.recv()
            if val is not _CH_EMPTY:
                return val
            if self.is_closed():
                return _CH_EMPTY

    def close(self):
        with self._lock:
            self._closed = True

    def is_closed(self):
        return self._closed and self._queue.empty()

    def __iter__(self):
        while True:
            val = self.recv()
            if val is _CH_EMPTY:
                if self._closed:
                    break
                continue
            yield val


class AuroraMutex:
    """互斥锁 — Rust 风格 Mutex"""
    def __init__(self, value):
        import threading
        self._value = value
        self._lock = threading.Lock()
    
    def lock(self):
        self._lock.acquire()
        return MutexGuard(self)
    
    def __repr__(self):
        return f"Mutex({self._value!r})"


class MutexGuard:
    """Mutex 守卫 — RAII 风格锁管理"""
    def __init__(self, mutex: AuroraMutex):
        self._mutex = mutex
    
    def get(self):
        return self._mutex._value
    
    def set(self, value):
        self._mutex._value = value
    
    def release(self):
        self._mutex._lock.release()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.release()
    
    def __del__(self):
        try:
            self.release()
        except Exception:
            pass


class AuroraFiber:
    """轻量协程 — Go 风格 goroutine 封装"""
    _next_id = 0
    
    def __init__(self, func, args=(), kwargs=None):
        import threading
        AuroraFiber._next_id += 1
        self.id = AuroraFiber._next_id
        self._thread = threading.Thread(target=func, args=args, kwargs=kwargs or {}, daemon=True)
        self._result = None
        self._error = None
    
    def start(self):
        self._thread.start()
        return self
    
    def join(self, timeout=None):
        self._thread.join(timeout=timeout)
    
    def is_alive(self):
        return self._thread.is_alive()


class AuroraEnumVariant:
    """枚举变体值 — 携带变体名与命名字段

    - 支持属性访问 v.field、索引访问 v[key]
    - 支持 == / != 值比较与 repr
    - 支持模式匹配（解释器按 _name 与字段顺序对齐）
    """

    def __init__(self, name: str, fields: Dict[str, Any] = None):
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_fields', dict(fields or {}))
        object.__setattr__(self, '_order', list((fields or {}).keys()))

    def __getattr__(self, key):
        fields = object.__getattribute__(self, '_fields')
        if key in fields:
            return fields[key]
        raise AttributeError(f"枚举变体 {self._name} 没有字段 '{key}'")

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            object.__getattribute__(self, '_fields')[key] = value

    def __getitem__(self, key):
        return self._fields[key]

    def __setitem__(self, key, value):
        self._fields[key] = value

    def __iter__(self):
        return iter(self._fields)

    def get(self, key, default=None):
        return self._fields.get(key, default)

    def __repr__(self):
        inner = ', '.join(f"{k}={v!r}" for k, v in self._fields.items())
        return f"{self._name}({inner})" if inner else f"{self._name}()"

    def __eq__(self, other):
        return (isinstance(other, AuroraEnumVariant)
                and self._name == other._name
                and self._fields == other._fields)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._name, tuple(sorted(self._fields.items()))))


class AuroraResult:
    """Result 类型 — Rust 风格错误处理"""
    def __init__(self, ok=None, err=None):
        self._ok = ok
        self._err = err
    
    @staticmethod
    def Ok(value):
        return AuroraResult(ok=value)
    
    @staticmethod
    def Err(msg):
        return AuroraResult(err=msg)
    
    def is_ok(self):
        return self._err is None
    
    def is_err(self):
        return self._err is not None
    
    def unwrap(self):
        if self.is_err():
            raise AuroraError("UnwrapError", f"对 Err 调用 unwrap(): {self._err}")
        return self._ok
    
    def unwrap_or(self, default):
        return self._ok if self.is_ok() else default
    
    def map(self, func):
        if self.is_ok():
            try:
                return AuroraResult.Ok(func(self._ok))
            except Exception as e:
                return AuroraResult.Err(str(e))
        return self
    
    def __repr__(self):
        if self.is_ok():
            return f"Ok({self._ok!r})"
        return f"Err({self._err!r})"


class AuroraString:
    """字符串工具模块"""
    @staticmethod
    def split(s: str, sep: str = None) -> list:
        return s.split(sep)
    
    @staticmethod
    def join(parts: list, sep: str = "") -> str:
        return sep.join(str(p) for p in parts)
    
    @staticmethod
    def replace(s: str, old: str, new: str) -> str:
        return s.replace(old, new)
    
    @staticmethod
    def contains(s: str, sub: str) -> bool:
        return sub in s

    @staticmethod
    def find(s: str, sub: str, start: int = 0) -> int:
        return s.find(sub, start)

    @staticmethod
    def substring(s: str, start: int, end: int = -1) -> str:
        if end < 0:
            return s[start:]
        return s[start:end]

    @staticmethod
    def len(s: str) -> int:
        return len(s)

    @staticmethod
    def char_at(s: str, index: int) -> str:
        return s[index]
    
    @staticmethod
    def starts_with(s: str, prefix: str) -> bool:
        return s.startswith(prefix)
    
    @staticmethod
    def ends_with(s: str, suffix: str) -> bool:
        return s.endswith(suffix)
    
    @staticmethod
    def trim(s: str) -> str:
        return s.strip()
    
    @staticmethod
    def upper(s: str) -> str:
        return s.upper()
    
    @staticmethod
    def lower(s: str) -> str:
        return s.lower()
    
    @staticmethod
    def format(template: str, **kwargs) -> str:
        return template.format(**kwargs)


class AuroraIO:
    """IO 模块"""
    @staticmethod
    def read_file(path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise AuroraError("IOError", str(e))
    
    @staticmethod
    def write_file(path: str, content: str):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise AuroraError("IOError", str(e))
    
    @staticmethod
    def append_file(path: str, content: str):
        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise AuroraError("IOError", str(e))
    
    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def read_line(prompt: str = "") -> str:
        return input(prompt)

    @staticmethod
    def list_dir(path: str = ".") -> list:
        """列出目录内容(名称)"""
        try:
            return sorted(os.listdir(path))
        except Exception as e:
            raise AuroraError("IOError", str(e))

    @staticmethod
    def mkdir(path: str) -> bool:
        """递归创建目录,已存在返回 False"""
        try:
            if os.path.isdir(path):
                return False
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            raise AuroraError("IOError", str(e))

    @staticmethod
    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def files(dir_path: str = ".", ext: str = "") -> list:
        """列出目录下文件(可选按扩展名过滤,ext 如 .aur)"""
        out = []
        try:
            for n in sorted(os.listdir(dir_path)):
                p = os.path.join(dir_path, n)
                if os.path.isfile(p) and (not ext or n.endswith(ext)):
                    out.append(n)
            return out
        except Exception as e:
            raise AuroraError("IOError", str(e))


class AuroraMath:
    """数学模块"""
    PI = math.pi
    E = math.e
    INF = math.inf
    
    @staticmethod
    def abs(x): return abs(x)
    @staticmethod
    def sqrt(x): return math.sqrt(x)
    @staticmethod
    def pow(base, exp): return math.pow(base, exp)
    @staticmethod
    def floor(x): return math.floor(x)
    @staticmethod
    def ceil(x): return math.ceil(x)
    @staticmethod
    def round(x, n=0): return round(x, n)
    @staticmethod
    def min(*args): return min(*args)
    @staticmethod
    def max(*args): return max(*args)
    @staticmethod
    def sin(x): return math.sin(x)
    @staticmethod
    def cos(x): return math.cos(x)
    @staticmethod
    def tan(x): return math.tan(x)
    @staticmethod
    def log(x, base=None): return math.log(x, base) if base else math.log(x)
    @staticmethod
    def random(): return random.random()
    @staticmethod
    def randint(a, b): return random.randint(a, b)


class AuroraTime:
    """时间模块"""
    @staticmethod
    def now() -> float:
        return time.time()
    
    @staticmethod
    def sleep(ms: int):
        time.sleep(ms / 1000.0)
    
    @staticmethod
    def timestamp() -> int:
        return int(time.time())
    
    @staticmethod
    def format_time(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        return time.strftime(fmt)


class AuroraJson:
    """JSON 模块"""
    @staticmethod
    def parse(s: str):
        try:
            return json.loads(s)
        except Exception as e:
            raise AuroraError("JsonError", str(e))

    @staticmethod
    def stringify(obj, indent=None) -> str:
        return json.dumps(obj, indent=indent, ensure_ascii=False)

    @staticmethod
    def load(path: str):
        """读取 JSON 文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise AuroraError("JsonError", f"读取 {path}: {e}")

    @staticmethod
    def save(path: str, obj, indent=2) -> str:
        """写入 JSON 文件,返回文件路径"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=indent)
            return path
        except Exception as e:
            raise AuroraError("JsonError", f"写入 {path}: {e}")


class AuroraPython:
    """Python 桥:直接在 Aurora 中执行 Python、导入任意 Python 库
    安全提示:python.eval 可执行任意代码,仅用于本地可信环境"""

    @staticmethod
    def eval(code: str):
        """求值 Python 表达式,结果直接作为 Aurora 值返回"""
        try:
            return eval(code, {'__builtins__': __builtins__}, {})
        except Exception as e:
            raise AuroraError("PythonError", str(e))

    @staticmethod
    def exec(code: str) -> str:
        """执行 Python 语句(无返回值)"""
        try:
            exec(code, {'__builtins__': __builtins__}, {})
            return "ok"
        except Exception as e:
            raise AuroraError("PythonError", str(e))

    @staticmethod
    def import_module(name: str):
        """导入 Python 模块,返回模块对象(可直接取属性、调用函数)"""
        try:
            return __import__(name, fromlist=['*'])
        except Exception as e:
            raise AuroraError("PythonError", f"导入模块 {name}: {e}")

    @staticmethod
    def call(fn, *args):
        """调用任意 Python 可调用对象"""
        try:
            return fn(*args)
        except Exception as e:
            raise AuroraError("PythonError", str(e))

    @staticmethod
    def version() -> str:
        return sys.version.split()[0]


class AuroraFFI:
    """FFI:C ABI 共享库桥(Rust #[no_mangle] extern "C" / C++ extern "C" 导出)"""

    _TYPES = {
        'i8': ctypes.c_int8, 'i16': ctypes.c_int16, 'i32': ctypes.c_int32,
        'i64': ctypes.c_int64, 'u8': ctypes.c_uint8, 'u16': ctypes.c_uint16,
        'u32': ctypes.c_uint32, 'u64': ctypes.c_uint64,
        'f32': ctypes.c_float, 'f64': ctypes.c_double,
        'bool': ctypes.c_bool, 'void': None,
        'str': ctypes.c_char_p, 'ptr': ctypes.c_void_p,
        'char': ctypes.c_char,
    }

    @staticmethod
    def load(path: str):
        """加载共享库:macOS .dylib / Linux .so / Windows .dll"""
        try:
            return ctypes.CDLL(os.path.abspath(path))
        except Exception as e:
            raise AuroraError("FFIError", f"加载库 {path}: {e}")

    @staticmethod
    def func(lib, name: str, arg_types: list, ret_type: str = 'void'):
        """声明库函数签名,返回可直接调用的包装函数"""
        try:
            fn = getattr(lib, name)
        except AttributeError:
            raise AuroraError("FFIError", f"库中没有符号 '{name}'")
        ret = AuroraFFI._TYPES.get(ret_type)
        if ret is not None:
            fn.restype = ret
        fn.argtypes = [AuroraFFI._TYPES.get(t, ctypes.c_void_p) for t in arg_types]

        def wrapper(*args):
            try:
                return fn(*args)
            except Exception as e:
                raise AuroraError("FFIError", str(e))
        wrapper.__name__ = name
        return wrapper

    @staticmethod
    def cstr(s: str) -> bytes:
        """把 Aurora 字符串转成 C 字符串(用于 str 参数)"""
        return s.encode('utf-8')

    @staticmethod
    def struct(name: str, fields: list):
        """定义 C 结构体类型,fields 为 [(字段名, C类型字符串), ...],返回 ctypes.Structure 子类"""
        try:
            return type(name, (ctypes.Structure,), {
                '_fields_': [(fn, AuroraFFI._TYPES.get(ft, ctypes.c_void_p)) for fn, ft in fields],
            })
        except Exception as e:
            raise AuroraError("FFIError", f"定义结构体 {name}: {e}")

    @staticmethod
    def callback(ret_type: str, arg_types: list):
        """创建 C 回调函数类型,返回 CFUNCTYPE 工厂,用于把 Python 函数传给 C 库"""
        try:
            ret = AuroraFFI._TYPES.get(ret_type, ctypes.c_void_p)
            args = [AuroraFFI._TYPES.get(t, ctypes.c_void_p) for t in arg_types]
            return ctypes.CFUNCTYPE(ret, *args)
        except Exception as e:
            raise AuroraError("FFIError", f"创建回调类型: {e}")

    @staticmethod
    def string_array(strings: list):
        """把 Python 字符串列表转成 C 字符串数组(char*[])"""
        try:
            arr_type = ctypes.c_char_p * len(strings)
            return arr_type(*[s.encode('utf-8') for s in strings])
        except Exception as e:
            raise AuroraError("FFIError", f"创建字符串数组: {e}")

    @staticmethod
    def ptr(value, c_type: str = 'i32'):
        """创建指向值的指针,返回 ctypes.pointer 对象"""
        try:
            ctor = AuroraFFI._TYPES.get(c_type, ctypes.c_void_p)
            return ctypes.pointer(ctor(value))
        except Exception as e:
            raise AuroraError("FFIError", f"创建指针: {e}")

    @staticmethod
    def deref(ptr_obj):
        """解引用指针,返回指向的值"""
        try:
            return ptr_obj.contents.value
        except Exception as e:
            raise AuroraError("FFIError", f"解引用指针: {e}")

    @staticmethod
    def gen_bindings(lang: str, functions: list, output_path: str = None) -> str:
        """为 Rust/C++/Go 生成 FFI 绑定模板代码
        functions: [{"name": "add", "args": ["i32","i32"], "ret": "i32"}, ...]
        返回生成的代码字符串;若提供 output_path 则同时写入文件"""
        c_types = {
            'i8': 'int8_t', 'i16': 'int16_t', 'i32': 'int32_t', 'i64': 'int64_t',
            'u8': 'uint8_t', 'u16': 'uint16_t', 'u32': 'uint32_t', 'u64': 'uint64_t',
            'f32': 'float', 'f64': 'double', 'bool': 'bool', 'void': 'void',
        }
        rust_types = {
            'i8': 'i8', 'i16': 'i16', 'i32': 'i32', 'i64': 'i64',
            'u8': 'u8', 'u16': 'u16', 'u32': 'u32', 'u64': 'u64',
            'f32': 'f32', 'f64': 'f64', 'bool': 'bool', 'void': '()',
        }
        go_types = {
            'i8': 'int8', 'i16': 'int16', 'i32': 'int32', 'i64': 'int64',
            'u8': 'uint8', 'u16': 'uint16', 'u32': 'uint32', 'u64': 'uint64',
            'f32': 'float32', 'f64': 'float64', 'bool': 'bool', 'void': '',
        }
        try:
            if lang == "rust":
                lines = ["#![allow(non_snake_case)]", ""]
                for f in functions:
                    name = f["name"]
                    args = ", ".join(
                        f"a{i}: {rust_types.get(t, 'i64')}" for i, t in enumerate(f["args"])
                    )
                    ret_key = f.get("ret", "void")
                    ret = rust_types.get(ret_key, "i64")
                    ret_sig = f" -> {ret}" if ret_key != "void" else ""
                    lines.append("#[no_mangle]")
                    lines.append(f'pub extern "C" fn {name}({args}){ret_sig} {{')
                    lines.append("    unimplemented!()")
                    lines.append("}")
                    lines.append("")
                code = "\n".join(lines)
            elif lang == "cpp":
                lines = ['#include <stdint.h>', '#include <stdbool.h>', '', 'extern "C" {', '']
                for f in functions:
                    name = f["name"]
                    ret = c_types.get(f.get("ret", "i32"), "int64_t")
                    args = ", ".join(
                        f"{c_types.get(t, 'int64_t')} a{i}" for i, t in enumerate(f["args"])
                    )
                    args = args if args else "void"
                    lines.append(f'extern "C" {ret} {name}({args}) {{')
                    lines.append(f"    // TODO: 实现 {name}")
                    lines.append(f"    return ({ret})0;")
                    lines.append("}")
                    lines.append("")
                lines.append("}")
                code = "\n".join(lines)
            elif lang == "go":
                lines = ['package main', '', 'import "C"', '']
                for f in functions:
                    name = f["name"]
                    ret_key = f.get("ret", "void")
                    ret = go_types.get(ret_key, "int64")
                    args = ", ".join(
                        f"a{i} {go_types.get(t, 'int64')}" for i, t in enumerate(f["args"])
                    )
                    ret_sig = f" {ret}" if ret_key != "void" else ""
                    lines.append(f"//export {name}")
                    lines.append(f"func {name}({args}){ret_sig} {{")
                    lines.append(f"    // TODO: 实现 {name}")
                    if ret_key != "void":
                        lines.append(f"    return {ret}(0)")
                    lines.append("}")
                    lines.append("")
                lines.append("func main() {}")
                code = "\n".join(lines)
            else:
                raise AuroraError("FFIError", f"不支持的绑定语言: {lang}")
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as fh:
                    fh.write(code)
            return code
        except AuroraError:
            raise
        except Exception as e:
            raise AuroraError("FFIError", f"生成绑定: {e}")


class AuroraJS:
    """JavaScript/TypeScript 桥:通过 Node.js 子进程执行 JS/TS 代码
    安全提示:js.eval 可执行任意代码,仅用于本地可信环境"""

    @staticmethod
    def _run(args_list: list, timeout: float) -> subprocess.CompletedProcess:
        """内部:运行 Node.js 子进程并处理超时/异常"""
        try:
            return subprocess.run(args_list, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"JS 执行超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("JSError", "未找到 node 可执行文件")
        except Exception as e:
            raise AuroraError("JSError", str(e))

    @staticmethod
    def _parse_stderr(text: str) -> str:
        """解析 JS 错误输出(优先取 JSON 中的 error/message)"""
        text = (text or "").strip()
        if not text:
            return "未知错误"
        try:
            obj = json.loads(text)
            if isinstance(obj, dict) and 'error' in obj:
                stack = obj.get('stack', '')
                return f"{obj['error']}\n{stack}" if stack else str(obj['error'])
        except Exception:
            pass
        return text

    @staticmethod
    def _json_out(stdout: str):
        """把 stdout 解析为 JSON,失败时返回原始文本"""
        out = (stdout or "").strip()
        try:
            return json.loads(out)
        except Exception:
            return out

    @staticmethod
    def eval(code: str, timeout: float = 30.0):
        """通过 node -e 执行 JS 表达式,用 JSON.stringify 包装返回值并解析"""
        script = (
            "try { console.log(JSON.stringify(eval(%s))) } "
            "catch(e) { console.error(JSON.stringify({error: e.message, stack: e.stack})); process.exit(1) }"
        ) % json.dumps(code, ensure_ascii=False)
        proc = AuroraJS._run(["node", "-e", script], timeout)
        if proc.returncode != 0:
            raise AuroraError("JSError", AuroraJS._parse_stderr(proc.stderr))
        return AuroraJS._json_out(proc.stdout)

    @staticmethod
    def call(fn_name: str, *args, timeout: float = 30.0):
        """调用全局 JS 函数,args 通过 JSON 序列化传入"""
        args_json = json.dumps(list(args), ensure_ascii=False)
        script = (
            "try { console.log(JSON.stringify(globalThis[%s](...%s))) } "
            "catch(e) { console.error(JSON.stringify({error: e.message, stack: e.stack})); process.exit(1) }"
        ) % (json.dumps(fn_name, ensure_ascii=False), args_json)
        proc = AuroraJS._run(["node", "-e", script], timeout)
        if proc.returncode != 0:
            raise AuroraError("JSError", AuroraJS._parse_stderr(proc.stderr))
        return AuroraJS._json_out(proc.stdout)

    @staticmethod
    def require(module: str, timeout: float = 30.0):
        """require Node.js 模块,返回数据属性(函数无法序列化,标记为 [Function])"""
        script = (
            "const m = require(%s); "
            "console.log(JSON.stringify(m, (k,v)=>typeof v==='function'?'[Function]':v))"
        ) % json.dumps(module, ensure_ascii=False)
        proc = AuroraJS._run(["node", "-e", script], timeout)
        if proc.returncode != 0:
            raise AuroraError("JSError", AuroraJS._parse_stderr(proc.stderr))
        return AuroraJS._json_out(proc.stdout)

    @staticmethod
    def run_file(path: str, args: list = None, timeout: float = 30.0):
        """运行 .js/.ts 文件,返回 {code, out, err}
        .ts 自动检测:优先 ts-node,其次 npx ts-node,最后 tsc 编译到临时目录"""
        import shutil
        args = list(args or [])
        apath = os.path.abspath(path)
        ext = os.path.splitext(apath)[1].lower()
        try:
            if ext == '.ts':
                return AuroraJS._run_ts(apath, args, timeout)
            proc = subprocess.run(["node", apath] + args, capture_output=True, text=True, timeout=timeout)
            return {"code": proc.returncode, "out": proc.stdout, "err": proc.stderr}
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"JS 文件执行超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("JSError", "未找到 node 可执行文件")
        except AuroraError:
            raise
        except Exception as e:
            raise AuroraError("JSError", str(e))

    @staticmethod
    def _run_ts(path: str, args: list, timeout: float) -> dict:
        """内部:运行 TS 文件,依次尝试 ts-node / npx ts-node / tsc 编译"""
        import shutil
        import tempfile
        # 优先本地 ts-node
        if shutil.which("ts-node"):
            proc = subprocess.run(["ts-node", path] + args,
                                  capture_output=True, text=True, timeout=timeout)
            return {"code": proc.returncode, "out": proc.stdout, "err": proc.stderr}
        # 其次 npx ts-node
        try:
            proc = subprocess.run(["npx", "-y", "ts-node", path] + args,
                                  capture_output=True, text=True, timeout=timeout)
            return {"code": proc.returncode, "out": proc.stdout, "err": proc.stderr}
        except Exception:
            pass
        # 最后 tsc 编译到临时目录再用 node 运行
        tmpdir = tempfile.mkdtemp(prefix="aurora_ts_")
        try:
            cproc = subprocess.run(["tsc", path, "--outDir", tmpdir, "--target", "ES2019"],
                                   capture_output=True, text=True, timeout=timeout)
            if cproc.returncode != 0:
                raise AuroraError("JSError", f"tsc 编译失败: {cproc.stderr}")
            js_name = os.path.splitext(os.path.basename(path))[0] + ".js"
            js_path = os.path.join(tmpdir, js_name)
            proc = subprocess.run(["node", js_path] + args,
                                  capture_output=True, text=True, timeout=timeout)
            return {"code": proc.returncode, "out": proc.stdout, "err": proc.stderr}
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"TS 执行超时({timeout}s)")
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @staticmethod
    def version() -> str:
        """返回 Node.js 版本字符串"""
        try:
            proc = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
            return (proc.stdout or proc.stderr).strip()
        except Exception as e:
            raise AuroraError("JSError", f"获取 Node 版本: {e}")

    @staticmethod
    def available() -> bool:
        """检测 node 是否可用"""
        import shutil
        if shutil.which("node"):
            return True
        try:
            subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
            return True
        except Exception:
            return False


class AuroraJava:
    """Java 桥:通过 java/jshell 子进程调用 Java 代码
    支持 .class / .jar 文件,类路径配置"""

    @staticmethod
    def _java_arg(v) -> str:
        """把 Python 值转成 Java 表达式字符串(类型自动推断)"""
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, int):
            return f"(long) {v}"
        if isinstance(v, float):
            return f"(double) {repr(v)}"
        if isinstance(v, str):
            return json.dumps(v, ensure_ascii=False)
        if isinstance(v, (list, tuple)):
            if not v:
                return "new String[0]"
            first = v[0]
            if isinstance(first, bool):
                return "new boolean[]{" + ",".join("true" if x else "false" for x in v) + "}"
            if isinstance(first, int):
                return "new long[]{" + ",".join(str(int(x)) for x in v) + "}"
            if isinstance(first, float):
                return "new double[]{" + ",".join(repr(float(x)) for x in v) + "}"
            return "new String[]{" + ",".join(json.dumps(str(x), ensure_ascii=False) for x in v) + "}"
        return json.dumps(str(v), ensure_ascii=False)

    @staticmethod
    def _parse_json_output(text: str):
        """解析 Java 输出为 Python 值,失败时返回原始文本"""
        text = (text or "").strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception:
            return text

    @staticmethod
    def call(class_name: str, method_name: str, *args, classpath: str = None, timeout: float = 30.0):
        """调用 Java 静态方法,参数类型按 Python 类型推断,返回反序列化后的结果"""
        import shutil
        import tempfile
        arg_exprs = ", ".join(AuroraJava._java_arg(a) for a in args)
        # 注意:此处使用原始字符串保留 Java 转义,通过 %s 注入类名/方法名/实参
        src = r'''import java.util.Arrays;
public class AuroraCallMain {
  public static void main(String[] argv) {
    Object result = %s.%s(%s);
    AuroraCallMain.printJson(result);
  }
  static void printJson(Object r) {
    if (r == null) { System.out.println("null"); return; }
    if (r instanceof Number) { System.out.println(r.toString()); return; }
    if (r instanceof Boolean) { System.out.println(Boolean.toString((Boolean)r)); return; }
    if (r instanceof String) { System.out.println("\"" + ((String)r).replace("\\", "\\\\").replace("\"", "\\\"") + "\""); return; }
    if (r.getClass().isArray()) { System.out.println(Arrays.toString((Object[])r)); return; }
    System.out.println("\"" + r.toString().replace("\\", "\\\\").replace("\"", "\\\"") + "\"");
  }
}
''' % (class_name, method_name, arg_exprs)
        tmpdir = tempfile.mkdtemp(prefix="aurora_java_")
        try:
            src_path = os.path.join(tmpdir, "AuroraCallMain.java")
            with open(src_path, 'w', encoding='utf-8') as f:
                f.write(src)
            cp_parts = [tmpdir]
            if classpath:
                cp_parts.append(classpath)
            cp = os.pathsep.join(cp_parts)
            cproc = subprocess.run(["javac", src_path], capture_output=True, text=True, timeout=timeout)
            if cproc.returncode != 0:
                raise AuroraError("JavaError", f"编译失败: {cproc.stderr}")
            rproc = subprocess.run(["java", "-cp", cp, "AuroraCallMain"],
                                   capture_output=True, text=True, timeout=timeout)
            if rproc.returncode != 0:
                raise AuroraError("JavaError", f"运行失败: {rproc.stderr}")
            return AuroraJava._parse_json_output(rproc.stdout)
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"Java 调用超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("JavaError", "未找到 java/javac 可执行文件")
        except AuroraError:
            raise
        except Exception as e:
            raise AuroraError("JavaError", str(e))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @staticmethod
    def run(main_class: str, args: list = None, classpath: str = None, timeout: float = 30.0):
        """运行已编译的 Java 主类(class 或 jar 中的 main 类),返回 {code, out, err}"""
        args = list(args or [])
        cp = classpath or "."
        try:
            proc = subprocess.run(["java", "-cp", cp, main_class] + args,
                                  capture_output=True, text=True, timeout=timeout)
            return {"code": proc.returncode, "out": proc.stdout, "err": proc.stderr}
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"Java 运行超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("JavaError", "未找到 java 可执行文件")
        except Exception as e:
            raise AuroraError("JavaError", str(e))

    @staticmethod
    def _clean_jshell(text: str) -> str:
        """清理 jshell 输出:去掉欢迎信息、-> 与 $N ==> 前缀"""
        lines = []
        for ln in (text or "").splitlines():
            s = ln.strip()
            if not s:
                continue
            if s.startswith("Welcome") or s.startswith("|") or s.startswith("jshell>"):
                continue
            if s.startswith("$") and "==>" in s:
                s = s.split("==>", 1)[1].strip()
            if s.startswith("->"):
                s = s[2:].strip()
            if s:
                lines.append(s)
        return "\n".join(lines)

    @staticmethod
    def eval(code: str, timeout: float = 30.0):
        """通过 jshell 执行 Java 代码片段;jshell 不可用时回退到临时类编译运行"""
        import shutil
        if shutil.which("jshell"):
            try:
                proc = subprocess.run(["jshell", "-s"], input=code,
                                      capture_output=True, text=True, timeout=timeout)
                out = AuroraJava._clean_jshell(proc.stdout)
                if proc.returncode != 0 and not out:
                    raise AuroraError("JavaError", (proc.stderr or "jshell 执行失败").strip())
                return out
            except subprocess.TimeoutExpired:
                raise AuroraError("TimeoutError", f"jshell 超时({timeout}s)")
            except AuroraError:
                raise
            except Exception as e:
                raise AuroraError("JavaError", str(e))
        return AuroraJava._eval_fallback(code, timeout)

    @staticmethod
    def _eval_fallback(code: str, timeout: float):
        """内部回退:把代码包进临时 Java 类编译运行"""
        import shutil
        import tempfile
        src = (
            "public class AuroraEvalMain {\n"
            "  public static void main(String[] argv) {\n"
            + code + "\n"
            "  }\n"
            "}\n"
        )
        tmpdir = tempfile.mkdtemp(prefix="aurora_javaeval_")
        try:
            src_path = os.path.join(tmpdir, "AuroraEvalMain.java")
            with open(src_path, 'w', encoding='utf-8') as f:
                f.write(src)
            subprocess.run(["javac", src_path], capture_output=True, text=True, timeout=timeout)
            proc = subprocess.run(["java", "-cp", tmpdir, "AuroraEvalMain"],
                                  capture_output=True, text=True, timeout=timeout)
            if proc.returncode != 0:
                raise AuroraError("JavaError", proc.stderr)
            return proc.stdout.strip()
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"Java 编译运行超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("JavaError", "未找到 java/javac")
        except AuroraError:
            raise
        except Exception as e:
            raise AuroraError("JavaError", str(e))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @staticmethod
    def compile(source_path: str, classpath: str = None, output_dir: str = None, timeout: float = 30.0) -> str:
        """编译 Java 源文件(javac),返回输出目录路径"""
        import tempfile
        out_dir = output_dir or tempfile.mkdtemp(prefix="aurora_javac_")
        os.makedirs(out_dir, exist_ok=True)
        cmd = ["javac", "-d", out_dir]
        if classpath:
            cmd += ["-cp", classpath]
        cmd.append(source_path)
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if proc.returncode != 0:
                raise AuroraError("JavaError", f"编译 {source_path}: {proc.stderr}")
            return out_dir
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"Java 编译超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("JavaError", "未找到 javac")
        except AuroraError:
            raise
        except Exception as e:
            raise AuroraError("JavaError", str(e))

    @staticmethod
    def version() -> str:
        """返回 Java 版本字符串(java -version 的 stderr 第一行)"""
        try:
            proc = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=10)
            lines = (proc.stderr or proc.stdout or "").splitlines()
            return lines[0].strip() if lines else ""
        except Exception as e:
            raise AuroraError("JavaError", f"获取 Java 版本: {e}")

    @staticmethod
    def available() -> bool:
        """检测 java 是否可用"""
        import shutil
        if shutil.which("java"):
            return True
        try:
            subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=10)
            return True
        except Exception:
            return False


class AuroraInterop:
    """统一多语言互操作层:一个 API 调用所有支持的语言
    自动选择最佳调用方式(直连/FFI/子进程),类型自动转换"""

    @staticmethod
    def call(lang: str, code_or_fn: str, *args, **kwargs):
        """统一调用入口:lang ∈ python/js/java/c/cpp/rust/go"""
        if lang == "python":
            return AuroraPython.eval(code_or_fn)
        if lang == "js":
            if args:
                return AuroraJS.call(code_or_fn, *args, timeout=kwargs.get("timeout", 30.0))
            return AuroraJS.eval(code_or_fn, timeout=kwargs.get("timeout", 30.0))
        if lang == "java":
            if "." in code_or_fn:
                cls, method = code_or_fn.rsplit(".", 1)
                return AuroraJava.call(cls, method, *args,
                                       classpath=kwargs.get("classpath"),
                                       timeout=kwargs.get("timeout", 30.0))
            raise AuroraError("InteropError",
                              f"Java 调用需 ClassName.methodName 格式,收到: {code_or_fn}")
        if lang in ("c", "rust", "go", "cpp"):
            if ":" not in code_or_fn:
                raise AuroraError("InteropError",
                                  f"{lang} 调用需 libpath:symbol 格式,收到: {code_or_fn}")
            libpath, symbol = code_or_fn.split(":", 1)
            lib = AuroraFFI.load(libpath)
            arg_types = kwargs.get("arg_types")
            if arg_types is None:
                arg_types = ["i64"] * len(args)
            ret_type = kwargs.get("ret_type", "i64")
            fn = AuroraFFI.func(lib, symbol, arg_types, ret_type)
            return fn(*args)
        raise AuroraError("InteropError", f"不支持的语言: {lang}")

    @staticmethod
    def _import(lang: str, module: str):
        """统一导入模块"""
        if lang == "python":
            return AuroraPython.import_module(module)
        if lang == "js":
            return AuroraJS.require(module)
        if lang == "java":
            return {"class": module, "loaded": True}
        raise AuroraError("InteropError", f"不支持的语言导入: {lang}")

    @staticmethod
    def eval(lang: str, code: str, **kwargs):
        """统一求值代码"""
        if lang == "python":
            return AuroraPython.eval(code)
        if lang == "js":
            return AuroraJS.eval(code, timeout=kwargs.get("timeout", 30.0))
        if lang == "java":
            return AuroraJava.eval(code, timeout=kwargs.get("timeout", 30.0))
        raise AuroraError("InteropError", f"不支持的语言求值: {lang}")

    @staticmethod
    def languages() -> list:
        """返回所有支持语言的列表"""
        return ["python", "js", "java", "c", "cpp", "rust", "go"]

    @staticmethod
    def status() -> dict:
        """返回各语言桥的可用状态(python 恒为 True;c/cpp/rust/go 依赖 FFI 共享库)"""
        return {
            "python": True,
            "js": AuroraJS.available(),
            "java": AuroraJava.available(),
            "c": "ffi",
            "cpp": "ffi",
            "rust": "ffi",
            "go": "ffi",
        }


class AuroraWASM:
    """WebAssembly 桥:加载并调用 .wasm 模块
    通过 Node.js WebAssembly API 实现,是连接 Rust/Go/C++ 编译为 WASM 的桥梁"""

    @staticmethod
    def _node_run(script: str, timeout: float) -> subprocess.CompletedProcess:
        """内部:运行 Node.js 脚本并处理超时/异常"""
        try:
            return subprocess.run(["node", "-e", script],
                                   capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"WASM 执行超时({timeout}s)")
        except FileNotFoundError:
            raise AuroraError("WASMError", "未找到 node 可执行文件")
        except Exception as e:
            raise AuroraError("WASMError", str(e))

    @staticmethod
    def load(path: str, timeout: float = 30.0) -> dict:
        """加载 .wasm 模块,返回 {path, exports, loaded};exports 为 {函数名: 类型}"""
        apath = os.path.abspath(path)
        safe_path = json.dumps(apath, ensure_ascii=False)
        script = (
            "const fs = require('fs');\n"
            f"const bytes = fs.readFileSync({safe_path});\n"
            "WebAssembly.instantiate(bytes).then(result => {\n"
            "  const exports = {};\n"
            "  for (const k of Object.keys(result.instance.exports)) {\n"
            "    const v = result.instance.exports[k];\n"
            "    exports[k] = typeof v === 'function' ? 'function' : typeof v;\n"
            "  }\n"
            "  console.log(JSON.stringify({exports}));\n"
            "}).catch(e => { console.error(JSON.stringify({error: e.message})); process.exit(1); });\n"
        )
        proc = AuroraWASM._node_run(script, timeout)
        if proc.returncode != 0:
            raise AuroraError("WASMError", (proc.stderr or "").strip() or "加载 wasm 失败")
        try:
            data = json.loads(proc.stdout)
        except Exception:
            raise AuroraError("WASMError", f"解析 wasm 输出失败: {proc.stdout!r}")
        return {"path": apath, "exports": data.get("exports", {}), "loaded": True}

    @staticmethod
    def call(module: dict, fn_name: str, *args, timeout: float = 30.0):
        """调用 WASM 导出函数,args 必须是数字(i32/i64/f32/f64)"""
        apath = os.path.abspath(module.get("path", ""))
        safe_path = json.dumps(apath, ensure_ascii=False)
        safe_fn = json.dumps(fn_name, ensure_ascii=False)
        args_json = json.dumps(list(args), ensure_ascii=False)
        script = (
            "const fs = require('fs');\n"
            f"const bytes = fs.readFileSync({safe_path});\n"
            "WebAssembly.instantiate(bytes).then(inst => {\n"
            f"  const fn = inst.instance.exports[{safe_fn}];\n"
            "  if (typeof fn !== 'function') { console.error(JSON.stringify({error: '导出不是函数'})); process.exit(1); }\n"
            f"  const retval = fn(...{args_json});\n"
            "  console.log(JSON.stringify(retval));\n"
            "}).catch(e => { console.error(JSON.stringify({error: e.message})); process.exit(1); });\n"
        )
        proc = AuroraWASM._node_run(script, timeout)
        if proc.returncode != 0:
            raise AuroraError("WASMError", (proc.stderr or "").strip() or "调用 wasm 函数失败")
        out = (proc.stdout or "").strip()
        try:
            return json.loads(out)
        except Exception:
            return out

    @staticmethod
    def exports(path: str, timeout: float = 30.0) -> list:
        """列出 .wasm 模块的导出函数名列表"""
        info = AuroraWASM.load(path, timeout=timeout)
        return list(info.get("exports", {}).keys())

    @staticmethod
    def available() -> bool:
        """检测 node 是否可用(WASM 通过 Node.js 实现)"""
        import shutil
        if shutil.which("node"):
            return True
        try:
            subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
            return True
        except Exception:
            return False


class AuroraHtml:
    """HTML 桥:把 Aurora 数据渲染成网页"""
    @staticmethod
    def escape(s: str) -> str:
        return html.escape(str(s))

    @staticmethod
    def render(template: str, data: dict) -> str:
        """模板渲染:{{key}} 转义输出,{{!key}} 原始输出(嵌入 HTML 片段)"""
        out = template
        for k, v in (data or {}).items():
            out = out.replace("{{!" + k + "}}", str(v))
            out = out.replace("{{" + k + "}}", html.escape(str(v)))
        return out

    @staticmethod
    def page(title: str, body: str) -> str:
        """生成完整 HTML 文档"""
        return (
            "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n"
            "<meta charset=\"utf-8\">\n"
            f"<title>{html.escape(title)}</title>\n"
            "<style>body{font-family:system-ui,sans-serif;max-width:720px;"
            "margin:2rem auto;padding:0 1rem;color:#222;line-height:1.6}"
            "table{border-collapse:collapse}td,th{border:1px solid #ccc;"
            "padding:.3rem .6rem}h1{color:#1f8f86}</style>\n"
            "</head>\n<body>\n" + body + "\n</body>\n</html>"
        )

    @staticmethod
    def write(path: str, html_text: str) -> str:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        return path

    @staticmethod
    def open(path: str, html_text: str) -> str:
        """写入 HTML 并用默认浏览器打开"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        webbrowser.open("file://" + os.path.abspath(path))
        return path

    @staticmethod
    def link(href: str, text: str = None) -> str:
        """生成 <a> 链接"""
        return f'<a href="{html.escape(href, quote=True)}">{html.escape(text or href)}</a>'

    @staticmethod
    def list(items: list, ordered: bool = False, cls: str = "") -> str:
        """生成 <ul>/<ol> 列表"""
        tag = 'ol' if ordered else 'ul'
        cls_attr = f' class="{html.escape(cls, quote=True)}"' if cls else ''
        lis = ''.join(f'<li>{html.escape(str(x))}</li>' for x in items)
        return f'<{tag}{cls_attr}>{lis}</{tag}>'

    @staticmethod
    def json_script(data, id: str = "aurora-data") -> str:
        """把 Aurora 数据嵌入页面 <script>,前端 JS 可直接读取"""
        payload = json.dumps(data, ensure_ascii=False)
        payload = payload.replace('</', '<\\/')  # 防 </script> 注入
        return (f'<script id="{id}" type="application/json">{payload}</script>')


class AuroraProc:
    """进程桥:启动外部程序,多程序协同(数据经 stdin/stdout 交换)"""
    @staticmethod
    def run(cmd: str, stdin: str = "", timeout: float = 30.0) -> dict:
        """运行命令(字符串),返回 {code, out, err}"""
        try:
            p = subprocess.run(
                cmd, shell=True, input=stdin, capture_output=True,
                text=True, timeout=timeout)
            return {'code': p.returncode, 'out': p.stdout, 'err': p.stderr}
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"进程超时: {cmd}")
        except Exception as e:
            raise AuroraError("ProcError", str(e))

    @staticmethod
    def call(cmd: str, stdin: str = "", timeout: float = 30.0) -> str:
        """运行命令并返回标准输出"""
        r = AuroraProc.run(cmd, stdin, timeout)
        if r['code'] != 0:
            raise AuroraError("ProcError", r['err'] or f"退出码 {r['code']}")
        return r['out']

    @staticmethod
    def spawn(cmd: str) -> dict:
        """异步启动进程(不等待),返回 PID"""
        try:
            p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            return {'pid': p.pid}
        except Exception as e:
            raise AuroraError("ProcError", str(e))

    @staticmethod
    def run_args(args: list, stdin: str = "", timeout: float = 30.0) -> dict:
        """以参数列表运行命令(不经 shell,无引号转义问题)"""
        try:
            p = subprocess.run(
                list(args), input=stdin, capture_output=True,
                text=True, timeout=timeout)
            return {'code': p.returncode, 'out': p.stdout, 'err': p.stderr}
        except subprocess.TimeoutExpired:
            raise AuroraError("TimeoutError", f"进程超时: {args}")
        except Exception as e:
            raise AuroraError("ProcError", str(e))

    @staticmethod
    def call_args(args: list, stdin: str = "", timeout: float = 30.0) -> str:
        """参数列表运行并返回标准输出"""
        r = AuroraProc.run_args(list(args), stdin, timeout)
        if r['code'] != 0:
            raise AuroraError("ProcError", r['err'] or f"退出码 {r['code']}")
        return r['out']


class AuroraVex:
    """VEX 机器人桥:导出 VEXcode 工程源码(Python / C++)
    在 VEXcode 中新建同语言项目,把 main 文件粘贴即可编译部署"""

    @staticmethod
    def export(dir_path: str, name: str, code: str, lang: str = "python") -> dict:
        lang = lang.lower()
        if lang in ("python", "py"):
            fname = "main.py"
            header = (
                "# VEXcode Python 工程(由 Aurora 生成)\n"
                "# 在 VEXcode 新建 Python 项目后粘贴到 main.py\n"
                "# 依赖 VEX 库:from vex import *\n\n"
                "from vex import *\n"
                "brain = Brain()\n\n")
        elif lang in ("cpp", "c++"):
            fname = "main.cpp"
            header = (
                "// VEXcode C++ 工程(由 Aurora 生成)\n"
                "// 在 VEXcode 新建 C++ 项目后粘贴到 main.cpp\n\n"
                "#include \"vex.h\"\n"
                "using namespace vex;\n"
                "brain Brain;\n\n")
        else:
            raise AuroraError("VexError", f"不支持的语言 {lang},可用 python / cpp")
        d = os.path.join(dir_path, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(header + code)
        with open(os.path.join(d, "README.md"), 'w', encoding='utf-8') as f:
            f.write(
                f"# {name}\n\n由 Aurora `std.vex` 导出({lang} 工程)。\n"
                f"打开 VEXcode,新建 {lang} 项目,将 {fname} 内容粘贴到项目对应文件后编译。\n")
        return {'dir': d, 'file': fname}

    @staticmethod
    def python(dir_path: str, name: str, code: str) -> dict:
        return AuroraVex.export(dir_path, name, code, "python")

    @staticmethod
    def cpp(dir_path: str, name: str, code: str) -> dict:
        return AuroraVex.export(dir_path, name, code, "cpp")


class AuroraHttp:
    """HTTP 桥:请求 Web API,与外部服务/库互通"""
    _DEFAULT_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36")

    @staticmethod
    def get(url: str, timeout: float = 10.0, headers=None) -> str:
        try:
            import urllib.request
            hdrs = {'User-Agent': AuroraHttp._DEFAULT_UA}
            if headers:
                hdrs.update(headers)
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception as e:
            raise AuroraError("HttpError", str(e))

    @staticmethod
    def get_json(url: str, timeout: float = 10.0):
        """请求 JSON API,自动解析"""
        return json.loads(AuroraHttp.get(url, timeout))

    @staticmethod
    def post(url: str, data: str = "", content_type: str = "application/json",
             timeout: float = 10.0) -> str:
        try:
            import urllib.request
            body = data.encode('utf-8') if isinstance(data, str) else data
            req = urllib.request.Request(
                url, data=body, headers={'Content-Type': content_type})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception as e:
            raise AuroraError("HttpError", str(e))


class AuroraWeb:
    """Web 后端:让 Aurora 程序直接提供 HTTP 服务(路由 / JSON API / HTML 页面)

    handler(path, method, query, body) 返回值约定:
      - dict            → 200 + JSON
      - str             → 200 + text/html
      - [status, body]  → 指定状态码 + 文本
      - [status, headers_dict, body] → 完整控制
    """

    @staticmethod
    def serve(port: int, handler, host: str = "127.0.0.1") -> dict:
        """启动 HTTP 服务(后台线程),返回 {host, port, url}
        port = 0 时自动分配空闲端口。
        脚本若要常驻服务,末尾调用 std.web.wait()。"""
        try:
            class _Handler(BaseHTTPRequestHandler):
                def _dispatch(self):
                    length = int(self.headers.get('Content-Length') or 0)
                    body = (self.rfile.read(length).decode('utf-8', 'replace')
                            if length else '')
                    parsed = urllib.parse.urlparse(self.path)
                    query = dict(urllib.parse.parse_qsl(parsed.query))
                    path = parsed.path
                    try:
                        result = handler(path, self.command, query, body)
                        AuroraWeb._respond(self, result)
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-Type', 'text/plain; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(("ServerError: " + str(e)).encode('utf-8'))

                def do_GET(self): self._dispatch()
                def do_POST(self): self._dispatch()
                def do_PUT(self): self._dispatch()
                def do_DELETE(self): self._dispatch()
                def do_OPTIONS(self): self._dispatch()
                def log_message(self, *a): pass  # 安静日志

            server = ThreadingHTTPServer((host, port), _Handler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            actual = server.server_address[1]
            return {'host': host, 'port': actual, 'url': f'http://{host}:{actual}/'}
        except Exception as e:
            raise AuroraError("WebError", f"启动服务失败: {e}")

    _wait_event = threading.Event()

    @staticmethod
    def wait():
        """阻塞当前线程,保持服务运行(直到 Ctrl-C)"""
        AuroraWeb._wait_event.wait()

    @staticmethod
    def _respond(handler: BaseHTTPRequestHandler, result):
        """把 handler 返回值规范化为 HTTP 响应"""
        status, headers, body = 200, {'Content-Type': 'text/html; charset=utf-8'}, ''
        if isinstance(result, dict):
            status, headers, body = 200, {'Content-Type': 'application/json; charset=utf-8'}, json.dumps(result, ensure_ascii=False)
        elif isinstance(result, (list, tuple)):
            if len(result) == 2:
                status, body = int(result[0]), str(result[1])
            elif len(result) >= 3:
                status, headers, body = int(result[0]), dict(result[1]), str(result[2])
        else:
            body = str(result)
        handler.send_response(status)
        for k, v in headers.items():
            handler.send_header(k, v)
        handler.end_headers()
        handler.wfile.write(body.encode('utf-8'))

    @staticmethod
    def static(port: int, directory: str, host: str = "127.0.0.1") -> dict:
        """静态文件服务:GET /path → directory/path"""
        def handler(path, method, query, body):
            if path == '/':
                path = '/index.html'
            file_path = os.path.join(directory, path.lstrip('/'))
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return [200, {'Content-Type': 'text/html; charset=utf-8'}, f.read()]
            return [404, 'not found']
        return AuroraWeb.serve(port, handler, host)


class AuroraAI:
    """AI Agent:调用大模型 API(OpenAI 兼容),支持对话与工具调用式 Agent

    配置优先级:configure() > 环境变量(AURORA_AI_BASE_URL / AURORA_AI_API_KEY / AURORA_AI_MODEL)
    默认 base_url 为火山方舟(豆包)OpenAI 兼容端点;也可指向任何兼容服务或本地模型。
    """

    _base_url = (os.environ.get('AURORA_AI_BASE_URL')
                 or 'https://ark.cn-beijing.volces.com/api/v3')
    _api_key = (os.environ.get('AURORA_AI_API_KEY')
                or os.environ.get('DOUBAO_API_KEY')
                or os.environ.get('OPENAI_API_KEY') or '')
    _model = os.environ.get('AURORA_AI_MODEL') or 'doubao-seed-1-6-250615'

    @staticmethod
    def configure(base_url: str = None, api_key: str = None, model: str = None) -> dict:
        """设置 AI 服务配置(可只传部分)"""
        if base_url is not None:
            AuroraAI._base_url = base_url.rstrip('/')
        if api_key is not None:
            AuroraAI._api_key = api_key
        if model is not None:
            AuroraAI._model = model
        return {'base_url': AuroraAI._base_url, 'model': AuroraAI._model,
                'has_key': bool(AuroraAI._api_key)}

    @staticmethod
    def chat(prompt: str, system: str = None, model: str = None,
             temperature: float = 0.7) -> str:
        """单轮对话,返回回复文本"""
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        resp = AuroraAI._complete(messages, model=model, temperature=temperature)
        return resp['content']

    @staticmethod
    def messages(msgs: list, model: str = None) -> str:
        """多轮对话:msgs 形如 [{'role': 'user', 'content': '...'}, ...]"""
        resp = AuroraAI._complete(list(msgs), model=model)
        return resp['content']

    @staticmethod
    def agent(system: str, tools: dict, prompt: str,
              max_steps: int = 8, model: str = None,
              temperature: float = 0.3) -> dict:
        """工具调用式 Agent:
        tools = {'名称': {'fn': 可调用, 'desc': '给模型看的描述', 'params': 可选参数schema}}

        Agent 循环:模型决策 → 调用 Aurora 函数 → 结果回填 → 直到模型给出最终回复。
        返回 {'answer', 'steps', 'tool_calls': [{'name', 'args', 'result'}]}
        """
        if not AuroraAI._api_key:
            raise AuroraError(
                "AIError",
                "未配置 API Key。请设置环境变量 AURORA_AI_API_KEY / DOUBAO_API_KEY / "
                "OPENAI_API_KEY,或调用 std.ai.configure(api_key: \"...\")")
        if not tools:
            return AuroraAI._run_plain(system, prompt, model, temperature)

        tool_specs = []
        for name, spec in tools.items():
            if callable(spec):
                desc, params = getattr(spec, '__doc__', '') or '', {"type": "object"}
            elif isinstance(spec, dict):
                fn = spec.get('fn', spec)
                desc = spec.get('desc') or (getattr(fn, '__doc__', '') or '')
                params = spec.get('params') or {"type": "object"}
            else:
                fn, desc, params = spec, '', {"type": "object"}
            tool_specs.append({
                'type': 'function',
                'function': {'name': name, 'description': desc,
                             'parameters': params},
            })

        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})

        calls = []
        for step in range(1, max_steps + 1):
            data = {
                'model': model or AuroraAI._model,
                'messages': messages,
                'tools': tool_specs,
                'temperature': temperature,
            }
            raw = AuroraAI._post('/chat/completions', data)
            choice = raw['choices'][0]['message']
            msg_content = choice.get('content') or ''
            tool_calls = choice.get('tool_calls') or []

            if not tool_calls:
                return {'answer': msg_content, 'steps': step, 'tool_calls': calls}

            # 执行工具调用并回填
            messages.append(choice)
            for tc in tool_calls:
                name = tc['function']['name']
                try:
                    args = json.loads(tc['function'].get('arguments') or '{}')
                except Exception:
                    args = {}
                fn = tools.get(name)
                if isinstance(fn, dict):
                    fn = fn.get('fn', fn)
                try:
                    result = fn(**args) if isinstance(args, dict) else fn(args)
                except Exception as e:
                    result = f"工具错误: {e}"
                calls.append({'name': name, 'args': args, 'result': result})
                messages.append({
                    'role': 'tool', 'tool_call_id': tc.get('id', f'tc{step}'),
                    'content': json.dumps(result, ensure_ascii=False),
                })

        return {'answer': '(达到最大步数,未收敛)', 'steps': max_steps, 'tool_calls': calls}

    @staticmethod
    def _run_plain(system, prompt, model, temperature):
        try:
            answer = AuroraAI.chat(prompt, system, model, temperature)
            return {'answer': answer, 'steps': 1, 'tool_calls': []}
        except Exception as e:
            raise AuroraError("AIError", str(e))

    @staticmethod
    def _complete(messages, model=None, temperature=0.7) -> dict:
        data = {'model': model or AuroraAI._model,
                'messages': messages, 'temperature': temperature}
        raw = AuroraAI._post('/chat/completions', data)
        choice = raw['choices'][0]['message']
        content = choice.get('content') or ''
        return {'content': content, 'raw': raw}

    @staticmethod
    def _post(path: str, data: dict) -> dict:
        if not AuroraAI._api_key:
            raise AuroraError(
                "AIError",
                "未配置 API Key。请设置环境变量 AURORA_AI_API_KEY / DOUBAO_API_KEY / "
                "OPENAI_API_KEY,或调用 std.ai.configure(api_key: \"...\")")
        url = AuroraAI._base_url + path
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + AuroraAI._api_key})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', 'replace')[:300]
            raise AuroraError("AIError", f"HTTP {e.code}: {detail}")
        except Exception as e:
            raise AuroraError("AIError", str(e))


class HashMap:
    """哈希映射(基于 Python dict)"""
    def __init__(self, data=None):
        self._data = dict(data) if data else {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        return value

    def has(self, key) -> bool:
        return key in self._data

    def remove(self, key):
        if key in self._data:
            v = self._data.pop(key)
            return v
        return None

    def keys(self):
        return list(self._data.keys())

    def values(self):
        return list(self._data.values())

    def items(self):
        return [[k, v] for k, v in self._data.items()]

    def len(self) -> int:
        return len(self._data)

    def clear(self):
        self._data.clear()

    def to_dict(self):
        return dict(self._data)

    def __repr__(self):
        return f"HashMap({self._data})"


class HashSet:
    """哈希集合(基于 Python set)"""
    def __init__(self, data=None):
        self._data = set(data) if data else set()

    def add(self, value):
        self._data.add(value)
        return value

    def has(self, value) -> bool:
        return value in self._data

    def remove(self, value) -> bool:
        if value in self._data:
            self._data.remove(value)
            return True
        return False

    def len(self) -> int:
        return len(self._data)

    def clear(self):
        self._data.clear()

    def to_list(self):
        return list(self._data)

    def union(self, other):
        return HashSet(self._data | other._data)

    def intersect(self, other):
        return HashSet(self._data & other._data)

    def __repr__(self):
        return f"HashSet({list(self._data)})"


class Vec:
    """动态数组(基于 Python list)"""
    def __init__(self, data=None):
        self._data = list(data) if data else []

    def push(self, value):
        self._data.append(value)
        return value

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def get(self, index):
        return self._data[index]

    def set(self, index, value):
        self._data[index] = value
        return value

    def len(self) -> int:
        return len(self._data)

    def insert(self, index, value):
        self._data.insert(index, value)

    def remove(self, index):
        return self._data.pop(index)

    def slice(self, start, end=None):
        return Vec(self._data[start:end])

    def clear(self):
        self._data.clear()

    def to_list(self):
        return list(self._data)

    def sort(self, key=None):
        self._data.sort(key=key)

    def reverse(self):
        self._data.reverse()

    def contains(self, value) -> bool:
        return value in self._data

    def index_of(self, value):
        try:
            return self._data.index(value)
        except ValueError:
            return -1

    def __repr__(self):
        return f"Vec({self._data})"


class AuroraCollections:
    """集合类型:HashMap / HashSet / Vec"""
    @staticmethod
    def hash_map(data=None):
        return HashMap(data)

    @staticmethod
    def hash_set(data=None):
        return HashSet(data)

    @staticmethod
    def vec(data=None):
        return Vec(data)


# ── 标准库注册表 ────────────────────────────────────────

# v3.0.0 AI 引擎模块注册表。仅当 ai/ 成功导入时填充真实对象；
# 否则退化为空字典，保证其他 std.* 模块与解释器功能完全不受影响。
if _AURORA_AI_AVAILABLE:
    _AI_EXTRA_MODULES = {
        'std.tensor': {
            'Tensor': _AuroraTensor,
            'zeros': _AuroraTensor.zeros,
            'ones': _AuroraTensor.ones,
            'randn': _AuroraTensor.randn,
            'eye': _AuroraTensor.eye,
            'arange': _AuroraTensor.arange,
            'from_numpy': _AuroraTensor.from_numpy,
        },
        'std.autograd': {
            'Variable': _AuroraVariable,
            'SGD': _AuroraSGD,
            'Adam': _AuroraAdam,
        },
        'std.nn': {
            'Linear': _aurora_nn.Linear,
            'ReLU': _aurora_nn.ReLU,
            'Sigmoid': _aurora_nn.Sigmoid,
            'Tanh': _aurora_nn.Tanh,
            'Softmax': _aurora_nn.Softmax,
            'LeakyReLU': _aurora_nn.LeakyReLU,
            'Conv2d': _aurora_nn.Conv2d,
            'LSTM': _aurora_nn.LSTM,
            'Dropout': _aurora_nn.Dropout,
            'Flatten': _aurora_nn.Flatten,
            'BatchNorm1d': _aurora_nn.BatchNorm1d,
            'Sequential': _aurora_nn.Sequential,
            'MSELoss': _aurora_nn.MSELoss,
            'CrossEntropyLoss': _aurora_nn.CrossEntropyLoss,
            'BCELoss': _aurora_nn.BCELoss,
            'one_hot': _aurora_nn.one_hot,
        },
        'std.data': {
            'DataFrame': _AuroraDataFrame,
            'Dataset': _AuroraDataset,
            'DataLoader': _AuroraDataLoader,
            'read_csv': _AuroraDataFrame.read_csv,
        },
        'std.agent': {
            'Agent': _AuroraAgent,
            'LLM': _AuroraLLM,
            'PromptTemplate': _AuroraPromptTemplate,
            'LLMChain': _AuroraLLMChain,
        },
        'std.inference': {
            'InferenceEngine': _AuroraInferenceEngine,
            'InferenceServer': _AuroraInferenceServer,
        },
    }
else:
    # AI 引擎不可用：登记同名空模块，`import std.tensor` 不报错但成员为空。
    _AI_EXTRA_MODULES = {
        'std.tensor': {}, 'std.autograd': {}, 'std.nn': {},
        'std.data': {}, 'std.agent': {}, 'std.inference': {},
    }

STDLIB_MODULES = {
    'std.io': {
        'read_file': AuroraIO.read_file,
        'write_file': AuroraIO.write_file,
        'append_file': AuroraIO.append_file,
        'exists': AuroraIO.exists,
        'read_line': AuroraIO.read_line,
        'list_dir': AuroraIO.list_dir,
        'mkdir': AuroraIO.mkdir,
        'is_dir': AuroraIO.is_dir,
        'files': AuroraIO.files,
    },
    'std.math': {
        'PI': AuroraMath.PI,
        'E': AuroraMath.E,
        'abs': AuroraMath.abs,
        'sqrt': AuroraMath.sqrt,
        'pow': AuroraMath.pow,
        'floor': AuroraMath.floor,
        'ceil': AuroraMath.ceil,
        'round': AuroraMath.round,
        'min': AuroraMath.min,
        'max': AuroraMath.max,
        'sin': AuroraMath.sin,
        'cos': AuroraMath.cos,
        'tan': AuroraMath.tan,
        'log': AuroraMath.log,
        'random': AuroraMath.random,
        'randint': AuroraMath.randint,
    },
    'std.str': {
        'split': AuroraString.split,
        'join': AuroraString.join,
        'replace': AuroraString.replace,
        'contains': AuroraString.contains,
        'starts_with': AuroraString.starts_with,
        'ends_with': AuroraString.ends_with,
        'trim': AuroraString.trim,
        'upper': AuroraString.upper,
        'lower': AuroraString.lower,
        'format': AuroraString.format,
    },
    'std.time': {
        'now': AuroraTime.now,
        'sleep': AuroraTime.sleep,
        'timestamp': AuroraTime.timestamp,
        'format': AuroraTime.format_time,
    },
    'std.json': {
        'parse': AuroraJson.parse,
        'stringify': AuroraJson.stringify,
        'load': AuroraJson.load,
        'save': AuroraJson.save,
    },
    'std.python': {
        'eval': AuroraPython.eval,
        'exec': AuroraPython.exec,
        'import': AuroraPython.import_module,
        'call': AuroraPython.call,
        'version': AuroraPython.version,
    },
    'std.ffi': {
        'load': AuroraFFI.load,
        'func': AuroraFFI.func,
        'cstr': AuroraFFI.cstr,
        'struct': AuroraFFI.struct,
        'callback': AuroraFFI.callback,
        'string_array': AuroraFFI.string_array,
        'ptr': AuroraFFI.ptr,
        'deref': AuroraFFI.deref,
        'gen_bindings': AuroraFFI.gen_bindings,
    },
    'std.js': {
        'eval': AuroraJS.eval,
        'call': AuroraJS.call,
        'require': AuroraJS.require,
        'run_file': AuroraJS.run_file,
        'version': AuroraJS.version,
        'available': AuroraJS.available,
    },
    'std.java': {
        'call': AuroraJava.call,
        'run': AuroraJava.run,
        'eval': AuroraJava.eval,
        'compile': AuroraJava.compile,
        'version': AuroraJava.version,
        'available': AuroraJava.available,
    },
    'std.interop': {
        'call': AuroraInterop.call,
        'import': AuroraInterop._import,
        'eval': AuroraInterop.eval,
        'languages': AuroraInterop.languages,
        'status': AuroraInterop.status,
    },
    'std.wasm': {
        'load': AuroraWASM.load,
        'call': AuroraWASM.call,
        'exports': AuroraWASM.exports,
        'available': AuroraWASM.available,
    },
    'std.html': {
        'escape': AuroraHtml.escape,
        'render': AuroraHtml.render,
        'page': AuroraHtml.page,
        'write': AuroraHtml.write,
        'open': AuroraHtml.open,
        'link': AuroraHtml.link,
        'list': AuroraHtml.list,
        'json_script': AuroraHtml.json_script,
    },
    'std.web': {
        'serve': AuroraWeb.serve,
        'static': AuroraWeb.static,
        'wait': AuroraWeb.wait,
    },
    'std.ai': {
        # 原有 LLM 对话能力（向后兼容，保持不变）
        'configure': AuroraAI.configure,
        'chat': AuroraAI.chat,
        'messages': AuroraAI.messages,
        'agent': AuroraAI.agent,
        # v3.0.0 新增：AI 引擎高级能力（AI 不可用时为 None 占位）
        'ai_decorator': (_AuroraAIDecorator if _AURORA_AI_AVAILABLE else None),
        'Agent': (_AuroraAgent if _AURORA_AI_AVAILABLE else None),
        'LLM': (_AuroraLLM if _AURORA_AI_AVAILABLE else None),
        'PromptTemplate': (_AuroraPromptTemplate if _AURORA_AI_AVAILABLE else None),
        'LLMChain': (_AuroraLLMChain if _AURORA_AI_AVAILABLE else None),
        'InferenceEngine': (_AuroraInferenceEngine if _AURORA_AI_AVAILABLE else None),
        'InferenceServer': (_AuroraInferenceServer if _AURORA_AI_AVAILABLE else None),
    },
    # v3.0.0 AI 引擎细分模块（张量 / 自动微分 / 神经网络 / 数据 / Agent / 推理）
    **_AI_EXTRA_MODULES,
    'std.collections': {
        'HashMap': HashMap,
        'HashSet': HashSet,
        'Vec': Vec,
        'hash_map': AuroraCollections.hash_map,
        'hash_set': AuroraCollections.hash_set,
        'vec': AuroraCollections.vec,
    },
    'std.proc': {
        'run': AuroraProc.run,
        'call': AuroraProc.call,
        'spawn': AuroraProc.spawn,
        'run_args': AuroraProc.run_args,
        'call_args': AuroraProc.call_args,
    },
    'std.http': {
        'get': AuroraHttp.get,
        'get_json': AuroraHttp.get_json,
        'post': AuroraHttp.post,
    },
    'std.vex': {
        'export': AuroraVex.export,
        'python': AuroraVex.python,
        'cpp': AuroraVex.cpp,
    },
    'std.sync': {
        'Channel': AuroraChannel,
        'Mutex': AuroraMutex,
        'Fiber': AuroraFiber,
    },
    'std.result': {
        'Ok': AuroraResult.Ok,
        'Err': AuroraResult.Err,
        'Result': AuroraResult,
    },
}

# 全局内建函数
def _aurora_display(x):
    """把 Aurora 值转成可读文本：nil 显示为 nil，其余保持自然表示"""
    if x is None:
        return 'nil'
    return x


# ═══════════════════════════════════════════════════════════════
#  效率快捷函数 — Python 十步, Aurora 三-四步
# ═══════════════════════════════════════════════════════════════

def _read_file(path):
    """一行读取文件全部内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def _write_file(path, content):
    """一行写入文件"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(content))
    return True

def _append_file(path, content):
    """一行追加写入文件"""
    with open(path, 'a', encoding='utf-8') as f:
        f.write(str(content))
    return True

def _read_lines(path):
    """读取文件为行列表(去换行符)"""
    with open(path, 'r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f]

def _shell(cmd):
    """执行 shell 命令,返回输出文本"""
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def _http_get(url):
    """一行 HTTP GET,返回响应文本"""
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'Aurora/1.4'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')

def _http_download(url, path):
    """一行下载文件到指定路径"""
    import urllib.request
    urllib.request.urlretrieve(url, path)
    return path

def _json_parse(s):
    """一行解析 JSON 字符串"""
    import json
    return json.loads(s)

def _json_stringify(obj, indent=2):
    """一行对象转 JSON 字符串"""
    import json
    return json.dumps(obj, ensure_ascii=False, indent=indent)

def _unique(lst):
    """列表去重,保持顺序"""
    seen = set()
    result = []
    for item in lst:
        key = str(item) if not isinstance(item, (int, float, str, bool)) else item
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

def _flatten(lst):
    """扁平化嵌套列表"""
    result = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            result.extend(_flatten(item))
        else:
            result.append(item)
    return result

def _chunk(lst, n):
    """列表分块"""
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def _avg(lst):
    """平均值"""
    return sum(lst) / len(lst) if lst else 0

def _median(lst):
    """中位数"""
    if not lst:
        return 0
    s = sorted(lst)
    n = len(s)
    return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2

def _clamp(n, lo, hi):
    """限制数值范围"""
    return max(lo, min(hi, n))

def _find(fn, lst):
    """查找第一个满足条件的元素"""
    for item in lst:
        if fn(item):
            return item
    return None

def _find_index(fn, lst):
    """查找第一个满足条件的索引"""
    for i, item in enumerate(lst):
        if fn(item):
            return i
    return -1

def _count(fn, lst):
    """计数满足条件的元素"""
    return sum(1 for item in lst if fn(item))

def _partition(fn, lst):
    """分区为(满足, 不满足)两个列表"""
    yes, no = [], []
    for item in lst:
        (yes if fn(item) else no).append(item)
    return yes, no

def _pluck(lst, key):
    """从字典列表中提取指定字段"""
    return [item.get(key) if isinstance(item, dict) else getattr(item, key, None) for item in lst]

def _group_by(lst, key_fn):
    """按键函数分组"""
    groups = {}
    for item in lst:
        k = key_fn(item)
        if k not in groups:
            groups[k] = []
        groups[k].append(item)
    return groups

def _starts_with(s, prefix):
    return str(s).startswith(str(prefix))

def _ends_with(s, suffix):
    return str(s).endswith(str(suffix))

def _contains_str(s, sub):
    return str(sub) in str(s)

def _env(name, default=None):
    import os
    return os.environ.get(name, default)

def _now():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def _timestamp():
    import time
    return int(time.time())

def _cwd():
    import os
    return os.getcwd()

def _cd(path):
    import os
    os.chdir(path)
    return path

def _exists(path):
    import os
    return os.path.exists(path)

def _delete(path):
    import os
    if os.path.isdir(path):
        import shutil
        shutil.rmtree(path)
    else:
        os.remove(path)
    return True

def _mkdir(path):
    import os
    os.makedirs(path, exist_ok=True)
    return path

def _list_dir(path='.'):
    import os
    return sorted(os.listdir(path))

def _reduce(fn, lst, init=None):
    from functools import reduce as _rd
    return _rd(fn, lst, init) if init is not None else _rd(fn, lst)

def _any(lst):
    return any(lst)

def _all(lst):
    return all(lst)

def _product(lst):
    result = 1
    for x in lst:
        result *= x
    return result

def _keys(d):
    return list(d.keys()) if isinstance(d, dict) else []

def _values(d):
    return list(d.values()) if isinstance(d, dict) else []

def _items(d):
    return list(d.items()) if isinstance(d, dict) else []

def _dict_from(pairs):
    return dict(pairs)

def _join(lst, sep=''):
    return sep.join(str(x) for x in lst)

def _contains(lst, item):
    return item in lst

def _typeof(x):
    return type(x).__name__

def _repr(x):
    return repr(x)

def _floor(n):
    import math
    return math.floor(n)

def _ceil(n):
    import math
    return math.ceil(n)

def _round(n, ndigits=0):
    return round(n, ndigits)

def _abs(n):
    return abs(n)

def _exit(code=0):
    import sys
    sys.exit(code)

def _args():
    import sys
    return sys.argv[1:]

def _basename(path):
    import os
    return os.path.basename(path)

def _dirname(path):
    import os
    return os.path.dirname(path)

def _extname(path):
    import os
    return os.path.splitext(path)[1]

def _splitext(path):
    import os
    return list(os.path.splitext(path))

def _tempfile(content='', suffix=''):
    import tempfile
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path

def _tempdir():
    import tempfile
    return tempfile.mkdtemp()

def _copy(src, dst):
    import shutil
    shutil.copy2(src, dst)
    return dst

def _move(src, dst):
    import shutil
    shutil.move(src, dst)
    return dst

def _walk(path):
    import os
    result = []
    for root, dirs, files in os.walk(path):
        for f in files:
            result.append(os.path.join(root, f))
    return sorted(result)

def _grep(pattern, path):
    """在文件中搜索模式,返回匹配行列表"""
    import re
    matches = []
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            if re.search(pattern, line):
                matches.append({'line': i, 'text': line.rstrip('\n')})
    return matches

def _replace_in_file(path, old, new):
    """在文件中替换文本"""
    content = _read_file(path)
    content = content.replace(old, new)
    _write_file(path, content)
    return True

def _md5(text):
    import hashlib
    return hashlib.md5(str(text).encode()).hexdigest()

def _sha256(text):
    import hashlib
    return hashlib.sha256(str(text).encode()).hexdigest()

def _base64_encode(text):
    import base64
    return base64.b64encode(str(text).encode()).decode()

def _base64_decode(text):
    import base64
    return base64.b64decode(str(text).encode()).decode()

def _url_encode(text):
    import urllib.parse
    return urllib.parse.quote(str(text))

def _url_decode(text):
    import urllib.parse
    return urllib.parse.unquote(str(text))

def _parse_url(url):
    import urllib.parse
    p = urllib.parse.urlparse(url)
    return {
        'scheme': p.scheme, 'host': p.netloc, 'path': p.path,
        'query': p.query, 'fragment': p.fragment,
        'params': dict(urllib.parse.parse_qsl(p.query)),
    }

def _csv_parse(text, delimiter=','):
    import csv, io
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    return [row for row in reader]

def _csv_stringify(rows, delimiter=','):
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output, delimiter=delimiter)
    for row in rows:
        writer.writerow(row)
    return output.getvalue()

def _xml_parse(text):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(text)
    def _elem_to_dict(elem):
        d = {'tag': elem.tag, 'attrib': dict(elem.attrib), 'text': (elem.text or '').strip()}
        children = [_elem_to_dict(c) for c in elem]
        if children:
            d['children'] = children
        return d
    return _elem_to_dict(root)

def _regex_match(pattern, text):
    import re
    m = re.match(pattern, str(text))
    return m.groups() if m else None

def _regex_search(pattern, text):
    import re
    m = re.search(pattern, str(text))
    return m.group() if m else None

def _regex_findall(pattern, text):
    import re
    return re.findall(pattern, str(text))

def _regex_sub(pattern, repl, text):
    import re
    return re.sub(pattern, repl, str(text))

def _regex_split(pattern, text):
    import re
    return re.split(pattern, str(text))

def _datetime_format(fmt=None):
    import datetime
    now = datetime.datetime.now()
    return now.strftime(fmt) if fmt else now.isoformat()

def _datetime_parse(text, fmt):
    import datetime
    return datetime.datetime.strptime(text, fmt).isoformat()

def _sleep(seconds):
    import time
    time.sleep(seconds)

def _benchmark(fn, *args, **kwargs):
    """简单性能测试,返回(结果, 耗时秒)"""
    import time
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

def _memoize(fn):
    """简单记忆化装饰器"""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper

def _compose(*fns):
    """函数组合: compose(f, g)(x) = f(g(x))"""
    def composed(x):
        result = x
        for fn in reversed(fns):
            result = fn(result)
        return result
    return composed

def _pipe(value, *fns):
    """管道:将值依次通过多个函数"""
    result = value
    for fn in fns:
        result = fn(result)
    return result

def _tap(value, fn):
    """执行副作用并返回原值(用于调试)"""
    fn(value)
    return value

def _clone(obj):
    """深拷贝"""
    import copy
    return copy.deepcopy(obj)

def _merge(d1, d2):
    """合并两个字典,d2 覆盖 d1"""
    result = dict(d1) if isinstance(d1, dict) else {}
    if isinstance(d2, dict):
        result.update(d2)
    return result

def _pick(d, keys):
    """从字典中选取指定键"""
    return {k: d[k] for k in keys if k in d} if isinstance(d, dict) else {}

def _omit(d, keys):
    """从字典中排除指定键"""
    return {k: v for k, v in d.items() if k not in keys} if isinstance(d, dict) else {}

def _range_step(start, stop=None, step=1):
    if stop is None:
        return list(range(start))
    return list(range(start, stop, step))

def _zip_with(fn, *lists):
    """带函数的 zip"""
    return [fn(*items) for items in zip(*lists)]

def _interleave(*lists):
    """交错合并多个列表"""
    result = []
    max_len = max(len(l) for l in lists) if lists else 0
    for i in range(max_len):
        for l in lists:
            if i < len(l):
                result.append(l[i])
    return result

def _rotate(lst, n=1):
    """列表旋转"""
    if not lst:
        return lst
    n = n % len(lst)
    return lst[n:] + lst[:n]

def _sliding_window(lst, size):
    """滑动窗口"""
    return [lst[i:i+size] for i in range(len(lst) - size + 1)]

def _degrees_to_radians(deg):
    import math
    return deg * math.pi / 180

def _radians_to_degrees(rad):
    import math
    return rad * 180 / math.pi

def _is_even(n):
    return n % 2 == 0

def _is_odd(n):
    return n % 2 != 0

def _is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def _fibonacci(n):
    """生成前 n 个斐波那契数"""
    result = [0, 1]
    while len(result) < n:
        result.append(result[-1] + result[-2])
    return result[:n]

def _factorial(n):
    if n < 0:
        raise ValueError("factorial of negative number")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def _gcd(a, b):
    import math
    return math.gcd(a, b)

def _lcm(a, b):
    import math
    return abs(a * b) // math.gcd(a, b) if a and b else 0

def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))

def _levenshtein(s1, s2):
    """编辑距离"""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def _similarity(s1, s2):
    """字符串相似度 0-1"""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    return 1.0 - _levenshtein(s1, s2) / max_len

def _slugify(text):
    """URL 友好的 slug"""
    import re
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def _truncate(text, length, suffix='...'):
    text = str(text)
    return text[:length] + suffix if len(text) > length else text

def _pad_start(text, length, char=' '):
    return str(text).rjust(length, char)

def _pad_end(text, length, char=' '):
    return str(text).ljust(length, char)

def _repeat(text, n):
    return str(text) * n

def _reverse_str(text):
    return str(text)[::-1]

def _title_case(text):
    return str(text).title()

def _camel_case(text):
    import re
    words = re.sub(r'[^a-zA-Z0-9]', ' ', str(text)).split()
    if not words:
        return ''
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:])

def _snake_case(text):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str(text))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def _kebab_case(text):
    return _snake_case(text).replace('_', '-')

def _words(text):
    import re
    return re.findall(r'\b\w+\b', str(text))

def _word_count(text):
    return len(_words(text))

def _line_count(text):
    return str(text).count('\n') + 1

def _char_count(text):
    return len(str(text))

def _byte_size(text):
    return len(str(text).encode('utf-8'))

def _is_email(text):
    import re
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(text)))

def _is_url(text):
    import re
    return bool(re.match(r'^https?://[^\s]+$', str(text)))

def _is_ip(text):
    import re
    return bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', str(text)))

def _is_json(text):
    try:
        import json
        json.loads(str(text))
        return True
    except:
        return False

def _is_number(text):
    try:
        float(str(text))
        return True
    except:
        return False

def _is_int(text):
    try:
        int(str(text))
        return True
    except:
        return False

def _random(min_val=0, max_val=1):
    import random
    return random.uniform(min_val, max_val)

def _random_int(min_val, max_val):
    import random
    return random.randint(min_val, max_val)

def _random_choice(lst):
    import random
    return random.choice(lst)

def _shuffle(lst):
    import random
    result = list(lst)
    random.shuffle(result)
    return result

def _sample(lst, n):
    import random
    return random.sample(list(lst), min(n, len(lst)))

def _uuid():
    import uuid
    return str(uuid.uuid4())

def _nanoid(length=21):
    import random, string
    alphabet = string.ascii_letters + string.digits + '_-'
    return ''.join(random.choice(alphabet) for _ in range(length))

def _color_console(text, color='white'):
    """ANSI 颜色输出"""
    colors = {
        'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
        'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
        'bright_red': '91', 'bright_green': '92', 'bright_yellow': '93',
        'bright_blue': '94', 'bright_magenta': '95', 'bright_cyan': '96',
        'bright_white': '97',
    }
    code = colors.get(color, '37')
    return f'\033[{code}m{text}\033[0m'

def _table(rows, headers=None):
    """简单文本表格"""
    if not rows:
        return ''
    if headers:
        all_rows = [headers] + list(rows)
    else:
        all_rows = list(rows)
    cols = len(all_rows[0])
    widths = [max(len(str(row[i])) for row in all_rows) for i in range(cols)]
    lines = []
    for idx, row in enumerate(all_rows):
        line = ' | '.join(str(row[i]).ljust(widths[i]) for i in range(cols))
        lines.append(line)
        if idx == 0 and headers:
            lines.append('-+-'.join('-' * w for w in widths))
    return '\n'.join(lines)

def _progress(current, total, width=30):
    """文本进度条"""
    pct = current / total if total else 0
    filled = int(width * pct)
    bar = '█' * filled + '░' * (width - filled)
    return f'{bar} {pct*100:.1f}% ({current}/{total})'

def _spinner_frame(n):
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    return frames[n % len(frames)]

BUILTIN_GLOBALS = {
    'print': lambda *args, **kwargs: print(*map(_aurora_display, args), **kwargs),
    'println': lambda *args: print(*map(_aurora_display, args)),
    'len': lambda x: len(x),
    'range': lambda *args: list(range(*args)),
    'str': lambda x: str(x),
    'int': lambda x: int(x),
    'float': lambda x: float(x),
    'bool': lambda x: bool(x),
    'type': lambda x: type(x).__name__,
    'assert': lambda cond, msg="": (_ for _ in ()).throw(AuroraError("AssertError", msg or "assertion failed")) if not cond else None,
    'panic': lambda msg="": (_ for _ in ()).throw(AuroraError("Panic", msg)),
    'chan': lambda cap=0: AuroraChannel(cap),
    'sleep': lambda ms: time.sleep(ms / 1000.0),
    'spawn': lambda fn, *args: AuroraFiber(fn, args).start(),
    'input': lambda prompt="": input(prompt),
    'read_line': lambda prompt="": input(prompt),
    'read_int': lambda prompt="": int(input(prompt)),
    'read_float': lambda prompt="": float(input(prompt)),
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'sorted': sorted,
    'reversed': lambda x: list(reversed(x)),
    'enumerate': lambda x: list(enumerate(x)),
    'zip': lambda *xs: list(zip(*xs)),
    'map': lambda fn, xs: list(map(fn, xs)),
    'filter': lambda fn, xs: list(filter(fn, xs)),
    'isinstance': isinstance,
    # ── 文件操作(一行完成) ──
    'read': _read_file,
    'write': _write_file,
    'append': _append_file,
    'lines': _read_lines,
    'exists': _exists,
    'delete': _delete,
    'mkdir': _mkdir,
    'ls': _list_dir,
    'walk': _walk,
    'copy': _copy,
    'move': _move,
    'basename': _basename,
    'dirname': _dirname,
    'extname': _extname,
    'splitext': _splitext,
    'grep': _grep,
    'replace_in_file': _replace_in_file,
    # ── HTTP / 网络(一行完成) ──
    'get': _http_get,
    'download': _http_download,
    # ── JSON(一行完成) ──
    'json': _json_parse,
    'to_json': _json_stringify,
    # ── Shell / 进程(一行完成) ──
    'shell': _shell,
    # ── 列表操作 ──
    'unique': _unique,
    'flatten': _flatten,
    'chunk': _chunk,
    'group_by': _group_by,
    'pluck': _pluck,
    'join': _join,
    'contains': _contains,
    'find': _find,
    'find_index': _find_index,
    'count': _count,
    'partition': _partition,
    'rotate': _rotate,
    'sliding_window': _sliding_window,
    'interleave': _interleave,
    'zip_with': _zip_with,
    # ── 字符串操作 ──
    'split': lambda s, sep=' ': str(s).split(sep),
    'replace': lambda s, old, new: str(s).replace(old, new),
    'strip': lambda s: str(s).strip(),
    'upper': lambda s: str(s).upper(),
    'lower': lambda s: str(s).lower(),
    'starts_with': _starts_with,
    'ends_with': _ends_with,
    'contains_str': _contains_str,
    'reverse_str': _reverse_str,
    'title_case': _title_case,
    'camel_case': _camel_case,
    'snake_case': _snake_case,
    'kebab_case': _kebab_case,
    'slugify': _slugify,
    'truncate': _truncate,
    'pad_start': _pad_start,
    'pad_end': _pad_end,
    'repeat': _repeat,
    'words': _words,
    'word_count': _word_count,
    'line_count': _line_count,
    'char_count': _char_count,
    'byte_size': _byte_size,
    # ── 系统 / 环境 ──
    'env': _env,
    'args': _args,
    'exit': _exit,
    'now': _now,
    'timestamp': _timestamp,
    'cwd': _cwd,
    'cd': _cd,
    'datetime': _datetime_format,
    'datetime_parse': _datetime_parse,
    # ── 数学 / 统计 ──
    'avg': _avg,
    'mean': _avg,
    'median': _median,
    'product': _product,
    'clamp': _clamp,
    'floor': _floor,
    'ceil': _ceil,
    'round': _round,
    'abs': _abs,
    'deg2rad': _degrees_to_radians,
    'rad2deg': _radians_to_degrees,
    'is_even': _is_even,
    'is_odd': _is_odd,
    'is_prime': _is_prime,
    'fibonacci': _fibonacci,
    'factorial': _factorial,
    'gcd': _gcd,
    'lcm': _lcm,
    # ── 函数式 ──
    'reduce': _reduce,
    'any': _any,
    'all': _all,
    'compose': _compose,
    'pipe': _pipe,
    'tap': _tap,
    'memoize': _memoize,
    # ── 字典操作 ──
    'keys': _keys,
    'values': _values,
    'items': _items,
    'dict': _dict_from,
    'merge': _merge,
    'pick': _pick,
    'omit': _omit,
    'clone': _clone,
    # ── 类型 / 调试 ──
    'typeof': _typeof,
    'repr': _repr,
    'is_email': _is_email,
    'is_url': _is_url,
    'is_ip': _is_ip,
    'is_json': _is_json,
    'is_number': _is_number,
    'is_int': _is_int,
    # ── 编码 / 哈希 ──
    'md5': _md5,
    'sha256': _sha256,
    'base64_encode': _base64_encode,
    'base64_decode': _base64_decode,
    'url_encode': _url_encode,
    'url_decode': _url_decode,
    'parse_url': _parse_url,
    # ── 数据格式 ──
    'csv_parse': _csv_parse,
    'csv_stringify': _csv_stringify,
    'xml_parse': _xml_parse,
    # ── 正则 ──
    'regex_match': _regex_match,
    'regex_search': _regex_search,
    'regex_findall': _regex_findall,
    'regex_sub': _regex_sub,
    'regex_split': _regex_split,
    # ── 随机 / ID ──
    'random': _random,
    'random_int': _random_int,
    'random_choice': _random_choice,
    'shuffle': _shuffle,
    'sample': _sample,
    'uuid': _uuid,
    'nanoid': _nanoid,
    # ── 颜色 ──
    'hex2rgb': _hex_to_rgb,
    'rgb2hex': _rgb_to_hex,
    # ── 文本工具 ──
    'colorize': _color_console,
    'table': _table,
    'progress': _progress,
    'spinner': _spinner_frame,
    'levenshtein': _levenshtein,
    'similarity': _similarity,
    # ── 临时文件 ──
    'tempfile': _tempfile,
    'tempdir': _tempdir,
    # ── 性能 ──
    'benchmark': _benchmark,
}


# ════════════════════════════════════════════════════════════
# P3 扩充:正则 / 日期时间 / 加密 / 文件系统增强 / 网络增强
# (以下均为新代码,不改动上方已有实现)
# ════════════════════════════════════════════════════════════

import re as _re
import shutil as _shutil
import hashlib as _hashlib
import hmac as _hmac_mod
import base64 as _base64_mod
import uuid as _uuid_mod
import secrets as _secrets_mod
import socket as _socket_mod
from datetime import datetime as _dt_datetime, timedelta as _dt_timedelta


class AuroraRegex:
    """正则表达式模块(基于 Python re)。"""

    @staticmethod
    def match(pattern, text):
        """从头匹配;返回 {'match': str, 'start': int, 'end': int} 或 None。"""
        m = _re.match(pattern, text)
        if not m:
            return None
        return {'match': m.group(0), 'start': m.start(), 'end': m.end(),
                'groups': list(m.groups())}

    @staticmethod
    def search(pattern, text):
        """搜索第一个匹配;返回匹配信息或 None。"""
        m = _re.search(pattern, text)
        if not m:
            return None
        return {'match': m.group(0), 'start': m.start(), 'end': m.end(),
                'groups': list(m.groups())}

    @staticmethod
    def find_all(pattern, text):
        """返回所有匹配文本的列表。"""
        return _re.findall(pattern, text)

    @staticmethod
    def replace(pattern, replacement, text):
        """替换所有匹配。"""
        return _re.sub(pattern, replacement, text)

    @staticmethod
    def split(pattern, text):
        """按正则分割。"""
        return _re.split(pattern, text)


class AuroraDateTime:
    """日期时间模块(基于 Python datetime)。"""

    @staticmethod
    def now():
        """当前本地时间。"""
        return _dt_datetime.now()

    @staticmethod
    def timestamp():
        """当前 Unix 时间戳(秒)。"""
        return int(_dt_datetime.now().timestamp())

    @staticmethod
    def format(dt, fmt="%Y-%m-%d %H:%M:%S"):
        """格式化时间对象。"""
        return dt.strftime(fmt)

    @staticmethod
    def parse(s, fmt="%Y-%m-%d %H:%M:%S"):
        """按格式解析时间字符串。"""
        try:
            return _dt_datetime.strptime(s, fmt)
        except Exception as e:
            raise AuroraError("DateTimeError", str(e))

    @staticmethod
    def add_days(dt, n):
        """日期加减 n 天。"""
        return dt + _dt_timedelta(days=n)

    @staticmethod
    def diff(d1, d2):
        """两个日期相差天数(d1 - d2)。"""
        return (d1 - d2).days

    @staticmethod
    def today():
        """今天的日期(YYYY-MM-DD 字符串)。"""
        return _dt_datetime.now().strftime("%Y-%m-%d")


class AuroraCrypto:
    """加密 / 哈希 / 编码模块。"""

    @staticmethod
    def _bytes(data):
        if isinstance(data, bytes):
            return data
        return str(data).encode('utf-8')

    @staticmethod
    def md5(data):
        return _hashlib.md5(AuroraCrypto._bytes(data)).hexdigest()

    @staticmethod
    def sha1(data):
        return _hashlib.sha1(AuroraCrypto._bytes(data)).hexdigest()

    @staticmethod
    def sha256(data):
        return _hashlib.sha256(AuroraCrypto._bytes(data)).hexdigest()

    @staticmethod
    def sha512(data):
        return _hashlib.sha512(AuroraCrypto._bytes(data)).hexdigest()

    @staticmethod
    def hmac(key, data, algorithm='sha256'):
        algo = getattr(_hashlib, algorithm, _hashlib.sha256)
        return _hmac_mod.new(AuroraCrypto._bytes(key),
                             AuroraCrypto._bytes(data), algo).hexdigest()

    @staticmethod
    def base64_encode(data):
        return _base64_mod.b64encode(AuroraCrypto._bytes(data)).decode('ascii')

    @staticmethod
    def base64_decode(data):
        return _base64_mod.b64decode(AuroraCrypto._bytes(data)).decode('utf-8')

    @staticmethod
    def random_hex(length=16):
        """生成 n 个十六进制字符(实际 ceil(length/2) 字节)。"""
        nbytes = max(1, (length + 1) // 2)
        return _secrets_mod.token_hex(nbytes)[:length]

    @staticmethod
    def uuid():
        """UUID v4 字符串。"""
        return str(_uuid_mod.uuid4())


class AuroraFileSystem:
    """文件系统增强模块(补充 AuroraIO 未覆盖的操作)。"""

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def mkdir(path, recursive=True):
        try:
            if recursive:
                os.makedirs(path, exist_ok=True)
            else:
                os.mkdir(path)
            return True
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def remove(path):
        try:
            os.remove(path)
            return True
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def rmdir(path, recursive=False):
        try:
            if recursive:
                _shutil.rmtree(path)
            else:
                os.rmdir(path)
            return True
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def list_dir(path='.'):
        try:
            return sorted(os.listdir(path))
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def copy(src, dst):
        try:
            _shutil.copy2(src, dst)
            return dst
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def move(src, dst):
        try:
            _shutil.move(src, dst)
            return dst
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def file_size(path):
        try:
            return os.path.getsize(path)
        except Exception as e:
            raise AuroraError("FSError", str(e))

    @staticmethod
    def extension(path):
        return os.path.splitext(path)[1]

    @staticmethod
    def basename(path):
        return os.path.basename(path)

    @staticmethod
    def dirname(path):
        return os.path.dirname(path)

    @staticmethod
    def join_path(*parts):
        return os.path.join(*parts)

    @staticmethod
    def absolute_path(path):
        return os.path.abspath(path)


class AuroraNet:
    """网络增强模块(HTTP 动词 / 下载 / URL / TCP socket)。"""

    _DEFAULT_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    @staticmethod
    def _request(url, method='GET', data=None, json_body=None,
                 headers=None, timeout=30):
        hdrs = {'User-Agent': AuroraNet._DEFAULT_UA}
        if headers:
            hdrs.update(headers)
        body = None
        if json_body is not None:
            body = json.dumps(json_body).encode('utf-8')
            hdrs.setdefault('Content-Type', 'application/json')
        elif data is not None:
            body = data.encode('utf-8') if isinstance(data, str) else data
        try:
            req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception as e:
            raise AuroraError("NetError", str(e))

    @staticmethod
    def get(url, headers=None, timeout=30):
        return AuroraNet._request(url, 'GET', headers=headers, timeout=timeout)

    @staticmethod
    def post(url, data=None, json=None, headers=None, timeout=30):
        return AuroraNet._request(url, 'POST', data=data, json_body=json,
                                  headers=headers, timeout=timeout)

    @staticmethod
    def put(url, data=None, headers=None, timeout=30):
        return AuroraNet._request(url, 'PUT', data=data, headers=headers, timeout=timeout)

    @staticmethod
    def delete(url, headers=None, timeout=30):
        return AuroraNet._request(url, 'DELETE', headers=headers, timeout=timeout)

    @staticmethod
    def download(url, path):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AuroraNet._DEFAULT_UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, 'wb') as f:
                f.write(r.read())
            return path
        except Exception as e:
            raise AuroraError("NetError", str(e))

    @staticmethod
    def url_parse(url):
        p = urllib.parse.urlparse(url)
        return {'scheme': p.scheme, 'netloc': p.netloc, 'path': p.path,
                'params': p.params, 'query': p.query, 'fragment': p.fragment,
                'hostname': p.hostname, 'port': p.port}

    @staticmethod
    def url_encode(params):
        return urllib.parse.urlencode(params or {})

    # ── TCP socket(薄包装;连接对象用 dict 持有底层 socket)──

    @staticmethod
    def socket_connect(host, port):
        try:
            s = _socket_mod.create_connection((host, int(port)), timeout=30)
            return {'_sock': s}
        except Exception as e:
            raise AuroraError("NetError", str(e))

    @staticmethod
    def socket_send(conn, data):
        s = conn['_sock']
        payload = data.encode('utf-8') if isinstance(data, str) else data
        try:
            return s.sendall(payload) or len(payload)
        except Exception as e:
            raise AuroraError("NetError", str(e))

    @staticmethod
    def socket_recv(conn, size=4096):
        s = conn['_sock']
        try:
            return s.recv(size).decode('utf-8', errors='replace')
        except Exception as e:
            raise AuroraError("NetError", str(e))

    @staticmethod
    def socket_close(conn):
        try:
            conn['_sock'].close()
            return True
        except Exception as e:
            raise AuroraError("NetError", str(e))
