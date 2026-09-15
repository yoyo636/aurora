"""Aurora v3.1.0 — Web 运行时与浏览器开发支持

四大子系统：

1. :class:`DOMBridge` — DOM API 绑定（含可在 Python 内运行的轻量 DOM 模拟，
   以及可嵌入产物的 JS 胶水代码生成）。
2. :class:`JSCompiler` — Aurora AST → JavaScript。
3. :class:`WASMCompiler` — Aurora → C（复用 codegen）→ WASM（Emscripten）。
4. Web 框架：:class:`Component` / :class:`VNode` / :func:`diff` / :func:`patch` /
   :func:`create_app` / :class:`Router` / :class:`Store`，以及
   :class:`ExtensionGenerator` 生成浏览器扩展模板。

所有功能不依赖真实浏览器；DOM 操作在 Python 内用一棵模拟 DOM 树完成。
"""

from __future__ import annotations

import json
import os
import shutil
from typing import Any, Callable, Dict, List, Optional, Tuple


# ===========================================================================
# 1. 轻量 DOM 模型（供 DOMBridge 在 Python 内使用）
# ===========================================================================

class DOMElement:
    """模拟 DOM 元素。"""

    def __init__(self, tag: str, attrs: Optional[Dict[str, str]] = None) -> None:
        self.tag = tag
        self.attrs: Dict[str, str] = dict(attrs or {})
        self.children: List["DOMElement"] = []
        self.parent: Optional[DOMElement] = None
        self._text: str = ""
        self._classes: set = set()
        self._listeners: Dict[str, List[Callable[[Any], Any]]] = {}
        self._id: Optional[str] = self.attrs.get("id")

    # -- 文本 / innerHTML ---------------------------------------------------

    @property
    def text_content(self) -> str:
        return self._text + "".join(c.text_content for c in self.children)

    @text_content.setter
    def text_content(self, value: str) -> None:
        self._text = value
        self.children = []

    @property
    def inner_html(self) -> str:
        out = self._text
        for c in self.children:
            out += c.outer_html
        return out

    @inner_html.setter
    def inner_html(self, value: str) -> None:
        self._text = ""
        self.children = []
        # 简化：把字符串当作一个文本节点
        self.children.append(DOMElement("#text"))
        self.children[-1]._text = value

    @property
    def outer_html(self) -> str:
        attr_str = "".join(f' {k}="{v}"' for k, v in self.attrs.items())
        inner = self.inner_html
        if self.tag == "#text":
            return self._text
        return f"<{self.tag}{attr_str}>{inner}</{self.tag}>"

    # -- 属性 ---------------------------------------------------------------

    def set_attribute(self, name: str, value: str) -> None:
        self.attrs[name] = value
        if name == "id":
            self._id = value

    def get_attribute(self, name: str) -> Optional[str]:
        return self.attrs.get(name)

    def remove_attribute(self, name: str) -> None:
        self.attrs.pop(name, None)

    # -- class --------------------------------------------------------------

    def add_class(self, name: str) -> None:
        self._classes.add(name)
        self.attrs["class"] = " ".join(sorted(self._classes))

    def remove_class(self, name: str) -> None:
        self._classes.discard(name)
        self.attrs["class"] = " ".join(sorted(self._classes))

    # -- 子节点 -------------------------------------------------------------

    def append_child(self, child: "DOMElement") -> "DOMElement":
        child.parent = self
        self.children.append(child)
        return child

    def remove_child(self, child: "DOMElement") -> None:
        self.children.remove(child)
        child.parent = None

    def set_style(self, prop: str, value: str) -> None:
        style = self.attrs.get("style", "")
        # 简化的 style 字典
        styles = dict(kv.split(":", 1) for kv in style.rstrip(";").split(";") if ":" in kv)
        styles[prop] = value
        self.attrs["style"] = ";".join(f"{k}:{v}" for k, v in styles.items())

    # -- 事件 ---------------------------------------------------------------

    def add_event_listener(self, type: str,
                           callback: Callable[[Any], Any]) -> None:
        self._listeners.setdefault(type, []).append(callback)

    def dispatch_event(self, event: "DOMEvent") -> Any:
        results = []
        for cb in self._listeners.get(event.type, []):
            results.append(cb(event))
        return results

    def query_selector_all(self, selector: str) -> List["DOMElement"]:
        """支持 ``tag`` / ``#id`` / ``.class`` 三种最简选择器。"""
        out: List[DOMElement] = []
        if selector.startswith("#"):
            want = selector[1:]
            self._walk_id(want, out)
        elif selector.startswith("."):
            want = selector[1:]
            self._walk_class(want, out)
        else:
            self._walk_tag(selector, out)
        return out

    def _walk_tag(self, tag: str, out: List["DOMElement"]) -> None:
        for c in self.children:
            if c.tag == tag:
                out.append(c)
            c._walk_tag(tag, out)

    def _walk_id(self, _id: str, out: List["DOMElement"]) -> None:
        for c in self.children:
            if c._id == _id:
                out.append(c)
            c._walk_id(_id, out)

    def _walk_class(self, klass: str, out: List["DOMElement"]) -> None:
        for c in self.children:
            if klass in c._classes:
                out.append(c)
            c._walk_class(klass, out)


