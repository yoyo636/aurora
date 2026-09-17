"""Aurora ORM — 数据库对象关系映射模块 (v3.2.0 标准库扩展)

支持:
  - SQLite (内置 sqlite3,零依赖) / PostgreSQL (psycopg2) / MySQL (pymysql)
  - 连接字符串解析与连接池
  - Model 模型定义 + 字段类型 + Meta 配置
  - 链式查询构建器 (filter/where/order_by/limit/offset/select/paginate)
  - 完整 CRUD + 批量更新/删除 + get_or_create
  - 关联:has_many / belongs_to / has_one / many_to_many / prefetch_related
  - 迁移管理 (JSON 快照) / 事务 (含 savepoint 嵌套)
  - 数据库自省 / 种子数据 / 查询日志

示例:
    from orm import *

    db = connect("sqlite:///:memory:")

    class User(Model):
        __tablename__ = "users"
        id = IntegerField(primary_key=True, autoincrement=True)
        name = StringField(max_length=100)
        age = IntegerField(nullable=True)

    db.create_all([User])
    u = User.create(name="小明", age=12)
    users = User.filter(age__gt=10).order_by("-id").limit(5).all()
"""

import os
import re
import json
import time
import queue
import sqlite3
import threading
from datetime import datetime, date
from typing import Any, Callable, Dict, List, Optional, Tuple


# ── 异常 ──────────────────────────────────────────────────────────────
class OrmError(Exception):
    """Aurora ORM 运行时异常"""
    def __init__(self, kind: str, message: str):
        self.kind = kind
        super().__init__(f"[{kind}] {message}")


# ── 字段类型 ──────────────────────────────────────────────────────────
class Field:
    """模型字段基类

    选项:
      primary_key   是否主键
      autoincrement 是否自增 (仅 IntegerField 主键生效)
      unique        是否唯一
      index         是否建索引
      nullable      是否可空
      default       默认值 (可为可调用对象)
      column_name   数据库列名 (默认与属性名相同)
      max_length    最大长度 (StringField 使用)
    """

    sql_type_name = "TEXT"

    def __init__(self, primary_key: bool = False, autoincrement: bool = False,
                 unique: bool = False, index: bool = False, nullable: bool = True,
                 default: Any = None, column_name: Optional[str] = None,
                 max_length: Optional[int] = None):
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.unique = unique
        self.index = index
        self.nullable = nullable
        self.default = default
        self.column_name = column_name
        self.max_length = max_length
        self.name: str = ""  # 由 ModelMeta 注入

    # -- 方言适配 --
    def sql_type(self) -> str:
        return self.sql_type_name

    def to_db(self, value: Any) -> Any:
        """Python 值 → 数据库值"""
        return value

    def from_db(self, value: Any) -> Any:
        """数据库值 → Python 值"""
        return value

    def column_sql(self, name: str) -> str:
        """生成 CREATE TABLE 中的列定义 SQL"""
        col = self.column_name or name
        if self.primary_key and self.autoincrement and self.sql_type_name == "INTEGER":
            return f'"{col}" INTEGER PRIMARY KEY AUTOINCREMENT'
        sql = f'"{col}" {self.sql_type()}'
        if self.primary_key:
            sql += " PRIMARY KEY"
        if not self.nullable and not self.primary_key:
            sql += " NOT NULL"
        if self.unique:
            sql += " UNIQUE"
        return sql

    def db_name(self) -> str:
        return self.column_name or self.name

    def serialize(self) -> dict:
        return {
            "type": type(self).__name__,
            "primary_key": self.primary_key,
            "autoincrement": self.autoincrement,
            "unique": self.unique,
            "index": self.index,
            "nullable": self.nullable,
            "column_name": self.column_name,
            "max_length": self.max_length,
        }


class IntegerField(Field):
    """整数字段"""
    sql_type_name = "INTEGER"


class StringField(Field):
    """字符串字段"""
    sql_type_name = "VARCHAR"

    def sql_type(self) -> str:
        if self.max_length:
            return f"VARCHAR({int(self.max_length)})"
        return "VARCHAR(255)"


class TextField(Field):
    """长文本字段"""
    sql_type_name = "TEXT"


class BooleanField(Field):
    """布尔字段 (存储为 0/1)"""
    sql_type_name = "INTEGER"

    def to_db(self, value):
        if value is None:
            return None
        return 1 if value else 0

    def from_db(self, value):
        if value is None:
            return None
        return bool(value)


class FloatField(Field):
    """浮点字段"""
    sql_type_name = "REAL"


class DateTimeField(Field):
    """日期时间字段 (ISO 格式存储)"""
    sql_type_name = "TEXT"

    def to_db(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)

    def from_db(self, value):
        if value is None or isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return value


class DateField(Field):
    """日期字段"""
    sql_type_name = "TEXT"

    def to_db(self, value):
        if value is None:
            return None
        if isinstance(value, date) and not isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        return str(value)

    def from_db(self, value):
        if value is None or isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return value


