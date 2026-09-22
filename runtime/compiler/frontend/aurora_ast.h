/*
 * Aurora 编译器前端 - 语法分析器（AST 定义）
 * 支持 200+ AST 节点类型
 */

#ifndef AURORA_AST_H
#define AURORA_AST_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* AST 节点类型枚举 */
typedef enum {
    AST_NODE_000, /* AST 节点类型 0 */
    AST_NODE_001, /* AST 节点类型 1 */
    AST_NODE_002, /* AST 节点类型 2 */
    AST_NODE_003, /* AST 节点类型 3 */
    AST_NODE_004, /* AST 节点类型 4 */
    AST_NODE_005, /* AST 节点类型 5 */
    AST_NODE_006, /* AST 节点类型 6 */
    AST_NODE_007, /* AST 节点类型 7 */
    AST_NODE_008, /* AST 节点类型 8 */
    AST_NODE_009, /* AST 节点类型 9 */
    AST_NODE_010, /* AST 节点类型 10 */
    AST_NODE_011, /* AST 节点类型 11 */
    AST_NODE_012, /* AST 节点类型 12 */
    AST_NODE_013, /* AST 节点类型 13 */
    AST_NODE_014, /* AST 节点类型 14 */
    AST_NODE_015, /* AST 节点类型 15 */
    AST_NODE_016, /* AST 节点类型 16 */
    AST_NODE_017, /* AST 节点类型 17 */
    AST_NODE_018, /* AST 节点类型 18 */
    AST_NODE_019, /* AST 节点类型 19 */
    AST_NODE_020, /* AST 节点类型 20 */
    AST_NODE_021, /* AST 节点类型 21 */
    AST_NODE_022, /* AST 节点类型 22 */
    AST_NODE_023, /* AST 节点类型 23 */
    AST_NODE_024, /* AST 节点类型 24 */
    AST_NODE_025, /* AST 节点类型 25 */
    AST_NODE_026, /* AST 节点类型 26 */
    AST_NODE_027, /* AST 节点类型 27 */
    AST_NODE_028, /* AST 节点类型 28 */
    AST_NODE_029, /* AST 节点类型 29 */
    AST_NODE_030, /* AST 节点类型 30 */
    AST_NODE_031, /* AST 节点类型 31 */
    AST_NODE_032, /* AST 节点类型 32 */
    AST_NODE_033, /* AST 节点类型 33 */
    AST_NODE_034, /* AST 节点类型 34 */
    AST_NODE_035, /* AST 节点类型 35 */
    AST_NODE_036, /* AST 节点类型 36 */
    AST_NODE_037, /* AST 节点类型 37 */
    AST_NODE_038, /* AST 节点类型 38 */
    AST_NODE_039, /* AST 节点类型 39 */
    AST_NODE_040, /* AST 节点类型 40 */
    AST_NODE_041, /* AST 节点类型 41 */
    AST_NODE_042, /* AST 节点类型 42 */
    AST_NODE_043, /* AST 节点类型 43 */
    AST_NODE_044, /* AST 节点类型 44 */
    AST_NODE_045, /* AST 节点类型 45 */
    AST_NODE_046, /* AST 节点类型 46 */
    AST_NODE_047, /* AST 节点类型 47 */
    AST_NODE_048, /* AST 节点类型 48 */
    AST_NODE_049, /* AST 节点类型 49 */
    AST_NODE_050, /* AST 节点类型 50 */
    AST_NODE_051, /* AST 节点类型 51 */
    AST_NODE_052, /* AST 节点类型 52 */
    AST_NODE_053, /* AST 节点类型 53 */
    AST_NODE_054, /* AST 节点类型 54 */
    AST_NODE_055, /* AST 节点类型 55 */
    AST_NODE_056, /* AST 节点类型 56 */
    AST_NODE_057, /* AST 节点类型 57 */
    AST_NODE_058, /* AST 节点类型 58 */
    AST_NODE_059, /* AST 节点类型 59 */
    AST_NODE_060, /* AST 节点类型 60 */
    AST_NODE_061, /* AST 节点类型 61 */
    AST_NODE_062, /* AST 节点类型 62 */
    AST_NODE_063, /* AST 节点类型 63 */
    AST_NODE_064, /* AST 节点类型 64 */
    AST_NODE_065, /* AST 节点类型 65 */
    AST_NODE_066, /* AST 节点类型 66 */
    AST_NODE_067, /* AST 节点类型 67 */
    AST_NODE_068, /* AST 节点类型 68 */
    AST_NODE_069, /* AST 节点类型 69 */
    AST_NODE_070, /* AST 节点类型 70 */
    AST_NODE_071, /* AST 节点类型 71 */
    AST_NODE_072, /* AST 节点类型 72 */
    AST_NODE_073, /* AST 节点类型 73 */
    AST_NODE_074, /* AST 节点类型 74 */
    AST_NODE_075, /* AST 节点类型 75 */
    AST_NODE_076, /* AST 节点类型 76 */
    AST_NODE_077, /* AST 节点类型 77 */
    AST_NODE_078, /* AST 节点类型 78 */
    AST_NODE_079, /* AST 节点类型 79 */
    AST_NODE_080, /* AST 节点类型 80 */
    AST_NODE_081, /* AST 节点类型 81 */
    AST_NODE_082, /* AST 节点类型 82 */
    AST_NODE_083, /* AST 节点类型 83 */
    AST_NODE_084, /* AST 节点类型 84 */
    AST_NODE_085, /* AST 节点类型 85 */
    AST_NODE_086, /* AST 节点类型 86 */
    AST_NODE_087, /* AST 节点类型 87 */
    AST_NODE_088, /* AST 节点类型 88 */
    AST_NODE_089, /* AST 节点类型 89 */
    AST_NODE_090, /* AST 节点类型 90 */
    AST_NODE_091, /* AST 节点类型 91 */
    AST_NODE_092, /* AST 节点类型 92 */
    AST_NODE_093, /* AST 节点类型 93 */
    AST_NODE_094, /* AST 节点类型 94 */
    AST_NODE_095, /* AST 节点类型 95 */
    AST_NODE_096, /* AST 节点类型 96 */
    AST_NODE_097, /* AST 节点类型 97 */
    AST_NODE_098, /* AST 节点类型 98 */
    AST_NODE_099, /* AST 节点类型 99 */
    AST_NODE_100, /* AST 节点类型 100 */
    AST_NODE_101, /* AST 节点类型 101 */
    AST_NODE_102, /* AST 节点类型 102 */
    AST_NODE_103, /* AST 节点类型 103 */
    AST_NODE_104, /* AST 节点类型 104 */
    AST_NODE_105, /* AST 节点类型 105 */
    AST_NODE_106, /* AST 节点类型 106 */
    AST_NODE_107, /* AST 节点类型 107 */
    AST_NODE_108, /* AST 节点类型 108 */
    AST_NODE_109, /* AST 节点类型 109 */
    AST_NODE_110, /* AST 节点类型 110 */
    AST_NODE_111, /* AST 节点类型 111 */
    AST_NODE_112, /* AST 节点类型 112 */
    AST_NODE_113, /* AST 节点类型 113 */
    AST_NODE_114, /* AST 节点类型 114 */
    AST_NODE_115, /* AST 节点类型 115 */
    AST_NODE_116, /* AST 节点类型 116 */
    AST_NODE_117, /* AST 节点类型 117 */
    AST_NODE_118, /* AST 节点类型 118 */
    AST_NODE_119, /* AST 节点类型 119 */
    AST_NODE_120, /* AST 节点类型 120 */
    AST_NODE_121, /* AST 节点类型 121 */
    AST_NODE_122, /* AST 节点类型 122 */
    AST_NODE_123, /* AST 节点类型 123 */
    AST_NODE_124, /* AST 节点类型 124 */
    AST_NODE_125, /* AST 节点类型 125 */
    AST_NODE_126, /* AST 节点类型 126 */
    AST_NODE_127, /* AST 节点类型 127 */
    AST_NODE_128, /* AST 节点类型 128 */
    AST_NODE_129, /* AST 节点类型 129 */
    AST_NODE_130, /* AST 节点类型 130 */
    AST_NODE_131, /* AST 节点类型 131 */
    AST_NODE_132, /* AST 节点类型 132 */
    AST_NODE_133, /* AST 节点类型 133 */
    AST_NODE_134, /* AST 节点类型 134 */
    AST_NODE_135, /* AST 节点类型 135 */
    AST_NODE_136, /* AST 节点类型 136 */
    AST_NODE_137, /* AST 节点类型 137 */
    AST_NODE_138, /* AST 节点类型 138 */
    AST_NODE_139, /* AST 节点类型 139 */
    AST_NODE_140, /* AST 节点类型 140 */
    AST_NODE_141, /* AST 节点类型 141 */
    AST_NODE_142, /* AST 节点类型 142 */
    AST_NODE_143, /* AST 节点类型 143 */
    AST_NODE_144, /* AST 节点类型 144 */
    AST_NODE_145, /* AST 节点类型 145 */
    AST_NODE_146, /* AST 节点类型 146 */
    AST_NODE_147, /* AST 节点类型 147 */
    AST_NODE_148, /* AST 节点类型 148 */
    AST_NODE_149, /* AST 节点类型 149 */
    AST_NODE_150, /* AST 节点类型 150 */
    AST_NODE_151, /* AST 节点类型 151 */
    AST_NODE_152, /* AST 节点类型 152 */
    AST_NODE_153, /* AST 节点类型 153 */
    AST_NODE_154, /* AST 节点类型 154 */
    AST_NODE_155, /* AST 节点类型 155 */
    AST_NODE_156, /* AST 节点类型 156 */
    AST_NODE_157, /* AST 节点类型 157 */
    AST_NODE_158, /* AST 节点类型 158 */
    AST_NODE_159, /* AST 节点类型 159 */
    AST_NODE_160, /* AST 节点类型 160 */
    AST_NODE_161, /* AST 节点类型 161 */
    AST_NODE_162, /* AST 节点类型 162 */
    AST_NODE_163, /* AST 节点类型 163 */
    AST_NODE_164, /* AST 节点类型 164 */
    AST_NODE_165, /* AST 节点类型 165 */
    AST_NODE_166, /* AST 节点类型 166 */
    AST_NODE_167, /* AST 节点类型 167 */
    AST_NODE_168, /* AST 节点类型 168 */
    AST_NODE_169, /* AST 节点类型 169 */
    AST_NODE_170, /* AST 节点类型 170 */
    AST_NODE_171, /* AST 节点类型 171 */
    AST_NODE_172, /* AST 节点类型 172 */
    AST_NODE_173, /* AST 节点类型 173 */
    AST_NODE_174, /* AST 节点类型 174 */
    AST_NODE_175, /* AST 节点类型 175 */
    AST_NODE_176, /* AST 节点类型 176 */
    AST_NODE_177, /* AST 节点类型 177 */
    AST_NODE_178, /* AST 节点类型 178 */
    AST_NODE_179, /* AST 节点类型 179 */
    AST_NODE_180, /* AST 节点类型 180 */
    AST_NODE_181, /* AST 节点类型 181 */
    AST_NODE_182, /* AST 节点类型 182 */
    AST_NODE_183, /* AST 节点类型 183 */
    AST_NODE_184, /* AST 节点类型 184 */
    AST_NODE_185, /* AST 节点类型 185 */
    AST_NODE_186, /* AST 节点类型 186 */
    AST_NODE_187, /* AST 节点类型 187 */
    AST_NODE_188, /* AST 节点类型 188 */
    AST_NODE_189, /* AST 节点类型 189 */
    AST_NODE_190, /* AST 节点类型 190 */
    AST_NODE_191, /* AST 节点类型 191 */
    AST_NODE_192, /* AST 节点类型 192 */
    AST_NODE_193, /* AST 节点类型 193 */
    AST_NODE_194, /* AST 节点类型 194 */
    AST_NODE_195, /* AST 节点类型 195 */
    AST_NODE_196, /* AST 节点类型 196 */
    AST_NODE_197, /* AST 节点类型 197 */
    AST_NODE_198, /* AST 节点类型 198 */
    AST_NODE_199, /* AST 节点类型 199 */
    AST_NODE_COUNT
} ASTNodeType;

