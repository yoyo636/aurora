/*
 * Aurora 运行时 - 并发运行时
 * 支持 100+ 并发操作函数
 */

#ifndef AURORA_CONCURRENCY_H
#define AURORA_CONCURRENCY_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 线程状态 */
typedef enum {
    THREAD_STATE_NEW,
    THREAD_STATE_RUNNABLE,
    THREAD_STATE_RUNNING,
    THREAD_STATE_BLOCKED,
    THREAD_STATE_WAITING,
    THREAD_STATE_TIMED_WAITING,
    THREAD_STATE_TERMINATED,
    THREAD_STATE_SUSPENDED
} ThreadState;

/* 线程优先级 */
typedef enum {
    THREAD_PRIORITY_IDLE,
    THREAD_PRIORITY_LOWEST,
    THREAD_PRIORITY_BELOW_NORMAL,
    THREAD_PRIORITY_NORMAL,
    THREAD_PRIORITY_ABOVE_NORMAL,
    THREAD_PRIORITY_HIGHEST,
    THREAD_PRIORITY_TIME_CRITICAL
} ThreadPriority;

/* 线程 */
typedef struct Thread {
    int id;
    char* name;
    ThreadState state;
    ThreadPriority priority;
    void* stack;
    size_t stack_size;
    void* context;
    void* entry_point;
    void* arg;
    void* result;
    int exit_code;
    int is_daemon;
    int is_detached;
    int cpu_affinity;
    int cpu_count;
    double cpu_time;
    double user_time;
    double system_time;
    int context_switches;
    int page_faults;
    void* local_storage;
    int local_storage_count;
    void* wait_queue;
    int wait_count;
    void* mutex_held;
    int mutex_count;
    struct Thread* next;
    struct Thread* prev;
} Thread;

/* 互斥锁 */
typedef struct Mutex {
    int id;
    char* name;
    int locked;
    Thread* owner;
    int recursive;
    int recursion_count;
    int spin_count;
    int priority_ceiling;
    int protocol;
    int type;
    int robust;
    void* wait_queue;
    int wait_count;
    void* native_handle;
    int contention_count;
    int max_contention;
    double total_wait_time;
    double max_wait_time;
} Mutex;

/* 条件变量 */
typedef struct CondVar {
    int id;
    char* name;
    Mutex* mutex;
    void* wait_queue;
    int wait_count;
    int signal_count;
    int broadcast_count;
    void* native_handle;
    int clock;
    int pshared;
} CondVar;

/* 信号量 */
typedef struct Semaphore {
    int id;
    char* name;
    int count;
    int max_count;
    int initial_count;
    void* wait_queue;
    int wait_count;
    void* native_handle;
    int pshared;
    int acquire_count;
    int release_count;
    int try_acquire_count;
    int try_acquire_success;
    double total_wait_time;
} Semaphore;

/* 屏障 */
typedef struct Barrier {
    int id;
    char* name;
    int count;
    int threshold;
    int generation;
    void* wait_queue;
    int wait_count;
    void* native_handle;
    int pshared;
    int arrive_count;
    int wait_call_count;
} Barrier;

/* 读写锁 */
typedef struct RWLock {
    int id;
    char* name;
    int read_count;
    int write_count;
    int writer_waiting;
    int reader_waiting;
    Thread* writer;
    void* native_handle;
    int pshared;
    int kind;
    int read_lock_count;
    int write_lock_count;
    int read_unlock_count;
    int write_unlock_count;
    double total_read_wait;
    double total_write_wait;
} RWLock;

/* 自旋锁 */
typedef struct SpinLock {
    int id;
    char* name;
    volatile int locked;
    Thread* owner;
    int spin_count;
    int yield_count;
    int contention_count;
    int max_spin;
} SpinLock;

/* 原子变量 */
typedef struct Atomic {
    int id;
    char* name;
    volatile long long value;
    int memory_order;
    int is_lock_free;
    int exchange_count;
    int compare_exchange_count;
    int fetch_add_count;
    int fetch_sub_count;
    int fetch_and_count;
    int fetch_or_count;
    int fetch_xor_count;
} Atomic;

