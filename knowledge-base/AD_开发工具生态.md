# 自动驾驶生态地图与落地路线图

> 结构：总（生态位分布与优先级）→ 分（69 个数据集 / 框架 / 评测 / VLM·VLA / 世界模型条目）→ 总（环境落地 9 步计划）
> 优先级：**P0** 必装必会 / **P1** 按方向选 / **P2** 了解即可
> 本版调整：生态位分布合并为「条目数（P0 / P1 / P2）」单列；条目清单删除「与 py311 的关系」列，「安装方式」改为**安装途径 + 为什么这么装**，「关键坑」聚焦**版本兼容性与依赖冲突**。

---

## 一、总 · 生态位分布（9 类 / 69 条，P0 共 21 条）

自驾生态按「数据 → 算法 → 评测 → 大模型 → 基础设施」分成 9 个生态位；P0 是绕不开的地基，P1 按你的方向选，P2 知道有这回事即可。

| 生态位（类别） | 条目数（P0 必装必会 / P1 按方向选 / P2 了解即可） | 该生态位的定位 |
|---|---|---|
| A 数据集与数据接口 | 10（P0 3 / P1 4 / P2 3） | 数据入口：官方 devkit 与 GT 标签。决定你能跑哪个榜单，也决定环境 Python 版本（nuPlan / NAVSIM 死绑 3.9） |
| B 感知算法框架 | 7（P0 3 / P1 2 / P2 2） | 算法载体：3D 检测 / BEV / 占位的现成实现。OpenMMLab 系与 OpenPCDet 二选一，不要共存 |
| C 端到端与规划 | 8（P0 2 / P1 4 / P2 2） | 从「看见」到「怎么开」：坐标变换、地图几何、轨迹优化、MOT 指标与 E2E 基线模型 |
| D 闭环仿真与评测 | 5（P0 2 / P1 2 / P2 1） | 闭环真相：开环指标好不等于会开车。CARLA + Bench2Drive / NAVSIM 是唯二能验证行为能力的地方 |
| E VLM 与 VLA | 11（P0 3 / P1 6 / P2 2） | 语言与动作：把大模型接到驾驶决策上。含通用 VLM 微调链与机器人 VLA 框架（可迁移） |
| F 世界模型与生成式数据 | 6（P0 2 / P1 2 / P2 2） | 预测未来：生成式世界模型做数据增广与闭环训练，是当前最活跃的方向 |
| G 训练与加速基础设施 | 9（P0 3 / P1 4 / P2 2） | 算力与工程：多卡并行、实验管理、指标计算、编译工具链、部署链路 |
| H 几何地图与评测基础库 | 3（P0 0 / P1 2 / P2 1） | 坐标与几何底座：经纬度转换、点云读写、最近邻搜索，数据预处理阶段才用到 |
| I 现有环境可复用 | 10（P0 3 / P1 5 / P2 2） | 你 py311 里已经有的资产：哪些能直接迁移到自驾项目，哪些在新环境下要重装 |
| **合计** | **69（P0 21 / P1 31 / P2 17）** | |

---

## 二、分 · 生态条目清单（69 条）

每个条目回答三件事：它做什么、该怎么装（以及为什么这么装）、版本与依赖上要注意什么。

