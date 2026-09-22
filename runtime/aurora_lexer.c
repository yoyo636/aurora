// aurora_lexer.c — Aurora 词法分析器 (原生版)
// 把 Aurora 源码 token 化

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// Token 类型
typedef enum {
    TOK_EOF,
    TOK_IDENT,       // 标识符
    TOK_INT,         // 整数
    TOK_FLOAT,       // 浮点数
    TOK_STRING,      // 字符串
    TOK_KEYWORD,     // 关键字
    TOK_OP,          // 运算符
    TOK_PUNCT,       // 标点
    TOK_COMMENT      // 注释
} TokenType;

// Token
typedef struct {
    TokenType type;
    char* value;
    int line;
    int col;
} Token;

// 词法分析器状态
typedef struct {
    const char* source;
    int pos;
    int line;
    int col;
    int source_len;
} Lexer;

// 初始化词法分析器
void aurora_lexer_init(Lexer* lex, const char* source) {
    lex->source = source;
    lex->pos = 0;
    lex->line = 1;
    lex->col = 1;
    lex->source_len = strlen(source);
}

// 看当前字符
static char peek(Lexer* lex) {
    if (lex->pos >= lex->source_len) return '\0';
    return lex->source[lex->pos];
}

// 看下一个字符
static char peek_next(Lexer* lex) {
    if (lex->pos + 1 >= lex->source_len) return '\0';
    return lex->source[lex->pos + 1];
}

// 前进
static void advance(Lexer* lex) {
    if (peek(lex) == '\n') {
        lex->line++;
        lex->col = 1;
    } else {
        lex->col++;
    }
    lex->pos++;
}

// 跳过空白
static void skip_whitespace(Lexer* lex) {
    while (peek(lex) == ' ' || peek(lex) == '\t' || peek(lex) == '\n' || peek(lex) == '\r') {
        advance(lex);
    }
}

// 跳过注释
static void skip_comment(Lexer* lex) {
    if (peek(lex) == '/' && peek_next(lex) == '/') {
        while (peek(lex) != '\n' && peek(lex) != '\0') {
            advance(lex);
        }
    }
}

// 读取标识符
static char* read_ident(Lexer* lex) {
    int start = lex->pos;
    while (isalnum(peek(lex)) || peek(lex) == '_') {
        advance(lex);
    }
    int len = lex->pos - start;
    char* result = malloc(len + 1);
    memcpy(result, lex->source + start, len);
    result[len] = '\0';
    return result;
}

// 读取数字
static char* read_number(Lexer* lex) {
    int start = lex->pos;
    int has_dot = 0;
    while (isdigit(peek(lex)) || peek(lex) == '.') {
        if (peek(lex) == '.') has_dot = 1;
        advance(lex);
    }
    int len = lex->pos - start;
    char* result = malloc(len + 1);
    memcpy(result, lex->source + start, len);
    result[len] = '\0';
    return result;
}

// 读取字符串
static char* read_string(Lexer* lex) {
    advance(lex); // 跳过 "
    int start = lex->pos;
    while (peek(lex) != '"' && peek(lex) != '\0') {
        advance(lex);
    }
    int len = lex->pos - start;
    char* result = malloc(len + 1);
    memcpy(result, lex->source + start, len);
    result[len] = '\0';
    advance(lex); // 跳过 "
    return result;
}

// 检查关键字
static int is_keyword(const char* s) {
    return strcmp(s, "fn") == 0 || strcmp(s, "let") == 0 ||
           strcmp(s, "var") == 0 || strcmp(s, "if") == 0 ||
           strcmp(s, "else") == 0 || strcmp(s, "while") == 0 ||
           strcmp(s, "for") == 0 || strcmp(s, "return") == 0 ||
           strcmp(s, "true") == 0 || strcmp(s, "false") == 0 ||
           strcmp(s, "nil") == 0 || strcmp(s, "import") == 0 ||
           strcmp(s, "type") == 0 || strcmp(s, "pub") == 0 ||
           strcmp(s, "break") == 0 || strcmp(s, "continue") == 0;
}

// 获取下一个 token
Token aurora_lexer_next(Lexer* lex) {
    Token tok = {0};
    skip_whitespace(lex);
    skip_comment(lex);

    tok.line = lex->line;
    tok.col = lex->col;

    char c = peek(lex);
    if (c == '\0') {
        tok.type = TOK_EOF;
        tok.value = strdup("");
        return tok;
    }

    // 标识符
    if (isalpha(c) || c == '_') {
        tok.value = read_ident(lex);
        if (is_keyword(tok.value)) {
            tok.type = TOK_KEYWORD;
        } else {
            tok.type = TOK_IDENT;
        }
        return tok;
    }

    // 数字
    if (isdigit(c)) {
        tok.value = read_number(lex);
        if (strchr(tok.value, '.')) {
            tok.type = TOK_FLOAT;
        } else {
            tok.type = TOK_INT;
        }
        return tok;
    }

    // 字符串
    if (c == '"') {
        tok.value = read_string(lex);
        tok.type = TOK_STRING;
        return tok;
    }

    // 运算符
    if (c == '+' || c == '-' || c == '*' || c == '/' || c == '=' ||
        c == '<' || c == '>' || c == '!' || c == '&' || c == '|') {
        int start = lex->pos;
        advance(lex);
        if (peek(lex) == '=') advance(lex);  // ==, <=, >=, !=
        if (peek(lex) == '&') advance(lex);  // &&
        if (peek(lex) == '|') advance(lex);  // ||
        int len = lex->pos - start;
        tok.value = malloc(len + 1);
        memcpy(tok.value, lex->source + start, len);
        tok.value[len] = '\0';
        tok.type = TOK_OP;
        return tok;
    }

    // 标点
    tok.value = malloc(2);
    tok.value[0] = c;
    tok.value[1] = '\0';
    tok.type = TOK_PUNCT;
    advance(lex);
    return tok;
}

// Token 类型转字符串
const char* aurora_token_type_str(TokenType type) {
    switch (type) {
        case TOK_EOF: return "EOF";
        case TOK_IDENT: return "IDENT";
        case TOK_INT: return "INT";
        case TOK_FLOAT: return "FLOAT";
        case TOK_STRING: return "STRING";
        case TOK_KEYWORD: return "KEYWORD";
        case TOK_OP: return "OP";
        case TOK_PUNCT: return "PUNCT";
        case TOK_COMMENT: return "COMMENT";
        default: return "UNKNOWN";
    }
}
