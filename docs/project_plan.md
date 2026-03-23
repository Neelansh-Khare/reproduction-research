## Week 1 (Foundation + Paper Deconstruction)

1. Read and extract the paper’s experimental recipe
   - Prompt construction, context packing, position manipulation
   - Evaluation metrics and exact experimental comparisons
2. Define the minimal “position sensitivity” abstraction for reproduction
   - Context = ordered concatenation of passages
   - Variable = index bucket where the evidence-bearing passage appears
3. Implement the synthetic dataset schema and a tiny generator dataset
   - `query`, `answer`, `supporting_passage`, `distractor_passages`, `support_position`
4. Write smoke tests for dataset loading and context assembly
   - Ensure the supporting passage is placed in the expected bucket
5. Draft the evaluation loop and metrics interface
   - Exact Match (EM), token-level F1

## Week 2 (Baseline Runner + Reproducibility Hardening)

1. Implement `run_eval.py` to run the full pipeline end-to-end
   - Load YAML config, set deterministic seeds, evaluate, write outputs
2. Add configuration + run recording
   - Save the resolved config and run metadata with every run
3. Create a baseline script and config
   - `configs/baseline_repro.yaml`
   - `scripts/run_baseline_repro.sh`
4. Add threat-to-validity and “what we can/can’t reproduce” documentation
   - Update `docs/reproducible_claims.md` and `docs/experiment_log.md`
5. Smoke-test baseline end-to-end
   - Run baseline + confirm outputs and metrics files exist

