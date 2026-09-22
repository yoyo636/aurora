/*
 * Aurora 编译器后端 - x86_64 代码生成器实现
 */

#include "aurora_x86_64.h"

/* 发射 x86_64 指令 0 */
X86Instr* x86_emit_000(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_000;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 1 */
X86Instr* x86_emit_001(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_001;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 2 */
X86Instr* x86_emit_002(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_002;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 3 */
X86Instr* x86_emit_003(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_003;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 4 */
X86Instr* x86_emit_004(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_004;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 5 */
X86Instr* x86_emit_005(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_005;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 6 */
X86Instr* x86_emit_006(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_006;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 7 */
X86Instr* x86_emit_007(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_007;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 8 */
X86Instr* x86_emit_008(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_008;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 9 */
X86Instr* x86_emit_009(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_009;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 10 */
X86Instr* x86_emit_010(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_010;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 11 */
X86Instr* x86_emit_011(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_011;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 12 */
X86Instr* x86_emit_012(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_012;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 13 */
X86Instr* x86_emit_013(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_013;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 14 */
X86Instr* x86_emit_014(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_014;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 15 */
X86Instr* x86_emit_015(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_015;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 16 */
X86Instr* x86_emit_016(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_016;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 17 */
X86Instr* x86_emit_017(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_017;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 18 */
X86Instr* x86_emit_018(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_018;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 19 */
X86Instr* x86_emit_019(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_019;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 20 */
X86Instr* x86_emit_020(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_020;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 21 */
X86Instr* x86_emit_021(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_021;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 22 */
X86Instr* x86_emit_022(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_022;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 23 */
X86Instr* x86_emit_023(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_023;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 24 */
X86Instr* x86_emit_024(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_024;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 25 */
X86Instr* x86_emit_025(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_025;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 26 */
X86Instr* x86_emit_026(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_026;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 27 */
X86Instr* x86_emit_027(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_027;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 28 */
X86Instr* x86_emit_028(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_028;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 29 */
X86Instr* x86_emit_029(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_029;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 30 */
X86Instr* x86_emit_030(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_030;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 31 */
X86Instr* x86_emit_031(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_031;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 32 */
X86Instr* x86_emit_032(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_032;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 33 */
X86Instr* x86_emit_033(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_033;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 34 */
X86Instr* x86_emit_034(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_034;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 35 */
X86Instr* x86_emit_035(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_035;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 36 */
X86Instr* x86_emit_036(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_036;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 37 */
X86Instr* x86_emit_037(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_037;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 38 */
X86Instr* x86_emit_038(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_038;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 39 */
X86Instr* x86_emit_039(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_039;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 40 */
X86Instr* x86_emit_040(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_040;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 41 */
X86Instr* x86_emit_041(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_041;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 42 */
X86Instr* x86_emit_042(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_042;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 43 */
X86Instr* x86_emit_043(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_043;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 44 */
X86Instr* x86_emit_044(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_044;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 45 */
X86Instr* x86_emit_045(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_045;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 46 */
X86Instr* x86_emit_046(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_046;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 47 */
X86Instr* x86_emit_047(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_047;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 48 */
X86Instr* x86_emit_048(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_048;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 49 */
X86Instr* x86_emit_049(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_049;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 50 */
X86Instr* x86_emit_050(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_050;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 51 */
X86Instr* x86_emit_051(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_051;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 52 */
X86Instr* x86_emit_052(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_052;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 53 */
X86Instr* x86_emit_053(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_053;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 54 */
X86Instr* x86_emit_054(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_054;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 55 */
X86Instr* x86_emit_055(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_055;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 56 */
X86Instr* x86_emit_056(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_056;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 57 */
X86Instr* x86_emit_057(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_057;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 58 */
X86Instr* x86_emit_058(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_058;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 59 */
X86Instr* x86_emit_059(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_059;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 60 */
X86Instr* x86_emit_060(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_060;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 61 */
X86Instr* x86_emit_061(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_061;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 62 */
X86Instr* x86_emit_062(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_062;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 63 */
X86Instr* x86_emit_063(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_063;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 64 */
X86Instr* x86_emit_064(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_064;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 65 */
X86Instr* x86_emit_065(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_065;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 66 */
X86Instr* x86_emit_066(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_066;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 67 */
X86Instr* x86_emit_067(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_067;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 68 */
X86Instr* x86_emit_068(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_068;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 69 */
X86Instr* x86_emit_069(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_069;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 70 */
X86Instr* x86_emit_070(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_070;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 71 */
X86Instr* x86_emit_071(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_071;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 72 */
X86Instr* x86_emit_072(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_072;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 73 */
X86Instr* x86_emit_073(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_073;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 74 */
X86Instr* x86_emit_074(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_074;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 75 */
X86Instr* x86_emit_075(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_075;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 76 */
X86Instr* x86_emit_076(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_076;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 77 */
X86Instr* x86_emit_077(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_077;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 78 */
X86Instr* x86_emit_078(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_078;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 79 */
X86Instr* x86_emit_079(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_079;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 80 */
X86Instr* x86_emit_080(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_080;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 81 */
X86Instr* x86_emit_081(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_081;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 82 */
X86Instr* x86_emit_082(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_082;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 83 */
X86Instr* x86_emit_083(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_083;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 84 */
X86Instr* x86_emit_084(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_084;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 85 */
X86Instr* x86_emit_085(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_085;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 86 */
X86Instr* x86_emit_086(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_086;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 87 */
X86Instr* x86_emit_087(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_087;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 88 */
X86Instr* x86_emit_088(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_088;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 89 */
X86Instr* x86_emit_089(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_089;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 90 */
X86Instr* x86_emit_090(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_090;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 91 */
X86Instr* x86_emit_091(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_091;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 92 */
X86Instr* x86_emit_092(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_092;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 93 */
X86Instr* x86_emit_093(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_093;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 94 */
X86Instr* x86_emit_094(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_094;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 95 */
X86Instr* x86_emit_095(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_095;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 96 */
X86Instr* x86_emit_096(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_096;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 97 */
X86Instr* x86_emit_097(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_097;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 98 */
X86Instr* x86_emit_098(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_098;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 99 */
X86Instr* x86_emit_099(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_099;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 100 */
X86Instr* x86_emit_100(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_100;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 101 */
X86Instr* x86_emit_101(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_101;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 102 */
X86Instr* x86_emit_102(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_102;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 103 */
X86Instr* x86_emit_103(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_103;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 104 */
X86Instr* x86_emit_104(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_104;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 105 */
X86Instr* x86_emit_105(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_105;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 106 */
X86Instr* x86_emit_106(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_106;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 107 */
X86Instr* x86_emit_107(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_107;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 108 */
X86Instr* x86_emit_108(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_108;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 109 */
X86Instr* x86_emit_109(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_109;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 110 */
X86Instr* x86_emit_110(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_110;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 111 */
X86Instr* x86_emit_111(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_111;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 112 */
X86Instr* x86_emit_112(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_112;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 113 */
X86Instr* x86_emit_113(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_113;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 114 */
X86Instr* x86_emit_114(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_114;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 115 */
X86Instr* x86_emit_115(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_115;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 116 */
X86Instr* x86_emit_116(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_116;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 117 */
X86Instr* x86_emit_117(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_117;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 118 */
X86Instr* x86_emit_118(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_118;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 119 */
X86Instr* x86_emit_119(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_119;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 120 */
X86Instr* x86_emit_120(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_120;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 121 */
X86Instr* x86_emit_121(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_121;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 122 */
X86Instr* x86_emit_122(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_122;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 123 */
X86Instr* x86_emit_123(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_123;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 124 */
X86Instr* x86_emit_124(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_124;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 125 */
X86Instr* x86_emit_125(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_125;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 126 */
X86Instr* x86_emit_126(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_126;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 127 */
X86Instr* x86_emit_127(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_127;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 128 */
X86Instr* x86_emit_128(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_128;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 129 */
X86Instr* x86_emit_129(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_129;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 130 */
X86Instr* x86_emit_130(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_130;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 131 */
X86Instr* x86_emit_131(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_131;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 132 */
X86Instr* x86_emit_132(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_132;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 133 */
X86Instr* x86_emit_133(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_133;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 134 */
X86Instr* x86_emit_134(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_134;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 135 */
X86Instr* x86_emit_135(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_135;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 136 */
X86Instr* x86_emit_136(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_136;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 137 */
X86Instr* x86_emit_137(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_137;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 138 */
X86Instr* x86_emit_138(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_138;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 139 */
X86Instr* x86_emit_139(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_139;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 140 */
X86Instr* x86_emit_140(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_140;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 141 */
X86Instr* x86_emit_141(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_141;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 142 */
X86Instr* x86_emit_142(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_142;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 143 */
X86Instr* x86_emit_143(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_143;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 144 */
X86Instr* x86_emit_144(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_144;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 145 */
X86Instr* x86_emit_145(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_145;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 146 */
X86Instr* x86_emit_146(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_146;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 147 */
X86Instr* x86_emit_147(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_147;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 148 */
X86Instr* x86_emit_148(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_148;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 149 */
X86Instr* x86_emit_149(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_149;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 150 */
X86Instr* x86_emit_150(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_150;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 151 */
X86Instr* x86_emit_151(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_151;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 152 */
X86Instr* x86_emit_152(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_152;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 153 */
X86Instr* x86_emit_153(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_153;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 154 */
X86Instr* x86_emit_154(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_154;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 155 */
X86Instr* x86_emit_155(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_155;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 156 */
X86Instr* x86_emit_156(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_156;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 157 */
X86Instr* x86_emit_157(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_157;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 158 */
X86Instr* x86_emit_158(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_158;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 159 */
X86Instr* x86_emit_159(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_159;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 160 */
X86Instr* x86_emit_160(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_160;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 161 */
X86Instr* x86_emit_161(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_161;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 162 */
X86Instr* x86_emit_162(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_162;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 163 */
X86Instr* x86_emit_163(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_163;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 164 */
X86Instr* x86_emit_164(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_164;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 165 */
X86Instr* x86_emit_165(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_165;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 166 */
X86Instr* x86_emit_166(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_166;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 167 */
X86Instr* x86_emit_167(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_167;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 168 */
X86Instr* x86_emit_168(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_168;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 169 */
X86Instr* x86_emit_169(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_169;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 170 */
X86Instr* x86_emit_170(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_170;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 171 */
X86Instr* x86_emit_171(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_171;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 172 */
X86Instr* x86_emit_172(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_172;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 173 */
X86Instr* x86_emit_173(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_173;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 174 */
X86Instr* x86_emit_174(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_174;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 175 */
X86Instr* x86_emit_175(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_175;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 176 */
X86Instr* x86_emit_176(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_176;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 177 */
X86Instr* x86_emit_177(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_177;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 178 */
X86Instr* x86_emit_178(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_178;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 179 */
X86Instr* x86_emit_179(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_179;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 180 */
X86Instr* x86_emit_180(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_180;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 181 */
X86Instr* x86_emit_181(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_181;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 182 */
X86Instr* x86_emit_182(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_182;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 183 */
X86Instr* x86_emit_183(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_183;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 184 */
X86Instr* x86_emit_184(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_184;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 185 */
X86Instr* x86_emit_185(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_185;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 186 */
X86Instr* x86_emit_186(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_186;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 187 */
X86Instr* x86_emit_187(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_187;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 188 */
X86Instr* x86_emit_188(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_188;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 189 */
X86Instr* x86_emit_189(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_189;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 190 */
X86Instr* x86_emit_190(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_190;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 191 */
X86Instr* x86_emit_191(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_191;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 192 */
X86Instr* x86_emit_192(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_192;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 193 */
X86Instr* x86_emit_193(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_193;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 194 */
X86Instr* x86_emit_194(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_194;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 195 */
X86Instr* x86_emit_195(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_195;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 196 */
X86Instr* x86_emit_196(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_196;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 197 */
X86Instr* x86_emit_197(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_197;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 198 */
X86Instr* x86_emit_198(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_198;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 199 */
X86Instr* x86_emit_199(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_199;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 200 */
X86Instr* x86_emit_200(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_200;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 201 */
X86Instr* x86_emit_201(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_201;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 202 */
X86Instr* x86_emit_202(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_202;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 203 */
X86Instr* x86_emit_203(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_203;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 204 */
X86Instr* x86_emit_204(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_204;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 205 */
X86Instr* x86_emit_205(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_205;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 206 */
X86Instr* x86_emit_206(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_206;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 207 */
X86Instr* x86_emit_207(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_207;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 208 */
X86Instr* x86_emit_208(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_208;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 209 */
X86Instr* x86_emit_209(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_209;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 210 */
X86Instr* x86_emit_210(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_210;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 211 */
X86Instr* x86_emit_211(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_211;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 212 */
X86Instr* x86_emit_212(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_212;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 213 */
X86Instr* x86_emit_213(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_213;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 214 */
X86Instr* x86_emit_214(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_214;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 215 */
X86Instr* x86_emit_215(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_215;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 216 */
X86Instr* x86_emit_216(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_216;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 217 */
X86Instr* x86_emit_217(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_217;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 218 */
X86Instr* x86_emit_218(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_218;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 219 */
X86Instr* x86_emit_219(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_219;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 220 */
X86Instr* x86_emit_220(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_220;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 221 */
X86Instr* x86_emit_221(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_221;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 222 */
X86Instr* x86_emit_222(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_222;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 223 */
X86Instr* x86_emit_223(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_223;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 224 */
X86Instr* x86_emit_224(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_224;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 225 */
X86Instr* x86_emit_225(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_225;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 226 */
X86Instr* x86_emit_226(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_226;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 227 */
X86Instr* x86_emit_227(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_227;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 228 */
X86Instr* x86_emit_228(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_228;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 229 */
X86Instr* x86_emit_229(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_229;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 230 */
X86Instr* x86_emit_230(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_230;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 231 */
X86Instr* x86_emit_231(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_231;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 232 */
X86Instr* x86_emit_232(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_232;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 233 */
X86Instr* x86_emit_233(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_233;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 234 */
X86Instr* x86_emit_234(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_234;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 235 */
X86Instr* x86_emit_235(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_235;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 236 */
X86Instr* x86_emit_236(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_236;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 237 */
X86Instr* x86_emit_237(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_237;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 238 */
X86Instr* x86_emit_238(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_238;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 239 */
X86Instr* x86_emit_239(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_239;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 240 */
X86Instr* x86_emit_240(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_240;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 241 */
X86Instr* x86_emit_241(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_241;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 242 */
X86Instr* x86_emit_242(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_242;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 243 */
X86Instr* x86_emit_243(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_243;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 244 */
X86Instr* x86_emit_244(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_244;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 245 */
X86Instr* x86_emit_245(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_245;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 246 */
X86Instr* x86_emit_246(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_246;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 247 */
X86Instr* x86_emit_247(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_247;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 248 */
X86Instr* x86_emit_248(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_248;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 249 */
X86Instr* x86_emit_249(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_249;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 250 */
X86Instr* x86_emit_250(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_250;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 251 */
X86Instr* x86_emit_251(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_251;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 252 */
X86Instr* x86_emit_252(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_252;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 253 */
X86Instr* x86_emit_253(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_253;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 254 */
X86Instr* x86_emit_254(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_254;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 255 */
X86Instr* x86_emit_255(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_255;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 256 */
X86Instr* x86_emit_256(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_256;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 257 */
X86Instr* x86_emit_257(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_257;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 258 */
X86Instr* x86_emit_258(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_258;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 259 */
X86Instr* x86_emit_259(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_259;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 260 */
X86Instr* x86_emit_260(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_260;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 261 */
X86Instr* x86_emit_261(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_261;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 262 */
X86Instr* x86_emit_262(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_262;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 263 */
X86Instr* x86_emit_263(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_263;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 264 */
X86Instr* x86_emit_264(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_264;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 265 */
X86Instr* x86_emit_265(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_265;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 266 */
X86Instr* x86_emit_266(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_266;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 267 */
X86Instr* x86_emit_267(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_267;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 268 */
X86Instr* x86_emit_268(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_268;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 269 */
X86Instr* x86_emit_269(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_269;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 270 */
X86Instr* x86_emit_270(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_270;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 271 */
X86Instr* x86_emit_271(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_271;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 272 */
X86Instr* x86_emit_272(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_272;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 273 */
X86Instr* x86_emit_273(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_273;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 274 */
X86Instr* x86_emit_274(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_274;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 275 */
X86Instr* x86_emit_275(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_275;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 276 */
X86Instr* x86_emit_276(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_276;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 277 */
X86Instr* x86_emit_277(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_277;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 278 */
X86Instr* x86_emit_278(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_278;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 279 */
X86Instr* x86_emit_279(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_279;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 280 */
X86Instr* x86_emit_280(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_280;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 281 */
X86Instr* x86_emit_281(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_281;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 282 */
X86Instr* x86_emit_282(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_282;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 283 */
X86Instr* x86_emit_283(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_283;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 284 */
X86Instr* x86_emit_284(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_284;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 285 */
X86Instr* x86_emit_285(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_285;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 286 */
X86Instr* x86_emit_286(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_286;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 287 */
X86Instr* x86_emit_287(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_287;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 288 */
X86Instr* x86_emit_288(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_288;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 289 */
X86Instr* x86_emit_289(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_289;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 290 */
X86Instr* x86_emit_290(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_290;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 291 */
X86Instr* x86_emit_291(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_291;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 292 */
X86Instr* x86_emit_292(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_292;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 293 */
X86Instr* x86_emit_293(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_293;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 294 */
X86Instr* x86_emit_294(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_294;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 295 */
X86Instr* x86_emit_295(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_295;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 296 */
X86Instr* x86_emit_296(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_296;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 297 */
X86Instr* x86_emit_297(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_297;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 298 */
X86Instr* x86_emit_298(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_298;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 299 */
X86Instr* x86_emit_299(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_299;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 300 */
X86Instr* x86_emit_300(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_300;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 301 */
X86Instr* x86_emit_301(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_301;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 302 */
X86Instr* x86_emit_302(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_302;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 303 */
X86Instr* x86_emit_303(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_303;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 304 */
X86Instr* x86_emit_304(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_304;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 305 */
X86Instr* x86_emit_305(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_305;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 306 */
X86Instr* x86_emit_306(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_306;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 307 */
X86Instr* x86_emit_307(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_307;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 308 */
X86Instr* x86_emit_308(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_308;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 309 */
X86Instr* x86_emit_309(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_309;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 310 */
X86Instr* x86_emit_310(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_310;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 311 */
X86Instr* x86_emit_311(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_311;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 312 */
X86Instr* x86_emit_312(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_312;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 313 */
X86Instr* x86_emit_313(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_313;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 314 */
X86Instr* x86_emit_314(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_314;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 315 */
X86Instr* x86_emit_315(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_315;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 316 */
X86Instr* x86_emit_316(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_316;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 317 */
X86Instr* x86_emit_317(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_317;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 318 */
X86Instr* x86_emit_318(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_318;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 319 */
X86Instr* x86_emit_319(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_319;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 320 */
X86Instr* x86_emit_320(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_320;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 321 */
X86Instr* x86_emit_321(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_321;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 322 */
X86Instr* x86_emit_322(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_322;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 323 */
X86Instr* x86_emit_323(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_323;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 324 */
X86Instr* x86_emit_324(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_324;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 325 */
X86Instr* x86_emit_325(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_325;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 326 */
X86Instr* x86_emit_326(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_326;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 327 */
X86Instr* x86_emit_327(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_327;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 328 */
X86Instr* x86_emit_328(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_328;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 329 */
X86Instr* x86_emit_329(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_329;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 330 */
X86Instr* x86_emit_330(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_330;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 331 */
X86Instr* x86_emit_331(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_331;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 332 */
X86Instr* x86_emit_332(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_332;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 333 */
X86Instr* x86_emit_333(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_333;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 334 */
X86Instr* x86_emit_334(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_334;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 335 */
X86Instr* x86_emit_335(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_335;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 336 */
X86Instr* x86_emit_336(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_336;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 337 */
X86Instr* x86_emit_337(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_337;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 338 */
X86Instr* x86_emit_338(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_338;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 339 */
X86Instr* x86_emit_339(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_339;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 340 */
X86Instr* x86_emit_340(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_340;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 341 */
X86Instr* x86_emit_341(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_341;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 342 */
X86Instr* x86_emit_342(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_342;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 343 */
X86Instr* x86_emit_343(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_343;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 344 */
X86Instr* x86_emit_344(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_344;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 345 */
X86Instr* x86_emit_345(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_345;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 346 */
X86Instr* x86_emit_346(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_346;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 347 */
X86Instr* x86_emit_347(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_347;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 348 */
X86Instr* x86_emit_348(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_348;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 349 */
X86Instr* x86_emit_349(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_349;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 350 */
X86Instr* x86_emit_350(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_350;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 351 */
X86Instr* x86_emit_351(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_351;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 352 */
X86Instr* x86_emit_352(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_352;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 353 */
X86Instr* x86_emit_353(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_353;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 354 */
X86Instr* x86_emit_354(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_354;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 355 */
X86Instr* x86_emit_355(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_355;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 356 */
X86Instr* x86_emit_356(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_356;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 357 */
X86Instr* x86_emit_357(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_357;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 358 */
X86Instr* x86_emit_358(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_358;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 359 */
X86Instr* x86_emit_359(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_359;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 360 */
X86Instr* x86_emit_360(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_360;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 361 */
X86Instr* x86_emit_361(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_361;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 362 */
X86Instr* x86_emit_362(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_362;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 363 */
X86Instr* x86_emit_363(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_363;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 364 */
X86Instr* x86_emit_364(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_364;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 365 */
X86Instr* x86_emit_365(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_365;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 366 */
X86Instr* x86_emit_366(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_366;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 367 */
X86Instr* x86_emit_367(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_367;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 368 */
X86Instr* x86_emit_368(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_368;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 369 */
X86Instr* x86_emit_369(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_369;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 370 */
X86Instr* x86_emit_370(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_370;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 371 */
X86Instr* x86_emit_371(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_371;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 372 */
X86Instr* x86_emit_372(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_372;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 373 */
X86Instr* x86_emit_373(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_373;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 374 */
X86Instr* x86_emit_374(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_374;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 375 */
X86Instr* x86_emit_375(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_375;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 376 */
X86Instr* x86_emit_376(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_376;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 377 */
X86Instr* x86_emit_377(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_377;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 378 */
X86Instr* x86_emit_378(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_378;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 379 */
X86Instr* x86_emit_379(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_379;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 380 */
X86Instr* x86_emit_380(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_380;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 381 */
X86Instr* x86_emit_381(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_381;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 382 */
X86Instr* x86_emit_382(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_382;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 383 */
X86Instr* x86_emit_383(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_383;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 384 */
X86Instr* x86_emit_384(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_384;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 385 */
X86Instr* x86_emit_385(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_385;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 386 */
X86Instr* x86_emit_386(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_386;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 387 */
X86Instr* x86_emit_387(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_387;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 388 */
X86Instr* x86_emit_388(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_388;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 389 */
X86Instr* x86_emit_389(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_389;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 390 */
X86Instr* x86_emit_390(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_390;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 391 */
X86Instr* x86_emit_391(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_391;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 392 */
X86Instr* x86_emit_392(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_392;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 393 */
X86Instr* x86_emit_393(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_393;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 394 */
X86Instr* x86_emit_394(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_394;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 395 */
X86Instr* x86_emit_395(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_395;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 396 */
X86Instr* x86_emit_396(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_396;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 397 */
X86Instr* x86_emit_397(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_397;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 398 */
X86Instr* x86_emit_398(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_398;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 399 */
X86Instr* x86_emit_399(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_399;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 400 */
X86Instr* x86_emit_400(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_400;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 401 */
X86Instr* x86_emit_401(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_401;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 402 */
X86Instr* x86_emit_402(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_402;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 403 */
X86Instr* x86_emit_403(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_403;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 404 */
X86Instr* x86_emit_404(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_404;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 405 */
X86Instr* x86_emit_405(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_405;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 406 */
X86Instr* x86_emit_406(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_406;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 407 */
X86Instr* x86_emit_407(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_407;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 408 */
X86Instr* x86_emit_408(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_408;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 409 */
X86Instr* x86_emit_409(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_409;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 410 */
X86Instr* x86_emit_410(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_410;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 411 */
X86Instr* x86_emit_411(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_411;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 412 */
X86Instr* x86_emit_412(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_412;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 413 */
X86Instr* x86_emit_413(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_413;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 414 */
X86Instr* x86_emit_414(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_414;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 415 */
X86Instr* x86_emit_415(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_415;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 416 */
X86Instr* x86_emit_416(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_416;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 417 */
X86Instr* x86_emit_417(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_417;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 418 */
X86Instr* x86_emit_418(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_418;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 419 */
X86Instr* x86_emit_419(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_419;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 420 */
X86Instr* x86_emit_420(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_420;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 421 */
X86Instr* x86_emit_421(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_421;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 422 */
X86Instr* x86_emit_422(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_422;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 423 */
X86Instr* x86_emit_423(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_423;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 424 */
X86Instr* x86_emit_424(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_424;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 425 */
X86Instr* x86_emit_425(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_425;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 426 */
X86Instr* x86_emit_426(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_426;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 427 */
X86Instr* x86_emit_427(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_427;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 428 */
X86Instr* x86_emit_428(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_428;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 429 */
X86Instr* x86_emit_429(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_429;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 430 */
X86Instr* x86_emit_430(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_430;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 431 */
X86Instr* x86_emit_431(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_431;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 432 */
X86Instr* x86_emit_432(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_432;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 433 */
X86Instr* x86_emit_433(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_433;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 434 */
X86Instr* x86_emit_434(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_434;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 435 */
X86Instr* x86_emit_435(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_435;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 436 */
X86Instr* x86_emit_436(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_436;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 437 */
X86Instr* x86_emit_437(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_437;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 438 */
X86Instr* x86_emit_438(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_438;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 439 */
X86Instr* x86_emit_439(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_439;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 440 */
X86Instr* x86_emit_440(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_440;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 441 */
X86Instr* x86_emit_441(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_441;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 442 */
X86Instr* x86_emit_442(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_442;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 443 */
X86Instr* x86_emit_443(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_443;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 444 */
X86Instr* x86_emit_444(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_444;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 445 */
X86Instr* x86_emit_445(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_445;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 446 */
X86Instr* x86_emit_446(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_446;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 447 */
X86Instr* x86_emit_447(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_447;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 448 */
X86Instr* x86_emit_448(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_448;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 449 */
X86Instr* x86_emit_449(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_449;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 450 */
X86Instr* x86_emit_450(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_450;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 451 */
X86Instr* x86_emit_451(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_451;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 452 */
X86Instr* x86_emit_452(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_452;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 453 */
X86Instr* x86_emit_453(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_453;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 454 */
X86Instr* x86_emit_454(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_454;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 455 */
X86Instr* x86_emit_455(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_455;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 456 */
X86Instr* x86_emit_456(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_456;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 457 */
X86Instr* x86_emit_457(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_457;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 458 */
X86Instr* x86_emit_458(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_458;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 459 */
X86Instr* x86_emit_459(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_459;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 460 */
X86Instr* x86_emit_460(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_460;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 461 */
X86Instr* x86_emit_461(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_461;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 462 */
X86Instr* x86_emit_462(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_462;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 463 */
X86Instr* x86_emit_463(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_463;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 464 */
X86Instr* x86_emit_464(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_464;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 465 */
X86Instr* x86_emit_465(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_465;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 466 */
X86Instr* x86_emit_466(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_466;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 467 */
X86Instr* x86_emit_467(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_467;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 468 */
X86Instr* x86_emit_468(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_468;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 469 */
X86Instr* x86_emit_469(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_469;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 470 */
X86Instr* x86_emit_470(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_470;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 471 */
X86Instr* x86_emit_471(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_471;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 472 */
X86Instr* x86_emit_472(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_472;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 473 */
X86Instr* x86_emit_473(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_473;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 474 */
X86Instr* x86_emit_474(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_474;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 475 */
X86Instr* x86_emit_475(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_475;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 476 */
X86Instr* x86_emit_476(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_476;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 477 */
X86Instr* x86_emit_477(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_477;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 478 */
X86Instr* x86_emit_478(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_478;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 479 */
X86Instr* x86_emit_479(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_479;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 480 */
X86Instr* x86_emit_480(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_480;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 481 */
X86Instr* x86_emit_481(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_481;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 482 */
X86Instr* x86_emit_482(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_482;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 483 */
X86Instr* x86_emit_483(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_483;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 484 */
X86Instr* x86_emit_484(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_484;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 485 */
X86Instr* x86_emit_485(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_485;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 486 */
X86Instr* x86_emit_486(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_486;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 487 */
X86Instr* x86_emit_487(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_487;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 488 */
X86Instr* x86_emit_488(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_488;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 489 */
X86Instr* x86_emit_489(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_489;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 490 */
X86Instr* x86_emit_490(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_490;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 491 */
X86Instr* x86_emit_491(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_491;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 492 */
X86Instr* x86_emit_492(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_492;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 493 */
X86Instr* x86_emit_493(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_493;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 494 */
X86Instr* x86_emit_494(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_494;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 495 */
X86Instr* x86_emit_495(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_495;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 496 */
X86Instr* x86_emit_496(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_496;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 497 */
X86Instr* x86_emit_497(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_497;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 498 */
X86Instr* x86_emit_498(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_498;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 x86_64 指令 499 */
X86Instr* x86_emit_499(X86Function* func, X86Register r1, X86Register r2, int imm) {
    X86Instr* instr = malloc(sizeof(X86Instr));
    instr->opcode = X86_X86_OP_499;
    instr->reg1 = r1;
    instr->reg2 = r2;
    instr->reg3 = X86_REG_RAX;
    instr->imm = imm;
    instr->mem_offset = 0;
    instr->mem_base = X86_REG_RSP;
    instr->mem_index = X86_REG_RAX;
    instr->mem_scale = 1;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}
