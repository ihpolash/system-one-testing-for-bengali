"""Kaggle round 3 (2026-10-21): (A) laya-bangla v2 (algolyzer/laya-bangla, a Bangla fine-tune of Laya-multilingual published 2026-10-18) on all test/dev settings;
(B) Laya-multilingual re-run under laya==0.4.11 on native rot0 to measure package-version drift against the earlier 0.4.3/0.4.6 runs;
(C) laya-bangla on the AI-generated Banglish items (7 conditions); (D) SentNoB wording sensitivity (minimal English options, Bengali wording) for both Laya models."""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-1500:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness 'laya==0.4.11' 2>&1 | tail -2")
sh("python -c \"import laya; print('laya', laya.__version__)\"")
os.chdir(f"{work}/harness")
ROWS, ROWS_ED, HUMAN = f"{work}/data/human_rows.json", f"{work}/data/human_rows_edited.json", f"{work}/data/banglish_human.csv"
LB = "--backend laya --model algolyzer/laya-bangla --revision v2 --tag-suffix @4c5eb48932 --max-len 4096"
LM = "--backend laya --model convaiinnovations/laya-multilingual --max-len 4096"
RUN = "python scripts/run_system_one_model.py {tasks} --split {split} {lim} {args} --out {out}"
ALL, SMALL_R, LARGE = "bn_sentnob bn_belebele bn_sib200", "bn_sentnob bn_sib200", "bn_bnli bn_massive"
t_all = time.time()

def run(tasks, split, lim, args, out, **env):
    e = dict(os.environ); e.update(BN_QLANG="en", BN_ROT="0"); e.update({k: str(v) for k, v in env.items()})  # explicit overrides win
    sh(RUN.format(tasks=tasks, split=split, lim=lim, args=args, out=out), env=e)
    n = sum(1 for f in Path(out).glob("responses.jsonl") for _ in open(f)) if Path(out).exists() else 0
    print(f"   -> {out}: {n} lines ({(time.time()-t_all)/60:.0f} min elapsed)", flush=True)
    return n

# (A) laya-bangla rotations 1 and 2 (rot0 test + dev finished in the first attempt; set DO_ROT0=1 to redo them)
out = "/kaggle/working/runs/laya_bangla"
if os.environ.get("DO_ROT0") == "1":
    run(ALL, "eval", "", LB, out, BN_VARIANT="native"); run(LARGE, "eval", "--limit 1500", LB, out, BN_VARIANT="native")
    run(SMALL_R, "eval", "", LB, out, BN_VARIANT="roman"); run(LARGE, "eval", "--limit 1500", LB, out, BN_VARIANT="roman")
    for v in ("native", "roman"):
        run("bn_sentnob bn_bnli bn_massive", "dev", "--limit 1500", LB, out, BN_VARIANT=v)
for rot in (1, 2):
    for v, tasks in (("native", ALL), ("roman", SMALL_R)):
        run(tasks, "eval", "", LB, out, BN_VARIANT=v, BN_ROT=rot); run(LARGE, "eval", "--limit 1500", LB, out, BN_VARIANT=v, BN_ROT=rot)

# (B) package-version drift: Laya-multilingual native rot0 under 0.4.11 (same request keys as the earlier runs)
out = "/kaggle/working/runs/laya_ml_v0411"
run(ALL, "eval", "", LM, out, BN_VARIANT="native"); run(LARGE, "eval", "--limit 1500", LM, out, BN_VARIANT="native")

# (C) AI-generated Banglish items, seven conditions
out = "/kaggle/working/runs/laya_bangla_human"
HT = "bn_sentnob bn_massive bn_bnli"
for v, rows in (("native", ROWS), ("roman", ROWS), ("roman_nat", ROWS), ("human", ROWS), ("native_edit", ROWS_ED), ("roman_edit", ROWS_ED), ("roman_nat_edit", ROWS_ED)):
    run(HT, "eval", "", LB, out, BN_VARIANT=v, BN_ROWS_JSON=rows, BN_HUMAN_CSV=HUMAN)

# (D) SentNoB wording sensitivity (test split, native text, rot0): minimal English options; Bengali wording
for name, args in (("laya_bangla", LB), ("laya_ml", LM)):
    run("bn_sentnob", "eval", "", args, f"/kaggle/working/runs/{name}_tmpl_min", BN_VARIANT="native", BN_SENT_TEMPLATE="min")
    run("bn_sentnob", "eval", "", args, f"/kaggle/working/runs/{name}_tmpl_bn", BN_VARIANT="native", BN_QLANG="bn")
print("ALL DONE", (time.time() - t_all) / 3600, "h")
