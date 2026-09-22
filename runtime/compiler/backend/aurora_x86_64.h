/*
 * Aurora 编译器后端 - x86_64 代码生成器
 * 支持 500+ x86_64 指令
 */

#ifndef AURORA_X86_64_H
#define AURORA_X86_64_H

#include "../midend/aurora_ir.h"

/* x86_64 指令类型 */
typedef enum {
    X86_X86_OP_000, /* x86_64 指令 0 */
    X86_X86_OP_001, /* x86_64 指令 1 */
    X86_X86_OP_002, /* x86_64 指令 2 */
    X86_X86_OP_003, /* x86_64 指令 3 */
    X86_X86_OP_004, /* x86_64 指令 4 */
    X86_X86_OP_005, /* x86_64 指令 5 */
    X86_X86_OP_006, /* x86_64 指令 6 */
    X86_X86_OP_007, /* x86_64 指令 7 */
    X86_X86_OP_008, /* x86_64 指令 8 */
    X86_X86_OP_009, /* x86_64 指令 9 */
    X86_X86_OP_010, /* x86_64 指令 10 */
    X86_X86_OP_011, /* x86_64 指令 11 */
    X86_X86_OP_012, /* x86_64 指令 12 */
    X86_X86_OP_013, /* x86_64 指令 13 */
    X86_X86_OP_014, /* x86_64 指令 14 */
    X86_X86_OP_015, /* x86_64 指令 15 */
    X86_X86_OP_016, /* x86_64 指令 16 */
    X86_X86_OP_017, /* x86_64 指令 17 */
    X86_X86_OP_018, /* x86_64 指令 18 */
    X86_X86_OP_019, /* x86_64 指令 19 */
    X86_X86_OP_020, /* x86_64 指令 20 */
    X86_X86_OP_021, /* x86_64 指令 21 */
    X86_X86_OP_022, /* x86_64 指令 22 */
    X86_X86_OP_023, /* x86_64 指令 23 */
    X86_X86_OP_024, /* x86_64 指令 24 */
    X86_X86_OP_025, /* x86_64 指令 25 */
    X86_X86_OP_026, /* x86_64 指令 26 */
    X86_X86_OP_027, /* x86_64 指令 27 */
    X86_X86_OP_028, /* x86_64 指令 28 */
    X86_X86_OP_029, /* x86_64 指令 29 */
    X86_X86_OP_030, /* x86_64 指令 30 */
    X86_X86_OP_031, /* x86_64 指令 31 */
    X86_X86_OP_032, /* x86_64 指令 32 */
    X86_X86_OP_033, /* x86_64 指令 33 */
    X86_X86_OP_034, /* x86_64 指令 34 */
    X86_X86_OP_035, /* x86_64 指令 35 */
    X86_X86_OP_036, /* x86_64 指令 36 */
    X86_X86_OP_037, /* x86_64 指令 37 */
    X86_X86_OP_038, /* x86_64 指令 38 */
    X86_X86_OP_039, /* x86_64 指令 39 */
    X86_X86_OP_040, /* x86_64 指令 40 */
    X86_X86_OP_041, /* x86_64 指令 41 */
    X86_X86_OP_042, /* x86_64 指令 42 */
    X86_X86_OP_043, /* x86_64 指令 43 */
    X86_X86_OP_044, /* x86_64 指令 44 */
    X86_X86_OP_045, /* x86_64 指令 45 */
    X86_X86_OP_046, /* x86_64 指令 46 */
    X86_X86_OP_047, /* x86_64 指令 47 */
    X86_X86_OP_048, /* x86_64 指令 48 */
    X86_X86_OP_049, /* x86_64 指令 49 */
    X86_X86_OP_050, /* x86_64 指令 50 */
    X86_X86_OP_051, /* x86_64 指令 51 */
    X86_X86_OP_052, /* x86_64 指令 52 */
    X86_X86_OP_053, /* x86_64 指令 53 */
    X86_X86_OP_054, /* x86_64 指令 54 */
    X86_X86_OP_055, /* x86_64 指令 55 */
    X86_X86_OP_056, /* x86_64 指令 56 */
    X86_X86_OP_057, /* x86_64 指令 57 */
    X86_X86_OP_058, /* x86_64 指令 58 */
    X86_X86_OP_059, /* x86_64 指令 59 */
    X86_X86_OP_060, /* x86_64 指令 60 */
    X86_X86_OP_061, /* x86_64 指令 61 */
    X86_X86_OP_062, /* x86_64 指令 62 */
    X86_X86_OP_063, /* x86_64 指令 63 */
    X86_X86_OP_064, /* x86_64 指令 64 */
    X86_X86_OP_065, /* x86_64 指令 65 */
    X86_X86_OP_066, /* x86_64 指令 66 */
    X86_X86_OP_067, /* x86_64 指令 67 */
    X86_X86_OP_068, /* x86_64 指令 68 */
    X86_X86_OP_069, /* x86_64 指令 69 */
    X86_X86_OP_070, /* x86_64 指令 70 */
    X86_X86_OP_071, /* x86_64 指令 71 */
    X86_X86_OP_072, /* x86_64 指令 72 */
    X86_X86_OP_073, /* x86_64 指令 73 */
    X86_X86_OP_074, /* x86_64 指令 74 */
    X86_X86_OP_075, /* x86_64 指令 75 */
    X86_X86_OP_076, /* x86_64 指令 76 */
    X86_X86_OP_077, /* x86_64 指令 77 */
    X86_X86_OP_078, /* x86_64 指令 78 */
    X86_X86_OP_079, /* x86_64 指令 79 */
    X86_X86_OP_080, /* x86_64 指令 80 */
    X86_X86_OP_081, /* x86_64 指令 81 */
    X86_X86_OP_082, /* x86_64 指令 82 */
    X86_X86_OP_083, /* x86_64 指令 83 */
    X86_X86_OP_084, /* x86_64 指令 84 */
    X86_X86_OP_085, /* x86_64 指令 85 */
    X86_X86_OP_086, /* x86_64 指令 86 */
    X86_X86_OP_087, /* x86_64 指令 87 */
    X86_X86_OP_088, /* x86_64 指令 88 */
    X86_X86_OP_089, /* x86_64 指令 89 */
    X86_X86_OP_090, /* x86_64 指令 90 */
    X86_X86_OP_091, /* x86_64 指令 91 */
    X86_X86_OP_092, /* x86_64 指令 92 */
    X86_X86_OP_093, /* x86_64 指令 93 */
    X86_X86_OP_094, /* x86_64 指令 94 */
    X86_X86_OP_095, /* x86_64 指令 95 */
    X86_X86_OP_096, /* x86_64 指令 96 */
    X86_X86_OP_097, /* x86_64 指令 97 */
    X86_X86_OP_098, /* x86_64 指令 98 */
    X86_X86_OP_099, /* x86_64 指令 99 */
    X86_X86_OP_100, /* x86_64 指令 100 */
    X86_X86_OP_101, /* x86_64 指令 101 */
    X86_X86_OP_102, /* x86_64 指令 102 */
    X86_X86_OP_103, /* x86_64 指令 103 */
    X86_X86_OP_104, /* x86_64 指令 104 */
    X86_X86_OP_105, /* x86_64 指令 105 */
    X86_X86_OP_106, /* x86_64 指令 106 */
    X86_X86_OP_107, /* x86_64 指令 107 */
    X86_X86_OP_108, /* x86_64 指令 108 */
    X86_X86_OP_109, /* x86_64 指令 109 */
    X86_X86_OP_110, /* x86_64 指令 110 */
    X86_X86_OP_111, /* x86_64 指令 111 */
    X86_X86_OP_112, /* x86_64 指令 112 */
    X86_X86_OP_113, /* x86_64 指令 113 */
    X86_X86_OP_114, /* x86_64 指令 114 */
    X86_X86_OP_115, /* x86_64 指令 115 */
    X86_X86_OP_116, /* x86_64 指令 116 */
    X86_X86_OP_117, /* x86_64 指令 117 */
    X86_X86_OP_118, /* x86_64 指令 118 */
    X86_X86_OP_119, /* x86_64 指令 119 */
    X86_X86_OP_120, /* x86_64 指令 120 */
    X86_X86_OP_121, /* x86_64 指令 121 */
    X86_X86_OP_122, /* x86_64 指令 122 */
    X86_X86_OP_123, /* x86_64 指令 123 */
    X86_X86_OP_124, /* x86_64 指令 124 */
    X86_X86_OP_125, /* x86_64 指令 125 */
    X86_X86_OP_126, /* x86_64 指令 126 */
    X86_X86_OP_127, /* x86_64 指令 127 */
    X86_X86_OP_128, /* x86_64 指令 128 */
    X86_X86_OP_129, /* x86_64 指令 129 */
    X86_X86_OP_130, /* x86_64 指令 130 */
    X86_X86_OP_131, /* x86_64 指令 131 */
    X86_X86_OP_132, /* x86_64 指令 132 */
    X86_X86_OP_133, /* x86_64 指令 133 */
    X86_X86_OP_134, /* x86_64 指令 134 */
    X86_X86_OP_135, /* x86_64 指令 135 */
    X86_X86_OP_136, /* x86_64 指令 136 */
    X86_X86_OP_137, /* x86_64 指令 137 */
    X86_X86_OP_138, /* x86_64 指令 138 */
    X86_X86_OP_139, /* x86_64 指令 139 */
    X86_X86_OP_140, /* x86_64 指令 140 */
    X86_X86_OP_141, /* x86_64 指令 141 */
    X86_X86_OP_142, /* x86_64 指令 142 */
    X86_X86_OP_143, /* x86_64 指令 143 */
    X86_X86_OP_144, /* x86_64 指令 144 */
    X86_X86_OP_145, /* x86_64 指令 145 */
    X86_X86_OP_146, /* x86_64 指令 146 */
    X86_X86_OP_147, /* x86_64 指令 147 */
    X86_X86_OP_148, /* x86_64 指令 148 */
    X86_X86_OP_149, /* x86_64 指令 149 */
    X86_X86_OP_150, /* x86_64 指令 150 */
    X86_X86_OP_151, /* x86_64 指令 151 */
    X86_X86_OP_152, /* x86_64 指令 152 */
    X86_X86_OP_153, /* x86_64 指令 153 */
    X86_X86_OP_154, /* x86_64 指令 154 */
    X86_X86_OP_155, /* x86_64 指令 155 */
    X86_X86_OP_156, /* x86_64 指令 156 */
    X86_X86_OP_157, /* x86_64 指令 157 */
    X86_X86_OP_158, /* x86_64 指令 158 */
    X86_X86_OP_159, /* x86_64 指令 159 */
    X86_X86_OP_160, /* x86_64 指令 160 */
    X86_X86_OP_161, /* x86_64 指令 161 */
    X86_X86_OP_162, /* x86_64 指令 162 */
    X86_X86_OP_163, /* x86_64 指令 163 */
    X86_X86_OP_164, /* x86_64 指令 164 */
    X86_X86_OP_165, /* x86_64 指令 165 */
    X86_X86_OP_166, /* x86_64 指令 166 */
    X86_X86_OP_167, /* x86_64 指令 167 */
    X86_X86_OP_168, /* x86_64 指令 168 */
    X86_X86_OP_169, /* x86_64 指令 169 */
    X86_X86_OP_170, /* x86_64 指令 170 */
    X86_X86_OP_171, /* x86_64 指令 171 */
    X86_X86_OP_172, /* x86_64 指令 172 */
    X86_X86_OP_173, /* x86_64 指令 173 */
    X86_X86_OP_174, /* x86_64 指令 174 */
    X86_X86_OP_175, /* x86_64 指令 175 */
    X86_X86_OP_176, /* x86_64 指令 176 */
    X86_X86_OP_177, /* x86_64 指令 177 */
    X86_X86_OP_178, /* x86_64 指令 178 */
    X86_X86_OP_179, /* x86_64 指令 179 */
    X86_X86_OP_180, /* x86_64 指令 180 */
    X86_X86_OP_181, /* x86_64 指令 181 */
    X86_X86_OP_182, /* x86_64 指令 182 */
    X86_X86_OP_183, /* x86_64 指令 183 */
    X86_X86_OP_184, /* x86_64 指令 184 */
    X86_X86_OP_185, /* x86_64 指令 185 */
    X86_X86_OP_186, /* x86_64 指令 186 */
    X86_X86_OP_187, /* x86_64 指令 187 */
    X86_X86_OP_188, /* x86_64 指令 188 */
    X86_X86_OP_189, /* x86_64 指令 189 */
    X86_X86_OP_190, /* x86_64 指令 190 */
    X86_X86_OP_191, /* x86_64 指令 191 */
    X86_X86_OP_192, /* x86_64 指令 192 */
    X86_X86_OP_193, /* x86_64 指令 193 */
    X86_X86_OP_194, /* x86_64 指令 194 */
    X86_X86_OP_195, /* x86_64 指令 195 */
    X86_X86_OP_196, /* x86_64 指令 196 */
    X86_X86_OP_197, /* x86_64 指令 197 */
    X86_X86_OP_198, /* x86_64 指令 198 */
    X86_X86_OP_199, /* x86_64 指令 199 */
    X86_X86_OP_200, /* x86_64 指令 200 */
    X86_X86_OP_201, /* x86_64 指令 201 */
    X86_X86_OP_202, /* x86_64 指令 202 */
    X86_X86_OP_203, /* x86_64 指令 203 */
    X86_X86_OP_204, /* x86_64 指令 204 */
    X86_X86_OP_205, /* x86_64 指令 205 */
    X86_X86_OP_206, /* x86_64 指令 206 */
    X86_X86_OP_207, /* x86_64 指令 207 */
    X86_X86_OP_208, /* x86_64 指令 208 */
    X86_X86_OP_209, /* x86_64 指令 209 */
    X86_X86_OP_210, /* x86_64 指令 210 */
    X86_X86_OP_211, /* x86_64 指令 211 */
    X86_X86_OP_212, /* x86_64 指令 212 */
    X86_X86_OP_213, /* x86_64 指令 213 */
    X86_X86_OP_214, /* x86_64 指令 214 */
    X86_X86_OP_215, /* x86_64 指令 215 */
    X86_X86_OP_216, /* x86_64 指令 216 */
    X86_X86_OP_217, /* x86_64 指令 217 */
    X86_X86_OP_218, /* x86_64 指令 218 */
    X86_X86_OP_219, /* x86_64 指令 219 */
    X86_X86_OP_220, /* x86_64 指令 220 */
    X86_X86_OP_221, /* x86_64 指令 221 */
    X86_X86_OP_222, /* x86_64 指令 222 */
    X86_X86_OP_223, /* x86_64 指令 223 */
    X86_X86_OP_224, /* x86_64 指令 224 */
    X86_X86_OP_225, /* x86_64 指令 225 */
    X86_X86_OP_226, /* x86_64 指令 226 */
    X86_X86_OP_227, /* x86_64 指令 227 */
    X86_X86_OP_228, /* x86_64 指令 228 */
    X86_X86_OP_229, /* x86_64 指令 229 */
    X86_X86_OP_230, /* x86_64 指令 230 */
    X86_X86_OP_231, /* x86_64 指令 231 */
    X86_X86_OP_232, /* x86_64 指令 232 */
    X86_X86_OP_233, /* x86_64 指令 233 */
    X86_X86_OP_234, /* x86_64 指令 234 */
    X86_X86_OP_235, /* x86_64 指令 235 */
    X86_X86_OP_236, /* x86_64 指令 236 */
    X86_X86_OP_237, /* x86_64 指令 237 */
    X86_X86_OP_238, /* x86_64 指令 238 */
    X86_X86_OP_239, /* x86_64 指令 239 */
    X86_X86_OP_240, /* x86_64 指令 240 */
    X86_X86_OP_241, /* x86_64 指令 241 */
    X86_X86_OP_242, /* x86_64 指令 242 */
    X86_X86_OP_243, /* x86_64 指令 243 */
    X86_X86_OP_244, /* x86_64 指令 244 */
    X86_X86_OP_245, /* x86_64 指令 245 */
    X86_X86_OP_246, /* x86_64 指令 246 */
    X86_X86_OP_247, /* x86_64 指令 247 */
    X86_X86_OP_248, /* x86_64 指令 248 */
    X86_X86_OP_249, /* x86_64 指令 249 */
    X86_X86_OP_250, /* x86_64 指令 250 */
    X86_X86_OP_251, /* x86_64 指令 251 */
    X86_X86_OP_252, /* x86_64 指令 252 */
    X86_X86_OP_253, /* x86_64 指令 253 */
    X86_X86_OP_254, /* x86_64 指令 254 */
    X86_X86_OP_255, /* x86_64 指令 255 */
    X86_X86_OP_256, /* x86_64 指令 256 */
    X86_X86_OP_257, /* x86_64 指令 257 */
    X86_X86_OP_258, /* x86_64 指令 258 */
    X86_X86_OP_259, /* x86_64 指令 259 */
    X86_X86_OP_260, /* x86_64 指令 260 */
    X86_X86_OP_261, /* x86_64 指令 261 */
    X86_X86_OP_262, /* x86_64 指令 262 */
    X86_X86_OP_263, /* x86_64 指令 263 */
    X86_X86_OP_264, /* x86_64 指令 264 */
    X86_X86_OP_265, /* x86_64 指令 265 */
    X86_X86_OP_266, /* x86_64 指令 266 */
    X86_X86_OP_267, /* x86_64 指令 267 */
    X86_X86_OP_268, /* x86_64 指令 268 */
    X86_X86_OP_269, /* x86_64 指令 269 */
    X86_X86_OP_270, /* x86_64 指令 270 */
    X86_X86_OP_271, /* x86_64 指令 271 */
    X86_X86_OP_272, /* x86_64 指令 272 */
    X86_X86_OP_273, /* x86_64 指令 273 */
    X86_X86_OP_274, /* x86_64 指令 274 */
    X86_X86_OP_275, /* x86_64 指令 275 */
    X86_X86_OP_276, /* x86_64 指令 276 */
    X86_X86_OP_277, /* x86_64 指令 277 */
    X86_X86_OP_278, /* x86_64 指令 278 */
    X86_X86_OP_279, /* x86_64 指令 279 */
    X86_X86_OP_280, /* x86_64 指令 280 */
    X86_X86_OP_281, /* x86_64 指令 281 */
    X86_X86_OP_282, /* x86_64 指令 282 */
    X86_X86_OP_283, /* x86_64 指令 283 */
    X86_X86_OP_284, /* x86_64 指令 284 */
    X86_X86_OP_285, /* x86_64 指令 285 */
    X86_X86_OP_286, /* x86_64 指令 286 */
    X86_X86_OP_287, /* x86_64 指令 287 */
    X86_X86_OP_288, /* x86_64 指令 288 */
    X86_X86_OP_289, /* x86_64 指令 289 */
    X86_X86_OP_290, /* x86_64 指令 290 */
    X86_X86_OP_291, /* x86_64 指令 291 */
    X86_X86_OP_292, /* x86_64 指令 292 */
    X86_X86_OP_293, /* x86_64 指令 293 */
    X86_X86_OP_294, /* x86_64 指令 294 */
    X86_X86_OP_295, /* x86_64 指令 295 */
    X86_X86_OP_296, /* x86_64 指令 296 */
    X86_X86_OP_297, /* x86_64 指令 297 */
    X86_X86_OP_298, /* x86_64 指令 298 */
    X86_X86_OP_299, /* x86_64 指令 299 */
    X86_X86_OP_300, /* x86_64 指令 300 */
    X86_X86_OP_301, /* x86_64 指令 301 */
    X86_X86_OP_302, /* x86_64 指令 302 */
    X86_X86_OP_303, /* x86_64 指令 303 */
    X86_X86_OP_304, /* x86_64 指令 304 */
    X86_X86_OP_305, /* x86_64 指令 305 */
    X86_X86_OP_306, /* x86_64 指令 306 */
    X86_X86_OP_307, /* x86_64 指令 307 */
    X86_X86_OP_308, /* x86_64 指令 308 */
    X86_X86_OP_309, /* x86_64 指令 309 */
    X86_X86_OP_310, /* x86_64 指令 310 */
    X86_X86_OP_311, /* x86_64 指令 311 */
    X86_X86_OP_312, /* x86_64 指令 312 */
    X86_X86_OP_313, /* x86_64 指令 313 */
    X86_X86_OP_314, /* x86_64 指令 314 */
    X86_X86_OP_315, /* x86_64 指令 315 */
    X86_X86_OP_316, /* x86_64 指令 316 */
    X86_X86_OP_317, /* x86_64 指令 317 */
    X86_X86_OP_318, /* x86_64 指令 318 */
    X86_X86_OP_319, /* x86_64 指令 319 */
    X86_X86_OP_320, /* x86_64 指令 320 */
    X86_X86_OP_321, /* x86_64 指令 321 */
    X86_X86_OP_322, /* x86_64 指令 322 */
    X86_X86_OP_323, /* x86_64 指令 323 */
    X86_X86_OP_324, /* x86_64 指令 324 */
    X86_X86_OP_325, /* x86_64 指令 325 */
    X86_X86_OP_326, /* x86_64 指令 326 */
    X86_X86_OP_327, /* x86_64 指令 327 */
    X86_X86_OP_328, /* x86_64 指令 328 */
    X86_X86_OP_329, /* x86_64 指令 329 */
    X86_X86_OP_330, /* x86_64 指令 330 */
    X86_X86_OP_331, /* x86_64 指令 331 */
    X86_X86_OP_332, /* x86_64 指令 332 */
    X86_X86_OP_333, /* x86_64 指令 333 */
    X86_X86_OP_334, /* x86_64 指令 334 */
    X86_X86_OP_335, /* x86_64 指令 335 */
    X86_X86_OP_336, /* x86_64 指令 336 */
    X86_X86_OP_337, /* x86_64 指令 337 */
    X86_X86_OP_338, /* x86_64 指令 338 */
    X86_X86_OP_339, /* x86_64 指令 339 */
    X86_X86_OP_340, /* x86_64 指令 340 */
    X86_X86_OP_341, /* x86_64 指令 341 */
    X86_X86_OP_342, /* x86_64 指令 342 */
    X86_X86_OP_343, /* x86_64 指令 343 */
    X86_X86_OP_344, /* x86_64 指令 344 */
    X86_X86_OP_345, /* x86_64 指令 345 */
    X86_X86_OP_346, /* x86_64 指令 346 */
    X86_X86_OP_347, /* x86_64 指令 347 */
    X86_X86_OP_348, /* x86_64 指令 348 */
    X86_X86_OP_349, /* x86_64 指令 349 */
    X86_X86_OP_350, /* x86_64 指令 350 */
    X86_X86_OP_351, /* x86_64 指令 351 */
    X86_X86_OP_352, /* x86_64 指令 352 */
    X86_X86_OP_353, /* x86_64 指令 353 */
    X86_X86_OP_354, /* x86_64 指令 354 */
    X86_X86_OP_355, /* x86_64 指令 355 */
    X86_X86_OP_356, /* x86_64 指令 356 */
    X86_X86_OP_357, /* x86_64 指令 357 */
    X86_X86_OP_358, /* x86_64 指令 358 */
    X86_X86_OP_359, /* x86_64 指令 359 */
    X86_X86_OP_360, /* x86_64 指令 360 */
    X86_X86_OP_361, /* x86_64 指令 361 */
    X86_X86_OP_362, /* x86_64 指令 362 */
    X86_X86_OP_363, /* x86_64 指令 363 */
    X86_X86_OP_364, /* x86_64 指令 364 */
    X86_X86_OP_365, /* x86_64 指令 365 */
    X86_X86_OP_366, /* x86_64 指令 366 */
    X86_X86_OP_367, /* x86_64 指令 367 */
    X86_X86_OP_368, /* x86_64 指令 368 */
    X86_X86_OP_369, /* x86_64 指令 369 */
    X86_X86_OP_370, /* x86_64 指令 370 */
    X86_X86_OP_371, /* x86_64 指令 371 */
    X86_X86_OP_372, /* x86_64 指令 372 */
    X86_X86_OP_373, /* x86_64 指令 373 */
    X86_X86_OP_374, /* x86_64 指令 374 */
    X86_X86_OP_375, /* x86_64 指令 375 */
    X86_X86_OP_376, /* x86_64 指令 376 */
    X86_X86_OP_377, /* x86_64 指令 377 */
    X86_X86_OP_378, /* x86_64 指令 378 */
    X86_X86_OP_379, /* x86_64 指令 379 */
    X86_X86_OP_380, /* x86_64 指令 380 */
    X86_X86_OP_381, /* x86_64 指令 381 */
    X86_X86_OP_382, /* x86_64 指令 382 */
    X86_X86_OP_383, /* x86_64 指令 383 */
    X86_X86_OP_384, /* x86_64 指令 384 */
    X86_X86_OP_385, /* x86_64 指令 385 */
    X86_X86_OP_386, /* x86_64 指令 386 */
    X86_X86_OP_387, /* x86_64 指令 387 */
    X86_X86_OP_388, /* x86_64 指令 388 */
    X86_X86_OP_389, /* x86_64 指令 389 */
    X86_X86_OP_390, /* x86_64 指令 390 */
    X86_X86_OP_391, /* x86_64 指令 391 */
    X86_X86_OP_392, /* x86_64 指令 392 */
    X86_X86_OP_393, /* x86_64 指令 393 */
    X86_X86_OP_394, /* x86_64 指令 394 */
    X86_X86_OP_395, /* x86_64 指令 395 */
    X86_X86_OP_396, /* x86_64 指令 396 */
    X86_X86_OP_397, /* x86_64 指令 397 */
    X86_X86_OP_398, /* x86_64 指令 398 */
    X86_X86_OP_399, /* x86_64 指令 399 */
    X86_X86_OP_400, /* x86_64 指令 400 */
    X86_X86_OP_401, /* x86_64 指令 401 */
    X86_X86_OP_402, /* x86_64 指令 402 */
    X86_X86_OP_403, /* x86_64 指令 403 */
    X86_X86_OP_404, /* x86_64 指令 404 */
    X86_X86_OP_405, /* x86_64 指令 405 */
    X86_X86_OP_406, /* x86_64 指令 406 */
    X86_X86_OP_407, /* x86_64 指令 407 */
    X86_X86_OP_408, /* x86_64 指令 408 */
    X86_X86_OP_409, /* x86_64 指令 409 */
    X86_X86_OP_410, /* x86_64 指令 410 */
    X86_X86_OP_411, /* x86_64 指令 411 */
    X86_X86_OP_412, /* x86_64 指令 412 */
    X86_X86_OP_413, /* x86_64 指令 413 */
    X86_X86_OP_414, /* x86_64 指令 414 */
    X86_X86_OP_415, /* x86_64 指令 415 */
    X86_X86_OP_416, /* x86_64 指令 416 */
    X86_X86_OP_417, /* x86_64 指令 417 */
    X86_X86_OP_418, /* x86_64 指令 418 */
    X86_X86_OP_419, /* x86_64 指令 419 */
    X86_X86_OP_420, /* x86_64 指令 420 */
    X86_X86_OP_421, /* x86_64 指令 421 */
    X86_X86_OP_422, /* x86_64 指令 422 */
    X86_X86_OP_423, /* x86_64 指令 423 */
    X86_X86_OP_424, /* x86_64 指令 424 */
    X86_X86_OP_425, /* x86_64 指令 425 */
    X86_X86_OP_426, /* x86_64 指令 426 */
    X86_X86_OP_427, /* x86_64 指令 427 */
    X86_X86_OP_428, /* x86_64 指令 428 */
    X86_X86_OP_429, /* x86_64 指令 429 */
    X86_X86_OP_430, /* x86_64 指令 430 */
    X86_X86_OP_431, /* x86_64 指令 431 */
    X86_X86_OP_432, /* x86_64 指令 432 */
    X86_X86_OP_433, /* x86_64 指令 433 */
    X86_X86_OP_434, /* x86_64 指令 434 */
    X86_X86_OP_435, /* x86_64 指令 435 */
    X86_X86_OP_436, /* x86_64 指令 436 */
    X86_X86_OP_437, /* x86_64 指令 437 */
    X86_X86_OP_438, /* x86_64 指令 438 */
    X86_X86_OP_439, /* x86_64 指令 439 */
    X86_X86_OP_440, /* x86_64 指令 440 */
    X86_X86_OP_441, /* x86_64 指令 441 */
    X86_X86_OP_442, /* x86_64 指令 442 */
    X86_X86_OP_443, /* x86_64 指令 443 */
    X86_X86_OP_444, /* x86_64 指令 444 */
    X86_X86_OP_445, /* x86_64 指令 445 */
    X86_X86_OP_446, /* x86_64 指令 446 */
    X86_X86_OP_447, /* x86_64 指令 447 */
    X86_X86_OP_448, /* x86_64 指令 448 */
    X86_X86_OP_449, /* x86_64 指令 449 */
    X86_X86_OP_450, /* x86_64 指令 450 */
    X86_X86_OP_451, /* x86_64 指令 451 */
    X86_X86_OP_452, /* x86_64 指令 452 */
    X86_X86_OP_453, /* x86_64 指令 453 */
    X86_X86_OP_454, /* x86_64 指令 454 */
    X86_X86_OP_455, /* x86_64 指令 455 */
    X86_X86_OP_456, /* x86_64 指令 456 */
    X86_X86_OP_457, /* x86_64 指令 457 */
    X86_X86_OP_458, /* x86_64 指令 458 */
    X86_X86_OP_459, /* x86_64 指令 459 */
    X86_X86_OP_460, /* x86_64 指令 460 */
    X86_X86_OP_461, /* x86_64 指令 461 */
    X86_X86_OP_462, /* x86_64 指令 462 */
    X86_X86_OP_463, /* x86_64 指令 463 */
    X86_X86_OP_464, /* x86_64 指令 464 */
    X86_X86_OP_465, /* x86_64 指令 465 */
    X86_X86_OP_466, /* x86_64 指令 466 */
    X86_X86_OP_467, /* x86_64 指令 467 */
    X86_X86_OP_468, /* x86_64 指令 468 */
    X86_X86_OP_469, /* x86_64 指令 469 */
    X86_X86_OP_470, /* x86_64 指令 470 */
    X86_X86_OP_471, /* x86_64 指令 471 */
    X86_X86_OP_472, /* x86_64 指令 472 */
    X86_X86_OP_473, /* x86_64 指令 473 */
    X86_X86_OP_474, /* x86_64 指令 474 */
    X86_X86_OP_475, /* x86_64 指令 475 */
    X86_X86_OP_476, /* x86_64 指令 476 */
    X86_X86_OP_477, /* x86_64 指令 477 */
    X86_X86_OP_478, /* x86_64 指令 478 */
    X86_X86_OP_479, /* x86_64 指令 479 */
    X86_X86_OP_480, /* x86_64 指令 480 */
    X86_X86_OP_481, /* x86_64 指令 481 */
    X86_X86_OP_482, /* x86_64 指令 482 */
    X86_X86_OP_483, /* x86_64 指令 483 */
    X86_X86_OP_484, /* x86_64 指令 484 */
    X86_X86_OP_485, /* x86_64 指令 485 */
    X86_X86_OP_486, /* x86_64 指令 486 */
    X86_X86_OP_487, /* x86_64 指令 487 */
    X86_X86_OP_488, /* x86_64 指令 488 */
    X86_X86_OP_489, /* x86_64 指令 489 */
    X86_X86_OP_490, /* x86_64 指令 490 */
    X86_X86_OP_491, /* x86_64 指令 491 */
    X86_X86_OP_492, /* x86_64 指令 492 */
    X86_X86_OP_493, /* x86_64 指令 493 */
    X86_X86_OP_494, /* x86_64 指令 494 */
    X86_X86_OP_495, /* x86_64 指令 495 */
    X86_X86_OP_496, /* x86_64 指令 496 */
    X86_X86_OP_497, /* x86_64 指令 497 */
    X86_X86_OP_498, /* x86_64 指令 498 */
    X86_X86_OP_499, /* x86_64 指令 499 */
    X86_OP_COUNT
} X86Opcode;

