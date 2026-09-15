"""Aurora v3.1.0 — 全平台打包工具

把一个 Aurora 项目打包为目标平台可分发包：

* macOS: ``.app`` bundle（含 ``Info.plist``、``.icns`` 图标、可选 codesign / 公证）
* Windows: ``.exe`` + NSIS ``.nsi`` 安装脚本 / WiX ``.msi``
* Linux: ``.deb`` / ``.rpm`` / AppImage
* Web: 静态站点 + PWA（``manifest.json`` + ``service-worker.js``）
* 移动端（远期）：iOS / Android WebView 壳工程

设计原则
--------
* 所有打包器**只生成文件 / 脚本**；外部工具（codesign、dpkg-deb、emcc、
  makensis、rpmbuild、appimagetool 等）不可用时不抛异常，而是落一份
  构建脚本 / 配置供用户手动执行。
* 跨平台可导入，无第三方依赖。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional

IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _which(name: str) -> Optional[str]:
    """封装 shutil.which，便于测试 monkeypatch。"""
    return shutil.which(name)


def _write(path: str, content: str) -> str:
    """写文本文件（自动建目录），返回路径。"""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _copy(src: str, dst: str) -> str:
    """复制文件，目录不存在时自动创建。"""
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)
    return dst


# ===========================================================================
# 基类
# ===========================================================================

class Packager:
    """打包器基类。子类实现 :meth:`package`。"""

    target: str = "base"

    def __init__(self, app_name: str = "AuroraApp", version: str = "1.0.0",
                 identifier: str = "com.aurora.app") -> None:
        self.app_name = app_name
        self.version = version
        self.identifier = identifier

    def package(self, project_path: str, output_dir: str, **kwargs: Any) -> str:
        """打包入口，返回产物目录路径。子类必须覆盖。"""
        raise NotImplementedError


# ===========================================================================
# macOS
# ===========================================================================

class MacOSPackager(Packager):
    """生成 ``.app`` bundle。"""

    target = "macos"

    def build_app_structure(self, output_dir: str, executable: str,
                            resources_dir: Optional[str] = None,
                            ls_ui_element: bool = False) -> str:
        """构造 ``MyApp.app/Contents/{MacOS,Resources,Frameworks}`` 目录树。

        :return: ``.app`` 目录路径。
        """
        app_dir = os.path.join(output_dir, f"{self.app_name}.app")
        contents = os.path.join(app_dir, "Contents")
        for sub in ("MacOS", "Resources", "Frameworks"):
            os.makedirs(os.path.join(contents, sub), exist_ok=True)

        # 可执行文件
        if executable and os.path.exists(executable):
            dst = os.path.join(contents, "MacOS", self.app_name)
            shutil.copy(executable, dst)
            os.chmod(dst, 0o755)

        # 资源
        if resources_dir and os.path.isdir(resources_dir):
            res_dst = os.path.join(contents, "Resources")
            for entry in os.listdir(resources_dir):
                s = os.path.join(resources_dir, entry)
                d = os.path.join(res_dst, entry)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

        self.write_info_plist(app_dir, ls_ui_element=ls_ui_element)
        return app_dir

    def write_info_plist(self, app_dir: str,
                         ls_ui_element: bool = False,
                         extra: Optional[Dict[str, Any]] = None) -> str:
        """生成 ``Contents/Info.plist``（XML plist 文本）。"""
        plist_path = os.path.join(app_dir, "Contents", "Info.plist")
        entries: List[str] = []

        def _kv(key: str, value: str) -> None:
            entries.append(f"    <key>{key}</key>\n    <string>{value}</string>")

        _kv("CFBundleName", self.app_name)
        _kv("CFBundleIdentifier", self.identifier)
        _kv("CFBundleVersion", self.version)
        _kv("CFBundleShortVersionString", self.version)
        _kv("CFBundleExecutable", self.app_name)
        _kv("NSMainNibFile", "MainMenu")

        body = "\n".join(entries)
        extra_block = ""
        if ls_ui_element:
            extra_block = (
                "    <key>LSUIElement</key>\n"
                "    <true/>\n"
            )
        if extra:
            for k, v in extra.items():
                extra_block += f"    <key>{k}</key>\n"
                if isinstance(v, bool):
                    extra_block += "    <true/>\n" if v else "    <false/>\n"
                else:
                    extra_block += f"    <string>{v}</string>\n"

        plist = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
            '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
            '<plist version="1.0">\n<dict>\n'
            f"{body}\n{extra_block}"
            '</dict>\n</plist>\n'
        )
        return _write(plist_path, plist)

    # -- 图标 ---------------------------------------------------------------

    def generate_icns(self, png_path: str, output_dir: str) -> Optional[str]:
        """从 PNG 生成 ``.icns``。优先用 ``sips`` + ``iconutil``。

        工具不可用时生成 ``icon_build.sh`` 脚本。
        """
        icns_path = os.path.join(output_dir, f"{self.app_name}.icns")
        iconset = os.path.join(output_dir, f"{self.app_name}.iconset")
        os.makedirs(iconset, exist_ok=True)

        if _which("sips") and png_path and os.path.exists(png_path):
            try:  # pragma: no cover - 依赖本机工具
                for size in (16, 32, 128, 256, 512):
                    for scale in (1, 2):
                        px = size * scale
                        out = os.path.join(
                            iconset,
                            f"icon_{size}x{size}{'@2x' if scale == 2 else ''}.png")
                        subprocess.run(
                            ["sips", "-z", str(px), str(px), png_path,
                             "--out", out], check=True, capture_output=True)
                if _which("iconutil"):
                    subprocess.run(
                        ["iconutil", "-c", "icns", iconset, "-o", icns_path],
                        check=True, capture_output=True)
                    return icns_path
            except Exception:
                pass

        # 降级：生成构建脚本
        script = (
            "#!/bin/sh\nset -e\n"
            f'mkdir -p "{iconset}"\n'
            "for s in 16 32 128 256 512; do\n"
            '  sips -z $((s*1)) $((s*1)) "%s" --out "'
            f'{iconset}/icon_${{s}}x${{s}}.png"\n'
            '  sips -z $((s*2)) $((s*2)) "%s" --out "'
            f'{iconset}/icon_${{s}}x${{s}}@2x.png"\n'
            "done\n"
            f'iconutil -c icns "{iconset}" -o "{icns_path}"\n'
        ) % (png_path, png_path)
        return _write(os.path.join(output_dir, "build_icon.sh"), script)

    # -- 代码签名 / 公证 ----------------------------------------------------

    def codesign(self, app_path: str, identity: str = "-") -> bool:
        """执行 ``codesign --deep --force``。

        :param identity: 签名身份，默认 ``-`` 表示 ad-hoc。
        :return: 命令是否执行成功；工具不可用返回 False。
        """
        if not _which("codesign"):
            return False
        try:  # pragma: no cover
            subprocess.run(
                ["codesign", "--deep", "--force", "--sign", identity, app_path],
                check=True, capture_output=True)
            return True
        except Exception:
            return False

    def notarize(self, app_path: str, apple_id: str,
                 password: str, team_id: Optional[str] = None) -> str:
        """生成公证配置 / 构建脚本（实际 ``xcrun notarytool`` 需用户凭证）。

        :return: 写出的脚本路径。
        """
        script_path = os.path.join(
            os.path.dirname(app_path), "notarize.sh")
        args = [
            "xcrun", "notarytool", "submit", app_path,
            "--apple-id", apple_id, "--password", password,
            "--wait",
        ]
        if team_id:
            args += ["--team-id", team_id]
        content = "#!/bin/sh\nset -e\n" + " ".join(args) + "\n" + \
                  f'stapler staple "{app_path}"\n'
        return _write(script_path, content)

    def package(self, project_path: str, output_dir: str,
                executable: str = "", icon: str = "",
                sign: Optional[str] = None, **kwargs: Any) -> str:
        os.makedirs(output_dir, exist_ok=True)
        app_dir = self.build_app_structure(
            output_dir, executable or os.path.join(project_path, "build", self.app_name))
        if icon:
            self.generate_icns(icon, os.path.join(app_dir, "Contents", "Resources"))
        if sign:
            self.codesign(app_dir, sign)
        return app_dir


# ===========================================================================
# Windows
# ===========================================================================

class WindowsPackager(Packager):
    """生成 Windows 可执行文件与安装包。"""

    target = "windows"

    # -- .exe ---------------------------------------------------------------

    def build_exe(self, executable: str, output_dir: str,
                  gui_subsystem: bool = True) -> str:
        """复制编译产物为 ``<app>.exe``。

        :param gui_subsystem: 是否标记为 Windows GUI 子系统（不弹控制台）。
        """
        os.makedirs(output_dir, exist_ok=True)
        dst = os.path.join(output_dir, f"{self.app_name}.exe")
        if executable and os.path.exists(executable):
            shutil.copy(executable, dst)
        else:
            _write(dst, "")  # 占位，等待真实编译产物
        return dst

    # -- 图标 ---------------------------------------------------------------

    def generate_ico(self, png_path: str, output_dir: str) -> str:
        """生成 ``.ico``（工具不可用时降级为脚本）。"""
        ico_path = os.path.join(output_dir, f"{self.app_name}.ico")
        if _which("magick") or _which("convert"):  # pragma: no cover
            tool = _which("magick") or _which("convert")
            try:
                subprocess.run(
                    [tool, png_path, "-define", "icon:size=256,128,64,48,32,16",
                     ico_path], check=True, capture_output=True)
                return ico_path
            except Exception:
                pass
        return _write(
            os.path.join(output_dir, "build_icon.sh"),
            f"#!/bin/sh\nmagick {png_path} -define icon:size=256,128,64,48,32,16 {ico_path}\n")

    # -- NSIS 安装包 --------------------------------------------------------

    def generate_nsis_script(self, exe_path: str, output_dir: str) -> str:
        """生成 NSIS ``.nsi`` 安装脚本。"""
        nsi = f"""; 生成自 Aurora v3.1.0
