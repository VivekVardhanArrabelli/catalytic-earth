# Fold-Augmented Lever 3 P07658 Exact Route Attempt Readout - current702

Run: 2026-06-04T22:21:04Z

Lever 3 measured exact-route attempt readout for the remaining P07658 coordinate/provenance gate after the accepted bandpass counteraxis contract. It summarizes no-credential public/provider attempts on the frozen full-length sequence, stages no coordinate, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_lever3_p07658_exact_route_attempt_readout_no_coordinate
- Counteraxis contracts ready: True
- Exact route clears coordinate gap now: False
- Fixed-threshold audit ready to rerun now: False

## Operating Context

- Baseline threshold: 0.44155
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204

## Route Attempts

| route | status | coordinate | reason |
| --- | ---: | --- | --- |
| esm_atlas_foldsequence_v1_pdb_exact_full_length | 413 | False | public_endpoint_sequence_length_limit_400 |
| huggingface_legacy_api_inference_esmfold_exact_full_length | None | False | dns_unresolved_from_runtime |
| huggingface_router_hf_inference_esmfold_exact_full_length | 401 | False | authentication_required_or_unauthorized |
| biolm_esmfold_documented_items_payload_exact_full_length | 401 | False | authentication_credentials_not_provided |
| nvidia_nim_esmfold_exact_full_length | 401 | False | authorization_header_missing |
| swissmodel_repository_uniprot_json_refresh | 200 | False | repository_returns_only_pdb_provider_rows |

## Counts

- Routes attempted: 6
- Exact sequence submitted routes: 5
- Coordinates returned: 0
- Deployment-valid predicted coordinate rows: 0
- PDB-provider rows rejected: 5
- SWISS-MODEL predicted model rows: 0

## Decision

- Current evidence sufficient for deployment closure: False
- Remaining missing evidence: ['credentialed or local exact full-length P07658 predicted coordinate with provider/model/version/path/checksum and U140 provenance']
- Smallest next experiment: Provision a credentialed or local full-length predictor route that accepts the frozen 715-residue P07658 sequence with U140 preserved or explicitly documented, then rerun acceptance preflight before any fixed-threshold scoring.
- Next gate: Stop retrying equivalent no-credential public routes; use a credentialed/provider or local full-length predictor that can emit a coordinate with U140 provenance.

## Interpretation

- Exact no-credential P07658 routes still do not return a deployment-valid coordinate.
- 6 exact/public route surfaces were checked; 0 returned coordinates and 0 were deployment-valid predicted-coordinate rows for P07658.
- Use a credentialed or local full-length predictor route; do not truncate, mutate U140, use PDB-provider coordinates, or rerun fixed-threshold scoring until acceptance preflight passes.
