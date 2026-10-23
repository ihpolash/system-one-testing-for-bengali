# Reproduction. Targets that need an API key or a GPU say so; everything downstream of the stored results runs on a laptop.
#   make test      unit tests (harness + analysis)
#   make audit     recompute the headline numbers from the committed tables (runs from a fresh clone)
#   make tables    results CSVs -> paper/tables/*.tex and paper/numbers.tex     (needs the unpublished raw outputs, see README)
#   make figures   paper/figures/*.pdf                                          (same)
#   make paper     builds paper/main.pdf with tectonic
#   make data      re-freezes the dataset splits from Hugging Face (network; writes data/raw and data/split_hashes.json)
#   Not covered here: model inference. Jev needs TYPESAFE_API_KEY (analysis/human_roman_eval.py, runs/run_jev_*.sh);
#   open models ran on Kaggle GPUs (kaggle/ kernels, tools/run_models.py). Raw Jev responses are not redistributed.
PY ?= .venv/bin/python
.PHONY: all test data collect tables release figures paper audit
all: test collect tables release figures audit paper
test:
	cd harness && ../$(PY) -m pytest tests -q
	$(PY) -m pytest analysis/test_metrics.py -q
data:
	$(PY) data/freeze_splits.py
collect:
	$(PY) analysis/collect.py --all
	$(PY) analysis/human_models.py
tables: collect
	$(PY) analysis/make_tables.py
release: tables
	$(PY) analysis/make_release.py
figures: tables
	$(PY) analysis/make_figures.py
paper:
	cd paper && tectonic --keep-intermediates main.tex
audit:
	$(PY) analysis/audit_numbers.py
