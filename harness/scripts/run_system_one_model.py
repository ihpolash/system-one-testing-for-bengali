"""Score tasks with a System One decision model (Kev / Julia-1 / Laya) -> Jev-format JSONL (resumable).

Runs on a GPU node (Kaggle). Same output as run_open_model.py, so import_responses.py and evaluate.py work unchanged:
    python scripts/run_system_one_model.py bn_sentnob bn_bnli --backend laya --model convaiinnovations/laya-multilingual \
        --subfolder multilingual --split eval --out runs/laya_ml
    python scripts/run_system_one_model.py bn_belebele --backend kev --model jaredpalmer/kev-4b --kev-url http://127.0.0.1:8009
    python scripts/run_system_one_model.py bn_bnli --backend vllmsr --model vllm-sr/d3-nano --tag-suffix @3aeb1c22a5
    python scripts/run_system_one_model.py all --backend julia --model SupersonicLabs/Julia-1 --julia-path /path/to/Julia-1

Option rotation, script variant and question language come from BN_ROT / BN_VARIANT / BN_QLANG (see bn_text.py); the
request key includes them, so each setting is cached separately.
"""

import argparse
import json
import os
import logging
import platform
import time
from pathlib import Path

from jev_benchmarking.cache import request_key
from jev_benchmarking.openmodel.runner import done_keys, model_tag
from jev_benchmarking.tasks import get_tasks

log = logging.getLogger(__name__)


def confidence(probs: list[float]) -> float:
    k = len(probs)
    return 1.0 if k < 2 else max(0.0, (max(probs) - 1 / k) / (1 - 1 / k))


def make_predict(args):
    """Return predict(state, questions) -> {"answers": {...}}, plus library versions for the run metadata."""
    if args.backend == "kev":
        import requests

        def predict(state, questions):
            r = requests.post(f"{args.kev_url}/v1/systemone", json={"state": state, "model": "kev-latest", "questions": questions}, timeout=300)
            r.raise_for_status()
            return r.json()

        return predict, {"kev_url": args.kev_url}
    if args.backend == "laya":
        import laya

        kw = {"subfolder": args.subfolder} if args.subfolder else {}
        if args.revision:
            kw["revision"] = args.revision
        agent = laya.load(args.model, **kw)
        return (lambda state, questions: agent.predict(state, questions, max_len=args.max_len)), {"laya": getattr(laya, "__version__", "?")}
    if args.backend == "julia":
        import sys

        sys.path.insert(0, args.julia_path)
        from julia import load_model

        engine = load_model(args.julia_path, device=args.device, strict_encoding=True, max_length=args.max_len, head_length=512)
        def fill(questions):
            """Julia-1 requires non-empty option descriptions; labels without one (SIB-200, MASSIVE) get their own name."""
            q = json.loads(json.dumps(questions))
            for v in q.values():
                if isinstance(v.get("criteria"), dict):
                    v["criteria"] = {k: (d if d else k) for k, d in v["criteria"].items()}
            return q

        return (lambda state, questions: engine.predict(state=state, questions=fill(questions))), {"julia_path": args.julia_path, "note": "empty option descriptions replaced by the label name"}
    if args.backend == "vllmsr":  # vllm-sr Decision 2.0 / d3 (Decision 3.0): transformers remote code, needs transformers>=5.17
        import torch
        import transformers
        from transformers import AutoModel

        if args.d3_bnb:  # 4-bit/8-bit weight quantization of the d3 backbone (deviation from the checkpoint's BF16 numerics; report it)
            import transformers
            from transformers import BitsAndBytesConfig

            qcfg = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16) if args.d3_bnb == 4 \
                else BitsAndBytesConfig(load_in_8bit=True)
            orig = transformers.PreTrainedModel.from_pretrained.__func__

            def patched(cls, *a, **k):
                if k.get("device_map") and "quantization_config" not in k and str(k.get("dtype")) == "torch.bfloat16":
                    if os.environ.get("D3_BNB_DRYRUN"):  # local test: show the hook fired, do not quantize
                        print("PATCH HIT:", cls.__name__, sorted(k), flush=True)
                    else:
                        k["quantization_config"] = qcfg
                        print(f"PATCH HIT: quantizing {cls.__name__} to {args.d3_bnb}-bit", flush=True)
                return orig(cls, *a, **k)

            transformers.PreTrainedModel.from_pretrained = classmethod(patched)
        rev = args.tag_suffix.lstrip("@") or None
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"  # d3 takes a device name, never a torch dtype (see modeling_d3.py)
        model = AutoModel.from_pretrained(args.model, revision=rev, trust_remote_code=True, device=dev)
        model.eval()
        return (lambda state, questions: model.system_one(state=state, questions=questions)), {"transformers": transformers.__version__}
    raise SystemExit(f"unknown backend {args.backend}")


