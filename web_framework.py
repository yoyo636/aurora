"""Aurora v3.2.0 全栈 Web 框架(std.web 增强版)

纯 Python 标准库实现,将被注册为 Aurora 语言的 `std.web` 内置模块。
包含后端(Router / Middleware / Request / Response / WebSocket / Static /
Session / App)、前端概念层(Component / VDom / 响应式 State / CSS-in-JS
Style),以及全栈集成(TypeSharing / APIClient / SSR / HotReload)。

设计约定:
  - 所有类/函数在模块顶层定义,可 `from aurora.web_framework import *`。
  - 中间件以"包装器(wrap)"形式存在:每个工厂返回一个 (handler)->handler 的函数,
    apply_middleware 负责把它们组合成一条责任链。
  - handler 统一签名为 handler(request) -> Response(也可返回 dict/str,由 App 归一化)。
"""

import os
import re
import json
import time
import zlib
import hmac
import base64
import hashlib
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, List, Optional, Tuple

# 模块版本
__version__ = "3.2.0"


# ══════════════════════════════════════════════════════════════════════
# 1. Router —— 路由表,支持 :param 路径参数
# ══════════════════════════════════════════════════════════════════════
class Router:
    """HTTP 路由器:注册路由并把 (path, method) 映射到 handler。

    路径参数语法 `:name`,例如 `/users/:id/posts/:post_id`。
    """

    def __init__(self) -> None:
        # 每项: (method, path, compiled_regex, param_names, handler)
        self._routes: List[Tuple[str, str, "re.Pattern", List[str], Callable]] = []

    @staticmethod
    def _compile(path: str):
        """把 `/users/:id` 编译为带命名组的正则,并提取参数名。"""
        param_names: List[str] = []
        regex_parts: List[str] = []
        for segment in path.split("/"):
            if segment.startswith(":"):
                name = segment[1:]
                param_names.append(name)
                regex_parts.append(r"(?P<%s>[^/]+)" % name)
            else:
                regex_parts.append(re.escape(segment))
        pattern = re.compile(r"^" + "/".join(regex_parts) + r"$")
        return pattern, param_names

    def add_route(self, method: str, path: str, handler: Callable) -> None:
        """注册一条路由。"""
        pattern, param_names = self._compile(path)
        self._routes.append((method.upper(), path, pattern, param_names, handler))

    # —— 便捷注册方法 ——
    def get(self, path: str, handler: Callable) -> Callable:
        self.add_route("GET", path, handler)
        return handler

    def post(self, path: str, handler: Callable) -> Callable:
        self.add_route("POST", path, handler)
        return handler

    def put(self, path: str, handler: Callable) -> Callable:
        self.add_route("PUT", path, handler)
        return handler

    def delete(self, path: str, handler: Callable) -> Callable:
        self.add_route("DELETE", path, handler)
        return handler

    def match(self, path: str, method: str):
        """匹配路由。返回 (handler, params_dict);未命中返回 (None, {})。"""
        method = method.upper()
        for r_method, _path, pattern, _names, handler in self._routes:
            if r_method != method:
                continue
            m = pattern.match(path)
            if m:
                return handler, m.groupdict()
        return None, {}


# ══════════════════════════════════════════════════════════════════════
# 2. Middleware —— 中间件基类与内置工厂
# ══════════════════════════════════════════════════════════════════════
class Middleware:
    """中间件基类:包裹一个下游 handler,可在前后做横切逻辑。"""

    def __init__(self, handler: Optional[Callable] = None) -> None:
        self.handler = handler

    def __call__(self, request):
        # 默认行为:直接放行给下游
        if self.handler is not None:
            return self.handler(request)
        return None


def apply_middleware(handler: Callable, *middlewares: Callable) -> Callable:
    """把若干 wrap(handler)->handler 的中间件组合成一条链。

    按传入顺序包裹,因此第一个中间件最先拿到请求(最外层)。
    """
    for mw in reversed(middlewares):
        handler = mw(handler)
    return handler


def logger_middleware() -> Callable:
    """访问日志中间件:打印方法/路径/耗时。"""
    def wrap(handler: Callable) -> Callable:
        def inner(request):
            start = time.time()
            resp = handler(request)
            cost_ms = (time.time() - start) * 1000
            print("[web] %s %s -> %.1fms" % (getattr(request, "method", "?"),
                                             getattr(request, "path", "?"),
                                             cost_ms))
            return resp
        return inner
    return wrap


def cors_middleware(origins: str = "*") -> Callable:
    """CORS 中间件:注入跨域响应头,并处理 OPTIONS 预检。"""
    def wrap(handler: Callable) -> Callable:
        def inner(request):
            if getattr(request, "method", "") == "OPTIONS":
                return Response("", status=204, headers={
                    "Access-Control-Allow-Origin": origins,
                    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                })
            resp = handler(request)
            if isinstance(resp, Response):
                resp.set_header("Access-Control-Allow-Origin", origins)
            return resp
        return inner
    return wrap