### A 数据集与数据接口（10 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [A] nuscenes-devkit | nuScenes 官方工具包：加载多传感器数据、渲染标注、算 NDS/mAP/AMOTA 等官方指标，自动驾驶复现的地基 | **pip 安装（PyPI 纯 Python 包）**<br>为什么：官方已发布到 PyPI，纯 Python、无 CUDA 算子，无需编译也无需匹配 torch/CUDA，直接装即可 | 会顺带拉入 pyquaternion + shapely，并把 shapely 钉在 1.8 系，与要求 shapely 2.0 的 nuPlan / NAVSIM **直接冲突**，不要装进同一环境。许可证虽标 Apache-2.0，官方注明非商业用途，商用需另谈 |
| P0 | [A] nuplan-devkit | nuPlan 官方规划基准：1500+ 小时数据、开环/闭环规划评测、nuBoard 可视化，端到端规划论文的默认赛场 | **git clone → pip install -e .（源码可编辑安装）**<br>为什么：官方未上 PyPI（PyPI 上同名包是第三方非官方打包），且需配套地图文件与配置，只能源码装；可编辑模式便于改评测脚本 | 官方死绑 **Python 3.9**，与 py311 不兼容，必须单开环境；依赖 shapely 2.0（见上条冲突） |
| P0 | [A] navsim (navsim-devkit) | NAVSIM：目前最主流的闭环规划基准之一，基于 OpenScene + nuPlan 地图，用 PDM Score（NC/DAC/TTC/EP/C）打分，含 navtrain/navtest 划分与 HF 排行榜 | **git clone → conda env create -f environment.yml → pip install -e .（官方锁定环境 + 源码安装）**<br>为什么：官方提供锁定全部依赖的 environment.yml，用 conda 复现最稳，避免手工逐个对齐版本 | environment.yml 指定 **Python 3.9**，与 py311 不兼容；依赖 nuPlan 地图 + shapely 2.0；还需配 NUPLAN_MAPS_ROOT 等 5 个环境变量（配置依赖，pip 无法解决） |
| P1 | [A] waymo-open-dataset-tf-2-11-0 | Waymo Open Dataset（Perception / Motion / E2E Driving）官方读写与评测库，含 WOSAC 仿真智能体指标 | **pip 安装（PyPI 预编译包，按 TF 版本分发布包）**<br>为什么：官方按 TensorFlow 版本分别发包，pip 会自动解析匹配的 TF，无需源码编译 | **强绑 TensorFlow 2.11 + numpy 1.24**，会污染纯 torch 环境（TF 与 torch 对 numpy/protobuf 要求冲突），必须单独 env；不要预先手装 TF，让 pip 自行解析 |
| P1 | [A] av2 (Argoverse 2) | Argoverse 2 官方 API：运动预测、3D 检测、地图与坐标转换，Motion Forecasting 方向常用 | **pip 安装（PyPI 预编译 whl）**<br>为什么：官方维护并发布 whl，含少量编译组件但不必本地编译 | 依赖较新，**Python 3.10+ 体验最好**（py3.9 下依赖解析易失败）；与老版 mmdet3d 共存需实测 |
| P1 | [A] OpenOcc / nuScenes-Occupancy | CVPR24 AGC 占用与流挑战的官方 GT：17 类、200×200×16 体素，评测用 RayIoU + mAVE 合成 OccScore | **数据下载（OpenDataLab / Google Drive 压缩包，非 Python 包）**<br>为什么：本质是标注 GT 数据，没有可 pip 安装的库，解压后按评测脚本约定的目录放置即可 | 无 Python 依赖冲突；但**版本必须认准 v2.1**（v2.0 有 bug 已废弃）。nuScenes 本体 z 轴缺平移量，多帧点云累积会分层，属数据侧陷阱 |
| P1 | [A] Occ3D-nuScenes / Occ3D-Waymo | 清华 Mars Lab 的占用预测基准，提供稠密可见性感知标注生成流程与 CTF-Occ 基线 | **官网下载 + 按仓库说明放置（数据 / 标注 GT，非 pip）**<br>为什么：提供的是标注与生成流程，不是可分发的库 | 无安装冲突；但**与 OpenOcc 标签体系不同，不可混用**，复现前先确认论文用的是哪一套 GT，否则指标不可比 |
| P2 | [A] OpenLane-V2 / OpenLane | 车道线与车道拓扑（centerline + traffic element）基准，在线地图构建方向的事实标准 | **官网下载 + 自写 dataloader（无官方包）**<br>为什么：官方未提供 Python 包，社区各自实现 loader，因此也没有标准安装流程 | 没有官方包意味着没有版本约束、但也无法靠包管理解决兼容；各家 loader 对 numpy / shapely 版本假设不一，接入现有环境易冲突 |
| P2 | [A] DAIR-V2X / V2X-Seq | 国内车路协同数据集（路侧 + 车端），做 V2X 融合时才会用到 | **官网申请下载（数据，非包）**<br>为什么：需签署协议申请，不走任何包管理渠道 | 无 Python 依赖冲突；主要成本在申请流程（非版本问题） |
| P2 | [A] LightwheelOcc | 合成 3D 占用数据集，带稠密占用与深度标注，传感器配置模拟 nuScenes | **HuggingFace 下载（合成数据集，非包）**<br>为什么：是数据而非代码，HF 是唯一分发渠道 | 无 Python 依赖；传感器配置对齐 nuScenes，可直接接入现有 nuScenes 数据管线，无版本冲突 |

