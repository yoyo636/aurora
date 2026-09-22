#!/bin/bash
# build.sh — Aurora 自举构建脚本
# 用法: ./build.sh [test|runtime|clean|stats]

set -e
cd "$(dirname "$0")"

echo "╔══════════════════════════════════════╗"
echo "║  Aurora 自举构建系统 v4.0.0        ║"
echo "╚══════════════════════════════════════╝"
echo ""

case "${1:-all}" in
    test)
        echo "=== 运行自举测试 ==="
        ./aurora-run run selfhost/test_bootstrap.aur
        echo ""
        ./aurora-run run selfhost/test_selfhost_v2.aur
        ;;
    runtime)
        echo "=== 构建运行时 ==="
        make runtime
        ;;
    clean)
        echo "=== 清理 ==="
        make clean
        ;;
    stats)
        make stats
        ;;
    all)
        echo "=== 完整构建 ==="
        make all
        make stats
        ;;
    *)
        echo "用法: $0 [test|runtime|clean|stats|all]"
        exit 1
        ;;
esac

echo ""
echo "✓ 完成"
