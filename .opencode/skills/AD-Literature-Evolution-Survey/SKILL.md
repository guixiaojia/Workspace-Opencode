---
name: autonomous-driving-foundation-model-literature 自动驾驶基础模型文献研究
description: 分析多个 GitHub Awesome 列表与仓库中的自动驾驶基础模型文献，对重要论文进行排序，将其映射到六阶段技术演进框架，并识别可复现/开源的实现。
---

# 自动驾驶基础模型文献研究 Skill

## 目标
给定多个包含自动驾驶论文的 GitHub 仓库：
1. 从所有提供的仓库中构建论文池。
2. 规范化论文实体并对重复项去重。
3. 统计每篇论文出现在多少个**不同的**仓库中。
4. 使用仓库频次加技术重要性对论文排序。
5. 选出约 Top 30 核心论文。
6. 将 Top 30 映射到下面的六阶段演进框架。
7. 列出官方开源/可复现实现。
8. 区分「有代码」与「真正可复现」。

不要平均地机械地处理每一篇论文，而要聚焦于重复出现、奠基性、范式转变性和技术上有影响力的论文。

## 六阶段技术演进框架

### Stage 1 — Data-driven E2E 数据驱动型E2E
从纯视觉/信号输入直接到轨迹/控制，显式的语义理解有限。

演进：
Modular Perception → BEV Unified Representation → Planning-oriented E2E → Multi-task E2E → Unified Perception-Prediction-Planning-Control

模块化感知 → BEV统一表征 → 以规划为导向的E2E → 多任务E2E → 感知-预测-规划-控制统一E2E

### Stage 2 — Semantically Enhanced E2E 语义增强型E2E
VLM 充当语义副驾（semantic co-pilot）：感知、场景理解、解释/问答、意图/逻辑理解、规划辅助和语义决策支持。

演进：
VLM-assisted Perception → Scene Understanding → Explanation/QA → Planning Assistance → Semantic Decision

VLM辅助感知 → VLM场景理解 → VLM解释/问答 → VLM辅助规划 → 语义决策开始向 Action 对齐

边界：
VLM 参与规划/决策**并不自动等于** VLA。当视觉/语言表征被显式地与 Action/Trajectory/Control 输出对齐时，才算进入 VLA。

### Stage 3 — Action-native VLA 动作原生型VLA
VLM/LLM 的能力被吸收进驾驶策略，语义表征与 Action/Trajectory/Control 对齐。

演进：
LLM as Interpreter → Modular VLA → Unified End-to-End VLA → Reasoning-enhanced VLA

LLM作为解释器 → 模块化VLA → 统一端到端VLA → 推理增强的VLA模型

不要说 VLM 消失了；应将 VLM 能力视为已被吸收进 VLA 的 backbone/policy 中。

### Stage 4 — Cognitive-Reasoning VLA 认知推理型VLA
显式或结构化的推理影响动作生成。

规范抽象：
Observation → Reasoning → Planning → Action

演进：
Explicit CoT → Scene/Causal Reasoning → Multi-step Decision Reasoning → Memory/Reflection → Verifiable/Controllable Reasoning

CoT显式推理 → 场景/因果推理 → 多步决策推理 → 记忆与反思 → 可验证/可控Reasoning

仅有推理文本的演示是不够的；需验证推理确实影响了 planning/action。

### Stage 5 — Predictive-Simulation VLA 预测模拟型VLA
VLA 吸收 World Model 能力，并在选择动作之前使用未来预测/想象。

规范抽象：
Current State → World Model → Multiple Possible Futures → VLA Evaluation → Action

World Model 演进：
Scene Generation → Temporal Prediction → 3D/4D World Modeling → Latent World Model → Controllable World Model → World-Model-driven Planning/Decision

场景生成 → 时序预测 → 3D/4D世界建模 → 潜空间世界模型 → 可控世界模型 → 世界模型驱动规划与决策

视频生成器**并不自动等于**面向决策的 World Model；需检查时序预测、动作条件（action conditioning）、可控性、潜空间动态（latent dynamics）以及是否用于规划。

