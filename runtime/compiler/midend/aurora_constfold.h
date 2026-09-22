/*
 * Aurora 编译器中端 - 常量折叠器
 * 支持 100+ 常量折叠操作
 */

#ifndef AURORA_CONSTFOLD_H
#define AURORA_CONSTFOLD_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 常量类型 */
typedef enum {
    CONST_INT,
    CONST_FLOAT,
    CONST_DOUBLE,
    CONST_BOOL,
    CONST_CHAR,
    CONST_STRING,
    CONST_NULL,
    CONST_VOID,
    CONST_POINTER,
    CONST_ARRAY,
    CONST_STRUCT,
    CONST_UNION,
    CONST_ENUM,
    CONST_COMPLEX,
    CONST_VECTOR,
    CONST_MATRIX,
    CONST_TENSOR,
    CONST_SET,
    CONST_MAP,
    CONST_TUPLE,
    CONST_RANGE,
    CONST_OPTION,
    CONST_RESULT,
    CONST_FUTURE,
    CONST_PROMISE,
    CONST_CHANNEL,
    CONST_STREAM,
    CONST_ITERATOR,
    CONST_GENERATOR,
    CONST_COROUTINE,
    CONST_THREAD,
    CONST_MUTEX,
    CONST_CONDVAR,
    CONST_SEMAPHORE,
    CONST_BARRIER,
    CONST_RWLOCK,
    CONST_SPINLOCK,
    CONST_ATOMIC,
    CONST_COUNT
} ConstType;

/* 常量值 */
typedef struct ConstValue {
    ConstType type;
    union {
        long long int_val;
        float float_val;
        double double_val;
        int bool_val;
        char char_val;
        char* string_val;
        void* pointer_val;
        void* array_val;
        void* struct_val;
        void* union_val;
        void* enum_val;
        void* complex_val;
        void* vector_val;
        void* matrix_val;
        void* tensor_val;
        void* set_val;
        void* map_val;
        void* tuple_val;
        void* range_val;
        void* option_val;
        void* result_val;
        void* future_val;
        void* promise_val;
        void* channel_val;
        void* stream_val;
        void* iterator_val;
        void* generator_val;
        void* coroutine_val;
        void* thread_val;
        void* mutex_val;
        void* condvar_val;
        void* semaphore_val;
        void* barrier_val;
        void* rwlock_val;
        void* spinlock_val;
        void* atomic_val;
    } value;
    int is_literal;
    int is_compile_time;
    int is_evaluated;
    int line;
    int column;
    void* ast_node;
    void* ir_node;
    struct ConstValue* next;
} ConstValue;

/* 常量折叠器 */
typedef struct ConstantFolder {
    int initialized;
    ConstValue* constants;
    int constant_count;
    int constant_capacity;
    void* constant_table;
    void* literal_pool;
    int literal_count;
    void* expression_cache;
    int cache_count;
    int cache_hits;
    int cache_misses;
    void* evaluation_stack;
    int eval_depth;
    int max_eval_depth;
    void* dependency_graph;
    int dependency_count;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int allow_overflow;
    int allow_underflow;
    int allow_division_by_zero;
    int allow_nan;
    int allow_infinity;
    int allow_undefined_behavior;
    int allow_side_effects;
    int allow_io;
    int allow_allocation;
    int allow_recursion;
    int allow_loops;
    int allow_branches;
    int allow_functions;
    int allow_generics;
    int allow_templates;
    int allow_macros;
    int allow_comptime;
    int max_constant_size;
    int max_expression_size;
    int max_evaluation_steps;
    int max_recursion_depth;
    int max_loop_iterations;
    int error_count;
    int warning_count;
    void* errors;
    int error_capacity;
    void* warnings;
    int warning_capacity;
    int debug_mode;
    int trace_mode;
    int profile_mode;
    int log_level;
    FILE* log_file;
    double start_time;
    double total_time;
    long long constants_folded;
    long long expressions_evaluated;
    long long literals_created;
    long long cache_hits_total;
    long long cache_misses_total;
    long long evaluations_performed;
    long long recursive_evaluations;
    long long loop_evaluations;
    long long branch_evaluations;
    long long function_evaluations;
    long long generic_instantiations;
    long long template_instantiations;
    long long macro_expansions;
    long long comptime_evaluations;
    long long overflow_detected;
    long long underflow_detected;
    long long division_by_zero_detected;
    long long nan_detected;
    long long infinity_detected;
    long long undefined_behavior_detected;
    long long side_effects_detected;
    long long io_detected;
    long long allocation_detected;
} ConstantFolder;

