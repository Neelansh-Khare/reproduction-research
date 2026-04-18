from __future__ import annotations

from typing import Tuple

from src.data.datasets import PositionEvalExample, SupportPosition


def get_support_insertion_index(num_passages: int, position: SupportPosition) -> int:
    """
    Map a discrete support-position bucket to an insertion index.

    For baseline settings (1 supporting + 4 distractors => 5 total), this yields:
      - beginning: 0
      - early-middle: 1
      - late-middle: 3
      - end: 4
    """
    if num_passages < 2:
        raise ValueError("num_passages must be >= 2")

    if position == "beginning":
        return 0
    if position == "end":
        return num_passages - 1

    # Use quantiles over passage index to define middle buckets.
    early = max(1, num_passages // 3)
    late = min(num_passages - 2, (2 * num_passages) // 3)
    if position == "early-middle":
        return early
    return late


def assemble_passages(
    supporting_passage: str,
    distractor_passages: list[str],
    support_position: SupportPosition,
    use_redundancy: bool = False,
    num_distractors: int | None = None,
) -> Tuple[list[str], int]:
    """
    Assemble the full list of passages while placing the supporting passage
    at the index corresponding to `support_position`.

    If `num_distractors` is provided, the distractor list is truncated or 
    cycled to match that count (Noise Shift extension).
    """
    if num_distractors is None:
        num_distractors = len(distractor_passages)
    
    # Noise Shift: truncate or cycle distractors to reach target count
    if num_distractors == 0:
        effective_distractors = []
    elif num_distractors <= len(distractor_passages):
        effective_distractors = distractor_passages[:num_distractors]
    else:
        # Cycle to fill if we need more than we have
        effective_distractors = []
        for i in range(num_distractors):
            effective_distractors.append(distractor_passages[i % len(distractor_passages)])

    total = 1 + len(effective_distractors)
    support_idx = get_support_insertion_index(total, support_position)

    ordered: list[str] = ["" for _ in range(total)]
    
    # Track indices where the supporting passage is placed.
    support_indices = {support_idx}
    if use_redundancy:
        support_indices.add(0)
    
    for idx in support_indices:
        ordered[idx] = supporting_passage

    cursor = 0
    for i in range(total):
        if i in support_indices:
            continue
        ordered[i] = effective_distractors[cursor]
        cursor += 1

    return ordered, support_idx


def _format_passage(passage_format: str, index_1_based: int, passage: str) -> str:
    return (
        passage_format.replace("{{index}}", str(index_1_based)).replace(
            "{{passage}}", passage
        )
    )


def build_full_prompt(
    example: PositionEvalExample,
    system_instruction: str,
    passage_format: str,
    use_redundancy: bool = False,
    num_distractors: int | None = None,
) -> str:
    """
    Build a deterministic prompt with a controlled passage order.
    """
    ordered_passages, _ = assemble_passages(
        supporting_passage=example.supporting_passage,
        distractor_passages=example.distractor_passages,
        support_position=example.support_position,
        use_redundancy=use_redundancy,
        num_distractors=num_distractors,
    )

    parts: list[str] = []
    parts.append(system_instruction.strip())
    parts.append("")
    parts.append("Context passages:")
    for i, passage in enumerate(ordered_passages, start=1):
        parts.append(_format_passage(passage_format, i, passage))
    parts.append("")
    parts.append(f"Question: {example.query}")
    parts.append("Answer:")
    return "\n".join(parts).strip() + "\n"