### B 感知算法框架（7 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [B] mmcv (完整版) | OpenMMLab 底层基础库。你现在的 mmcv-lite 2.1.0 是精简版，不含 CUDA 算子，跑不了 3D 检测/可变形卷积 | **mim install mmcv 或 pip 指定 OpenMMLab 预编译 whl 索引**<br>为什么：完整版含 CUDA 算子，必须选用与本机 CUDA + torch 对应的预编译 whl；源码编译要数十分钟且极易失败 | 完整版与 mmcv-lite **互斥**，必须先卸 lite 再装；版本与 torch / CUDA 严格绑定（cu126 + torch 2.11 目前无官方验证组合，建议降到 torch 2.4~2.6） |
| P0 | [B] mmdetection3d (mmdet3d) | 3D 目标检测主框架：KITTI / nuScenes / Waymo / Lyft / SemanticKITTI / ScanNet，含 PointPillars、CenterPoint、BEVFusion、TPVFormer 等，BEV 感知和占用任务的脚手架 | **mim install mmdet3d（OpenMMLab 索引）**<br>为什么：用 mim 而非裸 pip，可自动解析 mmcv / mmdet / torch 的互相匹配版本 | **版本必须与 mmcv、mmdet、torch 四者严格对齐**；torch 2.11 太新官方未验证，建议 2.4~2.6；与 py311 组合风险高，建议 py3.9 环境 |
| P0 | [B] mmdetection (mmdet) | 2D 检测与实例分割，mmdet3d 的硬依赖，也是 BEV 检测头（如 FCOS3D、PGD）的基础 | **mim install mmdet**<br>为什么：作为 mmdet3d 的依赖，由 mim 统一解析版本，避免手工指定错配 | 与 mmdet3d 版本一一对应，**不能单独升级** |
| P1 | [B] OpenPCDet | 激光雷达 3D 检测另一大主力代码库（PointPillars / SECOND / Part-A2 / CenterPoint / DSVT），比 mmdet3d 更轻、改起来更自由 | **git clone → pip install -e .（源码安装 + 本地编译 CUDA 算子）**<br>为什么：算子需现场编译，官方不提供通用 whl，只能源码装 | 编译依赖 nvcc 且与 torch 版本匹配；**与 mmdet3d 二选一**，不要装进同一环境（两者对 mmcv / numpy 要求不同） |
| P1 | [B] spconv (+ cumm) | 稀疏卷积库，CenterPoint、SECOND 等体素类检测器的性能核心 | **pip install spconv-cu120（PyPI 上按 CUDA 版本分发的预编译 whl）**<br>为什么：包名自带 cu 版本号，选与本机 CUDA 一致的即可免编译 | 版本与 CUDA 绑定（cu113 / cu117 / cu120…）；**升级前必须先卸载旧 spconv 和 cumm**，否则报 undefined symbol；需与 mmdet3d 的 CUDA / torch 版本一致 |
| P2 | [B] torchsparse / MinkowskiEngine | 稀疏卷积的另外两个选择，TorchSparse 偏稀疏点云分割，Minkowski 偏 4D 时空卷积 | **pip 预编译 whl 或源码编译（取决于是否有匹配 whl）**<br>为什么：二者对 torch/CUDA 组合覆盖不全，有匹配 whl 就 pip，没有才编译 | 与 spconv 功能重叠且**各自绑定不同 torch / CUDA 版本，共存易冲突**；除非论文明确要求否则不装 |
| P2 | [B] BEVDepth / BEVDet / LSS 系列 | 基于深度估计的 BEV 感知，需要编译自定义 CUDA 算子（bev_pool / deformable） | **项目级源码 + 自定义 CUDA 算子编译（无统一包）**<br>为什么：每个项目自带一套算子，无通用分发包 | 算子与特定 torch / CUDA 版本绑定，**环境不通用**，建议一个项目一个环境 |

### C 端到端与规划（8 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [C] pyquaternion | 四元数运算，nuScenes / nuPlan 位姿与坐标系转换的必备小库 | **pip install pyquaternion（纯 Python）**<br>为什么：纯 Python 实现、零编译，随 nuscenes-devkit 一起装即可 | 无版本冲突，极轻量 |
| P0 | [C] shapely | 2D 几何运算（多边形、缓冲区、相交），HD 地图与可行驶区域判定全靠它 | **pip install shapely（PyPI 预编译 whl，内含 GEOS 二进制）**<br>为什么：whl 已打包 GEOS C 库，不需要系统级依赖或编译 | ⚠ **自驾环境第一爆点**：nuScenes 老代码要 shapely 1.8，nuPlan / NAVSIM 要 2.0，两者互斥，必须分环境 |
| P1 | [C] casadi | 非线性优化求解器，UniAD、轨迹优化与 MPC 类规划器的依赖 | **pip install casadi（PyPI 预编译 whl，含 C++ 核心）**<br>为什么：官方提供各平台 whl，免去源码编译 NL 求解器 | ABI 依赖 C++ 运行库（libstdc++ / glibc），**Windows 上偶发 DLL 加载失败**，建议 Linux；与 Python 版本耦合较低 |
| P1 | [C] motmetrics | 多目标跟踪（MOT）官方指标库，UniAD/VAD 等端到端跟踪评测依赖它 | **pip install motmetrics==1.1.3（锁版本安装）**<br>为什么：需显式锁定版本，直接装最新版会拿到不兼容的新 API | **必须锁 1.1.3**，新版 API 变更，老项目（UniAD / VAD）直接报错 |
| P1 | [C] UniAD / UniAD 2.0 | 端到端自动驾驶里程碑工作（感知→预测→规划全栈），几乎所有 E2E 论文的对比基线 | **项目源码 + 权重（HF: OpenDriveLab，按项目 requirements 装）**<br>为什么：研究型项目非库，需按 commit 对应的 requirements 复现环境 | 老版要 py3.8 + torch 1.9 + mmcv-full 1.4 + mmdet3d 0.17.1；2.0 要 py3.9 + torch 2.0.1 + mmcv-full 1.6.1 + mmdet3d 1.0.0rc6 —— **与 py311 全不兼容，必须单开环境** |
| P1 | [C] VAD / SparseDrive / DiffusionDrive | 端到端规划的新一代代表（矢量化的 VAD、稀疏化 SparseDrive、扩散规划 DiffusionDrive） | **项目源码（按各自 requirements 安装）**<br>为什么：均为研究项目，无官方 pip 包 | 多数基于 mmdet3d + torch 2.x，比 UniAD 友好；仍受 mmdet3d 版本对齐约束（torch 2.4~2.6 较稳） |
| P2 | [C] lanelet2 | 高精地图标准格式与 C++/Python 库，nuPlan 地图与部分 E2E 项目依赖 | **apt / conda 装 C++ 库 + Python 绑定**<br>为什么：主体是 C++ 库，Python 只是绑定层，pip 装不了核心 | 编译重、Python 绑定**安装失败率高**；与 Boost / Python 版本耦合，建议优先 conda 装 |
| P2 | [C] Transfuser / TCP / Think2Drive | CARLA 闭环端到端的经典基线，Bench2Drive 里已内置 | **随 Bench2Drive 仓库附带（不单独安装）**<br>为什么：与仿真环境强绑定，单独装会导致版本漂移 | 跟随 Bench2Drive 环境（py3.7 / 3.8），不单独装 |

