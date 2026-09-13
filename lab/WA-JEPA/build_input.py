"""WA-JEPA 假输入构造器：构造最小 batch 用于前向采集。

WA-JEPA 的输入是多视角视频帧（4个摄像头 × 4个历史帧）+ 自车状态 + 历史轨迹。
为简化前向采集，这里用纯色图片构造 dummy 输入。
"""
from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn


def build(model_dir: Path, device: str = "cpu", dtype=torch.bfloat16) -> dict:
    """构造 WA-JEPA 的最小假输入 batch。

    Args:
        model_dir: 包含模型权重的目录（当前未使用，保留接口一致性）
        device: 目标设备
        dtype: 模型精度
    """
    batch_size = 1
    num_cameras = 4  # cam_l0, cam_f0, cam_r0, cam_b0
    num_history_frames = 4
    num_future_frames = 8
    image_height, image_width = 256, 512
    ego_status_dim = 8
    history_steps = 4
    trajectory_horizon = 8

    # 构造 dummy 历史帧 [B, T, V, C, H, W]
    # T = num_history_frames, V = num_cameras
    history_images = torch.randn(
        batch_size,
        num_history_frames,
        num_cameras,
        3,
        image_height,
        image_width,
        dtype=dtype,
        device=device,
    )

    # 构造 dummy 未来帧 [B, T, V, C, H, W]
    # T = num_future_frames, V = num_cameras
    future_images = torch.randn(
        batch_size,
        num_future_frames,
        num_cameras,
        3,
        image_height,
        image_width,
        dtype=dtype,
        device=device,
    )

    # 构造 dummy 自车状态 [B, ego_status_dim]
    # 包含速度、加速度、转向角等信息
    ego_status = torch.randn(
        batch_size,
        ego_status_dim,
        dtype=dtype,
        device=device,
    )

    # 构造 dummy 历史轨迹 [B, history_steps, 3]
    # 3 = (x, y, yaw)
    history_trajectory = torch.randn(
        batch_size,
        history_steps,
        3,
        dtype=dtype,
        device=device,
    )

    # 构造 dummy 未来轨迹（用于训练，前向采集时可选）[B, trajectory_horizon, 3]
    future_trajectory = torch.randn(
        batch_size,
        trajectory_horizon,
        3,
        dtype=dtype,
        device=device,
    )

    return {
        "history_images": history_images,
        "future_images": future_images,
        "ego_status": ego_status,
        "history_trajectory": history_trajectory,
        "future_trajectory": future_trajectory,
    }
