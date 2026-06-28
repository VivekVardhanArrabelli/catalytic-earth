# Predicted-Geometry Atlas Engine Preregistration

Run: 2026-06-28T01:42:47Z
Status: `preregistered_cached_surface_blocked_current57_router_drift_new_foldseek_backend_blocked`

## Capability

- Existing scored fold/TM surfaces reusable: True.
- New Foldseek/TM scoring runnable: False.
- Sequence sidecars reusable: True.
- Blockers: esm_missing_for_new_esm_embedding_generation, foldseek_missing_for_new_fold_tm_scoring.

## Preexisting Train/Cal Context

- Cofactor recovery calibration: experimental 34 -> apo 17 -> fused 30; recovered 12/17.
- Cofactor precision threshold dial: 0.44 (dominates suppression: True).
- Fold/TM fixed threshold: 0.44155; calibration OOS abstain 30/75.
- Current-router drift detected: True.

## Preregistered Next Readout

- Name: `predicted_apo_atlas_engine_v1_train_cal_contract`.
- Selection rule: On calibration rows, retain a primary call only when the cofactor-fused router score is at least the preregistered cofactor threshold and the fold/TM combined_mean_geometry_fold gate retains at its fixed threshold; otherwise abstain.
- Done bar: candidate keeps >=30/35 calibration in-scope cofactor-fused primaries while not increasing OOS FPs over the 0.44 cofactor threshold readout, and every missing fold/TM score is fail-closed

## Guardrails

- No heldout rows are scored or read by this artifact.
- No production threshold, model weight, registry, ontology, or fingerprint-family change is made.
- Next action: Resolve the current-router/fingerprint-surface drift before an atlas-engine readout: either freeze the intended June 9 router/fingerprint surface for cofactor precision, or preregister a new current-57-family cofactor precision rule on train/cal. Install or expose foldseek before any new Foldseek/TM scoring.
