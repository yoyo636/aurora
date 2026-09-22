/*
 * Aurora 编译器前端 - 语义分析器
 * 支持 100+ 语义分析操作
 */

#ifndef AURORA_SEMANTIC_H
#define AURORA_SEMANTIC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "../runtime/aurora_type.h"

/* 作用域类型 */
typedef enum {
    SCOPE_GLOBAL,
    SCOPE_MODULE,
    SCOPE_FUNCTION,
    SCOPE_BLOCK,
    SCOPE_LOOP,
    SCOPE_SWITCH,
    SCOPE_TRY,
    SCOPE_CATCH,
    SCOPE_FINALLY,
    SCOPE_CLASS,
    SCOPE_INTERFACE,
    SCOPE_STRUCT,
    SCOPE_UNION,
    SCOPE_ENUM,
    SCOPE_GENERIC,
    SCOPE_LAMBDA,
    SCOPE_CLOSURE,
    SCOPE_COROUTINE,
    SCOPE_ASYNC,
    SCOPE_COUNT
} ScopeType;

/* 符号类型 */
typedef enum {
    SYMBOL_VARIABLE,
    SYMBOL_CONSTANT,
    SYMBOL_FUNCTION,
    SYMBOL_PARAMETER,
    SYMBOL_TYPE,
    SYMBOL_CLASS,
    SYMBOL_INTERFACE,
    SYMBOL_STRUCT,
    SYMBOL_UNION,
    SYMBOL_ENUM,
    SYMBOL_ENUM_VALUE,
    SYMBOL_MODULE,
    SYMBOL_IMPORT,
    SYMBOL_EXPORT,
    SYMBOL_ALIAS,
    SYMBOL_GENERIC,
    SYMBOL_TEMPLATE,
    SYMBOL_MACRO,
    SYMBOL_LABEL,
    SYMBOL_FIELD,
    SYMBOL_METHOD,
    SYMBOL_PROPERTY,
    SYMBOL_NAMESPACE,
    SYMBOL_PACKAGE,
    SYMBOL_COUNT
} SymbolType;

/* 符号 */
typedef struct Symbol {
    char* name;
    SymbolType type;
    Type* data_type;
    void* ast_node;
    int line;
    int column;
    int is_const;
    int is_volatile;
    int is_static;
    int is_private;
    int is_protected;
    int is_public;
    int is_internal;
    int is_extern;
    int is_inline;
    int is_virtual;
    int is_override;
    int is_final;
    int is_abstract;
    int is_generic;
    int is_optional;
    int is_deprecated;
    int is_exported;
    int is_imported;
    int is_builtin;
    int is_synthetic;
    int ref_count;
    int use_count;
    struct Symbol* next;
    struct Symbol* prev;
} Symbol;

/* 作用域 */
typedef struct Scope {
    ScopeType type;
    char* name;
    struct Scope* parent;
    struct Scope** children;
    int child_count;
    int child_capacity;
    Symbol** symbols;
    int symbol_count;
    int symbol_capacity;
    void* symbol_table;
    int depth;
    int line;
    int column;
    int is_loop;
    int is_switch;
    int is_function;
    int is_class;
    int is_async;
    int is_coroutine;
    int has_return;
    int has_yield;
    int has_await;
    int has_break;
    int has_continue;
    int has_goto;
    int has_throw;
    Type* return_type;
    Type* yield_type;
    void* owner;
} Scope;

/* 诊断级别 */
typedef enum {
    DIAG_ERROR,
    DIAG_WARNING,
    DIAG_INFO,
    DIAG_HINT,
    DIAG_NOTE
} DiagnosticLevel;

/* 诊断 */
typedef struct Diagnostic {
    int id;
    DiagnosticLevel level;
    char* code;
    char* message;
    char* file;
    int line;
    int column;
    int end_line;
    int end_column;
    void* source;
    void* related;
    int related_count;
    void* fix;
    int fix_count;
    int is_suppressed;
    int is_fixable;
    struct Diagnostic* next;
} Diagnostic;

