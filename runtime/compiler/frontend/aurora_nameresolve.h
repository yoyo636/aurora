/*
 * Aurora 编译器前端 - 名称解析器
 * 支持 100+ 名称解析操作
 */

#ifndef AURORA_NAMERESOLVE_H
#define AURORA_NAMERESOLVE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "aurora_ast.h"

/* 名称类型 */
typedef enum {
    NAME_UNKNOWN,
    NAME_VARIABLE,
    NAME_CONSTANT,
    NAME_FUNCTION,
    NAME_PARAMETER,
    NAME_TYPE,
    NAME_CLASS,
    NAME_INTERFACE,
    NAME_STRUCT,
    NAME_UNION,
    NAME_ENUM,
    NAME_ENUM_VALUE,
    NAME_MODULE,
    NAME_IMPORT,
    NAME_EXPORT,
    NAME_ALIAS,
    NAME_GENERIC,
    NAME_TEMPLATE,
    NAME_MACRO,
    NAME_LABEL,
    NAME_FIELD,
    NAME_METHOD,
    NAME_PROPERTY,
    NAME_NAMESPACE,
    NAME_PACKAGE,
    NAME_BUILTIN,
    NAME_KEYWORD,
    NAME_OPERATOR,
    NAME_COUNT
} NameType;

/* 名称条目 */
typedef struct NameEntry {
    char* name;
    NameType type;
    void* declaration;
    void* definition;
    void* scope;
    int line;
    int column;
    int is_forward;
    int is_extern;
    int is_builtin;
    int is_exported;
    int is_imported;
    int is_deprecated;
    int ref_count;
    int use_count;
    struct NameEntry* next;
    struct NameEntry* prev;
} NameEntry;

/* 名称表 */
typedef struct NameTable {
    NameEntry** buckets;
    int bucket_count;
    int entry_count;
    int collision_count;
    int max_chain_length;
    double load_factor;
    int resize_count;
} NameTable;

/* 名称解析器 */
typedef struct NameResolver {
    int initialized;
    NameTable* global_table;
    NameTable* current_table;
    NameTable** table_stack;
    int table_stack_count;
    int table_stack_capacity;
    void* scope_stack;
    int scope_count;
    int scope_capacity;
    void* import_graph;
    int import_count;
    void* module_cache;
    int module_count;
    void* builtin_names;
    int builtin_count;
    void* keyword_names;
    int keyword_count;
    void* operator_names;
    int operator_count;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int allow_shadowing;
    int allow_forward_reference;
    int allow_implicit_import;
    int allow_wildcard_import;
    int allow_relative_import;
    int allow_absolute_import;
    int max_search_depth;
    int max_import_depth;
    int max_alias_depth;
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
    long long names_resolved;
    long long names_looked_up;
    long long names_declared;
    long long names_defined;
    long long names_used;
    long long names_forward;
    long long names_extern;
    long long names_builtin;
    long long names_exported;
    long long names_imported;
    long long names_aliased;
    long long names_shadowed;
    long long names_conflicted;
    long long names_ambiguous;
    long long names_undefined;
    long long imports_resolved;
    long long modules_loaded;
    long long scopes_entered;
    long long scopes_exited;
} NameResolver;

