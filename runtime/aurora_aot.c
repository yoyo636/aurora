// aurora_aot.c — Aurora AOT 编译器 v2.0
// 生成 ARM64 汇编，调用 as/ld 生成原生可执行文件
// 支持: 变量声明、整数运算、println、if/while、函数定义与调用

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#include <stdarg.h>

// ============ 词法分析 ============

typedef struct { const char* src; int pos; int line; int len; } Lexer;

enum { TK_EOF, TK_IDENT, TK_INT, TK_STR, TK_KW, TK_OP, TK_PUN };

typedef struct { int type; char val[256]; int line; } Token;

static char lpeek(Lexer* l) { return l->pos < l->len ? l->src[l->pos] : '\0'; }
static void ladv(Lexer* l) { if (lpeek(l) == '\n') l->line++; l->pos++; }

static void lskip(Lexer* l) {
    while (lpeek(l)==' '||lpeek(l)=='\t'||lpeek(l)=='\n'||lpeek(l)=='\r') ladv(l);
    if (lpeek(l)=='/' && l->pos+1<l->len && l->src[l->pos+1]=='/')
        while (lpeek(l)!='\n'&&lpeek(l)!='\0') ladv(l);
}

static int is_kw(const char* s) {
    return !strcmp(s,"fn")||!strcmp(s,"let")||!strcmp(s,"var")||
           !strcmp(s,"if")||!strcmp(s,"else")||!strcmp(s,"while")||
           !strcmp(s,"for")||!strcmp(s,"return")||!strcmp(s,"true")||
           !strcmp(s,"false")||!strcmp(s,"in");
}

static Token next_tok(Lexer* l) {
    Token t = {0};
    lskip(l);
    t.line = l->line;
    char c = lpeek(l);
    if (c == '\0') { t.type = TK_EOF; return t; }

    if (isalpha(c) || c=='_') {
        int s = l->pos;
        while (isalnum(lpeek(l))||lpeek(l)=='_') ladv(l);
        int n = l->pos-s; if (n>255) n=255;
        memcpy(t.val, l->src+s, n); t.val[n]=0;
        t.type = is_kw(t.val) ? TK_KW : TK_IDENT;
        return t;
    }

    if (isdigit(c)) {
        int s = l->pos;
        while (isdigit(lpeek(l))) ladv(l);
        int n = l->pos-s;
        memcpy(t.val, l->src+s, n); t.val[n]=0;
        t.type = TK_INT;
        return t;
    }

    if (c=='"') {
        ladv(l);
        int s = l->pos;
        while (lpeek(l)!='"'&&lpeek(l)!='\0') ladv(l);
        int n = l->pos-s; if (n>255) n=255;
        memcpy(t.val, l->src+s, n); t.val[n]=0;
        ladv(l);
        t.type = TK_STR;
        return t;
    }

    if (strchr("+-*/%=!<>&|", c)) {
        int s = l->pos;
        ladv(l);
        if (lpeek(l)=='='&&strchr("=!<>&|",c)) ladv(l);
        int n = l->pos-s;
        memcpy(t.val, l->src+s, n); t.val[n]=0;
        t.type = TK_OP;
        return t;
    }

    t.val[0] = c; t.val[1] = 0;
    t.type = TK_PUN;
    ladv(l);
    return t;
}

// ============ Token 缓冲 ============

static Token g_toks[16384];
static int g_ntok = 0;
static int g_tok_pos = 0;

static Token cur_tok()  { return g_toks[g_tok_pos]; }
static Token peek_tok() { return g_toks[g_tok_pos + 1]; }
static void adv_tok()  { if (g_tok_pos < g_ntok) g_tok_pos++; }

// ============ 符号表 ============

#define MAX_SYMBOLS 256
#define MAX_FUNCS 64

typedef struct { char name[64]; int offset; } Symbol;
static Symbol g_symbols[MAX_SYMBOLS];
static int g_symbol_count = 0;
static int g_stack_offset = 0;

// 函数表
typedef struct { char name[64]; int param_count; } Func;
static Func g_funcs[MAX_FUNCS];
static int g_func_count = 0;

static int find_func(const char* name) {
    for (int i = 0; i < g_func_count; i++)
        if (strcmp(g_funcs[i].name, name) == 0) return i;
    return -1;
}

static int find_symbol(const char* name) {
    for (int i = 0; i < g_symbol_count; i++)
        if (strcmp(g_symbols[i].name, name) == 0) return g_symbols[i].offset;
    return -1;
}

