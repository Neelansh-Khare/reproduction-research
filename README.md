# Lost-in-the-Middle Reproduction

This repository, `lost-in-the-middle-reproduction`, builds a clean, lightweight, reproducible evaluation environment to study the core claim from **“Lost in the Middle: How Language Models Use Long Contexts”**:

> For long contexts, model performance depends strongly on *where* the relevant evidence appears; information in the **middle** is often underused relative to beginning or end positions.

Instead of attempting full fidelity to every experimental detail in the original paper, this project provides a minimal framework that makes the *position sensitivity* mechanism easy to test and extend—especially with independent synthetic or templated long-context datasets.

## Setup

Requirements: Python `3.10+`.

1. Create an environment and install deps:
   - `make setup`
2. Run the small baseline reproduction experiment:
   - `make run-baseline`
3. Run smoke tests:
   - `make test`

## Baseline experiment

The included baseline uses:
- A small synthetic dataset (`data/sample_position_eval.jsonl`)
- A controlled prompt builder that assembles the full context with bucketed support positions
- Exact Match (EM) and token-level F1 metrics
- A deterministic “heuristic” local model (`model.type: heuristic`) so the environment is runnable without API keys

Outputs are written under `outputs/baseline_repro/`.

## Repo structure (high level)

- `src/`: minimal dataset, prompt builder, model interface, metrics, and evaluation pipeline
- `configs/`: YAML configs saved alongside every run
- `docs/`: reproduction planning notes, paper outline, claims, and an experiment log checklist
- `data/`: sample synthetic dataset(s)
- `outputs/`: per-run predictions + aggregate metrics
- `scripts/`: shell entrypoints for quick experiments

## Connection to RAG (independent work)

Long-context position sensitivity matters for retrieval-augmented generation (RAG) because retrieved passages are typically concatenated into a single prompt. If the most relevant evidence is placed in the middle of a long context (e.g., after several high-relevance but redundant passages), models may underweight it.

This reproduction baseline is designed to inform later RAG-focused work by:
- making “context placement” an explicit controlled variable
- enabling ablations that simulate retrieval saturation / context overload (more distractors, longer concatenations)
- motivating extensions that incorporate retrieval ranking and context-packing policies, where the same evidence can land in different positions across prompts

## Status

- **Baseline Reproduction:** Completed. The environment successfully reproduces the qualitative "lost-in-the-middle" curve using a heuristic baseline.
- **Redundancy Extension:** Completed. Verified that redundant information at the beginning rescues performance for middle-position evidence.
- **Noise Shift Extension:** Completed (Apr 26). Verified that the position-sensitivity mechanism scales correctly to longer context lengths (11 passages).

