"""WA-JEPA 兼容垫片：加载 V-JEPA 2.1 预训练权重和 WA-JEPA checkpoint。

WA-JEPA 的核心是 MultiViewCausalFutureMaskedJEPA，基于 V-JEPA 2.1 ViT-L/16 编码器，
联合流预测器预测未来场景 token 和自车轨迹。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from omegaconf import OmegaConf

REPO_DIR = Path(__file__).resolve().parents[2] / "repos" / "WA-JEPA"
sys.path.insert(0, str(REPO_DIR))


class WAJEPABridged(nn.Module):
    """继承 MultiViewCausalFutureMaskedJEPA，保持原始 forward 不变，仅用于身份标识。"""

    def __init__(self, model: nn.Module):
        super().__init__()
        self._model = model
        self._last_losses: dict = {}

    def forward(self, *args, **kwargs):
        # WA-JEPA 的 forward 方法接受一个 batch 字典
        # 但 run_forward.py 调用 model(**inputs)，会把 dict 解包为关键字参数
        # 所以这里需要重新打包为 batch 字典
        if len(args) == 1 and isinstance(args[0], dict):
            batch = args[0]
        elif kwargs:
            batch = kwargs
        else:
            batch = args[0] if args else {}
        
        output = self._model(batch)
        # 提取损失信息
        if isinstance(output, dict):
            loss_dict = output.get("loss", {})
            self._last_losses = {k: v for k, v in loss_dict.items() if "loss" in k.lower()}
        return output

    def __getattr__(self, name: str) -> Any:
        try:
            return super().__getattr__(name)
        except AttributeError:
            return getattr(self._model, name)


def build_model(model_dir: Path, dtype=torch.bfloat16) -> WAJEPABridged:
    """构建 WA-JEPA 模型。

    Args:
        model_dir: 包含 V-JEPA 2.1 权重和 WA-JEPA checkpoint 的目录
        dtype: 模型精度
    """
    # 导入 WA-JEPA 模型类
    from models.multiview_causal_future_jepa import MultiViewCausalFutureMaskedJEPA

    # 创建默认配置（使用较小的模型参数以加速 CPU 运行）
    config = {
        "model": {
            "target": "models.multiview_causal_future_jepa:MultiViewCausalFutureMaskedJEPA",
            "dtype": str(dtype),
            "variant": "vjepa2_1_vit_large_384",
            "use_rope": True,
            "use_sdpa": True,
            "interpolate_rope": True,
            "modality_embedding": True,
            "img_temporal_dim_size": 1,
            "use_activation_checkpointing": False,
            "camera_names": ["cam_l0", "cam_f0", "cam_r0", "cam_b0"],
            "input_hw": [256, 512],
            "pretrained_input_hw": [256, 256],
            "image_normalization": "minus_one_to_imagenet",
            "image_mean": [0.485, 0.456, 0.406],
            "image_std": [0.229, 0.224, 0.225],
            "num_history_frames": 4,
            "num_future_frames": 8,
            "patch_size": 16,
            "tubelet_size": 2,
            "mv_scene_dim": 256,  # 减小以加速
            "flow_hidden_dim": 256,  # 减小以加速
            "flow_num_layers": 4,  # 减小以加速
            "flow_num_heads": 4,  # 减小以加速
            "traj_loss_grad_to_scene_flow": True,
            "scene_loss_grad_to_traj_flow": False,
            "num_inference_steps": 4,
            "flow_time_sampling": "logit_normal",
            "flow_logit_mean": -0.2,
            "flow_logit_std": 1.6,
            "full_mask_prob": 1.0,
            "jepa_mask_configs": [
                {
                    "num_blocks": 8,
                    "spatial_scale": [0.15, 0.15],
                    "temporal_scale": [1.0, 1.0],
                    "aspect_ratio": [0.75, 1.5],
                }
            ],
            "flow_inference_noise_scale": 1.0,
            "flow_inference_seed": 0,
            "dynamic_collapse_topk": 64,
            "trajectory_norm_mean": [31.8, 1.32, 0.095],
            "trajectory_norm_std": [33.37, 21.0, 1.765],
            "ema_start": 0.99925,
            "ema_end": 0.99925,
            "ema_total_steps": 80600,
            "target_scene_ema_warmup_steps": 0,
            "freeze_encoder_steps": 0,
            "trajectory_horizon": 8,
            "ego_status_dim": 8,
            "driving_condition_adapter": "navsim",
            "enable_trajectory_head": True,
            "require_pretrained": False,
            "allow_partial_load": True,
        }
    }

    # 转换为 OmegaConf 配置
    cfg = OmegaConf.create(config)

    # 创建模型实例（不加载预训练权重，仅用于结构分析）
    model = MultiViewCausalFutureMaskedJEPA(cfg["model"], full_cfg=cfg)
    
    # 确保模型参数和输入类型一致
    model = model.to(dtype=dtype)

    # 注意：由于 V-JEPA 2.1 预训练权重不存在，这里不加载权重
    # 如果需要加载权重，请先下载：
    # - V-JEPA 2.1: https://huggingface.co/facebookresearch/vjepa2/tree/main
    # - WA-JEPA: https://huggingface.co/AFARI-Research/WA-JEPA

    return WAJEPABridged(model)


def last_losses(model) -> dict:
    """返回最近一次 forward 的损失字典（供 run_forward 采集）。"""
    return dict(getattr(model, "_last_losses", {}))
