/*
 * Aurora 编译器中端 - IR（中间表示）
 * 支持 300+ IR 指令类型
 */

#ifndef AURORA_IR_H
#define AURORA_IR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* IR 指令操作码 */
typedef enum {
    IR_OP_000, /* IR 指令 0 */
    IR_OP_001, /* IR 指令 1 */
    IR_OP_002, /* IR 指令 2 */
    IR_OP_003, /* IR 指令 3 */
    IR_OP_004, /* IR 指令 4 */
    IR_OP_005, /* IR 指令 5 */
    IR_OP_006, /* IR 指令 6 */
    IR_OP_007, /* IR 指令 7 */
    IR_OP_008, /* IR 指令 8 */
    IR_OP_009, /* IR 指令 9 */
    IR_OP_010, /* IR 指令 10 */
    IR_OP_011, /* IR 指令 11 */
    IR_OP_012, /* IR 指令 12 */
    IR_OP_013, /* IR 指令 13 */
    IR_OP_014, /* IR 指令 14 */
    IR_OP_015, /* IR 指令 15 */
    IR_OP_016, /* IR 指令 16 */
    IR_OP_017, /* IR 指令 17 */
    IR_OP_018, /* IR 指令 18 */
    IR_OP_019, /* IR 指令 19 */
    IR_OP_020, /* IR 指令 20 */
    IR_OP_021, /* IR 指令 21 */
    IR_OP_022, /* IR 指令 22 */
    IR_OP_023, /* IR 指令 23 */
    IR_OP_024, /* IR 指令 24 */
    IR_OP_025, /* IR 指令 25 */
    IR_OP_026, /* IR 指令 26 */
    IR_OP_027, /* IR 指令 27 */
    IR_OP_028, /* IR 指令 28 */
    IR_OP_029, /* IR 指令 29 */
    IR_OP_030, /* IR 指令 30 */
    IR_OP_031, /* IR 指令 31 */
    IR_OP_032, /* IR 指令 32 */
    IR_OP_033, /* IR 指令 33 */
    IR_OP_034, /* IR 指令 34 */
    IR_OP_035, /* IR 指令 35 */
    IR_OP_036, /* IR 指令 36 */
    IR_OP_037, /* IR 指令 37 */
    IR_OP_038, /* IR 指令 38 */
    IR_OP_039, /* IR 指令 39 */
    IR_OP_040, /* IR 指令 40 */
    IR_OP_041, /* IR 指令 41 */
    IR_OP_042, /* IR 指令 42 */
    IR_OP_043, /* IR 指令 43 */
    IR_OP_044, /* IR 指令 44 */
    IR_OP_045, /* IR 指令 45 */
    IR_OP_046, /* IR 指令 46 */
    IR_OP_047, /* IR 指令 47 */
    IR_OP_048, /* IR 指令 48 */
    IR_OP_049, /* IR 指令 49 */
    IR_OP_050, /* IR 指令 50 */
    IR_OP_051, /* IR 指令 51 */
    IR_OP_052, /* IR 指令 52 */
    IR_OP_053, /* IR 指令 53 */
    IR_OP_054, /* IR 指令 54 */
    IR_OP_055, /* IR 指令 55 */
    IR_OP_056, /* IR 指令 56 */
    IR_OP_057, /* IR 指令 57 */
    IR_OP_058, /* IR 指令 58 */
    IR_OP_059, /* IR 指令 59 */
    IR_OP_060, /* IR 指令 60 */
    IR_OP_061, /* IR 指令 61 */
    IR_OP_062, /* IR 指令 62 */
    IR_OP_063, /* IR 指令 63 */
    IR_OP_064, /* IR 指令 64 */
    IR_OP_065, /* IR 指令 65 */
    IR_OP_066, /* IR 指令 66 */
    IR_OP_067, /* IR 指令 67 */
    IR_OP_068, /* IR 指令 68 */
    IR_OP_069, /* IR 指令 69 */
    IR_OP_070, /* IR 指令 70 */
    IR_OP_071, /* IR 指令 71 */
    IR_OP_072, /* IR 指令 72 */
    IR_OP_073, /* IR 指令 73 */
    IR_OP_074, /* IR 指令 74 */
    IR_OP_075, /* IR 指令 75 */
    IR_OP_076, /* IR 指令 76 */
    IR_OP_077, /* IR 指令 77 */
    IR_OP_078, /* IR 指令 78 */
    IR_OP_079, /* IR 指令 79 */
    IR_OP_080, /* IR 指令 80 */
    IR_OP_081, /* IR 指令 81 */
    IR_OP_082, /* IR 指令 82 */
    IR_OP_083, /* IR 指令 83 */
    IR_OP_084, /* IR 指令 84 */
    IR_OP_085, /* IR 指令 85 */
    IR_OP_086, /* IR 指令 86 */
    IR_OP_087, /* IR 指令 87 */
    IR_OP_088, /* IR 指令 88 */
    IR_OP_089, /* IR 指令 89 */
    IR_OP_090, /* IR 指令 90 */
    IR_OP_091, /* IR 指令 91 */
    IR_OP_092, /* IR 指令 92 */
    IR_OP_093, /* IR 指令 93 */
    IR_OP_094, /* IR 指令 94 */
    IR_OP_095, /* IR 指令 95 */
    IR_OP_096, /* IR 指令 96 */
    IR_OP_097, /* IR 指令 97 */
    IR_OP_098, /* IR 指令 98 */
    IR_OP_099, /* IR 指令 99 */
    IR_OP_100, /* IR 指令 100 */
    IR_OP_101, /* IR 指令 101 */
    IR_OP_102, /* IR 指令 102 */
    IR_OP_103, /* IR 指令 103 */
    IR_OP_104, /* IR 指令 104 */
    IR_OP_105, /* IR 指令 105 */
    IR_OP_106, /* IR 指令 106 */
    IR_OP_107, /* IR 指令 107 */
    IR_OP_108, /* IR 指令 108 */
    IR_OP_109, /* IR 指令 109 */
    IR_OP_110, /* IR 指令 110 */
    IR_OP_111, /* IR 指令 111 */
    IR_OP_112, /* IR 指令 112 */
    IR_OP_113, /* IR 指令 113 */
    IR_OP_114, /* IR 指令 114 */
    IR_OP_115, /* IR 指令 115 */
    IR_OP_116, /* IR 指令 116 */
    IR_OP_117, /* IR 指令 117 */
    IR_OP_118, /* IR 指令 118 */
    IR_OP_119, /* IR 指令 119 */
    IR_OP_120, /* IR 指令 120 */
    IR_OP_121, /* IR 指令 121 */
    IR_OP_122, /* IR 指令 122 */
    IR_OP_123, /* IR 指令 123 */
    IR_OP_124, /* IR 指令 124 */
    IR_OP_125, /* IR 指令 125 */
    IR_OP_126, /* IR 指令 126 */
    IR_OP_127, /* IR 指令 127 */
    IR_OP_128, /* IR 指令 128 */
    IR_OP_129, /* IR 指令 129 */
    IR_OP_130, /* IR 指令 130 */
    IR_OP_131, /* IR 指令 131 */
    IR_OP_132, /* IR 指令 132 */
    IR_OP_133, /* IR 指令 133 */
    IR_OP_134, /* IR 指令 134 */
    IR_OP_135, /* IR 指令 135 */
    IR_OP_136, /* IR 指令 136 */
    IR_OP_137, /* IR 指令 137 */
    IR_OP_138, /* IR 指令 138 */
    IR_OP_139, /* IR 指令 139 */
    IR_OP_140, /* IR 指令 140 */
    IR_OP_141, /* IR 指令 141 */
    IR_OP_142, /* IR 指令 142 */
    IR_OP_143, /* IR 指令 143 */
    IR_OP_144, /* IR 指令 144 */
    IR_OP_145, /* IR 指令 145 */
    IR_OP_146, /* IR 指令 146 */
    IR_OP_147, /* IR 指令 147 */
    IR_OP_148, /* IR 指令 148 */
    IR_OP_149, /* IR 指令 149 */
    IR_OP_150, /* IR 指令 150 */
    IR_OP_151, /* IR 指令 151 */
    IR_OP_152, /* IR 指令 152 */
    IR_OP_153, /* IR 指令 153 */
    IR_OP_154, /* IR 指令 154 */
    IR_OP_155, /* IR 指令 155 */
    IR_OP_156, /* IR 指令 156 */
    IR_OP_157, /* IR 指令 157 */
    IR_OP_158, /* IR 指令 158 */
    IR_OP_159, /* IR 指令 159 */
    IR_OP_160, /* IR 指令 160 */
    IR_OP_161, /* IR 指令 161 */
    IR_OP_162, /* IR 指令 162 */
    IR_OP_163, /* IR 指令 163 */
    IR_OP_164, /* IR 指令 164 */
    IR_OP_165, /* IR 指令 165 */
    IR_OP_166, /* IR 指令 166 */
    IR_OP_167, /* IR 指令 167 */
    IR_OP_168, /* IR 指令 168 */
    IR_OP_169, /* IR 指令 169 */
    IR_OP_170, /* IR 指令 170 */
    IR_OP_171, /* IR 指令 171 */
    IR_OP_172, /* IR 指令 172 */
    IR_OP_173, /* IR 指令 173 */
    IR_OP_174, /* IR 指令 174 */
    IR_OP_175, /* IR 指令 175 */
    IR_OP_176, /* IR 指令 176 */
    IR_OP_177, /* IR 指令 177 */
    IR_OP_178, /* IR 指令 178 */
    IR_OP_179, /* IR 指令 179 */
    IR_OP_180, /* IR 指令 180 */
    IR_OP_181, /* IR 指令 181 */
    IR_OP_182, /* IR 指令 182 */
    IR_OP_183, /* IR 指令 183 */
    IR_OP_184, /* IR 指令 184 */
    IR_OP_185, /* IR 指令 185 */
    IR_OP_186, /* IR 指令 186 */
    IR_OP_187, /* IR 指令 187 */
    IR_OP_188, /* IR 指令 188 */
    IR_OP_189, /* IR 指令 189 */
    IR_OP_190, /* IR 指令 190 */
    IR_OP_191, /* IR 指令 191 */
    IR_OP_192, /* IR 指令 192 */
    IR_OP_193, /* IR 指令 193 */
    IR_OP_194, /* IR 指令 194 */
    IR_OP_195, /* IR 指令 195 */
    IR_OP_196, /* IR 指令 196 */
    IR_OP_197, /* IR 指令 197 */
    IR_OP_198, /* IR 指令 198 */
    IR_OP_199, /* IR 指令 199 */
    IR_OP_200, /* IR 指令 200 */
    IR_OP_201, /* IR 指令 201 */
    IR_OP_202, /* IR 指令 202 */
    IR_OP_203, /* IR 指令 203 */
    IR_OP_204, /* IR 指令 204 */
    IR_OP_205, /* IR 指令 205 */
    IR_OP_206, /* IR 指令 206 */
    IR_OP_207, /* IR 指令 207 */
    IR_OP_208, /* IR 指令 208 */
    IR_OP_209, /* IR 指令 209 */
    IR_OP_210, /* IR 指令 210 */
    IR_OP_211, /* IR 指令 211 */
    IR_OP_212, /* IR 指令 212 */
    IR_OP_213, /* IR 指令 213 */
    IR_OP_214, /* IR 指令 214 */
    IR_OP_215, /* IR 指令 215 */
    IR_OP_216, /* IR 指令 216 */
    IR_OP_217, /* IR 指令 217 */
    IR_OP_218, /* IR 指令 218 */
    IR_OP_219, /* IR 指令 219 */
    IR_OP_220, /* IR 指令 220 */
    IR_OP_221, /* IR 指令 221 */
    IR_OP_222, /* IR 指令 222 */
    IR_OP_223, /* IR 指令 223 */
    IR_OP_224, /* IR 指令 224 */
    IR_OP_225, /* IR 指令 225 */
    IR_OP_226, /* IR 指令 226 */
    IR_OP_227, /* IR 指令 227 */
    IR_OP_228, /* IR 指令 228 */
    IR_OP_229, /* IR 指令 229 */
    IR_OP_230, /* IR 指令 230 */
    IR_OP_231, /* IR 指令 231 */
    IR_OP_232, /* IR 指令 232 */
    IR_OP_233, /* IR 指令 233 */
    IR_OP_234, /* IR 指令 234 */
    IR_OP_235, /* IR 指令 235 */
    IR_OP_236, /* IR 指令 236 */
    IR_OP_237, /* IR 指令 237 */
    IR_OP_238, /* IR 指令 238 */
    IR_OP_239, /* IR 指令 239 */
    IR_OP_240, /* IR 指令 240 */
    IR_OP_241, /* IR 指令 241 */
    IR_OP_242, /* IR 指令 242 */
    IR_OP_243, /* IR 指令 243 */
    IR_OP_244, /* IR 指令 244 */
    IR_OP_245, /* IR 指令 245 */
    IR_OP_246, /* IR 指令 246 */
    IR_OP_247, /* IR 指令 247 */
    IR_OP_248, /* IR 指令 248 */
    IR_OP_249, /* IR 指令 249 */
    IR_OP_250, /* IR 指令 250 */
    IR_OP_251, /* IR 指令 251 */
    IR_OP_252, /* IR 指令 252 */
    IR_OP_253, /* IR 指令 253 */
    IR_OP_254, /* IR 指令 254 */
    IR_OP_255, /* IR 指令 255 */
    IR_OP_256, /* IR 指令 256 */
    IR_OP_257, /* IR 指令 257 */
    IR_OP_258, /* IR 指令 258 */
    IR_OP_259, /* IR 指令 259 */
    IR_OP_260, /* IR 指令 260 */
    IR_OP_261, /* IR 指令 261 */
    IR_OP_262, /* IR 指令 262 */
    IR_OP_263, /* IR 指令 263 */
    IR_OP_264, /* IR 指令 264 */
    IR_OP_265, /* IR 指令 265 */
    IR_OP_266, /* IR 指令 266 */
    IR_OP_267, /* IR 指令 267 */
    IR_OP_268, /* IR 指令 268 */
    IR_OP_269, /* IR 指令 269 */
    IR_OP_270, /* IR 指令 270 */
    IR_OP_271, /* IR 指令 271 */
    IR_OP_272, /* IR 指令 272 */
    IR_OP_273, /* IR 指令 273 */
    IR_OP_274, /* IR 指令 274 */
    IR_OP_275, /* IR 指令 275 */
    IR_OP_276, /* IR 指令 276 */
    IR_OP_277, /* IR 指令 277 */
    IR_OP_278, /* IR 指令 278 */
    IR_OP_279, /* IR 指令 279 */
    IR_OP_280, /* IR 指令 280 */
    IR_OP_281, /* IR 指令 281 */
    IR_OP_282, /* IR 指令 282 */
    IR_OP_283, /* IR 指令 283 */
    IR_OP_284, /* IR 指令 284 */
    IR_OP_285, /* IR 指令 285 */
    IR_OP_286, /* IR 指令 286 */
    IR_OP_287, /* IR 指令 287 */
    IR_OP_288, /* IR 指令 288 */
    IR_OP_289, /* IR 指令 289 */
    IR_OP_290, /* IR 指令 290 */
    IR_OP_291, /* IR 指令 291 */
    IR_OP_292, /* IR 指令 292 */
    IR_OP_293, /* IR 指令 293 */
    IR_OP_294, /* IR 指令 294 */
    IR_OP_295, /* IR 指令 295 */
    IR_OP_296, /* IR 指令 296 */
    IR_OP_297, /* IR 指令 297 */
    IR_OP_298, /* IR 指令 298 */
    IR_OP_299, /* IR 指令 299 */
    IR_OP_COUNT
} IROpcode;

