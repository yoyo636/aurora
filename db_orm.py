# -*- coding: utf-8 -*-
"""
Aurora v3.2.0 数据库 ORM 框架（std.db 内置模块）
==================================================

纯 Python 标准库实现，支持：
  - SQLite（内置，默认后端）
  - PostgreSQL（可选驱动 psycopg2）
  - MySQL（可选驱动 pymysql / mysql-connector）

使用示例：
    from db_orm import Model, Field, Connection

    Connection.connect_from_url("sqlite:///app.db")

    class User(Model):
        name  = Field(type='str', unique=True)
        email = Field(type='str')
        age   = Field(type='int', default=0)

    User.create_table()
    u = User.create(name="Alice", email="a@b.com")
    users = User.filter(age__gt=18).order_by("-id").all()
"""

import os
import re
import json
import sqlite3
import random
import datetime
import functools
from collections import OrderedDict


# ======================================================================
# 全局连接管理：模型操作默认使用的连接
# ======================================================================

# 当前默认连接（由 Connection.connect_from_url 设置）
_default_connection = None


def get_connection():
    """获取全局默认连接，未初始化时自动使用 SQLite 内存库。"""
    global _default_connection
    if _default_connection is None:
        _default_connection = Connection("sqlite:///:memory:")
        _default_connection.connect()
    return _default_connection


def set_connection(conn):
    """设置全局默认连接。"""
    global _default_connection
    _default_connection = conn


# ======================================================================
# 数据库后端（SQL 方言差异）
# ======================================================================

class SQLiteBackend:
    """SQLite 后端（标准库 sqlite3）。"""
    placeholder = "?"

    TYPE_MAP = {
        'int':      'INTEGER',
        'str':      'TEXT',
        'float':    'REAL',
        'bool':     'INTEGER',
        'text':     'TEXT',
        'datetime': 'TEXT',
        'json':     'TEXT',
        'blob':     'BLOB',
    }

    AUTOINCREMENT = "AUTOINCREMENT"

    def build_create_table(self, table_name, columns_sql):
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_sql)})"

    def connect(self, dbname):
        # dbname 为路径，:memory: 表示内存库
        return sqlite3.connect(dbname)


class PostgreSQLBackend:
    """PostgreSQL 后端（驱动可选，缺失时优雅降级）。"""
    placeholder = "%s"

    TYPE_MAP = {
        'int':      'INTEGER',
        'str':      'VARCHAR(255)',
        'float':    'DOUBLE PRECISION',
        'bool':     'BOOLEAN',
        'text':     'TEXT',
        'datetime': 'TIMESTAMP',
        'json':     'JSONB',
        'blob':     'BYTEA',
    }

    AUTOINCREMENT = "SERIAL"

    def __init__(self):
        self.driver = None
        try:
            import psycopg2
            self.driver = psycopg2
        except ImportError:
            import sys
            print("[db_orm] 警告：未安装 psycopg2，PostgreSQL 后端降级为 SQLite 语法。")

    def build_create_table(self, table_name, columns_sql):
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_sql)})"

    def connect(self, host, port, user, password, dbname):
        if self.driver is None:
            raise RuntimeError("psycopg2 未安装，无法连接 PostgreSQL。")
        return self.driver.connect(
            host=host, port=port, user=user, password=password, dbname=dbname
        )


class MySQLBackend:
    """MySQL 后端（驱动可选，缺失时优雅降级）。"""
    placeholder = "%s"

    TYPE_MAP = {
        'int':      'INT',
        'str':      'VARCHAR(255)',
        'float':    'DOUBLE',
        'bool':     'TINYINT(1)',
        'text':     'TEXT',
        'datetime': 'DATETIME',
        'json':     'JSON',
        'blob':     'LONGBLOB',
    }

    AUTOINCREMENT = "AUTO_INCREMENT"

    def __init__(self):
        self.driver = None
        try:
            import pymysql
            self.driver = pymysql
        except ImportError:
            print("[db_orm] 警告：未安装 pymysql，MySQL 后端降级为 SQLite 语法。")

    def build_create_table(self, table_name, columns_sql):
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_sql)})"

    def connect(self, host, port, user, password, dbname):
        if self.driver is None:
            raise RuntimeError("pymysql 未安装，无法连接 MySQL。")
        return self.driver.connect(
            host=host, port=port, user=user, password=password, database=dbname,
            charset="utf8mb4",
        )


# ======================================================================
# Field：字段定义
# ======================================================================

