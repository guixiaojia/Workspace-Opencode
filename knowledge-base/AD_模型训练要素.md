# 模型训练要素

> **文档定位**
>
> 本文面向自动驾驶大模型方向的技术调研与训练方案设计，重点解决一个核心问题：
>
> **面对一个 VLM4AD / LLM4AD / VLA4AD / World Model，训练时到底应该"训练哪些参数、采用什么微调方法、使用什么训练范式"？**
>
> 最后更新：2026-09-18

---

# 0. 总体框架：自动驾驶大模型训练到底在设计什么？

自动驾驶大模型的训练策略，可以抽象成相互独立、但最终需要组合起来考虑的**三个正交的设计维度**：

| 维度 | 核心问题 | 决定什么 |
|---|---|---|
| **参数状态** | **训练谁？** | 哪些模块冻结、部分训练或全部训练 |
| **微调方法** | **怎么更新？** | 参数采用全参数、LoRA、Adapter 等什么方式更新 |
| **训练范式** | **学什么？** | 用什么数据、监督信号和目标函数驱动模型学习 |

> 举例分析：
> 冻结 ViT + 训练 Projector + LLM LoRA + SFT
> **参数状态 = 训练谁**：冻结 ViT，训练 Projector，部分训练 LLM
> **微调方法 = 怎么训练**：LLM 使用 LoRA
> **训练范式 = 训练什么能力**：SFT

注意！！！不能把"LoRA""冻结 LLM""SFT"放在同一个层级比较。

---

# 1. 第一层：参数状态——训练谁？

## 1.1 先把一个 AD 大模型拆开

VLM4AD / VLA4AD / World Model 往往由多个组件构成：

| 模块 | 主要作用 | 参数量占比 | 典型实现 |
|---|---|---|---|
| **Vision Encoder** | 图像 / 多视角图像 → Visual Tokens | 5%~15% | CLIP / SigLIP / DINOv2 / Qwen-ViT |
| **Projector** | Visual Tokens → LLM Embedding Space | <1% | MLP / Q-Former / Resampler |
| **LLM Backbone** | 场景理解、推理、语言生成 | 60%~85% | Qwen / LLaMA / Vicuna |
| **Action Head** | 输出轨迹、动作或控制量 | 1%~10% | MLP / Diffusion / Flow Matching |
| **World Model Decoder** | 预测未来帧或未来隐状态 | 10%~30% | DiT / UNet / 隐空间预测器 |

**冻结的本质**：在"学习能力"和"保住已有能力"之间划界——放开的越多，越能拟合新任务，但越容易灾难性遗忘、也越吃显存。

## 1.2 参数状态的三个基本选择

| 状态 | 说明 | 优点 | 缺点 | 典型场景 |
|------|------|------|------|---------|
| **Frozen** | 完全冻结，参数不参与反向传播 | 节省显存、保留预训练能力、减少灾难性遗忘、训练稳定 | 模型适应新领域能力有限 | Vision Encoder、冻结的 LLM |
| **Partial** | 只训练模块的一部分参数（如最后几层、Attention 层、LoRA、Adapter 等） | 折中方案，平衡效率与适应性 | 需要设计具体的部分训练策略 | LLM LoRA、ViT 最后 k 层 |
| **Full** | 整个模块全部参与训练 | 最大适应能力、理论性能上限更高 | 显存/计算成本高、数据需求大、灾难性遗忘风险高 | Projector、Action Head |

## 1.3 不同模块应该怎么处理？

