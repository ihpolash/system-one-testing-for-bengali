# System One decision models on Bengali

Code, result tables and hand-written Banglish for the preprint *Accuracy, Calibration and Script Robustness of Decision Models on Bengali: A Zero-Shot Benchmark with Hand-Written Romanization* (Ismail Hossain Polas, Jahangirnagar University).

- `harness/` fork of [jev-benchmarking](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking) (MIT, Deußer et al.) with Bengali tasks, romanization variants and adapters for the open models.
- `analysis/` metrics, tables and figures (`make_tables.py`, `make_figures.py`); `analysis/tables/` holds the result tables the paper is generated from.
- `paper/` LaTeX source, generated tables, figures and `numbers.tex`.
- `data/banglish_human_release.csv` the author's corrected Bengali and hand-written Banglish for the MASSIVE and XNLI-bn sentences. SentNoB (CC-BY-ND) text and its Banglish are not included; `data/freeze_splits.py` rebuilds the splits from the public datasets.
- `Makefile` targets: `test`, `data`, `tables`, `figures`, `paper`. Model inference is not included: Jev needs an API key (`TYPESAFE_API_KEY`), and the open models were run on Kaggle GPUs. Raw Jev responses and item-level predictions are not redistributed.

Code is MIT-licensed (see `LICENSE`). The Banglish file is CC BY 4.0 and inherits the licences of the source datasets (MASSIVE CC BY 4.0; XNLI-bn CC BY-NC-SA).
