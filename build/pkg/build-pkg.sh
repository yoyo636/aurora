#!/bin/bash
# Aurora 编程语言 macOS 安装器构建脚本
# 用法: ./build-pkg.sh
# 输出: build/Aurora-Installer-v1.3.0.pkg

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PKG_DIR="$SCRIPT_DIR"
PAYLOAD="$PKG_DIR/payload"
RESOURCES="$PKG_DIR/resources"
SCRIPTS="$PKG_DIR/scripts"
BUILD_DIR="$PROJECT_ROOT/build"
VERSION="1.3.0"

echo "=== Aurora 安装器构建 ==="
echo "项目根: $PROJECT_ROOT"
echo "版本: $VERSION"

# 1. 清理并准备 payload
echo ""
echo "[1/5] 准备 payload..."
rm -rf "$PAYLOAD/usr/local/lib/aurora"
mkdir -p "$PAYLOAD/usr/local/lib/aurora"
mkdir -p "$PAYLOAD/usr/local/bin"

# 2. 复制 Aurora 源码(核心 .py 文件)
echo "[2/5] 复制 Aurora 运行时..."
CORE_FILES=(
    "__init__.py" "__main__.py" "cli.py" "lexer.py" "parser.py"
    "ast_nodes.py" "tokens.py" "type_checker.py" "ownership.py"
    "interpreter.py" "stdlib.py" "codegen.py" "repl.py"
)
for f in "${CORE_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$f" ]; then
        cp "$PROJECT_ROOT/$f" "$PAYLOAD/usr/local/lib/aurora/"
    fi
done

# 复制文档
mkdir -p "$PAYLOAD/usr/local/lib/aurora/docs"
cp "$PROJECT_ROOT/README.md" "$PAYLOAD/usr/local/lib/aurora/" 2>/dev/null || true
cp "$PROJECT_ROOT/CHANGELOG.md" "$PAYLOAD/usr/local/lib/aurora/" 2>/dev/null || true
cp "$PROJECT_ROOT/docs/SPEC.md" "$PAYLOAD/usr/local/lib/aurora/docs/" 2>/dev/null || true
cp "$PROJECT_ROOT/docs/AI_GUIDE.md" "$PAYLOAD/usr/local/lib/aurora/docs/" 2>/dev/null || true
cp "$PROJECT_ROOT/docs/AI_SYSTEM_PROMPT.md" "$PAYLOAD/usr/local/lib/aurora/docs/" 2>/dev/null || true
cp "$PROJECT_ROOT/docs/VERSIONING.md" "$PAYLOAD/usr/local/lib/aurora/docs/" 2>/dev/null || true

# 复制 VSCode 插件
mkdir -p "$PAYLOAD/usr/local/lib/aurora/vscode-extension"
cp "$PROJECT_ROOT"/vscode-aurora/*.vsix "$PAYLOAD/usr/local/lib/aurora/vscode-extension/" 2>/dev/null || true
cp "$PROJECT_ROOT/vscode-aurora/package.json" "$PAYLOAD/usr/local/lib/aurora/vscode-extension/" 2>/dev/null || true

# 复制示例
mkdir -p "$PAYLOAD/usr/local/lib/aurora/examples"
cp -r "$PROJECT_ROOT/examples/benchmarks" "$PAYLOAD/usr/local/lib/aurora/examples/" 2>/dev/null || true
cp -r "$PROJECT_ROOT/examples/largeapp" "$PAYLOAD/usr/local/lib/aurora/examples/" 2>/dev/null || true
cp -r "$PROJECT_ROOT/examples/fullstack" "$PAYLOAD/usr/local/lib/aurora/examples/" 2>/dev/null || true

# 3. 设置权限
echo "[3/5] 设置权限..."
chmod +x "$PAYLOAD/usr/local/bin/aurora"
chmod +x "$SCRIPTS/postinstall"
chmod -R a+rX "$PAYLOAD/usr/local/lib/aurora"
# 清除 macOS 扩展属性(否则 pkgbuild 会跳过带 com.apple.provenance 的文件)
xattr -cr "$PAYLOAD" 2>/dev/null || true

# 4. 构建核心包
echo "[4/5] 构建核心包..."
COPYFILE_DISABLE=1 pkgbuild \
    --root "$PAYLOAD" \
    --scripts "$SCRIPTS" \
    --identifier "com.aurora-lang.core" \
    --version "$VERSION" \
    --install-location "/" \
    "$BUILD_DIR/aurora-core.pkg"

# 5. 构建最终安装器
echo "[5/5] 构建最终安装器..."
COPYFILE_DISABLE=1 productbuild \
    --distribution "$PKG_DIR/Distribution.xml" \
    --resources "$RESOURCES" \
    --package-path "$BUILD_DIR" \
    "$BUILD_DIR/Aurora-Installer-v${VERSION}.pkg"

# 清理中间文件
rm -f "$BUILD_DIR/aurora-core.pkg"

echo ""
echo "=== 构建完成 ==="
echo "安装器: $BUILD_DIR/Aurora-Installer-v${VERSION}.pkg"
ls -lh "$BUILD_DIR/Aurora-Installer-v${VERSION}.pkg"
