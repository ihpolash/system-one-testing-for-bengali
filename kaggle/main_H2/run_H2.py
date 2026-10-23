"""[round 2, AI-generated Banglish of 2026-10-21] Kaggle: score every model on the items with AI-generated Banglish (SentNoB, MASSIVE, XNLI-bn pairs; ~880 items) under four spellings:
native Bengali, rule-based romanization, natural-style romanization, and the user's own Banglish. Rot0 only, English question wording.
Items and Banglish come from data/human_rows.json and data/banglish_human.csv (via BN_ROWS_JSON / BN_HUMAN_CSV). Resumable; cheapest models first."""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

MAX_HOURS = 8.0
os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-1800:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness 2>&1 | tail -1")
os.chdir(f"{work}/harness")
ROWS, ROWS_ED, HUMAN = f"{work}/data/human_rows.json", f"{work}/data/human_rows_edited.json", f"{work}/data/banglish_human.csv"
assert Path(ROWS).exists() and Path(ROWS_ED).exists() and Path(HUMAN).exists(), "human item files missing from the dataset"
# edit variants only differ from the originals on the sentences whose Bengali the author corrected; identical requests share one stored response
VARIANTS = [("human", ROWS), ("native_edit", ROWS_ED), ("roman_edit", ROWS_ED), ("roman_nat_edit", ROWS_ED)]
TASKS = "bn_sentnob bn_massive bn_bnli"

# (name, pip step, command template with {out}); group A uses the default transformers, group B needs >=5.17
SYS = "python scripts/run_system_one_model.py " + TASKS + " --split eval {args} --out {out}"
GEM = "python scripts/run_open_model.py " + TASKS + " --split eval --model google/gemma-4-E4B-it --device auto --dtype float16 --max-batch-tokens 3072 --out {out}"
PLAN = [
    ("laya_ml",  "pip install -q laya", SYS.replace("{args}", "--backend laya --model convaiinnovations/laya-multilingual --max-len 4096")),
    ("julia1",   "python -c \"from huggingface_hub import snapshot_download as s; s('SupersonicLabs/Julia-1', local_dir='/kaggle/tmp/Julia-1')\" && pip install -q -e /kaggle/tmp/Julia-1",
                 SYS.replace("{args}", "--backend julia --model SupersonicLabs/Julia-1 --julia-path /kaggle/tmp/Julia-1 --max-len 4096")),
    ("d3_edge",  "pip install -q 'transformers>=5.17' accelerate", SYS.replace("{args}", "--backend vllmsr --model vllm-sr/d3-edge --tag-suffix @18d61df786")),
    ("gemma4_e4b", None, GEM),
    ("d3_lite",  None, SYS.replace("{args}", "--backend vllmsr --model vllm-sr/d3-lite --tag-suffix @a8d25a91ef")),
    ("d3_nano",  None, SYS.replace("{args}", "--backend vllmsr --model vllm-sr/d3-nano --tag-suffix @3aeb1c22a5")),
    ("d3_mini",  None, SYS.replace("{args}", "--backend vllmsr --model vllm-sr/d3-mini --tag-suffix @a475367de0")),
    ("d3_flash", "pip install -q bitsandbytes", SYS.replace("{args}", "--backend vllmsr --model vllm-sr/d3-flash --tag-suffix @521525effa --d3-bnb 4")),
]
t_all = time.time()
for name, pre, cmd in PLAN:
    if (time.time() - t_all) / 3600 > MAX_HOURS:
        print("TIME GUARD: stopping", flush=True); break
    print(f"\n######## {name} (elapsed {(time.time()-t_all)/60:.0f} min)", flush=True)
    if pre:
        sh(pre + " 2>&1 | tail -2")
    out = f"/kaggle/working/runs/{name}_human2"
    for v, rows_file in VARIANTS:
        env = dict(os.environ, BN_VARIANT=v, BN_ROT="0", BN_QLANG="en", BN_ROWS_JSON=rows_file, BN_HUMAN_CSV=HUMAN)
        t0 = time.time()
        sh(cmd.format(out=out), env=env)
        n = sum(1 for f in Path(out).glob("*.jsonl") if f.name != "failures.jsonl" for _ in open(f))
        print(f"== {name} {v}: {(time.time()-t0)/60:.1f} min; lines so far {n}", flush=True)
        if n == 0:
            print(f"NO OUTPUT for {name}; moving on", flush=True); break
print("ALL DONE", (time.time() - t_all) / 3600, "h")
