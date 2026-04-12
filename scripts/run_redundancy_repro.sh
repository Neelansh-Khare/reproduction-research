#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

CONFIG_PATH="${1:-$ROOT_DIR/configs/redundancy_repro.yaml}"

# Set PYTHONPATH to root so we can find src
export PYTHONPATH="$ROOT_DIR"

if [ -d "$ROOT_DIR/.venv" ]; then
  source "$ROOT_DIR/.venv/bin/activate"
fi

python -m src.pipeline.run_eval --config "$CONFIG_PATH" --run-name redundancy_repro
