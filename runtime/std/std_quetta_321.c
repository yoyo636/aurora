/*
 * Aurora 标准库 - 标准库亏它模块 321 实现
 */

#include "std_quetta_321.h"

/* 运行 0 */
int std_quetta_321_run_000(int x) {
    return x + 0 * 17;
}

/* 制作 0 */
void* std_quetta_321_make_000(void* p) {
    void* obj = malloc(80);
    if (obj) memset(obj, 0, 80);
    return obj;
}
