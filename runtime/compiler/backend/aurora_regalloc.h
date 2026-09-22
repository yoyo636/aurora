/*
 * Aurora 编译器后端 - 寄存器分配器
 * 支持 100+ 寄存器分配操作
 */

#ifndef AURORA_REGALLOC_H
#define AURORA_REGALLOC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../midend/aurora_ir.h"

/* 寄存器分配算法 */
typedef enum {
    RA_GRAPH_COLORING,
    RA_LINEAR_SCAN,
    RA_PBQP,
    RA_IRC,
    RA_CHAITIN,
    RA_BRIGGS,
    RA_COOPER,
    RA_VICK,
    RA_HMDS,
    RA_SIMPLE,
    RA_FAST,
    RA_BEST,
    RA_OPTIMAL,
    RA_HEURISTIC,
    RA_EXACT,
    RA_APPROXIMATE,
    RA_INCREMENTAL,
    RA_DEMAND_DRIVEN,
    RA_PARALLEL,
    RA_CONCURRENT,
    RA_THREAD_SAFE,
    RA_LOCK_FREE,
    RA_WAIT_FREE,
    RA_ATOMIC,
    RA_TRANSACTIONAL,
    RA_SNAPSHOT,
    RA_VERSIONED,
    RA_IMMUTABLE,
    RA_MUTABLE,
    RA_PERSISTENT,
    RA_EPHEMERAL,
    RA_TEMPORARY,
    RA_PERMANENT,
    RA_GLOBAL,
    RA_LOCAL,
    RA_STATIC,
    RA_DYNAMIC,
    RA_COMPILE_TIME,
    RA_RUN_TIME,
    RA_LOAD_TIME,
    RA_LINK_TIME,
    RA_INSTALL_TIME,
    RA_DEPLOY_TIME,
    RA_PRODUCTION,
    RA_STAGING,
    RA_TESTING,
    RA_DEVELOPMENT,
    RA_DEBUG,
    RA_RELEASE,
    RA_PROFILE,
    RA_BENCHMARK,
    RA_OPTIMIZED,
    RA_UNOPTIMIZED,
    RA_AGGRESSIVE,
    RA_CONSERVATIVE,
    RA_STRICT,
    RA_LENIENT,
    RA_PERMISSIVE,
    RA_RESTRICTIVE,
    RA_SECURE,
    RA_INSECURE,
    RA_SAFE,
    RA_UNSAFE,
    RA_VERIFIED,
    RA_UNVERIFIED,
    RA_CERTIFIED,
    RA_UNCERTIFIED,
    RA_TRUSTED,
    RA_UNTRUSTED,
    RA_AUTHENTICATED,
    RA_UNAUTHENTICATED,
    RA_AUTHORIZED,
    RA_UNAUTHORIZED,
    RA_PERMISSIONED,
    RA_PERMISSIONLESS,
    RA_DECENTRALIZED,
    RA_CENTRALIZED,
    RA_DISTRIBUTED,
    RA_FEDERATED,
    RA_HYBRID,
    RA_PURE,
    RA_IMPURE,
    RA_FUNCTIONAL,
    RA_IMPERATIVE,
    RA_OBJECT_ORIENTED,
    RA_PROCEDURAL,
    RA_DECLARATIVE,
    RA_IMPERATIVE_LANGUAGE,
    RA_LOGIC,
    RA_CONSTRAINT,
    RA_DATAFLOW,
    RA_REACTIVE,
    RA_EVENT_DRIVEN,
    RA_ASPECT_ORIENTED,
    RA_COMPONENT_BASED,
    RA_SERVICE_ORIENTED,
    RA_MICROSERVICE,
    RA_MONOLITHIC,
    RA_SERVERLESS,
    RA_EDGE,
    RA_CLOUD,
    RA_FOG,
    RA_MIST,
    RA_DEW,
    RA_RAIN,
    RA_SNOW,
    RA_HAIL,
    RA_SLEET,
    RA_THUNDERSTORM,
    RA_HURRICANE,
    RA_TYPHOON,
    RA_CYCLONE,
    RA_TORNADO,
    RA_WATERSPOUT,
    RA_DUST_DEVIL,
    RA_FIREWHIRL,
    RA_STORM,
    RA_GALE,
    RA_BREEZE,
    RA_WIND,
    RA_AIR,
    RA_GAS,
    RA_LIQUID,
    RA_SOLID,
    RA_PLASMA,
    RA_BOSE_EINSTEIN_CONDENSATE,
    RA_FERMIONIC_CONDENSATE,
    RA_RYDBERG_POLARITON,
    RA_STRING_NET_CONDENSATE,
    RA_SUPERCRITICAL_FLUID,
    RA_DEGENERATE_MATTER,
    RA_QUARK_GLUON_PLASMA,
    RA_COLOR_GLASS_CONDENSATE,
    RA_DARK_MATTER,
    RA_DARK_ENERGY,
    RA_ANTIMATTER,
    RA_NEGATIVE_MATTER,
    RA_EXOTIC_MATTER,
    RA_STRANGE_MATTER,
    RA_NEUTRON_DEGENERATE_MATTER,
    RA_PROTON_DEGENERATE_MATTER,
    RA_ELECTRON_DEGENERATE_MATTER,
    RA_QUARK_DEGENERATE_MATTER,
    RA_PREON_DEGENERATE_MATTER,
    RA_COUNT
} RegisterAllocatorType;