class JSONField(Field):
    """JSON 字段 (存储为 TEXT)"""
    sql_type_name = "TEXT"

    def to_db(self, value):
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def from_db(self, value):
        if value is None or isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return value


class ForeignKey(Field):
    """外键字段,引用另一张表的主键"""
    sql_type_name = "INTEGER"

    def __init__(self, to, **kwargs):
        self.to = to  # 模型类或模型名字符串
        super().__init__(**kwargs)


# ── 连接字符串解析 ────────────────────────────────────────────────────
def _parse_url(url: str) -> Tuple[str, dict]:
    """解析连接字符串为 (方言, 参数 dict)

    支持:
      sqlite:///path.db   /   sqlite://:memory:
      postgres://user:pass@host:port/dbname
      mysql://user:pass@host:port/dbname
    """
    if url.startswith("sqlite:///"):
        path = url[len("sqlite:///"):]
        return "sqlite", {"path": path if path else ":memory:"}
    if url.startswith("sqlite://"):
        path = url[len("sqlite://"):]
        return "sqlite", {"path": path or ":memory:"}

    m = re.match(
        r"^(postgres(?:ql)?|mysql)://"
        r"(?:([^:@/]+)(?::([^@/]*))?@)?"
        r"([^:/@]+)(?::(\d+))?"
        r"/([^?]+)",
        url,
    )
    if not m:
        raise OrmError("ConnectError", f"无法解析数据库连接字符串: {url!r}")
    scheme, user, password, host, port, dbname = m.groups()
    dialect = "postgres" if scheme.startswith("postgres") else "mysql"
    return dialect, {
        "user": user,
        "password": password or "",
        "host": host or "127.0.0.1",
        "port": int(port) if port else (5432 if dialect == "postgres" else 3306),
        "dbname": dbname.strip("/"),
    }


