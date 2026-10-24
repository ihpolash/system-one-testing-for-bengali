"""Kaggle: Gemma-4-E4B-it baseline (each option scored by exact next-token probability) on the Dakshina-bn cross-script agreement task, 1,500 sentences.
fp16 or bf16 is picked by a smoke test (a T4 has no native bf16; Gemma can overflow in fp16)."""
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
LIMIT, MODEL, MAXTOK = 1500, "google/gemma-4-E4B-it", 3072
sh(f"pip install -q -e {work}/harness 'transformers>=5.0' accelerate 2>&1 | tail -1")
os.chdir(f"{work}/harness")
out = "/kaggle/working/runs/gemma4_e4b_dak"

def smoke(dtype):
    d = f"/kaggle/tmp/smoke_{dtype}"
    sh(f"python scripts/run_open_model.py bn_dakshina --split eval --limit 40 --model {MODEL} --device auto --dtype {dtype} --max-batch-tokens {MAXTOK} --out {d}", env=dict(os.environ, BN_VARIANT="native", BN_ROT="0", BN_QLANG="en"))
    rows = [json.loads(l) for f in Path(d).glob("*.jsonl") for l in open(f)]
    if not rows: return False
    mass = [m for r in rows for m in r["response"]["diagnostics"]["valid_mass"].values()]
    ok = all(m == m for m in mass) and sum(mass) / len(mass) > 0.9
    print(f"smoke {dtype}: {len(rows)} rows, mean valid mass {sum(mass)/max(1,len(mass)):.3f}, ok={ok}", flush=True)
    return ok

dtype = next((d for d in ("float16", "bfloat16") if smoke(d)), None)
if dtype is None:
    print("NO WORKING DTYPE; aborting", flush=True); sys.exit(1)
t_all = time.time()
for v in VARIANTS:
    t0 = time.time()
    sh(f"python scripts/run_open_model.py bn_dakshina --split eval --limit {LIMIT} --model {MODEL} --device auto --dtype {dtype} --max-batch-tokens {MAXTOK} --out {out}", env=dict(os.environ, BN_VARIANT=v, BN_ROT="0", BN_QLANG="en"))
    n = sum(1 for f in Path(out).glob("*.jsonl") for _ in open(f))
    print(f"== gemma {v}: {(time.time()-t0)/60:.1f} min; responses so far {n}", flush=True)
    if v == VARIANTS[0] and n == 0:
        print("NO OUTPUT AFTER FIRST CONDITION; aborting", flush=True); sys.exit(2)
print("ALL DONE", (time.time() - t_all) / 3600, "h")
