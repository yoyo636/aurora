/*
 * Aurora 编译器中端 - IR 实现
 */

#include "aurora_ir.h"

/* 创建 IR 指令 0 指令 */
IRInstruction* ir_create_000(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_000;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 1 指令 */
IRInstruction* ir_create_001(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_001;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 2 指令 */
IRInstruction* ir_create_002(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_002;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 3 指令 */
IRInstruction* ir_create_003(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_003;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 4 指令 */
IRInstruction* ir_create_004(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_004;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 5 指令 */
IRInstruction* ir_create_005(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_005;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 6 指令 */
IRInstruction* ir_create_006(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_006;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 7 指令 */
IRInstruction* ir_create_007(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_007;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 8 指令 */
IRInstruction* ir_create_008(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_008;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 9 指令 */
IRInstruction* ir_create_009(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_009;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 10 指令 */
IRInstruction* ir_create_010(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_010;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 11 指令 */
IRInstruction* ir_create_011(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_011;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 12 指令 */
IRInstruction* ir_create_012(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_012;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 13 指令 */
IRInstruction* ir_create_013(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_013;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 14 指令 */
IRInstruction* ir_create_014(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_014;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 15 指令 */
IRInstruction* ir_create_015(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_015;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 16 指令 */
IRInstruction* ir_create_016(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_016;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 17 指令 */
IRInstruction* ir_create_017(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_017;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 18 指令 */
IRInstruction* ir_create_018(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_018;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 19 指令 */
IRInstruction* ir_create_019(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_019;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 20 指令 */
IRInstruction* ir_create_020(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_020;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 21 指令 */
IRInstruction* ir_create_021(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_021;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 22 指令 */
IRInstruction* ir_create_022(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_022;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 23 指令 */
IRInstruction* ir_create_023(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_023;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 24 指令 */
IRInstruction* ir_create_024(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_024;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 25 指令 */
IRInstruction* ir_create_025(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_025;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 26 指令 */
IRInstruction* ir_create_026(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_026;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 27 指令 */
IRInstruction* ir_create_027(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_027;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 28 指令 */
IRInstruction* ir_create_028(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_028;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 29 指令 */
IRInstruction* ir_create_029(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_029;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 30 指令 */
IRInstruction* ir_create_030(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_030;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 31 指令 */
IRInstruction* ir_create_031(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_031;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 32 指令 */
IRInstruction* ir_create_032(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_032;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 33 指令 */
IRInstruction* ir_create_033(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_033;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 34 指令 */
IRInstruction* ir_create_034(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_034;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 35 指令 */
IRInstruction* ir_create_035(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_035;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 36 指令 */
IRInstruction* ir_create_036(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_036;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 37 指令 */
IRInstruction* ir_create_037(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_037;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 38 指令 */
IRInstruction* ir_create_038(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_038;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 39 指令 */
IRInstruction* ir_create_039(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_039;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 40 指令 */
IRInstruction* ir_create_040(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_040;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 41 指令 */
IRInstruction* ir_create_041(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_041;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 42 指令 */
IRInstruction* ir_create_042(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_042;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 43 指令 */
IRInstruction* ir_create_043(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_043;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 44 指令 */
IRInstruction* ir_create_044(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_044;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 45 指令 */
IRInstruction* ir_create_045(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_045;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 46 指令 */
IRInstruction* ir_create_046(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_046;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 47 指令 */
IRInstruction* ir_create_047(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_047;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 48 指令 */
IRInstruction* ir_create_048(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_048;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 49 指令 */
IRInstruction* ir_create_049(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_049;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 50 指令 */
IRInstruction* ir_create_050(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_050;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 51 指令 */
IRInstruction* ir_create_051(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_051;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 52 指令 */
IRInstruction* ir_create_052(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_052;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 53 指令 */
IRInstruction* ir_create_053(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_053;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 54 指令 */
IRInstruction* ir_create_054(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_054;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 55 指令 */
IRInstruction* ir_create_055(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_055;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 56 指令 */
IRInstruction* ir_create_056(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_056;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 57 指令 */
IRInstruction* ir_create_057(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_057;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 58 指令 */
IRInstruction* ir_create_058(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_058;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 59 指令 */
IRInstruction* ir_create_059(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_059;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 60 指令 */
IRInstruction* ir_create_060(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_060;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 61 指令 */
IRInstruction* ir_create_061(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_061;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 62 指令 */
IRInstruction* ir_create_062(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_062;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 63 指令 */
IRInstruction* ir_create_063(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_063;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 64 指令 */
IRInstruction* ir_create_064(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_064;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 65 指令 */
IRInstruction* ir_create_065(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_065;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 66 指令 */
IRInstruction* ir_create_066(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_066;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 67 指令 */
IRInstruction* ir_create_067(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_067;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 68 指令 */
IRInstruction* ir_create_068(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_068;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 69 指令 */
IRInstruction* ir_create_069(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_069;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 70 指令 */
IRInstruction* ir_create_070(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_070;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 71 指令 */
IRInstruction* ir_create_071(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_071;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 72 指令 */
IRInstruction* ir_create_072(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_072;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 73 指令 */
IRInstruction* ir_create_073(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_073;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 74 指令 */
IRInstruction* ir_create_074(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_074;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 75 指令 */
IRInstruction* ir_create_075(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_075;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 76 指令 */
IRInstruction* ir_create_076(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_076;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 77 指令 */
IRInstruction* ir_create_077(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_077;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 78 指令 */
IRInstruction* ir_create_078(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_078;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 79 指令 */
IRInstruction* ir_create_079(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_079;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 80 指令 */
IRInstruction* ir_create_080(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_080;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 81 指令 */
IRInstruction* ir_create_081(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_081;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 82 指令 */
IRInstruction* ir_create_082(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_082;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 83 指令 */
IRInstruction* ir_create_083(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_083;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 84 指令 */
IRInstruction* ir_create_084(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_084;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 85 指令 */
IRInstruction* ir_create_085(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_085;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 86 指令 */
IRInstruction* ir_create_086(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_086;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 87 指令 */
IRInstruction* ir_create_087(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_087;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 88 指令 */
IRInstruction* ir_create_088(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_088;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 89 指令 */
IRInstruction* ir_create_089(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_089;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 90 指令 */
IRInstruction* ir_create_090(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_090;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 91 指令 */
IRInstruction* ir_create_091(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_091;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 92 指令 */
IRInstruction* ir_create_092(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_092;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 93 指令 */
IRInstruction* ir_create_093(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_093;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 94 指令 */
IRInstruction* ir_create_094(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_094;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 95 指令 */
IRInstruction* ir_create_095(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_095;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 96 指令 */
IRInstruction* ir_create_096(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_096;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 97 指令 */
IRInstruction* ir_create_097(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_097;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 98 指令 */
IRInstruction* ir_create_098(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_098;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 99 指令 */
IRInstruction* ir_create_099(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_099;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 100 指令 */
IRInstruction* ir_create_100(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_100;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 101 指令 */
IRInstruction* ir_create_101(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_101;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 102 指令 */
IRInstruction* ir_create_102(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_102;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 103 指令 */
IRInstruction* ir_create_103(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_103;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 104 指令 */
IRInstruction* ir_create_104(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_104;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 105 指令 */
IRInstruction* ir_create_105(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_105;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 106 指令 */
IRInstruction* ir_create_106(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_106;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 107 指令 */
IRInstruction* ir_create_107(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_107;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 108 指令 */
IRInstruction* ir_create_108(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_108;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 109 指令 */
IRInstruction* ir_create_109(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_109;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 110 指令 */
IRInstruction* ir_create_110(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_110;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 111 指令 */
IRInstruction* ir_create_111(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_111;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 112 指令 */
IRInstruction* ir_create_112(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_112;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 113 指令 */
IRInstruction* ir_create_113(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_113;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 114 指令 */
IRInstruction* ir_create_114(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_114;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 115 指令 */
IRInstruction* ir_create_115(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_115;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 116 指令 */
IRInstruction* ir_create_116(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_116;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 117 指令 */
IRInstruction* ir_create_117(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_117;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 118 指令 */
IRInstruction* ir_create_118(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_118;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 119 指令 */
IRInstruction* ir_create_119(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_119;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 120 指令 */
IRInstruction* ir_create_120(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_120;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 121 指令 */
IRInstruction* ir_create_121(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_121;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 122 指令 */
IRInstruction* ir_create_122(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_122;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 123 指令 */
IRInstruction* ir_create_123(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_123;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 124 指令 */
IRInstruction* ir_create_124(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_124;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 125 指令 */
IRInstruction* ir_create_125(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_125;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 126 指令 */
IRInstruction* ir_create_126(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_126;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 127 指令 */
IRInstruction* ir_create_127(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_127;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 128 指令 */
IRInstruction* ir_create_128(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_128;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 129 指令 */
IRInstruction* ir_create_129(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_129;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 130 指令 */
IRInstruction* ir_create_130(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_130;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 131 指令 */
IRInstruction* ir_create_131(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_131;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 132 指令 */
IRInstruction* ir_create_132(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_132;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 133 指令 */
IRInstruction* ir_create_133(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_133;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 134 指令 */
IRInstruction* ir_create_134(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_134;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 135 指令 */
IRInstruction* ir_create_135(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_135;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 136 指令 */
IRInstruction* ir_create_136(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_136;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 137 指令 */
IRInstruction* ir_create_137(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_137;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 138 指令 */
IRInstruction* ir_create_138(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_138;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 139 指令 */
IRInstruction* ir_create_139(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_139;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 140 指令 */
IRInstruction* ir_create_140(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_140;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 141 指令 */
IRInstruction* ir_create_141(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_141;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 142 指令 */
IRInstruction* ir_create_142(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_142;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 143 指令 */
IRInstruction* ir_create_143(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_143;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 144 指令 */
IRInstruction* ir_create_144(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_144;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 145 指令 */
IRInstruction* ir_create_145(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_145;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 146 指令 */
IRInstruction* ir_create_146(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_146;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 147 指令 */
IRInstruction* ir_create_147(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_147;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 148 指令 */
IRInstruction* ir_create_148(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_148;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 149 指令 */
IRInstruction* ir_create_149(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_149;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 150 指令 */
IRInstruction* ir_create_150(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_150;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 151 指令 */
IRInstruction* ir_create_151(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_151;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 152 指令 */
IRInstruction* ir_create_152(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_152;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 153 指令 */
IRInstruction* ir_create_153(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_153;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 154 指令 */
IRInstruction* ir_create_154(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_154;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 155 指令 */
IRInstruction* ir_create_155(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_155;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 156 指令 */
IRInstruction* ir_create_156(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_156;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 157 指令 */
IRInstruction* ir_create_157(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_157;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 158 指令 */
IRInstruction* ir_create_158(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_158;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 159 指令 */
IRInstruction* ir_create_159(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_159;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 160 指令 */
IRInstruction* ir_create_160(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_160;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 161 指令 */
IRInstruction* ir_create_161(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_161;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 162 指令 */
IRInstruction* ir_create_162(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_162;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 163 指令 */
IRInstruction* ir_create_163(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_163;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 164 指令 */
IRInstruction* ir_create_164(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_164;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 165 指令 */
IRInstruction* ir_create_165(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_165;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 166 指令 */
IRInstruction* ir_create_166(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_166;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 167 指令 */
IRInstruction* ir_create_167(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_167;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 168 指令 */
IRInstruction* ir_create_168(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_168;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 169 指令 */
IRInstruction* ir_create_169(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_169;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 170 指令 */
IRInstruction* ir_create_170(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_170;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 171 指令 */
IRInstruction* ir_create_171(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_171;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 172 指令 */
IRInstruction* ir_create_172(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_172;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 173 指令 */
IRInstruction* ir_create_173(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_173;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 174 指令 */
IRInstruction* ir_create_174(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_174;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 175 指令 */
IRInstruction* ir_create_175(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_175;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 176 指令 */
IRInstruction* ir_create_176(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_176;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 177 指令 */
IRInstruction* ir_create_177(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_177;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 178 指令 */
IRInstruction* ir_create_178(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_178;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 179 指令 */
IRInstruction* ir_create_179(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_179;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 180 指令 */
IRInstruction* ir_create_180(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_180;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 181 指令 */
IRInstruction* ir_create_181(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_181;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 182 指令 */
IRInstruction* ir_create_182(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_182;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 183 指令 */
IRInstruction* ir_create_183(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_183;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 184 指令 */
IRInstruction* ir_create_184(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_184;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 185 指令 */
IRInstruction* ir_create_185(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_185;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 186 指令 */
IRInstruction* ir_create_186(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_186;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 187 指令 */
IRInstruction* ir_create_187(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_187;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 188 指令 */
IRInstruction* ir_create_188(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_188;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 189 指令 */
IRInstruction* ir_create_189(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_189;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 190 指令 */
IRInstruction* ir_create_190(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_190;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 191 指令 */
IRInstruction* ir_create_191(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_191;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 192 指令 */
IRInstruction* ir_create_192(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_192;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 193 指令 */
IRInstruction* ir_create_193(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_193;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 194 指令 */
IRInstruction* ir_create_194(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_194;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 195 指令 */
IRInstruction* ir_create_195(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_195;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 196 指令 */
IRInstruction* ir_create_196(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_196;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 197 指令 */
IRInstruction* ir_create_197(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_197;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 198 指令 */
IRInstruction* ir_create_198(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_198;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 199 指令 */
IRInstruction* ir_create_199(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_199;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 200 指令 */
IRInstruction* ir_create_200(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_200;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 201 指令 */
IRInstruction* ir_create_201(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_201;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 202 指令 */
IRInstruction* ir_create_202(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_202;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 203 指令 */
IRInstruction* ir_create_203(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_203;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 204 指令 */
IRInstruction* ir_create_204(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_204;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 205 指令 */
IRInstruction* ir_create_205(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_205;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 206 指令 */
IRInstruction* ir_create_206(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_206;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 207 指令 */
IRInstruction* ir_create_207(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_207;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 208 指令 */
IRInstruction* ir_create_208(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_208;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 209 指令 */
IRInstruction* ir_create_209(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_209;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 210 指令 */
IRInstruction* ir_create_210(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_210;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 211 指令 */
IRInstruction* ir_create_211(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_211;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 212 指令 */
IRInstruction* ir_create_212(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_212;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 213 指令 */
IRInstruction* ir_create_213(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_213;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 214 指令 */
IRInstruction* ir_create_214(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_214;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 215 指令 */
IRInstruction* ir_create_215(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_215;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 216 指令 */
IRInstruction* ir_create_216(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_216;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 217 指令 */
IRInstruction* ir_create_217(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_217;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 218 指令 */
IRInstruction* ir_create_218(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_218;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 219 指令 */
IRInstruction* ir_create_219(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_219;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 220 指令 */
IRInstruction* ir_create_220(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_220;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 221 指令 */
IRInstruction* ir_create_221(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_221;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 222 指令 */
IRInstruction* ir_create_222(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_222;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 223 指令 */
IRInstruction* ir_create_223(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_223;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 224 指令 */
IRInstruction* ir_create_224(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_224;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 225 指令 */
IRInstruction* ir_create_225(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_225;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 226 指令 */
IRInstruction* ir_create_226(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_226;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 227 指令 */
IRInstruction* ir_create_227(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_227;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 228 指令 */
IRInstruction* ir_create_228(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_228;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 229 指令 */
IRInstruction* ir_create_229(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_229;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 230 指令 */
IRInstruction* ir_create_230(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_230;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 231 指令 */
IRInstruction* ir_create_231(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_231;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 232 指令 */
IRInstruction* ir_create_232(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_232;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 233 指令 */
IRInstruction* ir_create_233(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_233;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 234 指令 */
IRInstruction* ir_create_234(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_234;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 235 指令 */
IRInstruction* ir_create_235(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_235;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 236 指令 */
IRInstruction* ir_create_236(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_236;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 237 指令 */
IRInstruction* ir_create_237(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_237;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 238 指令 */
IRInstruction* ir_create_238(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_238;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 239 指令 */
IRInstruction* ir_create_239(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_239;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 240 指令 */
IRInstruction* ir_create_240(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_240;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 241 指令 */
IRInstruction* ir_create_241(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_241;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 242 指令 */
IRInstruction* ir_create_242(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_242;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 243 指令 */
IRInstruction* ir_create_243(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_243;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 244 指令 */
IRInstruction* ir_create_244(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_244;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 245 指令 */
IRInstruction* ir_create_245(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_245;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 246 指令 */
IRInstruction* ir_create_246(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_246;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 247 指令 */
IRInstruction* ir_create_247(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_247;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 248 指令 */
IRInstruction* ir_create_248(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_248;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 249 指令 */
IRInstruction* ir_create_249(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_249;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 250 指令 */
IRInstruction* ir_create_250(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_250;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 251 指令 */
IRInstruction* ir_create_251(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_251;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 252 指令 */
IRInstruction* ir_create_252(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_252;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 253 指令 */
IRInstruction* ir_create_253(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_253;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 254 指令 */
IRInstruction* ir_create_254(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_254;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 255 指令 */
IRInstruction* ir_create_255(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_255;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 256 指令 */
IRInstruction* ir_create_256(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_256;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 257 指令 */
IRInstruction* ir_create_257(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_257;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 258 指令 */
IRInstruction* ir_create_258(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_258;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 259 指令 */
IRInstruction* ir_create_259(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_259;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 260 指令 */
IRInstruction* ir_create_260(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_260;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 261 指令 */
IRInstruction* ir_create_261(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_261;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 262 指令 */
IRInstruction* ir_create_262(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_262;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 263 指令 */
IRInstruction* ir_create_263(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_263;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 264 指令 */
IRInstruction* ir_create_264(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_264;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 265 指令 */
IRInstruction* ir_create_265(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_265;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 266 指令 */
IRInstruction* ir_create_266(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_266;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 267 指令 */
IRInstruction* ir_create_267(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_267;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 268 指令 */
IRInstruction* ir_create_268(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_268;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 269 指令 */
IRInstruction* ir_create_269(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_269;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 270 指令 */
IRInstruction* ir_create_270(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_270;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 271 指令 */
IRInstruction* ir_create_271(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_271;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 272 指令 */
IRInstruction* ir_create_272(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_272;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 273 指令 */
IRInstruction* ir_create_273(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_273;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 274 指令 */
IRInstruction* ir_create_274(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_274;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 275 指令 */
IRInstruction* ir_create_275(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_275;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 276 指令 */
IRInstruction* ir_create_276(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_276;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 277 指令 */
IRInstruction* ir_create_277(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_277;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 278 指令 */
IRInstruction* ir_create_278(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_278;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 279 指令 */
IRInstruction* ir_create_279(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_279;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 280 指令 */
IRInstruction* ir_create_280(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_280;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 281 指令 */
IRInstruction* ir_create_281(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_281;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 282 指令 */
IRInstruction* ir_create_282(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_282;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 283 指令 */
IRInstruction* ir_create_283(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_283;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 284 指令 */
IRInstruction* ir_create_284(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_284;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 285 指令 */
IRInstruction* ir_create_285(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_285;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 286 指令 */
IRInstruction* ir_create_286(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_286;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 287 指令 */
IRInstruction* ir_create_287(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_287;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 288 指令 */
IRInstruction* ir_create_288(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_288;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 289 指令 */
IRInstruction* ir_create_289(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_289;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 290 指令 */
IRInstruction* ir_create_290(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_290;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 291 指令 */
IRInstruction* ir_create_291(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_291;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 292 指令 */
IRInstruction* ir_create_292(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_292;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 293 指令 */
IRInstruction* ir_create_293(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_293;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 294 指令 */
IRInstruction* ir_create_294(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_294;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 295 指令 */
IRInstruction* ir_create_295(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_295;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 296 指令 */
IRInstruction* ir_create_296(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_296;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 297 指令 */
IRInstruction* ir_create_297(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_297;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 298 指令 */
IRInstruction* ir_create_298(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_298;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

/* 创建 IR 指令 299 指令 */
IRInstruction* ir_create_299(IRValue* result, IRValue** operands, int count) {
    IRInstruction* instr = malloc(sizeof(IRInstruction));
    instr->opcode = IR_OP_299;
    instr->result = result;
    instr->operands = operands;
    instr->operand_count = count;
    instr->parent = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    instr->extra = NULL;
    return instr;
}

IRModule* ir_module_create(const char* name) {
    IRModule* mod = malloc(sizeof(IRModule));
    mod->name = strdup(name);
    mod->functions = NULL;
    mod->function_count = 0;
    mod->function_capacity = 0;
    mod->globals = NULL;
    mod->global_count = 0;
    mod->types = NULL;
    mod->type_count = 0;
    mod->extra = NULL;
    return mod;
}
