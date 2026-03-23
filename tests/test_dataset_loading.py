import json
from pathlib import Path

from src.data.datasets import PositionEvalExample, load_position_eval_jsonl


def test_load_position_eval_jsonl_parses_fields(tmp_path: Path) -> None:
    sample = {
        "id": "ex1",
        "query": "What is 2+2?",
        "answer": "4",
        "supporting_passage": "The answer is: 4.",
        "distractor_passages": ["Noise 1", "Noise 2"],
        "support_position": "beginning",
    }
    p = tmp_path / "sample.jsonl"
    p.write_text(json.dumps(sample) + "\n", encoding="utf-8")

    examples = load_position_eval_jsonl(str(p))
    assert len(examples) == 1

    ex = examples[0]
    assert isinstance(ex, PositionEvalExample)
    assert ex.id == "ex1"
    assert ex.query == "What is 2+2?"
    assert ex.answer == "4"
    assert ex.supporting_passage == "The answer is: 4."
    assert ex.distractor_passages == ["Noise 1", "Noise 2"]
    assert ex.support_position == "beginning"