Unicode true
!define APPNAME "{self.app_name}"
!define VERSION "{self.version}"
!define APPID "{self.identifier}"

Name "${{APPNAME}} ${{VERSION}}"
OutFile "{self.app_name}-setup.exe"
InstallDir "$PROGRAMFILES64\\${{APPNAME}}"

Section "MainProgram"
  SectionIn RO
  SetOutPath "$INSTDIR"
  File "{exe_path}"
  CreateDirectory "$INSTDIR"

  ; 快捷方式
  CreateDirectory "$DESKTOP"
  CreateShortCut "$DESKTOP\\${{APPNAME}}.lnk" "$INSTDIR\\{self.app_name}.exe"
  CreateDirectory "$SMPROGRAMS\\${{APPNAME}}"
  CreateShortCut "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk" "$INSTDIR\\{self.app_name}.exe"

  ; 注册表
  WriteRegStr SHCTX "Software\\${{APPID}}" "Version" "${{VERSION}}"

  ; 卸载器
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\\${{APPNAME}}.lnk"
  RMDir /r "$SMPROGRAMS\\${{APPNAME}}"
  Delete "$INSTDIR\\{self.app_name}.exe"
  Delete "$INSTDIR\\Uninstall.exe"
  RMDir "$INSTDIR"
  DeleteRegKey SHCTX "Software\\${{APPID}}"
