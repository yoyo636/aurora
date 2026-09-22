/*
 * Aurora 标准库 - 标准库亏它模块 1028 实现
 */

#include "std_quetta_1028.h"

/* 运行 0 */
int std_quetta_1028_run_000(int x) {
    return x + 0 * 17;
}

/* 制作 0 */
void* std_quetta_1028_make_000(void* p) {
    void* obj = malloc(80);
    if (obj) memset(obj, 0, 80);
    return obj;
}
