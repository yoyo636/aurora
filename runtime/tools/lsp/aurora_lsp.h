/*
 * Aurora 工具链 - LSP 语言服务器
 * 支持 100+ LSP 请求处理
 */

#ifndef AURORA_LSP_H
#define AURORA_LSP_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* LSP 消息类型 */
typedef enum {
    LSP_MSG_REQUEST,
    LSP_MSG_RESPONSE,
    LSP_MSG_NOTIFICATION,
    LSP_MSG_ERROR
} LSPMessageType;

/* LSP 位置 */
typedef struct {
    int line;
    int character;
} LSPPosition;

/* LSP 范围 */
typedef struct {
    LSPPosition start;
    LSPPosition end;
} LSPRange;

/* LSP 位置（带 URI） */
typedef struct {
    char* uri;
    LSPPosition position;
} LSPLocation;

/* LSP 诊断 */
typedef struct {
    LSPRange range;
    int severity;
    char* code;
    char* source;
    char* message;
    void* related_info;
    int related_count;
} LSPDiagnostic;

/* LSP 完成项 */
typedef struct {
    char* label;
    int kind;
    char* detail;
    char* documentation;
    int deprecated;
    int preselect;
    LSPRange sort_text;
    LSPRange filter_text;
    void* insert_text;
    int insert_text_format;
    void* text_edit;
    void* additional_text_edits;
    int additional_edit_count;
    void* commit_characters;
    int commit_count;
    void* command;
    void* data;
} LSPCompletionItem;

/* LSP 悬停 */
typedef struct {
    void* contents;
    LSPRange range;
} LSPHover;

/* LSP 签名帮助 */
typedef struct {
    void* signatures;
    int signature_count;
    int active_signature;
    int active_parameter;
} LSPSignatureHelp;

/* LSP 符号信息 */
typedef struct {
    char* name;
    int kind;
    char* detail;
    LSPLocation location;
    void* children;
    int child_count;
    int deprecated;
} LSPSymbolInformation;

/* LSP 文档符号 */
typedef struct {
    char* name;
    char* detail;
    int kind;
    int deprecated;
    LSPRange range;
    LSPRange selection_range;
    void* children;
    int child_count;
} LSPDocumentSymbol;

/* LSP 代码透镜 */
typedef struct {
    LSPRange range;
    void* command;
    void* data;
} LSPCodeLens;

/* LSP 代码动作 */
typedef struct {
    char* title;
    int kind;
    void* diagnostics;
    int diagnostic_count;
    int is_preferred;
    int disabled;
    void* edit;
    void* command;
    void* data;
} LSPCodeAction;

/* LSP 格式化编辑 */
typedef struct {
    LSPRange range;
    char* new_text;
} LSPTextEdit;

/* LSP 重命名 */
typedef struct {
    void* changes;
    int change_count;
    void* document_changes;
    int document_change_count;
} LSPWorkspaceEdit;

/* LSP 服务器 */
typedef struct {
    int initialized;
    int shutdown;
    char* root_uri;
    void* capabilities;
    void* workspace_folders;
    int folder_count;
    void* open_documents;
    int document_count;
    void* diagnostics;
    int diagnostic_count;
    void* ast_cache;
    void* symbol_cache;
    void* semantic_tokens;
    int token_count;
    int log_level;
    FILE* log_file;
    void* client;
    int request_id;
} LSPServer;

