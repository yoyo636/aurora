/*
 * Aurora 编译器中端 - 优化 Pass 管理器
 * 支持 200+ 优化 Pass
 */

#ifndef AURORA_OPT_H
#define AURORA_OPT_H

#include "aurora_ir.h"

/* 优化 Pass 类型 */
typedef enum {
    OPT_OPT_PASS_000, /* 优化 Pass 0 */
    OPT_OPT_PASS_001, /* 优化 Pass 1 */
    OPT_OPT_PASS_002, /* 优化 Pass 2 */
    OPT_OPT_PASS_003, /* 优化 Pass 3 */
    OPT_OPT_PASS_004, /* 优化 Pass 4 */
    OPT_OPT_PASS_005, /* 优化 Pass 5 */
    OPT_OPT_PASS_006, /* 优化 Pass 6 */
    OPT_OPT_PASS_007, /* 优化 Pass 7 */
    OPT_OPT_PASS_008, /* 优化 Pass 8 */
    OPT_OPT_PASS_009, /* 优化 Pass 9 */
    OPT_OPT_PASS_010, /* 优化 Pass 10 */
    OPT_OPT_PASS_011, /* 优化 Pass 11 */
    OPT_OPT_PASS_012, /* 优化 Pass 12 */
    OPT_OPT_PASS_013, /* 优化 Pass 13 */
    OPT_OPT_PASS_014, /* 优化 Pass 14 */
    OPT_OPT_PASS_015, /* 优化 Pass 15 */
    OPT_OPT_PASS_016, /* 优化 Pass 16 */
    OPT_OPT_PASS_017, /* 优化 Pass 17 */
    OPT_OPT_PASS_018, /* 优化 Pass 18 */
    OPT_OPT_PASS_019, /* 优化 Pass 19 */
    OPT_OPT_PASS_020, /* 优化 Pass 20 */
    OPT_OPT_PASS_021, /* 优化 Pass 21 */
    OPT_OPT_PASS_022, /* 优化 Pass 22 */
    OPT_OPT_PASS_023, /* 优化 Pass 23 */
    OPT_OPT_PASS_024, /* 优化 Pass 24 */
    OPT_OPT_PASS_025, /* 优化 Pass 25 */
    OPT_OPT_PASS_026, /* 优化 Pass 26 */
    OPT_OPT_PASS_027, /* 优化 Pass 27 */
    OPT_OPT_PASS_028, /* 优化 Pass 28 */
    OPT_OPT_PASS_029, /* 优化 Pass 29 */
    OPT_OPT_PASS_030, /* 优化 Pass 30 */
    OPT_OPT_PASS_031, /* 优化 Pass 31 */
    OPT_OPT_PASS_032, /* 优化 Pass 32 */
    OPT_OPT_PASS_033, /* 优化 Pass 33 */
    OPT_OPT_PASS_034, /* 优化 Pass 34 */
    OPT_OPT_PASS_035, /* 优化 Pass 35 */
    OPT_OPT_PASS_036, /* 优化 Pass 36 */
    OPT_OPT_PASS_037, /* 优化 Pass 37 */
    OPT_OPT_PASS_038, /* 优化 Pass 38 */
    OPT_OPT_PASS_039, /* 优化 Pass 39 */
    OPT_OPT_PASS_040, /* 优化 Pass 40 */
    OPT_OPT_PASS_041, /* 优化 Pass 41 */
    OPT_OPT_PASS_042, /* 优化 Pass 42 */
    OPT_OPT_PASS_043, /* 优化 Pass 43 */
    OPT_OPT_PASS_044, /* 优化 Pass 44 */
    OPT_OPT_PASS_045, /* 优化 Pass 45 */
    OPT_OPT_PASS_046, /* 优化 Pass 46 */
    OPT_OPT_PASS_047, /* 优化 Pass 47 */
    OPT_OPT_PASS_048, /* 优化 Pass 48 */
    OPT_OPT_PASS_049, /* 优化 Pass 49 */
    OPT_OPT_PASS_050, /* 优化 Pass 50 */
    OPT_OPT_PASS_051, /* 优化 Pass 51 */
    OPT_OPT_PASS_052, /* 优化 Pass 52 */
    OPT_OPT_PASS_053, /* 优化 Pass 53 */
    OPT_OPT_PASS_054, /* 优化 Pass 54 */
    OPT_OPT_PASS_055, /* 优化 Pass 55 */
    OPT_OPT_PASS_056, /* 优化 Pass 56 */
    OPT_OPT_PASS_057, /* 优化 Pass 57 */
    OPT_OPT_PASS_058, /* 优化 Pass 58 */
    OPT_OPT_PASS_059, /* 优化 Pass 59 */
    OPT_OPT_PASS_060, /* 优化 Pass 60 */
    OPT_OPT_PASS_061, /* 优化 Pass 61 */
    OPT_OPT_PASS_062, /* 优化 Pass 62 */
    OPT_OPT_PASS_063, /* 优化 Pass 63 */
    OPT_OPT_PASS_064, /* 优化 Pass 64 */
    OPT_OPT_PASS_065, /* 优化 Pass 65 */
    OPT_OPT_PASS_066, /* 优化 Pass 66 */
    OPT_OPT_PASS_067, /* 优化 Pass 67 */
    OPT_OPT_PASS_068, /* 优化 Pass 68 */
    OPT_OPT_PASS_069, /* 优化 Pass 69 */
    OPT_OPT_PASS_070, /* 优化 Pass 70 */
    OPT_OPT_PASS_071, /* 优化 Pass 71 */
    OPT_OPT_PASS_072, /* 优化 Pass 72 */
    OPT_OPT_PASS_073, /* 优化 Pass 73 */
    OPT_OPT_PASS_074, /* 优化 Pass 74 */
    OPT_OPT_PASS_075, /* 优化 Pass 75 */
    OPT_OPT_PASS_076, /* 优化 Pass 76 */
    OPT_OPT_PASS_077, /* 优化 Pass 77 */
    OPT_OPT_PASS_078, /* 优化 Pass 78 */
    OPT_OPT_PASS_079, /* 优化 Pass 79 */
    OPT_OPT_PASS_080, /* 优化 Pass 80 */
    OPT_OPT_PASS_081, /* 优化 Pass 81 */
    OPT_OPT_PASS_082, /* 优化 Pass 82 */
    OPT_OPT_PASS_083, /* 优化 Pass 83 */
    OPT_OPT_PASS_084, /* 优化 Pass 84 */
    OPT_OPT_PASS_085, /* 优化 Pass 85 */
    OPT_OPT_PASS_086, /* 优化 Pass 86 */
    OPT_OPT_PASS_087, /* 优化 Pass 87 */
    OPT_OPT_PASS_088, /* 优化 Pass 88 */
    OPT_OPT_PASS_089, /* 优化 Pass 89 */
    OPT_OPT_PASS_090, /* 优化 Pass 90 */
    OPT_OPT_PASS_091, /* 优化 Pass 91 */
    OPT_OPT_PASS_092, /* 优化 Pass 92 */
    OPT_OPT_PASS_093, /* 优化 Pass 93 */
    OPT_OPT_PASS_094, /* 优化 Pass 94 */
    OPT_OPT_PASS_095, /* 优化 Pass 95 */
    OPT_OPT_PASS_096, /* 优化 Pass 96 */
    OPT_OPT_PASS_097, /* 优化 Pass 97 */
    OPT_OPT_PASS_098, /* 优化 Pass 98 */
    OPT_OPT_PASS_099, /* 优化 Pass 99 */
    OPT_OPT_PASS_100, /* 优化 Pass 100 */
    OPT_OPT_PASS_101, /* 优化 Pass 101 */
    OPT_OPT_PASS_102, /* 优化 Pass 102 */
    OPT_OPT_PASS_103, /* 优化 Pass 103 */
    OPT_OPT_PASS_104, /* 优化 Pass 104 */
    OPT_OPT_PASS_105, /* 优化 Pass 105 */
    OPT_OPT_PASS_106, /* 优化 Pass 106 */
    OPT_OPT_PASS_107, /* 优化 Pass 107 */
    OPT_OPT_PASS_108, /* 优化 Pass 108 */
    OPT_OPT_PASS_109, /* 优化 Pass 109 */
    OPT_OPT_PASS_110, /* 优化 Pass 110 */
    OPT_OPT_PASS_111, /* 优化 Pass 111 */
    OPT_OPT_PASS_112, /* 优化 Pass 112 */
    OPT_OPT_PASS_113, /* 优化 Pass 113 */
    OPT_OPT_PASS_114, /* 优化 Pass 114 */
    OPT_OPT_PASS_115, /* 优化 Pass 115 */
    OPT_OPT_PASS_116, /* 优化 Pass 116 */
    OPT_OPT_PASS_117, /* 优化 Pass 117 */
    OPT_OPT_PASS_118, /* 优化 Pass 118 */
    OPT_OPT_PASS_119, /* 优化 Pass 119 */
    OPT_OPT_PASS_120, /* 优化 Pass 120 */
    OPT_OPT_PASS_121, /* 优化 Pass 121 */
    OPT_OPT_PASS_122, /* 优化 Pass 122 */
    OPT_OPT_PASS_123, /* 优化 Pass 123 */
    OPT_OPT_PASS_124, /* 优化 Pass 124 */
    OPT_OPT_PASS_125, /* 优化 Pass 125 */
    OPT_OPT_PASS_126, /* 优化 Pass 126 */
    OPT_OPT_PASS_127, /* 优化 Pass 127 */
    OPT_OPT_PASS_128, /* 优化 Pass 128 */
    OPT_OPT_PASS_129, /* 优化 Pass 129 */
    OPT_OPT_PASS_130, /* 优化 Pass 130 */
    OPT_OPT_PASS_131, /* 优化 Pass 131 */
    OPT_OPT_PASS_132, /* 优化 Pass 132 */
    OPT_OPT_PASS_133, /* 优化 Pass 133 */
    OPT_OPT_PASS_134, /* 优化 Pass 134 */
    OPT_OPT_PASS_135, /* 优化 Pass 135 */
    OPT_OPT_PASS_136, /* 优化 Pass 136 */
    OPT_OPT_PASS_137, /* 优化 Pass 137 */
    OPT_OPT_PASS_138, /* 优化 Pass 138 */
    OPT_OPT_PASS_139, /* 优化 Pass 139 */
    OPT_OPT_PASS_140, /* 优化 Pass 140 */
    OPT_OPT_PASS_141, /* 优化 Pass 141 */
    OPT_OPT_PASS_142, /* 优化 Pass 142 */
    OPT_OPT_PASS_143, /* 优化 Pass 143 */
    OPT_OPT_PASS_144, /* 优化 Pass 144 */
    OPT_OPT_PASS_145, /* 优化 Pass 145 */
    OPT_OPT_PASS_146, /* 优化 Pass 146 */
    OPT_OPT_PASS_147, /* 优化 Pass 147 */
    OPT_OPT_PASS_148, /* 优化 Pass 148 */
    OPT_OPT_PASS_149, /* 优化 Pass 149 */
    OPT_OPT_PASS_150, /* 优化 Pass 150 */
    OPT_OPT_PASS_151, /* 优化 Pass 151 */
    OPT_OPT_PASS_152, /* 优化 Pass 152 */
    OPT_OPT_PASS_153, /* 优化 Pass 153 */
    OPT_OPT_PASS_154, /* 优化 Pass 154 */
    OPT_OPT_PASS_155, /* 优化 Pass 155 */
    OPT_OPT_PASS_156, /* 优化 Pass 156 */
    OPT_OPT_PASS_157, /* 优化 Pass 157 */
    OPT_OPT_PASS_158, /* 优化 Pass 158 */
    OPT_OPT_PASS_159, /* 优化 Pass 159 */
    OPT_OPT_PASS_160, /* 优化 Pass 160 */
    OPT_OPT_PASS_161, /* 优化 Pass 161 */
    OPT_OPT_PASS_162, /* 优化 Pass 162 */
    OPT_OPT_PASS_163, /* 优化 Pass 163 */
    OPT_OPT_PASS_164, /* 优化 Pass 164 */
    OPT_OPT_PASS_165, /* 优化 Pass 165 */
    OPT_OPT_PASS_166, /* 优化 Pass 166 */
    OPT_OPT_PASS_167, /* 优化 Pass 167 */
    OPT_OPT_PASS_168, /* 优化 Pass 168 */
    OPT_OPT_PASS_169, /* 优化 Pass 169 */
    OPT_OPT_PASS_170, /* 优化 Pass 170 */
    OPT_OPT_PASS_171, /* 优化 Pass 171 */
    OPT_OPT_PASS_172, /* 优化 Pass 172 */
    OPT_OPT_PASS_173, /* 优化 Pass 173 */
    OPT_OPT_PASS_174, /* 优化 Pass 174 */
    OPT_OPT_PASS_175, /* 优化 Pass 175 */
    OPT_OPT_PASS_176, /* 优化 Pass 176 */
    OPT_OPT_PASS_177, /* 优化 Pass 177 */
    OPT_OPT_PASS_178, /* 优化 Pass 178 */
    OPT_OPT_PASS_179, /* 优化 Pass 179 */
    OPT_OPT_PASS_180, /* 优化 Pass 180 */
    OPT_OPT_PASS_181, /* 优化 Pass 181 */
    OPT_OPT_PASS_182, /* 优化 Pass 182 */
    OPT_OPT_PASS_183, /* 优化 Pass 183 */
    OPT_OPT_PASS_184, /* 优化 Pass 184 */
    OPT_OPT_PASS_185, /* 优化 Pass 185 */
    OPT_OPT_PASS_186, /* 优化 Pass 186 */
    OPT_OPT_PASS_187, /* 优化 Pass 187 */
    OPT_OPT_PASS_188, /* 优化 Pass 188 */
    OPT_OPT_PASS_189, /* 优化 Pass 189 */
    OPT_OPT_PASS_190, /* 优化 Pass 190 */
    OPT_OPT_PASS_191, /* 优化 Pass 191 */
    OPT_OPT_PASS_192, /* 优化 Pass 192 */
    OPT_OPT_PASS_193, /* 优化 Pass 193 */
    OPT_OPT_PASS_194, /* 优化 Pass 194 */
    OPT_OPT_PASS_195, /* 优化 Pass 195 */
    OPT_OPT_PASS_196, /* 优化 Pass 196 */
    OPT_OPT_PASS_197, /* 优化 Pass 197 */
    OPT_OPT_PASS_198, /* 优化 Pass 198 */
    OPT_OPT_PASS_199, /* 优化 Pass 199 */
    OPT_PASS_COUNT
} OptPassType;

