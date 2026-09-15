# macos-app — macOS 原生应用示例

通过 Aurora 的 **Cocoa 绑定** 直接构建原生 macOS 应用。所有平台特定代码都被
`#[cfg(target_os = "macos")]` 守卫，跨平台编译时自动裁剪。

## 展示内容

- `NSApplication` / `NSWindow`：应用与窗口
- `NSButton`：控件与 Action 回调
- `NSMenu`：菜单栏（标准 File / Edit / View / Help 布局）
- `NSNotification`：通知中心推送
- Dock 集成：自定义图标与未读徽章

## 运行

```bash
aurora run mac_app.aur
```

## 打包为 .app

```bash
aurora package macos
```

产物位于 `target/macos/AuroraMacDemo.app`，自动签名、嵌入 Info.plist 与
资源目录。交叉构建仅支持在 macOS 主机上进行。