static int add_symbol(const char* name) {
    int off = find_symbol(name);
    if (off >= 0) return off;
    if (g_symbol_count < MAX_SYMBOLS) {
        strncpy(g_symbols[g_symbol_count].name, name, 63);
        g_stack_offset += 8;
        g_symbols[g_symbol_count].offset = g_stack_offset;
        g_symbol_count++;
        return g_stack_offset;
    }
    return 0;
}

// ============ 汇编输出 ============

static FILE* g_out = NULL;
static int g_label_id = 0;

static void emit(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vfprintf(g_out, fmt, args);
    va_end(args);
    fprintf(g_out, "\n");
}

static int new_label(void) { return g_label_id++; }

// ============ 代码生成 ============

// 生成表达式：结果放在 x0
static void gen_expr(void);

// 加载变量到 x0
static void gen_load(const char* name) {
    int off = find_symbol(name);
    if (off >= 0) {
        emit("    ldr x0, [x29, #-%d]", off);
    } else {
        emit("    mov x0, #0");
    }
}

// 保存 x0 到变量
static void gen_store(const char* name) {
    int off = add_symbol(name);
    emit("    str x0, [x29, #-%d]", off);
}

// 乘除模
static void gen_mul(void) {
    // 左操作数
    Token t = cur_tok();
    if (t.type == TK_INT) {
        adv_tok();
        emit("    mov x0, #%s", t.val);
    } else if (t.type == TK_IDENT) {
        adv_tok();
        gen_load(t.val);
    } else if (t.type == TK_PUN && t.val[0] == '(') {
        adv_tok();
        gen_expr();
        adv_tok();
    } else {
        emit("    mov x0, #0");
        adv_tok();
    }

    while (cur_tok().type == TK_OP &&
           (!strcmp(cur_tok().val,"*") || !strcmp(cur_tok().val,"/") || !strcmp(cur_tok().val,"%"))) {
        char op[8]; strcpy(op, cur_tok().val);
        adv_tok();

        // 保存左操作数到 x3（不覆盖外层的 x1）
        emit("    mov x3, x0");

        // 加载右操作数到 x0
        Token rt = cur_tok();
        if (rt.type == TK_INT) {
            adv_tok();
            emit("    mov x0, #%s", rt.val);
        } else if (rt.type == TK_IDENT) {
            adv_tok();
            int off = find_symbol(rt.val);
            if (off >= 0) {
                emit("    ldr x0, [x29, #-%d]", off);
            } else {
                emit("    mov x0, #0");
            }
        } else {
            emit("    mov x0, #0");
            adv_tok();
        }

        if (!strcmp(op,"*")) emit("    mul x0, x3, x0");
        else if (!strcmp(op,"/")) emit("    udiv x0, x3, x0");
        else if (!strcmp(op,"%")) {
            emit("    udiv x1, x3, x0");
            emit("    msub x0, x1, x0, x3");
        }
    }
}

// 加减
static void gen_add(void) {
    gen_mul();

    while (cur_tok().type == TK_OP &&
           (!strcmp(cur_tok().val,"+") || !strcmp(cur_tok().val,"-"))) {
        char op[8]; strcpy(op, cur_tok().val);
        adv_tok();

        emit("    mov x1, x0");
        gen_mul();

        if (!strcmp(op,"+")) emit("    add x0, x1, x0");
        else emit("    sub x0, x1, x0");
    }
}

// 比较
static void gen_cmp(void) {
    gen_add();

    while (cur_tok().type == TK_OP &&
           (!strcmp(cur_tok().val,"==") || !strcmp(cur_tok().val,"!=") ||
            !strcmp(cur_tok().val,"<") || !strcmp(cur_tok().val,">") ||
            !strcmp(cur_tok().val,"<=") || !strcmp(cur_tok().val,">="))) {
        char op[8]; strcpy(op, cur_tok().val);
        adv_tok();

        emit("    mov x1, x0");
        gen_add();

        emit("    cmp x1, x0");
        emit("    cset x0, %s",
             !strcmp(op,"==") ? "eq" :
             !strcmp(op,"!=") ? "ne" :
             !strcmp(op,"<")  ? "lt" :
             !strcmp(op,">")  ? "gt" :
             !strcmp(op,"<=") ? "le" : "ge");
    }
}

static void gen_expr(void) {
    gen_cmp();
}

