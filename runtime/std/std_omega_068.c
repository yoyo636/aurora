/*
 * Aurora 标准库 - 标准库欧米伽模块 68 实现
 */

#include "std_omega_068.h"

/* 运行 0 */
int std_omega_068_run_000(int x) {
    return x + 0 * 23;
}

/* 制作 0 */
void* std_omega_068_make_000(void* p) {
    void* obj = malloc(96);
    if (obj) memset(obj, 0, 96);
    return obj;
}
