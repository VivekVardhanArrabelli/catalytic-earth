# Countable Label Unblocker Matrix - current702 - 20260608

- Created UTC: `2026-06-08T21:44:52Z`
- JSON artifact: `artifacts/v3_countable_label_unblocker_matrix_current702_20260608.json`
- Source surface: `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`

## Result

The unblocker consumed the non-reject canonical candidates from the merged scale-out surface and classified each row into a terminal machine action. No registry, import, sidecar, coordinate, ontology, threshold, model, split, training, or tuning surface was changed.

- Target canonical rows: `523`
- Target source-member rows: `1105`
- Merged source rows reconciled: `4820`
- Import-preview candidates: `0`
- Rows with `ready_for_label_import=True`: `0`
- Rows with `countable_label_candidate=True`: `0`
- Current-registry overlap blockers: `37`
- Positive duplicate-screen blockers: `17`
- Rows with local coordinate files found: `255`
- Rows with approved locator matches: `12`

## Input Terminal Counts

- `blocked_coordinate`: 24
- `blocked_family_decision`: 134
- `blocked_locator`: 85
- `review_only_evidence`: 280

## Target Source-Member Counts

- `blocked_coordinate`: 94
- `blocked_family_decision`: 142
- `blocked_locator`: 231
- `review_only_evidence`: 638

## Unblock Classification Counts

- `coordinate_repair_candidate`: 2
- `family_default_resolved`: 102
- `hard_blocked_with_next_action`: 273
- `locator_repair_candidate`: 96
- `reject/OOS_preserve_signal`: 14
- `true_expert_only`: 36

## Classification By Input State

| Unblock classification | Input terminal mix |
| --- | --- |
| `coordinate_repair_candidate` | `blocked_coordinate`=2 |
| `family_default_resolved` | `blocked_family_decision`=102 |
| `hard_blocked_with_next_action` | `blocked_coordinate`=1, `blocked_family_decision`=22, `blocked_locator`=2, `review_only_evidence`=248 |
| `locator_repair_candidate` | `blocked_coordinate`=21, `blocked_locator`=75 |
| `reject/OOS_preserve_signal` | `blocked_locator`=8, `review_only_evidence`=6 |
| `true_expert_only` | `blocked_family_decision`=10, `review_only_evidence`=26 |

## Import Preview

- None. No target row had both `ready_for_label_import=True` and `countable_label_candidate=True`, and duplicate/current-registry screens still block several otherwise informative rows.

## Mechanical Findings

- Review-only rows are not countable by default: they carry evidence but no source gate grants import-preview authority in this surface.
- Family-decision rows are split between existing policy/default no-import resolutions, exact expert-only decisions, and hard missing source-free family evidence.
- Locator rows remain repair candidates unless a current duplicate signal or exact current-registry overlap blocks them earlier.
- Coordinate rows with local coordinate files were moved to locator repair; rows without local coordinates remain coordinate repair candidates.

## Representative Next Actions

- `coordinate_repair_candidate` sample `m_csa:946`: materialize or hash-match coordinate provenance before locator and import-gate review
- `family_default_resolved` sample `m_csa:760`: apply existing family policy: keep non-counting until source-free active-site/substrate-mode evidence and gates pass
- `hard_blocked_with_next_action` sample `m_csa:1001`: keep review-only; run a controlled promotion/import-preview gate before any countable use
- `locator_repair_candidate` sample `m_csa:1005`: repair or approve a source-free active-site locator, then rerun duplicate and label-factory gates
- `reject/OOS_preserve_signal` sample `m_csa:955`: preserve the current duplicate-screen signal as non-counting evidence; do not import
- `true_expert_only` sample `m_csa:510`: keep review-only until explicit expert promotion request and full gates exist

## Validation

- Validation passed: `True`
- Target counts match merged surface: `True`
- Merged source rows reconcile to canonical members: `True`
- Required row fields present: `True`
