/* Aurora IDE —— VSCode 风格纯编程 IDE 前端逻辑 */
"use strict";

const $ = (sel) => document.querySelector(sel);

// ───────── 状态 ─────────
const state = {
  tree: [],
  expanded: new Set(),
  tabs: [],            // {id, title, path, code, savedCode, dirty}
  activeId: null,
  panel: "output",
  errors: [],          // [{line, col, kind, message}]
  running: false,
};

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ───────── 语法高亮 ─────────
const KEYWORDS = new Set([
  "fn", "let", "var", "const", "if", "elif", "else", "for", "while", "return",
  "type", "enum", "impl", "match", "trait", "true", "false", "nil", "in", "break",
  "continue", "import", "from", "as", "spawn", "chan", "select", "default",
  "try", "catch", "finally", "panic", "self", "std", "and", "or", "not", "loop",
  "pub", "mut", "defer", "yield",
]);
const BUILTINS = new Set([
  "println", "print", "read_int", "read_line", "read_float", "input", "range",
  "len", "str", "int", "float", "bool", "type", "assert", "sleep", "abs", "min",
  "max", "push", "pop", "map", "filter", "reduce", "contains", "sort", "keys",
  "clone", "join", "split", "upper", "lower", "trim", "exists",
  "serve", "static", "wait", "configure", "chat", "messages", "agent",
  "list_dir", "mkdir", "is_dir", "files", "link", "json_script",
]);

function highlight(src) {
  let html = "", i = 0;
  const n = src.length;
  while (i < n) {
    const ch = src[i];
    if ((ch === "r" || ch === "R") && (src[i + 1] === '"' || src[i + 1] === "'")) {
      // 原始字符串 r'...' / r"..."(不插值)
      const q = src[i + 1];
      let j = i + 2;
      while (j < n && src[j] !== q) j++;
      html += '<span class="tok-str">' + esc(src.slice(i, Math.min(j + 1, n))) + "</span>";
      i = Math.min(j + 1, n);
    } else if (ch === '"' || ch === "'") {
      let j = i + 1;
      while (j < n) {
        if (src[j] === "\\") { j += 2; continue; }
        if (src[j] === ch) break;
        j++;
      }
      html += '<span class="tok-str">' + esc(src.slice(i, Math.min(j + 1, n))) + "</span>";
      i = Math.min(j + 1, n);
    } else if (ch === "/" && src[i + 1] === "/") {
      let j = src.indexOf("\n", i); if (j < 0) j = n;
      html += '<span class="tok-com">' + esc(src.slice(i, j)) + "</span>"; i = j;
    } else if (ch === "#") {
      let j = src.indexOf("\n", i); if (j < 0) j = n;
      html += '<span class="tok-com">' + esc(src.slice(i, j)) + "</span>"; i = j;
    } else if (/[A-Za-z_]/.test(ch)) {
      let j = i;
      while (j < n && /[A-Za-z0-9_]/.test(src[j])) j++;
      const w = src.slice(i, j);
      html += '<span class="' + (KEYWORDS.has(w) ? "tok-kw" : BUILTINS.has(w) ? "tok-builtin" : "tok-id") + '">' + esc(w) + "</span>";
      i = j;
    } else if (/[0-9]/.test(ch)) {
      let j = i;
      while (j < n && /[0-9.a-zA-Z_]/.test(src[j])) j++;
      html += '<span class="tok-num">' + esc(src.slice(i, j)) + "</span>"; i = j;
    } else {
      html += esc(ch); i++;
    }
  }
  return html;
}

// ───────── 工具 ─────────
async function api(method, path, body) {
  const opt = { method, headers: {} };
  if (body !== undefined) {
    opt.headers["Content-Type"] = "application/json";
    opt.body = JSON.stringify(body);
  }
  const r = await fetch(path, opt);
  return r.json();
}

function activeTab() {
  return state.tabs.find((t) => t.id === state.activeId) || null;
}
function tabTitle(t) {
  return t.title + (t.dirty ? " •" : "");
}
function setButtons() {
  const has = !!activeTab();
  $("#btn-save").disabled = !has;
  $("#btn-run").disabled = !has || state.running;
  $("#btn-check").disabled = !has;
}

// ───────── 文件树 ─────────
async function loadTree() {
  const d = await api("GET", "/api/files");
  state.tree = d.tree || [];
  renderTree();
}

function renderTree() {
  const root = $("#file-tree");
  root.innerHTML = "";
  if (!state.tree.length) {
    root.innerHTML = '<div class="dim" style="padding:10px 14px">工作区为空</div>';
    return;
  }
  const frag = document.createDocumentFragment();
  for (const node of state.tree) frag.appendChild(treeItem(node, 0));
  root.appendChild(frag);
}