### D 闭环仿真与评测（5 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [D] CARLA 0.9.15 | 开源自动驾驶仿真器，闭环评测的事实基础设施 | **官网下载二进制发行包（CARLA_0.9.15.tar.gz + AdditionalMaps）**<br>为什么：仿真器内含 UE4 引擎与资产，是完整二进制发行版，不走 Python 包管理 | **Bench2Drive 绑死 0.9.15，不能升**；Python API egg 版本必须与服务端一致；渲染走 Vulkan（用 -graphicsadapter 指定显卡，与 CUDA_VISIBLE_DEVICES 无关） |
| P0 | [D] Bench2Drive | 220 条路线的闭环多能力评测基准，输出 Driving Score / 成功率 / 12 项能力（并线、超车、让行…），端到端必跑 | **git clone + 写 carla.pth（源码 + 手动指向 CARLA 的 egg）**<br>为什么：需把 CARLA 的 Python egg 路径写进 site-packages，属非标准 pip 流程 | 要求 **Python 3.7 / 3.8**，与 py311 完全不兼容，必须独立环境；依赖 CARLA 0.9.15 的 Python API 版本 |
| P1 | [D] carla-leaderboard / scenario_runner | CARLA 官方榜评测框架与场景定义器，Bench2Drive 的底座 | **随 Bench2Drive / 官网源码附带**<br>为什么：与 CARLA 版本强耦合，跟随主环境获取最稳 | 版本必须与 CARLA 严格对应（0.9.15），**混版本直接报错** |
| P1 | [D] HUGSIM | 闭环仿真基准，NAVSIM 的 private_test_e2e 划分即用于 HUGSIM 评测 | **随 navsim 仓库附带**<br>为什么：复用 navsim 已锁定的环境，单独装会重复解决依赖 | 依赖 navsim devkit，需 NAVSIM_DEVKIT_ROOT 指向正确；共用 navsim 的 py3.9 环境 |
| P2 | [D] HuggingFace 榜单提交工具 | NAVSIM / Bench2Drive 都走 HF 榜单提交，需 submission.pkl 生成与合并脚本 | **随仓库脚本使用（非独立包）**<br>为什么：就是几个提交脚本，无独立分发需求 | 继承 navsim / Bench2Drive 环境，无独立版本问题；提交格式随榜单版本变化 |