/* 函数声明 */
int lsp_req_000(LSPServer* server, void* request, void* response);
int lsp_req_001(LSPServer* server, void* request, void* response);
int lsp_req_002(LSPServer* server, void* request, void* response);
int lsp_req_003(LSPServer* server, void* request, void* response);
int lsp_req_004(LSPServer* server, void* request, void* response);
int lsp_req_005(LSPServer* server, void* request, void* response);
int lsp_req_006(LSPServer* server, void* request, void* response);
int lsp_req_007(LSPServer* server, void* request, void* response);
int lsp_req_008(LSPServer* server, void* request, void* response);
int lsp_req_009(LSPServer* server, void* request, void* response);
int lsp_req_010(LSPServer* server, void* request, void* response);
int lsp_req_011(LSPServer* server, void* request, void* response);
int lsp_req_012(LSPServer* server, void* request, void* response);
int lsp_req_013(LSPServer* server, void* request, void* response);
int lsp_req_014(LSPServer* server, void* request, void* response);
int lsp_req_015(LSPServer* server, void* request, void* response);
int lsp_req_016(LSPServer* server, void* request, void* response);
int lsp_req_017(LSPServer* server, void* request, void* response);
int lsp_req_018(LSPServer* server, void* request, void* response);
int lsp_req_019(LSPServer* server, void* request, void* response);
int lsp_req_020(LSPServer* server, void* request, void* response);
int lsp_req_021(LSPServer* server, void* request, void* response);
int lsp_req_022(LSPServer* server, void* request, void* response);
int lsp_req_023(LSPServer* server, void* request, void* response);
int lsp_req_024(LSPServer* server, void* request, void* response);
int lsp_req_025(LSPServer* server, void* request, void* response);
int lsp_req_026(LSPServer* server, void* request, void* response);
int lsp_req_027(LSPServer* server, void* request, void* response);
int lsp_req_028(LSPServer* server, void* request, void* response);
int lsp_req_029(LSPServer* server, void* request, void* response);
int lsp_req_030(LSPServer* server, void* request, void* response);
int lsp_req_031(LSPServer* server, void* request, void* response);
int lsp_req_032(LSPServer* server, void* request, void* response);
int lsp_req_033(LSPServer* server, void* request, void* response);
int lsp_req_034(LSPServer* server, void* request, void* response);
int lsp_req_035(LSPServer* server, void* request, void* response);
int lsp_req_036(LSPServer* server, void* request, void* response);
int lsp_req_037(LSPServer* server, void* request, void* response);
int lsp_req_038(LSPServer* server, void* request, void* response);
int lsp_req_039(LSPServer* server, void* request, void* response);
int lsp_req_040(LSPServer* server, void* request, void* response);
int lsp_req_041(LSPServer* server, void* request, void* response);
int lsp_req_042(LSPServer* server, void* request, void* response);
int lsp_req_043(LSPServer* server, void* request, void* response);
int lsp_req_044(LSPServer* server, void* request, void* response);
int lsp_req_045(LSPServer* server, void* request, void* response);
int lsp_req_046(LSPServer* server, void* request, void* response);
int lsp_req_047(LSPServer* server, void* request, void* response);
int lsp_req_048(LSPServer* server, void* request, void* response);
int lsp_req_049(LSPServer* server, void* request, void* response);
int lsp_req_050(LSPServer* server, void* request, void* response);
int lsp_req_051(LSPServer* server, void* request, void* response);
int lsp_req_052(LSPServer* server, void* request, void* response);
int lsp_req_053(LSPServer* server, void* request, void* response);
int lsp_req_054(LSPServer* server, void* request, void* response);
int lsp_req_055(LSPServer* server, void* request, void* response);
int lsp_req_056(LSPServer* server, void* request, void* response);
int lsp_req_057(LSPServer* server, void* request, void* response);
int lsp_req_058(LSPServer* server, void* request, void* response);
int lsp_req_059(LSPServer* server, void* request, void* response);
int lsp_req_060(LSPServer* server, void* request, void* response);
int lsp_req_061(LSPServer* server, void* request, void* response);
int lsp_req_062(LSPServer* server, void* request, void* response);
int lsp_req_063(LSPServer* server, void* request, void* response);
int lsp_req_064(LSPServer* server, void* request, void* response);
int lsp_req_065(LSPServer* server, void* request, void* response);
int lsp_req_066(LSPServer* server, void* request, void* response);
int lsp_req_067(LSPServer* server, void* request, void* response);
int lsp_req_068(LSPServer* server, void* request, void* response);
int lsp_req_069(LSPServer* server, void* request, void* response);
int lsp_req_070(LSPServer* server, void* request, void* response);
int lsp_req_071(LSPServer* server, void* request, void* response);
int lsp_req_072(LSPServer* server, void* request, void* response);
int lsp_req_073(LSPServer* server, void* request, void* response);
int lsp_req_074(LSPServer* server, void* request, void* response);
int lsp_req_075(LSPServer* server, void* request, void* response);
int lsp_req_076(LSPServer* server, void* request, void* response);
int lsp_req_077(LSPServer* server, void* request, void* response);
int lsp_req_078(LSPServer* server, void* request, void* response);
int lsp_req_079(LSPServer* server, void* request, void* response);
int lsp_req_080(LSPServer* server, void* request, void* response);
int lsp_req_081(LSPServer* server, void* request, void* response);
int lsp_req_082(LSPServer* server, void* request, void* response);
int lsp_req_083(LSPServer* server, void* request, void* response);
int lsp_req_084(LSPServer* server, void* request, void* response);
int lsp_req_085(LSPServer* server, void* request, void* response);
int lsp_req_086(LSPServer* server, void* request, void* response);
int lsp_req_087(LSPServer* server, void* request, void* response);
int lsp_req_088(LSPServer* server, void* request, void* response);
int lsp_req_089(LSPServer* server, void* request, void* response);
int lsp_req_090(LSPServer* server, void* request, void* response);
int lsp_req_091(LSPServer* server, void* request, void* response);
int lsp_req_092(LSPServer* server, void* request, void* response);
int lsp_req_093(LSPServer* server, void* request, void* response);
int lsp_req_094(LSPServer* server, void* request, void* response);
int lsp_req_095(LSPServer* server, void* request, void* response);
int lsp_req_096(LSPServer* server, void* request, void* response);
int lsp_req_097(LSPServer* server, void* request, void* response);
int lsp_req_098(LSPServer* server, void* request, void* response);
int lsp_req_099(LSPServer* server, void* request, void* response);
LSPServer* lsp_server_create();
void lsp_server_destroy(LSPServer* server);
int lsp_server_initialize(LSPServer* server, void* params);
int lsp_server_initialized(LSPServer* server);
int lsp_server_shutdown(LSPServer* server);
int lsp_server_exit(LSPServer* server);
int lsp_server_did_open(LSPServer* server, void* params);
int lsp_server_did_change(LSPServer* server, void* params);
int lsp_server_did_close(LSPServer* server, void* params);
int lsp_server_did_save(LSPServer* server, void* params);
int lsp_server_completion(LSPServer* server, void* params, void* result);
int lsp_server_completion_resolve(LSPServer* server, void* params, void* result);
int lsp_server_hover(LSPServer* server, void* params, void* result);
int lsp_server_signature_help(LSPServer* server, void* params, void* result);
int lsp_server_go_to_definition(LSPServer* server, void* params, void* result);
int lsp_server_go_to_declaration(LSPServer* server, void* params, void* result);
int lsp_server_go_to_type_definition(LSPServer* server, void* params, void* result);
int lsp_server_go_to_implementation(LSPServer* server, void* params, void* result);
int lsp_server_find_references(LSPServer* server, void* params, void* result);
int lsp_server_document_highlight(LSPServer* server, void* params, void* result);
int lsp_server_document_symbol(LSPServer* server, void* params, void* result);
int lsp_server_workspace_symbol(LSPServer* server, void* params, void* result);
int lsp_server_code_action(LSPServer* server, void* params, void* result);
int lsp_server_code_lens(LSPServer* server, void* params, void* result);
int lsp_server_code_lens_resolve(LSPServer* server, void* params, void* result);
int lsp_server_document_link(LSPServer* server, void* params, void* result);
int lsp_server_document_link_resolve(LSPServer* server, void* params, void* result);
int lsp_server_document_color(LSPServer* server, void* params, void* result);
int lsp_server_color_presentation(LSPServer* server, void* params, void* result);
int lsp_server_formatting(LSPServer* server, void* params, void* result);
int lsp_server_range_formatting(LSPServer* server, void* params, void* result);
int lsp_server_on_type_formatting(LSPServer* server, void* params, void* result);
int lsp_server_rename(LSPServer* server, void* params, void* result);
int lsp_server_prepare_rename(LSPServer* server, void* params, void* result);
int lsp_server_folding_range(LSPServer* server, void* params, void* result);
int lsp_server_selection_range(LSPServer* server, void* params, void* result);
int lsp_server_call_hierarchy(LSPServer* server, void* params, void* result);
int lsp_server_semantic_tokens(LSPServer* server, void* params, void* result);
int lsp_server_inline_value(LSPServer* server, void* params, void* result);
int lsp_server_inlay_hint(LSPServer* server, void* params, void* result);
int lsp_server_moniker(LSPServer* server, void* params, void* result);
int lsp_server_type_hierarchy(LSPServer* server, void* params, void* result);
int lsp_server_inline_completion(LSPServer* server, void* params, void* result);

#endif /* AURORA_LSP_H */