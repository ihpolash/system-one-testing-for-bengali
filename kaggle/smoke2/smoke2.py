"""Kaggle smoke test 2: Laya-multilingual (fixed load), then Decision 3.0 (d3-nano, d3-edge). Caches stay out of /kaggle/working."""
import os, shutil, subprocess, sys

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, timeout=900, **kw):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, **kw)
        print((r.stdout + r.stderr)[-2500:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT after", timeout, "s", flush=True)
        return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"
shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness laya 2>&1 | tail -2")
os.chdir(f"{work}/harness")
env = dict(os.environ, BN_VARIANT="native", BN_QLANG="en", BN_ROT="0")

def run(name, args):
    print(f"\n===== {name}", flush=True)
    sh(f"python scripts/run_system_one_model.py bn_sentnob bn_bnli --split dev --limit 20 {args}", timeout=900, env=env)
    out = args.split("--out ")[1].split()[0]
    p = f"{out}/responses.jsonl"
    if os.path.exists(p):
        lines = open(p).read().splitlines(); print("lines:", len(lines)); print(lines[0][:900])

run("laya-multilingual", "--backend laya --model convaiinnovations/laya-multilingual --max-len 1024 --out /kaggle/working/runs/laya_ml")
sh("pip install -q 'transformers>=5.17' accelerate 2>&1 | tail -2")
run("d3-edge", "--backend vllmsr --model vllm-sr/d3-edge --tag-suffix @18d61df786 --out /kaggle/working/runs/d3_edge")
run("d3-nano", "--backend vllmsr --model vllm-sr/d3-nano --tag-suffix @3aeb1c22a5 --out /kaggle/working/runs/d3_nano")
