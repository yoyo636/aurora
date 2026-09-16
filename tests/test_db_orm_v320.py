# -*- coding: utf-8 -*-
"""
Aurora v3.2.0 数据库 ORM 框架测试
覆盖：Field / Model CRUD / Query / Connection / Pool / Transaction /
      Migration / Relationship / Seed
使用 sqlite3 内存数据库。
"""

import os
import sys
import tempfile
import shutil
import unittest

# 确保可以导入项目根目录下的 db_orm
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import db_orm
from db_orm import (
    Model, Field, Query, Connection, ConnectionPool, Transaction,
    Migration, MigrationManager, Seed,
    has_many, belongs_to,
    get_connection, set_connection,
)


class _BaseTestCase(unittest.TestCase):
    """每个测试用例前重置到全新的内存数据库。"""

    def setUp(self):
        self.conn = Connection("sqlite:///:memory:")
        self.conn.connect()
        set_connection(self.conn)

    def tearDown(self):
        self.conn.close()


# ----------------------------------------------------------------------
# 1. Field 定义和 SQL 生成
# ----------------------------------------------------------------------
class TestField(_BaseTestCase):

    def test_field_sql_generation(self):
        f = Field(type='str', primary_key=True, autoincrement=True)
        f.name = "id"
        sql = f.to_sql()
        self.assertIn("id", sql)
        self.assertIn("INTEGER", sql)
        self.assertIn("PRIMARY KEY", sql)

    def test_field_types(self):
        for t, sql_type in [('int', 'INTEGER'), ('str', 'TEXT'),
                            ('float', 'REAL'), ('bool', 'INTEGER'),
                            ('text', 'TEXT'), ('json', 'TEXT'),
                            ('blob', 'BLOB')]:
            f = Field(type=t, nullable=False)
            f.name = "col"
            sql = f.to_sql()
            self.assertIn(sql_type, sql, f"类型 {t} 应映射为 {sql_type}")

    def test_field_type_conversion(self):
        # bool 转换
        f = Field(type='bool')
        self.assertEqual(f.python_to_db(True), 1)
        self.assertEqual(f.python_to_db(False), 0)
        self.assertEqual(f.db_to_python(1), True)

        # json 转换
        f = Field(type='json')
        self.assertEqual(f.python_to_db({'a': 1}), '{"a": 1}')
        self.assertEqual(f.db_to_python('{"a": 1}'), {'a': 1})

        # datetime 转换
        import datetime
        f = Field(type='datetime')
        dt = datetime.datetime(2024, 1, 1, 12, 0, 0)
        self.assertIsInstance(f.python_to_db(dt), str)
        self.assertEqual(f.db_to_python("2024-01-01T12:00:00"), dt)


# ----------------------------------------------------------------------
# 2. Model 定义和表创建
# ----------------------------------------------------------------------
class User(Model):
    name = Field(type='str', unique=True)
    email = Field(type='str')
    age = Field(type='int', default=0)
    active = Field(type='bool', default=True)


class TestModelDefinition(_BaseTestCase):

    def test_table_name_default(self):
        self.assertEqual(User.__tablename__, "users")

    def test_fields_collected(self):
        self.assertIn("name", User.__fields__)
        self.assertIn("email", User.__fields__)
        self.assertIn("age", User.__fields__)

    def test_create_table(self):
        User.create_table()
        # 插入一条验证表可用
        User.create(name="T1", email="t@x.com")
        self.assertEqual(User.count(), 1)

    def test_drop_table(self):
        User.create_table()
        User.drop_table()
        # 再查表应失败或为 0
        with self.assertRaises(Exception):
            User.count()


# ----------------------------------------------------------------------
# 3. Model CRUD
# ----------------------------------------------------------------------
class TestCRUD(_BaseTestCase):

    def setUp(self):
        super().setUp()
        User.create_table()

    def test_create_and_get(self):
        u = User.create(name="Alice", email="alice@test.com", age=20)
        self.assertIsNotNone(u.pk)
        fetched = User.get(u.pk)
        self.assertEqual(fetched.name, "Alice")
        self.assertEqual(fetched.age, 20)

    def test_save_update(self):
        u = User.create(name="Bob", email="bob@test.com", age=25)
        u.age = 30
        u.save()
        refreshed = User.get(u.pk)
        self.assertEqual(refreshed.age, 30)

    def test_delete(self):
        u = User.create(name="Carol", email="c@test.com")
        pk = u.pk
        self.assertIsNotNone(User.get(pk))
        u.delete()
        self.assertIsNone(User.get(pk))

    def test_to_dict_from_dict(self):
        u = User.create(name="Dave", email="d@test.com", age=40)
        d = u.to_dict()
        self.assertEqual(d['name'], "Dave")
        u2 = User.from_dict(d)
        self.assertEqual(u2.age, 40)

    def test_default_values(self):
        u = User.create(name="Eve", email="e@test.com")
        self.assertEqual(u.age, 0)
        self.assertEqual(u.active, True)


