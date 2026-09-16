"""Aurora 递归下降解析器 — 将 Token 流转换为 AST"""

from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS
from .ast_nodes import *


# 关键字 token 类型集合(允许 obj.import 这类关键字成员名)
_KEYWORD_TYPES = set(KEYWORDS.values())


class ParseError(Exception):
    def __init__(self, message: str, token: Token = None):
        loc = f"L{token.line}:C{token.column}" if token else "?"
        super().__init__(f"{loc}: {message}")
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type not in
                       (TokenType.NEWLINE, TokenType.COMMENT, TokenType.INDENT, TokenType.DEDENT)]
        self.pos = 0

    # ── helpers ──────────────────────────────────────────

    def _current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "", 0, 0)

    def _peek(self, offset=0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return Token(TokenType.EOF, "", 0, 0)

    def _advance(self) -> Token:
        tok = self._current()
        self.pos += 1
        return tok

    def _expect(self, tt: TokenType, msg: str = "") -> Token:
        tok = self._current()
        if tok.type != tt:
            raise ParseError(
                msg or f"期望 {tt.name}，得到 {tok.type.name} ({tok.value!r})", tok)
        return self._advance()

    def _match(self, *types: TokenType) -> Optional[Token]:
        if self._current().type in types:
            return self._advance()
        return None

    def _at(self, *types: TokenType) -> bool:
        return self._current().type in types

    # ── program ──────────────────────────────────────────

    def parse(self) -> Program:
        stmts = []
        while not self._at(TokenType.EOF):
            stmt = self._parse_top_level()
            if stmt:
                stmts.append(stmt)
            # 分号作为可选语句分隔符
            while self._match(TokenType.SEMICOLON):
                pass
        return Program(statements=stmts)

    def _parse_top_level(self) -> Optional[Stmt]:
        # @perf(level) 等函数级注解（仅作用于紧随其后的 fn）
        annotations = self._parse_annotations()
        # v3.1.0：#[...] 属性，可多个，附加到紧随其后的定义
        attrs = self._parse_attributes()

        pub = bool(self._match(TokenType.PUB))
        # v3.1.0：async / unsafe 修饰符（仅在紧随 fn 时消费；否则交给语句解析
        # 以支持独立的 unsafe { ... } 块）
        is_async = bool(self._match(TokenType.ASYNC))
        is_unsafe = False
        if not is_async and self._at(TokenType.UNSAFE) and self._peek(1).type == TokenType.FN:
            self._advance()
            is_unsafe = True
        if is_async and self._at(TokenType.UNSAFE) and self._peek(1).type == TokenType.FN:
            self._advance()
            is_unsafe = True

        # extern "C" { ... } 外部函数声明块
        if self._at(TokenType.EXTERN):
            return self._parse_extern_block(attrs=attrs)

        tok = self._current()
        if tok.type == TokenType.FN:
            fn = self._parse_fn_def(is_pub=pub)
            fn.annotations = annotations
            fn.is_async = is_async
            fn.is_unsafe = is_unsafe
            fn.attributes = attrs
            return fn
        if tok.type == TokenType.TYPE:
            td = self._parse_type_def(is_pub=pub)
            td.attributes = attrs
            return td
        if tok.type == TokenType.STRUCT:
            td = self._parse_type_def(is_pub=pub)
            td.attributes = attrs
            return td
        if tok.type == TokenType.ENUM:
            return self._parse_enum_def(is_pub=pub)
        if tok.type == TokenType.TRAIT:
            return self._parse_trait_def(is_pub=pub)
        if tok.type == TokenType.IMPL:
            return self._parse_impl_block()
        if tok.type == TokenType.IMPORT or tok.type == TokenType.FROM:
            return self._parse_import()
        if tok.type == TokenType.TEST:
            return self._parse_test_block()
        if tok.type == TokenType.CONST:
            c = self._parse_const()
            c.is_pub = pub
            c.attributes = attrs
            return c
        # v3.1.0：pub let name = ...（顶层可见性变量）
        if pub and tok.type in (TokenType.LET, TokenType.VAR):
            s = self._parse_let(mutable=(tok.type == TokenType.VAR))
            if isinstance(s, LetStmt):
                s.is_pub = pub
            s.attributes = attrs
            return s

        # pub 后面必须跟 fn/type/enum/trait/const/let
        if pub:
            raise ParseError("'pub' 只能修饰 fn/type/struct/enum/trait/const/let", tok)
        return self._parse_statement()

    def _parse_attributes(self) -> List[Attribute]:
        """解析前导 #[...] 属性列表（v3.1.0），如 #[cfg(target_os = "macos")]"""
        attrs = []
        while self._at(TokenType.POUND):
            self._advance()  # #
            self._expect(TokenType.LBRACKET, "属性语法应为 #[...]")
            name = self._expect(TokenType.IDENTIFIER).value
            args = []
            raw_parts = []
            if self._match(TokenType.LPAREN):
                # 收集括号内原始文本直到匹配的 )
                depth = 1
                while depth and not self._at(TokenType.EOF):
                    t = self._current()
                    if t.type == TokenType.LPAREN:
                        depth += 1
                    elif t.type == TokenType.RPAREN:
                        depth -= 1
                        if depth == 0:
                            self._advance()
                            break
                    raw_parts.append(t.value)
                    self._advance()
                raw = ' '.join(raw_parts).strip()
                # 解析简单的 key = "value" 列表
                args = self._parse_attr_args(raw)
            else:
                raw = ''
            self._expect(TokenType.RBRACKET, "属性 ] 不匹配")
            attrs.append(Attribute(name=name, args=args, raw=raw))
        return attrs

    def _parse_attr_args(self, raw: str) -> List[tuple]:
        """把属性括号内文本切成 (key, value) 对，如 target_os = "macos"。"""
        import re as _re
        pairs = []
        # 按逗号切分（粗粒度：字符串内逗号不常见，cfg 表达式逗号多在顶层）
        for chunk in _re.split(r',(?![^"]*"\s*\))', raw):
            m = _re.match(r'\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"([^"]*)"', chunk)
            if m:
                pairs.append((m.group(1), m.group(2)))
        return pairs

    def _parse_extern_block(self, attrs=None) -> ExternBlock:
        """解析 extern "C" { fn a(...) -> T; fn b(...) -> U; }"""
        self._expect(TokenType.EXTERN)
        abi = "C"
        if self._at(TokenType.STRING):
            abi = self._advance().value
        self._expect(TokenType.LBRACE)
        decls = []
        while not self._at(TokenType.RBRACE):
            # 可选 pub 前缀（extern 块内通常不写，兼容）
            self._match(TokenType.PUB)
            self._expect(TokenType.FN)
            fname = self._expect(TokenType.IDENTIFIER).value
            self._expect(TokenType.LPAREN)
            params = self._parse_params()
            self._expect(TokenType.RPAREN)
            ret_type = None
            if self._match(TokenType.ARROW):
                ret_type = self._parse_type()
            is_variadic = any(p.variadic for p in params)
            decls.append(ExternFn(name=fname, params=params,
                                  return_type=ret_type, is_variadic=is_variadic))
            while self._match(TokenType.SEMICOLON):
                pass
        self._expect(TokenType.RBRACE)
        return ExternBlock(abi=abi, declarations=decls, attributes=attrs or [])

    # ── function definition ─────────────────────────────

    def _parse_annotations(self) -> List[dict]:
        """解析前导函数注解：@perf(level)，可多个"""
        annotations = []
        while self._at(TokenType.AT):
            self._advance()  # @
            if self._match(TokenType.PERF):
                self._expect(TokenType.LPAREN)
                level = self._expect(TokenType.IDENTIFIER).value
                self._expect(TokenType.RPAREN)
                annotations.append({"level": level})
            else:
                # 未知 @注解：保守忽略，避免破坏现有代码
                self._match(TokenType.LPAREN)
                depth = 1
                while depth and not self._at(TokenType.EOF):
                    if self._match(TokenType.LPAREN):
                        depth += 1
                    elif self._match(TokenType.RPAREN):
                        depth -= 1
                    else:
                        self._advance()
        return annotations

    def _parse_fn_def(self, is_pub=False, require_body=True) -> FnDef:
        tok = self._expect(TokenType.FN)
        name = self._expect(TokenType.IDENTIFIER).value
        type_params = self._parse_generic_params()
        self._expect(TokenType.LPAREN)
        params = self._parse_params()
        self._expect(TokenType.RPAREN)

        ret_type = None
        if self._match(TokenType.ARROW):
            ret_type = self._parse_type()

        body = None
        if require_body:
            body = self._parse_block()
        elif self._at(TokenType.LBRACE):
            # trait 方法允许带默认实现
            body = self._parse_block()
        return FnDef(name=name, params=params, return_type=ret_type,
                     body=body, is_pub=is_pub, type_params=type_params,
                     line=tok.line, column=tok.column)

    def _parse_params(self) -> List[Param]:
        params = []
        while not self._at(TokenType.RPAREN):
            variadic = bool(self._match(TokenType.VARIADIC))
            p_name = self._expect(TokenType.IDENTIFIER).value
            p_type = None
            if self._match(TokenType.COLON):
                p_type = self._parse_type()
            default = None
            if self._match(TokenType.ASSIGN):
                default = self._parse_expr()
            params.append(Param(name=p_name, type_annotation=p_type,
                                default_value=default, variadic=variadic))
            if not self._match(TokenType.COMMA):
                break
        return params

    # ── type definition ─────────────────────────────────

    def _parse_type_def(self, is_pub=False) -> TypeDef:
        tok = self._current()
        if tok.type not in (TokenType.TYPE, TokenType.STRUCT):
            raise ParseError(f"期望 type 或 struct，得到 {tok.type.name}", tok)
        self._advance()
        name = self._expect(TokenType.IDENTIFIER).value
        type_params = self._parse_generic_params()
        self._expect(TokenType.LBRACE)
        fields = []
        while not self._at(TokenType.RBRACE):
            f_name = self._expect(TokenType.IDENTIFIER).value
            self._expect(TokenType.COLON)
            f_type = self._parse_type()
            f_default = None
            if self._match(TokenType.ASSIGN):
                f_default = self._parse_expr()
            fields.append((f_name, f_type, f_default))
            self._match(TokenType.COMMA)
        self._expect(TokenType.RBRACE)
        return TypeDef(name=name, fields=fields, is_pub=is_pub, type_params=type_params)

    def _parse_generic_params(self) -> List[str]:
        if not self._match(TokenType.LT):
            return []
        names = []
        while not self._at(TokenType.GT):
            names.append(self._expect(TokenType.IDENTIFIER).value)
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.GT)
        return names

    # ── enum definition ─────────────────────────────────

    def _parse_enum_def(self, is_pub=False) -> EnumDef:
        self._expect(TokenType.ENUM)
        name = self._expect(TokenType.IDENTIFIER).value
        type_params = self._parse_generic_params()
        self._expect(TokenType.LBRACE)
        variants = []
        while not self._at(TokenType.RBRACE):
            v_name = self._expect(TokenType.IDENTIFIER).value
            v_fields = []
            if self._match(TokenType.LPAREN):
                # 元组变体: Circle(f64)
                while not self._at(TokenType.RPAREN):
                    f_name = self._expect(TokenType.IDENTIFIER).value
                    self._expect(TokenType.COLON)
                    f_type = self._parse_type()
                    v_fields.append((f_name, f_type))
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN)
            elif self._match(TokenType.LBRACE):
                # 结构体变体: Point { x: i64, y: i64 }
                while not self._at(TokenType.RBRACE):
                    f_name = self._expect(TokenType.IDENTIFIER).value
                    self._expect(TokenType.COLON)
                    f_type = self._parse_type()
                    v_fields.append((f_name, f_type))
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RBRACE)
            variants.append(EnumVariant(name=v_name, fields=v_fields))
            self._match(TokenType.COMMA)
        self._expect(TokenType.RBRACE)
        return EnumDef(name=name, variants=variants, is_pub=is_pub, type_params=type_params)

    # ── trait definition ────────────────────────────────

    def _parse_trait_def(self, is_pub=False) -> TraitDef:
        tok = self._expect(TokenType.TRAIT)
        name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.LBRACE)
        methods = []
        while not self._at(TokenType.RBRACE):
            methods.append(self._parse_fn_def(require_body=False))
        self._expect(TokenType.RBRACE)
        return TraitDef(name=name, methods=methods, is_pub=is_pub,
                        line=tok.line, column=tok.column)

    # ── impl block ──────────────────────────────────────

    def _parse_impl_block(self) -> ImplBlock:
        tok = self._expect(TokenType.IMPL)
        first = self._expect(TokenType.IDENTIFIER).value
        trait_name = None
        type_name = first

        if self._match(TokenType.FOR):
            trait_name = first
            type_name = self._expect(TokenType.IDENTIFIER).value

        self._expect(TokenType.LBRACE)
        methods = []
        while not self._at(TokenType.RBRACE):
            pub = bool(self._match(TokenType.PUB))
            methods.append(self._parse_fn_def(is_pub=pub))
        self._expect(TokenType.RBRACE)
        return ImplBlock(trait_name=trait_name, type_name=type_name, methods=methods,
                         line=tok.line, column=tok.column)

    # ── import ──────────────────────────────────────────

    def _parse_import(self) -> ImportStmt:
        if self._match(TokenType.FROM):
            path = [self._expect(TokenType.IDENTIFIER).value]
            while self._match(TokenType.DOT):
                path.append(self._expect(TokenType.IDENTIFIER).value)
            self._expect(TokenType.IMPORT)
            names = [self._expect(TokenType.IDENTIFIER).value]
            while self._match(TokenType.COMMA):
                names.append(self._expect(TokenType.IDENTIFIER).value)
            alias = None
            if len(names) == 1 and self._match(TokenType.AS):
                alias = self._expect(TokenType.IDENTIFIER).value
            return ImportStmt(path=path, names=names, alias=alias)
        else:
            self._expect(TokenType.IMPORT)
            path = [self._expect(TokenType.IDENTIFIER).value]
            while self._match(TokenType.DOT):
                path.append(self._expect(TokenType.IDENTIFIER).value)
            alias = None
            if self._match(TokenType.AS):
                alias = self._expect(TokenType.IDENTIFIER).value
            return ImportStmt(path=path, alias=alias)

    # ── test block ──────────────────────────────────────

    def _parse_test_block(self) -> TestBlock:
        self._expect(TokenType.TEST)
        name = self._expect(TokenType.STRING).value
        body = self._parse_block()
        return TestBlock(name=name, body=body)

    # ── const ───────────────────────────────────────────

    def _parse_const(self) -> ConstStmt:
        self._expect(TokenType.CONST)
        name = self._expect(TokenType.IDENTIFIER).value
        type_ann = None
        if self._match(TokenType.COLON):
            type_ann = self._parse_type()
        self._expect(TokenType.ASSIGN)
        init = self._parse_expr()
        return ConstStmt(name=name, type_annotation=type_ann, initializer=init)

    # ── statements ──────────────────────────────────────

    def _parse_statement(self) -> Stmt:
        # 空语句 / 前导分号
        while self._match(TokenType.SEMICOLON):
            pass
        tok = self._current()
        stmt = self._parse_statement_inner()
        # 统一填充源码位置（若内部未设置）
        if stmt is not None and stmt.line == 0:
            stmt.line = tok.line
            stmt.column = tok.column
        return stmt

    def _parse_statement_inner(self) -> Stmt:
        tok = self._current()

        if tok.type == TokenType.LET:
            return self._parse_let(mutable=False)
        if tok.type == TokenType.VAR:
            return self._parse_let(mutable=True)
        if tok.type == TokenType.CONST:
            return self._parse_const()
        if tok.type == TokenType.RETURN:
            return self._parse_return()
        if tok.type == TokenType.IF:
            return self._parse_if_stmt()
        if tok.type == TokenType.FOR:
            return self._parse_for_stmt()
        if tok.type == TokenType.WHILE:
            return self._parse_while_stmt()
        if tok.type == TokenType.MATCH:
            return self._parse_match_stmt()
        if tok.type == TokenType.BREAK:
            self._advance()
            return BreakStmt()
        if tok.type == TokenType.CONTINUE:
            self._advance()
            return ContinueStmt()
        if tok.type == TokenType.SPAWN:
            return self._parse_spawn_stmt()
        if tok.type == TokenType.SELECT:
            return self._parse_select_stmt()
        if tok.type == TokenType.TRY:
            return self._parse_try_stmt()
        if tok.type == TokenType.ASSERT:
            return self._parse_assert()
        if tok.type == TokenType.DEFER:
            return self._parse_defer()
        if tok.type == TokenType.UNSAFE:
            # v3.1.0: unsafe { ... } 块
            self._advance()
            return UnsafeBlock(body=self._parse_block())
        if tok.type == TokenType.YIELD:
            return self._parse_yield()
        if tok.type in (TokenType.TYPE, TokenType.STRUCT):
            return self._parse_type_def()
        if tok.type == TokenType.ENUM:
            return self._parse_enum_def()

        # 赋值或表达式
        return self._parse_assign_or_expr()

    def _parse_let(self, mutable: bool = False) -> Stmt:
        self._advance()  # let / var
        # 可变绑定还可显式写 let mut x
        if self._match(TokenType.MUT):
            mutable = True
        tok = self._current()

        # 模式解构: let (a, b) = expr / let (x, (y, z)) = expr / let [a, b] = expr / let {a, b} = expr
        if tok.type in (TokenType.LPAREN, TokenType.LBRACKET, TokenType.LBRACE):
            pattern = self._parse_pattern()
            # 扁平化收集所有绑定名
            names = []
            self._collect_pattern_names(pattern, names)
            self._expect(TokenType.ASSIGN, "解构绑定需要 = 初始化")
            init = self._parse_expr()
            return DestructureLet(names=names, mutable=mutable,
                                  initializer=init, pattern=pattern)

        name = self._expect(TokenType.IDENTIFIER).value
        type_ann = None
        if self._match(TokenType.COLON):
            type_ann = self._parse_type()
        init = None
        if self._match(TokenType.ASSIGN):
            init = self._parse_expr()
        return LetStmt(name=name, mutable=mutable, type_annotation=type_ann, initializer=init)

    def _collect_pattern_names(self, pattern: Pattern, names: List[str]):
        """递归收集模式中所有绑定名称"""
        if isinstance(pattern, BindPattern):
            names.append(pattern.name)
        elif isinstance(pattern, TuplePattern):
            for p in pattern.elements:
                self._collect_pattern_names(p, names)
        elif isinstance(pattern, ConstructorPattern):
            for p in pattern.fields:
                self._collect_pattern_names(p, names)
        elif isinstance(pattern, StructPattern):
            for fname, sub in pattern.fields:
                if sub:
                    self._collect_pattern_names(sub, names)
                else:
                    names.append(fname)

    def _parse_defer(self) -> DeferStmt:
        self._expect(TokenType.DEFER)
        if self._at(TokenType.LBRACE):
            body = self._parse_block()
            return DeferStmt(body=body)
        expr = self._parse_expr()
        return DeferStmt(expr=expr)

    def _parse_yield(self) -> YieldStmt:
        self._expect(TokenType.YIELD)
        val = None
        if not self._at(TokenType.RBRACE, TokenType.EOF, TokenType.SEMICOLON):
            val = self._parse_expr()
        return YieldStmt(value=val)

    def _parse_return(self) -> ReturnStmt:
        self._expect(TokenType.RETURN)
        val = None
        if not self._at(TokenType.RBRACE, TokenType.EOF, TokenType.SEMICOLON):
            val = self._parse_expr()
        return ReturnStmt(value=val)

    def _parse_if_stmt(self) -> IfStmt:
        self._expect(TokenType.IF)
        cond = self._parse_expr()
        then = self._parse_block()
        elifs = []
        while self._match(TokenType.ELIF):
            ec = self._parse_expr()
            eb = self._parse_block()
            elifs.append((ec, eb))
        else_body = None
        if self._match(TokenType.ELSE):
            else_body = self._parse_block()
        return IfStmt(condition=cond, then_body=then, elif_clauses=elifs, else_body=else_body)

    def _parse_for_stmt(self) -> ForStmt:
        self._expect(TokenType.FOR)
        # 支持 for (a, b) in pairs 元组解构
        if self._at(TokenType.LPAREN):
            self._advance()
            variables = []
            while not self._at(TokenType.RPAREN):
                variables.append(self._expect(TokenType.IDENTIFIER).value)
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RPAREN)
        else:
            variables = [self._expect(TokenType.IDENTIFIER).value]
            while self._match(TokenType.COMMA):
                variables.append(self._expect(TokenType.IDENTIFIER).value)
        # expect 'in' as identifier
        self._expect(TokenType.IDENTIFIER, "期望 'in'")
        iterable = self._parse_expr()
        body = self._parse_block()
        return ForStmt(variables=variables, iterable=iterable, body=body)

    def _parse_while_stmt(self) -> WhileStmt:
        self._expect(TokenType.WHILE)
        cond = self._parse_expr()
        body = self._parse_block()
        return WhileStmt(condition=cond, body=body)

    def _parse_match_stmt(self) -> MatchStmt:
        self._expect(TokenType.MATCH)
        subject = self._parse_expr()
        self._expect(TokenType.LBRACE)
        arms = []
        while not self._at(TokenType.RBRACE):
            pat = self._parse_pattern()
            self._expect(TokenType.FAT_ARROW)
            body = self._parse_expr()
            arms.append(MatchArm(pattern=pat, body=body))
            self._match(TokenType.COMMA)
        self._expect(TokenType.RBRACE)
        return MatchStmt(subject=subject, arms=arms)

    def _parse_spawn_stmt(self) -> SpawnStmt:
        self._expect(TokenType.SPAWN)
        call = self._parse_expr()
        return SpawnStmt(call=call)

    def _parse_select_stmt(self) -> SelectStmt:
        self._expect(TokenType.SELECT)
        self._expect(TokenType.LBRACE)
        arms = []
        while not self._at(TokenType.RBRACE):
            if (self._current().type == TokenType.IDENTIFIER
                    and self._current().value == 'default'):
                self._advance()
                self._expect(TokenType.FAT_ARROW)
                body = self._parse_block()
                arms.append(SelectArm(is_default=True, body=body))
            else:
                name = None
                # 绑定形式：v = <-ch => { ... }
                if (self._current().type == TokenType.IDENTIFIER
                        and self._peek(1).type == TokenType.ASSIGN):
                    name = self._advance().value
                    self._expect(TokenType.ASSIGN)
                ch_expr = self._parse_expr()
                self._expect(TokenType.FAT_ARROW)
                body = self._parse_block()
                arms.append(SelectArm(channel_expr=ch_expr, bind_name=name, body=body))
            self._match(TokenType.COMMA)
        self._expect(TokenType.RBRACE)
        return SelectStmt(arms=arms)

    def _parse_try_stmt(self) -> TryStmt:
        self._expect(TokenType.TRY)
        body = self._parse_block()
        catches = []
        finally_body = None
        while self._match(TokenType.CATCH):
            err_name = self._expect(TokenType.IDENTIFIER).value
            err_type = None
            if self._match(TokenType.COLON):
                err_type = self._parse_type()
            cb = self._parse_block()
            catches.append(CatchClause(name=err_name, error_type=err_type, body=cb))
        if self._match(TokenType.FINALLY):
            finally_body = self._parse_block()
        return TryStmt(body=body, catches=catches, finally_body=finally_body)

    def _parse_assert(self) -> ExprStmt:
        self._expect(TokenType.ASSERT)
        expr = self._parse_expr()
        return ExprStmt(expr=CallExpr(callee=Identifier(name="assert"), args=[expr]))

    def _parse_assign_or_expr(self) -> Stmt:
        expr = self._parse_expr()
        # 元组赋值: a, b = b, a / (a, b) = (1, 2)
        if self._at(TokenType.COMMA):
            targets = [expr]
            while self._match(TokenType.COMMA):
                targets.append(self._parse_expr())
            if self._at(TokenType.ASSIGN, TokenType.PLUS_EQ, TokenType.MINUS_EQ,
                        TokenType.STAR_EQ, TokenType.SLASH_EQ):
                op = self._advance().value
                value = self._parse_expr()
                # 右侧如果是逗号分隔,构造元组
                if self._at(TokenType.COMMA):
                    vals = [value]
                    while self._match(TokenType.COMMA):
                        vals.append(self._parse_expr())
                    value = TupleLiteral(elements=vals)
                return AssignStmt(target=TupleLiteral(elements=targets), value=value, op=op)
            # 非赋值的逗号表达式:构造元组
            return ExprStmt(expr=TupleLiteral(elements=targets))
        # 赋值
        if self._at(TokenType.ASSIGN, TokenType.PLUS_EQ, TokenType.MINUS_EQ,
                    TokenType.STAR_EQ, TokenType.SLASH_EQ):
            op = self._advance().value
            value = self._parse_expr()
            return AssignStmt(target=expr, value=value, op=op)
        return ExprStmt(expr=expr)

    # ── block ───────────────────────────────────────────

    def _parse_block(self) -> Block:
        self._expect(TokenType.LBRACE)
        stmts = []
        while not self._at(TokenType.RBRACE, TokenType.EOF):
            stmts.append(self._parse_statement())
            while self._match(TokenType.SEMICOLON):
                pass
        self._expect(TokenType.RBRACE)
        return Block(statements=stmts)

    # ── pattern ─────────────────────────────────────────

    def _parse_pattern(self) -> Pattern:
        tok = self._current()
        if tok.value == '_':
            self._advance()
            return WildcardPattern()
        # v3.2.0: 字典解构模式 {a, b = 1, c: x}
        if tok.type == TokenType.LBRACE:
            self._advance()
            fields = []
            while not self._at(TokenType.RBRACE):
                fname = self._expect(TokenType.IDENTIFIER).value
                sub = None
                if self._match(TokenType.COLON):
                    sub = self._parse_pattern()
                # v3.2.0: 解构默认值 { name = "default" }
                default = None
                if self._match(TokenType.ASSIGN):
                    default = self._parse_expr()
                if sub is None:
                    sub = BindPattern(name=fname, default=default)
                fields.append((fname, sub))
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RBRACE)
            return StructPattern(name="", fields=fields)
        if tok.type == TokenType.IDENTIFIER:
            name = self._advance().value
            # 构造器模式: Ok(val), Err(msg)
            if self._match(TokenType.LPAREN):
                fields = []
                while not self._at(TokenType.RPAREN):
                    fields.append(self._parse_pattern())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN)
                return ConstructorPattern(name=name, fields=fields)
            # 结构体模式: Point { x, y } / User { name: n, age: a }
            if self._match(TokenType.LBRACE):
                fields = []
                while not self._at(TokenType.RBRACE):
                    fname = self._expect(TokenType.IDENTIFIER).value
                    sub = None
                    if self._match(TokenType.COLON):
                        sub = self._parse_pattern()
                    # v3.2.0: 解构默认值
                    default = None
                    if self._match(TokenType.ASSIGN):
                        default = self._parse_expr()
                    if sub is None:
                        sub = BindPattern(name=fname, default=default)
                    fields.append((fname, sub))
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RBRACE)
                return StructPattern(name=name, fields=fields)
            # v3.2.0: 绑定默认值 let x = 1 in pattern context (a = 1, b)
            default = None
            if self._match(TokenType.ASSIGN):
                default = self._parse_expr()
            return BindPattern(name=name, default=default)
        # 元组模式: (a, b, c)
        if tok.type == TokenType.LPAREN:
            self._advance()
            elems = []
            while not self._at(TokenType.RPAREN):
                elems.append(self._parse_pattern())
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RPAREN)
            return TuplePattern(elements=elems)
        # 数组模式: [a, b, c]
        if tok.type == TokenType.LBRACKET:
            self._advance()
            elems = []
            while not self._at(TokenType.RBRACKET):
                elems.append(self._parse_pattern())
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RBRACKET)
            return TuplePattern(elements=elems)  # 复用 TuplePattern
        # 字面量模式
        lit = self._parse_primary()
        return LiteralPattern(value=lit)

    def _parse_comprehension_clauses(self):
        """解析推导式的 for/if 子句，返回 (generators, conditions)"""
        gens = []
        conds = []
        while self._at(TokenType.FOR):
            self._advance()  # for
            targets = [self._expect(TokenType.IDENTIFIER).value]
            while self._match(TokenType.COMMA):
                targets.append(self._expect(TokenType.IDENTIFIER).value)
            # expect 'in' as identifier
            self._expect(TokenType.IDENTIFIER, "期望 'in'")
            iterable = self._parse_expr()
            for t in targets:
                gens.append(CompFor(target=t, iterable=iterable))
            while self._at(TokenType.IF):
                self._advance()  # if
                conds.append(self._parse_expr())
        return gens, conds

    # ── types ───────────────────────────────────────────

    def _parse_type(self) -> TypeNode:
        """解析类型表达式"""
        # 引用类型 &T / &mut T
        if self._match(TokenType.AMP):
            mutable = bool(self._match(TokenType.MUT))
            inner = self._parse_type()
            return RefType(inner=inner, mutable=mutable)

        # v3.1.0: 原始指针类型 *T / *void（extern 块使用）
        if self._match(TokenType.STAR):
            if self._at(TokenType.IDENTIFIER) and self._current().value == 'void':
                self._advance()
                return RefType(inner=NamedType(name='void'), mutable=True)
            inner = self._parse_type()
            return RefType(inner=inner, mutable=True)

        base = self._parse_type_atom()

        # 可选类型 T?（可链式 T??）
        while self._match(TokenType.QUESTION):
            base = OptionalType(inner=base)

        # 函数类型 (T) -> U  — 已在 _parse_type_atom 中处理
        # 联合类型 T | U
        if self._at(TokenType.PIPE):
            variants = [base]
            while self._match(TokenType.PIPE):
                variants.append(self._parse_type_atom())
            return UnionType(variants=variants)

        return base

    def _parse_type_atom(self) -> TypeNode:
        tok = self._current()

        # 数组类型 [T]
        if tok.type == TokenType.LBRACKET:
            self._advance()
            elem = self._parse_type()
            self._expect(TokenType.RBRACKET)
            return ArrayType(element_type=elem)

        # 元组类型 (T, U)
        if tok.type == TokenType.LPAREN:
            self._advance()
            types = []
            while not self._at(TokenType.RPAREN):
                types.append(self._parse_type())
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RPAREN)
            # 函数类型 (T) -> U
            if self._match(TokenType.ARROW):
                ret = self._parse_type()
                return FunctionType(param_types=types, return_type=ret)
            return TupleType(element_types=types)

        # map<K, V>
        if tok.type == TokenType.IDENTIFIER and tok.value == 'map':
            self._advance()
            self._expect(TokenType.LT)
            k = self._parse_type()
            self._expect(TokenType.COMMA)
            v = self._parse_type()
            self._expect(TokenType.GT)
            return MapType(key_type=k, value_type=v)

        # 命名类型或泛型 T, Result<T>
        if tok.type == TokenType.IDENTIFIER:
            name = self._advance().value
            if self._match(TokenType.LT):
                args = []
                while not self._at(TokenType.GT):
                    args.append(self._parse_type())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.GT)
                return GenericType(base=name, type_args=args)
            # Result[T, E]（方括号写法，与 <T, E> 等价）
            if name == 'Result' and self._match(TokenType.LBRACKET):
                args = []
                while not self._at(TokenType.RBRACKET):
                    args.append(self._parse_type())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RBRACKET)
                return GenericType(base='Result', type_args=args)
            return NamedType(name=name)

        raise ParseError(f"无法解析类型: {tok.value!r}", tok)

    # ── expressions (Pratt-style precedence climbing) ───

    def _parse_expr(self) -> Expr:
        tok = self._current()
        expr = self._parse_pipe()
        # 表达式顶层位置（BinaryOp 等由拼接产生的节点没有位置）
        if expr.line == 0:
            expr.line = tok.line
            expr.column = tok.column
        return expr

    def parse_expression(self) -> Expr:
        """解析单个表达式（供字符串插值等场景使用）"""
        if self._at(TokenType.EOF):
            return NilLiteral()
        return self._parse_expr()

    def _parse_pipe(self) -> Expr:
        """管道：x |> f / x |> f(args) / x |> obj.m()（最低优先级，左结合）"""
        left = self._parse_coalesce()
        while self._match(TokenType.PIPE_OP):
            call = self._parse_postfix()
            left = PipeExpr(left=left, call=call)
        return left

    def _parse_coalesce(self) -> Expr:
        """空合并：a ?? b（最低优先级，左侧为 nil 时取右侧）"""
        left = self._parse_or()
        while self._match(TokenType.NULL_COALESCE):
            right = self._parse_or()
            left = NullCoalesce(left=left, right=right)
        return left

    def _parse_or(self) -> Expr:
        left = self._parse_and()
        while self._match(TokenType.OR):
            right = self._parse_and()
            left = BinaryOp(left=left, op="||", right=right)
        return left

    def _parse_and(self) -> Expr:
        left = self._parse_bitor()
        while self._match(TokenType.AND):
            right = self._parse_bitor()
            left = BinaryOp(left=left, op="&&", right=right)
        return left

    def _parse_bitor(self) -> Expr:
        """位或：a | b"""
        left = self._parse_bitxor()
        while self._match(TokenType.PIPE):
            right = self._parse_bitxor()
            left = BinaryOp(left=left, op="|", right=right)
        return left

    def _parse_bitxor(self) -> Expr:
        """异或：a ^ b"""
        left = self._parse_bitand()
        while self._match(TokenType.CARET):
            right = self._parse_bitand()
            left = BinaryOp(left=left, op="^", right=right)
        return left

    def _parse_bitand(self) -> Expr:
        """位与：a & b（前缀 &x 是引用，由 unary 层处理）"""
        left = self._parse_equality()
        while self._match(TokenType.AMP):
            right = self._parse_equality()
            left = BinaryOp(left=left, op="&", right=right)
        return left

    def _parse_equality(self) -> Expr:
        left = self._parse_relational()
        while self._at(TokenType.EQ, TokenType.NE):
            op = self._advance().value
            right = self._parse_relational()
            left = BinaryOp(left=left, op=op, right=right)
        return left

    def _parse_relational(self) -> Expr:
        left = self._parse_range()
        while self._at(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self._advance().value
            right = self._parse_range()
            left = BinaryOp(left=left, op=op, right=right)
        return left

    def _parse_range(self) -> Expr:
        """区间：a..b（闭区间,含 b;优先级低于比较,高于移位）"""
        left = self._parse_shift()
        while self._match(TokenType.RANGE):
            right = self._parse_shift()
            left = RangeExpr(start=left, end=right)
        return left

    def _parse_shift(self) -> Expr:
        """移位：a << b / a >> b（优先级低于 + -，高于关系比较）"""
        left = self._parse_addition()
        while self._at(TokenType.SHIFT_LEFT, TokenType.SHIFT_RIGHT):
            op = self._advance().value
            right = self._parse_addition()
            left = BinaryOp(left=left, op=op, right=right)
        return left

    def _parse_addition(self) -> Expr:
        left = self._parse_multiplication()
        while self._at(TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_multiplication()
            left = BinaryOp(left=left, op=op, right=right)
        return left

    def _parse_multiplication(self) -> Expr:
        start_line = self._current().line
        left = self._parse_power()
        # 行感知：跨行的 * 视为解引用而非乘法（支持 unsafe 块内 *ptr = v 独立成行）
        while self._at(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            if (self._current().type == TokenType.STAR and start_line
                    and self._current().line != start_line):
                break
            op = self._advance().value
            right = self._parse_power()
            left = BinaryOp(left=left, op=op, right=right)
        return left

    def _parse_power(self) -> Expr:
        base = self._parse_unary()
        if self._match(TokenType.POWER):
            # 右结合：2 ** 3 ** 2 == 2 ** (3 ** 2)
            exp = self._parse_power()
            return BinaryOp(left=base, op="**", right=exp)
        return base

    def _parse_unary(self) -> Expr:
        if self._match(TokenType.MINUS):
            return UnaryOp(op="-", operand=self._parse_unary())
        if self._match(TokenType.NOT):
            return UnaryOp(op="!", operand=self._parse_unary())
        if self._match(TokenType.AMP):
            mutable = bool(self._match(TokenType.MUT))
            return RefExpr(inner=self._parse_unary(), mutable=mutable)
        if self._match(TokenType.STAR):
            return DerefExpr(inner=self._parse_unary())
        if self._match(TokenType.CHANNEL_SEND):
            # 前缀通道接收: <-ch
            return ChannelRecv(channel=self._parse_unary())
        if self._match(TokenType.AWAIT):
            # v3.1.0: await expr
            return AwaitExpr(expression=self._parse_unary())
        return self._parse_postfix()

    def _parse_postfix(self) -> Expr:
        start_tok = self._current()
        expr = self._parse_primary()
        while True:
            if self._match(TokenType.DOT):
                # 元组索引: tup.0, tup.1
                if self._at(TokenType.INTEGER):
                    idx = int(self._advance().value)
                    expr = TupleIndex(object=expr, index=idx)
                    continue
                member = self._expect_member_name()
                # 强制解包: obj.field! (field! 后不跟 ()
                unwrap = member.endswith('!') and not self._at(TokenType.LPAREN)
                if unwrap:
                    member = member[:-1]
                if self._match(TokenType.LPAREN):
                    args, named = self._parse_args()
                    self._expect(TokenType.RPAREN)
                    expr = MethodCall(object=expr, method=member, args=args, named_args=named)
                else:
                    expr = MemberAccess(object=expr, member=member)
                if unwrap:
                    expr = ForcedUnwrap(operand=expr)
            elif self._match(TokenType.OPTIONAL_DOT):
                member = self._expect_member_name()
                unwrap = member.endswith('!') and not self._at(TokenType.LPAREN)
                if unwrap:
                    member = member[:-1]
                if self._match(TokenType.LPAREN):
                    args, named = self._parse_args()
                    self._expect(TokenType.RPAREN)
                    expr = OptionalCall(object=expr, method=member, args=args, named_args=named)
                else:
                    expr = OptionalAccess(object=expr, member=member)
                if unwrap:
                    expr = ForcedUnwrap(operand=expr)
            elif self._at(TokenType.LBRACKET):
                # 换行即语句边界:跨行的 [ 属于新的一行,不是上一表达式的索引
                if start_tok.line != 0 and self._current().line != start_tok.line:
                    break
                self._advance()
                idx = self._parse_expr()
                self._expect(TokenType.RBRACKET)
                expr = IndexAccess(object=expr, index=idx)
            elif self._at(TokenType.LPAREN):
                # 换行即语句边界:跨行的 ( 属于新的一行,不是上一表达式的调用参数
                if start_tok.line != 0 and self._current().line != start_tok.line:
                    break
                self._advance()
                args, named = self._parse_args()
                self._expect(TokenType.RPAREN)
                expr = CallExpr(callee=expr, args=args, named_args=named)
            elif self._match(TokenType.QUESTION):
                expr = TryExpr(expr=expr)
            elif self._match(TokenType.CHANNEL_SEND):
                val = self._parse_expr()
                expr = ChannelSend(channel=expr, value=val)
            else:
                break
        return expr

    def _parse_args(self):
        """解析调用参数，返回 (位置参数列表, 命名参数列表)

        命名参数形如 f(x: 1, y: 2)，仅在 identifier 后紧跟冒号时触发，
        与 map 字面量、lambda 类型注解互不冲突。
        """
        args = []
        named = []
        while not self._at(TokenType.RPAREN):
            if (self._current().type == TokenType.IDENTIFIER
                    and self._peek(1).type == TokenType.COLON):
                name = self._advance().value
                self._expect(TokenType.COLON)
                val = self._parse_expr()
                named.append((name, val))
            else:
                args.append(self._parse_expr())
            if not self._match(TokenType.COMMA):
                break
        return args, named

    def _expect_member_name(self) -> str:
        """成员名:标识符或关键字(支持 obj.import 这类访问)"""
        tok = self._current()
        if tok.type == TokenType.IDENTIFIER or tok.type in _KEYWORD_TYPES:
            return self._advance().value
        raise ParseError(f"期望成员名,得到 {tok.type.name} ({tok.value!r})", tok)

    def _parse_primary(self) -> Expr:
        tok = self._current()

        # 整数
        if tok.type == TokenType.INTEGER:
            self._advance()
            return IntLiteral(value=int(tok.value), line=tok.line, column=tok.column)

        # 浮点
        if tok.type == TokenType.FLOAT:
            self._advance()
            return FloatLiteral(value=float(tok.value), line=tok.line, column=tok.column)

        # 字符串
        if tok.type == TokenType.STRING:
            self._advance()
            return StringLiteral(value=tok.value, line=tok.line, column=tok.column)

        # 原始字符串 r'...' / r"..."(不插值)
        if tok.type == TokenType.RAW_STRING:
            self._advance()
            return StringLiteral(value=tok.value, raw=True, line=tok.line, column=tok.column)

        # 布尔
        if tok.type == TokenType.BOOLEAN:
            self._advance()
            return BoolLiteral(value=(tok.value == 'true'), line=tok.line, column=tok.column)

        # nil
        if tok.type == TokenType.NIL:
            self._advance()
            return NilLiteral(line=tok.line, column=tok.column)

        # lambda 简写: fn x => expr / fn (x, y) => expr
        if tok.type == TokenType.FN:
            self._advance()
            params = []
            if self._at(TokenType.LPAREN):
                self._advance()
                while not self._at(TokenType.RPAREN):
                    pname = self._expect(TokenType.IDENTIFIER).value
                    ptype = None
                    if self._match(TokenType.COLON):
                        ptype = self._parse_type()
                    params.append(Param(name=pname, type_annotation=ptype))
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN)
            else:
                pname = self._expect(TokenType.IDENTIFIER).value
                params.append(Param(name=pname))
            self._expect(TokenType.FAT_ARROW, "lambda 简写需要 =>")
            body_expr = self._parse_expr()
            body = Block(statements=[ReturnStmt(value=body_expr)])
            return LambdaExpr(params=params, body=body, is_expression=True,
                              line=tok.line, column=tok.column)

        # 标识符
        if tok.type == TokenType.IDENTIFIER:
            # Ok(expr) / Err(expr) 特殊形式（仍兼容裸标识符 Ok 作为值）
            if tok.value in ('Ok', 'Err') and self._peek(1).type == TokenType.LPAREN:
                kind = tok.value
                self._advance()  # Ok/Err
                self._expect(TokenType.LPAREN)
                arg = self._parse_expr()
                self._expect(TokenType.RPAREN)
                if kind == 'Ok':
                    return OkExpr(value=arg, line=tok.line, column=tok.column)
                return ErrExpr(error=arg, line=tok.line, column=tok.column)
            name = tok.value
            self._advance()
            # 强制解包: identifier! 后不跟 ( 时为强制解包
            unwrap = name.endswith('!') and not self._at(TokenType.LPAREN)
            if unwrap:
                name = name[:-1]
            ident = Identifier(name=name, line=tok.line, column=tok.column)
            # 结构体字面量: Name { field: value, ... }（仅大写开头的类型名）
            if name and name[0].isupper() and self._at(TokenType.LBRACE):
                self._advance()
                fields = []
                while not self._at(TokenType.RBRACE):
                    fname = self._expect(TokenType.IDENTIFIER).value
                    # v3.2.0: 属性简写 { name, age } 等价于 { name: name, age: age }
                    if self._match(TokenType.COLON):
                        fval = self._parse_expr()
                    else:
                        fval = Identifier(name=fname, line=tok.line, column=tok.column)
                    fields.append((fname, fval))
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RBRACE)
                sl = StructLiteral(type_name=name, fields=fields,
                                   line=tok.line, column=tok.column)
                if unwrap:
                    return ForcedUnwrap(operand=sl, line=tok.line, column=tok.column)
                return sl
            if unwrap:
                return ForcedUnwrap(operand=ident, line=tok.line, column=tok.column)
            return ident

        # 数组字面量 / 列表推导式
        if tok.type == TokenType.LBRACKET:
            self._advance()
            # 空数组 []
            if self._at(TokenType.RBRACKET):
                self._advance()
                return ArrayLiteral(elements=[], line=tok.line, column=tok.column)
            # v3.2.0: 展开运算符 [...arr, 4]
            if self._match(TokenType.VARIADIC):
                first = SpreadExpr(expr=self._parse_expr(), line=tok.line, column=tok.column)
            else:
                first = self._parse_expr()
            # 列表推导式: [expr for x in arr if cond]
            if self._at(TokenType.FOR):
                gens, conds = self._parse_comprehension_clauses()
                self._expect(TokenType.RBRACKET)
                return ListComp(expr=first, generators=gens, conditions=conds,
                                line=tok.line, column=tok.column)
            elems = [first]
            while self._match(TokenType.COMMA):
                if self._at(TokenType.RBRACKET):
                    break
                # v3.2.0: 展开运算符
                if self._match(TokenType.VARIADIC):
                    elems.append(SpreadExpr(expr=self._parse_expr(), line=tok.line, column=tok.column))
                else:
                    elems.append(self._parse_expr())
            self._expect(TokenType.RBRACKET)
            return ArrayLiteral(elements=elems, line=tok.line, column=tok.column)

        # map 字面量 / 集合推导式 / Map 推导式
        if tok.type == TokenType.LBRACE:
            self._advance()
            # 空 map {}
            if self._at(TokenType.RBRACE):
                self._advance()
                return MapLiteral(entries=[], line=tok.line, column=tok.column)
            # v3.2.0: 展开运算符 {...obj, b: 2}
            if self._match(TokenType.VARIADIC):
                spread = SpreadExpr(expr=self._parse_expr(), line=tok.line, column=tok.column)
                entries = [(spread, None)]
            else:
                first_key = self._parse_expr()
                # 集合推导式: {expr for x in arr}
                if self._at(TokenType.FOR):
                    gens, conds = self._parse_comprehension_clauses()
                    self._expect(TokenType.RBRACE)
                    return SetComp(expr=first_key, generators=gens, conditions=conds,
                                   line=tok.line, column=tok.column)
                # Map 字面量或 Map 推导式
                self._expect(TokenType.COLON)
                first_val = self._parse_expr()
                # Map 推导式: {k: v for k, v in pairs}
                if self._at(TokenType.FOR):
                    gens, conds = self._parse_comprehension_clauses()
                    self._expect(TokenType.RBRACE)
                    return MapComp(key_expr=first_key, value_expr=first_val,
                                   generators=gens, conditions=conds,
                                   line=tok.line, column=tok.column)
                entries = [(first_key, first_val)]
            while self._match(TokenType.COMMA):
                if self._at(TokenType.RBRACE):
                    break
                # v3.2.0: 展开运算符
                if self._match(TokenType.VARIADIC):
                    entries.append((SpreadExpr(expr=self._parse_expr(), line=tok.line, column=tok.column), None))
                else:
                    k = self._parse_expr()
                    self._expect(TokenType.COLON)
                    v = self._parse_expr()
                    entries.append((k, v))
            self._expect(TokenType.RBRACE)
            return MapLiteral(entries=entries, line=tok.line, column=tok.column)

        # 分组表达式 / 元组
        if tok.type == TokenType.LPAREN:
            self._advance()
            first = self._parse_expr()
            if self._match(TokenType.COMMA):
                elems = [first]
                while not self._at(TokenType.RPAREN):
                    elems.append(self._parse_expr())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN)
                return TupleLiteral(elements=elems, line=tok.line, column=tok.column)
            self._expect(TokenType.RPAREN)
            return first

        # lambda: |params| { body } 或 |params| expr
        if tok.type == TokenType.PIPE:
            return self._parse_lambda()

        # 空参数 lambda: || { body } / || expr（lexer 将相邻 || 合并为 OR）
        if tok.type == TokenType.OR:
            self._advance()
            return self._finish_lambda(tok, [])

        # if 表达式
        if tok.type == TokenType.IF:
            return self._parse_if_expr()

        # match 表达式
        if tok.type == TokenType.MATCH:
            return self._parse_match_expr()

        # spawn 表达式
        if tok.type == TokenType.SPAWN:
            self._advance()
            call = self._parse_expr()
            return SpawnExpr(call=call, line=tok.line, column=tok.column)

        # chan<T>()
        if tok.type == TokenType.IDENTIFIER and tok.value == 'chan':
            self._advance()
            self._expect(TokenType.LT)
            _ = self._parse_type()
            self._expect(TokenType.GT)
            self._expect(TokenType.LPAREN)
            self._expect(TokenType.RPAREN)
            return CallExpr(callee=Identifier(name="chan"), args=[])

        raise ParseError(f"无法解析的表达式: {tok.value!r} ({tok.type.name})", tok)

    def _parse_lambda(self) -> LambdaExpr:
        tok = self._expect(TokenType.PIPE)
        params = self._parse_lambda_params()
        # 闭合管道：|x| 或 ||（lexer 将相邻 || 合并为 OR token）
        if not self._match(TokenType.PIPE, TokenType.OR):
            self._expect(TokenType.PIPE)
        return self._finish_lambda(tok, params)

    def _parse_lambda_params(self) -> List[Param]:
        params = []
        while not self._at(TokenType.PIPE) and not self._at(TokenType.OR):
            p_name = self._expect(TokenType.IDENTIFIER).value
            p_type = None
            if self._match(TokenType.COLON):
                p_type = self._parse_type()
            default = None
            if self._match(TokenType.ASSIGN):
                default = self._parse_expr()
            params.append(Param(name=p_name, type_annotation=p_type, default_value=default))
            if not self._match(TokenType.COMMA):
                break
        return params

    def _finish_lambda(self, tok: Token, params: List[Param]) -> LambdaExpr:
        ret_type = None
        if self._match(TokenType.ARROW):
            ret_type = self._parse_type()
        if self._at(TokenType.LBRACE):
            body = self._parse_block()
            return LambdaExpr(params=params, return_type=ret_type, body=body,
                              is_expression=False, line=tok.line, column=tok.column)
        else:
            expr = self._parse_expr()
            body = Block(statements=[ReturnStmt(value=expr)])
            return LambdaExpr(params=params, return_type=ret_type, body=body,
                              is_expression=True, line=tok.line, column=tok.column)

    def _parse_if_expr(self) -> IfExpr:
        tok = self._expect(TokenType.IF)
        cond = self._parse_expr()
        then_body = self._parse_block()
        elif_clauses = []
        while self._match(TokenType.ELIF):
            ec = self._parse_expr()
            eb = self._parse_block()
            elif_clauses.append((ec, eb))
        else_body = None
        if self._match(TokenType.ELSE):
            else_body = self._parse_block()
        return IfExpr(condition=cond, then_body=then_body,
                      elif_clauses=elif_clauses, else_body=else_body,
                      line=tok.line, column=tok.column)

    def _parse_match_expr(self) -> MatchExpr:
        tok = self._expect(TokenType.MATCH)
        subject = self._parse_expr()
        self._expect(TokenType.LBRACE)
        arms = []
        while not self._at(TokenType.RBRACE):
            pat = self._parse_pattern()
            self._expect(TokenType.FAT_ARROW)
            body = self._parse_expr()
            arms.append(MatchArm(pattern=pat, body=body))
            self._match(TokenType.COMMA)
        self._expect(TokenType.RBRACE)
        return MatchExpr(subject=subject, arms=arms, line=tok.line, column=tok.column)
