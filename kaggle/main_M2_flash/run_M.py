"""Kaggle: d3-flash (9B, 4-bit NF4 because it does not fit a T4 in BF16) on the Dakshina-bn cross-script agreement task, a hash-ordered subset of 500 sentences
(nested in the 1,500 used for the other systems). Smoke test picks 4-bit or 8-bit first."""
import json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")
VARIANTS = ["roman_nat"]   # rerun: the natural-style lookup was rebuilt without Dakshina sentences

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-2200:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/tmp/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
for f in ("dakshina_bn", "sentnob", "sib200"):   # fail fast: a missing data file makes a task silently write 0 responses
    assert os.path.getsize(f"{work}/data/raw/{f}.jsonl") > 1000, f"data/raw/{f}.jsonl missing from the dataset"
assert os.path.exists(f"{work}/analysis/natural_banglish_lookup.json"), "natural-style lookup missing"
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
LIMIT = 500
sh(f"pip install -q -e {work}/harness 'transformers>=5.17' accelerate bitsandbytes 2>&1 | tail -2")
os.chdir(f"{work}/harness")
ARGS = "--backend vllmsr --model vllm-sr/d3-flash --tag-suffix @521525effa"

def smoke(bits):
    d = f"/kaggle/tmp/smoke_flash_{bits}"
    sh(f"python scripts/run_system_one_model.py bn_dakshina --split eval --limit 8 {ARGS} --d3-bnb {bits} --out {d}", env=dict(os.environ, BN_VARIANT="native", BN_ROT="0", BN_QLANG="en"))
    rows = [json.loads(l) for f in Path(d).glob("responses.jsonl") for l in open(f)]
    ok = bool(rows) and all(abs(sum(r["response"]["answers"]["answer"]["probabilities"].values()) - 1) < 1e-3 for r in rows)
    print(f"smoke {bits}-bit: {len(rows)} rows, valid={ok}", flush=True)
    return ok

bits = next((b for b in (4, 8) if smoke(b)), None)
if bits is None:
    print("NO WORKING QUANTIZATION; aborting", flush=True); sys.exit(1)
out = "/kaggle/working/runs/d3_flash_dak"; t_all = time.time()
for v in VARIANTS:
    t0 = time.time()
    sh(f"python scripts/run_system_one_model.py bn_dakshina --split eval --limit {LIMIT} {ARGS} --d3-bnb {bits} --out {out}", env=dict(os.environ, BN_VARIANT=v, BN_ROT="0", BN_QLANG="en"))
    n = sum(1 for f in Path(out).glob("responses.jsonl") for _ in open(f))
    print(f"== d3_flash {bits}-bit {v}: {(time.time()-t0)/60:.1f} min; responses so far {n}", flush=True)
    if v == VARIANTS[0] and n == 0:
        print("NO OUTPUT; aborting", flush=True); sys.exit(2)
print("ALL DONE", (time.time() - t_all) / 3600, "h")