function treeItem(node, depth) {
  const div = document.createElement("div");
  div.className = "tree-item" + (node.type === "file" ? " file ext-" + (node.ext || "").slice(1) : " dir");
  div.style.paddingLeft = (10 + depth * 14) + "px";
  if (node.type === "dir") {
    const open = state.expanded.has(node.path);
    div.innerHTML = '<span class="caret' + (open ? " open" : "") + '">▶</span><span class="fname">' + esc(node.name) + "</span>";
    div.addEventListener("click", () => {
      open ? state.expanded.delete(node.path) : state.expanded.add(node.path);
      renderTree();
    });
    if (open && node.children) {
      const wrap = document.createElement("div");
      wrap.className = "tree-children open";
      for (const c of node.children) wrap.appendChild(treeItem(c, depth + 1));
      div.appendChild(wrap);
    }
  } else {
    div.innerHTML = '<span class="caret"></span><span class="fname">' + esc(node.name) + "</span>";
    div.addEventListener("click", () => openFile(node.path));
    if (activeTab() && activeTab().path === node.path) div.classList.add("active");
  }
  return div;
}

function expandTo(path) {
  const parts = path.split("/");
  let acc = "";
  for (let i = 0; i < parts.length - 1; i++) {
    acc = acc ? acc + "/" + parts[i] : parts[i];
    state.expanded.add(acc);
  }
}

// ───────── 标签管理 ─────────
function renderTabs() {
  const bar = $("#tabs");
  bar.innerHTML = "";
  for (const t of state.tabs) {
    const el = document.createElement("div");
    el.className = "tab" + (t.id === state.activeId ? " active" : "") + (t.dirty ? " dirty" : "");
    el.innerHTML = '<span class="t-dirty"></span><span class="t-name">' + esc(t.title) + '</span><span class="t-close">×</span>';
    el.addEventListener("click", (e) => {
      if (e.target.classList.contains("t-close")) { closeTab(t.id); return; }
      switchTab(t.id);
    });
    bar.appendChild(el);
  }
  setButtons();
}

async function openFile(path, title) {
  const existing = state.tabs.find((t) => t.path === path);
  if (existing) { switchTab(existing.id); return; }
  const d = await api("GET", "/api/file?path=" + encodeURIComponent(path));
  if (d.error) { appendOutput("✗ " + (d.error || "读取失败"), "err-line"); return; }
  const tab = {
    id: "f_" + Date.now(),
    title: title || d.name || path.split("/").pop(),
    path: path,
    code: d.content,
    savedCode: d.content,
    dirty: false,
    kind: "file",
  };
  state.tabs.push(tab);
  state.activeId = tab.id;
  expandTo(path);
  renderTabs();
  renderTree();
  mountEditor();
}

function switchTab(id) {
  saveCurrentEditor();
  state.activeId = id;
  renderTabs();
  renderTree();
  mountEditor();
}

function closeTab(id) {
  const i = state.tabs.findIndex((t) => t.id === id);
  if (i < 0) return;
  const [t] = state.tabs.splice(i, 1);
  if (state.activeId === id) {
    state.activeId = state.tabs.length ? state.tabs[Math.max(0, i - 1)].id : null;
  }
  if (!state.tabs.length) {
    $("#editor-wrap").classList.add("hidden");
    $("#editor-empty").classList.remove("hidden");
  }
  renderTabs();
  renderTree();
  if (activeTab()) mountEditor();
}

function newTab(title, code) {
  const tab = {
    id: "n_" + Date.now(),
    title: title,
    path: null,
    code: code || "",
    savedCode: code || "",
    dirty: !!code,
    kind: "scratch",
  };
  state.tabs.push(tab);
  state.activeId = tab.id;
  renderTabs();
  mountEditor();
}

// ───────── 编辑器 ─────────
const codeTA = $("#code");
const codeHL = $("#code-hl");
const gutter = $("#gutter");

function editorSync() {
  const tab = activeTab();
  if (!tab) return;
  codeHL.innerHTML = highlight(tab.code) + "\n";
  const lines = tab.code.split("\n").length;
  const errLines = new Set(state.errors.filter((e) => e.line).map((e) => e.line));
  let g = "";
  for (let i = 1; i <= lines; i++) {
    g += '<span' + (errLines.has(i) ? ' class="err-line"' : "") + ">" + i + "</span>";
  }
  gutter.innerHTML = g;
}

function saveCurrentEditor() {
  const tab = activeTab();
  if (!tab) return;
  tab.code = codeTA.value;
}

function mountEditor() {
  const tab = activeTab();
  if (!tab) { return; }
  $("#editor-empty").classList.add("hidden");
  $("#editor-wrap").classList.remove("hidden");
  codeTA.value = tab.code;
  editorSync();
  codeTA.focus();
  updateCursor();
}

