"""Aurora Inference — 模型推理引擎 (AuroraInference)

本模块提供纯 Python 的模型推理引擎,包含:

- InferenceEngine:统一推理入口,支持 .aur 格式与 ONNX(onnxruntime 可选)
- Quantizer:int8 对称/非对称量化与 fp16 存储,推理时反量化
- InferenceServer:基于 http.server 的 REST 推理服务(/health /predict /model /batch_predict)
- .aur 模型格式:JSON 描述架构 + 权重 + 超参数,版本 "aurora-model-v1"
- 性能优化:warmup / set_num_threads / 自动记录 last_latency_ms

onnxruntime 是可选依赖;不可用时 load_onnx 会给出清晰提示。
"""

# Aurora v3.0.0 AI Engine

import os
import sys
import json
import time
import math
import socket
import threading
from array import array
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# 异常
# ---------------------------------------------------------------------------

class InferenceError(Exception):
    """推理引擎异常"""
    def __init__(self, message: str, kind: str = "InferenceError"):
        self.kind = kind
        super().__init__(f"[{kind}] {message}")


# ---------------------------------------------------------------------------
# 内置极简 Aurora 模型(用于 .aur 格式的纯 Python 前向)
# ---------------------------------------------------------------------------

class SimpleAuroraModel:
    """极简前馈模型:若干 linear(+ReLU)层。

    架构由 layers 列表描述,每层:
        {'type': 'linear', 'in': n, 'out': m, 'W': [[...]], 'b': [...], 'activation': 'relu'|None}
    前向:x @ W + b,可选 ReLU。
    """

    def __init__(self, layers: List[dict], hyperparams: dict = None,
                 metadata: dict = None):
        self.layers = layers
        self.hyperparams = hyperparams or {}
        self.metadata = metadata or {}
        self.format_version = "aurora-model-v1"

    def forward(self, x: List[float]) -> List[float]:
        """纯 Python 前向:x 为一维 float list。"""
        cur = list(x)
        for layer in self.layers:
            W = layer['W']  # shape [out, in]
            b = layer['b']  # shape [out]
            out = []
            for i in range(len(W)):
                row = W[i]
                s = b[i]
                # 点积
                n = min(len(row), len(cur))
                for j in range(n):
                    s += row[j] * cur[j]
                if layer.get('activation') == 'relu' and s < 0:
                    s = 0.0
                out.append(s)
            cur = out
        return cur

    def infer(self, input_data) -> Any:
        """统一入口:input_data 是 dict(单输入)或 list。"""
        if isinstance(input_data, dict):
            # 取第一个值作为输入向量
            if not input_data:
                raise InferenceError("infer: input dict 为空")
            x = next(iter(input_data.values()))
        else:
            x = input_data
        return self.forward(list(x))

    def summary(self) -> dict:
        """模型信息摘要。"""
        total_params = 0
        layer_infos = []
        for i, layer in enumerate(self.layers):
            n_in, n_out = layer['in'], layer['out']
            count = n_in * n_out + n_out
            total_params += count
            layer_infos.append({
                'index': i, 'type': layer['type'],
                'in': n_in, 'out': n_out,
                'activation': layer.get('activation'),
                'params': count,
            })
        return {
            'format': self.format_version,
            'num_layers': len(self.layers),
            'total_params': total_params,
            'layers': layer_infos,
            'hyperparams': self.hyperparams,
            'metadata': self.metadata,
        }


# ---------------------------------------------------------------------------
# .aur 模型格式读写
# ---------------------------------------------------------------------------