class Field:
    """模型字段定义。

    支持类型：'int', 'str', 'float', 'bool', 'text', 'datetime', 'json', 'blob'
    """

    def __init__(self, type='str', primary_key=False, autoincrement=False,
                 default=None, unique=False, index=False, nullable=True,
                 foreign_key=None):
        self.type = type
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.default = default
        self.unique = unique
        self.index = index
        self.nullable = nullable
        self.foreign_key = foreign_key  # 格式："OtherTable.other_col"
        self.name = None  # 由元类赋值

    # ---------- SQL 生成 ----------
    def to_sql(self, backend=None):
        """生成字段定义 SQL 片段。"""
        backend = backend or SQLiteBackend
        col_type = backend.TYPE_MAP.get(self.type, 'TEXT')
        parts = [self.name, col_type]

        if self.primary_key and self.autoincrement:
            # 各数据库自增主键写法不同
            auto = getattr(backend, 'AUTOINCREMENT', 'AUTOINCREMENT')
            if backend is SQLiteBackend:
                parts = [self.name, 'INTEGER', 'PRIMARY KEY', auto]
            else:
                parts = [self.name, col_type, 'PRIMARY KEY']
        elif self.primary_key:
            parts.append("PRIMARY KEY")

        if self.unique:
            parts.append("UNIQUE")
        if not self.nullable and not self.primary_key:
            parts.append("NOT NULL")

        if self.foreign_key:
            parts.append(f"REFERENCES {self.foreign_key}")

        return " ".join(parts)

    # ---------- 类型转换 ----------
    def python_to_db(self, value):
        """Python 值 -> 数据库值。"""
        if value is None:
            return None
        if self.type == 'bool':
            return 1 if value else 0
        if self.type == 'datetime':
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            return value
        if self.type == 'json':
            if isinstance(value, str):
                return value
            return json.dumps(value, ensure_ascii=False)
        if self.type == 'blob' and isinstance(value, str):
            return value.encode('utf-8')
        return value

    def db_to_python(self, value):
        """数据库值 -> Python 值。"""
        if value is None:
            return None
        if self.type == 'bool':
            return bool(value)
        if self.type == 'int':
            return int(value)
        if self.type == 'float':
            return float(value)
        if self.type == 'datetime':
            if isinstance(value, str):
                try:
                    return datetime.datetime.fromisoformat(value)
                except ValueError:
                    return value
            return value
        if self.type == 'json':
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except (ValueError, TypeError):
                    return value
            return value
        if self.type == 'blob' and isinstance(value, bytes):
            return value
        return value

    def get_default(self):
        """获取默认值（可调用则调用）。"""
        if callable(self.default):
            return self.default()
        return self.default

    def __repr__(self):
        return f"<Field {self.name}:{self.type} pk={self.primary_key}>"


# ======================================================================
# 关系声明辅助函数
# ======================================================================

class Relationship:
    """关系描述符基类。"""
    def __init__(self, model_class, foreign_key=None):
        self.model_class = model_class
        self.foreign_key = foreign_key
        self.rel_name = None

    def resolve_foreign_key(self, owner_model):
        """自动推断外键列名。"""
        if self.foreign_key:
            return self.foreign_key
        # 默认：引用表名小写_id
        fk_name = owner_model.__tablename__.rstrip('s') + "_id"
        return fk_name


class HasMany(Relationship):
    """一对多：一个主记录拥有多条从记录。"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        fk = self.resolve_foreign_key(self.model_class) if False else None
        # belongs_to 的反向：从表中持有主表 id
        fk_col = self.foreign_key or (instance.__class__.__tablename__.rstrip('s') + "_id")
        return self.model_class.filter(**{fk_col: instance.pk})


class BelongsTo(Relationship):
    """多对一：从记录属于一条主记录。"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        fk_col = self.foreign_key or (self.model_class.__tablename__.rstrip('s') + "_id")
        fk_val = getattr(instance, fk_col, None)
        if fk_val is None:
            return None
        return self.model_class.get(fk_val)


class ManyToMany(Relationship):
    """多对多：通过中间表关联。"""
    def __init__(self, model_class, through_table=None, foreign_key=None):
        super().__init__(model_class, foreign_key)
        self.through_table = through_table

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        through = self.through_table or self._default_through(instance.__class__)
        other_table = self.model_class.__tablename__
        own_col = instance.__class__.__tablename__.rstrip('s') + "_id"
        other_col = other_table.rstrip('s') + "_id"
        conn = get_connection()
        sql = (
            f"SELECT {other_table}.* FROM {other_table} "
            f"JOIN {through} ON {other_table}.id = {through}.{other_col} "
            f"WHERE {through}.{own_col} = ?"
        )
        rows = conn.fetchall(sql, (instance.pk,))
        return [self.model_class(**{**r, **{k: self.model_class.__fields__[k].db_to_python(r[k])
                                            for k in r if k in self.model_class.__fields__}})
                for r in rows]

    def _default_through(self, owner):
        tables = sorted([owner.__tablename__, self.model_class.__tablename__])
        return "_".join(tables)


def has_many(model_class, foreign_key=None):
    """声明一对多关系。"""
    return HasMany(model_class, foreign_key)


def belongs_to(model_class, foreign_key=None):
    """声明多对一关系。"""
    return BelongsTo(model_class, foreign_key)


