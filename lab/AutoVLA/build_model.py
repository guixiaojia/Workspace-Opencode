"""AutoVLA 兼容垫片：从 .ckpt 提取模型权重，加载到 Qwen2.5-VL-3B-Instruct。

AutoVLA 的核心就是 Qwen2_5_VLForConditionalGeneration + resized token embeddings，
没有额外的 trajectory head（轨迹通过 action tokens 自回归生成）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn as nn
from transformers import AutoConfig, AutoProcessor, Qwen2_5_VLForConditionalGeneration

REPO_DIR = Path(__file__).resolve().parents[2] / "repos" / "AutoVLA"
sys.path.insert(0, str(REPO_DIR))


class AutoVLABridged(Qwen2_5_VLForConditionalGeneration):
    """继承 Qwen2.5-VL，保持原始 forward 不变，仅用于身份标识。"""

    def __init__(self, config):
        super().__init__(config)
        self._last_losses: dict = {}

    def forward(self, *args, **kwargs):
        # 去掉 AutoVLA 训练时特有的字段
        kwargs.pop("gt_trajectory", None)
        kwargs.pop("gt_action", None)
        kwargs.pop("has_cot", None)
        return super().forward(*args, **kwargs)


def build_model(model_dir: Path, dtype=torch.bfloat16) -> AutoVLABridged:
    """构建 AutoVLA 模型。

    Args:
        model_dir: Qwen2.5-VL-3B-Instruct 权重目录（不是 .ckpt 路径）
        dtype: 模型精度
    """
    config = AutoConfig.from_pretrained(model_dir)

    model = AutoVLABridged.from_pretrained(
        model_dir,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    )

    return model


def last_losses(model) -> dict:
    """返回最近一次 forward 的损失字典（供 run_forward 采集）。"""
    return dict(getattr(model, "_last_losses", {}))
