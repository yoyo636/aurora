/*
 * Aurora 编译器中端 - 向量化器
 * 支持 100+ 向量化操作
 */

#ifndef AURORA_VECTORIZE_H
#define AURORA_VECTORIZE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 向量类型 */
typedef enum {
    VEC_NONE,
    VEC_SSE,
    VEC_SSE2,
    VEC_SSE3,
    VEC_SSSE3,
    VEC_SSE4_1,
    VEC_SSE4_2,
    VEC_AVX,
    VEC_AVX2,
    VEC_AVX512F,
    VEC_AVX512BW,
    VEC_AVX512CD,
    VEC_AVX512DQ,
    VEC_AVX512ER,
    VEC_AVX512IFMA,
    VEC_AVX512PF,
    VEC_AVX512VBMI,
    VEC_AVX512VL,
    VEC_AVX512_4FMAPS,
    VEC_AVX512_4VNNIW,
    VEC_AVX512_BF16,
    VEC_AVX512_BITALG,
    VEC_AVX512_FP16,
    VEC_AVX512_GFNI,
    VEC_AVX512_VBMI2,
    VEC_AVX512_VNNI,
    VEC_AVX512_VP2INTERSECT,
    VEC_AVX512_VPOPCNTDQ,
    VEC_NEON,
    VEC_SVE,
    VEC_SVE2,
    VEC_MSA,
    VEC_VSX,
    VEC_ALTIVEC,
    VEC_MMX,
    VEC_3DNOW,
    VEC_COUNT
} VectorType;

/* 向量宽度 */
typedef enum {
    VEC_WIDTH_64,
    VEC_WIDTH_128,
    VEC_WIDTH_256,
    VEC_WIDTH_512,
    VEC_WIDTH_1024,
    VEC_WIDTH_2048,
    VEC_WIDTH_SCALABLE,
    VEC_WIDTH_COUNT
} VectorWidth;

/* 向量元素类型 */
typedef enum {
    VEC_ELEM_INT8,
    VEC_ELEM_INT16,
    VEC_ELEM_INT32,
    VEC_ELEM_INT64,
    VEC_ELEM_UINT8,
    VEC_ELEM_UINT16,
    VEC_ELEM_UINT32,
    VEC_ELEM_UINT64,
    VEC_ELEM_FLOAT16,
    VEC_ELEM_FLOAT32,
    VEC_ELEM_FLOAT64,
    VEC_ELEM_BFLOAT16,
    VEC_ELEM_BOOL,
    VEC_ELEM_COUNT
} VectorElemType;

/* 向量值 */
typedef struct VectorValue {
    VectorType type;
    VectorWidth width;
    VectorElemType elem_type;
    int elem_count;
    void* data;
    int data_size;
    int is_constant;
    int is_literal;
    int line;
    int column;
    void* ast_node;
    void* ir_node;
    struct VectorValue* next;
} VectorValue;

/* 向量化器 */
typedef struct Vectorizer {
    int initialized;
    VectorType target_type;
    VectorWidth target_width;
    VectorElemType default_elem;
    int max_vector_width;
    int max_elem_count;
    void* vector_values;
    int value_count;
    int value_capacity;
    void* vector_table;
    void* loop_candidates;
    int candidate_count;
    void* dependence_analysis;
    int dependence_count;
    void* cost_model;
    int cost_count;
    void* transformation_list;
    int transformation_count;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int aggressive_mode;
    int conservative_mode;
    int allow_unsafe;
    int allow_undefined_behavior;
    int allow_side_effects;
    int allow_io;
    int allow_allocation;
    int allow_recursion;
    int allow_gather_scatter;
    int allow_masking;
    int allow_predication;
    int allow_fma;
    int allow_approximate;
    int allow_fast_math;
    int allow_reassociation;
    int max_unroll_factor;
    int max_vector_width;
    int max_iterations;
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
    long long loops_vectorized;
    long long vectors_created;
    long long vector_operations;
    long long gather_scatter;
    long long masked_operations;
    long long predicated_operations;
    long long fma_operations;
    long long approximate_operations;
    long long fast_math_operations;
    long long reassociated_operations;
    long long unrolled_loops;
    long long peeled_loops;
    long long remainder_loops;
    long long epilogue_loops;
    long long prologue_loops;
    long long alignment_checks;
    long long version_checks;
    long long runtime_checks;
    long long compile_time_checks;
    long long dependence_tests;
    long long cost_evaluations;
    long long transformations_applied;
    long long transformations_rejected;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} Vectorizer;

