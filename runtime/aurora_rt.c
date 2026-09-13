/*
 * Aurora Runtime Library Implementation
 */
#include "aurora_rt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <math.h>
#include <time.h>
#include <ctype.h>
#include <errno.h>

/* ============================================================
 * 内存管理(带统计)
 * ============================================================ */
static size_t g_allocated = 0;
static size_t g_alloc_count = 0;

void* au_malloc(size_t size) {
    void* p = malloc(size);
    if (!p) { fprintf(stderr, "aurora: out of memory (requested %zu bytes)\n", size); exit(1); }
    g_allocated += size;
    g_alloc_count++;
    return p;
}

void* au_calloc(size_t nmemb, size_t size) {
    void* p = calloc(nmemb, size);
    if (!p) { fprintf(stderr, "aurora: out of memory\n"); exit(1); }
    g_allocated += nmemb * size;
    g_alloc_count++;
    return p;
}

void* au_realloc(void* ptr, size_t size) {
    void* p = realloc(ptr, size);
    if (!p) { fprintf(stderr, "aurora: out of memory\n"); exit(1); }
    return p;
}

void au_free(void* ptr) {
    free(ptr);
}

void au_mem_stats(size_t* allocated, size_t* count) {
    if (allocated) *allocated = g_allocated;
    if (count) *count = g_alloc_count;
}

/* ============================================================
 * 字符串实现
 * ============================================================ */
AuString* au_string_new_len(const char* s, size_t len) {
    AuString* str = (AuString*)au_malloc(sizeof(AuString));
    str->data = (char*)au_malloc(len + 1);
    memcpy(str->data, s, len);
    str->data[len] = '\0';
    str->len = len;
    str->owned = true;
    return str;
}

AuString* au_string_new(const char* s) {
    return au_string_new_len(s, strlen(s));
}

AuString* au_string_from_literal(const char* s) {
    AuString* str = (AuString*)au_malloc(sizeof(AuString));
    str->data = (char*)s;
    str->len = strlen(s);
    str->owned = false;
    return str;
}

AuString* au_string_concat(AuString* a, AuString* b) {
    size_t len = a->len + b->len;
    char* buf = (char*)au_malloc(len + 1);
    memcpy(buf, a->data, a->len);
    memcpy(buf + a->len, b->data, b->len);
    buf[len] = '\0';
    AuString* s = (AuString*)au_malloc(sizeof(AuString));
    s->data = buf; s->len = len; s->owned = true;
    return s;
}

AuString* au_string_format(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    va_list args2;
    va_copy(args2, args);
    int len = vsnprintf(NULL, 0, fmt, args);
    va_end(args);
    char* buf = (char*)au_malloc(len + 1);
    vsnprintf(buf, len + 1, fmt, args2);
    va_end(args2);
    AuString* s = (AuString*)au_malloc(sizeof(AuString));
    s->data = buf; s->len = len; s->owned = true;
    return s;
}

bool au_string_eq(AuString* a, AuString* b) {
    if (a->len != b->len) return false;
    return memcmp(a->data, b->data, a->len) == 0;
}

int au_string_cmp(AuString* a, AuString* b) {
    size_t min_len = a->len < b->len ? a->len : b->len;
    int r = memcmp(a->data, b->data, min_len);
    if (r != 0) return r;
    if (a->len < b->len) return -1;
    if (a->len > b->len) return 1;
    return 0;
}

AuString* au_string_substring(AuString* s, int64_t start, int64_t end) {
    if (start < 0) start = 0;
    if (end > (int64_t)s->len) end = s->len;
    if (start >= end) return au_string_new("");
    return au_string_new_len(s->data + start, end - start);
}

AuString* au_string_replace(AuString* s, AuString* from, AuString* to) {
    if (from->len == 0) return au_string_new_len(s->data, s->len);
    size_t cap = s->len + 16;
    char* buf = (char*)au_malloc(cap);
    size_t pos = 0;
    size_t i = 0;
    while (i + from->len <= s->len) {
        if (memcmp(s->data + i, from->data, from->len) == 0) {
            if (pos + to->len + 1 > cap) { cap *= 2; buf = au_realloc(buf, cap); }
            memcpy(buf + pos, to->data, to->len);
            pos += to->len;
            i += from->len;
        } else {
            if (pos + 2 > cap) { cap *= 2; buf = au_realloc(buf, cap); }
            buf[pos++] = s->data[i++];
        }
    }
    while (i < s->len) {
        if (pos + 2 > cap) { cap *= 2; buf = au_realloc(buf, cap); }
        buf[pos++] = s->data[i++];
    }
    buf[pos] = '\0';
    AuString* result = (AuString*)au_malloc(sizeof(AuString));
    result->data = buf; result->len = pos; result->owned = true;
    return result;
}

AuString* au_string_to_lower(AuString* s) {
    char* buf = (char*)au_malloc(s->len + 1);
    for (size_t i = 0; i < s->len; i++) buf[i] = tolower((unsigned char)s->data[i]);
    buf[s->len] = '\0';
    AuString* r = (AuString*)au_malloc(sizeof(AuString));
    r->data = buf; r->len = s->len; r->owned = true;
    return r;
}

