"""标准库扩充测试:Regex / DateTime / Crypto / FileSystem / Net"""

import os
import json
import shutil
import socket as _socket
import tempfile
import unittest
from unittest import mock

from aurora.stdlib import (
    AuroraError,
    AuroraRegex, AuroraDateTime, AuroraCrypto,
    AuroraFileSystem, AuroraNet,
)


class TestAuroraRegex(unittest.TestCase):
    def test_match(self):
        m = AuroraRegex.match(r'\d+', '123abc')
        self.assertEqual(m['match'], '123')
        self.assertIsNone(AuroraRegex.match(r'^abc', '123abc'))

    def test_search(self):
        m = AuroraRegex.search(r'\d+', 'abc 42 def')
        self.assertEqual(m['match'], '42')
        self.assertEqual(m['groups'], [])
        self.assertIsNone(AuroraRegex.search(r'xyz', 'abc'))

    def test_find_all(self):
        self.assertEqual(AuroraRegex.find_all(r'\d+', 'a1 b22 c333'),
                         ['1', '22', '333'])

    def test_replace(self):
        self.assertEqual(AuroraRegex.replace(r'\d+', '#', 'a1b22c333'),
                         'a#b#c#')

    def test_split(self):
        self.assertEqual(AuroraRegex.split(r'[,;]\s*', 'a, b;c'),
                         ['a', 'b', 'c'])

    def test_groups(self):
        m = AuroraRegex.search(r'(\w+)@(\w+)', 'contact: a@b here')
        self.assertEqual(m['groups'], ['a', 'b'])


class TestAuroraDateTime(unittest.TestCase):
    def test_now_and_timestamp(self):
        now = AuroraDateTime.now()
        self.assertIsNotNone(now)
        self.assertIsInstance(AuroraDateTime.timestamp(), int)

    def test_today_format(self):
        today = AuroraDateTime.today()
        self.assertRegex(today, r'^\d{4}-\d{2}-\d{2}$')

    def test_parse_and_format(self):
        dt = AuroraDateTime.parse('2024-01-02 03:04:05', '%Y-%m-%d %H:%M:%S')
        self.assertEqual(AuroraDateTime.format(dt, '%Y/%m/%d'), '2024/01/02')

    def test_parse_error(self):
        with self.assertRaises(AuroraError) as ctx:
            AuroraDateTime.parse('not-a-date', '%Y-%m-%d')
        self.assertEqual(ctx.exception.kind, 'DateTimeError')

    def test_add_days(self):
        dt = AuroraDateTime.parse('2024-01-01', '%Y-%m-%d')
        self.assertEqual(
            AuroraDateTime.format(AuroraDateTime.add_days(dt, 10), '%Y-%m-%d'),
            '2024-01-11')
        self.assertEqual(
            AuroraDateTime.format(AuroraDateTime.add_days(dt, -1), '%Y-%m-%d'),
            '2023-12-31')

    def test_diff(self):
        d1 = AuroraDateTime.parse('2024-01-11', '%Y-%m-%d')
        d2 = AuroraDateTime.parse('2024-01-01', '%Y-%m-%d')
        self.assertEqual(AuroraDateTime.diff(d1, d2), 10)


class TestAuroraCrypto(unittest.TestCase):
    def test_md5(self):
        # md5('abc') 已知值
        self.assertEqual(AuroraCrypto.md5('abc'),
                         '900150983cd24fb0d6963f7d28e17f72')

    def test_sha256(self):
        self.assertEqual(len(AuroraCrypto.sha256('abc')), 64)

    def test_sha1_sha512_length(self):
        self.assertEqual(len(AuroraCrypto.sha1('x')), 40)
        self.assertEqual(len(AuroraCrypto.sha512('x')), 128)

    def test_hmac(self):
        import hmac as h, hashlib
        expected = h.new(b'k', b'msg', hashlib.sha256).hexdigest()
        self.assertEqual(AuroraCrypto.hmac('k', 'msg'), expected)

    def test_base64_roundtrip(self):
        enc = AuroraCrypto.base64_encode('你好 world')
        self.assertEqual(AuroraCrypto.base64_decode(enc), '你好 world')

    def test_random_hex(self):
        h1 = AuroraCrypto.random_hex(16)
        self.assertEqual(len(h1), 16)
        self.assertRegex(h1, r'^[0-9a-f]{16}$')

    def test_uuid(self):
        import uuid as u
        self.assertEqual(u.UUID(AuroraCrypto.uuid()).version, 4)


