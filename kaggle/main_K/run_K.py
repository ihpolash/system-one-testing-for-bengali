"""Kaggle round 4 (2026-10-21): Kev 1.0 (jaredpalmer/kev-0.8b, kev-4b; tag v1.0) served with kev.serve and scored through the System One endpoint.
Per model: native and rule-based romanized test sets (rotation 0).
SMOKE=1 runs 12 items only and prints latency (always run it first)."""
import json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

os.makedirs("/kaggle/tmp/hf", exist_ok=True)
os.environ.update(USE_TF="0", USE_FLAX="0", TRANSFORMERS_NO_TF="1", HF_HOME="/kaggle/tmp/hf", HF_HUB_DISABLE_PROGRESS_BARS="1")
SMOKE = os.environ.get("SMOKE", "0") == "1"
MODELS = os.environ.get("KEV_MODELS", "kev-4b").split(",")   # kev-0.8b finished in an earlier run (runs/kev_08b*)

# Kev-4B in bf16 sits at the 14.5 GiB limit of a T4 (its card asks for ~16 GB free): without these it ran out of memory during CUDA-graph capture and then on long inputs.
# Graph replay and the prefix cache change speed and memory only, not the answers.
KEV_ENV = {"kev-0.8b": {}, "kev-4b": {"KEV_CUDA_GRAPHS": "0", "KEV_PREFIX_CACHE": "0"}}

def sh(cmd, timeout=None, env=None):
    print("$", cmd, flush=True)
    try:
        r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
        print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HTTP Request" not in l and "examples/s" not in l)[-2500:], flush=True)
        return r.returncode
    except subprocess.TimeoutExpired:
        print("TIMEOUT", flush=True); return -1

src = next(p for p in ("/kaggle/input/bn-s1-code", "/kaggle/input/datasets/ipolas/bn-s1-code") if os.path.isdir(p))
work = "/kaggle/tmp/proj"; shutil.copytree(src, work, dirs_exist_ok=True)
for f in ("sentnob", "bnli", "massive", "belebele", "sib200"):   # fail fast: a missing split makes a task silently write 0 responses
    assert os.path.getsize(f"{work}/data/raw/{f}.jsonl") > 1000, f"data/raw/{f}.jsonl missing from the dataset"
assert os.path.exists(f"{work}/analysis/natural_banglish_lookup.json")
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh(f"pip install -q -e {work}/harness requests 2>&1 | tail -2")
# Official Kev setup (README "Run It Locally"): uv, isolated Python 3.13 environment, `uv sync --extra serve`. Kaggle's own packages are never touched.
sh("pip install -q uv 2>&1 | tail -1")
sh("mkdir -p /kaggle/tmp && cd /kaggle/tmp && git clone -q https://github.com/jaredpalmer/kev.git && cd kev && git checkout -q 2ecafc49fe && uv sync --extra serve --python 3.13 2>&1 | tail -5", timeout=1500)
os.chdir(f"{work}/harness")
RUN = "python scripts/run_system_one_model.py {tasks} --split eval {lim} {args} --out {out}"
t_all = time.time()

def run(tasks, lim, args, out, **env):
    e = dict(os.environ); e.update(BN_QLANG="en", BN_ROT="0"); e.update({k: str(v) for k, v in env.items()})
    sh(RUN.format(tasks=tasks, lim=lim, args=args, out=out), env=e)
    n = sum(1 for f in Path(out).glob("responses.jsonl") for _ in open(f)) if Path(out).exists() else 0
    print(f"   -> {out}: {n} lines ({(time.time()-t_all)/60:.0f} min elapsed)", flush=True)

for mi, m in enumerate(MODELS):
    port = 8009 + mi   # a distinct port per model, so a leftover server can never answer for the next one
    log = open(f"/kaggle/working/serve_{m}.log", "w")
    srv = subprocess.Popen(["uv", "run", "--extra", "serve", "python", "-m", "kev.serve", "--run", f"jaredpalmer/{m}@v1.0", "--port", str(port), "--device", "cuda"], stdout=log, stderr=subprocess.STDOUT, cwd="/kaggle/tmp/kev", start_new_session=True, env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True", **KEV_ENV[m]})
    ok = False
    for _ in range(120):
        time.sleep(5)
        if srv.poll() is not None: break
        if "Application startup complete" in open(f"/kaggle/working/serve_{m}.log").read() and subprocess.run(f"curl -s -m 5 -o /dev/null localhost:{port}/", shell=True).returncode == 0:
            ok = True; break
    print(f"server {m}: up={ok}", flush=True); print(open(f"/kaggle/working/serve_{m}.log").read()[-1500:], flush=True)
    if not ok:
        os.killpg(srv.pid, signal.SIGKILL); continue
    A = f"--backend kev --model jaredpalmer/{m} --tag-suffix @v1.0 --kev-url http://127.0.0.1:{port}"
    out = f"/kaggle/working/runs/{m.replace('-', '_').replace('.', '')}"
    if SMOKE:
        t = time.time(); run("bn_sentnob bn_massive", "--limit 12", A, out + "_smoke", BN_VARIANT="native"); print(f"SMOKE {m}: {time.time()-t:.0f}s for ~24 items", flush=True)
    else:
        for v in ("native", "roman"):
            tasks_s = "bn_sentnob bn_belebele bn_sib200" if v == "native" else "bn_sentnob bn_sib200"
            run(tasks_s, "", A, out, BN_VARIANT=v); run("bn_bnli bn_massive", "--limit 1500", A, out, BN_VARIANT=v)
    os.killpg(srv.pid, signal.SIGKILL); srv.wait(); time.sleep(10)   # kill the whole process group (uv run spawns the python server)
    sh("nvidia-smi --query-gpu=memory.used --format=csv")
print("ALL DONE", (time.time() - t_all) / 3600, "h")
