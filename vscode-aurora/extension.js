// Aurora Language —— VSCode 扩展
// 功能:运行 .aur 文件(集成终端)、静态检查(行内诊断)、运行选中代码
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

  // 关闭文档时清除诊断
  context.subscriptions.push(
    vscode.workspace.onDidCloseTextDocument((doc) => diagnostics.delete(doc.uri))
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
