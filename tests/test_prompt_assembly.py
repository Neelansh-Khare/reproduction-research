from src.data.datasets import PositionEvalExample
from src.prompts.context_positioning import assemble_passages, build_full_prompt


def test_assemble_passages_bucket_indices() -> None:
    supporting = "SUPPORT"
    distractors = ["D1", "D2", "D3", "D4"]
    base_example = PositionEvalExample(
        id="ex1",
        query="Q",
        answer="A",
        supporting_passage=supporting,
        distractor_passages=distractors,
        support_position="beginning",
    )

    # total passages = 1 supporting + 4 distractors = 5
    ordered, support_idx = assemble_passages(
        supporting_passage=base_example.supporting_passage,
        distractor_passages=base_example.distractor_passages,
        support_position="beginning",
    )
    assert ordered[support_idx] == supporting
    assert support_idx == 0

    ordered, support_idx = assemble_passages(
        supporting_passage=base_example.supporting_passage,
        distractor_passages=base_example.distractor_passages,
        support_position="early-middle",
    )
    assert support_idx == 1

    ordered, support_idx = assemble_passages(
        supporting_passage=base_example.supporting_passage,
        distractor_passages=base_example.distractor_passages,
        support_position="late-middle",
    )
    assert support_idx == 3

    ordered, support_idx = assemble_passages(
        supporting_passage=base_example.supporting_passage,
        distractor_passages=base_example.distractor_passages,
        support_position="end",
    )
    assert support_idx == 4

    # All passages should appear exactly once
    assert sorted(ordered) == sorted([supporting] + distractors)


def test_build_full_prompt_includes_numbering() -> None:
    example = PositionEvalExample(
        id="ex1",
        query="What is 2+2?",
        answer="4",
        supporting_passage="The answer is: 4.",
        distractor_passages=["Noise 1", "Noise 2", "Noise 3", "Noise 4"],
        support_position="end",
    )

    prompt = build_full_prompt(
        example=example,
        system_instruction="You are a careful assistant.",
        passage_format='[{{index}}] {{passage}}',
    )
    assert "You are a careful assistant." in prompt
    assert "[1] " in prompt
    assert "[5] " in prompt
    assert example.supporting_passage in prompt
    assert example.query in prompt

