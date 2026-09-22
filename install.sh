#!/bin/bash
# Aurora v5.0.0 安装脚本 — 把 aurora 命令安装到 PATH 中的用户 bin 目录
# 284万行自举标准库 · ARM64 原生机器码 · AOT 编译
# 优先级: ~/.local/bin > ~/bin > /usr/local/bin(sudo)
# 用法: bash install.sh
set -e

VERSION="5.0.0"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAUNCHER="$PROJECT_DIR/aurora-run"

if [ ! -f "$LAUNCHER" ]; then
  echo "错误: 找不到 $LAUNCHER"; exit 1
fi

echo "========================================"
echo "  Aurora v$VERSION 安装程序"
echo "  284万行自举标准库 · ARM64 原生机器码"
echo "========================================"
echo ""

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
# Aurora v$VERSION - 284万行自举标准库
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

echo "✓ 已安装: $BIN"
echo ""
echo "========================================"
echo "  Aurora v$VERSION 安装完成！"
echo "========================================"
echo ""
echo "核心命令:"
echo "  aurora run <file.aur>       VM 模式运行"
echo "  aurora compile <file.aur>   AOT 编译为原生机器码"
echo "  aurora check <file.aur>     静态检查"
echo "  aurora fmt <file.aur>       代码格式化"
echo ""
echo "开发工具:"
echo "  aurora new <name>           创建项目"
echo "  aurora test                 运行测试"
echo "  aurora profile <file.aur>   性能分析"
echo "  aurora debug <file.aur>     源码调试"
echo "  aurora lsp                  LSP 语言服务器"
echo ""
echo "全栈开发:"
echo "  aurora pkg add <dep>        包管理"
echo "  aurora ai train/infer       AI 训练/推理"
echo "  aurora bench                性能基准测试"
echo "  aurora dev                  开发模式(热重载)"
echo "  aurora deploy               部署应用"
echo ""
echo "版本信息:"
"$BIN" --version 2>/dev/null || echo "  Aurora v$VERSION"
echo ""
echo "开始使用 Aurora 构建超大型项目吧！"