def normalise(answers: dict, questions: dict) -> dict:
    """Make every answer carry the fields evaluate.py reads; fail loudly rather than guess a missing probability."""
    out = {}
    for qid, a in answers.items():
        a = dict(a)
        if a["type"] in ("choice", "score"):
            if "probabilities" not in a:
                raise KeyError(f"{qid}: model returned no probabilities: {a}")
            if "confidence" not in a:
                a["confidence"] = confidence(list(a["probabilities"].values()))
        out[qid] = a
    missing = set(questions) - set(out)
    if missing:
        raise KeyError(f"model omitted answers for {sorted(missing)}")
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tasks", nargs="+")
    p.add_argument("--backend", required=True, choices=["kev", "laya", "julia", "vllmsr"])
    p.add_argument("--model", required=True, help="HF id; becomes the cache tag hf:<id>")
    p.add_argument("--tag-suffix", default="", help="e.g. @<commit> to pin a revision in the cache tag")
    p.add_argument("--split", choices=["eval", "dev"], default="eval")
    p.add_argument("--limit", type=int)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--subfolder")
    p.add_argument("--kev-url", default="http://127.0.0.1:8009")
    p.add_argument("--julia-path")
    p.add_argument("--device", default="cuda")
    p.add_argument("--max-len", type=int, default=1024)
    p.add_argument("--revision", help="Hub revision (tag or commit) for the laya backend, e.g. v2")
    p.add_argument("--d3-bnb", type=int, choices=[4, 8], default=0, help="quantize the d3 backbone with bitsandbytes (4 or 8 bit)")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")

    predict, versions = make_predict(args)
    tag = model_tag(args.model) + args.tag_suffix
    args.out.mkdir(parents=True, exist_ok=True)
    skip = done_keys(args.out)
    meta = {"tag": tag, "backend": args.backend, "d3_bnb": args.d3_bnb, "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "python": platform.python_version(), **versions}
    try:
        import torch

        meta["torch"] = torch.__version__
        meta["gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
    except ImportError:
        pass
    (args.out / "meta.json").write_text(json.dumps(meta, indent=1))

    written = nfail = 0
    with (args.out / "responses.jsonl").open("a") as out, (args.out / "failures.jsonl").open("a") as fails:
        for task in get_tasks(args.tasks):
            if task.splits.get(args.split) is None:
                continue
            seen = set(skip)
            for e in task.examples(args.split, limit=args.limit):
                key = request_key(tag, e.state, e.questions)
                if key in seen:
                    continue
                seen.add(key)
                t0 = time.monotonic()
                try:
                    if args.backend == "julia" and any(len(q.get("criteria") or {}) > 20 for q in e.questions.values()):
                        raise ValueError("unsupported: more than 20 options (Julia-1 contract is 2-20)")
                    res = predict(e.state, e.questions)
                except (ValueError, KeyError) as err:  # model input contract violated: record, report coverage, never guess an answer
                    fails.write(json.dumps({"key": key, "task": task.name, "uid": e.uid, "error": str(err)[:200]}) + "\n")
                    nfail += 1
                    continue
                dt = time.monotonic() - t0
                out.write(json.dumps({
                    "key": key, "task": task.name, "uid": e.uid, "latency_s": dt,
                    "response": {"model": tag, "answers": normalise(res["answers"], e.questions),
                                 "usage": res.get("usage", {"input_tokens": 0, "output_tokens": 0}), "diagnostics": {}},
                }, ensure_ascii=False) + "\n")
                written += 1
                if written % 200 == 0:
                    out.flush()
                    log.info("%s: %d written", task.name, written)
            out.flush()
    print(f"wrote {written} responses to {args.out}; {nfail} unsupported/failed items (see failures.jsonl)")


if __name__ == "__main__":
    main()