AuString* au_string_to_upper(AuString* s) {
    char* buf = (char*)au_malloc(s->len + 1);
    for (size_t i = 0; i < s->len; i++) buf[i] = toupper((unsigned char)s->data[i]);
    buf[s->len] = '\0';
    AuString* r = (AuString*)au_malloc(sizeof(AuString));
    r->data = buf; r->len = s->len; r->owned = true;
    return r;
}

AuString* au_string_trim(AuString* s) {
    size_t start = 0, end = s->len;
    while (start < end && isspace((unsigned char)s->data[start])) start++;
    while (end > start && isspace((unsigned char)s->data[end-1])) end--;
    return au_string_new_len(s->data + start, end - start);
}

AuArray* au_string_split(AuString* s, AuString* sep) {
    AuArray* arr = au_array_new();
    if (sep->len == 0) {
        for (size_t i = 0; i < s->len; i++) {
            au_array_push(arr, (AuValue){.type=AU_STRING, .as.s=au_string_new_len(s->data+i, 1)});
        }
        return arr;
    }
    size_t i = 0;
    while (i + sep->len <= s->len) {
        if (memcmp(s->data + i, sep->data, sep->len) == 0) {
            au_array_push(arr, (AuValue){.type=AU_STRING, .as.s=au_string_new_len(s->data, i)});
            s->data += i + sep->len; s->len -= i + sep->len; i = 0;
        } else {
            i++;
        }
    }
    au_array_push(arr, (AuValue){.type=AU_STRING, .as.s=au_string_new_len(s->data, s->len)});
    return arr;
}

bool au_string_contains(AuString* s, AuString* sub) {
    if (sub->len > s->len) return false;
    for (size_t i = 0; i + sub->len <= s->len; i++) {
        if (memcmp(s->data + i, sub->data, sub->len) == 0) return true;
    }
    return false;
}

bool au_string_starts_with(AuString* s, AuString* prefix) {
    if (prefix->len > s->len) return false;
    return memcmp(s->data, prefix->data, prefix->len) == 0;
}

bool au_string_ends_with(AuString* s, AuString* suffix) {
    if (suffix->len > s->len) return false;
    return memcmp(s->data + s->len - suffix->len, suffix->data, suffix->len) == 0;
}

int64_t au_string_to_int(AuString* s) {
    return strtoll(s->data, NULL, 10);
}

double au_string_to_float(AuString* s) {
    return strtod(s->data, NULL);
}

void au_string_free(AuString* s) {
    if (!s) return;
    if (s->owned && s->data) au_free(s->data);
    au_free(s);
}

/* ============================================================
 * 动态数组实现
 * ============================================================ */
AuArray* au_array_new(void) {
    AuArray* arr = (AuArray*)au_calloc(1, sizeof(AuArray));
    arr->cap = 8;
    arr->data = (AuValue*)au_calloc(arr->cap, sizeof(AuValue));
    return arr;
}

AuArray* au_array_with_capacity(size_t cap) {
    AuArray* arr = (AuArray*)au_calloc(1, sizeof(AuArray));
    arr->cap = cap > 0 ? cap : 8;
    arr->data = (AuValue*)au_calloc(arr->cap, sizeof(AuValue));
    return arr;
}

AuArray* au_array_from_values(AuValue* vals, size_t n) {
    AuArray* arr = au_array_with_capacity(n);
    for (size_t i = 0; i < n; i++) arr->data[i] = vals[i];
    arr->len = n;
    return arr;
}

static void au_array_grow(AuArray* arr) {
    arr->cap *= 2;
    arr->data = (AuValue*)au_realloc(arr->data, arr->cap * sizeof(AuValue));
}

void au_array_push(AuArray* arr, AuValue val) {
    if (arr->len >= arr->cap) au_array_grow(arr);
    arr->data[arr->len++] = val;
}

AuValue au_array_pop(AuArray* arr) {
    if (arr->len == 0) return AU_NIL_VAL();
    return arr->data[--arr->len];
}

AuValue au_array_get(AuArray* arr, int64_t idx) {
    if (idx < 0) idx += arr->len;
    if (idx < 0 || idx >= (int64_t)arr->len) return AU_NIL_VAL();
    return arr->data[idx];
}

void au_array_set(AuArray* arr, int64_t idx, AuValue val) {
    if (idx < 0) idx += arr->len;
    if (idx < 0 || idx >= (int64_t)arr->len) return;
    arr->data[idx] = val;
}

void au_array_insert(AuArray* arr, int64_t idx, AuValue val) {
    if (idx < 0) idx += arr->len;
    if (idx < 0) idx = 0;
    if (idx > (int64_t)arr->len) idx = arr->len;
    if (arr->len >= arr->cap) au_array_grow(arr);
    for (size_t i = arr->len; i > (size_t)idx; i--) arr->data[i] = arr->data[i-1];
    arr->data[idx] = val;
    arr->len++;
}

