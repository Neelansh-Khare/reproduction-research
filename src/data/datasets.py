from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

SupportPosition = Literal["beginning", "early-middle", "late-middle", "end"]


@dataclass(frozen=True)
class PositionEvalExample:
    """
    Minimal example schema for position-controlled long-context evaluation.
    """

    id: str
    query: str
    answer: str
    supporting_passage: str
    distractor_passages: list[str]
    support_position: SupportPosition


def _validate_support_position(value: Any) -> SupportPosition:
    allowed = {"beginning", "early-middle", "late-middle", "end"}
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f"Invalid support_position: {value!r}")
    return value  # type: ignore[return-value]


def load_position_eval_jsonl(path: str | Path) -> list[PositionEvalExample]:
    """
    Load a JSONL file where each line stores one `PositionEvalExample`.

    Expected keys:
      - query (str)
      - answer (str)
      - supporting_passage (str)
      - distractor_passages (list[str])
      - support_position (beginning|early-middle|late-middle|end)
    Optional key:
      - id (str)
    """

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    examples: list[PositionEvalExample] = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)

            try:
                query = obj["query"]
                answer = obj["answer"]
                supporting_passage = obj["supporting_passage"]
                distractor_passages = obj["distractor_passages"]
                support_position = _validate_support_position(obj["support_position"])
            except KeyError as e:
                raise KeyError(f"Missing key {e!r} on line {i} of {path}") from e

            if not isinstance(query, str):
                raise TypeError(f"query must be str on line {i}")
            if not isinstance(answer, str):
                raise TypeError(f"answer must be str on line {i}")
            if not isinstance(supporting_passage, str):
                raise TypeError(f"supporting_passage must be str on line {i}")
            if not isinstance(distractor_passages, list) or not all(
                isinstance(x, str) for x in distractor_passages
            ):
                raise TypeError(f"distractor_passages must be list[str] on line {i}")

            example_id = obj.get("id", f"ex{i}")
            if not isinstance(example_id, str):
                raise TypeError(f"id must be str on line {i}")

            examples.append(
                PositionEvalExample(
                    id=example_id,
                    query=query,
                    answer=answer,
                    supporting_passage=supporting_passage,
                    distractor_passages=distractor_passages,
                    support_position=support_position,
                )
            )

    return examples

