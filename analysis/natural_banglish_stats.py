"""Build word-level natural-Banglish statistics from nahidstaq/bangla-transliteration-data (natural social-media typing, 45k pairs)
and evaluate rule variants of our romanizer on HELD-OUT word types. Writes analysis/natural_banglish_lookup.json."""
import collections, json, random, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "harness"))
from datasets import load_dataset

HERE = Path(__file__).parent


def aligned_pairs():
    d = load_dataset("nahidstaq/bangla-transliteration-data")
    out = []
    for s in d:
        for x in d[s]:
            rt = [t.lower() for t in re.findall(r"[A-Za-z0-9']+", x["roman"])]
            bt = re.findall(r"[ঀ-৿]+|[A-Za-z0-9]+", x["bangla"])
            if rt and len(rt) == len(bt):
                out.append(list(zip(bt, rt)))
    return out


def counts(pairs):
    c = collections.defaultdict(collections.Counter)
    for p in pairs:
        for b, r in p:
            if re.fullmatch(r"[ঀ-৿]+", b):
                c[b][r] += 1
    return c


def main():
    random.seed(0)
    pairs = aligned_pairs(); random.shuffle(pairs)
    cut = int(len(pairs) * .8)
    train, held = counts(pairs[:cut]), counts(pairs[cut:])
    print("aligned sentences", len(pairs), "| word types train", len(train), "held-out", len(held))
    # coverage of held-out tokens by a lookup built on train (min count 2)
    look = {w: c.most_common(1)[0][0] for w, c in train.items() if sum(c.values()) >= 2}
    tot = sum(sum(c.values()) for c in held.values()); cov = sum(sum(c.values()) for w, c in held.items() if w in look)
    hit = sum(c.get(look[w], 0) for w, c in held.items() if w in look)
    print(f"lookup covers {cov/tot:.1%} of held-out tokens; dominant-form lookup matches the typed form on {hit/max(cov,1):.1%} of covered tokens")
    # full lookup (all data, min count 2) saved for the romanizer
    allc = counts(pairs)
    full = {w: c.most_common(1)[0][0] for w, c in allc.items() if sum(c.values()) >= 2}
    (HERE / "natural_banglish_lookup.json").write_text(json.dumps(full, ensure_ascii=False))
    print("saved lookup with", len(full), "word types")
    # held-out word types NOT in the lookup -> evaluates the rule fallback
    unseen = {w: c for w, c in held.items() if w not in look}
    json.dump({w: dict(c) for w, c in unseen.items()}, open(HERE / "_unseen.json", "w"), ensure_ascii=False)
    print("held-out word types unseen in train:", len(unseen), "tokens", sum(sum(c.values()) for c in unseen.values()))


if __name__ == "__main__":
    main()
