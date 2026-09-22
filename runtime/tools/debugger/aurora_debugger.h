/*
 * Aurora 工具链 - 调试器
 * 支持 100+ 调试命令
 */

#ifndef AURORA_DEBUGGER_H
#define AURORA_DEBUGGER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 调试器状态 */
typedef enum {
    DBG_STATE_IDLE,
    DBG_STATE_RUNNING,
    DBG_STATE_PAUSED,
    DBG_STATE_STEPPING,
    DBG_STATE_FINISHED,
    DBG_STATE_ERROR
} DebuggerState;

/* 断点 */
typedef struct Breakpoint {
    int id;
    char* file;
    int line;
    int column;
    void* address;
    int enabled;
    int hit_count;
    char* condition;
    char* command;
    struct Breakpoint* next;
} Breakpoint;

/* 调用栈帧 */
typedef struct StackFrame {
    int index;
    char* function;
    char* file;
    int line;
    int column;
    void* address;
    void* locals;
    int local_count;
    void* args;
    int arg_count;
    struct StackFrame* caller;
} StackFrame;

/* 变量 */
typedef struct Variable {
    char* name;
    char* type;
    char* value;
    void* address;
    int size;
    int is_reference;
    int is_const;
    int scope;
    struct Variable* children;
    int child_count;
} Variable;

/* 调试器 */
typedef struct {
    DebuggerState state;
    void* process;
    int pid;
    Breakpoint* breakpoints;
    int breakpoint_count;
    StackFrame* current_frame;
    int frame_count;
    Variable* variables;
    int variable_count;
    char* current_file;
    int current_line;
    int current_column;
    void* current_address;
    int step_over;
    int step_in;
    int step_out;
    int continue_running;
    int verbose;
    int log_level;
    FILE* log_file;
    char* history[1000];
    int history_count;
    int history_index;
} Debugger;

