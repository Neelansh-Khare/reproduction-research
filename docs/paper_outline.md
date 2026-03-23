# Paper Outline + Reproduction Map (Lost in the Middle)

## Central finding (one-paragraph summary)

The paper argues that in long-context settings, language models are not uniformly sensitive to the content of the prompt. Instead, performance on long-context question answering is highly dependent on *where* the relevant evidence appears within the concatenated context. In particular, evidence placed in middle positions is often underutilized, leading to worse accuracy than comparable evidence at beginning or end positions.

## Mechanism intuition to test

Position sensitivity can arise from attention dynamics, recency biases, and how the model’s internal representations weight different segments of the prompt. Even when the same set of passages is provided, re-ordering them can change which information is effectively retrieved by the model at generation time.

## What the reproduction baseline captures

Our baseline environment reproduces the controllable part of the mechanism:
- Context is an ordered concatenation of passages.
- We vary a single discrete variable: the bucket where the supporting passage is inserted.
- We evaluate with EM and token-level F1.

## What remains open for full fidelity replication

Exact quantitative curves in the original paper require matching:
- exact prompt formatting and separators
- model families/sizes and decoding parameters
- the paper’s original evidence/distractor construction and truncation behavior

## Evaluation plan (baseline)

1. Run the baseline:
   - `scripts/run_baseline_repro.sh`
2. For each example, record:
   - `support_position`
   - `prediction`
   - EM and token-level F1
3. Aggregate:
   - bucket-wise average EM
   - bucket-wise average token-level F1
   - overall averages

## Threats to validity (independent-research version)

1. **Synthetic task mismatch:** The synthetic format may not induce the same failure modes as the paper’s benchmarks.
2. **Heuristic model gap:** The runnable baseline model is deterministic and does not reflect true LLM behavior; it validates the pipeline and helps debug the experimental manipulation.
3. **Normalization/tokenization drift:** Minor text normalization choices can change EM/F1 even if reasoning is qualitatively correct.
4. **Context-length effects:** Middle underuse may depend on total context length and prompt formatting; changing separators can shift results.

## Extension ideas (especially for RAG)

This project connects directly to retrieval-augmented generation (RAG):
- In RAG, relevant evidence often arrives as retrieved passages that are concatenated into a single context.
- If the most relevant passage ends up in the middle—after several high-scoring but redundant passages—models may underweight it.
- If context packing policies change which evidence lands near the beginning or end, the same underlying evidence set can yield different outcomes.

Concrete extensions to implement later:
- Vary retrieval ranking quality (swap ranked passages) and re-measure bucket effects.
- Simulate context overload: more distractors + truncation/prompt packing, then track where supporting evidence ends up.
- Measure “retrieval saturation” by progressively increasing the number of retrieved passages while controlling the position of the top-evidence passage.