def many_to_many(model_class, through_table=None):
    """声明多对多关系。"""
    return ManyToMany(model_class, through_table)


# ======================================================================
# ModelMeta 元类：自动收集字段
# ======================================================================

class ModelMeta(type):
    """模型元类：收集 Field 与 Relationship 定义。"""

    def __new__(mcs, name, bases, namespace):
        # 跳过 Model 基类本身
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)

        fields = OrderedDict()
        relationships = OrderedDict()

        # 收集父类的字段（继承支持）
        for base in bases:
            if hasattr(base, '__fields__'):
                for k, v in base.__fields__.items():
                    fields[k] = v
            if hasattr(base, '__relationships__'):
                for k, v in base.__relationships__.items():
                    relationships[k] = v

        # 遍历命名空间，收集 Field / Relationship
        for attr_name, attr_value in list(namespace.items()):
            if isinstance(attr_value, Field):
                attr_value.name = attr_name
                fields[attr_name] = attr_value
            elif isinstance(attr_value, Relationship):
                attr_value.rel_name = attr_name
                relationships[attr_name] = attr_value

        namespace['__fields__'] = fields
        namespace['__relationships__'] = relationships

        # 默认表名：类名小写 + s
        if '__tablename__' not in namespace:
            namespace['__tablename__'] = name.lower() + 's'

        # 若没有任何字段声明 primary_key，自动注入 id 自增主键
        has_pk = any(f.primary_key for f in fields.values())
        if not has_pk:
            auto_id = Field(type='int', primary_key=True, autoincrement=True)
            auto_id.name = 'id'
            fields['id'] = auto_id
            fields.move_to_end('id', last=False)

        return super().__new__(mcs, name, bases, namespace)


# ======================================================================
# Model 基类
# ======================================================================

class Model(metaclass=ModelMeta):
    """所有 ORM 模型的基类。"""

    # 子类应声明的类属性（由元类填充）：
    #   __fields__       OrderedDict[str, Field]
    #   __tablename__     str
    #   __relationships__ OrderedDict[str, Relationship]

    def __init__(self, **kwargs):
        self._data = {}
        self._loaded = False
        # 填充字段值
        for field_name, field in self.__class__.__fields__.items():
            if field_name in kwargs:
                self._data[field_name] = kwargs[field_name]
            elif field.default is not None:
                self._data[field_name] = field.get_default()
            else:
                self._data[field_name] = None

    # ---------- 主键 ----------
    @classmethod
    def _pk_field(cls):
        for name, field in cls.__fields__.items():
            if field.primary_key:
                return name, field
        return None, None

    @property
    def pk(self):
        pk_name, _ = self._pk_field()
        return self._data.get(pk_name) if pk_name else None

    # ---------- 属性访问 ----------
    def __getattribute__(self, name):
        # 字段名优先从实例 _data 读取（否则会命中元类放在类上的 Field 对象）
        if not name.startswith('_') and name != 'pk':
            fields = type(self).__dict__.get('__fields__', {})
            if name in fields:
                data = super().__getattribute__('_data')
                raw = data.get(name)
                return fields[name].db_to_python(raw)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name.startswith('_') or name in ('pk',):
            super().__setattr__(name, value)
        elif name in self.__class__.__fields__:
            self._data[name] = value
        else:
            super().__setattr__(name, value)

    # ---------- 序列化 ----------
    def to_dict(self):
        """转为字典（Python 类型）。"""
        result = {}
        for name, field in self.__class__.__fields__.items():
            result[name] = field.db_to_python(self._data.get(name))
        return result

    @classmethod
    def from_dict(cls, data):
        """从字典创建实例。"""
        return cls(**{k: v for k, v in data.items() if k in cls.__fields__})

    # ---------- 持久化 ----------
    def save(self):
        """插入或更新当前实例。"""
        conn = get_connection()
        pk_name, pk_field = self._pk_field()

        # 收集要写入的字段
        insert_fields = []
        insert_values = []
        for name, field in self.__class__.__fields__.items():
            val = self._data.get(name)
            if val is None and field.default is not None and not field.primary_key:
                val = field.get_default()
                self._data[name] = val
            insert_fields.append(name)
            insert_values.append(field.python_to_db(val))

        if self.pk is None:
            # 插入
            placeholders = ", ".join(["?"] * len(insert_fields))
            col_names = ", ".join(insert_fields)
            sql = f"INSERT INTO {self.__class__.__tablename__} ({col_names}) VALUES ({placeholders})"
            cur = conn.execute(sql, insert_values)
            if pk_name and self._data.get(pk_name) is None:
                self._data[pk_name] = cur.lastrowid
        else:
            # 更新
            set_clause = ", ".join([f"{f} = ?" for f in insert_fields if f != pk_name])
            update_vals = [self.__class__.__fields__[f].python_to_db(self._data.get(f))
                           for f in insert_fields if f != pk_name]
            sql = (f"UPDATE {self.__class__.__tablename__} SET {set_clause} "
                   f"WHERE {pk_name} = ?")
            conn.execute(sql, update_vals + [self.pk])
        return self

    def delete(self):
        """删除当前记录。"""
        if self.pk is None:
            return
        conn = get_connection()
        pk_name, _ = self._pk_field()
        conn.execute(f"DELETE FROM {self.__class__.__tablename__} WHERE {pk_name} = ?",
                     (self.pk,))

    # ---------- 类方法 ----------
    @classmethod
    def create(cls, **kwargs):
        """新建并保存一条记录。"""
        instance = cls(**kwargs)
        instance.save()
        return instance

    @classmethod
    def all(cls):
        """获取所有记录。"""
        return cls.query().all()

    @classmethod
    def get(cls, pk):
        """按主键获取单条记录，不存在返回 None。"""
        pk_name, _ = cls._pk_field()
        row = get_connection().fetchone(
            f"SELECT * FROM {cls.__tablename__} WHERE {pk_name} = ?", (pk,))
        if row is None:
            return None
        return cls.from_dict(row)

    @classmethod
    def filter(cls, **kwargs):
        """构造查询。"""
        return cls.query().filter(**kwargs)

    @classmethod
    def count(cls):
        """统计记录数。"""
        row = get_connection().fetchone(
            f"SELECT COUNT(*) AS cnt FROM {cls.__tablename__}")
        return row['cnt'] if row else 0

    @classmethod
    def query(cls):
        """返回 Query 对象。"""
        return Query(cls)

    @classmethod
    def create_table(cls):
        """创建数据表。"""
        conn = get_connection()
        columns = []
        for name, field in cls.__fields__.items():
            columns.append(field.to_sql())
        sql = SQLiteBackend.build_create_table(SQLiteBackend, cls.__tablename__, columns)
        conn.execute(sql)
        # 创建索引
        for name, field in cls.__fields__.items():
            if field.index and not field.primary_key:
                idx_name = f"idx_{cls.__tablename__}_{name}"
                conn.execute(
                    f"CREATE INDEX IF NOT EXISTS {idx_name} ON {cls.__tablename__} ({name})")

    @classmethod
    def drop_table(cls):
        """删除数据表。"""
        get_connection().execute(f"DROP TABLE IF EXISTS {cls.__tablename__}")

    def __repr__(self):
        d = self.to_dict()
        return f"<{self.__class__.__name__} {d}>"


