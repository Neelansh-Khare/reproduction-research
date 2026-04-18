#!/bin/bash
set -e

# Run the noise shift reproduction experiment
# This experiment increases the number of distractors to 10 (11 total passages)
# and observes how it affects the U-curve.

python -m src.pipeline.run_eval \
    --config configs/noise_shift_repro.yaml \
    --run-name noise_shift_repro
