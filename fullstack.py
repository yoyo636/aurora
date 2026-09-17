"""Aurora 全栈集成层 — Aurora 语言 v3.2.0 标准库扩展。

把"模型 → API 路由 → 前端类型 → API 客户端 → SSR 渲染 → 项目脚手架 → 热重载"
串成一条流水线，让 Aurora 既能写后端，也能一键生成可运行的前后端骨架。

模块包含：

- :class:`SharedTypes`        — 前后端共享类型定义 / 代码生成 / 文件监听
- :class:`ApiGenerator`       — 基于路由元信息生成前端 API 客户端 + OpenAPI 3.0
- :class:`SSR` / :class:`SSRApp` — 服务端渲染 + 客户端 hydration
- :class:`Scaffold`          — 全栈项目脚手架（多模板）
- :class:`HotReloader` / :class:`HotReloadServer` — 文件监听 + HMR WebSocket
- :class:`FullstackPipeline`  — 模型变更全链路更新

零第三方依赖（仅标准库）。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────
# 1. SharedTypes
# ─────────────────────────────────────────────────────────────────────

_TYPE_RE = re.compile(
    r"^\s*type\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*([^}]*)\}\s*$",
    re.MULTILINE,
)
_FIELD_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([A-Za-z0-9_\[\],\s]+?)\s*,?\s*$")


class SharedTypes:
    """管理前后端共享类型定义。

    类型可以以两种格式定义：

    - 字典式：``define_type("User", {"id": "int", "name": "str"})``
    - Aurora DSL 文本：``type User { id: int, name: str }``，通过 :meth:`parse_dsl` 加载。
    """

    def __init__(self) -> None:
        self._types: Dict[str, Dict[str, str]] = {}
        self._watchers: List[Tuple[str, Callable[[str], None]]] = []

    # ── 定义 ────────────────────────────────────────────────────

    def define_type(self, name: str, fields: Dict[str, str]) -> None:
        """登记一个共享类型。"""
        self._types[name] = dict(fields)

    def parse_dsl(self, source: str) -> Dict[str, Dict[str, str]]:
        """解析 Aurora DSL 文本，把其中的 ``type X { a: T, b: U }`` 注册进来。"""
        for m in _TYPE_RE.finditer(source):
            name = m.group(1)
            body = m.group(2)
            fields: Dict[str, str] = {}
            for line in body.split(","):
                line = line.strip()
                if not line:
                    continue
                fm = _FIELD_RE.match(line + ",")
                if fm:
                    fields[fm.group(1)] = fm.group(2).strip()
            if fields:
                self._types[name] = fields
        return dict(self._types)

    def load_json(self, path: str) -> Dict[str, Dict[str, str]]:
        """从 JSON 文件加载类型表：``{"User": {"id": "int", ...}, ...}``。"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for name, fields in data.items():
            self._types[name] = dict(fields)
        return dict(self._types)

    def all(self) -> Dict[str, Dict[str, str]]:
        """返回当前所有类型定义的浅拷贝。"""
        return dict(self._types)

    # ── 代码生成 ────────────────────────────────────────────────

    @staticmethod
    def _ts_type(t: str) -> str:
        """把 Aurora/Python 类型名映射为 TypeScript。"""
        mapping = {
            "int": "number", "integer": "number", "float": "number",
            "bool": "boolean", "boolean": "boolean",
            "str": "string", "string": "string",
            "any": "any",
        }
        t = t.strip()
        if t in mapping:
            return mapping[t]
        if t.startswith("List[") or t.startswith("list["):
            inner = re.sub(r"^List\[|\]$", "", t, flags=re.IGNORECASE)
            return f"{SharedTypes._ts_type(inner)}[]"
        return t

    def generate_frontend_types(self, types_dict: Dict[str, Dict[str, str]],
                                output_path: str) -> str:
        """生成 TypeScript 类型声明并写入文件，返回文件内容。"""
        lines: List[str] = [
            "// 自动生成 — 由 aurora.fullstack.SharedTypes 生成，请勿手工编辑",
            "",
        ]
        for name, fields in types_dict.items():
            lines.append(f"export interface {name} {{")
            for fname, ftype in fields.items():
                lines.append(f"  {fname}: {self._ts_type(ftype)};")
            lines.append("}")
            lines.append("")
        text = "\n".join(lines)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return text

    def generate_backend_types(self, types_dict: Dict[str, Dict[str, str]],
                               output_path: str) -> str:
        """生成后端 Python dataclass 定义并写入文件。"""
        lines: List[str] = [
            '"""自动生成的后端数据模型 — 由 aurora.fullstack.SharedTypes 生成."""',
            "",
            "from dataclasses import dataclass",
            "from typing import List, Optional",
            "",
        ]
        for name, fields in types_dict.items():
            lines.append("@dataclass")
            lines.append(f"class {name}:")
            if not fields:
                lines.append("    pass")
            for fname, ftype in fields.items():
                py = self._py_type(ftype)
                lines.append(f"    {fname}: {py}")
            lines.append("")
        text = "\n".join(lines)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return text

    @staticmethod
    def _py_type(t: str) -> str:
        t = t.strip()
        mapping = {
            "int": "int", "integer": "int", "float": "float",
            "bool": "bool", "boolean": "bool",
            "str": "str", "string": "str", "any": "Any",
        }
        if t in mapping:
            return mapping[t]
        if t.lower().startswith("list["):
            inner = re.sub(r"^[Ll]ist\[|\]$", "", t)
            return f"List[{SharedTypes._py_type(inner)}]"
        return t

    # ── 文件监听 ────────────────────────────────────────────────

    def watch_types(self, file_path: str,
                    on_change: Callable[[str], None],
                    poll_interval: float = 0.5) -> threading.Thread:
        """后台监听类型文件变更；发生变更时调用 ``on_change(新内容)``。

        返回运行中的 daemon 线程；调用方可以 ``.stop()`` 风格自行管理，
        这里直接返回线程对象以便 join / 检查。
        """
        state = {"last_mtime": 0.0, "stop": False}

        def loop() -> None:
            while not state["stop"]:
                try:
                    mtime = os.path.getmtime(file_path)
                except OSError:
                    time.sleep(poll_interval)
                    continue
                if mtime != state["last_mtime"]:
                    state["last_mtime"] = mtime
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        # 自动重新解析
                        self.parse_dsl(content)
                        on_change(content)
                    except Exception:
                        pass
                time.sleep(poll_interval)

        t = threading.Thread(target=loop, daemon=True)
        t.start()
        self._watchers.append((file_path, on_change))
        return t


