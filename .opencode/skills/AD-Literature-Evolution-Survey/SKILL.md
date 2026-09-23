---
name: autonomous-driving-foundation-model-literature 自动驾驶基础模型文献研究
description: 分析多个 GitHub Awesome 列表与仓库中的自动驾驶基础模型文献，对重要论文进行排序，将其映射到六阶段技术演进框架，并识别可复现/开源的实现。
---

# 自动驾驶基础模型文献研究 Skill

## 前置准备

**执行本技能前，必须先读取以下知识库文件**：

1. `knowledge-base/AD_演进框架.md` — 六阶段技术演进路径、边界判断、技术路线分类
2. `knowledge-base/AD_分析模板.md` — 批量调研记录格式
3. `knowledge-base/AD_任务数据集与开源.md` — 任务分类、数据集、开源代码
4. `knowledge-base/AD_开发工具生态.md` — 开发环境、工具链

使用这些文件中的框架、术语和格式，确保分析的一致性。

---

## 目标

给定多个包含自动驾驶论文的 GitHub 仓库：
1. 从所有提供的仓库中构建论文池。
2. 规范化论文实体并对重复项去重。
3. 统计每篇论文出现在多少个**不同的**仓库中。
4. 使用仓库频次加技术重要性对论文排序。
5. 选出约 Top 30 核心论文。
6. 将 Top 30 映射到 `AD_演进框架.md` 中的六阶段演进框架。
7. 列出官方开源/可复现实现。
8. 区分「有代码」与「真正可复现」。

不要平均地机械地处理每一篇论文，而要聚焦于重复出现、奠基性、范式转变性和技术上有影响力的论文。

---

## 六阶段技术演进框架

**详细内容请参考**：`knowledge-base/AD_演进框架.md`

快速参考：

| Stage | 名称 | 核心特征 |
|-------|------|---------|
| 1 | 数据驱动型E2E | 纯视觉/信号输入，直接映射轨迹 |
| 2 | 语义增强型E2E | VLM 作为语义副驾，辅助规划 |
| 3 | 动作原生型VLA | VLM 被 VLA 吸纳，输出动作 |
| 4 | 认知推理型VLA | 显式 CoT/因果推理影响动作 |
| 5 | 预测模拟型VLA | VLA + World Model 融合 |
| 6 | 统一闭环 | VLA + Reasoning + WM 联合潜空间 |

---

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
10. https://github.com/KwanWaiPang/Awesome-VLA
11. https://github.com/honalele/Foundation-Models-Meet-Driving-World-Models
12. https://github.com/Yanyeoo/Awesome-Efficient-VLA4AD

如果用户提供更新的 URL，则增加上用户提供的 URL。

---

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
1. Primary stage（主要阶段）— 参考 `AD_演进框架.md`
2. Specific evolution node（具体演进节点）
3. Secondary stage(s)（次要阶段，如适用）
4. 为何归属此处
5. 是否为跨阶段桥接（bridge）

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

---

## Required outputs 要求的输出格式

**输出文件**：`analysis/survey.md`

按照 `knowledge-base/AD_分析模板.md` 中的"批量调研记录格式"生成报告。

### 主要内容

1. **调研统计**：各 Stage 的论文数量和占比
2. **Top 论文列表**：Rank | 论文/模型 | 年份 | 会议 | Stage | 演进节点 | 技术路线 | 开源
3. **各 Stage 详细分析**：每个 Stage 的代表论文和核心贡献
4. **技术路线分布**：各技术路线的论文数量和占比
5. **开源情况统计**：完全开源/部分开源/仅论文的数量
6. **关键发现**：重要的观察和结论
7. **趋势观察**：技术发展趋势

---

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

---

## Analytical rules 分析规则

1. 不要将 category（分类）与 evolution stage（演进阶段）混淆。
2. 六个阶段是能力演进框架，而非严格的时间先后顺序主张。
3. 规划辅助不自动等于动作生成。
4. 推理文本不自动等于推理驱动的策略。
5. 视频生成不自动等于 World Model。
6. VLA 与 WM 的简单共存**不是** Stage 6；需要有意义的融合。
7. 保留历史性/奠基性论文的重要性。

---

## Stopping rule 停止规则

不要深入阅读所有仓库中的每一篇论文。
当满足以下条件时，停止广泛发现：
- 13 个仓库全部扫描完毕；
- 实体已充分规范化；
- 频次统计已稳定；
- 存在一个站得住脚的 Top-30 候选池。

然后将深度验证集中在 Top 30 及直接相关的 bridge papers 上。

---

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
- 输出文件已保存到 `analysis/survey.md`。
