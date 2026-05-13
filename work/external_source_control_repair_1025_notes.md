# External Source Control Repair 1025 Notes

The 1,025 external-source path remains review-only and non-countable. The
current repair surface covers heuristic collapse, representation-control
comparison, broad-EC disambiguation, active-site gap sourcing, and sequence
neighborhood controls.

## Current Gate

- `artifacts/v3_external_source_transfer_gate_check_1025.json` passes 38/38
  review-only checks.
- `countable_label_candidate_count` remains 0.
- `ready_for_label_import` remains false.
- Canonical countable labels remain 679.

## Expanded Controls

- Structure mapping now covers all 12 heuristic-ready external candidates:
  `artifacts/v3_external_source_structure_mapping_sample_1025.json` maps 12/12
  with 0 fetch failures.
- Heuristic scoring now covers 12 candidates:
  `artifacts/v3_external_source_heuristic_control_scores_1025.json` reports
  top1 counts of 9 `metal_dependent_hydrolase`, 2 `heme_peroxidase_oxidase`,
  and 1 `flavin_dehydrogenase_reductase`.
- The heuristic score audit keeps the artifact guardrail-clean but records a
  dominant metal-hydrolase top1 fraction of 0.75 and 9 scope/top1 mismatches.
- `artifacts/v3_external_source_control_repair_plan_1025.json` converts the
  observed failures into 25 review-only repair rows: 10 active-site feature
  gaps, 3 broad-EC disambiguation rows, and 12 heuristic-control repair rows.
- `artifacts/v3_external_source_representation_control_manifest_1025.json`
  exposes all 12 mapped controls as future representation rows with embeddings
  explicitly not computed and no countable training labels.
- `artifacts/v3_external_source_representation_control_comparison_1025.json`
  adds a feature-proxy comparison against the heuristic baseline: 7 rows flag
  metal-hydrolase collapse, 2 are glycan-boundary cases, 2 are other
  scope/top1 mismatches, and 1 is scope-consistent. No embeddings or labels are
  created.

## Active-Site Gap Repair

- `artifacts/v3_external_source_binding_context_repair_plan_1025.json` splits
  the 10 active-site feature gaps into 7 rows with binding context ready to map
  and 3 rows that still lack binding context.
- `artifacts/v3_external_source_binding_context_mapping_sample_1025.json` maps
  7/7 binding-context rows with 0 fetch failures. These rows are only repair
  context; binding positions do not replace catalytic active-site evidence.
- `artifacts/v3_external_source_active_site_gap_source_requests_1025.json`
  turns all 10 active-site-feature gaps into source requests: 7 have mapped
  binding context and 3 need curated active-site or catalytic-residue sources.

## Reaction And Sequence Controls

- `artifacts/v3_external_source_reaction_evidence_sample_1025.json` now covers
  all 30 external candidates, querying 45 EC contexts and collecting 64 Rhea
  reaction rows with 0 fetch failures.
- The reaction audit flags 16 broad-EC context rows across `1.1.1.-`,
  `1.11.1.-`, `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and `4.2.99.-`.
- `artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json` narrows
  the 3 broad-only repair rows to specific reaction-context review: all 3 have
  specific reaction context, with 2 requiring substrate selection among multiple
  specific reactions.
- `artifacts/v3_external_source_sequence_holdout_audit_1025.json` keeps
  `O15527` and `P42126` as exact M-CSA reference-overlap holdouts and marks the
  other 28 external candidates as requiring near-duplicate search before any
  future import decision.
- `artifacts/v3_external_source_sequence_neighborhood_plan_1025.json` converts
  the sequence-holdout surface into 2 exact-holdout rows and 28 explicit
  near-duplicate search requests.

## Next Repair Target

Do not import external labels yet. The next bounded work should either:

- source explicit catalytic or active-site residue evidence for the 10
  active-site feature gaps using
  `artifacts/v3_external_source_active_site_gap_source_requests_1025.json`; or
- run/attach real near-duplicate sequence searches for the 28
  `near_duplicate_search_required_before_import` rows; or
- replace the feature-proxy representation comparison with a real learned or
  structure-language representation while keeping heuristic retrieval as the
  required control.
