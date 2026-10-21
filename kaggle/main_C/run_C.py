"""Main Kaggle run: score the Bengali test splits with a set of System One models. Resumable, failure-tolerant.

MODELSET picks the models (set by the generator). Settings run in priority order so partial output is still useful:
native rot0, roman rot0, native rot1/2, roman rot1/2. Large tasks (bnli, massive) use a hash-ordered subset (LIMIT_LARGE).
Model caches live in /kaggle/tmp so /kaggle/working holds only results.
"""
import json, os, shutil, subprocess, sys, time, traceback

MODELSET = "C"
LIMIT_LARGE = 1500
DEV_LIMIT = 1500

MODELS = {
    "laya_ml": dict(pre="pip install -q laya", args="--backend laya --model convaiinnovations/laya-multilingual --max-len 4096"),
    "julia1": dict(pre="pip install -q -e /kaggle/tmp/Julia-1", args="--backend julia --model SupersonicLabs/Julia-1 --julia-path /kaggle/tmp/Julia-1 --max-len 4096",
                   hf_snapshot=("SupersonicLabs/Julia-1", "/kaggle/tmp/Julia-1")),
    "d3_edge": dict(pre="pip install -q 'transformers>=5.17' accelerate", args="--backend vllmsr --model vllm-sr/d3-edge --tag-suffix @18d61df786 --max-len 4096"),
    "d3_lite": dict(pre=None, args="--backend vllmsr --model vllm-sr/d3-lite --tag-suffix @a8d25a91ef --max-len 4096"),
    "d3_nano": dict(pre=None, args="--backend vllmsr --model vllm-sr/d3-nano --tag-suffix @3aeb1c22a5 --max-len 4096"),
    "d3_mini": dict(pre=None, args="--backend vllmsr --model vllm-sr/d3-mini --tag-suffix @a475367de0 --max-len 4096"),
}
SETS = {"B": ["d3_edge", "d3_lite", "d3_nano", "d3_mini"], "C": ["laya_ml", "julia1"]}
MAX_HOURS = 8.0  # stop starting new settings after this; Kaggle sessions end at 9-12 h
# (variant, rotation, split). Dev runs (disjoint from test) feed temperature scaling; they come right after rot0 test.
SETTINGS = [("native", 0, "eval"), ("roman", 0, "eval"), ("native", 0, "dev"), ("roman", 0, "dev"),
            ("native", 1, "eval"), ("native", 2, "eval"), ("roman", 1, "eval"), ("roman", 2, "eval")]
SMALL = {"native": "bn_sentnob bn_belebele bn_sib200", "roman": "bn_sentnob bn_sib200"}  # belebele ben_Latn is the human romanization
LARGE = "bn_bnli bn_massive"

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        tail = (r.stdout + r.stderr)
        tail = "\n".join(l for l in tail.splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-1800:]
        print(tail, flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True)
        return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"
shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness 2>&1 | tail -1")
os.chdir(f"{work}/harness")

t_all = time.time()
for m in SETS[MODELSET]:
    spec = MODELS[m]
    print(f"\n######## {m} (elapsed {(time.time()-t_all)/60:.0f} min)", flush=True)
    try:
        if spec.get("hf_snapshot"):
            from huggingface_hub import snapshot_download
            snapshot_download(spec["hf_snapshot"][0], local_dir=spec["hf_snapshot"][1])
        if spec["pre"]:
            sh(spec["pre"] + " 2>&1 | tail -1")
        out = f"/kaggle/working/runs/{m}"
        for variant, rot, split in SETTINGS:
            if (time.time() - t_all) / 3600 > MAX_HOURS:
                print("TIME GUARD: skipping remaining settings", flush=True)
                break
            env = dict(os.environ, BN_VARIANT=variant, BN_QLANG="en", BN_ROT=str(rot))
            t0 = time.time()
            groups = ((SMALL[variant], ""), (LARGE, f"--limit {LIMIT_LARGE}")) if split == "eval" else (("bn_sentnob bn_bnli bn_massive", f"--limit {DEV_LIMIT}"),)
            for tasks, lim in groups:
                sh(f"python scripts/run_system_one_model.py {tasks} --split {split} {lim} {spec['args']} --out {out}", env=env)
            print(f"== {m} {split} {variant} rot{rot}: {(time.time()-t0)/60:.1f} min; lines so far: "
                  f"{sum(1 for _ in open(out + '/responses.jsonl')) if os.path.exists(out + '/responses.jsonl') else 0}", flush=True)
    except Exception:
        traceback.print_exc()
print("ALL DONE", (time.time() - t_all) / 3600, "h")
