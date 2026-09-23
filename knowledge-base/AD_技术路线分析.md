# 技术路线分析

> 自动驾驶基础模型的 6 种主要技术路线，及其模块组合与对比分析。

---

## 技术路线总览

| 技术路线 | 核心特征 | 典型技术 | 论文数量 | 覆盖Stage | 优势 | 挑战 |
|----------|----------|----------|----------|-----------|------|------|
| **BEV-VLM** | BEV表征 + VLM | BEVFormer + LLM | 85篇 (21%) | Stage 1-2 | 成熟的BEV技术、强大的语义理解、良好的可解释性 | 计算复杂度高、实时性受限、模块间信息损失 |
| **End-to-End VLA** | 传感器直出动作 | Action Head、Flow Matching | 120篇 (30%) | Stage 1-3 | 端到端优化、最小化信息损失、潜在最优性能 | 数据需求大、可解释性差、安全验证困难 |
| **Modular VLA** | 模块化VLA | VLM + Action Head | 75篇 (19%) | Stage 2-3 | 模块可复用、易于调试、平衡性能与可解释性 | 模块间接口设计、信息瓶颈、端到端优化困难 |
| **Reasoning VLA** | 显式推理 + 动作 | CoT + VLA | 45篇 (11%) | Stage 4-6 | 可解释的决策过程、复杂场景处理、人类对齐性好 | 推理延迟高、推理质量不稳定、训练数据稀缺 |
| **World Model VLA** | 世界模型 + 动作 | DiT + VLA | 55篇 (14%) | Stage 5-6 | 未来预测能力、数据增强潜力、仿真到现实迁移 | 世界模型准确性、计算资源需求、预测误差累积 |
| **Unified VLA** | 统一联合空间 | 联合潜空间 | 20篇 (5%) | Stage 6 | 理论最优性能、信息无损融合、端到端可微 | 训练难度极大、架构设计复杂、工程实现困难 |

---

## 模块类型说明

| 模块类型 | 功能 | 典型实现 | 输入类型 | 输出类型 | 参数规模 |
|----------|------|----------|----------|----------|----------|
| **Visual Encoder** | 图像特征提取 | ViT-L/14, CLIP, DINOv2, SigLIP | 图像 [B, 3, H, W] | 视觉特征 [B, N, D] | 300M-400M |
| **LiDAR Encoder** | 点云特征提取 | VoxelNet, PointPillars, CenterPoint | 点云 [B, N, 4] | 点云特征 [B, M, C] | 50M-200M |
| **BEV Encoder** | 生成BEV表征 | BEVFormer, BEVDet, LSS, BEVFusion | 多视角特征 | BEV特征 [B, C, H, W] | 50M-100M |
| **LLM/VLM** | 语言理解与生成 | LLaMA, Qwen2.5, Vicuna, Phi-3 | 语言token序列 | 语言输出/特征 | 0.5B-72B |
| **Projector** | 特征对齐 | MLP, Cross-Attention, Q-Former | 视觉特征 | 语言空间特征 | 10M-50M |
| **Action Head** | 动作/轨迹输出 | MLP, GMM, Flow Matching, Diffusion | 融合特征 | 轨迹 [B, T, 2] 或 动作 | 10M-50M |
| **CoT Module** | 显式推理链生成 | Self-Reflect, Tree-of-Thought | VLM输出 | 推理链文本 | - (LLM内置) |
| **World Model** | 未来状态预测 | DiT, Diffusion, GPT, Sora-like | 当前状态+动作 | 预测未来状态 | 1B-7B |
| **Memory Module** | 历史信息存储 | RNN, Transformer KV-Cache, External Memory | 历史序列 | 融合后特征 | 可变 |

---

## 技术路线 × 模块组合

| 技术路线 | Visual Encoder | LiDAR Encoder | BEV Encoder | LLM/VLM | Projector | Action Head | CoT Module | World Model | 典型微调方式 |
|----------|----------------|---------------|-------------|---------|-----------|-------------|------------|-------------|--------------|
| **BEV-VLM** | ✅ ViT-L/14 | ⚠️ 可选 | ✅ BEVFormer | ✅ LLaMA/Qwen | ✅ MLP | ⚠️ 规划头 | ❌ | ❌ | 冻结VLM，微调BEV+规划头 |
| **End-to-End VLA** | ✅ ViT-L/14 | ⚠️ 可选 | ❌ | ❌ | ❌ | ✅ MLP/Flow | ❌ | ❌ | 全参微调或冻结Encoder |
| **Modular VLA** | ✅ ViT-L/14 | ⚠️ 可选 | ❌ | ✅ Qwen2.5 | ✅ MLP | ✅ MLP | ❌ | ❌ | LoRA微调LLM，冻结VLM |
| **Reasoning VLA** | ✅ ViT-L/14 | ⚠️ 可选 | ❌ | ✅ Qwen2.5 | ✅ MLP | ✅ MLP | ✅ LLM内置 | ❌ | LoRA微调LLM，全参微调CoT |
| **World Model VLA** | ✅ ViT-L/14 | ⚠️ 可选 | ❌ | ✅ Qwen2.5 | ✅ MLP | ✅ MLP | ❌ | ✅ DiT | 冻结VLM，微调World Model |
| **Unified VLA** | ✅ | ✅ | ❌ | 统一编码 | 统一 | 统一 | 统一 | 统一 | 端到端全参微调 |

---

## 技术路线对比

| 维度 | BEV-VLM | E2E VLA | Modular VLA | Reasoning VLA | WM VLA | Unified VLA |
|------|---------|---------|-------------|---------------|--------|-------------|
| **模块数量** | 5-6个 | 2-3个 | 4-5个 | 5-6个 | 5-6个 | 1个统一 |
| **端到端程度** | ⚠️ 半端到端 | ✅ 完全端到端 | ⚠️ 模块化 | ⚠️ 模块化 | ⚠️ 模块化 | ✅ 完全端到端 |
| **可解释性** | ✅ 良好 | ❌ 差 | ✅ 良好 | ✅ 优秀 | ⚠️ 中等 | ⚠️ 待研究 |
| **推理延迟** | ⚠️ 中等 | ✅ 低 | ⚠️ 中等 | ❌ 高 | ❌ 高 | ⚠️ 待研究 |
| **训练难度** | ⚠️ 中等 | ⚠️ 中等 | ✅ 较低 | ⚠️ 中等 | ❌ 高 | ❌ 极高 |
| **数据需求** | ⚠️ 中等 | ❌ 大 | ⚠️ 中等 | ❌ 大 | ❌ 大 | ❌ 极大 |
| **部署友好度** | ✅ 好 | ✅ 好 | ✅ 好 | ⚠️ 中等 | ⚠️ 中等 | ❌ 差 |
| **代表Stage** | 1-2 | 1-3 | 2-3 | 4-6 | 5-6 | 6 |

---

## 相关文档

| 文档 | 内容 | 用途 |
|------|------|------|
| [AD_技术演进框架.md](./AD_技术演进框架.md) | 六阶段定义、边界判断、坐标型框架图 | 论文技术定位时参考 |
| [AD_显存估算框架.md](./AD_显存估算框架.md) | 组件级显存表、速查矩阵、硬件采购建议 | 评估显存需求时参考 |
| [AD_模型训练要素.md](./AD_模型训练要素.md) | 参数状态、微调方法、训练范式 | 训练模型时参考 |
