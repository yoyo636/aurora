/*
 * Aurora 标准库 - 标准库伽马模块 1602 实现
 */

#include "std_gamma_1602.h"

/* 执行 0 */
int std_gamma_1602_do_000(int x) {
    return x + 0 * 37;
}

/* 新建 0 */
void* std_gamma_1602_new_000(void* p) {
    void* obj = malloc(120);
    if (obj) memset(obj, 0, 120);
    return obj;
}