| 模块 | 主要作用 | 推荐策略 | 经验说明 |
|------|---------|----------|---------|
| **Vision Encoder** | 图像/多视角图像 → Visual Tokens | 冻结为主，特殊情况 Partial/Full | 自然图像冻结即可（CLIP/SigLIP 已具备强表征能力）；BEV/Occupancy/深度图等非自然输入可能需要开放训练 |
| **Projector** | 视觉空间 → LLM 语义空间的"翻译层" | 通常 Full 训练 | 参数量小、成本最低；不训练则 LLM 直接接受陌生视觉 token 分布 |
| **LLM Backbone** | 场景理解、推理、语言生成 | 冻结 / LoRA / Partial / Full 视情况 | 数据少→冻结；数据适中→LoRA；数据充足+追求上限→Full FT |
| **Action Head** | 输出轨迹、动作或控制量 | 通常 Full Fine-Tune | 规模较小，输出连续动作（非离散 token），使用 LoRA 意义有限 |
| **World Model** | 预测未来帧或未来隐状态 | 冻结 Tokenizer + 训练 Dynamics Model + 训练规划头 | 核心思想：冻结"如何表示世界"，训练"世界如何变化" |

**关键判断**：
- **ViT 一般尽量冻住**。驾驶图像与 CLIP/SigLIP 预训练分布差距没大到必须微调，冻住能省下大量显存。**例外**：当输入不是自然图像（如纯 BEV 栅格图、占用栅格、深度图）时，ViT 必须放开。
- **Projector 几乎总是要训**。它是最廉价的"翻译层"，不训就等于让 LLM 硬吃一堆陌生 token。
- **VLA 与 VLM 的分水岭在动作头**。VLA 引入动作头后，主流做法是冻住整个 VLM 主干、只训动作头——因为动作输出是连续量，与语言 token 分布完全不同。
- **世界模型冻的是 tokenizer，训的是动力学**。视觉 tokenizer 负责压缩，动力学模型负责"未来怎么演化"，后者才是要学的。

## 1.4 典型训练方案

| 方案 | 冻结/训练配置 | 典型用途 |
|---|---|---|
| **① 只训 Projector** | 冻结: ViT + LLM，训练: Projector | 视觉-语言对齐、数据少 |
| **② Projector + LLM 全训** | 冻结: ViT，训练: Projector + LLM | 数据充足、追求性能 |
| **③ ViT + Projector + LLM 全训** | 冻结: 无，训练: 全部 | 域差异非常大 |
| **④ ViT 冻结 + Projector + LLM LoRA** | 冻结: ViT，训练: Projector + LoRA | **VLM4AD 最主流方案** |
| **⑤ VLM 冻结 + Action Head** | 冻结: ViT + Projector + LLM，训练: Action Head | **VLA4AD 主流方案** |
| **⑥ Tokenizer 冻结 + Dynamics Model** | 冻结: VAE / Tokenizer，训练: DiT / Dynamics | **World Model 主流方案** |

这里需要特别注意：**"冻结 + 部分微调"** 不是一种固定方案，而是一整个设计空间。真正需要调研的是：

```text
冻结谁？
    ↓
部分训练谁？
    ↓
训练比例是多少？
    ↓
为什么这样组合？
    ↓
对性能 / 显存 / 泛化 / 遗忘有什么影响？
```


## 1.5 分阶段解冻策略

实际训练中，不是一次决定所有参数，可以采用分阶段训练：

| 阶段 | 目标 | 可训练组件 |
|------|------|-----------|
| 阶段 1 视觉-语言对齐 | 视觉特征进入 LLM 空间 | Projector |
| 阶段 2 多模态指令微调 | 场景理解、推理、指令遵循 | Projector + LLM LoRA |
| 阶段 3 驾驶领域微调 | 交通规则、地图、规划、安全 | Projector + LLM LoRA + 可选视觉层 |
| 阶段 4 VLA 动作学习 | 从理解到动作 | Action Head + LLM LoRA + Projector |
| 阶段 5 闭环对齐 | 减少分布偏移、提升安全 | Action Head + LLM LoRA + Critic |

**核心思想**：随着模型能力目标从"看懂"逐渐走向"会开"，逐步扩大训练自由度。

---

# 2. 第二层：微调方法——怎么改参数？

## 2.1 PEFT 谱系（基础）

