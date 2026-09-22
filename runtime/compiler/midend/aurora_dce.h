/*
 * Aurora 编译器中端 - 死代码消除器
 * 支持 100+ 死代码消除操作
 */

#ifndef AURORA_DCE_H
#define AURORA_DCE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 死代码类型 */
typedef enum {
    DCE_UNREACHABLE,
    DCE_UNUSED,
    DCE_DEAD_STORE,
    DCE_DEAD_LOAD,
    DCE_DEAD_FUNCTION,
    DCE_DEAD_VARIABLE,
    DCE_DEAD_PARAMETER,
    DCE_DEAD_RETURN,
    DCE_DEAD_BRANCH,
    DCE_DEAD_LOOP,
    DCE_DEAD_BLOCK,
    DCE_DEAD_INSTRUCTION,
    DCE_DEAD_EXPRESSION,
    DCE_DEAD_STATEMENT,
    DCE_DEAD_DECLARATION,
    DCE_DEAD_DEFINITION,
    DCE_DEAD_IMPORT,
    DCE_DEAD_EXPORT,
    DCE_DEAD_TYPE,
    DCE_DEAD_CLASS,
    DCE_DEAD_INTERFACE,
    DCE_DEAD_STRUCT,
    DCE_DEAD_UNION,
    DCE_DEAD_ENUM,
    DCE_DEAD_METHOD,
    DCE_DEAD_FIELD,
    DCE_DEAD_PROPERTY,
    DCE_DEAD_CONSTANT,
    DCE_DEAD_MACRO,
    DCE_DEAD_TEMPLATE,
    DCE_DEAD_GENERIC,
    DCE_DEAD_MODULE,
    DCE_DEAD_FILE,
    DCE_DEAD_LIBRARY,
    DCE_DEAD_PACKAGE,
    DCE_DEAD_DEPENDENCY,
    DCE_DEAD_RESOURCE,
    DCE_DEAD_ASSET,
    DCE_DEAD_CONFIG,
    DCE_DEAD_OPTION,
    DCE_DEAD_FLAG,
    DCE_DEAD_PARAM,
    DCE_DEAD_ARG,
    DCE_DEAD_LOCAL,
    DCE_DEAD_GLOBAL,
    DCE_DEAD_STATIC,
    DCE_DEAD_EXTERN,
    DCE_DEAD_INLINE,
    DCE_DEAD_VIRTUAL,
    DCE_DEAD_OVERRIDE,
    DCE_DEAD_ABSTRACT,
    DCE_DEAD_FINAL,
    DCE_DEAD_SEALED,
    DCE_DEAD_OPEN,
    DCE_DEAD_CLOSED,
    DCE_DEAD_PRIVATE,
    DCE_DEAD_PROTECTED,
    DCE_DEAD_PUBLIC,
    DCE_DEAD_INTERNAL,
    DCE_DEAD_PACKAGE_PRIVATE,
    DCE_DEAD_FILE_PRIVATE,
    DCE_DEAD_MODULE_PRIVATE,
    DCE_DEAD_SCOPE,
    DCE_DEAD_NAMESPACE,
    DCE_DEAD_BLOCK_SCOPE,
    DCE_DEAD_FUNCTION_SCOPE,
    DCE_DEAD_CLASS_SCOPE,
    DCE_DEAD_MODULE_SCOPE,
    DCE_DEAD_GLOBAL_SCOPE,
    DCE_DEAD_FILE_SCOPE,
    DCE_DEAD_PACKAGE_SCOPE,
    DCE_DEAD_LIBRARY_SCOPE,
    DCE_DEAD_PROJECT_SCOPE,
    DCE_DEAD_WORKSPACE_SCOPE,
    DCE_DEAD_REPOSITORY_SCOPE,
    DCE_DEAD_ORGANIZATION_SCOPE,
    DCE_DEAD_TEAM_SCOPE,
    DCE_DEAD_USER_SCOPE,
    DCE_DEAD_SYSTEM_SCOPE,
    DCE_DEAD_PLATFORM_SCOPE,
    DCE_DEAD_ARCHITECTURE_SCOPE,
    DCE_DEAD_OPERATING_SYSTEM_SCOPE,
    DCE_DEAD_COMPILER_SCOPE,
    DCE_DEED_RUNTIME_SCOPE,
    DCE_DEAD_LANGUAGE_SCOPE,
    DCE_DEAD_STANDARD_SCOPE,
    DCE_DEAD_EXTENSION_SCOPE,
    DCE_DEAD_PLUGIN_SCOPE,
    DCE_DEAD_ADDON_SCOPE,
    DCE_DEAD_MODULE_EXTENSION_SCOPE,
    DCE_DEAD_COUNT
} DCETypes;

