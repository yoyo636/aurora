# browser — 简单浏览器示例

一个最小可用的浏览器外壳：地址栏 + WebView + 前进/后退导航，并演示离线渲染管线。

## 展示内容

- 工具栏：后退 / 前进 / 地址栏 / Go 按钮
- `WebView` 嵌入式网页视图
- 历史记录栈（前进 / 后退）
- 渲染管线：`html.parse` → `css.parse` → `layout.build` → `paint.draw` 到 `Canvas`

## 运行

```bash
aurora run mini_browser.aur
```

## 打包

```bash
aurora package            # 当前平台原生应用
```

> 本示例为展示性代码：WebView 与布局引擎后端随 `webview` / `engine` 模块提供。
