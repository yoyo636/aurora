/*
 * Aurora 编译器中端 - 别名分析器
 * 支持 100+ 别名分析操作
 */

#ifndef AURORA_ALIAS_H
#define AURORA_ALIAS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 别名关系 */
typedef enum {
    ALIAS_MUST,
    ALIAS_MAY,
    ALIAS_NO,
    ALIAS_UNKNOWN,
    ALIAS_PARTIAL,
    ALIAS_FULL,
    ALIAS_FIELD,
    ALIAS_ELEMENT,
    ALIAS_RANGE,
    ALIAS_OFFSET,
    ALIAS_POINTER,
    ALIAS_REFERENCE,
    ALIAS_HANDLE,
    ALIAS_ITERATOR,
    ALIAS_VIEW,
    ALIAS_SPAN,
    ALIAS_SLICE,
    ALIAS_PROXY,
    ALIAS_DELEGATE,
    ALIAS_WRAPPER,
    ALIAS_ADAPTER,
    ALIAS_FACADE,
    ALIAS_COMPOSITE,
    ALIAS_DECORATOR,
    ALIAS_OBSERVER,
    ALIAS_SUBJECT,
    ALIAS_PUBLISHER,
    ALIAS_SUBSCRIBER,
    ALIAS_DISPATCHER,
    ALIAS_SCHEDULER,
    ALIAS_EXECUTOR,
    ALIAS_WORKER,
    ALIAS_THREAD,
    ALIAS_PROCESS,
    ALIAS_FIBER,
    ALIAS_COROUTINE,
    ALIAS_GENERATOR,
    ALIAS_ITERATOR_TYPE,
    ALIAS_STREAM_TYPE,
    ALIAS_CHANNEL_TYPE,
    ALIAS_FUTURE_TYPE,
    ALIAS_PROMISE_TYPE,
    ALIAS_LATCH,
    ALIAS_BARRIER_TYPE,
    ALIAS_SEMAPHORE_TYPE,
    ALIAS_MUTEX_TYPE,
    ALIAS_SPINLOCK_TYPE,
    ALIAS_RWLOCK_TYPE,
    ALIAS_CONDVAR_TYPE,
    ALIAS_ATOMIC_TYPE,
    ALIAS_VOLATILE_TYPE,
    ALIAS_MEMORY_ORDER_TYPE,
    ALIAS_CACHE_LINE,
    ALIAS_FALSE_SHARING,
    ALIAS_TRUE_SHARING,
    ALIAS_CONTENTION,
    ALIAS_LOCK_CONTENTION,
    ALIAS_CACHE_CONTENTION,
    ALIAS_MEMORY_CONTENTION,
    ALIAS_BUS_CONTENTION,
    ALIAS_NETWORK_CONTENTION,
    ALIAS_DISK_CONTENTION,
    ALIAS_DATABASE_CONTENTION,
    ALIAS_FILE_LOCK,
    ALIAS_RECORD_LOCK,
    ALIAS_TABLE_LOCK,
    ALIAS_DATABASE_LOCK,
    ALIAS_TRANSACTION_LOCK,
    ALIAS_OPTIMISTIC_LOCK,
    ALIAS_PESSIMISTIC_LOCK,
    ALIAS_DEADLOCK,
    ALIAS_LIVELOCK,
    ALIAS_STARVATION,
    ALIAS_PRIORITY_INVERSION,
    ALIAS_RACE_CONDITION,
    ALIAS_DATA_RACE,
    ALIAS_ATOMICITY_VIOLATION,
    ALIAS_ORDERING_VIOLATION,
    ALIAS_VISIBILITY_VISIBILITY,
    ALIAS_HAPPENS_BEFORE_VIOLATION,
    ALIAS_SYNCHRONIZES_WITH_VIOLATION,
    ALIAS_MEMORY_MODEL_VIOLATION,
    ALIAS_SEQUENTIAL_CONSISTENCY,
    ALIAS_RELEASE_ACQUIRE,
    ALIAS_RELAXED,
    ALIAS_CONSUME,
    ALIAS_ACQUIRE,
    ALIAS_RELEASE,
    ALIAS_ACQ_REL,
    ALIAS_SEQ_CST,
    ALIAS_COUNT
} AliasRelation;

