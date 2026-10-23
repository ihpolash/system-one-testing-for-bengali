# System One decision models on Bengali

Code, result tables and hand-written Banglish for my preprint *Decision Models on Bengali: Accuracy, Calibration and Script Robustness with Hand-Written Romanization* (Ismail Hossain Polas, Jahangirnagar University, ismailhossainpolash@gmail.com).

I tested one hosted decision model (Jev), ten open decision models (the vLLM-SR d3 family, Laya, laya-bangla, Julia-1 and Kev) and a general-purpose baseline (Gemma) on five Bengali tasks, in Bengali script and in Latin letters, and compared tool-made romanization with Banglish I wrote by hand.

## Layout
- `paper/` LaTeX source, figures, generated tables and `numbers.tex`. `main.pdf` is built with `tectonic`.
- `analysis/` metrics, table and figure scripts. `analysis/tables/` holds the result tables the paper is generated from. `audit_numbers.py` recomputes the headline numbers independently of the table script.
- `harness/` my fork of [jev-benchmarking](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking) (MIT, Deußer et al.), with the Bengali tasks, the romanization variants and adapters for the open models.
- `docs/PROMPTS.md` the exact question structure sent for each task (dataset text replaced by placeholders). Regenerate with `analysis/dump_prompts.py`.
- `kaggle/` the kernel scripts that ran the open models on Kaggle GPUs.
- `data/banglish_human_release.csv` my corrected Bengali and hand-written Banglish for the MASSIVE and XNLI-bn sentences. SentNoB is CC-BY-ND, so its text and the Banglish of its sentences are not included. `data/freeze_splits.py` rebuilds the splits from the public datasets.

## What you can rerun
- `make test` runs the unit tests.
- Install `pip install -r requirements.txt` first. `make audit` recomputes the headline numbers from the committed tables and checks them against `paper/numbers.tex`. `make paper` compiles the PDF from the committed source. Both work from a fresh clone.
- `make collect tables figures` rebuild `analysis/tables/`, the LaTeX tables and the figures from the raw model outputs. Those outputs (`runs/`, the Jev response cache, the 288 MB item file) are not published: Jev's raw responses fall under the provider's terms, and the open-model outputs are large.
- Running the models again needs a TypeSafe API key for Jev (`TYPESAFE_API_KEY`) and a Kaggle GPU for the open ones (`kaggle/`).

## Licence
Code is MIT (`LICENSE`). The Banglish file is CC BY 4.0 and inherits the licences of the source datasets (MASSIVE CC BY 4.0; XNLI-bn CC BY-NC-SA).
