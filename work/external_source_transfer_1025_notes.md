# External Source Transfer 1025 Notes

The 1,025 preview is not promotable and should stay a source-limit audit point:
it adds 0 countable labels and leaves the canonical registry at 679 labels.
External-source transfer is now the active path for post-M-CSA scaling work, but
all current artifacts are review-only.

Current review-only external artifacts:

- `artifacts/v3_external_source_candidate_manifest_1025.json` carries 30
  UniProtKB/Swiss-Prot candidates across six lanes with 0 countable candidates.
- `artifacts/v3_external_source_lane_balance_audit_1025.json` is clean: each
  lane contributes five candidates and the dominant-lane fraction is `0.1667`.
- `artifacts/v3_external_source_candidate_manifest_audit_1025.json` is clean and
  confirms 0 rows are marked ready for label import.
- `artifacts/v3_external_source_evidence_plan_1025.json` requests active-site
  residue positions, curated reaction or mechanism evidence, structure mapping,
  heuristic geometry controls, OOD assignment, sequence holdouts, review
  decisions, and full label-factory gates before import. It flags seven broad
  or incomplete EC-context candidates and routes three broad-only candidates to
  reaction disambiguation before active-site mapping.
- `artifacts/v3_external_source_evidence_request_export_1025.json` exports 30
  no-decision review items and is marked `external_source_review_only`.
- `artifacts/v3_external_source_active_site_evidence_queue_1025.json` prioritizes
  25 review-only candidates for active-site evidence collection and defers five
  rows: two exact-reference holdouts and three broad-EC disambiguation cases.
- `artifacts/v3_external_source_active_site_evidence_sample_1025.json` samples
  all 25 ready rows from UniProtKB features: 15 have active-site features, 10
  are active-site-feature gaps, all 25 have catalytic-activity comments, and 0
  rows are countable or import-ready. The current active-site feature-gap
  accessions are `O60568`, `P29372`, `P27144`, `A2RUC4`, `P51580`, `O95050`,
  `Q9HBK9`, `A5PLL7`, `P32189`, and `Q32P41`.
- `artifacts/v3_external_source_heuristic_control_queue_1025.json` marks 12
  candidates ready for heuristic-control prototyping and defers 13 rows: 10
  active-site-feature gaps and 3 broad-EC disambiguation cases.
- `artifacts/v3_external_source_structure_mapping_plan_1025.json` carries 12
  candidates into structure mapping and keeps 13 deferred.
  `artifacts/v3_external_source_structure_mapping_sample_1025.json` maps all
  12 heuristic-ready candidates onto current AlphaFold CIFs with 0 fetch
  failures and 0 countable labels.
- `artifacts/v3_external_source_heuristic_control_scores_1025.json` runs the
  current geometry-retrieval heuristic on those 12 mapped controls. The top1
  predictions are 9 `metal_dependent_hydrolase`, 2
  `heme_peroxidase_oxidase`, and 1 `flavin_dehydrogenase_reductase`, so
  `artifacts/v3_external_source_failure_mode_audit_1025.json` records top1
  fingerprint collapse, metal-hydrolase collapse, and scope/top1 mismatch as
  review-only failure modes before any external decision artifact can count.
  The audit now records 9 scope/top1 mismatches; glycan-chemistry hydrolase
  controls are tracked separately from non-hydrolase transferase, isomerase,
  lyase, and oxidoreductase mismatch lanes.
- `artifacts/v3_external_source_control_repair_plan_1025.json` turns those
  weaknesses into 25 non-countable repair rows: 10 active-site feature gaps, 3
  broad-EC disambiguation rows, and 12 heuristic-control repair rows.
- `artifacts/v3_external_source_representation_control_manifest_1025.json`
  exposes all 12 mapped controls as future representation rows. Embeddings are
  explicitly not computed, and no row is a training label.
- `artifacts/v3_external_source_representation_control_comparison_1025.json`
  compares feature-proxy controls against the heuristic baseline without
  computing embeddings. It flags 7 metal-hydrolase collapse rows, keeps 2
  glycan-boundary rows as review-only, and creates 0 countable labels.
- `artifacts/v3_external_source_binding_context_repair_plan_1025.json` splits
  the 10 active-site-feature gaps into 7 rows ready for binding-context mapping
  and 3 rows still missing binding context.
- `artifacts/v3_external_source_binding_context_mapping_sample_1025.json` maps
  7/7 binding-context repair rows with 0 fetch failures. These mapped binding
  positions remain repair context only; they are not catalytic active-site
  evidence.
- `artifacts/v3_external_source_active_site_gap_source_requests_1025.json`
  converts all 10 active-site-feature gaps into sourcing requests: 7 have
  mapped binding context and 3 need curated residue sources.
- `artifacts/v3_external_source_review_only_import_safety_audit_1025.json`
  confirms countable import adds 0 labels from that export.
- `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json` runs a
  bounded sequence screen against 733 current countable M-CSA reference
  sequences. It fetches all 30 external sequences, records 0 high-similarity
  alerts under the current unaligned screen, retains the 2 exact-reference
  holdouts, and keeps complete near-duplicate search as a mandatory future
  control.
- `artifacts/v3_external_source_import_readiness_audit_1025.json` aggregates
  candidate-level blockers: 10 active-site gaps, 2 sequence holdouts, 28
  complete near-duplicate search requirements, 9 heuristic scope/top1
  mismatches, and 29 representation-control issues. It marks 0 rows ready for
  label import.
- `artifacts/v3_external_source_transfer_gate_check_1025.json` passes 33/33
  checks for review-only evidence collection in the earlier control-repair
  pass; the current gate passes 38/38 after representation comparison,
  broad-EC disambiguation, active-site gap source requests, and
  sequence-neighborhood controls, and now passes 41/41 after the sequence
  screen and import-readiness audit. It is still not ready for label
  import.

Sequence-similarity guardrail details:

- `O15527` overlaps `m_csa:185` and must stay a sequence-holdout control.
- `P42126` overlaps `m_csa:341` and must stay a sequence-holdout control.
- No external candidate is countable from exact-reference or lane membership
  alone.
- `artifacts/v3_external_source_sequence_neighborhood_plan_1025.json` turns the
  current sequence surface into 2 exact-holdout rows and 28 near-duplicate
  search requests.
- `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json` is a
  bounded sequence screen only, not a final homology search. Absence of a
  high-similarity hit in that artifact must not be used as import evidence.

Reaction-context details:

- `artifacts/v3_external_source_reaction_evidence_sample_1025.json` queries Rhea
  for all 30 external candidates and records 64 reaction-context rows with 0
  fetch failures.
- `artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json` is
  guardrail-clean, with 0 countable candidates and 0 import-ready rows.
- The audit flags 16 broad-EC context rows across `1.1.1.-`, `1.11.1.-`,
  `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and `4.2.99.-`. Treat those
  rows as weak reaction context only, not specific mechanism evidence.
- `artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json` finds
  specific reaction context for all 3 broad-only repair rows; 2 still require
  substrate selection among multiple specific reactions.

Sequence-holdout details:

- `artifacts/v3_external_source_sequence_holdout_audit_1025.json` keeps
  `O15527` and `P42126` as exact-reference holdouts and marks the other 28
  external candidates for near-duplicate search before any future import
  decision.

Next bounded work should keep repairing external-control weaknesses before any
external label decision: source explicit catalytic residues for the 10
active-site-feature gaps, run near-duplicate sequence searches for 28 rows, or
replace the feature-proxy representation comparison with real learned or
structure-language controls.