void au_array_remove(AuArray* arr, int64_t idx) {
    if (idx < 0) idx += arr->len;
    if (idx < 0 || idx >= (int64_t)arr->len) return;
    for (size_t i = idx; i + 1 < arr->len; i++) arr->data[i] = arr->data[i+1];
    arr->len--;
}

bool au_array_contains(AuArray* arr, AuValue val) {
    for (size_t i = 0; i < arr->len; i++) {
        if (au_value_eq(arr->data[i], val)) return true;
    }
    return false;
}

int64_t au_array_index_of(AuArray* arr, AuValue val) {
    for (size_t i = 0; i < arr->len; i++) {
        if (au_value_eq(arr->data[i], val)) return (int64_t)i;
    }
    return -1;
}

void au_array_reverse(AuArray* arr) {
    for (size_t i = 0, j = arr->len - 1; i < j; i++, j--) {
        AuValue tmp = arr->data[i];
        arr->data[i] = arr->data[j];
        arr->data[j] = tmp;
    }
}

AuArray* au_array_slice(AuArray* arr, int64_t start, int64_t end) {
    if (start < 0) start += arr->len;
    if (end < 0) end += arr->len;
    if (start < 0) start = 0;
    if (end > (int64_t)arr->len) end = arr->len;
    AuArray* result = au_array_new();
    for (int64_t i = start; i < end; i++) au_array_push(result, arr->data[i]);
    return result;
}

AuArray* au_array_concat(AuArray* a, AuArray* b) {
    AuArray* result = au_array_with_capacity(a->len + b->len);
    for (size_t i = 0; i < a->len; i++) result->data[i] = a->data[i];
    for (size_t i = 0; i < b->len; i++) result->data[a->len + i] = b->data[i];
    result->len = a->len + b->len;
    return result;
}

static int au_value_cmp_qsort(const void* a, const void* b) {
    return au_value_cmp(*(const AuValue*)a, *(const AuValue*)b);
}

void au_array_sort(AuArray* arr) {
    qsort(arr->data, arr->len, sizeof(AuValue), au_value_cmp_qsort);
}

void au_array_free(AuArray* arr) {
    if (!arr) return;
    for (size_t i = 0; i < arr->len; i++) au_value_free(arr->data[i]);
    au_free(arr->data);
    au_free(arr);
}

/* ============================================================
 * 哈希表实现(开放寻址,字符串键)
 * ============================================================ */
static size_t au_hash_string(AuString* key) {
    size_t h = 5381;
    for (size_t i = 0; i < key->len; i++) h = ((h << 5) + h) + (unsigned char)key->data[i];
    return h;
}

AuMap* au_map_new(void) {
    return au_map_with_capacity(16);
}

AuMap* au_map_with_capacity(size_t cap) {
    AuMap* map = (AuMap*)au_calloc(1, sizeof(AuMap));
    map->cap = cap;
    map->entries = (AuMapEntry*)au_calloc(cap, sizeof(AuMapEntry));
    return map;
}

static void au_map_resize(AuMap* map, size_t new_cap) {
    AuMapEntry* old = map->entries;
    size_t old_cap = map->cap;
    map->entries = (AuMapEntry*)au_calloc(new_cap, sizeof(AuMapEntry));
    map->cap = new_cap;
    map->len = 0;
    for (size_t i = 0; i < old_cap; i++) {
        if (old[i].occupied) {
            au_map_set(map, old[i].key, old[i].value);
        }
    }
    au_free(old);
}

void au_map_set(AuMap* map, AuString* key, AuValue val) {
    if (map->len * 4 >= map->cap * 3) au_map_resize(map, map->cap * 2);
    size_t idx = au_hash_string(key) % map->cap;
    while (map->entries[idx].occupied) {
        if (au_string_eq(map->entries[idx].key, key)) {
            au_value_free(map->entries[idx].value);
            map->entries[idx].value = val;
            return;
        }
        idx = (idx + 1) % map->cap;
    }
    map->entries[idx].key = key;
    map->entries[idx].value = val;
    map->entries[idx].occupied = true;
    map->len++;
}

AuValue au_map_get(AuMap* map, AuString* key) {
    size_t idx = au_hash_string(key) % map->cap;
    size_t probes = 0;
    while (map->entries[idx].occupied && probes < map->cap) {
        if (au_string_eq(map->entries[idx].key, key)) return map->entries[idx].value;
        idx = (idx + 1) % map->cap;
        probes++;
    }
    return AU_NIL_VAL();
}

bool au_map_has(AuMap* map, AuString* key) {
    size_t idx = au_hash_string(key) % map->cap;
    size_t probes = 0;
    while (map->entries[idx].occupied && probes < map->cap) {
        if (au_string_eq(map->entries[idx].key, key)) return true;
        idx = (idx + 1) % map->cap;
        probes++;
    }
    return false;
}

void au_map_remove(AuMap* map, AuString* key) {
    size_t idx = au_hash_string(key) % map->cap;
    size_t probes = 0;
    while (map->entries[idx].occupied && probes < map->cap) {
        if (au_string_eq(map->entries[idx].key, key)) {
            au_string_free(map->entries[idx].key);
            au_value_free(map->entries[idx].value);
            map->entries[idx].occupied = false;
            map->len--;
            return;
        }
        idx = (idx + 1) % map->cap;
        probes++;
    }
}