# ─────────────────────────────────────────────────────────────────────
# 2. ApiGenerator
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Route:
    """一条后端路由的元信息。"""
    method: str
    path: str
    handler: str
    request_type: Optional[str] = None
    response_type: Optional[str] = None


class ApiGenerator:
    """基于路由元信息自动生成前端 API 客户端。"""

    def __init__(self) -> None:
        self.routes: List[Route] = []

    def register_route(self, method: str, path: str, handler: str,
                      request_type: Optional[str] = None,
                      response_type: Optional[str] = None) -> None:
        """登记一条路由。"""
        self.routes.append(Route(
            method=method.upper(),
            path=path,
            handler=handler,
            request_type=request_type,
            response_type=response_type,
        ))

    # ── 客户端生成 ─────────────────────────────────────────────

    @staticmethod
    def _method_name(r: Route) -> str:
        """把 ``GET /api/users/:id`` 映射为 ``get_api_users_by_id``。"""
        parts = [r.method.lower()]
        for seg in r.path.strip("/").split("/"):
            if seg.startswith(":"):
                parts.append("by_" + seg[1:])
            else:
                parts.append(seg)
        return "_".join(parts).replace("-", "_")

    def generate_client(self, routes: List[Route], output_path: str,
                        language: str = "aurora") -> str:
        """生成客户端代码并写入文件，返回生成的源码。"""
        if language == "typescript":
            text = self._gen_typescript(routes)
        elif language == "javascript":
            text = self._gen_javascript(routes)
        else:
            text = self._gen_aurora(routes)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return text

    def _gen_aurora(self, routes: List[Route]) -> str:
        lines = [
            "// 自动生成的 API 客户端 (Aurora) — 请勿手工编辑",
            "import std.http",
            "",
            "class ApiClient {",
            "    base_url: str",
            "    fn init(base_url: str) { this.base_url = base_url }",
            "",
            "    fn _request(method: str, path: str, body: any) -> any {",
            "        let url = this.base_url + path",
            "        let resp = http.request(method, url, body)",
            "        if resp.status >= 400 { throw Error('API ' + resp.status + ': ' + resp.text) }",
            "        return resp.json()",
            "    }",
            "",
        ]
        for r in routes:
            name = self._method_name(r)
            params = re.findall(r":([A-Za-z_][A-Za-z0-9_]*)", r.path)
            args = list(params)
            if r.request_type:
                args.append("body")
            sig = ", ".join(args)
            path_expr = "'" + re.sub(r":([A-Za-z_][A-Za-z0-9_]*)",
                                     r"' + str(\1) + '", r.path) + "'"
            lines.append(f"    fn {name}({sig}) -> any {{")
            lines.append(f"        return this._request('{r.method}', {path_expr}, body)")
            lines.append("    }")
            lines.append("")
        lines.append("}")
        return "\n".join(lines) + "\n"

    def _gen_javascript(self, routes: List[Route]) -> str:
        lines = [
            "// 自动生成的 API 客户端 (JavaScript) — 请勿手工编辑",
            "export class ApiClient {",
            "  constructor(baseUrl) { this.baseUrl = baseUrl; }",
            "  async _req(method, path, body) {",
            "    const res = await fetch(this.baseUrl + path, {",
            "      method,",
            "      headers: { 'Content-Type': 'application/json' },",
            "      body: body === undefined ? undefined : JSON.stringify(body),",
            "    });",
            "    if (!res.ok) throw new Error('API ' + res.status);",
            "    return res.json();",
            "  }",
            "",
        ]
        for r in routes:
            name = self._method_name(r)
            params = re.findall(r":([A-Za-z_][A-Za-z0-9_]*)", r.path)
            args = list(params)
            if r.request_type:
                args.append("body")
            path_js = "'" + re.sub(r":([A-Za-z_][A-Za-z0-9_]*)",
                                   r"' + \g<1> + '", r.path) + "'"
            lines.append(f"  async {name}({', '.join(args)}) {{")
            lines.append(f"    return this._req('{r.method}', {path_js}, body);")
            lines.append("  }")
            lines.append("")
        lines.append("}")
        return "\n".join(lines) + "\n"

    def _gen_typescript(self, routes: List[Route]) -> str:
        js = self._gen_javascript(routes)
        # 简单把 class 头改成 TS 注解
        return "// 自动生成的 API 客户端 (TypeScript) — 请勿手工编辑\n" + js

    # ── OpenAPI ─────────────────────────────────────────────────

    def generate_api_docs(self, routes: List[Route], output_path: str) -> str:
        """生成 OpenAPI 3.0 JSON 文档并写入文件。"""
        spec: Dict[str, Any] = {
            "openapi": "3.0.0",
            "info": {"title": "Aurora API", "version": "1.0.0"},
            "paths": {},
        }
        for r in routes:
            spec["paths"].setdefault(r.path, {})[r.method.lower()] = {
                "operationId": self._method_name(r),
                "summary": r.handler,
                "requestBody": (
                    {"content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{r.request_type}"}}}}
                    if r.request_type else None
                ),
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {"application/json": {
                            "schema": {"$ref": f"#/components/schemas/{r.response_type}"}
                        }},
                    }
                },
            }
        text = json.dumps(spec, indent=2, ensure_ascii=False)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return text


