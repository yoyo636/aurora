import zipfile, os, shutil

SRC = "/Users/wuyuanduo/aurora/vscode-aurora"
VERSION = "3.2.0"
TMP = "/tmp/aurora-ide-{}.vsix".format(VERSION)
DEST1 = "/Users/wuyuanduo/aurora/vscode-aurora-{}.vsix".format(VERSION)
DEST2 = "/Users/wuyuanduo/aurora/vscode-aurora/aurora-{}.vsix".format(VERSION)

manifest = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">\n'
    "  <Metadata>\n"
    '    <Identity Language="zh-cn" Id="aurora-ide" Version="' + VERSION + '" Publisher="aurora"/>\n'
    "    <DisplayName>Aurora Language (v3)</DisplayName>\n"
    '    <Description xml:space="preserve">Aurora 编程语言支持 v3.2.0:语法高亮、一键运行、静态检查、行内诊断,内置格式化、性能分析、调试、LSP、包管理、AI 引擎与全平台开发工具;新增全栈脚手架、代码生成、数据库管理、开发模式与部署</Description>\n'
    "    <Tags>aurora,language,programming</Tags>\n"
    "    <GalleryFlags>Public</GalleryFlags>\n"
    "  </Metadata>\n"
    "  <Installation>\n"
    '    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>\n'
    "  </Installation>\n"
    "  <Dependencies/>\n"
    "  <Assets>\n"
    '    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json"/>\n'
    '    <Asset Type="Microsoft.VisualStudio.Code.Icon" Path="extension/icons/aurora.png"/>\n'
    "  </Assets>\n"
    "</PackageManifest>\n"
)

content_types = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
    '  <Default Extension="vsixmanifest" ContentType="text/xml"/>\n'
    '  <Default Extension="json" ContentType="application/json"/>\n'
    '  <Default Extension="js" ContentType="text/plain"/>\n'
    '  <Default Extension="png" ContentType="image/png"/>\n'
    '  <Default Extension="md" ContentType="text/plain"/>\n'
    "</Types>\n"
)

with zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", manifest)
    z.writestr("[Content_Types].xml", content_types)
    for root, dirs, files in os.walk(SRC):
        for f in files:
            if f.endswith(".vsix"):
                continue
            full = os.path.join(root, f)
            arc = "extension/" + os.path.relpath(full, SRC)
            z.write(full, arc)

shutil.copy(TMP, DEST1)
shutil.copy(TMP, DEST2)

for p in (DEST1, DEST2):
    print("vsix:", p, os.path.getsize(p), "bytes")