AuArray* au_map_keys(AuMap* map) {
    AuArray* arr = au_array_new();
    for (size_t i = 0; i < map->cap; i++) {
        if (map->entries[i].occupied) {
            au_array_push(arr, (AuValue){.type=AU_STRING, .as.s=au_string_new_len(map->entries[i].key->data, map->entries[i].key->len)});
        }
    }
    return arr;
}

AuArray* au_map_values(AuMap* map) {
    AuArray* arr = au_array_new();
    for (size_t i = 0; i < map->cap; i++) {
        if (map->entries[i].occupied) au_array_push(arr, au_value_clone(map->entries[i].value));
    }
    return arr;
}

void au_map_free(AuMap* map) {
    if (!map) return;
    for (size_t i = 0; i < map->cap; i++) {
        if (map->entries[i].occupied) {
            au_string_free(map->entries[i].key);
            au_value_free(map->entries[i].value);
        }
    }
    au_free(map->entries);
    au_free(map);
}

/* ============================================================
 * 值操作
 * ============================================================ */
AuValue au_value_clone(AuValue v) {
    switch (v.type) {
        case AU_STRING: return (AuValue){.type=AU_STRING, .as.s=au_string_new_len(v.as.s->data, v.as.s->len)};
        case AU_ARRAY: {
            AuArray* arr = au_array_with_capacity(v.as.arr->len);
            for (size_t i = 0; i < v.as.arr->len; i++) au_array_push(arr, au_value_clone(v.as.arr->data[i]));
            return (AuValue){.type=AU_ARRAY, .as.arr=arr};
        }
        case AU_MAP: {
            AuMap* map = au_map_with_capacity(v.as.map->cap);
            for (size_t i = 0; i < v.as.map->cap; i++) {
                if (v.as.map->entries[i].occupied) {
                    au_map_set(map, au_string_new_len(v.as.map->entries[i].key->data, v.as.map->entries[i].key->len), au_value_clone(v.as.map->entries[i].value));
                }
            }
            return (AuValue){.type=AU_MAP, .as.map=map};
        }
        default: return v;
    }
}

void au_value_free(AuValue v) {
    switch (v.type) {
        case AU_STRING: au_string_free(v.as.s); break;
        case AU_ARRAY: au_array_free(v.as.arr); break;
        case AU_MAP: au_map_free(v.as.map); break;
        default: break;
    }
}

bool au_value_eq(AuValue a, AuValue b) {
    if (a.type != b.type) {
        /* int 和 float 可以比较 */
        if (a.type == AU_INT && b.type == AU_FLOAT) return (double)a.as.i == b.as.f;
        if (a.type == AU_FLOAT && b.type == AU_INT) return a.as.f == (double)b.as.i;
        return false;
    }
    switch (a.type) {
        case AU_NIL: return true;
        case AU_INT: return a.as.i == b.as.i;
        case AU_FLOAT: return a.as.f == b.as.f;
        case AU_BOOL: return a.as.b == b.as.b;
        case AU_STRING: return au_string_eq(a.as.s, b.as.s);
        case AU_ARRAY: {
            if (a.as.arr->len != b.as.arr->len) return false;
            for (size_t i = 0; i < a.as.arr->len; i++) if (!au_value_eq(a.as.arr->data[i], b.as.arr->data[i])) return false;
            return true;
        }
        default: return false;
    }
}

int au_value_cmp(AuValue a, AuValue b) {
    if (a.type == AU_INT && b.type == AU_INT) return (a.as.i > b.as.i) - (a.as.i < b.as.i);
    if ((a.type == AU_INT || a.type == AU_FLOAT) && (b.type == AU_INT || b.type == AU_FLOAT)) {
        double da = a.type == AU_INT ? (double)a.as.i : a.as.f;
        double db = b.type == AU_INT ? (double)b.as.i : b.as.f;
        return (da > db) - (da < db);
    }
    if (a.type == AU_STRING && b.type == AU_STRING) return au_string_cmp(a.as.s, b.as.s);
    if (a.type == AU_BOOL && b.type == AU_BOOL) return (a.as.b > b.as.b) - (a.as.b < b.as.b);
    return 0;
}