| 方法 | 核心思路 | 可训参数 | 显存（相对全参） | 推理能否合并 | 适用场景 |
|------|---------|---------|----------------|-------------|---------|
| **Full Fine-Tune** | 全部参数更新 | 100% | 1×（基准） | 本就是原模型 | 数据足、追求上限 |
| **LoRA** | W′ = W + (α/r)·BA，低秩旁路 | 0.1%~3% | ~1/3 | ✅ 可合并，零推理开销 | **默认首选** |
| **QLoRA** | 4-bit NF4 量化主干 + LoRA | 0.1%~3% | ~1/6~1/10 | 需反量化 | 单卡训 7B~70B |
| **DoRA** | 把权重拆成幅度+方向，方向用 LoRA | ~+0.01% | 略高于 LoRA | ✅ | 追求逼近全参效果 |
| **AdaLoRA** | 自适应分配各层秩 | 动态 | 略高于 LoRA | ✅ | 层重要性差异大时 |
| **Adapter** | 插入瓶颈 MLP 旁路 | ~1%~3% | 中 | ❌ 增加推理延迟 | 多任务切换 |
| **Prompt Tuning** | 只学一组软提示 token | <0.01% | 最低 | ❌ 需保留前缀 | 效果上限低 |
| **OFT / BOFT** | 学正交旋转变换 | ~0.1% | 中 | ✅ | **VLA 常用** |

## 2.2 LoRA 实操要点（决定成败）

| 要点 | 说明 | 常见错误 |
|------|------|---------|
| **`target_modules` 比 rank 更重要** | 挂**所有线性层**（q/k/v/o + gate/up/down）在多模态任务上通常明显更优 | 只挂 q_proj、v_proj |
| **rank 与数据量正相关** | r=8~16 适合几千到几万条；r=32/64 适合十万级；再大不如全参 | 所有场景用同一个 r |
| **LoRA 的学习率要比全参高一个量级** | 全参 1e-5~2e-5，LoRA 1e-4~2e-4 | 用全参的 lr 训 LoRA |
| **Projector 与 LoRA 要分组设 lr** | Projector 随机初始化，需要更大 lr（1e-3 量级）；LoRA 用小 lr | 所有参数用同一个 lr |
| **QLoRA 的收益是显存不是速度** | 通常比 LoRA 慢（多了量化/反量化） | 卡够时仍用 QLoRA |
| **合并与卸载** | 训完用 `merge_and_unload()` 把 BA 加回 W，部署时无额外延迟 | 部署时保留旁路 |

## 2.3 视觉侧 PEFT（进阶）

| 方法 | 说明 | 适用场景 |
|------|------|---------|
| **VPT（Visual Prompt Tuning）** | 给 ViT 加可学 token | ViT 微调 |
| **AdaptFormer / Convpass** | ViT 内部插 adapter 或并行卷积分支 | ViT 微调 |
| **SSF** | 只学特征缩放+偏移，可合并零延迟 | ViT 微调，效果出奇地好 |
| **时序 adapter** | 在帧间插少量可学参数 | BEV4D 和世界模型 |

## 2.4 多模态对齐的特殊考虑（进阶）

- 只训 projector 是最弱的对齐，通常需要 projector + LoRA-on-LLM 才够。
- LoRA 挂载位置的经验：对生成/规划类任务，attention 的 q、v 投影收益最大；输出 embedding / lm_head 往往也需要覆盖。
- VLA 的动作输出是连续的，且常需高频（10~50Hz），Action head 一般用全参训练（它本身小），而不是 LoRA。

---

# 3. 第三层：训练范式——学什么？

## 3.1 范式谱系