def auth_middleware(check_fn: Callable) -> Callable:
    """鉴权中间件:check_fn(request) 返回 False 则拒绝(401)。"""
    def wrap(handler: Callable) -> Callable:
        def inner(request):
            if not check_fn(request):
                return Response.json({"error": "unauthorized"}, status=401)
            return handler(request)
        return inner
    return wrap


def compress_middleware() -> Callable:
    """压缩中间件占位:对纯文本/JSON 响应做 gzip 内容协商(简化版)。"""
    def wrap(handler: Callable) -> Callable:
        def inner(request):
            resp = handler(request)
            # 此处不实际压缩以保持纯标准库且行为可预测,仅打标记头
            if isinstance(resp, Response):
                resp.set_header("X-Compress", "identity")
            return resp
        return inner
    return wrap


def rate_limit_middleware(max_requests: int, window_sec: float) -> Callable:
    """简单滑动窗口限流(按进程内全局计数)。超限返回 429。"""
    buckets: Dict[str, List[float]] = {}
    lock = threading.Lock()

    def wrap(handler: Callable) -> Callable:
        def inner(request):
            now = time.time()
            key = "global"  # 简化:无客户端 IP 时全局计数
            with lock:
                hits = [t for t in buckets.get(key, []) if now - t < window_sec]
                hits.append(now)
                buckets[key] = hits
                if len(hits) > max_requests:
                    return Response.json({"error": "too many requests"}, status=429)
            return handler(request)
        return inner
    return wrap


