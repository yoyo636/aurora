# Aurora v3.0.0 AI 引擎性能对比报告

> 本报告所有数据均由 `benchmarks/ai_benchmark.py` 实际运行测量得出，非估算。
> 复现方式：`cd /Users/wuyuanduo/aurora && python3 benchmarks/ai_benchmark.py`

## 测试环境

| 项目 | 值 |
|---|---|
| 机器 | Apple Silicon（ARM64, `arm64`） |
| 系统 | macOS（Darwin 27.0.0） |
| Python 版本 | 3.14.7 |
| Aurora 版本 | 3.0.0 |
| NumPy | **未安装**（仅对比 Aurora Tensor vs 纯 Python 手写实现） |
| 测量方法 | `time.perf_counter()`，每项重复 3 次取平均（启动项 5 次） |

> 说明：当前环境没有 NumPy，因此无法给出 NumPy 列。脚本在检测到 NumPy 时会自动加入对比列。
> 为避免纯 Python 大矩阵过慢，按 agent 提示将矩阵规模从 1000×1000 缩小到 100×100、数据规模取 5000 行。

---

## 基准测试 1：张量元素运算（100×100 矩阵相加）

| 实现 | 耗时 | 相对纯 Python |
|---|---:|---:|
| Aurora Tensor | 2.75 ms | 0.11×（约慢 9 倍） |
| 纯 Python list 推导 | 0.31 ms | 1.00×（基准） |

**解读**：Aurora Tensor 的逐元素加法需要走广播解析（`_broadcast_shapes` + `_bc_strides` + 逐元素多维索引解码），额外的 shape/strides 管理开销在小张量上盖过了直接 `zip` 的速度。这是纯 Python 参考实现的典型开销。

## 基准测试 2：矩阵乘法（100×100 × 100×100）

| 实现 | 耗时 | 相对纯 Python |
|---|---:|---:|
| Aurora Tensor.matmul | 51.39 ms | 1.01× |
| 纯 Python 三重循环 | 52.01 ms | 1.00×（基准） |

**解读**：矩阵乘法是纯内存访存密集型三重循环，Aurora 实现把循环写得和手写三重循环几乎一样紧凑（带 i-k-j 缓存友好顺序），因此与手写纯 Python **基本持平**。这说明内核算法本身没有低效之处，瓶颈在解释器而非算法。

## 基准测试 3：通用函数（10 万元素上的 sigmoid + relu + exp）

| 实现 | 耗时 | 相对纯 Python |
|---|---:|---:|
| Aurora Tensor | 18.43 ms | 0.84× |
| 纯 Python math 循环 | 15.55 ms | 1.00×（基准） |

**解读**：逐元素一元函数在两条路径上都跑同一个 `math.exp/sigmoid` 内核，Aurora 多出一次 list 推导包装，因此略慢约 16%。

## 基准测试 4：数据处理（5000 行 DataFrame）

| 操作 | Aurora DataFrame | 纯 Python dict 列表 | 相对纯 Python |
|---|---:|---:|---:|
| groupby + mean | 2.78 ms | 1.10 ms | 0.40× |
| filter（`x > 0.5`） | 1.28 ms | 0.14 ms | 0.11× |
| standardize（Z-score） | 12.00 ms | 0.62 ms | 0.05× |

**解读**：DataFrame 是通用库——`filter` 会把每行 dict 拷贝成新 dict、再构造新 DataFrame（重建列顺序、index）；`standardize` 遍历每列并逐行写回。这些"正确性开销"在手写一次性脚本里可以省掉，所以通用 API 比硬编码循环慢 5–20 倍。这是所有 DataFrame 类库（pandas 相对裸 NumPy 也是类似差距）的通病。

## 基准测试 5：启动时间

| 进程 | 耗时 |
|---|---:|
| `python3 -c "pass"`（空解释器） | 25.21 ms |
| `python3 -c "import aurora; import aurora.ai"` | 51.76 ms |

**解读**：`import aurora.ai` 比空 Python 多花约 26 ms，主要来自一次性加载 6 个 AI 模块（约 19 万字符源码）的解析开销。这是 Python 解释器固有成本——**未来 Aurora 编译为原生 ARM64 可执行文件后，启动时间目标是 2ms 量级，从根本上消除该开销**。

---

## 结论

### 当前实现定位
当前 `aurora/ai/` 是**纯 Python 参考实现**（reference implementation），目标是：
1. 用可执行代码完整定义 AI 引擎的语义、API 和算法正确性（33 个单元测试全部通过）；
2. 作为未来 ARM64 原生后端编译的"黄金参考"，用于验证编译结果数值正确。

从实测看：
- **矩阵乘法**已与手写纯 Python 持平——算法内核无冗余；
- **逐元素运算 / DataFrame**比硬编码纯 Python 慢 5–20 倍，瓶颈是 Python 解释器的循环开销与通用 API 的正确性拷贝，**不是算法问题**；
- **启动**受 Python 解释器加载成本支配。

这与任务提示的判断一致：纯 Python 参考实现阶段不应期待性能领先，它的价值在语义与正确性。

### Aurora 的理论性能优势（未来）
1. **原生性能**：张量运算经 ARM64 后端编译为机器码后，逐元素/BLAS 内核可利用 SIMD 与缓存，预期相对纯 Python 参考实现获得 **10–100×** 加速；
2. **零依赖部署**：模型 + 运行时编译为单个原生可执行文件，无需 Python，启动从 ~50ms 降到 ~2ms；
3. **类型/形状系统**：编译期完成 shape 检查后，运行时无需广播解析，Elementwise 开销可进一步消除；
4. **统一栈**：训练、推理、Agent 在同一语言内，避免 Python↔C 扩展的数据往返。

### 优化路线图
| 阶段 | 目标 | 预期收益 |
|---|---|---|
| v3.0.x | 纯 Python 参考实现 + 完整测试 | 语义冻结、正确性验证（本版本） |
| v3.1 | 张量内核接入可选 NumPy 后端（`from_numpy`/`to_numpy` 已预留） | 逐元素/BLAS 即时提速 10–50× |
| v3.2 | ARM64 原生 codegen（asmgen 已存在）替换纯 Python 循环 | 矩阵乘法接近 BLAS 水平，启动降至 ms 级 |
| v3.3 | 编译期 shape 推断 + 静态广播折叠 | 消除运行时 shape/strides 解析开销 |
| v4.0 | 端到端原生模型编译（.aur → 可执行文件） | 零依赖部署 + 2ms 启动目标 |

---

## 复现命令

```bash
cd /Users/wuyuanduo/aurora
python3 benchmarks/ai_benchmark.py        # 本报告全部数字来源
python3 -m pytest tests/test_ai_engine.py -v   # 33 个测试
```
