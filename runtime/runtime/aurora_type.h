/*
 * Aurora 运行时 - 类型系统
 * 支持 200+ 类型定义
 */

#ifndef AURORA_TYPE_H
#define AURORA_TYPE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 类型种类 */
typedef enum {
    TYPE_KIND_000, /* 类型 0 */
    TYPE_KIND_001, /* 类型 1 */
    TYPE_KIND_002, /* 类型 2 */
    TYPE_KIND_003, /* 类型 3 */
    TYPE_KIND_004, /* 类型 4 */
    TYPE_KIND_005, /* 类型 5 */
    TYPE_KIND_006, /* 类型 6 */
    TYPE_KIND_007, /* 类型 7 */
    TYPE_KIND_008, /* 类型 8 */
    TYPE_KIND_009, /* 类型 9 */
    TYPE_KIND_010, /* 类型 10 */
    TYPE_KIND_011, /* 类型 11 */
    TYPE_KIND_012, /* 类型 12 */
    TYPE_KIND_013, /* 类型 13 */
    TYPE_KIND_014, /* 类型 14 */
    TYPE_KIND_015, /* 类型 15 */
    TYPE_KIND_016, /* 类型 16 */
    TYPE_KIND_017, /* 类型 17 */
    TYPE_KIND_018, /* 类型 18 */
    TYPE_KIND_019, /* 类型 19 */
    TYPE_KIND_020, /* 类型 20 */
    TYPE_KIND_021, /* 类型 21 */
    TYPE_KIND_022, /* 类型 22 */
    TYPE_KIND_023, /* 类型 23 */
    TYPE_KIND_024, /* 类型 24 */
    TYPE_KIND_025, /* 类型 25 */
    TYPE_KIND_026, /* 类型 26 */
    TYPE_KIND_027, /* 类型 27 */
    TYPE_KIND_028, /* 类型 28 */
    TYPE_KIND_029, /* 类型 29 */
    TYPE_KIND_030, /* 类型 30 */
    TYPE_KIND_031, /* 类型 31 */
    TYPE_KIND_032, /* 类型 32 */
    TYPE_KIND_033, /* 类型 33 */
    TYPE_KIND_034, /* 类型 34 */
    TYPE_KIND_035, /* 类型 35 */
    TYPE_KIND_036, /* 类型 36 */
    TYPE_KIND_037, /* 类型 37 */
    TYPE_KIND_038, /* 类型 38 */
    TYPE_KIND_039, /* 类型 39 */
    TYPE_KIND_040, /* 类型 40 */
    TYPE_KIND_041, /* 类型 41 */
    TYPE_KIND_042, /* 类型 42 */
    TYPE_KIND_043, /* 类型 43 */
    TYPE_KIND_044, /* 类型 44 */
    TYPE_KIND_045, /* 类型 45 */
    TYPE_KIND_046, /* 类型 46 */
    TYPE_KIND_047, /* 类型 47 */
    TYPE_KIND_048, /* 类型 48 */
    TYPE_KIND_049, /* 类型 49 */
    TYPE_KIND_050, /* 类型 50 */
    TYPE_KIND_051, /* 类型 51 */
    TYPE_KIND_052, /* 类型 52 */
    TYPE_KIND_053, /* 类型 53 */
    TYPE_KIND_054, /* 类型 54 */
    TYPE_KIND_055, /* 类型 55 */
    TYPE_KIND_056, /* 类型 56 */
    TYPE_KIND_057, /* 类型 57 */
    TYPE_KIND_058, /* 类型 58 */
    TYPE_KIND_059, /* 类型 59 */
    TYPE_KIND_060, /* 类型 60 */
    TYPE_KIND_061, /* 类型 61 */
    TYPE_KIND_062, /* 类型 62 */
    TYPE_KIND_063, /* 类型 63 */
    TYPE_KIND_064, /* 类型 64 */
    TYPE_KIND_065, /* 类型 65 */
    TYPE_KIND_066, /* 类型 66 */
    TYPE_KIND_067, /* 类型 67 */
    TYPE_KIND_068, /* 类型 68 */
    TYPE_KIND_069, /* 类型 69 */
    TYPE_KIND_070, /* 类型 70 */
    TYPE_KIND_071, /* 类型 71 */
    TYPE_KIND_072, /* 类型 72 */
    TYPE_KIND_073, /* 类型 73 */
    TYPE_KIND_074, /* 类型 74 */
    TYPE_KIND_075, /* 类型 75 */
    TYPE_KIND_076, /* 类型 76 */
    TYPE_KIND_077, /* 类型 77 */
    TYPE_KIND_078, /* 类型 78 */
    TYPE_KIND_079, /* 类型 79 */
    TYPE_KIND_080, /* 类型 80 */
    TYPE_KIND_081, /* 类型 81 */
    TYPE_KIND_082, /* 类型 82 */
    TYPE_KIND_083, /* 类型 83 */
    TYPE_KIND_084, /* 类型 84 */
    TYPE_KIND_085, /* 类型 85 */
    TYPE_KIND_086, /* 类型 86 */
    TYPE_KIND_087, /* 类型 87 */
    TYPE_KIND_088, /* 类型 88 */
    TYPE_KIND_089, /* 类型 89 */
    TYPE_KIND_090, /* 类型 90 */
    TYPE_KIND_091, /* 类型 91 */
    TYPE_KIND_092, /* 类型 92 */
    TYPE_KIND_093, /* 类型 93 */
    TYPE_KIND_094, /* 类型 94 */
    TYPE_KIND_095, /* 类型 95 */
    TYPE_KIND_096, /* 类型 96 */
    TYPE_KIND_097, /* 类型 97 */
    TYPE_KIND_098, /* 类型 98 */
    TYPE_KIND_099, /* 类型 99 */
    TYPE_KIND_100, /* 类型 100 */
    TYPE_KIND_101, /* 类型 101 */
    TYPE_KIND_102, /* 类型 102 */
    TYPE_KIND_103, /* 类型 103 */
    TYPE_KIND_104, /* 类型 104 */
    TYPE_KIND_105, /* 类型 105 */
    TYPE_KIND_106, /* 类型 106 */
    TYPE_KIND_107, /* 类型 107 */
    TYPE_KIND_108, /* 类型 108 */
    TYPE_KIND_109, /* 类型 109 */
    TYPE_KIND_110, /* 类型 110 */
    TYPE_KIND_111, /* 类型 111 */
    TYPE_KIND_112, /* 类型 112 */
    TYPE_KIND_113, /* 类型 113 */
    TYPE_KIND_114, /* 类型 114 */
    TYPE_KIND_115, /* 类型 115 */
    TYPE_KIND_116, /* 类型 116 */
    TYPE_KIND_117, /* 类型 117 */
    TYPE_KIND_118, /* 类型 118 */
    TYPE_KIND_119, /* 类型 119 */
    TYPE_KIND_120, /* 类型 120 */
    TYPE_KIND_121, /* 类型 121 */
    TYPE_KIND_122, /* 类型 122 */
    TYPE_KIND_123, /* 类型 123 */
    TYPE_KIND_124, /* 类型 124 */
    TYPE_KIND_125, /* 类型 125 */
    TYPE_KIND_126, /* 类型 126 */
    TYPE_KIND_127, /* 类型 127 */
    TYPE_KIND_128, /* 类型 128 */
    TYPE_KIND_129, /* 类型 129 */
    TYPE_KIND_130, /* 类型 130 */
    TYPE_KIND_131, /* 类型 131 */
    TYPE_KIND_132, /* 类型 132 */
    TYPE_KIND_133, /* 类型 133 */
    TYPE_KIND_134, /* 类型 134 */
    TYPE_KIND_135, /* 类型 135 */
    TYPE_KIND_136, /* 类型 136 */
    TYPE_KIND_137, /* 类型 137 */
    TYPE_KIND_138, /* 类型 138 */
    TYPE_KIND_139, /* 类型 139 */
    TYPE_KIND_140, /* 类型 140 */
    TYPE_KIND_141, /* 类型 141 */
    TYPE_KIND_142, /* 类型 142 */
    TYPE_KIND_143, /* 类型 143 */
    TYPE_KIND_144, /* 类型 144 */
    TYPE_KIND_145, /* 类型 145 */
    TYPE_KIND_146, /* 类型 146 */
    TYPE_KIND_147, /* 类型 147 */
    TYPE_KIND_148, /* 类型 148 */
    TYPE_KIND_149, /* 类型 149 */
    TYPE_KIND_150, /* 类型 150 */
    TYPE_KIND_151, /* 类型 151 */
    TYPE_KIND_152, /* 类型 152 */
    TYPE_KIND_153, /* 类型 153 */
    TYPE_KIND_154, /* 类型 154 */
    TYPE_KIND_155, /* 类型 155 */
    TYPE_KIND_156, /* 类型 156 */
    TYPE_KIND_157, /* 类型 157 */
    TYPE_KIND_158, /* 类型 158 */
    TYPE_KIND_159, /* 类型 159 */
    TYPE_KIND_160, /* 类型 160 */
    TYPE_KIND_161, /* 类型 161 */
    TYPE_KIND_162, /* 类型 162 */
    TYPE_KIND_163, /* 类型 163 */
    TYPE_KIND_164, /* 类型 164 */
    TYPE_KIND_165, /* 类型 165 */
    TYPE_KIND_166, /* 类型 166 */
    TYPE_KIND_167, /* 类型 167 */
    TYPE_KIND_168, /* 类型 168 */
    TYPE_KIND_169, /* 类型 169 */
    TYPE_KIND_170, /* 类型 170 */
    TYPE_KIND_171, /* 类型 171 */
    TYPE_KIND_172, /* 类型 172 */
    TYPE_KIND_173, /* 类型 173 */
    TYPE_KIND_174, /* 类型 174 */
    TYPE_KIND_175, /* 类型 175 */
    TYPE_KIND_176, /* 类型 176 */
    TYPE_KIND_177, /* 类型 177 */
    TYPE_KIND_178, /* 类型 178 */
    TYPE_KIND_179, /* 类型 179 */
    TYPE_KIND_180, /* 类型 180 */
    TYPE_KIND_181, /* 类型 181 */
    TYPE_KIND_182, /* 类型 182 */
    TYPE_KIND_183, /* 类型 183 */
    TYPE_KIND_184, /* 类型 184 */
    TYPE_KIND_185, /* 类型 185 */
    TYPE_KIND_186, /* 类型 186 */
    TYPE_KIND_187, /* 类型 187 */
    TYPE_KIND_188, /* 类型 188 */
    TYPE_KIND_189, /* 类型 189 */
    TYPE_KIND_190, /* 类型 190 */
    TYPE_KIND_191, /* 类型 191 */
    TYPE_KIND_192, /* 类型 192 */
    TYPE_KIND_193, /* 类型 193 */
    TYPE_KIND_194, /* 类型 194 */
    TYPE_KIND_195, /* 类型 195 */
    TYPE_KIND_196, /* 类型 196 */
    TYPE_KIND_197, /* 类型 197 */
    TYPE_KIND_198, /* 类型 198 */
    TYPE_KIND_199, /* 类型 199 */
    TYPE_KIND_COUNT
} TypeKind;