# ══════════════════════════════════════════════════════════════════════
# 3. Request —— 请求对象
# ══════════════════════════════════════════════════════════════════════
class Request:
    """封装一次 HTTP 请求的所有输入。"""

    def __init__(self, method: str = "GET", path: str = "/",
                 query: Optional[Dict[str, str]] = None,
                 headers: Optional[Dict[str, str]] = None,
                 body: str = "") -> None:
        self.method = method.upper()
        self.path = path
        self.query = dict(query or {})
        self.headers = {k.title(): v for k, v in (headers or {}).items()}
        self.body = body
        self.params: Dict[str, str] = {}      # 路径参数,由 Router 填充
        self._json: Optional[Any] = None
        self._json_parsed = False

    # —— JSON body ——
    @property
    def json(self):
        """解析 body 为 JSON 对象(惰性、缓存)。"""
        if not self._json_parsed:
            try:
                self._json = json.loads(self.body) if self.body else None
            except (ValueError, TypeError):
                self._json = None
            self._json_parsed = True
        return self._json

    # —— 表单 urlencoded body ——
    @property
    def form(self) -> Dict[str, str]:
        """解析 application/x-www-form-urlencoded body。"""
        return dict(urllib.parse.parse_qsl(self.body or ""))

    # —— Cookie ——
    @property
    def cookies(self) -> Dict[str, str]:
        """解析 Cookie 请求头为字典。"""
        raw = self.headers.get("Cookie", "")
        out: Dict[str, str] = {}
        for pair in raw.split(";"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                out[k.strip()] = v.strip()
        return out

    # —— 上传文件(简化 multipart 解析)——
    def file(self, name: str) -> Optional[Dict[str, Any]]:
        """按表单字段名取上传文件信息 {'filename','content'}。
        仅做最小可用解析;非 multipart 时返回 None。"""
        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            return None
        m = re.search(r'boundary=([^;]+)', ctype)
        if not m:
            return None
        boundary = m.group(1).strip()
        files: Dict[str, Dict[str, Any]] = {}
        for chunk in self.body.split("--" + boundary):
            name_m = re.search(r'name="([^"]+)"', chunk)
            file_m = re.search(r'filename="([^"]*)"', chunk)
            if name_m and file_m is not None and file_m.group(1):
                fname = file_m.group(1)
                # 取双换行之后的内容作为文件体(简化)
                parts = chunk.split("\r\n\r\n", 1)
                content = parts[1] if len(parts) == 2 else ""
                files[name_m.group(1)] = {"filename": fname, "content": content}
        return files.get(name)


# ══════════════════════════════════════════════════════════════════════
# 4. Response —— 响应对象
# ══════════════════════════════════════════════════════════════════════
class Response:
    """HTTP 响应:body / status / headers,可序列化为 (status, headers, body)。"""

    def __init__(self, body: str = "", status: int = 200,
                 headers: Optional[Dict[str, str]] = None,
                 content_type: Optional[str] = None) -> None:
        self.body = body if isinstance(body, str) else str(body)
        self.status = status
        self.headers: Dict[str, Any] = dict(headers or {})
        self._cookies: List[str] = []
        if content_type:
            self.headers["Content-Type"] = content_type

    # —— 便捷构造 ——
    @staticmethod
    def json(data: Any, status: int = 200) -> "Response":
        return Response(json.dumps(data, ensure_ascii=False),
                        status=status,
                        content_type="application/json; charset=utf-8")

    @staticmethod
    def html(content: str, status: int = 200) -> "Response":
        return Response(content, status=status,
                        content_type="text/html; charset=utf-8")

    @staticmethod
    def text(content: str, status: int = 200) -> "Response":
        return Response(content, status=status,
                        content_type="text/plain; charset=utf-8")

    @staticmethod
    def redirect(url: str, status: int = 302) -> "Response":
        return Response("", status=status, headers={"Location": url})

    # —— 头与 Cookie ——
    def set_header(self, key: str, value: str) -> None:
        self.headers[key] = value

    def set_cookie(self, name: str, value: str, max_age: Optional[int] = None,
                   path: str = "/") -> None:
        """追加一条 Set-Cookie 头。"""
        parts = ["%s=%s" % (name, value), "Path=%s" % path]
        if max_age is not None:
            parts.append("Max-Age=%d" % int(max_age))
        self._cookies.append("; ".join(parts))

    def to_http_response(self) -> Tuple[int, Dict[str, Any], str]:
        """序列化为 (status, headers_dict, body_str)。Set-Cookie 以列表形式存放。"""
        headers = dict(self.headers)
        if self._cookies:
            headers["Set-Cookie"] = list(self._cookies)
        return self.status, headers, self.body


# ══════════════════════════════════════════════════════════════════════
# 7. Static —— 静态文件服务
# ══════════════════════════════════════════════════════════════════════
class Static:
    """静态文件服务:把目录映射为 URL 前缀,自动推断 MIME、加缓存头。"""

    MIME = {
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".txt": "text/plain; charset=utf-8",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".map": "application/json",
    }

    @classmethod
    def serve(cls, directory: str, url_prefix: str = "/static") -> Callable:
        """返回一个 handler(request)->Response,用于挂到路由/App。"""
        url_prefix = url_prefix.rstrip("/") or "/"

        def handler(request: Request) -> Response:
            # 去掉 URL 前缀,得到相对路径
            rel = request.path[len(url_prefix):] if request.path.startswith(url_prefix) else request.path
            rel = rel.lstrip("/")
            # 防目录穿越
            real = os.path.normpath(os.path.join(directory, rel))
            if not real.startswith(os.path.normpath(directory)):
                return Response.text("Forbidden", status=403)
            if os.path.isdir(real):
                real = os.path.join(real, "index.html")
            if not os.path.isfile(real):
                return Response.text("Not Found", status=404)
            ext = os.path.splitext(real)[1].lower()
            ctype = cls.MIME.get(ext, "application/octet-stream")
            with open(real, "rb") as f:
                data = f.read()
            body = data.decode("utf-8", "replace")
            resp = Response(body, content_type=ctype)
            # 简单缓存头:1 小时
            resp.set_header("Cache-Control", "public, max-age=3600")
            return resp

        return handler


# ══════════════════════════════════════════════════════════════════════
# 8. Session —— 会话存储
# ══════════════════════════════════════════════════════════════════════
class MemorySessionStore:
    """进程内内存会话存储。"""

    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get(self, sid: str) -> Dict[str, Any]:
        return dict(self._data.get(sid, {}))

    def set(self, sid: str, key: str, value: Any) -> None:
        with self._lock:
            self._data.setdefault(sid, {})[key] = value

    def clear(self, sid: str) -> None:
        with self._lock:
            self._data.pop(sid, None)


class CookieSessionStore:
    """基于 Cookie 的签名会话存储(数据放在客户端,用 HMAC 防篡改)。"""

    def __init__(self, secret: str = "aurora-default-secret") -> None:
        self.secret = secret

    def _sign(self, payload: str) -> str:
        return hmac.new(self.secret.encode(), payload.encode(),
                        hashlib.sha256).hexdigest()[:32]

    def get(self, sid: str) -> Dict[str, Any]:
        # sid 形如 "payload.signature"
        try:
            payload, sig = sid.rsplit(".", 1)
        except ValueError:
            return {}
        if not hmac.compare_digest(sig, self._sign(payload)):
            return {}
        try:
            return json.loads(base64.b64decode(payload).decode("utf-8"))
        except Exception:
            return {}

    def set(self, sid: str, key: str, value: Any) -> str:
        data = self.get(sid)
        data[key] = value
        payload = base64.b64encode(json.dumps(data).encode()).decode()
        return "%s.%s" % (payload, self._sign(payload))

    def clear(self, sid: str) -> str:
        return ""


class Session:
    """会话门面:从请求 Cookie 取/存会话数据。"""

    # 默认使用内存存储
    default_store = MemorySessionStore()

    COOKIE_NAME = "aurora_sid"

    def __init__(self, store=None) -> None:
        self.store = store or Session.default_store

    @staticmethod
    def _sid_from_request(request: Request) -> str:
        return request.cookies.get(Session.COOKIE_NAME, "")

    def get(self, request: Request) -> Dict[str, Any]:
        sid = self._sid_from_request(request)
        if not sid:
            return {}
        return self.store.get(sid)

    def set(self, request: Request, key: str, value: Any) -> str:
        sid = self._sid_from_request(request) or self._new_sid()
        result = self.store.set(sid, key, value)
        # Cookie 存储会返回新的签名串,作为新的 sid
        return result if isinstance(result, str) else sid

    def clear(self, request: Request) -> None:
        sid = self._sid_from_request(request)
        if sid:
            self.store.clear(sid)

    @staticmethod
    def _new_sid() -> str:
        return base64.b64encode(os.urandom(16)).decode()


# ══════════════════════════════════════════════════════════════════════
# 5. WebSocket —— 手写 socket 简化版
# ══════════════════════════════════════════════════════════════════════
class WebSocket:
    """WebSocket 服务(标准库 socket 手写简化版)。

    提供握手与文本帧编解码;真正的 serve() 在独立线程里跑阻塞 socket。
    handler 对象应实现 on_connect/on_message/on_disconnect 回调。
    """

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self) -> None:
        self.on_connect: Optional[Callable] = None
        self.on_message: Optional[Callable] = None
        self.on_disconnect: Optional[Callable] = None
        self._clients: List[Any] = []

    # —— 帧编解码 ——
    @staticmethod
    def encode_text(message: str) -> bytes:
        """服务端 -> 客户端文本帧(不带掩码)。"""
        payload = message.encode("utf-8")
        n = len(payload)
        out = bytearray([0x81])  # FIN + opcode=1(text)
        if n < 126:
            out.append(n)
        elif n < 65536:
            out.append(126)
            out += n.to_bytes(2, "big")
        else:
            out.append(127)
            out += n.to_bytes(8, "big")
        out += payload
        return bytes(out)

    @staticmethod
    def decode_text(data: bytes) -> Optional[str]:
        """客户端 -> 服务端文本帧(掩码)。返回解码出的文本。"""
        if len(data) < 2:
            return None
        b1, b2 = data[0], data[1]
        opcode = b1 & 0x0F
        masked = b2 & 0x80
        length = b2 & 0x7F
        idx = 2
        if length == 126:
            length = int.from_bytes(data[idx:idx + 2], "big")
            idx += 2
        elif length == 127:
            length = int.from_bytes(data[idx:idx + 8], "big")
            idx += 8
        mask = data[idx:idx + 4] if masked else b""
        idx += 4 if masked else 0
        payload = data[idx:idx + length]
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 8:  # close
            return None
        return payload.decode("utf-8", "replace")

    @staticmethod
    def accept_key(client_key: str) -> str:
        """计算 Sec-WebSocket-Accept。"""
        merged = (client_key + WebSocket.GUID).encode()
        return base64.b64encode(hashlib.sha1(merged).digest()).decode()

    # —— 连接管理 ——
    def send(self, message: str) -> None:
        """向当前/默认连接发送(由具体连接对象持有 socket 时覆写)。"""
        for c in self._clients:
            try:
                c.send(self.encode_text(message))
            except Exception:
                pass

    def broadcast(self, message: str) -> None:
        """向所有已连接客户端广播。"""
        self.send(message)

    @classmethod
    def serve(cls, port: int = 8080, handlers: Optional[Dict[str, Any]] = None,
              host: str = "127.0.0.1") -> Dict[str, Any]:
        """启动 WebSocket 服务(后台线程)。handlers: {path: handler实例}。"""
        import socket

        handlers = handlers or {}
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(16)
        actual_port = server.getsockname()[1]

        def loop():
            while True:
                try:
                    conn, _addr = server.accept()
                except Exception:
                    break
                threading.Thread(target=cls._handle_conn,
                                 args=(conn, handlers), daemon=True).start()

        threading.Thread(target=loop, daemon=True).start()
        return {"host": host, "port": actual_port,
                "url": "ws://%s:%d/" % (host, actual_port)}

    @classmethod
    def _handle_conn(cls, conn, handlers: Dict[str, Any]) -> None:
        try:
            req = conn.recv(4096).decode("utf-8", "replace")
            headers = {}
            for line in req.splitlines()[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().title()] = v.strip()
            key = headers.get("Sec-WebSocket-Key", "")
            accept = cls.accept_key(key)
            handshake = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                "Sec-WebSocket-Accept: %s\r\n\r\n" % accept)
            conn.sendall(handshake.encode())
            path = req.split(" ", 2)[1] if " " in req else "/"
            handler = handlers.get(path) or handlers.get("/")
            if handler and getattr(handler, "on_connect", None):
                handler.on_connect()
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                text = cls.decode_text(data)
                if handler and getattr(handler, "on_message", None) and text is not None:
                    handler.on_message(text)
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════════════
# 9. App —— 主应用
# ══════════════════════════════════════════════════════════════════════
class App:
    """Aurora Web 主应用:聚合路由、中间件、静态文件、WebSocket。"""

    def __init__(self, name: str = "aurora-app") -> None:
        self.name = name
        self.router = Router()
        self._middleware: List[Callable] = []
        self._static: List[Tuple[str, str]] = []      # (url_prefix, directory)
        self._ws_handlers: Dict[str, Any] = {}
        self._httpd: Optional[ThreadingHTTPServer] = None

    # —— 全局中间件 ——
    def use(self, middleware: Callable) -> None:
        """注册全局中间件(wrap 工厂)。"""
        self._middleware.append(middleware)

    # —— 路由装饰器 ——
    def route(self, method: str, path: str) -> Callable:
        def decorator(fn: Callable) -> Callable:
            self.router.add_route(method, path, fn)
            return fn
        return decorator

    def get(self, path: str) -> Callable:
        return self.route("GET", path)

    def post(self, path: str) -> Callable:
        return self.route("POST", path)

    def put(self, path: str) -> Callable:
        return self.route("PUT", path)

    def delete(self, path: str) -> Callable:
        return self.route("DELETE", path)

    # —— 静态 / WebSocket ——
    def static(self, url_path: str, directory: str) -> None:
        self._static.append((url_path.rstrip("/"), directory))

    def websocket(self, path: str, handler) -> None:
        self._ws_handlers[path] = handler

    # —— 核心请求处理 ——
    def handle_request(self, request: Request) -> Response:
        """匹配路由 -> 串中间件 -> 调用 handler,返回 Response。"""
        handler, params = self.router.match(request.path, request.method)
        request.params = params

        # 路由未命中时尝试静态文件
        if handler is None and request.method == "GET":
            for prefix, directory in self._static:
                if request.path == prefix or request.path.startswith(prefix + "/"):
                    return Static.serve(directory, prefix)(request)
            return Response.text("Not Found", status=404)

        chain = apply_middleware(handler, *self._middleware)
        try:
            result = chain(request)
        except Exception as e:  # noqa: BLE001
            return Response.text("Internal Server Error: %s" % e, status=500)

        # 归一化返回值
        if isinstance(result, Response):
            return result
        if isinstance(result, dict):
            return Response.json(result)
        return Response.html(str(result))

    # —— 启动 HTTP 服务 ——
    def run(self, port: int = 8080, host: str = "127.0.0.1") -> Dict[str, Any]:
        """启动 HTTP 服务(后台线程),返回 {host, port, url}。"""
        app = self

        class _Handler(BaseHTTPRequestHandler):
            def _dispatch(self):
                length = int(self.headers.get("Content-Length") or 0)
                body = (self.rfile.read(length).decode("utf-8", "replace")
                        if length else "")
                parsed = urllib.parse.urlparse(self.path)
                query = dict(urllib.parse.parse_qsl(parsed.query))
                headers = {k: v for k, v in self.headers.items()}
                req = Request(self.command, parsed.path, query, headers, body)
                resp = app.handle_request(req)
                status, resp_headers, body_str = resp.to_http_response()
                self.send_response(status)
                for k, v in resp_headers.items():
                    if isinstance(v, list):
                        for item in v:
                            self.send_header(k, item)
                    else:
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(body_str.encode("utf-8"))

            def do_GET(self): self._dispatch()
            def do_POST(self): self._dispatch()
            def do_PUT(self): self._dispatch()
            def do_DELETE(self): self._dispatch()
            def do_OPTIONS(self): self._dispatch()
            def log_message(self, *a): pass

        self._httpd = ThreadingHTTPServer((host, port), _Handler)
        threading.Thread(target=self._httpd.serve_forever, daemon=True).start()
        # WebSocket(若注册了)
        if self._ws_handlers:
            WebSocket.serve(port + 1, self._ws_handlers, host)
        actual = self._httpd.server_address[1]
        return {"host": host, "port": actual, "url": "http://%s:%d/" % (host, actual)}


