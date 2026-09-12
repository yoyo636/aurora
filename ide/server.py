# -*- coding: utf-8 -*-
"""Aurora 教学工坊 —— 本地 HTTP 服务器。

macOS 本地 Web 应用:启动后浏览器访问 http://127.0.0.1:8697
提供:课程数据、代码运行(隔离子进程+超时+标准输入)、静态检查、练习验证。

启动:
    python3 server.py              # 启动服务(不自动开浏览器)
    python3 server.py --open       # 启动并自动打开默认浏览器
"""

import json
import os
import subprocess
import sys
import tempfile
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))  # /Users/wuyuanduo(包在 aurora/ 下)
WORKSPACE = os.path.dirname(HERE)  # 工作区 = aurora 项目根(IDE 的文件浏览/读写边界)
STATIC_DIR = os.path.join(HERE, "static")
WORKER = os.path.join(HERE, "worker.py")
PORT = int(os.environ.get("AURORA_PORT", "8697"))
TIMEOUT = 8  # 秒

# 文件浏览器忽略的目录
_EXCLUDE_DIRS = {
    ".git", "__pycache__", ".sessions", "node_modules", ".venv", "venv",
    "dist", "build", ".doubaowork", ".pytest_cache", ".mypy_cache", ".idea", ".vscode",
}
# 可保存的文本扩展名(工作区安全边界内的白名单)
_EDITABLE_EXTS = {
    ".aur", ".txt", ".md", ".py", ".json", ".toml", ".csv",
    ".html", ".css", ".js", ".sh", ".yaml", ".yml", ".xml",
}
_MAX_FILE_BYTES = 1024 * 1024  # 读取上限 1MB


def _safe_workspace_path(rel_path):
    """校验相对路径合法且解析后仍位于工作区内;返回绝对路径,否则返回 None。"""
    if not rel_path or "\x00" in rel_path:
        return None
    norm = os.path.normpath(rel_path)
    if norm.startswith("..") or os.path.isabs(norm):
        return None
    abs_path = os.path.realpath(os.path.join(WORKSPACE, norm))
    if not abs_path.startswith(os.path.realpath(WORKSPACE) + os.sep) and abs_path != os.path.realpath(WORKSPACE):
        return None
    return abs_path


def _scan_tree(rel_dir=""):
    """递归扫描工作区,返回文件树。"""
    nodes = []
    base = os.path.join(WORKSPACE, rel_dir)
    try:
        entries = sorted(os.listdir(base), key=lambda n: (not os.path.isdir(os.path.join(base, n)), n.lower()))
    except OSError:
        return nodes
    for name in entries:
        if name.startswith("."):
            continue
        full = os.path.join(base, name)
        rel = os.path.join(rel_dir, name) if rel_dir else name
        if os.path.isdir(full):
            if name in _EXCLUDE_DIRS or name.endswith(".app"):
                continue
            children = _scan_tree(rel)
            nodes.append({"name": name, "path": rel, "type": "dir", "children": children})
        else:
            ext = os.path.splitext(name)[1].lower()
            nodes.append({"name": name, "path": rel, "type": "file", "ext": ext})
    return nodes


def _load_lessons():
    sys.path.insert(0, HERE)
    from lessons import LESSONS
    return LESSONS


LESSONS = _load_lessons()


def _run_worker(mode, code, stdin_data=""):
    """在隔离子进程中运行 Aurora 代码,返回结果 dict。"""
    token = uuid.uuid4().hex[:12]
    src_path = os.path.join(tempfile.gettempdir(), f"aurora_src_{token}.aur")
    result_path = os.path.join(tempfile.gettempdir(), f"aurora_res_{token}.json")
    try:
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(code)
        proc = subprocess.run(
            [sys.executable, WORKER, mode, src_path, result_path, PROJECT_ROOT],
            input=stdin_data.encode("utf-8"),
            capture_output=True,
            timeout=TIMEOUT,
        )
        if os.path.exists(result_path):
            with open(result_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "kind": "error",
            "output": "",
            "errors": [{
                "kind": "WorkerError",
                "message": proc.stderr.decode("utf-8", "replace") or "解释器进程异常退出",
            }],
        }
    except subprocess.TimeoutExpired:
        return {
            "kind": "error",
            "output": "",
            "errors": [{
                "kind": "TimeoutError",
                "message": f"运行超时({TIMEOUT}s),可能存在死循环",
            }],
        }
    finally:
        for p in (src_path, result_path):
            try:
                os.remove(p)
            except OSError:
                pass


