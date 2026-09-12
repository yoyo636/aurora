# Aurora 生态链示例(interop)

展示 Aurora 与外部世界的互通能力。全部示例用 `./aurora-run run examples/interop/<文件>` 运行
(或 `python3 -m aurora.cli run`)。

| 示例 | 打通对象 | 说明 |
| --- | --- | --- |
| demo_ffi.aur | Rust / C++ | 通过 C ABI 加载共享库调用 |
| demo_python.aur | Python 生态 | 导入任意已安装 Python 库 |
| demo_json.aur | JSON 数据 | 解析 / 生成 / 文件读写 |
| demo_html.aur | HTML / Web | 数据渲染成网页 |
| demo_proc.aur | 多程序协同 | Aurora 编排其它程序,JSON 管道 |
| worker.aur | 被调用方 | demo_proc 启动的子程序 |
| demo_vex.aur | VEX 机器人 | 导出 VEXcode Python/C++ 工程 |
| demo_http.aur | HTTP / API | 请求 Web 接口 |

## FFI 前置构建(Rust / C++)

```bash
cd rust_math && cargo build --release     # → target/release/librust_math.dylib
clang++ -shared -fPIC -O2 cpp_math.cpp -o libcpp_math.dylib
```

## 语言侧生态模块

- `std.ffi`    — load(path) / func(lib, name, arg_types, ret_type) / cstr
- `std.python` — eval(code) / exec(code) / import(module) / call(fn, ...)
- `std.json`   — parse / stringify / load / save
- `std.html`   — escape / render({{key}} 转义、{{!key}} 原始) / page / write / open
- `std.proc`   — run / call / spawn / run_args / call_args(参数列表免引号)
- `std.http`   — get / get_json / post
- `std.vex`    — export(dir, name, code, lang) / python / cpp

原始字符串 `r'...'` 不插值,适合书写 JSON、正则、路径、外部代码片段。