# ══════════════════════════════════════════════════════════════════════
# 10. VDom —— 虚拟 DOM
# ══════════════════════════════════════════════════════════════════════
class VNode:
    """虚拟 DOM 节点。"""

    __slots__ = ("tag", "props", "children", "key")

    def __init__(self, tag: str, props: Optional[Dict] = None,
                 children: Optional[List] = None) -> None:
        self.tag = tag
        self.props = dict(props or {})
        self.children = list(children or [])
        self.key = self.props.get("key") if self.props else None

    def __repr__(self) -> str:
        return "VNode(%r, children=%d)" % (self.tag, len(self.children))


def create_element(tag: str, props: Optional[Dict] = None, *children) -> VNode:
    """工厂函数:创建 VNode。children 会被拍平并过滤 None/False。"""
    flat: List[Any] = []
    for c in children:
        if c is None or c is False:
            continue
        if isinstance(c, (list, tuple)):
            flat.extend(x for x in c if x is not None and x is not False)
        else:
            flat.append(c)
    return VNode(tag, props, flat)


def _render_node(node: Any) -> str:
    """递归渲染单个节点为 HTML 字符串。"""
    if node is None or node is False:
        return ""
    if isinstance(node, str):
        return _escape(node)
    if isinstance(node, (int, float)):
        return str(node)
    if isinstance(node, VNode):
        return _render_vnode(node)
    # Component 实例
    render = getattr(node, "render", None)
    if callable(render):
        return _render_node(render())
    return _escape(str(node))


