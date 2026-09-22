/*
 * Aurora 运行时 - 外部函数接口 (FFI)
 * 支持 100+ FFI 操作函数
 */

#ifndef AURORA_FFI_H
#define AURORA_FFI_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* FFI 类型 */
typedef enum {
    FFI_TYPE_VOID,
    FFI_TYPE_BOOL,
    FFI_TYPE_INT8,
    FFI_TYPE_UINT8,
    FFI_TYPE_INT16,
    FFI_TYPE_UINT16,
    FFI_TYPE_INT32,
    FFI_TYPE_UINT32,
    FFI_TYPE_INT64,
    FFI_TYPE_UINT64,
    FFI_TYPE_FLOAT,
    FFI_TYPE_DOUBLE,
    FFI_TYPE_LONG_DOUBLE,
    FFI_TYPE_POINTER,
    FFI_TYPE_STRING,
    FFI_TYPE_ARRAY,
    FFI_TYPE_STRUCT,
    FFI_TYPE_UNION,
    FFI_TYPE_ENUM,
    FFI_TYPE_FUNCTION,
    FFI_TYPE_CALLBACK,
    FFI_TYPE_CLOSURE,
    FFI_TYPE_OBJECT,
    FFI_TYPE_HANDLE,
    FFI_TYPE_BUFFER,
    FFI_TYPE_VECTOR,
    FFI_TYPE_MAP,
    FFI_TYPE_OPTIONAL,
    FFI_TYPE_RESULT,
    FFI_TYPE_VARIADIC,
    FFI_TYPE_COMPLEX,
    FFI_TYPE_COMPLEX_FLOAT,
    FFI_TYPE_COMPLEX_DOUBLE,
    FFI_TYPE_COMPLEX_LONG_DOUBLE,
    FFI_TYPE_SIZE_T,
    FFI_TYPE_SSIZE_T,
    FFI_TYPE_INTPTR_T,
    FFI_TYPE_UINTPTR_T,
    FFI_TYPE_PTRDIFF_T,
    FFI_TYPE_WCHAR_T,
    FFI_TYPE_CHAR16_T,
    FFI_TYPE_CHAR32_T,
    FFI_TYPE_INT128,
    FFI_TYPE_UINT128,
    FFI_TYPE_F16,
    FFI_TYPE_BF16,
    FFI_TYPE_F128,
    FFI_TYPE_DECIMAL32,
    FFI_TYPE_DECIMAL64,
    FFI_TYPE_DECIMAL128,
    FFI_TYPE_COUNT
} FFIType;

/* FFI ABI */
typedef enum {
    FFI_ABI_DEFAULT,
    FFI_ABI_CDECL,
    FFI_ABI_STDCALL,
    FFI_ABI_FASTCALL,
    FFI_ABI_THISCALL,
    FFI_ABI_VECTORCALL,
    FFI_ABI_SYSV,
    FFI_ABI_WIN64,
    FFI_ABI_AAPCS,
    FFI_ABI_AAPCS_VFP,
    FFI_ABI_EABI,
    FFI_ABI_EABI_HF,
    FFI_ABI_O32,
    FFI_ABI_N32,
    FFI_ABI_N64,
    FFI_ABI_O64,
    FFI_ABI_X32,
    FFI_ABI_ILP32,
    FFI_ABI_LP64,
    FFI_ABI_LLP64,
    FFI_ABI_COUNT
} FFIABI;

/* FFI 值 */
typedef struct FFIValue {
    FFIType type;
    union {
        int bool_val;
        char int8_val;
        unsigned char uint8_val;
        short int16_val;
        unsigned short uint16_val;
        int int32_val;
        unsigned int uint32_val;
        long long int64_val;
        unsigned long long uint64_val;
        float float_val;
        double double_val;
        long double long_double_val;
        void* pointer_val;
        char* string_val;
        void* struct_val;
        void* array_val;
        void* object_val;
        void* handle_val;
        void* buffer_val;
        void* vector_val;
        void* map_val;
        void* complex_val;
        void* decimal_val;
    };
    int size;
    int alignment;
    int owned;
    int ref_count;
} FFIValue;

/* FFI 函数签名 */
typedef struct FFIFunction {
    char* name;
    FFIType return_type;
    FFIType* param_types;
    int param_count;
    int is_variadic;
    FFIABI abi;
    void* address;
    void* handle;
    int call_count;
    double total_time;
    double max_time;
    double min_time;
} FFIFunction;