| 范式 | 数据格式要求 | 核心目标 | 监督类型 | 开环/闭环 | 主要解决的问题 |
|---|---|---|---|---|---|
| **CPT** | 原始语料/日志 | 下一Token预测 | - | 开环 | 领域知识 |
| **模态对齐预训练** | 图像-文本 | 图文对应 | 语言监督 | 开环 | 视觉进入语言空间 |
| **SFT** | 指令-回答 | 监督学习 | 语言监督 | 开环 | 指令遵循 |
| **CoT SFT** | 问题-推理链-答案 | 学习推理过程 | 语言监督 | 开环 | 推理能力 |
| **DPO/IPO/KTO** | chosen/rejected | 偏好优化 | 语言监督 | 开环 | 输出质量、安全 |
| **RLHF/PPO** | 奖励模型+采样 | 策略优化 | 语言监督 | 开环 | 不可微整体指标 |
| **RLVR** | 有客观判据的数据 | 可验证奖励 | 语言监督 | 开环 | 客观正确性 |
| **BC** | 专家轨迹 | 模仿专家 | 轨迹监督 | 开环 | 动作学习 |
| **DAgger** | 在线纠偏轨迹 | 减少分布漂移 | 轨迹监督 | **闭环** | 闭环驾驶 |
| **闭环RL** | 仿真交互 | 奖励优化 | 轨迹监督 | **闭环** | 真正驾驶能力 |
| **World Model Training** | 连续状态+动作 | 未来预测 | 轨迹监督 | - | 学习环境动力学 |

## 3.2 训练范式核心目标分层

按自动驾驶与具身智能大模型的能力构建逻辑，可分层展开：

**基础表征与感知**
- **下一Token预测**：通过自回归方式学习多模态序列的统计规律，赋予模型基础的物理世界常识、交通领域知识 → CPT
- **图文对应**：将视觉特征映射到语言特征空间，使模型能够"看懂"图像 → 模态对齐预训练

**认知与任务执行**
- **监督学习/指令遵循**：让模型学会听懂人类的具体任务要求 → SFT
- **学习推理过程**：不仅学习最终答案，更学习"如何思考"（思维链 CoT） → CoT SFT

**价值与策略对齐**
- **偏好优化**：学习人类认为"更好"、"更舒适"或"更安全"的选择 → DPO/IPO/KTO
- **策略优化**：通过奖励模型引导，优化模型在复杂交互中的整体策略 → RLHF/PPO
- **可验证奖励**：针对有明确对错标准的任务，利用客观反馈信号进行强化 → RLVR

**动作执行与闭环控制**
- **模仿专家**：直接学习人类驾驶员的操作轨迹 → BC
- **减少分布漂移**：在模型自己犯错时引入专家纠偏 → DAgger
- **奖励优化**：在闭环仿真中，通过试错和长期累积奖励优化模型 → 闭环RL

**环境理解与预测**
- **未来预测**：学习环境的物理规律和动力学，预测未来状态 → World Model Training

## 3.3 自驾特有的三条数据主轴

### 主轴1：语言监督 vs 轨迹监督

| 类型 | 优点 | 缺点 | 主流做法 |
|------|------|------|---------|
| 语言监督（QA、描述、推理） | 保住和增强语义推理能力 | 不直接优化轨迹 | 语言 SFT 打底 |
| 轨迹监督（L2 loss、碰撞 loss） | 直接优化驾驶指标 | 训多了会"说不出话" | 轨迹监督精调 |

**最佳实践**：语言 SFT 打底 + 轨迹监督精调，或双头联合训练。

### 主轴2：开环 vs 闭环

| 类型 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| 开环 SFT（模仿人类轨迹） | 简单稳定 | 分布漂移，误差累积 | 初期验证 |
| 闭环训练（CARLA / Bench2Drive） | 能治分布漂移 | 仿真成本高，训练不稳定 | 进阶优化 |

**这是 VLA4AD 与规划方向当前最核心的方法学分野**。

### 主轴3：世界模型的独特目标