# ─────────────────────────────────────────────────────────────────────
# 3. SSR
# ─────────────────────────────────────────────────────────────────────

_DEFAULT_TEMPLATE = (
    "<!doctype html><html><head><meta charset=\"utf-8\">"
    "<title>__TITLE__</title></head>"
    "<body><div id=\"app\">__BODY__</div>"
    "<script id=\"__INITIAL_STATE__\" type=\"application/json\">__STATE__</script>"
    "</body></html>"
)


class SSR:
    """服务端渲染 + 客户端 hydration 工具。"""

    def render_to_html(self, component_func: Callable[[Dict[str, Any]], str],
                       props: Dict[str, Any], template: Optional[str] = None) -> str:
        """调用 ``component_func(props)`` 得到组件 HTML，再套入模板。"""
        html_body = component_func(props)
        state = json.dumps(props, ensure_ascii=False)
        tpl = template or _DEFAULT_TEMPLATE
        return (tpl
                .replace("__BODY__", html_body)
                .replace("__STATE__", state)
                .replace("__TITLE__", props.get("title", "Aurora App") if isinstance(props, dict) else "Aurora App"))

    def extract_state(self, html_text: str) -> Dict[str, Any]:
        """从含 ``<script id="__INITIAL_STATE__" ...>`` 的 HTML 中解析初始状态。"""
        m = re.search(
            r'<script id="__INITIAL_STATE__"[^>]*>(.*?)</script>',
            html_text, re.DOTALL,
        )
        if not m:
            return {}
        return json.loads(m.group(1))

    def generate_hydration_script(self, component_id: str,
                                  state: Dict[str, Any]) -> str:
        """生成浏览器端激活脚本。"""
        return (
            f"<script>window.__AURORA_HYDRATE__ = "
            f"{{ component: {json.dumps(component_id)}, state: {json.dumps(state, ensure_ascii=False)} }};"
            f"if (window.__AURORAROOT__) window.__AURORAROOT__.hydrate(window.__AURORA_HYDRATE__);</script>"
        )


