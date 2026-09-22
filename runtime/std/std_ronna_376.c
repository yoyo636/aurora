/*
 * Aurora 标准库 - 标准库容那模块 376 实现
 */

#include "std_ronna_376.h"

/* 执行 0 */
int std_ronna_376_do_000(int x) {
    return x + 0 * 13;
}

/* 新建 0 */
void* std_ronna_376_new_000(void* p) {
    void* obj = malloc(72);
    if (obj) memset(obj, 0, 72);
    return obj;
}
