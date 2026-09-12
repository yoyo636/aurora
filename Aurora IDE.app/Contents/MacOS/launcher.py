# -*- coding: utf-8 -*-
"""Aurora IDE —— 内嵌窗口启动器。

启动本地 server(如未运行),并用 pywebview 打开原生窗口;
若 pywebview 不可用,则回退为默认浏览器。
窗口关闭时,回收本进程启动的 server。
"""

import os
import subprocess
import sys
import time

PROJECT_ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDE_DIR = os.path.join(PROJECT_ROOT, "ide")
PORT = int(os.environ.get("AURORA_PORT", "8697"))
URL = "http://127.0.0.1:%d" % PORT


def server_alive():
    try:
        import urllib.request
        with urllib.request.urlopen(URL + "/api/health", timeout=1) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    server_proc = None
    if not server_alive():
        server_proc = subprocess.Popen(
            [sys.executable, os.path.join(IDE_DIR, "server.py")],
            cwd=IDE_DIR,
        )
        for _ in range(40):  # 最多等 10s
            if server_alive():
                break
            time.sleep(0.25)

    try:
        import webview  # noqa: E402

        # 设置应用菜单栏名称(默认会显示 Python)
        def _rename_app():
            try:
                import AppKit  # noqa: E402
                AppKit.NSApplication.sharedApplication().setName_("Aurora IDE")
            except Exception:
                pass

        webview.create_window(
            "Aurora IDE",
            URL,
            width=1280,
            height=840,
            min_size=(900, 600),
        )
        webview.start(_rename_app)
    except Exception:
        # 回退:默认浏览器模式
        import webbrowser
        webbrowser.open(URL)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
    finally:
        if server_proc is not None:
            try:
                server_proc.terminate()
            except OSError:
                pass


if __name__ == "__main__":
    main()