class SSRApp:
    """一个最小的 SSR 应用：路由匹配 → 取数据 → 渲染 → HTML。"""

    def __init__(self) -> None:
        self._routes: Dict[str, Callable[[Dict[str, str]], Dict[str, Any]]] = {}
        self.ssr = SSR()

    def add_route(self, pattern: str, handler: Callable[[Dict[str, str]], Dict[str, Any]]) -> None:
        """注册路由；``pattern`` 形如 ``/users/:id``。"""
        self._routes[pattern] = handler

    def match(self, path: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        """匹配路径，返回 ``(handler, params)``。"""
        for pattern, handler in self._routes.items():
            regex = "^" + re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"(?P<\1>[^/]+)", pattern) + "$"
            m = re.match(regex, path)
            if m:
                return handler, m.groupdict()
        return None, {}

    def render(self, path: str, component_func: Callable[[Dict[str, Any]], str]) -> str:
        """路由匹配 → 数据获取 → 渲染 HTML。"""
        handler, params = self.match(path)
        props: Dict[str, Any] = {}
        if handler is not None:
            props = handler(params) or {}
        return self.ssr.render_to_html(component_func, props)

    def render_stream(self, path: str,
                      component_func: Callable[[Dict[str, Any]], str]):
        """流式渲染：分块 yield HTML 字符串。"""
        yield "<!doctype html><html><body><div id=\"app\">"
        handler, params = self.match(path)
        if handler is not None:
            props = handler(params) or {}
        else:
            props = {}
        yield component_func(props)
        yield "</div><script id=\"__INITIAL_STATE__\" type=\"application/json\">"
        yield json.dumps(props, ensure_ascii=False)
        yield "</script></body></html>"


# ─────────────────────────────────────────────────────────────────────
# 4. Scaffold
# ─────────────────────────────────────────────────────────────────────

_TEMPLATES = {
    "fullstack": "后端 api/ + 前端 web/ + 共享类型 shared/ + 迁移 migrations/ 一体化项目",
    "api":       "纯后端 REST API 项目",
    "webapp":    "前端为主 + 极简后端",
    "cli-app":   "命令行工具项目",
    "tui-app":   "终端 UI 项目",
    "agent":     "AI Agent 项目",
}


