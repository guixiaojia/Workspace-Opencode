# Awesome-LLM4AD（ThinkLab-SJTU）论文梳理：任务 / 数据集 / 开源代码

> 数据来源：`github.com/thinklab-sjtu/awesome-llm4ad` 仓库 README（5536 行，约 458 KB）
> 抓取时间：2026-09-09；README 最新条目 Publish Date 为 2026.06.18
> 条目规模：Papers 章节 522 篇 + Datasets 章节 15 条（WorkShop 2 个 Challenge 数据集 MAPLM、UCU 一并纳入）

## 一、任务（Task）总览

| 任务类别（README 原始写法示例） | 论文数（占比） | 任务说明 |
|---|---:|---|
| Planning<br>（Planning、Multi Agent Planning、Planning, Generation、Planning + QA） | 214（37.2%） | 规划 / 决策 / 轨迹生成（含闭环规划、多车协同） |
| Perception<br>（Perception、Perception, Planning、Object Detection） | 71（12.3%） | 感知：目标检测、跟踪、占据预测（Occ）、BEV 理解 |
| VQA / QA<br>（VQA、QA、VQA, Planning、QA, Prompt Engineer） | 66（11.5%） | 驾驶场景视觉问答、自然语言指令理解、可解释问答 |
| Generation<br>（Generation、Scenario Generation、Code generation, Planning） | 64（11.1%） | 场景 / 视频 / 数据生成、世界模型、场景合成 |
| End-to-End<br>（End-to-End、End-to-End, Generation） | 59（10.3%） | 端到端自动驾驶：传感器直出轨迹 |
| 评测与基准<br>（Evaluation、Benchmark、Benchmark & Evaluation） | 35（6.1%） | 评测协议、鲁棒性与可信度基准构建 |
| Prediction<br>（Prediction、Trajectory Prediction、Motion Prediction） | 33（5.7%） | 轨迹预测 / 运动预测 / 行为预测 |
| 推理与解释<br>（Reasoning、Planning, Reasoning、Explainable Driving） | 19（3.3%） | 链式推理、决策解释、可解释驾驶 |
| 数据集构建<br>（Datasets + VQA、Dataset + Reasoning） | 6（1.0%） | 以发布数据集为主要贡献 |
| 场景理解<br>（Scene Understanding、Context Recognition） | 3（0.5%） | 风险 / 意图 / 上下文理解 |
| 奖励设计<br>（Reward Design、Reward Generation） | 2（0.3%） | 用 VLM 生成强化学习奖励信号 |
| 框架与工具<br>（Framework、Development） | 2（0.3%） | 仿真 / 训练框架与开发工具 |
| 导航<br>（Navigation） | 1（0.2%） | 语言指令导航 |
| **合计** | **575（100.0%）** | |

## 二、数据集（Datasets）总览

> ⚠ nuScenes 为基础数据集，其衍生集已在名称后标注「（nuScenes 衍生）」；仿真 / 闭环环境标注「（仿真 / 闭环环境）」；计数「—」表示仅 README 正文提及、未被 `Datasets:` 字段标注（非 0）