codeTA.addEventListener("input", () => {
  const tab = activeTab();
  if (!tab) return;
  tab.code = codeTA.value;
  if (tab.savedCode !== tab.code) {
    if (!tab.dirty) { tab.dirty = true; renderTabs(); }
  }
  editorSync();
});
codeTA.addEventListener("scroll", () => {
  codeHL.scrollTop = codeTA.scrollTop;
  codeHL.scrollLeft = codeTA.scrollLeft;
  gutter.scrollTop = codeTA.scrollTop;
});
codeTA.addEventListener("select", updateCursor);
codeTA.addEventListener("click", updateCursor);
codeTA.addEventListener("keyup", updateCursor);
codeTA.addEventListener("keydown", (e) => {
  if (e.key === "Tab") {
    e.preventDefault();
    const s = codeTA.selectionStart, t = codeTA.selectionEnd;
    const tab = activeTab();
    tab.code = tab.code.slice(0, s) + "    " + tab.code.slice(t);
    codeTA.value = tab.code;
    codeTA.selectionStart = codeTA.selectionEnd = s + 4;
    editorSync();
  }
});

function updateCursor() {
  const pos = codeTA.selectionStart;
  const upTo = codeTA.value.slice(0, pos);
  const lines = upTo.split("\n");
  $("#st-cursor").textContent = "Ln " + lines.length + ", Col " + (lines[lines.length - 1].length + 1);
}

// ───────── 输出 / 问题面板 ─────────
function showPanel(name) {
  state.panel = name;
  document.querySelectorAll(".panel-tab").forEach((b) => b.classList.toggle("active", b.dataset.panel === name));
  document.querySelectorAll(".panel-content").forEach((p) => p.classList.remove("active"));
  const map = { output: "#panel-output", problems: "#panel-problems", input: "#panel-input" };
  $(map[name]).classList.add("active");
}

function appendOutput(text, cls) {
  showPanel("output");
  const out = $("#panel-output");
  if (out.querySelector(".dim")) out.innerHTML = "";
  const d = document.createElement("div");
  if (cls) d.className = cls;
  d.textContent = text;
  out.appendChild(d);
  out.scrollTop = out.scrollHeight;
}

function parseLoc(msg) {
  const m = /L(\d+):C(\d+)/.exec(msg || "");
  return m ? { line: +m[1], col: +m[2] } : null;
}

function setProblems(errors) {
  state.errors = errors || [];
  const list = $("#panel-problems");
  list.innerHTML = "";
  const count = $("#prob-count");
  if (!state.errors.length) {
    count.classList.add("hidden");
    list.innerHTML = '<div class="dim" style="padding:8px 14px">未发现问题</div>';
  } else {
    count.textContent = state.errors.length;
    count.classList.remove("hidden");
    for (const e of state.errors) {
      const loc = parseLoc(e.message);
      const it = document.createElement("div");
      it.className = "problem-item err";
      const kind = e.kind ? "[" + e.kind + "]" : "";
      if (loc) {
        it.innerHTML = '<span class="p-loc">L' + loc.line + ":" + loc.col + "</span><span class=\"p-kind\">" + esc(kind) + "</span><span class=\"p-msg\">" + esc(e.message) + "</span>";
        it.addEventListener("click", () => gotoLine(loc.line));
      } else {
        it.innerHTML = '<span class="p-kind">' + esc(kind) + "</span><span class=\"p-msg\">" + esc(e.message) + "</span>";
      }
      list.appendChild(it);
    }
  }
  $("#st-errors").textContent = state.errors.length ? state.errors.length + " 错误" : "0 错误";
  editorSync();
}

function gotoLine(line) {
  if (!activeTab()) return;
  const lines = codeTA.value.split("\n");
  let pos = 0;
  for (let i = 0; i < line - 1 && i < lines.length; i++) pos += lines[i].length + 1;
  codeTA.focus();
  codeTA.setSelectionRange(pos, pos);
  updateCursor();
}

// ───────── 运行 / 检查 / 保存 ─────────
async function runCode() {
  const tab = activeTab();
  if (!tab || state.running) return;
  state.running = true; setButtons();
  showPanel("output");
  const out = $("#panel-output");
  out.innerHTML = '<div class="time">▶ 运行 ' + esc(tab.title) + " …</div>";
  const t0 = performance.now();
  const res = await api("POST", "/api/run", { code: tab.code, stdin: $("#stdin").value });
  const dt = Math.round(performance.now() - t0);
  state.running = false; setButtons();
  if (res.errors && res.errors.length) {
    setProblems(res.errors);
    appendOutput("✗ 运行出错(" + dt + " ms)", "err-line");
  } else {
    setProblems([]);
    out.innerHTML = "";
    if (res.output) appendOutput(res.output);
    else appendOutput("(无输出)");
    appendOutput("— 运行完成,耗时 " + dt + " ms", "time");
  }
}