世界模型不直接输出动作，而是学「(当前状态, 动作) → 未来状态」。价值在于：
- 作为**数据引擎**生成长尾场景（Corner case 增广）
- 作为**规划器的 internal simulator**——在隐空间"想象"未来再选动作
- 作为**闭环训练环境**替代昂贵仿真

## 3.4 对齐的两个层次（进阶）

**术语上最大的坑**：

| 层次 | 含义 | 发生阶段 | 目标 |
|------|------|---------|------|
| **模态对齐（Alignment Pretraining）** | 视觉与语言的表层对齐 | SFT 之前 | 让模型"看得懂图" |
| **偏好对齐（Preference Alignment）** | RLHF/DPO | SFT 之后 | 让输出"符合人类偏好/安全准则" |

> 读论文时看到 alignment，必须看它处在流水线的哪个阶段。

---

# 4. 第四层：三维组合——训练方案设计框架

把前三层合起来：

```text
                  自动驾驶模型训练
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      参数状态        微调方法        训练范式
       训练谁？        怎么改？        学什么？
          │              │              │
      Frozen/Partial   Full/LoRA      SFT/RL/BC
      /Full            /QLoRA/...     /DPO/WM...
          └──────────────┼──────────────┘
                         ↓
                   最终训练方案
```

## 4.1 典型方案速查表

| 方案 | 核心问题与解决思路 | 适用场景 | 参数配置 | 训练范式 |
|------|-------------------|----------|----------|----------|
| **VLM4AD** | 看懂驾驶世界：先对齐视觉-语言空间，再学习指令遵循 | 数据<5万、单卡、场景理解/QA/推理 | 冻结ViT，训练Projector，LLM使用LoRA | 模态对齐 → SFT |
| **LLM4AD** | 理解/推理驾驶知识：通过持续预训练注入领域知识 | 纯语言场景理解、推理任务 | 冻结视觉模块，训练LLM（Full FT / LoRA） | CPT + SFT + Reasoning |
| **VLA4AD** | 从理解走向动作：先让模型"看懂"，再让模型"会做" | 多卡、数据充足、需要连续控制输出 | 冻结VLM，训练Action Head（Full FT） | BC → DAgger / RL |
| **World Model** | 预测世界未来：学习环境动力学，预测未来状态 | 预测未来环境变化、辅助规划 | 冻结Tokenizer，训练Dynamics Model | Future Prediction |

## 4.2 四套可落地配方

### 配方A：VLM4AD 起步配方（单卡，数据 <5 万条）

| 维度 | 选择 | 说明 |
|------|------|------|
| 参数状态 | 冻结 ViT，训 Projector + LLM 的 LoRA | r=16，挂所有线性层 |
| 微调方法 | bf16 LoRA，lr=1e-4，Projector 单独 lr=1e-3 | 分组设 lr |
| 训练范式 | 场景描述对齐 → 指令 SFT（QA + 推理链） | 渐进式训练 |

**适用场景**：DriveLM 类图结构 QA、NuScenes-QA、Dolphins 类驾驶问答。

**典型组合**：
- Vision Encoder：Frozen SigLIP / CLIP
- Projector：Train MLP
- LLM：LoRA Qwen / LLaMA
- 流程：视觉-语言对齐 → 多模态指令微调 → 驾驶领域微调

### 配方B：VLM4AD 进阶配方（多卡，数据充足）

| 维度 | 选择 | 说明 |
|------|------|------|
| 参数状态 | 冻结 ViT，LLM 全参或 r=64 的 LoRA，Projector 全参 | 根据算力选择 |
| 微调方法 | 全参（lr=1e-5）或大秩 LoRA | 追求上限 |
| 训练范式 | SFT → **DPO**（用"安全轨迹 vs 危险轨迹"构造偏好对） | 安全对齐 |

**关键点**：DPO 阶段要混入一部分通用 SFT 数据做 replay，否则通用推理能力会明显退化。

### 配方C：VLA4AD 标准配方

