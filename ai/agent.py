"""Aurora Agent — LLM Agent 框架 (AuroraAgent)

本模块将 stdlib.AuroraAI 的简单 chat/agent 能力增强为完整的 Agent 框架,包含:

- LLM 客户端:OpenAI 兼容 / Anthropic / 本地模型(llama.cpp server)三种后端,统一接口
- 工具系统:Tool 类 + 装饰器 + 全局注册表
- Agent 主类:ReAct 风格工具调用循环(Thought/Action/Observation)
- 记忆系统:短期对话记忆 ConversationMemory + 长期向量记忆 LongTermMemory
- RAG:检索增强生成管线(纯 Python TF-IDF,不依赖外部嵌入 API)
- Prompt 模板:PromptTemplate / FewShotTemplate
- Chain:LLMChain / SequentialChain / TransformChain

纯 Python 实现,HTTP 全部走 urllib(与 stdlib.AuroraAI 一致),流式输出用 generator。
不直接 import stdlib(避免循环导入),配置读取逻辑在模块内独立实现。
"""

# Aurora v3.0.0 AI Engine

import os
import json
import time
import math
import inspect
import urllib.request
import urllib.error
from typing import Any, Callable, Dict, Generator, List, Optional


# ---------------------------------------------------------------------------
# 配置读取(与 stdlib.AuroraAI 保持一致,但模块内独立实现,避免循环导入)
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = (os.environ.get('AURORA_AI_BASE_URL')
                    or 'https://ark.cn-beijing.volces.com/api/v3')
DEFAULT_API_KEY = (os.environ.get('AURORA_AI_API_KEY')
                   or os.environ.get('DOUBAO_API_KEY')
                   or os.environ.get('OPENAI_API_KEY') or '')
DEFAULT_MODEL = os.environ.get('AURORA_AI_MODEL') or 'doubao-seed-1-6-250615'
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY') or ''
ANTHROPIC_BASE_URL = 'https://api.anthropic.com/v1'


class AgentError(Exception):
    """Agent 框架运行时异常"""
    def __init__(self, message: str, kind: str = "AgentError"):
        self.kind = kind
        super().__init__(f"[{kind}] {message}")


# ---------------------------------------------------------------------------
# HTTP 工具(urllib 封装,与 stdlib.AuroraAI._post 同风格)
# ---------------------------------------------------------------------------

def _http_post_json(url: str, payload: dict, headers: dict,
                    timeout: int = 60) -> dict:
    """向 url 发送 JSON POST,返回解析后的 JSON dict。"""
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json', **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')[:300]
        raise AgentError(f"HTTP {e.code}: {detail}", "HTTPError")
    except Exception as e:
        raise AgentError(str(e), "HTTPError")


def _http_post_stream(url: str, payload: dict, headers: dict,
                      timeout: int = 120) -> Generator[str, None, None]:
    """发送 JSON POST 并按 SSE 流式逐块 yield 文本增量。

    SSE 格式:每行 `data: {...}\\n\\n`,解析 JSON 后取 delta.content / content_block.delta.text。
    """
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json',
                 'Accept': 'text/event-stream', **headers})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')[:300]
        raise AgentError(f"HTTP {e.code}: {detail}", "HTTPError")
    except Exception as e:
        raise AgentError(str(e), "HTTPError")

    with resp:
        buf = b""
        # 逐块读取响应流,按 \\n 切分出完整 SSE 事件行
        while True:
            chunk = resp.read(512)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                if not line.startswith(b"data:"):
                    continue
                data_str = line[5:].strip().decode('utf-8', 'replace')
                if data_str == "[DONE]":
                    return
                try:
                    obj = json.loads(data_str)
                except Exception:
                    continue
                # OpenAI 兼容:choices[0].delta.content
                choices = obj.get('choices') or []
                if choices:
                    delta = choices[0].get('delta') or {}
                    piece = delta.get('content')
                    if piece:
                        yield piece
                    continue
                # Anthropic:content_block.delta.text
                if obj.get('type') == 'content_block_delta':
                    piece = (obj.get('delta') or {}).get('text')
                    if piece:
                        yield piece


# ---------------------------------------------------------------------------
# LLM 后端适配
# ---------------------------------------------------------------------------

