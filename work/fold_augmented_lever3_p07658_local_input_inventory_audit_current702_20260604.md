# Fold-Augmented Lever 3 P07658 Local Input Inventory Audit - current702

Run: 2026-06-05T01:16:10Z

Lever 3 measured local inventory audit for the remaining P07658 deployment input gap. It scans bounded repo roots for P07658 coordinate/provenance candidates, records checksums, and does not stage coordinates or score rows.

## Status

- fold_augmented_lever3_p07658_local_input_inventory_audit_no_local_candidate
- Local inventory clears P07658 gap now: False
- Acceptance preflight ready from local inventory: False

## Counts

- Files scanned: 8028
- P07658 matched files: 38
- Coordinate candidates: 0
- Filled provenance candidates: 0
- Provenance templates: 2
- Dispatch FASTA files: 1

## Operator Targets

- Preferred coordinate path exists: False
- Filled provenance path exists: False

## Inventory Rows

| kind | path | size |
| --- | --- | ---: |
| readout_or_probe_json | artifacts/v3_fold_augmented_confounded_proxy_surface_and_calibration_state_after_q43088_p07658_current702_20260604.json | 7411 |
| readout_or_probe_json | artifacts/v3_fold_augmented_lever3_p07658_credential_route_preflight_current702_20260604.json | 6246 |
| readout_or_probe_json | artifacts/v3_fold_augmented_lever3_p07658_exact_route_attempt_readout_current702_20260604.json | 9889 |
| readout_or_probe_json | artifacts/v3_fold_augmented_lever3_p07658_exact_route_attempts_current702_20260604.json | 10784 |
| readout_or_probe_json | artifacts/v3_fold_augmented_lever3_p07658_local_runtime_refresh_after_bandpass_current702_20260604.json | 4788 |
| readout_or_probe_json | artifacts/v3_fold_augmented_lever3_p07658_public_route_refresh_after_bandpass_current702_20260604.json | 5474 |
| readout_or_probe_json | artifacts/v3_fold_augmented_lever3_p07658_sequence_compatibility_readout_current702_20260604.json | 8973 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_3dbeacons_predicted_structure_probe_current702_20260604.json | 6043 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_alphafold_prediction_api_probe_current702_20260604.json | 3858 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_biolm_single_provider_attempt_current702_20260604.json | 3125 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_computed_model_repository_broad_probe_current702_20260604.json | 7984 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_esmfold_api_preflight_current702_20260604.json | 3907 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_full_length_prediction_request_manifest_current702_20260604.json | 8770 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_full_length_predictor_provider_probe_current702_20260604.json | 3530 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_local_predictor_runtime_scan_current702_20260604.json | 7425 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_prediction_acceptance_preflight_current702_20260604.json | 7261 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_prediction_dispatch_packet_current702_20260604.json | 13248 |
| provenance_template | artifacts/v3_fold_augmented_p07658_prediction_provenance_template_current702_20260604.json | 4604 |
| readout_or_probe_json | artifacts/v3_fold_augmented_p07658_secondary_accession_predicted_coordinate_reprobe_current702_20260604.json | 4854 |
| human_report | work/fold_augmented_confounded_proxy_surface_and_calibration_state_after_q43088_p07658_current702_20260604.md | 2596 |
| human_report | work/fold_augmented_lever3_p07658_credential_route_preflight_current702_20260604.md | 2704 |
| human_report | work/fold_augmented_lever3_p07658_exact_route_attempt_readout_current702_20260604.md | 2795 |
| human_report | work/fold_augmented_lever3_p07658_local_runtime_refresh_after_bandpass_current702_20260604.md | 1014 |
| human_report | work/fold_augmented_lever3_p07658_sequence_compatibility_readout_current702_20260604.md | 4209 |
| human_report | work/fold_augmented_lever3_post_bandpass_p07658_live_probe_current702_20260604.md | 1941 |
| human_report | work/fold_augmented_p07658_3dbeacons_predicted_structure_probe_current702_20260604.md | 1976 |
| human_report | work/fold_augmented_p07658_alphafold_prediction_api_probe_current702_20260604.md | 1352 |
| human_report | work/fold_augmented_p07658_biolm_single_provider_attempt_current702_20260604.md | 777 |
| human_report | work/fold_augmented_p07658_computed_model_repository_broad_probe_current702_20260604.md | 2844 |
| human_report | work/fold_augmented_p07658_esmfold_api_preflight_current702_20260604.md | 1680 |
| dispatch_fasta | work/fold_augmented_p07658_full_length_prediction_input_current702_20260604.fasta | 816 |
| human_report | work/fold_augmented_p07658_full_length_prediction_request_manifest_current702_20260604.md | 2716 |
| human_report | work/fold_augmented_p07658_full_length_predictor_provider_probe_current702_20260604.md | 1627 |
| human_report | work/fold_augmented_p07658_local_predictor_runtime_scan_current702_20260604.md | 2023 |
| human_report | work/fold_augmented_p07658_prediction_acceptance_preflight_current702_20260604.md | 2206 |
| human_report | work/fold_augmented_p07658_prediction_dispatch_packet_current702_20260604.md | 3469 |
| provenance_template | work/fold_augmented_p07658_prediction_provenance_template_current702_20260604.md | 1888 |
| human_report | work/fold_augmented_p07658_secondary_accession_predicted_coordinate_reprobe_current702_20260604.md | 1822 |

## Decision

- Route-equivalent no-credential retries should stop: True
- Exact missing evidence needed: ['local exact full-length P07658 coordinate file', 'filled provider/model/version/path/checksum and U140 provenance']
- Smallest next experiment: Provision exactly one credentialed provider route (HF_TOKEN, NVIDIA_API_KEY, or BIOLM_API_KEY) or install one local predictor runtime that can handle the frozen 715-aa P07658 sequence with U140 provenance.
- Next gate: Rerun P07658 acceptance preflight if the preferred coordinate and filled provenance files are added locally; otherwise provision the credentialed/local exact prediction route first.

## Guardrails

- Local inventory only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, or secret values changed.
- Critical violations: 0

## Interpretation

- No local P07658 coordinate/provenance candidate is present in the bounded repo inventory.
- 0 coordinate-like P07658 files and 0 filled provenance files were found across 8028 files.
- Continue with the credentialed/local predictor experiment; the repo currently contains only dispatch/report/template P07658 files, not a coordinate candidate.
