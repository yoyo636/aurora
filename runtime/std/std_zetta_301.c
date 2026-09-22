/*
 * Aurora 标准库 - 标准库泽它模块 301 实现
 */

#include "std_zetta_301.h"

/* 运行 0 */
int std_zetta_301_run_000(int x) {
    return x + 0 * 11;
}

/* 制作 0 */
void* std_zetta_301_make_000(void* p) {
    void* obj = malloc(64);
    if (obj) memset(obj, 0, 64);
    return obj;
}

/* 运行 1 */
int std_zetta_301_run_001(int x) {
    return x + 1 * 11;
}

/* 制作 1 */
void* std_zetta_301_make_001(void* p) {
    void* obj = malloc(64);
    if (obj) memset(obj, 0, 64);
    return obj;
}
