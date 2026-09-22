/*
 * Aurora 编译器中端 - 逃逸分析器
 * 支持 100+ 逃逸分析操作
 */

#ifndef AURORA_ESCAPE_H
#define AURORA_ESCAPE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../frontend/aurora_ast.h"
#include "aurora_ir.h"

/* 逃逸状态 */
typedef enum {
    ESCAPE_UNKNOWN,
    ESCAPE_NONE,
    ESCAPE_LOCAL,
    ESCAPE_ARGUMENT,
    ESCAPE_RETURN,
    ESCAPE_GLOBAL,
    ESCAPE_THREAD,
    ESCAPE_HEAP,
    ESCAPE_STACK,
    ESCAPE_REGISTER,
    ESCAPE_MEMORY,
    ESCAPE_FILE,
    ESCAPE_NETWORK,
    ESCAPE_DATABASE,
    ESCAPE_CACHE,
    ESCAPE_SESSION,
    ESCAPE_COOKIE,
    ESCAPE_HEADER,
    ESCAPE_BODY,
    ESCAPE_PARAMETER,
    ESCAPE_VARIABLE,
    ESCAPE_CONSTANT,
    ESCAPE_LITERAL,
    ESCAPE_STRING,
    ESCAPE_ARRAY,
    ESCAPE_STRUCT,
    ESCAPE_UNION,
    ESCAPE_ENUM,
    ESCAPE_POINTER,
    ESCAPE_REFERENCE,
    ESCAPE_OBJECT,
    ESCAPE_CLASS,
    ESCAPE_INTERFACE,
    ESCAPE_TRAIT,
    ESCAPE_PROTOCOL,
    ESCAPE_CONCEPT,
    ESCAPE_TYPECLASS,
    ESCAPE_MODULE,
    ESCAPE_NAMESPACE,
    ESCAPE_PACKAGE,
    ESCAPE_LIBRARY,
    ESCAPE_FRAMEWORK,
    ESCAPE_PLUGIN,
    ESCAPE_EXTENSION,
    ESCAPE_ADDON,
    ESCAPE_MODULE_EXTENSION,
    ESCAPE_THREAD_LOCAL,
    ESCAPE_STATIC,
    ESCAPE_GLOBAL_VAR,
    ESCAPE_EXTERN,
    ESCAPE_IMPORT,
    ESCAPE_EXPORT,
    ESCAPE_FORWARD,
    ESCAPE_DECLARATION,
    ESCAPE_DEFINITION,
    ESCAPE_ALIAS,
    ESCAPE_TYPEDEF,
    ESCAPE_USING,
    ESCAPE_MACRO,
    ESCAPE_TEMPLATE,
    ESCAPE_GENERIC,
    ESCAPE_SPECIALIZATION,
    ESCAPE_INSTANTIATION,
    ESCAPE_MONOMORPHIZATION,
    ESCAPE_DEVIRTUALIZATION,
    ESCAPE_INLINING,
    ESCAPE_CLONING,
    ESCAPE_COPYING,
    ESCAPE_MOVING,
    ESCAPE_ASSIGNMENT,
    ESCAPE_INITIALIZATION,
    ESCAPE_DESTRUCTION,
    ESCAPE_FINALIZATION,
    ESCAPE_CONSTRUCTION,
    ESCAPE_COPY_CONSTRUCTION,
    ESCAPE_MOVE_CONSTRUCTION,
    ESCAPE_COPY_ASSIGNMENT,
    ESCAPE_MOVE_ASSIGNMENT,
    ESCAPE_DEFAULT_CONSTRUCTION,
    ESCAPE_VALUE_CONSTRUCTION,
    ESCAPE_AGGREGATE_CONSTRUCTION,
    ESCAPE_LIST_CONSTRUCTION,
    ESCAPE_BRACE_CONSTRUCTION,
    ESCAPE_PAREN_CONSTRUCTION,
    ESCAPE_FUNCTION_CALL,
    ESCAPE_METHOD_CALL,
    ESCAPE_OPERATOR_CALL,
    ESCAPE_CONSTRUCTOR_CALL,
    ESCAPE_DESTRUCTOR_CALL,
    ESCAPE_VIRTUAL_CALL,
    ESCAPE_INTERFACE_CALL,
    ESCAPE_TRAIT_CALL,
    ESCAPE_PROTOCOL_CALL,
    ESCAPE_CONCEPT_CALL,
    ESCAPE_TYPECLASS_CALL,
    ESCAPE_LAMBDA,
    ESCAPE_CLOSURE,
    ESCAPE_FUNCTOR,
    ESCAPE_FUNCTION_OBJECT,
    ESCAPE_CALLABLE,
    ESCAPE_INVOCABLE,
    ESCAPE_DELEGATE,
    ESCAPE_EVENT_HANDLER,
    ESCAPE_CALLBACK,
    ESCAPE_LISTENER,
    ESCAPE_OBSERVER,
    ESCAPE_SUBSCRIBER,
    ESCAPE_PUBLISHER,
    ESCAPE_DISPATCHER,
    ESCAPE_SCHEDULER,
    ESCAPE_EXECUTOR,
    ESCAPE_WORKER,
    ESCAPE_THREAD_POOL,
    ESCAPE_TASK_QUEUE,
    ESCAPE_FUTURE,
    ESCAPE_PROMISE,
    ESCAPE_CHANNEL,
    ESCAPE_STREAM,
    ESCAPE_ITERATOR,
    ESCAPE_GENERATOR,
    ESCAPE_COROUTINE,
    ESCAPE_ASYNC,
    ESCAPE_AWAIT,
    ESCAPE_YIELD,
    ESCAPE_SUSPEND,
    ESCAPE_RESUME,
    ESCAPE_CANCEL,
    ESCAPE_TIMEOUT,
    ESCAPE_RETRY,
    ESCAPE_FALLBACK,
    ESCAPE_RECOVERY,
    ESCAPE_COMPENSATION,
    ESCAPE_SAGA,
    ESCAPE_TRANSACTION,
    ESCAPE_COMMIT,
    ESCAPE_ROLLBACK,
    ESCAPE_SAVEPOINT,
    ESCAPE_CHECKPOINT,
    ESCAPE_SNAPSHOT,
    ESCAPE_BACKUP,
    ESCAPE_RESTORE,
    ESCAPE_MIGRATION,
    ESCAPE_REPLICATION,
    ESCAPE_SYNCHRONIZATION,
    ESCAPE_LOCK,
    ESCAPE_UNLOCK,
    ESCAPE_MUTEX,
    ESCAPE_SPINLOCK,
    ESCAPE_RWLOCK,
    ESCAPE_SEMAPHORE,
    ESCAPE_CONDITION_VARIABLE,
    ESCAPE_BARRIER,
    ESCAPE_LATCH,
    ESCAPE_GATE,
    ESCAPE_FENCE,
    ESCAPE_ATOMIC,
    ESCAPE_VOLATILE,
    ESCAPE_MEMORY_ORDER,
    ESCAPE_HAPPENS_BEFORE,
    ESCAPE_SYNCHRONIZES_WITH,
    ESCAPE_INTERTHREAD_HAPPENS_BEFORE,
    ESCAPE_SEQUENCED_BEFORE,
    ESCAPE_CARRIES_DEPENDENCY,
    ESCAPE_DEPENDENCY_ORDERED_BEFORE,
    ESCAPE_WEAKLY_CARRIES_DEPENDENCY,
    ESCAPE_SIMPLE_DEPENDENCY_ORDERED_BEFORE,
    ESCAPE_COUNT
} EscapeState;