class OpenAILLM:
    """OpenAI 兼容 LLM(默认,兼容火山方舟 / DeepSeek / 本地 llama.cpp server 等)。

    统一接口:
        complete(messages) -> str
        chat(prompt, system=None) -> str
        stream(messages) -> generator[yield str]
    """

    provider = "openai"

    def __init__(self, model: str = None, base_url: str = None,
                 api_key: str = None, temperature: float = 0.7):
        self.model = model or DEFAULT_MODEL
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip('/')
        self.api_key = api_key or DEFAULT_API_KEY
        self.temperature = temperature

    # -- 内部 --
    def _headers(self) -> dict:
        h = {'Authorization': 'Bearer ' + self.api_key} if self.api_key else {}
        return h

    def _build_payload(self, messages: list, temperature: float = None,
                       tools: list = None, stream: bool = False) -> dict:
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': self.temperature if temperature is None else temperature,
            'stream': stream,
        }
        if tools:
            payload['tools'] = tools
        return payload

    # -- 公开接口 --
    def complete(self, messages: list, temperature: float = None,
                 tools: list = None) -> dict:
        """多轮消息补全,返回 {'content': str, 'tool_calls': [...], 'message': dict, 'raw': dict}。"""
        if not self.api_key:
            raise AgentError(
                "未配置 API Key。请设置环境变量 AURORA_AI_API_KEY / DOUBAO_API_KEY / "
                "OPENAI_API_KEY,或在构造 LLM 时传入 api_key。", "AuthError")
        payload = self._build_payload(messages, temperature=temperature, tools=tools)
        raw = _http_post_json(self.base_url + '/chat/completions', payload,
                              self._headers())
        choice = (raw.get('choices') or [{}])[0]
        msg = choice.get('message') or {}
        return {
            'content': msg.get('content') or '',
            'tool_calls': msg.get('tool_calls') or [],
            'message': msg,
            'raw': raw,
        }

    def chat(self, prompt: str, system: str = None, temperature: float = None) -> str:
        """单轮对话,返回回复文本。"""
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        return self.complete(messages, temperature=temperature)['content']

    def stream(self, prompt_or_messages, temperature: float = None
               ) -> Generator[str, None, None]:
        """流式输出。入参可以是 str(prompt) 或 messages list,逐 token yield 文本增量。"""
        if isinstance(prompt_or_messages, str):
            messages = [{'role': 'user', 'content': prompt_or_messages}]
        else:
            messages = list(prompt_or_messages)
        if not self.api_key:
            raise AgentError("未配置 API Key。", "AuthError")
        payload = self._build_payload(messages, temperature=temperature, stream=True)
        yield from _http_post_stream(self.base_url + '/chat/completions',
                                    payload, self._headers())


class AnthropicLLM:
    """Anthropic Claude 后端适配。

    API 端点 https://api.anthropic.com/v1/messages;
    请求头需要 x-api-key 和 anthropic-version: 2023-06-01;
    system 为顶层字段(不在 messages 里)。
    """

    provider = "anthropic"

    def __init__(self, model: str = None, api_key: str = None,
                 temperature: float = 0.7, max_tokens: int = 4096):
        self.model = model or (os.environ.get('ANTHROPIC_MODEL') or 'claude-3-5-sonnet-latest')
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = ANTHROPIC_BASE_URL

    def _headers(self) -> dict:
        return {
            'x-api-key': self.api_key or '',
            'anthropic-version': '2023-06-01',
        }

    @staticmethod
    def _split_system(messages: list):
        """把 messages 里的 system 消息抽出来作为顶层 system 字段,其余原样保留。"""
        sys_parts, rest = [], []
        for m in messages:
            if m.get('role') == 'system':
                sys_parts.append(m.get('content') or '')
            else:
                rest.append(m)
        return "\n".join(p for p in sys_parts if p), rest

    def complete(self, messages: list, temperature: float = None,
                 tools: list = None) -> dict:
        if not self.api_key:
            raise AgentError("未配置 ANTHROPIC_API_KEY 环境变量。", "AuthError")
        system, msgs = self._split_system(messages)
        payload = {
            'model': self.model,
            'messages': msgs,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature if temperature is None else temperature,
        }
        if system:
            payload['system'] = system
        if tools:
            payload['tools'] = tools
        raw = _http_post_json(self.base_url + '/messages', payload, self._headers())
        # Anthropic 返回 content: [{type: "text", text: ...}, ...]
        text_parts = []
        for block in raw.get('content') or []:
            if isinstance(block, dict) and block.get('type') == 'text':
                text_parts.append(block.get('text') or '')
        msg = {'role': 'assistant', 'content': ''.join(text_parts)}
        return {
            'content': msg['content'],
            'tool_calls': [],
            'message': msg,
            'raw': raw,
        }

    def chat(self, prompt: str, system: str = None, temperature: float = None) -> str:
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        return self.complete(messages, temperature=temperature)['content']

    def stream(self, prompt_or_messages, temperature: float = None
               ) -> Generator[str, None, None]:
        if isinstance(prompt_or_messages, str):
            messages = [{'role': 'user', 'content': prompt_or_messages}]
        else:
            messages = list(prompt_or_messages)
        if not self.api_key:
            raise AgentError("未配置 ANTHROPIC_API_KEY。", "AuthError")
        system, msgs = self._split_system(messages)
        payload = {
            'model': self.model,
            'messages': msgs,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature if temperature is None else temperature,
            'stream': True,
        }
        if system:
            payload['system'] = system
        yield from _http_post_stream(self.base_url + '/messages', payload,
                                    self._headers())


