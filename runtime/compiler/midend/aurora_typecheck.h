/*
 * Aurora 编译器中端 - 类型检查器
 * 支持 100+ 类型检查操作
 */

#ifndef AURORA_TYPECHECK_H
#define AURORA_TYPECHECK_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "../runtime/aurora_type.h"

/* 类型检查结果 */
typedef enum {
    TC_OK,
    TC_ERROR,
    TC_WARNING,
    TC_INFO,
    TC_UNKNOWN
} TCResult;

/* 类型关系 */
typedef enum {
    TC_REL_EQUAL,
    TC_REL_SUBTYPE,
    TC_REL_SUPERTYPE,
    TC_REL_COMPATIBLE,
    TC_REL_INCOMPATIBLE,
    TC_REL_UNKNOWN
} TCRelation;

/* 类型检查器 */
typedef struct TypeChecker {
    int initialized;
    void* type_env;
    void* builtin_types;
    int builtin_count;
    void* generic_env;
    int generic_count;
    void* constraint_set;
    int constraint_count;
    void* unification_log;
    int unification_count;
    void* inference_log;
    int inference_count;
    int strict_mode;
    int infer_mode;
    int nominal_mode;
    int structural_mode;
    int allow_implicit;
    int allow_narrowing;
    int allow_widening;
    int allow_coercion;
    int allow_cast;
    int allow_any;
    int allow_dynamic;
    int allow_union;
    int allow_intersection;
    int allow_conditional;
    int allow_mapped;
    int allow_template;
    int allow_variadic;
    int allow_recursive;
    int allow_mutually_recursive;
    int max_recursion_depth;
    int max_inference_steps;
    int max_unification_steps;
    int max_generic_instantiations;
    int max_overload_candidates;
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
    long long nodes_checked;
    long long types_inferred;
    long long types_checked;
    long long unifications_performed;
    long long constraints_solved;
    long long generics_instantiated;
    long long overloads_resolved;
    long long coercions_inserted;
    long long casts_inserted;
} TypeChecker;

