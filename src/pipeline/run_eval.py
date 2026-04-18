from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.data.datasets import PositionEvalExample, load_position_eval_jsonl
from src.eval.metrics import exact_match, summarize_metrics, token_level_f1
from src.models.model_interface import build_model_from_config, ModelInterface
from src.prompts.context_positioning import (
    build_full_prompt,
    get_support_insertion_index,
)
from src.utils.config import load_yaml_config, save_yaml_config, set_deterministic_seed
from src.utils.logging import setup_logging


def _current_timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def evaluate_examples(
    *,
    model: ModelInterface,
    examples: list[PositionEvalExample],
    system_instruction: str,
    passage_format: str,
    use_redundancy: bool,
    num_distractors: int | None,
    seed: int,
) -> list[dict[str, Any]]:
    per_example: list[dict[str, Any]] = []

    for ex in examples:
        prompt = build_full_prompt(
            example=ex,
            system_instruction=system_instruction,
            passage_format=passage_format,
            use_redundancy=use_redundancy,
            num_distractors=num_distractors,
        )
        prediction = model.generate(prompt, seed=seed)

        em = exact_match(prediction, ex.answer)
        f1 = token_level_f1(prediction, ex.answer)

        # For reporting, calculate the actual insertion index used
        actual_distractor_count = (
            num_distractors if num_distractors is not None else len(ex.distractor_passages)
        )
        num_passages = 1 + actual_distractor_count
        support_idx = get_support_insertion_index(num_passages, ex.support_position)

        per_example.append(
            {
                "id": ex.id,
                "query": ex.query,
                "answer": ex.answer,
                "support_position": ex.support_position,
                "support_passage_index": support_idx,
                "use_redundancy": use_redundancy,
                "num_distractors": actual_distractor_count,
                "prediction": prediction,
                "exact_match": em,
                "token_f1": f1,
            }
        )
    return per_example


def run_from_config(config_path: str | Path, *, run_name: str) -> Path:
    cfg = load_yaml_config(config_path)

    seed = int(cfg.get("seed", 0))
    set_deterministic_seed(seed)

    dataset_cfg = cfg.get("dataset", {})
    dataset_path = dataset_cfg.get("path")
    if not dataset_path:
        raise ValueError("Missing dataset.path in config.")

    prompt_cfg = cfg.get("prompt", {})
    system_instruction = str(
        prompt_cfg.get(
            "system_instruction",
            "You are a careful assistant. Answer the question using the provided context.",
        )
    )
    passage_format = str(prompt_cfg.get("passage_format", "[{{index}}] {{passage}}"))
    use_redundancy = bool(prompt_cfg.get("use_redundancy", False))
    num_distractors = prompt_cfg.get("num_distractors")
    if num_distractors is not None:
        num_distractors = int(num_distractors)

    model_cfg = cfg.get("model", {})
    model = build_model_from_config(model_cfg)

    output_cfg = cfg.get("output", {})
    base_dir = Path(output_cfg.get("base_dir", "outputs/run"))
    run_dir = base_dir / f"{run_name}_seed{seed}_{_current_timestamp()}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Config snapshot for reproducibility.
    cfg_used = dict(cfg)
    cfg_used["run_name"] = run_name
    cfg_used["run_dir"] = str(run_dir)
    cfg_used["config_path"] = str(Path(config_path))
    cfg_used["seed"] = seed
    save_yaml_config(cfg_used, run_dir / "config_used.yaml")

    logger = setup_logging(run_dir, run_name=run_name)
    logger.info("Loaded config and set deterministic seed.")
    logger.info("Dataset path: %s", dataset_path)
    logger.info("Use redundancy: %s", use_redundancy)
    logger.info("Num distractors override: %s", num_distractors)

    examples = load_position_eval_jsonl(dataset_path)

    limit = dataset_cfg.get("limit")
    if limit is not None:
        examples = examples[: int(limit)]

    logger.info("Evaluating %d examples.", len(examples))
    per_example = evaluate_examples(
        model=model,
        examples=examples,
        system_instruction=system_instruction,
        passage_format=passage_format,
        use_redundancy=use_redundancy,
        num_distractors=num_distractors,
        seed=seed,
    )

    metrics = summarize_metrics(per_example)

    (run_dir / "predictions.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in per_example) + "\n",
        encoding="utf-8",
    )
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    logger.info("Done. Metrics: %s", metrics)
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to YAML config.")
    parser.add_argument("--run-name", default="run_eval", help="Name prefix for outputs.")
    args = parser.parse_args()

    run_from_config(args.config, run_name=args.run_name)


if __name__ == "__main__":
    main()

