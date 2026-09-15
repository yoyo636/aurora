"""Aurora v3.1.0 — 重构引擎（RefactorEngine）

基于 ProjectIndex 执行跨文件重构操作。所有操作只返回编辑（RefactorResult），
不直接写盘，由调用方（LSP codeAction / CLI）决定应用。

支持操作：
    - rename_symbol          跨文件重命名，更新所有引用，冲突检测
    - extract_function       把选中文本提取为新函数，自动推断入参/返回值
    - extract_variable      把表达式提取为变量
    - auto_import            为未解析符号自动添加 import
    - quick_fix              依据诊断消息给出修复建议
    - generate_constructor   根据类字段生成构造函数
"""

import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    from .project_index import ProjectIndex, SYM_FUNCTION, SYM_VARIABLE
except ImportError:  # pragma: no cover
    from project_index import ProjectIndex, SYM_FUNCTION, SYM_VARIABLE  # type: ignore


# ─────────────────────────────────────────────────────────────
# 结果数据结构
# ─────────────────────────────────────────────────────────────

@dataclass
class TextEdit:
    """一个文本编辑。"""
    file: str
    start_line: int          # 1-based
    start_col: int           # 1-based
    end_line: int
    end_col: int
    new_text: str
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "range": {
                "start": {"line": self.start_line - 1,
                          "character": self.start_col - 1},
                "end": {"line": self.end_line - 1,
                        "character": self.end_col - 1},
            },
            "newText": self.new_text,
            "description": self.description,
        }


@dataclass
class RefactorResult:
    """一次重构操作的全部编辑。"""
    title: str = ""
    success: bool = True
    message: str = ""
    edits: List[TextEdit] = field(default_factory=list)
    # file -> list[TextEdit]，便于按文件分组
    changed_files: Dict[str, List[TextEdit]] = field(default_factory=dict)

    def add_edit(self, edit: TextEdit):
        self.edits.append(edit)
        self.changed_files.setdefault(edit.file, []).append(edit)

    def files(self) -> List[str]:
        return sorted(self.changed_files.keys())

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "success": self.success,
            "message": self.message,
            "changed_files": self.files(),
            "edits": [e.to_dict() for e in self.edits],
        }


# 标识符正则（用于重命名 / 表达式分析）
_IDENT_RE = re.compile(r'[A-Za-z_]\w*')
_KEYWORDS = {
    "let", "mut", "const", "fn", "if", "elif", "else", "while", "for", "in",
    "return", "break", "continue", "match", "try", "catch", "panic",
    "import", "struct", "enum", "true", "false", "nil",
}


class RefactorError(Exception):
    """重构无法执行（冲突 / 语义错误等）。"""


# ─────────────────────────────────────────────────────────────
# 重构引擎
# ─────────────────────────────────────────────────────────────