| 数据集 / 环境（类型归属） | 被使用论文数 | 一句话说明 |
|---|---:|---|
| **▎真实基础集** | | |
| nuScenes | 106 | 6 相机 + LiDAR + 雷达，1000 场景 |
| Waymo（Open） | 21 | Waymo 家族总称；明细见「Waymo 衍生」组 |
| nuPlan | 12 | 大规模真实轨迹规划集 |
| KITTI | 5 | 经典视觉基准 |
| highD | 4 | 高速公路自然驾驶轨迹 |
| BDD100K | 3 | 大规模多场景驾驶数据 |
| DRAMA | 3 | 风险定位与描述 |
| CommonRoad | 2 | 运动规划基准 |
| Argoverse | 1 | 轨迹预测 / 矢量地图 |
| BDD | 1 | BDD 系列 |
| BDD-A | 1 | BDD 注意力标注 |
| BDD-X dataset | 1 | BDD 驾驶行为解释 |
| Cityscapes | 1 | 语义分割 |
| CODA | 1 | 长尾极端场景 |
| CODA-LM | 1 | CODA 语言扩展 |
| corner-case-focused CODA | 1 | CODA 极端子集 |
| DAIR-V2X | 1 | 车路协同 |
| DeepAccident | 1 | 事故场景 |
| DriveObj3D | 1 | 3D 目标指代 |
| Great-MSD | 1 | 低空无人机多模态 |
| HDD | 1 | 驾驶行为 |
| interPlan | 1 | 交互式规划 |
| KITTI-360 | 1 | KITTI 360° 扩展 |
| LingoQA | 1 | 驾驶问答评测 |
| Mapillary | 1 | 街景图像 |
| Mapillary Vistas | 1 | 语义分割 |
| MoCAD | 1 | 驾驶意图 |
| NGSIM | 1 | 自然驾驶轨迹 |
| nuPlan Closed-Loop Non-Reactive Challenge | 1 | nuPlan 闭环子集 |
| nuPlan Closed-Loop Reactive Hard20 | 1 | nuPlan 闭环子集 |
| OpenLane-V2 | 1 | 车道拓扑 |
| OpenOcc | 1 | 占据预测 |
| OpenStreetMap | 1 | 开源地图 |
| ORAD-3D | 1 | 3D 场景问答 |
| PandaSet | 1 | 多模态数据集 |
| RELLIS-3D | 1 | 越野语义分割 |
| ROADWork | 1 | 道路施工场景 |
| rounD | 1 | 环岛轨迹 |
| SafeDrive228K | 1 | 安全驾驶数据 |
| SemanticKITTI | 1 | KITTI 语义分割 |
| StyleDrive | 1 | 风格化驾驶 |
| Talk2Car | 1 | 语言指代检测 |
| TS-1M | 1 | 百万级轨迹 |
| **▎nuScenes 衍生** | | |
| DriveLM<br>（nuScenes 衍生） | 7 | 图结构 QA（感知-预测-规划） |
| NuScenes-QA<br>（nuScenes 衍生） | 4 | QA 标注（45.9 万问答对） |
| NuPrompt<br>（nuScenes 衍生） | 2 | 语言提示目标指代（未公开） |
| ADV-NuScenes<br>（nuScenes 衍生） | 1 | 对抗鲁棒性评测 |
| doScenes<br>（nuScenes 衍生） | 1 | 乘客指令↔真值轨迹对齐 |
| DriveLM-nuScenes<br>（nuScenes 衍生） | 1 | DriveLM 的 nuScenes 版本 |
| GroundView<br>（nuScenes 衍生） | 1 | 视觉定位评测（基于 nuImages） |
| nuCaption<br>（nuScenes 衍生） | 1 | 场景描述评测（基于 nuImages） |
| nuImages<br>（nuScenes 衍生） | 1 | 官方 2D 图像扩展 |
| nuView<br>（nuScenes 衍生） | 1 | 视觉定位评测（基于 nuImages） |
| Occ3D-nuScenes<br>（nuScenes 衍生） | 1 | 3D 占据标注 |
| Drive-nuScenes<br>（nuScenes 衍生） | — | nuScenes 驾驶任务变体 |
| nuScenes-corner<br>（nuScenes 衍生） | — | 角落场景（corner case） |
| nuScenes-FG<br>（nuScenes 衍生） | — | 前景重标注（24.1 万图像-掩码对） |
| nuScenes-GR-20K<br>（nuScenes 衍生） | — | 2 万条生成式推理数据 |
| NuScenes-S<br>（nuScenes 衍生） | — | 结构化场景表示 |
| NuScenes-SpatialQA<br>（nuScenes 衍生） | — | 空间理解与推理 QA |
| **▎Waymo 衍生** | | |
| Waymo Open Dataset<br>（Waymo 衍生） | 8 | Waymo 基础感知集 |
| Waymo Open Motion Dataset (WOMD)<br>（Waymo 衍生） | 6 | 运动预测子集 |
| Waymo Open E2E (WOD-E2E)<br>（Waymo 衍生） | 4 | 端到端驾驶子集 |
| Waymo Sim Agents<br>（Waymo 衍生） | 2 | 仿真智能体评测 |
| Waymax<br>（Waymo 衍生） | 1 | 可微分仿真器 |
| WOMD-Reasoning<br>（Waymo 衍生） | 1 | WOMD 推理评测 |
| WOSAC<br>（Waymo 衍生） | 1 | 仿真智能体评测 |
| **▎仿真 / 闭环环境** | | |
| NAVSIM<br>（仿真 / 闭环环境） | 63 | nuPlan 非反应式闭环基准 |
| Bench2Drive<br>（仿真 / 闭环环境） | 31 | CARLA 闭环端到端基准 |
| CARLA<br>（仿真 / 闭环环境） | 30 | CARLA 仿真器 |
| HighwayEnv<br>（仿真 / 闭环环境） | 9 | 高速公路 RL 环境 |
| MetaDrive<br>（仿真 / 闭环环境） | 2 | 轻量 RL 仿真器 |
| 4DWorldBench<br>（仿真 / 闭环环境） | 1 | 4D 世界生成评测 |
| AirSim<br>（仿真 / 闭环环境） | 1 | 无人机 / 驾驶仿真 |
| Carla Leadboard V2<br>（仿真 / 闭环环境） | 1 | CARLA 闭环榜单 |
| CARLA-Garage Dataset<br>（仿真 / 闭环环境） | 1 | CARLA 场景集 |
| Chat2Scenario<br>（仿真 / 闭环环境） | 1 | 场景生成环境 |
| DOS<br>（仿真 / 闭环环境） | 1 | 场景生成环境 |
| DrivingGen<br>（仿真 / 闭环环境） | 1 | 场景生成环境 |
| LangAuto<br>（仿真 / 闭环环境） | 1 | CARLA 语言指令基准 |
| SMARTS<br>（仿真 / 闭环环境） | 1 | 多智能体交通仿真 |
| SUMO<br>（仿真 / 闭环环境） | 1 | 交通流仿真 |
| **▎其他基准 / 长尾** | | |
| DriveLMM-o1 | 2 | — |
| ADGV-Bench | 1 | — |
| ALOHA | 1 | — |
| AutoDriDM | 1 | — |
| Box-QAymo | 1 | — |
| CALVIN | 1 | — |
| DeepAccident-CCoT | 1 | — |
| DeepMind Control Suite | 1 | — |
| DriveX | 1 | — |
| DSBench | 1 | — |
| FidelityDrivingBench | 1 | — |
| FSU-QA | 1 | — |
| IEDD | 1 | — |
| Intention-Drive | 1 | — |
| LIBERO | 1 | — |
| MD-NEX Outdoor-Driving | 1 | — |
| OODBench | 1 | — |
| OR-C2P Benchmark | 1 | — |
| PotentialRiskQA | 1 | — |
| RoadSceneBench | 1 | — |
| RoboDriveBench | 1 | — |
| RoboSense Challenge | 1 | — |
| SIGBench | 1 | — |
| Simplenv-Bridge | 1 | — |
| STRIDE-QA | 1 | — |
| STSBench | 1 | — |
| SUP-AD | 1 | — |
| TAD | 1 | — |
| UCU Dataset | 1 | — |
| WEDGE | 1 | — |
| 合计 | 411 |  |

