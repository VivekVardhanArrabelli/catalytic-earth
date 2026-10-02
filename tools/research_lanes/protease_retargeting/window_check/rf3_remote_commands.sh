#!/usr/bin/env bash
# PREPARED ONLY. Execute in the qualified remote environment after authorization.
# The owner enforces the shared $5 / 45-minute resource limit externally.
# No installation, provisioning, checkpoint download, retry, or rescue sampling here.
set -euo pipefail
: "${CE_RF3_DRIVER:?Path to rf3_native_gate.py required}"
: "${CE_RF3_INPUT_DIR:?Directory containing the two immutable input JSONs required}"
: "${CE_RF3_OUT:?Fresh output root required}"
unset LOCAL_MSA_DIRS
qualifier=()
if [[ -n "${CE_RF3_FOUNDRY:-}" ]]; then
  qualifier=(--foundry-root "$CE_RF3_FOUNDRY")
fi

# Phase 1: native imports and component/bond/charge checks, without model weights.
python3 "$CE_RF3_DRIVER" "${qualifier[@]}" --input-dir "$CE_RF3_INPUT_DIR" --out-dir "$CE_RF3_OUT/gate"

# Phase 2: only after the gate passes and a checkpoint content hash is pinned.
: "${CE_RF3_CKPT:?Exact local checkpoint file required}"
: "${CE_RF3_CKPT_SHA256:?Previously recorded checkpoint SHA256 required}"
python3 "$CE_RF3_DRIVER" "${qualifier[@]}" --input-dir "$CE_RF3_INPUT_DIR" --out-dir "$CE_RF3_OUT/seed-0" --infer-seed 0 --checkpoint "$CE_RF3_CKPT" --checkpoint-sha256 "$CE_RF3_CKPT_SHA256"
python3 "$CE_RF3_DRIVER" "${qualifier[@]}" --input-dir "$CE_RF3_INPUT_DIR" --out-dir "$CE_RF3_OUT/seed-1" --infer-seed 1 --checkpoint "$CE_RF3_CKPT" --checkpoint-sha256 "$CE_RF3_CKPT_SHA256"
# Assigned denominator: 2 conditions x 2 seeds x 5 samples = 20 structures.
# Keep every native sample/score and any missing assignments; do not select only ranking winners.
