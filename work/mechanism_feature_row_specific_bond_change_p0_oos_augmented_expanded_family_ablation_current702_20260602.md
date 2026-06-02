# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Expanded Family Ablation - current702

Run: 2026-06-02T11:22:46Z

Calibration-only single-family ablation for the retained-OOS expanded feature families. Each family is materialized separately on the approved train/cal surface, guardrail-audited, and scored with the existing no-template centroid/residual method; heldout remains unread.

## Status

- p0_oos_augmented_expanded_family_ablation_ready
- Candidate feature families: 8
- Families beating coarse residual contract: 0
- Coarse residual OOS abstain recall: 0.5
- Coarse residual AUC: 0.669643
- Critical violations: 0

## Family Ablations

| family | dimensions | OOS abstain recall | residual AUC | recall delta | AUC delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| event_type_sequence | 57 | 0.285714 | 0.598214 | -0.214286 | -0.071429 |
| event_mapped_residue_count | 44 | 0.142857 | 0.508929 | -0.357143 | -0.160714 |
| residue_role_count | 94 | 0.107143 | 0.401786 | -0.392857 | -0.267857 |
| event_participant_arity | 57 | 0.071429 | 0.526786 | -0.428571 | -0.142857 |
| event_residue_code | 73 | 0.035714 | 0.508929 | -0.464286 | -0.160714 |
| event_residue_code_count | 114 | 0.035714 | 0.508929 | -0.464286 | -0.160714 |
| event_residue_role_count | 204 | 0.035714 | 0.357143 | -0.464286 | -0.3125 |
| event_mapped_residue_bucket | 36 | 0.0 | 0.419643 | -0.5 | -0.25 |

## Decision

- Single-family expansion replaces frozen residual contract: False
- Best family by residual OOS abstain recall: event_type_sequence
- Keep existing residual threshold: True
- Next gate: No single ready expanded family beats the coarse residual contract. Do not promote these family-token expansions; next try narrower token-level ablations or regularized calibration while keeping heldout unread.

## Interpretation

- No single retained-OOS expanded feature family beats the coarse residual operating point on calibration OOS abstention while preserving residual AUC.
- Keep the coarse residual threshold frozen and pivot to token-level or regularized feature-family ablations before any heldout read.