# ======================================================================
# Query 查询构建器
# ======================================================================

# 支持的操作符映射
_OPERATORS = {
    'gt':    '>',
    'gte':   '>=',
    'lt':    '<',
    'lte':   '<=',
    'eq':    '=',
    'ne':    '!=',
    'in':    'IN',
    'not_in':'NOT IN',
    'contains': 'LIKE',
    'startswith': 'LIKE',
    'endswith':   'LIKE',
    'isnull':     'IS',
    'notnull':    'IS NOT',
}


class Query:
    """链式查询构建器。"""

    def __init__(self, model_class):
        self.model = model_class
        self._conditions = []   # [(sql_fragment, param)]
        self._order_by = []     # [(field, direction)]
        self._limit = None
        self._offset = None
        self._group_by = None

    # ---------- 条件 ----------
    def filter(self, **kwargs):
        """添加等值/操作符条件，支持 field__op 语法。"""
        for key, value in kwargs.items():
            parts = key.split('__')
            field_name = parts[0]
            op = parts[1] if len(parts) > 1 else 'eq'

            if op not in _OPERATORS:
                raise ValueError(f"不支持的操作符: {op}")

            sql_op = _OPERATORS[op]

            if op == 'in':
                placeholders = ", ".join(["?"] * len(value))
                self._conditions.append(
                    (f"{field_name} IN ({placeholders})", list(value)))
            elif op == 'not_in':
                placeholders = ", ".join(["?"] * len(value))
                self._conditions.append(
                    (f"{field_name} NOT IN ({placeholders})", list(value)))
            elif op == 'contains':
                self._conditions.append(
                    (f"{field_name} LIKE ?", [f"%{value}%"]))
            elif op == 'startswith':
                self._conditions.append(
                    (f"{field_name} LIKE ?", [f"{value}%"]))
            elif op == 'endswith':
                self._conditions.append(
                    (f"{field_name} LIKE ?", [f"%{value}"]))
            elif op == 'isnull':
                self._conditions.append(
                    (f"{field_name} IS {'NULL' if value else 'NOT NULL'}", []))
            elif op == 'notnull':
                self._conditions.append((f"{field_name} IS NOT NULL", []))
            else:
                self._conditions.append((f"{field_name} {sql_op} ?", [value]))
        return self

    # ---------- 排序 ----------
    def order_by(self, field):
        """排序，'-field' 表示降序。"""
        if field.startswith('-'):
            self._order_by.append((field[1:], 'DESC'))
        else:
            self._order_by.append((field, 'ASC'))
        return self

    # ---------- 分页 ----------
    def limit(self, n):
        self._limit = n
        return self

    def offset(self, n):
        self._offset = n
        return self

    # ---------- SQL 生成 ----------
    def _to_sql(self):
        """生成 (sql_str, params_list)。"""
        table = self.model.__tablename__
        sql = f"SELECT * FROM {table}"
        params = []

        if self._conditions:
            clauses = []
            for frag, vals in self._conditions:
                clauses.append(frag)
                params.extend(vals)
            sql += " WHERE " + " AND ".join(clauses)

        if self._order_by:
            orders = [f"{f} {d}" for f, d in self._order_by]
            sql += " ORDER BY " + ", ".join(orders)

        if self._limit is not None:
            sql += f" LIMIT {int(self._limit)}"
        if self._offset is not None:
            sql += f" OFFSET {int(self._offset)}"

        return sql, params

    # ---------- 执行 ----------
    def _fetch_rows(self):
        sql, params = self._to_sql()
        conn = get_connection()
        return conn.fetchall(sql, params)

    def all(self):
        """执行查询，返回模型实例列表。"""
        rows = self._fetch_rows()
        return [self.model.from_dict(r) for r in rows]

    def first(self):
        """返回第一条记录或 None。"""
        old_limit = self._limit
        self._limit = 1
        rows = self._fetch_rows()
        self._limit = old_limit
        if not rows:
            return None
        return self.model.from_dict(rows[0])

    def get(self):
        """返回唯一一条记录，否则抛异常。"""
        results = self.limit(2).all()
        if len(results) == 0:
            raise self.model.DoesNotExist(f"{self.model.__name__} 不存在")
        if len(results) > 1:
            raise self.MultipleObjectsReturned("返回了多条记录")
        return results[0]

    def count(self):
        """统计满足条件的记录数。"""
        table = self.model.__tablename__
        sql = f"SELECT COUNT(*) AS cnt FROM {table}"
        params = []
        if self._conditions:
            clauses = []
            for frag, vals in self._conditions:
                clauses.append(frag)
                params.extend(vals)
            sql += " WHERE " + " AND ".join(clauses)
        row = get_connection().fetchone(sql, params)
        return row['cnt'] if row else 0

    def exists(self):
        """是否存在满足条件的记录。"""
        return self.count() > 0

    def update(self, **kwargs):
        """批量更新满足条件的记录。"""
        table = self.model.__tablename__
        set_clause = ", ".join([f"{k} = ?" for k in kwargs])
        params = list(kwargs.values())
        sql = f"UPDATE {table} SET {set_clause}"
        if self._conditions:
            clauses = []
            for frag, vals in self._conditions:
                clauses.append(frag)
                params.extend(vals)
            sql += " WHERE " + " AND ".join(clauses)
        return get_connection().execute(sql, params).rowcount

    def delete(self):
        """批量删除满足条件的记录。"""
        table = self.model.__tablename__
        sql = f"DELETE FROM {table}"
        params = []
        if self._conditions:
            clauses = []
            for frag, vals in self._conditions:
                clauses.append(frag)
                params.extend(vals)
            sql += " WHERE " + " AND ".join(clauses)
        return get_connection().execute(sql, params).rowcount

    # ---------- 异常类 ----------
    class DoesNotExist(Exception):
        """记录不存在。"""

    class MultipleObjectsReturned(Exception):
        """期望单条但返回多条。"""


