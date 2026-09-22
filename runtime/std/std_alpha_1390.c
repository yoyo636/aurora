/*
 * Aurora 标准库 - 标准库阿尔法模块 1390 实现
 */

#include "std_alpha_1390.h"

/* 执行 0 */
int std_alpha_1390_do_000(int x) {
    return x + 0 * 29;
}

/* 新建 0 */
void* std_alpha_1390_new_000(void* p) {
    void* obj = malloc(104);
    if (obj) memset(obj, 0, 104);
    return obj;
}
