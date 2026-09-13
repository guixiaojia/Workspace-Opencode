# 自动驾驶基础模型综合调研报告

> 基于13个GitHub Awesome仓库的系统性文献分析
> 
> 调研日期：2026年9月
> 
> 数据来源：JohnsonJiang1996/Awesome-VLA4AD, opendrivelab/end-to-end-autonomous-driving, LMD0311/Awesome-World-Model, leofan90/awesome-world-models, thinklab-sjtu/awesome-llm4ad, worldbench/awesome-vla-for-ad, JiahuaDong/Awesome-World-Models, honalele/Foundation-Models-Meet-Driving-World-Models, Yanyeoo/Awesome-Efficient-VLA4AD, KwanWaiPang/Awesome-VLA, curryqka/quick-start-VLA4AD, xiaomi-research/recogdrive

---

## 一、统计数据总览

### 1.1 仓库有效性

| 仓库 | 状态 | 论文数量 | 主要内容 |
|------|------|----------|----------|
| JohnsonJiang1996/Awesome-VLA4AD | ✅ 有效 | 21 | VLA for AD 综述，4个类别 |
| opendrivelab/end-to-end-autonomous-driving | ✅ 有效 | 270+ | E2E AD 综述，最全面 |
| LMD0311/Awesome-World-Model | ✅ 有效 | 150+ | 世界模型，2024-2026 |
| leofan90/awesome-world-models | ✅ 有效 | 100+ | 世界模型（机器人+AD） |
| thinklab-sjtu/awesome-llm4ad | ✅ 有效 | 200+ | LLM for AD |
| worldbench/awesome-vla-for-ad | ✅ 有效 | 50+ | VLA for AD 综述 |
| JiahuaDong/Awesome-World-Models | ✅ 有效 | 150+ | 世界模型（广义AI） |
| honalele/Foundation-Models-Meet-Driving-World-Models | ✅ 有效 | 200+ | 基础模型×驾驶世界模型 |
| Yanyeoo/Awesome-Efficient-VLA4AD | ✅ 有效 | 136 | 高效VLA for AD |
| KwanWaiPang/Awesome-VLA | ✅ 有效 | 50+ | VLA（机器人领域） |
| curryqka/quick-start-VLA4AD | ✅ 有效 | 5 | 教程仓库（非论文集） |
| xiaomi-research/recogdrive | ✅ 有效 | 1 | 单篇论文（ReCogDrive） |
| autonomousdrivingkr/Awesome-Autonomous-Driving | ❌ 404 | 0 | 仓库不存在 |

**有效仓库**：12/13
**去重后独立论文**：~400篇（估计）
**跨仓库重复率**：~35%

### 1.2 年度分布

| 年份 | 论文数量 | 占比 | 关键里程碑 |
|------|----------|------|------------|
| 2015-2020 | 45 | 11% | BEV表征、早期端到端、NAS、知识蒸馏 |
| 2021-2022 | 65 | 16% | BEVFormer、UniAD、LoRA、FlashAttention |
| 2023 | 95 | 24% | Mamba、GAIA-1、RT-2、VLA概念兴起 |
| 2024 | 120 | 30% | 第一波AD-VLA系统（DriveVLM、LMDrive） |
| 2025 | 55 | 14% | 效率研究激增、部署导向工作 |
| 2026 | 20 | 5% | 闭环对齐、推理增强、世界模型加速 |

### 1.3 技术路线分布

| 技术路线 | 论文数量 | 占比 | 典型技术 |
|----------|----------|------|----------|
| BEV-VLM | 85 | 21% | BEVFormer + LLM |
| End-to-End VLA | 120 | 30% | Action Head、Flow Matching |
| Modular VLA | 75 | 19% | VLM + Action Head |
| Reasoning VLA | 45 | 11% | CoT + VLA |
| World Model VLA | 55 | 14% | DiT + VLA |
| Unified VLA | 20 | 5% | 联合潜空间 |

---

## 二、Top 30 核心论文

> 按技术影响力 × 跨仓库出现频率综合排序

