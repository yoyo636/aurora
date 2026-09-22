// aurora_parser.c — Aurora 语法分析器 (原生版)
// 把 token 流解析成 AST

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

// AST 节点类型
typedef enum {
    AST_PROGRAM,
    AST_FN_DEF,
    AST_LET,
    AST_VAR,
    AST_IF,
    AST_WHILE,
    AST_FOR,
    AST_RETURN,
    AST_BINARY,
    AST_UNARY,
    AST_CALL,
    AST_INT_LIT,
    AST_FLOAT_LIT,
    AST_STR_LIT,
    AST_IDENT,
    AST_LIST,
    AST_DICT,
    AST_INDEX,
    AST_ASSIGN
} AstType;

// AST 节点
typedef struct AstNode {
    AstType type;
    char* str_val;
    int64_t int_val;
    double float_val;
    char* op;
    struct AstNode** children;
    int child_count;
    int line;
} AstNode;

// Token 类型
typedef enum {
    TOK_EOF, TOK_IDENT, TOK_INT, TOK_FLOAT, TOK_STRING,
    TOK_KEYWORD, TOK_OP, TOK_PUNCT
} TokenType;

typedef struct {
    TokenType type;
    char* value;
    int line;
    int col;
} Token;

// 解析器状态
typedef struct {
    Token* tokens;
    int pos;
    int count;
} Parser;

// 创建 AST 节点
static AstNode* ast_node(AstType type, int line) {
    AstNode* n = calloc(1, sizeof(AstNode));
    n->type = type;
    n->line = line;
    return n;
}

// 添加子节点
static void ast_add_child(AstNode* parent, AstNode* child) {
    parent->child_count++;
    parent->children = realloc(parent->children,
        sizeof(AstNode*) * parent->child_count);
    parent->children[parent->child_count - 1] = child;
}

// 初始化解析器
void aurora_parser_init(Parser* p, Token* tokens, int count) {
    p->tokens = tokens;
    p->pos = 0;
    p->count = count;
}

// 看当前 token
static Token* peek(Parser* p) {
    if (p->pos >= p->count) return &p->tokens[p->count - 1];
    return &p->tokens[p->pos];
}

// 看下一个 token
static Token* peek_next(Parser* p) {
    if (p->pos + 1 >= p->count) return &p->tokens[p->count - 1];
    return &p->tokens[p->pos + 1];
}

// 前进
static Token* advance(Parser* p) {
    Token* t = &p->tokens[p->pos];
    if (p->pos < p->count - 1) p->pos++;
    return t;
}

// 期望 token
static int expect(Parser* p, TokenType type, const char* value) {
    Token* t = peek(p);
    if (t->type != type) return 0;
    if (value && strcmp(t->value, value) != 0) return 0;
    advance(p);
    return 1;
}

// 检查关键字
static int check_keyword(Parser* p, const char* kw) {
    return peek(p)->type == TOK_KEYWORD &&
           strcmp(peek(p)->value, kw) == 0;
}

// 解析表达式（简化版：优先级从低到高）
static AstNode* parse_expr(Parser* p);
static AstNode* parse_stmt(Parser* p);

