# How to Use This Repo

This repo provides a minimal, runnable baseline for reproducing the “lost in the middle” *context-position sensitivity* idea using:
- a position-controlled synthetic dataset
- deterministic prompt/context assembly
- a pluggable model interface (heuristic baseline included)
- EM + token-level F1 evaluation

## Quick Start

1. Create a virtual environment + install dependencies
   - `make setup`

2. Run the small baseline reproduction experiment
   - `make run-baseline`

3. Run smoke tests (dataset + prompt assembly)
   - `make test`

## What Runs in the Baseline

The baseline is configured by `configs/baseline_repro.yaml` and executed by:
- `scripts/run_baseline_repro.sh`
- `python -m src.pipeline.run_eval --config configs/baseline_repro.yaml --run-name baseline_repro`

The runner:
1. loads JSONL examples from `data/sample_position_eval.jsonl`
2. builds a prompt with bucketed support placement (beginning / early-middle / late-middle / end)
3. generates predictions with the configured model (`model.type: heuristic`)
4. computes:
   - Exact Match (EM)
   - token-level F1
5. writes outputs to `outputs/baseline_repro/<run_dir>/`

## Repository Architecture

Key modules (top to bottom):
- `src/data/datasets.py`
  - Defines `PositionEvalExample`
  - Loads JSONL via `load_position_eval_jsonl(...)`
- `src/prompts/context_positioning.py`
  - `assemble_passages(...)`: orders supporting passage + distractors by bucket
  - `build_full_prompt(...)`: produces the final deterministic prompt string
- `src/models/model_interface.py`
  - `ModelInterface`: abstraction for later API/local models
  - `HeuristicContextAnswerModel`: baseline deterministic generator
  - `build_model_from_config(...)`: picks a model from YAML
- `src/eval/metrics.py`
  - `exact_match(...)`
  - `token_level_f1(...)`
  - `summarize_metrics(...)` (aggregate EM/F1)
- `src/pipeline/run_eval.py`
  - End-to-end evaluation loop
  - Saves `config_used.yaml`, `predictions.jsonl`, and `metrics.json`

## Configuration Reference (baseline)

Edit `configs/baseline_repro.yaml` to change:
- `seed`
- `dataset.path` and `dataset.limit`
- prompt settings:
  - `prompt.system_instruction`
  - `prompt.passage_format`
- model settings:
  - `model.type` (currently `heuristic`)
  - heuristic “reading window”:
    - `model.read_beginning_n_passages`
    - `model.read_end_n_passages`
- `eval.position_buckets` (used for reporting expectations)
- `output.base_dir`

## Outputs

For each run, the runner creates a directory under:
- `outputs/baseline_repro/`

Inside a run directory you should find:
- `config_used.yaml`: resolved config snapshot (for reproducibility)
- `predictions.jsonl`: one JSON record per example
- `metrics.json`: aggregate EM and token-level F1
- `run.log`: run-time logs

## Extending the Baseline

1. Replace/extend the model:
   - Add a new `ModelInterface` implementation in `src/models/model_interface.py`
   - Update `build_model_from_config(...)` and your YAML config
2. Add a new dataset:
   - Provide a JSONL file matching the schema in `PositionEvalExample`
   - Point `dataset.path` in YAML to it
3. Add more position buckets / context layouts:
   - Update `SupportPosition` and the insertion mapping in `src/prompts/context_positioning.py`
   - Add corresponding examples in your dataset

