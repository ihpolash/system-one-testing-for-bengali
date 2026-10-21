"""Download the five core Bengali datasets, freeze test splits, record sha256 hashes.

Raw data goes to data/raw/ (gitignored, not redistributed). Hashes go to data/split_hashes.json.
SentNoB has no published test split on the HF mirror, so we make a seeded 10% split (seed 42).
"""
import hashlib, json
from pathlib import Path
from datasets import load_dataset

ROOT = Path(__file__).parent
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(name, ds, meta):
    p = RAW / f"{name}.jsonl"
    ds.to_json(str(p), force_ascii=False)
    return {"file": p.name, "n": len(ds), "sha256": sha(p), **meta}

out = {}
b = load_dataset("facebook/belebele", "ben_Beng")["test"]
out["belebele"] = save("belebele", b, {"source": "facebook/belebele ben_Beng test"})
s = load_dataset("Davlan/sib200", "ben_Beng")["test"]
out["sib200"] = save("sib200", s, {"source": "Davlan/sib200 ben_Beng test"})
m = load_dataset("SetFit/amazon_massive_intent_bn-BD")["test"]
out["massive"] = save("massive", m, {"source": "SetFit/amazon_massive_intent_bn-BD test (mirror of MASSIVE bn-BD)"})
n = load_dataset("csebuetnlp/xnli_bn", revision="refs/convert/parquet")["test"]
out["bnli"] = save("bnli", n, {"source": "csebuetnlp/xnli_bn test (parquet conversion)"})
sno = load_dataset("sadi2oo3q/SentNoB")  # 12,575 / 1,567 / 1,586; train and val sizes match the BLUB table (BanglaBERT)
out["sentnob"] = save("sentnob", sno["test"], {"source": "sadi2oo3q/SentNoB test (third-party mirror of the original split; provenance unverified; BLUB table lists 1,567 test, mirror has 1,586)"})

# Dev splits for prompt/question-language pilots (never overlap the test splits above).
out["sentnob_dev"] = save("sentnob_dev", sno["validation"], {"source": "sadi2oo3q/SentNoB validation (1,567), used for pilots and temperature scaling"})
out["bnli_dev"] = save("bnli_dev", load_dataset("csebuetnlp/xnli_bn", revision="refs/convert/parquet")["validation"], {"source": "csebuetnlp/xnli_bn validation"})
out["massive_dev"] = save("massive_dev", load_dataset("SetFit/amazon_massive_intent_bn-BD")["validation"], {"source": "SetFit massive bn-BD validation"})

(ROOT / "split_hashes.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
for k, v in out.items():
    print(k, v["n"], v["sha256"][:12])
