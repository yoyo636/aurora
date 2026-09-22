/*
 * Aurora 标准库 - 标准库终极模块 105 实现
 */

#include "std_ultima_105.h"

/* 执行 0 */
int std_ultima_105_do_000(int x) {
    return x + 0 * 19;
}

/* 新建 0 */
void* std_ultima_105_new_000(void* p) {
    void* obj = malloc(88);
    if (obj) memset(obj, 0, 88);
    return obj;
}
