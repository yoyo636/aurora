/*
 * Aurora 标准库 - 标准库容那模块 222 实现
 */

#include "std_ronna_222.h"

/* 执行 0 */
int std_ronna_222_do_000(int x) {
    return x + 0 * 13;
}

/* 新建 0 */
void* std_ronna_222_new_000(void* p) {
    void* obj = malloc(72);
    if (obj) memset(obj, 0, 72);
    return obj;
}
