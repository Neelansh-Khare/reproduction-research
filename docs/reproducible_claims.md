# Reproducible Claims (Lost in the Middle)

This doc distinguishes between (a) what we can fully reproduce in a small independent setup, (b) what we can partially reproduce, and (c) what we defer due to compute/model constraints.

## Main Claims (high level)

1. **Position sensitivity in long contexts:** Model performance on long-context QA depends strongly on where the evidence-bearing information appears in the concatenated context.
2. **Middle underuse:** When relevant evidence is placed in middle positions, performance often drops relative to beginning/end placements.
3. **Interaction with context construction:** The position effect depends on the exact prompt/context formatting and on how evidence competes with distractors across the full context.

## Exact Claims I Can Test (baseline-friendly)

### Claim A: Bucketed position degradation
- **Statement:** For a fixed query and a fixed set of distractors, performance (EM and token-level F1) is systematically lower when the supporting passage is in **middle buckets** than when it is in **beginning** or **end** buckets.
- **Operational test:** In our synthetic dataset, evaluate across support-position buckets: `beginning`, `early-middle`, `late-middle`, `end`.

### Claim B: EM and F1 correlate
- **Statement:** The ordering of bucket performance (begin/end vs middle) should be broadly consistent for EM and token-level F1.
- **Operational test:** Compare bucket-wise average EM with bucket-wise average F1; flag if curves diverge sharply.

### Claim C: Robustness under distractor count (extension-ready)
- **Statement:** Increasing distractor count (longer contexts) increases the magnitude of the middle-position penalty.
- **Operational test:** Run the same prompt builder with more distractors and re-measure bucket deltas. (Implemented once dataset/runner supports variable distractors.)

## Assumptions (what makes a baseline possible)

1. **Synthetic evidence realism:** The “evidence-bearing passage” contains an answer span that is extractable or learnable from local context cues.
2. **Prompt controllability:** The prompt builder controls the ordering of passages deterministically so “position buckets” correspond to meaningfully different context layouts.
3. **Metric alignment:** Exact Match and token-level F1 capture enough of the QA behavior for synthetic tasks.

## Ambiguities (things the paper may not specify enough for exact replication)

1. **Exact prompt formatting:** separators, numbering style, whether each passage is prefaced with roles, and how the instruction is embedded.
2. **Truncation boundaries:** the paper’s effective context length behavior when model max tokens are reached.
3. **Model-specific quirks:** whether the effect changes across model architectures, sizes, and decoding strategies.
4. **Dataset construction details:** distractor similarity distribution and whether distractors can accidentally leak the answer.

## Deviations from Original Setup (this repo)

1. **Independent synthetic dataset:** We use templated synthetic contexts rather than the paper’s exact corpora/tasks.
2. **Heuristic baseline model:** The runnable baseline uses a deterministic local heuristic model to verify the environment and to produce a qualitative “lost-in-the-middle-like” curve without API keys.
3. **Bucket discretization:** We use discrete bucket labels mapped to insertion indices based on passage count (not the paper’s exact token-length bins).

## Reproduction Status Note

1. **Fully reproduced (in this repo baseline):**
   - Position-bucket-controlled context assembly
   - Correct computation and reporting of EM + token-level F1
2. **Partially reproduced:**
   - Qualitative tendency for middle buckets to underperform (using the heuristic baseline, not a learned LLM)
3. **Deferred due to compute/model constraints:**
   - Quantitative match to the paper’s reported EM/F1 magnitudes with the same model families and context lengths
   - Statistical significance testing across many random seeds and model variants

## Evaluation Plan (baseline)

1. Run `scripts/run_baseline_repro.sh`.
2. For each example:
   - record `support_position`, `prediction`, EM, and token-F1
3. Report:
   - average EM by bucket
   - average token-F1 by bucket
   - overall averages across all buckets

## Threats to Validity

1. **Synthetic-to-real gap:** Synthetic templating may over/understate true long-context behavior of LLMs.
2. **Heuristic-model artifact:** The heuristic’s behavior may not reflect actual LLM attention/recency mechanisms.
3. **Tokenizer/normalization mismatch:** Differences in normalization or tokenization can change EM/F1 behavior.
4. **Prompt effects:** Small changes to separators/instructions can change failure modes.

## Extension Ideas (connect to RAG + context placement)

1. **Retrieval saturation simulation:** Increase distractor count and make distractors progressively more similar to the question.
2. **Evidence packing policy:** Simulate packing constraints (e.g., limited total tokens) so evidence can land in different buckets after truncation/packing.
3. **RAG-aware position:** Model multiple retrieved passages and test where the top-ranked evidence ends up (beginning vs middle vs end).