/* FFI 库 */
typedef struct FFILibrary {
    char* name;
    char* path;
    void* handle;
    int loaded;
    int ref_count;
    FFIFunction** functions;
    int function_count;
    int function_capacity;
    void* symbols;
    int symbol_count;
    int load_flags;
    int unload_on_destroy;
    double load_time;
    char* error;
} FFILibrary;

/* FFI 回调 */
typedef struct FFICallback {
    int id;
    char* name;
    FFIType return_type;
    FFIType* param_types;
    int param_count;
    FFIABI abi;
    void* native_trampoline;
    void* user_callback;
    void* user_data;
    int call_count;
    double total_time;
    int active;
    void* stack;
    size_t stack_size;
} FFICallback;

/* FFI 闭包 */
typedef struct FFIClosure {
    int id;
    char* name;
    FFIFunction* function;
    void* user_data;
    void* environment;
    int ref_count;
    int call_count;
    double total_time;
} FFIClosure;

/* FFI 结构体字段 */
typedef struct FFIStructField {
    char* name;
    FFIType type;
    int offset;
    int size;
    int alignment;
    int bit_offset;
    int bit_size;
    int is_bitfield;
    int is_array;
    int array_size;
    struct FFIStructField* next;
} FFIStructField;

/* FFI 结构体定义 */
typedef struct FFIStruct {
    char* name;
    FFIStructField* fields;
    int field_count;
    int size;
    int alignment;
    int is_packed;
    int is_union;
    int ref_count;
} FFIStruct;

/* FFI 数组 */
typedef struct FFIArray {
    FFIType element_type;
    void* data;
    int length;
    int capacity;
    int element_size;
    int owned;
    int ref_count;
} FFIArray;

/* FFI 缓冲区 */
typedef struct FFIBuffer {
    void* data;
    size_t size;
    size_t capacity;
    size_t position;
    size_t limit;
    int endianness;
    int owned;
    int ref_count;
    void* parent;
} FFIBuffer;

/* FFI 内存池 */
typedef struct FFIMemoryPool {
    char* name;
    void* memory;
    size_t size;
    size_t used;
    size_t free;
    void* free_list;
    int block_size;
    int block_count;
    int alignment;
    int owned;
    int ref_count;
    Mutex* mutex;
    int thread_safe;
    int alloc_count;
    int free_count;
    size_t peak_usage;
} FFIMemoryPool;

/* FFI 运行时 */
typedef struct FFIRuntime {
    int initialized;
    FFILibrary** libraries;
    int library_count;
    int library_capacity;
    FFIFunction** functions;
    int function_count;
    int function_capacity;
    FFICallback** callbacks;
    int callback_count;
    int callback_capacity;
    FFIClosure** closures;
    int closure_count;
    int closure_capacity;
    FFIStruct** structs;
    int struct_count;
    int struct_capacity;
    FFIMemoryPool** pools;
    int pool_count;
    int pool_capacity;
    int next_id;
    Mutex* mutex;
    int default_abi;
    int default_endianness;
    int default_alignment;
    int strict_type_checking;
    int safe_memory_access;
    int bounds_checking;
    int null_checking;
    int debug_mode;
    int trace_mode;
    int profile_mode;
    int log_level;
    FILE* log_file;
    char* error;
    int error_code;
    long long total_calls;
    double total_time;
    long long total_allocations;
    long long total_frees;
    size_t current_memory;
    size_t peak_memory;
} FFIRuntime;

