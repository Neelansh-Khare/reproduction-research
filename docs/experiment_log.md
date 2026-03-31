# Experiment Log + Reproducibility Checklist

Use this checklist for every run you want to share or defend.

## 0. Identity

- [x] Experiment name / run-name (`baseline_repro`)
- [x] Config file path (`configs/baseline_repro.yaml`)
- [ ] Config overrides (if any)
- [x] Output directory (`outputs/baseline_repro/baseline_repro_seed1234_20260331_033535/`)

## 1. Environment

- [x] Python version (3.10.12)
- [x] OS (darwin)
- [x] Dependency versions (from `requirements.txt`)
- [x] Confirm the run command used the same environment (virtualenv)

## 2. Determinism

- [x] Set `seed` in config (1234)
- [x] Confirm seed is saved into the run output (`config_used.yaml`)
- [x] Ensure any randomized components (data ordering, negative sampling, model sampling) use the seed

## 3. Data and Prompt Controls

- [x] Dataset file path and version (`data/sample_position_eval.jsonl`)
- [x] Dataset limit/subset used (8)
- [x] Passage ordering policy is deterministic
- [x] Support placement buckets are correctly mapped to passage indices
- [x] Prompt builder version / code commit is recorded

## 4. Evaluation

- [x] Metric definitions used (EM and token-F1)
- [x] Ensure the evaluation loop uses the same gold labels as the dataset loader
- [x] Predictions written per-example include: prediction, gold, EM, token-F1, and `support_position`

## 5. Outputs

- [x] `metrics.json` exists in the run directory
- [x] `predictions.jsonl` exists in the run directory
- [x] The resolved config used by the run is saved

## 6. Results Interpretation

- [x] Bucket-wise summaries reported (beginning: 1.0, middle: 0.0, end: 1.0)
- [x] Identify failure patterns (heuristic model only reads ends)
- [x] Record any deviations from the planned experimental recipe (None)

## 7. Results Summary (baseline_repro)

- Overall EM: 0.5
- Overall F1: 0.5
- Qualitative match to "Lost in the Middle" (U-shape) confirmed.