class TestAuroraFileSystem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_exists_is_file_is_dir(self):
        f = os.path.join(self.tmp, 'a.txt')
        open(f, 'w').write('hi')
        self.assertTrue(AuroraFileSystem.exists(f))
        self.assertTrue(AuroraFileSystem.is_file(f))
        self.assertFalse(AuroraFileSystem.is_dir(f))
        self.assertTrue(AuroraFileSystem.is_dir(self.tmp))

    def test_mkdir_and_rmdir(self):
        d = os.path.join(self.tmp, 'a', 'b')
        AuroraFileSystem.mkdir(d)
        self.assertTrue(os.path.isdir(d))
        AuroraFileSystem.rmdir(os.path.join(self.tmp, 'a'), recursive=True)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, 'a')))

    def test_list_dir(self):
        open(os.path.join(self.tmp, 'x.txt'), 'w').close()
        open(os.path.join(self.tmp, 'y.txt'), 'w').close()
        self.assertEqual(AuroraFileSystem.list_dir(self.tmp), ['x.txt', 'y.txt'])

    def test_copy_move_remove(self):
        src = os.path.join(self.tmp, 's.txt')
        open(src, 'w').write('data')
        dst = os.path.join(self.tmp, 'd.txt')
        AuroraFileSystem.copy(src, dst)
        self.assertTrue(os.path.exists(dst))
        moved = os.path.join(self.tmp, 'm.txt')
        AuroraFileSystem.move(dst, moved)
        self.assertTrue(os.path.exists(moved))
        AuroraFileSystem.remove(moved)
        self.assertFalse(os.path.exists(moved))

    def test_file_size(self):
        f = os.path.join(self.tmp, 'big.bin')
        open(f, 'wb').write(b'0123456789')
        self.assertEqual(AuroraFileSystem.file_size(f), 10)

    def test_path_ops(self):
        self.assertEqual(AuroraFileSystem.extension('/a/b/c.txt'), '.txt')
        self.assertEqual(AuroraFileSystem.basename('/a/b/c.txt'), 'c.txt')
        self.assertEqual(AuroraFileSystem.dirname('/a/b/c.txt'), '/a/b')
        self.assertEqual(AuroraFileSystem.join_path('a', 'b', 'c.txt'),
                         os.path.join('a', 'b', 'c.txt'))
        self.assertTrue(os.path.isabs(AuroraFileSystem.absolute_path('rel/x')))


class _FakeResponse:
    def __init__(self, body):
        self._body = body.encode('utf-8')

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class TestAuroraNet(unittest.TestCase):
    @mock.patch('aurora.stdlib.urllib.request.urlopen')
    def test_get(self, m_urlopen):
        m_urlopen.return_value = _FakeResponse('{"ok": true}')
        self.assertEqual(AuroraNet.get('https://api.example/x'), '{"ok": true}')
        m_urlopen.assert_called_once()

    @mock.patch('aurora.stdlib.urllib.request.urlopen')
    def test_post_json(self, m_urlopen):
        m_urlopen.return_value = _FakeResponse('done')
        self.assertEqual(AuroraNet.post('https://api.example/x', json={'a': 1}), 'done')
        req = m_urlopen.call_args[0][0]
        self.assertEqual(req.method, 'POST')

    @mock.patch('aurora.stdlib.urllib.request.urlopen')
    def test_put_delete(self, m_urlopen):
        m_urlopen.return_value = _FakeResponse('ok')
        AuroraNet.put('https://api.example/x')
        self.assertEqual(m_urlopen.call_args[0][0].method, 'PUT')
        AuroraNet.delete('https://api.example/x')
        self.assertEqual(m_urlopen.call_args[0][0].method, 'DELETE')

    def test_url_parse(self):
        p = AuroraNet.url_parse('https://user@example.com:8080/path?q=1#frag')
        self.assertEqual(p['scheme'], 'https')
        self.assertEqual(p['hostname'], 'example.com')
        self.assertEqual(p['port'], 8080)
        self.assertEqual(p['path'], '/path')
        self.assertEqual(p['query'], 'q=1')

    def test_url_encode(self):
        self.assertEqual(AuroraNet.url_encode({'a': 1, 'b': 'x y'}),
                         'a=1&b=x+y')


class TestAuroraNetSocket(unittest.TestCase):
    """socket 方法用真实回环 server 验证收发。"""

    def test_echo_roundtrip(self):
        import threading

        served = {}

        def _serve():
            srv = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
            srv.bind(('127.0.0.1', 0))
            port = srv.getsockname()[1]
            served['port'] = port
            srv.listen(1)
            srv.settimeout(5)
            conn, _ = srv.accept()
            data = conn.recv(1024)
            conn.sendall(b'echo:' + data)
            conn.close()
            srv.close()

        t = threading.Thread(target=_serve, daemon=True)
        t.start()
        t.join(timeout=1)

        conn = AuroraNet.socket_connect('127.0.0.1', served['port'])
        try:
            AuroraNet.socket_send(conn, 'hello')
            out = AuroraNet.socket_recv(conn)
            self.assertTrue(out.startswith('echo:hello'))
        finally:
            AuroraNet.socket_close(conn)


if __name__ == '__main__':
    unittest.main()