def _escape(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _render_vnode(vnode: VNode) -> str:
    """把 VNode 渲染为 HTML 字符串(SSR 用)。"""
    attrs: List[str] = []
    skip_event = {"key", "ref"}
    for k, v in vnode.props.items():
        if k.startswith("on_") or k in skip_event:
            continue
        if k == "class":
            attrs.append('class="%s"' % _escape(v))
        elif k == "style" and isinstance(v, dict):
            style = ";".join("%s:%s" % (_dash(sk), sv) for sk, sv in v.items())
            attrs.append('style="%s"' % _escape(style))
        elif v is True:
            attrs.append(_dash(k))
        elif v is False or v is None:
            continue
        else:
            attrs.append('%s="%s"' % (_dash(k), _escape(v)))
    attr_str = (" " + " ".join(attrs)) if attrs else ""
    inner = "".join(_render_node(c) for c in vnode.children)
    return "<%s%s>%s</%s>" % (vnode.tag, attr_str, inner, vnode.tag)


def _dash(name: str) -> str:
    """驼峰 -> 短横线(className -> class-name,但 className 特判为 class)。"""
    if name == "className":
        return "class"
    return re.sub(r"([A-Z])", r"-\1", name).lower()


def render_to_string(vnode) -> str:
    """把 VNode/组件渲染为 HTML 字符串(服务端渲染)。"""
    return _render_node(vnode)


def diff(old_vnode, new_vnode) -> List[Dict]:
    """简单 diff,返回补丁列表。每项形如 {'type','path',...}。"""
    patches: List[Dict] = []

    def walk(old, new, path: str):
        if old is None or old is False:
            patches.append({"type": "CREATE", "path": path, "node": new})
            return
        if isinstance(old, VNode) and isinstance(new, VNode):
            if old.tag != new.tag:
                patches.append({"type": "REPLACE", "path": path, "node": new})
                return
            # props 变化
            if old.props != new.props:
                patches.append({"type": "PROPS", "path": path,
                                "old": old.props, "new": new.props})
            # 子节点
            oc, nc = old.children, new.children
            for i in range(max(len(oc), len(nc))):
                child_path = "%s/%d" % (path, i)
                if i >= len(oc):
                    patches.append({"type": "CREATE", "path": child_path,
                                    "node": nc[i]})
                elif i >= len(nc):
                    patches.append({"type": "REMOVE", "path": child_path})
                else:
                    walk(oc[i], nc[i], child_path)
        else:
            if old != new:
                patches.append({"type": "TEXT", "path": path, "node": new})

    walk(old_vnode, new_vnode, "0")
    return patches


def patch(dom, patches: List[Dict]):
    """把补丁应用到一棵轻量 DOM 树(此处仅记录并返回 dom,概念性实现)。"""
    for op in patches:
        # 真实浏览器中会操作 DOM;这里的"dom"是任意对象,仅做标记
        if not hasattr(dom, "__aurora_patches__"):
            dom.__aurora_patches__ = []  # type: ignore[attr-defined]
        dom.__aurora_patches__.append(op)  # type: ignore[attr-defined]
    return dom


# ══════════════════════════════════════════════════════════════════════
# 11. State —— 响应式状态
# ══════════════════════════════════════════════════════════════════════
class _Ref:
    """响应式引用:读写 .value 并在变化时通知 watcher。"""

    def __init__(self, value: Any) -> None:
        self._value = value
        self._cbs: List[Callable] = []

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, v: Any) -> None:
        old = self._value
        self._value = v
        for cb in list(self._cbs):
            cb(v, old)

    def _watch(self, cb: Callable) -> None:
        self._cbs.append(cb)


