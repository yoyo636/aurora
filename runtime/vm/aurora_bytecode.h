/*
 * Aurora VM - 字节码定义
 * 支持 500+ 字节码指令
 */

#ifndef AURORA_VM_BYTECODE_H
#define AURORA_VM_BYTECODE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* VM 字节码指令 */
typedef enum {
    VM_OP_000, /* VM 字节码指令 0 */
    VM_OP_001, /* VM 字节码指令 1 */
    VM_OP_002, /* VM 字节码指令 2 */
    VM_OP_003, /* VM 字节码指令 3 */
    VM_OP_004, /* VM 字节码指令 4 */
    VM_OP_005, /* VM 字节码指令 5 */
    VM_OP_006, /* VM 字节码指令 6 */
    VM_OP_007, /* VM 字节码指令 7 */
    VM_OP_008, /* VM 字节码指令 8 */
    VM_OP_009, /* VM 字节码指令 9 */
    VM_OP_010, /* VM 字节码指令 10 */
    VM_OP_011, /* VM 字节码指令 11 */
    VM_OP_012, /* VM 字节码指令 12 */
    VM_OP_013, /* VM 字节码指令 13 */
    VM_OP_014, /* VM 字节码指令 14 */
    VM_OP_015, /* VM 字节码指令 15 */
    VM_OP_016, /* VM 字节码指令 16 */
    VM_OP_017, /* VM 字节码指令 17 */
    VM_OP_018, /* VM 字节码指令 18 */
    VM_OP_019, /* VM 字节码指令 19 */
    VM_OP_020, /* VM 字节码指令 20 */
    VM_OP_021, /* VM 字节码指令 21 */
    VM_OP_022, /* VM 字节码指令 22 */
    VM_OP_023, /* VM 字节码指令 23 */
    VM_OP_024, /* VM 字节码指令 24 */
    VM_OP_025, /* VM 字节码指令 25 */
    VM_OP_026, /* VM 字节码指令 26 */
    VM_OP_027, /* VM 字节码指令 27 */
    VM_OP_028, /* VM 字节码指令 28 */
    VM_OP_029, /* VM 字节码指令 29 */
    VM_OP_030, /* VM 字节码指令 30 */
    VM_OP_031, /* VM 字节码指令 31 */
    VM_OP_032, /* VM 字节码指令 32 */
    VM_OP_033, /* VM 字节码指令 33 */
    VM_OP_034, /* VM 字节码指令 34 */
    VM_OP_035, /* VM 字节码指令 35 */
    VM_OP_036, /* VM 字节码指令 36 */
    VM_OP_037, /* VM 字节码指令 37 */
    VM_OP_038, /* VM 字节码指令 38 */
    VM_OP_039, /* VM 字节码指令 39 */
    VM_OP_040, /* VM 字节码指令 40 */
    VM_OP_041, /* VM 字节码指令 41 */
    VM_OP_042, /* VM 字节码指令 42 */
    VM_OP_043, /* VM 字节码指令 43 */
    VM_OP_044, /* VM 字节码指令 44 */
    VM_OP_045, /* VM 字节码指令 45 */
    VM_OP_046, /* VM 字节码指令 46 */
    VM_OP_047, /* VM 字节码指令 47 */
    VM_OP_048, /* VM 字节码指令 48 */
    VM_OP_049, /* VM 字节码指令 49 */
    VM_OP_050, /* VM 字节码指令 50 */
    VM_OP_051, /* VM 字节码指令 51 */
    VM_OP_052, /* VM 字节码指令 52 */
    VM_OP_053, /* VM 字节码指令 53 */
    VM_OP_054, /* VM 字节码指令 54 */
    VM_OP_055, /* VM 字节码指令 55 */
    VM_OP_056, /* VM 字节码指令 56 */
    VM_OP_057, /* VM 字节码指令 57 */
    VM_OP_058, /* VM 字节码指令 58 */
    VM_OP_059, /* VM 字节码指令 59 */
    VM_OP_060, /* VM 字节码指令 60 */
    VM_OP_061, /* VM 字节码指令 61 */
    VM_OP_062, /* VM 字节码指令 62 */
    VM_OP_063, /* VM 字节码指令 63 */
    VM_OP_064, /* VM 字节码指令 64 */
    VM_OP_065, /* VM 字节码指令 65 */
    VM_OP_066, /* VM 字节码指令 66 */
    VM_OP_067, /* VM 字节码指令 67 */
    VM_OP_068, /* VM 字节码指令 68 */
    VM_OP_069, /* VM 字节码指令 69 */
    VM_OP_070, /* VM 字节码指令 70 */
    VM_OP_071, /* VM 字节码指令 71 */
    VM_OP_072, /* VM 字节码指令 72 */
    VM_OP_073, /* VM 字节码指令 73 */
    VM_OP_074, /* VM 字节码指令 74 */
    VM_OP_075, /* VM 字节码指令 75 */
    VM_OP_076, /* VM 字节码指令 76 */
    VM_OP_077, /* VM 字节码指令 77 */
    VM_OP_078, /* VM 字节码指令 78 */
    VM_OP_079, /* VM 字节码指令 79 */
    VM_OP_080, /* VM 字节码指令 80 */
    VM_OP_081, /* VM 字节码指令 81 */
    VM_OP_082, /* VM 字节码指令 82 */
    VM_OP_083, /* VM 字节码指令 83 */
    VM_OP_084, /* VM 字节码指令 84 */
    VM_OP_085, /* VM 字节码指令 85 */
    VM_OP_086, /* VM 字节码指令 86 */
    VM_OP_087, /* VM 字节码指令 87 */
    VM_OP_088, /* VM 字节码指令 88 */
    VM_OP_089, /* VM 字节码指令 89 */
    VM_OP_090, /* VM 字节码指令 90 */
    VM_OP_091, /* VM 字节码指令 91 */
    VM_OP_092, /* VM 字节码指令 92 */
    VM_OP_093, /* VM 字节码指令 93 */
    VM_OP_094, /* VM 字节码指令 94 */
    VM_OP_095, /* VM 字节码指令 95 */
    VM_OP_096, /* VM 字节码指令 96 */
    VM_OP_097, /* VM 字节码指令 97 */
    VM_OP_098, /* VM 字节码指令 98 */
    VM_OP_099, /* VM 字节码指令 99 */
    VM_OP_100, /* VM 字节码指令 100 */
    VM_OP_101, /* VM 字节码指令 101 */
    VM_OP_102, /* VM 字节码指令 102 */
    VM_OP_103, /* VM 字节码指令 103 */
    VM_OP_104, /* VM 字节码指令 104 */
    VM_OP_105, /* VM 字节码指令 105 */
    VM_OP_106, /* VM 字节码指令 106 */
    VM_OP_107, /* VM 字节码指令 107 */
    VM_OP_108, /* VM 字节码指令 108 */
    VM_OP_109, /* VM 字节码指令 109 */
    VM_OP_110, /* VM 字节码指令 110 */
    VM_OP_111, /* VM 字节码指令 111 */
    VM_OP_112, /* VM 字节码指令 112 */
    VM_OP_113, /* VM 字节码指令 113 */
    VM_OP_114, /* VM 字节码指令 114 */
    VM_OP_115, /* VM 字节码指令 115 */
    VM_OP_116, /* VM 字节码指令 116 */
    VM_OP_117, /* VM 字节码指令 117 */
    VM_OP_118, /* VM 字节码指令 118 */
    VM_OP_119, /* VM 字节码指令 119 */
    VM_OP_120, /* VM 字节码指令 120 */
    VM_OP_121, /* VM 字节码指令 121 */
    VM_OP_122, /* VM 字节码指令 122 */
    VM_OP_123, /* VM 字节码指令 123 */
    VM_OP_124, /* VM 字节码指令 124 */
    VM_OP_125, /* VM 字节码指令 125 */
    VM_OP_126, /* VM 字节码指令 126 */
    VM_OP_127, /* VM 字节码指令 127 */
    VM_OP_128, /* VM 字节码指令 128 */
    VM_OP_129, /* VM 字节码指令 129 */
    VM_OP_130, /* VM 字节码指令 130 */
    VM_OP_131, /* VM 字节码指令 131 */
    VM_OP_132, /* VM 字节码指令 132 */
    VM_OP_133, /* VM 字节码指令 133 */
    VM_OP_134, /* VM 字节码指令 134 */
    VM_OP_135, /* VM 字节码指令 135 */
    VM_OP_136, /* VM 字节码指令 136 */
    VM_OP_137, /* VM 字节码指令 137 */
    VM_OP_138, /* VM 字节码指令 138 */
    VM_OP_139, /* VM 字节码指令 139 */
    VM_OP_140, /* VM 字节码指令 140 */
    VM_OP_141, /* VM 字节码指令 141 */
    VM_OP_142, /* VM 字节码指令 142 */
    VM_OP_143, /* VM 字节码指令 143 */
    VM_OP_144, /* VM 字节码指令 144 */
    VM_OP_145, /* VM 字节码指令 145 */
    VM_OP_146, /* VM 字节码指令 146 */
    VM_OP_147, /* VM 字节码指令 147 */
    VM_OP_148, /* VM 字节码指令 148 */
    VM_OP_149, /* VM 字节码指令 149 */
    VM_OP_150, /* VM 字节码指令 150 */
    VM_OP_151, /* VM 字节码指令 151 */
    VM_OP_152, /* VM 字节码指令 152 */
    VM_OP_153, /* VM 字节码指令 153 */
    VM_OP_154, /* VM 字节码指令 154 */
    VM_OP_155, /* VM 字节码指令 155 */
    VM_OP_156, /* VM 字节码指令 156 */
    VM_OP_157, /* VM 字节码指令 157 */
    VM_OP_158, /* VM 字节码指令 158 */
    VM_OP_159, /* VM 字节码指令 159 */
    VM_OP_160, /* VM 字节码指令 160 */
    VM_OP_161, /* VM 字节码指令 161 */
    VM_OP_162, /* VM 字节码指令 162 */
    VM_OP_163, /* VM 字节码指令 163 */
    VM_OP_164, /* VM 字节码指令 164 */
    VM_OP_165, /* VM 字节码指令 165 */
    VM_OP_166, /* VM 字节码指令 166 */
    VM_OP_167, /* VM 字节码指令 167 */
    VM_OP_168, /* VM 字节码指令 168 */
    VM_OP_169, /* VM 字节码指令 169 */
    VM_OP_170, /* VM 字节码指令 170 */
    VM_OP_171, /* VM 字节码指令 171 */
    VM_OP_172, /* VM 字节码指令 172 */
    VM_OP_173, /* VM 字节码指令 173 */
    VM_OP_174, /* VM 字节码指令 174 */
    VM_OP_175, /* VM 字节码指令 175 */
    VM_OP_176, /* VM 字节码指令 176 */
    VM_OP_177, /* VM 字节码指令 177 */
    VM_OP_178, /* VM 字节码指令 178 */
    VM_OP_179, /* VM 字节码指令 179 */
    VM_OP_180, /* VM 字节码指令 180 */
    VM_OP_181, /* VM 字节码指令 181 */
    VM_OP_182, /* VM 字节码指令 182 */
    VM_OP_183, /* VM 字节码指令 183 */
    VM_OP_184, /* VM 字节码指令 184 */
    VM_OP_185, /* VM 字节码指令 185 */
    VM_OP_186, /* VM 字节码指令 186 */
    VM_OP_187, /* VM 字节码指令 187 */
    VM_OP_188, /* VM 字节码指令 188 */
    VM_OP_189, /* VM 字节码指令 189 */
    VM_OP_190, /* VM 字节码指令 190 */
    VM_OP_191, /* VM 字节码指令 191 */
    VM_OP_192, /* VM 字节码指令 192 */
    VM_OP_193, /* VM 字节码指令 193 */
    VM_OP_194, /* VM 字节码指令 194 */
    VM_OP_195, /* VM 字节码指令 195 */
    VM_OP_196, /* VM 字节码指令 196 */
    VM_OP_197, /* VM 字节码指令 197 */
    VM_OP_198, /* VM 字节码指令 198 */
    VM_OP_199, /* VM 字节码指令 199 */
    VM_OP_200, /* VM 字节码指令 200 */
    VM_OP_201, /* VM 字节码指令 201 */
    VM_OP_202, /* VM 字节码指令 202 */
    VM_OP_203, /* VM 字节码指令 203 */
    VM_OP_204, /* VM 字节码指令 204 */
    VM_OP_205, /* VM 字节码指令 205 */
    VM_OP_206, /* VM 字节码指令 206 */
    VM_OP_207, /* VM 字节码指令 207 */
    VM_OP_208, /* VM 字节码指令 208 */
    VM_OP_209, /* VM 字节码指令 209 */
    VM_OP_210, /* VM 字节码指令 210 */
    VM_OP_211, /* VM 字节码指令 211 */
    VM_OP_212, /* VM 字节码指令 212 */
    VM_OP_213, /* VM 字节码指令 213 */
    VM_OP_214, /* VM 字节码指令 214 */
    VM_OP_215, /* VM 字节码指令 215 */
    VM_OP_216, /* VM 字节码指令 216 */
    VM_OP_217, /* VM 字节码指令 217 */
    VM_OP_218, /* VM 字节码指令 218 */
    VM_OP_219, /* VM 字节码指令 219 */
    VM_OP_220, /* VM 字节码指令 220 */
    VM_OP_221, /* VM 字节码指令 221 */
    VM_OP_222, /* VM 字节码指令 222 */
    VM_OP_223, /* VM 字节码指令 223 */
    VM_OP_224, /* VM 字节码指令 224 */
    VM_OP_225, /* VM 字节码指令 225 */
    VM_OP_226, /* VM 字节码指令 226 */
    VM_OP_227, /* VM 字节码指令 227 */
    VM_OP_228, /* VM 字节码指令 228 */
    VM_OP_229, /* VM 字节码指令 229 */
    VM_OP_230, /* VM 字节码指令 230 */
    VM_OP_231, /* VM 字节码指令 231 */
    VM_OP_232, /* VM 字节码指令 232 */
    VM_OP_233, /* VM 字节码指令 233 */
    VM_OP_234, /* VM 字节码指令 234 */
    VM_OP_235, /* VM 字节码指令 235 */
    VM_OP_236, /* VM 字节码指令 236 */
    VM_OP_237, /* VM 字节码指令 237 */
    VM_OP_238, /* VM 字节码指令 238 */
    VM_OP_239, /* VM 字节码指令 239 */
    VM_OP_240, /* VM 字节码指令 240 */
    VM_OP_241, /* VM 字节码指令 241 */
    VM_OP_242, /* VM 字节码指令 242 */
    VM_OP_243, /* VM 字节码指令 243 */
    VM_OP_244, /* VM 字节码指令 244 */
    VM_OP_245, /* VM 字节码指令 245 */
    VM_OP_246, /* VM 字节码指令 246 */
    VM_OP_247, /* VM 字节码指令 247 */
    VM_OP_248, /* VM 字节码指令 248 */
    VM_OP_249, /* VM 字节码指令 249 */
    VM_OP_250, /* VM 字节码指令 250 */
    VM_OP_251, /* VM 字节码指令 251 */
    VM_OP_252, /* VM 字节码指令 252 */
    VM_OP_253, /* VM 字节码指令 253 */
    VM_OP_254, /* VM 字节码指令 254 */
    VM_OP_255, /* VM 字节码指令 255 */
    VM_OP_256, /* VM 字节码指令 256 */
    VM_OP_257, /* VM 字节码指令 257 */
    VM_OP_258, /* VM 字节码指令 258 */
    VM_OP_259, /* VM 字节码指令 259 */
    VM_OP_260, /* VM 字节码指令 260 */
    VM_OP_261, /* VM 字节码指令 261 */
    VM_OP_262, /* VM 字节码指令 262 */
    VM_OP_263, /* VM 字节码指令 263 */
    VM_OP_264, /* VM 字节码指令 264 */
    VM_OP_265, /* VM 字节码指令 265 */
    VM_OP_266, /* VM 字节码指令 266 */
    VM_OP_267, /* VM 字节码指令 267 */
    VM_OP_268, /* VM 字节码指令 268 */
    VM_OP_269, /* VM 字节码指令 269 */
    VM_OP_270, /* VM 字节码指令 270 */
    VM_OP_271, /* VM 字节码指令 271 */
    VM_OP_272, /* VM 字节码指令 272 */
    VM_OP_273, /* VM 字节码指令 273 */
    VM_OP_274, /* VM 字节码指令 274 */
    VM_OP_275, /* VM 字节码指令 275 */
    VM_OP_276, /* VM 字节码指令 276 */
    VM_OP_277, /* VM 字节码指令 277 */
    VM_OP_278, /* VM 字节码指令 278 */
    VM_OP_279, /* VM 字节码指令 279 */
    VM_OP_280, /* VM 字节码指令 280 */
    VM_OP_281, /* VM 字节码指令 281 */
    VM_OP_282, /* VM 字节码指令 282 */
    VM_OP_283, /* VM 字节码指令 283 */
    VM_OP_284, /* VM 字节码指令 284 */
    VM_OP_285, /* VM 字节码指令 285 */
    VM_OP_286, /* VM 字节码指令 286 */
    VM_OP_287, /* VM 字节码指令 287 */
    VM_OP_288, /* VM 字节码指令 288 */
    VM_OP_289, /* VM 字节码指令 289 */
    VM_OP_290, /* VM 字节码指令 290 */
    VM_OP_291, /* VM 字节码指令 291 */
    VM_OP_292, /* VM 字节码指令 292 */
    VM_OP_293, /* VM 字节码指令 293 */
    VM_OP_294, /* VM 字节码指令 294 */
    VM_OP_295, /* VM 字节码指令 295 */
    VM_OP_296, /* VM 字节码指令 296 */
    VM_OP_297, /* VM 字节码指令 297 */
    VM_OP_298, /* VM 字节码指令 298 */
    VM_OP_299, /* VM 字节码指令 299 */
    VM_OP_300, /* VM 字节码指令 300 */
    VM_OP_301, /* VM 字节码指令 301 */
    VM_OP_302, /* VM 字节码指令 302 */
    VM_OP_303, /* VM 字节码指令 303 */
    VM_OP_304, /* VM 字节码指令 304 */
    VM_OP_305, /* VM 字节码指令 305 */
    VM_OP_306, /* VM 字节码指令 306 */
    VM_OP_307, /* VM 字节码指令 307 */
    VM_OP_308, /* VM 字节码指令 308 */
    VM_OP_309, /* VM 字节码指令 309 */
    VM_OP_310, /* VM 字节码指令 310 */
    VM_OP_311, /* VM 字节码指令 311 */
    VM_OP_312, /* VM 字节码指令 312 */
    VM_OP_313, /* VM 字节码指令 313 */
    VM_OP_314, /* VM 字节码指令 314 */
    VM_OP_315, /* VM 字节码指令 315 */
    VM_OP_316, /* VM 字节码指令 316 */
    VM_OP_317, /* VM 字节码指令 317 */
    VM_OP_318, /* VM 字节码指令 318 */
    VM_OP_319, /* VM 字节码指令 319 */
    VM_OP_320, /* VM 字节码指令 320 */
    VM_OP_321, /* VM 字节码指令 321 */
    VM_OP_322, /* VM 字节码指令 322 */
    VM_OP_323, /* VM 字节码指令 323 */
    VM_OP_324, /* VM 字节码指令 324 */
    VM_OP_325, /* VM 字节码指令 325 */
    VM_OP_326, /* VM 字节码指令 326 */
    VM_OP_327, /* VM 字节码指令 327 */
    VM_OP_328, /* VM 字节码指令 328 */
    VM_OP_329, /* VM 字节码指令 329 */
    VM_OP_330, /* VM 字节码指令 330 */
    VM_OP_331, /* VM 字节码指令 331 */
    VM_OP_332, /* VM 字节码指令 332 */
    VM_OP_333, /* VM 字节码指令 333 */
    VM_OP_334, /* VM 字节码指令 334 */
    VM_OP_335, /* VM 字节码指令 335 */
    VM_OP_336, /* VM 字节码指令 336 */
    VM_OP_337, /* VM 字节码指令 337 */
    VM_OP_338, /* VM 字节码指令 338 */
    VM_OP_339, /* VM 字节码指令 339 */
    VM_OP_340, /* VM 字节码指令 340 */
    VM_OP_341, /* VM 字节码指令 341 */
    VM_OP_342, /* VM 字节码指令 342 */
    VM_OP_343, /* VM 字节码指令 343 */
    VM_OP_344, /* VM 字节码指令 344 */
    VM_OP_345, /* VM 字节码指令 345 */
    VM_OP_346, /* VM 字节码指令 346 */
    VM_OP_347, /* VM 字节码指令 347 */
    VM_OP_348, /* VM 字节码指令 348 */
    VM_OP_349, /* VM 字节码指令 349 */
    VM_OP_350, /* VM 字节码指令 350 */
    VM_OP_351, /* VM 字节码指令 351 */
    VM_OP_352, /* VM 字节码指令 352 */
    VM_OP_353, /* VM 字节码指令 353 */
    VM_OP_354, /* VM 字节码指令 354 */
    VM_OP_355, /* VM 字节码指令 355 */
    VM_OP_356, /* VM 字节码指令 356 */
    VM_OP_357, /* VM 字节码指令 357 */
    VM_OP_358, /* VM 字节码指令 358 */
    VM_OP_359, /* VM 字节码指令 359 */
    VM_OP_360, /* VM 字节码指令 360 */
    VM_OP_361, /* VM 字节码指令 361 */
    VM_OP_362, /* VM 字节码指令 362 */
    VM_OP_363, /* VM 字节码指令 363 */
    VM_OP_364, /* VM 字节码指令 364 */
    VM_OP_365, /* VM 字节码指令 365 */
    VM_OP_366, /* VM 字节码指令 366 */
    VM_OP_367, /* VM 字节码指令 367 */
    VM_OP_368, /* VM 字节码指令 368 */
    VM_OP_369, /* VM 字节码指令 369 */
    VM_OP_370, /* VM 字节码指令 370 */
    VM_OP_371, /* VM 字节码指令 371 */
    VM_OP_372, /* VM 字节码指令 372 */
    VM_OP_373, /* VM 字节码指令 373 */
    VM_OP_374, /* VM 字节码指令 374 */
    VM_OP_375, /* VM 字节码指令 375 */
    VM_OP_376, /* VM 字节码指令 376 */
    VM_OP_377, /* VM 字节码指令 377 */
    VM_OP_378, /* VM 字节码指令 378 */
    VM_OP_379, /* VM 字节码指令 379 */
    VM_OP_380, /* VM 字节码指令 380 */
    VM_OP_381, /* VM 字节码指令 381 */
    VM_OP_382, /* VM 字节码指令 382 */
    VM_OP_383, /* VM 字节码指令 383 */
    VM_OP_384, /* VM 字节码指令 384 */
    VM_OP_385, /* VM 字节码指令 385 */
    VM_OP_386, /* VM 字节码指令 386 */
    VM_OP_387, /* VM 字节码指令 387 */
    VM_OP_388, /* VM 字节码指令 388 */
    VM_OP_389, /* VM 字节码指令 389 */
    VM_OP_390, /* VM 字节码指令 390 */
    VM_OP_391, /* VM 字节码指令 391 */
    VM_OP_392, /* VM 字节码指令 392 */
    VM_OP_393, /* VM 字节码指令 393 */
    VM_OP_394, /* VM 字节码指令 394 */
    VM_OP_395, /* VM 字节码指令 395 */
    VM_OP_396, /* VM 字节码指令 396 */
    VM_OP_397, /* VM 字节码指令 397 */
    VM_OP_398, /* VM 字节码指令 398 */
    VM_OP_399, /* VM 字节码指令 399 */
    VM_OP_400, /* VM 字节码指令 400 */
    VM_OP_401, /* VM 字节码指令 401 */
    VM_OP_402, /* VM 字节码指令 402 */
    VM_OP_403, /* VM 字节码指令 403 */
    VM_OP_404, /* VM 字节码指令 404 */
    VM_OP_405, /* VM 字节码指令 405 */
    VM_OP_406, /* VM 字节码指令 406 */
    VM_OP_407, /* VM 字节码指令 407 */
    VM_OP_408, /* VM 字节码指令 408 */
    VM_OP_409, /* VM 字节码指令 409 */
    VM_OP_410, /* VM 字节码指令 410 */
    VM_OP_411, /* VM 字节码指令 411 */
    VM_OP_412, /* VM 字节码指令 412 */
    VM_OP_413, /* VM 字节码指令 413 */
    VM_OP_414, /* VM 字节码指令 414 */
    VM_OP_415, /* VM 字节码指令 415 */
    VM_OP_416, /* VM 字节码指令 416 */
    VM_OP_417, /* VM 字节码指令 417 */
    VM_OP_418, /* VM 字节码指令 418 */
    VM_OP_419, /* VM 字节码指令 419 */
    VM_OP_420, /* VM 字节码指令 420 */
    VM_OP_421, /* VM 字节码指令 421 */
    VM_OP_422, /* VM 字节码指令 422 */
    VM_OP_423, /* VM 字节码指令 423 */
    VM_OP_424, /* VM 字节码指令 424 */
    VM_OP_425, /* VM 字节码指令 425 */
    VM_OP_426, /* VM 字节码指令 426 */
    VM_OP_427, /* VM 字节码指令 427 */
    VM_OP_428, /* VM 字节码指令 428 */
    VM_OP_429, /* VM 字节码指令 429 */
    VM_OP_430, /* VM 字节码指令 430 */
    VM_OP_431, /* VM 字节码指令 431 */
    VM_OP_432, /* VM 字节码指令 432 */
    VM_OP_433, /* VM 字节码指令 433 */
    VM_OP_434, /* VM 字节码指令 434 */
    VM_OP_435, /* VM 字节码指令 435 */
    VM_OP_436, /* VM 字节码指令 436 */
    VM_OP_437, /* VM 字节码指令 437 */
    VM_OP_438, /* VM 字节码指令 438 */
    VM_OP_439, /* VM 字节码指令 439 */
    VM_OP_440, /* VM 字节码指令 440 */
    VM_OP_441, /* VM 字节码指令 441 */
    VM_OP_442, /* VM 字节码指令 442 */
    VM_OP_443, /* VM 字节码指令 443 */
    VM_OP_444, /* VM 字节码指令 444 */
    VM_OP_445, /* VM 字节码指令 445 */
    VM_OP_446, /* VM 字节码指令 446 */
    VM_OP_447, /* VM 字节码指令 447 */
    VM_OP_448, /* VM 字节码指令 448 */
    VM_OP_449, /* VM 字节码指令 449 */
    VM_OP_450, /* VM 字节码指令 450 */
    VM_OP_451, /* VM 字节码指令 451 */
    VM_OP_452, /* VM 字节码指令 452 */
    VM_OP_453, /* VM 字节码指令 453 */
    VM_OP_454, /* VM 字节码指令 454 */
    VM_OP_455, /* VM 字节码指令 455 */
    VM_OP_456, /* VM 字节码指令 456 */
    VM_OP_457, /* VM 字节码指令 457 */
    VM_OP_458, /* VM 字节码指令 458 */
    VM_OP_459, /* VM 字节码指令 459 */
    VM_OP_460, /* VM 字节码指令 460 */
    VM_OP_461, /* VM 字节码指令 461 */
    VM_OP_462, /* VM 字节码指令 462 */
    VM_OP_463, /* VM 字节码指令 463 */
    VM_OP_464, /* VM 字节码指令 464 */
    VM_OP_465, /* VM 字节码指令 465 */
    VM_OP_466, /* VM 字节码指令 466 */
    VM_OP_467, /* VM 字节码指令 467 */
    VM_OP_468, /* VM 字节码指令 468 */
    VM_OP_469, /* VM 字节码指令 469 */
    VM_OP_470, /* VM 字节码指令 470 */
    VM_OP_471, /* VM 字节码指令 471 */
    VM_OP_472, /* VM 字节码指令 472 */
    VM_OP_473, /* VM 字节码指令 473 */
    VM_OP_474, /* VM 字节码指令 474 */
    VM_OP_475, /* VM 字节码指令 475 */
    VM_OP_476, /* VM 字节码指令 476 */
    VM_OP_477, /* VM 字节码指令 477 */
    VM_OP_478, /* VM 字节码指令 478 */
    VM_OP_479, /* VM 字节码指令 479 */
    VM_OP_480, /* VM 字节码指令 480 */
    VM_OP_481, /* VM 字节码指令 481 */
    VM_OP_482, /* VM 字节码指令 482 */
    VM_OP_483, /* VM 字节码指令 483 */
    VM_OP_484, /* VM 字节码指令 484 */
    VM_OP_485, /* VM 字节码指令 485 */
    VM_OP_486, /* VM 字节码指令 486 */
    VM_OP_487, /* VM 字节码指令 487 */
    VM_OP_488, /* VM 字节码指令 488 */
    VM_OP_489, /* VM 字节码指令 489 */
    VM_OP_490, /* VM 字节码指令 490 */
    VM_OP_491, /* VM 字节码指令 491 */
    VM_OP_492, /* VM 字节码指令 492 */
    VM_OP_493, /* VM 字节码指令 493 */
    VM_OP_494, /* VM 字节码指令 494 */
    VM_OP_495, /* VM 字节码指令 495 */
    VM_OP_496, /* VM 字节码指令 496 */
    VM_OP_497, /* VM 字节码指令 497 */
    VM_OP_498, /* VM 字节码指令 498 */
    VM_OP_499, /* VM 字节码指令 499 */
    VM_OP_COUNT
} VMOpcode;