/* 死代码条目 */
typedef struct DCEEntry {
    DCETypes type;
    void* node;
    void* ir_node;
    int line;
    int column;
    char* name;
    char* file;
    int is_reachable;
    int is_used;
    int is_live;
    int ref_count;
    int use_count;
    int def_count;
    void* refs;
    void* uses;
    void* defs;
    struct DCEEntry* next;
    struct DCEEntry* prev;
} DCEEntry;

/* 死代码消除器 */
typedef struct DeadCodeEliminator {
    int initialized;
    DCEEntry* entries;
    int entry_count;
    int entry_capacity;
    void* entry_table;
    void* reachable_set;
    int reachable_count;
    void* live_set;
    int live_count;
    void* used_set;
    int used_count;
    void* worklist;
    int worklist_count;
    int worklist_capacity;
    void* call_graph;
    int call_count;
    void* def_use_chain;
    int def_use_count;
    void* use_def_chain;
    int use_def_count;
    void* control_flow_graph;
    int cfg_count;
    void* dominator_tree;
    int dominator_count;
    void* post_dominator_tree;
    int post_dominator_count;
    void* loop_tree;
    int loop_count;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int aggressive_mode;
    int conservative_mode;
    int allow_unsafe;
    int allow_undefined_behavior;
    int allow_side_effects_removal;
    int allow_io_removal;
    int allow_allocation_removal;
    int allow_recursion_removal;
    int allow_loop_removal;
    int allow_branch_removal;
    int allow_function_removal;
    int allow_variable_removal;
    int allow_parameter_removal;
    int allow_return_removal;
    int allow_import_removal;
    int allow_export_removal;
    int allow_type_removal;
    int allow_class_removal;
    int allow_interface_removal;
    int allow_struct_removal;
    int allow_union_removal;
    int allow_enum_removal;
    int allow_method_removal;
    int allow_field_removal;
    int allow_property_removal;
    int allow_constant_removal;
    int allow_macro_removal;
    int allow_template_removal;
    int allow_generic_removal;
    int allow_module_removal;
    int allow_file_removal;
    int allow_library_removal;
    int allow_package_removal;
    int allow_dependency_removal;
    int allow_resource_removal;
    int allow_asset_removal;
    int allow_config_removal;
    int max_iterations;
    int max_worklist_size;
    int max_call_depth;
    int max_cfg_size;
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
    long long code_eliminated;
    long long instructions_eliminated;
    long long functions_eliminated;
    long long variables_eliminated;
    long long parameters_eliminated;
    long long branches_eliminated;
    long long loops_eliminated;
    long long blocks_eliminated;
    long long expressions_eliminated;
    long long statements_eliminated;
    long long declarations_eliminated;
    long long definitions_eliminated;
    long long imports_eliminated;
    long long exports_eliminated;
    long long types_eliminated;
    long long classes_eliminated;
    long long interfaces_eliminated;
    long long structs_eliminated;
    long long unions_eliminated;
    long long enums_eliminated;
    long long methods_eliminated;
    long long fields_eliminated;
    long long properties_eliminated;
    long long constants_eliminated;
    long long macros_eliminated;
    long long templates_eliminated;
    long long generics_eliminated;
    long long modules_eliminated;
    long long files_eliminated;
    long long libraries_eliminated;
    long long packages_eliminated;
    long long dependencies_eliminated;
    long long resources_eliminated;
    long long assets_eliminated;
    long long configs_eliminated;
    long long reachable_marked;
    long long live_marked;
    long long used_marked;
    long long worklist_processed;
    long long iterations_performed;
    long long cfg_built;
    long long dominators_computed;
    long long post_dominators_computed;
    long long loops_detected;
    long long call_graph_built;
    long long def_use_chains_built;
    long long use_def_chains_built;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} DeadCodeEliminator;

