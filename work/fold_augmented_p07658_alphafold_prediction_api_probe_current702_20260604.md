# Fold-Augmented P07658 AlphaFold Prediction API Probe - current702

Run: 2026-06-04T15:22:13Z

Narrow Lever 3 AFDB prediction API route probe after the near-cofactor P68698 rescue showed that noncanonical AFDB model IDs may exist even when legacy direct URLs 404. It stages no P07658 coordinate, scores no P07658 row, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_alphafold_prediction_api_probe_no_p07658_model_p68698_route_confirmed
- P07658 API status: 404
- P07658 models returned: 0
- P68698 models returned: 1
- P68698 coordinate staged: True

## Decision

- P07658 coordinate blocker cleared now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not repeat legacy AFDB direct URL or prediction API checks for P07658 without new provider evidence. P07658 still needs an approved full-length predictor/provider that supports the exact 715-aa selenoprotein sequence and records selenocysteine handling.

## Interpretation

- The AFDB prediction API returns no P07658 model (404, empty object), so the API route cannot clear the P07658 surface-completeness blocker. The same route confirms why P68698 could be completed via a Viro3D ColabFold model.
- Run or provision a full-length P07658 predictor/provider with explicit selenocysteine position-140 handling and coordinate/provenance checksums.
