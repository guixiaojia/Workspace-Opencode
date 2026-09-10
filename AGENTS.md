# Project Instructions

## 语言原则

- 与用户的所有对话以**中文**为主，包括思考链、解释说明、注释、commit message 等
- 代码中的变量名、函数名等标识符保持英文（编程规范要求）
- 输出内容默认使用中文，除非用户明确要求英文

## 大文件下载原则

- 涉及大文件下载（模型权重、数据集等）时，**先询问用户是否亲自下载**，不要直接后台静默下载
- 提供下载链接和目标存放路径，等用户确认后再执行
- 原因：大文件下载耗时长、占用带宽，用户本地下载可能更快更可控

## README 一致性原则

- 每次对 `repos/`、`lab/`、`tools/` 及其子目录做增删改操作时，同步检查并更新对应的 `README.md`
- 上下文窗口切换或模型切换后，先扫描各目录 `README.md` 与实际内容的一致性，发现偏差主动提醒用户
- 用户的决策和判断优先级最高；遇到不一致且不确定如何处理时，优先询问用户，不要擅自决定
- Skills 文件夹（`.opencode/skills/`）中的技能文档同样适用此原则

## Python Environment

- 本项目使用 Conda 环境 `py311`（Python 3.11.14），解释器路径：`D:\anaconda3\envs\py311\python.exe`
- 运行 Python 脚本时始终使用该解释器（或 `conda run -n py311 python ...`），不要使用 base 环境
- 安装依赖时使用对应的 pip：`D:\anaconda3\envs\py311\python.exe -m pip install <pkg>`

## VSCode

- `.vscode/settings.json` 已将 `python.defaultInterpreterPath` 指向 py311，与命令行环境保持一致

## 工程结构（模型分析工作台）

- `repos/`：拉取的第三方 GitHub 仓库，**绝对只读**，登记表见 `repos/README.md`
- `lab/`：跑通与分析所有模型的统一工作台；**目录规范与数据契约的唯一权威源是 `lab/README.md`**
- `tools/`：本地工具链，新会话使用前先读 `tools/README.md` 了解可用性与坑
- 三者同名映射：分析某仓库时 `repos/<proj>` ↔ `lab/<proj>` ↔ `lab/<proj>/config.yaml`
- 标准工作流为技能 `model-forward-repro`（跑通+采集 trace.json/model_structure.md）；分析靠人工写 walk-through（制图路线已废弃）
- 硬件约束：GPU 仅 RTX 3050 4GB，>3B 模型默认 CPU 加载；ModelScope 缓存在 `D:\anaconda3_cache\modelscope_cache`