/* 函数声明 */
int dce_func_000(DeadCodeEliminator* dce, void* node);
int dce_func_001(DeadCodeEliminator* dce, void* node);
int dce_func_002(DeadCodeEliminator* dce, void* node);
int dce_func_003(DeadCodeEliminator* dce, void* node);
int dce_func_004(DeadCodeEliminator* dce, void* node);
int dce_func_005(DeadCodeEliminator* dce, void* node);
int dce_func_006(DeadCodeEliminator* dce, void* node);
int dce_func_007(DeadCodeEliminator* dce, void* node);
int dce_func_008(DeadCodeEliminator* dce, void* node);
int dce_func_009(DeadCodeEliminator* dce, void* node);
int dce_func_010(DeadCodeEliminator* dce, void* node);
int dce_func_011(DeadCodeEliminator* dce, void* node);
int dce_func_012(DeadCodeEliminator* dce, void* node);
int dce_func_013(DeadCodeEliminator* dce, void* node);
int dce_func_014(DeadCodeEliminator* dce, void* node);
int dce_func_015(DeadCodeEliminator* dce, void* node);
int dce_func_016(DeadCodeEliminator* dce, void* node);
int dce_func_017(DeadCodeEliminator* dce, void* node);
int dce_func_018(DeadCodeEliminator* dce, void* node);
int dce_func_019(DeadCodeEliminator* dce, void* node);
int dce_func_020(DeadCodeEliminator* dce, void* node);
int dce_func_021(DeadCodeEliminator* dce, void* node);
int dce_func_022(DeadCodeEliminator* dce, void* node);
int dce_func_023(DeadCodeEliminator* dce, void* node);
int dce_func_024(DeadCodeEliminator* dce, void* node);
int dce_func_025(DeadCodeEliminator* dce, void* node);
int dce_func_026(DeadCodeEliminator* dce, void* node);
int dce_func_027(DeadCodeEliminator* dce, void* node);
int dce_func_028(DeadCodeEliminator* dce, void* node);
int dce_func_029(DeadCodeEliminator* dce, void* node);
int dce_func_030(DeadCodeEliminator* dce, void* node);
int dce_func_031(DeadCodeEliminator* dce, void* node);
int dce_func_032(DeadCodeEliminator* dce, void* node);
int dce_func_033(DeadCodeEliminator* dce, void* node);
int dce_func_034(DeadCodeEliminator* dce, void* node);
int dce_func_035(DeadCodeEliminator* dce, void* node);
int dce_func_036(DeadCodeEliminator* dce, void* node);
int dce_func_037(DeadCodeEliminator* dce, void* node);
int dce_func_038(DeadCodeEliminator* dce, void* node);
int dce_func_039(DeadCodeEliminator* dce, void* node);
int dce_func_040(DeadCodeEliminator* dce, void* node);
int dce_func_041(DeadCodeEliminator* dce, void* node);
int dce_func_042(DeadCodeEliminator* dce, void* node);
int dce_func_043(DeadCodeEliminator* dce, void* node);
int dce_func_044(DeadCodeEliminator* dce, void* node);
int dce_func_045(DeadCodeEliminator* dce, void* node);
int dce_func_046(DeadCodeEliminator* dce, void* node);
int dce_func_047(DeadCodeEliminator* dce, void* node);
int dce_func_048(DeadCodeEliminator* dce, void* node);
int dce_func_049(DeadCodeEliminator* dce, void* node);
int dce_func_050(DeadCodeEliminator* dce, void* node);
int dce_func_051(DeadCodeEliminator* dce, void* node);
int dce_func_052(DeadCodeEliminator* dce, void* node);
int dce_func_053(DeadCodeEliminator* dce, void* node);
int dce_func_054(DeadCodeEliminator* dce, void* node);
int dce_func_055(DeadCodeEliminator* dce, void* node);
int dce_func_056(DeadCodeEliminator* dce, void* node);
int dce_func_057(DeadCodeEliminator* dce, void* node);
int dce_func_058(DeadCodeEliminator* dce, void* node);
int dce_func_059(DeadCodeEliminator* dce, void* node);
int dce_func_060(DeadCodeEliminator* dce, void* node);
int dce_func_061(DeadCodeEliminator* dce, void* node);
int dce_func_062(DeadCodeEliminator* dce, void* node);
int dce_func_063(DeadCodeEliminator* dce, void* node);
int dce_func_064(DeadCodeEliminator* dce, void* node);
int dce_func_065(DeadCodeEliminator* dce, void* node);
int dce_func_066(DeadCodeEliminator* dce, void* node);
int dce_func_067(DeadCodeEliminator* dce, void* node);
int dce_func_068(DeadCodeEliminator* dce, void* node);
int dce_func_069(DeadCodeEliminator* dce, void* node);
int dce_func_070(DeadCodeEliminator* dce, void* node);
int dce_func_071(DeadCodeEliminator* dce, void* node);
int dce_func_072(DeadCodeEliminator* dce, void* node);
int dce_func_073(DeadCodeEliminator* dce, void* node);
int dce_func_074(DeadCodeEliminator* dce, void* node);
int dce_func_075(DeadCodeEliminator* dce, void* node);
int dce_func_076(DeadCodeEliminator* dce, void* node);
int dce_func_077(DeadCodeEliminator* dce, void* node);
int dce_func_078(DeadCodeEliminator* dce, void* node);
int dce_func_079(DeadCodeEliminator* dce, void* node);
int dce_func_080(DeadCodeEliminator* dce, void* node);
int dce_func_081(DeadCodeEliminator* dce, void* node);
int dce_func_082(DeadCodeEliminator* dce, void* node);
int dce_func_083(DeadCodeEliminator* dce, void* node);
int dce_func_084(DeadCodeEliminator* dce, void* node);
int dce_func_085(DeadCodeEliminator* dce, void* node);
int dce_func_086(DeadCodeEliminator* dce, void* node);
int dce_func_087(DeadCodeEliminator* dce, void* node);
int dce_func_088(DeadCodeEliminator* dce, void* node);
int dce_func_089(DeadCodeEliminator* dce, void* node);
int dce_func_090(DeadCodeEliminator* dce, void* node);
int dce_func_091(DeadCodeEliminator* dce, void* node);
int dce_func_092(DeadCodeEliminator* dce, void* node);
int dce_func_093(DeadCodeEliminator* dce, void* node);
int dce_func_094(DeadCodeEliminator* dce, void* node);
int dce_func_095(DeadCodeEliminator* dce, void* node);
int dce_func_096(DeadCodeEliminator* dce, void* node);
int dce_func_097(DeadCodeEliminator* dce, void* node);
int dce_func_098(DeadCodeEliminator* dce, void* node);
int dce_func_099(DeadCodeEliminator* dce, void* node);
DeadCodeEliminator* dce_create();
void dce_destroy(DeadCodeEliminator* dce);
int dce_init(DeadCodeEliminator* dce);
int dce_eliminate(DeadCodeEliminator* dce, ASTNode* root);
int dce_eliminate_ir(DeadCodeEliminator* dce, IRModule* module);
int dce_eliminate_file(DeadCodeEliminator* dce, const char* filename);
DCEEntry* dce_entry_create(DCETypes type, void* node);
void dce_entry_destroy(DCEEntry* entry);
int dce_mark_reachable(DeadCodeEliminator* dce, void* node);
int dce_mark_live(DeadCodeEliminator* dce, void* node);
int dce_mark_used(DeadCodeEliminator* dce, void* node);
int dce_is_reachable(DeadCodeEliminator* dce, void* node);
int dce_is_live(DeadCodeEliminator* dce, void* node);
int dce_is_used(DeadCodeEliminator* dce, void* node);
int dce_is_dead(DeadCodeEliminator* dce, void* node);
int dce_eliminate_node(DeadCodeEliminator* dce, void* node);
int dce_eliminate_instruction(DeadCodeEliminator* dce, void* instr);
int dce_eliminate_function(DeadCodeEliminator* dce, void* func);
int dce_eliminate_variable(DeadCodeEliminator* dce, void* var);
int dce_eliminate_parameter(DeadCodeEliminator* dce, void* param);
int dce_eliminate_branch(DeadCodeEliminator* dce, void* branch);
int dce_eliminate_loop(DeadCodeEliminator* dce, void* loop);
int dce_eliminate_block(DeadCodeEliminator* dce, void* block);
int dce_eliminate_expression(DeadCodeEliminator* dce, void* expr);
int dce_eliminate_statement(DeadCodeEliminator* dce, void* stmt);
int dce_eliminate_declaration(DeadCodeEliminator* dce, void* decl);
int dce_eliminate_definition(DeadCodeEliminator* dce, void* def);
int dce_eliminate_import(DeadCodeEliminator* dce, void* import);
int dce_eliminate_export(DeadCodeEliminator* dce, void* export);
int dce_eliminate_type(DeadCodeEliminator* dce, void* type);
int dce_eliminate_class(DeadCodeEliminator* dce, void* cls);
int dce_eliminate_interface(DeadCodeEliminator* dce, void* iface);
int dce_eliminate_struct(DeadCodeEliminator* dce, void* str);
int dce_eliminate_union(DeadCodeEliminator* dce, void* uni);
int dce_eliminate_enum(DeadCodeEliminator* dce, void* enm);
int dce_eliminate_method(DeadCodeEliminator* dce, void* method);
int dce_eliminate_field(DeadCodeEliminator* dce, void* field);
int dce_eliminate_property(DeadCodeEliminator* dce, void* prop);
int dce_eliminate_constant(DeadCodeEliminator* dce, void* constant);
int dce_eliminate_macro(DeadCodeEliminator* dce, void* macro);
int dce_eliminate_template(DeadCodeEliminator* dce, void* tmpl);
int dce_eliminate_generic(DeadCodeEliminator* dce, void* generic);
int dce_eliminate_module(DeadCodeEliminator* dce, void* module);
int dce_eliminate_file(DeadCodeEliminator* dce, void* file);
int dce_eliminate_library(DeadCodeEliminator* dce, void* library);
int dce_eliminate_package(DeadCodeEliminator* dce, void* package);
int dce_eliminate_dependency(DeadCodeEliminator* dce, void* dep);
int dce_eliminate_resource(DeadCodeEliminator* dce, void* resource);
int dce_eliminate_asset(DeadCodeEliminator* dce, void* asset);
int dce_eliminate_config(DeadCodeEliminator* dce, void* config);
int dce_build_cfg(DeadCodeEliminator* dce, void* func);
int dce_build_dominators(DeadCodeEliminator* dce, void* cfg);
int dce_build_post_dominators(DeadCodeEliminator* dce, void* cfg);
int dce_detect_loops(DeadCodeEliminator* dce, void* cfg);
int dce_build_call_graph(DeadCodeEliminator* dce, void* module);
int dce_build_def_use(DeadCodeEliminator* dce, void* func);
int dce_build_use_def(DeadCodeEliminator* dce, void* func);
int dce_run_worklist(DeadCodeEliminator* dce);
int dce_iterate(DeadCodeEliminator* dce);
int dce_verify(DeadCodeEliminator* dce);
int dce_report(DeadCodeEliminator* dce);
int dce_stats(DeadCodeEliminator* dce);

#endif /* AURORA_DCE_H */