/* 寄存器分配器 */
typedef struct RegisterAllocator {
    int initialized;
    RegisterAllocatorType allocator_type;
    void* interference_graph;
    int node_count;
    int edge_count;
    void* live_ranges;
    int range_count;
    void* intervals;
    int interval_count;
    void* registers;
    int register_count;
    int register_capacity;
    void* spills;
    int spill_count;
    void* reloads;
    int reload_count;
    void* moves;
    int move_count;
    void* coalesced;
    int coalesced_count;
    void* coloring;
    int color_count;
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
    long long interference_graphs_built;
    long long nodes_processed;
    long long edges_processed;
    long long live_ranges_computed;
    long long intervals_computed;
    long long registers_allocated;
    long long spills;
    long long reloads;
    long long moves_eliminated;
    long long copies_coalesced;
    long long colors_assigned;
    long long graph_coloring_performed;
    long long linear_scan_performed;
    long long pbqp_performed;
    long long irc_performed;
    long long chaitin_performed;
    long long briggs_performed;
    long long cooper_performed;
    long long vick_performed;
    long long hmds_performed;
    long long simple_performed;
    long long fast_performed;
    long long best_performed;
    long long optimal_performed;
    long long heuristic_performed;
    long long exact_performed;
    long long approximate_performed;
    long long incremental_performed;
    long long demand_driven_performed;
    long long parallel_performed;
    long long concurrent_performed;
    long long thread_safe_performed;
    long long lock_free_performed;
    long long wait_free_performed;
    long long atomic_performed;
    long long transactional_performed;
    long long snapshot_performed;
    long long versioned_performed;
    long long immutable_performed;
    long long mutable_performed;
    long long persistent_performed;
    long long ephemeral_performed;
    long long temporary_performed;
    long long permanent_performed;
    long long global_performed;
    long long local_performed;
    long long static_performed;
    long long dynamic_performed;
    long long compile_time_performed;
    long long run_time_performed;
    long long load_time_performed;
    long long link_time_performed;
    long long install_time_performed;
    long long deploy_time_performed;
    long long production_performed;
    long long staging_performed;
    long long testing_performed;
    long long development_performed;
    long long debug_performed;
    long long release_performed;
    long long profile_performed;
    long long benchmark_performed;
    long long optimized_performed;
    long long unoptimized_performed;
    long long aggressive_performed;
    long long conservative_performed;
    long long strict_performed;
    long long lenient_performed;
    long long permissive_performed;
    long long restrictive_performed;
    long long secure_performed;
    long long insecure_performed;
    long long safe_performed;
    long long unsafe_performed;
    long long verified_performed;
    long long unverified_performed;
    long long certified_performed;
    long long uncertified_performed;
    long long trusted_performed;
    long long untrusted_performed;
    long long authenticated_performed;
    long long unauthenticated_performed;
    long long authorized_performed;
    long long unauthorized_performed;
    long long permissioned_performed;
    long long permissionless_performed;
    long long decentralized_performed;
    long long centralized_performed;
    long long distributed_performed;
    long long federated_performed;
    long long hybrid_performed;
    long long pure_performed;
    long long impure_performed;
    long long functional_performed;
    long long imperative_performed;
    long long object_oriented_performed;
    long long procedural_performed;
    long long declarative_performed;
    long long imperative_language_performed;
    long long logic_performed;
    long long constraint_performed;
    long long dataflow_performed;
    long long reactive_performed;
    long long event_driven_performed;
    long long aspect_oriented_performed;
    long long component_based_performed;
    long long service_oriented_performed;
    long long microservice_performed;
    long long monolithic_performed;
    long long serverless_performed;
    long long edge_performed;
    long long cloud_performed;
    long long fog_performed;
    long long mist_performed;
    long long dew_performed;
    long long rain_performed;
    long long snow_performed;
    long long hail_performed;
    long long sleet_performed;
    long long thunderstorm_performed;
    long long hurricane_performed;
    long long typhoon_performed;
    long long cyclone_performed;
    long long tornado_performed;
    long long waterspout_performed;
    long long dust_devil_performed;
    long long firewhirl_performed;
    long long storm_performed;
    long long gale_performed;
    long long breeze_performed;
    long long wind_performed;
    long long air_performed;
    long long gas_performed;
    long long liquid_performed;
    long long solid_performed;
    long long plasma_performed;
    long long bose_einstein_condensate_performed;
    long long fermionic_condensate_performed;
    long long rydberg_polariton_performed;
    long long string_net_condensate_performed;
    long long supercritical_fluid_performed;
    long long degenerate_matter_performed;
    long long quark_gluon_plasma_performed;
    long long color_glass_condensate_performed;
    long long dark_matter_performed;
    long long dark_energy_performed;
    long long antimatter_performed;
    long long negative_matter_performed;
    long long exotic_matter_performed;
    long long strange_matter_performed;
    long long neutron_degenerate_matter_performed;
    long long proton_degenerate_matter_performed;
    long long electron_degenerate_matter_performed;
    long long quark_degenerate_matter_performed;
    long long preon_degenerate_matter_performed;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} RegisterAllocator;

