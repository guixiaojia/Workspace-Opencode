# lab/ — 模型跑通与分析工作台（契约文件）

> **本文件是目录规范与数据契约的唯一权威源。**
> Skill A（model-forward-repro）引用本契约。修改契约只改这里。

## 1. 同名映射铁律

一个 GitHub 仓库在系统中出现 3 次，名字强制一致（= 仓库目录名，**逐字保留大小写与短横线**，不再另起简称）：

```
repos/<proj>/            原始仓库（只读）
lab/<proj>/config.yaml  项目配置（与适配代码同目录）
lab/<proj>/        项目适配代码（build_model + build_input）
lab/<proj>/outputs/        项目产物
```

## 2. 目录职责

```
lab/
├── tensor_probe.py   forward hook 采集器 → trace.json
├── arch_dumper.py    nn.Module 遍历 → model_structure.md
├── run_forward.py    入口：--project <proj>（加载模型+前向+采集）
└── <proj>/      项目特有四件套：config.yaml、build_model.py、build_input.py、outputs/
```

## 3. 产物归属

| 产物 | 生成方式 | 可再生 |
|---|---|---|
| outputs/trace.json | run_forward | ✅ |
| outputs/trace_digest.md | run_forward（trace.json 的人读聚合视图，同构事件折叠） | ✅ |
| outputs/model_structure.md | run_forward | ✅ |
| outputs/README.md、各级 README | 人工维护 | ❌ |
| outputs/walk-through.md | 人工撰写（基于以上素材） | ❌ |

## 4. trace.json 契约（采集落盘格式）

```json
{
  "meta": {
    "project": "quick-start-VLA4AD",
    "model_path": "绝对路径或模型ID",
    "torch_dtype": "bfloat16",
    "device": "cpu",
    "input_shapes": {"pixel_values": [1,3,448,448], "input_ids": [1,128]},
    "timestamp": "ISO8601",
    "git_head_repos": "a195b10",
    "note": "transformers 版本等环境信息"
  },
  "losses": {"language_ce": 10.9, "trajectory_mse": 0.02},
  "events": [
    {
      "module": "model.visual.patch_embed",       // 完整点分路径
      "depth": 2,                                  // 距根的层级，供聚合
      "input":  [{"shape": [1,3,448,448], "dtype": "bfloat16"}],
      "output": {"shape": [1,12544,1280], "dtype": "bfloat16"},
      "params": 157312                             // 该模块自身可训练参数量（无则 0）
    }
  ]
}
```

- `events` 按前向执行顺序记录；每个 `nn.LeafModule`（无子模块的模块）必现
- 只记 shape/dtype/参数量，**不记数值**（体积可控，3B 模型 full trace 预计 <2MB）

## 5. 环境与资源约定

- Python：`D:\anaconda3\envs\py311\python.exe`（一律显式使用，禁 base）
- 模型权重：ModelScope 下载，缓存 `D:\anaconda3_cache\modelscope_cache`（不设 local_dir）
- 显存：RTX 3050 4GB。降级链：GPU(bf16) → 失败 → CPU(bf16) → 内存不足 → 随机初始化仅结构
- 后台长任务（下载）日志统一写 `lab/*.log`，完成后登记进本 README 附注

## 6. 新仓库接入 checklist

1. clone → `repos/`，登记 `repos/README.md`
2. 建 `<proj>/config.yaml`（模型、入口、build_model、build_input 规格）
3. 建 `<proj>/build_model.py` + `<proj>/build_input.py` + `<proj>/outputs/`
4. `run_forward.py --project <proj>` 采集
5. 写 walk-through，更新产物 README

## 附注（运行留痕）

- 2026-09-07 Qwen/Qwen2.5-VL-3B-Instruct 经 ModelScope snapshot_download 下载完成（`dl_qwen3b.py`，日志 `ms_download.log`），缓存约 7GB
- run_forward 会置 `sys.dont_write_bytecode=True`，防止导入 repos/ 代码时污染只读目录
- 2026-09-07 用户决策：制图路线废弃（不直观），Skill B（model-analysis-diagrams）、run_analysis/mermaid_gen/dot_gen 及全部图产物已删除；分析只靠 trace.json + model_structure.md + walk-through.md
- 2026-09-07 用户决策：项目名不再缩写，`vla4ad` 目录/yaml/产物标签全部改为仓库目录名原样 `quick-start-VLA4AD`（§1 铁律相应从"小写短横线"改为"逐字一致"）；产物内的项目名标签已同步，重跑 run_forward 结果一致
- 2026-09-08 AutoVLA (NeurIPS 2025) 跑通：基于 Qwen2.5-VL-3B-Instruct，核心就是 VLM + resized token embeddings，轨迹通过 action tokens 自回归生成；前向采集 836 events，losses 为空（无标签时不计算 loss，符合仓库原生 forward 行为）
- 2026-09-08 工程结构优化：`configs/` 目录废弃，配置文件改为 `<proj>/config.yaml` 与适配代码同目录；`common/` 目录废弃，通用脚本（run_forward/tensor_probe/arch_dumper）直接放 `lab/` 根目录

