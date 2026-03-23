# Deep Read Notes Template (Lost in the Middle)

Use this document while reading the paper. Fill it in section-by-section so you can later map each design choice to something you can reproduce.

## 1. Paper Metadata

- Title:
- Authors / year:
- Venue:
- TL;DR (1-3 sentences):

## 2. Central Hypothesis / Mechanism

What causal mechanism is the paper arguing for?

## 3. Experimental Manipulation (Context Positioning)

3.1 What is the “evidence” unit?
- e.g., a passage, phrase, or answer-bearing span

3.2 How is “position” defined?
- beginning / middle / end in terms of token counts or passage counts

3.3 How do they construct the full input?
- prompt structure
- separators / formatting
- truncation behavior (if any)

## 4. Task Details

- task type (retrieval-augmented? QA? synthetic?)
- any assumptions about the model’s access to the evidence

## 5. Models and Decoding

- model family and size:
- decoding (temperature, max tokens, etc.):
- any special prompting:

## 6. Evaluation Metrics

6.1 Exact Match
- normalization rules:
- edge cases:

6.2 Token-level F1
- tokenization rules:
- averaging strategy:

## 7. Results to Extract (Make a Checklist)

For each experiment, record:

- experiment id/name:
- context lengths used:
- position buckets used:
- EM curve shape (begin/mid/end):
- F1 curve shape:
- strongest reported effect:
- any subgroup analysis:

## 8. Ablations / Controls

What did they change to rule out confounds?

- formatting changes:
- evidence content changes:
- distractor number / similarity:
- model family changes:

## 9. Threats to Validity (Paper-Specific)

What might the reported effect depend on?

## 10. Reproduction Mapping

For each component, answer:

- Can I reproduce it exactly?
- If not, what is the closest independent approximation?
- What could bias the conclusions?

## 11. Extension Ideas (RAG + Context Placement)

- How would you adapt the manipulation to a retrieval pipeline?
- What would “position bucket” mean after retrieval + packing?
- What would you vary (retrieval quality, redundancy, packing policy)?