class LocalLLM(OpenAILLM):
    """本地模型适配(llama.cpp server / vLLM 等),协议与 OpenAI 兼容,直接复用 OpenAILLM。

    默认 base_url 指向 http://localhost:8080/v1。
    """

    provider = "local"

    def __init__(self, model: str = None, base_url: str = None,
                 api_key: str = None, temperature: float = 0.7):
        super().__init__(
            model=model or os.environ.get('AURORA_LOCAL_MODEL') or 'local-model',
            base_url=base_url or 'http://localhost:8080/v1',
            api_key=api_key or 'not-needed',
            temperature=temperature,
        )


# 全局单例缓存
_global_llm: Optional[OpenAILLM] = None


def LLM(model: str = None, base_url: str = None, api_key: str = None,
        temperature: float = 0.7, provider: str = None) -> OpenAILLM:
    """LLM 工厂函数,根据 provider 创建对应后端实例。

    provider 可选:'openai'(默认)/ 'anthropic' / 'local'。
    未显式指定时,若 base_url 指向 localhost 或 env 里有 ANTHROPIC_API_KEY,自动选择。
    """
    if provider is None:
        if base_url and ('localhost' in base_url or '127.0.0.1' in base_url):
            provider = 'local'
        elif ANTHROPIC_API_KEY and not (api_key or DEFAULT_API_KEY):
            provider = 'anthropic'
        else:
            provider = 'openai'

    if provider == 'anthropic':
        return AnthropicLLM(model=model, api_key=api_key, temperature=temperature)
    if provider == 'local':
        return LocalLLM(model=model, base_url=base_url, api_key=api_key,
                        temperature=temperature)
    return OpenAILLM(model=model, base_url=base_url, api_key=api_key,
                     temperature=temperature)


def get_llm(model: str = None, temperature: float = 0.7) -> OpenAILLM:
    """获取全局共享的 LLM 实例(惰性创建)。"""
    global _global_llm
    if _global_llm is None:
        _global_llm = LLM(model=model, temperature=temperature)
    elif model:
        _global_llm.model = model
    return _global_llm


# ---------------------------------------------------------------------------
# 工具系统
# ---------------------------------------------------------------------------

class Tool:
    """工具定义:名称 + 可调用 + 描述 + JSON Schema 参数。"""

    def __init__(self, name: str, func: Callable, description: str = "",
                 parameters: dict = None):
        self.name = name
        self.func = func
        self.description = description or (func.__doc__ or "").strip()
        # 缺省参数 schema:自由 dict
        self.parameters = parameters or {"type": "object", "properties": {}}

    def to_openai_spec(self) -> dict:
        """转成 OpenAI tools 参数格式。"""
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': self.parameters,
            },
        }

    def run(self, **kwargs) -> Any:
        """执行工具。"""
        return self.func(**kwargs)

    def __repr__(self):
        return f"<Tool {self.name}>"