### E VLM 与 VLA（11 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [E] ms-swift / peft / trl（已有） | 你环境里已装的大模型微调三件套，做自动驾驶 VLM（Qwen-VL / InternVL）微调直接可用 | **已装（ms_swift 3.10.3 / peft 0.17.1 / trl 0.24.0）**<br>为什么：py311 的既有资产，无需操作 | 三者与 transformers / torch 版本联动，升级 torch 时需同步验证；**不要与 mmdet3d 装进同一环境**（依赖栈完全不同） |
| P0 | [E] qwen-vl-utils | Qwen2-VL / Qwen2.5-VL 官方多模态数据处理工具（图像分辨率动态压缩、视频抽帧） | **pip install qwen-vl-utils（纯 Python 包）**<br>为什么：纯 Python 工具库，零编译 | 依赖 transformers，与 Qwen2-VL / Qwen2.5-VL 版本配套即可，无编译依赖 |
| P0 | [E] flash-attn | 注意力算子加速，训练 VLM/VLA 时显存与速度的差距是数量级的 | **pip install flash-attn --no-build-isolation（源码编译安装）**<br>为什么：官方不提供通用 whl，需现场编译 CUDA 算子；--no-build-isolation 让它复用已装的 torch，而不是重新拉一份 | **与 torch / CUDA 强绑定**；CUDA 12.4+ 建议装 2.7.4 而非项目 pin 的 2.5.5（2.5.5 在新 CUDA 上编不过）；编译需 nvcc 在 PATH，耗时 10–30 分钟。你环境目前没有任何注意力加速库，这是明显缺口 |
| P1 | [E] VLMEvalKit / lmms-eval | 多模态大模型评测套件，跑通用 VLM 榜单的标准做法 | **pip install vlmeval 或 git clone lmms-eval**<br>为什么：套件型工具，体积大、依赖多，按需装 | 依赖较多（transformers、torchvision 及部分 API 依赖），**包体大易污染主环境**；只做自驾自研评测可不装 |
| P1 | [E] DriveLM / Dolphins | 自动驾驶专用 VLM：DriveLM 用图结构做感知-预测-规划推理，Dolphins 是 7B 驾驶多模态模型 | **项目源码 + HF 权重（非 pip）**<br>为什么：研究项目 + 权重，未提供库包 | 依赖各自 pin 的 transformers / torch 版本，与 py311 新版本组合需实测；建议作为对比基线跑，不与生产环境混装 |
| P1 | [E] DriveBench | ICCV25 的自动驾驶 VLM 可靠性基准：19200 帧 / 20498 问答 / 17 种输入退化设置，用 VGC / RRS / CMC 揭穿"伪视觉落地" | **HF: drive-bench/arena 下载 + 官方仓库脚本（数据 / 评测，非 pip 包）**<br>为什么：本质是评测集与打分脚本 | 无安装冲突；评测需调 GPT 打分（**外部 API 依赖**，需准备预算） |
| P1 | [E] lerobot | HuggingFace 的机器人/VLA 统一框架，含 SmolVLA、X-VLA、Diffusion Policy、π 系列策略与数据集格式 | **pip install lerobot 或按 extras 装（lerobot[all] / [pi] / [smolvla] / [diffusion] / [feetech]）**<br>为什么：基础包很轻，重依赖走 extras 按需引入，避免一次性拉全量依赖 | extras 会引入 ffmpeg、特定 torch 版本等；**Windows 支持有限，建议 Linux**；建议与自驾环境分开，避免 torch 版本被改 |
| P1 | [E] openpi (π0 / π0.5 / π0-FAST) | Physical Intelligence 的 VLA 开源实现，flow-matching 动作头，是目前 VLA 微调的事实参考实现 | **git clone --recurse-submodules → uv sync → uv pip install -e .**<br>为什么：含子模块且官方用 uv 锁定依赖，必须递归克隆；拉 LeRobot 子模块需 GIT_LFS_SKIP_SMUDGE=1 | **用 uv 管理（与 pip 环境隔离）**；官方只测过 Ubuntu 22.04；2025-09 起支持 PyTorch 后端（此前依赖 JAX） |
| P1 | [E] openvla | 开源 7B VLA 模型与训练代码，含 LoRA 微调、OFT 加速配方、FAST 动作分词器 | **git clone → pip install -e .（源码安装）**<br>为什么：必须从仓库装，PyPI 上的同名包不对应 | ⚠ PyPI 上有**同名无关的 prismatic（JSON 库）**，装错会静默失败；flash-attn 2.5.5 在 CUDA 12.4+ 编不过，需改用 2.7.4 |
| P2 | [E] RLDS / tensorflow-datasets | Open X-Embodiment 机器人数据格式（RLDS），OpenVLA 训练数据标准 | **pip install tensorflow-datasets**<br>为什么：官方标准 pip 包 | **会引入整个 TensorFlow 生态，与纯 torch 环境冲突风险高**（同 Waymo 包），建议单独环境 |
| P2 | [E] SmolVLA / X-VLA | 轻量 VLA：SmolVLA 4.5 亿参数可在消费级 GPU 跑；X-VLA 用软提示做跨本体泛化 | **pip install 'lerobot[smolvla]' / 'lerobot[xvla]'（随 lerobot extras 装）**<br>为什么：作为 lerobot 的可选组件分发，无需单独仓库 | 继承 lerobot 的 torch / ffmpeg 依赖，无额外冲突；轻量，适合作为 VLA 入门 |