/* 函数声明 */
int nr_func_000(NameResolver* resolver, void* node);
int nr_func_001(NameResolver* resolver, void* node);
int nr_func_002(NameResolver* resolver, void* node);
int nr_func_003(NameResolver* resolver, void* node);
int nr_func_004(NameResolver* resolver, void* node);
int nr_func_005(NameResolver* resolver, void* node);
int nr_func_006(NameResolver* resolver, void* node);
int nr_func_007(NameResolver* resolver, void* node);
int nr_func_008(NameResolver* resolver, void* node);
int nr_func_009(NameResolver* resolver, void* node);
int nr_func_010(NameResolver* resolver, void* node);
int nr_func_011(NameResolver* resolver, void* node);
int nr_func_012(NameResolver* resolver, void* node);
int nr_func_013(NameResolver* resolver, void* node);
int nr_func_014(NameResolver* resolver, void* node);
int nr_func_015(NameResolver* resolver, void* node);
int nr_func_016(NameResolver* resolver, void* node);
int nr_func_017(NameResolver* resolver, void* node);
int nr_func_018(NameResolver* resolver, void* node);
int nr_func_019(NameResolver* resolver, void* node);
int nr_func_020(NameResolver* resolver, void* node);
int nr_func_021(NameResolver* resolver, void* node);
int nr_func_022(NameResolver* resolver, void* node);
int nr_func_023(NameResolver* resolver, void* node);
int nr_func_024(NameResolver* resolver, void* node);
int nr_func_025(NameResolver* resolver, void* node);
int nr_func_026(NameResolver* resolver, void* node);
int nr_func_027(NameResolver* resolver, void* node);
int nr_func_028(NameResolver* resolver, void* node);
int nr_func_029(NameResolver* resolver, void* node);
int nr_func_030(NameResolver* resolver, void* node);
int nr_func_031(NameResolver* resolver, void* node);
int nr_func_032(NameResolver* resolver, void* node);
int nr_func_033(NameResolver* resolver, void* node);
int nr_func_034(NameResolver* resolver, void* node);
int nr_func_035(NameResolver* resolver, void* node);
int nr_func_036(NameResolver* resolver, void* node);
int nr_func_037(NameResolver* resolver, void* node);
int nr_func_038(NameResolver* resolver, void* node);
int nr_func_039(NameResolver* resolver, void* node);
int nr_func_040(NameResolver* resolver, void* node);
int nr_func_041(NameResolver* resolver, void* node);
int nr_func_042(NameResolver* resolver, void* node);
int nr_func_043(NameResolver* resolver, void* node);
int nr_func_044(NameResolver* resolver, void* node);
int nr_func_045(NameResolver* resolver, void* node);
int nr_func_046(NameResolver* resolver, void* node);
int nr_func_047(NameResolver* resolver, void* node);
int nr_func_048(NameResolver* resolver, void* node);
int nr_func_049(NameResolver* resolver, void* node);
int nr_func_050(NameResolver* resolver, void* node);
int nr_func_051(NameResolver* resolver, void* node);
int nr_func_052(NameResolver* resolver, void* node);
int nr_func_053(NameResolver* resolver, void* node);
int nr_func_054(NameResolver* resolver, void* node);
int nr_func_055(NameResolver* resolver, void* node);
int nr_func_056(NameResolver* resolver, void* node);
int nr_func_057(NameResolver* resolver, void* node);
int nr_func_058(NameResolver* resolver, void* node);
int nr_func_059(NameResolver* resolver, void* node);
int nr_func_060(NameResolver* resolver, void* node);
int nr_func_061(NameResolver* resolver, void* node);
int nr_func_062(NameResolver* resolver, void* node);
int nr_func_063(NameResolver* resolver, void* node);
int nr_func_064(NameResolver* resolver, void* node);
int nr_func_065(NameResolver* resolver, void* node);
int nr_func_066(NameResolver* resolver, void* node);
int nr_func_067(NameResolver* resolver, void* node);
int nr_func_068(NameResolver* resolver, void* node);
int nr_func_069(NameResolver* resolver, void* node);
int nr_func_070(NameResolver* resolver, void* node);
int nr_func_071(NameResolver* resolver, void* node);
int nr_func_072(NameResolver* resolver, void* node);
int nr_func_073(NameResolver* resolver, void* node);
int nr_func_074(NameResolver* resolver, void* node);
int nr_func_075(NameResolver* resolver, void* node);
int nr_func_076(NameResolver* resolver, void* node);
int nr_func_077(NameResolver* resolver, void* node);
int nr_func_078(NameResolver* resolver, void* node);
int nr_func_079(NameResolver* resolver, void* node);
int nr_func_080(NameResolver* resolver, void* node);
int nr_func_081(NameResolver* resolver, void* node);
int nr_func_082(NameResolver* resolver, void* node);
int nr_func_083(NameResolver* resolver, void* node);
int nr_func_084(NameResolver* resolver, void* node);
int nr_func_085(NameResolver* resolver, void* node);
int nr_func_086(NameResolver* resolver, void* node);
int nr_func_087(NameResolver* resolver, void* node);
int nr_func_088(NameResolver* resolver, void* node);
int nr_func_089(NameResolver* resolver, void* node);
int nr_func_090(NameResolver* resolver, void* node);
int nr_func_091(NameResolver* resolver, void* node);
int nr_func_092(NameResolver* resolver, void* node);
int nr_func_093(NameResolver* resolver, void* node);
int nr_func_094(NameResolver* resolver, void* node);
int nr_func_095(NameResolver* resolver, void* node);
int nr_func_096(NameResolver* resolver, void* node);
int nr_func_097(NameResolver* resolver, void* node);
int nr_func_098(NameResolver* resolver, void* node);
int nr_func_099(NameResolver* resolver, void* node);
NameResolver* name_resolver_create();
void name_resolver_destroy(NameResolver* resolver);
int name_resolver_init(NameResolver* resolver);
int name_resolver_resolve(NameResolver* resolver, ASTNode* root);
int name_resolver_resolve_file(NameResolver* resolver, const char* filename);
int name_resolver_resolve_module(NameResolver* resolver, const char* module_name);
NameTable* name_table_create(int bucket_count);
void name_table_destroy(NameTable* table);
int name_table_insert(NameTable* table, NameEntry* entry);
int name_table_remove(NameTable* table, const char* name);
NameEntry* name_table_lookup(NameTable* table, const char* name);
int name_table_contains(NameTable* table, const char* name);
int name_table_resize(NameTable* table, int new_bucket_count);
NameEntry* name_entry_create(const char* name, NameType type, void* declaration);
void name_entry_destroy(NameEntry* entry);
int name_resolver_enter_scope(NameResolver* resolver, void* scope);
int name_resolver_exit_scope(NameResolver* resolver);
void* name_resolver_current_scope(NameResolver* resolver);
int name_resolver_declare(NameResolver* resolver, const char* name, NameType type, void* declaration);
int name_resolver_define(NameResolver* resolver, const char* name, NameType type, void* definition);
NameEntry* name_resolver_lookup(NameResolver* resolver, const char* name);
NameEntry* name_resolver_lookup_in_scope(NameResolver* resolver, void* scope, const char* name);
NameEntry* name_resolver_lookup_global(NameResolver* resolver, const char* name);
int name_resolver_is_declared(NameResolver* resolver, const char* name);
int name_resolver_is_defined(NameResolver* resolver, const char* name);
int name_resolver_is_used(NameResolver* resolver, const char* name);
int name_resolver_is_shadowed(NameResolver* resolver, const char* name);
int name_resolver_is_ambiguous(NameResolver* resolver, const char* name);
int name_resolver_is_undefined(NameResolver* resolver, const char* name);
int name_resolver_resolve_import(NameResolver* resolver, const char* module_name, const char* name);
int name_resolver_resolve_alias(NameResolver* resolver, const char* alias, const char* target);
int name_resolver_resolve_forward(NameResolver* resolver, const char* name);
int name_resolver_resolve_extern(NameResolver* resolver, const char* name);
int name_resolver_resolve_builtin(NameResolver* resolver, const char* name);
int name_resolver_resolve_operator(NameResolver* resolver, const char* op);
int name_resolver_resolve_keyword(NameResolver* resolver, const char* keyword);
int name_resolver_check_undefined(NameResolver* resolver);
int name_resolver_check_unused(NameResolver* resolver);
int name_resolver_check_shadowing(NameResolver* resolver);
int name_resolver_check_conflict(NameResolver* resolver);
int name_resolver_check_ambiguity(NameResolver* resolver);
int name_resolver_check_forward(NameResolver* resolver);
int name_resolver_check_circular_import(NameResolver* resolver);
int name_resolver_check_circular_alias(NameResolver* resolver);
int name_resolver_check_access(NameResolver* resolver);
int name_resolver_check_export(NameResolver* resolver);
int name_resolver_check_import(NameResolver* resolver);
int name_resolver_check_deprecated(NameResolver* resolver);
int name_resolver_check_naming(NameResolver* resolver);
int name_resolver_check_style(NameResolver* resolver);

#endif /* AURORA_NAMERESOLVE_H */