/* AST 节点结构体 */
typedef struct ASTNode {
    ASTNodeType type;
    char* value;
    int line;
    int col;
    struct ASTNode* parent;
    struct ASTNode** children;
    int child_count;
    int child_capacity;
    void* extra;
} ASTNode;

/* AST 遍历器 */
typedef struct {
    ASTNode* root;
    ASTNode* current;
    int index;
    int* stack;
    int stack_size;
    int stack_capacity;
} ASTIterator;

/* 函数声明 */
ASTNode* ast_create_000(const char* value, int line, int col);
ASTNode* ast_create_001(const char* value, int line, int col);
ASTNode* ast_create_002(const char* value, int line, int col);
ASTNode* ast_create_003(const char* value, int line, int col);
ASTNode* ast_create_004(const char* value, int line, int col);
ASTNode* ast_create_005(const char* value, int line, int col);
ASTNode* ast_create_006(const char* value, int line, int col);
ASTNode* ast_create_007(const char* value, int line, int col);
ASTNode* ast_create_008(const char* value, int line, int col);
ASTNode* ast_create_009(const char* value, int line, int col);
ASTNode* ast_create_010(const char* value, int line, int col);
ASTNode* ast_create_011(const char* value, int line, int col);
ASTNode* ast_create_012(const char* value, int line, int col);
ASTNode* ast_create_013(const char* value, int line, int col);
ASTNode* ast_create_014(const char* value, int line, int col);
ASTNode* ast_create_015(const char* value, int line, int col);
ASTNode* ast_create_016(const char* value, int line, int col);
ASTNode* ast_create_017(const char* value, int line, int col);
ASTNode* ast_create_018(const char* value, int line, int col);
ASTNode* ast_create_019(const char* value, int line, int col);
ASTNode* ast_create_020(const char* value, int line, int col);
ASTNode* ast_create_021(const char* value, int line, int col);
ASTNode* ast_create_022(const char* value, int line, int col);
ASTNode* ast_create_023(const char* value, int line, int col);
ASTNode* ast_create_024(const char* value, int line, int col);
ASTNode* ast_create_025(const char* value, int line, int col);
ASTNode* ast_create_026(const char* value, int line, int col);
ASTNode* ast_create_027(const char* value, int line, int col);
ASTNode* ast_create_028(const char* value, int line, int col);
ASTNode* ast_create_029(const char* value, int line, int col);
ASTNode* ast_create_030(const char* value, int line, int col);
ASTNode* ast_create_031(const char* value, int line, int col);
ASTNode* ast_create_032(const char* value, int line, int col);
ASTNode* ast_create_033(const char* value, int line, int col);
ASTNode* ast_create_034(const char* value, int line, int col);
ASTNode* ast_create_035(const char* value, int line, int col);
ASTNode* ast_create_036(const char* value, int line, int col);
ASTNode* ast_create_037(const char* value, int line, int col);
ASTNode* ast_create_038(const char* value, int line, int col);
ASTNode* ast_create_039(const char* value, int line, int col);
ASTNode* ast_create_040(const char* value, int line, int col);
ASTNode* ast_create_041(const char* value, int line, int col);
ASTNode* ast_create_042(const char* value, int line, int col);
ASTNode* ast_create_043(const char* value, int line, int col);
ASTNode* ast_create_044(const char* value, int line, int col);
ASTNode* ast_create_045(const char* value, int line, int col);
ASTNode* ast_create_046(const char* value, int line, int col);
ASTNode* ast_create_047(const char* value, int line, int col);
ASTNode* ast_create_048(const char* value, int line, int col);
ASTNode* ast_create_049(const char* value, int line, int col);
ASTNode* ast_create_050(const char* value, int line, int col);
ASTNode* ast_create_051(const char* value, int line, int col);
ASTNode* ast_create_052(const char* value, int line, int col);
ASTNode* ast_create_053(const char* value, int line, int col);
ASTNode* ast_create_054(const char* value, int line, int col);
ASTNode* ast_create_055(const char* value, int line, int col);
ASTNode* ast_create_056(const char* value, int line, int col);
ASTNode* ast_create_057(const char* value, int line, int col);
ASTNode* ast_create_058(const char* value, int line, int col);
ASTNode* ast_create_059(const char* value, int line, int col);
ASTNode* ast_create_060(const char* value, int line, int col);
ASTNode* ast_create_061(const char* value, int line, int col);
ASTNode* ast_create_062(const char* value, int line, int col);
ASTNode* ast_create_063(const char* value, int line, int col);
ASTNode* ast_create_064(const char* value, int line, int col);
ASTNode* ast_create_065(const char* value, int line, int col);
ASTNode* ast_create_066(const char* value, int line, int col);
ASTNode* ast_create_067(const char* value, int line, int col);
ASTNode* ast_create_068(const char* value, int line, int col);
ASTNode* ast_create_069(const char* value, int line, int col);
ASTNode* ast_create_070(const char* value, int line, int col);
ASTNode* ast_create_071(const char* value, int line, int col);
ASTNode* ast_create_072(const char* value, int line, int col);
ASTNode* ast_create_073(const char* value, int line, int col);
ASTNode* ast_create_074(const char* value, int line, int col);
ASTNode* ast_create_075(const char* value, int line, int col);
ASTNode* ast_create_076(const char* value, int line, int col);
ASTNode* ast_create_077(const char* value, int line, int col);
ASTNode* ast_create_078(const char* value, int line, int col);
ASTNode* ast_create_079(const char* value, int line, int col);
ASTNode* ast_create_080(const char* value, int line, int col);
ASTNode* ast_create_081(const char* value, int line, int col);
ASTNode* ast_create_082(const char* value, int line, int col);
ASTNode* ast_create_083(const char* value, int line, int col);
ASTNode* ast_create_084(const char* value, int line, int col);
ASTNode* ast_create_085(const char* value, int line, int col);
ASTNode* ast_create_086(const char* value, int line, int col);
ASTNode* ast_create_087(const char* value, int line, int col);
ASTNode* ast_create_088(const char* value, int line, int col);
ASTNode* ast_create_089(const char* value, int line, int col);
ASTNode* ast_create_090(const char* value, int line, int col);
ASTNode* ast_create_091(const char* value, int line, int col);
ASTNode* ast_create_092(const char* value, int line, int col);
ASTNode* ast_create_093(const char* value, int line, int col);
ASTNode* ast_create_094(const char* value, int line, int col);
ASTNode* ast_create_095(const char* value, int line, int col);
ASTNode* ast_create_096(const char* value, int line, int col);
ASTNode* ast_create_097(const char* value, int line, int col);
ASTNode* ast_create_098(const char* value, int line, int col);
ASTNode* ast_create_099(const char* value, int line, int col);
ASTNode* ast_create_100(const char* value, int line, int col);
ASTNode* ast_create_101(const char* value, int line, int col);
ASTNode* ast_create_102(const char* value, int line, int col);
ASTNode* ast_create_103(const char* value, int line, int col);
ASTNode* ast_create_104(const char* value, int line, int col);
ASTNode* ast_create_105(const char* value, int line, int col);
ASTNode* ast_create_106(const char* value, int line, int col);
ASTNode* ast_create_107(const char* value, int line, int col);
ASTNode* ast_create_108(const char* value, int line, int col);
ASTNode* ast_create_109(const char* value, int line, int col);
ASTNode* ast_create_110(const char* value, int line, int col);
ASTNode* ast_create_111(const char* value, int line, int col);
ASTNode* ast_create_112(const char* value, int line, int col);
ASTNode* ast_create_113(const char* value, int line, int col);
ASTNode* ast_create_114(const char* value, int line, int col);
ASTNode* ast_create_115(const char* value, int line, int col);
ASTNode* ast_create_116(const char* value, int line, int col);
ASTNode* ast_create_117(const char* value, int line, int col);
ASTNode* ast_create_118(const char* value, int line, int col);
ASTNode* ast_create_119(const char* value, int line, int col);
ASTNode* ast_create_120(const char* value, int line, int col);
ASTNode* ast_create_121(const char* value, int line, int col);
ASTNode* ast_create_122(const char* value, int line, int col);
ASTNode* ast_create_123(const char* value, int line, int col);
ASTNode* ast_create_124(const char* value, int line, int col);
ASTNode* ast_create_125(const char* value, int line, int col);
ASTNode* ast_create_126(const char* value, int line, int col);
ASTNode* ast_create_127(const char* value, int line, int col);
ASTNode* ast_create_128(const char* value, int line, int col);
ASTNode* ast_create_129(const char* value, int line, int col);
ASTNode* ast_create_130(const char* value, int line, int col);
ASTNode* ast_create_131(const char* value, int line, int col);
ASTNode* ast_create_132(const char* value, int line, int col);
ASTNode* ast_create_133(const char* value, int line, int col);
ASTNode* ast_create_134(const char* value, int line, int col);
ASTNode* ast_create_135(const char* value, int line, int col);
ASTNode* ast_create_136(const char* value, int line, int col);
ASTNode* ast_create_137(const char* value, int line, int col);
ASTNode* ast_create_138(const char* value, int line, int col);
ASTNode* ast_create_139(const char* value, int line, int col);
ASTNode* ast_create_140(const char* value, int line, int col);
ASTNode* ast_create_141(const char* value, int line, int col);
ASTNode* ast_create_142(const char* value, int line, int col);
ASTNode* ast_create_143(const char* value, int line, int col);
ASTNode* ast_create_144(const char* value, int line, int col);
ASTNode* ast_create_145(const char* value, int line, int col);
ASTNode* ast_create_146(const char* value, int line, int col);
ASTNode* ast_create_147(const char* value, int line, int col);
ASTNode* ast_create_148(const char* value, int line, int col);
ASTNode* ast_create_149(const char* value, int line, int col);
ASTNode* ast_create_150(const char* value, int line, int col);
ASTNode* ast_create_151(const char* value, int line, int col);
ASTNode* ast_create_152(const char* value, int line, int col);
ASTNode* ast_create_153(const char* value, int line, int col);
ASTNode* ast_create_154(const char* value, int line, int col);
ASTNode* ast_create_155(const char* value, int line, int col);
ASTNode* ast_create_156(const char* value, int line, int col);
ASTNode* ast_create_157(const char* value, int line, int col);
ASTNode* ast_create_158(const char* value, int line, int col);
ASTNode* ast_create_159(const char* value, int line, int col);
ASTNode* ast_create_160(const char* value, int line, int col);
ASTNode* ast_create_161(const char* value, int line, int col);
ASTNode* ast_create_162(const char* value, int line, int col);
ASTNode* ast_create_163(const char* value, int line, int col);
ASTNode* ast_create_164(const char* value, int line, int col);
ASTNode* ast_create_165(const char* value, int line, int col);
ASTNode* ast_create_166(const char* value, int line, int col);
ASTNode* ast_create_167(const char* value, int line, int col);
ASTNode* ast_create_168(const char* value, int line, int col);
ASTNode* ast_create_169(const char* value, int line, int col);
ASTNode* ast_create_170(const char* value, int line, int col);
ASTNode* ast_create_171(const char* value, int line, int col);
ASTNode* ast_create_172(const char* value, int line, int col);
ASTNode* ast_create_173(const char* value, int line, int col);
ASTNode* ast_create_174(const char* value, int line, int col);
ASTNode* ast_create_175(const char* value, int line, int col);
ASTNode* ast_create_176(const char* value, int line, int col);
ASTNode* ast_create_177(const char* value, int line, int col);
ASTNode* ast_create_178(const char* value, int line, int col);
ASTNode* ast_create_179(const char* value, int line, int col);
ASTNode* ast_create_180(const char* value, int line, int col);
ASTNode* ast_create_181(const char* value, int line, int col);
ASTNode* ast_create_182(const char* value, int line, int col);
ASTNode* ast_create_183(const char* value, int line, int col);
ASTNode* ast_create_184(const char* value, int line, int col);
ASTNode* ast_create_185(const char* value, int line, int col);
ASTNode* ast_create_186(const char* value, int line, int col);
ASTNode* ast_create_187(const char* value, int line, int col);
ASTNode* ast_create_188(const char* value, int line, int col);
ASTNode* ast_create_189(const char* value, int line, int col);
ASTNode* ast_create_190(const char* value, int line, int col);
ASTNode* ast_create_191(const char* value, int line, int col);
ASTNode* ast_create_192(const char* value, int line, int col);
ASTNode* ast_create_193(const char* value, int line, int col);
ASTNode* ast_create_194(const char* value, int line, int col);
ASTNode* ast_create_195(const char* value, int line, int col);
ASTNode* ast_create_196(const char* value, int line, int col);
ASTNode* ast_create_197(const char* value, int line, int col);
ASTNode* ast_create_198(const char* value, int line, int col);
ASTNode* ast_create_199(const char* value, int line, int col);
void ast_destroy(ASTNode* node);
void ast_add_child(ASTNode* parent, ASTNode* child);
ASTNode* ast_get_child(ASTNode* parent, int index);
int ast_child_count(ASTNode* parent);
void ast_print(ASTNode* node, int indent);
ASTIterator* ast_iterator_create(ASTNode* root);
void ast_iterator_destroy(ASTIterator* it);
ASTNode* ast_iterator_next(ASTIterator* it);
int ast_iterator_has_next(ASTIterator* it);

#endif /* AURORA_AST_H */