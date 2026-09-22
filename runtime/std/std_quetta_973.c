/*
 * Aurora 标准库 - 标准库亏它模块 973 实现
 */

#include "std_quetta_973.h"

/* 运行 0 */
int std_quetta_973_run_000(int x) {
    return x + 0 * 17;
}

/* 制作 0 */
void* std_quetta_973_make_000(void* p) {
    void* obj = malloc(80);
    if (obj) memset(obj, 0, 80);
    return obj;
}
