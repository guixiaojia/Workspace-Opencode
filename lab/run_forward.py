"""Skill A 通用入口：python run_forward.py --project <proj>

流程：<proj>/config.yaml -> build_model 构建模型 -> build_input 造输入 -> hook 采集前向
产物：<proj>/outputs/trace.json + model_structure.md（契约见 lab/README.md）
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # 保证 repos/ 只读：导入仓库代码不产生 __pycache__
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch

LAB = Path(__file__).resolve().parent
ROOT = LAB.parent
sys.path.insert(0, str(LAB))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()

    import yaml

    cfg = yaml.safe_load((LAB / args.project / "config.yaml").read_text(encoding="utf-8"))
    proj_dir = LAB / args.project
    out_dir = proj_dir / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    model_dir = Path(cfg["model_dir"]).expanduser().resolve()
    dtype = getattr(torch, cfg.get("dtype", "bfloat16"))
    device = cfg.get("device", "cpu")

    shim = load_module(proj_dir / cfg["build_model"], f"build_model_{args.project}")
    fake = load_module(proj_dir / cfg["build_input"], f"build_input_{args.project}")

    print(f"[1/5] 构建模型 {cfg['model_class_hint']}（真实权重，{dtype} @ {device}）...")
    model = shim.build_model(model_dir, dtype=dtype)
    model.to(device).eval()

    print("[2/5] 构造假样本...")
    inputs = fake.build(model_dir, device=device, dtype=dtype)
    input_shapes = {k: list(v.shape) for k, v in inputs.items() if torch.is_tensor(v)}

    from tensor_probe import collect, write_trace, write_digest  # noqa: E402
    from arch_dumper import dump_structure  # noqa: E401

    probe = collect(model).attach()
    losses = {}
    with torch.no_grad():
        print("[3/5] 前向 #1（无轨迹标签，纯语言 CE）...")
        inputs_lang = {k: v for k, v in inputs.items() if k not in ("trajectory", "is_dummy_trajectory")}
        model(**inputs_lang)
        probe.detach()
        losses.update(shim.last_losses(model))
        probe.reset()

        print("[4/5] 前向 #2（含轨迹标签，双任务）+ 全量 hook 采集...")
        probe.attach()
        model(**inputs)
        probe.detach()
        losses.update(shim.last_losses(model))

    try:
        git_head = subprocess.run(
            ["git", "-C", str(ROOT / cfg.get("repo_dir", f"repos/{args.project}")), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10,
        ).stdout.strip()
    except Exception:
        git_head = ""

    write_trace(
        out_dir / "trace.json",
        project=args.project,
        model_path=str(model_dir),
        dtype=str(dtype).replace("torch.", ""),
        device=device,
        input_shapes=input_shapes,
        losses={
            k: (float(v) if isinstance(v, (int, float, torch.Tensor)) else v)
            for k, v in losses.items()
            if k not in ("_grad_total",)
        },
        events=probe.events,
        note=cfg.get("note", ""),
        git_head_repos=git_head,
    )
    dump_structure(model, out_dir / "model_structure.md", header_note=f"project={args.project} dtype={dtype} device={device}")
    write_digest(out_dir / "trace_digest.md", project=args.project, events=probe.events)

    n = len(probe.events)
    est = sum(len(e["input"]) + 1 for e in probe.events)
    clean = {
        k: (round(float(v), 4) if isinstance(v, (int, float, torch.Tensor)) else v)
        for k, v in losses.items()
        if k not in ("_grad_total",)
    }
    print(f"[5/5] 完成：{n} events（{est} 条 shape 记录），losses={json.dumps(clean, ensure_ascii=False)}")
    print(f"产物：{out_dir / 'trace.json'} | {out_dir / 'trace_digest.md'} | {out_dir / 'model_structure.md'}")


if __name__ == "__main__":
    main()
