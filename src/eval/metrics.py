from __future__ import annotations

import re
from collections import Counter


_NON_ALNUM_RE = re.compile(r"[^a-z0-9\s]+")
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """
    Lightweight normalization for EM/F1:
    - lowercases
    - removes punctuation (keeps letters/numbers/whitespace)
    - collapses whitespace
    """
    text = text.lower().strip()
    text = _NON_ALNUM_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def exact_match(prediction: str, ground_truth: str) -> bool:
    return normalize_text(prediction) == normalize_text(ground_truth)


def token_level_f1(prediction: str, ground_truth: str) -> float:
    pred_tokens = normalize_text(prediction).split()
    gold_tokens = normalize_text(ground_truth).split()

    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0

    pred_counts = Counter(pred_tokens)
    gold_counts = Counter(gold_tokens)
    overlap = sum((pred_counts & gold_counts).values())

    precision = overlap / len(pred_tokens)
    recall = overlap / len(gold_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def summarize_metrics(per_example: list[dict[str, float | bool]]) -> dict[str, float]:
    """
    Aggregate metric summary from per-example records.
    Expected keys per record:
      - exact_match: bool
      - token_f1: float
    """
    if not per_example:
        return {"exact_match": 0.0, "token_f1": 0.0}

    em = sum(1 for x in per_example if bool(x["exact_match"])) / len(per_example)
    f1 = sum(float(x["token_f1"]) for x in per_example) / len(per_example)
    return {"exact_match": em, "token_f1": f1}