/* 函数声明 */
int dbg_cmd_000(Debugger* dbg, const char* args);
int dbg_cmd_001(Debugger* dbg, const char* args);
int dbg_cmd_002(Debugger* dbg, const char* args);
int dbg_cmd_003(Debugger* dbg, const char* args);
int dbg_cmd_004(Debugger* dbg, const char* args);
int dbg_cmd_005(Debugger* dbg, const char* args);
int dbg_cmd_006(Debugger* dbg, const char* args);
int dbg_cmd_007(Debugger* dbg, const char* args);
int dbg_cmd_008(Debugger* dbg, const char* args);
int dbg_cmd_009(Debugger* dbg, const char* args);
int dbg_cmd_010(Debugger* dbg, const char* args);
int dbg_cmd_011(Debugger* dbg, const char* args);
int dbg_cmd_012(Debugger* dbg, const char* args);
int dbg_cmd_013(Debugger* dbg, const char* args);
int dbg_cmd_014(Debugger* dbg, const char* args);
int dbg_cmd_015(Debugger* dbg, const char* args);
int dbg_cmd_016(Debugger* dbg, const char* args);
int dbg_cmd_017(Debugger* dbg, const char* args);
int dbg_cmd_018(Debugger* dbg, const char* args);
int dbg_cmd_019(Debugger* dbg, const char* args);
int dbg_cmd_020(Debugger* dbg, const char* args);
int dbg_cmd_021(Debugger* dbg, const char* args);
int dbg_cmd_022(Debugger* dbg, const char* args);
int dbg_cmd_023(Debugger* dbg, const char* args);
int dbg_cmd_024(Debugger* dbg, const char* args);
int dbg_cmd_025(Debugger* dbg, const char* args);
int dbg_cmd_026(Debugger* dbg, const char* args);
int dbg_cmd_027(Debugger* dbg, const char* args);
int dbg_cmd_028(Debugger* dbg, const char* args);
int dbg_cmd_029(Debugger* dbg, const char* args);
int dbg_cmd_030(Debugger* dbg, const char* args);
int dbg_cmd_031(Debugger* dbg, const char* args);
int dbg_cmd_032(Debugger* dbg, const char* args);
int dbg_cmd_033(Debugger* dbg, const char* args);
int dbg_cmd_034(Debugger* dbg, const char* args);
int dbg_cmd_035(Debugger* dbg, const char* args);
int dbg_cmd_036(Debugger* dbg, const char* args);
int dbg_cmd_037(Debugger* dbg, const char* args);
int dbg_cmd_038(Debugger* dbg, const char* args);
int dbg_cmd_039(Debugger* dbg, const char* args);
int dbg_cmd_040(Debugger* dbg, const char* args);
int dbg_cmd_041(Debugger* dbg, const char* args);
int dbg_cmd_042(Debugger* dbg, const char* args);
int dbg_cmd_043(Debugger* dbg, const char* args);
int dbg_cmd_044(Debugger* dbg, const char* args);
int dbg_cmd_045(Debugger* dbg, const char* args);
int dbg_cmd_046(Debugger* dbg, const char* args);
int dbg_cmd_047(Debugger* dbg, const char* args);
int dbg_cmd_048(Debugger* dbg, const char* args);
int dbg_cmd_049(Debugger* dbg, const char* args);
int dbg_cmd_050(Debugger* dbg, const char* args);
int dbg_cmd_051(Debugger* dbg, const char* args);
int dbg_cmd_052(Debugger* dbg, const char* args);
int dbg_cmd_053(Debugger* dbg, const char* args);
int dbg_cmd_054(Debugger* dbg, const char* args);
int dbg_cmd_055(Debugger* dbg, const char* args);
int dbg_cmd_056(Debugger* dbg, const char* args);
int dbg_cmd_057(Debugger* dbg, const char* args);
int dbg_cmd_058(Debugger* dbg, const char* args);
int dbg_cmd_059(Debugger* dbg, const char* args);
int dbg_cmd_060(Debugger* dbg, const char* args);
int dbg_cmd_061(Debugger* dbg, const char* args);
int dbg_cmd_062(Debugger* dbg, const char* args);
int dbg_cmd_063(Debugger* dbg, const char* args);
int dbg_cmd_064(Debugger* dbg, const char* args);
int dbg_cmd_065(Debugger* dbg, const char* args);
int dbg_cmd_066(Debugger* dbg, const char* args);
int dbg_cmd_067(Debugger* dbg, const char* args);
int dbg_cmd_068(Debugger* dbg, const char* args);
int dbg_cmd_069(Debugger* dbg, const char* args);
int dbg_cmd_070(Debugger* dbg, const char* args);
int dbg_cmd_071(Debugger* dbg, const char* args);
int dbg_cmd_072(Debugger* dbg, const char* args);
int dbg_cmd_073(Debugger* dbg, const char* args);
int dbg_cmd_074(Debugger* dbg, const char* args);
int dbg_cmd_075(Debugger* dbg, const char* args);
int dbg_cmd_076(Debugger* dbg, const char* args);
int dbg_cmd_077(Debugger* dbg, const char* args);
int dbg_cmd_078(Debugger* dbg, const char* args);
int dbg_cmd_079(Debugger* dbg, const char* args);
int dbg_cmd_080(Debugger* dbg, const char* args);
int dbg_cmd_081(Debugger* dbg, const char* args);
int dbg_cmd_082(Debugger* dbg, const char* args);
int dbg_cmd_083(Debugger* dbg, const char* args);
int dbg_cmd_084(Debugger* dbg, const char* args);
int dbg_cmd_085(Debugger* dbg, const char* args);
int dbg_cmd_086(Debugger* dbg, const char* args);
int dbg_cmd_087(Debugger* dbg, const char* args);
int dbg_cmd_088(Debugger* dbg, const char* args);
int dbg_cmd_089(Debugger* dbg, const char* args);
int dbg_cmd_090(Debugger* dbg, const char* args);
int dbg_cmd_091(Debugger* dbg, const char* args);
int dbg_cmd_092(Debugger* dbg, const char* args);
int dbg_cmd_093(Debugger* dbg, const char* args);
int dbg_cmd_094(Debugger* dbg, const char* args);
int dbg_cmd_095(Debugger* dbg, const char* args);
int dbg_cmd_096(Debugger* dbg, const char* args);
int dbg_cmd_097(Debugger* dbg, const char* args);
int dbg_cmd_098(Debugger* dbg, const char* args);
int dbg_cmd_099(Debugger* dbg, const char* args);
Debugger* debugger_create();
void debugger_destroy(Debugger* dbg);
int debugger_start(Debugger* dbg, const char* program, char** args);
int debugger_attach(Debugger* dbg, int pid);
int debugger_detach(Debugger* dbg);
int debugger_continue(Debugger* dbg);
int debugger_pause(Debugger* dbg);
int debugger_step_over(Debugger* dbg);
int debugger_step_in(Debugger* dbg);
int debugger_step_out(Debugger* dbg);
int debugger_set_breakpoint(Debugger* dbg, const char* file, int line);
int debugger_remove_breakpoint(Debugger* dbg, int id);
int debugger_enable_breakpoint(Debugger* dbg, int id);
int debugger_disable_breakpoint(Debugger* dbg, int id);
StackFrame* debugger_get_stack(Debugger* dbg);
Variable* debugger_get_locals(Debugger* dbg);
Variable* debugger_get_variable(Debugger* dbg, const char* name);
int debugger_set_variable(Debugger* dbg, const char* name, const char* value);
int debugger_evaluate(Debugger* dbg, const char* expression, char* result, int size);
int debugger_disassemble(Debugger* dbg, void* start, void* end, char* output, int size);
int debugger_read_memory(Debugger* dbg, void* address, void* buffer, int size);
int debugger_write_memory(Debugger* dbg, void* address, void* buffer, int size);
int debugger_read_registers(Debugger* dbg, void* regs);
int debugger_write_registers(Debugger* dbg, void* regs);

#endif /* AURORA_DEBUGGER_H */