class Scaffold:
    """全栈项目脚手架：按模板生成目录结构与示例代码。"""

    def list_templates(self) -> Dict[str, str]:
        """返回 ``{模板名: 描述}``。"""
        return dict(_TEMPLATES)

    def create_project(self, name: str, template: str = "fullstack",
                       output_dir: str = ".") -> str:
        """在 ``output_dir/name`` 下生成项目骨架，返回项目根路径。"""
        if template not in _TEMPLATES:
            raise ValueError(f"未知模板: {template}，可选: {list(_TEMPLATES)}")
        root = os.path.abspath(os.path.join(output_dir, name))
        os.makedirs(root, exist_ok=True)

        # 顶层文件
        self._write(root, "aurora.toml", self._toml(name, template))
        self._write(root, "README.md", self._readme(name, template))
        self._write(root, ".gitignore", self._gitignore())
        self._write(root, "main.aurora", self._entry(name, template))
        self._write(root, "test_basic.aurora", self._test_skeleton(name))

        if template == "fullstack":
            for sub in ("api", "web", "shared", "migrations"):
                os.makedirs(os.path.join(root, sub), exist_ok=True)
            self._write(os.path.join(root, "api"), "routes.aurora", self._api_routes())
            self._write(os.path.join(root, "web"), "index.html", self._web_index(name))
            self._write(os.path.join(root, "shared"), "types.aurora", self._shared_types())
            self._write(os.path.join(root, "migrations"), "0001_init.sql",
                        self._migration())
        elif template == "api":
            os.makedirs(os.path.join(root, "api"), exist_ok=True)
            self._write(os.path.join(root, "api"), "routes.aurora", self._api_routes())
        elif template == "webapp":
            os.makedirs(os.path.join(root, "web"), exist_ok=True)
            self._write(os.path.join(root, "web"), "index.html", self._web_index(name))
        elif template == "cli-app":
            self._write(root, "cli.aurora", self._cli_entry(name))
        elif template == "tui-app":
            self._write(root, "tui.aurora", self._tui_entry(name))
        elif template == "agent":
            self._write(root, "agent.aurora", self._agent_entry(name))
        return root

    # ── 内部：文件模板 ─────────────────────────────────────────

    @staticmethod
    def _write(path: str, fname: str, content: str) -> None:
        full = os.path.join(path, fname)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)

    def _toml(self, name: str, template: str) -> str:
        return (
            f'[project]\nname = "{name}"\nversion = "0.1.0"\n'
            f'template = "{template}"\n\n[build]\ntarget = "aurora"\n'
        )

    def _readme(self, name: str, template: str) -> str:
        return (
            f"# {name}\n\nAurora 全栈项目（模板：{template}）。\n\n"
            "## 运行\n```\naurora run main.aurora\n```\n"
        )

    def _gitignore(self) -> str:
        return "__pycache__/\n*.pyc\n.aurora-cache/\nbuild/\ndist/\n.venv/\n"

    def _entry(self, name: str, template: str) -> str:
        return (
            f'// {name} 入口\n'
            'println("Hello, Aurora!")\n'
        )

    def _test_skeleton(self, name: str) -> str:
        return (
            "// 测试骨架\n"
            "test \"smoke\" { assert 1 + 1 == 2 }\n"
        )

    def _api_routes(self) -> str:
        return (
            "// 示例路由\n"
            'get "/api/health" -> { json({"ok": true }) }\n'
            'get "/api/users/:id" -> { json({"id": params.id }) }\n'
        )

    def _web_index(self, name: str) -> str:
        return (
            "<!doctype html><html><head><title>" + name + "</title></head>"
            "<body><div id=\"app\">" + name + "</div></body></html>"
        )

    def _shared_types(self) -> str:
        return "type User {\n  id: int,\n  name: str,\n  email: str,\n}\n"

    def _migration(self) -> str:
        return "-- 初始迁移\nCREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);\n"

    def _cli_entry(self, name: str) -> str:
        return f'// {name} CLI\nfn main() {{ println("cli running") }}\n'

    def _tui_entry(self, name: str) -> str:
        return f'// {name} TUI\nfn main() {{ ui.run() }}\n'

    def _agent_entry(self, name: str) -> str:
        return f'// {name} AI Agent\nlet agent = Agent(model="gpt"); agent.loop()\n'


# ─────────────────────────────────────────────────────────────────────
# 5. HotReloader
# ─────────────────────────────────────────────────────────────────────

