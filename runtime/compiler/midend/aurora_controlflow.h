/*
 * Aurora 编译器中端 - 控制流分析器
 * 支持 100+ 控制流分析操作
 */

#ifndef AURORA_CONTROLFLOW_H
#define AURORA_CONTROLFLOW_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 控制流分析类型 */
typedef enum {
    CF_CFG_CONSTRUCTION,
    CF_DOMINATOR_TREE,
    CF_POST_DOMINATOR_TREE,
    CF_LOOP_DETECTION,
    CF_LOOP_TREE,
    CF_LOOP_NESTING,
    CF_REACHABILITY,
    CF_CONTROL_DEPENDENCE,
    CF_DATA_DEPENDENCE,
    CF_MEMORY_DEPENDENCE,
    CF_SCHEDULING_DEPENDENCE,
    CF_ANTI_DEPENDENCE,
    CF_OUTPUT_DEPENDENCE,
    CF_FLOW_DEPENDENCE,
    CF_TRUE_DEPENDENCE,
    CF_FALSE_DEPENDENCE,
    CF_CRITICAL_EDGE,
    CF_EDGE_SPLITTING,
    CF_BLOCK_SPLITTING,
    CF_BLOCK_MERGING,
    CF_BLOCK_REORDERING,
    CF_BLOCK_CLONING,
    CF_BLOCK_DUPLICATION,
    CF_BLOCK_ELIMINATION,
    CF_UNREACHABLE_CODE,
    CF_DEAD_CODE,
    CF_INFINITE_LOOP,
    CF_TERMINATION,
    CF_NON_TERMINATION,
    CF_PATH_PROFILING,
    CF_PATH_COUNTING,
    CF_PATH_ENUMERATION,
    CF_PATH_SUMMARIZATION,
    CF_PATH_SENSITIVE,
    CF_PATH_INSENSITIVE,
    CF_FLOW_SENSITIVE,
    CF_FLOW_INSENSITIVE,
    CF_CONTEXT_SENSITIVE,
    CF_CONTEXT_INSENSITIVE,
    CF_FIELD_SENSITIVE,
    CF_FIELD_INSENSITIVE,
    CF_ARRAY_SENSITIVE,
    CF_ARRAY_INSENSITIVE,
    CF_INTERPROCEDURAL,
    CF_INTRAPROCEDURAL,
    CF_WHOLE_PROGRAM,
    CF_DEMAND_DRIVEN,
    CF_INCREMENTAL,
    CF_PARALLEL,
    CF_SSA_FORM,
    CF_SSA_CONSTRUCTION,
    CF_SSA_DESTRUCTION,
    CF_SSA_PRUNING,
    CF_SSA_RECONSTRUCTION,
    CF_MEMORY_SSA,
    CF_GATED_SSA,
    CF_EXTENDED_SSA,
    CF_HIGH_LEVEL_SSA,
    CF_LOW_LEVEL_SSA,
    CF_MACHINE_SSA,
    CF_REGISTER_ALLOCATION,
    CF_GRAPH_COLORING,
    CF_LINEAR_SCAN,
    CF_PBQP,
    CF_IRC,
    CF_CHAITIN,
    CF_BRIGGS,
    CF_COOPER,
    CF_VICK,
    CF_HMDS,
    CF_INSTRUCTION_SCHEDULING,
    CF_LIST_SCHEDULING,
    CF_TRACE_SCHEDULING,
    CF_SUPERBLOCK_SCHEDULING,
    CF_HYPERBLOCK_SCHEDULING,
    CF_REGION_SCHEDULING,
    CF_GLOBAL_SCHEDULING,
    CF_LOCAL_SCHEDULING,
    CF_MODULO_SCHEDULING,
    CF_SOFTWARE_PIPELINING,
    CF_LOOP_SCHEDULING,
    CF_ACYCLIC_SCHEDULING,
    CF_CYCLIC_SCHEDULING,
    CF_PREDICATED_EXECUTION,
    CF_IF_CONVERSION,
    CF_HAMMOCK_CONVERSION,
    CF_CONTROL_FLOW_GRAPH,
    CF_CALL_GRAPH,
    CF_DEF_USE_CHAIN,
    CF_USE_DEF_CHAIN,
    CF_POINTER_GRAPH,
    CF_DEPENDENCE_GRAPH,
    CF_INTERFERENCE_GRAPH,
    CF_COALESCING_GRAPH,
    CF_PRIORITY_GRAPH,
    CF_WEIGHTED_GRAPH,
    CF_DIRECTED_GRAPH,
    CF_UNDIRECTED_GRAPH,
    CF_MULTIGRAPH,
    CF_BIPARTITE_GRAPH,
    CF_COMPLETE_GRAPH,
    CF_PLANAR_GRAPH,
    CF_TREE,
    CF_FOREST,
    CF_DAG,
    CF_CYCLIC_GRAPH,
    CF_ACYCLIC_GRAPH,
    CF_CONNECTED_GRAPH,
    CF_DISCONNECTED_GRAPH,
    CF_STRONGLY_CONNECTED,
    CF_WEAKLY_CONNECTED,
    CF_ARTICULATION_POINT,
    CF_BRIDGE,
    CF_CUT_VERTEX,
    CF_CUT_EDGE,
    CF_BICONNECTED,
    CF_TRICONNECTED,
    CF_KCONNECTED,
    CF_VERTEX_CONNECTIVITY,
    CF_EDGE_CONNECTIVITY,
    CF_MAX_FLOW,
    CF_MIN_CUT,
    CF_MAX_CUT,
    CF_MIN_SPANNING_TREE,
    CF_MAX_SPANNING_TREE,
    CF_SHORTEST_PATH,
    CF_LONGEST_PATH,
    CF_ALL_PAIRS_SHORTEST_PATH,
    CF_SINGLE_SOURCE_SHORTEST_PATH,
    CF_TOPOLOGICAL_SORT,
    CF_REVERSE_TOPOLOGICAL_SORT,
    CF_DEPTH_FIRST_SEARCH,
    CF_BREADTH_FIRST_SEARCH,
    CF_PREORDER,
    CF_POSTORDER,
    CF_INORDER,
    CF_LEVELORDER,
    CF_REVERSE_LEVELORDER,
    CF_EULER_TOUR,
    CF_HAMILTONIAN_PATH,
    CF_HAMILTONIAN_CYCLE,
    CF_EULERIAN_PATH,
    CF_EULERIAN_CYCLE,
    CF_TRAVELING_SALESMAN,
    CF_VEHICLE_ROUTING,
    CF_JOB_SHOP,
    CF_FLOW_SHOP,
    CF_OPEN_SHOP,
    CF_MIXED_SHOP,
    CF_PROJECT_SCHEDULING,
    CF_RESOURCE_CONSTRAINED,
    CF_TIME_CONSTRAINED,
    CF_COST_CONSTRAINED,
    CF_QUALITY_CONSTRAINED,
    CF_MULTI_OBJECTIVE,
    CF_SINGLE_OBJECTIVE,
    CF_PARETO_OPTIMAL,
    CF_NASH_EQUILIBRIUM,
    CF_STACKELBERG_EQUILIBRIUM,
    CF_EVOLUTIONARY_ALGORITHM,
    CF_GENETIC_ALGORITHM,
    CF_GENETIC_PROGRAMMING,
    CF_GENETIC_EXPRESSION_PROGRAMMING,
    CF_ANT_COLONY_OPTIMIZATION,
    CF_PARTICLE_SWARM_OPTIMIZATION,
    CF_SIMULATED_ANNEALING,
    CF_TABU_SEARCH,
    CF_HILL_CLIMBING,
    CF_GRADIENT_DESCENT,
    CF_CONJUGATE_GRADIENT,
    CF_NEWTON_METHOD,
    CF_QUASI_NEWTON,
    CF_GAUSS_NEWTON,
    CF_LEVENBERG_MARQUARDT,
    CF_TRUST_REGION,
    CF_LINE_SEARCH,
    CF_BARRIER_METHOD,
    CF_PENALTY_METHOD,
    CF_AUGMENTED_LAGRANGIAN,
    CF_ALTERNATING_DIRECTION_METHOD_OF_MULTIPLIERS,
    CF_PROXIMAL_GRADIENT,
    CF_PROXIMAL_AVERAGE,
    CF_MIRROR_DESCENT,
    CF_NESTEROV_ACCELERATED_GRADIENT,
    CF_ADAM,
    CF_RMSPROP,
    CF_ADAGRAD,
    CF_ADADELTA,
    CF_SGD,
    CF_MOMENTUM,
    CF_NESTEROV,
    CF_COUNT
} ControlFlowType;