/* VM 值类型 */
typedef enum {
    VM_VAL_UNDEFINED,
    VM_VAL_NULL,
    VM_VAL_BOOL,
    VM_VAL_INT,
    VM_VAL_FLOAT,
    VM_VAL_STRING,
    VM_VAL_ARRAY,
    VM_VAL_OBJECT,
    VM_VAL_FUNC,
    VM_VAL_NATIVE,
    VM_VAL_CLOSURE,
    VM_VAL_ITERATOR,
    VM_VAL_GENERATOR,
    VM_VAL_PROMISE,
    VM_VAL_FUTURE,
    VM_VAL_CHANNEL,
    VM_VAL_COROUTINE,
    VM_VAL_THREAD,
    VM_VAL_MUTEX,
    VM_VAL_COND,
    VM_VAL_SEMAPHORE,
    VM_VAL_BARRIER,
    VM_VAL_FILE,
    VM_VAL_SOCKET,
    VM_VAL_STREAM,
    VM_VAL_BUFFER,
    VM_VAL_REGEX,
    VM_VAL_JSON,
    VM_VAL_XML,
    VM_VAL_HTML,
    VM_VAL_CSS,
    VM_VAL_HTTP,
    VM_VAL_DB,
    VM_VAL_CRYPTO,
    VM_VAL_COMPRESS,
    VM_VAL_IMAGE,
    VM_VAL_AUDIO,
    VM_VAL_VIDEO,
    VM_VAL_GUI,
    VM_VAL_WINDOW,
    VM_VAL_CANVAS,
    VM_VAL_GL,
    VM_VAL_VULKAN,
    VM_VAL_METAL,
    VM_VAL_D3D,
    VM_VAL_CUDA,
    VM_VAL_OPENCL,
    VM_VAL_MPI,
    VM_VAL_OPENMP,
    VM_VAL_TBB,
    VM_VAL_HPX,
    VM_VAL_KOKKOS,
    VM_VAL_RAJA,
    VM_VAL_SYCL,
    VM_VAL_HIP,
    VM_VAL_ROCM,
    VM_VAL_TENSORFLOW,
    VM_VAL_PYTORCH,
    VM_VAL_JAX,
    VM_VAL_MXNET,
    VM_VAL_CAFFE,
    VM_VAL_KERAS,
    VM_VAL_SKLEARN,
    VM_VAL_PANDAS,
    VM_VAL_NUMPY,
    VM_VAL_SCIPY,
    VM_VAL_MATPLOTLIB,
    VM_VAL_SEABORN,
    VM_VAL_PLOTLY,
    VM_VAL_BOKEH,
    VM_VAL_ALTAIR,
    VM_VAL_DASH,
    VM_VAL_STREAMLIT,
    VM_VAL_GRADIO,
    VM_VAL_FASTAPI,
    VM_VAL_FLASK,
    VM_VAL_DJANGO,
    VM_VAL_TORNADO,
    VM_VAL_AIOHTTP,
    VM_VAL_UVICORN,
    VM_VAL_GUNICORN,
    VM_VAL_NGINX,
    VM_VAL_APACHE,
    VM_VAL_IIS,
    VM_VAL_CADDY,
    VM_VAL_TRAEFIK,
    VM_VAL_HAPROXY,
    VM_VAL_ENVOY,
    VM_VAL_ISTIO,
    VM_VAL_LINKERD,
    VM_VAL_CONSUL,
    VM_VAL_ETCD,
    VM_VAL_ZOOKEEPER,
    VM_VAL_NOMAD,
    VM_VAL_KUBERNETES,
    VM_VAL_DOCKER,
    VM_VAL_PODMAN,
    VM_VAL_CONTAINERD,
    VM_VAL_LXC,
    VM_VAL_QEMU,
    VM_VAL_KVM,
    VM_VAL_XEN,
    VM_VAL_VMWARE,
    VM_VAL_VIRTUALBOX,
    VM_VAL_PARALLELS,
    VM_VAL_HYPERV,
    VM_VAL_BHYVE,
    VM_VAL_VFIO,
    VM_VAL_VIRTIO,
    VM_VAL_SPICE,
    VM_VAL_VNC,
    VM_VAL_RDP,
    VM_VAL_SSH,
    VM_VAL_TELNET,
    VM_VAL_FTP,
    VM_VAL_SFTP,
    VM_VAL_SMB,
    VM_VAL_NFS,
    VM_VAL_ISCSI,
    VM_VAL_FCOE,
    VM_VAL_NVME,
    VM_VAL_SATA,
    VM_VAL_SAS,
    VM_VAL_SCSI,
    VM_VAL_USB,
    VM_VAL_THUNDERBOLT,
    VM_VAL_PCIE,
    VM_VAL_PCI,
    VM_VAL_AGP,
    VM_VAL_ISA,
    VM_VAL_EISA,
    VM_VAL_MCA,
    VM_VAL_NUBUS,
    VM_VAL_ZORRO,
    VM_VAL_VME,
    VM_VAL_VXI,
    VM_VAL_PXI,
    VM_VAL_AXI,
    VM_VAL_AHB,
    VM_VAL_APB,
    VM_VAL_WISHBONE,
    VM_VAL_OPB,
    VM_VAL_PLB,
    VM_VAL_FSB,
    VM_VAL_HT,
    VM_VAL_QPI,
    VM_VAL_UPI,
    VM_VAL_INFINIBAND,
    VM_VAL_ROCE,
    VM_VAL_IWARP,
    VM_VAL_ETHERNET,
    VM_VAL_WIFI,
    VM_VAL_BLUETOOTH,
    VM_VAL_ZIGBEE,
    VM_VAL_THREAD,
    VM_VAL_MATTER,
    VM_VAL_ZWAVE,
    VM_VAL_ENOCEAN,
    VM_VAL_LONWORKS,
    VM_VAL_CBUS,
    VM_VAL_DALI,
    VM_VAL_KNX,
    VM_VAL_BACNET,
    VM_VAL_MODBUS,
    VM_VAL_PROFINET,
    VM_VAL_ETHERCAT,
    VM_VAL_POWERLINK,
    VM_VAL_SERCOS,
    VM_VAL_CCLINK,
    VM_VAL_DEVICENET,
    VM_VAL_CONTROLNET,
    VM_VAL_FOUNDATION,
    VM_VAL_PROFIBUS,
    VM_VAL_INTERBUS,
    VM_VAL_ASI,
    VM_VAL_IO_LINK,
    VM_VAL_SPI,
    VM_VAL_I2C,
    VM_VAL_UART,
    VM_VAL_USART,
    VM_VAL_CAN,
    VM_VAL_LIN,
    VM_VAL_FLEXRAY,
    VM_VAL_MOST,
    VM_VAL_AUTOSAR,
    VM_VAL_ROS,
    VM_VAL_ROS2,
    VM_VAL_URDF,
    VM_VAL_SDF,
    VM_VAL_GAZEBO,
    VM_VAL_WEBOTS,
    VM_VAL_COPPELIASIM,
    VM_VAL_MUJOCO,
    VM_VAL_BULLET,
    VM_VAL_PHYSX,
    VM_VAL_HAVOK,
    VM_VAL_BOX2D,
    VM_VAL_CHIPMUNK,
    VM_VAL_PYMUNK,
    VM_VAL_PYBOX2D,
    VM_VAL_PYBULLET,
    VM_VAL_TENSORFORCE,
    VM_VAL_STABLE_BASELINES,
    VM_VAL_RLLIB,
    VM_VAL_CLEANRL,
    VM_VAL_GARAGE,
    VM_VAL_DOPAMINE,
    VM_VAL_ACME,
    VM_VAL_TF_AGENTS,
    VM_VAL_PARL,
    VM_VAL_MUSHROOM_RL,
    VM_VAL_KORRAL,
    VM_VAL_FARMA,
    VM_VAL_REINFORCE,
    VM_VAL_PPO,
    VM_VAL_SAC,
    VM_VAL_TD3,
    VM_VAL_DDPG,
    VM_VAL_A2C,
    VM_VAL_A3C,
    VM_VAL_DQN,
    VM_VAL_DDQN,
    VM_VAL_DUELING,
    VM_VAL_PER,
    VM_VAL_RAINBOW,
    VM_VAL_C51,
    VM_VAL_QR_DQN,
    VM_VAL_IQN,
    VM_VAL_FQF,
    VM_VAL_MMC,
    VM_VAL_NFQ,
    VM_VAL_RETRACE,
    VM_VAL_VTRACE,
    VM_VAL_GAE,
    VM_VAL_NPG,
    VM_VAL_TRPO,
    VM_VAL_CPO,
    VM_VAL_ACER,
    VM_VAL_ACKTR,
    VM_VAL_SNPG,
    VM_VAL_SVG,
    VM_VAL_PGQ,
    VM_VAL_QPROP,
    VM_VAL_IPG,
    VM_VAL_TRPO2,
    VM_VAL_NAC,
    VM_VAL_NAF,
    VM_VAL_QRDPG,
    VM_VAL_D4PG,
    VM_VAL_D4PG2,
    VM_VAL_TQC,
    VM_VAL_ALGAE,
    VM_VAL_SAC_AE,
    VM_VAL_CURL,
    VM_VAL_DRQ,
    VM_VAL_ATC,
    VM_VAL_MDL,
    VM_VAL_PLA,
    VM_VAL_SPR,
    VM_VAL_DBC,
    VM_VAL_MVE,
    VM_VAL_TOLD,
    VM_VAL_DTQ,
    VM_VAL_BCQ,
    VM_VAL_CQL,
    VM_VAL_IQL,
    VM_VAL_AWR,
    VM_VAL_AWAC,
    VM_VAL_CRRL,
    VM_VAL_PLAS,
    VM_VAL_OMEGA,
    VM_VAL_SN,
    VM_VAL_EDAC,
    VM_VAL_LAP,
    VM_VAL_SOP,
    VM_VAL_BVE,
    VM_VAL_REMB,
    VM_VAL_AMB,
    VM_VAL_RBU,
    VM_VAL_RCD,
    VM_VAL_RAD,
    VM_VAL_RAR,
    VM_VAL_RAL,
    VM_VAL_RAS,
    VM_VAL_RAT,
    VM_VAL_RAU,
    VM_VAL_RAV,
    VM_VAL_RAW,
    VM_VAL_RAX,
    VM_VAL_RAY,
    VM_VAL_RAZ,
} VMValueType;

