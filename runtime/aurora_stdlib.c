// aurora_stdlib.c — Aurora 原生标准库
// 供 Aurora 程序调用的核心函数

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>

// ============ 基础类型 ============

typedef struct {
    int type;        // 0=int, 1=float, 2=string, 3=list, 4=dict, 5=bool, 6=nil
    union {
        int64_t i;
        double f;
        const char* s;
        void* p;
    } data;
} AuroraValue;

// ============ 字符串操作 ============

const char* aurora_str_concat(const char* a, const char* b) {
    size_t la = strlen(a);
    size_t lb = strlen(b);
    char* result = malloc(la + lb + 1);
    memcpy(result, a, la);
    memcpy(result + la, b, lb);
    result[la + lb] = '\0';
    return result;
}

int aurora_str_len(const char* s) {
    return (int)strlen(s);
}

char aurora_str_char_at(const char* s, int i) {
    return s[i];
}

const char* aurora_str_substr(const char* s, int start, int end) {
    int len = end - start;
    char* result = malloc(len + 1);
    memcpy(result, s + start, len);
    result[len] = '\0';
    return result;
}

int aurora_str_cmp(const char* a, const char* b) {
    return strcmp(a, b);
}

// ============ 整数转字符串 ============

const char* aurora_int_to_str(int64_t n) {
    char* buf = malloc(32);
    int pos = 0;
    int neg = 0;
    if (n < 0) { neg = 1; n = -n; }
    if (n == 0) {
        buf[0] = '0';
        buf[1] = '\0';
        return buf;
    }
    char tmp[32];
    int i = 0;
    while (n > 0) {
        tmp[i++] = '0' + (n % 10);
        n /= 10;
    }
    if (neg) tmp[i++] = '-';
    while (i > 0) {
        buf[pos++] = tmp[--i];
    }
    buf[pos] = '\0';
    return buf;
}

int64_t aurora_str_to_int(const char* s) {
    return atoll(s);
}

// ============ 列表操作 (简化版) ============

typedef struct AuroraList {
    AuroraValue* items;
    int count;
    int capacity;
} AuroraList;

AuroraList* aurora_list_new(int capacity) {
    AuroraList* list = malloc(sizeof(AuroraList));
    list->items = malloc(sizeof(AuroraValue) * capacity);
    list->count = 0;
    list->capacity = capacity;
    return list;
}

void aurora_list_push(AuroraList* list, AuroraValue item) {
    if (list->count >= list->capacity) {
        list->capacity *= 2;
        list->items = realloc(list->items, sizeof(AuroraValue) * list->capacity);
    }
    list->items[list->count++] = item;
}

AuroraValue aurora_list_pop(AuroraList* list) {
    return list->items[--list->count];
}

int aurora_list_len(AuroraList* list) {
    return list->count;
}

// ============ 数学函数 ============

double aurora_sqrt(double x) {
    // 牛顿法
    if (x <= 0) return 0;
    double guess = x / 2.0;
    for (int i = 0; i < 20; i++) {
        guess = (guess + x / guess) / 2.0;
    }
    return guess;
}

int64_t aurora_pow(int64_t base, int64_t exp) {
    int64_t result = 1;
    for (int64_t i = 0; i < exp; i++) {
        result *= base;
    }
    return result;
}

int64_t aurora_abs(int64_t x) {
    return x < 0 ? -x : x;
}

int64_t aurora_min(int64_t a, int64_t b) {
    return a < b ? a : b;
}

int64_t aurora_max(int64_t a, int64_t b) {
    return a > b ? a : b;
}

// ============ 时间 ============

int64_t aurora_time_now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (int64_t)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

// ============ 打印 ============

void aurora_print_str(const char* s) {
    write(1, s, strlen(s));
}

void aurora_print_int(int64_t n) {
    const char* s = aurora_int_to_str(n);
    aurora_print_str(s);
}

void aurora_println_str(const char* s) {
    aurora_print_str(s);
    aurora_print_str("\n");
}

void aurora_println_int(int64_t n) {
    aurora_print_int(n);
    aurora_print_str("\n");
}