/* 控制流分析器 */
typedef struct ControlFlowAnalyzer {
    int initialized;
    ControlFlowType analysis_type;
    void* cfg;
    int block_count;
    int edge_count;
    void* dominator_tree;
    int dominator_count;
    void* post_dominator_tree;
    int post_dominator_count;
    void* loop_tree;
    int loop_count;
    void* loop_nesting;
    int nesting_depth;
    void* reachability;
    int reachable_count;
    void* control_dependence;
    int control_dependence_count;
    void* data_dependence;
    int data_dependence_count;
    void* memory_dependence;
    int memory_dependence_count;
    void* scheduling_dependence;
    int scheduling_dependence_count;
    void* anti_dependence;
    int anti_dependence_count;
    void* output_dependence;
    int output_dependence_count;
    void* flow_dependence;
    int flow_dependence_count;
    void* true_dependence;
    int true_dependence_count;
    void* false_dependence;
    int false_dependence_count;
    void* critical_edges;
    int critical_edge_count;
    void* worklist;
    int worklist_count;
    int worklist_capacity;
    int current_file;
    char* current_file_name;
    int current_module;
    char* current_module_name;
    int strict_mode;
    int aggressive_mode;
    int conservative_mode;
    int max_iterations;
    int max_worklist_size;
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
    long long cfgs_constructed;
    long long dominator_trees_computed;
    long long post_dominator_trees_computed;
    long long loops_detected;
    long long loop_trees_computed;
    long long loop_nestings_computed;
    long long reachability_computed;
    long long control_dependences_computed;
    long long data_dependences_computed;
    long long memory_dependences_computed;
    long long scheduling_dependences_computed;
    long long anti_dependences_computed;
    long long output_dependences_computed;
    long long flow_dependences_computed;
    long long true_dependences_computed;
    long long false_dependences_computed;
    long long critical_edges_detected;
    long long edges_split;
    long long blocks_split;
    long long blocks_merged;
    long long blocks_reordered;
    long long blocks_cloned;
    long long blocks_duplicated;
    long long blocks_eliminated;
    long long unreachable_code_removed;
    long long dead_code_removed;
    long long infinite_loops_detected;
    long long termination_proven;
    long long non_termination_detected;
    long long paths_profiled;
    long long paths_counted;
    long long paths_enumerated;
    long long paths_summarized;
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
    long long instructions_scheduled;
    long long lists_scheduled;
    long long traces_scheduled;
    long long superblocks_scheduled;
    long long hyperblocks_scheduled;
    long long regions_scheduled;
    long long globals_scheduled;
    long long locals_scheduled;
    long long modulos_scheduled;
    long long software_pipelined;
    long long loops_scheduled;
    long long acyclics_scheduled;
    long long cyclics_scheduled;
    long long predicated_executions;
    long long if_conversions;
    long long hammock_conversions;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} ControlFlowAnalyzer;