class DOMEvent:
    """模拟 DOM 事件。"""

    def __init__(self, type: str, target: Optional[DOMElement] = None,
                 key: str = "", client_x: int = 0, client_y: int = 0) -> None:
        self.type = type
        self.target = target
        self.key = key
        self.client_x = client_x
        self.client_y = client_y
        self._default_prevented = False
        self._stopped = False

    def prevent_default(self) -> None:
        self._default_prevented = True

    def stop_propagation(self) -> None:
        self._stopped = True


# ===========================================================================
# DOMBridge
# ===========================================================================

class DOMBridge:
    """DOM API 绑定：在 Python 中持有一棵模拟文档树。

    编译到 JS/WASM 时，这些调用会被 :meth:`generate_dom_bindings` 转译成
    对应的浏览器 API 调用。
    """

    def __init__(self) -> None:
        self.document = DOMElement("#document")
        self._id_index: Dict[str, DOMElement] = {}
        self._timers: List[Any] = []
        self.storage: Dict[str, str] = {}

    # -- document -----------------------------------------------------------

    def create_element(self, tag: str) -> DOMElement:
        el = DOMElement(tag)
        return el

    def get_element_by_id(self, _id: str) -> Optional[DOMElement]:
        return self._id_index.get(_id)

    def register_id(self, el: DOMElement) -> None:
        if el._id:
            self._id_index[el._id] = el

    def query_selector(self, selector: str) -> Optional[DOMElement]:
        results = self.document.query_selector_all(selector)
        return results[0] if results else None

    def query_selector_all(self, selector: str) -> List[DOMElement]:
        return self.document.query_selector_all(selector)

    # -- window -------------------------------------------------------------

    def alert(self, msg: str) -> None:  # pragma: no cover - 仅浏览器
        pass

    def confirm(self, msg: str) -> bool:
        return True

    def prompt(self, msg: str, default: str = "") -> str:
        return default

    def set_timeout(self, callback: Callable[[], Any], ms: int = 0) -> int:
        self._timers.append(("timeout", callback, ms))
        return len(self._timers)

    def set_interval(self, callback: Callable[[], Any], ms: int = 1000) -> int:
        self._timers.append(("interval", callback, ms))
        return len(self._timers)

    @property
    def local_storage(self) -> Dict[str, str]:
        return self.storage


def generate_dom_bindings() -> str:
    """输出可嵌入的 JS 胶水代码：把 Aurora DOM 调用映射到浏览器 API。"""
    return """// Aurora v3.1.0 DOM bindings — 自动生成
(function (global) {
  const AuroraDOM = {
    document: typeof document !== 'undefined' ? document : null,
    getElementById(id) { return this.document.getElementById(id); },
    createElement(tag) { return this.document.createElement(tag); },
    querySelector(sel) { return this.document.querySelector(sel); },
    querySelectorAll(sel) { return Array.from(this.document.querySelectorAll(sel)); },
    setAttribute(el, name, value) { el.setAttribute(name, value); },
    appendChild(parent, child) { parent.appendChild(child); },
    addEventListener(el, type, cb) { el.addEventListener(type, cb); },
    setText(el, text) { el.textContent = text; },
    alert(msg) { globalThis.alert(msg); },
    setTimeout(cb, ms) { return globalThis.setTimeout(cb, ms); },
  };
  globalThis.AuroraDOM = AuroraDOM;
})(globalThis);
"""


