"""Bengali tasks built from the frozen local splits in data/raw/ (see data/freeze_splits.py).

Belebele and SIB-200 need no new class: run the existing tasks with `--subsets ben_Beng ben_Latn`.
Question wording language is chosen with BN_QLANG (en|bn); script variant with BN_VARIANT (native|roman).
"""

import os
from functools import cached_property

from datasets import load_dataset

from jev_benchmarking.bn_text import rot_items, transform
from jev_benchmarking.config import ROOT
from jev_benchmarking.tasks.base import Primary, Task, choice, ex, mc_criteria, option_keys
from jev_benchmarking.tasks.classification import SIB200
from jev_benchmarking.tasks.multiple_choice import Belebele

QLANG = os.environ.get("BN_QLANG", "en")

# Option-label language ablation (BN_LABELS=bn): only the returned option *names* change; descriptions stay English.
# Bengali names written by the project author, to be verified by a native speaker.
LABELS_BN = {
    "neutral": "নিরপেক্ষ", "positive": "ইতিবাচক", "negative": "নেতিবাচক",
    "entailment": "অন্তর্ভুক্তি", "contradiction": "বিরোধিতা",
    "science/technology": "বিজ্ঞান/প্রযুক্তি", "travel": "ভ্রমণ", "politics": "রাজনীতি", "sports": "খেলাধুলা",
    "health": "স্বাস্থ্য", "entertainment": "বিনোদন", "geography": "ভূগোল",
}


# Alternative wording for the two NLI labels I am least sure about (sensitivity check): নিহিত = "implied", বিরোধ = "conflict".
LABELS_BN2 = {**LABELS_BN, "entailment": "নিহিত", "contradiction": "বিরোধ"}


def lk(label: str) -> str:
    mode = os.environ.get("BN_LABELS", "en")
    return {"bn": LABELS_BN, "bn2": LABELS_BN2}.get(mode, {}).get(label, label)
RAW = ROOT.parent / "data" / "raw"


class _Local(Task):
    hf_path = "local-json"  # frozen splits in data/raw (see data/freeze_splits.py); documented source per task in data/split_hashes.json
    jsonl = ""
    configs = ("bn",)
    splits = {"eval": "test", "dev": "dev"}  # dev = disjoint split for pilots; eval = frozen test

    def load_split(self, config, split):
        f = self.jsonl if split == "test" else self.jsonl.replace(".jsonl", "_dev.jsonl")
        return load_dataset("json", data_files=str(RAW / f), split="train")


class BnSentNoB(_Local):
    name = "bn_sentnob"
    jsonl = "sentnob.jsonl"
    primary = Primary("answer", "macro_f1")
    labels = ("neutral", "positive", "negative")  # SentNoB: 0/1/2
    description = "SentNoB noisy Bengali social-media sentiment, 3 classes (seeded 10% split)."

    def build(self, row, config):
        crit = {
            "neutral": "The comment expresses no clear positive or negative opinion.",
            "positive": "The comment expresses a positive opinion or feeling.",
            "negative": "The comment expresses a negative opinion or feeling, including abuse.",
        }
        if QLANG == "bn":
            q = choice("`comment` এর সামগ্রিক অনুভূতি কী?", dict(rot_items(list({
                "neutral": "মন্তব্যে স্পষ্ট ইতিবাচক বা নেতিবাচক মত নেই।",
                "positive": "মন্তব্যে ইতিবাচক মত বা অনুভূতি প্রকাশ পেয়েছে।",
                "negative": "মন্তব্যে নেতিবাচক মত বা অনুভূতি প্রকাশ পেয়েছে, গালিগালাজসহ।",
            }.items()))))
        else:
            if os.environ.get("BN_SENT_TEMPLATE") == "min":  # wording-sensitivity check: option names only, no descriptions
                crit = {k: None for k in crit}
            q = choice("What is the overall sentiment of `comment`?", {lk(k): v for k, v in rot_items(list(crit.items()))})
        return ex({"comment": transform(row["Data"].strip())}, {"answer": q}, {"answer": lk(self.labels[row["Label"]])})


