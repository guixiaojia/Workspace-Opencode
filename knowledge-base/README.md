# Knowledge Base - 自动驾驶大模型知识库

> 本文件夹存放自动驾驶大模型领域的核心知识，供 AD-* 系列技能引用。

---

## 文件结构

```
knowledge-base/
├── README.md                    ← 本文件
├── AD_演进框架.md               ← 六阶段技术演进路径
├── AD_分析模板.md               ← 论文分析报告的标准格式
├── AD_模型训练要素.md           ← 参数状态、微调方法、训练范式
├── AD_任务数据集与开源.md       ← 任务分类、数据集、开源代码
├── AD_开发工具生态.md           ← 开发环境、工具链、框架
└── 项目环境py311.md             ← 本地 Python 环境详情
```

---

## 文件说明

| 文件 | 内容 | 更新频率 | 主要引用者 |
|------|------|---------|-----------|
| **AD_演进框架.md** | 六阶段技术演进路径、边界判断、技术路线分类 | 低（框架性内容） | AD-Literature-Evolution-Survey, AD-Single-Paper-Technical-Audit |
| **AD_分析模板.md** | 论文分析报告的标准格式、模板 | 低（格式稳定） | AD-Single-Paper-Technical-Audit, AD-Literature-Evolution-Survey |
| **AD_模型训练要素.md** | 参数状态、微调方法、训练范式、配方 | 中（技术发展） | AD-Single-Paper-Technical-Audit |
| **AD_任务数据集与开源.md** | 任务分类、数据集、开源代码统计 | 高（持续更新） | AD-Literature-Evolution-Survey |
| **AD_开发工具生态.md** | 开发环境、工具链、框架、硬件约束 | 中（环境变化） | AD-Single-Paper-Technical-Audit |
| **项目环境py311.md** | 本地 Python 环境详情、包版本 | 中（环境变化） | AD-Single-Paper-Technical-Audit |

---

## 更新原则

1. **独立性**：每个文件独立维护，避免内容重复
2. **稳定性**：框架性内容保持稳定，细节内容可频繁更新
3. **可追溯**：更新时记录主要变更（可在文件头部添加更新日志）

---

## 引用规则

技能引用知识库时，应：
1. 先读取相关文件
2. 使用文件中的框架和术语
3. 保持与知识库的一致性

---

## 维护者

- 主要维护：用户
- 辅助更新：AI 技能（在分析过程中发现新知识时建议更新）
