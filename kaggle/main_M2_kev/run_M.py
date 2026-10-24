"""Kaggle: Kev 1.0 (kev-0.8b, kev-4b; tag v1.0) on the Dakshina-bn cross-script agreement task, 1,500 sentences, served with the project's own code (official uv setup).
One server at a time on its own port; the whole process group is killed between models so that no leftover server holds GPU memory or answers for the next model."""
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
LIMIT = 1500
MODELS = ["kev-0.8b", "kev-4b"]
KEV_ENV = {"kev-0.8b": {}, "kev-4b": {"KEV_CUDA_GRAPHS": "0", "KEV_PREFIX_CACHE": "0"}}   # Kev-4B sits at the T4 memory limit; these change speed and memory only
sh(f"pip install -q -e {work}/harness requests 2>&1 | tail -2")
sh("pip install -q uv 2>&1 | tail -1")
sh("mkdir -p /kaggle/tmp && cd /kaggle/tmp && git clone -q https://github.com/jaredpalmer/kev.git && cd kev && git checkout -q 2ecafc49fe && uv sync --extra serve --python 3.13 2>&1 | tail -5", timeout=1500)
os.chdir(f"{work}/harness")
t_all = time.time()
for mi, m in enumerate(MODELS):
    port = 8009 + mi
    log = open(f"/kaggle/working/serve_{m}.log", "w")
    srv = subprocess.Popen(["uv", "run", "--extra", "serve", "python", "-m", "kev.serve", "--run", f"jaredpalmer/{m}@v1.0", "--port", str(port), "--device", "cuda"], stdout=log, stderr=subprocess.STDOUT,
                           cwd="/kaggle/tmp/kev", start_new_session=True, env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True", **KEV_ENV[m]})
    ok = False
    for _ in range(120):
        time.sleep(5)
        if srv.poll() is not None: break
        if "Application startup complete" in open(f"/kaggle/working/serve_{m}.log").read() and subprocess.run(f"curl -s -m 5 -o /dev/null localhost:{port}/", shell=True).returncode == 0:
            ok = True; break
    print(f"server {m}: up={ok}", flush=True)
    if not ok:
        print(open(f"/kaggle/working/serve_{m}.log").read()[-1500:], flush=True); os.killpg(srv.pid, signal.SIGKILL); continue
    A = f"--backend kev --model jaredpalmer/{m} --tag-suffix @v1.0 --kev-url http://127.0.0.1:{port}"
    out = f"/kaggle/working/runs/{m.replace('-', '_').replace('.', '')}_dak"
    for v in VARIANTS:
        t0 = time.time()
        sh(f"python scripts/run_system_one_model.py bn_dakshina --split eval --limit {LIMIT} {A} --out {out}", env=dict(os.environ, BN_VARIANT=v, BN_ROT="0", BN_QLANG="en"))
        n = sum(1 for f in Path(out).glob("responses.jsonl") for _ in open(f))
        print(f"== {m} {v}: {(time.time()-t0)/60:.1f} min; responses so far {n}", flush=True)
        if v == VARIANTS[0] and n == 0:
            print(f"{m}: no responses after the first condition; stopping this model", flush=True); break
    os.killpg(srv.pid, signal.SIGKILL); srv.wait(); time.sleep(10)
    sh("nvidia-smi --query-gpu=memory.used --format=csv")
print("ALL DONE", (time.time() - t_all) / 3600, "h")