/* 函数声明 */
int ffi_func_000(FFIRuntime* ffi, void* arg);
int ffi_func_001(FFIRuntime* ffi, void* arg);
int ffi_func_002(FFIRuntime* ffi, void* arg);
int ffi_func_003(FFIRuntime* ffi, void* arg);
int ffi_func_004(FFIRuntime* ffi, void* arg);
int ffi_func_005(FFIRuntime* ffi, void* arg);
int ffi_func_006(FFIRuntime* ffi, void* arg);
int ffi_func_007(FFIRuntime* ffi, void* arg);
int ffi_func_008(FFIRuntime* ffi, void* arg);
int ffi_func_009(FFIRuntime* ffi, void* arg);
int ffi_func_010(FFIRuntime* ffi, void* arg);
int ffi_func_011(FFIRuntime* ffi, void* arg);
int ffi_func_012(FFIRuntime* ffi, void* arg);
int ffi_func_013(FFIRuntime* ffi, void* arg);
int ffi_func_014(FFIRuntime* ffi, void* arg);
int ffi_func_015(FFIRuntime* ffi, void* arg);
int ffi_func_016(FFIRuntime* ffi, void* arg);
int ffi_func_017(FFIRuntime* ffi, void* arg);
int ffi_func_018(FFIRuntime* ffi, void* arg);
int ffi_func_019(FFIRuntime* ffi, void* arg);
int ffi_func_020(FFIRuntime* ffi, void* arg);
int ffi_func_021(FFIRuntime* ffi, void* arg);
int ffi_func_022(FFIRuntime* ffi, void* arg);
int ffi_func_023(FFIRuntime* ffi, void* arg);
int ffi_func_024(FFIRuntime* ffi, void* arg);
int ffi_func_025(FFIRuntime* ffi, void* arg);
int ffi_func_026(FFIRuntime* ffi, void* arg);
int ffi_func_027(FFIRuntime* ffi, void* arg);
int ffi_func_028(FFIRuntime* ffi, void* arg);
int ffi_func_029(FFIRuntime* ffi, void* arg);
int ffi_func_030(FFIRuntime* ffi, void* arg);
int ffi_func_031(FFIRuntime* ffi, void* arg);
int ffi_func_032(FFIRuntime* ffi, void* arg);
int ffi_func_033(FFIRuntime* ffi, void* arg);
int ffi_func_034(FFIRuntime* ffi, void* arg);
int ffi_func_035(FFIRuntime* ffi, void* arg);
int ffi_func_036(FFIRuntime* ffi, void* arg);
int ffi_func_037(FFIRuntime* ffi, void* arg);
int ffi_func_038(FFIRuntime* ffi, void* arg);
int ffi_func_039(FFIRuntime* ffi, void* arg);
int ffi_func_040(FFIRuntime* ffi, void* arg);
int ffi_func_041(FFIRuntime* ffi, void* arg);
int ffi_func_042(FFIRuntime* ffi, void* arg);
int ffi_func_043(FFIRuntime* ffi, void* arg);
int ffi_func_044(FFIRuntime* ffi, void* arg);
int ffi_func_045(FFIRuntime* ffi, void* arg);
int ffi_func_046(FFIRuntime* ffi, void* arg);
int ffi_func_047(FFIRuntime* ffi, void* arg);
int ffi_func_048(FFIRuntime* ffi, void* arg);
int ffi_func_049(FFIRuntime* ffi, void* arg);
int ffi_func_050(FFIRuntime* ffi, void* arg);
int ffi_func_051(FFIRuntime* ffi, void* arg);
int ffi_func_052(FFIRuntime* ffi, void* arg);
int ffi_func_053(FFIRuntime* ffi, void* arg);
int ffi_func_054(FFIRuntime* ffi, void* arg);
int ffi_func_055(FFIRuntime* ffi, void* arg);
int ffi_func_056(FFIRuntime* ffi, void* arg);
int ffi_func_057(FFIRuntime* ffi, void* arg);
int ffi_func_058(FFIRuntime* ffi, void* arg);
int ffi_func_059(FFIRuntime* ffi, void* arg);
int ffi_func_060(FFIRuntime* ffi, void* arg);
int ffi_func_061(FFIRuntime* ffi, void* arg);
int ffi_func_062(FFIRuntime* ffi, void* arg);
int ffi_func_063(FFIRuntime* ffi, void* arg);
int ffi_func_064(FFIRuntime* ffi, void* arg);
int ffi_func_065(FFIRuntime* ffi, void* arg);
int ffi_func_066(FFIRuntime* ffi, void* arg);
int ffi_func_067(FFIRuntime* ffi, void* arg);
int ffi_func_068(FFIRuntime* ffi, void* arg);
int ffi_func_069(FFIRuntime* ffi, void* arg);
int ffi_func_070(FFIRuntime* ffi, void* arg);
int ffi_func_071(FFIRuntime* ffi, void* arg);
int ffi_func_072(FFIRuntime* ffi, void* arg);
int ffi_func_073(FFIRuntime* ffi, void* arg);
int ffi_func_074(FFIRuntime* ffi, void* arg);
int ffi_func_075(FFIRuntime* ffi, void* arg);
int ffi_func_076(FFIRuntime* ffi, void* arg);
int ffi_func_077(FFIRuntime* ffi, void* arg);
int ffi_func_078(FFIRuntime* ffi, void* arg);
int ffi_func_079(FFIRuntime* ffi, void* arg);
int ffi_func_080(FFIRuntime* ffi, void* arg);
int ffi_func_081(FFIRuntime* ffi, void* arg);
int ffi_func_082(FFIRuntime* ffi, void* arg);
int ffi_func_083(FFIRuntime* ffi, void* arg);
int ffi_func_084(FFIRuntime* ffi, void* arg);
int ffi_func_085(FFIRuntime* ffi, void* arg);
int ffi_func_086(FFIRuntime* ffi, void* arg);
int ffi_func_087(FFIRuntime* ffi, void* arg);
int ffi_func_088(FFIRuntime* ffi, void* arg);
int ffi_func_089(FFIRuntime* ffi, void* arg);
int ffi_func_090(FFIRuntime* ffi, void* arg);
int ffi_func_091(FFIRuntime* ffi, void* arg);
int ffi_func_092(FFIRuntime* ffi, void* arg);
int ffi_func_093(FFIRuntime* ffi, void* arg);
int ffi_func_094(FFIRuntime* ffi, void* arg);
int ffi_func_095(FFIRuntime* ffi, void* arg);
int ffi_func_096(FFIRuntime* ffi, void* arg);
int ffi_func_097(FFIRuntime* ffi, void* arg);
int ffi_func_098(FFIRuntime* ffi, void* arg);
int ffi_func_099(FFIRuntime* ffi, void* arg);
FFIRuntime* ffi_runtime_create();
void ffi_runtime_destroy(FFIRuntime* ffi);
int ffi_runtime_init(FFIRuntime* ffi);
int ffi_runtime_shutdown(FFIRuntime* ffi);
FFILibrary* ffi_library_load(FFIRuntime* ffi, const char* path, int flags);
int ffi_library_unload(FFIRuntime* ffi, FFILibrary* lib);
void* ffi_library_get_symbol(FFILibrary* lib, const char* name);
int ffi_library_has_symbol(FFILibrary* lib, const char* name);
FFIFunction* ffi_function_create(FFIRuntime* ffi, const char* name, void* address, FFIType ret, FFIType* params, int count);
void ffi_function_destroy(FFIFunction* func);
FFIValue ffi_function_call(FFIFunction* func, FFIValue* args, int count);
int ffi_function_call_void(FFIFunction* func, FFIValue* args, int count);
FFIValue ffi_function_call_variadic(FFIFunction* func, FFIValue* args, int count, ...);
FFICallback* ffi_callback_create(FFIRuntime* ffi, const char* name, FFIType ret, FFIType* params, int count, void* user_cb, void* user_data);
void ffi_callback_destroy(FFICallback* cb);
void* ffi_callback_get_trampoline(FFICallback* cb);
FFIClosure* ffi_closure_create(FFIRuntime* ffi, const char* name, FFIFunction* func, void* user_data);
void ffi_closure_destroy(FFIClosure* closure);
FFIValue ffi_closure_call(FFIClosure* closure, FFIValue* args, int count);
FFIStruct* ffi_struct_create(FFIRuntime* ffi, const char* name, int is_union, int is_packed);
void ffi_struct_destroy(FFIStruct* str);
int ffi_struct_add_field(FFIStruct* str, const char* name, FFIType type, int bit_size);
int ffi_struct_get_field_offset(FFIStruct* str, const char* name);
FFIValue ffi_struct_get_field(FFIStruct* str, void* data, const char* name);
int ffi_struct_set_field(FFIStruct* str, void* data, const char* name, FFIValue value);
void* ffi_struct_alloc(FFIStruct* str);
void ffi_struct_free(FFIStruct* str, void* data);
FFIArray* ffi_array_create(FFIRuntime* ffi, FFIType type, int length);
void ffi_array_destroy(FFIArray* arr);
FFIValue ffi_array_get(FFIArray* arr, int index);
int ffi_array_set(FFIArray* arr, int index, FFIValue value);
int ffi_array_length(FFIArray* arr);
void* ffi_array_data(FFIArray* arr);
FFIBuffer* ffi_buffer_create(FFIRuntime* ffi, size_t size, int endianness);
void ffi_buffer_destroy(FFIBuffer* buf);
int ffi_buffer_get_int8(FFIBuffer* buf, size_t offset);
int ffi_buffer_get_uint8(FFIBuffer* buf, size_t offset);
int ffi_buffer_get_int16(FFIBuffer* buf, size_t offset);
int ffi_buffer_get_uint16(FFIBuffer* buf, size_t offset);
int ffi_buffer_get_int32(FFIBuffer* buf, size_t offset);
unsigned int ffi_buffer_get_uint32(FFIBuffer* buf, size_t offset);
long long ffi_buffer_get_int64(FFIBuffer* buf, size_t offset);
unsigned long long ffi_buffer_get_uint64(FFIBuffer* buf, size_t offset);
float ffi_buffer_get_float(FFIBuffer* buf, size_t offset);
double ffi_buffer_get_double(FFIBuffer* buf, size_t offset);
void* ffi_buffer_get_pointer(FFIBuffer* buf, size_t offset);
char* ffi_buffer_get_string(FFIBuffer* buf, size_t offset, size_t max_len);
int ffi_buffer_set_int8(FFIBuffer* buf, size_t offset, int value);
int ffi_buffer_set_uint8(FFIBuffer* buf, size_t offset, unsigned int value);
int ffi_buffer_set_int16(FFIBuffer* buf, size_t offset, int value);
int ffi_buffer_set_uint16(FFIBuffer* buf, size_t offset, unsigned int value);
int ffi_buffer_set_int32(FFIBuffer* buf, size_t offset, int value);
int ffi_buffer_set_uint32(FFIBuffer* buf, size_t offset, unsigned int value);
int ffi_buffer_set_int64(FFIBuffer* buf, size_t offset, long long value);
int ffi_buffer_set_uint64(FFIBuffer* buf, size_t offset, unsigned long long value);
int ffi_buffer_set_float(FFIBuffer* buf, size_t offset, float value);
int ffi_buffer_set_double(FFIBuffer* buf, size_t offset, double value);
int ffi_buffer_set_pointer(FFIBuffer* buf, size_t offset, void* value);
int ffi_buffer_set_string(FFIBuffer* buf, size_t offset, const char* value);
void* ffi_memory_alloc(FFIRuntime* ffi, size_t size, int alignment);
void ffi_memory_free(FFIRuntime* ffi, void* ptr);
void* ffi_memory_realloc(FFIRuntime* ffi, void* ptr, size_t size);
void* ffi_memory_calloc(FFIRuntime* ffi, size_t count, size_t size);
int ffi_memory_copy(void* dest, const void* src, size_t size);
int ffi_memory_move(void* dest, const void* src, size_t size);
int ffi_memory_set(void* ptr, int value, size_t size);
int ffi_memory_compare(const void* a, const void* b, size_t size);
int ffi_memory_is_null(const void* ptr);
size_t ffi_memory_size(void* ptr);
FFIMemoryPool* ffi_pool_create(FFIRuntime* ffi, const char* name, size_t size, int block_size, int alignment);
void ffi_pool_destroy(FFIMemoryPool* pool);
void* ffi_pool_alloc(FFIMemoryPool* pool);
void ffi_pool_free(FFIMemoryPool* pool, void* ptr);
int ffi_pool_reset(FFIMemoryPool* pool);
size_t ffi_pool_used(FFIMemoryPool* pool);
size_t ffi_pool_free(FFIMemoryPool* pool);
FFIValue ffi_value_create(FFIType type, void* data);
void ffi_value_destroy(FFIValue* value);
FFIValue ffi_value_copy(FFIValue* value);
int ffi_value_equals(FFIValue* a, FFIValue* b);
int ffi_value_type_size(FFIType type);
int ffi_value_type_alignment(FFIType type);
const char* ffi_type_name(FFIType type);
FFIType ffi_type_from_name(const char* name);
const char* ffi_abi_name(FFIABI abi);
FFIABI ffi_abi_from_name(const char* name);
int ffi_set_error(FFIRuntime* ffi, int code, const char* message);
const char* ffi_get_error(FFIRuntime* ffi);
int ffi_get_error_code(FFIRuntime* ffi);
int ffi_clear_error(FFIRuntime* ffi);

#endif /* AURORA_FFI_H */