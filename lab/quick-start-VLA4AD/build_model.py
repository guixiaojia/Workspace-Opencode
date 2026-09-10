"""Qwen2.5-VLA 兼容垫片：让 repos/quick-start-VLA4AD/modeling_qwen2_5_vla.py 的
模型定义在当前 transformers 4.57.6 上跑通前向。**不修改 repos/ 内文件**。

版本注记（2026-09-07 回退适配）：环境从 transformers 5.7.0 降至 4.57.6（配合
ms-swift 3.10.3，与仓库要求的 3.10.0dev 代际一致）。仓库代码本就是按 4.x 写的，
原先三处 v5 workaround 已回退为仓库原生路径：
- 适配点 1（回退）：4.57 基类形参仍收 output_attentions/output_hidden_states，
  按仓库 L65-81 原样透传，不再清洗。
- 适配点 2（回退）：直接取 outputs.hidden_states[-1]（仓库 L90 原路径），
  删除 v5 时代的 lm_head 前置钩子。
- 适配点 0（保留为无操作守卫）：4.57 config.hidden_size 在顶层，hasattr 检查
  自然跳过；守卫保留以兼容万一再升 v5。
与仓库源码的唯一语义差异（适配点 3，保留）：轨迹头计算、最后有效 token 提取
（L95-102）、view(-1,6,2)、MSE×权重（L105-133）逐行复刻，仅加 _last_losses
记账（分解 lang/traj loss 供 trace 采集，不改变任何计算与返回值）。
"""
from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn
from transformers import AutoConfig, Qwen2_5_VLForConditionalGeneration
from transformers.models.qwen2_5_vl.modeling_qwen2_5_vl import Qwen2_5_VLCausalLMOutputWithPast

REPO_DIR = Path(__file__).resolve().parents[2] / "repos" / "quick-start-VLA4AD"
import sys

sys.path.insert(0, str(REPO_DIR))
from modeling_qwen2_5_vla import Qwen2_5_VLAForConditionalGeneration as RepoVLA  # noqa: E402


class Qwen25VLABridged(RepoVLA):
    """继承仓库 VLA 类（含其 trajectory_head 与初始化），只重写 forward 的胶水层。"""

    def __init__(self, config):
        super().__init__(config)  # 仓库 __init__：建 trajectory_head + xavier 初始化
        self._last_losses: dict = {}

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        position_ids=None,
        past_key_values=None,
        inputs_embeds=None,
        labels=None,
        trajectory=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=True,  # 仓库 L53 默认值
        pixel_values=None,
        pixel_values_videos=None,
        image_grid_thw=None,
        video_grid_thw=None,
        return_dict=None,
        **_ignored_repo_kwargs,  # 吞掉 swift 框架可能传入的多余字段（仓库会把 **kwargs 透传给基类，此处不再透传以防意外键）
    ):
        # 适配点 1（回退）：4.57 基类原生接受 output_attentions/output_hidden_states，
        # 以下调用镜像仓库 L61-81。
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        output_hidden_states = True  # 仓库 L62 强制
        outputs = Qwen2_5_VLForConditionalGeneration.forward(
            self,
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            labels=labels,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            pixel_values=pixel_values,
            pixel_values_videos=pixel_values_videos,
            image_grid_thw=image_grid_thw,
            video_grid_thw=video_grid_thw,
            return_dict=return_dict,
        )
        lang_loss = outputs.loss

        self._last_losses = {
            "language_ce": None if lang_loss is None else float(lang_loss),
            "trajectory_mse": None,
            "trajectory_weighted": None,
            "total": None if lang_loss is None else float(lang_loss),
        }

        traj_predictions = None
        total_loss = lang_loss
        if trajectory is not None:
            # ==== 以下为仓库 modeling_qwen2_5_vla.py L87-141 逐行复刻 ====
            # 适配点 2（回退）：仓库 L90 原路径
            last_hidden_state = outputs.hidden_states[-1]  # [B, L, hidden]

            if attention_mask is not None:
                seq_lengths = attention_mask.sum(dim=1) - 1
                batch_indices = torch.arange(last_hidden_state.size(0), device=last_hidden_state.device)
                last_token_states = last_hidden_state[batch_indices, seq_lengths]
            else:
                last_token_states = last_hidden_state[:, -1, :]

            traj_predictions = self.trajectory_head(last_token_states)  # [B, 12]
            traj_predictions = traj_predictions.view(-1, 6, 2)  # [B, 6, 2]

            if traj_predictions.shape[0] != trajectory.shape[0]:
                if traj_predictions.shape[0] < trajectory.shape[0]:
                    repeat_factor = trajectory.shape[0] // traj_predictions.shape[0]
                    traj_predictions = traj_predictions.repeat(repeat_factor, 1, 1)
                    remaining = trajectory.shape[0] % traj_predictions.shape[0]
                    if remaining > 0:
                        traj_predictions = torch.cat([traj_predictions, traj_predictions[:remaining]], dim=0)
                else:
                    traj_predictions = traj_predictions[: trajectory.shape[0]]

            if traj_predictions.shape != trajectory.shape:
                traj_predictions = traj_predictions.reshape(trajectory.shape)

            raw_mse = nn.MSELoss()(traj_predictions, trajectory.float())
            traj_loss = raw_mse * getattr(self, "traj_loss_weight", 0.01)
            # 仓库 L136-141：合并损失
            total_loss = (lang_loss + traj_loss) if lang_loss is not None else traj_loss
            # ==== 复刻结束 ====

            self._last_losses.update(
                trajectory_mse=float(raw_mse),
                trajectory_weighted=float(traj_loss),
                traj_pred_shape=list(traj_predictions.shape),
            )
            if lang_loss is not None:
                self._last_losses["total"] = float(total_loss)
                self._last_losses["_grad_total"] = total_loss

        self._traj_predictions = traj_predictions
        # 镜像仓库 L147-154：返回合并 loss 后的输出对象（而非基类原始 outputs）
        return Qwen2_5_VLCausalLMOutputWithPast(
            loss=total_loss,
            logits=outputs.logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            rope_deltas=outputs.rope_deltas,
        )


def build_model(model_dir: Path, dtype=torch.bfloat16) -> Qwen25VLABridged:
    config = AutoConfig.from_pretrained(model_dir)
    # 适配点 0（4.57 下为无操作守卫）：config.hidden_size 本就在顶层，hasattr 跳过；
    # 守卫保留以兼容万一再升 v5（v5 拆为 text_config/vision_config 子配置）。
    if not hasattr(config, "hidden_size"):
        config.hidden_size = config.text_config.hidden_size
    # 对应仓库 save_custom_model.py L64-67 的配置注入
    config.trajectory_output_dim = 12          # 6 步 × (x,y)
    config.trajectory_head_hidden_size = 512
    config.trajectory_loss_weight = 0.5
    config.architectures = ["Qwen2_5_VLAForConditionalGeneration"]

    try:
        return Qwen25VLABridged.from_pretrained(model_dir, config=config, dtype=dtype, low_cpu_mem_usage=True)
    except TypeError:  # 兼容旧版参数名
        return Qwen25VLABridged.from_pretrained(model_dir, config=config, torch_dtype=dtype, low_cpu_mem_usage=True)


def last_losses(model) -> dict:
    return dict(getattr(model, "_last_losses", {}))