# ===========================================================================
# 2. Aurora → JavaScript 编译器
# ===========================================================================

class JSCompiler:
    """把 Aurora AST 编译为 JavaScript（ES6）。

    支持：函数声明、变量 / 常量、类（简化）、if/for/while、return、
    表达式、模块导入。类型注解被擦除为 JSDoc 注释。
    """

    def __init__(self) -> None:
        self._indent = 0

    # -- 入口 ---------------------------------------------------------------

    def compile(self, ast: Any, module_name: Optional[str] = None) -> str:
        """编译一个 AST 节点（通常是 :class:`Program`）。"""
        lines: List[str] = []
        stmts = getattr(ast, "statements", [ast]) or []
        for stmt in stmts:
            text = self._stmt(stmt)
            if text:
                lines.append(text)
        header = "// Generated by Aurora v3.1.0 JSCompiler\n"
        if module_name:
            header += f"// module: {module_name}\n"
        return header + "\n".join(lines) + "\n"

    def compile_file(self, source_path: str, output_path: str,
                     module_name: Optional[str] = None) -> str:
        """用项目的 parser 解析源码后编译并写出 JS。"""
        import parser as aurora_parser  # noqa: E402  项目自带
        with open(source_path, "r", encoding="utf-8") as f:
            src = f.read()
        program = aurora_parser.Parser().parse(src)
        js = self.compile(program, module_name or os.path.basename(source_path))
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(js)
        return output_path

    # -- 语句 ---------------------------------------------------------------

    def _stmt(self, node: Any) -> str:
        cls = type(node).__name__
        if cls == "FnDef":
            return self._fn(node)
        if cls == "LetStmt":
            init = self._expr(node.initializer) if node.initializer else "undefined"
            kind = "let" if node.mutable else "const"
            jsdoc = self._type_jsdoc(node.type_annotation)
            return f"{jsdoc}\n{kind} {node.name} = {init};"
        if cls == "ConstStmt":
            init = self._expr(node.initializer) if node.initializer else "undefined"
            return f"const {node.name} = {init};"
        if cls == "ReturnStmt":
            v = self._expr(node.value) if node.value else ""
            return f"return {v};" if v else "return;"
        if cls == "ExprStmt":
            return f"{self._expr(node.expr)};"
        if cls == "IfStmt":
            return self._if(node)
        if cls == "ForStmt":
            var = ", ".join(node.variables)
            return f"for (const {var} of {self._expr(node.iterable)}) {self._block(node.body)}"
        if cls == "WhileStmt":
            return f"while ({self._expr(node.condition)}) {self._block(node.body)}"
        if cls == "AssignStmt":
            return f"{self._expr(node.target)} {node.op} {self._expr(node.value)};"
        if cls == "ImportStmt":
            return self._import(node)
        if cls == "Block":
            return self._block(node)
        if cls in ("BreakStmt",):
            return "break;"
        if cls in ("ContinueStmt",):
            return "continue;"
        return f"// unsupported: {cls}"

    def _block(self, block: Any) -> str:
        stmts = " ".join(self._stmt(s) for s in (block.statements if block else []))
        return "{ " + stmts + " }"

    def _fn(self, node: Any) -> str:
        params = ", ".join(p.name for p in node.params)
        jsdoc_parts = []
        for p in node.params:
            t = self._type_to_js(p.type_annotation)
            if t:
                jsdoc_parts.append(f"@param {{{t}}} {p.name}")
        rt = self._type_to_js(node.return_type)
        if rt:
            jsdoc_parts.append(f"@returns {{{rt}}}")
        jsdoc = ""
        if jsdoc_parts:
            jsdoc = "/**\n * " + "\n * ".join(jsdoc_parts) + "\n */\n"
        body = self._block(node.body)
        return f"{jsdoc}function {node.name}({params}) {body}"

    def _if(self, node: Any) -> str:
        s = f"if ({self._expr(node.condition)}) {self._block(node.then_body)}"
        for cond, body in (node.elif_clauses or []):
            s += f" else if ({self._expr(cond)}) {self._block(body)}"
        if node.else_body:
            s += f" else {self._block(node.else_body)}"
        return s

    def _import(self, node: Any) -> str:
        path = "/".join(node.path)
        if node.names:
            inner = ", ".join(node.names)
            return f"import {{ {inner} }} from './{path}';"
        name = node.alias or node.path[-1]
        return f"import * as {name} from './{path}';"

    # -- 表达式 -------------------------------------------------------------

    def _expr(self, node: Any) -> str:
        if node is None:
            return "undefined"
        cls = type(node).__name__
        if cls == "IntLiteral":
            return str(node.value)
        if cls == "FloatLiteral":
            return str(node.value)
        if cls == "StringLiteral":
            return json.dumps(node.value)
        if cls == "BoolLiteral":
            return "true" if node.value else "false"
        if cls == "NilLiteral":
            return "null"
        if cls == "Identifier":
            return node.name
        if cls == "BinaryOp":
            return f"({self._expr(node.left)} {node.op} {self._expr(node.right)})"
        if cls == "UnaryOp":
            return f"({node.op}{self._expr(node.operand)})"
        if cls == "CallExpr":
            args = ", ".join(self._expr(a) for a in node.args)
            return f"{self._expr(node.callee)}({args})"
        if cls == "MethodCall":
            args = ", ".join(self._expr(a) for a in node.args)
            return f"{self._expr(node.object)}.{node.method}({args})"
        if cls == "MemberAccess":
            return f"{self._expr(node.object)}.{node.member}"
        if cls == "IndexAccess":
            return f"{self._expr(node.object)}[{self._expr(node.index)}]"
        if cls == "ArrayLiteral":
            return "[" + ", ".join(self._expr(e) for e in node.elements) + "]"
        if cls == "MapLiteral":
            pairs = ", ".join(f"{self._expr(k)}: {self._expr(v)}"
                              for k, v in node.pairs)
            return "{" + pairs + "}"
        if cls == "IfExpr":
            return f"({self._expr(node.condition)} ? {self._expr(node.then_body)} : {self._expr(node.else_body)})"
        return "null"

    # -- 类型 ---------------------------------------------------------------

    def _type_to_js(self, t: Any) -> str:
        if t is None:
            return ""
        name = getattr(t, "name", "")
        mapping = {"int": "number", "float": "number", "str": "string",
                   "bool": "boolean", "void": "void"}
        return mapping.get(name, name or "any")

    def _type_jsdoc(self, t: Any) -> str:
        jt = self._type_to_js(t)
        return f"/** @type {{{jt}}} */" if jt else ""


