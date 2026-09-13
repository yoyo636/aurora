/*
 * Aurora Runtime Library
 * 原生编译器运行时 — 字符串/数组/Map/通用值/内存管理/内置函数
 */
#ifndef AURORA_RT_H
#define AURORA_RT_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================
 * 通用值类型(标签联合)
 * ============================================================ */
typedef enum {
    AU_NIL = 0,
    AU_INT,
    AU_FLOAT,
    AU_BOOL,
    AU_STRING,
    AU_ARRAY,
    AU_MAP,
} AuType;

typedef struct AuString AuString;
typedef struct AuArray  AuArray;
typedef struct AuMap    AuMap;

typedef struct AuValue {
    AuType type;
    union {
        int64_t  i;
        double   f;
        bool     b;
        AuString* s;
        AuArray*  arr;
        AuMap*    map;
    } as;
} AuValue;

/* 值构造宏 */
#define AU_NIL_VAL()    ((AuValue){.type = AU_NIL})
#define AU_INT_VAL(v)   ((AuValue){.type = AU_INT, .as.i = (v)})
#define AU_FLOAT_VAL(v) ((AuValue){.type = AU_FLOAT, .as.f = (v)})
#define AU_BOOL_VAL(v)  ((AuValue){.type = AU_BOOL, .as.b = (v)})

/* ============================================================
 * 字符串(AuString)— 带长度,UTF-8,不可变视图+拥有
 * ============================================================ */
struct AuString {
    char*  data;
    size_t len;
    bool   owned;  /* true 时 free(data),false 时不 free(字符串字面量) */
};

AuString* au_string_new(const char* s);
AuString* au_string_new_len(const char* s, size_t len);
AuString* au_string_from_literal(const char* s);  /* 不拷贝,owned=false */
AuString* au_string_concat(AuString* a, AuString* b);
AuString* au_string_format(const char* fmt, ...);
bool      au_string_eq(AuString* a, AuString* b);
int       au_string_cmp(AuString* a, AuString* b);
AuString* au_string_substring(AuString* s, int64_t start, int64_t end);
AuString* au_string_replace(AuString* s, AuString* from, AuString* to);
AuString* au_string_to_lower(AuString* s);
AuString* au_string_to_upper(AuString* s);
AuString* au_string_trim(AuString* s);
AuArray*  au_string_split(AuString* s, AuString* sep);
bool      au_string_contains(AuString* s, AuString* sub);
bool      au_string_starts_with(AuString* s, AuString* prefix);
bool      au_string_ends_with(AuString* s, AuString* suffix);
int64_t   au_string_to_int(AuString* s);
double    au_string_to_float(AuString* s);
void      au_string_free(AuString* s);

/* ============================================================
 * 动态数组(AuArray)
 * ============================================================ */
struct AuArray {
    AuValue* data;
    size_t   len;
    size_t   cap;
};

AuArray* au_array_new(void);
AuArray* au_array_with_capacity(size_t cap);
AuArray* au_array_from_values(AuValue* vals, size_t n);
void      au_array_push(AuArray* arr, AuValue val);
AuValue   au_array_pop(AuArray* arr);
AuValue   au_array_get(AuArray* arr, int64_t idx);
void      au_array_set(AuArray* arr, int64_t idx, AuValue val);
void      au_array_insert(AuArray* arr, int64_t idx, AuValue val);
void      au_array_remove(AuArray* arr, int64_t idx);
bool      au_array_contains(AuArray* arr, AuValue val);
int64_t   au_array_index_of(AuArray* arr, AuValue val);
void      au_array_reverse(AuArray* arr);
AuArray*  au_array_slice(AuArray* arr, int64_t start, int64_t end);
AuArray*  au_array_concat(AuArray* a, AuArray* b);
void      au_array_sort(AuArray* arr);
void      au_array_free(AuArray* arr);

/* ============================================================
 * 哈希表(AuMap)— 开放寻址,字符串键
 * ============================================================ */