| 维度 | 选择 | 说明 |
|------|------|------|
| 参数状态 | **冻结整个 VLM 主干**，只训 Action Head | flow matching 或 diffusion |
| 微调方法 | Action Head 全参（它小，不值得 LoRA） | 连续回归目标 |
| 训练范式 | 行为克隆 BC 打底 → 可选闭环 RL / DAgger | 渐进式 |

**代表**：π0 / OpenVLA / SmolVLA。

**算力紧张时**：OpenVLA 的 LoRA + OFT 配方可在单卡上跑，FAST 分词器让动作能走自回归。

**典型组合**：
- Vision Encoder：Frozen ViT / DINOv2 / SigLIP
- Projector：Q-Former / MLP
- LLM：LoRA LLaMA / Qwen
- Action Head：Diffusion / Flow Matching / Action Token
- 流程：视觉-语言对齐 → 多模态 SFT → 驾驶领域 SFT → VLA 行为克隆 → 闭环 RL 微调

### 配方D：世界模型 + 规划配方

| 维度 | 选择 | 说明 |
|------|------|------|
| 参数状态 | 冻结视觉 tokenizer（VAE / 离散编码），训时空预测器（DiT），再接轻量规划头 | 冻结压缩，学习动力学 |
| 微调方法 | 预测器全参，规划头全参 | 从头训的模块不需要 LoRA |
| 训练范式 | 重建 loss + 未来预测 loss → 规划头监督 → 可选闭环微调 | 多目标联合 |

**评价**：必须同时看开环（nuScenes L2）与闭环（NAVSIM PDM Score / Bench2Drive Driving Score）两套指标。

**典型组合**：
- 视觉 tokenizer：Frozen VAE / 离散编码
- 时空预测器：Train DiT
- 规划头：Train MLP
- 流程：重建 + 未来预测 → 规划头监督 → 闭环微调

---

# 5. 第五层：实操指南

## 5.1 选型决策树

```text
先问：有没有连续动作输出需求？
├─ 有（VLA）→ 冻 VLM 主干 + 训 action head，BC 起手，算力允许再上闭环 RL
└─ 无（VLM / 世界模型）
   ├─ 目标是"理解与问答" → 冻 ViT + LLM LoRA + SFT          （配方 A）
   ├─ 目标是"安全与偏好" → 配方 A + DPO                      （配方 B）
   └─ 目标是"预测未来/生成数据" → 冻 tokenizer + 训 DiT       （配方 D）

再问：单卡还是多卡？
├─ 单卡 24G：QLoRA 或 bf16 LoRA，r=8~16，7B 模型
├─ 单卡 80G：bf16 LoRA r=32~64，或 7B 全参
└─ 多机多卡：全参 SFT + DPO / PPO
```

## 5.2 完整选型流程（8步）

```text
Step 1：模型要获得什么能力？
  ├─ 看懂驾驶世界 → VLM4AD
  ├─ 从理解走向动作 → VLA4AD
  ├─ 预测世界未来 → World Model
  └─ 想象→推理→行动 → VLA + World Model
             ↓
Step 2：最终输出是什么？
  ├─ 语言输出 → VLM4AD
  ├─ 连续动作输出 → VLA4AD
  ├─ 未来状态预测 → World Model
  └─ 完整规划决策 → VLA + World Model
             ↓
Step 3：需要训练哪些模块？
  ├─ VLM4AD：Projector + LLM
  ├─ VLA4AD：Action Head + 部分 VLM
  ├─ World Model：Dynamics Model + Planning Head
  └─ VLA + World Model：VLA + World Model
             ↓
Step 4：数据规模是多少？
  ├─ 数据<5万 → LoRA（r=8~16）
  ├─ 数据充足 → Full FT / 大 Rank LoRA（r=32~64）
  └─ 多任务切换 → Adapter
             ↓
Step 5：算力是多少？
  ├─ 单卡24G → QLoRA
  ├─ 单卡80G → bf16 LoRA / 部分 Full FT
  ├─ 多卡 → Full FT / 大 Rank LoRA
  └─ 多机多卡 → Full SFT + DPO / PPO
             ↓
Step 6：选择微调方法
  ├─ 参数量极低要求 → Prompt Tuning / VPT
  ├─ 视觉模型微调 → VPT / AdaptFormer / SSF
  ├─ 大模型默认 → LoRA
  └─ 追求性能上限 → Full FT
             ↓
Step 7：选择训练范式
  ├─ 基础表征学习 → CPT
  ├─ 视觉-语言对齐 → 模态对齐预训练
  ├─ 指令遵循 → SFT
  ├─ 推理能力 → CoT SFT
  ├─ 偏好对齐 → DPO/IPO/KTO
  ├─ 策略优化 → RLHF/PPO
  ├─ 客观正确性 → RLVR
  ├─ 动作学习 → BC
  ├─ 闭环驾驶 → DAgger / 闭环RL
  └─ 未来预测 → World Model Training
             ↓
Step 8：最终必须用 AD 指标验证
  ├─ 开环指标：Language Loss、QA Accuracy、L2
  └─ 闭环指标：Collision Rate、Driving Score、PDM Score
```