/* 函数声明 */
int cf_func_000(ConstantFolder* folder, void* node);
int cf_func_001(ConstantFolder* folder, void* node);
int cf_func_002(ConstantFolder* folder, void* node);
int cf_func_003(ConstantFolder* folder, void* node);
int cf_func_004(ConstantFolder* folder, void* node);
int cf_func_005(ConstantFolder* folder, void* node);
int cf_func_006(ConstantFolder* folder, void* node);
int cf_func_007(ConstantFolder* folder, void* node);
int cf_func_008(ConstantFolder* folder, void* node);
int cf_func_009(ConstantFolder* folder, void* node);
int cf_func_010(ConstantFolder* folder, void* node);
int cf_func_011(ConstantFolder* folder, void* node);
int cf_func_012(ConstantFolder* folder, void* node);
int cf_func_013(ConstantFolder* folder, void* node);
int cf_func_014(ConstantFolder* folder, void* node);
int cf_func_015(ConstantFolder* folder, void* node);
int cf_func_016(ConstantFolder* folder, void* node);
int cf_func_017(ConstantFolder* folder, void* node);
int cf_func_018(ConstantFolder* folder, void* node);
int cf_func_019(ConstantFolder* folder, void* node);
int cf_func_020(ConstantFolder* folder, void* node);
int cf_func_021(ConstantFolder* folder, void* node);
int cf_func_022(ConstantFolder* folder, void* node);
int cf_func_023(ConstantFolder* folder, void* node);
int cf_func_024(ConstantFolder* folder, void* node);
int cf_func_025(ConstantFolder* folder, void* node);
int cf_func_026(ConstantFolder* folder, void* node);
int cf_func_027(ConstantFolder* folder, void* node);
int cf_func_028(ConstantFolder* folder, void* node);
int cf_func_029(ConstantFolder* folder, void* node);
int cf_func_030(ConstantFolder* folder, void* node);
int cf_func_031(ConstantFolder* folder, void* node);
int cf_func_032(ConstantFolder* folder, void* node);
int cf_func_033(ConstantFolder* folder, void* node);
int cf_func_034(ConstantFolder* folder, void* node);
int cf_func_035(ConstantFolder* folder, void* node);
int cf_func_036(ConstantFolder* folder, void* node);
int cf_func_037(ConstantFolder* folder, void* node);
int cf_func_038(ConstantFolder* folder, void* node);
int cf_func_039(ConstantFolder* folder, void* node);
int cf_func_040(ConstantFolder* folder, void* node);
int cf_func_041(ConstantFolder* folder, void* node);
int cf_func_042(ConstantFolder* folder, void* node);
int cf_func_043(ConstantFolder* folder, void* node);
int cf_func_044(ConstantFolder* folder, void* node);
int cf_func_045(ConstantFolder* folder, void* node);
int cf_func_046(ConstantFolder* folder, void* node);
int cf_func_047(ConstantFolder* folder, void* node);
int cf_func_048(ConstantFolder* folder, void* node);
int cf_func_049(ConstantFolder* folder, void* node);
int cf_func_050(ConstantFolder* folder, void* node);
int cf_func_051(ConstantFolder* folder, void* node);
int cf_func_052(ConstantFolder* folder, void* node);
int cf_func_053(ConstantFolder* folder, void* node);
int cf_func_054(ConstantFolder* folder, void* node);
int cf_func_055(ConstantFolder* folder, void* node);
int cf_func_056(ConstantFolder* folder, void* node);
int cf_func_057(ConstantFolder* folder, void* node);
int cf_func_058(ConstantFolder* folder, void* node);
int cf_func_059(ConstantFolder* folder, void* node);
int cf_func_060(ConstantFolder* folder, void* node);
int cf_func_061(ConstantFolder* folder, void* node);
int cf_func_062(ConstantFolder* folder, void* node);
int cf_func_063(ConstantFolder* folder, void* node);
int cf_func_064(ConstantFolder* folder, void* node);
int cf_func_065(ConstantFolder* folder, void* node);
int cf_func_066(ConstantFolder* folder, void* node);
int cf_func_067(ConstantFolder* folder, void* node);
int cf_func_068(ConstantFolder* folder, void* node);
int cf_func_069(ConstantFolder* folder, void* node);
int cf_func_070(ConstantFolder* folder, void* node);
int cf_func_071(ConstantFolder* folder, void* node);
int cf_func_072(ConstantFolder* folder, void* node);
int cf_func_073(ConstantFolder* folder, void* node);
int cf_func_074(ConstantFolder* folder, void* node);
int cf_func_075(ConstantFolder* folder, void* node);
int cf_func_076(ConstantFolder* folder, void* node);
int cf_func_077(ConstantFolder* folder, void* node);
int cf_func_078(ConstantFolder* folder, void* node);
int cf_func_079(ConstantFolder* folder, void* node);
int cf_func_080(ConstantFolder* folder, void* node);
int cf_func_081(ConstantFolder* folder, void* node);
int cf_func_082(ConstantFolder* folder, void* node);
int cf_func_083(ConstantFolder* folder, void* node);
int cf_func_084(ConstantFolder* folder, void* node);
int cf_func_085(ConstantFolder* folder, void* node);
int cf_func_086(ConstantFolder* folder, void* node);
int cf_func_087(ConstantFolder* folder, void* node);
int cf_func_088(ConstantFolder* folder, void* node);
int cf_func_089(ConstantFolder* folder, void* node);
int cf_func_090(ConstantFolder* folder, void* node);
int cf_func_091(ConstantFolder* folder, void* node);
int cf_func_092(ConstantFolder* folder, void* node);
int cf_func_093(ConstantFolder* folder, void* node);
int cf_func_094(ConstantFolder* folder, void* node);
int cf_func_095(ConstantFolder* folder, void* node);
int cf_func_096(ConstantFolder* folder, void* node);
int cf_func_097(ConstantFolder* folder, void* node);
int cf_func_098(ConstantFolder* folder, void* node);
int cf_func_099(ConstantFolder* folder, void* node);
ConstantFolder* constant_folder_create();
void constant_folder_destroy(ConstantFolder* folder);
int constant_folder_init(ConstantFolder* folder);
int constant_folder_fold(ConstantFolder* folder, ASTNode* root);
int constant_folder_fold_ir(ConstantFolder* folder, IRModule* module);
int constant_folder_fold_file(ConstantFolder* folder, const char* filename);
ConstValue* const_value_create(ConstType type);
void const_value_destroy(ConstValue* value);
ConstValue* const_value_from_int(long long val);
ConstValue* const_value_from_float(float val);
ConstValue* const_value_from_double(double val);
ConstValue* const_value_from_bool(int val);
ConstValue* const_value_from_char(char val);
ConstValue* const_value_from_string(const char* val);
ConstValue* const_value_from_null();
ConstValue* const_value_add(ConstValue* a, ConstValue* b);
ConstValue* const_value_sub(ConstValue* a, ConstValue* b);
ConstValue* const_value_mul(ConstValue* a, ConstValue* b);
ConstValue* const_value_div(ConstValue* a, ConstValue* b);
ConstValue* const_value_mod(ConstValue* a, ConstValue* b);
ConstValue* const_value_pow(ConstValue* a, ConstValue* b);
ConstValue* const_value_neg(ConstValue* a);
ConstValue* const_value_abs(ConstValue* a);
ConstValue* const_value_min(ConstValue* a, ConstValue* b);
ConstValue* const_value_max(ConstValue* a, ConstValue* b);
ConstValue* const_value_and(ConstValue* a, ConstValue* b);
ConstValue* const_value_or(ConstValue* a, ConstValue* b);
ConstValue* const_value_not(ConstValue* a);
ConstValue* const_value_xor(ConstValue* a, ConstValue* b);
ConstValue* const_value_shl(ConstValue* a, ConstValue* b);
ConstValue* const_value_shr(ConstValue* a, ConstValue* b);
ConstValue* const_value_eq(ConstValue* a, ConstValue* b);
ConstValue* const_value_ne(ConstValue* a, ConstValue* b);
ConstValue* const_value_lt(ConstValue* a, ConstValue* b);
ConstValue* const_value_le(ConstValue* a, ConstValue* b);
ConstValue* const_value_gt(ConstValue* a, ConstValue* b);
ConstValue* const_value_ge(ConstValue* a, ConstValue* b);
ConstValue* const_value_cast(ConstValue* a, ConstType type);
ConstValue* const_value_convert(ConstValue* a, ConstType type);
int const_value_is_truthy(ConstValue* a);
int const_value_is_zero(ConstValue* a);
int const_value_is_nan(ConstValue* a);
int const_value_is_infinity(ConstValue* a);
int const_value_is_negative(ConstValue* a);
int const_value_is_positive(ConstValue* a);
int const_value_is_integer(ConstValue* a);
int const_value_is_floating(ConstValue* a);
int const_value_is_numeric(ConstValue* a);
int const_value_is_string(ConstValue* a);
int const_value_is_boolean(ConstValue* a);
int const_value_is_null(ConstValue* a);
int const_value_is_pointer(ConstValue* a);
int const_value_is_array(ConstValue* a);
int const_value_is_struct(ConstValue* a);
int const_value_is_object(ConstValue* a);
int const_value_is_collection(ConstValue* a);
int const_value_is_iterable(ConstValue* a);
int const_value_is_callable(ConstValue* a);
int const_value_is_indexable(ConstValue* a);
int const_value_is_comparable(ConstValue* a);
int const_value_is_equatable(ConstValue* a);
int const_value_is_hashable(ConstValue* a);
int const_value_is_sortable(ConstValue* a);
int const_value_is_serializable(ConstValue* a);
int const_value_is_deserializable(ConstValue* a);
int const_value_is_cloneable(ConstValue* a);
int const_value_is_copyable(ConstValue* a);
int const_value_is_movable(ConstValue* a);
int const_value_is_destructible(ConstValue* a);
int const_value_is_default_constructible(ConstValue* a);
int const_value_is_copy_constructible(ConstValue* a);
int const_value_is_move_constructible(ConstValue* a);
int const_value_is_copy_assignable(ConstValue* a);
int const_value_is_move_assignable(ConstValue* a);
int const_value_is_trivially_copyable(ConstValue* a);
int const_value_is_trivially_destructible(ConstValue* a);
int const_value_is_standard_layout(ConstValue* a);
int const_value_is_pod(ConstValue* a);
int const_value_is_aggregate(ConstValue* a);
int const_value_is_empty(ConstValue* a);
int const_value_is_final(ConstValue* a);
int const_value_is_abstract(ConstValue* a);
int const_value_is_polymorphic(ConstValue* a);
int const_value_is_virtual(ConstValue* a);
int const_value_is_override(ConstValue* a);
int const_value_is_sealed(ConstValue* a);
int const_value_is_open(ConstValue* a);
int const_value_is_closed(ConstValue* a);

#endif /* AURORA_CONSTFOLD_H */