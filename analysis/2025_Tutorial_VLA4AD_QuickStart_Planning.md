# VLA4AD Quick Start 技术分析报告

> **文档元数据**
> - **论文标题**：VLA4AD Quick Start: A hands-on repository for VLA-based autonomous driving
> - **作者**：curryqka（GitHub 用户）
> - **发表**：Tutorial / 开源项目（2025）
> - **arXiv**：https://arxiv.org/abs/2506.24044（相关综述）
> - **GitHub**：https://github.com/curryqka/quick-start-VLA4AD
> - **标签**：#2025 #Tutorial #VLA #Planning #Qwen2.5-VL #MS-Swift

---

## 一、模型组件

| 组件 | 具体实现 | 参数量 | 说明 |
|------|---------|--------|------|
| **Vision Encoder** | Qwen2.5-VL 内置 ViT | ~300M | Qwen2.5-VL 的视觉编码器，处理多相机图像 |
| **LLM** | Qwen2.5-VL-3B-Instruct | 3B | 基座 VLM，支持视觉-语言理解 |
| **Projector** | Qwen2.5-VL 内置 | - | 视觉-语言投影器（Qwen2.5-VL 自带） |
| **Action Head** | MLP Head（2层MLP） | ~10M | 将 LLM 最后一个 token 的隐藏状态映射为轨迹点 |
| **其他组件** | OmniDrive 数据转换器 | - | 将 nuScenes 轨迹数据转换为文本格式 |

---

## 二、参数状态

| 组件 | 冻结/训练 | 训练方法 | 可训参数占比 |
|------|----------|---------|-------------|
| **Vision Encoder** | 冻结 | - | 0%（`--freeze_vit true`） |
| **Projector** | 冻结 | - | 0%（Qwen2.5-VL 内置） |
| **LLM** | 冻结 + LoRA | LoRA r=8 | ~1% |
| **LLM-LoRA** | 训练 | LoRA r=8, α=32 | ~1% |
| **Action Head（MLP）** | 训练 | 全参 | ~0.3% |

**说明**：
- 基座模型使用 Qwen2.5-VL-3B-Instruct
- 训练时冻结 ViT，对 LLM 使用 LoRA 微调
- 轨迹预测头（MLP）随机初始化，全参训练
- 双任务训练：语言损失 + 轨迹损失（MSE）

---

## 三、微调方法

| 方法 | 应用位置 | 关键超参 | 说明 |
|------|---------|---------|------|
| **LoRA** | LLM 全线性层 | r=8, α=32, lr=1e-4 | 标准 LoRA 配置 |
| **全参训练** | MLP Head | lr=1e-4 | 轨迹预测头随机初始化，全参训练 |

**关键参数**：
- `--target_modules all-linear`：LoRA 挂载所有线性层
- `--freeze_vit true`：冻结视觉编码器
- `--gradient_accumulation_steps 16`：梯度累积
- `--max_length 2048`：最大序列长度

---

## 四、训练范式

| 阶段 | 目标 | 数据 | 损失函数 | 备注 |
|------|------|------|---------|------|
| **阶段1：SFT** | 视觉-语言-轨迹对齐 | OmniDrive VQA + 轨迹数据 | 语言损失（CE）+ 轨迹损失（MSE） | 双任务联合训练 |

**数据特点**：
- 使用 OmniDrive 数据集（基于 nuScenes）
- 包含 VQA 问答数据和轨迹数据
- 轨迹格式：6个时间步 × 2维（x, y）

---

## 五、技术定位

| 维度 | 定位 |
|------|------|
| **演进阶段** | Stage 3 — 动作原生型 VLA |
| **演进节点** | 模块化VLA模型（VLM + Action Head） |
| **技术路线** | Modular VLA |
| **核心创新** | 教程级实现，展示如何在 Qwen2.5-VL 上添加轨迹预测头，使用 MS-Swift 框架进行 VLA 训练 |
| **技术优势** | 1. 简单易懂，适合入门<br>2. 使用 MS-Swift 框架，训练流程标准化<br>3. 支持 LoRA 微调，显存友好 |
| **技术局限** | 1. 教程性质，非 SOTA 性能<br>2. 轨迹头简单（2层MLP），表达能力有限<br>3. 无 CoT 推理、无 RL 对齐 |

---

## 六、任务与数据集

| 维度 | 信息 |
|------|------|
| **核心任务** | 端到端自动驾驶规划（Planning） |
| **输入** | 多相机图像 + 语言指令 |
| **输出** | 轨迹点（6个时间步 × 2维：x, y） |
| **主要数据集** | OmniDrive（基于 nuScenes） |
| **评测指标** | 未定义（教程项目） |
| **性能排名** | 无（教程项目） |

---

## 七、复现信息

| 维度 | 信息 |
|------|------|
| **开源代码** | ✅ 有：https://github.com/curryqka/quick-start-VLA4AD |
| **预训练权重** | ❌ 无（需要自己训练） |
| **训练代码** | ✅ 有（基于 MS-Swift） |
| **推理代码** | ✅ 有（基于 MS-Swift） |
| **复现难度** | 低（教程级，步骤清晰） |
| **依赖环境** | Python ≥ 3.9, PyTorch ≥ 2.0, CUDA ≥ 11.7, ms-swift 3.10.x |
| **硬件需求** | 推理 ≥ 24GB GPU，训练 ≥ 48GB GPU |

---

## 八、关键图表

> 项目结构：
> - `modeling_qwen2_5_vla.py`：在 Qwen2.5-VL 上添加 MLP 轨迹头
> - `custom_model.py`：注册自定义模型到 MS-Swift
> - `custom_dataset.py`：自定义数据集加载
> - `convert_omnidrive.py`：OmniDrive 数据格式转换

---

## 九、总结

### 技术贡献
1. **教程级实现**：提供完整的 VLA4AD 入门教程，从数据准备到训练推理
2. **MS-Swift 集成**：展示如何将自定义 VLA 模型集成到 MS-Swift 框架
3. **双任务训练**：语言损失 + 轨迹损失联合训练

### 局限性
1. 教程性质，非 SOTA 性能
2. 轨迹头简单（2层MLP），表达能力有限
3. 无 CoT 推理、无 RL 对齐
4. 无预训练权重，需要自己训练

### 适用场景
- VLA4AD 入门学习
- 快速验证 VLA 概念
- 基于 MS-Swift 的二次开发

### 不适用场景
- 追求 SOTA 性能
- 需要 CoT 推理的场景
- 需要 RL 对齐的场景

---

## 十、与知识库对照

| 维度 | 本报告定位 | 知识库参考 |
|------|-----------|-----------|
| 演进阶段 | Stage 3 - 动作原生型 VLA | AD_演进框架.md |
| 技术路线 | Modular VLA | AD_演进框架.md |
| 微调方法 | LoRA + 全参 MLP | AD_模型训练要素.md |
| 训练范式 | SFT（双任务） | AD_模型训练要素.md |
| 任务类型 | Planning | AD_任务数据集与开源.md |
| 复现难度 | 低 | AD_开发工具生态.md |