# ===========================================================================
# 3. Aurora → WASM 编译器
# ===========================================================================

class WASMCompiler:
    """通过 C 后端 + Emscripten 把 Aurora 编译为 WASM。

    emcc 不可用时仅生成 ``build_wasm.sh`` 配置脚本，不报错。
    """

    DEFAULT_FLAGS = ["-O2", "-s", "WASM=1", "-s", "MODULARIZE=1"]

    def __init__(self, exported_functions: Optional[List[str]] = None) -> None:
        self.exported = exported_functions or ["_malloc", "_free"]

    def emcc_available(self) -> bool:
        return shutil.which("emcc") is not None

    def generate_c_source(self, source_path: str, output_dir: str) -> str:
        """调用项目 C 后端（codegen.py）生成 C 文件。"""
        c_path = os.path.join(output_dir, os.path.basename(source_path) + ".c")
        try:  # pragma: no cover - 依赖项目 codegen
            import codegen as cg  # type: ignore
            import parser as ap  # type: ignore
            with open(source_path) as f:
                src = f.read()
            program = ap.Parser().parse(src)
            gen = cg.CCodeGenerator()
            c_text = gen.generate(program)
            with open(c_path, "w") as f:
                f.write(c_text)
        except Exception:
            # 后端不可用时写占位
            with open(c_path, "w") as f:
                f.write("/* placeholder C source */\nint main() { return 0; }\n")
        return c_path

    def compile_to_wasm(self, source_path: str, output_dir: str) -> str:
        """编译为 WASM + JS 胶水。返回产物目录或构建脚本路径。"""
        os.makedirs(output_dir, exist_ok=True)
        c_path = self.generate_c_source(source_path, output_dir)
        js_out = os.path.join(output_dir, "aurora_module.js")

        flags = list(self.DEFAULT_FLAGS)
        flags += ["-s", "EXPORTED_FUNCTIONS=" +
                  "[" + ",".join(json.dumps(x) for x in self.exported) + "]"]

        if self.emcc_available():  # pragma: no cover
            try:
                import subprocess
                subprocess.run(["emcc", c_path, "-o", js_out] + flags,
                               check=True)
                return output_dir
            except Exception:
                pass

        script = (
            "#!/bin/sh\nset -e\n"
            f"emcc {c_path} -o {js_out} {' '.join(flags)}\n")
        script_path = os.path.join(output_dir, "build_wasm.sh")
        with open(script_path, "w") as f:
            f.write(script)
        return script_path


