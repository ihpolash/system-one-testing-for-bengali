# Reproduction. Targets that need an API key or a GPU say so; everything downstream of the stored results runs on a laptop.
#   make test      unit tests (harness + analysis)
#   make tables    results CSVs -> paper/tables/*.tex and paper/numbers.tex     (needs runs/ and harness/cache/, see README)
#   make figures   paper/figures/*.pdf
#   make paper     builds paper/main.pdf with tectonic
#   make data      re-freezes the dataset splits from Hugging Face (network; writes data/raw and data/split_hashes.json)
#   Not covered here: model inference. Jev needs TYPESAFE_API_KEY (analysis/human_roman_eval.py, runs/run_jev_*.sh);
#   open models ran on Kaggle GPUs (kaggle/ kernels, tools/run_models.py). Raw Jev responses are not redistributed.
PY ?= .venv/bin/python
.PHONY: all test data collect tables figures paper
all: test collect tables figures paper
test:
	cd harness && ../$(PY) -m pytest tests -q
	$(PY) -m pytest analysis/test_metrics.py -q
data:
	$(PY) data/freeze_splits.py
collect:
	$(PY) analysis/collect.py
	$(PY) analysis/human_models.py
tables: collect
	$(PY) analysis/make_tables.py
figures: tables
	$(PY) analysis/make_figures.py
paper: tables figures
	cd paper && tectonic --keep-intermediates main.tex