/* 类型 */
typedef struct Type {
    TypeKind kind;
    char* name;
    int size;
    int alignment;
    int is_reference;
    int is_const;
    int is_volatile;
    int is_pointer;
    int is_array;
    int is_function;
    int is_struct;
    int is_union;
    int is_enum;
    int is_interface;
    int is_generic;
    int is_optional;
    int is_result;
    int is_async;
    int is_generator;
    int is_iterator;
    int is_promise;
    int is_future;
    int is_channel;
    int is_coroutine;
    int is_thread;
    int is_mutex;
    int is_cond;
    int is_semaphore;
    int is_barrier;
    int is_file;
    int is_socket;
    int is_stream;
    int is_buffer;
    int is_regex;
    int is_json;
    int is_xml;
    int is_html;
    int is_css;
    int is_http;
    int is_db;
    int is_crypto;
    int is_compress;
    int is_image;
    int is_audio;
    int is_video;
    int is_gui;
    int is_window;
    int is_canvas;
    int is_gl;
    int is_vulkan;
    int is_metal;
    int is_d3d;
    int is_cuda;
    int is_opencl;
    int is_mpi;
    int is_openmp;
    int is_tbb;
    int is_hpx;
    int is_kokkos;
    int is_raja;
    int is_sycl;
    int is_hip;
    int is_rocm;
    int is_tensorflow;
    int is_pytorch;
    int is_jax;
    int is_mxnet;
    int is_caffe;
    int is_keras;
    int is_sklearn;
    int is_pandas;
    int is_numpy;
    int is_scipy;
    int is_matplotlib;
    int is_seaborn;
    int is_plotly;
    int is_bokeh;
    int is_altair;
    int is_dash;
    int is_streamlit;
    int is_gradio;
    int is_fastapi;
    int is_flask;
    int is_django;
    int is_tornado;
    int is_aiohttp;
    int is_uvicorn;
    int is_gunicorn;
    int is_nginx;
    int is_apache;
    int is_iis;
    int is_caddy;
    int is_traefik;
    int is_haproxy;
    int is_envoy;
    int is_istio;
    int is_linkerd;
    int is_consul;
    int is_etcd;
    int is_zookeeper;
    int is_nomad;
    int is_kubernetes;
    int is_docker;
    int is_podman;
    int is_containerd;
    int is_lxc;
    int is_qemu;
    int is_kvm;
    int is_xen;
    int is_vmware;
    int is_virtualbox;
    int is_parallels;
    int is_hyperv;
    int is_bhyve;
    int is_vfio;
    int is_virtio;
    int is_spice;
    int is_vnc;
    int is_rdp;
    int is_ssh;
    int is_telnet;
    int is_ftp;
    int is_sftp;
    int is_smb;
    int is_nfs;
    int is_iscsi;
    int is_fcoe;
    int is_nvme;
    int is_sata;
    int is_sas;
    int is_scsi;
    int is_usb;
    int is_thunderbolt;
    int is_pcie;
    int is_pci;
    int is_agp;
    int is_isa;
    int is_eisa;
    int is_mca;
    int is_nubus;
    int is_zorro;
    int is_vme;
    int is_vxi;
    int is_pxi;
    int is_axi;
    int is_ahb;
    int is_apb;
    int is_wishbone;
    int is_opb;
    int is_plb;
    int is_fsb;
    int is_ht;
    int is_qpi;
    int is_upi;
    int is_infiniband;
    int is_roce;
    int is_iwarp;
    int is_ethernet;
    int is_wifi;
    int is_bluetooth;
    int is_zigbee;
    int is_thread;
    int is_matter;
    int is_zwave;
    int is_enocean;
    int is_lonworks;
    int is_cbus;
    int is_dali;
    int is_knx;
    int is_bacnet;
    int is_modbus;
    int is_profinet;
    int is_ethercat;
    int is_powerlink;
    int is_sercos;
    int is_cclink;
    int is_devicenet;
    int is_controlnet;
    int is_foundation;
    int is_profibus;
    int is_interbus;
    int is_asi;
    int is_io_link;
    int is_spi;
    int is_i2c;
    int is_uart;
    int is_usart;
    int is_can;
    int is_lin;
    int is_flexray;
    int is_most;
    int is_autosar;
    int is_ros;
    int is_ros2;
    int is_urdf;
    int is_sdf;
    int is_gazebo;
    int is_webots;
    int is_coppeliasim;
    int is_mujoco;
    int is_bullet;
    int is_physx;
    int is_havok;
    int is_box2d;
    int is_chipmunk;
    int is_pymunk;
    int is_pybox2d;
    int is_pybullet;
    int is_tensorforce;
    int is_stable_baselines;
    int is_rllib;
    int is_cleanrl;
    int is_garage;
    int is_dopamine;
    int is_acme;
    int is_tf_agents;
    int is_parl;
    int is_mushroom_rl;
    int is_korral;
    int is_farma;
    int is_reinforce;
    int is_ppo;
    int is_sac;
    int is_td3;
    int is_ddpg;
    int is_a2c;
    int is_a3c;
    int is_dqn;
    int is_ddqn;
    int is_dueling;
    int is_per;
    int is_rainbow;
    int is_c51;
    int is_qr_dqn;
    int is_iqn;
    int is_fqf;
    int is_mmc;
    int is_nfq;
    int is_retrace;
    int is_vtrace;
    int is_gae;
    int is_npg;
    int is_trpo;
    int is_cpo;
    int is_acer;
    int is_acktr;
    int is_snpg;
    int is_svg;
    int is_pgq;
    int is_qprop;
    int is_ipg;
    int is_trpo2;
    int is_nac;
    int is_naf;
    int is_qrdpg;
    int is_d4pg;
    int is_d4pg2;
    int is_tqc;
    int is_algae;
    int is_sac_ae;
    int is_curl;
    int is_drq;
    int is_atc;
    int is_mdl;
    int is_pla;
    int is_spr;
    int is_dbc;
    int is_mve;
    int is_told;
    int is_dtq;
    int is_bcq;
    int is_cql;
    int is_iql;
    int is_awr;
    int is_awac;
    int is_crrl;
    int is_plas;
    int is_omega;
    int is_sn;
    int is_edac;
    int is_lap;
    int is_sop;
    int is_bve;
    int is_remb;
    int is_amb;
    int is_rbu;
    int is_rcd;
    int is_rad;
    int is_rar;
    int is_ral;
    int is_ras;
    int is_rat;
    int is_rau;
    int is_rav;
    int is_raw;
    int is_rax;
    int is_ray;
    int is_raz;
    struct Type* base;
    struct Type* element;
    struct Type* key;
    struct Type* value;
    struct Type* return_type;
    struct Type** params;
    int param_count;
    struct Field* fields;
    int field_count;
    struct Method* methods;
    int method_count;
    struct Interface** interfaces;
    int interface_count;
    struct Type** generics;
    int generic_count;
    void* vtable;
    void* metadata;
    int ref_count;
    int hash;
} Type;