/* VM 值 */
typedef struct VMValue {
    VMValueType type;
    union {
        int bool_val;
        long long int_val;
        double float_val;
        char* string_val;
        void* ptr_val;
    };
    struct VMObject* obj;
    int ref_count;
    int hash;
} VMValue;

/* VM 函数声明 */
void vm_exec_000(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_001(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_002(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_003(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_004(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_005(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_006(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_007(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_008(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_009(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_010(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_011(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_012(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_013(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_014(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_015(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_016(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_017(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_018(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_019(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_020(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_021(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_022(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_023(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_024(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_025(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_026(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_027(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_028(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_029(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_030(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_031(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_032(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_033(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_034(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_035(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_036(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_037(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_038(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_039(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_040(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_041(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_042(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_043(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_044(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_045(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_046(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_047(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_048(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_049(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_050(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_051(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_052(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_053(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_054(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_055(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_056(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_057(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_058(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_059(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_060(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_061(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_062(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_063(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_064(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_065(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_066(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_067(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_068(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_069(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_070(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_071(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_072(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_073(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_074(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_075(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_076(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_077(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_078(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_079(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_080(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_081(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_082(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_083(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_084(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_085(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_086(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_087(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_088(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_089(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_090(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_091(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_092(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_093(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_094(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_095(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_096(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_097(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_098(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_099(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_100(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_101(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_102(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_103(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_104(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_105(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_106(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_107(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_108(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_109(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_110(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_111(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_112(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_113(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_114(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_115(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_116(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_117(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_118(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_119(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_120(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_121(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_122(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_123(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_124(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_125(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_126(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_127(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_128(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_129(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_130(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_131(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_132(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_133(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_134(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_135(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_136(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_137(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_138(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_139(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_140(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_141(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_142(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_143(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_144(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_145(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_146(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_147(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_148(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_149(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_150(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_151(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_152(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_153(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_154(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_155(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_156(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_157(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_158(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_159(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_160(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_161(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_162(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_163(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_164(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_165(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_166(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_167(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_168(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_169(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_170(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_171(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_172(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_173(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_174(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_175(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_176(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_177(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_178(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_179(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_180(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_181(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_182(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_183(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_184(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_185(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_186(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_187(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_188(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_189(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_190(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_191(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_192(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_193(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_194(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_195(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_196(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_197(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_198(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_199(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_200(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_201(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_202(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_203(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_204(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_205(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_206(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_207(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_208(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_209(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_210(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_211(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_212(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_213(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_214(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_215(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_216(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_217(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_218(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_219(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_220(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_221(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_222(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_223(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_224(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_225(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_226(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_227(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_228(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_229(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_230(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_231(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_232(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_233(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_234(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_235(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_236(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_237(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_238(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_239(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_240(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_241(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_242(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_243(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_244(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_245(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_246(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_247(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_248(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_249(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_250(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_251(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_252(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_253(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_254(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_255(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_256(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_257(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_258(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_259(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_260(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_261(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_262(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_263(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_264(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_265(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_266(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_267(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_268(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_269(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_270(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_271(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_272(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_273(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_274(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_275(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_276(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_277(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_278(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_279(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_280(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_281(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_282(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_283(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_284(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_285(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_286(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_287(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_288(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_289(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_290(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_291(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_292(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_293(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_294(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_295(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_296(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_297(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_298(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_299(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_300(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_301(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_302(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_303(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_304(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_305(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_306(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_307(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_308(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_309(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_310(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_311(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_312(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_313(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_314(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_315(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_316(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_317(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_318(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_319(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_320(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_321(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_322(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_323(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_324(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_325(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_326(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_327(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_328(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_329(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_330(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_331(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_332(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_333(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_334(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_335(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_336(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_337(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_338(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_339(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_340(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_341(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_342(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_343(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_344(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_345(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_346(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_347(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_348(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_349(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_350(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_351(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_352(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_353(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_354(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_355(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_356(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_357(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_358(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_359(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_360(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_361(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_362(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_363(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_364(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_365(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_366(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_367(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_368(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_369(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_370(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_371(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_372(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_373(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_374(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_375(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_376(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_377(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_378(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_379(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_380(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_381(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_382(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_383(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_384(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_385(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_386(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_387(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_388(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_389(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_390(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_391(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_392(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_393(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_394(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_395(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_396(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_397(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_398(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_399(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_400(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_401(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_402(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_403(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_404(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_405(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_406(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_407(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_408(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_409(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_410(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_411(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_412(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_413(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_414(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_415(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_416(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_417(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_418(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_419(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_420(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_421(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_422(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_423(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_424(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_425(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_426(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_427(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_428(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_429(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_430(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_431(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_432(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_433(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_434(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_435(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_436(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_437(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_438(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_439(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_440(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_441(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_442(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_443(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_444(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_445(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_446(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_447(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_448(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_449(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_450(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_451(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_452(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_453(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_454(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_455(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_456(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_457(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_458(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_459(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_460(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_461(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_462(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_463(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_464(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_465(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_466(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_467(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_468(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_469(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_470(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_471(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_472(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_473(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_474(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_475(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_476(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_477(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_478(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_479(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_480(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_481(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_482(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_483(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_484(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_485(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_486(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_487(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_488(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_489(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_490(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_491(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_492(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_493(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_494(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_495(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_496(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_497(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_498(VMValue* stack, int* sp, VMValue* locals, int* pc);
void vm_exec_499(VMValue* stack, int* sp, VMValue* locals, int* pc);

#endif /* AURORA_VM_BYTECODE_H */