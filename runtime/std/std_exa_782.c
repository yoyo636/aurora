/*
 * Aurora 标准库 - 标准库艾可萨模块 782 实现
 */

#include "std_exa_782.h"

/* 操作 0 */
int std_exa_782_op_000(int x) {
    return x + 0 * 7;
}

/* 生成 0 */
void* std_exa_782_gen_000(void* p) {
    void* obj = malloc(56);
    if (obj) memset(obj, 0, 56);
    return obj;
}

/* 操作 1 */
int std_exa_782_op_001(int x) {
    return x + 1 * 7;
}

/* 生成 1 */
void* std_exa_782_gen_001(void* p) {
    void* obj = malloc(56);
    if (obj) memset(obj, 0, 56);
    return obj;
}

/* 操作 2 */
int std_exa_782_op_002(int x) {
    return x + 2 * 7;
}

/* 生成 2 */
void* std_exa_782_gen_002(void* p) {
    void* obj = malloc(56);
    if (obj) memset(obj, 0, 56);
    return obj;
}