/* 别名分析器 */
typedef struct AliasAnalyzer {
    int initialized;
    void* alias_sets;
    int set_count;
    int set_capacity;
    void* set_table;
    void* pointer_graph;
    int pointer_count;
    void* points_to;
    int points_to_count;
    void* call_graph;
    int call_count;
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
    int flow_sensitive;
    int context_sensitive;
    int field_sensitive;
    int array_sensitive;
    int path_sensitive;
    int interprocedural;
    int intraprocedural;
    int whole_program;
    int demand_driven;
    int incremental;
    int parallel;
    int max_iterations;
    int max_worklist_size;
    int max_call_depth;
    int max_context_depth;
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
    long long pointers_analyzed;
    long long alias_sets_computed;
    long long points_to_computed;
    long long must_alias;
    long long may_alias;
    long long no_alias;
    long long unknown_alias;
    long long partial_alias;
    long long full_alias;
    long long field_alias;
    long long element_alias;
    long long range_alias;
    long long offset_alias;
    long long pointer_alias;
    long long reference_alias;
    long long handle_alias;
    long long iterator_alias;
    long long view_alias;
    long long span_alias;
    long long slice_alias;
    long long proxy_alias;
    long long delegate_alias;
    long long wrapper_alias;
    long long adapter_alias;
    long long facade_alias;
    long long composite_alias;
    long long decorator_alias;
    long long observer_alias;
    long long subject_alias;
    long long publisher_alias;
    long long subscriber_alias;
    long long dispatcher_alias;
    long long scheduler_alias;
    long long executor_alias;
    long long worker_alias;
    long long thread_alias;
    long long process_alias;
    long long fiber_alias;
    long long coroutine_alias;
    long long generator_alias;
    long long iterator_type_alias;
    long long stream_type_alias;
    long long channel_type_alias;
    long long future_type_alias;
    long long promise_type_alias;
    long long latch_alias;
    long long barrier_type_alias;
    long long semaphore_type_alias;
    long long mutex_type_alias;
    long long spinlock_type_alias;
    long long rwlock_type_alias;
    long long condvar_type_alias;
    long long atomic_type_alias;
    long long volatile_type_alias;
    long long memory_order_type_alias;
    long long cache_line_alias;
    long long false_sharing_detected;
    long long true_sharing_detected;
    long long contention_detected;
    long long lock_contention_detected;
    long long cache_contention_detected;
    long long memory_contention_detected;
    long long bus_contention_detected;
    long long network_contention_detected;
    long long disk_contention_detected;
    long long database_contention_detected;
    long long file_lock_detected;
    long long record_lock_detected;
    long long table_lock_detected;
    long long database_lock_detected;
    long long transaction_lock_detected;
    long long optimistic_lock_detected;
    long long pessimistic_lock_detected;
    long long deadlocks_detected;
    long long livelocks_detected;
    long long starvation_detected;
    long long priority_inversion_detected;
    long long race_conditions_detected;
    long long data_races_detected;
    long long atomicity_violations_detected;
    long long ordering_violations_detected;
    long long visibility_violations_detected;
    long long happens_before_violations_detected;
    long long synchronizes_with_violations_detected;
    long long memory_model_violations_detected;
    long long sequential_consistency_violations;
    long long release_acquire_violations;
    long long relaxed_violations;
    long long consume_violations;
    long long acquire_violations;
    long long release_violations;
    long long acq_rel_violations;
    long long seq_cst_violations;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} AliasAnalyzer;