// 解析主键
static AstNode* parse_primary(Parser* p) {
    Token* t = peek(p);

    if (t->type == TOK_INT) {
        advance(p);
        AstNode* n = ast_node(AST_INT_LIT, t->line);
        n->int_val = atoll(t->value);
        return n;
    }

    if (t->type == TOK_FLOAT) {
        advance(p);
        AstNode* n = ast_node(AST_FLOAT_LIT, t->line);
        n->float_val = atof(t->value);
        return n;
    }

    if (t->type == TOK_STRING) {
        advance(p);
        AstNode* n = ast_node(AST_STR_LIT, t->line);
        n->str_val = strdup(t->value);
        return n;
    }

    if (t->type == TOK_IDENT) {
        advance(p);
        AstNode* n = ast_node(AST_IDENT, t->line);
        n->str_val = strdup(t->value);

        // 函数调用
        if (peek(p)->type == TOK_PUNCT && strcmp(peek(p)->value, "(") == 0) {
            advance(p);
            AstNode* call = ast_node(AST_CALL, t->line);
            call->str_val = n->str_val;
            free(n);

            while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, ")") != 0) {
                ast_add_child(call, parse_expr(p));
                if (peek(p)->type == TOK_PUNCT && strcmp(peek(p)->value, ",") == 0) {
                    advance(p);
                }
            }
            advance(p); // )
            return call;
        }

        return n;
    }

    // 括号表达式
    if (t->type == TOK_PUNCT && strcmp(t->value, "(") == 0) {
        advance(p);
        AstNode* e = parse_expr(p);
        expect(p, TOK_PUNCT, ")");
        return e;
    }

    // 列表字面量
    if (t->type == TOK_PUNCT && strcmp(t->value, "[") == 0) {
        advance(p);
        AstNode* list = ast_node(AST_LIST, t->line);
        while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, "]") != 0) {
            ast_add_child(list, parse_expr(p));
            if (peek(p)->type == TOK_PUNCT && strcmp(peek(p)->value, ",") == 0) {
                advance(p);
            }
        }
        advance(p);
        return list;
    }

    return ast_node(AST_INT_LIT, t->line);
}

// 乘除
static AstNode* parse_mul(Parser* p) {
    AstNode* left = parse_primary(p);
    while (peek(p)->type == TOK_OP &&
           (strcmp(peek(p)->value, "*") == 0 || strcmp(peek(p)->value, "/") == 0)) {
        Token* op = advance(p);
        AstNode* right = parse_primary(p);
        AstNode* bin = ast_node(AST_BINARY, op->line);
        bin->str_val = strdup(op->value);
        ast_add_child(bin, left);
        ast_add_child(bin, right);
        left = bin;
    }
    return left;
}

// 加减
static AstNode* parse_add(Parser* p) {
    AstNode* left = parse_mul(p);
    while (peek(p)->type == TOK_OP &&
           (strcmp(peek(p)->value, "+") == 0 || strcmp(peek(p)->value, "-") == 0)) {
        Token* op = advance(p);
        AstNode* right = parse_mul(p);
        AstNode* bin = ast_node(AST_BINARY, op->line);
        bin->str_val = strdup(op->value);
        ast_add_child(bin, left);
        ast_add_child(bin, right);
        left = bin;
    }
    return left;
}

// 比较
static AstNode* parse_cmp(Parser* p) {
    AstNode* left = parse_add(p);
    while (peek(p)->type == TOK_OP &&
           (strcmp(peek(p)->value, "==") == 0 || strcmp(peek(p)->value, "!=") == 0 ||
            strcmp(peek(p)->value, "<") == 0 || strcmp(peek(p)->value, ">") == 0 ||
            strcmp(peek(p)->value, "<=") == 0 || strcmp(peek(p)->value, ">=") == 0)) {
        Token* op = advance(p);
        AstNode* right = parse_add(p);
        AstNode* bin = ast_node(AST_BINARY, op->line);
        bin->str_val = strdup(op->value);
        ast_add_child(bin, left);
        ast_add_child(bin, right);
        left = bin;
    }
    return left;
}

// 逻辑与
static AstNode* parse_and(Parser* p) {
    AstNode* left = parse_cmp(p);
    while (peek(p)->type == TOK_OP && strcmp(peek(p)->value, "&&") == 0) {
        Token* op = advance(p);
        AstNode* right = parse_cmp(p);
        AstNode* bin = ast_node(AST_BINARY, op->line);
        bin->str_val = strdup("and");
        ast_add_child(bin, left);
        ast_add_child(bin, right);
        left = bin;
    }
    return left;
}

// 逻辑或
static AstNode* parse_or(Parser* p) {
    AstNode* left = parse_and(p);
    while (peek(p)->type == TOK_OP && strcmp(peek(p)->value, "||") == 0) {
        Token* op = advance(p);
        AstNode* right = parse_and(p);
        AstNode* bin = ast_node(AST_BINARY, op->line);
        bin->str_val = strdup("or");
        ast_add_child(bin, left);
        ast_add_child(bin, right);
        left = bin;
    }
    return left;
}