class ToolRegistry:
    """全局工具注册表:register / lookup / list。"""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> Tool:
        self._tools[tool.name] = tool
        return tool

    def lookup(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def unregister(self, name: str) -> None:
        self._tools.pop(name, None)

    def list_tools(self) -> List[Tool]:
        return list(self._tools.values())

    def specs(self) -> List[dict]:
        return [t.to_openai_spec() for t in self._tools.values()]


# 全局默认注册表
tool_registry = ToolRegistry()


def _infer_parameters_from_signature(fn: Callable) -> dict:
    """从函数签名推断 JSON Schema(参数名 + 默认值 + 类型提示)。"""
    sig = inspect.signature(fn)
    properties: Dict[str, dict] = {}
    required: List[str] = []
    for pname, param in sig.parameters.items():
        if pname in ('self', 'cls'):
            continue
        spec: Dict[str, Any] = {}
        ann = param.annotation
        if ann is int:
            spec['type'] = 'integer'
        elif ann is float:
            spec['type'] = 'number'
        elif ann is bool:
            spec['type'] = 'boolean'
        else:
            spec['type'] = 'string'
        properties[pname] = spec
        if param.default is inspect.Parameter.empty:
            required.append(pname)
    return {
        'type': 'object',
        'properties': properties,
        'required': required,
    }


def tool_decorator(func: Callable = None, *, name: str = None,
                   description: str = None, parameters: dict = None,
                   auto_register: bool = True):
    """装饰器:把 Python 函数自动包装成 Tool 并注册到全局注册表。

    用法:
        @tool_decorator
        def add(a: int, b: int) -> int:
            \"\"\"两个数相加\"\"\"
            return a + b
    """
    def wrap(f: Callable) -> Tool:
        t = Tool(
            name=name or f.__name__,
            func=f,
            description=description or (f.__doc__ or "").strip(),
            parameters=parameters or _infer_parameters_from_signature(f),
        )
        # 把 Tool 对象挂在函数上,方便后续访问
        f._tool = t
        if auto_register:
            tool_registry.register(t)
        return t

    if func is not None and callable(func):
        return wrap(func)
    return wrap


# ---------------------------------------------------------------------------
# 记忆系统
# ---------------------------------------------------------------------------

class ConversationMemory:
    """短期对话记忆:维护消息列表,支持取最近 n 条。"""

    def __init__(self, max_messages: int = 200):
        self.max_messages = max_messages
        self._messages: List[dict] = []

    def add(self, role: str, content: str) -> None:
        """添加一条消息。role 通常是 'user' / 'assistant' / 'system' / 'tool'。"""
        self._messages.append({'role': role, 'content': content})
        if len(self._messages) > self.max_messages:
            # 保留 system 在前,再保留最近 max-1 条
            sys_msgs = [m for m in self._messages if m['role'] == 'system']
            rest = [m for m in self._messages if m['role'] != 'system']
            self._messages = sys_msgs + rest[-(self.max_messages - len(sys_msgs)):]

    def get_recent(self, n: int = 10) -> List[dict]:
        """取最近 n 条消息。"""
        return self._messages[-n:] if n else list(self._messages)

    def clear(self) -> None:
        self._messages.clear()

    def to_messages(self) -> List[dict]:
        """转为 LLM messages 格式(浅拷贝)。"""
        return [dict(m) for m in self._messages]

    def __len__(self):
        return len(self._messages)


class LongTermMemory:
    """长期记忆:纯 Python 词袋 + TF-IDF + 余弦相似度(不依赖 numpy/外部嵌入)。

    每条文档转成 {词: tfidf_weight} 字典向量,查询时与文档向量做点积和模长。
    """

    def __init__(self):
        self._docs: List[str] = []
        self._metadatas: List[dict] = []
        self._doc_freq: Dict[str, int] = {}   # 文档频率(用于 IDF)
        self._doc_vectors: List[Dict[str, float]] = []  # 缓存的 TF-IDF 向量

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """极简分词:小写化,按非字母数字字符切分。"""
        text = (text or "").lower()
        out, buf = [], []
        for ch in text:
            if ch.isalnum():
                buf.append(ch)
            else:
                if buf:
                    out.append("".join(buf))
                    buf = []
        if buf:
            out.append("".join(buf))
        return out

    def _tfidf_vector(self, tokens: List[str]) -> Dict[str, float]:
        """把 token 列表转成 TF-IDF 向量 dict。"""
        n_docs = max(len(self._docs), 1)
        # TF
        tf: Dict[str, float] = {}
        for tok in tokens:
            tf[tok] = tf.get(tok, 0.0) + 1.0
        # TF-IDF
        vec: Dict[str, float] = {}
        for tok, freq in tf.items():
            df = self._doc_freq.get(tok, 1)
            idf = math.log((1.0 + n_docs) / (1.0 + df)) + 1.0
            vec[tok] = (freq / max(len(tokens), 1)) * idf
        return vec

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        """余弦相似度:dot(a,b)/(||a||*||b||),小向量用 dict 直接算。"""
        if not a or not b:
            return 0.0
        # 选较小的 dict 做迭代,减少循环
        if len(a) > len(b):
            a, b = b, a
        dot = sum(v * b.get(k, 0.0) for k, v in a.items())
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def add(self, text: str, metadata: dict = None, **kwargs) -> None:
        """添加文档。metadata 字典,kwargs 也会合并进 metadata。"""
        tokens = self._tokenize(text)
        if not tokens:
            return
        meta = dict(metadata or {})
        meta.update(kwargs)
        self._docs.append(text)
        self._metadatas.append(meta)
        # 更新文档频率
        for tok in set(tokens):
            self._doc_freq[tok] = self._doc_freq.get(tok, 0) + 1
        # 重新计算全部向量(IDF 会随文档数变化,简化处理:重算)
        self._rebuild_vectors()

    def _rebuild_vectors(self) -> None:
        self._doc_vectors = [
            self._tfidf_vector(self._tokenize(doc)) for doc in self._docs
        ]

    def search(self, query: str, k: int = 3) -> List[dict]:
        """检索最相关的 k 条文档,返回 [{'text', 'metadata', 'score'}]。"""
        q_vec = self._tfidf_vector(self._tokenize(query))
        scored = []
        for i, d_vec in enumerate(self._doc_vectors):
            score = self._cosine(q_vec, d_vec)
            if score > 0:
                scored.append((score, i))
        scored.sort(reverse=True)
        results = []
        for score, idx in scored[:k]:
            results.append({
                'text': self._docs[idx],
                'metadata': self._metadatas[idx],
                'score': score,
            })
        return results

    def save(self, path: str) -> None:
        """持久化到 JSON 文件。"""
        data = {
            'docs': self._docs,
            'metadatas': self._metadatas,
            'doc_freq': self._doc_freq,
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def load(self, path: str) -> None:
        """从 JSON 文件加载。"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._docs = data.get('docs', [])
        self._metadatas = data.get('metadatas', [])
        self._doc_freq = data.get('doc_freq', {})
        self._rebuild_vectors()

    def __len__(self):
        return len(self._docs)


# ---------------------------------------------------------------------------
# Prompt 模板
# ---------------------------------------------------------------------------

class PromptTemplate:
    """提示词模板,使用 {variable} 占位符。

    用法:
        t = PromptTemplate("你好,{name}。今天{day}。", variables=['name', 'day'])
        t.format(name="元铎", day="周二")
    """

    def __init__(self, template: str, variables: List[str] = None):
        self.template = template
        self.variables = list(variables) if variables else self._extract_vars(template)

    @staticmethod
    def _extract_vars(template: str) -> List[str]:
        """从模板里提取 {var} 占位符(简单扫描)。"""
        vars_, i, n = [], 0, len(template)
        while i < n:
            if template[i] == '{':
                j = template.find('}', i)
                if j != -1:
                    vars_.append(template[i + 1:j])
                    i = j + 1
                    continue
            i += 1
        return vars_

    def format(self, **kwargs) -> str:
        """填充全部变量。"""
        return self.template.format(**kwargs)

    def partial(self, **kwargs) -> 'PromptTemplate':
        """部分填充:把已提供的变量替换掉,返回新模板(剩余变量继续用)。"""
        new_template = self.template
        for k, v in kwargs.items():
            new_template = new_template.replace("{" + k + "}", str(v))
        remaining = [v for v in self._extract_vars(new_template)]
        return PromptTemplate(new_template, variables=remaining)

    def __repr__(self):
        return f"<PromptTemplate vars={self.variables}>"


class FewShotTemplate:
    """Few-shot 模板:用一组示例 + 提示模板引导模型。

    examples: [{"input": "...", "output": "..."}, ...]
    template: PromptTemplate 或 str,最终格式化为
        示例 1: ... 输入... 输出...
        ...
        问题: {input}
    """

    def __init__(self, examples: List[dict], template,
                 example_template: str = "输入: {input}\n输出: {output}"):
        self.examples = examples
        if isinstance(template, str):
            self.template = PromptTemplate(template)
        else:
            self.template = template
        self.example_template = example_template

    def format(self, **kwargs) -> str:
        blocks = []
        for ex in self.examples:
            try:
                blocks.append(self.example_template.format(**ex))
            except Exception:
                blocks.append(str(ex))
        joined_examples = "\n\n".join(blocks)
        return self.template.format(examples=joined_examples, **kwargs)


# ---------------------------------------------------------------------------
# Chain 链
# ---------------------------------------------------------------------------

class LLMChain:
    """基础链:PromptTemplate + LLM → 输出文本。"""

    def __init__(self, prompt, llm: OpenAILLM = None, output_key: str = 'text'):
        if isinstance(prompt, str):
            self.prompt = PromptTemplate(prompt)
        else:
            self.prompt = prompt
        self.llm = llm or get_llm()
        self.output_key = output_key

    def run(self, **kwargs) -> str:
        """执行链:填充 prompt,调 LLM,返回文本。"""
        text = self.prompt.format(**kwargs)
        return self.llm.chat(text)


class TransformChain:
    """自定义变换链:把上一步输出经过 Python 函数变换后传给下一步。"""

    def __init__(self, fn: Callable, input_key: str = 'text',
                 output_key: str = 'text'):
        self.fn = fn
        self.input_key = input_key
        self.output_key = output_key

    def run(self, **kwargs) -> dict:
        value = kwargs.get(self.input_key, "")
        result = self.fn(value)
        out = dict(kwargs)
        out[self.output_key] = result
        return out


class SequentialChain:
    """顺序链:把多个链串起来执行,前一个的输出作为后一个的输入。"""

    def __init__(self, chains: List):
        self.chains = chains

    def run(self, **kwargs) -> str:
        ctx = dict(kwargs)
        for chain in self.chains:
            if isinstance(chain, LLMChain):
                # LLMChain.run 直接返回 str,把它塞进 ctx['text']
                text = chain.run(**ctx)
                ctx[chain.output_key] = text
            elif isinstance(chain, TransformChain):
                ctx = chain.run(**ctx)
            else:
                # 兼容任何带 run(...) 方法的对象
                result = chain.run(**ctx)
                if isinstance(result, str):
                    ctx['text'] = result
                elif isinstance(result, dict):
                    ctx.update(result)
        return ctx.get('text', '')


# ---------------------------------------------------------------------------
# RAG 管线
# ---------------------------------------------------------------------------

class RAG:
    """检索增强生成管线。

    嵌入:纯 Python TF-IDF(复用 LongTermMemory 的向量逻辑,但独立维护)。
    流程:add_document 分块 → chunk 存入向量索引 → retrieve 召回 → query 拼 prompt 调 LLM。
    """

    def __init__(self, retriever: LongTermMemory = None, llm: OpenAILLM = None,
                 chunk_size: int = 500, overlap: int = 50):
        self.memory = retriever or LongTermMemory()
        self.llm = llm or get_llm()
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, chunk_size: int = 500,
                   overlap: int = 50) -> List[str]:
        """按字符数分块,相邻块重叠 overlap 个字符。"""
        text = text or ""
        if chunk_size <= 0:
            return [text] if text else []
        step = max(1, chunk_size - overlap)
        chunks = []
        start = 0
        n = len(text)
        while start < n:
            end = min(start + chunk_size, n)
            chunks.append(text[start:end])
            if end >= n:
                break
            start += step
        return chunks

    def add_document(self, text: str, source: str = None) -> int:
        """添加文档,自动分块。返回新增块数。"""
        chunks = self.chunk_text(text, self.chunk_size, self.overlap)
        for i, chunk in enumerate(chunks):
            self.memory.add(chunk, metadata={
                'source': source,
                'chunk_index': i,
            })
        return len(chunks)

    def add_file(self, path: str) -> int:
        """从文件加载(.txt / .md)。"""
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.add_document(text, source=os.path.basename(path))

    def retrieve(self, query: str, k: int = 3) -> List[dict]:
        """检索相关块。"""
        return self.memory.search(query, k=k)

    def query(self, question: str, k: int = 3) -> str:
        """检索 + LLM 生成回答。"""
        hits = self.retrieve(question, k=k)
        if not hits:
            return self.llm.chat(question)
        context = "\n\n---\n\n".join(
            f"[来源 {i+1}] {h['text']}" for i, h in enumerate(hits)
        )
        prompt = (
            "请根据下面提供的上下文回答用户问题。如果上下文不足以回答,请直接说明。\n\n"
            f"上下文:\n{context}\n\n问题:{question}\n\n回答:"
        )
        return self.llm.chat(prompt)


# ---------------------------------------------------------------------------
# Agent 主类
# ---------------------------------------------------------------------------

# ReAct 提示词模板(Thought / Action / Observation 风格)
REACT_SYSTEM_TEMPLATE = (
    "你是一个使用工具解决问题的智能 Agent。请按以下循环思考:\n"
    "Thought: 分析当前情况,决定下一步做什么。\n"
    "Action: 选择可用工具并给出 JSON 参数。\n"
    "Observation: 工具返回结果。\n"
    "重复直到可以给出最终答案。\n"
    "可用工具:\n{tools_desc}\n"
    "当你不需要工具时,直接给出最终答案。"
)


class Agent:
    """Aurora Agent 主类:工具调用循环 + 记忆 + ReAct 模式。

    用法:
        agent = Agent(model="doubao-seed-1-6-250615", system_prompt="你是助手")
        agent.register_tool(my_tool)
        result = agent.run("北京今天天气怎么样?")
        # result = {'answer': ..., 'steps': ..., 'tool_calls': [...], 'messages': [...]}
    """

    def __init__(self, tools: List[Tool] = None, model: str = None,
                 system_prompt: str = None, max_steps: int = 10,
                 temperature: float = 0.3, memory: ConversationMemory = None,
                 llm: OpenAILLM = None, react_mode: bool = True):
        self.llm = llm or LLM(model=model, temperature=temperature)
        self.max_steps = max_steps
        self.temperature = temperature
        self.memory = memory or ConversationMemory()
        self.tools: Dict[str, Tool] = {}
        self.react_mode = react_mode
        self.system_prompt = system_prompt

        # 注册初始工具
        for t in (tools or []):
            if isinstance(t, Tool):
                self.register_tool(t)
            elif isinstance(t, dict):
                # 兼容 {name: callable} 字典
                for name, fn in t.items():
                    self.register_tool(Tool(name, fn))

    def register_tool(self, tool: Tool) -> Tool:
        """动态注册工具。"""
        if isinstance(tool, Tool):
            self.tools[tool.name] = tool
        elif isinstance(tool, Callable):  # type: ignore[arg-type]
            self.tools[tool.__name__] = Tool(tool.__name__, tool)
        return tool

    def _build_system_prompt(self) -> str:
        """组装 system prompt(自定义 + ReAct 模板)。"""
        parts = []
        if self.system_prompt:
            parts.append(self.system_prompt)
        if self.react_mode and self.tools:
            tool_lines = [f"- {t.name}: {t.description}" for t in self.tools.values()]
            parts.append(REACT_SYSTEM_TEMPLATE.format(
                tools_desc="\n".join(tool_lines)))
        return "\n\n".join(parts)

    def _tool_specs(self) -> List[dict]:
        return [t.to_openai_spec() for t in self.tools.values()]

    def run(self, prompt: str) -> dict:
        """主 Agent 循环:用户输入 → LLM 决策 → 工具调用 → 结果回填 → 最终回复。

        返回:{'answer', 'steps', 'tool_calls': [{'name','args','result'}], 'messages'}
        """
        system = self._build_system_prompt()
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})

        calls: List[dict] = []
        tool_specs = self._tool_specs() if self.tools else None

        for step in range(1, self.max_steps + 1):
            result = self.llm.complete(messages, temperature=self.temperature,
                                       tools=tool_specs)
            msg = result['message']
            content = result['content']
            tool_calls = result['tool_calls']

            if not tool_calls:
                return {
                    'answer': content,
                    'steps': step,
                    'tool_calls': calls,
                    'messages': messages + [msg],
                }

            # 把 assistant 的 tool_calls 消息追加进 messages
            messages.append(msg)
            for tc in tool_calls:
                fname = tc.get('function', {}).get('name', '')
                try:
                    args = json.loads(tc.get('function', {}).get('arguments') or '{}')
                except Exception:
                    args = {}
                tool = self.tools.get(fname)
                try:
                    if tool is None:
                        out = f"错误:未注册工具 {fname}"
                    else:
                        out = tool.run(**args) if isinstance(args, dict) else tool.run(args)
                except Exception as e:
                    out = f"工具错误: {e}"
                calls.append({'name': fname, 'args': args, 'result': out})
                messages.append({
                    'role': 'tool',
                    'tool_call_id': tc.get('id', f'tc{step}_{fname}'),
                    'content': json.dumps(out, ensure_ascii=False, default=str),
                })

        return {
            'answer': '(达到最大步数,未收敛)',
            'steps': self.max_steps,
            'tool_calls': calls,
            'messages': messages,
        }

    def chat(self, message: str) -> str:
        """带记忆的对话接口:消息进 memory,返回 assistant 回复。"""
        self.memory.add('user', message)
        result = self.run(message)
        answer = result['answer']
        self.memory.add('assistant', answer)
        return answer


# ---------------------------------------------------------------------------
# 冒烟测试
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("=" * 60)
    print("Aurora Agent 框架 — 冒烟测试")
    print("=" * 60)

    # 1. PromptTemplate
    t = PromptTemplate("你好,{name}!今天是{day}。", variables=['name', 'day'])
    assert t.format(name="元铎", day="周二") == "你好,元铎!今天是周二。"
    p = t.partial(name="元铎")
    assert "元铎" in p.format(day="周二")
    print("[OK] PromptTemplate")

    # 2. FewShotTemplate
    fs = FewShotTemplate(
        examples=[{'input': 'hi', 'output': '你好'}],
        template="示例:\n{examples}\n输入: {input}\n输出:",
    )
    out = fs.format(input="hello")
    assert "示例" in out and "hi" in out
    print("[OK] FewShotTemplate")

    # 3. 工具系统
    @tool_decorator
    def add(a: int, b: int) -> int:
        """两个整数相加"""
        return a + b

    assert isinstance(add, Tool)
    assert tool_registry.lookup('add').run(a=1, b=2) == 3
    print("[OK] Tool / tool_decorator / tool_registry")

    # 4. ConversationMemory
    mem = ConversationMemory()
    mem.add('user', '你好')
    mem.add('assistant', '你好呀')
    assert len(mem) == 2
    assert mem.get_recent(1)[0]['role'] == 'assistant'
    mem.clear()
    assert len(mem) == 0
    print("[OK] ConversationMemory")

    # 5. LongTermMemory(纯 Python TF-IDF)
    ltm = LongTermMemory()
    ltm.add("Aurora is a programming language", source="doc1")
    ltm.add("Python is a programming language too", source="doc2")
    ltm.add("Today is Tuesday in Beijing", source="doc3")
    hits = ltm.search("programming language", k=2)
    assert len(hits) >= 1
    assert "programming" in hits[0]['text'].lower()
    print(f"[OK] LongTermMemory (top hit score={hits[0]['score']:.3f})")

    # 6. RAG 分块 + 检索
    rag = RAG()
    chunks = rag.chunk_text("ABCDEFGHIJ" * 100, chunk_size=100, overlap=20)
    assert chunks[0].startswith("ABCDEFGHIJ")
    assert len(chunks) > 5
    rag.add_document("The capital of China is Beijing.")
    rag.add_document("Python was created by Guido van Rossum.")
    hits = rag.retrieve("capital city", k=1)
    assert "Beijing" in hits[0]['text']
    print("[OK] RAG chunk_text / retrieve")

    # 7. Chain
    chain = SequentialChain([
        TransformChain(lambda s: s.strip().upper(), input_key='text', output_key='text'),
    ])
    out = chain.run(text="  hello  ")
    assert out == "HELLO"
    print("[OK] TransformChain / SequentialChain")

    # 8. Agent 注册工具(不发网络请求)
    agent = Agent(
        tools=[Tool("echo", lambda msg: msg, "回显输入")],
        system_prompt="你是助手",
    )
    assert 'echo' in agent.tools
    print("[OK] Agent.register_tool")

    # 9. LLM 工厂(不发请求,只验证实例化)
    llm_local = LLM(provider='local', base_url='http://localhost:8080/v1')
    assert llm_local.provider == 'local'
    llm_oa = LLM(provider='openai')
    assert llm_oa.provider == 'openai'
    print("[OK] LLM factory (openai/local)")

    # 10. Anthropic 消息拆分
    sys_text, rest = AnthropicLLM._split_system([
        {'role': 'system', 'content': 'SYS'},
        {'role': 'user', 'content': 'HI'},
    ])
    assert sys_text == 'SYS' and rest[0]['role'] == 'user'
    print("[OK] AnthropicLLM._split_system")

    print("=" * 60)
    print("全部冒烟测试通过 ✔")
    print("=" * 60)
