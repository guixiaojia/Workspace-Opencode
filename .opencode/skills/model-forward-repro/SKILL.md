---
name: model-forward-repro
description: 当用户提供 GitHub 模型仓库链接并要求"跑通/复现/前向传播/观察张量/加载模型到本地"时使用。标准化流程：登记克隆仓库、下载权重（ModelScope）、编写 build_model/build_input 兼容层、CPU/GPU 降级加载、前向采集 trace.json 与 model_structure.md。
---

# 模型前向复现（Skill A）

职责边界：本技能负责**跑通与采集**，产物是 `trace.json` + `model_structure.md`；后续的人工拆解讲解（walk-through.md）基于这两份素材撰写。目录规范与 trace.json schema 的唯一权威源是 `lab/README.md`，执行前先读它。

## 环境事实（勿重复探测）

- Python：`D:\anaconda3\envs\py311\python.exe`（transformers 4.57.6 / torch 2.11+cu126 / ms_swift 3.10.3）
- GPU：RTX 3050 4GB。经验规则：≥1B 模型直接 CPU bf16，不尝试 GPU
- 权重下载：`MODELSCOPE_CACHE=D:\anaconda3_cache\modelscope_cache`；CLI 入口是 `modelscope` 命令，若不可用则 `python -c "from modelscope import snapshot_download; snapshot_download('<id>')"`（不要用 `python -m modelscope`，会报 no module __main__）
- 后台大文件下载用 `(nohup ... > lab/<name>.log 2>&1 &)` 并与写代码并行

## 流程

1. **登记克隆**：`git clone --depth 1 <url> repos/<name>`；记录 `git rev-parse --short HEAD` 进 `repos/README.md` 表格。此后 repos/ 内零修改（含 README 也不改）。
2. **通读源码定入口**：找到模型主类（modeling_*.py）与真正的 forward 依赖。区分"训练框架胶水"（如 ms-swift 注册代码——通常因版本不匹配跑不了，**绕开它**，不要试图升级/降级框架去迁就）与"纯模型代码"（继承 transformers 基类的那部分，可直接用）。
3. **兼容性诊断**（先探测后动手）：
   ```
   python -c "from transformers import <BaseClass>; import inspect; print(inspect.signature(<BaseClass>.forward))"
   ```
   对照仓库 forward 的传参，列出差异清单（典型：transformers v5 移除了 output_attentions/output_hidden_states 形参、past_key_values 类型变更、rope_deltas 位置参数化）。详查 `references/transformers-compat.md`。
4. **写项目三件套**（位置规范见 lab/README.md 第 1、2 节）：
   - `lab/<proj>/config.yaml`
   - `lab/<proj>/build_model.py`：加载 config → 注入项目特有参数（如轨迹头维度）→ 实例化模型。若仓库类与当前 transformers 签名不兼容，在此文件内写桥接子类重写 forward，**不改 repos/ 文件**
   - `lab/<proj>/build_input.py`：走真实 processor/tokenizer（从权重目录加载）构造最小 batch，让 patch 化、坐标网格等前置变换也进入 trace，而不是手捏最终张量
5. **跑通用 `run_forward.py --project <proj>`**。验收标准：trace.json 生成、含 losses 字段、events 数 > 模型叶子模块数的 80%。
6. 更新 `lab/<proj>/outputs/README.md` 登记生成命令与时间。

## 降级链（按序尝试，每次降级须告知用户）

真实权重+CPU bf16 → 内存不足：真实权重+fp16 → 权重加载失败：`from_config` 随机初始化（trace 仍有效，shape 与真实一致，meta 里注明 random_init）→ 底座类不存在（transformers 太旧/太新）：仓库创新点模块 + 官方等价基类组合复现，或最简 nn.Module 复刻 + 文档注明偏离。

## 检查清单（结束前逐项过）

- [ ] repos/README.md 已登记 commit
- [ ] repos/ 目录 `git status` 干净
- [ ] trace.json 通过 lab/README.md schema 校验（meta 齐全）
- [ ] losses 有真实数值（language + 项目自定义头各自的值）
- [ ] outputs/README.md 已更新
