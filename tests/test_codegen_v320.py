"""
Aurora v3.2.0 代码生成器与脚手架工具测试

覆盖:
  - 各类项目脚手架(fullstack / cli / tui / microservice / webapp)
  - 代码生成器(controller / model / component / service)
  - OpenAPI 文档生成
  - 文件已存在时的覆盖/跳过逻辑

全部使用 tempfile.TemporaryDirectory 作为目标目录。
"""
import json
import os
import tempfile
import unittest

from aurora import codegen as cg


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestScaffoldFullstack(unittest.TestCase):
    """scaffold_fullstack 应生成完整目录结构。"""

    def test_fullstack_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = cg.scaffold_fullstack("myapp", target_dir=tmp)
            self.assertEqual(root, os.path.join(tmp, "myapp"))

            # 目录结构
            for d in ["src", "src/controllers", "src/models", "src/components",
                      "static", "migrations", "tests", "config"]:
                self.assertTrue(os.path.isdir(os.path.join(root, d)),
                                "缺少目录 %s" % d)

            # 关键文件
            expected_files = [
                "aurora.toml",
                "src/main.aur",
                "src/models/user.aur",
                "src/controllers/user_controller.aur",
                "src/components/app.aur",
                "config/dev.toml",
                "config/prod.toml",
                "README.md",
            ]
            for rel in expected_files:
                self.assertTrue(os.path.isfile(os.path.join(root, rel)),
                                "缺少文件 %s" % rel)

            # 入口文件内容:创建 App 并启动
            main_src = _read(os.path.join(root, "src/main.aur"))
            self.assertIn("App(", main_src)
            self.assertIn("app.run", main_src)
            self.assertIn("std.web", main_src)

            # 模型文件:使用 db.Model
            model_src = _read(os.path.join(root, "src/models/user.aur"))
            self.assertIn("struct User extends db.Model", model_src)


class TestScaffoldCli(unittest.TestCase):
    """scaffold_cli 应生成基于 std.cli 的 CLI 项目。"""

    def test_cli_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = cg.scaffold_cli("mycli", target_dir=tmp)
            main_path = os.path.join(root, "src/main.aur")
            self.assertTrue(os.path.isfile(main_path))
            self.assertTrue(os.path.isfile(os.path.join(root, "aurora.toml")))

            src = _read(main_path)
            # 演示彩色输出 / 表格 / 确认 / 选择
            self.assertIn("std.cli", src)
            self.assertIn("cli.color.fg", src)
            self.assertIn("cli.Table", src)
            self.assertIn("cli.confirm", src)


class TestScaffoldTuiAndMicroservice(unittest.TestCase):
    """scaffold_tui 与 scaffold_microservice 的基本产物校验。"""

    def test_tui_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = cg.scaffold_tui("myeditor", target_dir=tmp)
            src = _read(os.path.join(root, "src/main.aur"))
            self.assertIn("tui.App", src)
            self.assertIn("VBox", src)
            self.assertIn("Input", src)

    def test_microservice_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = cg.scaffold_microservice("svc", target_dir=tmp)
            self.assertTrue(os.path.isfile(os.path.join(root, "Dockerfile")))
            self.assertTrue(os.path.isfile(os.path.join(root, "config/prod.toml")))
            src = _read(os.path.join(root, "src/main.aur"))
            self.assertIn("/health", src)


class TestGenerateController(unittest.TestCase):
    """generate_controller 应生成包含 CRUD 动作的控制器文件。"""

    def test_default_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = cg.generate_controller("user", target_dir=tmp)
            self.assertTrue(os.path.isfile(path))
            src = _read(path)
            for act in ["index", "show", "create", "update", "destroy"]:
                self.assertIn("fn %s(" % act, src)

    def test_filtered_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = cg.generate_controller("post", actions=["index", "show"],
                                          target_dir=tmp)
            src = _read(path)
            self.assertIn("fn index(", src)
            self.assertIn("fn show(", src)
            self.assertNotIn("fn create(", src)


