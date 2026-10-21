"""Kaggle round 4 (2026-10-21): Kev 1.0 (jaredpalmer/kev-0.8b, kev-4b; tag v1.0) served with kev.serve and scored through the System One endpoint.
Per model: native and rule-based romanized test sets (rotation 0), then the author's 877 hand-written items in seven conditions.
SMOKE=1 runs 12 items only and prints latency (always run it first)."""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")
SMOKE = os.environ.get("SMOKE", "1") == "1"
MODELS = os.environ.get("KEV_MODELS", "kev-0.8b,kev-4b").split(",")

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-2500:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/working/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness requests 2>&1 | tail -2")
sh("cd /kaggle/working && git clone -q https://github.com/jaredpalmer/kev.git && cd kev && git checkout -q 2ecafc49fe && pip install -q -e '.[serve]' 2>&1 | tail -5")
os.chdir(f"{work}/harness")
ROWS, ROWS_ED, HUMAN = f"{work}/data/human_rows.json", f"{work}/data/human_rows_edited.json", f"{work}/data/banglish_human.csv"
RUN = "python scripts/run_system_one_model.py {tasks} --split eval {lim} {args} --out {out}"
t_all = time.time()

def run(tasks, lim, args, out, **env):
    e = dict(os.environ); e.update(BN_QLANG="en", BN_ROT="0"); e.update({k: str(v) for k, v in env.items()})
    sh(RUN.format(tasks=tasks, lim=lim, args=args, out=out), env=e)
    n = sum(1 for f in Path(out).glob("responses.jsonl") for _ in open(f)) if Path(out).exists() else 0
    print(f"   -> {out}: {n} lines ({(time.time()-t_all)/60:.0f} min elapsed)", flush=True)

for m in MODELS:
    port = 8009
    log = open(f"/kaggle/working/serve_{m}.log", "w")
    srv = subprocess.Popen([sys.executable, "-m", "kev.serve", "--run", f"jaredpalmer/{m}@v1.0", "--port", str(port), "--device", "cuda"], stdout=log, stderr=subprocess.STDOUT, cwd="/kaggle/working/kev")
    ok = False
    for _ in range(120):
        time.sleep(5)
        if srv.poll() is not None: break
        if subprocess.run(f"curl -s -m 5 localhost:{port}/health >/dev/null || curl -s -m 5 -o /dev/null localhost:{port}/", shell=True).returncode == 0:
            ok = True; break
    print(f"server {m}: up={ok}", flush=True); print(open(f"/kaggle/working/serve_{m}.log").read()[-1500:], flush=True)
    if not ok:
        srv.kill(); continue
    A = f"--backend kev --model jaredpalmer/{m} --tag-suffix @v1.0 --kev-url http://127.0.0.1:{port}"
    out = f"/kaggle/working/runs/{m.replace('-', '_').replace('.', '')}"
    if SMOKE:
        t = time.time(); run("bn_sentnob bn_massive", "--limit 12", A, out + "_smoke", BN_VARIANT="native"); print(f"SMOKE {m}: {time.time()-t:.0f}s for ~24 items", flush=True)
    else:
        for v in ("native", "roman"):
            tasks_s = "bn_sentnob bn_belebele bn_sib200" if v == "native" else "bn_sentnob bn_sib200"
            run(tasks_s, "", A, out, BN_VARIANT=v); run("bn_bnli bn_massive", "--limit 1500", A, out, BN_VARIANT=v)
        hout = out + "_human"
        for v, rows in (("native", ROWS), ("roman", ROWS), ("roman_nat", ROWS), ("human", ROWS), ("native_edit", ROWS_ED), ("roman_edit", ROWS_ED), ("roman_nat_edit", ROWS_ED)):
            run("bn_sentnob bn_massive bn_bnli", "", A, hout, BN_VARIANT=v, BN_ROWS_JSON=rows, BN_HUMAN_CSV=HUMAN)
    srv.kill(); time.sleep(5)
print("ALL DONE", (time.time() - t_all) / 3600, "h")
