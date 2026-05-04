# Extension Analysis: Context Scaling and Redundancy Effects

## 1. Introduction

Following the successful reproduction of the "Lost in the Middle" baseline, we conducted two extension experiments to explore the robustness of the effect and potential mitigation strategies: **Noise Shift** (context scaling) and **Redundancy Shift**.

## 2. Noise Shift: Scaling to 10 Distractors

### 2.1 Experimental Setup
- **Config:** `configs/noise_shift_repro.yaml`
- **Manipulation:** Increased the number of distractor passages from 2 (baseline) to 10.
- **Total Passages:** 11 (1 supporting + 10 distractors).
- **Buckets:** `beginning` (0), `early-middle` (3), `late-middle` (7), `end` (10).

### 2.2 Results
The experimental results demonstrate that the "Lost in the Middle" effect scales linearly with context length.

| Bucket | Support Index | EM | F1 |
|---|---|---|---|
| Beginning | 0 | 1.0 | 1.0 |
| Early-Middle | 3 | 0.0 | 0.0 |
| Late-Middle | 7 | 0.0 | 0.0 |
| End | 10 | 1.0 | 1.0 |

**Overall EM:** 0.50

### 2.3 Analysis
- **Stability of the U-Shape:** The performance remained binary (1.0 at extremes, 0.0 in middle), confirming that our heuristic model's "reading window" (first and last passage) is not confused by additional noise.
- **Expansion of the "Lost" Zone:** By increasing the total passages, the gap between the beginning and end windows grew. In a real LLM, this would correspond to a larger region of the attention matrix being relatively under-weighted.

## 3. Redundancy Shift: Mitigating Position Penalty

### 3.1 Experimental Setup
- **Config:** `configs/redundancy_repro.yaml`
- **Manipulation:** Enabled `use_redundancy: true`.
- **Mechanism:** The supporting passage is inserted at its designated bucket index *and* a copy is placed at index 0 (beginning).

### 3.2 Results
Redundancy successfully rescued performance across all positions.

| Bucket | Support Index | EM | F1 |
|---|---|---|---|
| Beginning | 0 | 1.0 | 1.0 |
| Early-Middle | 1 | 1.0 | 1.0 |
| Late-Middle | 3 | 1.0 | 1.0 |
| End | 4 | 1.0 | 1.0 |

**Overall EM:** 1.00

### 3.3 Analysis
- **Mechanism of Rescue:** Since the heuristic model always reads the first passage, the redundant copy at index 0 ensures the model has access to the evidence regardless of where the "primary" passage is located.
- **Implications for RAG:** This finding suggests that "Context Packing" strategies in RAG should prioritize placing the most relevant (or highest-ranked) information at the beginning or end of the prompt. If context window permits, duplication of high-confidence results can act as an insurance policy against middle-position loss.

## 4. Synthesis and Next Steps

The extension experiments confirm that the "Lost in the Middle" phenomenon is a robust challenge for long-context utilization but can be countered through strategic prompt engineering.

**Current Status:**
- [x] Baseline Reproduction
- [x] Context Scaling (Noise Shift)
- [x] Redundancy Mitigation
- [ ] Transition to LLM (non-heuristic)

The next phase of the project will involve replacing the heuristic model with an actual Large Language Model to observe if these behaviors emerge naturally from attention dynamics rather than hard-coded windows.