# 给 Model 动态添加内部异常类引用
Model.DoesNotExist = Query.DoesNotExist


# ======================================================================
# Connection：数据库连接
# ======================================================================

# URL 解析正则
_URL_RE = re.compile(
    r'^(?P<scheme>\w+)://'
    r'(?:(?P<user>[^:@/]+)(?::(?P<password>[^@]*))?@)?'
    r'(?P<host>[^:/]+)?'
    r'(?::(?P<port>\d+))?'
    r'/(?P<path>.+)$'
)


class Connection:
    """数据库连接，支持多种后端。"""

    def __init__(self, db_url):
        self.db_url = db_url
        self.raw_conn = None
        self.backend = None
        self._parse_url(db_url)

    def _parse_url(self, url):
        """解析数据库 URL。"""
        m = _URL_RE.match(url)
        if not m:
            raise ValueError(f"无法解析数据库 URL: {url}")
        self.scheme = m.group('scheme')
        self.user = m.group('user')
        self.password = m.group('password')
        self.host = m.group('host')
        self.port = int(m.group('port')) if m.group('port') else None
        self.path = m.group('path')

    def connect(self):
        """建立连接。"""
        if self.scheme == 'sqlite':
            self.backend = SQLiteBackend()
            db_path = self.path
            if db_path != ':memory:':
                os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            self.raw_conn = sqlite3.connect(db_path)
            self.raw_conn.row_factory = sqlite3.Row
        elif self.scheme == 'postgresql':
            self.backend = PostgreSQLBackend()
            self.raw_conn = self.backend.connect(
                self.host, self.port or 5432, self.user, self.password, self.path)
        elif self.scheme == 'mysql':
            self.backend = MySQLBackend()
            self.raw_conn = self.backend.connect(
                self.host, self.port or 3306, self.user, self.password, self.path)
        else:
            raise ValueError(f"不支持的数据库类型: {self.scheme}")
        return self

    @classmethod
    def connect_from_url(cls, url):
        """便捷方法：连接并设为全局默认。"""
        conn = cls(url)
        conn.connect()
        set_connection(conn)
        return conn

    def execute(self, sql, params=None):
        """执行 SQL，返回游标。"""
        cur = self.raw_conn.execute(sql, params or [])
        self.raw_conn.commit()
        return cur

    def fetchone(self, sql, params=None):
        """执行查询，返回单行（dict-like）。"""
        cur = self.raw_conn.execute(sql, params or [])
        row = cur.fetchone()
        if row is None:
            return None
        if isinstance(row, sqlite3.Row):
            return dict(row)
        return row

    def fetchall(self, sql, params=None):
        """执行查询，返回所有行列表。"""
        cur = self.raw_conn.execute(sql, params or [])
        rows = cur.fetchall()
        result = []
        for row in rows:
            if isinstance(row, sqlite3.Row):
                result.append(dict(row))
            else:
                result.append(row)
        return result

    def close(self):
        """关闭连接。"""
        if self.raw_conn:
            self.raw_conn.close()
            self.raw_conn = None

    # 上下文管理器
    def __enter__(self):
        if self.raw_conn is None:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                self.raw_conn.commit()
            except Exception:
                pass
        else:
            try:
                self.raw_conn.rollback()
            except Exception:
                pass
        return False