async function runCheck() {
  const tab = activeTab();
  if (!tab) return;
  const res = await api("POST", "/api/check", { code: tab.code });
  if (res.errors && res.errors.length) {
    setProblems(res.errors);
  } else {
    setProblems([]);
    $("#panel-problems").innerHTML = '<div class="ok-line" style="padding:8px 14px">✓ 类型检查与所有权检查全部通过</div>';
  }
  showPanel("problems");
}

async function saveFile() {
  const tab = activeTab();
  if (!tab) return;
  if (tab.kind === "scratch" || !tab.path) {
    promptNewFile();
    return;
  }
  const res = await api("POST", "/api/file/save", { path: tab.path, content: tab.code });
  if (res.error) { appendOutput("✗ 保存失败: " + res.error, "err-line"); return; }
  tab.savedCode = tab.code;
  tab.dirty = false;
  renderTabs();
  appendOutput("✓ 已保存 " + tab.title, "ok-line");
}

// ───────── 新建文件 ─────────
function promptNewFile() {
  const name = $("#newfile-name");
  name.value = "";
  $("#newfile").classList.remove("hidden");
  setTimeout(() => name.focus(), 50);
}

async function doNewFile() {
  const name = $("#newfile-name").value.trim();
  if (!name) return;
  if (!/^[A-Za-z0-9_\-\u4e00-\u9fa5]+(\.[A-Za-z0-9]+)?$/.test(name)) {
    appendOutput("✗ 文件名不合法(避免使用 / 等特殊字符)", "err-line");
    return;
  }
  const res = await api("POST", "/api/file/new", { path: name });
  if (res.error) { appendOutput("✗ 创建失败: " + res.error, "err-line"); return; }
  $("#newfile").classList.add("hidden");
  await loadTree();
  openFile(name);
}

// ───────── 快捷键 ─────────
document.addEventListener("keydown", (e) => {
  const mod = e.metaKey || e.ctrlKey;
  if (!mod) return;
  const k = e.key.toLowerCase();
  if (k === "s") { e.preventDefault(); saveFile(); }
  else if (k === "r") { e.preventDefault(); runCode(); }
  else if (k === "k") { e.preventDefault(); runCheck(); }
  else if (k === "n") { e.preventDefault(); promptNewFile(); }
  else if (k === "w") { e.preventDefault(); if (activeTab()) closeTab(state.activeId); }
  else if (k === "b") { e.preventDefault(); $("#sidebar").classList.toggle("hidden"); }
});

// ───────── 事件绑定 ─────────
$("#btn-run").addEventListener("click", runCode);
$("#btn-check").addEventListener("click", runCheck);
$("#btn-save").addEventListener("click", saveFile);
$("#btn-new-file").addEventListener("click", promptNewFile);
$("#btn-refresh").addEventListener("click", loadTree);
$("#btn-collapse-dirs").addEventListener("click", () => {
  state.expanded.clear();
  renderTree();
});
$("#panel-collapse").addEventListener("click", () => $("#panel").classList.toggle("collapsed"));
document.querySelectorAll(".panel-tab").forEach((b) =>
  b.addEventListener("click", () => showPanel(b.dataset.panel)));
$("#act-settings").addEventListener("click", () => $("#about").classList.remove("hidden"));
$("#about-close").addEventListener("click", () => $("#about").classList.add("hidden"));
$("#newfile-ok").addEventListener("click", doNewFile);
$("#newfile-cancel").addEventListener("click", () => $("#newfile").classList.add("hidden"));
$("#newfile-name").addEventListener("keydown", (e) => { if (e.key === "Enter") doNewFile(); if (e.key === "Escape") $("#newfile").classList.add("hidden"); });

// ───────── 启动 ─────────
async function init() {
  try {
    await loadTree();
    const h = await api("GET", "/api/health");
    if (!h.ok) $("#st-server").textContent = "○ 服务异常";
  } catch (e) {
    $("#st-server").textContent = "○ 无法连接";
  }
  // 首次打开:自动展开根目录下的一级目录
  for (const n of state.tree) if (n.type === "dir") state.expanded.add(n.path);
  renderTree();
  // 打开欢迎示例(新建临时标签,不落盘)
  newTab("welcome.aur", '// Aurora IDE —— 欢迎\n// ⌘R 运行当前文件,⌘S 保存,⌘K 静态检查\n\nfn fib(n: int) -> int {\n    if n < 2 { return n }\n    return fib(n - 1) + fib(n - 2)\n}\n\nfor i in range(10) {\n    println("fib({i}) = {fib(i)}")\n}');
}
init();
