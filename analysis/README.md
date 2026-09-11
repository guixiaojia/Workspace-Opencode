# Analysis - 论文分析记录

> 本文件夹存放论文分析报告，由 AD-* 系列技能生成。

---

## 文件结构

```
analysis/
├── README.md                              ← 本文件
├── survey.md                              ← 批量调研记录（AD-Literature-Evolution-Survey 生成）
├── [年份]_[会议]_[模型名称]_[核心任务].md  ← 单篇论文分析（AD-Single-Paper-Technical-Audit 生成）
└── ...
```

---

## 文件命名规范

### 单篇论文分析

**格式**：`[年份]_[会议]_[模型名称]_[核心任务].md`

**示例**：
- `2026_ICRA_UniDriveVLA_Planning.md`
- `2025_CVPR_MagicDrive_Generation.md`
- `2024_NeurIPS_OpenVLA_Action.md`

**字段说明**：
- `年份`：论文发表年份
- `会议`：发表会议/期刊缩写（ICRA/CVPR/ECCV/NeurIPS/ICLR/arXiv 等）
- `模型名称`：论文提出的主要模型名称
- `核心任务`：主要任务类型（Planning/Perception/VLA/Generation/VQA 等）

### 批量调研记录

**文件**：`survey.md`（固定名称，持续追加更新）

---

## 内容格式

所有分析报告遵循 `knowledge-base/AD_分析模板.md` 中定义的标准格式。

主要包含：
1. 模型组件
2. 参数状态
3. 微调方法
4. 训练范式
5. 技术定位
6. 任务与数据集
7. 复现信息

---

## 生成方式

| 技能 | 输入 | 输出 | 说明 |
|------|------|------|------|
| **AD-Single-Paper-Technical-Audit** | 一篇论文（PDF/链接） | `analysis/[年份]_[会议]_[模型]_[任务].md` | 深度分析，侧重技术构型 |
| **AD-Literature-Evolution-Survey** | 多个 GitHub 仓库 | `analysis/survey.md` | 批量调研，侧重演进阶段 |

---

## 维护原则

1. **只增不删**：分析报告只追加，不删除已有内容
2. **命名规范**：严格遵循命名规范，便于检索
3. **格式一致**：使用统一的模板格式
4. **及时更新**：发现错误或新信息时更新报告

---

## 索引

> （无需手动维护，直接浏览文件夹即可）