### F 世界模型与生成式数据（6 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [F] diffusers | 扩散模型库，几乎所有驾驶视频世界模型（DriveDreamer、Cosmos 同类）的底层 | **pip install diffusers（纯 Python 包）**<br>为什么：官方持续发布到 PyPI，纯 Python 无编译 | 与 transformers、accelerate **版本联动**，升级 torch / transformers 时需同步；装完跑一次自带自检 |
| P0 | [F] NVIDIA Cosmos (Predict / Transfer / Reason) | 英伟达世界基础模型平台：Predict 生成未来世界状态，Transfer 按 HD 地图+LiDAR 深度+文本生成多视角驾驶视频，Reason 做时空推理与拒绝采样 | **HuggingFace / NGC 下载开源权重 + Cosmos Cookbook 流程（模型级，非 pip）**<br>为什么：交付物是权重与流程，不是可 pip 安装的库 | 依赖较新 torch / CUDA 与大量显存；与 diffusers / transformers 版本联动；**权重版本需与代码 commit 对应** |
| P1 | [F] DriveDreamer / DriveDreamer4D | 第一个完全从真实驾驶场景构建的世界模型，可做可控驾驶视频生成、4D 重建、复杂机动渲染 | **GigaAI-research 仓库源码（老项目）**<br>为什么：无包分发，只能按仓库装 | 依赖较旧（旧版 diffusers / torch），**与 py311 新版本冲突**；建议读思路 + 用它的可视化，不建议直接搭环境 |
| P1 | [F] World4Drive | ICCV25：意图感知的潜世界模型，无需感知标注做端到端规划，nuScenes 开环 + NAVSIM 闭环双榜，L2 降 18.1%、碰撞率降 46.7%、收敛快 3.75 倍 | **项目源码（github.com/ucaszyp/World4Drive）**<br>为什么：研究项目，按 requirements 装 | 同时依赖 nuScenes 与 NAVSIM 两套评测，**即同时受 navsim 的 py3.9 约束与 nuScenes 侧依赖约束**，建议在 planning 环境中搭建 |
| P2 | [F] OccWorld / Drive-OccWorld | 基于占用表示的驾驶世界模型，直接在 3D 占用上预测未来演化 | **项目源码**<br>为什么：研究项目，无统一分发 | 依赖 OpenOcc / Occ3D 标签（数据前置依赖）；绑定特定 mmdet3d / torch 版本 |
| P2 | [F] gsplat / diff-gaussian-rasterization | 3D 高斯泼溅，驾驶场景重建与新视角合成，世界模型的数据侧常用 | **pip 预编译 whl 或源码编译（取决于 CUDA/torch 是否有匹配 whl）**<br>为什么：有匹配 whl 时优先 pip，没有才本地编译 | **编译型依赖，需 CUDA 工具链与 torch 版本匹配**；与 PyTorch3D 等共存易冲突 |

### G 训练与加速基础设施（9 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [G] deepspeed | 大模型/多卡训练的显存优化与并行框架，VLM/VLA 全参数微调绕不开 | **pip install deepspeed（多数情况有预编译 whl，缺则现场编译 ops）**<br>为什么：优先用匹配环境的 whl，避免耗时编译 | **版本约束常见（部分项目要求 <0.17）**，与 torch / CUDA 耦合；Windows 支持差，建议 Linux；升级 torch 后常需重装以匹配 |
| P0 | [G] wandb | 实验管理与指标看板。你现在只有 tensorboard，多人协作和超参对比会很难受 | **pip install wandb（纯 Python）**<br>为什么：纯 Python 客户端，零编译 | 无版本冲突；网络受限时用 WANDB_MODE=offline（可关闭外部依赖） |
| P0 | [G] torchmetrics | 指标计算标准库（mAP、IoU、F1…），替代你已经过时的 rouge + thop | **pip install torchmetrics（纯 Python）**<br>为什么：官方持续发布，纯 Python | 与 torch 主版本联动（需匹配 torch 大版本）；可替代 rouge / thop |
| P1 | [G] ninja / packaging | 编译 CUDA 算子的前置工具（几乎所有 3D 检测项目第一步就是装它俩） | **pip install ninja packaging（预编译 / 纯 Python）**<br>为什么：构建期工具，直接 pip 最快 | 无冲突；但**缺了会在编译 CUDA 算子时报 gcc 失败**，属隐性前置依赖 |
| P1 | [G] liger-kernel | 大模型训练 kernel 融合，省显存提速，ms-swift 已支持 | **pip install liger-kernel（含 triton kernel，Python 分发）**<br>为什么：kernel 以 triton 形式分发，无需 CUDA 编译 | 依赖 triton 与 torch 版本匹配；你已装 ms_swift，可直接开启 |
| P1 | [G] nvitop / py-spy | GPU 监控与 Python 性能剖析，排查训练卡顿/显存泄漏 | **pip install nvitop py-spy（预编译 whl）**<br>为什么：独立 CLI 工具，pip 装完即用 | 独立工具，**不侵入项目依赖树**，无冲突 |
| P1 | [G] onnx / tensorrt / polygraphy | 车端部署链路，模型训完要上板时的必备 | **onnx 走 pip；TensorRT 走 NVIDIA 官网安装包（系统级）**<br>为什么：TRT 与驱动强绑定，不能用 pip 装，必须走官方安装包 | **TensorRT 版本与 GPU 驱动、CUDA 强绑定**；现有 onnxruntime 是非 gpu 版，装 gpu 版前需先卸（同名包冲突） |
| P2 | [G] xformers | Meta 的注意力/算子加速库，flash-attn 的补充 | **pip install xformers（需匹配 torch 版本的预编译 whl）**<br>为什么：官方按 torch + CUDA 组合分发，常需指定索引 | **与 torch 版本强绑定**；装了 flash-attn 一般不必再装，共存可能冲突 |
| P2 | [G] apex | NVIDIA 混合精度老库，UniAD/老 CenterPoint 依赖 | **源码编译（无官方 whl）**<br>为什么：官方已停止发 whl，只能从源码编 | 与 torch / CUDA 版本强耦合，**新版 torch 常编不过**；只在复现 2022 年前老项目时需要 |

