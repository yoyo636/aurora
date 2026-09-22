/*
 * Aurora 编译器中端 - 宏展开器
 * 支持 100+ 宏展开操作
 */

#ifndef AURORA_MACRO_H
#define AURORA_MACRO_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"

/* 宏类型 */
typedef enum {
    MACRO_OBJECT,
    MACRO_FUNCTION,
    MACRO_VARIADIC,
    MACRO_GENERIC,
    MACRO_TEMPLATE,
    MACRO_COMPTIME,
    MACRO_PROCEDURAL,
    MACRO_DECLARATIVE,
    MACRO_ATTRIBUTE,
    MACRO_DERIVE,
    MACRO_COUNT
} MacroType;

/* 宏参数 */
typedef struct MacroParam {
    char* name;
    int is_variadic;
    int is_default;
    void* default_value;
    int is_lazy;
    int is_by_name;
    int is_by_value;
    struct MacroParam* next;
} MacroParam;

/* 宏定义 */
typedef struct MacroDef {
    char* name;
    MacroType type;
    MacroParam* params;
    int param_count;
    void* body;
    void* tokens;
    int token_count;
    void* ast;
    int line;
    int column;
    int is_builtin;
    int is_prelude;
    int is_exported;
    int is_deprecated;
    int is_experimental;
    int is_unstable;
    int use_count;
    int expand_count;
    int recursion_depth;
    int max_recursion;
    void* environment;
    void* captured;
    int captured_count;
    struct MacroDef* next;
} MacroDef;

/* 宏展开器 */
typedef struct MacroExpander {
    int initialized;
    MacroDef* macros;
    int macro_count;
    int macro_capacity;
    void* macro_table;
    void* builtin_macros;
    int builtin_count;
    void* prelude_macros;
    int prelude_count;
    void* expansion_stack;
    int expansion_depth;
    int max_expansion_depth;
    void* expansion_cache;
    int cache_count;
    int cache_hits;
    int cache_misses;
    void* token_buffer;
    int token_count;
    int token_capacity;
    void* ast_buffer;
    int ast_count;
    int ast_capacity;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int allow_recursion;
    int allow_self_reference;
    int allow_circular;
    int allow_hygiene_break;
    int allow_unhygienic;
    int allow_implicit_quote;
    int allow_implicit_unquote;
    int allow_splicing;
    int allow_gensym;
    int allow_eval;
    int allow_comptime;
    int allow_procedural;
    int allow_attribute;
    int allow_derive;
    int max_token_count;
    int max_ast_count;
    int max_expansion_count;
    int max_macro_count;
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
    long long macros_defined;
    long long macros_expanded;
    long long macros_used;
    long long tokens_processed;
    long long ast_nodes_processed;
    long long expansions_performed;
    long long recursive_expansions;
    long long cached_expansions;
    long long gensyms_created;
    long long quotes_processed;
    long long unquotes_processed;
    long long splices_processed;
    long long evals_performed;
    long long comptime_evals;
    long long procedural_calls;
    long long attribute_applications;
    long long derive_invocations;
} MacroExpander;

