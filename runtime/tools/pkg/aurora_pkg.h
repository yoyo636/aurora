/*
 * Aurora 工具链 - 包管理器
 * 支持 100+ 包管理命令
 */

#ifndef AURORA_PKG_H
#define AURORA_PKG_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 包状态 */
typedef enum {
    PKG_STATE_AVAILABLE,
    PKG_STATE_INSTALLED,
    PKG_STATE_UPDATABLE,
    PKG_STATE_BROKEN,
    PKG_STATE_REMOVED,
    PKG_STATE_PENDING
} PackageState;

/* 包版本 */
typedef struct {
    int major;
    int minor;
    int patch;
    char* pre_release;
    char* build;
    char* raw;
} PackageVersion;

/* 包依赖 */
typedef struct {
    char* name;
    char* version_constraint;
    int optional;
    int dev_only;
    int peer;
    int bundled;
    struct PackageDependency* next;
} PackageDependency;

/* 包 */
typedef struct {
    char* name;
    PackageVersion version;
    char* description;
    char* author;
    char* license;
    char* repository;
    char* homepage;
    char* keywords;
    int keyword_count;
    PackageState state;
    char* install_path;
    char* cache_path;
    PackageDependency* dependencies;
    int dependency_count;
    PackageDependency* dev_dependencies;
    int dev_dependency_count;
    PackageDependency* peer_dependencies;
    int peer_dependency_count;
    PackageDependency* optional_dependencies;
    int optional_dependency_count;
    void* scripts;
    int script_count;
    void* binaries;
    int binary_count;
    void* files;
    int file_count;
    int size;
    int unpacked_size;
    char* checksum;
    char* signature;
    int published_at;
    int updated_at;
    int download_count;
    int star_count;
    int fork_count;
    int issue_count;
    int open_issue_count;
    int pull_request_count;
    int open_pull_request_count;
    int contributor_count;
    void* contributors;
    int maintainer_count;
    void* maintainers;
    int deprecated;
    char* deprecation_message;
    int private;
    int funding;
    void* funding_links;
    int funding_link_count;
} Package;

/* 包注册表 */
typedef struct {
    char* url;
    char* name;
    int priority;
    int enabled;
    char* auth_token;
    char* username;
    char* password;
    int verify_ssl;
    int timeout;
    int retry_count;
    int cache_ttl;
    void* cache;
    int cache_count;
} PackageRegistry;

/* 包管理器 */
typedef struct {
    char* root_path;
    char* cache_path;
    char* config_path;
    char* global_path;
    char* temp_path;
    PackageRegistry* registries;
    int registry_count;
    Package* installed;
    int installed_count;
    Package* available;
    int available_count;
    void* lock_file;
    int lock_count;
    void* config;
    int verbose;
    int quiet;
    int dry_run;
    int force;
    int yes;
    int no_color;
    int log_level;
    FILE* log_file;
    int concurrent_downloads;
    int network_timeout;
    int retries;
    int offline;
    int prefer_offline;
    int strict_ssl;
    char* proxy;
    char* https_proxy;
    char* no_proxy;
    char* user_agent;
    char* cafile;
    char* capath;
} PackageManager;

