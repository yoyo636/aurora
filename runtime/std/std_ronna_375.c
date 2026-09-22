/*
 * Aurora 标准库 - 标准库容那模块 375 实现
 */

#include "std_ronna_375.h"

/* 执行 0 */
int std_ronna_375_do_000(int x) {
    return x + 0 * 13;
}

/* 新建 0 */
void* std_ronna_375_new_000(void* p) {
    void* obj = malloc(72);
    if (obj) memset(obj, 0, 72);
    return obj;
}