class RefactorEngine:
    """基于 ProjectIndex 的重构引擎。"""

    def __init__(self, index: Optional[ProjectIndex] = None):
        self.index = index

    # ── 工具：读取文件 ─────────────────────────────

    @staticmethod
    def _read(path: str) -> List[str]:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()

    # ── 1. 重命名 ─────────────────────────────────

    def rename_symbol(self, old_name: str, new_name: str,
                      file: str, line: int) -> RefactorResult:
        """跨文件重命名符号。

        返回所有需修改的位置；不直接写文件。
        冲突检测：new_name 已存在于同一作用域/项目时失败。
        """
        result = RefactorResult(title=f"重命名 {old_name} → {new_name}")

        if not self._is_valid_ident(new_name):
            result.success = False
            result.message = f"'{new_name}' 不是合法标识符"
            return result

        # 冲突检测：新名字已存在定义
        if self.index is not None:
            existing = self.index.find_definition(new_name)
            if existing is not None:
                result.success = False
                result.message = (
                    f"冲突：'{new_name}' 已定义于 "
                    f"{existing['file']}:{existing['line']}")
                return result
            refs = self.index.find_references(old_name)
        else:
            refs = []

        if not refs:
            # 退化：只在当前文件做文本替换
            return self._rename_in_single_file(old_name, new_name, file)

        # 按文件分组生成编辑
        by_file: Dict[str, List[dict]] = {}
        for r in refs:
            by_file.setdefault(r["file"], []).append(r)

        # 词边界替换：lexer 上报的 column 是标识符结束位置，不同 AST 节点
        # （FnDef / Identifier / LetStmt）语义不一致，因此以行号为准，
        # 用正则在该行上做整词替换，列号仅作参考。
        word_re = re.compile(r'(?<![A-Za-z0-9_])' + re.escape(old_name)
                             + r'(?![A-Za-z0-9_])')

        for fpath, items in by_file.items():
            try:
                lines = self._read(fpath)
            except OSError:
                continue
            # 按行号去重（同一行可能有多处引用，一并替换）
            line_nos = sorted({r["line"] for r in items if 1 <= r["line"] <= len(lines)},
                              reverse=True)
            for ln in line_nos:
                text = lines[ln - 1]
                new_text, count = word_re.subn(new_name, text)
                if count == 0:
                    continue
                # 记录每个被替换片段的位置（用于编辑描述）
                col = 1
                last_end = 0
                for m in word_re.finditer(text):
                    start_c = m.start() + 1
                    end_c = m.end() + 1
                    result.add_edit(TextEdit(
                        file=fpath, start_line=ln, start_col=start_c,
                        end_line=ln, end_col=end_c,
                        new_text=m.group(0),
                        description=f"{old_name} → {new_name}"))
                    last_end = end_c
                lines[ln - 1] = new_text

        result.message = f"已在 {len(result.files())} 个文件中替换 " \
                         f"{len(result.edits)} 处引用"
        return result

    def _rename_in_single_file(self, old_name: str, new_name: str,
                               file: str) -> RefactorResult:
        result = RefactorResult(title=f"重命名 {old_name} → {new_name}")
        try:
            lines = self._read(file)
        except OSError as e:
            result.success = False
            result.message = str(e)
            return result
        for i, text in enumerate(lines, start=1):
            for m in _IDENT_RE.finditer(text):
                if m.group(0) != old_name:
                    continue
                start, end = m.span()
                new_text = text[:start] + new_name + text[end:]
                result.add_edit(TextEdit(
                    file=file, start_line=i, start_col=start + 1,
                    end_line=i, end_col=end, new_text=new_text,
                    description=f"{old_name} → {new_name}"))
                text = new_text
                lines[i - 1] = text
        result.message = f"已在 {file} 中替换 {len(result.edits)} 处"
        return result

    @staticmethod
    def _is_valid_ident(name: str) -> bool:
        if not name or not (name[0].isalpha() or name[0] == '_'):
            return False
        if name in _KEYWORDS:
            return False
        return all(c.isalnum() or c == '_' for c in name)

    # ── 2. 提取函数 ─────────────────────────────

    def extract_function(self, file: str, start_line: int,
                         end_line: int, func_name: str) -> RefactorResult:
        """把 start_line..end_line（1-based，含）选中代码提取为新函数。"""
        result = RefactorResult(title=f"提取函数 {func_name}")
        if not self._is_valid_ident(func_name):
            result.success = False
            result.message = f"'{func_name}' 不是合法函数名"
            return result
        try:
            lines = self._read(file)
        except OSError as e:
            result.success = False
            result.message = str(e)
            return result

        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            result.success = False
            result.message = "行范围非法"
            return result

        selected = lines[start_line - 1:end_line]
        # 分析选中块内用到的标识符：入参 = 选中块外定义、块内首次使用的变量
        used_names = self._collect_used_names(selected)
        # 粗略：在选中块上方查找这些名字是否已定义
        preceding = "\n".join(lines[:start_line - 1])
        inputs = sorted(
            n for n in used_names
            if re.search(rf'\b(?:let|var|const)\s+{re.escape(n)}\b',
                         preceding)
            or re.search(rf'\b{n}\s*[:=]', preceding)
        )
        # 返回值：若选中块最后一条是表达式，或有 return，则带返回值
        has_return = any("return" in ln for ln in selected)
        body_indent = self._min_indent(selected)

        params = ", ".join(inputs)
        # 生成函数定义（插入到当前块上方）
        if has_return:
            fn_def = [f"fn {func_name}({params}) {{"]
            body = ["    " + s[body_indent:] if len(s) > body_indent else s
                    for s in selected]
            fn_def.extend(body)
            fn_def.append("}")
            call_line = f"let __result_{func_name} = {func_name}({', '.join(inputs)})"
        else:
            fn_def = [f"fn {func_name}({params}) {{"]
            body = ["    " + s[body_indent:] if len(s) > body_indent else s
                    for s in selected]
            fn_def.extend(body)
            fn_def.append("}")
            call_line = f"{func_name}({', '.join(inputs)})"

        # 编辑 1：把选中行替换为调用
        result.add_edit(TextEdit(
            file=file, start_line=start_line, start_col=1,
            end_line=end_line, end_col=len(lines[end_line - 1]) + 1,
            new_text=call_line,
            description="替换为函数调用"))
        # 编辑 2：在 start_line 前插入函数定义
        insertion = "\n".join(fn_def) + "\n"
        result.add_edit(TextEdit(
            file=file, start_line=start_line, start_col=1,
            end_line=start_line, end_col=1,
            new_text=insertion,
            description=f"生成函数定义 fn {func_name}"))

        result.message = (
            f"已生成 fn {func_name}({params})，"
            f"入参 {len(inputs)} 个，返回值={'有' if has_return else '无'}")
        return result

    @staticmethod
    def _collect_used_names(block_lines: List[str]) -> List[str]:
        names = set()
        for ln in block_lines:
            for m in _IDENT_RE.finditer(ln):
                tok = m.group(0)
                if tok in _KEYWORDS or tok[0].isdigit():
                    continue
                names.add(tok)
        # 排除赋值目标自身（粗略：块内 let 定义的不算外部输入）
        local_defs = set()
        for ln in block_lines:
            m = re.match(r'\s*(?:let|var|const)\s+([A-Za-z_]\w*)', ln)
            if m:
                local_defs.add(m.group(1))
        return sorted(n for n in names if n not in local_defs)

    @staticmethod
    def _min_indent(lines: List[str]) -> int:
        indents = [len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()]
        return min(indents) if indents else 0

    # ── 3. 提取变量 ───────────────────────────────

    def extract_variable(self, file: str, line: int, expr: str,
                         var_name: str) -> RefactorResult:
        """把 line 行上的 expr 提取为 let var_name = expr。"""
        result = RefactorResult(title=f"提取变量 {var_name}")
        if not self._is_valid_ident(var_name):
            result.success = False
            result.message = f"'{var_name}' 不是合法变量名"
            return result
        try:
            lines = self._read(file)
        except OSError as e:
            result.success = False
            result.message = str(e)
            return result
        if line < 1 or line > len(lines):
            result.success = False
            result.message = "行号越界"
            return result
        text = lines[line - 1]
        if expr not in text:
            result.success = False
            result.message = f"未在第 {line} 行找到表达式 '{expr}'"
            return result

        new_text = text.replace(expr, var_name, 1)
        indent = text[:len(text) - len(text.lstrip())]
        decl = f"{indent}let {var_name} = {expr}"

        # 编辑 1：替换当前行
        result.add_edit(TextEdit(
            file=file, start_line=line, start_col=1,
            end_line=line, end_col=len(text) + 1,
            new_text=new_text, description=f"{expr} → {var_name}"))
        # 编辑 2：插入声明行
        result.add_edit(TextEdit(
            file=file, start_line=line, start_col=1,
            end_line=line, end_col=1,
            new_text=decl + "\n",
            description=f"let {var_name} = {expr}"))
        result.message = f"已提取 let {var_name} = {expr}"
        return result

    # ── 4. 自动导入 ───────────────────────────────

    def auto_import(self, file: str, symbol_name: str) -> RefactorResult:
        """在 file 顶部添加 import，使 symbol_name 可用。"""
        result = RefactorResult(title=f"自动导入 {symbol_name}")
        module = self._find_module_for(symbol_name)
        if module is None:
            result.success = False
            result.message = f"未找到 '{symbol_name}' 所在模块"
            return result
        try:
            lines = self._read(file)
        except OSError as e:
            result.success = False
            result.message = str(e)
            return result

        import_line = f"import {module}"
        # 找到现有 import 块末尾插入
        insert_at = 0
        for i, ln in enumerate(lines):
            if re.match(r'\s*import\s+', ln):
                insert_at = i + 1
        if insert_at == 0:
            # 没有 import：插到文件首行
            insert_at = 0
        result.add_edit(TextEdit(
            file=file, start_line=insert_at + 1, start_col=1,
            end_line=insert_at + 1, end_col=1,
            new_text=import_line + "\n",
            description=f"添加 {import_line}"))
        result.message = f"已添加 {import_line}"
        return result

    def _find_module_for(self, symbol_name: str) -> Optional[str]:
        if self.index is None:
            return None
        loc = self.index.find_definition(symbol_name)
        if loc is None:
            return None
        f = loc["file"]
        # 从文件路径推导模块名：去掉项目根与后缀
        mod = os.path.relpath(f, self.index.root)
        mod = mod.replace(os.sep, "/")
        if mod.endswith(".aur"):
            mod = mod[:-4]
        if mod.endswith("/index"):
            mod = mod[:-6]
        return mod

    # ── 5. 快速修复 ───────────────────────────────

    def quick_fix(self, file: str, diagnostic: dict) -> List[RefactorResult]:
        """根据诊断信息给出零个或多个修复建议。"""
        out: List[RefactorResult] = []
        message = diagnostic.get("message", "")
        rng = diagnostic.get("range", {})
        start = rng.get("start", {})
        line = start.get("line", 0) + 1   # LSP 0-based → 1-based
        char = start.get("character", 0) + 1

        # 未定义变量 → 尝试导入 / 声明
        # 同时兼容 "未定义 foo" 与 "foo 未定义" / "'foo' is not defined" 等形式
        m = re.search(
            r"(?:未定义|is not defined|undefined)['\"]?\s*([A-Za-z_]\w*)"
            r"|['\"]?([A-Za-z_]\w*)['\"]?\s*(?:未定义|is not defined|undefined)",
            message, re.IGNORECASE)
        if m:
            name = m.group(1) or m.group(2)
            if not name:
                return out
            # 尝试自动导入
            imp = self.auto_import(file, name)
            if imp.success:
                out.append(imp)
            # 声明为变量
            try:
                lines = self._read(file)
                if 1 <= line <= len(lines):
                    result = RefactorResult(title=f"声明变量 {name}")
                    result.add_edit(TextEdit(
                        file=file, start_line=line, start_col=1,
                        end_line=line, end_col=1,
                        new_text=f"let {name} = nil\n",
                        description=f"let {name} = nil"))
                    out.append(result)
            except OSError:
                pass
            return out

        # 未使用变量 → 重命名为 _ 前缀 / 删除
        # 兼容 "未使用的变量: name" / "name is unused" / "未使用 name" 等
        m = re.search(
            r"未使用(?:的变量|参数)?[:\s]+(['\"]?([A-Za-z_]\w*)['\"]?)"
            r"|(['\"]?([A-Za-z_]\w*)['\"]?)\s*(?:is unused|unused)",
            message, re.IGNORECASE)
        if m:
            old = m.group(2) or m.group(4)
            if old:
                result = RefactorResult(title=f"前缀下划线 {old} → _{old}")
                result.add_edit(TextEdit(
                    file=file, start_line=line, start_col=char,
                    end_line=line, end_col=char + len(old),
                    new_text="_" + old,
                    description=f"将 {old} 重命名为 _{old}"))
                out.append(result)
        return out

    # ── 6. 生成构造函数 ───────────────────────────

    def generate_constructor(self, class_name: str, file: str) -> RefactorResult:
        """根据类字段生成 __init__（简化：在文件末尾追加构造函数）。"""
        result = RefactorResult(title=f"为 {class_name} 生成构造函数")
        # 从索引取类字段
        fields: List[Tuple[str, str]] = []
        if self.index is not None:
            for s in self.index.get_file_symbols(file):
                if s.get("kind") == "field":
                    fields.append((s["name"], s.get("type", "")))
        if not fields:
            # 退化：从文件中按 struct 字段语法抓
            try:
                lines = self._read(file)
            except OSError as e:
                result.success = False
                result.message = str(e)
                return result
            in_class = False
            for ln in lines:
                if re.match(rf'\s*(?:pub\s+)?(?:struct|class)\s+{re.escape(class_name)}\b', ln):
                    in_class = True
                    continue
                if in_class:
                    if re.match(r'^\s*\}', ln):
                        break
                    m = re.match(r'\s*([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w\[\]<>,]*)', ln)
                    if m:
                        fields.append((m.group(1), m.group(2)))

        if not fields:
            result.success = False
            result.message = f"未找到 {class_name} 的字段"
            return result

        param_str = ", ".join(f"{n}: {t}" if t else n for n, t in fields)
        body_lines = [f"fn __init__(self, {param_str}) {{"]
        for n, _ in fields:
            body_lines.append(f"    self.{n} = {n}")
        body_lines.append("}")
        new_text = "\n".join(body_lines) + "\n"

        try:
            with open(file, "r", encoding="utf-8") as f:
                n = sum(1 for _ in f)
        except OSError as e:
            result.success = False
            result.message = str(e)
            return result

        result.add_edit(TextEdit(
            file=file, start_line=n + 1, start_col=1,
            end_line=n + 1, end_col=1,
            new_text=new_text,
            description=f"生成 {class_name}.__init__"))
        result.message = f"已生成 __init__，参数 {len(fields)} 个"
        return result