AuString* au_value_to_string(AuValue v) {
    switch (v.type) {
        case AU_NIL: return au_string_from_literal("nil");
        case AU_INT: return au_string_format("%lld", (long long)v.as.i);
        case AU_FLOAT: return au_string_format("%g", v.as.f);
        case AU_BOOL: return au_string_from_literal(v.as.b ? "true" : "false");
        case AU_STRING: return au_string_new_len(v.as.s->data, v.as.s->len);
        case AU_ARRAY: {
            AuString* result = au_string_from_literal("[");
            for (size_t i = 0; i < v.as.arr->len; i++) {
                if (i > 0) { AuString* tmp = au_string_concat(result, au_string_from_literal(", ")); au_string_free(result); result = tmp; }
                AuString* elem = au_value_to_string(v.as.arr->data[i]);
                AuString* tmp = au_string_concat(result, elem); au_string_free(result); au_string_free(elem); result = tmp;
            }
            AuString* tmp = au_string_concat(result, au_string_from_literal("]")); au_string_free(result); result = tmp;
            return result;
        }
        case AU_MAP: {
            AuString* result = au_string_from_literal("{");
            bool first = true;
            for (size_t i = 0; i < v.as.map->cap; i++) {
                if (v.as.map->entries[i].occupied) {
                    if (!first) { AuString* tmp = au_string_concat(result, au_string_from_literal(", ")); au_string_free(result); result = tmp; }
                    first = false;
                    AuString* k = au_string_format("\"%s\"", v.as.map->entries[i].key->data);
                    AuString* tmp = au_string_concat(result, k); au_string_free(result); au_string_free(k); result = tmp;
                    tmp = au_string_concat(result, au_string_from_literal(": ")); au_string_free(result); result = tmp;
                    AuString* val = au_value_to_string(v.as.map->entries[i].value);
                    tmp = au_string_concat(result, val); au_string_free(result); au_string_free(val); result = tmp;
                }
            }
            AuString* tmp = au_string_concat(result, au_string_from_literal("}")); au_string_free(result); result = tmp;
            return result;
        }
    }
    return au_string_from_literal("?");
}

AuString* au_value_type_name(AuValue v) {
    switch (v.type) {
        case AU_NIL: return au_string_from_literal("nil");
        case AU_INT: return au_string_from_literal("int");
        case AU_FLOAT: return au_string_from_literal("float");
        case AU_BOOL: return au_string_from_literal("bool");
        case AU_STRING: return au_string_from_literal("string");
        case AU_ARRAY: return au_string_from_literal("array");
        case AU_MAP: return au_string_from_literal("map");
    }
    return au_string_from_literal("unknown");
}

bool au_value_truthy(AuValue v) {
    switch (v.type) {
        case AU_NIL: return false;
        case AU_BOOL: return v.as.b;
        case AU_INT: return v.as.i != 0;
        case AU_FLOAT: return v.as.f != 0.0;
        case AU_STRING: return v.as.s->len > 0;
        case AU_ARRAY: return v.as.arr->len > 0;
        case AU_MAP: return v.as.map->len > 0;
    }
    return false;
}

/* ============================================================
 * 算术运算
 * ============================================================ */
AuValue au_add(AuValue a, AuValue b) {
    if (a.type == AU_STRING || b.type == AU_STRING) {
        AuString* sa = au_value_to_string(a);
        AuString* sb = au_value_to_string(b);
        AuString* r = au_string_concat(sa, sb);
        if (a.type != AU_STRING) au_string_free(sa);
        if (b.type != AU_STRING) au_string_free(sb);
        return (AuValue){.type=AU_STRING, .as.s=r};
    }
    if (a.type == AU_ARRAY && b.type == AU_ARRAY) return (AuValue){.type=AU_ARRAY, .as.arr=au_array_concat(a.as.arr, b.as.arr)};
    if (a.type == AU_FLOAT || b.type == AU_FLOAT) {
        double da = a.type == AU_INT ? (double)a.as.i : a.as.f;
        double db = b.type == AU_INT ? (double)b.as.i : b.as.f;
        return AU_FLOAT_VAL(da + db);
    }
    return AU_INT_VAL(a.as.i + b.as.i);
}

AuValue au_sub(AuValue a, AuValue b) {
    if (a.type == AU_FLOAT || b.type == AU_FLOAT) {
        double da = a.type == AU_INT ? (double)a.as.i : a.as.f;
        double db = b.type == AU_INT ? (double)b.as.i : b.as.f;
        return AU_FLOAT_VAL(da - db);
    }
    return AU_INT_VAL(a.as.i - b.as.i);
}

AuValue au_mul(AuValue a, AuValue b) {
    if (a.type == AU_STRING && b.type == AU_INT) {
        AuString* result = au_string_new("");
        for (int64_t i = 0; i < b.as.i; i++) { AuString* tmp = au_string_concat(result, a.as.s); au_string_free(result); result = tmp; }
        return (AuValue){.type=AU_STRING, .as.s=result};
    }
    if (b.type == AU_STRING && a.type == AU_INT) return au_mul(b, a);
    if (a.type == AU_FLOAT || b.type == AU_FLOAT) {
        double da = a.type == AU_INT ? (double)a.as.i : a.as.f;
        double db = b.type == AU_INT ? (double)b.as.i : b.as.f;
        return AU_FLOAT_VAL(da * db);
    }
    return AU_INT_VAL(a.as.i * b.as.i);
}

AuValue au_div(AuValue a, AuValue b) {
    if (a.type == AU_INT && b.type == AU_INT && b.as.i != 0) return AU_INT_VAL(a.as.i / b.as.i);
    double da = a.type == AU_INT ? (double)a.as.i : a.as.f;
    double db = b.type == AU_INT ? (double)b.as.i : b.as.f;
    if (db == 0) { fprintf(stderr, "aurora: division by zero\n"); exit(1); }
    return AU_FLOAT_VAL(da / db);
}

