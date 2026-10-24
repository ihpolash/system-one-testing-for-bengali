"""Audit the SentNoB split used here (the test split of the Hugging Face mirror sadi2oo3q/SentNoB, frozen in data/raw/sentnob.jsonl).
Compares sizes with the SentNoB paper and the BanglaBERT (BLUB) benchmark, and flags test comments that also occur in the mirror's train or validation split
or earlier in the test split (exact match after whitespace normalisation). Writes results/sentnob_overlap_flags.csv (no text) and analysis/tables/sentnob_split_audit.json.
    python analysis/sentnob_overlap.py"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
base = "https://huggingface.co/datasets/sadi2oo3q/SentNoB/resolve/main/"
norm = lambda s: " ".join(str(s).split())
tr, va, te = (pd.read_csv(base + f"{n}.csv") for n in ("train", "validation", "test"))
for d in (tr, va, te):
    d["t"] = d.Data.map(norm)
frozen = [norm(json.loads(l)["Data"]) for l in open(ROOT / "data" / "raw" / "sentnob.jsonl", encoding="utf-8")]
assert frozen == list(te.t), "data/raw/sentnob.jsonl is not the mirror's test split"
flags = pd.DataFrame({"uid": [f"bn/{i}" for i in range(len(te))], "in_train": te.t.isin(set(tr.t)).astype(int), "in_validation": te.t.isin(set(va.t)).astype(int),
                      "repeated_in_test": te.t.duplicated(keep="first").astype(int)})
flags["overlap"] = (flags[["in_train", "in_validation", "repeated_in_test"]].sum(axis=1) > 0).astype(int)
flags.to_csv(ROOT / "results" / "sentnob_overlap_flags.csv", index=False)
audit = {"mirror_train": len(tr), "mirror_validation": len(va), "mirror_test": len(te), "mirror_total": len(tr) + len(va) + len(te),
         "paper_total": 15728, "blub_train": 12575, "blub_validation": 1567, "blub_test": 1567, "laya_bangla_card_test": 1564,
         "test_in_train": int(flags.in_train.sum()), "test_in_validation": int(flags.in_validation.sum()), "test_repeated": int(flags.repeated_in_test.sum()), "test_overlap_any": int(flags.overlap.sum())}
(ROOT / "analysis" / "tables" / "sentnob_split_audit.json").write_text(json.dumps(audit, indent=1))
print(json.dumps(audit))
