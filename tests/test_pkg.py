"""Aurora 包管理器测试:init / add / remove / install / list / 版本解析 / 锁文件"""

import os
import json
import shutil
import tempfile
import unittest

from aurora.pkg import (
    PackageManager, LocalRegistry,
    satisfies, pick_version, parse_version,
)


class TestVersionResolve(unittest.TestCase):
    def test_parse_version(self):
        self.assertEqual(parse_version('1.2.3'), (1, 2, 3))
        self.assertEqual(parse_version('v2.10.0'), (2, 10, 0))
        self.assertIsNone(parse_version('abc'))

    def test_caret(self):
        self.assertTrue(satisfies('1.2.9', '^1.0.0'))
        self.assertTrue(satisfies('1.99.0', '^1.2.3'))
        self.assertFalse(satisfies('2.0.0', '^1.2.3'))
        # 0.x:caret 只在同一 minor 内升级
        self.assertTrue(satisfies('0.2.5', '^0.2.0'))
        self.assertFalse(satisfies('0.3.0', '^0.2.0'))

    def test_tilde(self):
        self.assertTrue(satisfies('1.2.9', '~1.2.0'))
        self.assertFalse(satisfies('1.3.0', '~1.2.0'))
        self.assertTrue(satisfies('1.2.3', '~1.2.3'))

    def test_exact_and_operators(self):
        self.assertTrue(satisfies('1.2.3', '1.2.3'))
        self.assertFalse(satisfies('1.2.4', '1.2.3'))
        self.assertTrue(satisfies('1.2.3', '>=1.2.0'))
        self.assertFalse(satisfies('1.1.0', '>=1.2.0'))
        self.assertTrue(satisfies('1.2.3', '*'))

    def test_pick_version(self):
        avail = ['1.0.0', '1.0.5', '1.1.0', '2.0.0']
        self.assertEqual(pick_version(avail, '^1.0.0'), '1.1.0')
        self.assertEqual(pick_version(avail, '~1.0.0'), '1.0.5')
        self.assertEqual(pick_version(avail, '1.0.5'), '1.0.5')
        self.assertIsNone(pick_version(avail, '^3.0.0'))


class TestLocalRegistry(unittest.TestCase):
    def setUp(self):
        self.reg = LocalRegistry()

    def test_search(self):
        names = [r['name'] for r in self.reg.search('json')]
        self.assertEqual(names, ['aurora-json'])

    def test_search_all(self):
        self.assertGreaterEqual(len(self.reg.search('')), 3)

    def test_versions_sorted(self):
        self.assertEqual(self.reg.versions('aurora-math'),
                         ['1.0.0', '1.0.5', '1.1.0'])

    def test_get(self):
        v, content, desc = self.reg.get('aurora-json', '1.2.0')
        self.assertEqual(v, '1.2.0')
        self.assertIn('stringify', content)


class _PkgFixture(unittest.TestCase):
    """每个用例使用独立的临时项目目录与包缓存目录。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.proj = os.path.join(self.tmp, 'proj')
        self.cache = os.path.join(self.tmp, 'cache')
        os.makedirs(self.proj)
        self.pm = PackageManager(self.proj, packages_dir=self.cache)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestInit(_PkgFixture):
    def test_init_creates_structure(self):
        self.pm.init('demo')
        self.assertTrue(os.path.exists(os.path.join(self.proj, 'aurora.toml')))
        self.assertTrue(os.path.exists(os.path.join(self.proj, 'src', 'main.aur')))
        self.assertTrue(os.path.exists(os.path.join(self.proj, '.gitignore')))

    def test_init_manifest_fields(self):
        self.pm.init('demo')
        cfg = self.pm._read_config()
        self.assertEqual(cfg['project']['name'], 'demo')
        self.assertEqual(cfg['project']['version'], '0.1.0')
        self.assertEqual(cfg['build']['entry'], 'src/main.aur')

    def test_init_rejects_bad_name(self):
        with self.assertRaises(ValueError):
            self.pm.init('123bad')


class TestAddRemoveInstall(_PkgFixture):
    def setUp(self):
        super().setUp()
        self.pm.init('demo')

    def test_add_pins_version(self):
        v = self.pm.add('aurora-math', '~1.0.0')
        self.assertEqual(v, '1.0.5')
        deps = self.pm._dependencies()
        self.assertEqual(deps['aurora-math'], '~1.0.0')

    def test_add_defaults_latest(self):
        v = self.pm.add('aurora-http')
        self.assertEqual(v, '1.2.0')

    def test_add_unknown_package(self):
        with self.assertRaises(KeyError):
            self.pm.add('no-such-pkg')

    def test_lock_file_generated(self):
        self.pm.add('aurora-math', '1.0.5')
        self.assertTrue(os.path.exists(self.pm.lock_path))
        data = json.load(open(self.pm.lock_path, encoding='utf-8'))
        entry = data['packages']['aurora-math']
        self.assertEqual(entry['version'], '1.0.5')
        self.assertEqual(len(entry['hash']), 64)

    def test_install_all(self):
        self.pm.add('aurora-math', '1.0.5')
        self.pm.add('aurora-json', '^1.0.0')
        installed = self.pm.install()
        self.assertIn('aurora-math', installed)
        self.assertIn('aurora-json', installed)
        # ^1.0.0 应升到 1.2.0
        self.assertEqual(installed['aurora-json']['version'], '1.2.0')

    def test_list(self):
        self.pm.add('aurora-math', '1.0.5')
        items = self.pm.list()
        self.assertEqual(items['aurora-math']['require'], '1.0.5')
        self.assertEqual(items['aurora-math']['installed'], '1.0.5')

    def test_remove(self):
        self.pm.add('aurora-math', '1.0.5')
        self.assertTrue(self.pm.remove('aurora-math'))
        self.assertNotIn('aurora-math', self.pm.list())
        # 锁文件同步移除
        lock = self.pm._read_lock()
        self.assertNotIn('aurora-math', lock)

    def test_remove_absent(self):
        self.assertFalse(self.pm.remove('ghost'))

    def test_package_cached_on_disk(self):
        self.pm.add('aurora-math', '1.0.5')
        pkg_file = os.path.join(self.cache, 'aurora-math', '1.0.5', 'index.aur')
        self.assertTrue(os.path.exists(pkg_file))


class TestSearchOutdatedPublish(_PkgFixture):
    def setUp(self):
        super().setUp()
        self.pm.init('demo')

    def test_search(self):
        res = self.pm.search('math')
        self.assertEqual(res[0]['name'], 'aurora-math')
        self.assertIn('description', res[0])

    def test_outdated(self):
        # 锁定旧版本,注册表有更新
        self.pm.add('aurora-math', '1.0.0')
        out = self.pm.outdated()
        names = [o['name'] for o in out]
        self.assertIn('aurora-math', names)
        entry = [o for o in out if o['name'] == 'aurora-math'][0]
        self.assertEqual(entry['latest'], '1.1.0')

    def test_publish_ok(self):
        info = self.pm.publish()
        self.assertEqual(info['name'], 'demo')
        self.assertEqual(info['version'], '0.1.0')

    def test_publish_missing_fields(self):
        # 写一个残缺的 manifest
        with open(self.pm.manifest_path, 'w', encoding='utf-8') as f:
            f.write('[project]\nname = "x"\n')
        with self.assertRaises(RuntimeError):
            self.pm.publish()


if __name__ == '__main__':
    unittest.main()