class TestGenerateModel(unittest.TestCase):
    """generate_model 应生成模型文件与迁移文件。"""

    def test_model_and_migration(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_dir = os.path.join(tmp, "models")
            # 迁移文件默认写到 ./migrations,这里把工作目录指到 tmp 下
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                path = cg.generate_model(
                    "User",
                    fields=[("name", "str"), ("age", "int"),
                            ("email", "str", {"unique": True})],
                    target_dir=model_dir,
                )
            finally:
                os.chdir(old_cwd)

            self.assertTrue(os.path.isfile(path))
            src = _read(path)
            self.assertIn("struct User extends db.Model", src)
            self.assertIn("name: str", src)
            self.assertIn("age: int", src)

            # 迁移文件应生成到 migrations/
            mig = os.path.join(tmp, "migrations", "001_create_user.aur")
            self.assertTrue(os.path.isfile(mig))
            mig_src = _read(mig)
            self.assertIn("table \"user\"", mig_src)


class TestGenerateComponent(unittest.TestCase):
    """generate_component 应生成带生命周期的前端组件。"""

    def test_component(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = cg.generate_component(
                "App", props=[("title", "str"), ("items", "list")],
                target_dir=tmp,
            )
            self.assertTrue(os.path.isfile(path))
            src = _read(path)
            self.assertIn("struct App extends Component", src)
            self.assertIn("title: str", src)
            self.assertIn("items: list", src)
            # 生命周期
            for hook in ["mount", "render", "unmount"]:
                self.assertIn(hook, src)


class TestGenerateService(unittest.TestCase):
    """generate_service 应生成服务层方法骨架。"""

    def test_service(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = cg.generate_service("Auth", methods=["login", "logout"],
                                       target_dir=tmp)
            self.assertTrue(os.path.isfile(path))
            src = _read(path)
            self.assertIn("fn login(", src)
            self.assertIn("fn logout(", src)

    def test_default_methods(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = cg.generate_service("Order", target_dir=tmp)
            src = _read(path)
            for m in ["create", "list", "get", "update", "delete"]:
                self.assertIn("fn %s(" % m, src)


class TestGenerateOpenAPI(unittest.TestCase):
    """generate_openapi 应输出合法的 OpenAPI 3.0 JSON。"""

    def test_openapi_doc(self):
        routes = [
            ("get", "/users"),
            {"path": "/users/{id}", "method": "get",
             "query_params": ["detail"]},
            {"path": "/users", "method": "post",
             "body": {"type": "object"}},
        ]
        out = cg.generate_openapi(routes, title="测试 API", version="0.1.0")
        doc = json.loads(out)  # 必须是合法 JSON

        self.assertEqual(doc["openapi"], "3.0.0")
        self.assertEqual(doc["info"]["title"], "测试 API")
        self.assertIn("/users", doc["paths"])
        self.assertIn("/users/{id}", doc["paths"])

        # 路径参数 {id} 应被识别为 path 段参数
        get_by_id = doc["paths"]["/users/{id}"]["get"]
        params = get_by_id.get("parameters", [])
        id_param = [p for p in params if p["name"] == "id" and p["in"] == "path"]
        self.assertTrue(id_param, "应包含路径参数 id")
        self.assertTrue(id_param[0]["required"])

        # 查询参数 detail
        q = [p for p in params if p["name"] == "detail" and p["in"] == "query"]
        self.assertTrue(q)

        # 请求体
        self.assertIn("requestBody", doc["paths"]["/users"]["post"])


class TestOverwriteBehavior(unittest.TestCase):
    """文件已存在时:overwrite=False 应跳过,True 应覆盖。"""

    def test_existing_file_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = cg.generate_controller("user", target_dir=tmp)
            original = _read(path)

            # 写入一个标记内容
            with open(path, "w", encoding="utf-8") as f:
                f.write("// MARKER")

            # overwrite=False:应跳过,文件保持 MARKER
            written = cg._cg_write(path, "// NEW", overwrite=False)
            self.assertFalse(written)
            self.assertEqual(_read(path), "// MARKER")

            # overwrite=True:应覆盖
            written = cg._cg_write(path, "// NEW", overwrite=True)
            self.assertTrue(written)
            self.assertEqual(_read(path), "// NEW")

            # 生成器本身:再次生成时 overwrite=False 不覆盖
            self.assertNotEqual(_read(path), original)


class TestDeployStatic(unittest.TestCase):
    """deploy_static 应把 static/ 导出到 dist/ 并生成清单。"""

    def test_deploy_static(self):
        with tempfile.TemporaryDirectory() as tmp:
            # 造一个带 static 目录的项目
            static_dir = os.path.join(tmp, "static")
            os.makedirs(static_dir)
            with open(os.path.join(static_dir, "app.js"), "w", encoding="utf-8") as f:
                f.write("console.log('hi')")

            out = cg.deploy_static(tmp, os.path.join(tmp, "dist"))
            self.assertTrue(os.path.isfile(os.path.join(out, "app.js")))
            manifest = json.loads(_read(os.path.join(out, "manifest.json")))
            self.assertIn("app.js", manifest["files"])


if __name__ == "__main__":
    unittest.main()