### H 几何地图与评测基础库（3 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P1 | [H] utm / pyproj | 经纬度与 UTM 坐标转换，nuPlan / Argoverse 数据预处理必用 | **pip install utm pyproj（pyproj 提供预编译 whl，内含 PROJ 二进制）**<br>为什么：whl 已打包 PROJ，不需要系统级地理库 | pyproj 与 numpy 版本联动弱，基本无冲突 |
| P1 | [H] ckdtree / scipy.spatial（已有 scipy） | 最近邻搜索，点云配准、轨迹匹配、Occ 评测都在用 | **已装（scipy 1.17.1）**<br>为什么：随 scipy 提供，无需额外安装 | scipy 与 numpy 版本联动，升级 numpy 时需同步；无其他冲突 |
| P2 | [H] pyntcloud / laspy | 点云与激光雷达文件（.las/.laz）读写，做自建数据集采集时用到 | **pip install pyntcloud laspy（纯 Python + 少量编译）**<br>为什么：标准 pip 包，按需装 | pyntcloud 对 pandas / numpy 版本有隐含假设，**可能与 py311 的 pandas 2.x 冲突**；只在自建数据时装 |

### I 现有环境可复用（10 条）

| 优先级 | 名称 | 它做什么 | 安装方式与选用理由 | 版本兼容与依赖要点 |
|---|---|---|---|---|
| P0 | [I] torch 2.11.0+cu126 / torchvision | 深度学习底座。CUDA 12.6 编译，对 VLM/VLA/世界模型友好，但对 2023 年前的感知项目过于超前 | **已装**<br>为什么：py311 的既有底座，不要动 | ⚠ torch 2.11 + cu126 对 2023 年前的感知项目过于超前（mmdet3d / UniAD / mmcv 均无对应预编译组合），**做感知 / E2E 必须另开环境降到 torch 2.0~2.4** |
| P0 | [I] mmsegmentation + mmengine + openmim + model-index | BEV 语义分割、占用（occupancy）任务的现成脚手架，也是 mmdet3d 的兄弟组件 | **已装**<br>为什么：OpenMMLab 组件已就位，补齐缺失件即可升级到 mmdet3d | 缺完整 mmcv 与 mmdet；补齐时**三者版本必须与 torch 对齐**（mmseg / mmengine / mmdet3d 属同一版本矩阵） |
| P0 | [I] kornia 0.8.2 / kornia_rs | 可微分相机几何与图像变换，BEV 投影、图像增广、畸变校正都靠它，自动驾驶里非常实用 | **已装**<br>为什么：纯 Python + Rust 扩展，已分发 whl | 与 torch 版本联动，**降级 torch 时需同步降 kornia** |
| P1 | [I] open3d 0.19.0 | 点云可视化与处理，debug 激光雷达数据的第一选择 | **已装**<br>为什么：官方 whl 已覆盖主流平台 | open3d 对 numpy 版本敏感，**在 py3.9 老环境重装时可能需降 open3d 版本** |
| P1 | [I] einops 0.8.2 | 张量维度重排，BEV/占用这种 5 维张量（B, C, D, H, W）操作的救命稻草 | **已装**<br>为什么：纯 Python，零依赖 | 纯 Python 无冲突，跨环境通用 |
| P1 | [I] timm 1.0.28 | 视觉骨干网络库（ResNet、Swin、ConvNeXt），自驾模型 backbone 的默认来源 | **已装**<br>为什么：纯 Python，pip 分发 | **timm 与 torch / torchvision 联动较强**（新 timm 常要求新 torch）；老环境需降 timm |
| P1 | [I] opencv-python / pillow / numpy / pandas | 图像 IO、标定、数据清洗的基础 | **已装**<br>为什么：基础库，pip 分发 | 服务器上建议把 opencv-python 换成 headless 版（避免 libGL 依赖缺失）；**numpy 2.x 与老 mmcv / spconv 不兼容**，老环境需 numpy<2 |
| P1 | [I] accelerate 1.13.0 / peft / trl / ms_swift | VLM 微调与分布式训练链，做自动驾驶大模型的核心资产 | **已装**<br>为什么：py311 核心资产，无需操作 | 与 torch / transformers 版本联动；**不要与 3D 感知栈共存**（numpy / torch 要求冲突），建议把 py311 定位成"大模型环境" |
| P2 | [I] langchain + chromadb + openai | 做驾驶场景检索、日志问答、长尾场景语义搜索（RAG）时可用 | **已装**<br>为什么：能力型依赖，按需保留 | langchain 生态更新快、版本碎片化，**与 pydantic v1/v2 冲突常见**；与主线弱相关，不建议升级 |
| P2 | [I] onnxruntime / safetensors / bitsandbytes | 模型导出、权重存储与量化推理 | **已装**<br>为什么：部署与量化链，上板前启用 | 现有 onnxruntime 非 gpu 版，换 gpu 版需先卸；**bitsandbytes 与 torch / CUDA 版本绑定较紧** |

