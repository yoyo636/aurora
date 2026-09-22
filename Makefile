# Makefile — Aurora 自举构建系统
# 目标：从 .aur 源码构建独立的 aurora 二进制

.PHONY: all clean test bootstrap runtime

# 编译器
CC = clang
AR = ar
LD = ld

# 架构
ARCH = arm64
CFLAGS = -O2 -Wall -Wextra -target aarch64-linux-gnu

# 目录
RUNTIME_DIR = runtime
SRC_DIR = .
SELFHOST_DIR = selfhost

# 目标
TARGET = bin/aurora
RUNTIME_OBJ = $(RUNTIME_DIR)/aurora_runtime.o
CRT0_OBJ = $(RUNTIME_DIR)/crt0.o

# 默认目标
all: runtime test
	@echo "✓ Aurora 构建完成"

# 构建运行时 (C 桥接层)
runtime: $(RUNTIME_OBJ) $(CRT0_OBJ)
	@echo "✓ 运行时构建完成"

$(RUNTIME_OBJ): $(RUNTIME_DIR)/aurora_runtime.c
	@mkdir -p bin
	$(CC) $(CFLAGS) -c $< -o $@

$(CRT0_OBJ): $(RUNTIME_DIR)/crt0.s
	@mkdir -p bin
	$(CC) $(CFLAGS) -c $< -o $@

# 自举测试
test:
	@echo "=== 自举测试 ==="
	./aurora-run run $(SELFHOST_DIR)/test_bootstrap.aur
	@echo ""
	@echo "=== 完整测试 ==="
	./aurora-run run $(SELFHOST_DIR)/test_selfhost_v2.aur

# 清理
clean:
	rm -f $(RUNTIME_OBJ) $(CRT0_OBJ)
	rm -f bin/*.o bin/aurora
	@echo "✓ 清理完成"

# 统计
stats:
	@echo "=== Aurora 项目统计 ==="
	@echo ".aur 文件: $$(ls *.aur selfhost/*.aur 2>/dev/null | wc -l)"
	@echo "总行数: $$(cat *.aur selfhost/*.aur 2>/dev/null | wc -l)"
	@echo "C 运行时: $$(wc -l < $(RUNTIME_DIR)/aurora_runtime.c)"
	@echo "汇编启动: $$(wc -l < $(RUNTIME_DIR)/crt0.s)"
	@echo "Python 文件(根目录): $$(find . -maxdepth 1 -name '*.py' | wc -l)"