/* 通道 */
typedef struct Channel {
    int id;
    char* name;
    void* buffer;
    int capacity;
    int count;
    int head;
    int tail;
    int closed;
    Mutex* mutex;
    CondVar* not_empty;
    CondVar* not_full;
    int send_count;
    int receive_count;
    int try_send_count;
    int try_receive_count;
    int sender_count;
    int receiver_count;
    double total_send_wait;
    double total_receive_wait;
} Channel;

/* 协程 */
typedef struct Coroutine {
    int id;
    char* name;
    int state;
    void* stack;
    size_t stack_size;
    void* context;
    void* entry_point;
    void* arg;
    void* result;
    int yield_count;
    int resume_count;
    struct Coroutine* caller;
    struct Coroutine* callee;
    void* local_storage;
    int local_storage_count;
    double total_run_time;
    int context_switches;
} Coroutine;

/* 线程池 */
typedef struct ThreadPool {
    int id;
    char* name;
    Thread** threads;
    int thread_count;
    int core_count;
    int max_count;
    int active_count;
    int idle_count;
    void* task_queue;
    int task_count;
    int task_capacity;
    int completed_count;
    int failed_count;
    int rejected_count;
    int shutdown;
    int shutdown_now;
    int terminated;
    int keep_alive_time;
    int allow_core_thread_timeout;
    void* rejected_handler;
    void* thread_factory;
    Mutex* mutex;
    CondVar* not_empty;
    CondVar* termination;
    double total_task_time;
    double max_task_time;
    double min_task_time;
} ThreadPool;

/* 任务 */
typedef struct Task {
    int id;
    char* name;
    void* entry_point;
    void* arg;
    void* result;
    int state;
    int priority;
    int cancelable;
    int cancelled;
    int completed;
    int failed;
    int exception;
    double submit_time;
    double start_time;
    double end_time;
    double duration;
    Thread* executor;
    ThreadPool* pool;
    void* callbacks;
    int callback_count;
    void* dependencies;
    int dependency_count;
    void* dependents;
    int dependent_count;
    struct Task* next;
    struct Task* prev;
} Task;

/* Future/Promise */
typedef struct Future {
    int id;
    char* name;
    int state;
    void* result;
    int exception;
    void* error;
    Mutex* mutex;
    CondVar* completed;
    void* callbacks;
    int callback_count;
    double create_time;
    double complete_time;
    double duration;
    int await_count;
    int poll_count;
} Future;

/* 并发运行时 */
typedef struct ConcurrencyRuntime {
    int initialized;
    int thread_count;
    int core_count;
    int max_threads;
    Thread** threads;
    int thread_capacity;
    ThreadPool** pools;
    int pool_count;
    int pool_capacity;
    Coroutine** coroutines;
    int coroutine_count;
    int coroutine_capacity;
    Mutex** mutexes;
    int mutex_count;
    int mutex_capacity;
    CondVar** condvars;
    int condvar_count;
    int condvar_capacity;
    Semaphore** semaphores;
    int semaphore_count;
    int semaphore_capacity;
    Barrier** barriers;
    int barrier_count;
    int barrier_capacity;
    RWLock** rwlocks;
    int rwlock_count;
    int rwlock_capacity;
    SpinLock** spinlocks;
    int spinlock_count;
    int spinlock_capacity;
    Atomic** atomics;
    int atomic_count;
    int atomic_capacity;
    Channel** channels;
    int channel_count;
    int channel_capacity;
    Task** tasks;
    int task_count;
    int task_capacity;
    Future** futures;
    int future_count;
    int future_capacity;
    int next_id;
    Mutex* global_mutex;
    int scheduler_policy;
    int load_balancing;
    int work_stealing;
    int thread_affinity;
    int cpu_pinning;
    int numa_aware;
    int huge_pages;
    int stack_size;
    int guard_pages;
    int signal_handling;
    int exception_handling;
    int debug_mode;
    int profile_mode;
    int trace_mode;
    int log_level;
    FILE* log_file;
    double start_time;
    double total_cpu_time;
    double total_user_time;
    double total_system_time;
    long long total_context_switches;
    long long total_page_faults;
    long long total_memory_allocated;
    long long total_memory_freed;
    long long current_memory_usage;
    long long peak_memory_usage;
} ConcurrencyRuntime;