// 生成 println（整数）
static void gen_println(void) {
    // x0 已经是要打印的值
    // macOS arm64: 可变参数放在栈上 [sp]
    emit("    str x0, [sp]");  // 值放 [sp]
    emit("    adrp x0, l_.int_fmt@PAGE");
    emit("    add x0, x0, l_.int_fmt@PAGEOFF");
    emit("    bl _printf");
}

// 生成 print_str（字符串）
static int g_str_count = 0;
static void gen_print_str(const char* str) {
    char label[32];
    snprintf(label, sizeof(label), "l_.str_%d", g_str_count++);
    
    // 打印字符串
    emit("    adrp x0, %s@PAGE", label);
    emit("    add x0, x0, %s@PAGEOFF", label);
    emit("    bl _puts");
}

// 函数调用: name(args)
static void gen_func_call(const char* name) {
    int fi = find_func(name);
    if (fi < 0) {
        // 未知函数，默认返回 0
        emit("    mov x0, #0");
        return;
    }
    
    // 调用函数（简化：不传递参数）
    emit("    bl _func_%s", name);
}

// 生成语句
static void gen_stmt(void) {
    Token t = cur_tok();

    // 函数定义: fn name(params) { body }
    if (t.type == TK_KW && !strcmp(t.val,"fn")) {
        adv_tok();
        Token fname = cur_tok();
        adv_tok();  // 跳过函数名
        adv_tok();  // 跳过 (
        // 跳过参数列表
        while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == ')')) adv_tok();
        adv_tok();  // 跳过 )
        adv_tok();  // 跳过 {
        
        // 生成函数标签
        emit("_func_%s:", fname.val);
        
        // 函数体
        while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == '}')) {
            gen_stmt();
        }
        adv_tok();  // 跳过 }
        
        // 函数返回
        emit("    ret");
        return;
    }

    // println（优先处理，不被函数调用拦截）
    if (t.type == TK_IDENT && !strcmp(t.val, "println")) {
        adv_tok();
        adv_tok();  // 跳过 (
        gen_expr();
        adv_tok();  // 跳过 )
        gen_println();
        return;
    }

    // 函数调用: name(args)
    if (t.type == TK_IDENT && peek_tok().type == TK_PUN && peek_tok().val[0] == '(') {
        char fname[64]; strncpy(fname, t.val, 63);
        adv_tok();
        adv_tok();  // 跳过 (
        
        // 跳过参数（简化）
        while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == ')')) adv_tok();
        adv_tok();  // 跳过 )
        
        gen_func_call(fname);
        return;
    }

    // let/var 声明
    if (t.type == TK_KW && (!strcmp(t.val,"let") || !strcmp(t.val,"var"))) {
        adv_tok();
        Token name = cur_tok();
        adv_tok();
        adv_tok();  // 跳过 =
        gen_expr();
        gen_store(name.val);
        return;
    }

    // 赋值
    if (t.type == TK_IDENT && peek_tok().type == TK_OP && strcmp(peek_tok().val,"=")==0) {
        adv_tok();
        adv_tok();  // 跳过 =
        gen_expr();
        gen_store(t.val);
        return;
    }

    // if 语句
    if (t.type == TK_KW && !strcmp(t.val,"if")) {
        adv_tok();
        gen_expr();  // 条件

        int else_label = new_label();
        int end_label = new_label();

        emit("    cbz x0, L%d", else_label);

        // if 块
        adv_tok();  // 跳过 {
        while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == '}')) {
            gen_stmt();
        }
        adv_tok();  // 跳过 }

        emit("    b L%d", end_label);

        // else 块
        emit("L%d:", else_label);
        if (cur_tok().type == TK_KW && !strcmp(cur_tok().val,"else")) {
            adv_tok();
            adv_tok();  // 跳过 {
            while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == '}')) {
                gen_stmt();
            }
            adv_tok();  // 跳过 }
        }

        emit("L%d:", end_label);
        return;
    }

    // while 循环
    if (t.type == TK_KW && !strcmp(t.val,"while")) {
        int start_label = new_label();
        int end_label = new_label();

        emit("L%d:", start_label);
        adv_tok();
        gen_expr();  // 条件

        emit("    cbz x0, L%d", end_label);

        adv_tok();  // 跳过 {
        while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == '}')) {
            gen_stmt();
        }
        adv_tok();  // 跳过 }

        emit("    b L%d", start_label);
        emit("L%d:", end_label);
        return;
    }

    // 跳过其他
    adv_tok();
}