### Stage 6 — Unified Imagine–Reason–Act Loop
VLA、Reasoning 与 World Model 日益融合，理想情况下在共享/联合潜空间中融合。

演进：
VLA Decision → World Model Future Prediction → VLA Closed-loop Planning → Joint VLA+WM Latent Space → Imagine–Reason–Act

VLA决策 → World Model未来预测 → VLA闭环规划 → VLA + World Model联合潜空间 → Imagine–Reason–Act统一闭环

目标闭环：
Observe → Imagine → Reason → Act → Observe → ...

除非有实证，否则不要声称实现了完整的参数空间统一。要区分「已被验证的融合」与「仅停留在构想层面的架构」。

## Input repositories 输入仓库
1. https://github.com/JohnsonJiang1996/Awesome-VLA4AD
2. https://github.com/opendrivelab/end-to-end-autonomous-driving
3. https://github.com/LMD0311/Awesome-World-Model
4. https://github.com/leofan90/awesome-world-models
5. https://github.com/curryqka/quick-start-VLA4AD
6. https://github.com/xiaomi-research/recogdrive
7. https://github.com/thinklab-sjtu/awesome-llm4ad
8. https://github.com/worldbench/awesome-vla-for-ad
9. https://github.com/JiahuaDong/Awesome-World-Models
10. https://github.com/autonomousdrivingkr/Awesome-Autonomous-Driving
11. https://github.com/KwanWaiPang/Awesome-VLA
12. https://github.com/honalele/Foundation-Models-Meet-Driving-World-Models
13. https://github.com/Yanyeoo/Awesome-Efficient-VLA4AD

如果用户提供更新的 URL，则增加上用户提供的 URL。

## Workflow 工作流

### Phase A — Repository discovery 仓库检索
对每一个仓库：
- 检查 README 及链接的论文列表；
- 提取论文标题、模型名、年份、分类，以及论文/项目链接；
- 记录每篇论文出现在哪个仓库中；
- 此阶段**不要**按主观重要性排序。

构建「仓库-论文」矩阵。

### Phase B — Entity normalization 实例规范化
规范化标题变体、arXiv/会议版本、论文标题与模型名、别名、大小写和标点。

关键规则：
相同的缩写/模型名**并不意味着**是同一篇论文，除非标题/作者/证据能确认为同一篇，否则应保持分开。

### Phase C — Frequency ranking 频率排序
对每篇规范化后的论文：
Repository Frequency = 包含该论文的、所提供的**不同**仓库的数量。
每个仓库最多计一次。

### Phase D — Technical importance re-ranking 技术重要性排序
使用：
- Repository Frequency：30%
- Paradigm Contribution：30%
- Technical/Research Influence：25%
- Reproducibility/Open-source value：15%

对奠基性/范式转变性论文，即使频次不高，也要加入 Paradigm Override（范式优先）。

Importance 分级：
S = paradigm-changing/foundational（范式转变/奠基性）
A = major technical evolution（重大技术演进）
B = representative method（代表性方法）
C = supplementary（补充性）

不要让近期 World Model/VLA 的论文数量挤掉奠基性的 E2E/VLM 工作。

### Phase E — Select Top 30 选择30篇核心论文
选出约 30 篇核心论文。不要强行套用死板配额，但要确保六个阶段都有充分代表。

初始平衡：
Stage 1：5–6
Stage 2：4–5
Stage 3：5–7
Stage 4：3–5
Stage 5：5–7
Stage 6：2–5

根据证据进行调整。

### Phase F — Six-stage mapping 六阶段映射
对每篇 Top-30 论文识别：
1. Primary stage（主要阶段）。
2. Specific evolution node（具体演进节点）。
3. Secondary stage(s)（次要阶段，如适用）。
4. 为何归属此处。
5. 是否为跨阶段桥接（bridge）。

使用「主要节点 + 次要标签」，而不是强行做人为的单一分类。