static AstNode* parse_expr(Parser* p) {
    return parse_or(p);
}

// 解析语句
static AstNode* parse_stmt(Parser* p) {
    Token* t = peek(p);

    // let
    if (check_keyword(p, "let")) {
        advance(p);
        Token* name = advance(p);
        AstNode* n = ast_node(AST_LET, t->line);
        n->str_val = strdup(name->value);
        if (expect(p, TOK_OP, "=")) {
            ast_add_child(n, parse_expr(p));
        }
        return n;
    }

    // var
    if (check_keyword(p, "var")) {
        advance(p);
        Token* name = advance(p);
        AstNode* n = ast_node(AST_VAR, t->line);
        n->str_val = strdup(name->value);
        if (expect(p, TOK_OP, "=")) {
            ast_add_child(n, parse_expr(p));
        }
        return n;
    }

    // fn
    if (check_keyword(p, "fn")) {
        advance(p);
        Token* name = advance(p);
        AstNode* n = ast_node(AST_FN_DEF, t->line);
        n->str_val = strdup(name->value);

        expect(p, TOK_PUNCT, "(");
        // 参数（简化版：跳过）
        while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, ")") != 0) {
            advance(p);
        }
        expect(p, TOK_PUNCT, ")");
        expect(p, TOK_PUNCT, "{");

        while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, "}") != 0) {
            ast_add_child(n, parse_stmt(p));
        }
        expect(p, TOK_PUNCT, "}");
        return n;
    }

    // if
    if (check_keyword(p, "if")) {
        advance(p);
        AstNode* n = ast_node(AST_IF, t->line);
        ast_add_child(n, parse_expr(p));
        expect(p, TOK_PUNCT, "{");
        while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, "}") != 0) {
            ast_add_child(n, parse_stmt(p));
        }
        expect(p, TOK_PUNCT, "}");

        if (check_keyword(p, "else")) {
            advance(p);
            expect(p, TOK_PUNCT, "{");
            while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, "}") != 0) {
                ast_add_child(n, parse_stmt(p));
            }
            expect(p, TOK_PUNCT, "}");
        }
        return n;
    }

    // while
    if (check_keyword(p, "while")) {
        advance(p);
        AstNode* n = ast_node(AST_WHILE, t->line);
        ast_add_child(n, parse_expr(p));
        expect(p, TOK_PUNCT, "{");
        while (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, "}") != 0) {
            ast_add_child(n, parse_stmt(p));
        }
        expect(p, TOK_PUNCT, "}");
        return n;
    }

    // return
    if (check_keyword(p, "return")) {
        advance(p);
        AstNode* n = ast_node(AST_RETURN, t->line);
        if (peek(p)->type != TOK_PUNCT || strcmp(peek(p)->value, ";") != 0) {
            ast_add_child(n, parse_expr(p));
        }
        return n;
    }

    // 表达式语句
    return parse_expr(p);
}

// 解析整个程序
AstNode* aurora_parse_program(Parser* p) {
    AstNode* program = ast_node(AST_PROGRAM, 1);
    while (peek(p)->type != TOK_EOF) {
        ast_add_child(program, parse_stmt(p));
    }
    return program;
}

// AST 类型转字符串
const char* aurora_ast_type_str(AstType type) {
    switch (type) {
        case AST_PROGRAM: return "Program";
        case AST_FN_DEF: return "FnDef";
        case AST_LET: return "Let";
        case AST_VAR: return "Var";
        case AST_IF: return "If";
        case AST_WHILE: return "While";
        case AST_FOR: return "For";
        case AST_RETURN: return "Return";
        case AST_BINARY: return "Binary";
        case AST_UNARY: return "Unary";
        case AST_CALL: return "Call";
        case AST_INT_LIT: return "IntLit";
        case AST_FLOAT_LIT: return "FloatLit";
        case AST_STR_LIT: return "StrLit";
        case AST_IDENT: return "Ident";
        case AST_LIST: return "List";
        case AST_DICT: return "Dict";
        case AST_INDEX: return "Index";
        case AST_ASSIGN: return "Assign";
        default: return "Unknown";
    }
}
