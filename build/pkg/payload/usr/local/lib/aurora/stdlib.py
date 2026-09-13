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
        'configure': AuroraAI.configure,
        'chat': AuroraAI.chat,
        'messages': AuroraAI.messages,
        'agent': AuroraAI.agent,
    },
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
}
