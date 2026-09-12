import zipfile, os

SRC = "/Users/wuyuanduo/aurora/vscode-aurora"
OUT = "/tmp/aurora-ide-0.3.0.vsix"

manifest = """<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="zh-cn" Id="aurora-ide" Version="0.3.0" Publisher="aurora"/>
    <DisplayName>Aurora Language</DisplayName>
    <Description xml:space="preserve">Aurora 编程语言支持:语法高亮、一键运行、静态检查与行内诊断</Description>
    <Tags>aurora,language,programming</Tags>
    <GalleryFlags>Public</GalleryFlags>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>
  </Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json"/>
    <Asset Type="Microsoft.VisualStudio.Code.Icon" Path="extension/icons/aurora.png"/>
  </Assets>
</PackageManifest>
"""

content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="vsixmanifest" ContentType="text/xml"/>
  <Default Extension="json" ContentType="application/json"/>
  <Default Extension="js" ContentType="text/plain"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="md" ContentType="text/plain"/>
</Types>
"""

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", manifest)
    z.writestr("[Content_Types].xml", content_types)
    for root, dirs, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f)
            arc = "extension/" + os.path.relpath(full, SRC)
            z.write(full, arc)
print("vsix:", OUT, os.path.getsize(OUT), "bytes")
