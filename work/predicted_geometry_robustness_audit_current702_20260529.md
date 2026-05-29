# Predicted Geometry Robustness Audit

Run: 2026-05-29T14:35:35Z

This swaps experimental M-CSA/PDB coordinates for AlphaFoldDB predicted coordinates on the frozen current702 heldout rows. No labels, registries, ontologies, imports, production scoring, or global thresholds were edited.

## Headline

- Targeted 128/140 heldout rows; 12 heldout rows were excluded by missing/incompatible sequence-position or experimental-geometry prerequisites.
- AlphaFoldDB geometry availability: 126/128 rows ok; 2 fetch failures; 0 rows with proximal ligands.
- Hand router on predicted geometry: 23/45 primary correct, 17 abstained, 5 wrong nonabstained, 0 missing.
- Hand router OOS/sec false-positive rate: 0.123457.
- OOS-aware MLP-32 transfer: 16/45 primary correct, 29 abstained, 0 wrong nonabstained.
- Interpretation: predicted_geometry_introduces_wrong_primary_calls; robustness_not_raw_clean_geometry_accuracy_is_the_learned_model_job.

## Caveat

This isolates coordinate-source degradation while still using curated M-CSA catalytic residue identities, roles, and sequence positions. It is not an active-site localization benchmark from bare sequence.

## Per-bin Hand Router

| Bin | Primary support | Primary available | Primary correct | Primary abstain | Primary wrong | OOS/sec support | OOS/sec FP rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| broad_bucket_ambiguous | 0 | 0 | 0 | 0 | 0 | 78 | 0.12987 |
| dense_same_mechanism_structural_neighborhood | 10 | 10 | 4 | 5 | 1 | 0 | None |
| high_structure_similarity_different_fingerprint | 0 | 0 | 0 | 0 | 0 | 5 | 0.0 |
| low_structure_neighborhood_near_orphan | 30 | 30 | 15 | 11 | 4 | 0 | None |
| no_reliable_structure | 5 | 5 | 4 | 1 | 0 | 0 | None |
