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

## 8. Results Summary (tuned_repro - Apr 5)

- **Config:** `configs/tuned_repro.yaml`
- **Changes:** `read_beginning_n_passages: 2` (up from 1)
- **Overall EM:** 0.75
- **Overall F1:** 0.75
- **Shift observed:** Performance in the `early-middle` bucket shifted from 0.0 to 1.0 because the supporting passage at index 1 now falls within the model's "reading window".

## 9. Redundancy Shift Results Summary (Apr 12)

- **Config:** `configs/redundancy_repro.yaml`
- **Changes:** `use_redundancy: true`
- **Overall EM:** 1.00
- **Overall F1:** 1.00
- **Shift observed:** All buckets, including `early-middle` and `late-middle`, now achieve 1.0 EM. This replicates the paper's secondary finding that providing relevant information twice (specifically, adding a copy at the beginning) rescues performance even when the primary information is in the middle.

## 10. Position and Redundancy Shift Results Table

| Run ID | read_begin | read_end | Redundancy? | Overall EM | Beginning | Early-Middle | Late-Middle | End |
|---|---|---|---|---|---|---|---|---|
| baseline_repro | 1 | 1 | No | 0.50 | 1.0 | 0.0 | 0.0 | 1.0 |
| tuned_repro | 2 | 1 | No | 0.75 | 1.0 | 1.0 | 0.0 | 1.0 |
| redundancy_repro | 1 | 1 | Yes | 1.00 | 1.0 | 1.0 | 1.0 | 1.0 |
| noise_shift_repro | 1 | 1 | No | 0.50 | 1.0 | 0.0 | 0.0 | 1.0 |

## 11. Noise Shift Results Summary (Apr 19)

- **Config:** `configs/noise_shift_repro.yaml`
- **Changes:** `num_distractors: 10` (up from 4)
- **Overall EM:** 0.50
- **Overall F1:** 0.50
- **Shift observed:** While the overall EM remains at 0.50 (same as baseline), the "noise floor" has increased. The supporting passage at `early-middle` and `late-middle` is now pushed further into the context (indices 3 and 7, respectively, in an 11-passage block), confirming that the position-controlled assembly scales correctly with arbitrary noise levels. This setup allows for testing "retrieval saturation" where the model must find a needle in a much larger haystack.

## 12. Gap Analysis (Reproduction vs. Paper)

- **Mechanism Gap:** The original paper observes "lost in the middle" as a property of transformer attention and training data distribution. Our reproduction uses a **heuristic model** that hard-codes this behavior via a "reading window".
- **Quantitative Gap:** While we reproduce the *qualitative* U-shape (high performance at extremes, low in middle), our absolute numbers (0.0 vs 1.0) are more extreme than the paper's (where middle performance is often non-zero but degraded).
- **Hyperparameter Sensitivity:** Tuning `read_beginning_n_passages` directly controls the width of the "beginning" plateau. In real LLMs, this "window" is not a fixed number of passages but an emergent property of the context length and model capacity.
- **Conclusion:** The environment successfully validates the **context assembly and evaluation pipeline**. To close the gap, the next phase should replace the `heuristic` model with an actual LLM (e.g., via OpenAI or HuggingFace API) to see if the U-shape emerges naturally without being hard-coded.

