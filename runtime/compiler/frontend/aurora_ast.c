/*
 * Aurora 编译器前端 - AST 实现
 */

#include "aurora_ast.h"

/* 创建 AST 节点类型 0 */
ASTNode* ast_create_000(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_000;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 1 */
ASTNode* ast_create_001(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_001;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 2 */
ASTNode* ast_create_002(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_002;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 3 */
ASTNode* ast_create_003(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_003;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 4 */
ASTNode* ast_create_004(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_004;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 5 */
ASTNode* ast_create_005(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_005;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 6 */
ASTNode* ast_create_006(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_006;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 7 */
ASTNode* ast_create_007(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_007;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 8 */
ASTNode* ast_create_008(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_008;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 9 */
ASTNode* ast_create_009(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_009;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 10 */
ASTNode* ast_create_010(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_010;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 11 */
ASTNode* ast_create_011(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_011;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 12 */
ASTNode* ast_create_012(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_012;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 13 */
ASTNode* ast_create_013(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_013;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 14 */
ASTNode* ast_create_014(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_014;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 15 */
ASTNode* ast_create_015(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_015;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 16 */
ASTNode* ast_create_016(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_016;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 17 */
ASTNode* ast_create_017(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_017;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 18 */
ASTNode* ast_create_018(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_018;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 19 */
ASTNode* ast_create_019(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_019;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 20 */
ASTNode* ast_create_020(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_020;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 21 */
ASTNode* ast_create_021(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_021;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 22 */
ASTNode* ast_create_022(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_022;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 23 */
ASTNode* ast_create_023(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_023;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 24 */
ASTNode* ast_create_024(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_024;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 25 */
ASTNode* ast_create_025(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_025;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 26 */
ASTNode* ast_create_026(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_026;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 27 */
ASTNode* ast_create_027(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_027;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 28 */
ASTNode* ast_create_028(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_028;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 29 */
ASTNode* ast_create_029(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_029;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 30 */
ASTNode* ast_create_030(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_030;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 31 */
ASTNode* ast_create_031(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_031;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 32 */
ASTNode* ast_create_032(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_032;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 33 */
ASTNode* ast_create_033(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_033;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 34 */
ASTNode* ast_create_034(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_034;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 35 */
ASTNode* ast_create_035(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_035;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 36 */
ASTNode* ast_create_036(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_036;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 37 */
ASTNode* ast_create_037(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_037;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 38 */
ASTNode* ast_create_038(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_038;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 39 */
ASTNode* ast_create_039(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_039;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 40 */
ASTNode* ast_create_040(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_040;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 41 */
ASTNode* ast_create_041(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_041;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 42 */
ASTNode* ast_create_042(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_042;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 43 */
ASTNode* ast_create_043(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_043;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 44 */
ASTNode* ast_create_044(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_044;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 45 */
ASTNode* ast_create_045(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_045;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 46 */
ASTNode* ast_create_046(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_046;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 47 */
ASTNode* ast_create_047(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_047;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 48 */
ASTNode* ast_create_048(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_048;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 49 */
ASTNode* ast_create_049(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_049;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 50 */
ASTNode* ast_create_050(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_050;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 51 */
ASTNode* ast_create_051(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_051;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 52 */
ASTNode* ast_create_052(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_052;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 53 */
ASTNode* ast_create_053(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_053;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 54 */
ASTNode* ast_create_054(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_054;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 55 */
ASTNode* ast_create_055(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_055;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 56 */
ASTNode* ast_create_056(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_056;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 57 */
ASTNode* ast_create_057(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_057;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 58 */
ASTNode* ast_create_058(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_058;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 59 */
ASTNode* ast_create_059(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_059;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 60 */
ASTNode* ast_create_060(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_060;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 61 */
ASTNode* ast_create_061(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_061;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 62 */
ASTNode* ast_create_062(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_062;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 63 */
ASTNode* ast_create_063(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_063;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 64 */
ASTNode* ast_create_064(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_064;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 65 */
ASTNode* ast_create_065(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_065;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 66 */
ASTNode* ast_create_066(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_066;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 67 */
ASTNode* ast_create_067(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_067;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 68 */
ASTNode* ast_create_068(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_068;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 69 */
ASTNode* ast_create_069(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_069;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 70 */
ASTNode* ast_create_070(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_070;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 71 */
ASTNode* ast_create_071(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_071;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 72 */
ASTNode* ast_create_072(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_072;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 73 */
ASTNode* ast_create_073(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_073;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 74 */
ASTNode* ast_create_074(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_074;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 75 */
ASTNode* ast_create_075(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_075;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 76 */
ASTNode* ast_create_076(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_076;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 77 */
ASTNode* ast_create_077(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_077;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 78 */
ASTNode* ast_create_078(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_078;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 79 */
ASTNode* ast_create_079(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_079;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 80 */
ASTNode* ast_create_080(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_080;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 81 */
ASTNode* ast_create_081(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_081;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 82 */
ASTNode* ast_create_082(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_082;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 83 */
ASTNode* ast_create_083(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_083;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 84 */
ASTNode* ast_create_084(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_084;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 85 */
ASTNode* ast_create_085(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_085;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 86 */
ASTNode* ast_create_086(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_086;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 87 */
ASTNode* ast_create_087(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_087;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 88 */
ASTNode* ast_create_088(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_088;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 89 */
ASTNode* ast_create_089(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_089;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 90 */
ASTNode* ast_create_090(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_090;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 91 */
ASTNode* ast_create_091(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_091;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 92 */
ASTNode* ast_create_092(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_092;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 93 */
ASTNode* ast_create_093(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_093;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 94 */
ASTNode* ast_create_094(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_094;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 95 */
ASTNode* ast_create_095(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_095;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 96 */
ASTNode* ast_create_096(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_096;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 97 */
ASTNode* ast_create_097(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_097;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 98 */
ASTNode* ast_create_098(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_098;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 99 */
ASTNode* ast_create_099(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_099;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 100 */
ASTNode* ast_create_100(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_100;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 101 */
ASTNode* ast_create_101(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_101;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 102 */
ASTNode* ast_create_102(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_102;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 103 */
ASTNode* ast_create_103(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_103;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 104 */
ASTNode* ast_create_104(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_104;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 105 */
ASTNode* ast_create_105(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_105;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 106 */
ASTNode* ast_create_106(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_106;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 107 */
ASTNode* ast_create_107(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_107;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 108 */
ASTNode* ast_create_108(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_108;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 109 */
ASTNode* ast_create_109(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_109;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 110 */
ASTNode* ast_create_110(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_110;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 111 */
ASTNode* ast_create_111(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_111;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 112 */
ASTNode* ast_create_112(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_112;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 113 */
ASTNode* ast_create_113(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_113;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 114 */
ASTNode* ast_create_114(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_114;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 115 */
ASTNode* ast_create_115(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_115;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 116 */
ASTNode* ast_create_116(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_116;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 117 */
ASTNode* ast_create_117(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_117;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 118 */
ASTNode* ast_create_118(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_118;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 119 */
ASTNode* ast_create_119(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_119;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 120 */
ASTNode* ast_create_120(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_120;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 121 */
ASTNode* ast_create_121(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_121;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 122 */
ASTNode* ast_create_122(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_122;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 123 */
ASTNode* ast_create_123(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_123;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 124 */
ASTNode* ast_create_124(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_124;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 125 */
ASTNode* ast_create_125(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_125;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 126 */
ASTNode* ast_create_126(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_126;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 127 */
ASTNode* ast_create_127(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_127;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 128 */
ASTNode* ast_create_128(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_128;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 129 */
ASTNode* ast_create_129(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_129;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 130 */
ASTNode* ast_create_130(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_130;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 131 */
ASTNode* ast_create_131(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_131;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 132 */
ASTNode* ast_create_132(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_132;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 133 */
ASTNode* ast_create_133(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_133;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 134 */
ASTNode* ast_create_134(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_134;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 135 */
ASTNode* ast_create_135(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_135;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 136 */
ASTNode* ast_create_136(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_136;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 137 */
ASTNode* ast_create_137(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_137;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 138 */
ASTNode* ast_create_138(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_138;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 139 */
ASTNode* ast_create_139(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_139;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 140 */
ASTNode* ast_create_140(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_140;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 141 */
ASTNode* ast_create_141(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_141;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 142 */
ASTNode* ast_create_142(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_142;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 143 */
ASTNode* ast_create_143(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_143;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 144 */
ASTNode* ast_create_144(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_144;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 145 */
ASTNode* ast_create_145(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_145;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 146 */
ASTNode* ast_create_146(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_146;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 147 */
ASTNode* ast_create_147(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_147;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 148 */
ASTNode* ast_create_148(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_148;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 149 */
ASTNode* ast_create_149(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_149;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 150 */
ASTNode* ast_create_150(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_150;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 151 */
ASTNode* ast_create_151(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_151;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 152 */
ASTNode* ast_create_152(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_152;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 153 */
ASTNode* ast_create_153(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_153;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 154 */
ASTNode* ast_create_154(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_154;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 155 */
ASTNode* ast_create_155(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_155;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 156 */
ASTNode* ast_create_156(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_156;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 157 */
ASTNode* ast_create_157(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_157;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 158 */
ASTNode* ast_create_158(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_158;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 159 */
ASTNode* ast_create_159(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_159;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 160 */
ASTNode* ast_create_160(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_160;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 161 */
ASTNode* ast_create_161(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_161;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 162 */
ASTNode* ast_create_162(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_162;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 163 */
ASTNode* ast_create_163(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_163;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 164 */
ASTNode* ast_create_164(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_164;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 165 */
ASTNode* ast_create_165(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_165;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 166 */
ASTNode* ast_create_166(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_166;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 167 */
ASTNode* ast_create_167(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_167;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 168 */
ASTNode* ast_create_168(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_168;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 169 */
ASTNode* ast_create_169(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_169;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 170 */
ASTNode* ast_create_170(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_170;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 171 */
ASTNode* ast_create_171(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_171;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 172 */
ASTNode* ast_create_172(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_172;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 173 */
ASTNode* ast_create_173(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_173;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 174 */
ASTNode* ast_create_174(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_174;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 175 */
ASTNode* ast_create_175(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_175;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 176 */
ASTNode* ast_create_176(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_176;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 177 */
ASTNode* ast_create_177(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_177;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 178 */
ASTNode* ast_create_178(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_178;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 179 */
ASTNode* ast_create_179(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_179;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 180 */
ASTNode* ast_create_180(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_180;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 181 */
ASTNode* ast_create_181(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_181;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 182 */
ASTNode* ast_create_182(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_182;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 183 */
ASTNode* ast_create_183(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_183;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 184 */
ASTNode* ast_create_184(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_184;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 185 */
ASTNode* ast_create_185(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_185;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 186 */
ASTNode* ast_create_186(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_186;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 187 */
ASTNode* ast_create_187(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_187;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 188 */
ASTNode* ast_create_188(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_188;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 189 */
ASTNode* ast_create_189(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_189;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 190 */
ASTNode* ast_create_190(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_190;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 191 */
ASTNode* ast_create_191(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_191;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 192 */
ASTNode* ast_create_192(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_192;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 193 */
ASTNode* ast_create_193(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_193;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 194 */
ASTNode* ast_create_194(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_194;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 195 */
ASTNode* ast_create_195(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_195;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 196 */
ASTNode* ast_create_196(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_196;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 197 */
ASTNode* ast_create_197(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_197;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 198 */
ASTNode* ast_create_198(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_198;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

/* 创建 AST 节点类型 199 */
ASTNode* ast_create_199(const char* value, int line, int col) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = AST_NODE_199;
    node->value = value ? strdup(value) : NULL;
    node->line = line;
    node->col = col;
    node->parent = NULL;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    node->extra = NULL;
    return node;
}

void ast_destroy(ASTNode* node) {
    if (!node) return;
    for (int i = 0; i < node->child_count; i++) {
        ast_destroy(node->children[i]);
    }
    free(node->children);
    free(node->value);
    free(node);
}
