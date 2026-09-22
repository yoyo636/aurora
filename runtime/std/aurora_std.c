/*
 * Aurora 标准库 - C 语言原生实现
 * 绑定到 Aurora VM，提供真正可用的函数
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <time.h>

/* ========== 字符串操作 ========== */

int aurora_std_string_len(const char* s) {
    return (int)strlen(s);
}

char* aurora_std_string_upper(char* s) {
    for (char* p = s; *p; p++) *p = toupper((unsigned char)*p);
    return s;
}

char* aurora_std_string_lower(char* s) {
    for (char* p = s; *p; p++) *p = tolower((unsigned char)*p);
    return s;
}

char* aurora_std_string_trim(char* s) {
    char* start = s;
    while (*start && isspace((unsigned char)*start)) start++;
    if (start != s) memmove(s, start, strlen(start) + 1);
    int len = (int)strlen(s);
    while (len > 0 && isspace((unsigned char)s[len-1])) s[--len] = '\0';
    return s;
}

char* aurora_std_string_concat(const char* a, const char* b) {
    int la = (int)strlen(a), lb = (int)strlen(b);
    char* r = malloc(la + lb + 1);
    memcpy(r, a, la);
    memcpy(r + la, b, lb + 1);
    return r;
}

int aurora_std_string_contains(const char* s, const char* sub) {
    return strstr(s, sub) != NULL;
}

int aurora_std_string_index_of(const char* s, const char* sub) {
    char* p = strstr(s, sub);
    return p ? (int)(p - s) : -1;
}

int aurora_std_string_starts_with(const char* s, const char* prefix) {
    return strncmp(s, prefix, strlen(prefix)) == 0;
}

int aurora_std_string_ends_with(const char* s, const char* suffix) {
    int ls = (int)strlen(s), lf = (int)strlen(suffix);
    if (lf > ls) return 0;
    return strcmp(s + ls - lf, suffix) == 0;
}

char* aurora_std_string_reverse(char* s) {
    int len = (int)strlen(s);
    for (int i = 0; i < len / 2; i++) {
        char t = s[i]; s[i] = s[len-1-i]; s[len-1-i] = t;
    }
    return s;
}

char* aurora_std_string_repeat(const char* s, int n) {
    if (n <= 0) { char* r = malloc(1); r[0] = '\0'; return r; }
    int len = (int)strlen(s);
    char* r = malloc(len * n + 1);
    for (int i = 0; i < n; i++) memcpy(r + i * len, s, len);
    r[len * n] = '\0';
    return r;
}

int aurora_std_string_count(const char* s, const char* sub) {
    int count = 0, sublen = (int)strlen(sub);
    const char* p = s;
    while ((p = strstr(p, sub)) != NULL) { count++; p += sublen; }
    return count;
}

char* aurora_std_string_replace(const char* s, const char* old, const char* new) {
    int count = aurora_std_string_count(s, old);
    if (count == 0) return strdup(s);
    int oldlen = (int)strlen(old), newlen = (int)strlen(new);
    int result_len = (int)strlen(s) + count * (newlen - oldlen);
    char* result = malloc(result_len + 1);
    char* dst = result;
    const char* p = s;
    while (*p) {
        if (strncmp(p, old, oldlen) == 0) {
            memcpy(dst, new, newlen);
            dst += newlen;
            p += oldlen;
        } else {
            *dst++ = *p++;
        }
    }
    *dst = '\0';
    return result;
}

/* ========== 数学函数 ========== */

double aurora_std_math_abs(double x) { return fabs(x); }
double aurora_std_math_min(double a, double b) { return a < b ? a : b; }
double aurora_std_math_max(double a, double b) { return a > b ? a : b; }
double aurora_std_math_floor(double x) { return floor(x); }
double aurora_std_math_ceil(double x) { return ceil(x); }
double aurora_std_math_round(double x) { return round(x); }
double aurora_std_math_sqrt(double x) { return sqrt(x); }
double aurora_std_math_pow(double x, double y) { return pow(x, y); }
double aurora_std_math_exp(double x) { return exp(x); }
double aurora_std_math_log(double x) { return log(x); }
double aurora_std_math_log2(double x) { return log2(x); }
double aurora_std_math_log10(double x) { return log10(x); }
double aurora_std_math_sin(double x) { return sin(x); }
double aurora_std_math_cos(double x) { return cos(x); }
double aurora_std_math_tan(double x) { return tan(x); }
double aurora_std_math_asin(double x) { return asin(x); }
double aurora_std_math_acos(double x) { return acos(x); }
double aurora_std_math_atan(double x) { return atan(x); }
double aurora_std_math_atan2(double y, double x) { return atan2(y, x); }
double aurora_std_math_hypot(double x, double y) { return hypot(x, y); }
double aurora_std_math_clamp(double x, double min, double max) { return x < min ? min : (x > max ? max : x); }
double aurora_std_math_lerp(double a, double b, double t) { return a + (b - a) * t; }

