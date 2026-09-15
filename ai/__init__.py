"""Aurora AI 原生引擎 — 打破 Python 在 AI 领域垄断的核心模块

包含 7 大模块:
- tensor:  原生张量计算库 (AuroraTensor)
- autograd: 自动微分引擎 (AuroraAutograd)
- nn:      神经网络 DSL (AuroraNN)
- data:    数据处理库 (AuroraData)
- agent:   LLM Agent 框架 (AuroraAgent)
- inference: 模型推理引擎 (AuroraInference)
- kernel:  Jupyter 内核 (AuroraKernel)
"""

__version__ = "3.0.0"
__all__ = ["tensor", "autograd", "nn", "data", "agent", "inference", "kernel"]