def save_model(model: SimpleAuroraModel, path: str) -> str:
    """保存 Aurora 模型为 JSON 格式(.aur 后缀)。

    保存:模型架构描述、权重(list)、超参数、元信息,带版本标记。
    """
    if not path.endswith('.aur'):
        path = path + '.aur'
    data = {
        'format': 'aurora-model-v1',
        'layers': model.layers,
        'hyperparams': model.hyperparams,
        'metadata': model.metadata,
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return path


def load_model(path: str) -> SimpleAuroraModel:
    """加载 .aur 模型文件。"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data.get('format') != 'aurora-model-v1':
        raise InferenceError(
            f"不支持的模型格式: {data.get('format')!r},期望 'aurora-model-v1'",
            "FormatError")
    return SimpleAuroraModel(
        layers=data['layers'],
        hyperparams=data.get('hyperparams', {}),
        metadata=data.get('metadata', {}),
    )


# ---------------------------------------------------------------------------
# 量化器
# ---------------------------------------------------------------------------

class QuantizedModel:
    """量化后的模型:持有 int8 权重 + scale/zero_point,推理时反量化。"""

    def __init__(self, base_model: SimpleAuroraModel, precision: str = 'int8'):
        self.base = base_model
        self.precision = precision
        # quantized_layers:与原层结构一致,但 W 替换为 (W_q_flat, shape, scale, zero_point)
        self.quantized_layers: List[dict] = []
        self._quantize()

    @staticmethod
    def _quantize_int8(W: List[List[float]]):
        """对二维权重矩阵做非对称 int8 量化。

        公式:
            scale       = (max - min) / 255
            zero_point  = round(-min / scale),clip 到 [0, 255]
            W_q         = clip(round(W / scale) + zero_point, 0, 255)
        反量化:W_dequant = (W_q - zero_point) * scale
        """
        flat = [v for row in W for v in row]
        wmin = min(flat) if flat else 0.0
        wmax = max(flat) if flat else 0.0
        rng = wmax - wmin
        if rng == 0:
            rng = 1.0
        scale = rng / 255.0
        zp = int(round(-wmin / scale))
        zp = max(0, min(255, zp))
        q = array('b')  # signed char, -128..127;但我们用 0..255,改用 'B'
        q = array('B')
        for row in W:
            for v in row:
                val = int(round(v / scale)) + zp
                val = max(0, min(255, val))
                q.append(val)
        shape = (len(W), len(W[0]) if W else 0)
        return q, shape, scale, zp

    @staticmethod
    def _quantize_fp16(W: List[List[float]]):
        """fp16:把权重值按半精度精度截断后存储。

        Python array 在部分平台不支持 'e'(IEEE 754 半精度),
        这里统一用 list[float] 存储,并把每个值四舍五入到 ~1e-3 精度
        (模拟 fp16 仅 ~3.3 位十进制有效数字),不做量化 scale/zp。
        """
        q: List[float] = []
        for row in W:
            for v in row:
                # 模拟 fp16 的有限精度:保留 3 位有效数字
                q.append(float(f"{v:.3e}"))
        shape = (len(W), len(W[0]) if W else 0)
        return q, shape, 1.0, 0

    def _quantize(self):
        """对所有 linear 层的 W 做量化。"""
        quant_fn = (self._quantize_int8 if self.precision == 'int8'
                    else self._quantize_fp16)
        for layer in self.base.layers:
            if layer.get('type') != 'linear':
                self.quantized_layers.append(dict(layer))
                continue
            q, shape, scale, zp = quant_fn(layer['W'])
            new_layer = dict(layer)
            new_layer['W_quant'] = {
                'data': list(q),
                'shape': shape,
                'scale': scale,
                'zero_point': zp,
                'precision': self.precision,
            }
            # 保留 b 为 float(fp32)
            self.quantized_layers.append(new_layer)

    def _dequant_layer(self, layer: dict) -> List[List[float]]:
        """把量化权重反量化回二维 float list。"""
        wq = layer['W_quant']
        data = wq['data']
        rows, cols = wq['shape']
        scale = wq['scale']
        zp = wq['zero_point']
        precision = wq.get('precision', 'int8')
        W: List[List[float]] = []
        idx = 0
        for _ in range(rows):
            row: List[float] = []
            for _ in range(cols):
                v = data[idx]
                idx += 1
                if precision == 'int8':
                    row.append((v - zp) * scale)
                else:
                    # fp16 存储时无需反量化
                    row.append(float(v))
            W.append(row)
        return W

    def infer(self, input_data) -> Any:
        """反量化 + 前向推理。"""
        # 构造一个临时 SimpleAuroraModel,用反量化后的 W 跑 forward
        layers = []
        for layer in self.quantized_layers:
            if 'W_quant' in layer:
                l = dict(layer)
                l['W'] = self._dequant_layer(layer)
                del l['W_quant']
                layers.append(l)
            else:
                layers.append(layer)
        tmp = SimpleAuroraModel(layers, self.base.hyperparams, self.base.metadata)
        return tmp.infer(input_data)

    def summary(self) -> dict:
        s = self.base.summary()
        s['quantized'] = True
        s['precision'] = self.precision
        return s


class Quantizer:
    """模型量化器入口。"""

    def __init__(self, precision: str = 'int8'):
        if precision not in ('int8', 'fp16'):
            raise InferenceError(f"不支持的量化精度: {precision!r}(仅 int8/fp16)",
                                 "QuantizeError")
        self.precision = precision

    def quantize(self, model: SimpleAuroraModel) -> QuantizedModel:
        """量化模型权重,返回 QuantizedModel(可直接 .infer)。"""
        return QuantizedModel(model, precision=self.precision)


# ---------------------------------------------------------------------------
# 推理引擎
# ---------------------------------------------------------------------------

class InferenceEngine:
    """统一推理引擎:支持 .aur 与 ONNX。

    用法:
        engine = InferenceEngine()
        engine.load("model.aur")
        out = engine.infer([1.0, 2.0, 3.0])
    """

    def __init__(self, model_path: str = None, device: str = 'cpu'):
        self.device = device
        self.model: Optional[Any] = None
        self.model_path: Optional[str] = model_path
        self.model_format: Optional[str] = None   # 'aur' / 'onnx'
        self._ort_session = None                   # onnxruntime session
        self._input_names: List[str] = []
        self._num_threads = 1
        self.last_latency_ms: float = 0.0
        if model_path:
            self.load(model_path)

    # -- 加载 --
    def load(self, model_path: str) -> Any:
        """加载模型:根据后缀自动识别 .aur / .onnx。"""
        self.model_path = model_path
        if model_path.endswith('.onnx'):
            return self.load_onnx(model_path)
        if model_path.endswith('.aur'):
            self.model = load_model(model_path)
            self.model_format = 'aur'
            return self.model
        raise InferenceError(f"未知模型格式: {model_path}(支持 .aur / .onnx)",
                             "FormatError")

    def load_onnx(self, onnx_path: str) -> Any:
        """通过 onnxruntime 加载 ONNX 模型(可选依赖)。

        优先 import onnxruntime;若不可用,给出清晰错误提示。
        """
        try:
            import onnxruntime as ort  # type: ignore
        except ImportError:
            raise InferenceError(
                "未安装 onnxruntime。请先 `pip install onnxruntime`,"
                "或使用 .aur 格式模型。",
                "DependencyError")
        so = ort.SessionOptions()
        so.intra_op_num_threads = self._num_threads
        self._ort_session = ort.InferenceSession(
            onnx_path, sess_options=so, providers=['CPUExecutionProvider'])
        self._input_names = [i.name for i in self._ort_session.get_inputs()]
        self.model = self._ort_session
        self.model_format = 'onnx'
        return self._ort_session

    # -- 推理 --
    def infer(self, input_data) -> Any:
        """单样本推理。input_data 是 dict(输入名->值)或 list。

        自动记录耗时到 self.last_latency_ms。
        """
        if self.model is None:
            raise InferenceError("模型未加载,请先调用 load()", "StateError")
        t0 = time.perf_counter()
        try:
            if self.model_format == 'onnx':
                result = self.infer_onnx(input_data)
            else:
                result = self.model.infer(input_data)
        finally:
            self.last_latency_ms = (time.perf_counter() - t0) * 1000.0
        return result

    def infer_onnx(self, input_data) -> Any:
        """ONNX 推理:自动获取输入名称并 run。"""
        if self._ort_session is None:
            raise InferenceError("ONNX session 未加载", "StateError")
        if isinstance(input_data, dict):
            feed = dict(input_data)
        else:
            # list / numpy-like:按顺序喂给 session 的输入名
            if len(self._input_names) == 1:
                feed = {self._input_names[0]: input_data}
            else:
                if not isinstance(input_data, (list, tuple)):
                    raise InferenceError("多输入模型请传入 dict")
                feed = {name: val for name, val in
                        zip(self._input_names, input_data)}
        outputs = self._ort_session.run(None, feed)
        return outputs[0] if len(outputs) == 1 else list(outputs)

    def batch_infer(self, inputs, batch_size: int = 32) -> List[Any]:
        """批量推理:按 batch_size 切分 inputs 依次推理。"""
        results: List[Any] = []
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i:i + batch_size]
            for single in batch:
                results.append(self.infer(single))
        return results

    def predict(self, input_data) -> Any:
        """infer 的别名,返回预测结果。"""
        return self.infer(input_data)

    # -- 信息 --
    def summary(self) -> dict:
        """模型信息摘要。"""
        if self.model is None:
            return {'loaded': False}
        if self.model_format == 'aur' and hasattr(self.model, 'summary'):
            s = self.model.summary()
            s.update({'loaded': True, 'format': 'aur',
                      'path': self.model_path, 'device': self.device})
            return s
        if self.model_format == 'onnx':
            inputs_meta = []
            for i in self._ort_session.get_inputs():
                inputs_meta.append({'name': i.name, 'shape': list(i.shape),
                                    'type': str(i.type)})
            outputs_meta = [{'name': o.name, 'shape': list(o.shape)}
                           for o in self._ort_session.get_outputs()]
            return {'loaded': True, 'format': 'onnx',
                    'path': self.model_path, 'device': self.device,
                    'inputs': inputs_meta, 'outputs': outputs_meta}
        return {'loaded': True, 'path': self.model_path}

    # -- 性能 --
    def warmup(self, input_shape) -> None:
        """预热:用一个零向量跑一次推理,初始化后端。"""
        if isinstance(input_shape, int):
            dummy = [0.0] * input_shape
        elif isinstance(input_shape, (list, tuple)):
            n = input_shape[-1] if input_shape else 1
            dummy = [0.0] * n
        else:
            dummy = [0.0]
        self.infer(dummy)

    def set_num_threads(self, n: int) -> None:
        """设置线程数(对 ONNX session 即时生效;.aur 为纯 Python,仅记录)。"""
        self._num_threads = max(1, int(n))
        if self._ort_session is not None:
            try:
                self._ort_session.get_session_options().intra_op_num_threads = n
            except Exception:
                pass


# ---------------------------------------------------------------------------
# 推理服务器
# ---------------------------------------------------------------------------

class _InferenceHandlerFactory:
    """为 InferenceServer 生成带 model/engine 闭包的请求处理器。"""

    @staticmethod
    def make(server: 'InferenceServer'):
        class Handler(BaseHTTPRequestHandler):
            # 静默默认日志,避免污染 stdout
            def log_message(self, fmt, *args):
                return

            def _send_json(self, code: int, obj: dict):
                body = json.dumps(obj, ensure_ascii=False, default=str).encode('utf-8')
                self.send_response(code)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path == '/health':
                    self._send_json(200, {
                        'status': 'ok',
                        'model': server.engine.model_path or server.model_name,
                    })
                elif self.path == '/model':
                    self._send_json(200, server.engine.summary())
                else:
                    self._send_json(404, {'error': f'unknown path {self.path}'})

            def do_POST(self):
                try:
                    length = int(self.headers.get('Content-Length', 0))
                    raw = self.rfile.read(length) if length > 0 else b'{}'
                    body = json.loads(raw.decode('utf-8') or '{}')
                except Exception as e:
                    self._send_json(400, {'error': f'invalid JSON: {e}'})
                    return

                try:
                    if self.path == '/predict':
                        inputs = body.get('inputs')
                        out = server.engine.infer(inputs)
                        self._send_json(200, {
                            'output': out,
                            'latency_ms': server.engine.last_latency_ms,
                        })
                    elif self.path == '/batch_predict':
                        inputs = body.get('inputs') or []
                        out = server.engine.batch_infer(
                            inputs, batch_size=body.get('batch_size', 32))
                        self._send_json(200, {'outputs': out})
                    else:
                        self._send_json(404, {'error': f'unknown path {self.path}'})
                except Exception as e:
                    self._send_json(500, {'error': str(e)})

        return Handler


class InferenceServer:
    """基于 ThreadingHTTPServer 的推理服务器,支持并发。

    REST API:
        GET  /health         健康检查
        POST /predict         推理(JSON body: {"inputs": ...})
        GET  /model           模型信息
        POST /batch_predict   批量推理(JSON body: {"inputs": [...], "batch_size": 32})
    """

    def __init__(self, model, host: str = '0.0.0.0', port: int = 8080):
        # model 可以是 InferenceEngine,或任意带 infer/batch_infer/summary 的对象
        if isinstance(model, InferenceEngine):
            self.engine = model
        else:
            self.engine = InferenceEngine()
            self.engine.model = model
        self.host = host
        self.port = port
        self.model_name = getattr(model, '__class__', type(model)).__name__
        self._httpd: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> str:
        """启动 HTTP 服务器(后台线程),返回服务地址。"""
        handler = _InferenceHandlerFactory.make(self)
        self._httpd = ThreadingHTTPServer((self.host, self.port), handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        # 回显实际端口(允许 port=0 时系统分配)
        actual_host, actual_port = self._httpd.server_address[:2]
        self.port = actual_port
        return f"http://{actual_host}:{actual_port}"

    def stop(self) -> None:
        """停止服务器。"""
        if self._httpd is not None:
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None


# ---------------------------------------------------------------------------
# 冒烟测试
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import tempfile

    print("=" * 60)
    print("Aurora Inference 引擎 — 冒烟测试")
    print("=" * 60)

    # 1. 构造一个简单模型:3 -> 4 (relu) -> 2
    def _make_model() -> SimpleAuroraModel:
        layer1 = {
            'type': 'linear', 'in': 3, 'out': 4, 'activation': 'relu',
            'W': [[0.1, 0.2, 0.3],
                  [0.4, 0.5, 0.6],
                  [-0.1, -0.2, -0.3],
                  [0.7, 0.8, 0.9]],
            'b': [0.0] * 4,
        }
        layer2 = {
            'type': 'linear', 'in': 4, 'out': 2, 'activation': None,
            'W': [[1.0, 0.0, 0.5, 0.2],
                  [0.2, 0.3, 0.1, -0.4]],
            'b': [0.0] * 2,
        }
        return SimpleAuroraModel([layer1, layer2],
                                 hyperparams={'lr': 0.01, 'epochs': 10},
                                 metadata={'name': 'demo'})

    m = _make_model()
    out = m.infer([1.0, 1.0, 1.0])
    assert len(out) == 2
    print(f"[OK] SimpleAuroraModel.forward -> {out}")

    # 2. .aur 保存 / 加载
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "demo.aur")
        save_model(m, p)
        loaded = load_model(p)
        out2 = loaded.infer([1.0, 1.0, 1.0])
        assert [round(x, 6) for x in out] == [round(x, 6) for x in out2]
        print(f"[OK] save_model / load_model (.aur) -> {out2}")

    # 3. InferenceEngine 加载 .aur 并推理
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "demo.aur")
        save_model(m, p)
        engine = InferenceEngine(p)
        assert engine.model_format == 'aur'
        pred = engine.predict([1.0, 1.0, 1.0])
        assert len(pred) == 2
        assert engine.last_latency_ms >= 0
        summary = engine.summary()
        assert summary['total_params'] == (3 * 4 + 4) + (4 * 2 + 2)
        print(f"[OK] InferenceEngine.infer -> {pred}, "
              f"latency={engine.last_latency_ms:.3f}ms, "
              f"params={summary['total_params']}")

        # 4. batch_infer
        batch = engine.batch_infer([[1, 1, 1], [0, 0, 0], [2, 2, 2]], batch_size=2)
        assert len(batch) == 3
        print(f"[OK] batch_infer (3 samples)")

        # 5. warmup + set_num_threads
        engine.warmup(3)
        engine.set_num_threads(2)
        print(f"[OK] warmup / set_num_threads(2)")

    # 6. Quantizer int8 量化
    q = Quantizer(precision='int8')
    qmodel = q.quantize(m)
    qout = qmodel.infer([1.0, 1.0, 1.0])
    # 反量化误差应很小(int8 非对称量化)
    max_err = max(abs(a - b) for a, b in zip(out, qout))
    assert max_err < 0.5, f"量化误差过大: {max_err}"
    print(f"[OK] Quantizer int8 -> {qout}, max_err={max_err:.4f}")

    # 7. fp16 量化
    qf = Quantizer(precision='fp16')
    qfmodel = qf.quantize(m)
    qfout = qfmodel.infer([1.0, 1.0, 1.0])
    assert len(qfout) == 2
    print(f"[OK] Quantizer fp16 -> {qfout}")

    # 8. ONNX 可用性检测(不强制安装,只验证错误提示清晰)
    engine2 = InferenceEngine()
    try:
        import onnxruntime  # noqa: F401
        print("[OK] onnxruntime 已安装(跳过错误提示验证)")
    except ImportError:
        try:
            engine2.load_onnx("dummy.onnx")
        except InferenceError as e:
            assert "onnxruntime" in str(e)
            print(f"[OK] load_onnx 缺依赖时给出清晰提示: {e}")

    # 9. InferenceServer(用随机端口,后台启动,请求一次 /health)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "demo.aur")
        save_model(m, p)
        eng = InferenceEngine(p)
        server = InferenceServer(eng, host='127.0.0.1', port=0)
        addr = server.start()
        # 用 urllib 请求 /health
        import urllib.request
        with urllib.request.urlopen(addr + '/health', timeout=5) as r:
            hb = json.loads(r.read().decode('utf-8'))
        assert hb['status'] == 'ok'
        # /predict
        req = urllib.request.Request(
            addr + '/predict',
            data=json.dumps({'inputs': [1.0, 1.0, 1.0]}).encode('utf-8'),
            headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as r:
            pb = json.loads(r.read().decode('utf-8'))
        assert len(pb['output']) == 2
        # /model
        with urllib.request.urlopen(addr + '/model', timeout=5) as r:
            mb = json.loads(r.read().decode('utf-8'))
        assert mb['format'] == 'aur'
        server.stop()
        print(f"[OK] InferenceServer @ {addr} (health/predict/model)")

    print("=" * 60)
    print("全部冒烟测试通过 ✔")
    print("=" * 60)