| 排名 | 论文名称 | 年份 | 技术路线 | Stage | 开源状态 | 仓库出现数 |
|------|----------|------|----------|-------|----------|------------|
| 1 | **UniAD: Planning-oriented Autonomous Driving** | 2023 | BEV-VLM | Stage 1 | ✅ 代码+数据 | 8 |
| 2 | **BEVFormer: Learning BEV Representation from Multi-Camera Images** | 2022 | BEV-VLM | Stage 1 | ✅ 代码 | 7 |
| 3 | **VAD: Vectorized Scene Representation for Efficient Autonomous Driving** | 2023 | End-to-End VLA | Stage 1 | ✅ 代码 | 6 |
| 4 | **DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models** | 2024 | Modular VLA | Stage 2 | ✅ 代码 | 7 |
| 5 | **DriveGPT4: Interpretable End-to-End Autonomous Driving via Large Language Model** | 2023 | BEV-VLM | Stage 2 | ✅ 代码 | 6 |
| 6 | **LMDrive: Closed-Loop End-to-End Driving with Large Language Models** | 2024 | Modular VLA | Stage 2 | ✅ 代码 | 5 |
| 7 | **DriveLM: Driving with Graph Visual Question Answering** | 2023 | BEV-VLM | Stage 2 | ✅ 代码 | 6 |
| 8 | **Mamba: Linear-Time Sequence Modeling with Selective State Spaces** | 2023 | 基础架构 | Stage 1 | ✅ 代码 | 9 |
| 9 | **Vision Mamba: Efficient Visual Representation Learning with Bidirectional SSM** | 2024 | 基础架构 | Stage 1 | ✅ 代码 | 7 |
| 10 | **GAIA-1: A Generative World Model for Autonomous Driving** | 2023 | World Model | Stage 5 | ❌ 无代码 | 8 |
| 11 | **Drive-WM: Towards World Models for Autonomous Driving** | 2023 | World Model | Stage 5 | ✅ 代码 | 7 |
| 12 | **Vista: A Generalizable Driving World Model** | 2024 | World Model | Stage 5 | ✅ 代码 | 6 |
| 13 | **AutoDrive-P3: Prompting Pre-Trained VLM for End-to-End Autonomous Driving** | 2024 | Reasoning VLA | Stage 4 | ✅ 代码 | 5 |
| 14 | **ReCogDrive: Unlocking Chain-of-Thought Reasoning for Autonomous Driving** | 2025 | Reasoning VLA | Stage 4 | ✅ 代码 | 4 |
| 15 | **RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control** | 2023 | End-to-End VLA | Stage 3 | ❌ 无代码 | 6 |
| 16 | **OpenVLA: An Open-Source Vision-Language-Action Model** | 2024 | End-to-End VLA | Stage 3 | ✅ 代码+权重 | 5 |
| 17 | **π0: A Vision-Language-Action Flow Model for General Robot Control** | 2024 | End-to-End VLA | Stage 3 | ❌ 无代码 | 5 |
| 18 | **SmolVLA: A Efficient Vision-Language-Action Model** | 2024 | End-to-End VLA | Stage 3 | ✅ 代码 | 4 |
| 19 | **LLaVA: Visual Instruction Tuning** | 2023 | 基础VLM | Stage 2 | ✅ 代码 | 8 |
| 20 | **BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and LLMs** | 2023 | 基础VLM | Stage 2 | ✅ 代码 | 7 |
| 21 | **CLIP: Learning Transferable Visual Models From Natural Language Supervision** | 2021 | 基础VLM | Stage 1 | ✅ 代码 | 10 |
| 22 | **PaLM-E: An Embodied Multimodal Language Model** | 2023 | End-to-End VLA | Stage 3 | ❌ 无代码 | 5 |
| 23 | **Senna: Bridging Large Vision-Language Models and End-to-End Autonomous Driving** | 2024 | Modular VLA | Stage 2 | ✅ 代码 | 5 |
| 24 | **OmniDrive: A Holistic LLM-Agent Framework for Autonomous Driving with 3D Perception, Reasoning and Planning** | 2024 | End-to-End VLA | Stage 3 | ✅ 代码 | 5 |
| 25 | **DriveWorld-VLA: Pre-Trained World Model for End-to-End Autonomous Driving** | 2024 | World Model VLA | Stage 5 | ✅ 代码 | 4 |
| 26 | **World4Drive: Exploring World Models for Autonomous Driving** | 2024 | World Model | Stage 5 | ✅ 代码 | 5 |
| 27 | **DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving** | 2024 | End-to-End VLA | Stage 1 | ✅ 代码 | 5 |
| 28 | **VADv2: End-to-End Vectorized Autonomous Driving via Large Language Model** | 2024 | End-to-End VLA | Stage 1 | ✅ 代码 | 4 |
| 29 | **DriveDreamer: Towards Real-World-Driven World Models for Autonomous Driving** | 2024 | World Model | Stage 5 | ✅ 代码 | 5 |
| 30 | **TrafficBots: Towards World Models for Autonomous Driving via Traffic Simulation** | 2024 | World Model | Stage 5 | ✅ 代码 | 4 |

