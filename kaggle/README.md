# Kaggle kernels

All open models ran on Kaggle (Tesla T4, 15 GB). Each kernel copies the code dataset `ipolas/bn-s1-code` to `/kaggle/tmp`, installs the model's dependencies and calls `harness/scripts/run_system_one_model.py` (or `run_open_model.py` for Gemma).

| Kernel | What it ran |
|---|---|
| `main_A`-`main_D`, `main_J` (`tools/run_models.py` template) | Laya-multilingual, Julia-1 and the d3 models on the five test sets (Bengali and rule-based romanization), rotations and development splits |
| `main_F` | d3-flash, 4-bit, on a test-set subset |
| `main_G` | Gemma-4-E4B-it on the test sets |
| `main_K` | Kev-0.8B and Kev-4B on the test sets (official `uv` setup, one server at a time) |
| `main_L` | laya-bangla v2 on the test sets, package-version drift check, SentNoB wording check |
| `main_M`, `main_M_*` | Dakshina agreement: `main_M` is the generic script (smoke test by default); `main_M_cl`, `_b`, `_gemma`, `_kev`, `_flash` ran the four spellings per system |
| `main_M2_*` | the natural-style spelling again, after its lookup was rebuilt without Dakshina sentences |

Each driver stops early if its data files are missing or the first condition writes nothing. Kernel logs and outputs are not stored here; the per-item results are in `../results/`.