/* 语义分析器 */
typedef struct SemanticAnalyzer {
    int initialized;
    Scope* global_scope;
    Scope* current_scope;
    Scope** scope_stack;
    int scope_stack_count;
    int scope_stack_capacity;
    Diagnostic* diagnostics;
    int diagnostic_count;
    int diagnostic_capacity;
    int error_count;
    int warning_count;
    int info_count;
    int hint_count;
    void* type_env;
    void* builtin_types;
    int builtin_type_count;
    void* builtin_functions;
    int builtin_function_count;
    void* builtin_constants;
    int builtin_constant_count;
    void* module_cache;
    int module_count;
    void* import_graph;
    int import_count;
    int current_file;
    char* current_file_name;
    int strict_mode;
    int pedantic_mode;
    int warn_as_error;
    int allow_unused;
    int allow_shadowing;
    int allow_implicit_conversion;
    int allow_goto;
    int allow_deprecated;
    int max_errors;
    int max_warnings;
    int max_diagnostics;
    int debug_mode;
    int trace_mode;
    int profile_mode;
    int log_level;
    FILE* log_file;
    double start_time;
    double total_time;
    long long nodes_visited;
    long long symbols_created;
    long long types_checked;
    long long conversions_performed;
    long long overloads_resolved;
    long long generics_instantiated;
    long long imports_resolved;
} SemanticAnalyzer;