SectionEnd
"""
        return _write(os.path.join(output_dir, "installer.nsi"), nsi)

    # -- WiX / MSI ----------------------------------------------------------

    def generate_wxs(self, exe_path: str, output_dir: str) -> str:
        """生成 WiX Toolset ``.wxs``（用于 candle/light 构建 .msi）。"""
        wxs = f"""<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="{self.app_name}" Language="1033"
           Version="{self.version}" Manufacturer="Aurora"
           UpgradeCode="PUT-GUID-HERE">
    <Package InstallerVersion="200" Compressed="yes"
             InstallScope="perMachine" />
    <MediaTemplate />
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="{self.app_name}" />
      </Directory>
    </Directory>
    <Feature Id="Main" Title="{self.app_name}" Level="1">
      <Component Directory="INSTALLFOLDER">
        <File Source="{exe_path}" KeyPath="yes" />
      </Component>
    </Feature>
  </Product>
</Wix>
"""
        return _write(os.path.join(output_dir, "installer.wxs"), wxs)

    def package(self, project_path: str, output_dir: str,
                installer: str = "nsis", executable: str = "",
                icon: str = "", **kwargs: Any) -> str:
        os.makedirs(output_dir, exist_ok=True)
        exe = self.build_exe(executable, output_dir)
        if icon:
            self.generate_ico(icon, output_dir)
        if installer == "nsis":
            self.generate_nsis_script(exe, output_dir)
        elif installer == "msi":
            self.generate_wxs(exe, output_dir)
        return output_dir


# ===========================================================================
# Linux
# ===========================================================================

class LinuxPackager(Packager):
    """Linux: ``.deb`` / ``.rpm`` / AppImage。"""

    target = "linux"

    def build_deb(self, executable: str, output_dir: str,
                 maintainer: str = "dev@aurora.dev") -> str:
        """生成 .deb 包骨架（DEBIAN/control + 数据目录）。"""
        root = os.path.join(output_dir, "deb_root")
        debian = os.path.join(root, "DEBIAN")
        os.makedirs(debian, exist_ok=True)
        bin_dir = os.path.join(root, "usr", "bin")
        os.makedirs(bin_dir, exist_ok=True)
        if executable and os.path.exists(executable):
            shutil.copy(executable, os.path.join(bin_dir, self.app_name))
            os.chmod(os.path.join(bin_dir, self.app_name), 0o755)

        control = (
            f"Package: {self.app_name.lower()}\n"
            f"Version: {self.version}\n"
            "Section: utils\n"
            "Priority: optional\n"
            "Architecture: any\n"
            f"Maintainer: {maintainer}\n"
            f"Description: {self.app_name} packaged by Aurora\n"
        )
        _write(os.path.join(debian, "control"), control)

        if _which("dpkg-deb"):  # pragma: no cover
            try:
                out = os.path.join(output_dir, f"{self.app_name}_{self.version}_any.deb")
                subprocess.run(["dpkg-deb", "--build", root, out],
                               check=True, capture_output=True)
                return out
            except Exception:
                pass
        return root

    def build_rpm(self, executable: str, output_dir: str) -> str:
        """生成 rpmbuild SPEC 文件。"""
        spec = f"""Name:           {self.app_name.lower()}