### Phase G — Open-source/reproducibility analysis 开源/可复现分析
优先采用官方项目来源。记录：
- 官方 GitHub/代码；
- 训练代码；
- 推理/demo 代码；
- 预训练权重；
- 数据集/数据准备；
- 评测环境；
- 闭源/不可获取的依赖。

Reproducibility 分级：
★★★★★ Full：code + weights + data/data pipeline + configuration/environment 基本齐备。
★★★★☆ Strong：code + weights，外部数据需求可控。
★★★☆☆ Partial：有大量公开代码，但缺少 weights/data/某些组件。
★★☆☆☆ Demo-level：主要是推理/demo 或实现不完整。
★☆☆☆☆ Not reproducible：没有可用的公开实现。

绝不能将「GitHub 上存在」等同于「可复现」。

## Required outputs 要求的输出格式

### Output 1 — 13-repository paper inventory 论文清单
Repository → paper list，随后是一张规范化主表：
Rank | Paper | Year | Model | Repositories | Frequency | Initial Direction

### Output 2 — Frequency and importance ranking 频率和重要性排序
Rank | Paper/Model | Frequency | Paradigm Contribution | Technical Influence | Open Source | Final Level

解释主要的排序 override。

### Output 3 — Final Top 30 mapped to six-stage evolution 六阶段演化
Rank | Paper/Model | Stage | Evolution Node | Role in Evolution | Importance

同时展示演进链：
Data-driven E2E → Semantically Enhanced E2E → Action-native VLA → Cognitive-Reasoning VLA → Predictive-Simulation VLA → Imagine–Reason–Act

### Output 4 — Reproducible/open-source model list 可复现/开源模型列表
使用格式：
Model/Paper Name: Official Open-Source Link
可选地附加上 reproducibility 状态。

### Output 5 — Key conclusions 主要结论
识别：
- paradigm-changing papers（范式转变性论文）；
- bridge papers（桥接性论文）；
- 被频繁列出但只是增量改进的论文；
- 重要的低频论文；
- VLA + World Model 融合的证据；
- 概念上的 Imagine–Reason–Act 终点与已被验证的系统之间的差距。

## Source rules 来源规则
优先级：
1. 原始论文/arXiv/会议论文。
2. 官方 GitHub/项目仓库。
3. 官方数据集/模型文档。
4. 高质量二手来源。
5. 用于发现/交叉引用的社区列表。

所提供的 GitHub 仓库，在确定「每个列表包含哪些论文」时具有权威性。

关于当前代码/权重/项目状态，需核实官方来源。
当来源不一致时，记录该分歧并说明首选证据及理由。

## Analytical rules 分析规则
1. 不要将 category（分类）与 evolution stage（演进阶段）混淆。
2. 六个阶段是能力演进框架，而非严格的时间先后顺序主张。
3. 规划辅助不自动等于动作生成。
4. 推理文本不自动等于推理驱动的策略。
5. 视频生成不自动等于 World Model。
6. VLA 与 WM 的简单共存**不是** Stage 6；需要有意义的融合。
7. 保留历史性/奠基性论文的重要性。

## Stopping rule 停止规则
不要深入阅读所有仓库中的每一篇论文。
当满足以下条件时，停止广泛发现：
- 13 个仓库全部扫描完毕；
- 实体已充分规范化；
- 频次统计已稳定；
- 存在一个站得住脚的 Top-30 候选池。

然后将深度验证集中在 Top 30 及直接相关的 bridge papers 上。

## Final quality checklist 最终质量检测清单
- 13 个仓库全部检查过。
- 频次统计使用「不同仓库」计数。
- 重复实体已规范化。
- 同名不同论文的情况保持分开。
- Top 30 不是仅由频次决定。
- 六个阶段都有代表。
- 遵守 VLM/VLA 边界。
- 推理分类基于其对 action/planning 的影响。
- World Model 分类检查 prediction/action conditioning/planning。
- VLA+WM 分类检查是否真正融合。
- 优先使用官方开源链接。
- 区分「有代码」与「可复现性」。
- 已核实仓库/权重的当前状态。
- 主要论断有证据支持。
