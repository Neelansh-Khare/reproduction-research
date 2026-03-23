# Weekly Update

## Week 1

- Established a minimal repository skeleton for a position-controlled reproduction study.
- Defined the discrete support-position buckets to use in independent experiments:
  - `beginning`, `early-middle`, `late-middle`, `end`
- Started the deep-read / extraction workflow (template + mapping plan) so each paper choice can be translated into a controllable baseline variable.

## Week 2 (baseline stability + reproducibility)

- Implemented (or will implement) an end-to-end baseline evaluation runner that:
  - sets deterministic seeds
  - assembles long-context prompts with controlled ordering
  - computes EM and token-level F1
  - saves per-example predictions and aggregate metrics
  - records the resolved config used for each run

## Connection to independent RAG work (position sensitivity at scale)

Long-context position sensitivity is a natural fit for RAG settings where:
- retrieved passages are concatenated in a fixed order
- “relevant evidence” may be displaced by redundant or high-ranked but less useful passages
- limited context windows force evidence packing/truncation decisions

This reproduction baseline provides a mechanism-level testbed for later RAG experiments on “retrieval saturation”:
- If the evidence bearing passage lands in middle prompt segments, models may underutilize it, even if it was retrieved and included.
- As the number of retrieved passages grows, context packing can increasingly place the most relevant evidence away from the beginning/end, potentially reducing downstream utility.