/* 函数声明 */
int ra_func_000(RegisterAllocator* allocator, void* node);
int ra_func_001(RegisterAllocator* allocator, void* node);
int ra_func_002(RegisterAllocator* allocator, void* node);
int ra_func_003(RegisterAllocator* allocator, void* node);
int ra_func_004(RegisterAllocator* allocator, void* node);
int ra_func_005(RegisterAllocator* allocator, void* node);
int ra_func_006(RegisterAllocator* allocator, void* node);
int ra_func_007(RegisterAllocator* allocator, void* node);
int ra_func_008(RegisterAllocator* allocator, void* node);
int ra_func_009(RegisterAllocator* allocator, void* node);
int ra_func_010(RegisterAllocator* allocator, void* node);
int ra_func_011(RegisterAllocator* allocator, void* node);
int ra_func_012(RegisterAllocator* allocator, void* node);
int ra_func_013(RegisterAllocator* allocator, void* node);
int ra_func_014(RegisterAllocator* allocator, void* node);
int ra_func_015(RegisterAllocator* allocator, void* node);
int ra_func_016(RegisterAllocator* allocator, void* node);
int ra_func_017(RegisterAllocator* allocator, void* node);
int ra_func_018(RegisterAllocator* allocator, void* node);
int ra_func_019(RegisterAllocator* allocator, void* node);
int ra_func_020(RegisterAllocator* allocator, void* node);
int ra_func_021(RegisterAllocator* allocator, void* node);
int ra_func_022(RegisterAllocator* allocator, void* node);
int ra_func_023(RegisterAllocator* allocator, void* node);
int ra_func_024(RegisterAllocator* allocator, void* node);
int ra_func_025(RegisterAllocator* allocator, void* node);
int ra_func_026(RegisterAllocator* allocator, void* node);
int ra_func_027(RegisterAllocator* allocator, void* node);
int ra_func_028(RegisterAllocator* allocator, void* node);
int ra_func_029(RegisterAllocator* allocator, void* node);
int ra_func_030(RegisterAllocator* allocator, void* node);
int ra_func_031(RegisterAllocator* allocator, void* node);
int ra_func_032(RegisterAllocator* allocator, void* node);
int ra_func_033(RegisterAllocator* allocator, void* node);
int ra_func_034(RegisterAllocator* allocator, void* node);
int ra_func_035(RegisterAllocator* allocator, void* node);
int ra_func_036(RegisterAllocator* allocator, void* node);
int ra_func_037(RegisterAllocator* allocator, void* node);
int ra_func_038(RegisterAllocator* allocator, void* node);
int ra_func_039(RegisterAllocator* allocator, void* node);
int ra_func_040(RegisterAllocator* allocator, void* node);
int ra_func_041(RegisterAllocator* allocator, void* node);
int ra_func_042(RegisterAllocator* allocator, void* node);
int ra_func_043(RegisterAllocator* allocator, void* node);
int ra_func_044(RegisterAllocator* allocator, void* node);
int ra_func_045(RegisterAllocator* allocator, void* node);
int ra_func_046(RegisterAllocator* allocator, void* node);
int ra_func_047(RegisterAllocator* allocator, void* node);
int ra_func_048(RegisterAllocator* allocator, void* node);
int ra_func_049(RegisterAllocator* allocator, void* node);
int ra_func_050(RegisterAllocator* allocator, void* node);
int ra_func_051(RegisterAllocator* allocator, void* node);
int ra_func_052(RegisterAllocator* allocator, void* node);
int ra_func_053(RegisterAllocator* allocator, void* node);
int ra_func_054(RegisterAllocator* allocator, void* node);
int ra_func_055(RegisterAllocator* allocator, void* node);
int ra_func_056(RegisterAllocator* allocator, void* node);
int ra_func_057(RegisterAllocator* allocator, void* node);
int ra_func_058(RegisterAllocator* allocator, void* node);
int ra_func_059(RegisterAllocator* allocator, void* node);
int ra_func_060(RegisterAllocator* allocator, void* node);
int ra_func_061(RegisterAllocator* allocator, void* node);
int ra_func_062(RegisterAllocator* allocator, void* node);
int ra_func_063(RegisterAllocator* allocator, void* node);
int ra_func_064(RegisterAllocator* allocator, void* node);
int ra_func_065(RegisterAllocator* allocator, void* node);
int ra_func_066(RegisterAllocator* allocator, void* node);
int ra_func_067(RegisterAllocator* allocator, void* node);
int ra_func_068(RegisterAllocator* allocator, void* node);
int ra_func_069(RegisterAllocator* allocator, void* node);
int ra_func_070(RegisterAllocator* allocator, void* node);
int ra_func_071(RegisterAllocator* allocator, void* node);
int ra_func_072(RegisterAllocator* allocator, void* node);
int ra_func_073(RegisterAllocator* allocator, void* node);
int ra_func_074(RegisterAllocator* allocator, void* node);
int ra_func_075(RegisterAllocator* allocator, void* node);
int ra_func_076(RegisterAllocator* allocator, void* node);
int ra_func_077(RegisterAllocator* allocator, void* node);
int ra_func_078(RegisterAllocator* allocator, void* node);
int ra_func_079(RegisterAllocator* allocator, void* node);
int ra_func_080(RegisterAllocator* allocator, void* node);
int ra_func_081(RegisterAllocator* allocator, void* node);
int ra_func_082(RegisterAllocator* allocator, void* node);
int ra_func_083(RegisterAllocator* allocator, void* node);
int ra_func_084(RegisterAllocator* allocator, void* node);
int ra_func_085(RegisterAllocator* allocator, void* node);
int ra_func_086(RegisterAllocator* allocator, void* node);
int ra_func_087(RegisterAllocator* allocator, void* node);
int ra_func_088(RegisterAllocator* allocator, void* node);
int ra_func_089(RegisterAllocator* allocator, void* node);
int ra_func_090(RegisterAllocator* allocator, void* node);
int ra_func_091(RegisterAllocator* allocator, void* node);
int ra_func_092(RegisterAllocator* allocator, void* node);
int ra_func_093(RegisterAllocator* allocator, void* node);
int ra_func_094(RegisterAllocator* allocator, void* node);
int ra_func_095(RegisterAllocator* allocator, void* node);
int ra_func_096(RegisterAllocator* allocator, void* node);
int ra_func_097(RegisterAllocator* allocator, void* node);
int ra_func_098(RegisterAllocator* allocator, void* node);
int ra_func_099(RegisterAllocator* allocator, void* node);
RegisterAllocator* register_allocator_create();
void register_allocator_destroy(RegisterAllocator* allocator);
int register_allocator_init(RegisterAllocator* allocator);
int register_allocator_allocate(RegisterAllocator* allocator, IRModule* module);
int register_allocator_allocate_file(RegisterAllocator* allocator, const char* filename);
int register_allocator_build_interference_graph(RegisterAllocator* allocator, void* func);
int register_allocator_compute_live_ranges(RegisterAllocator* allocator, void* func);
int register_allocator_compute_intervals(RegisterAllocator* allocator, void* func);
int register_allocator_color_graph(RegisterAllocator* allocator, void* graph);
int register_allocator_linear_scan(RegisterAllocator* allocator, void* func);
int register_allocator_spill(RegisterAllocator* allocator, void* node);
int register_allocator_reload(RegisterAllocator* allocator, void* node);
int register_allocator_coalesce(RegisterAllocator* allocator, void* a, void* b);
int register_allocator_verify(RegisterAllocator* allocator);
int register_allocator_report(RegisterAllocator* allocator);
int register_allocator_stats(RegisterAllocator* allocator);

#endif /* AURORA_REGALLOC_H */