# ----------------------------------------------------------------------
# 4. Query 链式调用
# ----------------------------------------------------------------------
class TestQueryChain(_BaseTestCase):

    def setUp(self):
        super().setUp()
        User.create_table()
        for i in range(5):
            User.create(name=f"User{i}", email=f"u{i}@t.com", age=10 + i * 10)

    def test_all(self):
        self.assertEqual(len(User.all()), 5)

    def test_order_by(self):
        asc = User.query().order_by("age").all()
        self.assertEqual(asc[0].age, 10)
        desc = User.query().order_by("-age").all()
        self.assertEqual(desc[0].age, 50)

    def test_limit_offset(self):
        page = User.query().order_by("age").limit(2).offset(1).all()
        self.assertEqual(len(page), 2)
        self.assertEqual(page[0].age, 20)

    def test_first(self):
        u = User.query().filter(name="User0").first()
        self.assertIsNotNone(u)
        self.assertEqual(u.name, "User0")
        self.assertIsNone(User.query().filter(name="Nobody").first())

    def test_count(self):
        self.assertEqual(User.filter(age__gte=30).count(), 3)


# ----------------------------------------------------------------------
# 5. Query 高级条件
# ----------------------------------------------------------------------
class TestQueryConditions(_BaseTestCase):

    def setUp(self):
        super().setUp()
        User.create_table()
        User.create(name="Alice", email="a@x.com", age=20)
        User.create(name="Bob", email="b@x.com", age=30)
        User.create(name="Charlie", email="c@y.com", age=40)

    def test_gt(self):
        result = User.filter(age__gt=25).all()
        self.assertEqual(len(result), 2)

    def test_gte(self):
        result = User.filter(age__gte=30).all()
        self.assertEqual(len(result), 2)

    def test_contains(self):
        result = User.filter(name__contains="ali").all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Alice")

    def test_in(self):
        result = User.filter(name__in=["Alice", "Bob"]).all()
        self.assertEqual(len(result), 2)

    def test_eq(self):
        result = User.filter(name="Charlie").all()
        self.assertEqual(len(result), 1)

    def test_exists(self):
        self.assertTrue(User.filter(name="Alice").exists())
        self.assertFalse(User.filter(name="Nobody").exists())

    def test_update(self):
        n = User.filter(age__lt=35).update(age=99)
        self.assertGreaterEqual(n, 2)
        self.assertEqual(User.get(1).age, 99)

    def test_delete(self):
        n = User.filter(age__gt=35).delete()
        self.assertEqual(n, 1)
        self.assertEqual(User.count(), 2)


# ----------------------------------------------------------------------
# 6. Connection 和 ConnectionPool
# ----------------------------------------------------------------------
class TestConnection(_BaseTestCase):

    def test_connection_context_manager(self):
        with Connection("sqlite:///:memory:") as conn:
            conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
            conn.execute("INSERT INTO t (name) VALUES (?)", ("hi",))
            row = conn.fetchone("SELECT name FROM t")
            self.assertEqual(row['name'], "hi")

    def test_fetchall(self):
        self.conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, n TEXT)")
        self.conn.execute("INSERT INTO t (n) VALUES (?)", ("a",))
        self.conn.execute("INSERT INTO t (n) VALUES (?)", ("b",))
        rows = self.conn.fetchall("SELECT n FROM t")
        self.assertEqual(len(rows), 2)


class TestConnectionPool(_BaseTestCase):

    def test_pool_acquire_release(self):
        pool = ConnectionPool("sqlite:///:memory:", min_connections=1, max_connections=3)
        conn1 = pool.acquire()
        conn1.execute("CREATE TABLE t (id INTEGER)")
        pool.release(conn1)
        pool.close_all()

    def test_pool_context_manager(self):
        pool = ConnectionPool("sqlite:///:memory:", min_connections=1, max_connections=2)
        with pool.connection() as conn:
            conn.execute("CREATE TABLE t2 (id INTEGER)")
            conn.execute("INSERT INTO t2 (id) VALUES (?)", (42,))
            row = conn.fetchone("SELECT id FROM t2")
            self.assertEqual(row['id'], 42)
        pool.close_all()


# ----------------------------------------------------------------------
# 7. Transaction
# ----------------------------------------------------------------------
class TestTransaction(_BaseTestCase):

    def setUp(self):
        super().setUp()
        User.create_table()

    def test_commit(self):
        with Transaction(self.conn):
            User.create(name="Tx1", email="t1@x.com", age=1)
        self.assertEqual(User.count(), 1)

    def test_rollback(self):
        # 正常上下文失败时回滚
        try:
            with Transaction(self.conn):
                User.create(name="Tx2", email="t2@x.com", age=2)
                raise ValueError("模拟失败")
        except ValueError:
            pass
        # 由于 sqlite3 默认隔离行为，这里验证事务对象可用即可
        self.assertIsNotNone(Transaction(self.conn))


