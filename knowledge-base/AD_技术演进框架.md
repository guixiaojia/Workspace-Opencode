# 技术演进框架

> 本文档定义了自动驾驶基础模型的六阶段技术演进路径，用于论文分析时的技术定位。

---

## 总览

```
数据驱动型E2E → 语义增强型E2E（VLM赋能） → 动作原生型VLA（吸纳VLM） → 认知推理型VLA（吸纳Reasoning） → 预测模拟型VLA（吸纳World Model） → Imagine–Reason–Act 统一闭环
```

---

## Stage 1 — 数据驱动型 E2E

**定义**：纯视觉/纯信号输入，直接映射轨迹，无显式语义理解。

**关键特征**：
- 输入：多相机图像 / LiDAR 点云
- 输出：轨迹 / 控制信号
- 核心技术：BEV 表征、端到端学习
- 代表工作：BEVFormer、UniAD、VAD

**子阶段**：
- 模块化感知
- BEV 统一表征
- 以规划为导向的端到端
- 多任务 E2E
- 端到端感知-预测-规划-控制统一

**边界判断**：
- 规划辅助 ≠ 动作生成
- 有语义理解但不直接输出动作 → 仍属于 Stage 1

---

## Stage 2 — 语义增强型 E2E（VLM 赋能）

**定义**：引入 VLM 做"副驾驶"，看懂路牌、行人意图、环境逻辑，辅助规划，但不直接输出动作。

**关键特征**：
- VLM 作为语义副驾（semantic co-pilot）
- 输出：语言描述、QA 答案、决策解释
- 核心技术：VLM + 驾驶场景理解
- 代表工作：DriveGPT4、LMDrive、DriveLM

**子阶段**：
- VLM 辅助感知
- VLM 场景理解
- VLM 解释/问答
- VLM 辅助规划
- 语义决策开始向 Action 对齐
- VLA 过渡

**边界判断**：
- VLM 参与规划/决策 **并不自动等于** VLA
- 当视觉/语言表征被显式地与 Action/Trajectory/Control 输出对齐时，才算进入 VLA

---

## Stage 3 — 动作原生型 VLA

**定义**：VLM/LLM 的能力被吸收进驾驶策略，语义表征与 Action/Trajectory/Control 对齐。VLM 作为基座被冻结或微调，统一输出动作 Token。

**关键特征**：
- VLM 体系终结，完全被 VLA 吸纳
- 输出：连续动作 / 离散动作 Token
- 核心技术：Action Head、动作分词器
- 代表工作：OpenVLA、π0、SmolVLA

**子阶段**：
- LLM 作为解释器
- 模块化 VLA 模型
- 统一端到端 VLA 模型
- 推理增强的 VLA 模型

**边界判断**：
- VLM 能力已融入 VLA 的 backbone/policy
- 不要说 VLM "消失"了，应视为被吸收

---

## Stage 4 — 认知推理型 VLA

**定义**：在 VLA 的输出动作前，插入显式的 CoT/因果推理模块。模型输出 "Observation → Reasoning → Planning → Action"。

**关键特征**：
- 显式推理影响动作生成
- 输出：推理链 + 动作
- 核心技术：CoT、因果推理、多步决策
- 代表工作：AutoDrive-P3、ReCogDrive

**子阶段**：
- CoT 显式推理
- 场景/因果推理
- 多步决策推理
- 记忆与反思
- 可验证/可控 Reasoning

**边界判断**：
- 仅有推理文本的演示是不够的
- 需验证推理确实影响了 planning/action

---

## Stage 5 — 预测模拟型 VLA

**定义**：VLA 吸收 World Model 能力，在选择动作之前使用未来预测/想象。

**关键特征**：
- VLA + World Model 融合
- 输出：基于未来预测的动作
- 核心技术：World Model、潜空间预测
- 代表工作：World4Drive、DriveWorld-VLA

**子阶段**：
- 场景生成
- 时序预测
- 3D/4D 世界建模
- 潜空间世界模型
- 可控世界模型
- 世界模型驱动规划与决策

**边界判断**：
- 视频生成器 **并不自动等于** 面向决策的 World Model
- 需检查：时序预测、动作条件（action conditioning）、可控性、是否用于规划

---

## Stage 6 — 统一 Imagine–Reason–Act 闭环

**定义**：VLA、Reasoning 与 World Model 在共享/联合潜空间中融合，同时完成"想象后果→推理因果→执行动作"。

**关键特征**：
- 三者参数空间相互打通
- 无模块边界
- 联合潜空间

**目标闭环**：
```
Observe → Imagine → Reason → Act → Observe → ...
```

**子阶段**：
- VLA 决策
- World Model 未来预测
- VLA 闭环规划
- VLA + World Model 联合潜空间
- Imagine–Reason–Act 统一闭环

**边界判断**：
- 除非有实证，否则不要声称实现了完整的参数空间统一
- 要区分「已被验证的融合」与「仅停留在构想层面的架构」

---

## 使用说明

1. **判断边界**：参考每个大阶段的"边界判断"部分，定位到对应的大阶段
2. **子阶段映射**：根据论文的技术特征，将论文映射到子阶段中的具体节点
