/*
 * Aurora 运行时 - 分代垃圾回收器
 * 支持 100+ GC 操作函数
 */

#ifndef AURORA_GC_H
#define AURORA_GC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "aurora_objects.h"

/* GC 代 */
typedef enum {
    GC_GEN_YOUNG,
    GC_GEN_OLD,
    GC_GEN_PERMANENT,
    GC_GEN_COUNT
} GCGeneration;

/* GC 颜色 */
typedef enum {
    GC_COLOR_WHITE,
    GC_COLOR_GRAY,
    GC_COLOR_BLACK,
    GC_COLOR_PURPLE
} GCColor;

/* GC 堆 */
typedef struct {
    void* heap_start;
    void* heap_end;
    size_t heap_size;
    size_t used_size;
    size_t free_size;
    ObjectHeader* free_list;
    ObjectHeader* object_list;
    ObjectHeader* gray_stack;
    int gray_count;
    int gray_capacity;
    int gc_running;
    int gc_threshold;
    int gc_heap_growth;
    int gc_minor_count;
    int gc_major_count;
    int gc_total_objects;
    int gc_freed_objects;
    double gc_minor_time;
    double gc_major_time;
    int gc_concurrent;
    int gc_incremental;
    int gc_barrier;
    void* gc_thread;
    void* gc_mutex;
    void* gc_cond;
} GCHeap;

/* 函数声明 */
void gc_func_000(GCHeap* heap);
void gc_func_001(GCHeap* heap);
void gc_func_002(GCHeap* heap);
void gc_func_003(GCHeap* heap);
void gc_func_004(GCHeap* heap);
void gc_func_005(GCHeap* heap);
void gc_func_006(GCHeap* heap);
void gc_func_007(GCHeap* heap);
void gc_func_008(GCHeap* heap);
void gc_func_009(GCHeap* heap);
void gc_func_010(GCHeap* heap);
void gc_func_011(GCHeap* heap);
void gc_func_012(GCHeap* heap);
void gc_func_013(GCHeap* heap);
void gc_func_014(GCHeap* heap);
void gc_func_015(GCHeap* heap);
void gc_func_016(GCHeap* heap);
void gc_func_017(GCHeap* heap);
void gc_func_018(GCHeap* heap);
void gc_func_019(GCHeap* heap);
void gc_func_020(GCHeap* heap);
void gc_func_021(GCHeap* heap);
void gc_func_022(GCHeap* heap);
void gc_func_023(GCHeap* heap);
void gc_func_024(GCHeap* heap);
void gc_func_025(GCHeap* heap);
void gc_func_026(GCHeap* heap);
void gc_func_027(GCHeap* heap);
void gc_func_028(GCHeap* heap);
void gc_func_029(GCHeap* heap);
void gc_func_030(GCHeap* heap);
void gc_func_031(GCHeap* heap);
void gc_func_032(GCHeap* heap);
void gc_func_033(GCHeap* heap);
void gc_func_034(GCHeap* heap);
void gc_func_035(GCHeap* heap);
void gc_func_036(GCHeap* heap);
void gc_func_037(GCHeap* heap);
void gc_func_038(GCHeap* heap);
void gc_func_039(GCHeap* heap);
void gc_func_040(GCHeap* heap);
void gc_func_041(GCHeap* heap);
void gc_func_042(GCHeap* heap);
void gc_func_043(GCHeap* heap);
void gc_func_044(GCHeap* heap);
void gc_func_045(GCHeap* heap);
void gc_func_046(GCHeap* heap);
void gc_func_047(GCHeap* heap);
void gc_func_048(GCHeap* heap);
void gc_func_049(GCHeap* heap);
void gc_func_050(GCHeap* heap);
void gc_func_051(GCHeap* heap);
void gc_func_052(GCHeap* heap);
void gc_func_053(GCHeap* heap);
void gc_func_054(GCHeap* heap);
void gc_func_055(GCHeap* heap);
void gc_func_056(GCHeap* heap);
void gc_func_057(GCHeap* heap);
void gc_func_058(GCHeap* heap);
void gc_func_059(GCHeap* heap);
void gc_func_060(GCHeap* heap);
void gc_func_061(GCHeap* heap);
void gc_func_062(GCHeap* heap);
void gc_func_063(GCHeap* heap);
void gc_func_064(GCHeap* heap);
void gc_func_065(GCHeap* heap);
void gc_func_066(GCHeap* heap);
void gc_func_067(GCHeap* heap);
void gc_func_068(GCHeap* heap);
void gc_func_069(GCHeap* heap);
void gc_func_070(GCHeap* heap);
void gc_func_071(GCHeap* heap);
void gc_func_072(GCHeap* heap);
void gc_func_073(GCHeap* heap);
void gc_func_074(GCHeap* heap);
void gc_func_075(GCHeap* heap);
void gc_func_076(GCHeap* heap);
void gc_func_077(GCHeap* heap);
void gc_func_078(GCHeap* heap);
void gc_func_079(GCHeap* heap);
void gc_func_080(GCHeap* heap);
void gc_func_081(GCHeap* heap);
void gc_func_082(GCHeap* heap);
void gc_func_083(GCHeap* heap);
void gc_func_084(GCHeap* heap);
void gc_func_085(GCHeap* heap);
void gc_func_086(GCHeap* heap);
void gc_func_087(GCHeap* heap);
void gc_func_088(GCHeap* heap);
void gc_func_089(GCHeap* heap);
void gc_func_090(GCHeap* heap);
void gc_func_091(GCHeap* heap);
void gc_func_092(GCHeap* heap);
void gc_func_093(GCHeap* heap);
void gc_func_094(GCHeap* heap);
void gc_func_095(GCHeap* heap);
void gc_func_096(GCHeap* heap);
void gc_func_097(GCHeap* heap);
void gc_func_098(GCHeap* heap);
void gc_func_099(GCHeap* heap);
GCHeap* gc_heap_create(size_t initial_size);
void gc_heap_destroy(GCHeap* heap);
void* gc_alloc(GCHeap* heap, size_t size);
void gc_free(GCHeap* heap, void* ptr);
void gc_collect(GCHeap* heap);
void gc_collect_minor(GCHeap* heap);
void gc_collect_major(GCHeap* heap);
void gc_mark(GCHeap* heap, Object* obj);
void gc_sweep(GCHeap* heap);
void gc_compact(GCHeap* heap);
void gc_promote(GCHeap* heap, Object* obj);
void gc_write_barrier(GCHeap* heap, Object* obj, void* field, Object* new_val);
void gc_add_root(GCHeap* heap, Object** root);
void gc_remove_root(GCHeap* heap, Object** root);

#endif /* AURORA_GC_H */