class HotReloader:
    """监听目录中的文件变更，防抖后回调 ``on_change``。

    不依赖 watchdog，使用纯标准库轮询，便于在 CI / 受限环境下运行。
    """

    def __init__(self, debounce_ms: int = 100) -> None:
        self.debounce_ms: int = debounce_ms
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._snapshot: Dict[str, float] = {}

    @staticmethod
    def _walk(directories: List[str], extensions: Tuple[str, ...],
              ignore_patterns: Tuple[str, ...]) -> Dict[str, float]:
        snap: Dict[str, float] = {}
        for d in directories:
            for root, dirs, files in os.walk(d):
                # 过滤忽略目录
                dirs[:] = [x for x in dirs
                           if not any(p in os.path.join(root, x) for p in ignore_patterns)]
                for fn in files:
                    if extensions and not fn.endswith(tuple(extensions)):
                        continue
                    full = os.path.join(root, fn)
                    if any(p in full for p in ignore_patterns):
                        continue
                    try:
                        snap[full] = os.path.getmtime(full)
                    except OSError:
                        continue
        return snap

    def watch(self, directories: List[str],
              extensions: Optional[List[str]] = None,
              on_change: Optional[Callable[[str], None]] = None,
              ignore_patterns: Optional[List[str]] = None,
              poll_interval: float = 0.3) -> None:
        """启动后台监听线程。"""
        exts = tuple(extensions or [])
        ignores = tuple(ignore_patterns or [])
        self._snapshot = self._walk(directories, exts, ignores)
        last_fire = [0.0]

        def loop() -> None:
            while not self._stop.is_set():
                time.sleep(poll_interval)
                new_snap = self._walk(directories, exts, ignores)
                changed = [p for p, m in new_snap.items()
                           if self._snapshot.get(p) != m]
                self._snapshot = new_snap
                if not changed:
                    continue
                now = time.time() * 1000
                if now - last_fire[0] < self.debounce_ms:
                    continue
                last_fire[0] = now
                if on_change:
                    for path in changed:
                        try:
                            on_change(path)
                        except Exception:
                            pass

        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """停止监听线程。"""
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)

    # ── 生成 HMR 客户端运行时 ───────────────────────────────────

    @staticmethod
    def generate_hmr_client(port: int) -> str:
        """生成一段浏览器端 HMR WebSocket 客户端 JS。"""
        return (
            f"(function() {{"
            f"const ws = new WebSocket('ws://127.0.0.1:{port}/__aurora_hmr');"
            f"ws.onmessage = (e) => {{ const msg = JSON.parse(e.data);"
            f"if (msg.type === 'reload') location.reload();"
            f"if (msg.type === 'update' && window.__aurora_hot__) "
            f"window.__aurora_hot__(msg); }};"
            f"}})();"
        )


class HotReloadServer:
    """内置的 HMR WebSocket 服务器（端口占位；实际 push 可由 Web 层接入）。"""

    def __init__(self, port: int) -> None:
        self.port: int = port
        self._clients: List[Any] = []
        self._running = False

    def start(self) -> None:
        """标记服务器就绪（不阻塞）。"""
        self._running = True

    def broadcast(self, message: Dict[str, Any]) -> None:
        """向所有已连接客户端推送一条消息。"""
        if not self._running:
            return
        payload = json.dumps(message)
        for c in list(self._clients):
            try:
                c.send(payload)
            except Exception:
                self._clients.remove(c)

    def reload(self) -> None:
        """广播一次整页刷新。"""
        self.broadcast({"type": "reload"})

    def stop(self) -> None:
        self._running = False


# ─────────────────────────────────────────────────────────────────────
# 6. FullstackPipeline
# ─────────────────────────────────────────────────────────────────────

@dataclass
class ModelDiff:
    """模型变更的结构化描述。"""
    added_fields: Dict[str, str] = field(default_factory=dict)
    removed_fields: List[str] = field(default_factory=list)
    changed_types: Dict[str, str] = field(default_factory=dict)