typedef struct AuMapEntry {
    AuString* key;
    AuValue   value;
    bool      occupied;
} AuMapEntry;

struct AuMap {
    AuMapEntry* entries;
    size_t      len;
    size_t      cap;
};

AuMap*  au_map_new(void);
AuMap*  au_map_with_capacity(size_t cap);
void    au_map_set(AuMap* map, AuString* key, AuValue val);
AuValue au_map_get(AuMap* map, AuString* key);
bool    au_map_has(AuMap* map, AuString* key);
void    au_map_remove(AuMap* map, AuString* key);
AuArray* au_map_keys(AuMap* map);
AuArray* au_map_values(AuMap* map);
void    au_map_free(AuMap* map);

/* ============================================================
 * 值操作
 * ============================================================ */
AuValue   au_value_clone(AuValue v);
void      au_value_free(AuValue v);
bool      au_value_eq(AuValue a, AuValue b);
int       au_value_cmp(AuValue a, AuValue b);
AuString* au_value_to_string(AuValue v);
AuString* au_value_type_name(AuValue v);
bool      au_value_truthy(AuValue v);

/* 算术运算 */
AuValue au_add(AuValue a, AuValue b);
AuValue au_sub(AuValue a, AuValue b);
AuValue au_mul(AuValue a, AuValue b);
AuValue au_div(AuValue a, AuValue b);
AuValue au_mod(AuValue a, AuValue b);
AuValue au_pow(AuValue a, AuValue b);
AuValue au_neg(AuValue a);

/* 比较运算 */
bool au_lt(AuValue a, AuValue b);
bool au_le(AuValue a, AuValue b);
bool au_gt(AuValue a, AuValue b);
bool au_ge(AuValue a, AuValue b);

/* 逻辑运算 */
bool au_and(AuValue a, AuValue b);
bool au_or(AuValue a, AuValue b);
bool au_not(AuValue a);

/* ============================================================
 * 内置函数
 * ============================================================ */
void    au_print(AuValue v);
void    au_println(AuValue v);
int64_t au_len(AuValue v);
AuValue au_range(int64_t start, int64_t end);  /* 闭区间 [start, end] */
AuValue au_read_line(void);
AuValue au_read_file(AuString* path);
void    au_write_file(AuString* path, AuString* content);
void    au_append_file(AuString* path, AuString* content);
bool    au_file_exists(AuString* path);
AuArray* au_list_dir(AuString* path);
void    au_shell(AuString* cmd);
AuValue au_get_env(AuString* name);
void    au_set_env(AuString* name, AuString* value);
int64_t au_now_ms(void);
void    au_sleep_ms(int64_t ms);

/* 数学函数 */
double au_sqrt(double x);
double au_abs(double x);
double au_sin(double x);
double au_cos(double x);
double au_tan(double x);
double au_log(double x);
double au_exp(double x);
double au_floor(double x);
double au_ceil(double x);
double au_round(double x);
double au_min(double a, double b);
double au_max(double a, double b);
int64_t au_gcd(int64_t a, int64_t b);
int64_t au_lcm(int64_t a, int64_t b);
bool    au_is_prime(int64_t n);
int64_t au_factorial(int64_t n);
int64_t au_fibonacci(int64_t n);

/* JSON */
AuValue au_json_parse(AuString* s);
AuString* au_json_stringify(AuValue v);

/* ============================================================
 * 内存管理
 * ============================================================ */
void* au_malloc(size_t size);
void* au_calloc(size_t nmemb, size_t size);
void* au_realloc(void* ptr, size_t size);
void  au_free(void* ptr);
void  au_mem_stats(size_t* allocated, size_t* count);

/* ============================================================
 * 程序入口辅助
 * ============================================================ */
void au_runtime_init(void);
void au_runtime_shutdown(void);

#ifdef __cplusplus
}
#endif

#endif /* AURORA_RT_H */