## 三、开源总览（提供 Code 的论文）

> 共收录 111 篇（大类少于 5 篇的不予列出：Reasoning & Explanation 1 篇、Framework / Toolchain 1 篇、Scene Understanding 1 篇、其他 4 篇）｜另有约 64 篇仅有 Project Page 无 Code，未列入

| 任务 | Datasets | 论文名称 | Code | 发布日期 |
|---|---|---|---|---|
| **▎Planning（54 篇）** | | | | |
| Planning | Bench2Drive | [BLUE: Toward Better Language Use in Efficient Vision-Language-Action Models for Autonomous Driving](https://arxiv.org/abs/2606.08684) | [BLUE](https://github.com/George-Ling3/BLUE) | 2026.06.07 |
| Planning | NAVSIM | [ChainFlow-VLA: Causal Flow Planning with Vision-Language Models](https://arxiv.org/abs/2605.23270) | [ChainFlow-VLA](https://github.com/AFARI-Research/ChainFlow-VLA) | 2026.05.22 |
| Planning | Bench2Drive | [DeepSight: Long-Horizon World Modeling via Latent States Prediction for End-to-End Autonomous Driving](https://arxiv.org/abs/2605.10564) | [DeepSight](https://github.com/hotdogcheesewhite/DeepSight) | 2026.05.11 |
| Planning | nuScenes | [GSDrive: Reinforcing Driving Policies by Multi-mode Trajectory Probing with 3D Gaussian Splatting Environment](https://arxiv.org/abs/2604.28111) | [GSDrive](https://github.com/ZionGo6/GSDrive) | 2026.04.30 |
| Planning | NAVSIM、nuScenes | [OneDrive: Unified Multi-Paradigm Driving with Vision-Language-Action Models](https://arxiv.org/abs/2604.17915) | [OneDrive](https://github.com/Z1zyw/OneDrive) | 2026.04.20 |
| Planning · Perception, Planning | nuScenes、Bench2Drive | [UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving](https://arxiv.org/abs/2604.02190) | [UniDriveVLA](https://github.com/xiaomi-research/unidrivevla) | 2026.04.02 |
| Planning | highD、rounD | [C-TRAIL: A Commonsense World Framework for Trajectory Planning in Autonomous Driving](https://arxiv.org/abs/2603.29908) | [C-TRAIL](https://github.com/ZhihongCui/CTRAIL) | 2026.03.31 |
| Planning · Perception, Prediction, Planning | nuScenes、NAVSIM | [$AutoDrive\text{-}P^3$: Unified Chain of Perception-Prediction-Planning Thought via Reinforcement Fine-Tuning](https://arxiv.org/abs/2603.28116) | [$AutoDrive\text{-}P^3$](https://github.com/haha-yuki-haha/AutoDrive-P3) | 2026.03.30 |
| Planning | Bench2Drive | [Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving](https://arxiv.org/abs/2603.25740) | [Drive My Way](https://github.com/tasl-lab/DMW) | 2026.03.26 |
| Planning | nuScenes、NAVSIM | [DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving](https://arxiv.org/abs/2603.19675) | [DynFlowDrive](https://github.com/xiaolul2/DynFlowDrive) | 2026.03.20 |
| Planning | CARLA | [DriveVLM-RL: Neuroscience-Inspired Reinforcement Learning with Vision-Language Models for Safe and Deployable Autonomous Driving](https://arxiv.org/abs/2603.18315) | [DriveVLM-RL](https://zilin-huang.github.io/DriveVLM-RL-website/) | 2026.03.18 |
| Planning | OR-C2P Benchmark | [Wild-Drive: Off-Road Scene Captioning and Path Planning via Robust Multi-modal Routing and Efficient Large Language Model](https://arxiv.org/abs/2603.00694) | [Wild-Drive](https://github.com/wangzihanggg/Wild-Drive) | 2026.02.28 |
| Planning | nuScenes | [MindDriver: Introducing Progressive Multimodal Reasoning for Autonomous Driving](https://arxiv.org/abs/2602.21952) | [MindDriver](https://github.com/hotdogcheesewhite/MindDriver) | 2026.02.25 |
| Planning | NAVSIM | [MeanFuser: Fast One-Step Multi-Modal Trajectory Generation and Adaptive Reconstruction via MeanFlow for End-to-End Autonomous Driving](https://arxiv.org/abs/2602.20060) | [MeanFuser](https://github.com/wjl2244/MeanFuser) | 2026.02.23 |
| Planning | NAVSIM | [DriveFine: Refining-Augmented Masked Diffusion VLA for Precise and Robust Driving](https://arxiv.org/abs/2602.14577) | [DriveFine](https://github.com/MSunDYY/DriveFine) | 2026.02.16 |
| Planning | nuScenes、NAVSIM | [ResWorld: Temporal Residual World Model for End-to-End Autonomous Driving](https://arxiv.org/abs/2602.10884) | [ResWorld](https://github.com/mengtan00/ResWorld.git) | 2026.02.11 |
| Planning | NAVSIM、nuScenes | [DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521) | [DriveWorld-VLA](https://github.com/liulin815/DriveWorld-VLA.git) | 2026.02.06 |
| Planning | doScenes、nuScenes | [Natural Language Instructions for Scene-Responsive Human-in-the-Loop Motion Planning in Autonomous Driving using Vision-Language-Action Models](https://arxiv.org/abs/2602.04184) | [doScenes-VLM-Planning](https://github.com/Mi3-Lab/doScenes-VLM-Planning) | 2026.02.04 |
| Planning · Perception, Prediction, Planning, Generation | — | [UniDWM: Towards a Unified Driving World Model via Multifaceted Representation Learning](https://arxiv.org/abs/2602.01536) | [UniDWM](https://github.com/Say2L/UniDWM) | 2026.02.02 |
| Planning | nuScenes | [LLaViDA: A Large Language Vision Driving Assistant for Explicit Reasoning and Enhanced Trajectory Planning](https://arxiv.org/abs/2512.18211) | [LLaViDA](https://github.com/) | 2025.12.20 |
| Planning | nuScenes | [DrivePI: Spatial-aware 4D MLLM for Unified Autonomous Driving Understanding, Perception, Prediction and Planning](https://arxiv.org/abs/2512.12799) | [DrivePI](https://github.com/happinesslz/DrivePI) | 2025.12.14 |
| Planning | NAVSIM | [WAM-Diff: A Masked Diffusion VLA Framework with MoE and Online Reinforcement Learning for Autonomous Driving](https://arxiv.org/abs/2512.11872) | [WAM-Diff](https://github.com/fudan-generative-vision/WAM-Diff) | 2025.12.06 |
| Planning | NAVSIM、nuScenes | [WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving](https://arxiv.org/abs/2512.06112) | [WAM-Flow](https://github.com/fudan-generative-vision/WAM-Flow) | 2025.12.05 |
| Planning | Bench2Drive、nuScenes、NAVSIM、ADV-NuScenes | [GuideFlow: Constraint-Guided Flow Matching for Planning in End-to-End Autonomous Driving](https://arxiv.org/abs/2511.18729) | [GuideFlow](https://github.com/liulin815/GuideFlow) | 2025.11.24 |
| Planning | CARLA | [QuickLAP: Quick Language-Action Preference Learning for Autonomous Driving Agents](https://arxiv.org/abs/2511.17855) | [QuickLAP](https://github.com/MIT-CLEAR-Lab/QuickLAP) | 2025.11.22 |
| Planning | LangAuto | [Enhancing LLM-based Autonomous Driving with Modular Traffic Light and Sign Recognition](https://arxiv.org/abs/2511.14391) | [TLS-Assist](https://github.com/iis-esslingen/TLS-Assist) | 2025.11.18 |
| Planning | — | [AdaDrive: Self-Adaptive Slow-Fast System for Language-Grounded Autonomous Driving](https://arxiv.org/abs/2511.06253) | [AdaDrive](https://github.com/ReaFly/AdaDrive) | 2025.11.09 |
| Planning | — | [Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail](https://arxiv.org/abs/2511.00088) | [Alpamayo-R1](https://github.com/NVlabs/alpamayo) | 2025.10.30 |
| Planning | nuPlan、interPlan | [Flow Matching-Based Autonomous Driving Planning with Advanced Interactive Behavior Modeling](https://arxiv.org/abs/2510.11083) | [Flow-Planner](https://github.com/DiffusionAD/Flow-Planner) | 2025.10.13 |
| Planning | — | [Game-Theoretic Risk-Shaped Reinforcement Learning for Safe Autonomous Driving](https://arxiv.org/abs/2510.10960) | [GTR2L](https://github.com/DanielHu197/GTR2L) | 2025.10.13 |
| Planning | CODA、Waymo（Open） | [Nav-EE: Navigation-Guided Early Exiting for Efficient Vision-Language Models in Autonomous Driving](https://arxiv.org/abs/2510.01795) | [Nav-EE](https://anonymous.4open.science/r/Nav-EE-BBC4) | 2025.10.02 |
| Planning | CommonRoad | [Learning to Sample: Reinforcement Learning-Guided Sampling for Autonomous Vehicle Motion Planning](https://arxiv.org/abs/2509.24313) | [Learning-to-Sample](https://github.com/TUM-AVS/Learning-to-Sample) | 2025.09.29 |
| Planning | — | [VLM-UDMC: VLM-Enhanced Unified Decision-Making and Motion Control for Urban Autonomous Driving](https://arxiv.org/abs/2507.15266) | [VLM-UDMC](https://github.com/henryhcliu/vlmudmc.git) | 2025.07.21 |
| Planning | NAVSIM | [Epona: Autoregressive Diffusion World Model for Autonomous Driving](https://arxiv.org/abs/2506.24113) | [Epona](https://github.com/Kevin-thu/Epona/) | 2025.06.30 |
| Planning | nuPlan、nuScenes、Waymo（Open）、Bench2Drive、CARLA-Garage Dataset | [AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning](https://arxiv.org/abs/2506.13757) | [AutoVLA](https://github.com/ucla-mobility/AutoVLA) | 2025.06.16 |
| Planning | NAVSIM | [ReCogDrive: A Reinforced Cognitive Framework for End-to-End Autonomous Driving](https://arxiv.org/abs/2506.08052) | [ReCogDrive](https://xiaomi-research.github.io/recogdrive/) | 2025.06.09 |
| Planning · Generation, Planning | nuScenes | [FutureSightDrive: Thinking Visually with Spatio-Temporal CoT for Autonomous Driving](https://arxiv.org/abs/2505.17685) | [FSDrive](https://github.com/MIV-XJTU/FSDrive) | 2025.05.23 |
| Planning | Bench2Drive | [DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving](https://arxiv.org/abs/2505.16278) | [DriveMoE](https://github.com/Thinklab-SJTU/DriveMoE) | 2025.05.22 |
| Planning · VQA, Planning | — | [OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model](https://arxiv.org/abs/2503.23463) | [OpenDriveVLA](https://github.com/DriveVLA/OpenDriveVLA) | 2025.03.30 |
| Planning | Bench2Drive | [ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation](https://arxiv.org/abs/2503.19755) | [ORION](https://github.com/xiaomi-mlab/Orion) | 2025.03.25 |
| Planning | HighwayEnv（仿真） | [Large Language Model guided Deep Reinforcement Learning for Decision Making in Autonomous Driving](https://arxiv.org/abs/2412.18511) | [LGDRL](https://github.com/bitmobility/LGDRL) | 2024.12.24 |
| Planning · VQA, Planning | nuScenes、DriveX | [Senna: Bridging Large Vision-Language Models and End-to-End Autonomous Driving](https://arxiv.org/abs/2410.22313) | [Senna](https://github.com/hustvl/Senna) | 2024.10.29 |
| Planning | — | [CANVAS: Commonsense-Aware Navigation System for Intuitive Human-Robot Interaction](https://arxiv.org/abs/2410.01273) | [CANVAS](https://github.com/worv-ai/canvas) | 2024.10.02 |
| Planning | DAIR-V2X | [V2X-VLM: End-to-End V2X Cooperative Autonomous Driving Through Large Vision-Language Models](https://arxiv.org/abs/2408.09251) | [V2X-VLM](https://github.com/zilin-huang/V2X-VLM) | 2024.08.09 |
| Planning | nuPlan Closed-Loop Reactive Hard20 | [Asynchronous Large Language Model Enhanced Planner for Autonomous Driving](https://arxiv.org/abs/2406.14556) | [AsyncDriver](https://github.com/memberRE/AsyncDriver) | 2024.06.20 |
| Planning · Code generation, Planning | CARLA（仿真） | [LangProp: A code optimization framework using Language Models applied to driving](https://openreview.net/forum?id=UgTrngiN16) | [LangProp](https://github.com/shuishida/LangProp) | 2024.01.18 |
| Planning · Planning + Explanation | CARLA（仿真） | [DriveMLM: Aligning Multi-Modal Large Language Models with Behavioral Planning States for Autonomous Driving](https://arxiv.org/abs/2312.09245) | [official](https://github.com/OpenGVLab/DriveMLM) | 2023.12.14 |
| Planning · Planning + Datasets | CARLA（仿真） | [LMDrive: Closed-Loop End-to-End Driving with Large Language Models](https://arxiv.org/abs/2312.07488) | [official](https://github.com/opendilab/LMDrive) | 2023.12.12 |
| Planning | HighwayEnv（仿真） | [Empowering Autonomous Driving with Large Language Models: A Safety Perspective](https://arxiv.org/abs/2312.00812) | [official](https://github.com/wangyixu14/llm_conditioned_mpc_ad) | 2023.11.28 |
| Planning · Generation Planning/Control Planning + VQA | nuScenes、data collection using RL experts in simulator | [DrivingDiffusion: Layout-Guided multi-view driving scene video generation with latent diffusion model](https://arxiv.org/abs/2310.07771) | [official ; official](https://sites.google.com/view/llm-mpc) | 2023.10.04 |
| Planning · Planning/Control + VQA Planning(Fine-tuning Pre-trained Model) | nuScenes | [Talk2BEV: Language-enhanced Bird’s-eye View Maps for Autonomous Driving](https://arxiv.org/abs/2310.02251) | [Talk2BEV ; GPT-Driver](https://github.com/llmbev/talk2bev) | 2023.10.03 |
| Planning | — | [TrafficGPT: Viewing, Processing and Interacting with Traffic Foundation Models](https://arxiv.org/abs/2309.06719) | [official](https://github.com/lijlansg/TrafficGPT.git) | 2023.09.13 |
| Planning | HighwayEnv（仿真） | [Drive Like a Human: Rethinking Autonomous Driving with Large Language Models](https://browse.arxiv.org/abs/2307.07162) | [official](https://github.com/PJLab-ADG/DriveLikeAHuman) | 2023.07.14 |
| Planning · Benchmark & Planning | — | [OmniDrive: A Holistic LLM-Agent Framework for Autonomous Driving with 3D Perception Reasoning and Planning](https://arxiv.org/abs/2405.01533) | [OmniDrive](https://github.com/NVlabs/OmniDrive) | — |
| **▎End-to-End（6 篇）** | | | | |
| End-to-End | CARLA | [Found-RL: foundation model-enhanced reinforcement learning for autonomous driving](https://arxiv.org/abs/2602.10458) | [Found-RL](https://github.com/ys-qu/found-rl) | 2026.02.11 |
| End-to-End | CARLA | [VLDrive: Vision-Augmented Lightweight MLLMs for Efficient Language-grounded Autonomous Driving](https://arxiv.org/abs/2511.06256) | [VLDrive](https://github.com/ReaFly/VLDrive) | 2025.11.09 |
| End-to-End | nuScenes | [CoIRL-AD: Collaborative-Competitive Imitation-Reinforcement Learning in Latent World Models for Autonomous Driving](https://arxiv.org/abs/2510.12560) | [CoIRL-AD](https://github.com/SEU-zxj/CoIRL-AD) | 2025.10.14 |
| End-to-End | Bench2Drive | [CoReVLA: A Dual-Stage End-to-End Autonomous Driving Framework for Long-Tail Scenarios via Collect-and-Refine](https://arxiv.org/abs/2509.15968) | [CoReVLA](https://github.com/FanGShiYuu/CoReVLA) | 2025.09.19 |
| End-to-End | nuScenes、NAVSIM | [World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model](https://arxiv.org/abs/2507.00603) | [World4Drive](https://github.com/ucaszyp/World4Drive) | 2025.07.01 |
| End-to-End | nuScenes | [NetRoller: Interfacing General and Specialized Models for End-to-End Autonomous Driving](https://arxiv.org/abs/2506.14589) | [NetRoller](https://github.com/Rex-sys-hk/NetRoller) | 2025.06.17 |
| **▎Perception（8 篇）** | | | | |
| Perception | nuScenes、KITTI | [NOVA: Next-step Open-Vocabulary Autoregression for 3D Multi-Object Tracking in Autonomous Driving](https://arxiv.org/abs/2603.06254) | [NOVA](https://github.com/xifen523/NOVA) | 2026.03.06 |
| Perception | KITTI | [LiFlow: Flow Matching for 3D LiDAR Scene Completion](https://arxiv.org/abs/2602.02232) | [LiFlow](https://github.com/matteandre/LiFlow) | 2026.02.02 |
| Perception | DriveObj3D | [Rethinking Driving World Model as Synthetic Data Generator for Perception Tasks](https://arxiv.org/abs/2510.19195) | [Dream4Drive](https://github.com/wm-research/Dream4Drive) | 2025.10.22 |
| Perception | Mapillary Vistas | [Mapillary Vistas Validation for Fine-Grained Traffic Signs: A Benchmark Revealing Vision-Language Model Limitations](https://arxiv.org/abs/2508.02047) | [relabeling](https://github.com/nec-labs-ma/relabeling) | 2025.08.04 |
| Perception | — | [NRSeg: Noise-Resilient Learning for BEV Semantic Segmentation via Driving World Models](https://arxiv.org/abs/2507.04002) | [NRSeg](https://github.com/lynn-yu/NRSeg) | 2025.07.05 |
| Perception | — | [On the Natural Robustness of Vision-Language Models Against Visual Perception Attacks in Autonomous Driving](https://arxiv.org/abs/2506.11472) | [V2LM](https://github.com/pedram-mohajer/V2LM) | 2025.06.13 |
| Perception · Detection/Prediction | — | [GPT-4 Enhanced Multimodal Grounding for Autonomous Driving: Leveraging Cross-Modal Attention with Large Language Models](https://arxiv.org/abs/2312.03543) | [official](https://github.com/Petrichor625/Talk2car_CAVG) | 2023.12.06 |
| Perception · Detection + VQA Tracking | DRAMA、nuScenes、NuPrompt | [HiLM-D: Towards High-Resolution Understanding in Multimodal Large Language Models for Autonomous Driving](https://arxiv.org/abs/2309.05186) | [official](https://github.com/wudongming97/Prompt4Driving) | 2023.09.11 |
| **▎Prediction（6 篇）** | | | | |
| Prediction | WOSAC | [AutoWorld: Scaling Multi-Agent Traffic Simulation with Self-Supervised World Models](https://arxiv.org/abs/2603.28963) | [AutoWorld](https://github.com/auto-world/autoworld) | 2026.03.30 |
| Prediction · Prediction, Generation | Waymo Open Motion Dataset (WOMD)、nuPlan | [VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652) | [VectorWorld](https://github.com/jiangchaokang/VectorWorld) | 2026.03.18 |
| Prediction | — | [Orbis: Overcoming Challenges of Long-Horizon Prediction in Driving World Models](https://arxiv.org/abs/2507.13162) | [Orbis](https://lmb-freiburg.github.io/orbis.github.io/) | 2025.07.17 |
| Prediction | — | [DriveMRP: Enhancing Vision-Language Models with Synthetic Motion Data for Motion Risk Prediction](https://arxiv.org/abs/2507.02948) | [DriveMRP](https://github.com/SII-HZY/DriveMRP) | 2025.06.28 |
| Prediction | — | [Exploring the Potential of Multi-Modal AI for Driving Hazard Prediction](https://ieeexplore.ieee.org/document/10568360) | [DHPR](https://github.com/DHPR-dataset/DHPR-dataset) | 2024.06.21 |
| Prediction · Trajectory Prediction | CARLA（仿真） | [LeGo-Drive: Language-enhanced Goal-oriented Closed-Loop End-to-End Autonomous Driving](https://arxiv.org/abs/2403.20116) | [LeGo-Drive](https://github.com/reachpranjal/lego-drive) | 2024.03.20 |
| **▎Generation（14 篇）** | | | | |
| Generation | — | [GEM: Generating LiDAR World Model via Deformable Mamba](https://arxiv.org/abs/2605.07326v1) | [GitHub](https://github.com/wuyang98/GEM) | 2026.05.08 |
| Generation | — | [HERMES++: Toward a Unified Driving World Model for 3D Scene Understanding and Generation](https://arxiv.org/abs/2604.28196) | [HERMESV2](https://github.com/H-EmbodVis/HERMESV2) | 2026.04.30 |
| Generation | KITTI-360 | [Leveraging 3D Representation Alignment and RGB Pretrained Priors for LiDAR Scene Generation](https://arxiv.org/abs/2601.07692) | [R3DPA](https://github.com/valeoai/R3DPA) | 2026.01.12 |
| Generation | ORAD-3D | [Advancing Off-Road Autonomous Driving: The Large-Scale ORAD-3D Dataset and Comprehensive Benchmarks](https://arxiv.org/abs/2510.16500) | [ORAD-3D](https://github.com/chaytonmin/ORAD-3D) | 2025.10.18 |
| Generation | Great-MSD | [Unreal is all you need: Multimodal ISAC Data Simulation with Only One Engine](https://arxiv.org/abs/2507.08716) | [Great-MCD](https://github.com/hkw-xg/Great-MCD) | 2025.07.11 |
| Generation | CARLA（仿真） | [Generating Traffic Scenarios via In-Context Learning to Learn Better Motion Planner](https://arxiv.org/abs/2412.18086) | [AutoSceneGen](https://github.com/Ezharjan/AutoSceneGen) | 2024.12.24 |
| Generation | — | [LeGEND: A Top-Down Approach to Scenario Generation of Autonomous Driving Systems Assisted by Large Language Models](https://arxiv.org/abs/2409.10066) | [LeGEND](https://github.com/MayDGT/LeGEND) | 2024.09.16 |
| Generation · Scenario Generation | CARLA（仿真） | [ChatScene: Knowledge-Enabled Safety-Critical Scenario Generation for Autonomous Vehicles](https://arxiv.org/abs/2405.14062) | [ChatScene](https://github.com/javyduck/ChatScene) | 2024.05.22 |
| Generation · Datasets + Generation | — | [Generalized Predictive Model for Autonomous Driving](https://arxiv.org/abs/2403.09630) | [DriveAGI](https://github.com/OpenDriveLab/DriveAGI.) | 2024.03.14 |
| Generation | — | [LLM-Assisted Light: Leveraging Large Language Model Capabilities for Human-Mimetic Traffic Signal Control in Complex Urban Environments](https://arxiv.org/abs/2403.08337) | [LLM-Assisted-Light](https://github.com/Traffic-Alpha/LLM-Assisted-Light) | 2024.03.13 |
| Generation | Waymo（Open） | [Editable Scene Simulation for Autonomous Driving via Collaborative LLM-Agents](https://arxiv.org/abs/2402.05746) | [ChatSim](https://github.com/yifanlu0227/ChatSim) | 2024.03.11 |
| Generation | nuScenes | [GenAD: Generative End-to-End Autonomous Driving](https://arxiv.org/abs/2402.11502) | [GenAD](https://github.com/wzzheng/GenAD) | 2024.02.20 |
| Generation | nuScenes、Waymo Open Dataset | [Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving](https://arxiv.org/abs/2311.17918) | [Drive-WM](https://github.com/BraveGroup/Drive-WM) | 2023.11.29 |
| Generation | nuScenes | [MagicDrive: Street View Generation with Diverse 3D Geometry Control](https://arxiv.org/abs/2310.02601) | [MagicDrive](https://github.com/cure-lab/MagicDrive) | 2023.10.13 |
| **▎VQA / QA（15 篇）** | | | | |
| VQA / QA · VQA | RoboSense Challenge | [Enhancing Vision-Language Models for Autonomous Driving through Task-Specific Prompting and Spatial Reasoning](https://arxiv.org/abs/2510.24152) | [UCAS-CSU-phase2](https://github.com/wuaodi/UCAS-CSU-phase2) | 2025.10.28 |
| VQA / QA · VQA | SafeDrive228K | [SafeDriveRAG: Towards Safe Autonomous Driving with Knowledge Graph-based Retrieval-Augmented Generation](https://arxiv.org/abs/2507.21585) | [SafeDriveRAG](https://github.com/Lumos0507/SafeDriveRAG) | 2025.07.29 |
| VQA / QA · QA | STSBench | [STSBench: A Spatio-temporal Scenario Benchmark for Multi-modal Large Language Models in Autonomous Driving](https://arxiv.org/abs/2506.06218) | [STSBench](https://github.com/LRP-IVC/STSBench) | 2025.06.06 |
| VQA / QA · VQA | Waymo Open Motion Dataset (WOMD) | [WOMD-Reasoning: A Large-Scale Dataset for Interaction Reasoning in Driving](https://arxiv.org/abs/2407.04281) | [WOMD-Reasoning](https://github.com/yhli123/WOMD-Reasoning) | 2025.05.25 |
| VQA / QA · VQA | — | [Extending Large Vision-Language Model for Diverse Interactive Tasks in Autonomous Driving](https://arxiv.org/abs/2505.08725) | [DriveMonkey](https://github.com/zc-zhao/DriveMonkey) | 2025.05.13 |
| VQA / QA · VQA | — | [Fine-Grained Evaluation of Large Vision-Language Models in Autonomous Driving](https://arxiv.org/abs/2503.21505) | [VLADBench](https://github.com/Depth2World/VLADBench) | 2025.03.27 |
| VQA / QA · VQA | — | [AutoTrust: Benchmarking Trustworthiness in Large Vision Language Models for Autonomous Driving](https://arxiv.org/abs/2412.15206) | [AutoTrust](https://github.com/taco-group/AutoTrust) | 2024.12.19 |
| VQA / QA · QA | — | [MiniDrive: More Efficient Vision-Language Models with Multi-Level 2D Features as Text Tokens for Autonomous Driving](https://arxiv.org/abs/2409.07267) | [MiniDrive](https://github.com/EMZucas/minidrive) | 2024.09.14 |
| VQA / QA · QA | DriveLM | [Multi-Frame, Lightweight & Efficient Vision-Language Models for Question Answering in Autonomous Driving](https://arxiv.org/abs/2403.19838) | [official](https://github.com/akshaygopalkr/EM-VLM4AD) | 2024.03.28 |
| VQA / QA · Datasets + VQA | — | [Holistic Autonomous Driving Understanding by Bird’s-Eye-View Injected Multi-Modal Large Models](https://arxiv.org/abs/2401.00988) | [official](https://github.com/xmed-lab/NuInstruct) | 2023.12.21 |
| VQA / QA · VQA + Evaluation/Datasets | — | [LingoQA: Video Question Answering for Autonomous Driving](https://arxiv.org/abs/2312.14115) | [official](https://github.com/wayveai/LingoQA) | 2023.12.21 |
| VQA / QA · VQA + Datasets | — | [Reason2Drive: Towards Interpretable and Chain-based Reasoning for Autonomous Driving](https://arxiv.org/abs/2312.03661) | [official](https://github.com/fudan-zvg/Reason2Drive) | 2023.12.06 |
| VQA / QA · VQA | — | [Dolphins: Multimodal Language Model for Driving](https://arxiv.org/abs/2312.00438) | [Dolphins](https://github.com/vlm-driver/Dolphins) | 2023.12.01 |
| VQA / QA · QA | UCU Dataset | [Human-Centric Autonomous Systems With LLMs for User Command Reasoning](https://arxiv.org/abs/2311.08206) | [DriveCmd](https://github.com/KTH-RPL/DriveCmd_LLM) | 2023.11.14 |
| VQA / QA · VQA | — | [VLAAD: Vision and Language Assistant for Autonomous Driving](https://ieeexplore.ieee.org/document/10495690) | [VLAAD](https://github.com/sungyeonparkk/vision-assistant-for-driving) | — |
| **▎Evaluation & Benchmark（8 篇）** | | | | |
| Evaluation & Benchmark · Evaluation | — | [D2-V2X: Depth-Driven Cooperative V2X Reasoning for Autonomous Driving](https://arxiv.org/abs/2605.24098) | [D2-V2X](https://github.com/KevinRichard1/D2-V2X) | 2026.05.22 |
| Evaluation & Benchmark · Evaluation | — | [OccSTeP: Benchmarking 4D Occupancy Spatio-Temporal Persistence](https://arxiv.org/abs/2512.15621) | [OccSTeP](https://github.com/FaterYU/OccSTeP) | 2025.12.17 |
| Evaluation & Benchmark · Evaluation | RoadSceneBench | [RoadSceneBench: A Lightweight Benchmark for Mid-Level Road Scene Understanding](https://arxiv.org/abs/2511.22466) | [RoadSceneBench](https://github.com/XiyanLiu/RoadSceneBench) | 2025.11.27 |
| Evaluation & Benchmark · Evaluation | — | [GTR-Bench: Evaluating Geo-Temporal Reasoning in Vision-Language Models](https://arxiv.org/abs/2510.07791) | [GTR-Bench](https://github.com/X-Luffy/GTR-Bench) | 2025.10.09 |
| Evaluation & Benchmark · Evaluation | — | [Evaluation of Safety Cognition Capability in Vision-Language Models for Autonomous Driving](https://arxiv.org/abs/2503.06497) | [SCD-Bench](https://github.com/EMZucas/SCD-Bench) | 2025.03.09 |
| Evaluation & Benchmark · Benchmark | — | [Are VLMs Ready for Autonomous Driving? An Empirical Study from the Reliability, Data, and Metric Perspectives](https://arxiv.org/abs/2501.04003) | [DriveBench](https://github.com/drive-bench/toolkit) | 2025.01.07 |
| Evaluation & Benchmark · Benchmark & Evaluation | — | [Probing Multimodal LLMs as World Models for Driving](https://arxiv.org/abs/2405.05956) | [DriveSim](https://github.com/sreeramsa/DriveSim) | 2024.05.09 |
| Evaluation & Benchmark · Benchmark & Scene Understanding | — | [Embodied Understanding of Driving Scenarios](https://arxiv.org/abs/2403.04593) | [ELM](https://github.com/OpenDriveLab/ELM) | 2024.03.07 |
| **合计** | | **111** | | |

## 四、统计口径与数据来源

| 项目 | 说明 |
|---|---|
| 数据来源 | github.com/thinklab-sjtu/awesome-llm4ad 仓库 README.md（5536 行 / 约 458 KB） |
| 抓取时间 | 2026-09-09；README 最新条目 Publish Date 为 2026.06.18 |
| 条目规模 | Papers 章节 522 篇 + Datasets 章节 15 条；WorkShop 2 个 Challenge 数据集（MAPLM、UCU）一并纳入 |
| Task 计数 | 按「标签拆分」：标注 "Perception, Planning" 时同时计入两类，故合计大于带标注的论文数（516 篇） |
| 数据集计数 | 合并同义写法（nuScenes/NuScenes、WOMD/Waymo Open Motion Dataset、Bench2Drive/Bench2drive、HighwayEnv/Highway-Env），并合并 Datasets 与 Env 两种字段 |
| nuScenes 衍生判定 | 仅将 README 明确说明基于 nuScenes 二次标注 / 重构建者列为衍生集，共 17 个（nuScenes-FG、NuScenes-QA、DriveLM、NuScenes-S、nuImages / nuCaption / nuView…） |
| 计数为「—」 | nuScenes-FG、NuScenes-S、nuScenes-GR-20K、nuScenes-corner、NuScenes-SpatialQA、Drive-nuScenes 仅见于 README 正文，未被 Datasets 字段标注，故无计数（非 0） |
| Code 判定 | 以 README 显式标注的 "- Code:" 为准；"Project Page"、"HuggingFace"、"Leaderboard" 不计入 |
| 仿真环境 | 部分论文用 "- Env:" 而非 "- Datasets:"（CARLA、HighwayEnv 等），在 Datasets 列以「（仿真）」后缀标注 |
| 开源总览过滤规则 | 任务大类下开源论文少于 5 篇的不予列出（本次省略：其他 4 篇、推理与解释 1 篇、场景理解 1 篇、框架与工具 1 篇） |
| 排重提示 | README 为自由文本维护，存在拼写变异（Precption、Evalution、Bench2drive），已按语义归并 |