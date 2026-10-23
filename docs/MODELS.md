# Systems evaluated: identifiers and settings

All open models ran as deterministic forward passes on Kaggle (Tesla T4, 15 GB), one request at a time per item, with no sampling. Question structure: `docs/PROMPTS.md`. Request tags below are the keys under which responses are stored (`analysis/collect.py`).

| System | Identifier / revision | How it was run |
|---|---|---|
| Jev | `jev-1.13.0` (TypeSafe API) | hosted API, accessed Oct 2026; raw responses not released (provider terms) |
| d3-edge, d3-lite, d3-nano, d3-mini | `vllm-sr/d3-edge@18d61df786`, `d3-lite@a8d25a91ef`, `d3-nano@3aeb1c22a5`, `d3-mini@a475367de0` | `--backend vllmsr --max-len 4096` (`kaggle/tools/run_models.py`) |
| d3-flash | `vllm-sr/d3-flash@521525effa` | 4-bit NF4 (bitsandbytes), does not fit a T4 in BF16; hash-ordered subset of 400 items per task (`kaggle/main_F`) |
| Laya-multilingual | `convaiinnovations/laya-multilingual` (package `laya` 0.4.3; a 0.4.11 rerun gave identical answers on 6,563 requests) | `--backend laya --max-len 4096` |
| laya-bangla v2 | `algolyzer/laya-bangla@4c5eb48932` (revision `v2`) | `--backend laya --max-len 4096` (`kaggle/main_L`) |
| Julia-1 | `SupersonicLabs/Julia-1` | `--backend julia --max-len 4096`; cannot take more than 20 options, so no MASSIVE; option descriptions filled with label names |
| Kev-0.8B, Kev-4B | `jaredpalmer/kev-0.8b@v1.0`, `kev-4b@v1.0` (code `jaredpalmer/kev@2ecafc49fe`) | served with `kev.serve` in bf16 via `uv sync --extra serve` on Python 3.13, shipped temperature; for Kev-4B `KEV_CUDA_GRAPHS=0`, `KEV_PREFIX_CACHE=0` and `expandable_segments` to fit memory (`kaggle/main_K`) |
| Gemma-4-E4B-it | `google/gemma-4-E4B-it` (no revision pinned) | not a decision model: each option scored by the next-token probability of its label, normalised over the options (`harness/jev_benchmarking/openmodel/prompts.py`) |

Not run: Kev-9B, Kev-27B, d3-27B (do not fit the GPU), Microsoft-Decision-1 (API only).

Procedures (identical for all systems): splits and subsets `data/freeze_splits.py` (`data/split_hashes.json`); XNLI-bn and MASSIVE limited to the first 1,500 items in hash order; options rotated cyclically for rotations 1 and 2; temperature scaling and the confidence gate fitted on development splits of 1,500 items per task, never on test items (`analysis/metrics.py`).
