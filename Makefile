SHELL := /bin/zsh

.PHONY: setup test run-baseline

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

test:
	. .venv/bin/activate && pytest -q

run-baseline:
	. .venv/bin/activate && bash scripts/run_baseline_repro.sh

