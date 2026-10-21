"""Kaggle: vllm-sr/d3-flash (9B) with bitsandbytes weight quantization (it does not fit a 15 GB T4 in BF16: ~24 GB peak).
Smoke test picks 4-bit (nf4) or falls back to 8-bit; aborts if neither produces valid output. Then a hash-ordered test SUBSET
(--limit 400 per task; nested in the larger subsets used for other models) in native and synthetic-romanized text, rot0 only.
Deviation from the checkpoint's BF16 numerics must be reported."""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

LIMIT, MAX_HOURS = 400, 8.0
os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-2200:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness 'transformers>=5.17' accelerate bitsandbytes 2>&1 | tail -2")
os.chdir(f"{work}/harness")
ARGS = "--backend vllmsr --model vllm-sr/d3-flash --tag-suffix @521525effa"

def smoke(bits):
    d = f"/kaggle/working/smoke_flash_{bits}"
    env = dict(os.environ, BN_VARIANT="native", BN_ROT="0", BN_QLANG="en")
    t0 = time.time()
    sh(f"python scripts/run_system_one_model.py bn_belebele bn_sentnob --split eval --limit 8 {ARGS} --d3-bnb {bits} --out {d}", env=env)
    rows = [json.loads(l) for f in Path(d).glob("responses.jsonl") for l in open(f)]
    ok = bool(rows) and all(abs(sum(r["response"]["answers"]["answer"]["probabilities"].values()) - 1) < 1e-3 for r in rows)
    print(f"smoke {bits}-bit: {len(rows)} rows in {time.time()-t0:.0f}s (includes load), valid={ok}", flush=True)
    return ok

bits = next((b for b in (4, 8) if smoke(b)), None)
if bits is None:
    print("NO WORKING QUANTIZATION; aborting", flush=True); sys.exit(1)

out = "/kaggle/working/runs/d3_flash"
t_all = time.time()
for variant, tasks in (("native", "bn_sentnob bn_belebele bn_sib200 bn_bnli bn_massive"), ("roman", "bn_sentnob bn_sib200 bn_bnli bn_massive")):
    if (time.time() - t_all) / 3600 > MAX_HOURS:
        print("TIME GUARD", flush=True); break
    env = dict(os.environ, BN_VARIANT=variant, BN_ROT="0", BN_QLANG="en")
    t0 = time.time()
    sh(f"python scripts/run_system_one_model.py {tasks} --split eval --limit {LIMIT} {ARGS} --d3-bnb {bits} --out {out}", env=env)
    n = sum(1 for f in Path(out).glob("responses.jsonl") for _ in open(f))
    print(f"== d3_flash {bits}-bit eval {variant} rot0: {(time.time()-t0)/60:.1f} min; lines so far {n}", flush=True)
    if n == 0:
        print("NO OUTPUT; aborting", flush=True); sys.exit(2)
print("ALL DONE", (time.time() - t_all) / 3600, "h")