AuValue au_mod(AuValue a, AuValue b) {
    if (b.type == AU_INT && b.as.i == 0) { fprintf(stderr, "aurora: modulo by zero\n"); exit(1); }
    return AU_INT_VAL(a.as.i % b.as.i);
}

AuValue au_pow(AuValue a, AuValue b) {
    double da = a.type == AU_INT ? (double)a.as.i : a.as.f;
    double db = b.type == AU_INT ? (double)b.as.i : b.as.f;
    double r = pow(da, db);
    if (a.type == AU_INT && b.type == AU_INT && r == floor(r)) return AU_INT_VAL((int64_t)r);
    return AU_FLOAT_VAL(r);
}

AuValue au_neg(AuValue a) {
    if (a.type == AU_INT) return AU_INT_VAL(-a.as.i);
    if (a.type == AU_FLOAT) return AU_FLOAT_VAL(-a.as.f);
    return a;
}

/* 比较运算 */
bool au_lt(AuValue a, AuValue b) { return au_value_cmp(a, b) < 0; }
bool au_le(AuValue a, AuValue b) { return au_value_cmp(a, b) <= 0; }
bool au_gt(AuValue a, AuValue b) { return au_value_cmp(a, b) > 0; }
bool au_ge(AuValue a, AuValue b) { return au_value_cmp(a, b) >= 0; }

/* 逻辑运算 */
bool au_and(AuValue a, AuValue b) { return au_value_truthy(a) && au_value_truthy(b); }
bool au_or(AuValue a, AuValue b) { return au_value_truthy(a) || au_value_truthy(b); }
bool au_not(AuValue a) { return !au_value_truthy(a); }

/* ============================================================
 * 内置函数
 * ============================================================ */
void au_print(AuValue v) {
    AuString* s = au_value_to_string(v);
    fwrite(s->data, 1, s->len, stdout);
    if (s->owned) au_string_free(s);
}

void au_println(AuValue v) {
    au_print(v);
    putchar('\n');
}

int64_t au_len(AuValue v) {
    switch (v.type) {
        case AU_STRING: return v.as.s->len;
        case AU_ARRAY: return v.as.arr->len;
        case AU_MAP: return v.as.map->len;
        default: return 0;
    }
}

AuValue au_range(int64_t start, int64_t end) {
    AuArray* arr = au_array_new();
    for (int64_t i = start; i <= end; i++) au_array_push(arr, AU_INT_VAL(i));
    return (AuValue){.type=AU_ARRAY, .as.arr=arr};
}

AuValue au_read_line(void) {
    char* line = NULL;
    size_t cap = 0;
    ssize_t len = getline(&line, &cap, stdin);
    if (len < 0) return AU_NIL_VAL();
    while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = '\0';
    AuString* s = au_string_new_len(line, len);
    free(line);
    return (AuValue){.type=AU_STRING, .as.s=s};
}

AuValue au_read_file(AuString* path) {
    FILE* f = fopen(path->data, "rb");
    if (!f) return AU_NIL_VAL();
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* buf = (char*)au_malloc(size + 1);
    fread(buf, 1, size, f);
    buf[size] = '\0';
    fclose(f);
    AuString* s = (AuString*)au_malloc(sizeof(AuString));
    s->data = buf; s->len = size; s->owned = true;
    return (AuValue){.type=AU_STRING, .as.s=s};
}

void au_write_file(AuString* path, AuString* content) {
    FILE* f = fopen(path->data, "wb");
    if (!f) { fprintf(stderr, "aurora: cannot write %s: %s\n", path->data, strerror(errno)); return; }
    fwrite(content->data, 1, content->len, f);
    fclose(f);
}

void au_append_file(AuString* path, AuString* content) {
    FILE* f = fopen(path->data, "ab");
    if (!f) return;
    fwrite(content->data, 1, content->len, f);
    fclose(f);
}

bool au_file_exists(AuString* path) {
    FILE* f = fopen(path->data, "r");
    if (f) { fclose(f); return true; }
    return false;
}

AuArray* au_list_dir(AuString* path) {
    /* 简单实现:用 popen 调 ls */
    AuArray* arr = au_array_new();
    char cmd[4096];
    snprintf(cmd, sizeof(cmd), "ls -1 '%s' 2>/dev/null", path->data);
    FILE* p = popen(cmd, "r");
    if (!p) return arr;
    char line[4096];
    while (fgets(line, sizeof(line), p)) {
        size_t len = strlen(line);
        while (len > 0 && line[len-1] == '\n') line[--len] = '\0';
        if (len > 0) au_array_push(arr, (AuValue){.type=AU_STRING, .as.s=au_string_new(line)});
    }
    pclose(p);
    return arr;
}

void au_shell(AuString* cmd) {
    int ret = system(cmd->data);
    (void)ret;
}