/* 函数声明 */
int vec_func_000(Vectorizer* vec, void* loop);
int vec_func_001(Vectorizer* vec, void* loop);
int vec_func_002(Vectorizer* vec, void* loop);
int vec_func_003(Vectorizer* vec, void* loop);
int vec_func_004(Vectorizer* vec, void* loop);
int vec_func_005(Vectorizer* vec, void* loop);
int vec_func_006(Vectorizer* vec, void* loop);
int vec_func_007(Vectorizer* vec, void* loop);
int vec_func_008(Vectorizer* vec, void* loop);
int vec_func_009(Vectorizer* vec, void* loop);
int vec_func_010(Vectorizer* vec, void* loop);
int vec_func_011(Vectorizer* vec, void* loop);
int vec_func_012(Vectorizer* vec, void* loop);
int vec_func_013(Vectorizer* vec, void* loop);
int vec_func_014(Vectorizer* vec, void* loop);
int vec_func_015(Vectorizer* vec, void* loop);
int vec_func_016(Vectorizer* vec, void* loop);
int vec_func_017(Vectorizer* vec, void* loop);
int vec_func_018(Vectorizer* vec, void* loop);
int vec_func_019(Vectorizer* vec, void* loop);
int vec_func_020(Vectorizer* vec, void* loop);
int vec_func_021(Vectorizer* vec, void* loop);
int vec_func_022(Vectorizer* vec, void* loop);
int vec_func_023(Vectorizer* vec, void* loop);
int vec_func_024(Vectorizer* vec, void* loop);
int vec_func_025(Vectorizer* vec, void* loop);
int vec_func_026(Vectorizer* vec, void* loop);
int vec_func_027(Vectorizer* vec, void* loop);
int vec_func_028(Vectorizer* vec, void* loop);
int vec_func_029(Vectorizer* vec, void* loop);
int vec_func_030(Vectorizer* vec, void* loop);
int vec_func_031(Vectorizer* vec, void* loop);
int vec_func_032(Vectorizer* vec, void* loop);
int vec_func_033(Vectorizer* vec, void* loop);
int vec_func_034(Vectorizer* vec, void* loop);
int vec_func_035(Vectorizer* vec, void* loop);
int vec_func_036(Vectorizer* vec, void* loop);
int vec_func_037(Vectorizer* vec, void* loop);
int vec_func_038(Vectorizer* vec, void* loop);
int vec_func_039(Vectorizer* vec, void* loop);
int vec_func_040(Vectorizer* vec, void* loop);
int vec_func_041(Vectorizer* vec, void* loop);
int vec_func_042(Vectorizer* vec, void* loop);
int vec_func_043(Vectorizer* vec, void* loop);
int vec_func_044(Vectorizer* vec, void* loop);
int vec_func_045(Vectorizer* vec, void* loop);
int vec_func_046(Vectorizer* vec, void* loop);
int vec_func_047(Vectorizer* vec, void* loop);
int vec_func_048(Vectorizer* vec, void* loop);
int vec_func_049(Vectorizer* vec, void* loop);
int vec_func_050(Vectorizer* vec, void* loop);
int vec_func_051(Vectorizer* vec, void* loop);
int vec_func_052(Vectorizer* vec, void* loop);
int vec_func_053(Vectorizer* vec, void* loop);
int vec_func_054(Vectorizer* vec, void* loop);
int vec_func_055(Vectorizer* vec, void* loop);
int vec_func_056(Vectorizer* vec, void* loop);
int vec_func_057(Vectorizer* vec, void* loop);
int vec_func_058(Vectorizer* vec, void* loop);
int vec_func_059(Vectorizer* vec, void* loop);
int vec_func_060(Vectorizer* vec, void* loop);
int vec_func_061(Vectorizer* vec, void* loop);
int vec_func_062(Vectorizer* vec, void* loop);
int vec_func_063(Vectorizer* vec, void* loop);
int vec_func_064(Vectorizer* vec, void* loop);
int vec_func_065(Vectorizer* vec, void* loop);
int vec_func_066(Vectorizer* vec, void* loop);
int vec_func_067(Vectorizer* vec, void* loop);
int vec_func_068(Vectorizer* vec, void* loop);
int vec_func_069(Vectorizer* vec, void* loop);
int vec_func_070(Vectorizer* vec, void* loop);
int vec_func_071(Vectorizer* vec, void* loop);
int vec_func_072(Vectorizer* vec, void* loop);
int vec_func_073(Vectorizer* vec, void* loop);
int vec_func_074(Vectorizer* vec, void* loop);
int vec_func_075(Vectorizer* vec, void* loop);
int vec_func_076(Vectorizer* vec, void* loop);
int vec_func_077(Vectorizer* vec, void* loop);
int vec_func_078(Vectorizer* vec, void* loop);
int vec_func_079(Vectorizer* vec, void* loop);
int vec_func_080(Vectorizer* vec, void* loop);
int vec_func_081(Vectorizer* vec, void* loop);
int vec_func_082(Vectorizer* vec, void* loop);
int vec_func_083(Vectorizer* vec, void* loop);
int vec_func_084(Vectorizer* vec, void* loop);
int vec_func_085(Vectorizer* vec, void* loop);
int vec_func_086(Vectorizer* vec, void* loop);
int vec_func_087(Vectorizer* vec, void* loop);
int vec_func_088(Vectorizer* vec, void* loop);
int vec_func_089(Vectorizer* vec, void* loop);
int vec_func_090(Vectorizer* vec, void* loop);
int vec_func_091(Vectorizer* vec, void* loop);
int vec_func_092(Vectorizer* vec, void* loop);
int vec_func_093(Vectorizer* vec, void* loop);
int vec_func_094(Vectorizer* vec, void* loop);
int vec_func_095(Vectorizer* vec, void* loop);
int vec_func_096(Vectorizer* vec, void* loop);
int vec_func_097(Vectorizer* vec, void* loop);
int vec_func_098(Vectorizer* vec, void* loop);
int vec_func_099(Vectorizer* vec, void* loop);
Vectorizer* vectorizer_create();
void vectorizer_destroy(Vectorizer* vec);
int vectorizer_init(Vectorizer* vec);
int vectorizer_vectorize(Vectorizer* vec, ASTNode* root);
int vectorizer_vectorize_ir(Vectorizer* vec, IRModule* module);
int vectorizer_vectorize_file(Vectorizer* vec, const char* filename);
VectorValue* vector_value_create(VectorType type, VectorWidth width, VectorElemType elem);
void vector_value_destroy(VectorValue* value);
int vectorizer_detect_loops(Vectorizer* vec, void* func);
int vectorizer_analyze_dependences(Vectorizer* vec, void* loop);
int vectorizer_evaluate_cost(Vectorizer* vec, void* loop);
int vectorizer_apply_vectorization(Vectorizer* vec, void* loop);
int vectorizer_create_vector(Vectorizer* vec, void* scalar);
int vectorizer_extract_element(Vectorizer* vec, void* vector, int index);
int vectorizer_insert_element(Vectorizer* vec, void* vector, int index, void* value);
int vectorizer_shuffle(Vectorizer* vec, void* a, void* b, int* mask);
int vectorizer_blend(Vectorizer* vec, void* a, void* b, void* mask);
int vectorizer_gather(Vectorizer* vec, void* base, void* indices);
int vectorizer_scatter(Vectorizer* vec, void* base, void* indices, void* values);
int vectorizer_mask_load(Vectorizer* vec, void* base, void* mask);
int vectorizer_mask_store(Vectorizer* vec, void* base, void* mask, void* values);
int vectorizer_add(Vectorizer* vec, void* a, void* b);
int vectorizer_sub(Vectorizer* vec, void* a, void* b);
int vectorizer_mul(Vectorizer* vec, void* a, void* b);
int vectorizer_div(Vectorizer* vec, void* a, void* b);
int vectorizer_fma(Vectorizer* vec, void* a, void* b, void* c);
int vectorizer_min(Vectorizer* vec, void* a, void* b);
int vectorizer_max(Vectorizer* vec, void* a, void* b);
int vectorizer_abs(Vectorizer* vec, void* a);
int vectorizer_sqrt(Vectorizer* vec, void* a);
int vectorizer_exp(Vectorizer* vec, void* a);
int vectorizer_log(Vectorizer* vec, void* a);
int vectorizer_sin(Vectorizer* vec, void* a);
int vectorizer_cos(Vectorizer* vec, void* a);
int vectorizer_tan(Vectorizer* vec, void* a);
int vectorizer_and(Vectorizer* vec, void* a, void* b);
int vectorizer_or(Vectorizer* vec, void* a, void* b);
int vectorizer_xor(Vectorizer* vec, void* a, void* b);
int vectorizer_not(Vectorizer* vec, void* a);
int vectorizer_shl(Vectorizer* vec, void* a, void* b);
int vectorizer_shr(Vectorizer* vec, void* a, void* b);
int vectorizer_compare_eq(Vectorizer* vec, void* a, void* b);
int vectorizer_compare_ne(Vectorizer* vec, void* a, void* b);
int vectorizer_compare_lt(Vectorizer* vec, void* a, void* b);
int vectorizer_compare_le(Vectorizer* vec, void* a, void* b);
int vectorizer_compare_gt(Vectorizer* vec, void* a, void* b);
int vectorizer_compare_ge(Vectorizer* vec, void* a, void* b);
int vectorizer_reduce_add(Vectorizer* vec, void* a);
int vectorizer_reduce_mul(Vectorizer* vec, void* a);
int vectorizer_reduce_min(Vectorizer* vec, void* a);
int vectorizer_reduce_max(Vectorizer* vec, void* a);
int vectorizer_reduce_and(Vectorizer* vec, void* a);
int vectorizer_reduce_or(Vectorizer* vec, void* a);
int vectorizer_reduce_xor(Vectorizer* vec, void* a);
int vectorizer_broadcast(Vectorizer* vec, void* scalar);
int vectorizer_load(Vectorizer* vec, void* ptr);
int vectorizer_store(Vectorizer* vec, void* ptr, void* value);
int vectorizer_convert(Vectorizer* vec, void* a, VectorElemType type);
int vectorizer_cast(Vectorizer* vec, void* a, VectorElemType type);
int vectorizer_pack(Vectorizer* vec, void* a, void* b);
int vectorizer_unpack(Vectorizer* vec, void* a, void* low, void* high);
int vectorizer_interleave(Vectorizer* vec, void* a, void* b);
int vectorizer_deinterleave(Vectorizer* vec, void* a, void* even, void* odd);
int vectorizer_verify(Vectorizer* vec);
int vectorizer_report(Vectorizer* vec);
int vectorizer_stats(Vectorizer* vec);

#endif /* AURORA_VECTORIZE_H */