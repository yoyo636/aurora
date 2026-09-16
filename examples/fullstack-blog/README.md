# fullstack-blog — 全栈博客应用

基于 `std.web` 的 REST 风格博客服务示例。用 Aurora 一个文件起服务器，另一个文件定义数据模型，演示路由、JSON 响应、路径参数与查询参数。

## 功能介绍

| 路由 | 方法 | 说明 |
| --- | --- | --- |
| `/` | GET | 返回 HTML 首页 |
| `/posts` | GET | 文章列表（JSON），支持 `?tag=xxx` 查询参数过滤 |
| `/posts/:id` | GET | 单篇文章详情（JSON），`:id` 为路径参数 |
| `/posts` | POST | 读取 JSON 请求体，创建新文章 |

涉及的核心 API：

- `web.App("name")` —— 创建应用实例
- `app.router.add_route("GET", "/path", handler)` —— 注册路由
- `fn handler(req)` —— 处理函数，接收 `req` 请求对象
- `req.method` / `req.path` / `req.query` / `req.params` / `req.body` / `req.json` —— 请求信息
- `web.Response.json(data)` / `web.Response.html(content)` / `web.Response.text(content)` —— 构造响应
- `app.run(port=8080)` —— 启动 HTTP 服务

## 文件结构

```
fullstack-blog/
├── main.aur     # 入口:创建 web.App、注册路由、启动服务
├── models.aur   # Post / User 结构体定义与 dict 映射函数
└── README.md
```

## 运行方式

```bash
cd examples/fullstack-blog
../../aurora-run run main.aur
```

启动后另开终端测试接口：

```bash
# 文章列表
curl http://127.0.0.1:8080/posts

# 按标签过滤
curl "http://127.0.0.1:8080/posts?tag=web"

# 单篇文章(路径参数)
curl http://127.0.0.1:8080/posts/1

# 新建文章(POST + JSON)
curl -X POST http://127.0.0.1:8080/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"新文章","content":"内容","author_id":1,"tags":["demo"]}'
```

也可只做语法静态检查：

```bash
../../aurora-run check main.aur
```

## 说明

- 数据保存在内存里（`var posts = [...]`），服务重启后清空，便于演示。
- `models.aur` 中的 `struct` 用于声明数据形状；`post_to_dict` / `user_to_dict` 演示 struct → 字典的手动映射。
- 本示例为 v3.2.0 概念演示，实际运行需要解释器注册 `std.web` 模块支持。