/* 函数声明 */
int conc_func_000(ConcurrencyRuntime* rt, void* arg);
int conc_func_001(ConcurrencyRuntime* rt, void* arg);
int conc_func_002(ConcurrencyRuntime* rt, void* arg);
int conc_func_003(ConcurrencyRuntime* rt, void* arg);
int conc_func_004(ConcurrencyRuntime* rt, void* arg);
int conc_func_005(ConcurrencyRuntime* rt, void* arg);
int conc_func_006(ConcurrencyRuntime* rt, void* arg);
int conc_func_007(ConcurrencyRuntime* rt, void* arg);
int conc_func_008(ConcurrencyRuntime* rt, void* arg);
int conc_func_009(ConcurrencyRuntime* rt, void* arg);
int conc_func_010(ConcurrencyRuntime* rt, void* arg);
int conc_func_011(ConcurrencyRuntime* rt, void* arg);
int conc_func_012(ConcurrencyRuntime* rt, void* arg);
int conc_func_013(ConcurrencyRuntime* rt, void* arg);
int conc_func_014(ConcurrencyRuntime* rt, void* arg);
int conc_func_015(ConcurrencyRuntime* rt, void* arg);
int conc_func_016(ConcurrencyRuntime* rt, void* arg);
int conc_func_017(ConcurrencyRuntime* rt, void* arg);
int conc_func_018(ConcurrencyRuntime* rt, void* arg);
int conc_func_019(ConcurrencyRuntime* rt, void* arg);
int conc_func_020(ConcurrencyRuntime* rt, void* arg);
int conc_func_021(ConcurrencyRuntime* rt, void* arg);
int conc_func_022(ConcurrencyRuntime* rt, void* arg);
int conc_func_023(ConcurrencyRuntime* rt, void* arg);
int conc_func_024(ConcurrencyRuntime* rt, void* arg);
int conc_func_025(ConcurrencyRuntime* rt, void* arg);
int conc_func_026(ConcurrencyRuntime* rt, void* arg);
int conc_func_027(ConcurrencyRuntime* rt, void* arg);
int conc_func_028(ConcurrencyRuntime* rt, void* arg);
int conc_func_029(ConcurrencyRuntime* rt, void* arg);
int conc_func_030(ConcurrencyRuntime* rt, void* arg);
int conc_func_031(ConcurrencyRuntime* rt, void* arg);
int conc_func_032(ConcurrencyRuntime* rt, void* arg);
int conc_func_033(ConcurrencyRuntime* rt, void* arg);
int conc_func_034(ConcurrencyRuntime* rt, void* arg);
int conc_func_035(ConcurrencyRuntime* rt, void* arg);
int conc_func_036(ConcurrencyRuntime* rt, void* arg);
int conc_func_037(ConcurrencyRuntime* rt, void* arg);
int conc_func_038(ConcurrencyRuntime* rt, void* arg);
int conc_func_039(ConcurrencyRuntime* rt, void* arg);
int conc_func_040(ConcurrencyRuntime* rt, void* arg);
int conc_func_041(ConcurrencyRuntime* rt, void* arg);
int conc_func_042(ConcurrencyRuntime* rt, void* arg);
int conc_func_043(ConcurrencyRuntime* rt, void* arg);
int conc_func_044(ConcurrencyRuntime* rt, void* arg);
int conc_func_045(ConcurrencyRuntime* rt, void* arg);
int conc_func_046(ConcurrencyRuntime* rt, void* arg);
int conc_func_047(ConcurrencyRuntime* rt, void* arg);
int conc_func_048(ConcurrencyRuntime* rt, void* arg);
int conc_func_049(ConcurrencyRuntime* rt, void* arg);
int conc_func_050(ConcurrencyRuntime* rt, void* arg);
int conc_func_051(ConcurrencyRuntime* rt, void* arg);
int conc_func_052(ConcurrencyRuntime* rt, void* arg);
int conc_func_053(ConcurrencyRuntime* rt, void* arg);
int conc_func_054(ConcurrencyRuntime* rt, void* arg);
int conc_func_055(ConcurrencyRuntime* rt, void* arg);
int conc_func_056(ConcurrencyRuntime* rt, void* arg);
int conc_func_057(ConcurrencyRuntime* rt, void* arg);
int conc_func_058(ConcurrencyRuntime* rt, void* arg);
int conc_func_059(ConcurrencyRuntime* rt, void* arg);
int conc_func_060(ConcurrencyRuntime* rt, void* arg);
int conc_func_061(ConcurrencyRuntime* rt, void* arg);
int conc_func_062(ConcurrencyRuntime* rt, void* arg);
int conc_func_063(ConcurrencyRuntime* rt, void* arg);
int conc_func_064(ConcurrencyRuntime* rt, void* arg);
int conc_func_065(ConcurrencyRuntime* rt, void* arg);
int conc_func_066(ConcurrencyRuntime* rt, void* arg);
int conc_func_067(ConcurrencyRuntime* rt, void* arg);
int conc_func_068(ConcurrencyRuntime* rt, void* arg);
int conc_func_069(ConcurrencyRuntime* rt, void* arg);
int conc_func_070(ConcurrencyRuntime* rt, void* arg);
int conc_func_071(ConcurrencyRuntime* rt, void* arg);
int conc_func_072(ConcurrencyRuntime* rt, void* arg);
int conc_func_073(ConcurrencyRuntime* rt, void* arg);
int conc_func_074(ConcurrencyRuntime* rt, void* arg);
int conc_func_075(ConcurrencyRuntime* rt, void* arg);
int conc_func_076(ConcurrencyRuntime* rt, void* arg);
int conc_func_077(ConcurrencyRuntime* rt, void* arg);
int conc_func_078(ConcurrencyRuntime* rt, void* arg);
int conc_func_079(ConcurrencyRuntime* rt, void* arg);
int conc_func_080(ConcurrencyRuntime* rt, void* arg);
int conc_func_081(ConcurrencyRuntime* rt, void* arg);
int conc_func_082(ConcurrencyRuntime* rt, void* arg);
int conc_func_083(ConcurrencyRuntime* rt, void* arg);
int conc_func_084(ConcurrencyRuntime* rt, void* arg);
int conc_func_085(ConcurrencyRuntime* rt, void* arg);
int conc_func_086(ConcurrencyRuntime* rt, void* arg);
int conc_func_087(ConcurrencyRuntime* rt, void* arg);
int conc_func_088(ConcurrencyRuntime* rt, void* arg);
int conc_func_089(ConcurrencyRuntime* rt, void* arg);
int conc_func_090(ConcurrencyRuntime* rt, void* arg);
int conc_func_091(ConcurrencyRuntime* rt, void* arg);
int conc_func_092(ConcurrencyRuntime* rt, void* arg);
int conc_func_093(ConcurrencyRuntime* rt, void* arg);
int conc_func_094(ConcurrencyRuntime* rt, void* arg);
int conc_func_095(ConcurrencyRuntime* rt, void* arg);
int conc_func_096(ConcurrencyRuntime* rt, void* arg);
int conc_func_097(ConcurrencyRuntime* rt, void* arg);
int conc_func_098(ConcurrencyRuntime* rt, void* arg);
int conc_func_099(ConcurrencyRuntime* rt, void* arg);
ConcurrencyRuntime* concurrency_runtime_create();
void concurrency_runtime_destroy(ConcurrencyRuntime* rt);
int concurrency_runtime_init(ConcurrencyRuntime* rt, int thread_count);
int concurrency_runtime_shutdown(ConcurrencyRuntime* rt);
int concurrency_runtime_await_termination(ConcurrencyRuntime* rt, int timeout);
Thread* thread_create(ConcurrencyRuntime* rt, const char* name, void* entry, void* arg);
int thread_start(Thread* thread);
int thread_join(Thread* thread, void** result);
int thread_detach(Thread* thread);
int thread_yield();
int thread_sleep(int milliseconds);
int thread_interrupt(Thread* thread);
int thread_cancel(Thread* thread);
int thread_suspend(Thread* thread);
int thread_resume(Thread* thread);
int thread_set_priority(Thread* thread, ThreadPriority priority);
int thread_set_affinity(Thread* thread, int cpu);
int thread_set_name(Thread* thread, const char* name);
Thread* thread_current();
int thread_id(Thread* thread);
const char* thread_name(Thread* thread);
ThreadState thread_state(Thread* thread);
int thread_is_alive(Thread* thread);
int thread_is_daemon(Thread* thread);
int thread_set_daemon(Thread* thread, int daemon);
Mutex* mutex_create(ConcurrencyRuntime* rt, const char* name, int recursive);
void mutex_destroy(Mutex* mutex);
int mutex_lock(Mutex* mutex);
int mutex_try_lock(Mutex* mutex);
int mutex_timed_lock(Mutex* mutex, int timeout);
int mutex_unlock(Mutex* mutex);
int mutex_is_locked(Mutex* mutex);
Thread* mutex_owner(Mutex* mutex);
CondVar* condvar_create(ConcurrencyRuntime* rt, const char* name, Mutex* mutex);
void condvar_destroy(CondVar* cond);
int condvar_wait(CondVar* cond);
int condvar_timed_wait(CondVar* cond, int timeout);
int condvar_signal(CondVar* cond);
int condvar_broadcast(CondVar* cond);
Semaphore* semaphore_create(ConcurrencyRuntime* rt, const char* name, int initial, int max);
void semaphore_destroy(Semaphore* sem);
int semaphore_acquire(Semaphore* sem);
int semaphore_try_acquire(Semaphore* sem);
int semaphore_timed_acquire(Semaphore* sem, int timeout);
int semaphore_release(Semaphore* sem);
int semaphore_release_n(Semaphore* sem, int n);
int semaphore_count(Semaphore* sem);
Barrier* barrier_create(ConcurrencyRuntime* rt, const char* name, int count);
void barrier_destroy(Barrier* barrier);
int barrier_wait(Barrier* barrier);
int barrier_arrive(Barrier* barrier);
int barrier_arrive_and_wait(Barrier* barrier);
int barrier_arrive_and_drop(Barrier* barrier);
int barrier_reset(Barrier* barrier);
int barrier_count(Barrier* barrier);
RWLock* rwlock_create(ConcurrencyRuntime* rt, const char* name);
void rwlock_destroy(RWLock* lock);
int rwlock_read_lock(RWLock* lock);
int rwlock_try_read_lock(RWLock* lock);
int rwlock_timed_read_lock(RWLock* lock, int timeout);
int rwlock_read_unlock(RWLock* lock);
int rwlock_write_lock(RWLock* lock);
int rwlock_try_write_lock(RWLock* lock);
int rwlock_timed_write_lock(RWLock* lock, int timeout);
int rwlock_write_unlock(RWLock* lock);
SpinLock* spinlock_create(ConcurrencyRuntime* rt, const char* name);
void spinlock_destroy(SpinLock* lock);
int spinlock_lock(SpinLock* lock);
int spinlock_try_lock(SpinLock* lock);
int spinlock_unlock(SpinLock* lock);
Atomic* atomic_create(ConcurrencyRuntime* rt, const char* name, long long initial);
void atomic_destroy(Atomic* atomic);
long long atomic_load(Atomic* atomic);
void atomic_store(Atomic* atomic, long long value);
long long atomic_exchange(Atomic* atomic, long long value);
int atomic_compare_exchange(Atomic* atomic, long long* expected, long long desired);
long long atomic_fetch_add(Atomic* atomic, long long value);
long long atomic_fetch_sub(Atomic* atomic, long long value);
long long atomic_fetch_and(Atomic* atomic, long long value);
long long atomic_fetch_or(Atomic* atomic, long long value);
long long atomic_fetch_xor(Atomic* atomic, long long value);
Channel* channel_create(ConcurrencyRuntime* rt, const char* name, int capacity);
void channel_destroy(Channel* channel);
int channel_send(Channel* channel, void* value);
int channel_try_send(Channel* channel, void* value);
int channel_timed_send(Channel* channel, void* value, int timeout);
void* channel_receive(Channel* channel);
void* channel_try_receive(Channel* channel);
void* channel_timed_receive(Channel* channel, int timeout);
int channel_close(Channel* channel);
int channel_is_closed(Channel* channel);
int channel_count(Channel* channel);
int channel_capacity(Channel* channel);
Coroutine* coroutine_create(ConcurrencyRuntime* rt, const char* name, void* entry, void* arg);
void coroutine_destroy(Coroutine* coro);
int coroutine_resume(Coroutine* coro);
int coroutine_yield(Coroutine* coro);
int coroutine_yield_value(Coroutine* coro, void* value);
void* coroutine_result(Coroutine* coro);
int coroutine_state(Coroutine* coro);
int coroutine_is_done(Coroutine* coro);
Coroutine* coroutine_current();
ThreadPool* threadpool_create(ConcurrencyRuntime* rt, const char* name, int core, int max);
void threadpool_destroy(ThreadPool* pool);
int threadpool_shutdown(ThreadPool* pool);
int threadpool_shutdown_now(ThreadPool* pool);
int threadpool_await_termination(ThreadPool* pool, int timeout);
int threadpool_is_shutdown(ThreadPool* pool);
int threadpool_is_terminated(ThreadPool* pool);
Task* threadpool_submit(ThreadPool* pool, const char* name, void* entry, void* arg);
int threadpool_execute(ThreadPool* pool, void* entry, void* arg);
int threadpool_active_count(ThreadPool* pool);
int threadpool_pool_size(ThreadPool* pool);
int threadpool_completed_count(ThreadPool* pool);
int threadpool_task_count(ThreadPool* pool);
Task* task_create(ConcurrencyRuntime* rt, const char* name, void* entry, void* arg);
void task_destroy(Task* task);
int task_start(Task* task);
int task_cancel(Task* task);
int task_is_cancelled(Task* task);
int task_is_done(Task* task);
void* task_result(Task* task);
int task_wait(Task* task);
int task_timed_wait(Task* task, int timeout);
int task_add_callback(Task* task, void* callback, void* arg);
int task_add_dependency(Task* task, Task* dependency);
Future* future_create(ConcurrencyRuntime* rt, const char* name);
void future_destroy(Future* future);
int future_complete(Future* future, void* result);
int future_complete_exception(Future* future, void* error);
int future_is_done(Future* future);
int future_is_cancelled(Future* future);
void* future_result(Future* future);
void* future_error(Future* future);
int future_await(Future* future);
int future_timed_await(Future* future, int timeout);
int future_poll(Future* future);
int future_add_callback(Future* future, void* callback, void* arg);
Future* future_then(Future* future, void* callback, void* arg);
Future* future_catch(Future* future, void* callback, void* arg);
Future* future_finally(Future* future, void* callback, void* arg);
Future* future_all(ConcurrencyRuntime* rt, Future** futures, int count);
Future* future_any(ConcurrencyRuntime* rt, Future** futures, int count);
Future* future_all_settled(ConcurrencyRuntime* rt, Future** futures, int count);
Future* future_race(ConcurrencyRuntime* rt, Future** futures, int count);

#endif /* AURORA_CONCURRENCY_H */