/* 优化 Pass 结构体 */
typedef struct OptPass {
    OptPassType type;
    const char* name;
    const char* description;
    int enabled;
    int level;
    int (*run)(IRModule* mod);
    int (*run_function)(IRFunction* func);
    int (*run_block)(IRBasicBlock* bb);
    void* data;
} OptPass;

/* 优化 Pass 管理器 */
typedef struct {
    OptPass** passes;
    int pass_count;
    int pass_capacity;
    int opt_level;
    int size_level;
    int debug_info;
    int time_passes;
    int verify_passes;
    int print_passes;
    int stats_passes;
} OptPassManager;

/* 函数声明 */
int opt_pass_000(IRModule* mod);
int opt_pass_000_function(IRFunction* func);
int opt_pass_000_block(IRBasicBlock* bb);
int opt_pass_001(IRModule* mod);
int opt_pass_001_function(IRFunction* func);
int opt_pass_001_block(IRBasicBlock* bb);
int opt_pass_002(IRModule* mod);
int opt_pass_002_function(IRFunction* func);
int opt_pass_002_block(IRBasicBlock* bb);
int opt_pass_003(IRModule* mod);
int opt_pass_003_function(IRFunction* func);
int opt_pass_003_block(IRBasicBlock* bb);
int opt_pass_004(IRModule* mod);
int opt_pass_004_function(IRFunction* func);
int opt_pass_004_block(IRBasicBlock* bb);
int opt_pass_005(IRModule* mod);
int opt_pass_005_function(IRFunction* func);
int opt_pass_005_block(IRBasicBlock* bb);
int opt_pass_006(IRModule* mod);
int opt_pass_006_function(IRFunction* func);
int opt_pass_006_block(IRBasicBlock* bb);
int opt_pass_007(IRModule* mod);
int opt_pass_007_function(IRFunction* func);
int opt_pass_007_block(IRBasicBlock* bb);
int opt_pass_008(IRModule* mod);
int opt_pass_008_function(IRFunction* func);
int opt_pass_008_block(IRBasicBlock* bb);
int opt_pass_009(IRModule* mod);
int opt_pass_009_function(IRFunction* func);
int opt_pass_009_block(IRBasicBlock* bb);
int opt_pass_010(IRModule* mod);
int opt_pass_010_function(IRFunction* func);
int opt_pass_010_block(IRBasicBlock* bb);
int opt_pass_011(IRModule* mod);
int opt_pass_011_function(IRFunction* func);
int opt_pass_011_block(IRBasicBlock* bb);
int opt_pass_012(IRModule* mod);
int opt_pass_012_function(IRFunction* func);
int opt_pass_012_block(IRBasicBlock* bb);
int opt_pass_013(IRModule* mod);
int opt_pass_013_function(IRFunction* func);
int opt_pass_013_block(IRBasicBlock* bb);
int opt_pass_014(IRModule* mod);
int opt_pass_014_function(IRFunction* func);
int opt_pass_014_block(IRBasicBlock* bb);
int opt_pass_015(IRModule* mod);
int opt_pass_015_function(IRFunction* func);
int opt_pass_015_block(IRBasicBlock* bb);
int opt_pass_016(IRModule* mod);
int opt_pass_016_function(IRFunction* func);
int opt_pass_016_block(IRBasicBlock* bb);
int opt_pass_017(IRModule* mod);
int opt_pass_017_function(IRFunction* func);
int opt_pass_017_block(IRBasicBlock* bb);
int opt_pass_018(IRModule* mod);
int opt_pass_018_function(IRFunction* func);
int opt_pass_018_block(IRBasicBlock* bb);
int opt_pass_019(IRModule* mod);
int opt_pass_019_function(IRFunction* func);
int opt_pass_019_block(IRBasicBlock* bb);
int opt_pass_020(IRModule* mod);
int opt_pass_020_function(IRFunction* func);
int opt_pass_020_block(IRBasicBlock* bb);
int opt_pass_021(IRModule* mod);
int opt_pass_021_function(IRFunction* func);
int opt_pass_021_block(IRBasicBlock* bb);
int opt_pass_022(IRModule* mod);
int opt_pass_022_function(IRFunction* func);
int opt_pass_022_block(IRBasicBlock* bb);
int opt_pass_023(IRModule* mod);
int opt_pass_023_function(IRFunction* func);
int opt_pass_023_block(IRBasicBlock* bb);
int opt_pass_024(IRModule* mod);
int opt_pass_024_function(IRFunction* func);
int opt_pass_024_block(IRBasicBlock* bb);
int opt_pass_025(IRModule* mod);
int opt_pass_025_function(IRFunction* func);
int opt_pass_025_block(IRBasicBlock* bb);
int opt_pass_026(IRModule* mod);
int opt_pass_026_function(IRFunction* func);
int opt_pass_026_block(IRBasicBlock* bb);
int opt_pass_027(IRModule* mod);
int opt_pass_027_function(IRFunction* func);
int opt_pass_027_block(IRBasicBlock* bb);
int opt_pass_028(IRModule* mod);
int opt_pass_028_function(IRFunction* func);
int opt_pass_028_block(IRBasicBlock* bb);
int opt_pass_029(IRModule* mod);
int opt_pass_029_function(IRFunction* func);
int opt_pass_029_block(IRBasicBlock* bb);
int opt_pass_030(IRModule* mod);
int opt_pass_030_function(IRFunction* func);
int opt_pass_030_block(IRBasicBlock* bb);
int opt_pass_031(IRModule* mod);
int opt_pass_031_function(IRFunction* func);
int opt_pass_031_block(IRBasicBlock* bb);
int opt_pass_032(IRModule* mod);
int opt_pass_032_function(IRFunction* func);
int opt_pass_032_block(IRBasicBlock* bb);
int opt_pass_033(IRModule* mod);
int opt_pass_033_function(IRFunction* func);
int opt_pass_033_block(IRBasicBlock* bb);
int opt_pass_034(IRModule* mod);
int opt_pass_034_function(IRFunction* func);
int opt_pass_034_block(IRBasicBlock* bb);
int opt_pass_035(IRModule* mod);
int opt_pass_035_function(IRFunction* func);
int opt_pass_035_block(IRBasicBlock* bb);
int opt_pass_036(IRModule* mod);
int opt_pass_036_function(IRFunction* func);
int opt_pass_036_block(IRBasicBlock* bb);
int opt_pass_037(IRModule* mod);
int opt_pass_037_function(IRFunction* func);
int opt_pass_037_block(IRBasicBlock* bb);
int opt_pass_038(IRModule* mod);
int opt_pass_038_function(IRFunction* func);
int opt_pass_038_block(IRBasicBlock* bb);
int opt_pass_039(IRModule* mod);
int opt_pass_039_function(IRFunction* func);
int opt_pass_039_block(IRBasicBlock* bb);
int opt_pass_040(IRModule* mod);
int opt_pass_040_function(IRFunction* func);
int opt_pass_040_block(IRBasicBlock* bb);
int opt_pass_041(IRModule* mod);
int opt_pass_041_function(IRFunction* func);
int opt_pass_041_block(IRBasicBlock* bb);
int opt_pass_042(IRModule* mod);
int opt_pass_042_function(IRFunction* func);
int opt_pass_042_block(IRBasicBlock* bb);
int opt_pass_043(IRModule* mod);
int opt_pass_043_function(IRFunction* func);
int opt_pass_043_block(IRBasicBlock* bb);
int opt_pass_044(IRModule* mod);
int opt_pass_044_function(IRFunction* func);
int opt_pass_044_block(IRBasicBlock* bb);
int opt_pass_045(IRModule* mod);
int opt_pass_045_function(IRFunction* func);
int opt_pass_045_block(IRBasicBlock* bb);
int opt_pass_046(IRModule* mod);
int opt_pass_046_function(IRFunction* func);
int opt_pass_046_block(IRBasicBlock* bb);
int opt_pass_047(IRModule* mod);
int opt_pass_047_function(IRFunction* func);
int opt_pass_047_block(IRBasicBlock* bb);
int opt_pass_048(IRModule* mod);
int opt_pass_048_function(IRFunction* func);
int opt_pass_048_block(IRBasicBlock* bb);
int opt_pass_049(IRModule* mod);
int opt_pass_049_function(IRFunction* func);
int opt_pass_049_block(IRBasicBlock* bb);
int opt_pass_050(IRModule* mod);
int opt_pass_050_function(IRFunction* func);
int opt_pass_050_block(IRBasicBlock* bb);
int opt_pass_051(IRModule* mod);
int opt_pass_051_function(IRFunction* func);
int opt_pass_051_block(IRBasicBlock* bb);
int opt_pass_052(IRModule* mod);
int opt_pass_052_function(IRFunction* func);
int opt_pass_052_block(IRBasicBlock* bb);
int opt_pass_053(IRModule* mod);
int opt_pass_053_function(IRFunction* func);
int opt_pass_053_block(IRBasicBlock* bb);
int opt_pass_054(IRModule* mod);
int opt_pass_054_function(IRFunction* func);
int opt_pass_054_block(IRBasicBlock* bb);
int opt_pass_055(IRModule* mod);
int opt_pass_055_function(IRFunction* func);
int opt_pass_055_block(IRBasicBlock* bb);
int opt_pass_056(IRModule* mod);
int opt_pass_056_function(IRFunction* func);
int opt_pass_056_block(IRBasicBlock* bb);
int opt_pass_057(IRModule* mod);
int opt_pass_057_function(IRFunction* func);
int opt_pass_057_block(IRBasicBlock* bb);
int opt_pass_058(IRModule* mod);
int opt_pass_058_function(IRFunction* func);
int opt_pass_058_block(IRBasicBlock* bb);
int opt_pass_059(IRModule* mod);
int opt_pass_059_function(IRFunction* func);
int opt_pass_059_block(IRBasicBlock* bb);
int opt_pass_060(IRModule* mod);
int opt_pass_060_function(IRFunction* func);
int opt_pass_060_block(IRBasicBlock* bb);
int opt_pass_061(IRModule* mod);
int opt_pass_061_function(IRFunction* func);
int opt_pass_061_block(IRBasicBlock* bb);
int opt_pass_062(IRModule* mod);
int opt_pass_062_function(IRFunction* func);
int opt_pass_062_block(IRBasicBlock* bb);
int opt_pass_063(IRModule* mod);
int opt_pass_063_function(IRFunction* func);
int opt_pass_063_block(IRBasicBlock* bb);
int opt_pass_064(IRModule* mod);
int opt_pass_064_function(IRFunction* func);
int opt_pass_064_block(IRBasicBlock* bb);
int opt_pass_065(IRModule* mod);
int opt_pass_065_function(IRFunction* func);
int opt_pass_065_block(IRBasicBlock* bb);
int opt_pass_066(IRModule* mod);
int opt_pass_066_function(IRFunction* func);
int opt_pass_066_block(IRBasicBlock* bb);
int opt_pass_067(IRModule* mod);
int opt_pass_067_function(IRFunction* func);
int opt_pass_067_block(IRBasicBlock* bb);
int opt_pass_068(IRModule* mod);
int opt_pass_068_function(IRFunction* func);
int opt_pass_068_block(IRBasicBlock* bb);
int opt_pass_069(IRModule* mod);
int opt_pass_069_function(IRFunction* func);
int opt_pass_069_block(IRBasicBlock* bb);
int opt_pass_070(IRModule* mod);
int opt_pass_070_function(IRFunction* func);
int opt_pass_070_block(IRBasicBlock* bb);
int opt_pass_071(IRModule* mod);
int opt_pass_071_function(IRFunction* func);
int opt_pass_071_block(IRBasicBlock* bb);
int opt_pass_072(IRModule* mod);
int opt_pass_072_function(IRFunction* func);
int opt_pass_072_block(IRBasicBlock* bb);
int opt_pass_073(IRModule* mod);
int opt_pass_073_function(IRFunction* func);
int opt_pass_073_block(IRBasicBlock* bb);
int opt_pass_074(IRModule* mod);
int opt_pass_074_function(IRFunction* func);
int opt_pass_074_block(IRBasicBlock* bb);
int opt_pass_075(IRModule* mod);
int opt_pass_075_function(IRFunction* func);
int opt_pass_075_block(IRBasicBlock* bb);
int opt_pass_076(IRModule* mod);
int opt_pass_076_function(IRFunction* func);
int opt_pass_076_block(IRBasicBlock* bb);
int opt_pass_077(IRModule* mod);
int opt_pass_077_function(IRFunction* func);
int opt_pass_077_block(IRBasicBlock* bb);
int opt_pass_078(IRModule* mod);
int opt_pass_078_function(IRFunction* func);
int opt_pass_078_block(IRBasicBlock* bb);
int opt_pass_079(IRModule* mod);
int opt_pass_079_function(IRFunction* func);
int opt_pass_079_block(IRBasicBlock* bb);
int opt_pass_080(IRModule* mod);
int opt_pass_080_function(IRFunction* func);
int opt_pass_080_block(IRBasicBlock* bb);
int opt_pass_081(IRModule* mod);
int opt_pass_081_function(IRFunction* func);
int opt_pass_081_block(IRBasicBlock* bb);
int opt_pass_082(IRModule* mod);
int opt_pass_082_function(IRFunction* func);
int opt_pass_082_block(IRBasicBlock* bb);
int opt_pass_083(IRModule* mod);
int opt_pass_083_function(IRFunction* func);
int opt_pass_083_block(IRBasicBlock* bb);
int opt_pass_084(IRModule* mod);
int opt_pass_084_function(IRFunction* func);
int opt_pass_084_block(IRBasicBlock* bb);
int opt_pass_085(IRModule* mod);
int opt_pass_085_function(IRFunction* func);
int opt_pass_085_block(IRBasicBlock* bb);
int opt_pass_086(IRModule* mod);
int opt_pass_086_function(IRFunction* func);
int opt_pass_086_block(IRBasicBlock* bb);
int opt_pass_087(IRModule* mod);
int opt_pass_087_function(IRFunction* func);
int opt_pass_087_block(IRBasicBlock* bb);
int opt_pass_088(IRModule* mod);
int opt_pass_088_function(IRFunction* func);
int opt_pass_088_block(IRBasicBlock* bb);
int opt_pass_089(IRModule* mod);
int opt_pass_089_function(IRFunction* func);
int opt_pass_089_block(IRBasicBlock* bb);
int opt_pass_090(IRModule* mod);
int opt_pass_090_function(IRFunction* func);
int opt_pass_090_block(IRBasicBlock* bb);
int opt_pass_091(IRModule* mod);
int opt_pass_091_function(IRFunction* func);
int opt_pass_091_block(IRBasicBlock* bb);
int opt_pass_092(IRModule* mod);
int opt_pass_092_function(IRFunction* func);
int opt_pass_092_block(IRBasicBlock* bb);
int opt_pass_093(IRModule* mod);
int opt_pass_093_function(IRFunction* func);
int opt_pass_093_block(IRBasicBlock* bb);
int opt_pass_094(IRModule* mod);
int opt_pass_094_function(IRFunction* func);
int opt_pass_094_block(IRBasicBlock* bb);
int opt_pass_095(IRModule* mod);
int opt_pass_095_function(IRFunction* func);
int opt_pass_095_block(IRBasicBlock* bb);
int opt_pass_096(IRModule* mod);
int opt_pass_096_function(IRFunction* func);
int opt_pass_096_block(IRBasicBlock* bb);
int opt_pass_097(IRModule* mod);
int opt_pass_097_function(IRFunction* func);
int opt_pass_097_block(IRBasicBlock* bb);
int opt_pass_098(IRModule* mod);
int opt_pass_098_function(IRFunction* func);
int opt_pass_098_block(IRBasicBlock* bb);
int opt_pass_099(IRModule* mod);
int opt_pass_099_function(IRFunction* func);
int opt_pass_099_block(IRBasicBlock* bb);
int opt_pass_100(IRModule* mod);
int opt_pass_100_function(IRFunction* func);
int opt_pass_100_block(IRBasicBlock* bb);
int opt_pass_101(IRModule* mod);
int opt_pass_101_function(IRFunction* func);
int opt_pass_101_block(IRBasicBlock* bb);
int opt_pass_102(IRModule* mod);
int opt_pass_102_function(IRFunction* func);
int opt_pass_102_block(IRBasicBlock* bb);
int opt_pass_103(IRModule* mod);
int opt_pass_103_function(IRFunction* func);
int opt_pass_103_block(IRBasicBlock* bb);
int opt_pass_104(IRModule* mod);
int opt_pass_104_function(IRFunction* func);
int opt_pass_104_block(IRBasicBlock* bb);
int opt_pass_105(IRModule* mod);
int opt_pass_105_function(IRFunction* func);
int opt_pass_105_block(IRBasicBlock* bb);
int opt_pass_106(IRModule* mod);
int opt_pass_106_function(IRFunction* func);
int opt_pass_106_block(IRBasicBlock* bb);
int opt_pass_107(IRModule* mod);
int opt_pass_107_function(IRFunction* func);
int opt_pass_107_block(IRBasicBlock* bb);
int opt_pass_108(IRModule* mod);
int opt_pass_108_function(IRFunction* func);
int opt_pass_108_block(IRBasicBlock* bb);
int opt_pass_109(IRModule* mod);
int opt_pass_109_function(IRFunction* func);
int opt_pass_109_block(IRBasicBlock* bb);
int opt_pass_110(IRModule* mod);
int opt_pass_110_function(IRFunction* func);
int opt_pass_110_block(IRBasicBlock* bb);
int opt_pass_111(IRModule* mod);
int opt_pass_111_function(IRFunction* func);
int opt_pass_111_block(IRBasicBlock* bb);
int opt_pass_112(IRModule* mod);
int opt_pass_112_function(IRFunction* func);
int opt_pass_112_block(IRBasicBlock* bb);
int opt_pass_113(IRModule* mod);
int opt_pass_113_function(IRFunction* func);
int opt_pass_113_block(IRBasicBlock* bb);
int opt_pass_114(IRModule* mod);
int opt_pass_114_function(IRFunction* func);
int opt_pass_114_block(IRBasicBlock* bb);
int opt_pass_115(IRModule* mod);
int opt_pass_115_function(IRFunction* func);
int opt_pass_115_block(IRBasicBlock* bb);
int opt_pass_116(IRModule* mod);
int opt_pass_116_function(IRFunction* func);
int opt_pass_116_block(IRBasicBlock* bb);
int opt_pass_117(IRModule* mod);
int opt_pass_117_function(IRFunction* func);
int opt_pass_117_block(IRBasicBlock* bb);
int opt_pass_118(IRModule* mod);
int opt_pass_118_function(IRFunction* func);
int opt_pass_118_block(IRBasicBlock* bb);
int opt_pass_119(IRModule* mod);
int opt_pass_119_function(IRFunction* func);
int opt_pass_119_block(IRBasicBlock* bb);
int opt_pass_120(IRModule* mod);
int opt_pass_120_function(IRFunction* func);
int opt_pass_120_block(IRBasicBlock* bb);
int opt_pass_121(IRModule* mod);
int opt_pass_121_function(IRFunction* func);
int opt_pass_121_block(IRBasicBlock* bb);
int opt_pass_122(IRModule* mod);
int opt_pass_122_function(IRFunction* func);
int opt_pass_122_block(IRBasicBlock* bb);
int opt_pass_123(IRModule* mod);
int opt_pass_123_function(IRFunction* func);
int opt_pass_123_block(IRBasicBlock* bb);
int opt_pass_124(IRModule* mod);
int opt_pass_124_function(IRFunction* func);
int opt_pass_124_block(IRBasicBlock* bb);
int opt_pass_125(IRModule* mod);
int opt_pass_125_function(IRFunction* func);
int opt_pass_125_block(IRBasicBlock* bb);
int opt_pass_126(IRModule* mod);
int opt_pass_126_function(IRFunction* func);
int opt_pass_126_block(IRBasicBlock* bb);
int opt_pass_127(IRModule* mod);
int opt_pass_127_function(IRFunction* func);
int opt_pass_127_block(IRBasicBlock* bb);
int opt_pass_128(IRModule* mod);
int opt_pass_128_function(IRFunction* func);
int opt_pass_128_block(IRBasicBlock* bb);
int opt_pass_129(IRModule* mod);
int opt_pass_129_function(IRFunction* func);
int opt_pass_129_block(IRBasicBlock* bb);
int opt_pass_130(IRModule* mod);
int opt_pass_130_function(IRFunction* func);
int opt_pass_130_block(IRBasicBlock* bb);
int opt_pass_131(IRModule* mod);
int opt_pass_131_function(IRFunction* func);
int opt_pass_131_block(IRBasicBlock* bb);
int opt_pass_132(IRModule* mod);
int opt_pass_132_function(IRFunction* func);
int opt_pass_132_block(IRBasicBlock* bb);
int opt_pass_133(IRModule* mod);
int opt_pass_133_function(IRFunction* func);
int opt_pass_133_block(IRBasicBlock* bb);
int opt_pass_134(IRModule* mod);
int opt_pass_134_function(IRFunction* func);
int opt_pass_134_block(IRBasicBlock* bb);
int opt_pass_135(IRModule* mod);
int opt_pass_135_function(IRFunction* func);
int opt_pass_135_block(IRBasicBlock* bb);
int opt_pass_136(IRModule* mod);
int opt_pass_136_function(IRFunction* func);
int opt_pass_136_block(IRBasicBlock* bb);
int opt_pass_137(IRModule* mod);
int opt_pass_137_function(IRFunction* func);
int opt_pass_137_block(IRBasicBlock* bb);
int opt_pass_138(IRModule* mod);
int opt_pass_138_function(IRFunction* func);
int opt_pass_138_block(IRBasicBlock* bb);
int opt_pass_139(IRModule* mod);
int opt_pass_139_function(IRFunction* func);
int opt_pass_139_block(IRBasicBlock* bb);
int opt_pass_140(IRModule* mod);
int opt_pass_140_function(IRFunction* func);
int opt_pass_140_block(IRBasicBlock* bb);
int opt_pass_141(IRModule* mod);
int opt_pass_141_function(IRFunction* func);
int opt_pass_141_block(IRBasicBlock* bb);
int opt_pass_142(IRModule* mod);
int opt_pass_142_function(IRFunction* func);
int opt_pass_142_block(IRBasicBlock* bb);
int opt_pass_143(IRModule* mod);
int opt_pass_143_function(IRFunction* func);
int opt_pass_143_block(IRBasicBlock* bb);
int opt_pass_144(IRModule* mod);
int opt_pass_144_function(IRFunction* func);
int opt_pass_144_block(IRBasicBlock* bb);
int opt_pass_145(IRModule* mod);
int opt_pass_145_function(IRFunction* func);
int opt_pass_145_block(IRBasicBlock* bb);
int opt_pass_146(IRModule* mod);
int opt_pass_146_function(IRFunction* func);
int opt_pass_146_block(IRBasicBlock* bb);
int opt_pass_147(IRModule* mod);
int opt_pass_147_function(IRFunction* func);
int opt_pass_147_block(IRBasicBlock* bb);
int opt_pass_148(IRModule* mod);
int opt_pass_148_function(IRFunction* func);
int opt_pass_148_block(IRBasicBlock* bb);
int opt_pass_149(IRModule* mod);
int opt_pass_149_function(IRFunction* func);
int opt_pass_149_block(IRBasicBlock* bb);
int opt_pass_150(IRModule* mod);
int opt_pass_150_function(IRFunction* func);
int opt_pass_150_block(IRBasicBlock* bb);
int opt_pass_151(IRModule* mod);
int opt_pass_151_function(IRFunction* func);
int opt_pass_151_block(IRBasicBlock* bb);
int opt_pass_152(IRModule* mod);
int opt_pass_152_function(IRFunction* func);
int opt_pass_152_block(IRBasicBlock* bb);
int opt_pass_153(IRModule* mod);
int opt_pass_153_function(IRFunction* func);
int opt_pass_153_block(IRBasicBlock* bb);
int opt_pass_154(IRModule* mod);
int opt_pass_154_function(IRFunction* func);
int opt_pass_154_block(IRBasicBlock* bb);
int opt_pass_155(IRModule* mod);
int opt_pass_155_function(IRFunction* func);
int opt_pass_155_block(IRBasicBlock* bb);
int opt_pass_156(IRModule* mod);
int opt_pass_156_function(IRFunction* func);
int opt_pass_156_block(IRBasicBlock* bb);
int opt_pass_157(IRModule* mod);
int opt_pass_157_function(IRFunction* func);
int opt_pass_157_block(IRBasicBlock* bb);
int opt_pass_158(IRModule* mod);
int opt_pass_158_function(IRFunction* func);
int opt_pass_158_block(IRBasicBlock* bb);
int opt_pass_159(IRModule* mod);
int opt_pass_159_function(IRFunction* func);
int opt_pass_159_block(IRBasicBlock* bb);
int opt_pass_160(IRModule* mod);
int opt_pass_160_function(IRFunction* func);
int opt_pass_160_block(IRBasicBlock* bb);
int opt_pass_161(IRModule* mod);
int opt_pass_161_function(IRFunction* func);
int opt_pass_161_block(IRBasicBlock* bb);
int opt_pass_162(IRModule* mod);
int opt_pass_162_function(IRFunction* func);
int opt_pass_162_block(IRBasicBlock* bb);
int opt_pass_163(IRModule* mod);
int opt_pass_163_function(IRFunction* func);
int opt_pass_163_block(IRBasicBlock* bb);
int opt_pass_164(IRModule* mod);
int opt_pass_164_function(IRFunction* func);
int opt_pass_164_block(IRBasicBlock* bb);
int opt_pass_165(IRModule* mod);
int opt_pass_165_function(IRFunction* func);
int opt_pass_165_block(IRBasicBlock* bb);
int opt_pass_166(IRModule* mod);
int opt_pass_166_function(IRFunction* func);
int opt_pass_166_block(IRBasicBlock* bb);
int opt_pass_167(IRModule* mod);
int opt_pass_167_function(IRFunction* func);
int opt_pass_167_block(IRBasicBlock* bb);
int opt_pass_168(IRModule* mod);
int opt_pass_168_function(IRFunction* func);
int opt_pass_168_block(IRBasicBlock* bb);
int opt_pass_169(IRModule* mod);
int opt_pass_169_function(IRFunction* func);
int opt_pass_169_block(IRBasicBlock* bb);
int opt_pass_170(IRModule* mod);
int opt_pass_170_function(IRFunction* func);
int opt_pass_170_block(IRBasicBlock* bb);
int opt_pass_171(IRModule* mod);
int opt_pass_171_function(IRFunction* func);
int opt_pass_171_block(IRBasicBlock* bb);
int opt_pass_172(IRModule* mod);
int opt_pass_172_function(IRFunction* func);
int opt_pass_172_block(IRBasicBlock* bb);
int opt_pass_173(IRModule* mod);
int opt_pass_173_function(IRFunction* func);
int opt_pass_173_block(IRBasicBlock* bb);
int opt_pass_174(IRModule* mod);
int opt_pass_174_function(IRFunction* func);
int opt_pass_174_block(IRBasicBlock* bb);
int opt_pass_175(IRModule* mod);
int opt_pass_175_function(IRFunction* func);
int opt_pass_175_block(IRBasicBlock* bb);
int opt_pass_176(IRModule* mod);
int opt_pass_176_function(IRFunction* func);
int opt_pass_176_block(IRBasicBlock* bb);
int opt_pass_177(IRModule* mod);
int opt_pass_177_function(IRFunction* func);
int opt_pass_177_block(IRBasicBlock* bb);
int opt_pass_178(IRModule* mod);
int opt_pass_178_function(IRFunction* func);
int opt_pass_178_block(IRBasicBlock* bb);
int opt_pass_179(IRModule* mod);
int opt_pass_179_function(IRFunction* func);
int opt_pass_179_block(IRBasicBlock* bb);
int opt_pass_180(IRModule* mod);
int opt_pass_180_function(IRFunction* func);
int opt_pass_180_block(IRBasicBlock* bb);
int opt_pass_181(IRModule* mod);
int opt_pass_181_function(IRFunction* func);
int opt_pass_181_block(IRBasicBlock* bb);
int opt_pass_182(IRModule* mod);
int opt_pass_182_function(IRFunction* func);
int opt_pass_182_block(IRBasicBlock* bb);
int opt_pass_183(IRModule* mod);
int opt_pass_183_function(IRFunction* func);
int opt_pass_183_block(IRBasicBlock* bb);
int opt_pass_184(IRModule* mod);
int opt_pass_184_function(IRFunction* func);
int opt_pass_184_block(IRBasicBlock* bb);
int opt_pass_185(IRModule* mod);
int opt_pass_185_function(IRFunction* func);
int opt_pass_185_block(IRBasicBlock* bb);
int opt_pass_186(IRModule* mod);
int opt_pass_186_function(IRFunction* func);
int opt_pass_186_block(IRBasicBlock* bb);
int opt_pass_187(IRModule* mod);
int opt_pass_187_function(IRFunction* func);
int opt_pass_187_block(IRBasicBlock* bb);
int opt_pass_188(IRModule* mod);
int opt_pass_188_function(IRFunction* func);
int opt_pass_188_block(IRBasicBlock* bb);
int opt_pass_189(IRModule* mod);
int opt_pass_189_function(IRFunction* func);
int opt_pass_189_block(IRBasicBlock* bb);
int opt_pass_190(IRModule* mod);
int opt_pass_190_function(IRFunction* func);
int opt_pass_190_block(IRBasicBlock* bb);
int opt_pass_191(IRModule* mod);
int opt_pass_191_function(IRFunction* func);
int opt_pass_191_block(IRBasicBlock* bb);
int opt_pass_192(IRModule* mod);
int opt_pass_192_function(IRFunction* func);
int opt_pass_192_block(IRBasicBlock* bb);
int opt_pass_193(IRModule* mod);
int opt_pass_193_function(IRFunction* func);
int opt_pass_193_block(IRBasicBlock* bb);
int opt_pass_194(IRModule* mod);
int opt_pass_194_function(IRFunction* func);
int opt_pass_194_block(IRBasicBlock* bb);
int opt_pass_195(IRModule* mod);
int opt_pass_195_function(IRFunction* func);
int opt_pass_195_block(IRBasicBlock* bb);
int opt_pass_196(IRModule* mod);
int opt_pass_196_function(IRFunction* func);
int opt_pass_196_block(IRBasicBlock* bb);
int opt_pass_197(IRModule* mod);
int opt_pass_197_function(IRFunction* func);
int opt_pass_197_block(IRBasicBlock* bb);
int opt_pass_198(IRModule* mod);
int opt_pass_198_function(IRFunction* func);
int opt_pass_198_block(IRBasicBlock* bb);
int opt_pass_199(IRModule* mod);
int opt_pass_199_function(IRFunction* func);
int opt_pass_199_block(IRBasicBlock* bb);
OptPassManager* opt_manager_create();
void opt_manager_destroy(OptPassManager* mgr);
void opt_manager_add_pass(OptPassManager* mgr, OptPassType type);
void opt_manager_remove_pass(OptPassManager* mgr, OptPassType type);
int opt_manager_run(OptPassManager* mgr, IRModule* mod);
void opt_manager_set_level(OptPassManager* mgr, int level);

#endif /* AURORA_OPT_H */