## 5.3 高频翻车点

| 现象 | 根因 | 解法 |
|------|------|------|
| 训完不会说话 / 输出格式崩坏 | SFT 数据量过大或 lr 过高，语言能力被冲掉 | 混入通用指令数据、降 lr、减 epoch |
| 开环 L2 很好，闭环一跑就撞 | 分布漂移，纯模仿学习固有缺陷 | 加 DAgger / 闭环 RL，或用 PDM Score 做奖励 |
| LoRA 训了跟没训一样 | lr 用了全参量级（1e-5）或 `target_modules` 只挂了两处 | lr 提到 1e-4，挂全线性层 |
| 多轮训练后指标不升反降 | 灾难性遗忘 / 数据分布偏移 | 分阶段训练 + replay，或用 EMA |
| VLA 动作抖动、不连贯 | 逐帧独立预测，时序不一致 | 动作分块（action chunking）+ 时序平滑，或改 flow matching |
| 视觉能力下降 | Vision Backbone 过度微调 | 冻结或降低视觉侧训练比例 |

## 5.4 架构师 Trade-offs

| 权衡维度 | 选项 A | 选项 B | 建议 |
|---------|--------|--------|------|
| **算力 vs 性能** | 冻结主干 + QLoRA + 高质量数据 | 全参数微调 + 端到端联合训练 | 算力有限选 A，充沛选 B |
| **通用性 vs 专业性** | 冻结主干（保留 zero-shot） | 全参微调（可能退化为"偏科生"） | 安全攸关系统选 A |
| **训练效率 vs 推理延迟** | Adapter（增加延迟） | LoRA（零推理延迟） | 实时性要求高选 LoRA |

---

# 6. 第六层：三维耦合关系（进阶）

## 6.1 参数状态 × 微调方法

LoRA 只能作用于有线性层的模块（LLM、ViT），对 action head 这种小 MLP 意义不大。

因此：
- `LLM + LoRA` → 非常自然
- `小型 Action Head + LoRA` → 意义通常有限

## 6.2 微调方法 × 训练范式

训练范式越复杂，对显存和可训练参数的要求往往越高。

例如：
```text
SFT → DPO → RL
```
训练复杂度逐渐增加。PEFT / QLoRA 等方法可以帮助降低训练成本。

## 6.3 参数状态 × 训练范式

不同训练阶段需要不同的训练自由度：
- 小数据 SFT → 不适合直接 Full FT
- 闭环 RL → 需要更强的策略更新能力

**参数状态不能脱离训练范式单独决定。**

## 6.4 遗忘风险的量化感知

