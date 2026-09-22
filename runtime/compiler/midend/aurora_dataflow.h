/*
 * Aurora 编译器中端 - 数据流分析器
 * 支持 100+ 数据流分析操作
 */

#ifndef AURORA_DATAFLOW_H
#define AURORA_DATAFLOW_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 数据流分析类型 */
typedef enum {
    DF_REACHING_DEFINITIONS,
    DF_LIVE_VARIABLES,
    DF_AVAILABLE_EXPRESSIONS,
    DF_BUSY_EXPRESSIONS,
    DF_VERY_BUSY_EXPRESSIONS,
    DF_CONSTANT_PROPAGATION,
    DF_COPY_PROPAGATION,
    DF_DEAD_CODE,
    DF_POINTER_ANALYSIS,
    DF_ALIAS_ANALYSIS,
    DF_ESCAPE_ANALYSIS,
    DF_SHAPE_ANALYSIS,
    DF_TYPE_ANALYSIS,
    DF_VALUE_RANGE_ANALYSIS,
    DF_DIVISION_BY_ZERO,
    DF_NULL_POINTER,
    DF_ARRAY_BOUNDS,
    DF_UNINITIALIZED_VARIABLE,
    DF_UNUSED_VARIABLE,
    DF_UNUSED_FUNCTION,
    DF_UNUSED_PARAMETER,
    DF_UNUSED_RETURN,
    DF_UNUSED_IMPORT,
    DF_UNUSED_EXPORT,
    DF_UNUSED_TYPE,
    DF_UNUSED_CLASS,
    DF_UNUSED_INTERFACE,
    DF_UNUSED_STRUCT,
    DF_UNUSED_UNION,
    DF_UNUSED_ENUM,
    DF_UNUSED_METHOD,
    DF_UNUSED_FIELD,
    DF_UNUSED_PROPERTY,
    DF_UNUSED_CONSTANT,
    DF_UNUSED_MACRO,
    DF_UNUSED_TEMPLATE,
    DF_UNUSED_GENERIC,
    DF_UNUSED_MODULE,
    DF_UNUSED_FILE,
    DF_UNUSED_LIBRARY,
    DF_UNUSED_PACKAGE,
    DF_UNUSED_DEPENDENCY,
    DF_UNUSED_RESOURCE,
    DF_UNUSED_ASSET,
    DF_UNUSED_CONFIG,
    DF_SSA_CONSTRUCTION,
    DF_SSA_DESTRUCTION,
    DF_SSA_PRUNING,
    DF_SSA_RECONSTRUCTION,
    DF_MEMORY_SSA,
    DF_GATED_SSA,
    DF_EXTENDED_SSA,
    DF_HIGH_LEVEL_SSA,
    DF_LOW_LEVEL_SSA,
    DF_MACHINE_SSA,
    DF_REGISTER_ALLOCATION,
    DF_GRAPH_COLORING,
    DF_LINEAR_SCAN,
    DF_PBQP,
    DF_IRC,
    DF_CHAITIN,
    DF_BRIGGS,
    DF_COOPER,
    DF_VICK,
    DF_HMDS,
    DF_SSA_FORM,
    DF_CRITICAL_EDGE,
    DF_EDGE_SPLITTING,
    DF_BLOCK_SPLITTING,
    DF_LOOP_SPLITTING,
    DF_LOOP_PEELING,
    DF_LOOP_UNROLLING,
    DF_LOOP_VECTORIZATION,
    DF_LOOP_PARALLELIZATION,
    DF_LOOP_DISTRIBUTION,
    DF_LOOP_FUSION,
    DF_LOOP_INTERCHANGE,
    DF_LOOP_TILING,
    DF_LOOP_SKEWING,
    DF_LOOP_SHIFTING,
    DF_LOOP_JAMMING,
    DF_LOOP_COLLAPSING,
    DF_LOOP_EXPANSION,
    DF_LOOP_SPLITTING,
    DF_LOOP_MERGING,
    DF_LOOP_REVERSAL,
    DF_LOOP_PERMUTATION,
    DF_LOOP_ROTATION,
    DF_LOOP_TRANSPOSITION,
    DF_LOOP_INVERSION,
    DF_LOOP_CONVERSION,
    DF_LOOP_TRANSFORMATION,
    DF_LOOP_RESTRUCTURING,
    DF_LOOP_REORGANIZATION,
    DF_LOOP_REARRANGEMENT,
    DF_LOOP_REORDERING,
    DF_LOOP_RESCHEDULING,
    DF_LOOP_REALLOCATION,
    DF_LOOP_REMAPPING,
    DF_LOOP_REBINDING,
    DF_LOOP_RENAMING,
    DF_LOOP_RELABELING,
    DF_LOOP_REINDEXING,
    DF_LOOP_RECALIBRATION,
    DF_LOOP_RENORMALIZATION,
    DF_LOOP_REPARAMETERIZATION,
    DF_COUNT
} DataflowType;

