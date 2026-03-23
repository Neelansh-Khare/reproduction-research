# Experiment Log + Reproducibility Checklist

Use this checklist for every run you want to share or defend.

## 0. Identity

- [ ] Experiment name / run-name (e.g., `baseline_repro`)
- [ ] Config file path (e.g., `configs/baseline_repro.yaml`)
- [ ] Config overrides (if any)
- [ ] Output directory (e.g., `outputs/baseline_repro/<run_id>/`)

## 1. Environment

- [ ] Python version (e.g., `3.10.x+`)
- [ ] OS (e.g., macOS version)
- [ ] Dependency versions (from `requirements.txt` + lock if available)
- [ ] Confirm the run command used the same environment (virtualenv)

## 2. Determinism

- [ ] Set `seed` in config
- [ ] Confirm seed is saved into the run output (`config_used.yaml`)
- [ ] Ensure any randomized components (data ordering, negative sampling, model sampling) use the seed

## 3. Data and Prompt Controls

- [ ] Dataset file path and version (if the file changes, record it)
- [ ] Dataset limit/subset used
- [ ] Passage ordering policy is deterministic
- [ ] Support placement buckets are correctly mapped to passage indices
- [ ] Prompt builder version / code commit is recorded (file timestamps are a weak substitute; prefer commit hashes when available)

## 4. Evaluation

- [ ] Metric definitions used (exact normalization rules for EM and tokenization rules for token-F1)
- [ ] Ensure the evaluation loop uses the same gold labels as the dataset loader
- [ ] Predictions written per-example include: prediction, gold, EM, token-F1, and `support_position`

## 5. Outputs

- [ ] `metrics.json` exists in the run directory
- [ ] `predictions.jsonl` exists in the run directory
- [ ] The resolved config used by the run is saved (no “mental config”)

## 6. Results Interpretation

- [ ] Bucket-wise summaries reported (beginning / early-middle / late-middle / end)
- [ ] Identify failure patterns (e.g., empty extraction, distractor leakage)
- [ ] Record any deviations from the planned experimental recipe