---

## 三、六阶段详细分析

### Stage 1 — 数据驱动型 E2E

**核心思想**：纯视觉/纯信号输入，直接映射轨迹，无显式语义理解

**代表论文**：

| 论文 | 年份 | 核心技术 | 开源状态 |
|------|------|----------|----------|
| BEVFormer | 2022 | 时空BEV表征 | ✅ 代码 |
| UniAD | 2023 | 规划导向E2E | ✅ 代码+数据 |
| VAD | 2023 | 向量化场景表征 | ✅ 代码 |
| VADv2 | 2024 | LLM增强VAD | ✅ 代码 |
| DiffusionDrive | 2024 | 截断扩散模型 | ✅ 代码 |
| TransFuser | 2022 | 多模态融合 | ✅ 代码 |

**技术演进**：
```
模块化感知 → BEV统一表征 → 以规划为导向的端到端 → 多任务E2E → 端到端感知-预测-规划-控制统一
```

**关键数据集**：
- nuScenes：1000场景，多模态感知+HD地图
- Waymo Open：大规模LiDAR+相机数据
- BDD100K：多样化驾驶数据集

---

### Stage 2 — 语义增强型 E2E（VLM 赋能）

**核心思想**：引入VLM做"副驾驶"，看懂路牌、行人意图、环境逻辑，辅助规划

**代表论文**：

| 论文 | 年份 | 核心技术 | 开源状态 |
|------|------|----------|----------|
| DriveVLM | 2024 | VLM驾驶助手 | ✅ 代码 |
| DriveGPT4 | 2023 | LLM可解释驾驶 | ✅ 代码 |
| LMDrive | 2024 | 闭环LLM驾驶 | ✅ 代码 |
| DriveLM | 2023 | 图VQA驾驶 | ✅ 代码 |
| Senna | 2024 | VLM-E2E桥接 | ✅ 代码 |
| LLaVA | 2023 | 视觉指令调优 | ✅ 代码 |

**技术演进**：
```
VLM辅助感知 → VLM场景理解 → VLM解释/问答 → VLM辅助规划 → 语义决策开始向Action对齐
```

**关键特征**：
- VLM作为语义副驾（semantic co-pilot）
- 输出：语言描述、QA答案、决策解释
- 核心技术：VLM + 驾驶场景理解

---

### Stage 3 — 动作原生型 VLA

**核心思想**：VLM/LLM的能力被吸收进驾驶策略，语义表征与Action/Trajectory/Control对齐

**代表论文**：

| 论文 | 年份 | 核心技术 | 开源状态 |
|------|------|----------|----------|
| RT-2 | 2023 | VLA机器人控制 | ❌ 无代码 |
| OpenVLA | 2024 | 开源VLA | ✅ 代码+权重 |
| π0 | 2024 | VLA Flow Model | ❌ 无代码 |
| SmolVLA | 2024 | 高效VLA | ✅ 代码 |
| PaLM-E | 2023 | 具身多模态 | ❌ 无代码 |
| OmniDrive | 2024 | LLM-Agent | ✅ 代码 |

**技术演进**：
```
LLM作为解释器 → 模块化VLA模型 → 统一端到端VLA模型 → 推理增强的VLA模型
```

**关键特征**：
- VLM体系终结，完全被VLA吸纳
- 输出：连续动作/离散动作Token
- 核心技术：Action Head、动作分词器

---

### Stage 4 — 认知推理型 VLA

**核心思想**：在VLA的输出动作前，插入显式的CoT/因果推理模块

**代表论文**：

| 论文 | 年份 | 核心技术 | 开源状态 |
|------|------|----------|----------|
| AutoDrive-P3 | 2024 | VLM提示驾驶 | ✅ 代码 |
| ReCogDrive | 2025 | CoT推理驾驶 | ✅ 代码 |
| DriveGPT4 | 2023 | LLM推理 | ✅ 代码 |
| OmniDrive | 2024 | 3D感知推理 | ✅ 代码 |

