// aurora_runtime.c — Aurora 运行时 (macOS arm64)
// 桥接到 libc 函数

#include <stdint.h>
#include <stddef.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

// ============ 堆分配器 ============

static void* heap_ptr = NULL;
static size_t heap_used = 0;
static size_t heap_capacity = 0;

#define HEAP_INIT_SIZE (16 * 1024 * 1024)  // 16MB

void aurora_runtime_init(void) {
    heap_ptr = malloc(HEAP_INIT_SIZE);
    heap_capacity = HEAP_INIT_SIZE;
    heap_used = 0;
}

void* aurora_alloc(size_t size) {
    size = (size + 15) & ~15;  // 16 字节对齐
    if (heap_used + size > heap_capacity) {
        return NULL;
    }
    void* ptr = (char*)heap_ptr + heap_used;
    heap_used += size;
    return ptr;
}

// ============ IO 原语 ============

long aurora_write(int fd, const void* buf, size_t count) {
    return write(fd, buf, count);
}

long aurora_read(int fd, void* buf, size_t count) {
    return read(fd, buf, count);
}

long aurora_open(const char* path, int flags, int mode) {
    return open(path, flags, mode);
}

long aurora_close(int fd) {
    return close(fd);
}

void aurora_exit(int code) {
    exit(code);
}

// ============ 时间 ============

long aurora_clock_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

// ============ 字符串原语 ============

size_t aurora_strlen(const char* s) {
    return strlen(s);
}

char aurora_char_at(const char* s, size_t i) {
    return s[i];
}

// ============ Aurora main 桥接 ============

extern int aurora_main(int argc, char** argv, char** envp);