/* 逃逸分析器 */
typedef struct EscapeAnalyzer {
    int initialized;
    void* escape_states;
    int state_count;
    int state_capacity;
    void* state_table;
    void* allocation_sites;
    int allocation_count;
    void* pointer_graph;
    int pointer_count;
    void* points_to_set;
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
    int allow_unsafe;
    int allow_undefined_behavior;
    int allow_side_effects;
    int allow_io;
    int allow_allocation;
    int allow_recursion;
    int allow_threads;
    int allow_concurrency;
    int allow_parallelism;
    int allow_distributed;
    int max_iterations;
    int max_worklist_size;
    int max_call_depth;
    int max_pointer_depth;
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
    long long allocations_analyzed;
    long long allocations_stack_allocated;
    long long allocations_heap_allocated;
    long long allocations_eliminated;
    long long allocations_merged;
    long long allocations_reused;
    long long pointers_analyzed;
    long long points_to_computed;
    long long escape_states_computed;
    long long no_escape;
    long long local_escape;
    long long argument_escape;
    long long return_escape;
    long long global_escape;
    long long thread_escape;
    long long heap_escape;
    long long stack_escape;
    long long register_escape;
    long long memory_escape;
    long long file_escape;
    long long network_escape;
    long long database_escape;
    long long cache_escape;
    long long session_escape;
    long long cookie_escape;
    long long header_escape;
    long long body_escape;
    long long parameter_escape;
    long long variable_escape;
    long long constant_escape;
    long long literal_escape;
    long long string_escape;
    long long array_escape;
    long long struct_escape;
    long long union_escape;
    long long enum_escape;
    long long pointer_escape;
    long long reference_escape;
    long long object_escape;
    long long class_escape;
    long long interface_escape;
    long long trait_escape;
    long long protocol_escape;
    long long concept_escape;
    long long typeclass_escape;
    long long module_escape;
    long long namespace_escape;
    long long package_escape;
    long long library_escape;
    long long framework_escape;
    long long plugin_escape;
    long long extension_escape;
    long long addon_escape;
    long long module_extension_escape;
    long long thread_local_escape;
    long long static_escape;
    long long global_var_escape;
    long long extern_escape;
    long long import_escape;
    long long export_escape;
    long long forward_escape;
    long long declaration_escape;
    long long definition_escape;
    long long alias_escape;
    long long typedef_escape;
    long long using_escape;
    long long macro_escape;
    long long template_escape;
    long long generic_escape;
    long long specialization_escape;
    long long instantiation_escape;
    long long monomorphization_escape;
    long long devirtualization_escape;
    long long inlining_escape;
    long long cloning_escape;
    long long copying_escape;
    long long moving_escape;
    long long assignment_escape;
    long long initialization_escape;
    long long destruction_escape;
    long long finalization_escape;
    long long construction_escape;
    long long copy_construction_escape;
    long long move_construction_escape;
    long long copy_assignment_escape;
    long long move_assignment_escape;
    long long default_construction_escape;
    long long value_construction_escape;
    long long aggregate_construction_escape;
    long long list_construction_escape;
    long long brace_construction_escape;
    long long paren_construction_escape;
    long long function_call_escape;
    long long method_call_escape;
    long long operator_call_escape;
    long long constructor_call_escape;
    long long destructor_call_escape;
    long long virtual_call_escape;
    long long interface_call_escape;
    long long trait_call_escape;
    long long protocol_call_escape;
    long long concept_call_escape;
    long long typeclass_call_escape;
    long long lambda_escape;
    long long closure_escape;
    long long functor_escape;
    long long function_object_escape;
    long long callable_escape;
    long long invocable_escape;
    long long delegate_escape;
    long long event_handler_escape;
    long long callback_escape;
    long long listener_escape;
    long long observer_escape;
    long long subscriber_escape;
    long long publisher_escape;
    long long dispatcher_escape;
    long long scheduler_escape;
    long long executor_escape;
    long long worker_escape;
    long long thread_pool_escape;
    long long task_queue_escape;
    long long future_escape;
    long long promise_escape;
    long long channel_escape;
    long long stream_escape;
    long long iterator_escape;
    long long generator_escape;
    long long coroutine_escape;
    long long async_escape;
    long long await_escape;
    long long yield_escape;
    long long suspend_escape;
    long long resume_escape;
    long long cancel_escape;
    long long timeout_escape;
    long long retry_escape;
    long long fallback_escape;
    long long recovery_escape;
    long long compensation_escape;
    long long saga_escape;
    long long transaction_escape;
    long long commit_escape;
    long long rollback_escape;
    long long savepoint_escape;
    long long checkpoint_escape;
    long long snapshot_escape;
    long long backup_escape;
    long long restore_escape;
    long long migration_escape;
    long long replication_escape;
    long long synchronization_escape;
    long long lock_escape;
    long long unlock_escape;
    long long mutex_escape;
    long long spinlock_escape;
    long long rwlock_escape;
    long long semaphore_escape;
    long long condition_variable_escape;
    long long barrier_escape;
    long long latch_escape;
    long long gate_escape;
    long long fence_escape;
    long long atomic_escape;
    long long volatile_escape;
    long long memory_order_escape;
    long long happens_before_escape;
    long long synchronizes_with_escape;
    long long interthread_happens_before_escape;
    long long sequenced_before_escape;
    long long carries_dependency_escape;
    long long dependency_ordered_before_escape;
    long long weakly_carries_dependency_escape;
    long long simple_dependency_ordered_before_escape;
    long long bytes_saved;
    long long lines_saved;
    long long characters_saved;
} EscapeAnalyzer;

