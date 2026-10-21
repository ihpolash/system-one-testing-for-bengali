"""Kaggle: Gemma-4-E4B-it baseline, scored by exact next-token option probabilities (Deussers protocol) on the Bengali tasks.
Picks fp16 or bf16 by a smoke test (T4 has no native bf16; Gemma can overflow in fp16). Rot0 test + dev first, rotations if time remains."""
import json, os, shutil, subprocess, sys, time

MODEL = "google/gemma-4-E4B-it"
LIMIT_LARGE, DEV_LIMIT, MAX_HOURS = 1500, 1500, 7.0
MAXTOK = 3072  # batch token budget; the default 32,768 ran out of memory on 2x T4 (the model is 16 GB in fp16)
SETTINGS = [("native", 0, "eval"), ("roman", 0, "eval"), ("native", 0, "dev"), ("roman", 0, "dev"),
            ("native", 1, "eval"), ("native", 2, "eval"), ("roman", 1, "eval"), ("roman", 2, "eval")]
SMALL = {"native": "bn_sentnob bn_belebele bn_sib200", "roman": "bn_sentnob bn_sib200"}
LARGE = "bn_bnli bn_massive"

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        t = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-1800:]
        print(t, flush=True); return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness 'transformers>=5.0' accelerate 2>&1 | tail -1")
os.chdir(f"{work}/harness")
out = "/kaggle/working/runs/gemma4_e4b"

def smoke(dtype):
    d = f"/kaggle/working/smoke_{dtype}"
    env = dict(os.environ, BN_VARIANT="native", BN_ROT="0", BN_QLANG="en")
    # realistic load: long Belebele passages (test split) plus short items, at the production batch budget
    sh(f"python scripts/run_open_model.py bn_belebele bn_sentnob --split eval --limit 40 --model {MODEL} --device auto --dtype {dtype} --max-batch-tokens {MAXTOK} --out {d}", env=env)
    rows = [json.loads(l) for f in __import__('pathlib').Path(d).glob('*.jsonl') for l in open(f)]
    if not rows: return False
    mass = [m for r in rows for m in r["response"]["diagnostics"]["valid_mass"].values()]
    ok = all(m == m for m in mass) and sum(mass) / len(mass) > 0.9  # no NaN, most probability on the answer codes
    print(f"smoke {dtype}: {len(rows)} rows, mean valid mass {sum(mass)/max(1,len(mass)):.3f}, ok={ok}", flush=True)
    return ok

dtype = next((d for d in ("float16", "bfloat16") if smoke(d)), None)
if dtype is None:
    print("NO WORKING DTYPE; aborting", flush=True); sys.exit(1)

t_all = time.time()
for variant, rot, split in SETTINGS:
    if (time.time() - t_all) / 3600 > MAX_HOURS:
        print("TIME GUARD: stopping", flush=True); break
    env = dict(os.environ, BN_VARIANT=variant, BN_QLANG="en", BN_ROT=str(rot))
    t0 = time.time()
    groups = ((SMALL[variant], ""), (LARGE, f"--limit {LIMIT_LARGE}")) if split == "eval" else (("bn_sentnob bn_bnli bn_massive", f"--limit {DEV_LIMIT}"),)
    for tasks, lim in groups:
        sh(f"python scripts/run_open_model.py {tasks} --split {split} {lim} --model {MODEL} --device auto --dtype {dtype} --max-batch-tokens {MAXTOK} --out {out}", env=env)
    n = sum(1 for f in __import__('pathlib').Path(out).glob('*.jsonl') for _ in open(f))
    if n == 0:
        print("NO OUTPUT AFTER FIRST SETTING; aborting instead of burning quota", flush=True); sys.exit(2)
    print(f"== gemma {split} {variant} rot{rot}: {(time.time()-t0)/60:.1f} min; lines so far {n}", flush=True)
print("ALL DONE", (time.time() - t_all) / 3600, "h")