class _ReactiveDict(dict):
    """响应式字典:赋值时通知订阅者。"""

    def __init__(self, *a, **kw) -> None:
        super().__init__(*a, **kw)
        self._cbs: List[Callable] = []

    def __setitem__(self, key, value):  # noqa: D401
        old = super().get(key)
        super().__setitem__(key, value)
        for cb in list(self._cbs):
            cb(key, value, old)

    def _watch(self, cb: Callable) -> None:
        self._cbs.append(cb)


def reactive(initial: Optional[Dict] = None):
    """把字典包装为响应式对象。"""
    return _ReactiveDict(initial or {})


def ref(value: Any = None) -> _Ref:
    """创建响应式引用。"""
    return _Ref(value)


class _Computed:
    """计算属性:惰性求值,读取时执行 fn。"""

    def __init__(self, fn: Callable) -> None:
        self._fn = fn
        self._cache: Any = None
        self._dirty = True

    @property
    def value(self):
        if self._dirty:
            self._cache = self._fn()
            self._dirty = False
        return self._cache

    def invalidate(self):
        self._dirty = True


def computed(fn: Callable) -> _Computed:
    """创建计算属性。"""
    return _Computed(fn)


def watch(source, callback: Callable) -> None:
    """监听响应式源(ref 或 reactive dict)的变化。"""
    watcher = getattr(source, "_watch", None)
    if callable(watcher):
        watcher(callback)


# ══════════════════════════════════════════════════════════════════════
# 9. Component —— 组件基类
# ══════════════════════════════════════════════════════════════════════
class Component:
    """前端组件基类:props/state + 生命周期 + render()。"""

    def __init__(self, props: Optional[Dict] = None) -> None:
        self.props: Dict = dict(props or {})
        self.state: Dict = {}
        self._mounted = False

    # —— 生命周期 ——
    def mount(self) -> None:
        """挂载完成时调用(子类可覆写)。"""
        self._mounted = True

    def update(self, new_props: Optional[Dict] = None) -> None:
        """props 更新时调用。"""
        if new_props:
            self.props.update(new_props)

    def unmount(self) -> None:
        """卸载时调用。"""
        self._mounted = False

    # —— 状态 ——
    def set_state(self, new_state: Dict) -> None:
        """合并状态并触发更新(此处直接合并,概念上会触发重渲染)。"""
        self.state.update(new_state)

    # —— 渲染 ——
    def render(self) -> VNode:
        """子类覆写:返回 VNode。"""
        return create_element("div", None, "Component")