/* 函数声明 */
int alias_func_000(AliasAnalyzer* analyzer, void* node);
int alias_func_001(AliasAnalyzer* analyzer, void* node);
int alias_func_002(AliasAnalyzer* analyzer, void* node);
int alias_func_003(AliasAnalyzer* analyzer, void* node);
int alias_func_004(AliasAnalyzer* analyzer, void* node);
int alias_func_005(AliasAnalyzer* analyzer, void* node);
int alias_func_006(AliasAnalyzer* analyzer, void* node);
int alias_func_007(AliasAnalyzer* analyzer, void* node);
int alias_func_008(AliasAnalyzer* analyzer, void* node);
int alias_func_009(AliasAnalyzer* analyzer, void* node);
int alias_func_010(AliasAnalyzer* analyzer, void* node);
int alias_func_011(AliasAnalyzer* analyzer, void* node);
int alias_func_012(AliasAnalyzer* analyzer, void* node);
int alias_func_013(AliasAnalyzer* analyzer, void* node);
int alias_func_014(AliasAnalyzer* analyzer, void* node);
int alias_func_015(AliasAnalyzer* analyzer, void* node);
int alias_func_016(AliasAnalyzer* analyzer, void* node);
int alias_func_017(AliasAnalyzer* analyzer, void* node);
int alias_func_018(AliasAnalyzer* analyzer, void* node);
int alias_func_019(AliasAnalyzer* analyzer, void* node);
int alias_func_020(AliasAnalyzer* analyzer, void* node);
int alias_func_021(AliasAnalyzer* analyzer, void* node);
int alias_func_022(AliasAnalyzer* analyzer, void* node);
int alias_func_023(AliasAnalyzer* analyzer, void* node);
int alias_func_024(AliasAnalyzer* analyzer, void* node);
int alias_func_025(AliasAnalyzer* analyzer, void* node);
int alias_func_026(AliasAnalyzer* analyzer, void* node);
int alias_func_027(AliasAnalyzer* analyzer, void* node);
int alias_func_028(AliasAnalyzer* analyzer, void* node);
int alias_func_029(AliasAnalyzer* analyzer, void* node);
int alias_func_030(AliasAnalyzer* analyzer, void* node);
int alias_func_031(AliasAnalyzer* analyzer, void* node);
int alias_func_032(AliasAnalyzer* analyzer, void* node);
int alias_func_033(AliasAnalyzer* analyzer, void* node);
int alias_func_034(AliasAnalyzer* analyzer, void* node);
int alias_func_035(AliasAnalyzer* analyzer, void* node);
int alias_func_036(AliasAnalyzer* analyzer, void* node);
int alias_func_037(AliasAnalyzer* analyzer, void* node);
int alias_func_038(AliasAnalyzer* analyzer, void* node);
int alias_func_039(AliasAnalyzer* analyzer, void* node);
int alias_func_040(AliasAnalyzer* analyzer, void* node);
int alias_func_041(AliasAnalyzer* analyzer, void* node);
int alias_func_042(AliasAnalyzer* analyzer, void* node);
int alias_func_043(AliasAnalyzer* analyzer, void* node);
int alias_func_044(AliasAnalyzer* analyzer, void* node);
int alias_func_045(AliasAnalyzer* analyzer, void* node);
int alias_func_046(AliasAnalyzer* analyzer, void* node);
int alias_func_047(AliasAnalyzer* analyzer, void* node);
int alias_func_048(AliasAnalyzer* analyzer, void* node);
int alias_func_049(AliasAnalyzer* analyzer, void* node);
int alias_func_050(AliasAnalyzer* analyzer, void* node);
int alias_func_051(AliasAnalyzer* analyzer, void* node);
int alias_func_052(AliasAnalyzer* analyzer, void* node);
int alias_func_053(AliasAnalyzer* analyzer, void* node);
int alias_func_054(AliasAnalyzer* analyzer, void* node);
int alias_func_055(AliasAnalyzer* analyzer, void* node);
int alias_func_056(AliasAnalyzer* analyzer, void* node);
int alias_func_057(AliasAnalyzer* analyzer, void* node);
int alias_func_058(AliasAnalyzer* analyzer, void* node);
int alias_func_059(AliasAnalyzer* analyzer, void* node);
int alias_func_060(AliasAnalyzer* analyzer, void* node);
int alias_func_061(AliasAnalyzer* analyzer, void* node);
int alias_func_062(AliasAnalyzer* analyzer, void* node);
int alias_func_063(AliasAnalyzer* analyzer, void* node);
int alias_func_064(AliasAnalyzer* analyzer, void* node);
int alias_func_065(AliasAnalyzer* analyzer, void* node);
int alias_func_066(AliasAnalyzer* analyzer, void* node);
int alias_func_067(AliasAnalyzer* analyzer, void* node);
int alias_func_068(AliasAnalyzer* analyzer, void* node);
int alias_func_069(AliasAnalyzer* analyzer, void* node);
int alias_func_070(AliasAnalyzer* analyzer, void* node);
int alias_func_071(AliasAnalyzer* analyzer, void* node);
int alias_func_072(AliasAnalyzer* analyzer, void* node);
int alias_func_073(AliasAnalyzer* analyzer, void* node);
int alias_func_074(AliasAnalyzer* analyzer, void* node);
int alias_func_075(AliasAnalyzer* analyzer, void* node);
int alias_func_076(AliasAnalyzer* analyzer, void* node);
int alias_func_077(AliasAnalyzer* analyzer, void* node);
int alias_func_078(AliasAnalyzer* analyzer, void* node);
int alias_func_079(AliasAnalyzer* analyzer, void* node);
int alias_func_080(AliasAnalyzer* analyzer, void* node);
int alias_func_081(AliasAnalyzer* analyzer, void* node);
int alias_func_082(AliasAnalyzer* analyzer, void* node);
int alias_func_083(AliasAnalyzer* analyzer, void* node);
int alias_func_084(AliasAnalyzer* analyzer, void* node);
int alias_func_085(AliasAnalyzer* analyzer, void* node);
int alias_func_086(AliasAnalyzer* analyzer, void* node);
int alias_func_087(AliasAnalyzer* analyzer, void* node);
int alias_func_088(AliasAnalyzer* analyzer, void* node);
int alias_func_089(AliasAnalyzer* analyzer, void* node);
int alias_func_090(AliasAnalyzer* analyzer, void* node);
int alias_func_091(AliasAnalyzer* analyzer, void* node);
int alias_func_092(AliasAnalyzer* analyzer, void* node);
int alias_func_093(AliasAnalyzer* analyzer, void* node);
int alias_func_094(AliasAnalyzer* analyzer, void* node);
int alias_func_095(AliasAnalyzer* analyzer, void* node);
int alias_func_096(AliasAnalyzer* analyzer, void* node);
int alias_func_097(AliasAnalyzer* analyzer, void* node);
int alias_func_098(AliasAnalyzer* analyzer, void* node);
int alias_func_099(AliasAnalyzer* analyzer, void* node);
AliasAnalyzer* alias_analyzer_create();
void alias_analyzer_destroy(AliasAnalyzer* analyzer);
int alias_analyzer_init(AliasAnalyzer* analyzer);
int alias_analyzer_analyze(AliasAnalyzer* analyzer, ASTNode* root);
int alias_analyzer_analyze_ir(AliasAnalyzer* analyzer, IRModule* module);
int alias_analyzer_analyze_file(AliasAnalyzer* analyzer, const char* filename);
int alias_analyzer_analyze_pointer(AliasAnalyzer* analyzer, void* pointer);
int alias_analyzer_compute_alias_set(AliasAnalyzer* analyzer, void* pointer);
int alias_analyzer_compute_points_to(AliasAnalyzer* analyzer, void* pointer);
AliasRelation alias_analyzer_query(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_must_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_may_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_no_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_unknown_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_partial_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_full_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_field_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_element_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_range_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_is_offset_alias(AliasAnalyzer* analyzer, void* p1, void* p2);
int alias_analyzer_build_pointer_graph(AliasAnalyzer* analyzer, void* func);
int alias_analyzer_build_call_graph(AliasAnalyzer* analyzer, void* module);
int alias_analyzer_run_worklist(AliasAnalyzer* analyzer);
int alias_analyzer_iterate(AliasAnalyzer* analyzer);
int alias_analyzer_verify(AliasAnalyzer* analyzer);
int alias_analyzer_report(AliasAnalyzer* analyzer);
int alias_analyzer_stats(AliasAnalyzer* analyzer);

#endif /* AURORA_ALIAS_H */