# gui — 原生计算器示例

基于 **AuroraUI**（内置声明式 UI 框架）构建的桌面计算器，展示 v3.1.0 的
全平台 GUI 开发能力。

## 展示内容

- `Window`：原生窗口，跨平台（macOS / Windows / Linux）
- `Button` / `Label`：基础控件与样式类
- `Grid`：响应式网格布局
- 事件处理：`on_click(fn() { ... })` 闭包回调
- CSS 样式：`css.parse(...)` 定义主题

## 运行

```bash
aurora run calculator.aur
```

## 打包为原生应用

```bash
aurora package gui       # 当前平台原生包
aurora package macos     # 交叉构建 .app（仅在 macOS 上）
```

> 本示例为展示性代码：AuroraUI 的窗口后端在 v3.1.0 随 `aurora-ui` 模块提供。