AuValue au_get_env(AuString* name) {
    const char* v = getenv(name->data);
    if (!v) return AU_NIL_VAL();
    return (AuValue){.type=AU_STRING, .as.s=au_string_new(v)};
}

void au_set_env(AuString* name, AuString* value) {
    setenv(name->data, value->data, 1);
}

int64_t au_now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return (int64_t)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

void au_sleep_ms(int64_t ms) {
    struct timespec ts;
    ts.tv_sec = ms / 1000;
    ts.tv_nsec = (ms % 1000) * 1000000;
    nanosleep(&ts, NULL);
}

/* 数学函数 */
double au_sqrt(double x) { return sqrt(x); }
double au_abs(double x) { return fabs(x); }
double au_sin(double x) { return sin(x); }
double au_cos(double x) { return cos(x); }
double au_tan(double x) { return tan(x); }
double au_log(double x) { return log(x); }
double au_exp(double x) { return exp(x); }
double au_floor(double x) { return floor(x); }
double au_ceil(double x) { return ceil(x); }
double au_round(double x) { return round(x); }
double au_min(double a, double b) { return a < b ? a : b; }
double au_max(double a, double b) { return a > b ? a : b; }

int64_t au_gcd(int64_t a, int64_t b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) { int64_t t = b; b = a % b; a = t; }
    return a;
}

int64_t au_lcm(int64_t a, int64_t b) {
    if (a == 0 || b == 0) return 0;
    return (a / au_gcd(a, b)) * b;
}

bool au_is_prime(int64_t n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0) return false;
    for (int64_t i = 3; i * i <= n; i += 2) if (n % i == 0) return false;
    return true;
}

int64_t au_factorial(int64_t n) {
    if (n < 0) return 0;
    int64_t r = 1;
    for (int64_t i = 2; i <= n; i++) r *= i;
    return r;
}

int64_t au_fibonacci(int64_t n) {
    if (n < 0) return 0;
    if (n < 2) return n;
    int64_t a = 0, b = 1;
    for (int64_t i = 2; i <= n; i++) { int64_t t = a + b; a = b; b = t; }
    return b;
}

/* int 幂运算(用于类型特化代码) */
int64_t _aurora_pow_int(int64_t base, int64_t exp) {
    if (exp < 0) return 0;
    int64_t result = 1;
    while (exp > 0) {
        if (exp & 1) result *= base;
        base *= base;
        exp >>= 1;
    }
    return result;
}

/* ============================================================
 * JSON 解析与序列化(递归下降)
 * ============================================================ */
typedef struct {
    const char* p;
    const char* end;
} JsonParser;

static void json_skip_ws(JsonParser* jp) {
    while (jp->p < jp->end && (*jp->p == ' ' || *jp->p == '\t' || *jp->p == '\n' || *jp->p == '\r')) jp->p++;
}

static AuValue json_parse_value(JsonParser* jp);

static AuValue json_parse_string(JsonParser* jp) {
    jp->p++; /* skip " */
    const char* start = jp->p;
    char* buf = (char*)au_malloc(jp->end - start + 1);
    size_t len = 0;
    while (jp->p < jp->end && *jp->p != '"') {
        if (*jp->p == '\\' && jp->p + 1 < jp->end) {
            jp->p++;
            switch (*jp->p) {
                case 'n': buf[len++] = '\n'; break;
                case 't': buf[len++] = '\t'; break;
                case 'r': buf[len++] = '\r'; break;
                case '"': buf[len++] = '"'; break;
                case '\\': buf[len++] = '\\'; break;
                case '/': buf[len++] = '/'; break;
                default: buf[len++] = *jp->p; break;
            }
        } else {
            buf[len++] = *jp->p;
        }
        jp->p++;
    }
    if (jp->p < jp->end) jp->p++; /* skip " */
    buf[len] = '\0';
    AuString* s = (AuString*)au_malloc(sizeof(AuString));
    s->data = buf; s->len = len; s->owned = true;
    return (AuValue){.type=AU_STRING, .as.s=s};
}

static AuValue json_parse_number(JsonParser* jp) {
    const char* start = jp->p;
    bool is_float = false;
    while (jp->p < jp->end && (isdigit((unsigned char)*jp->p) || *jp->p == '-' || *jp->p == '+' || *jp->p == '.' || *jp->p == 'e' || *jp->p == 'E')) {
        if (*jp->p == '.' || *jp->p == 'e' || *jp->p == 'E') is_float = true;
        jp->p++;
    }
    char buf[64];
    size_t len = jp->p - start;
    if (len >= sizeof(buf)) len = sizeof(buf) - 1;
    memcpy(buf, start, len);
    buf[len] = '\0';
    if (is_float) return AU_FLOAT_VAL(strtod(buf, NULL));
    return AU_INT_VAL(strtoll(buf, NULL, 10));
}

