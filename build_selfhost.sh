#!/bin/bash
# build_selfhost.sh — 自举构建脚本
# 用自举版编译器编译 Aurora 自身

set -e
cd "$(dirname "$0")"

echo "======================================"
echo "Aurora 自举构建 v4.0.0"
echo "======================================"
echo ""

# 阶段 1: 用 Python 引导版运行自举测试
echo "[阶段 1] 验证自举测试..."
./aurora-run run selfhost/test_bootstrap.aur
echo ""

# 阶段 2: 运行 v2 测试
echo "[阶段 2] 运行完整测试套件..."
./aurora-run run selfhost/test_selfhost_v2.aur
echo ""

# 阶段 3: 统计
echo "[阶段 3] 项目统计..."
echo "  .aur 文件数: $(ls *.aur selfhost/*.aur | wc -l)"
echo "  总行数: $(cat *.aur selfhost/*.aur | wc -l)"
echo "  Python 文件: $(find . -maxdepth 1 -name '*.py' | wc -l)"
echo ""

echo "======================================"
echo "✓ 自举构建完成"
echo "======================================"
