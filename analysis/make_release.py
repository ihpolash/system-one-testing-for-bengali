"""Build the shareable result files and their checksums.   python analysis/make_release.py
 results/predictions_test_sets.csv.gz  item-level predictions of every system (labels only, except that Belebele option labels are the Bengali option texts, CC BY-SA 4.0; for Jev only the top choice and its confidence, since raw outputs fall under the provider's terms)
 results/MANIFEST.sha256                 SHA-256 of every released result/data file, so a reader can check they hold the files the paper was built from"""
import hashlib, json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"; OUT.mkdir(exist_ok=True)
cols = ["model", "task", "split", "variant", "rot", "uid", "subset", "cluster", "gold_id", "pred_id", "pmax", "probs", "correct"]
chunks = []
for ch in pd.read_csv(ROOT / "analysis" / "items.csv", usecols=cols, chunksize=200000):
    ch = ch.copy(); ch["probs"] = [("" if m.startswith("jev") else x) for m, x in zip(ch.model, ch.probs)]   # Jev: top choice and confidence only (provider terms)
    chunks.append(ch)
df = pd.concat(chunks)
df["probs"] = df.probs.map(lambda x: "" if not isinstance(x, str) or not x else json.dumps({k: round(v, 4) for k, v in json.loads(x).items()}, ensure_ascii=False, separators=(",", ":")))
df["pmax"] = df.pmax.round(4)   # 4 decimals, no whitespace
df.to_csv(OUT / "predictions_test_sets.csv.gz", index=False, compression={"method": "gzip", "compresslevel": 9, "mtime": 0})
print(len(df), "rows;", df.model.nunique(), "models;", round((OUT / "predictions_test_sets.csv.gz").stat().st_size / 1e6, 1), "MB")
# Dakshina cross-script agreement: per-sentence top choice and probabilities for the open models; for Jev only the top choice and its confidence (provider terms: no probability vectors)
dk = pd.read_csv(ROOT / "analysis" / "dak_items.csv")
dk["conf"] = dk.probs.map(lambda x: round(max(json.loads(x).values()), 4))
dk["probs"] = [("" if m.startswith("jev") else json.dumps({k: round(v, 4) for k, v in json.loads(x).items()}, separators=(",", ":"))) for m, x in zip(dk.model, dk.probs)]
dk[["model", "variant", "id", "choice", "conf", "probs"]].to_csv(OUT / "predictions_dakshina.csv.gz", index=False, compression={"method": "gzip", "compresslevel": 9, "mtime": 0})
print(len(dk), "Dakshina rows;", round((OUT / "predictions_dakshina.csv.gz").stat().st_size / 1e6, 1), "MB")
files = sorted([*OUT.glob("*.csv.gz"), *(ROOT / "analysis" / "tables").glob("*.csv"), ROOT / "data" / "split_hashes.json", *(ROOT / "paper" / "tables").glob("*.tex"), ROOT / "paper" / "numbers.tex"])
(OUT / "MANIFEST.sha256").write_text("".join(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(ROOT)}\n" for f in files))
print(len(files), "files in manifest")