def _normalize_output(text):
    """去掉首尾空白,压缩行尾空白,便于对比。"""
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # 静默访问日志
        pass

    # ---------- 工具 ----------
    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _serve_static(self, path):
        if path in ("/", "/index.html"):
            file_path = os.path.join(STATIC_DIR, "index.html")
        else:
            # 只允许静态目录内的普通文件,防目录穿越
            name = os.path.basename(path)
            file_path = os.path.join(STATIC_DIR, name)
        if not os.path.isfile(file_path):
            self.send_error(404)
            return
        ext = os.path.splitext(file_path)[1]
        ctype = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".ico": "image/x-icon",
        }.get(ext, "application/octet-stream")
        with open(file_path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ---------- 路由 ----------
    def do_GET(self):
        if self.path == "/api/health":
            return self._send_json({"ok": True, "version": "aurora-ide 1.0"})
        if self.path == "/api/lessons":
            return self._send_json({"lessons": LESSONS})
        if self.path == "/api/files":
            return self._send_json({"workspace": WORKSPACE, "tree": _scan_tree()})
        if self.path.startswith("/api/file"):
            # /api/file?path=相对路径
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            rel = qs.get("path", [""])[0]
            abs_path = _safe_workspace_path(rel)
            if abs_path is None:
                return self._send_json({"error": "非法的文件路径"}, 400)
            if not os.path.isfile(abs_path):
                return self._send_json({"error": "文件不存在"}, 404)
            if os.path.getsize(abs_path) > _MAX_FILE_BYTES:
                return self._send_json({"error": "文件过大"}, 413)
            try:
                with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except OSError as e:
                return self._send_json({"error": f"读取失败: {e}"}, 500)
            return self._send_json({"path": rel, "name": os.path.basename(abs_path), "content": content})
        if self.path.startswith("/api/"):
            return self._send_json({"error": "not found"}, 404)
        return self._serve_static(self.path)

    def do_POST(self):
        if self.path == "/api/run":
            data = self._read_json()
            code = data.get("code", "")
            stdin_data = data.get("stdin", "")
            result = _run_worker("run", code, stdin_data)
            return self._send_json(result)

        if self.path == "/api/check":
            data = self._read_json()
            code = data.get("code", "")
            result = _run_worker("check", code)
            return self._send_json(result)

        if self.path == "/api/file/save":
            data = self._read_json()
            rel = data.get("path", "")
            content = data.get("content", "")
            abs_path = _safe_workspace_path(rel)
            if abs_path is None:
                return self._send_json({"error": "非法的文件路径"}, 400)
            ext = os.path.splitext(abs_path)[1].lower()
            if ext not in _EDITABLE_EXTS:
                return self._send_json({"error": f"不允许编辑 {ext or '无扩展名'} 文件"}, 400)
            if len(content.encode("utf-8")) > _MAX_FILE_BYTES:
                return self._send_json({"error": "内容过大"}, 413)
            try:
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                with open(abs_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except OSError as e:
                return self._send_json({"error": f"保存失败: {e}"}, 500)
            return self._send_json({"ok": True, "path": rel})

        if self.path == "/api/file/new":
            data = self._read_json()
            rel = data.get("path", "")
            abs_path = _safe_workspace_path(rel)
            if abs_path is None:
                return self._send_json({"error": "非法的文件路径"}, 400)
            ext = os.path.splitext(abs_path)[1].lower()
            if ext not in _EDITABLE_EXTS:
                return self._send_json({"error": f"不允许创建 {ext or '无扩展名'} 文件"}, 400)
            if os.path.exists(abs_path):
                return self._send_json({"error": "文件已存在"}, 409)
            try:
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                with open(abs_path, "w", encoding="utf-8") as f:
                    f.write("")
            except OSError as e:
                return self._send_json({"error": f"创建失败: {e}"}, 500)
            return self._send_json({"ok": True, "path": rel})

        if self.path == "/api/verify":
            data = self._read_json()
            lesson_id = data.get("lesson_id", "")
            code = data.get("code", "")
            lesson = next((l for l in LESSONS if l["id"] == lesson_id), None)
            if lesson is None:
                return self._send_json({"error": f"未知课程 {lesson_id}"}, 404)
            expected = (lesson.get("exercise") or {}).get("expected")
            result = _run_worker("run", code, data.get("stdin", ""))
            actual = result.get("output", "")
            if result.get("errors"):
                return self._send_json({
                    "pass": False,
                    "reason": "程序运行出错",
                    "errors": result["errors"],
                    "expected": expected,
                    "actual": actual,
                })
            if expected is None:
                return self._send_json({
                    "pass": True,
                    "note": "本题无固定输出,运行成功即通过",
                    "actual": actual,
                })
            ok = _normalize_output(actual) == _normalize_output(expected)
            return self._send_json({
                "pass": ok,
                "expected": expected,
                "actual": actual,
            })

        return self._send_json({"error": "not found"}, 404)


def main():
    open_browser = "--open" in sys.argv
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}"
    print("=" * 52)
    print("  Aurora 教学工坊已启动")
    print(f"  地址: {url}")
    print(f"  按 Ctrl+C 停止服务")
    print("=" * 52)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")


if __name__ == "__main__":
    main()