/* 函数声明 */
int cf_func_000(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_001(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_002(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_003(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_004(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_005(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_006(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_007(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_008(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_009(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_010(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_011(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_012(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_013(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_014(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_015(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_016(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_017(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_018(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_019(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_020(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_021(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_022(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_023(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_024(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_025(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_026(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_027(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_028(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_029(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_030(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_031(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_032(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_033(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_034(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_035(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_036(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_037(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_038(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_039(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_040(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_041(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_042(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_043(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_044(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_045(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_046(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_047(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_048(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_049(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_050(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_051(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_052(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_053(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_054(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_055(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_056(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_057(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_058(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_059(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_060(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_061(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_062(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_063(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_064(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_065(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_066(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_067(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_068(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_069(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_070(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_071(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_072(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_073(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_074(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_075(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_076(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_077(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_078(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_079(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_080(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_081(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_082(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_083(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_084(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_085(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_086(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_087(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_088(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_089(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_090(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_091(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_092(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_093(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_094(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_095(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_096(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_097(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_098(ControlFlowAnalyzer* analyzer, void* node);
int cf_func_099(ControlFlowAnalyzer* analyzer, void* node);
ControlFlowAnalyzer* controlflow_analyzer_create();
void controlflow_analyzer_destroy(ControlFlowAnalyzer* analyzer);
int controlflow_analyzer_init(ControlFlowAnalyzer* analyzer);
int controlflow_analyzer_analyze(ControlFlowAnalyzer* analyzer, ASTNode* root);
int controlflow_analyzer_analyze_ir(ControlFlowAnalyzer* analyzer, IRModule* module);
int controlflow_analyzer_analyze_file(ControlFlowAnalyzer* analyzer, const char* filename);
int controlflow_analyzer_build_cfg(ControlFlowAnalyzer* analyzer, void* func);
int controlflow_analyzer_compute_dominators(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_post_dominators(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_detect_loops(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_loop_tree(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_reachability(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_control_dependence(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_data_dependence(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_memory_dependence(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_compute_scheduling_dependence(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_detect_critical_edges(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_split_critical_edges(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_split_edges(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_split_blocks(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_merge_blocks(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_reorder_blocks(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_clone_blocks(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_duplicate_blocks(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_eliminate_blocks(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_remove_unreachable_code(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_remove_dead_code(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_detect_infinite_loops(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_prove_termination(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_detect_non_termination(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_profile_paths(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_count_paths(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_enumerate_paths(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_summarize_paths(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_construct_ssa(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_destroy_ssa(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_prune_ssa(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_reconstruct_ssa(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_allocate_registers(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_schedule_instructions(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_convert_if(ControlFlowAnalyzer* analyzer, void* cfg);
int controlflow_analyzer_verify(ControlFlowAnalyzer* analyzer);
int controlflow_analyzer_report(ControlFlowAnalyzer* analyzer);
int controlflow_analyzer_stats(ControlFlowAnalyzer* analyzer);

#endif /* AURORA_CONTROLFLOW_H */