Version:        {self.version}
Release:        1%{{?dist}}
Summary:        {self.app_name}
License:        MIT

%description
{self.app_name} packaged by Aurora.

%install
mkdir -p %{{buildroot}}/usr/bin
install -m 0755 {executable} %{{buildroot}}/usr/bin/{self.app_name}

%files
/usr/bin/{self.app_name}

%changelog
* Aurora v3.1.0
- autogenerated
"""
        return _write(os.path.join(output_dir, f"{self.app_name}.spec"), spec)

    def build_appimage(self, executable: str, output_dir: str) -> str:
        """生成 AppDir 骨架（+ AppRun 脚本）。"""
        appdir = os.path.join(output_dir, f"{self.app_name}.AppDir")
        usr_bin = os.path.join(appdir, "usr", "bin")
        os.makedirs(usr_bin, exist_ok=True)
        if executable and os.path.exists(executable):
            shutil.copy(executable, os.path.join(usr_bin, self.app_name))
            os.chmod(os.path.join(usr_bin, self.app_name), 0o755)
        _write(os.path.join(appdir, "AppRun"),
               f"#!/bin/sh\nexec $APPDIR/usr/bin/{self.app_name}\n")
        os.chmod(os.path.join(appdir, "AppRun"), 0o755)
        desktop = (
            f"[Desktop Entry]\nType=Application\nName={self.app_name}\n"
            f"Exec={self.app_name}\nIcon=app\nCategories=Utility;\n")
        _write(os.path.join(appdir, f"{self.app_name}.desktop"), desktop)
        return appdir

    def package(self, project_path: str, output_dir: str,
                fmt: str = "deb", executable: str = "", **kwargs: Any) -> str:
        os.makedirs(output_dir, exist_ok=True)
        if fmt == "deb":
            return self.build_deb(executable, output_dir)
        if fmt == "rpm":
            return self.build_rpm(executable, output_dir)
        if fmt == "appimage":
            return self.build_appimage(executable, output_dir)
        raise ValueError(f"未知打包格式: {fmt}")


# ===========================================================================
# Web
# ===========================================================================

class WebPackager(Packager):
    """静态站点 / PWA 打包。"""

    target = "web"

    def build_static(self, output_dir: str, title: str = "") -> str:
        """生成 index.html + 占位 JS/CSS。"""
        os.makedirs(output_dir, exist_ok=True)
        html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title or self.app_name}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="root"></div>
  <script src="app.js"></script>
</body>
</html>
"""
        _write(os.path.join(output_dir, "index.html"), html)
        _write(os.path.join(output_dir, "app.js"),
               f"// {self.app_name} — 由 Aurora v3.1.0 打包\n")
        _write(os.path.join(output_dir, "style.css"),
               f"/* {self.app_name} */\n")
        return output_dir

    def build_pwa(self, output_dir: str,
                  icons: Optional[List[Dict[str, str]]] = None) -> str:
        """生成 manifest.json 与 service-worker.js。"""
        self.build_static(output_dir)
        icons = icons or [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ]
        manifest = {
            "name": self.app_name,
            "short_name": self.app_name,
            "description": f"{self.app_name} PWA",
            "start_url": ".",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#4f46e5",
            "icons": icons,
        }
        _write(os.path.join(output_dir, "manifest.json"),
               json.dumps(manifest, indent=2, ensure_ascii=False))
        sw = """// service worker — 生成自 Aurora v3.1.0
const CACHE = 'aurora-v%s';
const ASSETS = ['.', 'index.html', 'app.js', 'style.css'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
""" % self.version
        _write(os.path.join(output_dir, "service-worker.js"), sw)
        return output_dir

    def package(self, project_path: str, output_dir: str,
                pwa: bool = False, **kwargs: Any) -> str:
        os.makedirs(output_dir, exist_ok=True)
        if pwa:
            return self.build_pwa(output_dir)
        return self.build_static(output_dir)