/* 函数声明 */
int escape_func_000(EscapeAnalyzer* analyzer, void* node);
int escape_func_001(EscapeAnalyzer* analyzer, void* node);
int escape_func_002(EscapeAnalyzer* analyzer, void* node);
int escape_func_003(EscapeAnalyzer* analyzer, void* node);
int escape_func_004(EscapeAnalyzer* analyzer, void* node);
int escape_func_005(EscapeAnalyzer* analyzer, void* node);
int escape_func_006(EscapeAnalyzer* analyzer, void* node);
int escape_func_007(EscapeAnalyzer* analyzer, void* node);
int escape_func_008(EscapeAnalyzer* analyzer, void* node);
int escape_func_009(EscapeAnalyzer* analyzer, void* node);
int escape_func_010(EscapeAnalyzer* analyzer, void* node);
int escape_func_011(EscapeAnalyzer* analyzer, void* node);
int escape_func_012(EscapeAnalyzer* analyzer, void* node);
int escape_func_013(EscapeAnalyzer* analyzer, void* node);
int escape_func_014(EscapeAnalyzer* analyzer, void* node);
int escape_func_015(EscapeAnalyzer* analyzer, void* node);
int escape_func_016(EscapeAnalyzer* analyzer, void* node);
int escape_func_017(EscapeAnalyzer* analyzer, void* node);
int escape_func_018(EscapeAnalyzer* analyzer, void* node);
int escape_func_019(EscapeAnalyzer* analyzer, void* node);
int escape_func_020(EscapeAnalyzer* analyzer, void* node);
int escape_func_021(EscapeAnalyzer* analyzer, void* node);
int escape_func_022(EscapeAnalyzer* analyzer, void* node);
int escape_func_023(EscapeAnalyzer* analyzer, void* node);
int escape_func_024(EscapeAnalyzer* analyzer, void* node);
int escape_func_025(EscapeAnalyzer* analyzer, void* node);
int escape_func_026(EscapeAnalyzer* analyzer, void* node);
int escape_func_027(EscapeAnalyzer* analyzer, void* node);
int escape_func_028(EscapeAnalyzer* analyzer, void* node);
int escape_func_029(EscapeAnalyzer* analyzer, void* node);
int escape_func_030(EscapeAnalyzer* analyzer, void* node);
int escape_func_031(EscapeAnalyzer* analyzer, void* node);
int escape_func_032(EscapeAnalyzer* analyzer, void* node);
int escape_func_033(EscapeAnalyzer* analyzer, void* node);
int escape_func_034(EscapeAnalyzer* analyzer, void* node);
int escape_func_035(EscapeAnalyzer* analyzer, void* node);
int escape_func_036(EscapeAnalyzer* analyzer, void* node);
int escape_func_037(EscapeAnalyzer* analyzer, void* node);
int escape_func_038(EscapeAnalyzer* analyzer, void* node);
int escape_func_039(EscapeAnalyzer* analyzer, void* node);
int escape_func_040(EscapeAnalyzer* analyzer, void* node);
int escape_func_041(EscapeAnalyzer* analyzer, void* node);
int escape_func_042(EscapeAnalyzer* analyzer, void* node);
int escape_func_043(EscapeAnalyzer* analyzer, void* node);
int escape_func_044(EscapeAnalyzer* analyzer, void* node);
int escape_func_045(EscapeAnalyzer* analyzer, void* node);
int escape_func_046(EscapeAnalyzer* analyzer, void* node);
int escape_func_047(EscapeAnalyzer* analyzer, void* node);
int escape_func_048(EscapeAnalyzer* analyzer, void* node);
int escape_func_049(EscapeAnalyzer* analyzer, void* node);
int escape_func_050(EscapeAnalyzer* analyzer, void* node);
int escape_func_051(EscapeAnalyzer* analyzer, void* node);
int escape_func_052(EscapeAnalyzer* analyzer, void* node);
int escape_func_053(EscapeAnalyzer* analyzer, void* node);
int escape_func_054(EscapeAnalyzer* analyzer, void* node);
int escape_func_055(EscapeAnalyzer* analyzer, void* node);
int escape_func_056(EscapeAnalyzer* analyzer, void* node);
int escape_func_057(EscapeAnalyzer* analyzer, void* node);
int escape_func_058(EscapeAnalyzer* analyzer, void* node);
int escape_func_059(EscapeAnalyzer* analyzer, void* node);
int escape_func_060(EscapeAnalyzer* analyzer, void* node);
int escape_func_061(EscapeAnalyzer* analyzer, void* node);
int escape_func_062(EscapeAnalyzer* analyzer, void* node);
int escape_func_063(EscapeAnalyzer* analyzer, void* node);
int escape_func_064(EscapeAnalyzer* analyzer, void* node);
int escape_func_065(EscapeAnalyzer* analyzer, void* node);
int escape_func_066(EscapeAnalyzer* analyzer, void* node);
int escape_func_067(EscapeAnalyzer* analyzer, void* node);
int escape_func_068(EscapeAnalyzer* analyzer, void* node);
int escape_func_069(EscapeAnalyzer* analyzer, void* node);
int escape_func_070(EscapeAnalyzer* analyzer, void* node);
int escape_func_071(EscapeAnalyzer* analyzer, void* node);
int escape_func_072(EscapeAnalyzer* analyzer, void* node);
int escape_func_073(EscapeAnalyzer* analyzer, void* node);
int escape_func_074(EscapeAnalyzer* analyzer, void* node);
int escape_func_075(EscapeAnalyzer* analyzer, void* node);
int escape_func_076(EscapeAnalyzer* analyzer, void* node);
int escape_func_077(EscapeAnalyzer* analyzer, void* node);
int escape_func_078(EscapeAnalyzer* analyzer, void* node);
int escape_func_079(EscapeAnalyzer* analyzer, void* node);
int escape_func_080(EscapeAnalyzer* analyzer, void* node);
int escape_func_081(EscapeAnalyzer* analyzer, void* node);
int escape_func_082(EscapeAnalyzer* analyzer, void* node);
int escape_func_083(EscapeAnalyzer* analyzer, void* node);
int escape_func_084(EscapeAnalyzer* analyzer, void* node);
int escape_func_085(EscapeAnalyzer* analyzer, void* node);
int escape_func_086(EscapeAnalyzer* analyzer, void* node);
int escape_func_087(EscapeAnalyzer* analyzer, void* node);
int escape_func_088(EscapeAnalyzer* analyzer, void* node);
int escape_func_089(EscapeAnalyzer* analyzer, void* node);
int escape_func_090(EscapeAnalyzer* analyzer, void* node);
int escape_func_091(EscapeAnalyzer* analyzer, void* node);
int escape_func_092(EscapeAnalyzer* analyzer, void* node);
int escape_func_093(EscapeAnalyzer* analyzer, void* node);
int escape_func_094(EscapeAnalyzer* analyzer, void* node);
int escape_func_095(EscapeAnalyzer* analyzer, void* node);
int escape_func_096(EscapeAnalyzer* analyzer, void* node);
int escape_func_097(EscapeAnalyzer* analyzer, void* node);
int escape_func_098(EscapeAnalyzer* analyzer, void* node);
int escape_func_099(EscapeAnalyzer* analyzer, void* node);
EscapeAnalyzer* escape_analyzer_create();
void escape_analyzer_destroy(EscapeAnalyzer* analyzer);
int escape_analyzer_init(EscapeAnalyzer* analyzer);
int escape_analyzer_analyze(EscapeAnalyzer* analyzer, ASTNode* root);
int escape_analyzer_analyze_ir(EscapeAnalyzer* analyzer, IRModule* module);
int escape_analyzer_analyze_file(EscapeAnalyzer* analyzer, const char* filename);
int escape_analyzer_analyze_allocation(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_analyze_pointer(EscapeAnalyzer* analyzer, void* pointer);
int escape_analyzer_compute_points_to(EscapeAnalyzer* analyzer, void* pointer);
int escape_analyzer_compute_escape_state(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_no_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_local_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_argument_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_return_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_global_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_thread_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_is_heap_escape(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_can_stack_allocate(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_can_elide_allocation(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_can_merge_allocations(EscapeAnalyzer* analyzer, void* a1, void* a2);
int escape_analyzer_can_reuse_allocation(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_stack_allocate(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_elide_allocation(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_merge_allocations(EscapeAnalyzer* analyzer, void* a1, void* a2);
int escape_analyzer_reuse_allocation(EscapeAnalyzer* analyzer, void* allocation);
int escape_analyzer_build_pointer_graph(EscapeAnalyzer* analyzer, void* func);
int escape_analyzer_build_call_graph(EscapeAnalyzer* analyzer, void* module);
int escape_analyzer_run_worklist(EscapeAnalyzer* analyzer);
int escape_analyzer_iterate(EscapeAnalyzer* analyzer);
int escape_analyzer_verify(EscapeAnalyzer* analyzer);
int escape_analyzer_report(EscapeAnalyzer* analyzer);
int escape_analyzer_stats(EscapeAnalyzer* analyzer);

#endif /* AURORA_ESCAPE_H */