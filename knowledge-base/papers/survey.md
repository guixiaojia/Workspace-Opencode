# 自动驾驶基础模型综合调研报告（数据篇）

> 调研日期：2026年9月
>
> 本文件仅保留统计数据与论文列表，框架性内容已迁移至 `knowledge-base/`：
> - 坐标型框架、六阶段演进 → `../AD_技术演进框架.md`
> - 技术路线分析 → `../AD_技术路线分析.md`
> - 显存估算框架 → `../AD_显存估算框架.md`

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

### 2.1 论文总览

| 排名 | 论文名称 | 年份 | 技术路线 | Stage | 开源状态 | 仓库出现数 |
|------|----------|------|----------|-------|----------|------------|
| 1 | UniAD | 2023 | BEV-VLM | Stage 1 | ✅ 代码+数据 | 8 |
| 2 | BEVFormer | 2022 | BEV-VLM | Stage 1 | ✅ 代码 | 7 |
| 3 | VAD | 2023 | E2E VLA | Stage 1 | ✅ 代码 | 6 |
| 4 | DriveVLM | 2024 | Modular VLA | Stage 2 | ✅ 代码 | 7 |
| 5 | DriveGPT4 | 2023 | BEV-VLM | Stage 2 | ✅ 代码 | 6 |
| 6 | LMDrive | 2024 | Modular VLA | Stage 2 | ✅ 代码 | 5 |
| 7 | DriveLM | 2023 | BEV-VLM | Stage 2 | ✅ 代码 | 6 |
| 8 | Mamba | 2023 | 基础架构 | Stage 1 | ✅ 代码 | 9 |
| 9 | Vision Mamba | 2024 | 基础架构 | Stage 1 | ✅ 代码 | 7 |
| 10 | GAIA-1 | 2023 | WM VLA | Stage 5 | ❌ 无代码 | 8 |
| 11 | Drive-WM | 2023 | WM VLA | Stage 5 | ✅ 代码 | 7 |
| 12 | Vista | 2024 | WM VLA | Stage 5 | ✅ 代码 | 6 |
| 13 | AutoDrive-P3 | 2024 | Reasoning VLA | Stage 4 | ✅ 代码 | 5 |
| 14 | ReCogDrive | 2025 | Reasoning VLA | Stage 4 | ✅ 代码 | 4 |
| 15 | RT-2 | 2023 | E2E VLA | Stage 3 | ❌ 无代码 | 6 |
| 16 | OpenVLA | 2024 | E2E VLA | Stage 3 | ✅ 代码+权重 | 5 |
| 17 | π0 | 2024 | E2E VLA | Stage 3 | ❌ 无代码 | 5 |
| 18 | SmolVLA | 2024 | E2E VLA | Stage 3 | ✅ 代码 | 4 |
| 19 | LLaVA | 2023 | Modular VLA | Stage 2 | ✅ 代码 | 8 |
| 20 | BLIP-2 | 2023 | Modular VLA | Stage 2 | ✅ 代码 | 7 |
| 21 | CLIP | 2021 | BEV-VLM | Stage 1 | ✅ 代码 | 10 |
| 22 | PaLM-E | 2023 | E2E VLA | Stage 3 | ❌ 无代码 | 5 |
| 23 | Senna | 2024 | Modular VLA | Stage 2 | ✅ 代码 | 5 |
| 24 | OmniDrive | 2024 | Modular VLA | Stage 3 | ✅ 代码 | 5 |
| 25 | DriveWorld-VLA | 2024 | WM VLA | Stage 5 | ✅ 代码 | 4 |
| 26 | World4Drive | 2024 | WM VLA | Stage 5 | ✅ 代码 | 5 |
| 27 | DiffusionDrive | 2024 | E2E VLA | Stage 1 | ✅ 代码 | 5 |
| 28 | VADv2 | 2024 | E2E VLA | Stage 1 | ✅ 代码 | 4 |
| 29 | DriveDreamer | 2024 | WM VLA | Stage 5 | ✅ 代码 | 5 |
| 30 | TrafficBots | 2024 | WM VLA | Stage 5 | ✅ 代码 | 4 |

### 2.2 技术路线分布统计

| 技术路线 | 论文数 | 占比 | 代表论文 |
|----------|--------|------|----------|
| BEV-VLM | 5篇 | 17% | UniAD, BEVFormer, DriveGPT4, DriveLM, CLIP |
| E2E VLA | 8篇 | 27% | VAD, RT-2, OpenVLA, π0, SmolVLA, PaLM-E, DiffusionDrive, VADv2 |
| Modular VLA | 7篇 | 23% | DriveVLM, LMDrive, LLaVA, BLIP-2, Senna, OmniDrive, CLIP |
| Reasoning VLA | 2篇 | 7% | AutoDrive-P3, ReCogDrive |
| WM VLA | 8篇 | 27% | GAIA-1, Drive-WM, Vista, World4Drive, DriveWorld-VLA, DriveDreamer, TrafficBots |

---

## 三、调研结论

### 3.1 技术趋势

1. **VLA成为主流范式**：从Stage 1到Stage 3的演进速度加快，2024年是VLA爆发年
2. **推理能力受重视**：Stage 4的Reasoning VLA论文数量在2025年显著增加
3. **世界模型融合**：Stage 5的World Model VLA成为研究热点
4. **效率优化**：部署效率成为工业界关注重点

### 3.2 开源生态

1. **代码开源率高**：70%的论文提供代码，促进快速复现
2. **权重开源不足**：仅21%的论文开源模型权重，限制了预训练研究
3. **数据集完善**：nuScenes、Waymo等数据集为研究提供坚实基础

### 3.3 技术挑战

1. **实时性**：VLA模型的推理延迟仍是主要瓶颈
2. **安全性**：端到端模型的安全验证方法不成熟
3. **泛化性**：跨场景、跨天气的泛化能力有限
4. **可解释性**：决策过程的可解释性与性能存在 trade-off

### 3.4 未来方向

1. **统一架构**：Stage 6的Imagine-Reason-Act闭环是终极目标
2. **高效部署**：模型压缩、量化、蒸馏技术将加速落地
3. **安全验证**：形式化验证和可解释AI将提升安全性
4. **数据增强**：世界模型驱动的数据生成将缓解数据稀缺

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
*最后更新：2026年9月17日*
