"""forward hook 采集器：把模型前向的每个模块 I/O 形状写成 trace.json（契约第 4 节），
并派生人读聚合视图 trace_digest.md（同构事件折叠，如 32 个 vision block × N 子模块）。

只记 shape/dtype/参数量，不保存张量引用（3B 模型全量驻留会爆内存）。
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import torch
import torch.nn as nn


def _describe(obj: Any) -> Optional[Dict]:
    if isinstance(obj, torch.Tensor):
        return {"shape": list(obj.shape), "dtype": str(obj.dtype).replace("torch.", "")}
    return None


def _pack(obj: Any) -> Any:
    d = _describe(obj)
    if d is not None:
        return d
    if isinstance(obj, (tuple, list)):
        items = [x for x in (_pack(o) for o in obj) if x is not None]
        return items or None
    if isinstance(obj, dict):
        items = [x for x in (_pack(v) for v in obj.values()) if x is not None]
        return items or None
    return None


class TensorProbe:
    """给 root 下所有命名模块挂 with_kwargs 前向钩子，按执行顺序收集 events。"""

    def __init__(self, root: nn.Module):
        self.root = root
        self.events: List[Dict] = []
        self._handles = []

    def attach(self) -> "TensorProbe":
        for name, mod in self.root.named_modules():
            if not name:
                continue
            h = mod.register_forward_hook(self._make_hook(), with_kwargs=True)
            self._handles.append(h)
        return self

    def _make_hook(self):
        def hook(m: nn.Module, args: tuple, kwargs: dict, output: Any):
            name = self.root._probe_names[id(m)]
            ins = [d for d in (_describe(a) for a in args) if d]
            if not ins:
                for v in kwargs.values():
                    d = _describe(v)
                    if d:
                        ins = [d]
                        break
            self.events.append(
                {
                    "module": name,
                    "class": type(m).__name__,
                    "depth": name.count(".") + 1,
                    "input": ins,
                    "output": _pack(output),
                    "params": sum(p.numel() for p in m.parameters(recurse=False)),
                }
            )

        return hook

    def detach(self) -> None:
        for h in self._handles:
            h.remove()
        self._handles.clear()

    def reset(self) -> None:
        self.events.clear()


def collect(root: nn.Module):
    root._probe_names = {id(m): n for n, m in root.named_modules() if n}
    return TensorProbe(root)


def write_trace(
    path: Path,
    project: str,
    model_path: str,
    dtype: str,
    device: str,
    input_shapes: Dict[str, List[int]],
    losses: Dict[str, float],
    events: List[Dict],
    note: str = "",
    git_head_repos: str = "",
) -> None:
    trace = {
        "meta": {
            "project": project,
            "model_path": model_path,
            "torch_dtype": dtype,
            "device": device,
            "input_shapes": {k: list(v) for k, v in input_shapes.items()},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "git_head_repos": git_head_repos,
            "note": note,
        },
        "losses": losses,
        "events": events,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trace, ensure_ascii=False, indent=1), encoding="utf-8")


def _fold_name(name: str) -> str:
    """把 ModuleList 编号段折叠为 {}：`blocks.12.attn.qkv` -> `blocks.{}.attn.qkv`"""
    return re.sub(r"\.\d+(?=\.|$)", ".{}", name)


def _fmt_shape(d: Any) -> str:
    """{"shape":[a,b]} -> 'a×b'；嵌套列表 -> '(x, y)'（超 3 项截断为 'x, y …×N'）；空 -> ''"""
    if isinstance(d, dict):
        return "×".join(str(x) for x in d["shape"])
    if isinstance(d, list):
        items = [s for s in (_fmt_shape(x) for x in d) if s]
        if not items:
            return ""
        if len(items) > 3:
            return f"({items[0]}, {items[1]} …×{len(items)})"
        return f"({', '.join(items)})"
    return ""


def write_digest(path: Path, project: str, events: List[Dict]) -> None:
    """trace.json 的人读派生视图：按折叠名+类+I/O 签名合并同构事件，保留执行顺序。"""
    groups: Dict[tuple, Dict] = {}
    order: List[tuple] = []
    for ev in events:
        folded = _fold_name(ev["module"])
        sig = (folded, ev["class"], json.dumps([ev["input"], ev["output"]]))
        if sig not in groups:
            groups[sig] = {
                "name": ev["module"],  # 单例组保留原名；多例组展示折叠名
                "class": ev["class"],
                "count": 0,
                "in": _fmt_shape(ev["input"]),
                "out": _fmt_shape(ev["output"]),
                "params": ev["params"],
            }
            order.append(sig)
        groups[sig]["count"] += 1

    lines = [
        f"# trace_digest.md — 聚合张量流（{project}）",
        "",
        f"> trace.json 的 {len(events)} events 折叠为 {len(groups)} 组（同构模块合并，×N 为重复次数）；"
        f"shape 记法 `a×b×c`，`(x, y)` 为多元组；按前向执行顺序排列。原始数据见 trace.json。",
        "",
        "| # | 模块 | 类 | ×N | 输入 → 输出 | 参数 |",
        "|---|---|---|---|---|---:|",
    ]
    for i, sig in enumerate(order, 1):
        g = groups[sig]
        name = _fold_name(g["name"]) if g["count"] > 1 else g["name"]
        io = f"{g['in'] or '—'} → {g['out'] or '—'}"
        lines.append(f"| {i} | `{name}` | {g['class']} | ×{g['count']} | {io} | {g['params']:,} |")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
