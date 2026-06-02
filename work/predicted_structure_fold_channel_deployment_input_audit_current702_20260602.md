# Predicted-Structure Fold Channel Deployment Input Audit - current702

Run: 2026-06-02T16:12:19Z

Validation-only audit that the current fold channel is a predicted-structure-vs-atlas signal. It checks coordinate request provenance and scored row payload fields without rerunning Foldseek/TM, changing thresholds, or editing labels.

## Status

- predicted_structure_fold_channel_deployment_inputs_predicted_only
- Coordinate request rows: 299
- AFDB URL requests: 299
- AFDB local path requests: 299
- Row-score rows: 126
- Row scores with nearest-atlas TM score: 126
- Critical violations: 0

## Critical Counts

- coordinate_request_local_path_not_afdb_v6_cif: 0
- coordinate_request_url_not_afdb_v6_cif: 0
- coordinate_requests_with_experimental_pdb_metadata_keys: 0
- row_scores_with_experimental_pdb_metadata_keys: 0
- unexpected_fold_signal_keys: 0

## Decision

- Deployment input contract passed: True
- Next gate: Use this audit with the confounded readiness artifact: the fold channel input surface is predicted-only, while deployment closure still depends on the composed production-blocker and coordinate-provenance gates.

## Interpretation

- The current fold channel coordinate requests and scored row signals are predicted-structure-vs-atlas inputs; experimental PDB metadata does not appear in the checked channel fields.
- Keep using the fixed operating point; clear production blockers and verify the composed coordinate-provenance gate before deployment-closed claims.