/* 函数声明 */
int pkg_cmd_000(PackageManager* pm, const char* args);
int pkg_cmd_001(PackageManager* pm, const char* args);
int pkg_cmd_002(PackageManager* pm, const char* args);
int pkg_cmd_003(PackageManager* pm, const char* args);
int pkg_cmd_004(PackageManager* pm, const char* args);
int pkg_cmd_005(PackageManager* pm, const char* args);
int pkg_cmd_006(PackageManager* pm, const char* args);
int pkg_cmd_007(PackageManager* pm, const char* args);
int pkg_cmd_008(PackageManager* pm, const char* args);
int pkg_cmd_009(PackageManager* pm, const char* args);
int pkg_cmd_010(PackageManager* pm, const char* args);
int pkg_cmd_011(PackageManager* pm, const char* args);
int pkg_cmd_012(PackageManager* pm, const char* args);
int pkg_cmd_013(PackageManager* pm, const char* args);
int pkg_cmd_014(PackageManager* pm, const char* args);
int pkg_cmd_015(PackageManager* pm, const char* args);
int pkg_cmd_016(PackageManager* pm, const char* args);
int pkg_cmd_017(PackageManager* pm, const char* args);
int pkg_cmd_018(PackageManager* pm, const char* args);
int pkg_cmd_019(PackageManager* pm, const char* args);
int pkg_cmd_020(PackageManager* pm, const char* args);
int pkg_cmd_021(PackageManager* pm, const char* args);
int pkg_cmd_022(PackageManager* pm, const char* args);
int pkg_cmd_023(PackageManager* pm, const char* args);
int pkg_cmd_024(PackageManager* pm, const char* args);
int pkg_cmd_025(PackageManager* pm, const char* args);
int pkg_cmd_026(PackageManager* pm, const char* args);
int pkg_cmd_027(PackageManager* pm, const char* args);
int pkg_cmd_028(PackageManager* pm, const char* args);
int pkg_cmd_029(PackageManager* pm, const char* args);
int pkg_cmd_030(PackageManager* pm, const char* args);
int pkg_cmd_031(PackageManager* pm, const char* args);
int pkg_cmd_032(PackageManager* pm, const char* args);
int pkg_cmd_033(PackageManager* pm, const char* args);
int pkg_cmd_034(PackageManager* pm, const char* args);
int pkg_cmd_035(PackageManager* pm, const char* args);
int pkg_cmd_036(PackageManager* pm, const char* args);
int pkg_cmd_037(PackageManager* pm, const char* args);
int pkg_cmd_038(PackageManager* pm, const char* args);
int pkg_cmd_039(PackageManager* pm, const char* args);
int pkg_cmd_040(PackageManager* pm, const char* args);
int pkg_cmd_041(PackageManager* pm, const char* args);
int pkg_cmd_042(PackageManager* pm, const char* args);
int pkg_cmd_043(PackageManager* pm, const char* args);
int pkg_cmd_044(PackageManager* pm, const char* args);
int pkg_cmd_045(PackageManager* pm, const char* args);
int pkg_cmd_046(PackageManager* pm, const char* args);
int pkg_cmd_047(PackageManager* pm, const char* args);
int pkg_cmd_048(PackageManager* pm, const char* args);
int pkg_cmd_049(PackageManager* pm, const char* args);
int pkg_cmd_050(PackageManager* pm, const char* args);
int pkg_cmd_051(PackageManager* pm, const char* args);
int pkg_cmd_052(PackageManager* pm, const char* args);
int pkg_cmd_053(PackageManager* pm, const char* args);
int pkg_cmd_054(PackageManager* pm, const char* args);
int pkg_cmd_055(PackageManager* pm, const char* args);
int pkg_cmd_056(PackageManager* pm, const char* args);
int pkg_cmd_057(PackageManager* pm, const char* args);
int pkg_cmd_058(PackageManager* pm, const char* args);
int pkg_cmd_059(PackageManager* pm, const char* args);
int pkg_cmd_060(PackageManager* pm, const char* args);
int pkg_cmd_061(PackageManager* pm, const char* args);
int pkg_cmd_062(PackageManager* pm, const char* args);
int pkg_cmd_063(PackageManager* pm, const char* args);
int pkg_cmd_064(PackageManager* pm, const char* args);
int pkg_cmd_065(PackageManager* pm, const char* args);
int pkg_cmd_066(PackageManager* pm, const char* args);
int pkg_cmd_067(PackageManager* pm, const char* args);
int pkg_cmd_068(PackageManager* pm, const char* args);
int pkg_cmd_069(PackageManager* pm, const char* args);
int pkg_cmd_070(PackageManager* pm, const char* args);
int pkg_cmd_071(PackageManager* pm, const char* args);
int pkg_cmd_072(PackageManager* pm, const char* args);
int pkg_cmd_073(PackageManager* pm, const char* args);
int pkg_cmd_074(PackageManager* pm, const char* args);
int pkg_cmd_075(PackageManager* pm, const char* args);
int pkg_cmd_076(PackageManager* pm, const char* args);
int pkg_cmd_077(PackageManager* pm, const char* args);
int pkg_cmd_078(PackageManager* pm, const char* args);
int pkg_cmd_079(PackageManager* pm, const char* args);
int pkg_cmd_080(PackageManager* pm, const char* args);
int pkg_cmd_081(PackageManager* pm, const char* args);
int pkg_cmd_082(PackageManager* pm, const char* args);
int pkg_cmd_083(PackageManager* pm, const char* args);
int pkg_cmd_084(PackageManager* pm, const char* args);
int pkg_cmd_085(PackageManager* pm, const char* args);
int pkg_cmd_086(PackageManager* pm, const char* args);
int pkg_cmd_087(PackageManager* pm, const char* args);
int pkg_cmd_088(PackageManager* pm, const char* args);
int pkg_cmd_089(PackageManager* pm, const char* args);
int pkg_cmd_090(PackageManager* pm, const char* args);
int pkg_cmd_091(PackageManager* pm, const char* args);
int pkg_cmd_092(PackageManager* pm, const char* args);
int pkg_cmd_093(PackageManager* pm, const char* args);
int pkg_cmd_094(PackageManager* pm, const char* args);
int pkg_cmd_095(PackageManager* pm, const char* args);
int pkg_cmd_096(PackageManager* pm, const char* args);
int pkg_cmd_097(PackageManager* pm, const char* args);
int pkg_cmd_098(PackageManager* pm, const char* args);
int pkg_cmd_099(PackageManager* pm, const char* args);
PackageManager* pkg_manager_create(const char* root_path);
void pkg_manager_destroy(PackageManager* pm);
int pkg_manager_init(PackageManager* pm);
int pkg_manager_install(PackageManager* pm, const char* package_name, const char* version);
int pkg_manager_uninstall(PackageManager* pm, const char* package_name);
int pkg_manager_update(PackageManager* pm, const char* package_name);
int pkg_manager_upgrade(PackageManager* pm);
int pkg_manager_list(PackageManager* pm, int global, int outdated);
int pkg_manager_search(PackageManager* pm, const char* query);
int pkg_manager_info(PackageManager* pm, const char* package_name);
int pkg_manager_show(PackageManager* pm, const char* package_name);
int pkg_manager_view(PackageManager* pm, const char* package_name);
int pkg_manager_publish(PackageManager* pm, const char* path);
int pkg_manager_unpublish(PackageManager* pm, const char* package_name, const char* version);
int pkg_manager_deprecate(PackageManager* pm, const char* package_name, const char* message);
int pkg_manager_undeprecate(PackageManager* pm, const char* package_name);
int pkg_manager_owner_add(PackageManager* pm, const char* package_name, const char* user);
int pkg_manager_owner_remove(PackageManager* pm, const char* package_name, const char* user);
int pkg_manager_owner_list(PackageManager* pm, const char* package_name);
int pkg_manager_star(PackageManager* pm, const char* package_name);
int pkg_manager_unstar(PackageManager* pm, const char* package_name);
int pkg_manager_stars(PackageManager* pm);
int pkg_manager_whoami(PackageManager* pm);
int pkg_manager_login(PackageManager* pm, const char* registry);
int pkg_manager_logout(PackageManager* pm, const char* registry);
int pkg_manager_token_create(PackageManager* pm, const char* name);
int pkg_manager_token_list(PackageManager* pm);
int pkg_manager_token_revoke(PackageManager* pm, const char* token);
int pkg_manager_config_get(PackageManager* pm, const char* key);
int pkg_manager_config_set(PackageManager* pm, const char* key, const char* value);
int pkg_manager_config_delete(PackageManager* pm, const char* key);
int pkg_manager_config_list(PackageManager* pm);
int pkg_manager_cache_clean(PackageManager* pm);
int pkg_manager_cache_verify(PackageManager* pm);
int pkg_manager_cache_dir(PackageManager* pm);
int pkg_manager_dedupe(PackageManager* pm);
int pkg_manager_prune(PackageManager* pm);
int pkg_manager_fund(PackageManager* pm);
int pkg_manager_audit(PackageManager* pm);
int pkg_manager_fix(PackageManager* pm);
int pkg_manager_outdated(PackageManager* pm);
int pkg_manager_link(PackageManager* pm, const char* package_path);
int pkg_manager_unlink(PackageManager* pm, const char* package_name);
int pkg_manager_rebuild(PackageManager* pm, const char* package_name);
int pkg_manager_run(PackageManager* pm, const char* script, char** args);
int pkg_manager_test(PackageManager* pm);
int pkg_manager_build(PackageManager* pm);
int pkg_manager_pack(PackageManager* pm, const char* path);
int pkg_manager_diff(PackageManager* pm, const char* package_a, const char* package_b);
int pkg_manager_versions(PackageManager* pm, const char* package_name);
int pkg_manager_dist_tags(PackageManager* pm, const char* package_name);
int pkg_manager_dist_tag_add(PackageManager* pm, const char* package_name, const char* tag, const char* version);
int pkg_manager_dist_tag_remove(PackageManager* pm, const char* package_name, const char* tag);
int pkg_manager_team_create(PackageManager* pm, const char* team_name);
int pkg_manager_team_destroy(PackageManager* pm, const char* team_name);
int pkg_manager_team_add(PackageManager* pm, const char* team_name, const char* user);
int pkg_manager_team_remove(PackageManager* pm, const char* team_name, const char* user);
int pkg_manager_team_list(PackageManager* pm);
int pkg_manager_team_members(PackageManager* pm, const char* team_name);
int pkg_manager_access(PackageManager* pm, const char* package_name, const char* access_level);
int pkg_manager_access_list(PackageManager* pm, const char* package_name);
int pkg_manager_adduser(PackageManager* pm, const char* registry);
int pkg_manager_profile(PackageManager* pm);
int pkg_manager_org(PackageManager* pm, const char* org_name);
int pkg_manager_hook_add(PackageManager* pm, const char* event, const char* url);
int pkg_manager_hook_remove(PackageManager* pm, const char* event, const char* url);
int pkg_manager_hook_list(PackageManager* pm);

#endif /* AURORA_PKG_H */