/* 数据流分析器 */
typedef struct DataflowAnalyzer {
    int initialized;
    DataflowType analysis_type;
    void* cfg;
    int block_count;
    void* in_sets;
    void* out_sets;
    void* gen_sets;
    void* kill_sets;
    void* worklist;
    int worklist_count;
    int worklist_capacity;
    int forward;
    int backward;
    int may;
    int must;
    int flow_sensitive;
    int context_sensitive;
    int field_sensitive;
    int path_sensitive;
    int interprocedural;
    int intraprocedural;
    int whole_program;
    int demand_driven;
    int incremental;
    int parallel;
    int max_iterations;
    int max_worklist_size;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int aggressive_mode;
    int conservative_mode;
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
    long long blocks_analyzed;
    long long instructions_analyzed;
    long long iterations_performed;
    long long worklist_processed;
    long long reaching_definitions;
    long long live_variables;
    long long available_expressions;
    long long busy_expressions;
    long long very_busy_expressions;
    long long constants_propagated;
    long long copies_propagated;
    long long dead_code_removed;
    long long pointers_analyzed;
    long long aliases_analyzed;
    long long escapes_analyzed;
    long long shapes_analyzed;
    long long types_analyzed;
    long long value_ranges_analyzed;
    long long division_by_zero_detected;
    long long null_pointers_detected;
    long long array_bounds_detected;
    long long uninitialized_variables_detected;
    long long unused_variables_detected;
    long long unused_functions_detected;
    long long unused_parameters_detected;
    long long unused_returns_detected;
    long long unused_imports_detected;
    long long unused_exports_detected;
    long long unused_types_detected;
    long long unused_classes_detected;
    long long unused_interfaces_detected;
    long long unused_structs_detected;
    long long unused_unions_detected;
    long long unused_enums_detected;
    long long unused_methods_detected;
    long long unused_fields_detected;
    long long unused_properties_detected;
    long long unused_constants_detected;
    long long unused_macros_detected;
    long long unused_templates_detected;
    long long unused_generics_detected;
    long long unused_modules_detected;
    long long unused_files_detected;
    long long unused_libraries_detected;
    long long unused_packages_detected;
    long long unused_dependencies_detected;
    long long unused_resources_detected;
    long long unused_assets_detected;
    long long unused_configs_detected;
    long long ssa_constructed;
    long long ssa_destroyed;
    long long ssa_pruned;
    long long ssa_reconstructed;
    long long memory_ssa;
    long long gated_ssa;
    long long extended_ssa;
    long long high_level_ssa;
    long long low_level_ssa;
    long long machine_ssa;
    long long registers_allocated;
    long long spills;
    long long reloads;
    long long moves_eliminated;
    long long copies_coalesced;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} DataflowAnalyzer;