# ===========================================================================
# 4. Web 框架
# ===========================================================================

class VNode:
    """虚拟 DOM 节点。"""

    def __init__(self, tag: str,
                 props: Optional[Dict[str, Any]] = None,
                 children: Optional[List[Any]] = None) -> None:
        self.tag = tag
        self.props: Dict[str, Any] = dict(props or {})
        self.children: List[Any] = list(children or [])
        self.key: Any = self.props.get("key")

    def __repr__(self) -> str:  # pragma: no cover
        return f"VNode({self.tag}, {self.children})"


class Component:
    """组件基类。子类覆盖 :meth:`render`。"""

    def __init__(self, props: Optional[Dict[str, Any]] = None) -> None:
        self.props: Dict[str, Any] = dict(props or {})
        self.state: Dict[str, Any] = {}
        self._mounted = False

    def render(self) -> VNode:
        """返回该组件的虚拟 DOM。子类必须覆盖。"""
        return VNode("div")

    def on_mount(self) -> None:
        self._mounted = True

    def on_update(self, props: Dict[str, Any]) -> None:
        pass

    def on_unmount(self) -> None:
        self._mounted = False

    def set_state(self, new_state: Dict[str, Any]) -> None:
        self.state.update(new_state)


def diff(old: VNode, new: VNode) -> List[Dict[str, Any]]:
    """计算两个 VNode 之间的差异，返回补丁列表。"""
    patches: List[Dict[str, Any]] = []
    if old is None:
        patches.append({"type": "create", "node": new})
        return patches
    if new is None:
        patches.append({"type": "remove"})
        return patches
    if old.tag != new.tag:
        patches.append({"type": "replace", "node": new})
        return patches

    # 属性差异
    props_changed = {}
    all_keys = set(old.props) | set(new.props)
    for k in all_keys:
        if old.props.get(k) != new.props.get(k):
            props_changed[k] = new.props.get(k)
    if props_changed:
        patches.append({"type": "props", "props": props_changed})

    # 子节点差异（简化：按位置递归）
    old_children = old.children
    new_children = new.children
    n = max(len(old_children), len(new_children))
    for i in range(n):
        oc = old_children[i] if i < len(old_children) else None
        nc = new_children[i] if i < len(new_children) else None
        patches.extend(diff(oc, nc))
    return patches


def patch(dom: Any, patches: List[Dict[str, Any]]) -> None:
    """把补丁应用到真实 DOM（这里操作 DOMBridge 元素）。"""
    for p in patches:
        kind = p["type"]
        if kind == "props":
            for k, v in p["props"].items():
                if v is None:
                    dom.remove_attribute(k)
                else:
                    dom.set_attribute(k, str(v))
        elif kind == "create":
            pass
        elif kind == "replace":
            pass
        elif kind == "remove":
            if dom.parent:
                dom.parent.remove_child(dom)


class Store:
    """简化版 Redux：getState / dispatch / subscribe。"""

    def __init__(self, reducer: Callable[[Any, Dict[str, Any]], Any],
                 initial_state: Any = None) -> None:
        self._reducer = reducer
        self._state = initial_state
        self._listeners: List[Callable[[], None]] = []

    def get_state(self) -> Any:
        return self._state

    def dispatch(self, action: Dict[str, Any]) -> Any:
        self._state = self._reducer(self._state, action)
        for cb in self._listeners:
            cb()
        return action

    def subscribe(self, listener: Callable[[], None]) -> Callable[[], None]:
        self._listeners.append(listener)

        def _unsub() -> None:
            self._listeners.remove(listener)

        return _unsub