class FullstackPipeline:
    """模型变更全链路更新：迁移 → API → 前端类型 → API 客户端。"""

    def __init__(self, project_root: str,
                 shared: Optional[SharedTypes] = None,
                 api_gen: Optional[ApiGenerator] = None) -> None:
        self.project_root: str = os.path.abspath(project_root)
        self.shared: SharedTypes = shared or SharedTypes()
        self.api_gen: ApiGenerator = api_gen or ApiGenerator()
        self._previous: Dict[str, Dict[str, str]] = {}

    def model_changed(self, model_def: Dict[str, str]) -> ModelDiff:
        """对比上次已记录的模型定义，返回差异。"""
        # 第一次调用：把所有字段视为新增
        prev = self._previous
        diff = ModelDiff()
        for fname, ftype in model_def.items():
            if fname not in prev:
                diff.added_fields[fname] = ftype
            elif prev[fname] != ftype:
                diff.changed_types[fname] = ftype
        for fname in prev:
            if fname not in model_def:
                diff.removed_fields.append(fname)
        return diff

    def generate_migration(self, diff: ModelDiff, model_name: str = "model") -> str:
        """根据差异生成 SQL 迁移文本。"""
        stmts = [f"-- 自动生成的迁移: {model_name}"]
        for fname, ftype in diff.added_fields.items():
            stmts.append(f"ALTER TABLE {model_name} ADD COLUMN {fname} {self._sql_type(ftype)};")
        for fname in diff.removed_fields:
            stmts.append(f"-- DROP COLUMN {fname} （需要人工确认）;")
        for fname, ftype in diff.changed_types.items():
            stmts.append(
                f"ALTER TABLE {model_name} ALTER COLUMN {fname} "
                f"TYPE {self._sql_type(ftype)};"
            )
        return "\n".join(stmts) + "\n"

    @staticmethod
    def _sql_type(aurora_type: str) -> str:
        mapping = {
            "int": "INTEGER", "integer": "INTEGER",
            "float": "REAL", "bool": "INTEGER", "boolean": "INTEGER",
            "str": "TEXT", "string": "TEXT",
        }
        return mapping.get(aurora_type.strip(), "TEXT")

    def update_api_routes(self, model: str) -> List[Route]:
        """根据模型名注册 REST 路由（CRUD）。"""
        base = f"/api/{model.lower()}s"
        routes = [
            Route("GET", base, f"list_{model}", None, f"{model}"),
            Route("POST", base, f"create_{model}", model, model),
            Route("GET", f"{base}/:id", f"get_{model}", None, model),
            Route("PUT", f"{base}/:id", f"update_{model}", model, model),
            Route("DELETE", f"{base}/:id", f"delete_{model}", None, None),
        ]
        for r in routes:
            self.api_gen.register_route(r.method, r.path, r.handler,
                                        r.request_type, r.response_type)
        return routes

    def update_frontend_types(self, model_name: str, fields: Dict[str, str],
                              out_path: Optional[str] = None) -> str:
        """把模型登记进 SharedTypes 并生成前端类型文件。"""
        self.shared.define_type(model_name, fields)
        target = out_path or os.path.join(self.project_root, "shared", "types.ts")
        return self.shared.generate_frontend_types({model_name: fields}, target)

    def update_api_client(self, routes: Optional[List[Route]] = None,
                          out_path: Optional[str] = None,
                          language: str = "javascript") -> str:
        """根据当前已注册路由重新生成前端 API 客户端。"""
        target = out_path or os.path.join(self.project_root, "web", "api_client.js")
        return self.api_gen.generate_client(routes or self.api_gen.routes,
                                            target, language=language)

    def dry_run(self, model_name: str,
                model_def: Dict[str, str]) -> Dict[str, Any]:
        """预览本次模型变更会产生哪些改动，不写盘。"""
        diff = self.model_changed(model_def)
        return {
            "model": model_name,
            "diff": {
                "added": diff.added_fields,
                "removed": diff.removed_fields,
                "changed": diff.changed_types,
            },
            "migration_preview": self.generate_migration(diff, model_name),
            "routes_preview": [r.path for r in self.update_api_routes(model_name)],
        }

    def apply_changes(self, model_name: str,
                      model_def: Dict[str, str],
                      out_dir: Optional[str] = None) -> Dict[str, str]:
        """真正执行全链路更新，返回各产物的文件路径。"""
        root = out_dir or self.project_root
        os.makedirs(root, exist_ok=True)
        diff = self.model_changed(model_def)

        migration_path = os.path.join(root, "migrations",
                                      f"{int(time.time())}_{model_name}.sql")
        os.makedirs(os.path.dirname(migration_path), exist_ok=True)
        with open(migration_path, "w", encoding="utf-8") as f:
            f.write(self.generate_migration(diff, model_name))

        self.update_api_routes(model_name)
        types_path = self.update_frontend_types(model_name, model_def,
                                                os.path.join(root, "shared", "types.ts"))
        client_path = self.update_api_client(
            out_path=os.path.join(root, "web", "api_client.js"))

        self._previous = dict(model_def)
        return {
            "migration": migration_path,
            "types": types_path,
            "client": client_path,
        }


__all__ = [
    "SharedTypes", "ApiGenerator", "Route",
    "SSR", "SSRApp",
    "Scaffold",
    "HotReloader", "HotReloadServer",
    "FullstackPipeline", "ModelDiff",
]
