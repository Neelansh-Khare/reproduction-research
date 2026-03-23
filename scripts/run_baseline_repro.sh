#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

CONFIG_PATH="${1:-$ROOT_DIR/configs/baseline_repro.yaml}"

if [ -d "$ROOT_DIR/.venv" ]; then
  source "$ROOT_DIR/.venv/bin/activate"
fi

python -m src.pipeline.run_eval --config "$CONFIG_PATH" --run-name baseline_repro