# ══════════════════════════════════════════════════════════════════════
# 12. Style —— CSS-in-JS
# ══════════════════════════════════════════════════════════════════════
class _StyleRegistry:
    """收集作用域 className 与 CSS,最后统一输出。"""

    def __init__(self) -> None:
        self.rules: List[str] = []
        self.counter = 0

    def reset(self) -> None:
        self.rules = []
        self.counter = 0


_style_registry = _StyleRegistry()


def css(styles_dict: Dict) -> str:
    """生成作用域 className 并记录 CSS 规则。"""
    digest = zlib.crc32(json.dumps(styles_dict, sort_keys=True).encode()) & 0xffffffff
    cls_name = "ax-%08x" % digest
    body = ";".join("%s:%s" % (_dash(k), v) for k, v in styles_dict.items())
    _style_registry.rules.append(".%s { %s; }" % (cls_name, body))
    return cls_name


def keyframes(name: str, frames: Dict[str, Dict]) -> str:
    """注册 CSS 关键帧动画,返回动画名。"""
    blocks = []
    for progress, props in frames.items():
        body = ";".join("%s:%s" % (_dash(k), v) for k, v in props.items())
        blocks.append("%s { %s; }" % (progress, body))
    _style_registry.rules.append("@keyframes %s { %s }" % (name, " ".join(blocks)))
    return name


def inject_styles() -> str:
    """输出已收集的全部 CSS(用于 <style> 标签内容)。"""
    return "\n".join(_style_registry.rules)


# ══════════════════════════════════════════════════════════════════════
# 13. TypeSharing —— 前后端类型共享
# ══════════════════════════════════════════════════════════════════════
_TYPE_MAP = {"int": "number", "float": "number", "str": "string",
             "bool": "boolean", "null": "null", "any": "any"}


def define_types(type_defs: Dict[str, Any]) -> Dict[str, Any]:
    """定义共享类型,原样返回(可链式)。"""
    return dict(type_defs)


def generate_typescript(defs: Dict[str, Any]) -> str:
    """从类型定义生成 TypeScript interface 字符串。"""
    lines: List[str] = []
    for name, fields in defs.items():
        lines.append("export interface %s {" % name)
        for fname, ftype in (fields or {}).items():
            ts_type = _TYPE_MAP.get(ftype, str(ftype))
            lines.append("  %s: %s;" % (fname, ts_type))
        lines.append("}")
    return "\n".join(lines)


def generate_aurora(defs: Dict[str, Any]) -> str:
    """从类型定义生成 Aurora 类型定义字符串。"""
    lines: List[str] = []
    for name, fields in defs.items():
        lines.append("type %s {" % name)
        for fname, ftype in (fields or {}).items():
            lines.append("  %s: %s" % (fname, ftype))
        lines.append("}")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════
# 14. APIClient —— 从路由生成前端 fetch 封装
# ══════════════════════════════════════════════════════════════════════
def generate_client(routes, base_url: str = "/api") -> str:
    """从路由列表生成前端 JS API 调用代码(字符串)。

    routes 可为 [(method, path), ...] 或 Router 实例。
    """
    if hasattr(routes, "_routes"):
        route_list = [(m, p) for (m, p, _pat, _names, _h) in routes._routes]
    else:
        route_list = list(routes)

    lines = [
        "// 自动生成的 Aurora API Client(请勿手动编辑)",
        "const BASE = %s;" % json.dumps(base_url),
        "async function _req(method, url, body) {",
        "  const res = await fetch(BASE + url, {",
        "    method,",
        "    headers: { 'Content-Type': 'application/json' },",
        "    body: body === undefined ? undefined : JSON.stringify(body),",
        "  });",
        "  return res.json();",
        "}",
        "function _fill(path, params) {",
        "  return Object.keys(params || {}).reduce((p, k) =>",
        "    p.replace(':' + k, encodeURIComponent(params[k])), path);",
        "}",
        "export const api = {",
    ]
    for method, path in route_list:
        # /users/:id -> users_id
        fn_name = re.sub(r":([a-z_]+)", r"\1", path)
        fn_name = re.sub(r"[^a-zA-Z0-9]+", "_", fn_name).strip("_") or "root"
        full_name = "%s_%s" % (method.lower(), fn_name)
        lines.append(
            "  %s: (params, body) => _req(%s, _fill(%s, params), body),"
            % (full_name, json.dumps(method.upper()), json.dumps(path))
        )
    lines.append("};")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════