# ===========================================================================
# Mobile（远期）
# ===========================================================================

class MobilePackager(Packager):
    """iOS / Android WebView 壳工程生成（远期）。"""

    def build_ios(self, web_dir: str, output_dir: str) -> str:
        """生成 Xcode 工程目录骨架。"""
        proj = os.path.join(output_dir, f"{self.app_name}IOS")
        os.makedirs(os.path.join(proj, "Sources"), exist_ok=True)
        _write(os.path.join(proj, "Sources", "AppDelegate.swift"),
               "import UIKit\n@main\nclass AppDelegate: UIResponder, UIApplicationDelegate {}\n")
        _write(os.path.join(proj, "Info.plist"),
               '<?xml version="1.0"?><plist version="1.0"><dict>'
               "<key>NSAppTransportSecurity</key><dict>"
               "<key>NSAllowsArbitraryLoads</key><true/></dict></dict></plist>")
        return proj

    def build_android(self, web_dir: str, output_dir: str) -> str:
        """生成 Android 工程目录骨架。"""
        proj = os.path.join(output_dir, f"{self.app_name}Android")
        app = os.path.join(proj, "app")
        os.makedirs(os.path.join(app, "src", "main"), exist_ok=True)
        manifest = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n'
            f'  <application android:label="{self.app_name}">\n'
            '    <activity android:name=".MainActivity" android:exported="true">\n'
            '      <intent-filter>\n'
            '        <action android:name="android.intent.action.MAIN"/>\n'
            '        <category android:name="android.intent.category.LAUNCHER"/>\n'
            '      </intent-filter>\n'
            '    </activity>\n'
            '  </application>\n</manifest>\n')
        _write(os.path.join(app, "src", "main", "AndroidManifest.xml"), manifest)
        gradle = (
            "plugins { id 'com.android.application' }\n"
            f"android {{ namespace = '{self.identifier.replace('.', '_')}' "
            f"compileSdk 34 }}\n")
        _write(os.path.join(app, "build.gradle"), gradle)
        return proj

    def package(self, project_path: str, output_dir: str,
                platform: str = "ios", **kwargs: Any) -> str:
        os.makedirs(output_dir, exist_ok=True)
        if platform == "ios":
            return self.build_ios(project_path, output_dir)
        return self.build_android(project_path, output_dir)