/* IR 值类型 */
typedef enum {
    IR_VAL_VOID,
    IR_VAL_INT,
    IR_VAL_FLOAT,
    IR_VAL_STRING,
    IR_VAL_BOOL,
    IR_VAL_PTR,
    IR_VAL_STRUCT,
    IR_VAL_ARRAY,
    IR_VAL_FUNC,
    IR_VAL_BLOCK,
    IR_VAL_REG,
    IR_VAL_CONST,
    IR_VAL_GLOBAL,
    IR_VAL_LOCAL,
    IR_VAL_ARG,
    IR_VAL_TEMP,
    IR_VAL_LABEL,
    IR_VAL_TYPE,
    IR_VAL_META,
} IRValueType;

/* IR 值 */
typedef struct IRValue {
    IRValueType type;
    union {
        long long int_val;
        double float_val;
        char* string_val;
        int bool_val;
        void* ptr_val;
        int reg_val;
        int label_val;
    };
    struct IRType* ir_type;
    char* name;
    int id;
    int use_count;
    struct IRInstruction** uses;
} IRValue;

/* IR 指令 */
typedef struct IRInstruction {
    IROpcode opcode;
    IRValue* result;
    IRValue** operands;
    int operand_count;
    struct IRBasicBlock* parent;
    struct IRInstruction* prev;
    struct IRInstruction* next;
    void* extra;
} IRInstruction;