---

## 三、总 · 环境落地 9 步计划

回到全局：一个技术栈一个环境，绝不共存。py311（py3.11 / torch 2.11）只服务大模型方向，感知与 E2E 另起旧版本环境。

| 阶段 | 目标 | 具体动作 + 关键命令 | 风险与提示 |
|---|---|---|---|
| 第 0 步 | 定位 py311，别再往里塞 | 把现有 py311 明确定义为「大模型 / VLM / VLA / 世界模型」环境，所有 3D 感知与 E2E 依赖一律不装进来<br><br>▸ `pip freeze > requirements_py311_vlm.txt` | py311 的 torch 2.11 + py3.11 与 mmdet3d / UniAD / nuplan 全线不兼容，硬塞必炸 |
| 第 1 步 | 补 py311 的四个缺口 | flash-attn、deepspeed、wandb、torchmetrics + diffusers<br><br>▸ `pip install flash-attn --no-build-isolation && pip install deepspeed wandb torchmetrics diffusers qwen-vl-utils` | flash-attn 编译前确认 nvcc 在 PATH；CUDA 12.4 以上装 2.7.4 而非 2.5.5 |
| 第 2 步 | 新建 adv-perception 环境 | python 3.9 + torch 2.0.1(cu118) + mmcv-full 1.6.1 + mmdet 2.26 + mmseg 0.29.1 + mmdet3d 1.0.0rc6 + nuscenes-devkit + spconv<br><br>▸ `conda create -n adv-perception python=3.9 -y && mim install mmcv-full==1.6.1 && mim install mmdet3d` | 这套是 UniAD 2.0 / BEVFormer / BEVFusion 的黄金组合，能复现绝大多数 2023-2024 的感知与 E2E 论文 |
| 第 3 步 | 新建 adv-planning 环境 | python 3.9 + nuplan-devkit + navsim，专做开环/闭环规划评测<br><br>▸ `git clone nuplan-devkit / navsim，各自 conda env create -f environment.yml` | nuplan 与 nuScenes 对 shapely 版本要求冲突，必须隔离；先下 mini 集（nuplan mini / navsim mini）验证跑通再下全量 |
| 第 4 步 | 新建 adv-sim 环境 | python 3.8 + CARLA 0.9.15 + Bench2Drive，专做闭环仿真<br><br>▸ 下载 CARLA_0.9.15 + AdditionalMaps，写 carla.pth，跑 `run_evaluation_debug.sh` | CARLA 进程难杀，常跑 clean_carla.sh；先用 Dev10 子集再上 220 条 |
| 第 5 步 | VLA 环境用 uv 管理 | openpi / lerobot 用 uv 而非 pip，避免子模块与 LFS 问题<br><br>▸ `GIT_LFS_SKIP_SMUDGE=1 uv sync && GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .` | openpi 只测过 Ubuntu 22.04，Windows 需走 Docker |
| 第 6 步 | 数据分层存放 | 把 nuScenes / nuPlan / OpenScene / OpenOcc 分开目录，用环境变量指向，绝不放进代码仓库<br><br>▸ `export NUSCENES_ROOT / NUPLAN_MAPS_ROOT / NAVSIM_EXP_ROOT / OPENSCENE_DATA_ROOT` | 全量数据 TB 级，后期换盘/迁移时环境变量方案能救命 |
| 第 7 步 | 建立复现台账 | 每复现一个项目就记：commit hash、环境版本、数据集版本、复现指标 vs 论文指标<br><br>▸ 用 Notion/飞书或仓库根目录 `REPRODUCE.md` | 自动驾驶复现最大的隐性成本是「三个月后忘了当初怎么跑通的」 |
| 第 8 步 | 按方向收缩 | VLM/VLA 与 3D 感知二选一作为主线深耕，另一条保持只读跟进<br><br>▸ 每季度复盘一次 | 生态盘根错节的根源是同时追两条技术栈，摊薄算力也摊薄注意力 |
