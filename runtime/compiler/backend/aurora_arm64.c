/*
 * Aurora 编译器后端 - ARM64 代码生成器实现
 */

#include "aurora_arm64.h"

/* 发射 ARM64 指令 0 */
ARM64Instr* arm64_emit_000(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_000;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 1 */
ARM64Instr* arm64_emit_001(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_001;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 2 */
ARM64Instr* arm64_emit_002(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_002;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 3 */
ARM64Instr* arm64_emit_003(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_003;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 4 */
ARM64Instr* arm64_emit_004(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_004;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 5 */
ARM64Instr* arm64_emit_005(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_005;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 6 */
ARM64Instr* arm64_emit_006(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_006;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 7 */
ARM64Instr* arm64_emit_007(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_007;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 8 */
ARM64Instr* arm64_emit_008(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_008;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 9 */
ARM64Instr* arm64_emit_009(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_009;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 10 */
ARM64Instr* arm64_emit_010(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_010;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 11 */
ARM64Instr* arm64_emit_011(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_011;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 12 */
ARM64Instr* arm64_emit_012(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_012;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 13 */
ARM64Instr* arm64_emit_013(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_013;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 14 */
ARM64Instr* arm64_emit_014(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_014;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 15 */
ARM64Instr* arm64_emit_015(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_015;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 16 */
ARM64Instr* arm64_emit_016(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_016;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 17 */
ARM64Instr* arm64_emit_017(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_017;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 18 */
ARM64Instr* arm64_emit_018(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_018;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 19 */
ARM64Instr* arm64_emit_019(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_019;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 20 */
ARM64Instr* arm64_emit_020(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_020;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 21 */
ARM64Instr* arm64_emit_021(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_021;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 22 */
ARM64Instr* arm64_emit_022(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_022;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 23 */
ARM64Instr* arm64_emit_023(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_023;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 24 */
ARM64Instr* arm64_emit_024(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_024;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 25 */
ARM64Instr* arm64_emit_025(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_025;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 26 */
ARM64Instr* arm64_emit_026(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_026;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 27 */
ARM64Instr* arm64_emit_027(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_027;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 28 */
ARM64Instr* arm64_emit_028(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_028;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 29 */
ARM64Instr* arm64_emit_029(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_029;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 30 */
ARM64Instr* arm64_emit_030(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_030;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 31 */
ARM64Instr* arm64_emit_031(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_031;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 32 */
ARM64Instr* arm64_emit_032(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_032;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 33 */
ARM64Instr* arm64_emit_033(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_033;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 34 */
ARM64Instr* arm64_emit_034(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_034;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 35 */
ARM64Instr* arm64_emit_035(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_035;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 36 */
ARM64Instr* arm64_emit_036(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_036;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 37 */
ARM64Instr* arm64_emit_037(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_037;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 38 */
ARM64Instr* arm64_emit_038(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_038;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 39 */
ARM64Instr* arm64_emit_039(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_039;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 40 */
ARM64Instr* arm64_emit_040(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_040;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 41 */
ARM64Instr* arm64_emit_041(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_041;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 42 */
ARM64Instr* arm64_emit_042(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_042;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 43 */
ARM64Instr* arm64_emit_043(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_043;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 44 */
ARM64Instr* arm64_emit_044(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_044;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 45 */
ARM64Instr* arm64_emit_045(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_045;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 46 */
ARM64Instr* arm64_emit_046(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_046;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 47 */
ARM64Instr* arm64_emit_047(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_047;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 48 */
ARM64Instr* arm64_emit_048(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_048;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 49 */
ARM64Instr* arm64_emit_049(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_049;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 50 */
ARM64Instr* arm64_emit_050(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_050;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 51 */
ARM64Instr* arm64_emit_051(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_051;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 52 */
ARM64Instr* arm64_emit_052(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_052;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 53 */
ARM64Instr* arm64_emit_053(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_053;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 54 */
ARM64Instr* arm64_emit_054(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_054;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 55 */
ARM64Instr* arm64_emit_055(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_055;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 56 */
ARM64Instr* arm64_emit_056(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_056;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 57 */
ARM64Instr* arm64_emit_057(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_057;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 58 */
ARM64Instr* arm64_emit_058(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_058;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 59 */
ARM64Instr* arm64_emit_059(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_059;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 60 */
ARM64Instr* arm64_emit_060(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_060;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 61 */
ARM64Instr* arm64_emit_061(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_061;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 62 */
ARM64Instr* arm64_emit_062(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_062;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 63 */
ARM64Instr* arm64_emit_063(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_063;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 64 */
ARM64Instr* arm64_emit_064(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_064;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 65 */
ARM64Instr* arm64_emit_065(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_065;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 66 */
ARM64Instr* arm64_emit_066(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_066;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 67 */
ARM64Instr* arm64_emit_067(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_067;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 68 */
ARM64Instr* arm64_emit_068(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_068;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 69 */
ARM64Instr* arm64_emit_069(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_069;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 70 */
ARM64Instr* arm64_emit_070(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_070;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 71 */
ARM64Instr* arm64_emit_071(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_071;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 72 */
ARM64Instr* arm64_emit_072(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_072;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 73 */
ARM64Instr* arm64_emit_073(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_073;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 74 */
ARM64Instr* arm64_emit_074(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_074;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 75 */
ARM64Instr* arm64_emit_075(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_075;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 76 */
ARM64Instr* arm64_emit_076(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_076;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 77 */
ARM64Instr* arm64_emit_077(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_077;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 78 */
ARM64Instr* arm64_emit_078(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_078;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 79 */
ARM64Instr* arm64_emit_079(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_079;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 80 */
ARM64Instr* arm64_emit_080(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_080;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 81 */
ARM64Instr* arm64_emit_081(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_081;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 82 */
ARM64Instr* arm64_emit_082(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_082;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 83 */
ARM64Instr* arm64_emit_083(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_083;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 84 */
ARM64Instr* arm64_emit_084(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_084;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 85 */
ARM64Instr* arm64_emit_085(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_085;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 86 */
ARM64Instr* arm64_emit_086(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_086;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 87 */
ARM64Instr* arm64_emit_087(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_087;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 88 */
ARM64Instr* arm64_emit_088(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_088;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 89 */
ARM64Instr* arm64_emit_089(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_089;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 90 */
ARM64Instr* arm64_emit_090(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_090;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 91 */
ARM64Instr* arm64_emit_091(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_091;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 92 */
ARM64Instr* arm64_emit_092(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_092;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 93 */
ARM64Instr* arm64_emit_093(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_093;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 94 */
ARM64Instr* arm64_emit_094(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_094;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 95 */
ARM64Instr* arm64_emit_095(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_095;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 96 */
ARM64Instr* arm64_emit_096(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_096;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 97 */
ARM64Instr* arm64_emit_097(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_097;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 98 */
ARM64Instr* arm64_emit_098(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_098;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 99 */
ARM64Instr* arm64_emit_099(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_099;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 100 */
ARM64Instr* arm64_emit_100(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_100;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 101 */
ARM64Instr* arm64_emit_101(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_101;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 102 */
ARM64Instr* arm64_emit_102(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_102;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 103 */
ARM64Instr* arm64_emit_103(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_103;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 104 */
ARM64Instr* arm64_emit_104(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_104;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 105 */
ARM64Instr* arm64_emit_105(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_105;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 106 */
ARM64Instr* arm64_emit_106(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_106;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 107 */
ARM64Instr* arm64_emit_107(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_107;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 108 */
ARM64Instr* arm64_emit_108(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_108;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 109 */
ARM64Instr* arm64_emit_109(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_109;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 110 */
ARM64Instr* arm64_emit_110(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_110;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 111 */
ARM64Instr* arm64_emit_111(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_111;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 112 */
ARM64Instr* arm64_emit_112(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_112;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 113 */
ARM64Instr* arm64_emit_113(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_113;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 114 */
ARM64Instr* arm64_emit_114(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_114;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 115 */
ARM64Instr* arm64_emit_115(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_115;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 116 */
ARM64Instr* arm64_emit_116(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_116;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 117 */
ARM64Instr* arm64_emit_117(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_117;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 118 */
ARM64Instr* arm64_emit_118(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_118;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 119 */
ARM64Instr* arm64_emit_119(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_119;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 120 */
ARM64Instr* arm64_emit_120(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_120;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 121 */
ARM64Instr* arm64_emit_121(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_121;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 122 */
ARM64Instr* arm64_emit_122(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_122;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 123 */
ARM64Instr* arm64_emit_123(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_123;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 124 */
ARM64Instr* arm64_emit_124(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_124;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 125 */
ARM64Instr* arm64_emit_125(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_125;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 126 */
ARM64Instr* arm64_emit_126(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_126;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 127 */
ARM64Instr* arm64_emit_127(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_127;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 128 */
ARM64Instr* arm64_emit_128(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_128;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 129 */
ARM64Instr* arm64_emit_129(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_129;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 130 */
ARM64Instr* arm64_emit_130(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_130;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 131 */
ARM64Instr* arm64_emit_131(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_131;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 132 */
ARM64Instr* arm64_emit_132(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_132;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 133 */
ARM64Instr* arm64_emit_133(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_133;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 134 */
ARM64Instr* arm64_emit_134(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_134;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 135 */
ARM64Instr* arm64_emit_135(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_135;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 136 */
ARM64Instr* arm64_emit_136(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_136;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 137 */
ARM64Instr* arm64_emit_137(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_137;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 138 */
ARM64Instr* arm64_emit_138(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_138;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 139 */
ARM64Instr* arm64_emit_139(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_139;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 140 */
ARM64Instr* arm64_emit_140(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_140;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 141 */
ARM64Instr* arm64_emit_141(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_141;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 142 */
ARM64Instr* arm64_emit_142(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_142;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 143 */
ARM64Instr* arm64_emit_143(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_143;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 144 */
ARM64Instr* arm64_emit_144(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_144;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 145 */
ARM64Instr* arm64_emit_145(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_145;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 146 */
ARM64Instr* arm64_emit_146(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_146;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 147 */
ARM64Instr* arm64_emit_147(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_147;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 148 */
ARM64Instr* arm64_emit_148(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_148;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 149 */
ARM64Instr* arm64_emit_149(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_149;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 150 */
ARM64Instr* arm64_emit_150(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_150;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 151 */
ARM64Instr* arm64_emit_151(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_151;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 152 */
ARM64Instr* arm64_emit_152(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_152;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 153 */
ARM64Instr* arm64_emit_153(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_153;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 154 */
ARM64Instr* arm64_emit_154(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_154;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 155 */
ARM64Instr* arm64_emit_155(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_155;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 156 */
ARM64Instr* arm64_emit_156(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_156;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 157 */
ARM64Instr* arm64_emit_157(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_157;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 158 */
ARM64Instr* arm64_emit_158(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_158;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 159 */
ARM64Instr* arm64_emit_159(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_159;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 160 */
ARM64Instr* arm64_emit_160(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_160;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 161 */
ARM64Instr* arm64_emit_161(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_161;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 162 */
ARM64Instr* arm64_emit_162(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_162;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 163 */
ARM64Instr* arm64_emit_163(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_163;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 164 */
ARM64Instr* arm64_emit_164(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_164;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 165 */
ARM64Instr* arm64_emit_165(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_165;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 166 */
ARM64Instr* arm64_emit_166(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_166;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 167 */
ARM64Instr* arm64_emit_167(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_167;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 168 */
ARM64Instr* arm64_emit_168(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_168;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 169 */
ARM64Instr* arm64_emit_169(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_169;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 170 */
ARM64Instr* arm64_emit_170(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_170;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 171 */
ARM64Instr* arm64_emit_171(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_171;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 172 */
ARM64Instr* arm64_emit_172(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_172;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 173 */
ARM64Instr* arm64_emit_173(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_173;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 174 */
ARM64Instr* arm64_emit_174(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_174;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 175 */
ARM64Instr* arm64_emit_175(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_175;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 176 */
ARM64Instr* arm64_emit_176(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_176;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 177 */
ARM64Instr* arm64_emit_177(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_177;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 178 */
ARM64Instr* arm64_emit_178(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_178;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 179 */
ARM64Instr* arm64_emit_179(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_179;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 180 */
ARM64Instr* arm64_emit_180(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_180;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 181 */
ARM64Instr* arm64_emit_181(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_181;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 182 */
ARM64Instr* arm64_emit_182(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_182;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 183 */
ARM64Instr* arm64_emit_183(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_183;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 184 */
ARM64Instr* arm64_emit_184(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_184;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 185 */
ARM64Instr* arm64_emit_185(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_185;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 186 */
ARM64Instr* arm64_emit_186(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_186;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 187 */
ARM64Instr* arm64_emit_187(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_187;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 188 */
ARM64Instr* arm64_emit_188(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_188;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 189 */
ARM64Instr* arm64_emit_189(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_189;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 190 */
ARM64Instr* arm64_emit_190(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_190;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 191 */
ARM64Instr* arm64_emit_191(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_191;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 192 */
ARM64Instr* arm64_emit_192(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_192;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 193 */
ARM64Instr* arm64_emit_193(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_193;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 194 */
ARM64Instr* arm64_emit_194(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_194;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 195 */
ARM64Instr* arm64_emit_195(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_195;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 196 */
ARM64Instr* arm64_emit_196(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_196;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 197 */
ARM64Instr* arm64_emit_197(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_197;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 198 */
ARM64Instr* arm64_emit_198(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_198;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 199 */
ARM64Instr* arm64_emit_199(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_199;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 200 */
ARM64Instr* arm64_emit_200(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_200;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 201 */
ARM64Instr* arm64_emit_201(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_201;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 202 */
ARM64Instr* arm64_emit_202(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_202;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 203 */
ARM64Instr* arm64_emit_203(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_203;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 204 */
ARM64Instr* arm64_emit_204(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_204;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 205 */
ARM64Instr* arm64_emit_205(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_205;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 206 */
ARM64Instr* arm64_emit_206(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_206;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 207 */
ARM64Instr* arm64_emit_207(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_207;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 208 */
ARM64Instr* arm64_emit_208(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_208;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 209 */
ARM64Instr* arm64_emit_209(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_209;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 210 */
ARM64Instr* arm64_emit_210(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_210;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 211 */
ARM64Instr* arm64_emit_211(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_211;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 212 */
ARM64Instr* arm64_emit_212(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_212;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 213 */
ARM64Instr* arm64_emit_213(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_213;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 214 */
ARM64Instr* arm64_emit_214(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_214;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 215 */
ARM64Instr* arm64_emit_215(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_215;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 216 */
ARM64Instr* arm64_emit_216(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_216;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 217 */
ARM64Instr* arm64_emit_217(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_217;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 218 */
ARM64Instr* arm64_emit_218(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_218;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 219 */
ARM64Instr* arm64_emit_219(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_219;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 220 */
ARM64Instr* arm64_emit_220(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_220;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 221 */
ARM64Instr* arm64_emit_221(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_221;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 222 */
ARM64Instr* arm64_emit_222(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_222;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 223 */
ARM64Instr* arm64_emit_223(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_223;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 224 */
ARM64Instr* arm64_emit_224(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_224;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 225 */
ARM64Instr* arm64_emit_225(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_225;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 226 */
ARM64Instr* arm64_emit_226(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_226;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 227 */
ARM64Instr* arm64_emit_227(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_227;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 228 */
ARM64Instr* arm64_emit_228(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_228;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 229 */
ARM64Instr* arm64_emit_229(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_229;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 230 */
ARM64Instr* arm64_emit_230(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_230;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 231 */
ARM64Instr* arm64_emit_231(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_231;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 232 */
ARM64Instr* arm64_emit_232(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_232;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 233 */
ARM64Instr* arm64_emit_233(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_233;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 234 */
ARM64Instr* arm64_emit_234(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_234;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 235 */
ARM64Instr* arm64_emit_235(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_235;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 236 */
ARM64Instr* arm64_emit_236(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_236;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 237 */
ARM64Instr* arm64_emit_237(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_237;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 238 */
ARM64Instr* arm64_emit_238(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_238;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 239 */
ARM64Instr* arm64_emit_239(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_239;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 240 */
ARM64Instr* arm64_emit_240(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_240;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 241 */
ARM64Instr* arm64_emit_241(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_241;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 242 */
ARM64Instr* arm64_emit_242(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_242;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 243 */
ARM64Instr* arm64_emit_243(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_243;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 244 */
ARM64Instr* arm64_emit_244(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_244;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 245 */
ARM64Instr* arm64_emit_245(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_245;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 246 */
ARM64Instr* arm64_emit_246(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_246;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 247 */
ARM64Instr* arm64_emit_247(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_247;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 248 */
ARM64Instr* arm64_emit_248(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_248;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 249 */
ARM64Instr* arm64_emit_249(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_249;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 250 */
ARM64Instr* arm64_emit_250(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_250;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 251 */
ARM64Instr* arm64_emit_251(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_251;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 252 */
ARM64Instr* arm64_emit_252(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_252;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 253 */
ARM64Instr* arm64_emit_253(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_253;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 254 */
ARM64Instr* arm64_emit_254(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_254;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 255 */
ARM64Instr* arm64_emit_255(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_255;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 256 */
ARM64Instr* arm64_emit_256(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_256;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 257 */
ARM64Instr* arm64_emit_257(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_257;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 258 */
ARM64Instr* arm64_emit_258(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_258;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 259 */
ARM64Instr* arm64_emit_259(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_259;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 260 */
ARM64Instr* arm64_emit_260(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_260;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 261 */
ARM64Instr* arm64_emit_261(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_261;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 262 */
ARM64Instr* arm64_emit_262(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_262;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 263 */
ARM64Instr* arm64_emit_263(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_263;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 264 */
ARM64Instr* arm64_emit_264(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_264;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 265 */
ARM64Instr* arm64_emit_265(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_265;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 266 */
ARM64Instr* arm64_emit_266(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_266;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 267 */
ARM64Instr* arm64_emit_267(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_267;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 268 */
ARM64Instr* arm64_emit_268(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_268;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 269 */
ARM64Instr* arm64_emit_269(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_269;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 270 */
ARM64Instr* arm64_emit_270(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_270;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 271 */
ARM64Instr* arm64_emit_271(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_271;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 272 */
ARM64Instr* arm64_emit_272(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_272;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 273 */
ARM64Instr* arm64_emit_273(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_273;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 274 */
ARM64Instr* arm64_emit_274(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_274;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 275 */
ARM64Instr* arm64_emit_275(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_275;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 276 */
ARM64Instr* arm64_emit_276(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_276;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 277 */
ARM64Instr* arm64_emit_277(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_277;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 278 */
ARM64Instr* arm64_emit_278(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_278;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 279 */
ARM64Instr* arm64_emit_279(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_279;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 280 */
ARM64Instr* arm64_emit_280(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_280;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 281 */
ARM64Instr* arm64_emit_281(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_281;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 282 */
ARM64Instr* arm64_emit_282(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_282;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 283 */
ARM64Instr* arm64_emit_283(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_283;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 284 */
ARM64Instr* arm64_emit_284(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_284;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 285 */
ARM64Instr* arm64_emit_285(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_285;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 286 */
ARM64Instr* arm64_emit_286(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_286;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 287 */
ARM64Instr* arm64_emit_287(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_287;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 288 */
ARM64Instr* arm64_emit_288(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_288;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 289 */
ARM64Instr* arm64_emit_289(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_289;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 290 */
ARM64Instr* arm64_emit_290(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_290;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 291 */
ARM64Instr* arm64_emit_291(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_291;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 292 */
ARM64Instr* arm64_emit_292(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_292;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 293 */
ARM64Instr* arm64_emit_293(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_293;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 294 */
ARM64Instr* arm64_emit_294(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_294;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 295 */
ARM64Instr* arm64_emit_295(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_295;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 296 */
ARM64Instr* arm64_emit_296(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_296;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 297 */
ARM64Instr* arm64_emit_297(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_297;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 298 */
ARM64Instr* arm64_emit_298(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_298;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 299 */
ARM64Instr* arm64_emit_299(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_299;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 300 */
ARM64Instr* arm64_emit_300(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_300;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 301 */
ARM64Instr* arm64_emit_301(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_301;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 302 */
ARM64Instr* arm64_emit_302(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_302;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 303 */
ARM64Instr* arm64_emit_303(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_303;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 304 */
ARM64Instr* arm64_emit_304(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_304;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 305 */
ARM64Instr* arm64_emit_305(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_305;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 306 */
ARM64Instr* arm64_emit_306(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_306;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 307 */
ARM64Instr* arm64_emit_307(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_307;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 308 */
ARM64Instr* arm64_emit_308(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_308;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 309 */
ARM64Instr* arm64_emit_309(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_309;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 310 */
ARM64Instr* arm64_emit_310(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_310;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 311 */
ARM64Instr* arm64_emit_311(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_311;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 312 */
ARM64Instr* arm64_emit_312(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_312;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 313 */
ARM64Instr* arm64_emit_313(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_313;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 314 */
ARM64Instr* arm64_emit_314(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_314;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 315 */
ARM64Instr* arm64_emit_315(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_315;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 316 */
ARM64Instr* arm64_emit_316(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_316;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 317 */
ARM64Instr* arm64_emit_317(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_317;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 318 */
ARM64Instr* arm64_emit_318(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_318;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 319 */
ARM64Instr* arm64_emit_319(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_319;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 320 */
ARM64Instr* arm64_emit_320(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_320;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 321 */
ARM64Instr* arm64_emit_321(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_321;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 322 */
ARM64Instr* arm64_emit_322(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_322;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 323 */
ARM64Instr* arm64_emit_323(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_323;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 324 */
ARM64Instr* arm64_emit_324(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_324;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 325 */
ARM64Instr* arm64_emit_325(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_325;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 326 */
ARM64Instr* arm64_emit_326(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_326;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 327 */
ARM64Instr* arm64_emit_327(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_327;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 328 */
ARM64Instr* arm64_emit_328(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_328;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 329 */
ARM64Instr* arm64_emit_329(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_329;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 330 */
ARM64Instr* arm64_emit_330(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_330;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 331 */
ARM64Instr* arm64_emit_331(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_331;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 332 */
ARM64Instr* arm64_emit_332(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_332;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 333 */
ARM64Instr* arm64_emit_333(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_333;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 334 */
ARM64Instr* arm64_emit_334(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_334;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 335 */
ARM64Instr* arm64_emit_335(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_335;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 336 */
ARM64Instr* arm64_emit_336(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_336;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 337 */
ARM64Instr* arm64_emit_337(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_337;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 338 */
ARM64Instr* arm64_emit_338(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_338;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 339 */
ARM64Instr* arm64_emit_339(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_339;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 340 */
ARM64Instr* arm64_emit_340(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_340;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 341 */
ARM64Instr* arm64_emit_341(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_341;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 342 */
ARM64Instr* arm64_emit_342(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_342;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 343 */
ARM64Instr* arm64_emit_343(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_343;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 344 */
ARM64Instr* arm64_emit_344(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_344;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 345 */
ARM64Instr* arm64_emit_345(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_345;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 346 */
ARM64Instr* arm64_emit_346(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_346;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 347 */
ARM64Instr* arm64_emit_347(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_347;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 348 */
ARM64Instr* arm64_emit_348(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_348;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 349 */
ARM64Instr* arm64_emit_349(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_349;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 350 */
ARM64Instr* arm64_emit_350(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_350;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 351 */
ARM64Instr* arm64_emit_351(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_351;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 352 */
ARM64Instr* arm64_emit_352(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_352;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 353 */
ARM64Instr* arm64_emit_353(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_353;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 354 */
ARM64Instr* arm64_emit_354(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_354;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 355 */
ARM64Instr* arm64_emit_355(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_355;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 356 */
ARM64Instr* arm64_emit_356(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_356;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 357 */
ARM64Instr* arm64_emit_357(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_357;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 358 */
ARM64Instr* arm64_emit_358(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_358;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 359 */
ARM64Instr* arm64_emit_359(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_359;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 360 */
ARM64Instr* arm64_emit_360(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_360;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 361 */
ARM64Instr* arm64_emit_361(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_361;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 362 */
ARM64Instr* arm64_emit_362(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_362;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 363 */
ARM64Instr* arm64_emit_363(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_363;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 364 */
ARM64Instr* arm64_emit_364(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_364;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 365 */
ARM64Instr* arm64_emit_365(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_365;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 366 */
ARM64Instr* arm64_emit_366(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_366;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 367 */
ARM64Instr* arm64_emit_367(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_367;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 368 */
ARM64Instr* arm64_emit_368(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_368;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 369 */
ARM64Instr* arm64_emit_369(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_369;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 370 */
ARM64Instr* arm64_emit_370(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_370;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 371 */
ARM64Instr* arm64_emit_371(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_371;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 372 */
ARM64Instr* arm64_emit_372(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_372;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 373 */
ARM64Instr* arm64_emit_373(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_373;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 374 */
ARM64Instr* arm64_emit_374(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_374;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 375 */
ARM64Instr* arm64_emit_375(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_375;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 376 */
ARM64Instr* arm64_emit_376(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_376;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 377 */
ARM64Instr* arm64_emit_377(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_377;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 378 */
ARM64Instr* arm64_emit_378(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_378;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 379 */
ARM64Instr* arm64_emit_379(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_379;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 380 */
ARM64Instr* arm64_emit_380(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_380;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 381 */
ARM64Instr* arm64_emit_381(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_381;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 382 */
ARM64Instr* arm64_emit_382(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_382;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 383 */
ARM64Instr* arm64_emit_383(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_383;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 384 */
ARM64Instr* arm64_emit_384(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_384;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 385 */
ARM64Instr* arm64_emit_385(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_385;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 386 */
ARM64Instr* arm64_emit_386(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_386;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 387 */
ARM64Instr* arm64_emit_387(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_387;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 388 */
ARM64Instr* arm64_emit_388(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_388;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 389 */
ARM64Instr* arm64_emit_389(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_389;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 390 */
ARM64Instr* arm64_emit_390(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_390;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 391 */
ARM64Instr* arm64_emit_391(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_391;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 392 */
ARM64Instr* arm64_emit_392(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_392;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 393 */
ARM64Instr* arm64_emit_393(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_393;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 394 */
ARM64Instr* arm64_emit_394(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_394;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 395 */
ARM64Instr* arm64_emit_395(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_395;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 396 */
ARM64Instr* arm64_emit_396(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_396;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 397 */
ARM64Instr* arm64_emit_397(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_397;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 398 */
ARM64Instr* arm64_emit_398(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_398;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 399 */
ARM64Instr* arm64_emit_399(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_399;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 400 */
ARM64Instr* arm64_emit_400(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_400;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 401 */
ARM64Instr* arm64_emit_401(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_401;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 402 */
ARM64Instr* arm64_emit_402(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_402;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 403 */
ARM64Instr* arm64_emit_403(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_403;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 404 */
ARM64Instr* arm64_emit_404(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_404;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 405 */
ARM64Instr* arm64_emit_405(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_405;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 406 */
ARM64Instr* arm64_emit_406(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_406;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 407 */
ARM64Instr* arm64_emit_407(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_407;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 408 */
ARM64Instr* arm64_emit_408(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_408;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 409 */
ARM64Instr* arm64_emit_409(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_409;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 410 */
ARM64Instr* arm64_emit_410(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_410;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 411 */
ARM64Instr* arm64_emit_411(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_411;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 412 */
ARM64Instr* arm64_emit_412(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_412;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 413 */
ARM64Instr* arm64_emit_413(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_413;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 414 */
ARM64Instr* arm64_emit_414(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_414;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 415 */
ARM64Instr* arm64_emit_415(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_415;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 416 */
ARM64Instr* arm64_emit_416(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_416;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 417 */
ARM64Instr* arm64_emit_417(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_417;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 418 */
ARM64Instr* arm64_emit_418(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_418;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 419 */
ARM64Instr* arm64_emit_419(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_419;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 420 */
ARM64Instr* arm64_emit_420(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_420;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 421 */
ARM64Instr* arm64_emit_421(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_421;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 422 */
ARM64Instr* arm64_emit_422(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_422;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 423 */
ARM64Instr* arm64_emit_423(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_423;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 424 */
ARM64Instr* arm64_emit_424(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_424;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 425 */
ARM64Instr* arm64_emit_425(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_425;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 426 */
ARM64Instr* arm64_emit_426(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_426;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 427 */
ARM64Instr* arm64_emit_427(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_427;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 428 */
ARM64Instr* arm64_emit_428(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_428;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 429 */
ARM64Instr* arm64_emit_429(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_429;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 430 */
ARM64Instr* arm64_emit_430(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_430;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 431 */
ARM64Instr* arm64_emit_431(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_431;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 432 */
ARM64Instr* arm64_emit_432(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_432;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 433 */
ARM64Instr* arm64_emit_433(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_433;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 434 */
ARM64Instr* arm64_emit_434(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_434;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 435 */
ARM64Instr* arm64_emit_435(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_435;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 436 */
ARM64Instr* arm64_emit_436(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_436;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 437 */
ARM64Instr* arm64_emit_437(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_437;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 438 */
ARM64Instr* arm64_emit_438(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_438;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 439 */
ARM64Instr* arm64_emit_439(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_439;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 440 */
ARM64Instr* arm64_emit_440(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_440;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 441 */
ARM64Instr* arm64_emit_441(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_441;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 442 */
ARM64Instr* arm64_emit_442(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_442;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 443 */
ARM64Instr* arm64_emit_443(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_443;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 444 */
ARM64Instr* arm64_emit_444(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_444;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 445 */
ARM64Instr* arm64_emit_445(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_445;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 446 */
ARM64Instr* arm64_emit_446(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_446;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 447 */
ARM64Instr* arm64_emit_447(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_447;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 448 */
ARM64Instr* arm64_emit_448(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_448;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 449 */
ARM64Instr* arm64_emit_449(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_449;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 450 */
ARM64Instr* arm64_emit_450(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_450;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 451 */
ARM64Instr* arm64_emit_451(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_451;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 452 */
ARM64Instr* arm64_emit_452(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_452;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 453 */
ARM64Instr* arm64_emit_453(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_453;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 454 */
ARM64Instr* arm64_emit_454(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_454;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 455 */
ARM64Instr* arm64_emit_455(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_455;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 456 */
ARM64Instr* arm64_emit_456(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_456;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 457 */
ARM64Instr* arm64_emit_457(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_457;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 458 */
ARM64Instr* arm64_emit_458(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_458;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 459 */
ARM64Instr* arm64_emit_459(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_459;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 460 */
ARM64Instr* arm64_emit_460(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_460;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 461 */
ARM64Instr* arm64_emit_461(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_461;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 462 */
ARM64Instr* arm64_emit_462(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_462;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 463 */
ARM64Instr* arm64_emit_463(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_463;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 464 */
ARM64Instr* arm64_emit_464(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_464;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 465 */
ARM64Instr* arm64_emit_465(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_465;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 466 */
ARM64Instr* arm64_emit_466(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_466;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 467 */
ARM64Instr* arm64_emit_467(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_467;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 468 */
ARM64Instr* arm64_emit_468(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_468;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 469 */
ARM64Instr* arm64_emit_469(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_469;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 470 */
ARM64Instr* arm64_emit_470(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_470;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 471 */
ARM64Instr* arm64_emit_471(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_471;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 472 */
ARM64Instr* arm64_emit_472(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_472;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 473 */
ARM64Instr* arm64_emit_473(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_473;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 474 */
ARM64Instr* arm64_emit_474(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_474;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 475 */
ARM64Instr* arm64_emit_475(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_475;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 476 */
ARM64Instr* arm64_emit_476(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_476;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 477 */
ARM64Instr* arm64_emit_477(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_477;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 478 */
ARM64Instr* arm64_emit_478(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_478;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 479 */
ARM64Instr* arm64_emit_479(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_479;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 480 */
ARM64Instr* arm64_emit_480(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_480;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 481 */
ARM64Instr* arm64_emit_481(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_481;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 482 */
ARM64Instr* arm64_emit_482(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_482;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 483 */
ARM64Instr* arm64_emit_483(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_483;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 484 */
ARM64Instr* arm64_emit_484(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_484;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 485 */
ARM64Instr* arm64_emit_485(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_485;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 486 */
ARM64Instr* arm64_emit_486(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_486;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 487 */
ARM64Instr* arm64_emit_487(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_487;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 488 */
ARM64Instr* arm64_emit_488(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_488;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 489 */
ARM64Instr* arm64_emit_489(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_489;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 490 */
ARM64Instr* arm64_emit_490(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_490;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 491 */
ARM64Instr* arm64_emit_491(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_491;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 492 */
ARM64Instr* arm64_emit_492(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_492;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 493 */
ARM64Instr* arm64_emit_493(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_493;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 494 */
ARM64Instr* arm64_emit_494(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_494;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 495 */
ARM64Instr* arm64_emit_495(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_495;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 496 */
ARM64Instr* arm64_emit_496(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_496;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 497 */
ARM64Instr* arm64_emit_497(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_497;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 498 */
ARM64Instr* arm64_emit_498(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_498;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}

/* 发射 ARM64 指令 499 */
ARM64Instr* arm64_emit_499(ARM64Function* func, ARM64Register rd, ARM64Register rn, ARM64Register rm, int imm) {
    ARM64Instr* instr = malloc(sizeof(ARM64Instr));
    instr->opcode = ARM64_ARM64_OP_499;
    instr->rd = rd;
    instr->rn = rn;
    instr->rm = rm;
    instr->ra = ARM64_REG_XZR;
    instr->imm = imm;
    instr->shift = 0;
    instr->shift_type = 0;
    instr->label = NULL;
    instr->prev = NULL;
    instr->next = NULL;
    if (func->last) {
        func->last->next = instr;
        instr->prev = func->last;
    } else {
        func->first = instr;
    }
    func->last = instr;
    func->instr_count++;
    return instr;
}