class BnBNLI(_Local):
    name = "bn_bnli"
    jsonl = "bnli.jsonl"
    labels = ("contradiction", "entailment", "neutral")  # csebuetnlp/xnli_bn order, NOT the XNLI order
    description = "Bengali XNLI (machine-translated, csebuetnlp/xnli_bn), 3 classes."

    def build(self, row, config):
        if QLANG == "bn":
            q = choice("`premise` ও `hypothesis` এর মধ্যে সম্পর্ক কী?", dict(rot_items(list({
                "entailment": "`premise` সত্য হলে `hypothesis` অবশ্যই সত্য।",
                "neutral": "`premise` থেকে `hypothesis` সত্য না মিথ্যা বোঝা যায় না।",
                "contradiction": "`premise` সত্য হলে `hypothesis` অবশ্যই মিথ্যা।",
            }.items()))))
        else:
            q = choice("What is the relationship between `premise` and `hypothesis`?", {lk(k): v for k, v in rot_items(list({
                "entailment": "`hypothesis` is definitely true given `premise`.",
                "neutral": "`hypothesis` may or may not be true; `premise` does not settle it.",
                "contradiction": "`hypothesis` is definitely false given `premise`.",
            }.items()))})
        state = {"premise": transform(row["sentence1"]), "hypothesis": transform(row["sentence2"])}
        return ex(state, {"answer": q}, {"answer": lk(self.labels[row["label"]])})


class BnMASSIVE(_Local):
    name = "bn_massive"
    jsonl = "massive.jsonl"
    description = "MASSIVE bn-BD intent classification, 60 intents offered, 59 of them present in the test split (utterances are human translations)."

    @cached_property
    def intents(self):
        import json

        rows = [json.loads(l) for f in (self.jsonl, self.jsonl.replace(".jsonl", "_dev.jsonl")) for l in (RAW / f).open()]
        return tuple(sorted({r["label_text"] for r in rows}))

    def build(self, row, config):
        q = choice(
            "What does the user want the assistant to do with `utterance`?" if QLANG == "en"
            else "`utterance` এ ব্যবহারকারী সহকারীকে দিয়ে কী করাতে চান?",
            {i: None for i in rot_items(list(self.intents))},
        )
        return ex({"utterance": transform(row["text"].strip())}, {"answer": q}, {"answer": row["label_text"]})


class BnBelebele(Belebele):
    """Belebele restricted to Bengali script and its Latin-script variant (ben_Latn: annotators transliterated with IndicXlit support, so tool-assisted, not natural typing), with option rotation (letters stay A-D)."""

    name = "bn_belebele"
    configs = ("ben_Beng", "ben_Latn")

    def list_configs(self):
        return list(self.configs)

    def build(self, row, config):
        options = [row[f"mc_answer{i}"].strip() for i in range(1, 5)]
        gold_idx = int(row["correct_answer_num"]) - 1
        rotated = rot_items(list(enumerate(options)))  # keep original indices to remap gold
        q = choice("Which option correctly answers `question` according to `passage`?", mc_criteria([o for _, o in rotated]))
        gold = option_keys(4)[[i for i, _ in rotated].index(gold_idx)]
        return ex({"passage": row["flores_passage"], "question": row["question"]}, {"answer": q}, {"answer": gold})


class BnDakshina(_Local):
    """Bengali Wikipedia sentences that native speakers romanized by hand (Dakshina). No task labels exist, so every sentence carries a placeholder gold
    answer that must NOT be used for accuracy: the analysis measures agreement with the model's own answer on the Bengali-script sentence (analysis/dakshina.py)."""
    name = "bn_dakshina"
    jsonl = "dakshina_bn.jsonl"
    splits = {"eval": "test"}
    primary = Primary("answer", "accuracy")
    labels = SIB200.labels
    description = "Dakshina-bn sentences, 7-way topic question; unlabelled, used only for cross-script agreement."

    def build(self, row, config):
        q = choice("What is the topic of `text`?", {lk(l): None for l in rot_items(list(self.labels))})
        return ex({"text": transform(row["text"])}, {"answer": q}, {"answer": lk(row["category"])})


class BnSIB200(SIB200):
    name = "bn_sib200"
    configs = ("ben_Beng",)  # SIB-200 has no ben_Latn config

    def list_configs(self):
        return list(self.configs)

    def build(self, row, config):
        q = choice("What is the topic of `text`?", {lk(l): None for l in rot_items(list(self.labels))})
        return ex({"text": transform(row["text"])}, {"answer": q}, {"answer": lk(row["category"])})
