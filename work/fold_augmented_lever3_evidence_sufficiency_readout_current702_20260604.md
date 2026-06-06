# Fold-Augmented Lever 3 Evidence-Sufficiency Readout - current702

Run: 2026-06-04T16:40:25Z

Lever 3 measured evidence-sufficiency readout after trying the current strict operating point, near-cofactor pressure rows, loose same-family pressure rows, protein-only topology residual rows, and the P07658 full-length prediction path. It is not a blocker packet and does not change thresholds.

## Status

- fold_augmented_lever3_evidence_sufficiency_readout_ready_evidence_insufficient
- Fixed threshold: 0.44155
- Canonical train/cal OOS abstained: 72/204
- Calibration in-scope retained: 31/34
- Strict high-cofactor proxy: 0/4
- Strict same-family proxy: 11/59
- Protein-only topology combined/fold-only: 7/8 and 2/8
- Blockers: ['p07658_exact_predicted_coordinate_not_accepted', 'strict_high_cofactor_proxy_target_not_met', 'strict_same_family_structural_proxy_target_not_met', 'protein_only_topology_residual_diagnostic_has_blockers']

## Measured Routes

| route | rows | abstained | closure support | result |
| --- | ---: | ---: | --- | --- |
| canonical_strict_proxy_operating_point | 204 | 72 | False | strict high-cofactor 0/4; strict same-family structural 11/59 |
| near_cofactor_pressure_tranche | 16 | 8 | False | 8/16 abstained |
| loose_same_family_pressure_surface | 80 | 26 | False | 26/80 abstained |
| protein_only_fold_topology_residual_tranche | 8 | 7 | False | combined 7/8; fold-only 2/8 abstained |
| p07658_full_length_prediction_coordinate | 1 | 0 | False | acceptance failed 7/8 checks; AlphaFold API models 0; local commands 0/5; provider coordinates 0; public predicted coordinates 0/0 |

## Missing Evidence

| gap | current measured state | smallest next experiment |
| --- | --- | --- |
| p07658_surface_completeness | `{"acceptance_checks_failed": 7, "acceptance_preflight_passes": false, "alphafold_api_models_returned": 0, "credentialed_or_denied_providers": 2, "local_path_commands_available": 0, "local_path_commands_checked": 5, "provider_coordinates_returned": 0, "public_repository_deployment_valid_predicted_rows": 0, "surface_completeness_blocker_rows": 1, "three_d_beacons_deployment_valid_predicted_rows": 0}` | Run or provision one approved full-length predictor/provider for exact P07658, with documented selenocysteine position-140 handling and coordinate/provider/model/version/checksum provenance; rerun the acceptance preflight before scoring. |
| strict_high_cofactor_train_cal_oos_rows | `{"intake_slots_required": 16, "near_cofactor_diagnostic_abstained": 8, "near_cofactor_diagnostic_rows": 16, "strict_abstained": 0, "strict_high_cofactor_contract_rows_added": 0, "strict_rows": 4}` | Acquire and score 16 new non-heldout train/cal OOS rows with strict source-free high-cofactor/locus membership; near-cofactor pressure rows are insufficient. |
| strict_same_family_structural_surface | `{"intake_slots_required": 170, "strict_abstained": 11, "strict_plus_loose_diagnostic_abstained": 26, "strict_plus_loose_diagnostic_rows": 80, "strict_rows": 59}` | Acquire a new strict same-family structural train/cal OOS surface; the current strict-plus-loose diagnostic reaches only 26/80 and cannot close the 170-row lower-bound gap. |
| protein_only_topology_residual_contract | `{"artifact_blockers": ["some_tranche_rows_missing_predicted_geometry"], "diagnostic_abstained": 7, "diagnostic_rows": 8, "fold_only_abstained": 2, "fold_only_rows": 8, "fold_only_threshold": 0.4325, "predicted_geometry_blocker_rows": 7, "predicted_geometry_ok_rows": 1}` | Convert the protein-only topology signal into a deployment-valid axis only if it uses a geometry-independent protein-only rule or repairs the row-specific geometry caveats, then scale beyond the eight-row diagnostic tranche. |

## Decision

- Current evidence sufficient for deployment closure: False
- Protein-only topology residual promising but not closure: True
- P07658 prediction path cleared now: False
- Next gate: Current evidence is not enough. Keep threshold 0.44155 fixed; clear P07658 with an accepted full-length prediction packet, then acquire strict high-cofactor train/cal OOS rows before the larger same-family structural surface.

## Interpretation

- Current Lever 3 evidence is measured but not sufficient for deployment closure.
- Canonical strict proxy readout is high-cofactor 0/4 and same-family 11/59; diagnostics add near-cofactor 8/16, loose same-family 26/80, and protein-only combined 7/8 (fold-only 2/8), none of which can close the strict contracts.
- Do not emit a blocker packet yet; continue with P07658 accepted prediction provenance or strict high-cofactor row acquisition.