# ======================================================================
# ConnectionPool：连接池
# ======================================================================

import threading


class ConnectionPool:
    """简单的数据库连接池。"""

    def __init__(self, db_url, min_connections=1, max_connections=5):
        self.db_url = db_url
        self.min_connections = min_connections
        self.max_connections = max_connections
        self._pool = []
        self._lock = threading.Lock()
        self._created = 0
        # 预创建最小连接
        for _ in range(min_connections):
            conn = Connection(db_url)
            conn.connect()
            self._pool.append(conn)
            self._created += 1

    def acquire(self):
        """获取一个连接。"""
        with self._lock:
            if self._pool:
                return self._pool.pop()
            if self._created < self.max_connections:
                conn = Connection(self.db_url)
                conn.connect()
                self._created += 1
                return conn
            raise RuntimeError("连接池已满，无法获取更多连接")

    def release(self, conn):
        """归还连接。"""
        with self._lock:
            if len(self._pool) < self.max_connections:
                self._pool.append(conn)
            else:
                conn.close()
                self._created -= 1

    class _ConnectionContext:
        """with 语句用的上下文包装。"""
        def __init__(self, pool):
            self.pool = pool
            self.conn = None

        def __enter__(self):
            self.conn = self.pool.acquire()
            return self.conn

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                try:
                    self.conn.raw_conn.commit()
                except Exception:
                    pass
            else:
                try:
                    self.conn.raw_conn.rollback()
                except Exception:
                    pass
            self.pool.release(self.conn)
            return False

    def connection(self):
        """返回上下文管理器。"""
        return self._ConnectionContext(self)

    def close_all(self):
        """关闭所有连接。"""
        with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()
            self._created = 0


# ======================================================================
# Transaction：事务
# ======================================================================

class Transaction:
    """事务管理器，支持上下文管理器和装饰器。"""

    def __init__(self, connection):
        self.connection = connection

    def begin(self):
        """开始事务（sqlite3 默认隐式开启，这里做标记）。"""
        self.connection.execute("BEGIN")
        return self

    def commit(self):
        """提交事务。"""
        self.connection.raw_conn.commit()

    def rollback(self):
        """回滚事务。"""
        self.connection.raw_conn.rollback()

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False


