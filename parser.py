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
        pub = bool(self._match(TokenType.PUB))

        tok = self._current()
        if tok.type == TokenType.FN:
            return self._parse_fn_def(is_pub=pub)
        if tok.type == TokenType.TYPE:
            return self._parse_type_def(is_pub=pub)
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
            return self._parse_const()

        # pub 后面必须跟 fn/type/enum/trait
        if pub:
            raise ParseError("'pub' 只能修饰 fn/type/enum/trait", tok)
        return self._parse_statement()

    # ── function definition ─────────────────────────────

    def _parse_fn_def(self, is_pub=False, require_body=True) -> FnDef:
        tok = self._expect(TokenType.FN)
        name = self._expect(TokenType.IDENTIFIER).value
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
                     body=body, is_pub=is_pub, line=tok.line, column=tok.column)

    def _parse_params(self) -> List[Param]:
        params = []
        while not self._at(TokenType.RPAREN):
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

    # ── type definition ─────────────────────────────────

    def _parse_type_def(self, is_pub=False) -> TypeDef:
        self._expect(TokenType.TYPE)
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
                while not self._at(TokenType.RPAREN):
                    f_name = self._expect(TokenType.IDENTIFIER).value
                    self._expect(TokenType.COLON)
                    f_type = self._parse_type()
                    v_fields.append((f_name, f_type))
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN)
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
        if tok.type == TokenType.YIELD:
            return self._parse_yield()

        # 赋值或表达式
        return self._parse_assign_or_expr()

    def _parse_let(self, mutable: bool = False) -> Stmt:
        self._advance()  # let / var
        # 可变绑定还可显式写 let mut x
        if self._match(TokenType.MUT):
            mutable = True
        tok = self._current()

        # 模式解构: let (a, b) = expr / let [a, b] = expr
        if tok.type in (TokenType.LPAREN, TokenType.LBRACKET):
            self._advance()
            names = []
            closing = TokenType.RPAREN if tok.type == TokenType.LPAREN else TokenType.RBRACKET
            while not self._at(closing):
                if self._at(TokenType.EOF):
                    break
                names.append(self._expect(TokenType.IDENTIFIER).value)
                if not self._match(TokenType.COMMA):
                    break
            self._expect(closing)
            self._expect(TokenType.ASSIGN, "解构绑定需要 = 初始化")
            init = self._parse_expr()
            return DestructureLet(names=names, mutable=mutable, initializer=init)

        name = self._expect(TokenType.IDENTIFIER).value
        type_ann = None
        if self._match(TokenType.COLON):
            type_ann = self._parse_type()
        init = None
        if self._match(TokenType.ASSIGN):
            init = self._parse_expr()
        return LetStmt(name=name, mutable=mutable, type_annotation=type_ann, initializer=init)

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
            return BindPattern(name=name)
        # 字面量模式
        lit = self._parse_primary()
        return LiteralPattern(value=lit)

    # ── types ───────────────────────────────────────────

    def _parse_type(self) -> TypeNode:
        """解析类型表达式"""
        # 引用类型 &T / &mut T
        if self._match(TokenType.AMP):
            mutable = bool(self._match(TokenType.MUT))
            inner = self._parse_type()
            return RefType(inner=inner, mutable=mutable)

        base = self._parse_type_atom()

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
        left = self._parse_power()
        while self._at(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
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
        return self._parse_postfix()

    def _parse_postfix(self) -> Expr:
        start_tok = self._current()
        expr = self._parse_primary()
        while True:
            if self._match(TokenType.DOT):
                member = self._expect_member_name()
                if self._match(TokenType.LPAREN):
                    args, named = self._parse_args()
                    self._expect(TokenType.RPAREN)
                    expr = MethodCall(object=expr, method=member, args=args, named_args=named)
                else:
                    expr = MemberAccess(object=expr, member=member)
            elif self._match(TokenType.OPTIONAL_DOT):
                member = self._expect_member_name()
                if self._match(TokenType.LPAREN):
                    args, named = self._parse_args()
                    self._expect(TokenType.RPAREN)
                    expr = OptionalCall(object=expr, method=member, args=args, named_args=named)
                else:
                    expr = OptionalAccess(object=expr, member=member)
            elif self._match(TokenType.LBRACKET):
                idx = self._parse_expr()
                self._expect(TokenType.RBRACKET)
                expr = IndexAccess(object=expr, index=idx)
            elif self._at(TokenType.LPAREN):
                # 换行即语句边界:跨行的 ( 属于新的一行,不是上一表达式的调用参数
                # (NEWLINE token 在解析前被过滤,故用行号判断,避免 `1\n(2)` 被当作 `1(2)`)
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

        # 标识符
        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(name=tok.value, line=tok.line, column=tok.column)

        # 数组字面量
        if tok.type == TokenType.LBRACKET:
            self._advance()
            elems = []
            while not self._at(TokenType.RBRACKET):
                elems.append(self._parse_expr())
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RBRACKET)
            return ArrayLiteral(elements=elems, line=tok.line, column=tok.column)

        # map 字面量
        if tok.type == TokenType.LBRACE:
            self._advance()
            entries = []
            while not self._at(TokenType.RBRACE):
                k = self._parse_expr()
                self._expect(TokenType.COLON)
                v = self._parse_expr()
                entries.append((k, v))
                if not self._match(TokenType.COMMA):
                    break
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
