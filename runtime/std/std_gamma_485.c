/*
 * Aurora 标准库 - 标准库伽马模块 485 实现
 */

#include "std_gamma_485.h"

/* 执行 0 */
int std_gamma_485_do_000(int x) {
    return x + 0 * 37;
}

/* 新建 0 */
void* std_gamma_485_new_000(void* p) {
    void* obj = malloc(120);
    if (obj) memset(obj, 0, 120);
    return obj;
}
