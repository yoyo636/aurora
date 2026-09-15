# windows-app — Windows 应用示例

通过 **Win32 绑定** 直接构建原生 Windows 桌面应用。平台特定代码由
`#[cfg(target_os = "windows")]` 守卫。

## 展示内容

- 窗口创建与 `WndProc` 消息处理
- `CreateWindowEx` 编辑框 / 按钮控件
- 系统托盘（NotifyIcon）
- 注册表读写（`RegOpenCurrentUser`）
- `MessageLoop` 主消息循环

## 运行

```powershell
aurora run win_app.aur
```

## 打包为 .exe / MSI

```powershell
aurora package windows
```

产物位于 `target/windows/`，生成单文件 `.exe` 与 WiX 打包的 `.msi` 安装器。
交叉构建仅支持在 Windows 主机上进行。
