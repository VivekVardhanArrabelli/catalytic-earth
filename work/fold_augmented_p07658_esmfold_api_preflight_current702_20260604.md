# Fold-Augmented P07658 ESMFold API Preflight - current702

Run: 2026-06-04T10:17:10Z

Smallest fresh-predicted-structure preflight for the remaining P07658 Lever 3 coordinate blocker. It probes whether the public ESMFold sequence-to-PDB endpoint can fold the exact current UniProt sequence. It stages no coordinates, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_esmfold_api_preflight_blocked_sequence_too_long
- Sequence length: 715
- Public endpoint limit: 400
- Noncanonical residues: 1
- Coordinates returned: 0
- Blockers: ['p07658_exact_sequence_exceeds_public_esmfold_endpoint_limit', 'p07658_contains_selenocysteine_requires_model_generator_support', 'p07658_predicted_coordinate_not_staged', 'fixed_threshold_audit_not_ready_to_rerun']

## Endpoint Probe

| provider | endpoint | status | response |
| --- | --- | ---: | --- |
| ESMFold API | https://api.esmatlas.com/foldSequence/v1/pdb/ | 413 | Sequence is longer than 400. |

## Decision

- Public ESMFold clears P07658 now: False
- Smallest next experiment: Use a model-generation route that supports at least 715 residues and selenocysteine without modifying the sequence, or run an approved local/remote predictor with recorded model/version/path/checksum provenance.

## Interpretation

- Public ESMFold API cannot produce a deployment-valid P07658 coordinate for the exact current sequence because the 715-residue sequence exceeds the 400-residue endpoint limit; the row remains blocked.
- The smallest remaining P07658 experiment is a full-length predictor/runtime that supports 715 residues and selenocysteine, with provider/model/version/path/checksum provenance.