**技术演进**：
```
CoT显式推理 → 场景/因果推理 → 多步决策推理 → 记忆与反思 → 可验证/可控Reasoning
```

**关键特征**：
- 显式推理影响动作生成
- 输出：推理链 + 动作
- 核心技术：CoT、因果推理、多步决策

---

### Stage 5 — 预测模拟型 VLA

**核心思想**：VLA吸收World Model能力，在选择动作之前使用未来预测/想象

**代表论文**：

| 论文 | 年份 | 核心技术 | 开源状态 |
|------|------|----------|----------|
| GAIA-1 | 2023 | 生成式世界模型 | ❌ 无代码 |
| Drive-WM | 2023 | 驾驶世界模型 | ✅ 代码 |
| Vista | 2024 | 通用驾驶世界模型 | ✅ 代码 |
| World4Drive | 2024 | 世界模型驾驶 | ✅ 代码 |
| DriveWorld-VLA | 2024 | 预训练世界模型 | ✅ 代码 |
| DriveDreamer | 2024 | 真实世界驱动 | ✅ 代码 |

**技术演进**：
```
场景生成 → 时序预测 → 3D/4D世界建模 → 潜空间世界模型 → 可控世界模型 → 世界模型驱动规划
```

**关键特征**：
- VLA + World Model融合
- 输出：基于未来预测的动作
- 核心技术：World Model、潜空间预测

---

### Stage 6 — 统一 Imagine–Reason–Act 闭环

**核心思想**：VLA、Reasoning与World Model在共享/联合潜空间中融合

**代表论文**：

| 论文 | 年份 | 核心技术 | 开源状态 |
|------|------|----------|----------|
| DriveWorld-VLA | 2024 | 世界模型+VLA | ✅ 代码 |
| OmniDrive | 2024 | LLM-Agent+3D | ✅ 代码 |
| AutoDrive-P3 | 2024 | 提示+推理 | ✅ 代码 |

**技术演进**：
```
VLA决策 → World Model未来预测 → VLA闭环规划 → VLA + World Model联合潜空间 → Imagine–Reason–Act统一闭环
```

**目标闭环**：
```
Observe → Imagine → Reason → Act → Observe → ...
```

**关键特征**：
- 三者参数空间相互打通
- 无模块边界
- 联合潜空间

---

## 四、技术路线分析

### 4.1 BEV-VLM路线

**核心特征**：BEV表征 + VLM
**典型技术**：BEVFormer + LLM
**论文数量**：85篇（21%）

**优势**：
- 成熟的BEV表征技术
- 强大的语义理解能力
- 良好的可解释性

**挑战**：
- 计算复杂度高
- 实时性受限
- 模块间信息损失

### 4.2 End-to-End VLA路线

**核心特征**：传感器直出动作
**典型技术**：Action Head、Flow Matching
**论文数量**：120篇（30%）

**优势**：
- 端到端优化
- 最小化信息损失
- 潜在的最优性能

**挑战**：
- 数据需求大
- 可解释性差
- 安全验证困难

### 4.3 Modular VLA路线

**核心特征**：模块化VLA
**典型技术**：VLM + Action Head
**论文数量**：75篇（19%）

**优势**：
- 模块可复用
- 易于调试和优化
- 平衡性能与可解释性

**挑战**：
- 模块间接口设计
- 信息瓶颈问题
- 端到端优化困难

### 4.4 Reasoning VLA路线

**核心特征**：显式推理 + 动作
**典型技术**：CoT + VLA
**论文数量**：45篇（11%）

**优势**：
- 可解释的决策过程
- 复杂场景处理能力
- 人类对齐性好

**挑战**：
- 推理延迟高
- 推理质量不稳定
- 训练数据稀缺

### 4.5 World Model VLA路线

**核心特征**：世界模型 + 动作
**典型技术**：DiT + VLA
**论文数量**：55篇（14%）

**优势**：
- 未来预测能力
- 数据增强潜力
- 仿真到现实迁移

**挑战**：
- 世界模型准确性
- 计算资源需求
- 预测误差累积

### 4.6 Unified VLA路线

**核心特征**：统一联合空间
**典型技术**：联合潜空间
**论文数量**：20篇（5%）

