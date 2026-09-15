#!/bin/bash
# Aurora 安装脚本 — 把 aurora 命令安装到 PATH 中的用户 bin 目录
# 优先级: ~/.local/bin > ~/bin > /usr/local/bin(sudo)
# 用法: bash install.sh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAUNCHER="$PROJECT_DIR/aurora-run"

if [ ! -f "$LAUNCHER" ]; then
  echo "错误: 找不到 $LAUNCHER"; exit 1
fi

# 选择安装目录
if [ -d "$HOME/.local/bin" ] && echo ":$PATH:" | grep -q ":$HOME/.local/bin:"; then
  BIN_DIR="$HOME/.local/bin"
elif [ -d "$HOME/bin" ] && echo ":$PATH:" | grep -q ":$HOME/bin:"; then
  BIN_DIR="$HOME/bin"
else
  BIN_DIR="/usr/local/bin"
fi

BIN="$BIN_DIR/aurora"

# 生成 wrapper(指向真实 aurora-run)
WRAPPER=$(mktemp)
cat > "$WRAPPER" <<EOF
#!/bin/bash
exec "$LAUNCHER" "\$@"
EOF
chmod 755 "$WRAPPER"

if [ -w "$BIN_DIR" ]; then
  cp "$WRAPPER" "$BIN"
else
  echo "需要权限写入 $BIN_DIR(将使用 sudo)"
  sudo cp "$WRAPPER" "$BIN"
fi
rm -f "$WRAPPER"

echo "已安装: $BIN"
"$BIN" --version
echo ""
echo "现在可以直接使用:"
echo "  aurora repl           交互式编程"
echo "  aurora new myapp      创建项目"
echo "  aurora run            运行项目(读 aurora.toml)"
echo "  aurora test           运行测试"
echo "  aurora check main.aur 静态检查"
echo "  aurora fmt main.aur   代码格式化"
echo "  aurora profile main.aur 性能分析"
echo "  aurora debug main.aur 源码调试"
echo "  aurora lsp            LSP 语言服务器"
echo "  aurora pkg add <dep>  包管理"
echo "  aurora ai train/infer    AI 训练/推理"
echo "  aurora bench             性能基准测试"
echo "  aurora workspace         工作区管理"
echo "  aurora deps              依赖管理"
echo "  aurora ui                GUI 应用"
echo "  aurora package           跨平台打包"
echo "  aurora kernel            Jupyter 内核"
echo "  aurora serve             推理服务"
echo "  aurora interop           语言互操作"
echo "  aurora wasm              WebAssembly"