# ─────────────────────────────────────────────────────────────
# CLI 注册（可选）
# ─────────────────────────────────────────────────────────────

def cmd_refactor(args):
    """aurora refactor 命令实现（简化：打印计划的编辑）。"""
    from .project_index import ProjectIndex
    idx = ProjectIndex(root=args.root)
    idx.reindex_all()
    engine = RefactorEngine(index=idx)

    if args.op == "rename":
        r = engine.rename_symbol(args.old, args.new, args.file, args.line or 1)
    elif args.op == "extract-function":
        r = engine.extract_function(args.file, args.start, args.end, args.name)
    elif args.op == "extract-variable":
        r = engine.extract_variable(args.file, args.line, args.expr, args.name)
    else:
        print(f"未知操作 {args.op}")
        return

    print(r.message)
    for fpath, edits in r.changed_files.items():
        print(f"  {fpath}: {len(edits)} 处编辑")


def register_cli(subparsers):
    """把 refactor 子命令注册到全局 argparse。"""
    p = subparsers.add_parser("refactor", help="执行 Aurora 重构操作")
    p.add_argument("--root", default=".")
    sub = p.add_subparsers(dest="op")

    pr = sub.add_parser("rename", help="重命名符号")
    pr.add_argument("old")
    pr.add_argument("new")
    pr.add_argument("--file", required=True)
    pr.add_argument("--line", type=int, default=1)
    pr.set_defaults(func=cmd_refactor)

    pf = sub.add_parser("extract-function", help="提取函数")
    pf.add_argument("--file", required=True)
    pf.add_argument("--start", type=int, required=True)
    pf.add_argument("--end", type=int, required=True)
    pf.add_argument("name")
    pf.set_defaults(func=cmd_refactor)

    pv = sub.add_parser("extract-variable", help="提取变量")
    pv.add_argument("--file", required=True)
    pv.add_argument("--line", type=int, required=True)
    pv.add_argument("--expr", required=True)
    pv.add_argument("name")
    pv.set_defaults(func=cmd_refactor)
