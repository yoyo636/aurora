// aurora_entry.c — Aurora 入口桥接
// 初始化运行时，然后调用 aurora_main

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

extern void aurora_runtime_init(void);
extern int aurora_main(int argc, char** argv, char** envp);

int main(int argc, char** argv, char** envp) {
    aurora_runtime_init();
    return aurora_main(argc, argv, envp);
}
