# WA-JEPA 技术分析报告

> **文档元数据**
> - **论文标题**：WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving
> - **作者**：Xinlin Wang, Yujiao Xiang, Yuheng Zhou, Jingqi Wang, Minqing Huang, Jiajie Huang, Dongxu Wei, Tingguang Zhou, Xiyang Wang, Gong Chen, Zhi Xu, Feiyang Tan, Hangning Zhou, Mu Yang
> - **发表**：arXiv 2026
> - **arXiv**：https://arxiv.org/abs/2608.20974
> - **GitHub**：https://github.com/AFARI-Research/WA-JEPA
> - **标签**：#2026 #arX10 #World Model VLA #Planning

---

## 一、模型组件

| 组件 | 具体实现 | 参数量 | 说明 |
|------|---------|--------|------|
| **Vision Encoder** | V-JEPA 2.1 ViT-L/16 | 304.68M | 24层Transformer，使用RoPE位置编码，支持多视角视频输入 |
| **LLM** | 无 | - | 该模型不使用LLM，而是使用联合流预测器进行动作预测 |
| **Projector** | SceneTokenProjector | 1.06M | 轻量级投影器，将per-camera V-JEPA tokens映射到场景token特征空间 |
| **Action Head** | SceneTrajectoryFlowPredictor | 15.27M | 联合流预测器，预测未来场景token和自车轨迹 |
| **其他组件** | target_encoder | 304.68M | EMA教师编码器，用于生成训练目标 |

---

## 二、参数状态

| 组件 | 冻结/训练 | 训练方法 | 可训参数占比 |
|------|----------|---------|-------------|
| **Vision Encoder** | 训练（微调） | 全参微调 | 48.6% |
| **target_encoder** | 冻结 | EMA更新 | 0% |
| **SceneTokenProjector** | 训练 | 全参 | 0.2% |
| **SceneTrajectoryFlowPredictor** | 训练 | 全参 | 2.4% |
| **其他组件** | - | - | - |

---

## 三、微调方法

| 方法 | 应用位置 | 关键超参 | 说明 |
|------|---------|---------|------|
| **全参微调** | Vision Encoder | lr=1e-5 | 对V-JEPA 2.1编码器进行全参微调 |
| **全参训练** | SceneTokenProjector | lr=1e-4 | 轻量级投影器全参训练 |
| **全参训练** | SceneTrajectoryFlowPredictor | lr=1.5e-4 | 联合流预测器全参训练 |

---

## 四、训练范式

| 阶段 | 目标 | 数据 | 损失函数 | 备注 |
|------|------|------|---------|------|
| **阶段1** | 混合未来掩码因果预训练 | nuPlan视频 | 场景流匹配损失 | 从过去帧预测未来场景特征 |
| **阶段2** | 联合世界-动作建模 | NAVSIM | 场景损失 + 轨迹损失 | 在统一时空潜在空间中去噪未来场景token和自车轨迹 |

---

## 五、技术定位

| 维度 | 定位 |
|------|------|
| **演进阶段** | Stage 5 - 预测模拟型VLA |
| **演进节点** | V-JEPA-native World-Action Modeling |
| **技术路线** | World Model VLA |
| **核心创新** | 将V-JEPA从随机掩码完成重新设计为未来导向的规划，通过混合未来掩码预训练、扩散世界建模和联合世界-动作建模三个关键设计 |
| **技术优势** | 1. 不需要LLM，减少计算开销；2. 联合预测场景和轨迹，提高规划一致性；3. 在NAVSIM和HUGSIM基准测试上达到SOTA |
| **技术局限** | 1. 需要大量视频数据进行预训练；2. 模型较大（627M参数），推理成本较高；3. 依赖V-JEPA 2.1预训练权重 |

---

## 六、任务与数据集

| 维度 | 信息 |
|------|------|
| **核心任务** | 自动驾驶轨迹规划 |
| **输入** | 4个摄像头视图 × 4个历史帧（256×512） + 自车状态 + 历史轨迹 |
| **输出** | 8个未来轨迹点（2 Hz） |
| **主要数据集** | nuPlan（预训练）, NAVSIM（微调）, HUGSIM（评估） |
| **评测指标** | EPDMS（NAVSIM）, HD-Score（HUGSIM） |
| **性能排名** | NAVSIM v2.2: 91.7 EPDMS (TOP 1), HUGSIM: 0.4462 HD-Score (TOP 1) |

---

## 七、复现信息

| 维度 | 信息 |
|------|------|
| **开源代码** | 有，https://github.com/AFARI-Research/WA-JEPA |
| **预训练权重** | 有，https://huggingface.co/AFARI-Research/WA-JEPA |
| **训练代码** | 有 |
| **推理代码** | 有 |
| **复现难度** | 中 |
| **依赖环境** | PyTorch >= 2.1.0, torchvision >= 0.16.0, numpy >= 1.23.4, timm >= 0.9.0, < 1.0 |
| **硬件需求** | GPU（推荐A100 40GB以上），当前实验在RTX 3050 4GB上可运行（CPU模式） |

---

## 八、关键图表

> （可选）如有关键的架构图、性能对比表，在此引用或描述。

---

## 九、总结

### 技术贡献
1. 提出了V-JEPA-native世界-动作建模范式，将V-JEPA从随机掩码完成重新设计为未来导向的规划
2. 设计了混合未来掩码因果预训练，从过去帧预测未来场景特征
3. 提出了联合未来-动作预测器，在统一时空潜在空间中去噪未来场景token和自车轨迹

### 局限性
1. 需要大量视频数据进行预训练（nuPlan数据集）
2. 模型较大（627M参数），推理成本较高
3. 依赖V-JEPA 2.1预训练权重

### 适用场景
- 自动驾驶轨迹规划
- 多摄像头视频理解
- 世界模型预训练

### 不适用场景
- 实时性要求极高的场景（模型较大）
- 资源受限的边缘设备
- 需要显式推理能力的场景（该模型不使用LLM）

---

## 附录：模型结构详情

### 总参数量
- **总参数量**：626,745,859（626.75M）
- **可训练参数量**：321,007,875

### 顶层模块参数分布
| 模块 | 参数量 | 占比 |
|------|--------|------|
| encoder | 304,680,960 | 48.6% |
| target_encoder | 304,680,960 | 48.6% |
| scene_projector | 1,057,024 | 0.2% |
| target_scene_projector | 1,057,024 | 0.2% |
| predictor | 15,269,635 | 2.4% |

### 模型架构特点
1. **双编码器结构**：encoder用于特征提取，target_encoder用于EMA教师目标生成
2. **轻量级投影器**：SceneTokenProjector仅1.06M参数，高效映射特征
3. **联合预测器**：SceneTrajectoryFlowPredictor同时预测场景和轨迹
4. **RoPE位置编码**：支持相对位置编码，提高泛化能力
5. **多视角支持**：支持4个摄像头视图的联合处理
