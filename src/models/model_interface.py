from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


class ModelInterface(ABC):
    """
    Minimal model interface for later plugging in API-based or local generation.
    """

    @abstractmethod
    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class HeuristicContextAnswerModel(ModelInterface):
    """
    Deterministic baseline that simulates lost-in-the-middle behavior.

    Assumptions for the included synthetic dataset:
    - The supporting passage contains: "The answer is: <ANSWER>."
    - Distractor passages do not contain that substring.

    Behavior:
    - Only the first N and last M passages are considered "readable".
    - If the supporting passage falls outside that window, the model returns "".
    """

    read_beginning_n_passages: int = 1
    read_end_n_passages: int = 1
    answer_marker_regex: str = (
        r"The answer is:\s*(?P<ans>.*?)(?:\.\s*$|\n|$)"
    )

    def generate(self, prompt: str, *, seed: int | None = None) -> str:
        del seed  # deterministic baseline; seed exists for interface compatibility

        # Extract passage lines in the form: "[i] passage text"
        passage_lines = re.findall(r"^\[(\d+)\]\s*(.+)$", prompt, flags=re.MULTILINE)
        if not passage_lines:
            return ""

        passage_lines.sort(key=lambda x: int(x[0]))
        passages = [txt for _, txt in passage_lines]

        support_passage_idx: Optional[int] = None
        extracted_answer: str | None = None
        marker_re = re.compile(self.answer_marker_regex, flags=re.MULTILINE)

        for i, passage in enumerate(passages):
            m = marker_re.search(passage)
            if m:
                support_passage_idx = i
                extracted_answer = (m.group("ans") or "").strip()
                break

        if support_passage_idx is None or extracted_answer is None:
            return ""

        total = len(passages)
        readable_begin = set(range(0, min(total, self.read_beginning_n_passages)))
        readable_end = set(range(max(0, total - self.read_end_n_passages), total))

        if support_passage_idx in readable_begin or support_passage_idx in readable_end:
            return extracted_answer
        return ""


def build_model_from_config(model_cfg: dict[str, Any]) -> ModelInterface:
    model_type = model_cfg.get("type")
    if model_type == "heuristic":
        return HeuristicContextAnswerModel(
            read_beginning_n_passages=int(
                model_cfg.get("read_beginning_n_passages", 1)
            ),
            read_end_n_passages=int(model_cfg.get("read_end_n_passages", 1)),
            answer_marker_regex=str(
                model_cfg.get(
                    "answer_marker_regex",
                    HeuristicContextAnswerModel.answer_marker_regex,
                )
            ),
        )

    raise ValueError(f"Unsupported model.type: {model_type!r}")

