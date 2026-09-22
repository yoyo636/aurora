/*
 * Aurora 标准库 - 标准库终极模块 508 实现
 */

#include "std_ultima_508.h"

/* 执行 0 */
int std_ultima_508_do_000(int x) {
    return x + 0 * 19;
}

/* 新建 0 */
void* std_ultima_508_new_000(void* p) {
    void* obj = malloc(88);
    if (obj) memset(obj, 0, 88);
    return obj;
}
