"""nn.Module -> model_structure.md：顶层模块表 + 全量 print(model) + 子树参数量。"""
from __future__ import annotations

import io
from pathlib import Path

import torch.nn as nn


def _count_params(mod: nn.Module, only_direct: bool = False) -> int:
    if only_direct:
        return sum(p.numel() for p in mod.parameters(recurse=False))
    return sum(p.numel() for p in mod.parameters())


def _fmt(n: int) -> str:
    if n >= 1e9:
        return f"{n / 1e9:.2f}B"
    if n >= 1e6:
        return f"{n / 1e6:.2f}M"
    if n >= 1e3:
        return f"{n / 1e3:.1f}K"
    return str(n)


def dump_structure(model: nn.Module, out_path: Path, header_note: str = "") -> Path:
    buf = io.StringIO()
    print(model, file=buf)
    total = _count_params(model)

    lines = ["# model_structure.md", ""]
    if header_note:
        lines += [f"> {header_note}", ""]
    lines += [f"- 总参数量：**{total:,}**（{_fmt(total)}）", f"- 顶层模块数：{len(list(model.children()))}", ""]

    lines += ["## 顶层模块一览", "", "| 模块 | 类 | 参数量 | 占比 | 子模块数 |", "|---|---|---:|---:|---:|"]
    for name, child in model.named_children():
        p = _count_params(child)
        lines.append(
            f"| `{name}` | {type(child).__name__} | {p:,}（{_fmt(p)}） | {100 * p / total:.1f}% | {len(list(child.children()))} |"
        )
    lines += ["", "## 二级模块参数量", "", "| 路径 | 类 | 参数量 |", "|---|---|---:|"]
    for name, child in model.named_children():
        for sub_name, sub in child.named_children():
            p = _count_params(sub)
            lines.append(f"| `{name}.{sub_name}` | {type(sub).__name__} | {p:,}（{_fmt(p)}） |")

    lines += ["", "## print(model) 全量输出", "", "```python", buf.getvalue().rstrip(), "```", ""]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