/* 函数声明 */
int macro_func_000(MacroExpander* expander, void* node);
int macro_func_001(MacroExpander* expander, void* node);
int macro_func_002(MacroExpander* expander, void* node);
int macro_func_003(MacroExpander* expander, void* node);
int macro_func_004(MacroExpander* expander, void* node);
int macro_func_005(MacroExpander* expander, void* node);
int macro_func_006(MacroExpander* expander, void* node);
int macro_func_007(MacroExpander* expander, void* node);
int macro_func_008(MacroExpander* expander, void* node);
int macro_func_009(MacroExpander* expander, void* node);
int macro_func_010(MacroExpander* expander, void* node);
int macro_func_011(MacroExpander* expander, void* node);
int macro_func_012(MacroExpander* expander, void* node);
int macro_func_013(MacroExpander* expander, void* node);
int macro_func_014(MacroExpander* expander, void* node);
int macro_func_015(MacroExpander* expander, void* node);
int macro_func_016(MacroExpander* expander, void* node);
int macro_func_017(MacroExpander* expander, void* node);
int macro_func_018(MacroExpander* expander, void* node);
int macro_func_019(MacroExpander* expander, void* node);
int macro_func_020(MacroExpander* expander, void* node);
int macro_func_021(MacroExpander* expander, void* node);
int macro_func_022(MacroExpander* expander, void* node);
int macro_func_023(MacroExpander* expander, void* node);
int macro_func_024(MacroExpander* expander, void* node);
int macro_func_025(MacroExpander* expander, void* node);
int macro_func_026(MacroExpander* expander, void* node);
int macro_func_027(MacroExpander* expander, void* node);
int macro_func_028(MacroExpander* expander, void* node);
int macro_func_029(MacroExpander* expander, void* node);
int macro_func_030(MacroExpander* expander, void* node);
int macro_func_031(MacroExpander* expander, void* node);
int macro_func_032(MacroExpander* expander, void* node);
int macro_func_033(MacroExpander* expander, void* node);
int macro_func_034(MacroExpander* expander, void* node);
int macro_func_035(MacroExpander* expander, void* node);
int macro_func_036(MacroExpander* expander, void* node);
int macro_func_037(MacroExpander* expander, void* node);
int macro_func_038(MacroExpander* expander, void* node);
int macro_func_039(MacroExpander* expander, void* node);
int macro_func_040(MacroExpander* expander, void* node);
int macro_func_041(MacroExpander* expander, void* node);
int macro_func_042(MacroExpander* expander, void* node);
int macro_func_043(MacroExpander* expander, void* node);
int macro_func_044(MacroExpander* expander, void* node);
int macro_func_045(MacroExpander* expander, void* node);
int macro_func_046(MacroExpander* expander, void* node);
int macro_func_047(MacroExpander* expander, void* node);
int macro_func_048(MacroExpander* expander, void* node);
int macro_func_049(MacroExpander* expander, void* node);
int macro_func_050(MacroExpander* expander, void* node);
int macro_func_051(MacroExpander* expander, void* node);
int macro_func_052(MacroExpander* expander, void* node);
int macro_func_053(MacroExpander* expander, void* node);
int macro_func_054(MacroExpander* expander, void* node);
int macro_func_055(MacroExpander* expander, void* node);
int macro_func_056(MacroExpander* expander, void* node);
int macro_func_057(MacroExpander* expander, void* node);
int macro_func_058(MacroExpander* expander, void* node);
int macro_func_059(MacroExpander* expander, void* node);
int macro_func_060(MacroExpander* expander, void* node);
int macro_func_061(MacroExpander* expander, void* node);
int macro_func_062(MacroExpander* expander, void* node);
int macro_func_063(MacroExpander* expander, void* node);
int macro_func_064(MacroExpander* expander, void* node);
int macro_func_065(MacroExpander* expander, void* node);
int macro_func_066(MacroExpander* expander, void* node);
int macro_func_067(MacroExpander* expander, void* node);
int macro_func_068(MacroExpander* expander, void* node);
int macro_func_069(MacroExpander* expander, void* node);
int macro_func_070(MacroExpander* expander, void* node);
int macro_func_071(MacroExpander* expander, void* node);
int macro_func_072(MacroExpander* expander, void* node);
int macro_func_073(MacroExpander* expander, void* node);
int macro_func_074(MacroExpander* expander, void* node);
int macro_func_075(MacroExpander* expander, void* node);
int macro_func_076(MacroExpander* expander, void* node);
int macro_func_077(MacroExpander* expander, void* node);
int macro_func_078(MacroExpander* expander, void* node);
int macro_func_079(MacroExpander* expander, void* node);
int macro_func_080(MacroExpander* expander, void* node);
int macro_func_081(MacroExpander* expander, void* node);
int macro_func_082(MacroExpander* expander, void* node);
int macro_func_083(MacroExpander* expander, void* node);
int macro_func_084(MacroExpander* expander, void* node);
int macro_func_085(MacroExpander* expander, void* node);
int macro_func_086(MacroExpander* expander, void* node);
int macro_func_087(MacroExpander* expander, void* node);
int macro_func_088(MacroExpander* expander, void* node);
int macro_func_089(MacroExpander* expander, void* node);
int macro_func_090(MacroExpander* expander, void* node);
int macro_func_091(MacroExpander* expander, void* node);
int macro_func_092(MacroExpander* expander, void* node);
int macro_func_093(MacroExpander* expander, void* node);
int macro_func_094(MacroExpander* expander, void* node);
int macro_func_095(MacroExpander* expander, void* node);
int macro_func_096(MacroExpander* expander, void* node);
int macro_func_097(MacroExpander* expander, void* node);
int macro_func_098(MacroExpander* expander, void* node);
int macro_func_099(MacroExpander* expander, void* node);
MacroExpander* macro_expander_create();
void macro_expander_destroy(MacroExpander* expander);
int macro_expander_init(MacroExpander* expander);
int macro_expander_expand(MacroExpander* expander, ASTNode* root);
int macro_expander_expand_file(MacroExpander* expander, const char* filename);
MacroDef* macro_def_create(const char* name, MacroType type);
void macro_def_destroy(MacroDef* macro);
int macro_def_add_param(MacroDef* macro, const char* name, int is_variadic);
int macro_def_set_body(MacroDef* macro, void* body);
int macro_def_set_tokens(MacroDef* macro, void* tokens, int count);
int macro_def_set_ast(MacroDef* macro, void* ast);
int macro_expander_define(MacroExpander* expander, MacroDef* macro);
int macro_expander_undefine(MacroExpander* expander, const char* name);
MacroDef* macro_expander_lookup(MacroExpander* expander, const char* name);
int macro_expander_is_defined(MacroExpander* expander, const char* name);
int macro_expander_is_builtin(MacroExpander* expander, const char* name);
int macro_expander_is_prelude(MacroExpander* expander, const char* name);
void* macro_expander_expand_macro(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
void* macro_expander_expand_object(MacroExpander* expander, MacroDef* macro);
void* macro_expander_expand_function(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
void* macro_expander_expand_variadic(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
void* macro_expander_expand_generic(MacroExpander* expander, MacroDef* macro, void** type_args, int type_count, void** args, int arg_count);
void* macro_expander_expand_template(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
void* macro_expander_expand_comptime(MacroExpander* expander, void* expr);
void* macro_expander_expand_procedural(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
void* macro_expander_expand_declarative(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
void* macro_expander_expand_attribute(MacroExpander* expander, MacroDef* macro, void* target, void** args, int arg_count);
void* macro_expander_expand_derive(MacroExpander* expander, MacroDef* macro, void* target);
int macro_expander_quote(MacroExpander* expander, void* expr);
int macro_expander_unquote(MacroExpander* expander, void* expr);
int macro_expander_splice(MacroExpander* expander, void* expr);
char* macro_expander_gensym(MacroExpander* expander, const char* prefix);
int macro_expander_eval(MacroExpander* expander, void* expr);
int macro_expander_comptime_eval(MacroExpander* expander, void* expr);
int macro_expander_check_recursion(MacroExpander* expander, MacroDef* macro);
int macro_expander_check_circular(MacroExpander* expander, MacroDef* macro);
int macro_expander_check_hygiene(MacroExpander* expander, MacroDef* macro);
int macro_expander_check_arity(MacroExpander* expander, MacroDef* macro, int arg_count);
int macro_expander_check_types(MacroExpander* expander, MacroDef* macro, void** args, int arg_count);
int macro_expander_check_undefined(MacroExpander* expander);
int macro_expander_check_unused(MacroExpander* expander);
int macro_expander_check_shadowing(MacroExpander* expander);
int macro_expander_check_conflict(MacroExpander* expander);
int macro_expander_check_ambiguity(MacroExpander* expander);
int macro_expander_check_deprecated(MacroExpander* expander);
int macro_expander_check_experimental(MacroExpander* expander);
int macro_expander_check_unstable(MacroExpander* expander);

#endif /* AURORA_MACRO_H */