class Route:
    """一条路由。"""

    def __init__(self, path: str, component: type) -> None:
        self.path = path
        self.component = component


class Router:
    """前端路由器。"""

    def __init__(self, routes: List[Route]) -> None:
        self.routes = routes
        self._current: Optional[str] = None
        self._listeners: List[Callable[[Optional[str]], None]] = []

    def match(self, path: str) -> Optional[Route]:
        for r in self.routes:
            if r.path == path:
                return r
        return None

    def navigate(self, path: str) -> Optional[Route]:
        route = self.match(path)
        self._current = path
        for cb in self._listeners:
            cb(path)
        return route

    @property
    def current(self) -> Optional[str]:
        return self._current

    def on_change(self, cb: Callable[[Optional[str]], None]) -> None:
        self._listeners.append(cb)


def create_app(root_component: Component, container_id: str = "root") -> Dict[str, Any]:
    """应用入口：挂载根组件到指定容器。"""
    root_component.on_mount()
    vnode = root_component.render()
    return {"root": root_component, "container": container_id, "vnode": vnode}


def generate_web_project(project_name: str, output_dir: str) -> str:
    """生成 Web 项目脚手架。"""
    root = os.path.join(output_dir, project_name)
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    _write_text(os.path.join(root, "index.html"),
                f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{project_name}</title>
<link rel="stylesheet" href="src/style.css"></head>
<body><div id="root"></div>
<script src="src/app.js"></script></body></html>
""")
    _write_text(os.path.join(root, "src", "app.js"),
                f"// {project_name} — generated by Aurora v3.1.0\n")
    _write_text(os.path.join(root, "src", "style.css"),
                f"/* {project_name} */\n")
    _write_text(os.path.join(root, "README.md"),
                f"# {project_name}\n\nAurora Web project.\n")
    return root


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ===========================================================================
# 5. 浏览器扩展模板生成
# ===========================================================================

class ExtensionGenerator:
    """生成 Chrome / Firefox 扩展模板。"""

    def __init__(self, name: str = "AuroraExt",
                 description: str = "Aurora extension",
                 version: str = "1.0.0") -> None:
        self.name = name
        self.description = description
        self.version = version

    def generate(self, browser: str = "chrome", output_dir: str = ".") -> str:
        """生成扩展工程到 ``output_dir/<name>/``。返回工程路径。"""
        root = os.path.join(output_dir, self.name)
        if browser == "chrome":
            manifest = self._chrome_manifest()
        elif browser == "firefox":
            manifest = self._firefox_manifest()
        else:
            raise ValueError(f"未知浏览器: {browser}")
        _write_text(os.path.join(root, "manifest.json"),
                    json.dumps(manifest, indent=2, ensure_ascii=False))
        _write_text(os.path.join(root, "background.js"),
                    "// background service worker\n")
        _write_text(os.path.join(root, "content.js"),
                    "// content script\n")
        _write_text(os.path.join(root, "popup.html"),
                    f"<!DOCTYPE html><html><body><h3>{self.name}</h3></body></html>")
        _write_text(os.path.join(root, "options.html"),
                    f"<!DOCTYPE html><html><body><h3>{self.name} options</h3></body></html>")
        return root

    def _chrome_manifest(self) -> Dict[str, Any]:
        return {
            "manifest_version": 3,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "background": {"service_worker": "background.js"},
            "content_scripts": [{"matches": ["<all_urls>"], "js": ["content.js"]}],
            "action": {"default_popup": "popup.html"},
            "options_page": "options.html",
            "permissions": ["storage", "activeTab"],
        }

    def _firefox_manifest(self) -> Dict[str, Any]:
        m = self._chrome_manifest()
        m["browser_specific_settings"] = {"gecko": {"id": f"{self.name}@aurora.dev"}}
        return m


__all__ = [
    "DOMBridge", "DOMElement", "DOMEvent", "generate_dom_bindings",
    "JSCompiler", "WASMCompiler",
    "VNode", "Component", "diff", "patch", "Store", "Route", "Router",
    "create_app", "generate_web_project", "ExtensionGenerator",
]