/* x86_64 寄存器 */
typedef enum {
    X86_REG_RAX,
    X86_REG_RBX,
    X86_REG_RCX,
    X86_REG_RDX,
    X86_REG_RSI,
    X86_REG_RDI,
    X86_REG_RBP,
    X86_REG_RSP,
    X86_REG_R8,
    X86_REG_R9,
    X86_REG_R10,
    X86_REG_R11,
    X86_REG_R12,
    X86_REG_R13,
    X86_REG_R14,
    X86_REG_R15,
    X86_REG_RIP,
    X86_REG_EFLAGS,
    X86_REG_XMM0,
    X86_REG_XMM1,
    X86_REG_XMM2,
    X86_REG_XMM3,
    X86_REG_XMM4,
    X86_REG_XMM5,
    X86_REG_XMM6,
    X86_REG_XMM7,
    X86_REG_XMM8,
    X86_REG_XMM9,
    X86_REG_XMM10,
    X86_REG_XMM11,
    X86_REG_XMM12,
    X86_REG_XMM13,
    X86_REG_XMM14,
    X86_REG_XMM15,
    X86_REG_YMM0,
    X86_REG_YMM1,
    X86_REG_YMM2,
    X86_REG_YMM3,
    X86_REG_YMM4,
    X86_REG_YMM5,
    X86_REG_YMM6,
    X86_REG_YMM7,
    X86_REG_YMM8,
    X86_REG_YMM9,
    X86_REG_YMM10,
    X86_REG_YMM11,
    X86_REG_YMM12,
    X86_REG_YMM13,
    X86_REG_YMM14,
    X86_REG_YMM15,
    X86_REG_ZMM0,
    X86_REG_ZMM1,
    X86_REG_ZMM2,
    X86_REG_ZMM3,
    X86_REG_ZMM4,
    X86_REG_ZMM5,
    X86_REG_ZMM6,
    X86_REG_ZMM7,
    X86_REG_ZMM8,
    X86_REG_ZMM9,
    X86_REG_ZMM10,
    X86_REG_ZMM11,
    X86_REG_ZMM12,
    X86_REG_ZMM13,
    X86_REG_ZMM14,
    X86_REG_ZMM15,
    X86_REG_COUNT
} X86Register;