| 阶段 | 遗忘类型 | 说明 |
|------|---------|------|
| SFT 阶段 | 语言常识退化 | 通用指令数据可缓解 |
| DPO 阶段 | 风格漂移 | 需要 replay 通用数据 |
| Full FT | 感知 backbone 的 OOD 泛化 | 最危险，需谨慎 |

---

# 7. 统一认知框架

将全文压缩成一张图：

```text
             自动驾驶大模型训练
                     │
                     ↓
        ┌─────────────────────────┐
        │   第一问：训练谁？       │
        │   参数状态               │
        └────────────┬────────────┘
                     ↓
          Frozen / Partial / Full
                     │
                     ↓
        ┌─────────────────────────┐
        │   第二问：怎么训练？     │
        │   微调方法               │
        └────────────┬────────────┘
                     ↓
       Full FT / LoRA / QLoRA / ...
                     │
                     ↓
        ┌─────────────────────────┐
        │   第三问：学什么？       │
        │   训练范式               │
        └────────────┬────────────┘
                     ↓
    CPT / Alignment / SFT / DPO / RL
            / BC / DAgger / WM
                     │
                     ↓
        ┌─────────────────────────┐
        │    三者组合成训练方案    │
        └────────────┬────────────┘
                     ↓
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
    VLM4AD        VLA4AD       World Model
       │             │             │
    理解世界       输出动作       预测世界
       │             │             │
       └─────────────┼─────────────┘
                     ↓
              闭环驾驶能力
                     ↓
        Collision / Driving Score
               / PDM Score
```

---

# 8. 一句话记忆

> **参数状态决定"训练谁"，微调方法决定"怎么更新这些参数"，训练范式决定"让模型学什么能力"，三者组合起来才构成完整的自动驾驶大模型训练方案。**

进一步可以记成：

> **训练谁 → 怎么改 → 学什么 → 怎么组合 → 怎么验证**

而对于自动驾驶：

> **最终不是"模型 Loss 降了多少"，而是"模型在闭环环境里是否真的更会开车"。**

---

# 附录：术语快速对照

| 术语 | 常见英文 / 其他叫法 | 核心含义 |
|---|---|---|
| 参数状态 | Freezing Strategy | 哪些参数参与训练 |
| 微调方法 | Fine-tuning / PEFT | 参数具体如何更新 |
| Full Fine-Tuning | Full FT | 全参数更新 |
| LoRA | Low-Rank Adaptation | 低秩参数更新 |
| QLoRA | Quantized LoRA | 量化 + LoRA |
| DoRA | Weight-Decomposed Low-Rank Adaptation | 幅度+方向分解 |
| Adapter | - | 瓶颈网络旁路 |
| OFT / BOFT | Orthogonal Fine-Tuning | 正交变换 |
| VPT | Visual Prompt Tuning | 视觉提示调优 |
| SSF | Scale and Shift Features | 缩放和偏移特征 |
| 模态对齐 | Alignment Pretraining | 视觉与语言空间对齐 |
| 偏好对齐 | Preference Alignment | RLHF/DPO 安全对齐 |
| SFT | Supervised Fine-Tuning | 监督指令学习 |
| CoT | Chain-of-Thought | 思维链 |
| DPO | Direct Preference Optimization | 直接偏好优化 |
| IPO | Identity Preference Optimization | 身份偏好优化 |
| KTO | Kahneman-Tversky Optimization | 基于前景理论的偏好优化 |
| RLHF | Reinforcement Learning from Human Feedback | 人类反馈强化学习 |
| PPO | Proximal Policy Optimization | 近端策略优化 |
| RLVR | Reinforcement Learning with Verifiable Rewards | 可验证奖励强化学习 |
| BC | Behavior Cloning | 行为克隆 |
| DAgger | Dataset Aggregation | 在线纠偏、减少分布漂移 |
| CPT | Continual Pre-Training | 持续预训练 |
| World Model | 世界模型 | 学习环境状态演化 |
| Action Head | 动作头 | 将模型表征映射到动作/轨迹 |