static AuValue json_parse_array(JsonParser* jp) {
    jp->p++; /* skip [ */
    AuArray* arr = au_array_new();
    json_skip_ws(jp);
    if (jp->p < jp->end && *jp->p == ']') { jp->p++; return (AuValue){.type=AU_ARRAY, .as.arr=arr}; }
    while (jp->p < jp->end) {
        json_skip_ws(jp);
        au_array_push(arr, json_parse_value(jp));
        json_skip_ws(jp);
        if (jp->p < jp->end && *jp->p == ',') { jp->p++; continue; }
        if (jp->p < jp->end && *jp->p == ']') { jp->p++; break; }
        break;
    }
    return (AuValue){.type=AU_ARRAY, .as.arr=arr};
}

static AuValue json_parse_object(JsonParser* jp) {
    jp->p++; /* skip { */
    AuMap* map = au_map_new();
    json_skip_ws(jp);
    if (jp->p < jp->end && *jp->p == '}') { jp->p++; return (AuValue){.type=AU_MAP, .as.map=map}; }
    while (jp->p < jp->end) {
        json_skip_ws(jp);
        AuValue key = json_parse_string(jp);
        json_skip_ws(jp);
        if (jp->p < jp->end && *jp->p == ':') jp->p++;
        json_skip_ws(jp);
        AuValue val = json_parse_value(jp);
        au_map_set(map, key.as.s, val);
        json_skip_ws(jp);
        if (jp->p < jp->end && *jp->p == ',') { jp->p++; continue; }
        if (jp->p < jp->end && *jp->p == '}') { jp->p++; break; }
        break;
    }
    return (AuValue){.type=AU_MAP, .as.map=map};
}

static AuValue json_parse_value(JsonParser* jp) {
    json_skip_ws(jp);
    if (jp->p >= jp->end) return AU_NIL_VAL();
    char c = *jp->p;
    if (c == '"') return json_parse_string(jp);
    if (c == '[') return json_parse_array(jp);
    if (c == '{') return json_parse_object(jp);
    if (c == 't' && jp->p + 4 <= jp->end && strncmp(jp->p, "true", 4) == 0) { jp->p += 4; return AU_BOOL_VAL(true); }
    if (c == 'f' && jp->p + 5 <= jp->end && strncmp(jp->p, "false", 5) == 0) { jp->p += 5; return AU_BOOL_VAL(false); }
    if (c == 'n' && jp->p + 4 <= jp->end && strncmp(jp->p, "null", 4) == 0) { jp->p += 4; return AU_NIL_VAL(); }
    if (c == '-' || isdigit((unsigned char)c)) return json_parse_number(jp);
    return AU_NIL_VAL();
}

AuValue au_json_parse(AuString* s) {
    JsonParser jp = {.p = s->data, .end = s->data + s->len};
    return json_parse_value(&jp);
}

static void json_append_string(AuString** buf, AuString* s) {
    /* 简单实现:直接拼接,后续可优化 */
    AuString* quoted = au_string_format("\"%s\"", s->data);
    AuString* tmp = au_string_concat(*buf, quoted);
    au_string_free(*buf); au_string_free(quoted);
    *buf = tmp;
}

AuString* au_json_stringify(AuValue v) {
    switch (v.type) {
        case AU_NIL: return au_string_from_literal("null");
        case AU_BOOL: return au_string_from_literal(v.as.b ? "true" : "false");
        case AU_INT: return au_string_format("%lld", (long long)v.as.i);
        case AU_FLOAT: return au_string_format("%g", v.as.f);
        case AU_STRING: return au_string_format("\"%s\"", v.as.s->data);
        case AU_ARRAY: {
            AuString* result = au_string_from_literal("[");
            for (size_t i = 0; i < v.as.arr->len; i++) {
                if (i > 0) { AuString* tmp = au_string_concat(result, au_string_from_literal(",")); au_string_free(result); result = tmp; }
                AuString* elem = au_json_stringify(v.as.arr->data[i]);
                AuString* tmp = au_string_concat(result, elem); au_string_free(result); au_string_free(elem); result = tmp;
            }
            AuString* tmp = au_string_concat(result, au_string_from_literal("]")); au_string_free(result); result = tmp;
            return result;
        }
        case AU_MAP: {
            AuString* result = au_string_from_literal("{");
            bool first = true;
            for (size_t i = 0; i < v.as.map->cap; i++) {
                if (v.as.map->entries[i].occupied) {
                    if (!first) { AuString* tmp = au_string_concat(result, au_string_from_literal(",")); au_string_free(result); result = tmp; }
                    first = false;
                    AuString* k = au_string_format("\"%s\":", v.as.map->entries[i].key->data);
                    AuString* tmp = au_string_concat(result, k); au_string_free(result); au_string_free(k); result = tmp;
                    AuString* val = au_json_stringify(v.as.map->entries[i].value);
                    tmp = au_string_concat(result, val); au_string_free(result); au_string_free(val); result = tmp;
                }
            }
            AuString* tmp = au_string_concat(result, au_string_from_literal("}")); au_string_free(result); result = tmp;
            return result;
        }
    }
    return au_string_from_literal("null");
}

/* ============================================================
 * 运行时初始化/关闭
 * ============================================================ */
void au_runtime_init(void) { /* 预留 */ }
void au_runtime_shutdown(void) { /* 预留 */ }
