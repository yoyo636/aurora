#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Aurora v3.0.0 AI Engine
"""kernel.py — Aurora Jupyter 内核 + AI CLI 命令 + 运行时装饰器。

本文件把三件事集成到一处：

1. **AuroraKernel**：在 Jupyter 中执行 Aurora 代码的内核。优先基于
   ``ipykernel.kernelbase.Kernel``；若环境没有 ipykernel，则退化为一个
   独立的轻量实现（同样暴露 ``do_execute`` 等接口，可被程序调用）。
2. **AI CLI 命令**：``aurora ai train/infer``、``aurora serve``、
   ``aurora kernel [install]``，由 :func:`register_cli` 注册到主 CLI。
3. **``@ai`` 装饰器**：重导出 :mod:`aurora.ai.decorators.ai`。
"""

import io
import os
import sys
import json
import time
import signal
import argparse
import traceback
from typing import Any, Dict, Optional

# ── 重导出 @ai 装饰器 ─────────────────────────────────────────────────
from aurora.ai.decorators import ai, is_ai  # noqa: F401  (公共 API)

__version__ = "3.0.0"

# ── 探测 ipykernel（优先模式 A）───────────────────────────────────────
try:  # pragma: no cover - 取决于运行环境
    from ipykernel.kernelbase import Kernel as _IPyKernelBase
    _HAS_IPYKERNEL = True
except Exception:  # 模式 B：独立 fallback
    _IPyKernelBase = object  # type: ignore
    _HAS_IPYKERNEL = False


# ══════════════════════════════════════════════════════════════════════
#  Aurora 代码执行辅助
# ══════════════════════════════════════════════════════════════════════
def _run_aurora_source(source: str, interp=None) -> Dict[str, Any]:
    """执行一段 Aurora 源码，捕获 stdout / stderr。

    返回 {'ok': bool, 'stdout': str, 'stderr': str, 'error': str|None}。
    解释器按进程内单例复用（同一内核实例保留全局环境）。
    """
    from aurora.lexer import Lexer, LexerError
    from aurora.parser import Parser, ParseError
    from aurora.interpreter import Interpreter

    if interp is None:
        interp = Interpreter()

    buf_out, buf_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = buf_out, buf_err
    try:
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        interp.run(program)
        ok, err = True, None
    except (LexerError, ParseError) as e:
        ok, err = False, f"解析错误: {e}"
    except Exception as e:  # noqa: BLE001 - 内核需把任何运行时错误回传给前端
        ok, err = False, f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
    finally:
        sys.stdout, sys.stderr = old_out, old_err

    return {
        'ok': ok,
        'stdout': buf_out.getvalue(),
        'stderr': buf_err.getvalue(),
        'error': err,
        'interpreter': interp,
    }


