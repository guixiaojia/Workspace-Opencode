"""AutoVLA 假输入构造器：走真实 processor 构造最小 batch。

AutoVLA 的输入是多视角视频帧 + 车辆状态 + 驾驶指令。
为简化前向采集，这里用纯色图片构造 dummy 输入。
"""
from __future__ import annotations

from pathlib import Path

import torch
from PIL import Image
from transformers import AutoProcessor


def build(model_dir: Path, device: str = "cpu", dtype=torch.bfloat16) -> dict:
    """构造 AutoVLA 的最小假输入 batch。

    Args:
        model_dir: Qwen2.5-VL-3B-Instruct 权重目录（用于加载 processor）
        device: 目标设备
        dtype: 模型精度
    """
    from qwen_vl_utils import process_vision_info

    processor = AutoProcessor.from_pretrained(model_dir)

    # 构造 dummy 视频帧（28x28 纯色图）
    dummy_frames = [Image.new("RGB", (28, 28), color=(128, 128, 128)) for _ in range(4)]

    # 构造 chat template 消息（单视角 × 4 帧 = 4 张图）
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "You are an Advanced Driver Assistance and Full Self-Driving System. "
                        "You will be provided with video observations from the ego vehicle's surrounding cameras, "
                        "along with the vehicle's current dynamic states. "
                        "Your task is to predict the most appropriate driving action for the next five seconds."
                    ),
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "The autonomous vehicle is equipped with cameras.",
                },
                {
                    "type": "video",
                    "min_pixels": 109760,
                    "max_pixels": 109760,
                    "video": dummy_frames,
                },
                {
                    "type": "text",
                    "text": (
                        "The current velocity of the vehicle is 5.000 m/s, and the current acceleration is 0.000 m/s². "
                        "The driving instruction is: go straight."
                    ),
                },
            ],
        },
    ]

    # 使用 qwen_vl_utils 处理视觉信息
    image_inputs, video_inputs = process_vision_info(messages)

    # 使用 processor 处理消息
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, add_vision_id=True
    )

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )

    return {k: v.to(device) if torch.is_tensor(v) else v for k, v in inputs.items()}