# 15. SSR —— 服务端渲染
# ══════════════════════════════════════════════════════════════════════
def render_server(component_class, props: Optional[Dict] = None) -> Tuple[str, str]:
    """服务端渲染组件,返回 (html字符串, 初始状态JSON字符串)。"""
    comp = component_class(props or {})
    comp.mount()
    html_str = render_to_string(comp.render())
    state_json = json.dumps({"props": comp.props, "state": comp.state},
                            ensure_ascii=False)
    return html_str, state_json


def hydrate_script(component_name: str, props: Dict, state: Any) -> str:
    """生成浏览器端水合脚本。"""
    return (
        "<script>window.__AURORA_HYDRATE__ = {"
        "component: %s, props: %s, state: %s};</script>"
        % (json.dumps(component_name), json.dumps(props, ensure_ascii=False),
           json.dumps(state, ensure_ascii=False))
    )


# ══════════════════════════════════════════════════════════════════════
# 16. HotReload —— 文件监听与开发服务器
# ══════════════════════════════════════════════════════════════════════
def watch_directory(directory: str, on_change: Callable, interval: float = 1.0) -> threading.Event:
    """后台轮询监听目录文件变化,触发 on_change(changed_path)。
    返回一个 Event,set() 即可停止监听。"""
    stop = threading.Event()
    seen: Dict[str, float] = {}

    def scan():
        while not stop.is_set():
            try:
                for root, _dirs, files in os.walk(directory):
                    for fn in files:
                        full = os.path.join(root, fn)
                        try:
                            mtime = os.path.getmtime(full)
                        except OSError:
                            continue
                        if full in seen and seen[full] != mtime:
                            on_change(full)
                        seen[full] = mtime
            except Exception:
                pass
            stop.wait(interval)

    threading.Thread(target=scan, daemon=True).start()
    return stop


def dev_server(app: App, port: int = 8080, host: str = "127.0.0.1") -> Dict[str, Any]:
    """开发模式:启动应用并在源码变化时提示重启(此处仅启动+打印)。"""
    info = app.run(port=port, host=host)
    print("[aurora dev] watching for changes at %s" % info.get("url"))
    return info


# ══════════════════════════════════════════════════════════════════════
# CLI 脚手架:aurora new webapp <name>
# ══════════════════════════════════════════════════════════════════════
_MAIN_AUR = '''// {name} —— Aurora v3.2.0 Web 应用
use std.web;

let app = App("{name}");

app.get("/") = |req| {{
    return Response.html("<h1>Hello from {name}!</h1>");
}}

app.get("/api/hello") = |req| {{
    return Response.json({{ msg: "hello", path: req.path }});
}}

app.run(8080);
std.web.wait();
'''

_AURORA_TOML = '''[project]
name = "{name}"
version = "0.1.0"
aurora = ">=3.2.0"

[dependencies]

[scripts]
dev = "aurora run main.aur"
'''


def _scaffold_webapp(args) -> None:
    """`aurora new webapp <name>`:生成后端脚手架。"""
    name = getattr(args, "name", "myapp")
    root = os.path.join(os.getcwd(), name)
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "main.aur"), "w", encoding="utf-8") as f:
        f.write(_MAIN_AUR.format(name=name))
    with open(os.path.join(root, "aurora.toml"), "w", encoding="utf-8") as f:
        f.write(_AURORA_TOML.format(name=name))
    print("Created Aurora webapp '%s' at %s" % (name, root))


def register_cli(subparsers) -> None:
    """向 CLI 的 subparsers 注册 `aurora new webapp <name>` 命令。"""
    try:
        p = subparsers.add_parser("webapp", help="创建一个 Aurora 全栈 Web 应用")
        p.add_argument("name", help="应用名称")
        p.set_defaults(func=_scaffold_webapp)
    except Exception:
        # subparsers 结构未知时静默退化,不影响主流程
        pass


# ══════════════════════════════════════════════════════════════════════
# 标准库注册入口
# ══════════════════════════════════════════════════════════════════════
STDLIB_REGISTRATION = {
    'std.web': {
        'Router': Router,
        'App': App,
        'Request': Request,
        'Response': Response,
        'Middleware': Middleware,
        'WebSocket': WebSocket,
        'Static': Static,
        'Session': Session,
        'Component': Component,
        'VNode': VNode,
        'create_element': create_element,
        'reactive': reactive,
        'ref': ref,
        'computed': computed,
        'css': css,
        'define_types': define_types,
        'generate_client': generate_client,
        'render_server': render_server,
        'logger_middleware': logger_middleware,
        'cors_middleware': cors_middleware,
        # 附加导出(增强)
        'apply_middleware': apply_middleware,
        'auth_middleware': auth_middleware,
        'compress_middleware': compress_middleware,
        'rate_limit_middleware': rate_limit_middleware,
        'diff': diff,
        'patch': patch,
        'render_to_string': render_to_string,
        'watch': watch,
        'keyframes': keyframes,
        'inject_styles': inject_styles,
        'generate_typescript': generate_typescript,
        'generate_aurora': generate_aurora,
        'hydrate_script': hydrate_script,
        'dev_server': dev_server,
        'MemorySessionStore': MemorySessionStore,
        'CookieSessionStore': CookieSessionStore,
        'register_cli': register_cli,
    }
}