long long aurora_std_math_factorial(int n) {
    if (n < 0) return -1;
    long long r = 1;
    for (int i = 2; i <= n; i++) r *= i;
    return r;
}

long long aurora_std_math_gcd(long long a, long long b) {
    a = llabs(a); b = llabs(b);
    while (b) { long long t = b; b = a % b; a = t; }
    return a;
}

long long aurora_std_math_lcm(long long a, long long b) {
    if (a == 0 || b == 0) return 0;
    return llabs(a / aurora_std_math_gcd(a, b) * b);
}

/* ========== 随机数 ========== */

static int rand_initialized = 0;

void aurora_std_random_seed(unsigned int seed) {
    srand(seed);
    rand_initialized = 1;
}

int aurora_std_random_int(int min, int max) {
    if (!rand_initialized) { srand((unsigned int)time(NULL)); rand_initialized = 1; }
    if (min > max) { int t = min; min = max; max = t; }
    return min + rand() % (max - min + 1);
}

double aurora_std_random_double() {
    if (!rand_initialized) { srand((unsigned int)time(NULL)); rand_initialized = 1; }
    return (double)rand() / RAND_MAX;
}

/* ========== 时间 ========== */

long long aurora_std_time_now() {
    return (long long)time(NULL);
}

long long aurora_std_time_millis() {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return (long long)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

void aurora_std_time_sleep(int ms) {
    struct timespec ts = { ms / 1000, (ms % 1000) * 1000000 };
    nanosleep(&ts, NULL);
}

/* ========== 控制台输出 ========== */

void aurora_std_print_int(int x) { printf("%d", x); }
void aurora_std_print_double(double x) { printf("%g", x); }
void aurora_std_print_string(const char* s) { printf("%s", s); }
void aurora_std_println() { printf("\n"); }

/* ========== 列表（动态数组） ========== */

typedef struct {
    void** data;
    int size;
    int capacity;
} AuroraList;

AuroraList* aurora_std_list_create() {
    AuroraList* list = malloc(sizeof(AuroraList));
    list->data = NULL;
    list->size = 0;
    list->capacity = 0;
    return list;
}

void aurora_std_list_push(AuroraList* list, void* item) {
    if (list->size >= list->capacity) {
        list->capacity = list->capacity ? list->capacity * 2 : 4;
        list->data = realloc(list->data, list->capacity * sizeof(void*));
    }
    list->data[list->size++] = item;
}

void* aurora_std_list_pop(AuroraList* list) {
    if (list->size == 0) return NULL;
    return list->data[--list->size];
}

void* aurora_std_list_get(AuroraList* list, int index) {
    if (index < 0 || index >= list->size) return NULL;
    return list->data[index];
}

void aurora_std_list_set(AuroraList* list, int index, void* item) {
    if (index >= 0 && index < list->size) list->data[index] = item;
}

int aurora_std_list_length(AuroraList* list) { return list->size; }

int aurora_std_list_contains(AuroraList* list, void* item) {
    for (int i = 0; i < list->size; i++) if (list->data[i] == item) return 1;
    return 0;
}

void aurora_std_list_reverse(AuroraList* list) {
    for (int i = 0; i < list->size / 2; i++) {
        void* t = list->data[i];
        list->data[i] = list->data[list->size-1-i];
        list->data[list->size-1-i] = t;
    }
}

void aurora_std_list_clear(AuroraList* list) { list->size = 0; }

void aurora_std_list_destroy(AuroraList* list) {
    free(list->data);
    free(list);
}

/* ========== 字典（哈希表） ========== */

typedef struct DictEntry {
    char* key;
    void* value;
    struct DictEntry* next;
} DictEntry;

typedef struct {
    DictEntry** buckets;
    int size;
    int capacity;
} AuroraDict;

static unsigned int dict_hash(const char* key) {
    unsigned int h = 5381;
    while (*key) h = ((h << 5) + h) + (unsigned char)*key++;
    return h;
}

AuroraDict* aurora_std_dict_create() {
    AuroraDict* dict = malloc(sizeof(AuroraDict));
    dict->capacity = 16;
    dict->size = 0;
    dict->buckets = calloc(dict->capacity, sizeof(DictEntry*));
    return dict;
}

void aurora_std_dict_set(AuroraDict* dict, const char* key, void* value) {
    unsigned int h = dict_hash(key) % dict->capacity;
    DictEntry* e = dict->buckets[h];
    while (e) {
        if (strcmp(e->key, key) == 0) { e->value = value; return; }
        e = e->next;
    }
    e = malloc(sizeof(DictEntry));
    e->key = strdup(key);
    e->value = value;
    e->next = dict->buckets[h];
    dict->buckets[h] = e;
    dict->size++;
}

void* aurora_std_dict_get(AuroraDict* dict, const char* key) {
    unsigned int h = dict_hash(key) % dict->capacity;
    DictEntry* e = dict->buckets[h];
    while (e) {
        if (strcmp(e->key, key) == 0) return e->value;
        e = e->next;
    }
    return NULL;
}

int aurora_std_dict_has(AuroraDict* dict, const char* key) {
    return aurora_std_dict_get(dict, key) != NULL;
}

int aurora_std_dict_delete(AuroraDict* dict, const char* key) {
    unsigned int h = dict_hash(key) % dict->capacity;
    DictEntry* e = dict->buckets[h], *prev = NULL;
    while (e) {
        if (strcmp(e->key, key) == 0) {
            if (prev) prev->next = e->next;
            else dict->buckets[h] = e->next;
            free(e->key); free(e);
            dict->size--;
            return 1;
        }
        prev = e; e = e->next;
    }
    return 0;
}

int aurora_std_dict_length(AuroraDict* dict) { return dict->size; }

void aurora_std_dict_clear(AuroraDict* dict) {
    for (int i = 0; i < dict->capacity; i++) {
        DictEntry* e = dict->buckets[i];
        while (e) { DictEntry* next = e->next; free(e->key); free(e); e = next; }
        dict->buckets[i] = NULL;
    }
    dict->size = 0;
}

void aurora_std_dict_destroy(AuroraDict* dict) {
    aurora_std_dict_clear(dict);
    free(dict->buckets);
    free(dict);
}

/* ========== 文件操作 ========== */

char* aurora_std_file_read(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* buf = malloc(size + 1);
    fread(buf, 1, size, f);
    buf[size] = '\0';
    fclose(f);
    return buf;
}

int aurora_std_file_write(const char* path, const char* content) {
    FILE* f = fopen(path, "w");
    if (!f) return -1;
    int r = fputs(content, f);
    fclose(f);
    return r;
}

int aurora_std_file_append(const char* path, const char* content) {
    FILE* f = fopen(path, "a");
    if (!f) return -1;
    int r = fputs(content, f);
    fclose(f);
    return r;
}

int aurora_std_file_exists(const char* path) {
    FILE* f = fopen(path, "r");
    if (f) { fclose(f); return 1; }
    return 0;
}

int aurora_std_file_delete(const char* path) {
    return remove(path);
}

long aurora_std_file_size(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fclose(f);
    return size;
}

/* ========== JSON（简化版） ========== */

char* aurora_std_json_escape(const char* s) {
    int len = (int)strlen(s);
    char* r = malloc(len * 2 + 3);
    char* dst = r;
    *dst++ = '"';
    for (int i = 0; i < len; i++) {
        switch (s[i]) {
            case '"': *dst++ = '\\'; *dst++ = '"'; break;
            case '\\': *dst++ = '\\'; *dst++ = '\\'; break;
            case '\n': *dst++ = '\\'; *dst++ = 'n'; break;
            case '\t': *dst++ = '\\'; *dst++ = 't'; break;
            case '\r': *dst++ = '\\'; *dst++ = 'r'; break;
            default: *dst++ = s[i];
        }
    }
    *dst++ = '"';
    *dst = '\0';
    return r;
}

/* ========== 加密（简化版） ========== */

unsigned int aurora_std_crypto_hash(const char* data) {
    unsigned int h = 2166136261u;
    while (*data) {
        h ^= (unsigned char)*data++;
        h *= 16777619u;
    }
    return h;
}

char* aurora_std_crypto_base64_encode(const unsigned char* data, int len) {
    static const char table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    int out_len = ((len + 2) / 3) * 4;
    char* out = malloc(out_len + 1);
    int i, j;
    for (i = 0, j = 0; i < len; ) {
        unsigned int octet_a = i < len ? data[i++] : 0;
        unsigned int octet_b = i < len ? data[i++] : 0;
        unsigned int octet_c = i < len ? data[i++] : 0;
        unsigned int triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;
        out[j++] = table[(triple >> 3 * 6) & 0x3F];
        out[j++] = table[(triple >> 2 * 6) & 0x3F];
        out[j++] = table[(triple >> 1 * 6) & 0x3F];
        out[j++] = table[(triple >> 0 * 6) & 0x3F];
    }
    for (int k = 0; k < (3 - len % 3) % 3; k++) out[out_len - 1 - k] = '=';
    out[out_len] = '\0';
    return out;
}

/* ========== 模块初始化 ========== */

void aurora_std_init() {
    aurora_std_random_seed((unsigned int)time(NULL));
}
