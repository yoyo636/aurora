# web-app — TodoList Web 应用示例

基于 Aurora Web 框架构建的组件化 TodoList，编译为 **WebAssembly** 运行在浏览器。

## 展示内容

- `@component`：声明式组件（返回虚拟 DOM 节点）
- 虚拟 DOM：自动 diff 与最小化重渲染
- `router`：客户端路由（`/` 与 `/about`）
- 状态管理：全局 store + 不可变更新
- DOM 事件：`on("click", ...)` / `on("keydown", ...)`

## 运行（开发模式）

```bash
aurora run web_app.aur
```

## 打包为 PWA

```bash
aurora package web --pwa
```

产物位于 `target/web/`，生成静态站点 + Service Worker + manifest，
可直接部署到任意静态托管（GitHub Pages / Cloudflare Pages / Vercel）。
