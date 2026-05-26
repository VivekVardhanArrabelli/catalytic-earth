# Wave 1 Representation Shootout Diagnostic

Generated: 2026-05-26T04:27:02Z

This is a diagnostic map for the current702 heldout split, not a bigger-model leaderboard. It joins the main sequence/geometry/Foldseek artifacts with read-only representation-branch outputs and keeps every decision proposal-only.

## Artifacts

- `artifacts/v3_wave1_structure_neighborhood_audit_20260526.json`
- `artifacts/v3_wave1_representation_shootout_result_card_20260526.json`
- Preserved prior design artifacts:
  - `artifacts/v3_mechanism_prediction_fold_controlled_eval_design_702_20260525.json`
  - `artifacts/v3_mechanism_prediction_orphan_eval_design_702_20260525.json`
  - `artifacts/v3_mechanism_fingerprint_v2_sublabel_audit_702_20260525.json`

## Interpretation

Wave 1 is best read as broad-bucket structural-neighborhood transfer plus abstention diagnostics, not as evidence that a larger learned model has solved mechanism prediction.

Next month should not start by scaling model size. The practical path is Foldseek plus geometry with calibrated abstention, fold-controlled contrasts, near-orphan evaluation rows, and proposal-only v2 sublabel strata. Sparse and misleading structural cells need targeted labels before any mechanism-prediction claim.

## Track Snapshot

| Track | Primary accuracy | Primary macro F1 | OOS FP rate | Heldout rows joined |
| --- | ---: | ---: | ---: | ---: |
| Foldseek full-structure NN | 0.622 | 0.765 | 0.087 | 140/140 |
| ESM-2 150M logistic | 0.578 | 0.696 | 0.168 | 140/140 |
| ESM-C 300M corrected logistic | 0.378 | 0.460 | 0.168 | 140/140 |
| ProtT5 Swiss-Prot H5 cosine NN | 0.395 | 0.576 | 0.230 | 132/140 |
| SaProt 35M structure-token NN | 0.333 | 0.513 | 0.196 | 140/140 |
| Foldseek 3Di token 3-mer NN | 0.178 | 0.313 | 0.196 | 139/140 |
| Active-site geometry baseline | n/a | n/a | n/a | 135/140 |
| Sequence-NN 3-mer Jaccard | 0.156 | n/a | 0.272 | 140/140 |

## Structural-Neighborhood Bins

| Bin | Rows | Foldseek primary acc | ESM-2 primary acc | Geometry primary acc | Sequence-NN primary acc |
| --- | ---: | ---: | ---: | ---: | ---: |
| broad_bucket_ambiguous | 89 | n/a | n/a | n/a | n/a |
| dense_same_mechanism_structural_neighborhood | 10 | 1.000 | 0.700 | 1.000 | 0.100 |
| high_structure_similarity_different_fingerprint | 5 | n/a | n/a | n/a | n/a |
| low_structure_neighborhood_near_orphan | 30 | 0.600 | 0.533 | 1.000 | 0.167 |
| no_reliable_structure | 6 | 0.000 | 0.600 | n/a | 0.200 |

## Diagnostic Cases

- Foldseek fails while ESM-2, ESM-C, SaProt, ProtT5, or geometry succeeds: 15 primary heldout rows.
- Foldseek succeeds while all available learned sequence/structure reps fail: 2 primary heldout rows.
- Fold-controlled contrast candidates: 6 rows.
- Near-orphan/orphan candidates: 35 rows.
- Rows where proposal-only v2 sublabels are likely needed: 38 rows.

## Input Caveats

ProtT5 has 132/140 heldout rows because Swiss-Prot H5 embeddings are missing for 8 heldout entries. Foldseek 3Di token NN has 139/140 rows. Geometry joins 135/140 heldout entries from an existing 678-row eval artifact rather than a current702-native standardized row export. The retained Foldseek TM artifact is partial pairwise evidence and is used only as a provenance proxy.

No labels, registries, ontology files, thresholds, imports, production scoring, or representation-branch outputs were edited. Source/review context remains provenance/review-only metadata, not a predictive feature.
