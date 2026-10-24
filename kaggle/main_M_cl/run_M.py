"""Kaggle: Dakshina-bn cross-script agreement (data/make_dakshina.py; analysis/dakshina.py). For each system: one 7-way topic question per sentence in four spellings
(native, dakshina = native-speaker romanization, roman = rule-based, roman_nat = natural-style), rotation 0.
DAK_SET picks the systems, SMOKE=1 runs 24 sentences only (always smoke a new backend first), LIMIT is the sentence count otherwise.
Code and data are copied to /kaggle/tmp so that only runs/ and the logs are saved as output."""
import os, shutil, subprocess, sys, time, traceback
from pathlib import Path

SMOKE = os.environ.get("SMOKE", "0") == "1"
LIMIT = 24 if SMOKE else int(os.environ.get("LIMIT", "1500"))
DAK_SET = os.environ.get("DAK_SET", "CL")
VARIANTS = ["native", "dakshina", "roman", "roman_nat"]
MODELS = {
    "laya_ml": dict(pre="pip install -q laya", args="--backend laya --model convaiinnovations/laya-multilingual --max-len 4096"),
    "julia1": dict(pre="pip install -q -e /kaggle/tmp/Julia-1", args="--backend julia --model SupersonicLabs/Julia-1 --julia-path /kaggle/tmp/Julia-1 --max-len 4096",
                   hf_snapshot=("SupersonicLabs/Julia-1", "/kaggle/tmp/Julia-1")),
    "d3_edge": dict(pre="pip install -q 'transformers>=5.17' accelerate", args="--backend vllmsr --model vllm-sr/d3-edge --tag-suffix @18d61df786 --max-len 4096"),
    "d3_lite": dict(pre=None, args="--backend vllmsr --model vllm-sr/d3-lite --tag-suffix @a8d25a91ef --max-len 4096"),
    "d3_nano": dict(pre=None, args="--backend vllmsr --model vllm-sr/d3-nano --tag-suffix @3aeb1c22a5 --max-len 4096"),
    "d3_mini": dict(pre="pip install -q flash-linear-attention || true", args="--backend vllmsr --model vllm-sr/d3-mini --tag-suffix @a475367de0 --max-len 4096"),
    "laya_bangla": dict(pre="pip install -q 'laya==0.4.11'", args="--backend laya --model algolyzer/laya-bangla --revision v2 --tag-suffix @4c5eb48932 --max-len 4096"),
}
SETS = {"C": ["laya_ml", "julia1"], "CL": ["laya_ml", "julia1", "laya_bangla"], "B": ["d3_edge", "d3_lite", "d3_nano", "d3_mini"], "LB": ["laya_bangla"]}

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, env=None):
    print("$", cmd, flush=True)
    r = subprocess.run(cmd, shell=True, text=True, capture_output=True, env=env)
    print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-1800:], flush=True)
    return r.returncode

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/tmp/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
for f in ("dakshina_bn", "sentnob", "sib200"):   # fail fast: a missing data file makes a task silently write 0 responses
    assert os.path.getsize(f"{work}/data/raw/{f}.jsonl") > 1000, f"data/raw/{f}.jsonl missing from the dataset"
assert os.path.exists(f"{work}/analysis/natural_banglish_lookup.json"), "natural-style lookup missing"
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness 2>&1 | tail -1")
os.chdir(f"{work}/harness")
t_all = time.time()
for m in SETS[DAK_SET]:
    spec = MODELS[m]
    print(f"\n######## {m} (elapsed {(time.time()-t_all)/60:.0f} min), limit {LIMIT}", flush=True)
    try:
        if spec.get("hf_snapshot"):
            from huggingface_hub import snapshot_download
            snapshot_download(spec["hf_snapshot"][0], local_dir=spec["hf_snapshot"][1])
        if spec["pre"]:
            sh(spec["pre"] + " 2>&1 | tail -1")
        out = f"/kaggle/working/runs/{m}_dak"
        for v in VARIANTS:
            t0 = time.time()
            sh(f"python scripts/run_system_one_model.py bn_dakshina --split eval --limit {LIMIT} {spec['args']} --out {out}", env=dict(os.environ, BN_VARIANT=v, BN_QLANG="en", BN_ROT="0"))
            n = sum(1 for f in Path(out).glob("*.jsonl") if f.name != "failures.jsonl" for _ in open(f)) if Path(out).exists() else 0
            print(f"== {m} {v}: {(time.time()-t0)/60:.1f} min; responses so far {n}", flush=True)
            if v == "native" and n == 0:
                raise RuntimeError(f"{m}: no responses after the first condition; stopping this system")
    except Exception:
        traceback.print_exc()
print("ALL DONE", (time.time() - t_all) / 3600, "h")
