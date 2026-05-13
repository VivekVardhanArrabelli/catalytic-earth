# External Source Control Repair 1025 Notes

The 1,025 external-source path remains review-only and non-countable. The
current repair surface covers heuristic collapse, representation-control
comparison, broad-EC disambiguation, active-site gap sourcing/export,
active-site sourcing resolution, sequence-search export, representation-backend
planning/sample, a candidate blocker matrix, candidate-lineage validation, a
review-only pilot priority worklist, no-decision review packet export, and a
consolidated pilot evidence packet with review-only dossier safeguards.

## Current Gate

- `artifacts/v3_external_source_transfer_gate_check_1025.json` passes 65/65
  review-only checks under `ExternalSourceTransferGateInputs.v1`.
- `countable_label_candidate_count` remains 0.
- `ready_for_label_import` remains false.
- `artifacts/v3_external_source_pilot_candidate_priority_1025.json` selects 10
  non-countable review candidates and defers holdout or near-duplicate rows.
- `artifacts/v3_external_source_pilot_review_decision_export_1025.json` exports
  those rows as no-decision packets with 0 completed decisions.
- `artifacts/v3_external_source_pilot_evidence_packet_1025.json` consolidates
  79 source targets for those rows, with all 10 sequence-search packets and 3
  active-site sourcing packets carried forward.
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
- `artifacts/v3_external_source_kmer_representation_backend_sample_1025.json`
  preserves a computed deterministic sequence k-mer baseline for all 12 planned
  representation rows. It is review-only, flags 1 representation near-duplicate
  holdout, and stays a proxy control.
- `artifacts/v3_external_source_representation_backend_sample_1025.json` adds
  the canonical 12-row ESM-2 representation sample. It is review-only, flags 3
  representation near-duplicate holdouts, emits learned-vs-heuristic
  disagreements, and keeps all rows non-countable.

## Active-Site Gap Repair

- `artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`
  re-checks the 10 active-site-gap rows against UniProt feature evidence: 7 rows
  have binding plus reaction context only, 3 have reaction context only, and 0
  expose explicit active-site residue positions.

- `artifacts/v3_external_source_binding_context_repair_plan_1025.json` splits
  the 10 active-site feature gaps into 7 rows with binding context ready to map
  and 3 rows that still lack binding context.
- `artifacts/v3_external_source_binding_context_mapping_sample_1025.json` maps
  7/7 binding-context rows with 0 fetch failures. These rows are only repair
  context; binding positions do not replace catalytic active-site evidence.
- `artifacts/v3_external_source_active_site_gap_source_requests_1025.json`
  turns all 10 active-site-feature gaps into source requests: 7 have mapped
  binding context and 3 need curated active-site or catalytic-residue sources.
- `artifacts/v3_external_source_active_site_sourcing_queue_1025.json`
  prioritizes those 10 gaps into 7 mapped-binding-context sourcing rows and 3
  primary active-site source rows, all non-countable.
- `artifacts/v3_external_source_active_site_sourcing_export_1025.json` packages
  those rows into source-review packets with 72 source targets and 0 completed
  decisions.

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
- `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json` fetches
  sequences for all 30 external rows and 733 current countable M-CSA reference
  sequences. It records 0 high-similarity hits in the bounded unaligned screen,
  retains the 2 exact-reference holdouts, and keeps full near-duplicate or
  UniRef-style search as required before import.
- `artifacts/v3_external_source_sequence_alignment_verification_1025.json`
  checks the top 90 sequence-neighborhood pairs, confirms the two
  exact-reference holdouts by alignment, records 88 no-signal pairs, and
  remains a bounded review-only control.
- `artifacts/v3_external_source_sequence_search_export_1025.json` keeps all 30
  external rows in no-decision sequence controls, with 28 complete
  near-duplicate searches and 2 sequence holdout tasks.

## Import Readiness

- `artifacts/v3_external_source_import_readiness_audit_1025.json` keeps all 30
  external rows non-countable and import-blocked.
- The readiness audit records 10 active-site-gap rows, 2 sequence holdouts, 28
  rows still requiring complete near-duplicate search, 9 heuristic scope/top1
  mismatches, 29 representation-control issues, and 2 alignment-confirmed
  sequence holdouts.
- Readiness buckets are: 10 blocked by active-site sourcing, 11 blocked by
  heuristic controls, 6 blocked by representation controls, 2 blocked by
  sequence holdouts, and 1 blocked by sequence search.
- `artifacts/v3_external_source_representation_backend_plan_1025.json` keeps 12
  mapped controls ready for backend selection but explicitly unembedded.
- `artifacts/v3_external_source_transfer_blocker_matrix_1025.json` joins all 30
  candidates into a non-countable blocker matrix: 7 primary literature/PDB
  active-site source reviews after the UniProt re-check found no explicit
  positions, 3 primary-source tasks, 18 near-duplicate sequence searches, and 2
  sequence holdouts as prioritized actions. The matrix now carries active-site
  resolution and representation sample statuses directly. The dominant action
  fraction is 0.6000 and the dominant lane fraction is 0.1667, so this queue has
  not collapsed to one action or chemistry lane.
- Remaining-time plan executed for the 2026-05-13T03:08:55-05:00 run: after
  the sequence screen and import-readiness audit passed targeted tests, keep
  work bounded to artifact regression coverage, docs, validation, and final
  gate verification rather than opening any external label decision.

## Next Repair Target

Do not import external labels yet. The next bounded work should either:

- source explicit catalytic or active-site residue evidence for the 10
  active-site feature gaps using
  `artifacts/v3_external_source_active_site_sourcing_export_1025.json`; or
- run/attach real near-duplicate sequence searches for the 28
  `near_duplicate_search_required_before_import` rows in
  `artifacts/v3_external_source_sequence_search_export_1025.json`; or
- select/run a real learned or structure-language representation backend from
  `artifacts/v3_external_source_representation_backend_plan_1025.json` while
  keeping heuristic retrieval as the required control.
