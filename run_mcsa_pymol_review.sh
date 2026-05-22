#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
REPO="$SCRIPT_DIR"
PYTHON_BIN="${PYTHON_BIN:-python}"
REVIEWER="${REVIEWER:-vivek}"
OUT_PATH="${OUT_PATH:-$REPO/artifacts/v3_expert_review_decision_batch_pymol_manual.json}"
QUEUE_PATH="${QUEUE_PATH:-/tmp/mcsa_1025_absolute_queue.json}"
PML_DIR="${PML_DIR:-$REPO/artifacts/review_pymol/mcsa_1025_absolute_local}"

unset PYTHONHOME
export PYTHONPATH="$REPO/src"

# Avoid Python cwd resolution failures seen from macOS-protected Documents paths.
cd /tmp

"$PYTHON_BIN" -m catalytic_earth.cli build-mcsa-pymol-review-queue \
  --expert-review-export "$REPO/artifacts/v3_expert_label_decision_review_export_1000.json" \
  --review-debt-summary "$REPO/artifacts/v3_review_debt_summary_1025_preview.json" \
  --review-evidence-gaps "$REPO/artifacts/v3_review_evidence_gaps_1025_preview.json" \
  --geometry-features "$REPO/artifacts/v3_geometry_features_1025.json" \
  --structure-dir "$REPO/artifacts/v3_mcsa_pymol_materialized_coordinates_20260522" \
  --structure-dir "$REPO/artifacts/v3_foldseek_coordinates_1000" \
  --write-pml \
  --pml-dir "$PML_DIR" \
  --out "$QUEUE_PATH"

"$PYTHON_BIN" -m catalytic_earth.cli launch-mcsa-pymol-review \
  --queue "$QUEUE_PATH" \
  --out "$OUT_PATH" \
  --reviewer "$REVIEWER" \
  "$@"
