// Aurora Language —— VSCode 扩展 (v3.2.0)
// 功能:运行 .aur 文件(集成终端)、静态检查(行内诊断)、运行选中代码
// v3.1.0 新增:AI 引擎、基准测试、工作区/依赖管理、GUI、跨平台打包、
//            Jupyter 内核、HTTP 推理服务、语言互操作、WebAssembly 编译
// v3.2.0 新增:全栈脚手架(new)、代码生成(generate)、数据库管理(db)、
//            开发模式(dev)、部署(deploy)、Web 应用脚手架(webapp)
"use strict";

const vscode = require("vscode");
const { execFile } = require("child_process");
const os = require("os");
const path = require("path");
const fs = require("fs");

const CLI = "aurora-run";
const OUT_CHANNEL_NAME = "Aurora";

function activate(context) {
  const diagnostics = vscode.languages.createDiagnosticCollection("aurora");
  const output = vscode.window.createOutputChannel(OUT_CHANNEL_NAME);
  context.subscriptions.push(diagnostics, output);

  // ── 配置 ──────────────────────────────
  function cfg() {
    return vscode.workspace.getConfiguration("aurora");
  }
  function auroraDir() {
    return cfg().get("auroraDir", path.join(os.homedir(), "aurora"));
  }
  function pythonPath() {
    return cfg().get("pythonPath", "python3");
  }
  function runCli(args, cwd, cb) {
    execFile(pythonPath(), [path.join(auroraDir(), CLI)].concat(args), { cwd: cwd || auroraDir() }, cb);
  }
  function quote(s) {
    return "'" + String(s).replace(/'/g, "'\\''") + "'";
  }
  async function ensureSaved() {
    const ed = vscode.window.activeTextEditor;
    if (ed && ed.document.isDirty) {
      await ed.document.save();
    }
    return ed;
  }
  function currentAuroraFile() {
    const ed = vscode.window.activeTextEditor;
    if (!ed || ed.document.languageId !== "aurora") {
      vscode.window.showWarningMessage("请先打开一个 .aur 文件");
      return null;
    }
    return ed;
  }

  // ── 运行:集成终端(支持 stdin 交互) ──
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.run", async () => {
      const ed = await ensureSaved();
      if (!ed || ed.document.languageId !== "aurora") {
        vscode.window.showWarningMessage("请先打开一个 .aur 文件");
        return;
      }
      const file = ed.document.fileName;
      const term = vscode.window.createTerminal({
        name: "Aurora",
        cwd: path.dirname(file),
      });
      term.show();
      term.sendText(path.join(auroraDir(), CLI) + " run " + quote(file));
    })
  );

  // ── 运行选中代码:写入临时文件执行 ──
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.runSelection", async () => {
      const ed = vscode.window.activeTextEditor;
      if (!ed || ed.document.languageId !== "aurora") {
        vscode.window.showWarningMessage("请先打开一个 .aur 文件");
        return;
      }
      const sel = ed.selection;
      const text = ed.document.getText(sel);
      if (!text.trim()) {
        vscode.window.showWarningMessage("请先选中要运行的代码");
        return;
      }
      const tmp = path.join(os.tmpdir(), "aurora_selection_" + Date.now() + ".aur");
      try {
        fs.writeFileSync(tmp, text, "utf-8");
      } catch (e) {
        vscode.window.showErrorMessage("写入临时文件失败: " + e.message);
        return;
      }
      const term = vscode.window.createTerminal({ name: "Aurora 选中代码" });
      term.show();
      term.sendText(path.join(auroraDir(), CLI) + " run " + quote(tmp));
      fs.unlink(tmp, () => {});
    })
  );

  // ── 静态检查:行内诊断 ──
  function parseProblems(text) {
    // 匹配 "L<行>:C<列>: <消息>"(check 模式 "- L1:C4: ..." 与解析错误均适用)
    const problems = [];
    const re = /L(\d+):C(\d+):\s*(.+)$/gm;
    let m;
    while ((m = re.exec(text)) !== null) {
      problems.push({ line: parseInt(m[1], 10), col: parseInt(m[2], 10), msg: m[3].trim() });
    }
    return problems;
  }

  function applyDiagnostics(uri, problems) {
    diagnostics.delete(uri);
    if (!problems.length) return;
    const items = [];
    for (const p of problems) {
      const line = Math.max(0, p.line - 1);
      const col = Math.max(0, p.col - 1);
      const rng = new vscode.Range(line, col, line, col + 1);
      items.push(new vscode.Diagnostic(rng, p.msg, vscode.DiagnosticSeverity.Error));
    }
    diagnostics.set(uri, items);
  }

  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.check", async () => {
      const ed = await ensureSaved();
      if (!ed || ed.document.languageId !== "aurora") {
        vscode.window.showWarningMessage("请先打开一个 .aur 文件");
        return;
      }
      const file = ed.document.fileName;
      vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: "Aurora 检查中…" },
        () =>
          new Promise((resolve) => {
            runCli(["check", file], path.dirname(file), (err, stdout, stderr) => {
              const text = (stdout || "") + "\n" + (stderr || "");
              const problems = parseProblems(text);
              applyDiagnostics(ed.document.uri, problems);
              output.clear();
              output.appendLine(text.trim() || "✓ 未发现问题");
              output.show(true);
              resolve();
            });
          })
      );
    })
  );

  // ── v2.0.0 新命令:格式化 / 性能分析 / 调试 / LSP / 包管理 ──
  // 统一通过集成终端调用 aurora-run 的子命令
  function termCli(args, name, cwd) {
    const term = vscode.window.createTerminal({ name: name || "Aurora" });
    term.show();
    term.sendText(path.join(auroraDir(), CLI) + " " + args.map(quote).join(" "));
  }

  async function activeAuroraFile() {
    const ed = await ensureSaved();
    if (!ed || ed.document.languageId !== "aurora") {
      vscode.window.showWarningMessage("请先打开一个 .aur 文件");
      return null;
    }
    return ed;
  }

  // 格式化:aurora fmt <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.fmt", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["fmt", ed.document.fileName], "Aurora 格式化", path.dirname(ed.document.fileName));
    })
  );

  // 性能分析:aurora profile <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.profile", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["profile", ed.document.fileName], "Aurora 性能分析", path.dirname(ed.document.fileName));
    })
  );

  // 调试:aurora debug <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.debug", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["debug", ed.document.fileName], "Aurora 调试", path.dirname(ed.document.fileName));
    })
  );

  // LSP:aurora lsp --stdio(无需打开文件,在工作区根启动)
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.lsp", async () => {
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["lsp", "--stdio"], "Aurora LSP", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // 包管理:aurora pkg <subcommand>,交互输入子命令
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.pkg", async () => {
      const pick = await vscode.window.showQuickPick(
        ["init", "add", "remove", "install", "list", "search", "publish", "outdated"],
        { placeHolder: "选择 aurora pkg 子命令" }
      );
      if (!pick) return;
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["pkg", pick], "Aurora 包管理", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // ── v3.1.0 新命令 ──────────────────────────────────
  // 统一通过集成终端调用 aurora-run 的子命令

  // AI:aurora ai train|infer <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.ai", async () => {
      const pick = await vscode.window.showQuickPick(
        ["train", "infer"],
        { placeHolder: "选择 aurora ai 子命令 (train / infer)" }
      );
      if (!pick) return;
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["ai", pick, ed.document.fileName], "Aurora AI", path.dirname(ed.document.fileName));
    })
  );

  // 性能基准测试:aurora bench <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.bench", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["bench", ed.document.fileName], "Aurora 基准测试", path.dirname(ed.document.fileName));
    })
  );

  // 工作区管理:aurora workspace init|list
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.workspace", async () => {
      const pick = await vscode.window.showQuickPick(
        ["init", "list"],
        { placeHolder: "选择 aurora workspace 子命令" }
      );
      if (!pick) return;
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["workspace", pick], "Aurora 工作区", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // 依赖管理:aurora deps tree|outdated
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.deps", async () => {
      const pick = await vscode.window.showQuickPick(
        ["tree", "outdated"],
        { placeHolder: "选择 aurora deps 子命令" }
      );
      if (!pick) return;
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["deps", pick], "Aurora 依赖", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // 运行 GUI 应用:aurora ui run <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.ui", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["ui", "run", ed.document.fileName], "Aurora GUI", path.dirname(ed.document.fileName));
    })
  );

  // 跨平台打包:aurora package macos|windows|linux|web
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.package", async () => {
      const pick = await vscode.window.showQuickPick(
        ["macos", "windows", "linux", "web"],
        { placeHolder: "选择目标平台进行打包" }
      );
      if (!pick) return;
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["package", pick], "Aurora 打包", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // 安装 Jupyter 内核:aurora kernel install
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.kernel", async () => {
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["kernel", "install"], "Aurora Jupyter 内核", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // 启动推理服务:aurora serve <model.aur>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.serve", async () => {
      const modelPath = await vscode.window.showInputBox({
        prompt: "输入模型文件路径 (model.aur)",
        placeHolder: "/path/to/model.aur",
      });
      if (!modelPath) return;
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      termCli(["serve", modelPath], "Aurora 推理服务", folder ? folder.uri.fsPath : auroraDir());
    })
  );

  // 语言互操作:aurora interop <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.interop", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["interop", ed.document.fileName], "Aurora 互操作", path.dirname(ed.document.fileName));
    })
  );

  // 编译 WebAssembly:aurora wasm <file>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.wasm", async () => {
      const ed = await activeAuroraFile();
      if (!ed) return;
      termCli(["wasm", ed.document.fileName], "Aurora WASM", path.dirname(ed.document.fileName));
    })
  );

  // ── v3.2.0 新命令:全栈开发工具链 ──────────────────────
  function workspaceDir() {
    const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
    return folder ? folder.uri.fsPath : auroraDir();
  }

  // 创建项目:aurora new <type> [name]
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.new", async () => {
      const pick = await vscode.window.showQuickPick(
        ["fullstack", "cli", "tui", "microservice", "webapp"],
        { placeHolder: "选择 aurora new 项目类型" }
      );
      if (!pick) return;
      const name = await vscode.window.showInputBox({
        prompt: "输入项目名称 (可选)",
        placeHolder: "my-app",
      });
      const args = ["new", pick];
      if (name) args.push(name);
      termCli(args, "Aurora 创建项目", workspaceDir());
    })
  );

  // 代码生成:aurora generate <kind> <name>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.generate", async () => {
      const pick = await vscode.window.showQuickPick(
        ["controller", "model", "component", "service"],
        { placeHolder: "选择 aurora generate 生成类型" }
      );
      if (!pick) return;
      const name = await vscode.window.showInputBox({
        prompt: "输入要生成的名称",
        placeHolder: "User",
      });
      if (!name) return;
      termCli(["generate", pick, name], "Aurora 代码生成", workspaceDir());
    })
  );

  // 数据库管理:aurora db <sub>
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.db", async () => {
      const pick = await vscode.window.showQuickPick(
        ["migrate", "rollback", "seed"],
        { placeHolder: "选择 aurora db 子命令" }
      );
      if (!pick) return;
      termCli(["db", pick], "Aurora 数据库", workspaceDir());
    })
  );

  // 开发模式:aurora dev
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.dev", async () => {
      termCli(["dev"], "Aurora 开发模式", workspaceDir());
    })
  );

  // 部署:aurora deploy
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.deploy", async () => {
      termCli(["deploy"], "Aurora 部署", workspaceDir());
    })
  );

  // Web 应用脚手架:aurora webapp [name]
  context.subscriptions.push(
    vscode.commands.registerCommand("aurora.webapp", async () => {
      const name = await vscode.window.showInputBox({
        prompt: "输入 Web 应用名称 (可选)",
        placeHolder: "my-webapp",
      });
      const args = ["webapp"];
      if (name) args.push(name);
      termCli(args, "Aurora Web 脚手架", workspaceDir());
    })
  );

  // 关闭文档时清除诊断
  context.subscriptions.push(
    vscode.workspace.onDidCloseTextDocument((doc) => diagnostics.delete(doc.uri))
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
