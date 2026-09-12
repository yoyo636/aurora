#!/bin/bash
# Aurora 教学工坊 —— macOS 双击启动
# 双击此文件即可启动;关闭服务器时按 Ctrl+C,或直接关闭本窗口
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
if curl -s --max-time 1 http://127.0.0.1:8697/api/health > /dev/null 2>&1; then
  echo "服务已在运行,打开浏览器…"
  open "http://127.0.0.1:8697"
  sleep 1
  exit 0
fi
python3 server.py --open
echo ""
echo "服务器已停止。窗口即将关闭…"
sleep 2