/* 函数声明 */
int sem_func_000(SemanticAnalyzer* analyzer, void* node);
int sem_func_001(SemanticAnalyzer* analyzer, void* node);
int sem_func_002(SemanticAnalyzer* analyzer, void* node);
int sem_func_003(SemanticAnalyzer* analyzer, void* node);
int sem_func_004(SemanticAnalyzer* analyzer, void* node);
int sem_func_005(SemanticAnalyzer* analyzer, void* node);
int sem_func_006(SemanticAnalyzer* analyzer, void* node);
int sem_func_007(SemanticAnalyzer* analyzer, void* node);
int sem_func_008(SemanticAnalyzer* analyzer, void* node);
int sem_func_009(SemanticAnalyzer* analyzer, void* node);
int sem_func_010(SemanticAnalyzer* analyzer, void* node);
int sem_func_011(SemanticAnalyzer* analyzer, void* node);
int sem_func_012(SemanticAnalyzer* analyzer, void* node);
int sem_func_013(SemanticAnalyzer* analyzer, void* node);
int sem_func_014(SemanticAnalyzer* analyzer, void* node);
int sem_func_015(SemanticAnalyzer* analyzer, void* node);
int sem_func_016(SemanticAnalyzer* analyzer, void* node);
int sem_func_017(SemanticAnalyzer* analyzer, void* node);
int sem_func_018(SemanticAnalyzer* analyzer, void* node);
int sem_func_019(SemanticAnalyzer* analyzer, void* node);
int sem_func_020(SemanticAnalyzer* analyzer, void* node);
int sem_func_021(SemanticAnalyzer* analyzer, void* node);
int sem_func_022(SemanticAnalyzer* analyzer, void* node);
int sem_func_023(SemanticAnalyzer* analyzer, void* node);
int sem_func_024(SemanticAnalyzer* analyzer, void* node);
int sem_func_025(SemanticAnalyzer* analyzer, void* node);
int sem_func_026(SemanticAnalyzer* analyzer, void* node);
int sem_func_027(SemanticAnalyzer* analyzer, void* node);
int sem_func_028(SemanticAnalyzer* analyzer, void* node);
int sem_func_029(SemanticAnalyzer* analyzer, void* node);
int sem_func_030(SemanticAnalyzer* analyzer, void* node);
int sem_func_031(SemanticAnalyzer* analyzer, void* node);
int sem_func_032(SemanticAnalyzer* analyzer, void* node);
int sem_func_033(SemanticAnalyzer* analyzer, void* node);
int sem_func_034(SemanticAnalyzer* analyzer, void* node);
int sem_func_035(SemanticAnalyzer* analyzer, void* node);
int sem_func_036(SemanticAnalyzer* analyzer, void* node);
int sem_func_037(SemanticAnalyzer* analyzer, void* node);
int sem_func_038(SemanticAnalyzer* analyzer, void* node);
int sem_func_039(SemanticAnalyzer* analyzer, void* node);
int sem_func_040(SemanticAnalyzer* analyzer, void* node);
int sem_func_041(SemanticAnalyzer* analyzer, void* node);
int sem_func_042(SemanticAnalyzer* analyzer, void* node);
int sem_func_043(SemanticAnalyzer* analyzer, void* node);
int sem_func_044(SemanticAnalyzer* analyzer, void* node);
int sem_func_045(SemanticAnalyzer* analyzer, void* node);
int sem_func_046(SemanticAnalyzer* analyzer, void* node);
int sem_func_047(SemanticAnalyzer* analyzer, void* node);
int sem_func_048(SemanticAnalyzer* analyzer, void* node);
int sem_func_049(SemanticAnalyzer* analyzer, void* node);
int sem_func_050(SemanticAnalyzer* analyzer, void* node);
int sem_func_051(SemanticAnalyzer* analyzer, void* node);
int sem_func_052(SemanticAnalyzer* analyzer, void* node);
int sem_func_053(SemanticAnalyzer* analyzer, void* node);
int sem_func_054(SemanticAnalyzer* analyzer, void* node);
int sem_func_055(SemanticAnalyzer* analyzer, void* node);
int sem_func_056(SemanticAnalyzer* analyzer, void* node);
int sem_func_057(SemanticAnalyzer* analyzer, void* node);
int sem_func_058(SemanticAnalyzer* analyzer, void* node);
int sem_func_059(SemanticAnalyzer* analyzer, void* node);
int sem_func_060(SemanticAnalyzer* analyzer, void* node);
int sem_func_061(SemanticAnalyzer* analyzer, void* node);
int sem_func_062(SemanticAnalyzer* analyzer, void* node);
int sem_func_063(SemanticAnalyzer* analyzer, void* node);
int sem_func_064(SemanticAnalyzer* analyzer, void* node);
int sem_func_065(SemanticAnalyzer* analyzer, void* node);
int sem_func_066(SemanticAnalyzer* analyzer, void* node);
int sem_func_067(SemanticAnalyzer* analyzer, void* node);
int sem_func_068(SemanticAnalyzer* analyzer, void* node);
int sem_func_069(SemanticAnalyzer* analyzer, void* node);
int sem_func_070(SemanticAnalyzer* analyzer, void* node);
int sem_func_071(SemanticAnalyzer* analyzer, void* node);
int sem_func_072(SemanticAnalyzer* analyzer, void* node);
int sem_func_073(SemanticAnalyzer* analyzer, void* node);
int sem_func_074(SemanticAnalyzer* analyzer, void* node);
int sem_func_075(SemanticAnalyzer* analyzer, void* node);
int sem_func_076(SemanticAnalyzer* analyzer, void* node);
int sem_func_077(SemanticAnalyzer* analyzer, void* node);
int sem_func_078(SemanticAnalyzer* analyzer, void* node);
int sem_func_079(SemanticAnalyzer* analyzer, void* node);
int sem_func_080(SemanticAnalyzer* analyzer, void* node);
int sem_func_081(SemanticAnalyzer* analyzer, void* node);
int sem_func_082(SemanticAnalyzer* analyzer, void* node);
int sem_func_083(SemanticAnalyzer* analyzer, void* node);
int sem_func_084(SemanticAnalyzer* analyzer, void* node);
int sem_func_085(SemanticAnalyzer* analyzer, void* node);
int sem_func_086(SemanticAnalyzer* analyzer, void* node);
int sem_func_087(SemanticAnalyzer* analyzer, void* node);
int sem_func_088(SemanticAnalyzer* analyzer, void* node);
int sem_func_089(SemanticAnalyzer* analyzer, void* node);
int sem_func_090(SemanticAnalyzer* analyzer, void* node);
int sem_func_091(SemanticAnalyzer* analyzer, void* node);
int sem_func_092(SemanticAnalyzer* analyzer, void* node);
int sem_func_093(SemanticAnalyzer* analyzer, void* node);
int sem_func_094(SemanticAnalyzer* analyzer, void* node);
int sem_func_095(SemanticAnalyzer* analyzer, void* node);
int sem_func_096(SemanticAnalyzer* analyzer, void* node);
int sem_func_097(SemanticAnalyzer* analyzer, void* node);
int sem_func_098(SemanticAnalyzer* analyzer, void* node);
int sem_func_099(SemanticAnalyzer* analyzer, void* node);
SemanticAnalyzer* semantic_analyzer_create();
void semantic_analyzer_destroy(SemanticAnalyzer* analyzer);
int semantic_analyzer_init(SemanticAnalyzer* analyzer);
int semantic_analyzer_analyze(SemanticAnalyzer* analyzer, ASTNode* root);
int semantic_analyzer_analyze_file(SemanticAnalyzer* analyzer, const char* filename);
int semantic_analyzer_analyze_module(SemanticAnalyzer* analyzer, const char* module_name);
Scope* semantic_scope_create(SemanticAnalyzer* analyzer, ScopeType type, const char* name);
void semantic_scope_destroy(SemanticAnalyzer* analyzer, Scope* scope);
int semantic_scope_enter(SemanticAnalyzer* analyzer, Scope* scope);
int semantic_scope_exit(SemanticAnalyzer* analyzer);
Scope* semantic_scope_current(SemanticAnalyzer* analyzer);
Scope* semantic_scope_parent(SemanticAnalyzer* analyzer);
Scope* semantic_scope_find(SemanticAnalyzer* analyzer, const char* name);
Symbol* semantic_symbol_create(SemanticAnalyzer* analyzer, const char* name, SymbolType type, Type* data_type);
void semantic_symbol_destroy(SemanticAnalyzer* analyzer, Symbol* symbol);
int semantic_symbol_add(SemanticAnalyzer* analyzer, Scope* scope, Symbol* symbol);
int semantic_symbol_remove(SemanticAnalyzer* analyzer, Scope* scope, const char* name);
Symbol* semantic_symbol_lookup(SemanticAnalyzer* analyzer, const char* name);
Symbol* semantic_symbol_lookup_in_scope(SemanticAnalyzer* analyzer, Scope* scope, const char* name);
int semantic_symbol_exists(SemanticAnalyzer* analyzer, const char* name);
int semantic_symbol_is_shadowed(SemanticAnalyzer* analyzer, const char* name);
Diagnostic* semantic_diagnostic_create(SemanticAnalyzer* analyzer, DiagnosticLevel level, const char* code, const char* message);
void semantic_diagnostic_destroy(SemanticAnalyzer* analyzer, Diagnostic* diag);
int semantic_diagnostic_add(SemanticAnalyzer* analyzer, Diagnostic* diag);
int semantic_error(SemanticAnalyzer* analyzer, const char* code, const char* message, int line, int column);
int semantic_warning(SemanticAnalyzer* analyzer, const char* code, const char* message, int line, int column);
int semantic_info(SemanticAnalyzer* analyzer, const char* code, const char* message, int line, int column);
int semantic_hint(SemanticAnalyzer* analyzer, const char* code, const char* message, int line, int column);
int semantic_check_types(SemanticAnalyzer* analyzer, Type* expected, Type* actual);
int semantic_check_assignable(SemanticAnalyzer* analyzer, Type* from, Type* to);
int semantic_check_cast(SemanticAnalyzer* analyzer, Type* from, Type* to);
Type* semantic_infer_type(SemanticAnalyzer* analyzer, ASTNode* node);
Type* semantic_resolve_type(SemanticAnalyzer* analyzer, ASTNode* type_node);
int semantic_check_undefined(SemanticAnalyzer* analyzer);
int semantic_check_unused(SemanticAnalyzer* analyzer);
int semantic_check_unreachable(SemanticAnalyzer* analyzer);
int semantic_check_overflow(SemanticAnalyzer* analyzer);
int semantic_check_null_pointer(SemanticAnalyzer* analyzer);
int semantic_check_array_bounds(SemanticAnalyzer* analyzer);
int semantic_check_division_by_zero(SemanticAnalyzer* analyzer);
int semantic_check_type_mismatch(SemanticAnalyzer* analyzer);
int semantic_check_signature_mismatch(SemanticAnalyzer* analyzer);
int semantic_check_ambiguous_call(SemanticAnalyzer* analyzer);
int semantic_check_recursive_type(SemanticAnalyzer* analyzer);
int semantic_check_circular_dependency(SemanticAnalyzer* analyzer);
int semantic_check_access_control(SemanticAnalyzer* analyzer);
int semantic_check_override(SemanticAnalyzer* analyzer);
int semantic_check_abstract(SemanticAnalyzer* analyzer);
int semantic_check_generic_constraints(SemanticAnalyzer* analyzer);
int semantic_check_variadic(SemanticAnalyzer* analyzer);
int semantic_check_default_arguments(SemanticAnalyzer* analyzer);
int semantic_check_lambda_capture(SemanticAnalyzer* analyzer);
int semantic_check_async_await(SemanticAnalyzer* analyzer);
int semantic_check_coroutine(SemanticAnalyzer* analyzer);
int semantic_check_exception_handling(SemanticAnalyzer* analyzer);
int semantic_check_resource_management(SemanticAnalyzer* analyzer);
int semantic_check_memory_safety(SemanticAnalyzer* analyzer);
int semantic_check_thread_safety(SemanticAnalyzer* analyzer);
int semantic_check_data_race(SemanticAnalyzer* analyzer);
int semantic_check_deadlock(SemanticAnalyzer* analyzer);
int semantic_check_immutability(SemanticAnalyzer* analyzer);
int semantic_check_purity(SemanticAnalyzer* analyzer);
int semantic_check_side_effects(SemanticAnalyzer* analyzer);
int semantic_check_deprecated(SemanticAnalyzer* analyzer);
int semantic_check_naming_conventions(SemanticAnalyzer* analyzer);
int semantic_check_style(SemanticAnalyzer* analyzer);
int semantic_check_complexity(SemanticAnalyzer* analyzer);
int semantic_check_performance(SemanticAnalyzer* analyzer);
int semantic_check_security(SemanticAnalyzer* analyzer);

#endif /* AURORA_SEMANTIC_H */