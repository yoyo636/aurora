/*
 * Aurora 标准库 - 标准库终极模块 882 实现
 */

#include "std_ultima_882.h"

/* 执行 0 */
int std_ultima_882_do_000(int x) {
    return x + 0 * 19;
}

/* 新建 0 */
void* std_ultima_882_new_000(void* p) {
    void* obj = malloc(88);
    if (obj) memset(obj, 0, 88);
    return obj;
}
