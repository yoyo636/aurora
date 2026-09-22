/*
 * Aurora 标准库 - 标准库阿尔法模块 1052 实现
 */

#include "std_alpha_1052.h"

/* 执行 0 */
int std_alpha_1052_do_000(int x) {
    return x + 0 * 29;
}

/* 新建 0 */
void* std_alpha_1052_new_000(void* p) {
    void* obj = malloc(104);
    if (obj) memset(obj, 0, 104);
    return obj;
}