/* 函数声明 */
int df_func_000(DataflowAnalyzer* analyzer, void* node);
int df_func_001(DataflowAnalyzer* analyzer, void* node);
int df_func_002(DataflowAnalyzer* analyzer, void* node);
int df_func_003(DataflowAnalyzer* analyzer, void* node);
int df_func_004(DataflowAnalyzer* analyzer, void* node);
int df_func_005(DataflowAnalyzer* analyzer, void* node);
int df_func_006(DataflowAnalyzer* analyzer, void* node);
int df_func_007(DataflowAnalyzer* analyzer, void* node);
int df_func_008(DataflowAnalyzer* analyzer, void* node);
int df_func_009(DataflowAnalyzer* analyzer, void* node);
int df_func_010(DataflowAnalyzer* analyzer, void* node);
int df_func_011(DataflowAnalyzer* analyzer, void* node);
int df_func_012(DataflowAnalyzer* analyzer, void* node);
int df_func_013(DataflowAnalyzer* analyzer, void* node);
int df_func_014(DataflowAnalyzer* analyzer, void* node);
int df_func_015(DataflowAnalyzer* analyzer, void* node);
int df_func_016(DataflowAnalyzer* analyzer, void* node);
int df_func_017(DataflowAnalyzer* analyzer, void* node);
int df_func_018(DataflowAnalyzer* analyzer, void* node);
int df_func_019(DataflowAnalyzer* analyzer, void* node);
int df_func_020(DataflowAnalyzer* analyzer, void* node);
int df_func_021(DataflowAnalyzer* analyzer, void* node);
int df_func_022(DataflowAnalyzer* analyzer, void* node);
int df_func_023(DataflowAnalyzer* analyzer, void* node);
int df_func_024(DataflowAnalyzer* analyzer, void* node);
int df_func_025(DataflowAnalyzer* analyzer, void* node);
int df_func_026(DataflowAnalyzer* analyzer, void* node);
int df_func_027(DataflowAnalyzer* analyzer, void* node);
int df_func_028(DataflowAnalyzer* analyzer, void* node);
int df_func_029(DataflowAnalyzer* analyzer, void* node);
int df_func_030(DataflowAnalyzer* analyzer, void* node);
int df_func_031(DataflowAnalyzer* analyzer, void* node);
int df_func_032(DataflowAnalyzer* analyzer, void* node);
int df_func_033(DataflowAnalyzer* analyzer, void* node);
int df_func_034(DataflowAnalyzer* analyzer, void* node);
int df_func_035(DataflowAnalyzer* analyzer, void* node);
int df_func_036(DataflowAnalyzer* analyzer, void* node);
int df_func_037(DataflowAnalyzer* analyzer, void* node);
int df_func_038(DataflowAnalyzer* analyzer, void* node);
int df_func_039(DataflowAnalyzer* analyzer, void* node);
int df_func_040(DataflowAnalyzer* analyzer, void* node);
int df_func_041(DataflowAnalyzer* analyzer, void* node);
int df_func_042(DataflowAnalyzer* analyzer, void* node);
int df_func_043(DataflowAnalyzer* analyzer, void* node);
int df_func_044(DataflowAnalyzer* analyzer, void* node);
int df_func_045(DataflowAnalyzer* analyzer, void* node);
int df_func_046(DataflowAnalyzer* analyzer, void* node);
int df_func_047(DataflowAnalyzer* analyzer, void* node);
int df_func_048(DataflowAnalyzer* analyzer, void* node);
int df_func_049(DataflowAnalyzer* analyzer, void* node);
int df_func_050(DataflowAnalyzer* analyzer, void* node);
int df_func_051(DataflowAnalyzer* analyzer, void* node);
int df_func_052(DataflowAnalyzer* analyzer, void* node);
int df_func_053(DataflowAnalyzer* analyzer, void* node);
int df_func_054(DataflowAnalyzer* analyzer, void* node);
int df_func_055(DataflowAnalyzer* analyzer, void* node);
int df_func_056(DataflowAnalyzer* analyzer, void* node);
int df_func_057(DataflowAnalyzer* analyzer, void* node);
int df_func_058(DataflowAnalyzer* analyzer, void* node);
int df_func_059(DataflowAnalyzer* analyzer, void* node);
int df_func_060(DataflowAnalyzer* analyzer, void* node);
int df_func_061(DataflowAnalyzer* analyzer, void* node);
int df_func_062(DataflowAnalyzer* analyzer, void* node);
int df_func_063(DataflowAnalyzer* analyzer, void* node);
int df_func_064(DataflowAnalyzer* analyzer, void* node);
int df_func_065(DataflowAnalyzer* analyzer, void* node);
int df_func_066(DataflowAnalyzer* analyzer, void* node);
int df_func_067(DataflowAnalyzer* analyzer, void* node);
int df_func_068(DataflowAnalyzer* analyzer, void* node);
int df_func_069(DataflowAnalyzer* analyzer, void* node);
int df_func_070(DataflowAnalyzer* analyzer, void* node);
int df_func_071(DataflowAnalyzer* analyzer, void* node);
int df_func_072(DataflowAnalyzer* analyzer, void* node);
int df_func_073(DataflowAnalyzer* analyzer, void* node);
int df_func_074(DataflowAnalyzer* analyzer, void* node);
int df_func_075(DataflowAnalyzer* analyzer, void* node);
int df_func_076(DataflowAnalyzer* analyzer, void* node);
int df_func_077(DataflowAnalyzer* analyzer, void* node);
int df_func_078(DataflowAnalyzer* analyzer, void* node);
int df_func_079(DataflowAnalyzer* analyzer, void* node);
int df_func_080(DataflowAnalyzer* analyzer, void* node);
int df_func_081(DataflowAnalyzer* analyzer, void* node);
int df_func_082(DataflowAnalyzer* analyzer, void* node);
int df_func_083(DataflowAnalyzer* analyzer, void* node);
int df_func_084(DataflowAnalyzer* analyzer, void* node);
int df_func_085(DataflowAnalyzer* analyzer, void* node);
int df_func_086(DataflowAnalyzer* analyzer, void* node);
int df_func_087(DataflowAnalyzer* analyzer, void* node);
int df_func_088(DataflowAnalyzer* analyzer, void* node);
int df_func_089(DataflowAnalyzer* analyzer, void* node);
int df_func_090(DataflowAnalyzer* analyzer, void* node);
int df_func_091(DataflowAnalyzer* analyzer, void* node);
int df_func_092(DataflowAnalyzer* analyzer, void* node);
int df_func_093(DataflowAnalyzer* analyzer, void* node);
int df_func_094(DataflowAnalyzer* analyzer, void* node);
int df_func_095(DataflowAnalyzer* analyzer, void* node);
int df_func_096(DataflowAnalyzer* analyzer, void* node);
int df_func_097(DataflowAnalyzer* analyzer, void* node);
int df_func_098(DataflowAnalyzer* analyzer, void* node);
int df_func_099(DataflowAnalyzer* analyzer, void* node);
DataflowAnalyzer* dataflow_analyzer_create();
void dataflow_analyzer_destroy(DataflowAnalyzer* analyzer);
int dataflow_analyzer_init(DataflowAnalyzer* analyzer);
int dataflow_analyzer_analyze(DataflowAnalyzer* analyzer, ASTNode* root);
int dataflow_analyzer_analyze_ir(DataflowAnalyzer* analyzer, IRModule* module);
int dataflow_analyzer_analyze_file(DataflowAnalyzer* analyzer, const char* filename);
int dataflow_analyzer_build_cfg(DataflowAnalyzer* analyzer, void* func);
int dataflow_analyzer_compute_gen_kill(DataflowAnalyzer* analyzer, void* block);
int dataflow_analyzer_compute_in_out(DataflowAnalyzer* analyzer, void* block);
int dataflow_analyzer_meet(DataflowAnalyzer* analyzer, void* a, void* b);
int dataflow_analyzer_transfer(DataflowAnalyzer* analyzer, void* block, void* in);
int dataflow_analyzer_run_worklist(DataflowAnalyzer* analyzer);
int dataflow_analyzer_iterate(DataflowAnalyzer* analyzer);
int dataflow_analyzer_verify(DataflowAnalyzer* analyzer);
int dataflow_analyzer_report(DataflowAnalyzer* analyzer);
int dataflow_analyzer_stats(DataflowAnalyzer* analyzer);

#endif /* AURORA_DATAFLOW_H */