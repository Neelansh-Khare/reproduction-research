# Weekly Update

## Week 1

- Established a minimal repository skeleton for a position-controlled reproduction study.
- Defined the discrete support-position buckets to use in independent experiments:
  - `beginning`, `early-middle`, `late-middle`, `end`
- Started the deep-read / extraction workflow (template + mapping plan) so each paper choice can be translated into a controllable baseline variable.

## Week 2 (baseline stability + reproducibility)

- Implemented an end-to-end baseline evaluation runner that:
  - sets deterministic seeds
  - assembles long-context prompts with controlled ordering
  - computes EM and token-level F1
  - saves per-example predictions and aggregate metrics
  - records the resolved config used for each run
- **Completed Baseline Reproduction (`baseline_repro`):**
  - Confirmed the qualitative "Lost in the Middle" U-shaped performance curve using a heuristic model.
  - Achieved 100% EM for `beginning`/`end` positions and 0% EM for `middle` positions, validating the position-controlled assembly logic.
  - Successfully mapped the reproduction environment to the paper's core claims (see `docs/reproducible_claims.md`).
- **Completed Redundancy Shift Study (`redundancy_repro` - Apr 12):**
  - Replicated the paper's secondary finding regarding redundant information.
  - Demonstrated that placing a copy of the supporting passage at the beginning (index 0) "rescues" performance for examples where the primary evidence is in the middle.
  - Achieved 100% EM across all buckets using the redundancy mechanism.

## Connection to independent RAG work (position sensitivity at scale)

Long-context position sensitivity is a natural fit for RAG settings where:
- retrieved passages are concatenated in a fixed order
- “relevant evidence” may be displaced by redundant or high-ranked but less useful passages
- limited context windows force evidence packing/truncation decisions

This reproduction baseline provides a mechanism-level testbed for later RAG experiments on “retrieval saturation”:
- If the evidence bearing passage lands in middle prompt segments, models may underutilize it, even if it was retrieved and included.
- As the number of retrieved passages grows, context packing can increasingly place the most relevant evidence away from the beginning/end, potentially reducing downstream utility.

