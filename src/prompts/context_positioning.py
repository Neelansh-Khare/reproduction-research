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
) -> Tuple[list[str], int]:
    """
    Assemble the full list of passages while placing the supporting passage
    at the index corresponding to `support_position`.
    """
    total = 1 + len(distractor_passages)
    support_idx = get_support_insertion_index(total, support_position)

    ordered: list[str] = ["" for _ in range(total)]
    ordered[support_idx] = supporting_passage

    cursor = 0
    for i in range(total):
        if i == support_idx:
            continue
        ordered[i] = distractor_passages[cursor]
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
) -> str:
    """
    Build a deterministic prompt with a controlled passage order.
    """
    ordered_passages, _ = assemble_passages(
        supporting_passage=example.supporting_passage,
        distractor_passages=example.distractor_passages,
        support_position=example.support_position,
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