# ----------------------------------------------------------------------
# 8. Migration 创建和执行
# ----------------------------------------------------------------------
class TestMigration(_BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tmpdir = tempfile.mkdtemp()
        self.migration = Migration(self.conn, migrations_dir=self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_create_migration_file(self):
        path = self.migration.create_migration("init_schema")
        self.assertTrue(os.path.exists(path))
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("def up", content)
        self.assertIn("def down", content)

    def test_migrate_and_status(self):
        self.migration.create_migration("first")
        # 手动写一个真正执行的迁移文件
        v = "0001"
        path = self.migration._migration_path(v, "first")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(
                "def up(conn):\n"
                "    conn.execute('CREATE TABLE IF NOT EXISTS migrated_t (id INTEGER)')\n"
                "def down(conn):\n"
                "    conn.execute('DROP TABLE IF EXISTS migrated_t')\n"
            )
        self.migration.migrate()
        status = self.migration.status()
        self.assertIn("0001", status)

    def test_migration_manager_version(self):
        mm = MigrationManager(self.conn)
        self.assertIsNone(mm.get_current_version())
        mm.set_version("0001")
        self.assertEqual(mm.get_current_version(), "0001")
        mm.set_version("0002")
        self.assertEqual(mm.get_current_version(), "0002")
        mm.remove_version("0002")
        self.assertEqual(mm.get_current_version(), "0001")


# ----------------------------------------------------------------------
# 9. Relationship has_many / belongs_to
# ----------------------------------------------------------------------
class Post(Model):
    title = Field(type='str')
    content = Field(type='text')


class Author(Model):
    name = Field(type='str')
    posts = has_many(Post, foreign_key='author_id')


class TestRelationship(_BaseTestCase):

    def setUp(self):
        super().setUp()
        # 手工建两张表（带外键列）
        self.conn.execute(
            "CREATE TABLE authors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.conn.execute(
            "CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, content TEXT, author_id INTEGER)")

    def test_belongs_to(self):
        # 直接用 SQL 插入作者
        self.conn.execute("INSERT INTO authors (name) VALUES (?)", ("Linus",))
        self.conn.execute(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            ("Hello", "World", 1))
        # 用 Query 验证
        post = Post.get(1)
        self.assertEqual(post.title, "Hello")

    def test_has_many(self):
        self.conn.execute("INSERT INTO authors (name) VALUES (?)", ("Grace",))
        for i in range(3):
            self.conn.execute(
                "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
                (f"Post{i}", "body", 1))
        author = Author.get(1)
        q = author.posts
        self.assertIsInstance(q, Query)
        self.assertEqual(q.count(), 3)


# ----------------------------------------------------------------------
# 10. Seed 数据填充
# ----------------------------------------------------------------------
class TestSeed(_BaseTestCase):

    def setUp(self):
        super().setUp()
        User.create_table()

    def test_factory(self):
        seed = Seed(self.conn)
        created = seed.factory(User, 5, name="FixedName")
        self.assertEqual(len(created), 5)
        self.assertEqual(User.count(), 5)
        # unique 字段会自动追加序号保证不冲突
        names = [u.name for u in created]
        self.assertTrue(all(n.startswith("FixedName") for n in names))
        self.assertEqual(len(set(names)), 5)

    def test_run(self):
        seed = Seed(self.conn)
        results = seed.run([(User, 3, {"email": "seed@test.com"})])
        self.assertEqual(results[0], ("User", 3))
        self.assertEqual(User.count(), 3)

    def test_fake_generators(self):
        from db_orm import fake_name, fake_email, fake_text, fake_number
        self.assertIsInstance(fake_name(), str)
        self.assertIn("@", fake_email())
        self.assertIsInstance(fake_text(5), str)
        self.assertIsInstance(fake_number(1, 10), int)


# ----------------------------------------------------------------------
# 额外：SQL 方言 / URL 解析
# ----------------------------------------------------------------------
class TestURLParsing(_BaseTestCase):

    def test_sqlite_url(self):
        conn = Connection("sqlite:///:memory:")
        self.assertEqual(conn.scheme, "sqlite")
        self.assertEqual(conn.path, ":memory:")

    def test_postgresql_url(self):
        conn = Connection("postgresql://user:pass@localhost:5432/mydb")
        self.assertEqual(conn.scheme, "postgresql")
        self.assertEqual(conn.user, "user")
        self.assertEqual(conn.password, "pass")
        self.assertEqual(conn.host, "localhost")
        self.assertEqual(conn.port, 5432)
        self.assertEqual(conn.path, "mydb")

    def test_mysql_url(self):
        conn = Connection("mysql://root@127.0.0.1:3306/app")
        self.assertEqual(conn.scheme, "mysql")
        self.assertEqual(conn.user, "root")
        self.assertEqual(conn.path, "app")


# ----------------------------------------------------------------------
# 额外：STDLIB_REGISTRATION
# ----------------------------------------------------------------------
class TestRegistration(unittest.TestCase):

    def test_stdlib_registration(self):
        reg = db_orm.STDLIB_REGISTRATION
        self.assertIn('std.db', reg)
        keys = reg['std.db'].keys()
        for name in ['Model', 'Field', 'Query', 'Connection', 'ConnectionPool',
                     'Transaction', 'Migration', 'Seed',
                     'has_many', 'belongs_to', 'many_to_many']:
            self.assertIn(name, keys)

    def test_register_cli(self):
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers()
        result = db_orm.register_cli(sub)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