// ============ 主入口 ============

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr, "用法: %s <input.aur> <output.s>\n", argv[0]);
        return 1;
    }

    // 读取源文件
    FILE* f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "错误: 无法打开 %s\n", argv[1]); return 1; }
    fseek(f, 0, SEEK_END);
    int fsize = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* src = malloc(fsize + 1);
    fread(src, 1, fsize, f);
    src[fsize] = '\0';
    fclose(f);

    // 词法分析
    Lexer l = {src, 0, 1, fsize};
    while (1) {
        Token t = next_tok(&l);
        if (t.type == TK_EOF) break;
        if (g_ntok < 16384) g_toks[g_ntok++] = t;
    }
    Token eof = {TK_EOF, "", 0};
    g_toks[g_ntok++] = eof;

    // 预扫描：计算变量和函数
    g_symbol_count = 0;
    g_stack_offset = 0;
    g_func_count = 0;
    
    for (int i = 0; i < g_ntok; i++) {
        // 收集函数
        if (g_toks[i].type == TK_KW && !strcmp(g_toks[i].val,"fn")) {
            if (i+1 < g_ntok && g_toks[i+1].type == TK_IDENT && g_func_count < MAX_FUNCS) {
                strncpy(g_funcs[g_func_count].name, g_toks[i+1].val, 63);
                g_funcs[g_func_count].param_count = 0;
                g_func_count++;
            }
        }
        // 收集变量
        if (g_toks[i].type == TK_KW && (!strcmp(g_toks[i].val,"let") || !strcmp(g_toks[i].val,"var"))) {
            if (i+1 < g_ntok && g_toks[i+1].type == TK_IDENT) {
                add_symbol(g_toks[i+1].val);
            }
        }
    }

    // 打开输出
    g_out = fopen(argv[2], "w");
    if (!g_out) { fprintf(stderr, "错误: 无法创建 %s\n", argv[2]); return 1; }

    // 生成汇编头
    emit(".section __TEXT,__text,regular,pure_instructions");

    // 生成所有函数定义（在 main 之前）
    g_tok_pos = 0;
    while (g_tok_pos < g_ntok && cur_tok().type != TK_EOF) {
        if (cur_tok().type == TK_KW && !strcmp(cur_tok().val,"fn")) {
            // 函数定义
            adv_tok();  // 跳过 fn
            Token fname = cur_tok();
            adv_tok();  // 跳过函数名
            adv_tok();  // 跳过 (
            while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == ')')) adv_tok();
            adv_tok();  // 跳过 )
            adv_tok();  // 跳过 {
            
            emit("_func_%s:", fname.val);
            emit("    stp x29, x30, [sp, #-16]!");
            emit("    mov x29, sp");
            emit("    sub sp, sp, #32");  // 函数栈空间
            
            while (!(cur_tok().type == TK_PUN && cur_tok().val[0] == '}')) {
                gen_stmt();
            }
            adv_tok();  // 跳过 }
            
            emit("    add sp, sp, #32");  // 恢复栈
            emit("    ldp x29, x30, [sp], #16");
            emit("    ret");
        } else {
            // 其他语句，先跳过（main 里再生成）
            break;
        }
    }

    // 生成 main 函数
    emit(".globl _main");
    emit("_main:");
    emit("    stp x29, x30, [sp, #-16]!");
    emit("    mov x29, sp");
    emit("    sub sp, sp, #%d", ((g_stack_offset + 32 + 15) / 16) * 16);

    // 继续生成 main 里的代码
    while (g_tok_pos < g_ntok && cur_tok().type != TK_EOF) {
        gen_stmt();
    }

    // 生成 main epilogue
    emit("    mov x0, #0");
    emit("    add sp, sp, #%d", ((g_stack_offset + 32 + 15) / 16) * 16);
    emit("    ldp x29, x30, [sp], #16");
    emit("    ret");

    // 字符串常量
    fprintf(g_out, "    .section __TEXT,__cstring,cstring_literals\n");
    fprintf(g_out, "l_.int_fmt:\n");
    fprintf(g_out, "    .asciz \"%%d\\n\"\n");
    
    // 示例字符串常量
    fprintf(g_out, "l_.str_0:\n");
    fprintf(g_out, "    .asciz \"Hello, Aurora!\\n\"\n");

    fclose(g_out);

    printf("✓ 生成汇编: %s\n", argv[2]);
    printf("  变量: %d, 栈帧: %d 字节\n", g_symbol_count, g_stack_offset);

    free(src);
    return 0;
}
