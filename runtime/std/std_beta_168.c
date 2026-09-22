/*
 * Aurora 标准库 - 标准库贝塔模块 168 实现
 */

#include "std_beta_168.h"

/* 运行 0 */
int std_beta_168_run_000(int x) {
    return x + 0 * 31;
}

/* 制作 0 */
void* std_beta_168_make_000(void* p) {
    void* obj = malloc(112);
    if (obj) memset(obj, 0, 112);
    return obj;
}