# ── 连接池 / 数据库 ───────────────────────────────────────────────────
class Database:
    """数据库连接管理 + 连接池 + 查询日志 + 事务

    用法:
        db = connect("sqlite:///app.db", min_conn=1, max_conn=5)
        db.execute("SELECT 1")
        with db.transaction():
            ...
    """

    def __init__(self, url: str, min_conn: int = 1, max_conn: int = 5,
                 timeout: float = 30.0):
        self.url = url
        self.dialect, self.params = _parse_url(url)
        self.min_conn = max(1, min_conn)
        self.max_conn = max(self.min_conn, max_conn)
        self.timeout = timeout
        self.queries: List[dict] = []
        self._pool: "queue.Queue" = queue.Queue()
        self._in_use = 0
        self._lock = threading.Lock()
        self._local = threading.local()
        self._txn_stack: List[Optional[str]] = []
        self._closed = False

        # SQLite 内存库必须使用单连接 (每个连接独立数据库)
        self._memory_single = (self.dialect == "sqlite"
                               and self.params.get("path") in (":memory:", ""))
        if self._memory_single:
            self._single = self._create_conn()
        else:
            for _ in range(self.min_conn):
                self._pool.put(self._create_conn())

    # -- 连接创建 --
    def _create_conn(self):
        if self.dialect == "sqlite":
            conn = sqlite3.connect(self.params["path"],
                                   check_same_thread=False,
                                   timeout=self.timeout)
            conn.row_factory = sqlite3.Row
            return conn
        if self.dialect == "postgres":
            try:
                import psycopg2  # type: ignore
                import psycopg2.extras  # type: ignore
            except ImportError:
                raise OrmError("ConnectError",
                               "未安装 psycopg2,无法连接 PostgreSQL;请执行 pip install psycopg2-binary")
            return psycopg2.connect(
                dbname=self.params["dbname"], user=self.params["user"],
                password=self.params["password"], host=self.params["host"],
                port=self.params["port"], connect_timeout=int(self.timeout))
        if self.dialect == "mysql":
            try:
                import pymysql  # type: ignore
            except ImportError:
                raise OrmError("ConnectError",
                               "未安装 pymysql,无法连接 MySQL;请执行 pip install pymysql")
            return pymysql.connect(
                database=self.params["dbname"], user=self.params["user"],
                password=self.params["password"], host=self.params["host"],
                port=self.params["port"], connect_timeout=int(self.timeout),
                charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
        raise OrmError("ConnectError", f"不支持的数据库类型: {self.dialect}")

    # -- 连接池 --
    def acquire(self):
        if self._memory_single:
            return self._single
        with self._lock:
            try:
                conn = self._pool.get_nowait()
            except queue.Empty:
                if self._in_use >= self.max_conn:
                    try:
                        conn = self._pool.get(timeout=self.timeout)
                    except queue.Empty:
                        raise OrmError("PoolError",
                                       f"连接池耗尽 (max={self.max_conn})")
                else:
                    conn = self._create_conn()
            self._in_use += 1
            return conn

    def release(self, conn):
        if self._memory_single:
            return
        with self._lock:
            self._in_use -= 1
            self._pool.put(conn)

    def _txn_conn(self):
        return getattr(self._local, "conn", None)

    # -- SQL 执行 --
    def execute(self, sql: str, params=()):
        """执行 SQL,返回 cursor。自动提交/回滚 (事务内由事务管理)"""
        in_txn = self._txn_conn() is not None
        conn = self._txn_conn() or self.acquire()
        try:
            self.queries.append({"sql": sql, "params": list(params)})
            cur = conn.cursor()
            cur.execute(sql, list(params))
            if not in_txn:
                conn.commit()
            return cur
        except Exception as e:
            if not in_txn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            raise OrmError("SQLError", str(e)) from e
        finally:
            if not in_txn:
                self.release(conn)

    def executemany(self, sql: str, seq_of_params):
        """批量执行 SQL"""
        in_txn = self._txn_conn() is not None
        conn = self._txn_conn() or self.acquire()
        try:
            self.queries.append({"sql": sql, "params": f"<{len(seq_of_params)} rows>"})
            cur = conn.cursor()
            cur.executemany(sql, [list(p) for p in seq_of_params])
            if not in_txn:
                conn.commit()
            return cur
        except Exception as e:
            if not in_txn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            raise OrmError("SQLError", str(e)) from e
        finally:
            if not in_txn:
                self.release(conn)

    # -- 事务 --
    def begin(self):
        """开启事务;嵌套时使用 SAVEPOINT"""
        conn = self._txn_conn()
        if conn is None:
            conn = self.acquire()
            self._local.conn = conn
            self._txn_stack.append(None)
        else:
            sp = f"sp_{len(self._txn_stack)}"
            conn.execute(f"SAVEPOINT {sp}")
            self._txn_stack.append(sp)
        return conn

    def commit(self):
        conn = self._txn_conn()
        if conn is None:
            raise OrmError("TransactionError", "没有活动的事务")
        sp = self._txn_stack.pop()
        if sp is None:
            conn.commit()
            self._local.conn = None
            self.release(conn)
        else:
            conn.execute(f"RELEASE SAVEPOINT {sp}")

    def rollback(self):
        conn = self._txn_conn()
        if conn is None:
            raise OrmError("TransactionError", "没有活动的事务")
        sp = self._txn_stack.pop()
        if sp is None:
            conn.rollback()
            self._local.conn = None
            self.release(conn)
        else:
            conn.execute(f"ROLLBACK TO SAVEPOINT {sp}")

    def transaction(self, fn: Callable):
        """在事务中执行 fn,成功 commit,异常 rollback"""
        self.begin()
        try:
            result = fn()
            self.commit()
            return result
        except Exception:
            try:
                self.rollback()
            except Exception:
                pass
            raise

    # -- 自省 --
    def tables(self) -> List[str]:
        """列出数据库中的所有表"""
        if self.dialect == "sqlite":
            cur = self.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            return [r[0] for r in cur.fetchall()]
        raise OrmError("IntrospectError", f"方言 {self.dialect} 暂未支持 tables()")

    def columns(self, table: str) -> List[dict]:
        """列出表的列信息"""
        if self.dialect == "sqlite":
            cur = self.execute(f"PRAGMA table_info('{table}')")
            return [{"cid": r[0], "name": r[1], "type": r[2],
                     "notnull": bool(r[3]), "pk": bool(r[5])}
                    for r in cur.fetchall()]
        raise OrmError("IntrospectError", f"方言 {self.dialect} 暂未支持 columns()")

    def indexes(self, table: str) -> List[dict]:
        """列出表的索引"""
        if self.dialect == "sqlite":
            cur = self.execute(f"PRAGMA index_list('{table}')")
            return [{"seq": r[0], "name": r[1], "unique": bool(r[2])}
                    for r in cur.fetchall()]
        raise OrmError("IntrospectError", f"方言 {self.dialect} 暂未支持 indexes()")

    # -- 建表 --
    def create_all(self, models: List[type]):
        """为给定模型创建所有表 (IF NOT EXISTS)"""
        for model in models:
            model._build_table()

    def close(self):
        """关闭所有连接"""
        if self._memory_single:
            try:
                self._single.close()
            except Exception:
                pass
            return
        while True:
            try:
                conn = self._pool.get_nowait()
                conn.close()
            except queue.Empty:
                break
        self._closed = True


# 全局默认数据库
_DEFAULT_DB: Optional[Database] = None


def connect(url: str, min_conn: int = 1, max_conn: int = 5,
            timeout: float = 30.0) -> Database:
    """连接数据库并设为默认数据库

    支持:
      sqlite:///path.db   /   sqlite://:memory:
      postgres://user:pass@host:port/db
      mysql://user:pass@host:port/db
    """
    global _DEFAULT_DB
    db = Database(url, min_conn=min_conn, max_conn=max_conn, timeout=timeout)
    _DEFAULT_DB = db
    return db


def _get_db() -> Database:
    if _DEFAULT_DB is None:
        raise OrmError("ConnectError", "尚未连接数据库,请先调用 connect(...)")
    return _DEFAULT_DB


# ── 关联描述符 ────────────────────────────────────────────────────────
class _RelationBase:
    def __init__(self, to, foreign_key: Optional[str] = None, through: Optional[str] = None):
        self.to = to
        self.foreign_key = foreign_key
        self.through = through
        self.name = ""  # 由 ModelMeta 注入

    def _resolve_model(self):
        if isinstance(self.to, str):
            registry = getattr(ModelMeta, "_registry", {})
            return registry.get(self.to)
        return self.to


class HasMany(_RelationBase):
    """一对多:父对象拥有多个子对象"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        cache = instance.__dict__.get(f"_prefetch_{self.name}")
        if cache is not None:
            return QuerySet(self._resolve_model(), _results=list(cache))
        fk = self.foreign_key or _guess_fk(owner)
        return self._resolve_model().filter(**{fk: instance.pk})


class BelongsTo(_RelationBase):
    """多对一:子对象属于一个父对象"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        fk = self.foreign_key or _guess_fk(self._resolve_model())
        fk_val = getattr(instance, fk, None)
        if fk_val is None:
            return None
        return self._resolve_model().get(fk_val)


class HasOne(_RelationBase):
    """一对一"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        fk = self.foreign_key or _guess_fk(owner)
        return self._resolve_model().filter(**{fk: instance.pk}).first()


class ManyToMany(_RelationBase):
    """多对多,through 为中间表名"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        rel = self._resolve_model()
        through = self.through
        if not through:
            raise OrmError("RelationError", f"many_to_many 需指定 through_table")
        fk_self = _guess_fk(owner)
        fk_other = _guess_fk(rel)
        sql = (f"SELECT r.* FROM \"{rel._tablename}\" r "
               f"JOIN \"{through}\" t ON r.\"{rel._pk_col()}\" = t.\"{fk_other}\" "
               f"WHERE t.\"{fk_self}\" = ?")
        cur = rel._db.execute(sql, (instance.pk,))
        return [rel._from_row(dict(row)) for row in cur.fetchall()]


def has_many(to, foreign_key: Optional[str] = None):
    """声明一对多关联"""
    return HasMany(to, foreign_key)


def belongs_to(to, foreign_key: Optional[str] = None):
    """声明多对一关联"""
    return BelongsTo(to, foreign_key)


def has_one(to, foreign_key: Optional[str] = None):
    """声明一对一关联"""
    return HasOne(to, foreign_key)


def many_to_many(to, through_table: str):
    """声明多对多关联"""
    return ManyToMany(to, through=through_table)


def _guess_fk(model) -> str:
    return f"{model.__name__.lower()}_id"


# ── Model 元类 ────────────────────────────────────────────────────────
class ModelMeta(type):
    """收集字段、关联与表配置"""
    _registry: Dict[str, type] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name == "Model":
            return cls

        fields: Dict[str, Field] = {}
        relations: Dict[str, _RelationBase] = {}
        for base in bases:
            base_fields = getattr(base, "_fields", None)
            if base_fields:
                fields.update(base_fields)

        for attr, val in list(namespace.items()):
            if isinstance(val, Field):
                val.name = attr
                fields[attr] = val
            elif isinstance(val, _RelationBase):
                val.name = attr
                relations[attr] = val

        cls._fields = fields
        cls._relations = relations

        # 表名:__tablename__ 直接属性 > Meta.db_table > 类名复数
        tablename = namespace.get("__tablename__")
        meta = namespace.get("Meta")
        if tablename is None and meta is not None:
            tablename = getattr(meta, "db_table", None) or getattr(meta, "table", None)
        if tablename is None:
            tablename = name.lower() + "s"
        cls._tablename = tablename

        # 主键字段
        pk_field = next((f for f in fields.values() if f.primary_key), None)
        if pk_field is None:
            # 自动注入 id 主键
            auto = IntegerField(primary_key=True, autoincrement=True)
            auto.name = "id"
            fields["id"] = auto
            cls.id = auto
            pk_field = auto
        cls._pk_field = pk_field
        cls._pk_name = pk_field.name

        ModelMeta._registry[name] = cls
        return cls


# ── 查询构建器 ─────────────────────────────────────────────────────────
_OPERATORS = {
    "exact":      (lambda c, v: (f'"{c}" = ?', lambda v: [v])),
    "gt":         (lambda c, v: (f'"{c}" > ?', lambda v: [v])),
    "lt":         (lambda c, v: (f'"{c}" < ?', lambda v: [v])),
    "gte":        (lambda c, v: (f'"{c}" >= ?', lambda v: [v])),
    "lte":        (lambda c, v: (f'"{c}" <= ?', lambda v: [v])),
    "ne":         (lambda c, v: (f'"{c}" != ?', lambda v: [v])),
    "contains":   (lambda c, v: (f'"{c}" LIKE ?', lambda v: [f"%{v}%"])),
    "startswith": (lambda c, v: (f'"{c}" LIKE ?', lambda v: [f"{v}%"])),
    "endswith":   (lambda c, v: (f'"{c}" LIKE ?', lambda v: [f"%{v}"])),
    "in":         (lambda c, v: (f'"{c}" IN ({",".join("?" * len(list(v)))})', list)),
    "isnull":     (lambda c, v: (f'"{c}" IS {"NOT" if v else "NULL"}', lambda v: [])),
}


class QuerySet:
    """惰性查询构建器,支持链式调用"""

    def __init__(self, model, _results=None):
        self.model = model
        self.db = model._db or _get_db()
        self._where: List[Tuple[str, list]] = []
        self._order: List[str] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._columns: Optional[List[str]] = None
        self._prefetch: List[str] = []
        self._cached = _results  # 预加载结果直接返回

    def _clone(self) -> "QuerySet":
        qs = QuerySet(self.model)
        qs._where = list(self._where)
        qs._order = list(self._order)
        qs._limit = self._limit
        qs._offset = self._offset
        qs._columns = self._columns
        qs._prefetch = list(self._prefetch)
        return qs

    # -- 条件 --
    def filter(self, **kwargs) -> "QuerySet":
        """按字段条件过滤,支持 field__gt / field__in 等操作符"""
        qs = self._clone()
        for key, val in kwargs.items():
            col, op = self._parse_key(key)
            if op not in _OPERATORS:
                raise OrmError("QueryError", f"不支持的查询操作符: {op}")
            col_obj = self.model._fields.get(col)
            if col_obj is None:
                raise OrmError("QueryError",
                               f"模型 {self.model.__name__} 没有字段 {col!r}")
            db_col = col_obj.db_name()
            sql, param_fn = _OPERATORS[op](db_col, val)
            params = param_fn(val)
            qs._where.append((sql, list(params)))
        return qs

    def where(self, raw_sql: str, *params) -> "QuerySet":
        """添加原始 SQL 条件"""
        qs = self._clone()
        qs._where.append((raw_sql, list(params)))
        return qs

    @staticmethod
    def _parse_key(key: Tuple[str, str]):
        parts = key.split("__")
        if len(parts) == 1:
            return parts[0], "exact"
        return "__".join(parts[:-1]), parts[-1]

    def order_by(self, *fields) -> "QuerySet":
        """排序;-id 表示降序"""
        qs = self._clone()
        for f in fields:
            if f.startswith("-"):
                qs._order.append(f'"{f[1:]}" DESC')
            else:
                qs._order.append(f'"{f}" ASC')
        return qs

    def limit(self, n: int) -> "QuerySet":
        qs = self._clone()
        qs._limit = int(n)
        return qs

    def offset(self, n: int) -> "QuerySet":
        qs = self._clone()
        qs._offset = int(n)
        return qs

    def select(self, *cols) -> "QuerySet":
        """只查询指定列"""
        qs = self._clone()
        qs._columns = list(cols)
        return qs

    def prefetch_related(self, *paths) -> "QuerySet":
        """预加载关联,如 prefetch_related('posts', 'posts.comments')"""
        qs = self._clone()
        qs._prefetch.extend(paths)
        return qs

    # -- SQL 构建 --
    def _build_where(self) -> Tuple[str, list]:
        if not self._where:
            return "", []
        clauses, params = [], []
        for frag, ps in self._where:
            clauses.append(frag)
            params.extend(ps)
        return " AND ".join(clauses), params

    def _build_select(self, count: bool = False) -> Tuple[str, list]:
        table = self.model._tablename
        if count:
            select = "COUNT(*)"
        elif self._columns:
            select = ", ".join(f'"{c}"' for c in self._columns)
        else:
            select = "*"
        sql = f'SELECT {select} FROM "{table}"'
        where_sql, params = self._build_where()
        if where_sql:
            sql += " WHERE " + where_sql
        if not count:
            if self._order:
                sql += " ORDER BY " + ", ".join(self._order)
            if self._limit is not None:
                sql += f" LIMIT {int(self._limit)}"
            if self._offset is not None:
                sql += f" OFFSET {int(self._offset)}"
        return sql, params

    # -- 终端操作 --
    def all(self) -> list:
        """执行查询并返回模型实例列表"""
        if self._cached is not None:
            return list(self._cached)
        sql, params = self._build_select()
        cur = self.db.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        objects = [self.model._from_row(r) for r in rows]
        for path in self._prefetch:
            self._do_prefetch(objects, path)
        return objects

    def first(self):
        """返回第一条记录或 None"""
        return self.limit(1).all()[0] if self.limit(1).all() else None

    def count(self) -> int:
        """计数"""
        sql, params = self._build_select(count=True)
        cur = self.db.execute(sql, params)
        row = cur.fetchone()
        return int(row[0] if row else 0)

    def exists(self) -> bool:
        """是否存在记录"""
        return self.limit(1).count() > 0

    def paginate(self, page: int = 1, per_page: int = 20) -> dict:
        """分页,返回 {items, total, page, per_page, pages}"""
        total = self.count()
        page = max(1, int(page))
        per_page = max(1, int(per_page))
        items = self.offset((page - 1) * per_page).limit(per_page).all()
        pages = max(1, (total + per_page - 1) // per_page) if total else 0
        return {"items": items, "total": total, "page": page,
                "per_page": per_page, "pages": pages}

    # -- 预加载实现 --
    def _do_prefetch(self, objects: list, path: str):
        parts = path.split(".", 1)
        rel_name = parts[0]
        rel = getattr(self.model, rel_name, None)
        if not isinstance(rel, _RelationBase):
            return
        rel_model = rel._resolve_model()
        if isinstance(rel, HasMany):
            fk = rel.foreign_key or _guess_fk(self.model)
            pks = [o.pk for o in objects]
            if not pks:
                return
            related = rel_model.filter(**{fk + "__in": pks}).all()
            groups: dict = {}
            for r in related:
                groups.setdefault(getattr(r, fk), []).append(r)
            for o in objects:
                o.__dict__[f"_prefetch_{rel_name}"] = groups.get(o.pk, [])
            if len(parts) > 1:
                deeper = QuerySet(rel_model).prefetch_related(parts[1:][0])
                deeper._do_prefetch(related, parts[1:][0])


# ── 批量更新/删除 ─────────────────────────────────────────────────────
class _BatchUpdater:
    """Model.update(**values) 的链式批量更新器"""
    def __init__(self, model, values: dict):
        self.model = model
        self.values = values

    def where(self, **kwargs) -> int:
        """按条件批量更新,返回受影响行数"""
        qs = self.model.filter(**kwargs)
        where_sql, params = qs._build_where()
        table = self.model._tablename
        sets = ", ".join(f'"{k}" = ?' for k in self.values)
        params = list(self.values.values()) + params
        sql = f'UPDATE "{table}" SET {sets}'
        if where_sql:
            sql += " WHERE " + where_sql
        cur = self.model._get_db().execute(sql, params)
        return cur.rowcount


class _BatchDeleter:
    """Model.delete() 的链式批量删除器"""
    def __init__(self, model):
        self.model = model

    def where(self, **kwargs) -> int:
        """按条件批量删除,返回受影响行数"""
        qs = self.model.filter(**kwargs)
        where_sql, params = qs._build_where()
        sql = f'DELETE FROM "{self.model._tablename}"'
        if where_sql:
            sql += " WHERE " + where_sql
        cur = self.model._get_db().execute(sql, params)
        return cur.rowcount


# ── Model 基类 ────────────────────────────────────────────────────────
class Model(metaclass=ModelMeta):
    """所有 ORM 模型的基类

    用法:
        class User(Model):
            __tablename__ = "users"
            id = IntegerField(primary_key=True, autoincrement=True)
            name = StringField(max_length=100)
    """

    _db: Optional[Database] = None
    _fields: Dict[str, Field] = {}
    _relations: Dict[str, _RelationBase] = {}
    _tablename: str = ""
    _pk_field: Optional[Field] = None
    _pk_name: str = "id"

    # -- 数据库绑定 --
    @classmethod
    def use_db(cls, db: Database):
        """绑定模型到指定数据库"""
        cls._db = db

    @classmethod
    def _get_db(cls) -> Database:
        return cls._db or _get_db()

    @classmethod
    def _pk_col(cls) -> str:
        return cls._pk_field.db_name()

    # -- 构造 --
    def __init__(self, **kwargs):
        object.__setattr__(self, "_data", {})
        object.__setattr__(self, "_loaded", False)
        for name, field in self._fields.items():
            if name in kwargs:
                self._data[name] = kwargs[name]
            elif field.default is not None:
                self._data[name] = (field.default() if callable(field.default)
                                     else field.default)
            else:
                self._data[name] = None

    def __getattribute__(self, name):
        # 拦截字段名:返回 _data 中的值,而非类上的 Field 对象
        fields = type(self).__dict__.get("_fields") or {}
        if name in fields:
            data = object.__getattribute__(self, "_data")
            field = fields[name]
            return field.from_db(data.get(name))
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        # 仅在正常属性查找失败时调用 (字段名已由 __getattribute__ 拦截)
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        data = self.__dict__.get("_data")
        if data is not None and name in data:
            field = type(self)._fields.get(name)
            if field is not None:
                return field.from_db(data[name])
            return data[name]
        raise AttributeError(f"{type(self).__name__} 没有属性 {name!r}")

    def __setattr__(self, name, value):
        if name in type(self)._fields:
            self._data[name] = value
        else:
            object.__setattr__(self, name, value)

    def __repr__(self):
        pk = self.pk
        return f"<{type(self).__name__} id={pk}>"

    @property
    def pk(self):
        return self._data.get(self._pk_name)

    @pk.setter
    def pk(self, value):
        self._data[self._pk_name] = value

    @classmethod
    def _from_row(cls, row: dict) -> "Model":
        obj = cls.__new__(cls)
        # 把数据库列名映射回属性名
        data = {}
        for name, field in cls._fields.items():
            col = field.db_name()
            if col in row:
                data[name] = row[col]
            elif name in row:
                data[name] = row[name]
        object.__setattr__(obj, "_data", data)
        object.__setattr__(obj, "_loaded", True)
        return obj

    # -- 建表 --
    @classmethod
    def _build_table(cls):
        cols = [f.column_sql(n) for n, f in cls._fields.items()]
        sql = f'CREATE TABLE IF NOT EXISTS "{cls._tablename}" ({", ".join(cols)})'
        cls._get_db().execute(sql)
        # 建索引
        for name, field in cls._fields.items():
            if field.index and not field.primary_key:
                idx_name = f"idx_{cls._tablename}_{field.db_name()}"
                cls._get_db().execute(
                    f'CREATE INDEX IF NOT EXISTS "{idx_name}" ON "{cls._tablename}" ("{field.db_name()}")')

    # -- 查询入口 --
    @classmethod
    def filter(cls, **kwargs) -> QuerySet:
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def where(cls, raw_sql: str, *params) -> QuerySet:
        return QuerySet(cls).where(raw_sql, *params)

    @classmethod
    def all(cls) -> list:
        return QuerySet(cls).all()

    @classmethod
    def first(cls):
        return QuerySet(cls).first()

    @classmethod
    def get(cls, *args, **kwargs):
        """按主键或条件获取单个对象;不存在返回 None"""
        if args and len(args) == 1 and not kwargs:
            qs = QuerySet(cls).filter(**{cls._pk_name: args[0]})
        else:
            qs = QuerySet(cls).filter(**kwargs)
        results = qs.limit(2).all()
        if not results:
            return None
        if len(results) > 1:
            raise OrmError("MultipleObjectsReturned",
                           f"get() 查到了多条 {cls.__name__} 记录")
        return results[0]

    @classmethod
    def count(cls) -> int:
        return QuerySet(cls).count()

    @classmethod
    def exists(cls) -> bool:
        return QuerySet(cls).exists()

    @classmethod
    def paginate(cls, page: int = 1, per_page: int = 20) -> dict:
        return QuerySet(cls).paginate(page, per_page)

    @classmethod
    def raw(cls, sql: str, *params) -> list:
        """执行原始 SQL,返回模型实例列表"""
        cur = cls._get_db().execute(sql, params)
        return [cls._from_row(dict(r)) for r in cur.fetchall()]

    # -- CRUD --
    @classmethod
    def create(cls, **kwargs) -> "Model":
        """创建并保存一条记录,返回实例"""
        obj = cls(**kwargs)
        obj.save()
        return obj

    def save(self):
        """插入或更新 (根据是否已从数据库加载)"""
        db = self._get_db()
        if self._loaded:
            sets, params = [], []
            pk_col = self._pk_field.db_name()
            for name, field in self._fields.items():
                if name == self._pk_name:
                    continue
                sets.append(f'"{field.db_name()}" = ?')
                params.append(field.to_db(self._data.get(name)))
            params.append(self._data.get(self._pk_name))
            sql = (f'UPDATE "{self._tablename}" SET {", ".join(sets)} '
                   f'WHERE "{pk_col}" = ?')
            db.execute(sql, params)
        else:
            cols, vals, params = [], [], []
            for name, field in self._fields.items():
                v = self._data.get(name)
                if v is None and field.autoincrement:
                    continue
                cols.append(f'"{field.db_name()}"')
                vals.append("?")
                params.append(field.to_db(v))
            sql = (f'INSERT INTO "{self._tablename}" ({", ".join(cols)}) '
                   f'VALUES ({", ".join(vals)})')
            cur = db.execute(sql, params)
            if self._pk_field.autoincrement and self._data.get(self._pk_name) is None:
                self._data[self._pk_name] = cur.lastrowid
            self._loaded = True
        return self

    def delete(self):
        """删除当前实例"""
        pk_col = self._pk_field.db_name()
        self._get_db().execute(
            f'DELETE FROM "{self._tablename}" WHERE "{pk_col}" = ?',
            (self._data.get(self._pk_name),))
        self._loaded = False

    @classmethod
    def update(cls, **kwargs) -> _BatchUpdater:
        """批量更新入口:Model.update(name='x').where(id=1)"""
        return _BatchUpdater(cls, kwargs)

    @classmethod
    def delete(cls) -> _BatchDeleter:  # type: ignore[override]
        """批量删除入口:Model.delete().where(age__lt=18)"""
        return _BatchDeleter(cls)

    @classmethod
    def get_or_create(cls, defaults: Optional[dict] = None, **kwargs):
        """按条件查询,不存在则创建,返回 (实例, 是否新建)"""
        obj = QuerySet(cls).filter(**kwargs).first()
        if obj is not None:
            return obj, False
        data = dict(kwargs)
        data.update(defaults or {})
        return cls.create(**data), True

    @classmethod
    def seed(cls, records: List[dict]):
        """批量插入种子数据"""
        if not records:
            return
        cols = list(records[0].keys())
        table = cls._tablename
        col_sql = ", ".join(f'"{c}"' for c in cols)
        placeholders = ", ".join("?" for _ in cols)
        sql = f'INSERT INTO "{table}" ({col_sql}) VALUES ({placeholders})'
        db = cls._get_db()
        params_seq = [tuple(r.get(c) for c in cols) for r in records]
        db.executemany(sql, params_seq)

    # -- 快照 (迁移用) --
    @classmethod
    def _snapshot(cls) -> dict:
        return {
            "table": cls._tablename,
            "fields": {n: f.serialize() for n, f in cls._fields.items()},
        }


# ── 迁移 ──────────────────────────────────────────────────────────────
class Migration:
    """迁移管理器:以 JSON 快照记录模型定义并执行建表/回滚

    用法:
        m = Migration(db, migrations_dir="migrations")
        m.makemigrations("init")   # 生成迁移文件
        m.migrate()                # 执行未应用的迁移
        m.show()                  # 查看状态
        m.rollback(1)              # 回滚一步
    """

    TRACK_TABLE = "_orm_migrations"

    def __init__(self, db: Optional[Database] = None,
                 migrations_dir: str = "migrations"):
        self.db = db or _get_db()
        self.dir = migrations_dir
        os.makedirs(self.dir, exist_ok=True)
        self.db.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TRACK_TABLE} "
            f"(name TEXT PRIMARY KEY, applied_at TEXT)")

    def _track_rows(self) -> set:
        cur = self.db.execute(f"SELECT name FROM {self.TRACK_TABLE}")
        return {r[0] for r in cur.fetchall()}

    def _list_files(self) -> List[str]:
        files = sorted(f for f in os.listdir(self.dir)
                       if f.endswith(".json"))
        return files

    def makemigrations(self, name: str = "auto", models: Optional[List[type]] = None) -> str:
        """根据模型注册表生成一份 JSON 迁移快照"""
        if models is None:
            models = list(ModelMeta._registry.values())
        applied = self._track_rows()
        next_num = len(applied) + 1
        # 文件名序号按已有文件编号递增
        existing = self._list_files()
        if existing:
            last_num = max(int(f.split("_")[0]) for f in existing if f.split("_")[0].isdigit())
            next_num = last_num + 1
        fname = f"{next_num:04d}_{name}.json"
        payload = {
            "name": fname,
            "models": {m.__name__: m._snapshot() for m in models},
        }
        path = os.path.join(self.dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return fname

    def migrate(self):
        """执行所有未应用的迁移"""
        applied = self._track_rows()
        for fname in self._list_files():
            if fname in applied:
                continue
            with open(os.path.join(self.dir, fname), "r", encoding="utf-8") as f:
                payload = json.load(f)
            for model_name, snap in payload.get("models", {}).items():
                model = ModelMeta._registry.get(model_name)
                if model is not None:
                    model._build_table()
            self.db.execute(
                f"INSERT OR REPLACE INTO {self.TRACK_TABLE} (name, applied_at) "
                f"VALUES (?, ?)",
                (fname, datetime.now().isoformat(timespec="seconds")))

    def rollback(self, steps: int = 1):
        """回滚最近 N 步迁移 (DROP 对应表)"""
        rows = self.db.execute(
            f"SELECT name FROM {self.TRACK_TABLE} ORDER BY applied_at DESC"
        ).fetchall()
        to_rollback = [r[0] for r in rows[:steps]]
        for fname in to_rollback:
            path = os.path.join(self.dir, fname)
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                for model_name, snap in payload.get("models", {}).items():
                    table = snap.get("table")
                    if table:
                        self.db.execute(f'DROP TABLE IF EXISTS "{table}"')
            self.db.execute(
                f"DELETE FROM {self.TRACK_TABLE} WHERE name = ?", (fname,))

    def show(self) -> List[dict]:
        """查看迁移状态"""
        applied = self._track_rows()
        result = []
        for fname in self._list_files():
            result.append({"name": fname, "applied": fname in applied})
        return result


# ── 公开导出 ──────────────────────────────────────────────────────────
__all__ = [
    "OrmError",
    "Field", "IntegerField", "StringField", "TextField", "BooleanField",
    "FloatField", "DateTimeField", "DateField", "JSONField", "ForeignKey",
    "Database", "connect",
    "Model", "QuerySet",
    "has_many", "belongs_to", "has_one", "many_to_many",
    "Migration",
]