# ===========================================================================
# CLI 注册
# ===========================================================================

def register_cli(subparsers: Any) -> None:
    """在主 CLI 上注册 ``aurora package ...`` 命令组。"""
    pkg = subparsers.add_parser("package", help="全平台打包（macos/windows/linux/web/ios/android）")
    sub = pkg.add_subparsers(dest="package_platform", help="目标平台")

    def _common(p: Any) -> None:
        p.add_argument("project", nargs="?", default=".", help="项目路径")
        p.add_argument("-o", "--output", default="dist", help="输出目录")
        p.add_argument("--name", default="AuroraApp", help="应用名")
        p.add_argument("--version", default="1.0.0", help="版本号")
        p.add_argument("--id", default="com.aurora.app", help="Bundle 标识符")

    p = sub.add_parser("macos", help="打包 macOS .app")
    _common(p)
    p.add_argument("--sign", default=None, help="codesign 签名身份")
    p.add_argument("--notarize", action="store_true", help="生成公证脚本")
    p.add_argument("--executable", default="", help="可执行文件路径")
    p.set_defaults(func=_cmd_macos)

    p = sub.add_parser("windows", help="打包 Windows .exe / 安装包")
    _common(p)
    p.add_argument("--installer", choices=["nsis", "msi"], default="nsis")
    p.add_argument("--executable", default="")
    p.set_defaults(func=_cmd_windows)

    p = sub.add_parser("linux", help="打包 Linux 发行包")
    _common(p)
    p.add_argument("--format", choices=["deb", "rpm", "appimage"], default="deb")
    p.add_argument("--executable", default="")
    p.set_defaults(func=_cmd_linux)

    p = sub.add_parser("web", help="打包 Web 静态站点 / PWA")
    _common(p)
    p.add_argument("--pwa", action="store_true", help="生成 PWA")
    p.set_defaults(func=_cmd_web)

    p = sub.add_parser("ios", help="生成 iOS WebView 壳工程（远期）")
    _common(p)
    p.set_defaults(func=_cmd_mobile("ios"))

    p = sub.add_parser("android", help="生成 Android WebView 壳工程（远期）")
    _common(p)
    p.set_defaults(func=_cmd_mobile("android"))


def _cmd_macos(args: Any) -> int:
    pk = MacOSPackager(args.name, args.version, args.id)
    out = pk.package(args.project, args.output, executable=args.executable,
                     sign=args.sign)
    print(f"[package/macos] -> {out}")
    return 0


def _cmd_windows(args: Any) -> int:
    pk = WindowsPackager(args.name, args.version, args.id)
    out = pk.package(args.project, args.output, installer=args.installer,
                     executable=args.executable)
    print(f"[package/windows] -> {out}")
    return 0


def _cmd_linux(args: Any) -> int:
    pk = LinuxPackager(args.name, args.version, args.id)
    out = pk.package(args.project, args.output, fmt=args.format,
                     executable=args.executable)
    print(f"[package/linux:{args.format}] -> {out}")
    return 0


def _cmd_web(args: Any) -> int:
    pk = WebPackager(args.name, args.version, args.id)
    out = pk.package(args.project, args.output, pwa=args.pwa)
    print(f"[package/web] -> {out}")
    return 0


def _cmd_mobile(platform: str) -> Any:
    def _run(args: Any) -> int:
        pk = MobilePackager(args.name, args.version, args.id)
        out = pk.package(args.project, args.output, platform=platform)
        print(f"[package/{platform}] -> {out}")
        return 0
    return _run


__all__ = [
    "Packager", "MacOSPackager", "WindowsPackager", "LinuxPackager",
    "WebPackager", "MobilePackager", "register_cli",
]