# ══════════════════════════════════════════════════════════════════════
#  Jupyter 内核
# ══════════════════════════════════════════════════════════════════════
class AuroraKernel(_IPyKernelBase):
    """Aurora Jupyter 内核：在 notebook 中直接运行 .aur 代码。

    模式 A：ipykernel 可用时继承 ``Kernel``，通过 ZMQ 与 notebook 通信。
    模式 B：ipykernel 不可用时退化为纯 Python 对象，接口保持一致，
            可被脚本直接实例化并调用 :meth:`do_execute`。
    """

    implementation = 'Aurora'
    implementation_version = __version__
    language = 'aurora'
    language_version = __version__
    language_info = {
        'name': 'aurora',
        'mimetype': 'text/x-aurora',
        'file_extension': '.aur',
        'pygments_lexer': 'python',   # 回退高亮（Aurora 语法近 Python）
    }
    banner = f'Aurora v{__version__} — AI 原生编程语言'

    def __init__(self, **kwargs):
        self._interp = None
        if _HAS_IPYKERNEL:
            super().__init__(**kwargs)
        self.execution_count = 0

    # ── 内部 ──────────────────────────────────────────────────────────
    def _get_interp(self):
        """惰性创建并复用解释器实例（保留 cell 间的全局环境）。"""
        if self._interp is None:
            from aurora.interpreter import Interpreter
            self._interp = Interpreter()
        return self._interp

    def _publish(self, name: str, text: str):
        """向前端发送流式输出；无 ipykernel 时打印到本机 stdout。"""
        if not text:
            return
        if _HAS_IPYKERNEL and hasattr(self, 'iopub_socket'):
            self.send_response(self.iopub_socket, 'stream',
                               {'name': name, 'text': text})
        else:  # fallback：直接打印
            stream = sys.stderr if name == 'stderr' else sys.stdout
            stream.write(text)

    # ── 魔法命令 ─────────────────────────────────────────────────────
    def _handle_magic(self, line: str) -> Optional[Dict[str, Any]]:
        """解析并执行以 ``%`` 开头的魔法命令。

        返回 None 表示该行不是魔法命令（按普通 Aurora 代码执行）。
        """
        stripped = line.strip()
        if not stripped.startswith('%'):
            return None
        body = stripped.lstrip('%').strip()
        parts = body.split(maxsplit=1)
        cmd = parts[0] if parts else ''
        arg = parts[1] if len(parts) > 1 else ''

        interp = self._get_interp()

        if cmd == 'time':
            # %time <aurora code>：计时执行
            if not arg:
                return {'ok': False, 'error': '用法: %time <aurora 代码>'}
            t0 = time.perf_counter()
            result = _run_aurora_source(arg, interp=interp)
            elapsed = (time.perf_counter() - t0) * 1000.0
            result['stdout'] += f'\nCPU 耗时: {elapsed:.3f} ms\n'
            return result

        if cmd == 'load':
            # %load <path>：显示文件内容（不执行）
            try:
                with open(arg, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:  # noqa: BLE001
                return {'ok': False, 'error': f'%load 失败: {e}'}
            return {'ok': True, 'stdout': f'# 加载自 {arg}\n{content}', 'stderr': '', 'error': None}

        if cmd == 'run':
            # %run <path>：运行 .aur 文件
            try:
                out = io.StringIO()
                old = sys.stdout
                sys.stdout = out
                try:
                    interp.run_file(arg)
                finally:
                    sys.stdout = old
                return {'ok': True, 'stdout': out.getvalue(), 'stderr': '', 'error': None}
            except Exception as e:  # noqa: BLE001
                return {'ok': False, 'error': f'%run 失败: {e}'}

        if cmd == 'python':
            # %python <code>：在 Python 中执行代码
            try:
                out = io.StringIO()
                old = sys.stdout
                sys.stdout = out
                try:
                    exec(arg, {'__name__': '__aurora_magic__'})
                finally:
                    sys.stdout = old
                return {'ok': True, 'stdout': out.getvalue(), 'stderr': '', 'error': None}
            except Exception as e:  # noqa: BLE001
                return {'ok': False, 'error': f'%python 失败: {e}'}

        return {'ok': False, 'error': f'未知魔法命令: %{cmd}（支持 %time / %load / %run / %python）'}

    # ── Jupyter 主入口 ───────────────────────────────────────────────
    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        self.execution_count += 1
        reply: Dict[str, Any] = {
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

        # 识别魔法命令（首行非空即以 % 开头）
        first = next((ln for ln in code.splitlines() if ln.strip()), '')
        magic = self._handle_magic(first)

        if magic is None:
            result = _run_aurora_source(code, interp=self._get_interp())
        else:
            result = magic

        # 回传输出
        if not silent:
            self._publish('stdout', result.get('stdout', ''))
            self._publish('stderr', result.get('stderr', ''))
            if result.get('error'):
                self._publish('stderr', result['error'] + '\n')

        if result.get('ok'):
            reply['status'] = 'ok'
        else:
            reply['status'] = 'error'
            ename = 'AuroraRuntimeError'
            evalue = result.get('error', '未知错误')
            reply.update({'ename': ename, 'evalue': evalue,
                          'traceback': evalue.splitlines()})
            if _HAS_IPYKERNEL:
                try:
                    self.send_response(self.iopub_socket, 'error', {
                        'ename': ename, 'evalue': evalue,
                        'traceback': reply['traceback'],
                    })
                except Exception:
                    pass
        return reply

    def do_complete(self, code, cursor_pos):
        """简单补全：返回关键字与 std 模块名。"""
        matches = [
            'import', 'let', 'mut', 'fn', 'return', 'if', 'else', 'for',
            'while', 'print', 'import std.tensor', 'import std.nn',
            'import std.data', 'import std.agent', 'import std.inference',
        ]
        return {
            'matches': matches,
            'cursor_start': 0,
            'cursor_end': cursor_pos,
            'metadata': {},
            'status': 'ok',
        }

    def do_is_complete(self, code):
        return {'status': 'complete'}

    def do_shutdown(self, restart):
        return {'status': 'ok', 'restart': restart}


# ══════════════════════════════════════════════════════════════════════
#  kernelspec 安装
# ══════════════════════════════════════════════════════════════════════
def install_kernelspec() -> str:
    """把 Aurora kernelspec 写入用户 Jupyter 内核目录。

    macOS: ~/Library/Jupyter/kernels/aurora/kernel.json
    其他平台: 遵循 jupyter_client 的标准数据目录（~/.local/share/jupyter 等）。
    返回安装目录路径。
    """
    # 优先用 jupyter_client 的标准路径；不可用时退回到平台默认。
    candidate = None
    try:
        from jupyter_client import paths as _jpaths  # type: ignore
        candidate = os.path.join(_jpaths.jupyter_data_dir(), 'kernels', 'aurora')
    except Exception:
        if sys.platform == 'darwin':
            candidate = os.path.expanduser('~/Library/Jupyter/kernels/aurora')
        else:
            candidate = os.path.join(
                os.environ.get('XDG_DATA_HOME',
                               os.path.expanduser('~/.local/share')),
                'jupyter', 'kernels', 'aurora')

    os.makedirs(candidate, exist_ok=True)
    spec = {
        'argv': [sys.executable, '-m', 'aurora.ai.kernel', '-f', '{connection_file}'],
        'display_name': 'Aurora 3.0',
        'language': 'aurora',
        'name': 'aurora',
    }
    with open(os.path.join(candidate, 'kernel.json'), 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    return candidate


# ══════════════════════════════════════════════════════════════════════
#  AI CLI 命令实现
# ══════════════════════════════════════════════════════════════════════
def _cmd_ai_train(args):
    """加载 .aur 模型架构，用 JSON 数据训练指定轮数。"""
    from aurora.ai.tensor import Tensor
    from aurora.ai.autograd import Variable, SGD
    from aurora.ai import nn

    # 1. 读取模型架构
    try:
        with open(args.model, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"无法读取模型文件: {e}")
        sys.exit(1)
    layers = spec.get('layers', [])
    if not layers:
        print("模型文件中没有 'layers' 架构定义")
        sys.exit(1)

    # 2. 据架构重建 nn.Sequential
    model = nn.Sequential()
    for L in layers:
        if L.get('type', 'linear') != 'linear':
            continue
        model.add(nn.Linear(L['in'], L['out']))
        if L.get('activation') == 'relu':
            model.add(nn.ReLU())

    # 3. 读取训练数据
    if not args.data:
        print("提示: 未提供 --data，仅展示模型架构。")
        print(json.dumps(spec.get('hyperparams', {}), ensure_ascii=False))
        return
    try:
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"无法读取数据文件: {e}")
        sys.exit(1)
    X = data.get('X') or data.get('features') or data.get('x')
    y = data.get('y') or data.get('labels') or data.get('target')
    if X is None or y is None:
        print("数据 JSON 需包含 X/features 与 y/labels 字段")
        sys.exit(1)

    # 4. 训练循环
    criterion = nn.MSELoss()
    opt = SGD(model.parameters(), lr=args.lr)
    print(f"开始训练: {args.model}  epochs={args.epochs}  lr={args.lr}")
    for epoch in range(1, args.epochs + 1):
        opt.zero_grad()
        pred = model(Variable(Tensor(X)))
        target = Variable(Tensor(y))
        loss = criterion(pred, target)
        loss.backward()
        opt.step()
        loss_val = loss.data.item()
        print(f"  epoch {epoch:>4d}/{args.epochs}  loss={loss_val:.6f}")
    print("训练完成。")


def _cmd_ai_infer(args):
    """加载模型，对 JSON 输入执行推理。"""
    from aurora.ai.inference import InferenceEngine

    engine = InferenceEngine(args.model)
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'inputs' in data:
        inp = data['inputs']
    else:
        inp = data
    result = engine.infer(inp)
    print(json.dumps(result, ensure_ascii=False, default=str))


def _cmd_serve(args):
    """启动基于 InferenceServer 的 HTTP 推理服务。"""
    from aurora.ai.inference import InferenceEngine, InferenceServer

    engine = InferenceEngine(args.model)
    server = InferenceServer(engine, host=args.host, port=args.port)
    addr = server.start()
    print(f"Aurora 推理服务器已启动: {addr}")
    print("可用端点:")
    print("  GET  /health        健康检查")
    print("  POST /predict       推理  (JSON: {\"inputs\": ...})")
    print("  GET  /model         模型信息")
    print("  POST /batch_predict 批量推理")
    print("按 Ctrl+C 停止服务")

    def _stop(signum, frame):
        server.stop()
        print("\n服务已停止。")
        sys.exit(0)

    signal.signal(signal.SIGINT, _stop)
    try:
        signal.pause()
    except AttributeError:  # Windows 无 signal.pause
        while True:
            time.sleep(3600)


def _cmd_kernel_launch(args):
    """启动 / 说明 Jupyter 内核。"""
    if _HAS_IPYKERNEL:
        print("Aurora Jupyter 内核已就绪。")
        print("通常由 Jupyter 通过 kernelspec 自动调用；请先运行: aurora kernel install")
        print("然后在 jupyter notebook / lab 中选择 'Aurora 3.0' 内核。")
    else:
        print("当前环境未安装 ipykernel，无法直接启动 Jupyter 内核。")
        print("请先安装:  pip3 install ipykernel")
        print("然后:      aurora kernel install")


def _cmd_kernel_install(args):
    """安装 Jupyter kernelspec。"""
    path = install_kernelspec()
    print(f"已安装 Aurora kernelspec -> {os.path.join(path, 'kernel.json')}")
    print("现在可以在 Jupyter 中选择 'Aurora 3.0' 内核。")


# ══════════════════════════════════════════════════════════════════════
#  注册到主 CLI
# ══════════════════════════════════════════════════════════════════════
def register_cli(subparsers):
    """把 AI / serve / kernel 子命令注册到 aurora CLI。"""

    # ── aurora ai train / infer ──
    p_ai = subparsers.add_parser('ai', help='AI 模型训练与推理')
    ai_sub = p_ai.add_subparsers(dest='ai_cmd')

    p_train = ai_sub.add_parser('train', help='训练 .aur 模型')
    p_train.add_argument('model', help='.aur 模型文件路径')
    p_train.add_argument('--data', help='训练数据 JSON（含 X/features 与 y/labels）')
    p_train.add_argument('--epochs', type=int, default=10, help='训练轮数（默认 10）')
    p_train.add_argument('--lr', type=float, default=0.01, help='学习率（默认 0.01）')
    p_train.set_defaults(func=_cmd_ai_train)

    p_infer = ai_sub.add_parser('infer', help='对输入数据执行推理')
    p_infer.add_argument('model', help='.aur 模型文件路径')
    p_infer.add_argument('--input', required=True, help='输入数据 JSON 文件')
    p_infer.set_defaults(func=_cmd_ai_infer)

    # ── aurora serve ──
    p_serve = subparsers.add_parser('serve', help='启动模型推理 HTTP 服务器')
    p_serve.add_argument('model', help='.aur 模型文件路径')
    p_serve.add_argument('--port', type=int, default=8080, help='监听端口（默认 8080）')
    p_serve.add_argument('--host', default='0.0.0.0', help='监听地址（默认 0.0.0.0）')
    p_serve.set_defaults(func=_cmd_serve)

    # ── aurora kernel [install] ──
    p_kernel = subparsers.add_parser('kernel', help='Jupyter 内核管理')
    p_kernel.add_argument('--ip', default='127.0.0.1', help='内核监听 IP（默认 127.0.0.1）')
    p_kernel.add_argument('--port', type=int, default=8888, help='内核端口（默认 8888）')
    k_sub = p_kernel.add_subparsers(dest='kernel_cmd')
    p_ki = k_sub.add_parser('install', help='安装 Jupyter kernelspec')
    p_ki.set_defaults(func=_cmd_kernel_install)
    p_kernel.set_defaults(func=_cmd_kernel_launch)


# ══════════════════════════════════════════════════════════════════════
#  内核入口（由 jupyter 通过 kernelspec 调用：python -m aurora.ai.kernel -f conn）
# ══════════════════════════════════════════════════════════════════════
def _launch():
    parser = argparse.ArgumentParser(prog='aurora.ai.kernel')
    parser.add_argument('-f', '--connection-file', default=None,
                        help='Jupyter 连接文件（由 kernelspec 提供）')
    parser.add_argument('--ip', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8888)
    ns = parser.parse_args()

    if _HAS_IPYKERNEL:
        from ipykernel.kernelapp import IPKernelApp  # type: ignore
        IPKernelApp.launch_instance(kernel_class=AuroraKernel)
    else:
        print("未安装 ipykernel。请先 `pip3 install ipykernel`，再由 Jupyter 启动本内核。")
        sys.exit(1)


if __name__ == '__main__':
    _launch()
