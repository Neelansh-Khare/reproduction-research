from __future__ import annotations

import os
import random
from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if cfg is None:
        return {}
    if not isinstance(cfg, dict):
        raise TypeError("Top-level YAML config must be a mapping/dict.")
    return cfg


def set_deterministic_seed(seed: int) -> None:
    """
    Best-effort deterministic seeding for baseline experiments.

    Note: setting `PYTHONHASHSEED` after interpreter startup does not retroactively
    affect Python's hash randomization. For complete determinism, set it in the
    environment before starting Python.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)


def save_yaml_config(cfg: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