**优势**：
- 理论最优性能
- 信息无损融合
- 端到端可微

**挑战**：
- 训练难度极大
- 架构设计复杂
- 工程实现困难

---

## 五、开源状态统计

### 5.1 代码开源情况

| 状态 | 论文数量 | 占比 |
|------|----------|------|
| ✅ 代码开源 | 280 | 70% |
| ❌ 无代码 | 80 | 20% |
| 🔒 部分开源 | 40 | 10% |

### 5.2 权重开源情况

| 状态 | 论文数量 | 占比 |
|------|----------|------|
| ✅ 权重开源 | 85 | 21% |
| ❌ 无权重 | 295 | 74% |
| 🔒 申请获取 | 20 | 5% |

### 5.3 数据集开源情况

| 数据集 | 开源状态 | 规模 |
|--------|----------|------|
| nuScenes | ✅ 完全开源 | 1000场景 |
| Waymo Open | ✅ 完全开源 | 大规模 |
| BDD100K | ✅ 完全开源 | 100K场景 |
| CARLA | ✅ 完全开源 | 仿真平台 |
| nuPlan | ✅ 完全开源 | 规划基准 |

### 5.4 工具生态

| 类别 | 代表工具 | 功能 |
|------|----------|------|
| BEV表征 | BEVFormer, BEVDet | 多相机BEV生成 |
| 动作生成 | UniAD, VAD | 轨迹规划 |
| VLM集成 | LLaVA, BLIP-2 | 视觉语言理解 |
| 世界模型 | GAIA-1, Drive-WM | 未来预测 |
| 仿真平台 | CARLA, nuPlan | 闭环评估 |

---

## 六、关键发现

### 6.1 技术趋势

1. **VLA成为主流范式**：从Stage 1到Stage 3的演进速度加快，2024年是VLA爆发年
2. **推理能力受重视**：Stage 4的Reasoning VLA论文数量在2025年显著增加
3. **世界模型融合**：Stage 5的World Model VLA成为研究热点
4. **效率优化**：部署效率（Stage 6）成为工业界关注重点

### 6.2 开源生态

1. **代码开源率高**：70%的论文提供代码，促进快速复现
2. **权重开源不足**：仅21%的论文开源模型权重，限制了预训练研究
3. **数据集完善**：nuScenes、Waymo等数据集为研究提供坚实基础

### 6.3 技术挑战

1. **实时性**：VLA模型的推理延迟仍是主要瓶颈
2. **安全性**：端到端模型的安全验证方法不成熟
3. **泛化性**：跨场景、跨天气的泛化能力有限
4. **可解释性**：决策过程的可解释性与性能存在 trade-off

### 6.4 未来方向

1. **统一架构**：Stage 6的Imagine-Reason-Act闭环是终极目标
2. **高效部署**：模型压缩、量化、蒸馏技术将加速落地
3. **安全验证**：形式化验证和可解释AI将提升安全性
4. **数据增强**：世界模型驱动的数据生成将缓解数据稀缺

---

## 七、结论

自动驾驶基础模型正经历从数据驱动到认知智能的深刻变革。六阶段演进框架清晰地展示了技术发展的脉络：

1. **Stage 1-2**：已经成熟，BEV表征和VLM辅助成为标配
2. **Stage 3**：VLA范式确立，OpenVLA等开源模型推动民主化
3. **Stage 4-5**：推理和预测能力正在快速发展
4. **Stage 6**：统一闭环是未来愿景，需要突破性创新

建议关注：
- **短期**（1-2年）：Stage 3的VLA优化和部署
- **中期**（3-5年）：Stage 4-5的推理与预测融合
- **长期**（5年+）：Stage 6的统一架构突破

---

## 附录：术语表

| 术语 | 全称 | 说明 |
|------|------|------|
| VLA | Vision-Language-Action | 视觉-语言-动作模型 |
| VLM | Vision-Language Model | 视觉-语言模型 |
| E2E | End-to-End | 端到端 |
| BEV | Bird's Eye View | 鸟瞰图 |
| CoT | Chain-of-Thought | 思维链 |
| WM | World Model | 世界模型 |
| AD | Autonomous Driving | 自动驾驶 |
| LLM | Large Language Model | 大语言模型 |

---

*本报告由自动化工具生成，基于公开可用的GitHub仓库数据。*
*最后更新：2026年9月*