/* 函数声明 */
TCResult tc_func_000(TypeChecker* checker, void* node);
TCResult tc_func_001(TypeChecker* checker, void* node);
TCResult tc_func_002(TypeChecker* checker, void* node);
TCResult tc_func_003(TypeChecker* checker, void* node);
TCResult tc_func_004(TypeChecker* checker, void* node);
TCResult tc_func_005(TypeChecker* checker, void* node);
TCResult tc_func_006(TypeChecker* checker, void* node);
TCResult tc_func_007(TypeChecker* checker, void* node);
TCResult tc_func_008(TypeChecker* checker, void* node);
TCResult tc_func_009(TypeChecker* checker, void* node);
TCResult tc_func_010(TypeChecker* checker, void* node);
TCResult tc_func_011(TypeChecker* checker, void* node);
TCResult tc_func_012(TypeChecker* checker, void* node);
TCResult tc_func_013(TypeChecker* checker, void* node);
TCResult tc_func_014(TypeChecker* checker, void* node);
TCResult tc_func_015(TypeChecker* checker, void* node);
TCResult tc_func_016(TypeChecker* checker, void* node);
TCResult tc_func_017(TypeChecker* checker, void* node);
TCResult tc_func_018(TypeChecker* checker, void* node);
TCResult tc_func_019(TypeChecker* checker, void* node);
TCResult tc_func_020(TypeChecker* checker, void* node);
TCResult tc_func_021(TypeChecker* checker, void* node);
TCResult tc_func_022(TypeChecker* checker, void* node);
TCResult tc_func_023(TypeChecker* checker, void* node);
TCResult tc_func_024(TypeChecker* checker, void* node);
TCResult tc_func_025(TypeChecker* checker, void* node);
TCResult tc_func_026(TypeChecker* checker, void* node);
TCResult tc_func_027(TypeChecker* checker, void* node);
TCResult tc_func_028(TypeChecker* checker, void* node);
TCResult tc_func_029(TypeChecker* checker, void* node);
TCResult tc_func_030(TypeChecker* checker, void* node);
TCResult tc_func_031(TypeChecker* checker, void* node);
TCResult tc_func_032(TypeChecker* checker, void* node);
TCResult tc_func_033(TypeChecker* checker, void* node);
TCResult tc_func_034(TypeChecker* checker, void* node);
TCResult tc_func_035(TypeChecker* checker, void* node);
TCResult tc_func_036(TypeChecker* checker, void* node);
TCResult tc_func_037(TypeChecker* checker, void* node);
TCResult tc_func_038(TypeChecker* checker, void* node);
TCResult tc_func_039(TypeChecker* checker, void* node);
TCResult tc_func_040(TypeChecker* checker, void* node);
TCResult tc_func_041(TypeChecker* checker, void* node);
TCResult tc_func_042(TypeChecker* checker, void* node);
TCResult tc_func_043(TypeChecker* checker, void* node);
TCResult tc_func_044(TypeChecker* checker, void* node);
TCResult tc_func_045(TypeChecker* checker, void* node);
TCResult tc_func_046(TypeChecker* checker, void* node);
TCResult tc_func_047(TypeChecker* checker, void* node);
TCResult tc_func_048(TypeChecker* checker, void* node);
TCResult tc_func_049(TypeChecker* checker, void* node);
TCResult tc_func_050(TypeChecker* checker, void* node);
TCResult tc_func_051(TypeChecker* checker, void* node);
TCResult tc_func_052(TypeChecker* checker, void* node);
TCResult tc_func_053(TypeChecker* checker, void* node);
TCResult tc_func_054(TypeChecker* checker, void* node);
TCResult tc_func_055(TypeChecker* checker, void* node);
TCResult tc_func_056(TypeChecker* checker, void* node);
TCResult tc_func_057(TypeChecker* checker, void* node);
TCResult tc_func_058(TypeChecker* checker, void* node);
TCResult tc_func_059(TypeChecker* checker, void* node);
TCResult tc_func_060(TypeChecker* checker, void* node);
TCResult tc_func_061(TypeChecker* checker, void* node);
TCResult tc_func_062(TypeChecker* checker, void* node);
TCResult tc_func_063(TypeChecker* checker, void* node);
TCResult tc_func_064(TypeChecker* checker, void* node);
TCResult tc_func_065(TypeChecker* checker, void* node);
TCResult tc_func_066(TypeChecker* checker, void* node);
TCResult tc_func_067(TypeChecker* checker, void* node);
TCResult tc_func_068(TypeChecker* checker, void* node);
TCResult tc_func_069(TypeChecker* checker, void* node);
TCResult tc_func_070(TypeChecker* checker, void* node);
TCResult tc_func_071(TypeChecker* checker, void* node);
TCResult tc_func_072(TypeChecker* checker, void* node);
TCResult tc_func_073(TypeChecker* checker, void* node);
TCResult tc_func_074(TypeChecker* checker, void* node);
TCResult tc_func_075(TypeChecker* checker, void* node);
TCResult tc_func_076(TypeChecker* checker, void* node);
TCResult tc_func_077(TypeChecker* checker, void* node);
TCResult tc_func_078(TypeChecker* checker, void* node);
TCResult tc_func_079(TypeChecker* checker, void* node);
TCResult tc_func_080(TypeChecker* checker, void* node);
TCResult tc_func_081(TypeChecker* checker, void* node);
TCResult tc_func_082(TypeChecker* checker, void* node);
TCResult tc_func_083(TypeChecker* checker, void* node);
TCResult tc_func_084(TypeChecker* checker, void* node);
TCResult tc_func_085(TypeChecker* checker, void* node);
TCResult tc_func_086(TypeChecker* checker, void* node);
TCResult tc_func_087(TypeChecker* checker, void* node);
TCResult tc_func_088(TypeChecker* checker, void* node);
TCResult tc_func_089(TypeChecker* checker, void* node);
TCResult tc_func_090(TypeChecker* checker, void* node);
TCResult tc_func_091(TypeChecker* checker, void* node);
TCResult tc_func_092(TypeChecker* checker, void* node);
TCResult tc_func_093(TypeChecker* checker, void* node);
TCResult tc_func_094(TypeChecker* checker, void* node);
TCResult tc_func_095(TypeChecker* checker, void* node);
TCResult tc_func_096(TypeChecker* checker, void* node);
TCResult tc_func_097(TypeChecker* checker, void* node);
TCResult tc_func_098(TypeChecker* checker, void* node);
TCResult tc_func_099(TypeChecker* checker, void* node);
TypeChecker* type_checker_create();
void type_checker_destroy(TypeChecker* checker);
int type_checker_init(TypeChecker* checker);
TCResult type_checker_check(TypeChecker* checker, ASTNode* root);
TCResult type_checker_check_file(TypeChecker* checker, const char* filename);
Type* type_checker_infer(TypeChecker* checker, ASTNode* node);
TCRelation type_checker_compare(TypeChecker* checker, Type* a, Type* b);
int type_checker_is_subtype(TypeChecker* checker, Type* sub, Type* super);
int type_checker_is_assignable(TypeChecker* checker, Type* from, Type* to);
int type_checker_is_convertible(TypeChecker* checker, Type* from, Type* to);
int type_checker_is_comparable(TypeChecker* checker, Type* a, Type* b);
int type_checker_is_equatable(TypeChecker* checker, Type* a, Type* b);
int type_checker_is_callable(TypeChecker* checker, Type* type);
int type_checker_is_indexable(TypeChecker* checker, Type* type);
int type_checker_is_iterable(TypeChecker* checker, Type* type);
int type_checker_is_awaitable(TypeChecker* checker, Type* type);
int type_checker_is_thenable(TypeChecker* checker, Type* type);
Type* type_checker_union(TypeChecker* checker, Type** types, int count);
Type* type_checker_intersection(TypeChecker* checker, Type** types, int count);
Type* type_checker_common_supertype(TypeChecker* checker, Type** types, int count);
Type* type_checker_meet(TypeChecker* checker, Type* a, Type* b);
Type* type_checker_join(TypeChecker* checker, Type* a, Type* b);
Type* type_checker_narrow(TypeChecker* checker, Type* type, ASTNode* condition);
Type* type_checker_widen(TypeChecker* checker, Type* type);
Type* type_checker_instantiate(TypeChecker* checker, Type* generic, Type** args, int count);
Type* type_checker_specialize(TypeChecker* checker, Type* generic, void* context);
int type_checker_unify(TypeChecker* checker, Type* a, Type* b);
int type_checker_match(TypeChecker* checker, Type* pattern, Type* actual);
int type_checker_resolve_overload(TypeChecker* checker, void* candidates, Type** args, int count);
int type_checker_check_signature(TypeChecker* checker, Type* expected, Type* actual);
int type_checker_check_arguments(TypeChecker* checker, Type** params, int param_count, Type** args, int arg_count);
int type_checker_check_return(TypeChecker* checker, Type* expected, Type* actual);
int type_checker_check_assignment(TypeChecker* checker, Type* target, Type* value);
int type_checker_check_binary(TypeChecker* checker, int op, Type* left, Type* right);
int type_checker_check_unary(TypeChecker* checker, int op, Type* operand);
int type_checker_check_cast(TypeChecker* checker, Type* from, Type* to);
int type_checker_check_index(TypeChecker* checker, Type* container, Type* index);
int type_checker_check_call(TypeChecker* checker, Type* callee, Type** args, int count);
int type_checker_check_member(TypeChecker* checker, Type* object, const char* member);
int type_checker_check_generic_constraints(TypeChecker* checker, Type* param, Type* arg);
int type_checker_check_recursive_type(TypeChecker* checker, Type* type);
int type_checker_check_circular_dependency(TypeChecker* checker, void* graph);
int type_checker_check_variance(TypeChecker* checker, Type* type, int position);
int type_checker_check_purity(TypeChecker* checker, ASTNode* node);
int type_checker_check_side_effects(TypeChecker* checker, ASTNode* node);
int type_checker_check_immutability(TypeChecker* checker, ASTNode* node);
int type_checker_check_null_safety(TypeChecker* checker, ASTNode* node);
int type_checker_check_memory_safety(TypeChecker* checker, ASTNode* node);
int type_checker_check_thread_safety(TypeChecker* checker, ASTNode* node);
int type_checker_check_exception_safety(TypeChecker* checker, ASTNode* node);
int type_checker_check_resource_safety(TypeChecker* checker, ASTNode* node);
int type_checker_check_type_safety(TypeChecker* checker, ASTNode* node);
int type_checker_check_undefined_behavior(TypeChecker* checker, ASTNode* node);
int type_checker_check_overflow(TypeChecker* checker, ASTNode* node);
int type_checker_check_underflow(TypeChecker* checker, ASTNode* node);
int type_checker_check_division_by_zero(TypeChecker* checker, ASTNode* node);
int type_checker_check_array_bounds(TypeChecker* checker, ASTNode* node);
int type_checker_check_null_pointer(TypeChecker* checker, ASTNode* node);
int type_checker_check_dangling_pointer(TypeChecker* checker, ASTNode* node);
int type_checker_check_use_after_free(TypeChecker* checker, ASTNode* node);
int type_checker_check_double_free(TypeChecker* checker, ASTNode* node);
int type_checker_check_memory_leak(TypeChecker* checker, ASTNode* node);
int type_checker_check_data_race(TypeChecker* checker, ASTNode* node);
int type_checker_check_deadlock(TypeChecker* checker, ASTNode* node);
int type_checker_check_livelock(TypeChecker* checker, ASTNode* node);
int type_checker_check_starvation(TypeChecker* checker, ASTNode* node);

#endif /* AURORA_TYPECHECK_H */