def transaction(conn=None):
    """事务装饰器。用法：@transaction(conn) 或 @transaction"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            connection = conn or get_connection()
            with Transaction(connection):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# ======================================================================
# MigrationManager：迁移版本管理
# ======================================================================

class MigrationManager:
    """管理迁移版本表。"""

    VERSION_TABLE = "_aurora_migrations"

    def __init__(self, connection):
        self.connection = connection
        self._ensure_table()

    def _ensure_table(self):
        """创建版本表（如果不存在）。"""
        self.connection.execute(
            f"CREATE TABLE IF NOT EXISTS {self.VERSION_TABLE} ("
            f"version TEXT PRIMARY KEY, applied_at TEXT)"
        )

    def get_current_version(self):
        """获取当前已应用的最新版本号。"""
        row = self.connection.fetchone(
            f"SELECT version FROM {self.VERSION_TABLE} ORDER BY version DESC LIMIT 1")
        return row['version'] if row else None

    def get_applied_versions(self):
        """获取所有已应用版本。"""
        rows = self.connection.fetchall(
            f"SELECT version, applied_at FROM {self.VERSION_TABLE} ORDER BY version")
        return [r['version'] for r in rows]

    def set_version(self, version):
        """记录一个版本已应用。"""
        now = datetime.datetime.now().isoformat()
        self.connection.execute(
            f"INSERT OR REPLACE INTO {self.VERSION_TABLE} (version, applied_at) VALUES (?, ?)",
            (version, now))

    def remove_version(self, version):
        """移除一个版本记录（回滚时用）。"""
        self.connection.execute(
            f"DELETE FROM {self.VERSION_TABLE} WHERE version = ?", (version,))


# ======================================================================
# Migration：迁移
# ======================================================================

class Migration:
    """数据库迁移管理。"""

    def __init__(self, connection, migrations_dir='migrations'):
        self.connection = connection
        self.migrations_dir = migrations_dir
        self.manager = MigrationManager(connection)
        os.makedirs(migrations_dir, exist_ok=True)

    def _migration_path(self, version, name):
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        return os.path.join(self.migrations_dir, f"{version}_{safe}.py")

    def _list_migration_files(self):
        """列出迁移目录中的迁移文件，按版本排序。"""
        files = []
        if not os.path.isdir(self.migrations_dir):
            return files
        for fname in os.listdir(self.migrations_dir):
            m = re.match(r'^(\d+)_(.+)\.py$', fname)
            if m:
                files.append((m.group(1), m.group(2), fname))
        files.sort(key=lambda x: int(x[0]))
        return files

    def create_migration(self, name, models=None):
        """生成迁移脚本文件。"""
        applied = self.manager.get_applied_versions()
        next_version = f"{len(applied) + 1:04d}"

        up_sql = []
        down_sql = []
        if models:
            for model in models:
                up_sql.append(f"-- 创建表 {model.__tablename__}")
                up_sql.append(model.create_table.__func__.__wrapped__ if hasattr(model.create_table, '__wrapped__') else
                              f"-- 请手动编写 {model.__tablename__} 的建表 SQL")
                down_sql.append(f"DROP TABLE IF EXISTS {model.__tablename__};")

        content = f'''# 自动生成的迁移文件
# 版本: {next_version}
# 名称: {name}

def up(conn):
    """向上迁移"""
{chr(10).join('    ' + line for line in up_sql) if up_sql else '    pass'}


def down(conn):
    """向下迁移（回滚）"""
{chr(10).join('    ' + line for line in down_sql) if down_sql else '    pass'}
'''
        path = self._migration_path(next_version, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def generate_from_models(self, models):
        """根据模型定义自动生成建表迁移。"""
        return self.create_migration("auto_create_tables", models)

    def migrate(self, target=None):
        """执行待应用的迁移。"""
        files = self._list_migration_files()
        applied = set(self.manager.get_applied_versions())

        for version, name, fname in files:
            if target and version > target:
                break
            if version in applied:
                continue
            path = os.path.join(self.migrations_dir, fname)
            module = self._load_module(path)
            if hasattr(module, 'up'):
                module.up(self.connection)
            self.manager.set_version(version)
            print(f"[migration] 已应用 {version}_{name}")

    def rollback(self, steps=1):
        """回滚指定步数的迁移。"""
        applied = self.manager.get_applied_versions()
        to_rollback = applied[-steps:] if steps else applied[::-1]

        files = {v: n for v, n, _ in self._list_migration_files()}

        for version in reversed(to_rollback):
            if version not in files:
                print(f"[migration] 警告：找不到版本 {version} 的文件，跳过")
                continue
            path = self._migration_path(version, files[version])
            module = self._load_module(path)
            if hasattr(module, 'down'):
                module.down(self.connection)
            self.manager.remove_version(version)
            print(f"[migration] 已回滚 {version}_{files[version]}")

    def status(self):
        """返回已执行迁移列表。"""
        return self.manager.get_applied_versions()

    def _load_module(self, path):
        """动态加载迁移模块。"""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            f"migration_{os.path.basename(path)}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


# ======================================================================
# Seed：数据填充
# ======================================================================

# ---------- 内置假数据生成器 ----------

_FIRST_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank',
                'Grace', 'Henry', 'Ivy', 'Jack', 'Karen', 'Leo']
_LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
               'Miller', 'Davis', 'Wilson', 'Moore']
_WORDS = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur',
          'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor']


def fake_name():
    """生成假人名。"""
    return f"{random.choice(_FIRST_NAMES)} {random.choice(_LAST_NAMES)}"


def fake_email():
    """生成假邮箱。"""
    name = random.choice(_FIRST_NAMES).lower()
    domain = random.choice(['example.com', 'test.org', 'demo.net'])
    return f"{name}{random.randint(10, 99)}@{domain}"


def fake_text(words=8):
    """生成假文本。"""
    return ' '.join(random.choice(_WORDS) for _ in range(words))


def fake_number(start=1, end=100):
    """生成假数字。"""
    return random.randint(start, end)


class Seed:
    """数据填充工具。"""

    def __init__(self, connection=None):
        self.connection = connection or get_connection()
        self.generators = {
            'name': fake_name,
            'email': fake_email,
            'text': fake_text,
            'number': fake_number,
        }

    def register_generator(self, name, func):
        """注册自定义假数据生成器。"""
        self.generators[name] = func

    def run(self, seeders_list):
        """执行填充任务列表。

        seeders_list: [(model_class, count, defaults_dict), ...]
        """
        results = []
        for item in seeders_list:
            if len(item) == 2:
                model_class, count = item
                defaults = {}
            else:
                model_class, count, defaults = item
            created = self.factory(model_class, count, **defaults)
            results.append((model_class.__name__, len(created)))
        return results

    def factory(self, model_class, count, **defaults):
        """批量生成测试数据并保存。"""
        created = []
        # 记录 unique 字段已用过的值，避免唯一约束冲突
        used_unique = {}
        for i in range(count):
            data = self._generate_data(model_class, defaults)
            # 对 unique 字段追加序号保证唯一
            for name, field in model_class.__fields__.items():
                if field.unique and name in data and data[name] is not None:
                    base = str(data[name])
                    if base in used_unique.setdefault(name, set()):
                        data[name] = f"{base}_{i}"
                    used_unique[name].add(data[name])
            instance = model_class.create(**data)
            created.append(instance)
        return created

    def _generate_data(self, model_class, defaults):
        """根据字段类型自动生成数据。"""
        data = dict(defaults)
        for name, field in model_class.__fields__.items():
            if name in data:
                continue
            if field.primary_key and field.autoincrement:
                continue
            if field.default is not None:
                data[name] = field.get_default()
                continue
            data[name] = self._value_for_field(field)
        return data

    def _value_for_field(self, field):
        """根据字段类型生成随机值。"""
        t = field.type
        if t == 'int':
            return fake_number()
        if t == 'float':
            return round(random.uniform(0, 1000), 2)
        if t == 'bool':
            return random.choice([True, False])
        if t == 'str':
            if 'email' in (field.name or ''):
                return fake_email()
            if 'name' in (field.name or ''):
                return fake_name()
            return fake_text(3)
        if t == 'text':
            return fake_text(20)
        if t == 'datetime':
            return datetime.datetime.now() - datetime.timedelta(days=fake_number(0, 365))
        if t == 'json':
            return {"key": fake_text(2), "value": fake_number()}
        if t == 'blob':
            return fake_text(10).encode('utf-8')
        return None


# ======================================================================
# CLI 注册
# ======================================================================

def register_cli(subparsers):
    """向 Aurora CLI 注册 db 子命令。"""
    db_parser = subparsers.add_parser('db', help='数据库管理命令')
    db_sub = db_parser.add_subparsers(dest='db_command')

    # migrate
    db_sub.add_parser('migrate', help='执行数据库迁移')

    # rollback
    rb = db_sub.add_parser('rollback', help='回滚迁移')
    rb.add_argument('--steps', type=int, default=1, help='回滚步数')

    # seed
    db_sub.add_parser('seed', help='执行数据填充')

    # generate model
    gen = db_sub.add_parser('generate', help='生成模型代码')
    gen_sub = gen.add_subparsers(dest='generate_command')
    model_gen = gen_sub.add_parser('model', help='生成模型')
    model_gen.add_argument('name', help='模型名')
    model_gen.add_argument('fields', nargs='*', help='字段定义 field:type')

    return db_parser


def _generate_model_code(name, fields):
    """根据字段定义生成模型代码字符串。"""
    lines = [
        f"class {name}(Model):",
        f'    """{name} 模型（自动生成）"""',
    ]
    for fdef in fields:
        if ':' in fdef:
            fname, ftype = fdef.split(':', 1)
        else:
            fname, ftype = fdef, 'str'
        if fname == 'id':
            lines.append(f"    {fname} = Field(type='{ftype}', primary_key=True, autoincrement=True)")
        else:
            lines.append(f"    {fname} = Field(type='{ftype}')")
    return "\n".join(lines)


# ======================================================================
# STDLIB 注册
# ======================================================================

STDLIB_REGISTRATION = {
    'std.db': {
        'Model': Model,
        'Field': Field,
        'Query': Query,
        'Connection': Connection,
        'ConnectionPool': ConnectionPool,
        'Transaction': Transaction,
        'Migration': Migration,
        'Seed': Seed,
        'has_many': has_many,
        'belongs_to': belongs_to,
        'many_to_many': many_to_many,
    }
}