/* IR 基本块 */
typedef struct IRBasicBlock {
    int id;
    char* name;
    IRInstruction* first;
    IRInstruction* last;
    int instr_count;
    struct IRBasicBlock** predecessors;
    int pred_count;
    struct IRBasicBlock** successors;
    int succ_count;
    struct IRFunction* parent;
    void* extra;
} IRBasicBlock;

/* IR 函数 */
typedef struct IRFunction {
    char* name;
    struct IRType* return_type;
    struct IRType** param_types;
    int param_count;
    IRBasicBlock** blocks;
    int block_count;
    int block_capacity;
    IRValue** locals;
    int local_count;
    struct IRModule* parent;
    void* extra;
} IRFunction;

/* IR 模块 */
typedef struct IRModule {
    char* name;
    IRFunction** functions;
    int function_count;
    int function_capacity;
    IRValue** globals;
    int global_count;
    struct IRType** types;
    int type_count;
    void* extra;
} IRModule;

/* 函数声明 */
IRInstruction* ir_create_000(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_001(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_002(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_003(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_004(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_005(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_006(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_007(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_008(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_009(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_010(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_011(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_012(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_013(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_014(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_015(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_016(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_017(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_018(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_019(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_020(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_021(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_022(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_023(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_024(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_025(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_026(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_027(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_028(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_029(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_030(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_031(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_032(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_033(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_034(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_035(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_036(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_037(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_038(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_039(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_040(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_041(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_042(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_043(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_044(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_045(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_046(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_047(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_048(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_049(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_050(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_051(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_052(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_053(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_054(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_055(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_056(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_057(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_058(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_059(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_060(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_061(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_062(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_063(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_064(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_065(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_066(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_067(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_068(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_069(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_070(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_071(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_072(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_073(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_074(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_075(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_076(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_077(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_078(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_079(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_080(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_081(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_082(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_083(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_084(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_085(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_086(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_087(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_088(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_089(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_090(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_091(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_092(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_093(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_094(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_095(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_096(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_097(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_098(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_099(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_100(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_101(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_102(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_103(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_104(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_105(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_106(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_107(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_108(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_109(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_110(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_111(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_112(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_113(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_114(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_115(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_116(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_117(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_118(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_119(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_120(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_121(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_122(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_123(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_124(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_125(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_126(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_127(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_128(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_129(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_130(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_131(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_132(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_133(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_134(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_135(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_136(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_137(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_138(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_139(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_140(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_141(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_142(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_143(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_144(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_145(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_146(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_147(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_148(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_149(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_150(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_151(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_152(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_153(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_154(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_155(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_156(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_157(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_158(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_159(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_160(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_161(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_162(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_163(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_164(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_165(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_166(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_167(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_168(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_169(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_170(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_171(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_172(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_173(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_174(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_175(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_176(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_177(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_178(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_179(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_180(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_181(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_182(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_183(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_184(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_185(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_186(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_187(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_188(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_189(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_190(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_191(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_192(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_193(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_194(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_195(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_196(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_197(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_198(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_199(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_200(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_201(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_202(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_203(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_204(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_205(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_206(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_207(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_208(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_209(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_210(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_211(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_212(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_213(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_214(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_215(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_216(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_217(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_218(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_219(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_220(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_221(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_222(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_223(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_224(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_225(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_226(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_227(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_228(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_229(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_230(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_231(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_232(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_233(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_234(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_235(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_236(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_237(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_238(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_239(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_240(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_241(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_242(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_243(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_244(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_245(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_246(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_247(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_248(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_249(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_250(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_251(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_252(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_253(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_254(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_255(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_256(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_257(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_258(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_259(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_260(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_261(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_262(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_263(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_264(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_265(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_266(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_267(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_268(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_269(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_270(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_271(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_272(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_273(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_274(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_275(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_276(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_277(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_278(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_279(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_280(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_281(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_282(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_283(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_284(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_285(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_286(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_287(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_288(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_289(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_290(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_291(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_292(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_293(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_294(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_295(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_296(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_297(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_298(IRValue* result, IRValue** operands, int count);
IRInstruction* ir_create_299(IRValue* result, IRValue** operands, int count);
IRModule* ir_module_create(const char* name);
void ir_module_destroy(IRModule* mod);
IRFunction* ir_function_create(IRModule* mod, const char* name);
IRBasicBlock* ir_basic_block_create(IRFunction* func, const char* name);
void ir_basic_block_append(IRBasicBlock* bb, IRInstruction* instr);
void ir_print(IRModule* mod);

#endif /* AURORA_IR_H */