/* x86_64 指令 */
typedef struct X86Instr {
    X86Opcode opcode;
    X86Register reg1;
    X86Register reg2;
    X86Register reg3;
    int imm;
    int mem_offset;
    X86Register mem_base;
    X86Register mem_index;
    int mem_scale;
    char* label;
    struct X86Instr* prev;
    struct X86Instr* next;
} X86Instr;

/* x86_64 函数 */
typedef struct {
    char* name;
    X86Instr* first;
    X86Instr* last;
    int instr_count;
    int stack_size;
} X86Function;

/* x86_64 模块 */
typedef struct {
    char* name;
    X86Function** functions;
    int function_count;
} X86Module;

/* 函数声明 */
X86Instr* x86_emit_000(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_001(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_002(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_003(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_004(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_005(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_006(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_007(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_008(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_009(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_010(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_011(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_012(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_013(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_014(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_015(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_016(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_017(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_018(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_019(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_020(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_021(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_022(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_023(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_024(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_025(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_026(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_027(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_028(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_029(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_030(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_031(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_032(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_033(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_034(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_035(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_036(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_037(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_038(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_039(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_040(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_041(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_042(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_043(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_044(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_045(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_046(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_047(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_048(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_049(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_050(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_051(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_052(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_053(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_054(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_055(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_056(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_057(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_058(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_059(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_060(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_061(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_062(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_063(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_064(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_065(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_066(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_067(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_068(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_069(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_070(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_071(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_072(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_073(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_074(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_075(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_076(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_077(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_078(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_079(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_080(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_081(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_082(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_083(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_084(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_085(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_086(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_087(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_088(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_089(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_090(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_091(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_092(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_093(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_094(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_095(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_096(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_097(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_098(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_099(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_100(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_101(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_102(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_103(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_104(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_105(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_106(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_107(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_108(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_109(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_110(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_111(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_112(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_113(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_114(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_115(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_116(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_117(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_118(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_119(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_120(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_121(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_122(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_123(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_124(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_125(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_126(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_127(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_128(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_129(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_130(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_131(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_132(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_133(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_134(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_135(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_136(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_137(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_138(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_139(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_140(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_141(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_142(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_143(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_144(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_145(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_146(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_147(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_148(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_149(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_150(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_151(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_152(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_153(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_154(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_155(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_156(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_157(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_158(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_159(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_160(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_161(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_162(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_163(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_164(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_165(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_166(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_167(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_168(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_169(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_170(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_171(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_172(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_173(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_174(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_175(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_176(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_177(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_178(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_179(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_180(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_181(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_182(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_183(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_184(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_185(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_186(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_187(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_188(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_189(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_190(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_191(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_192(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_193(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_194(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_195(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_196(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_197(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_198(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_199(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_200(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_201(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_202(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_203(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_204(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_205(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_206(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_207(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_208(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_209(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_210(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_211(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_212(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_213(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_214(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_215(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_216(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_217(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_218(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_219(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_220(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_221(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_222(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_223(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_224(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_225(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_226(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_227(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_228(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_229(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_230(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_231(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_232(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_233(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_234(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_235(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_236(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_237(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_238(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_239(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_240(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_241(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_242(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_243(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_244(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_245(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_246(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_247(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_248(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_249(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_250(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_251(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_252(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_253(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_254(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_255(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_256(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_257(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_258(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_259(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_260(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_261(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_262(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_263(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_264(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_265(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_266(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_267(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_268(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_269(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_270(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_271(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_272(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_273(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_274(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_275(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_276(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_277(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_278(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_279(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_280(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_281(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_282(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_283(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_284(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_285(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_286(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_287(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_288(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_289(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_290(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_291(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_292(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_293(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_294(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_295(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_296(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_297(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_298(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_299(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_300(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_301(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_302(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_303(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_304(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_305(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_306(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_307(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_308(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_309(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_310(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_311(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_312(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_313(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_314(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_315(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_316(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_317(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_318(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_319(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_320(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_321(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_322(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_323(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_324(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_325(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_326(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_327(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_328(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_329(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_330(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_331(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_332(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_333(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_334(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_335(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_336(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_337(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_338(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_339(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_340(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_341(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_342(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_343(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_344(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_345(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_346(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_347(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_348(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_349(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_350(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_351(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_352(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_353(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_354(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_355(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_356(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_357(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_358(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_359(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_360(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_361(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_362(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_363(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_364(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_365(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_366(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_367(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_368(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_369(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_370(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_371(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_372(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_373(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_374(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_375(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_376(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_377(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_378(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_379(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_380(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_381(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_382(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_383(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_384(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_385(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_386(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_387(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_388(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_389(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_390(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_391(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_392(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_393(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_394(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_395(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_396(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_397(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_398(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_399(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_400(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_401(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_402(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_403(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_404(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_405(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_406(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_407(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_408(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_409(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_410(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_411(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_412(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_413(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_414(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_415(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_416(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_417(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_418(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_419(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_420(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_421(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_422(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_423(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_424(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_425(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_426(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_427(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_428(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_429(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_430(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_431(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_432(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_433(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_434(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_435(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_436(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_437(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_438(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_439(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_440(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_441(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_442(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_443(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_444(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_445(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_446(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_447(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_448(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_449(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_450(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_451(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_452(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_453(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_454(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_455(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_456(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_457(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_458(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_459(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_460(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_461(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_462(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_463(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_464(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_465(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_466(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_467(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_468(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_469(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_470(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_471(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_472(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_473(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_474(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_475(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_476(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_477(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_478(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_479(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_480(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_481(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_482(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_483(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_484(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_485(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_486(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_487(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_488(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_489(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_490(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_491(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_492(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_493(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_494(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_495(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_496(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_497(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_498(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Instr* x86_emit_499(X86Function* func, X86Register r1, X86Register r2, int imm);
X86Module* x86_module_create(const char* name);
void x86_module_destroy(X86Module* mod);
X86Function* x86_function_create(X86Module* mod, const char* name);
void x86_function_emit(X86Function* func, X86Instr* instr);
void x86_print(X86Module* mod);
void x86_lower_ir(X86Module* mod, IRModule* ir);

#endif /* AURORA_X86_64_H */