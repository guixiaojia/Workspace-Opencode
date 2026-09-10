"""假样本构造：真实 processor/tokenizer 管线 + 随机噪声图像 + 随机轨迹标签。

故意走 processor 全路径（而非手捏 pixel_values），让 smart_resize、patch 重排、
image token 展开等前置变换都进入 trace。等价于 custom_dataset.py 中
Qwen2_5VLATemplate._encode 的轨迹注入逻辑（L69-118）的最小离线复刻。
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import AutoProcessor


def build(model_dir: Path, device="cpu", dtype=torch.bfloat16, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    img = Image.fromarray(rng.integers(0, 255, (448, 448, 3), dtype=np.uint8))

    processor = AutoProcessor.from_pretrained(model_dir)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Observe the scene and plan the future driving trajectory."},
            ],
        },
        {
            "role": "assistant",
            "content": [{"type": "text", "text": "The ego vehicle will keep going straight at a constant speed."}],
        },
    ]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    enc = processor(images=[img], text=[text], return_tensors="pt")

    input_ids = enc["input_ids"]
    # labels：图像 pad token 与 system/user 前缀不参与语言监督，只监督 assistant 内容
    labels = input_ids.clone()
    image_token_id = processor.tokenizer.convert_tokens_to_ids("<|image_pad|>")
    labels[input_ids == image_token_id] = -100
    assistant_marker = processor.tokenizer("assistant\n", add_special_tokens=False)["input_ids"]
    start = None
    ids = input_ids[0].tolist()
    for i in range(len(ids) - len(assistant_marker)):
        if ids[i : i + len(assistant_marker)] == assistant_marker:
            start = i + len(assistant_marker)
    if start is not None:
        labels[:, : start] = -100

    # 轨迹标签 [1, 6, 2]：匀速直行的平滑曲线 + 噪声（对应 gt_planning 语义，custom_dataset.py L105 校验的形状）
    t = np.linspace(0, 1, 6)
    traj = np.stack([2.0 * t, 0.1 * np.sin(3 * t) + rng.normal(0, 0.02, 6)], axis=1)

    inputs = {
        "input_ids": input_ids.to(device),
        "attention_mask": enc["attention_mask"].to(device),
        "labels": labels.to(device),
        "pixel_values": enc["pixel_values"].to(device=device, dtype=dtype),
        "image_grid_thw": enc["image_grid_thw"].to(device),
        "trajectory": torch.tensor(traj, dtype=torch.float32).unsqueeze(0).to(device),
    }
    return inputs