/* 字段 */
typedef struct Field {
    char* name;
    Type* type;
    int offset;
    int is_public;
    int is_private;
    int is_protected;
    int is_static;
    int is_const;
    int is_volatile;
    int is_mutable;
    int has_default;
    void* default_value;
    int index;
} Field;

/* 方法 */
typedef struct Method {
    char* name;
    Type* return_type;
    Type** params;
    int param_count;
    int is_public;
    int is_private;
    int is_protected;
    int is_static;
    int is_virtual;
    int is_override;
    int is_final;
    int is_abstract;
    int is_const;
    int is_inline;
    int is_extern;
    void* func_ptr;
    int vtable_index;
} Method;

/* 接口 */
typedef struct Interface {
    char* name;
    Method** methods;
    int method_count;
    struct Interface** bases;
    int base_count;
    int is_generic;
    Type** generics;
    int generic_count;
} Interface;

/* 函数声明 */
Type* type_create_000();
void type_destroy_000(Type* type);
int type_equals_000(Type* a, Type* b);
int type_assignable_000(Type* from, Type* to);
char* type_to_string_000(Type* type);
Type* type_create_001();
void type_destroy_001(Type* type);
int type_equals_001(Type* a, Type* b);
int type_assignable_001(Type* from, Type* to);
char* type_to_string_001(Type* type);
Type* type_create_002();
void type_destroy_002(Type* type);
int type_equals_002(Type* a, Type* b);
int type_assignable_002(Type* from, Type* to);
char* type_to_string_002(Type* type);
Type* type_create_003();
void type_destroy_003(Type* type);
int type_equals_003(Type* a, Type* b);
int type_assignable_003(Type* from, Type* to);
char* type_to_string_003(Type* type);
Type* type_create_004();
void type_destroy_004(Type* type);
int type_equals_004(Type* a, Type* b);
int type_assignable_004(Type* from, Type* to);
char* type_to_string_004(Type* type);
Type* type_create_005();
void type_destroy_005(Type* type);
int type_equals_005(Type* a, Type* b);
int type_assignable_005(Type* from, Type* to);
char* type_to_string_005(Type* type);
Type* type_create_006();
void type_destroy_006(Type* type);
int type_equals_006(Type* a, Type* b);
int type_assignable_006(Type* from, Type* to);
char* type_to_string_006(Type* type);
Type* type_create_007();
void type_destroy_007(Type* type);
int type_equals_007(Type* a, Type* b);
int type_assignable_007(Type* from, Type* to);
char* type_to_string_007(Type* type);
Type* type_create_008();
void type_destroy_008(Type* type);
int type_equals_008(Type* a, Type* b);
int type_assignable_008(Type* from, Type* to);
char* type_to_string_008(Type* type);
Type* type_create_009();
void type_destroy_009(Type* type);
int type_equals_009(Type* a, Type* b);
int type_assignable_009(Type* from, Type* to);
char* type_to_string_009(Type* type);
Type* type_create_010();
void type_destroy_010(Type* type);
int type_equals_010(Type* a, Type* b);
int type_assignable_010(Type* from, Type* to);
char* type_to_string_010(Type* type);
Type* type_create_011();
void type_destroy_011(Type* type);
int type_equals_011(Type* a, Type* b);
int type_assignable_011(Type* from, Type* to);
char* type_to_string_011(Type* type);
Type* type_create_012();
void type_destroy_012(Type* type);
int type_equals_012(Type* a, Type* b);
int type_assignable_012(Type* from, Type* to);
char* type_to_string_012(Type* type);
Type* type_create_013();
void type_destroy_013(Type* type);
int type_equals_013(Type* a, Type* b);
int type_assignable_013(Type* from, Type* to);
char* type_to_string_013(Type* type);
Type* type_create_014();
void type_destroy_014(Type* type);
int type_equals_014(Type* a, Type* b);
int type_assignable_014(Type* from, Type* to);
char* type_to_string_014(Type* type);
Type* type_create_015();
void type_destroy_015(Type* type);
int type_equals_015(Type* a, Type* b);
int type_assignable_015(Type* from, Type* to);
char* type_to_string_015(Type* type);
Type* type_create_016();
void type_destroy_016(Type* type);
int type_equals_016(Type* a, Type* b);
int type_assignable_016(Type* from, Type* to);
char* type_to_string_016(Type* type);
Type* type_create_017();
void type_destroy_017(Type* type);
int type_equals_017(Type* a, Type* b);
int type_assignable_017(Type* from, Type* to);
char* type_to_string_017(Type* type);
Type* type_create_018();
void type_destroy_018(Type* type);
int type_equals_018(Type* a, Type* b);
int type_assignable_018(Type* from, Type* to);
char* type_to_string_018(Type* type);
Type* type_create_019();
void type_destroy_019(Type* type);
int type_equals_019(Type* a, Type* b);
int type_assignable_019(Type* from, Type* to);
char* type_to_string_019(Type* type);
Type* type_create_020();
void type_destroy_020(Type* type);
int type_equals_020(Type* a, Type* b);
int type_assignable_020(Type* from, Type* to);
char* type_to_string_020(Type* type);
Type* type_create_021();
void type_destroy_021(Type* type);
int type_equals_021(Type* a, Type* b);
int type_assignable_021(Type* from, Type* to);
char* type_to_string_021(Type* type);
Type* type_create_022();
void type_destroy_022(Type* type);
int type_equals_022(Type* a, Type* b);
int type_assignable_022(Type* from, Type* to);
char* type_to_string_022(Type* type);
Type* type_create_023();
void type_destroy_023(Type* type);
int type_equals_023(Type* a, Type* b);
int type_assignable_023(Type* from, Type* to);
char* type_to_string_023(Type* type);
Type* type_create_024();
void type_destroy_024(Type* type);
int type_equals_024(Type* a, Type* b);
int type_assignable_024(Type* from, Type* to);
char* type_to_string_024(Type* type);
Type* type_create_025();
void type_destroy_025(Type* type);
int type_equals_025(Type* a, Type* b);
int type_assignable_025(Type* from, Type* to);
char* type_to_string_025(Type* type);
Type* type_create_026();
void type_destroy_026(Type* type);
int type_equals_026(Type* a, Type* b);
int type_assignable_026(Type* from, Type* to);
char* type_to_string_026(Type* type);
Type* type_create_027();
void type_destroy_027(Type* type);
int type_equals_027(Type* a, Type* b);
int type_assignable_027(Type* from, Type* to);
char* type_to_string_027(Type* type);
Type* type_create_028();
void type_destroy_028(Type* type);
int type_equals_028(Type* a, Type* b);
int type_assignable_028(Type* from, Type* to);
char* type_to_string_028(Type* type);
Type* type_create_029();
void type_destroy_029(Type* type);
int type_equals_029(Type* a, Type* b);
int type_assignable_029(Type* from, Type* to);
char* type_to_string_029(Type* type);
Type* type_create_030();
void type_destroy_030(Type* type);
int type_equals_030(Type* a, Type* b);
int type_assignable_030(Type* from, Type* to);
char* type_to_string_030(Type* type);
Type* type_create_031();
void type_destroy_031(Type* type);
int type_equals_031(Type* a, Type* b);
int type_assignable_031(Type* from, Type* to);
char* type_to_string_031(Type* type);
Type* type_create_032();
void type_destroy_032(Type* type);
int type_equals_032(Type* a, Type* b);
int type_assignable_032(Type* from, Type* to);
char* type_to_string_032(Type* type);
Type* type_create_033();
void type_destroy_033(Type* type);
int type_equals_033(Type* a, Type* b);
int type_assignable_033(Type* from, Type* to);
char* type_to_string_033(Type* type);
Type* type_create_034();
void type_destroy_034(Type* type);
int type_equals_034(Type* a, Type* b);
int type_assignable_034(Type* from, Type* to);
char* type_to_string_034(Type* type);
Type* type_create_035();
void type_destroy_035(Type* type);
int type_equals_035(Type* a, Type* b);
int type_assignable_035(Type* from, Type* to);
char* type_to_string_035(Type* type);
Type* type_create_036();
void type_destroy_036(Type* type);
int type_equals_036(Type* a, Type* b);
int type_assignable_036(Type* from, Type* to);
char* type_to_string_036(Type* type);
Type* type_create_037();
void type_destroy_037(Type* type);
int type_equals_037(Type* a, Type* b);
int type_assignable_037(Type* from, Type* to);
char* type_to_string_037(Type* type);
Type* type_create_038();
void type_destroy_038(Type* type);
int type_equals_038(Type* a, Type* b);
int type_assignable_038(Type* from, Type* to);
char* type_to_string_038(Type* type);
Type* type_create_039();
void type_destroy_039(Type* type);
int type_equals_039(Type* a, Type* b);
int type_assignable_039(Type* from, Type* to);
char* type_to_string_039(Type* type);
Type* type_create_040();
void type_destroy_040(Type* type);
int type_equals_040(Type* a, Type* b);
int type_assignable_040(Type* from, Type* to);
char* type_to_string_040(Type* type);
Type* type_create_041();
void type_destroy_041(Type* type);
int type_equals_041(Type* a, Type* b);
int type_assignable_041(Type* from, Type* to);
char* type_to_string_041(Type* type);
Type* type_create_042();
void type_destroy_042(Type* type);
int type_equals_042(Type* a, Type* b);
int type_assignable_042(Type* from, Type* to);
char* type_to_string_042(Type* type);
Type* type_create_043();
void type_destroy_043(Type* type);
int type_equals_043(Type* a, Type* b);
int type_assignable_043(Type* from, Type* to);
char* type_to_string_043(Type* type);
Type* type_create_044();
void type_destroy_044(Type* type);
int type_equals_044(Type* a, Type* b);
int type_assignable_044(Type* from, Type* to);
char* type_to_string_044(Type* type);
Type* type_create_045();
void type_destroy_045(Type* type);
int type_equals_045(Type* a, Type* b);
int type_assignable_045(Type* from, Type* to);
char* type_to_string_045(Type* type);
Type* type_create_046();
void type_destroy_046(Type* type);
int type_equals_046(Type* a, Type* b);
int type_assignable_046(Type* from, Type* to);
char* type_to_string_046(Type* type);
Type* type_create_047();
void type_destroy_047(Type* type);
int type_equals_047(Type* a, Type* b);
int type_assignable_047(Type* from, Type* to);
char* type_to_string_047(Type* type);
Type* type_create_048();
void type_destroy_048(Type* type);
int type_equals_048(Type* a, Type* b);
int type_assignable_048(Type* from, Type* to);
char* type_to_string_048(Type* type);
Type* type_create_049();
void type_destroy_049(Type* type);
int type_equals_049(Type* a, Type* b);
int type_assignable_049(Type* from, Type* to);
char* type_to_string_049(Type* type);
Type* type_create_050();
void type_destroy_050(Type* type);
int type_equals_050(Type* a, Type* b);
int type_assignable_050(Type* from, Type* to);
char* type_to_string_050(Type* type);
Type* type_create_051();
void type_destroy_051(Type* type);
int type_equals_051(Type* a, Type* b);
int type_assignable_051(Type* from, Type* to);
char* type_to_string_051(Type* type);
Type* type_create_052();
void type_destroy_052(Type* type);
int type_equals_052(Type* a, Type* b);
int type_assignable_052(Type* from, Type* to);
char* type_to_string_052(Type* type);
Type* type_create_053();
void type_destroy_053(Type* type);
int type_equals_053(Type* a, Type* b);
int type_assignable_053(Type* from, Type* to);
char* type_to_string_053(Type* type);
Type* type_create_054();
void type_destroy_054(Type* type);
int type_equals_054(Type* a, Type* b);
int type_assignable_054(Type* from, Type* to);
char* type_to_string_054(Type* type);
Type* type_create_055();
void type_destroy_055(Type* type);
int type_equals_055(Type* a, Type* b);
int type_assignable_055(Type* from, Type* to);
char* type_to_string_055(Type* type);
Type* type_create_056();
void type_destroy_056(Type* type);
int type_equals_056(Type* a, Type* b);
int type_assignable_056(Type* from, Type* to);
char* type_to_string_056(Type* type);
Type* type_create_057();
void type_destroy_057(Type* type);
int type_equals_057(Type* a, Type* b);
int type_assignable_057(Type* from, Type* to);
char* type_to_string_057(Type* type);
Type* type_create_058();
void type_destroy_058(Type* type);
int type_equals_058(Type* a, Type* b);
int type_assignable_058(Type* from, Type* to);
char* type_to_string_058(Type* type);
Type* type_create_059();
void type_destroy_059(Type* type);
int type_equals_059(Type* a, Type* b);
int type_assignable_059(Type* from, Type* to);
char* type_to_string_059(Type* type);
Type* type_create_060();
void type_destroy_060(Type* type);
int type_equals_060(Type* a, Type* b);
int type_assignable_060(Type* from, Type* to);
char* type_to_string_060(Type* type);
Type* type_create_061();
void type_destroy_061(Type* type);
int type_equals_061(Type* a, Type* b);
int type_assignable_061(Type* from, Type* to);
char* type_to_string_061(Type* type);
Type* type_create_062();
void type_destroy_062(Type* type);
int type_equals_062(Type* a, Type* b);
int type_assignable_062(Type* from, Type* to);
char* type_to_string_062(Type* type);
Type* type_create_063();
void type_destroy_063(Type* type);
int type_equals_063(Type* a, Type* b);
int type_assignable_063(Type* from, Type* to);
char* type_to_string_063(Type* type);
Type* type_create_064();
void type_destroy_064(Type* type);
int type_equals_064(Type* a, Type* b);
int type_assignable_064(Type* from, Type* to);
char* type_to_string_064(Type* type);
Type* type_create_065();
void type_destroy_065(Type* type);
int type_equals_065(Type* a, Type* b);
int type_assignable_065(Type* from, Type* to);
char* type_to_string_065(Type* type);
Type* type_create_066();
void type_destroy_066(Type* type);
int type_equals_066(Type* a, Type* b);
int type_assignable_066(Type* from, Type* to);
char* type_to_string_066(Type* type);
Type* type_create_067();
void type_destroy_067(Type* type);
int type_equals_067(Type* a, Type* b);
int type_assignable_067(Type* from, Type* to);
char* type_to_string_067(Type* type);
Type* type_create_068();
void type_destroy_068(Type* type);
int type_equals_068(Type* a, Type* b);
int type_assignable_068(Type* from, Type* to);
char* type_to_string_068(Type* type);
Type* type_create_069();
void type_destroy_069(Type* type);
int type_equals_069(Type* a, Type* b);
int type_assignable_069(Type* from, Type* to);
char* type_to_string_069(Type* type);
Type* type_create_070();
void type_destroy_070(Type* type);
int type_equals_070(Type* a, Type* b);
int type_assignable_070(Type* from, Type* to);
char* type_to_string_070(Type* type);
Type* type_create_071();
void type_destroy_071(Type* type);
int type_equals_071(Type* a, Type* b);
int type_assignable_071(Type* from, Type* to);
char* type_to_string_071(Type* type);
Type* type_create_072();
void type_destroy_072(Type* type);
int type_equals_072(Type* a, Type* b);
int type_assignable_072(Type* from, Type* to);
char* type_to_string_072(Type* type);
Type* type_create_073();
void type_destroy_073(Type* type);
int type_equals_073(Type* a, Type* b);
int type_assignable_073(Type* from, Type* to);
char* type_to_string_073(Type* type);
Type* type_create_074();
void type_destroy_074(Type* type);
int type_equals_074(Type* a, Type* b);
int type_assignable_074(Type* from, Type* to);
char* type_to_string_074(Type* type);
Type* type_create_075();
void type_destroy_075(Type* type);
int type_equals_075(Type* a, Type* b);
int type_assignable_075(Type* from, Type* to);
char* type_to_string_075(Type* type);
Type* type_create_076();
void type_destroy_076(Type* type);
int type_equals_076(Type* a, Type* b);
int type_assignable_076(Type* from, Type* to);
char* type_to_string_076(Type* type);
Type* type_create_077();
void type_destroy_077(Type* type);
int type_equals_077(Type* a, Type* b);
int type_assignable_077(Type* from, Type* to);
char* type_to_string_077(Type* type);
Type* type_create_078();
void type_destroy_078(Type* type);
int type_equals_078(Type* a, Type* b);
int type_assignable_078(Type* from, Type* to);
char* type_to_string_078(Type* type);
Type* type_create_079();
void type_destroy_079(Type* type);
int type_equals_079(Type* a, Type* b);
int type_assignable_079(Type* from, Type* to);
char* type_to_string_079(Type* type);
Type* type_create_080();
void type_destroy_080(Type* type);
int type_equals_080(Type* a, Type* b);
int type_assignable_080(Type* from, Type* to);
char* type_to_string_080(Type* type);
Type* type_create_081();
void type_destroy_081(Type* type);
int type_equals_081(Type* a, Type* b);
int type_assignable_081(Type* from, Type* to);
char* type_to_string_081(Type* type);
Type* type_create_082();
void type_destroy_082(Type* type);
int type_equals_082(Type* a, Type* b);
int type_assignable_082(Type* from, Type* to);
char* type_to_string_082(Type* type);
Type* type_create_083();
void type_destroy_083(Type* type);
int type_equals_083(Type* a, Type* b);
int type_assignable_083(Type* from, Type* to);
char* type_to_string_083(Type* type);
Type* type_create_084();
void type_destroy_084(Type* type);
int type_equals_084(Type* a, Type* b);
int type_assignable_084(Type* from, Type* to);
char* type_to_string_084(Type* type);
Type* type_create_085();
void type_destroy_085(Type* type);
int type_equals_085(Type* a, Type* b);
int type_assignable_085(Type* from, Type* to);
char* type_to_string_085(Type* type);
Type* type_create_086();
void type_destroy_086(Type* type);
int type_equals_086(Type* a, Type* b);
int type_assignable_086(Type* from, Type* to);
char* type_to_string_086(Type* type);
Type* type_create_087();
void type_destroy_087(Type* type);
int type_equals_087(Type* a, Type* b);
int type_assignable_087(Type* from, Type* to);
char* type_to_string_087(Type* type);
Type* type_create_088();
void type_destroy_088(Type* type);
int type_equals_088(Type* a, Type* b);
int type_assignable_088(Type* from, Type* to);
char* type_to_string_088(Type* type);
Type* type_create_089();
void type_destroy_089(Type* type);
int type_equals_089(Type* a, Type* b);
int type_assignable_089(Type* from, Type* to);
char* type_to_string_089(Type* type);
Type* type_create_090();
void type_destroy_090(Type* type);
int type_equals_090(Type* a, Type* b);
int type_assignable_090(Type* from, Type* to);
char* type_to_string_090(Type* type);
Type* type_create_091();
void type_destroy_091(Type* type);
int type_equals_091(Type* a, Type* b);
int type_assignable_091(Type* from, Type* to);
char* type_to_string_091(Type* type);
Type* type_create_092();
void type_destroy_092(Type* type);
int type_equals_092(Type* a, Type* b);
int type_assignable_092(Type* from, Type* to);
char* type_to_string_092(Type* type);
Type* type_create_093();
void type_destroy_093(Type* type);
int type_equals_093(Type* a, Type* b);
int type_assignable_093(Type* from, Type* to);
char* type_to_string_093(Type* type);
Type* type_create_094();
void type_destroy_094(Type* type);
int type_equals_094(Type* a, Type* b);
int type_assignable_094(Type* from, Type* to);
char* type_to_string_094(Type* type);
Type* type_create_095();
void type_destroy_095(Type* type);
int type_equals_095(Type* a, Type* b);
int type_assignable_095(Type* from, Type* to);
char* type_to_string_095(Type* type);
Type* type_create_096();
void type_destroy_096(Type* type);
int type_equals_096(Type* a, Type* b);
int type_assignable_096(Type* from, Type* to);
char* type_to_string_096(Type* type);
Type* type_create_097();
void type_destroy_097(Type* type);
int type_equals_097(Type* a, Type* b);
int type_assignable_097(Type* from, Type* to);
char* type_to_string_097(Type* type);
Type* type_create_098();
void type_destroy_098(Type* type);
int type_equals_098(Type* a, Type* b);
int type_assignable_098(Type* from, Type* to);
char* type_to_string_098(Type* type);
Type* type_create_099();
void type_destroy_099(Type* type);
int type_equals_099(Type* a, Type* b);
int type_assignable_099(Type* from, Type* to);
char* type_to_string_099(Type* type);
Type* type_create_100();
void type_destroy_100(Type* type);
int type_equals_100(Type* a, Type* b);
int type_assignable_100(Type* from, Type* to);
char* type_to_string_100(Type* type);
Type* type_create_101();
void type_destroy_101(Type* type);
int type_equals_101(Type* a, Type* b);
int type_assignable_101(Type* from, Type* to);
char* type_to_string_101(Type* type);
Type* type_create_102();
void type_destroy_102(Type* type);
int type_equals_102(Type* a, Type* b);
int type_assignable_102(Type* from, Type* to);
char* type_to_string_102(Type* type);
Type* type_create_103();
void type_destroy_103(Type* type);
int type_equals_103(Type* a, Type* b);
int type_assignable_103(Type* from, Type* to);
char* type_to_string_103(Type* type);
Type* type_create_104();
void type_destroy_104(Type* type);
int type_equals_104(Type* a, Type* b);
int type_assignable_104(Type* from, Type* to);
char* type_to_string_104(Type* type);
Type* type_create_105();
void type_destroy_105(Type* type);
int type_equals_105(Type* a, Type* b);
int type_assignable_105(Type* from, Type* to);
char* type_to_string_105(Type* type);
Type* type_create_106();
void type_destroy_106(Type* type);
int type_equals_106(Type* a, Type* b);
int type_assignable_106(Type* from, Type* to);
char* type_to_string_106(Type* type);
Type* type_create_107();
void type_destroy_107(Type* type);
int type_equals_107(Type* a, Type* b);
int type_assignable_107(Type* from, Type* to);
char* type_to_string_107(Type* type);
Type* type_create_108();
void type_destroy_108(Type* type);
int type_equals_108(Type* a, Type* b);
int type_assignable_108(Type* from, Type* to);
char* type_to_string_108(Type* type);
Type* type_create_109();
void type_destroy_109(Type* type);
int type_equals_109(Type* a, Type* b);
int type_assignable_109(Type* from, Type* to);
char* type_to_string_109(Type* type);
Type* type_create_110();
void type_destroy_110(Type* type);
int type_equals_110(Type* a, Type* b);
int type_assignable_110(Type* from, Type* to);
char* type_to_string_110(Type* type);
Type* type_create_111();
void type_destroy_111(Type* type);
int type_equals_111(Type* a, Type* b);
int type_assignable_111(Type* from, Type* to);
char* type_to_string_111(Type* type);
Type* type_create_112();
void type_destroy_112(Type* type);
int type_equals_112(Type* a, Type* b);
int type_assignable_112(Type* from, Type* to);
char* type_to_string_112(Type* type);
Type* type_create_113();
void type_destroy_113(Type* type);
int type_equals_113(Type* a, Type* b);
int type_assignable_113(Type* from, Type* to);
char* type_to_string_113(Type* type);
Type* type_create_114();
void type_destroy_114(Type* type);
int type_equals_114(Type* a, Type* b);
int type_assignable_114(Type* from, Type* to);
char* type_to_string_114(Type* type);
Type* type_create_115();
void type_destroy_115(Type* type);
int type_equals_115(Type* a, Type* b);
int type_assignable_115(Type* from, Type* to);
char* type_to_string_115(Type* type);
Type* type_create_116();
void type_destroy_116(Type* type);
int type_equals_116(Type* a, Type* b);
int type_assignable_116(Type* from, Type* to);
char* type_to_string_116(Type* type);
Type* type_create_117();
void type_destroy_117(Type* type);
int type_equals_117(Type* a, Type* b);
int type_assignable_117(Type* from, Type* to);
char* type_to_string_117(Type* type);
Type* type_create_118();
void type_destroy_118(Type* type);
int type_equals_118(Type* a, Type* b);
int type_assignable_118(Type* from, Type* to);
char* type_to_string_118(Type* type);
Type* type_create_119();
void type_destroy_119(Type* type);
int type_equals_119(Type* a, Type* b);
int type_assignable_119(Type* from, Type* to);
char* type_to_string_119(Type* type);
Type* type_create_120();
void type_destroy_120(Type* type);
int type_equals_120(Type* a, Type* b);
int type_assignable_120(Type* from, Type* to);
char* type_to_string_120(Type* type);
Type* type_create_121();
void type_destroy_121(Type* type);
int type_equals_121(Type* a, Type* b);
int type_assignable_121(Type* from, Type* to);
char* type_to_string_121(Type* type);
Type* type_create_122();
void type_destroy_122(Type* type);
int type_equals_122(Type* a, Type* b);
int type_assignable_122(Type* from, Type* to);
char* type_to_string_122(Type* type);
Type* type_create_123();
void type_destroy_123(Type* type);
int type_equals_123(Type* a, Type* b);
int type_assignable_123(Type* from, Type* to);
char* type_to_string_123(Type* type);
Type* type_create_124();
void type_destroy_124(Type* type);
int type_equals_124(Type* a, Type* b);
int type_assignable_124(Type* from, Type* to);
char* type_to_string_124(Type* type);
Type* type_create_125();
void type_destroy_125(Type* type);
int type_equals_125(Type* a, Type* b);
int type_assignable_125(Type* from, Type* to);
char* type_to_string_125(Type* type);
Type* type_create_126();
void type_destroy_126(Type* type);
int type_equals_126(Type* a, Type* b);
int type_assignable_126(Type* from, Type* to);
char* type_to_string_126(Type* type);
Type* type_create_127();
void type_destroy_127(Type* type);
int type_equals_127(Type* a, Type* b);
int type_assignable_127(Type* from, Type* to);
char* type_to_string_127(Type* type);
Type* type_create_128();
void type_destroy_128(Type* type);
int type_equals_128(Type* a, Type* b);
int type_assignable_128(Type* from, Type* to);
char* type_to_string_128(Type* type);
Type* type_create_129();
void type_destroy_129(Type* type);
int type_equals_129(Type* a, Type* b);
int type_assignable_129(Type* from, Type* to);
char* type_to_string_129(Type* type);
Type* type_create_130();
void type_destroy_130(Type* type);
int type_equals_130(Type* a, Type* b);
int type_assignable_130(Type* from, Type* to);
char* type_to_string_130(Type* type);
Type* type_create_131();
void type_destroy_131(Type* type);
int type_equals_131(Type* a, Type* b);
int type_assignable_131(Type* from, Type* to);
char* type_to_string_131(Type* type);
Type* type_create_132();
void type_destroy_132(Type* type);
int type_equals_132(Type* a, Type* b);
int type_assignable_132(Type* from, Type* to);
char* type_to_string_132(Type* type);
Type* type_create_133();
void type_destroy_133(Type* type);
int type_equals_133(Type* a, Type* b);
int type_assignable_133(Type* from, Type* to);
char* type_to_string_133(Type* type);
Type* type_create_134();
void type_destroy_134(Type* type);
int type_equals_134(Type* a, Type* b);
int type_assignable_134(Type* from, Type* to);
char* type_to_string_134(Type* type);
Type* type_create_135();
void type_destroy_135(Type* type);
int type_equals_135(Type* a, Type* b);
int type_assignable_135(Type* from, Type* to);
char* type_to_string_135(Type* type);
Type* type_create_136();
void type_destroy_136(Type* type);
int type_equals_136(Type* a, Type* b);
int type_assignable_136(Type* from, Type* to);
char* type_to_string_136(Type* type);
Type* type_create_137();
void type_destroy_137(Type* type);
int type_equals_137(Type* a, Type* b);
int type_assignable_137(Type* from, Type* to);
char* type_to_string_137(Type* type);
Type* type_create_138();
void type_destroy_138(Type* type);
int type_equals_138(Type* a, Type* b);
int type_assignable_138(Type* from, Type* to);
char* type_to_string_138(Type* type);
Type* type_create_139();
void type_destroy_139(Type* type);
int type_equals_139(Type* a, Type* b);
int type_assignable_139(Type* from, Type* to);
char* type_to_string_139(Type* type);
Type* type_create_140();
void type_destroy_140(Type* type);
int type_equals_140(Type* a, Type* b);
int type_assignable_140(Type* from, Type* to);
char* type_to_string_140(Type* type);
Type* type_create_141();
void type_destroy_141(Type* type);
int type_equals_141(Type* a, Type* b);
int type_assignable_141(Type* from, Type* to);
char* type_to_string_141(Type* type);
Type* type_create_142();
void type_destroy_142(Type* type);
int type_equals_142(Type* a, Type* b);
int type_assignable_142(Type* from, Type* to);
char* type_to_string_142(Type* type);
Type* type_create_143();
void type_destroy_143(Type* type);
int type_equals_143(Type* a, Type* b);
int type_assignable_143(Type* from, Type* to);
char* type_to_string_143(Type* type);
Type* type_create_144();
void type_destroy_144(Type* type);
int type_equals_144(Type* a, Type* b);
int type_assignable_144(Type* from, Type* to);
char* type_to_string_144(Type* type);
Type* type_create_145();
void type_destroy_145(Type* type);
int type_equals_145(Type* a, Type* b);
int type_assignable_145(Type* from, Type* to);
char* type_to_string_145(Type* type);
Type* type_create_146();
void type_destroy_146(Type* type);
int type_equals_146(Type* a, Type* b);
int type_assignable_146(Type* from, Type* to);
char* type_to_string_146(Type* type);
Type* type_create_147();
void type_destroy_147(Type* type);
int type_equals_147(Type* a, Type* b);
int type_assignable_147(Type* from, Type* to);
char* type_to_string_147(Type* type);
Type* type_create_148();
void type_destroy_148(Type* type);
int type_equals_148(Type* a, Type* b);
int type_assignable_148(Type* from, Type* to);
char* type_to_string_148(Type* type);
Type* type_create_149();
void type_destroy_149(Type* type);
int type_equals_149(Type* a, Type* b);
int type_assignable_149(Type* from, Type* to);
char* type_to_string_149(Type* type);
Type* type_create_150();
void type_destroy_150(Type* type);
int type_equals_150(Type* a, Type* b);
int type_assignable_150(Type* from, Type* to);
char* type_to_string_150(Type* type);
Type* type_create_151();
void type_destroy_151(Type* type);
int type_equals_151(Type* a, Type* b);
int type_assignable_151(Type* from, Type* to);
char* type_to_string_151(Type* type);
Type* type_create_152();
void type_destroy_152(Type* type);
int type_equals_152(Type* a, Type* b);
int type_assignable_152(Type* from, Type* to);
char* type_to_string_152(Type* type);
Type* type_create_153();
void type_destroy_153(Type* type);
int type_equals_153(Type* a, Type* b);
int type_assignable_153(Type* from, Type* to);
char* type_to_string_153(Type* type);
Type* type_create_154();
void type_destroy_154(Type* type);
int type_equals_154(Type* a, Type* b);
int type_assignable_154(Type* from, Type* to);
char* type_to_string_154(Type* type);
Type* type_create_155();
void type_destroy_155(Type* type);
int type_equals_155(Type* a, Type* b);
int type_assignable_155(Type* from, Type* to);
char* type_to_string_155(Type* type);
Type* type_create_156();
void type_destroy_156(Type* type);
int type_equals_156(Type* a, Type* b);
int type_assignable_156(Type* from, Type* to);
char* type_to_string_156(Type* type);
Type* type_create_157();
void type_destroy_157(Type* type);
int type_equals_157(Type* a, Type* b);
int type_assignable_157(Type* from, Type* to);
char* type_to_string_157(Type* type);
Type* type_create_158();
void type_destroy_158(Type* type);
int type_equals_158(Type* a, Type* b);
int type_assignable_158(Type* from, Type* to);
char* type_to_string_158(Type* type);
Type* type_create_159();
void type_destroy_159(Type* type);
int type_equals_159(Type* a, Type* b);
int type_assignable_159(Type* from, Type* to);
char* type_to_string_159(Type* type);
Type* type_create_160();
void type_destroy_160(Type* type);
int type_equals_160(Type* a, Type* b);
int type_assignable_160(Type* from, Type* to);
char* type_to_string_160(Type* type);
Type* type_create_161();
void type_destroy_161(Type* type);
int type_equals_161(Type* a, Type* b);
int type_assignable_161(Type* from, Type* to);
char* type_to_string_161(Type* type);
Type* type_create_162();
void type_destroy_162(Type* type);
int type_equals_162(Type* a, Type* b);
int type_assignable_162(Type* from, Type* to);
char* type_to_string_162(Type* type);
Type* type_create_163();
void type_destroy_163(Type* type);
int type_equals_163(Type* a, Type* b);
int type_assignable_163(Type* from, Type* to);
char* type_to_string_163(Type* type);
Type* type_create_164();
void type_destroy_164(Type* type);
int type_equals_164(Type* a, Type* b);
int type_assignable_164(Type* from, Type* to);
char* type_to_string_164(Type* type);
Type* type_create_165();
void type_destroy_165(Type* type);
int type_equals_165(Type* a, Type* b);
int type_assignable_165(Type* from, Type* to);
char* type_to_string_165(Type* type);
Type* type_create_166();
void type_destroy_166(Type* type);
int type_equals_166(Type* a, Type* b);
int type_assignable_166(Type* from, Type* to);
char* type_to_string_166(Type* type);
Type* type_create_167();
void type_destroy_167(Type* type);
int type_equals_167(Type* a, Type* b);
int type_assignable_167(Type* from, Type* to);
char* type_to_string_167(Type* type);
Type* type_create_168();
void type_destroy_168(Type* type);
int type_equals_168(Type* a, Type* b);
int type_assignable_168(Type* from, Type* to);
char* type_to_string_168(Type* type);
Type* type_create_169();
void type_destroy_169(Type* type);
int type_equals_169(Type* a, Type* b);
int type_assignable_169(Type* from, Type* to);
char* type_to_string_169(Type* type);
Type* type_create_170();
void type_destroy_170(Type* type);
int type_equals_170(Type* a, Type* b);
int type_assignable_170(Type* from, Type* to);
char* type_to_string_170(Type* type);
Type* type_create_171();
void type_destroy_171(Type* type);
int type_equals_171(Type* a, Type* b);
int type_assignable_171(Type* from, Type* to);
char* type_to_string_171(Type* type);
Type* type_create_172();
void type_destroy_172(Type* type);
int type_equals_172(Type* a, Type* b);
int type_assignable_172(Type* from, Type* to);
char* type_to_string_172(Type* type);
Type* type_create_173();
void type_destroy_173(Type* type);
int type_equals_173(Type* a, Type* b);
int type_assignable_173(Type* from, Type* to);
char* type_to_string_173(Type* type);
Type* type_create_174();
void type_destroy_174(Type* type);
int type_equals_174(Type* a, Type* b);
int type_assignable_174(Type* from, Type* to);
char* type_to_string_174(Type* type);
Type* type_create_175();
void type_destroy_175(Type* type);
int type_equals_175(Type* a, Type* b);
int type_assignable_175(Type* from, Type* to);
char* type_to_string_175(Type* type);
Type* type_create_176();
void type_destroy_176(Type* type);
int type_equals_176(Type* a, Type* b);
int type_assignable_176(Type* from, Type* to);
char* type_to_string_176(Type* type);
Type* type_create_177();
void type_destroy_177(Type* type);
int type_equals_177(Type* a, Type* b);
int type_assignable_177(Type* from, Type* to);
char* type_to_string_177(Type* type);
Type* type_create_178();
void type_destroy_178(Type* type);
int type_equals_178(Type* a, Type* b);
int type_assignable_178(Type* from, Type* to);
char* type_to_string_178(Type* type);
Type* type_create_179();
void type_destroy_179(Type* type);
int type_equals_179(Type* a, Type* b);
int type_assignable_179(Type* from, Type* to);
char* type_to_string_179(Type* type);
Type* type_create_180();
void type_destroy_180(Type* type);
int type_equals_180(Type* a, Type* b);
int type_assignable_180(Type* from, Type* to);
char* type_to_string_180(Type* type);
Type* type_create_181();
void type_destroy_181(Type* type);
int type_equals_181(Type* a, Type* b);
int type_assignable_181(Type* from, Type* to);
char* type_to_string_181(Type* type);
Type* type_create_182();
void type_destroy_182(Type* type);
int type_equals_182(Type* a, Type* b);
int type_assignable_182(Type* from, Type* to);
char* type_to_string_182(Type* type);
Type* type_create_183();
void type_destroy_183(Type* type);
int type_equals_183(Type* a, Type* b);
int type_assignable_183(Type* from, Type* to);
char* type_to_string_183(Type* type);
Type* type_create_184();
void type_destroy_184(Type* type);
int type_equals_184(Type* a, Type* b);
int type_assignable_184(Type* from, Type* to);
char* type_to_string_184(Type* type);
Type* type_create_185();
void type_destroy_185(Type* type);
int type_equals_185(Type* a, Type* b);
int type_assignable_185(Type* from, Type* to);
char* type_to_string_185(Type* type);
Type* type_create_186();
void type_destroy_186(Type* type);
int type_equals_186(Type* a, Type* b);
int type_assignable_186(Type* from, Type* to);
char* type_to_string_186(Type* type);
Type* type_create_187();
void type_destroy_187(Type* type);
int type_equals_187(Type* a, Type* b);
int type_assignable_187(Type* from, Type* to);
char* type_to_string_187(Type* type);
Type* type_create_188();
void type_destroy_188(Type* type);
int type_equals_188(Type* a, Type* b);
int type_assignable_188(Type* from, Type* to);
char* type_to_string_188(Type* type);
Type* type_create_189();
void type_destroy_189(Type* type);
int type_equals_189(Type* a, Type* b);
int type_assignable_189(Type* from, Type* to);
char* type_to_string_189(Type* type);
Type* type_create_190();
void type_destroy_190(Type* type);
int type_equals_190(Type* a, Type* b);
int type_assignable_190(Type* from, Type* to);
char* type_to_string_190(Type* type);
Type* type_create_191();
void type_destroy_191(Type* type);
int type_equals_191(Type* a, Type* b);
int type_assignable_191(Type* from, Type* to);
char* type_to_string_191(Type* type);
Type* type_create_192();
void type_destroy_192(Type* type);
int type_equals_192(Type* a, Type* b);
int type_assignable_192(Type* from, Type* to);
char* type_to_string_192(Type* type);
Type* type_create_193();
void type_destroy_193(Type* type);
int type_equals_193(Type* a, Type* b);
int type_assignable_193(Type* from, Type* to);
char* type_to_string_193(Type* type);
Type* type_create_194();
void type_destroy_194(Type* type);
int type_equals_194(Type* a, Type* b);
int type_assignable_194(Type* from, Type* to);
char* type_to_string_194(Type* type);
Type* type_create_195();
void type_destroy_195(Type* type);
int type_equals_195(Type* a, Type* b);
int type_assignable_195(Type* from, Type* to);
char* type_to_string_195(Type* type);
Type* type_create_196();
void type_destroy_196(Type* type);
int type_equals_196(Type* a, Type* b);
int type_assignable_196(Type* from, Type* to);
char* type_to_string_196(Type* type);
Type* type_create_197();
void type_destroy_197(Type* type);
int type_equals_197(Type* a, Type* b);
int type_assignable_197(Type* from, Type* to);
char* type_to_string_197(Type* type);
Type* type_create_198();
void type_destroy_198(Type* type);
int type_equals_198(Type* a, Type* b);
int type_assignable_198(Type* from, Type* to);
char* type_to_string_198(Type* type);
Type* type_create_199();
void type_destroy_199(Type* type);
int type_equals_199(Type* a, Type* b);
int type_assignable_199(Type* from, Type* to);
char* type_to_string_199(Type* type);
Type* type_create(TypeKind kind);
void type_destroy(Type* type);
int type_equals(Type* a, Type* b);
int type_assignable(Type* from, Type* to);
char* type_to_string(Type* type);
Type* type_pointer(Type* base);
Type* type_array(Type* element, int size);
Type* type_function(Type* ret, Type** params, int count);
Type* type_struct(const char* name, Field* fields, int count);
Type* type_union(const char* name, Field* fields, int count);
Type* type_enum(const char* name, char** values, int count);
Type* type_interface(const char* name, Method* methods, int count);
Type* type_generic(Type* base, Type** args, int count);
Type* type_optional(Type* inner);
Type* type_result(Type* ok, Type* err);
Type* type_async(Type* inner);
Type* type_generator(Type* yield, Type* return_type);
Type* type_iterator(Type* element);
Type* type_promise(Type* value);
Type* type_future(Type* value);
Type* type_channel(Type* element);
Type* type_coroutine(Type* return_type);
Type* type_thread(Type* return_type);

#endif /* AURORA_TYPE_H */