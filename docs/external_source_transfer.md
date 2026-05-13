# External Source Transfer

The 1,025 preview shows that M-CSA-only tranche growth is no longer the right
path to 10,000 countable labels. The current M-CSA slice exposes 1,003 source
records, while the benchmark target is 10,000 countable labels. External-source
transfer is therefore a new methodology, not a continuation of M-CSA label
import.

## Current State

- Canonical countable labels remain at 679.
- The 1,025 preview passes 21/21 label-factory gates but adds 0 clean countable
  labels.
- All 329 preview review-state rows remain non-countable.
- External UniProtKB/Swiss-Prot artifacts are review-only and create 0
  countable label candidates.
- The first read-only external sample has 30 candidates across six query lanes,
  0 fetch failures, and a clean non-countable guardrail audit.
- The external candidate manifest attaches OOD controls, heuristic-control
  requirements, and exact-reference sequence-cluster controls to those 30
  candidates. Two candidates (`O15527` and `P42126`) overlap existing M-CSA
  reference accessions and are routed to holdout controls, not count growth.
  The lane-balance audit is clean: six lanes have five candidates each, so the
  first external sample has not collapsed to one chemistry.
- The external evidence plan/export requests active-site residue evidence,
  curated mechanism/reaction evidence, structure mapping, OOD assignment,
  sequence holdout checks, heuristic retrieval controls, review decisions, and
  full factory gates for every candidate while carrying the sampled PDB and
  AlphaFold structure references forward. It flags seven candidates with broad
  or incomplete EC context, defers three broad-only candidates for specific
  reaction disambiguation, and exports a review-only active-site evidence queue
  with 25 ready candidates and five deferred candidates.

## Immediate Pilot Direction

The next phase is a small external-source import pilot, not more abstract gate
accumulation. New gates or audits should be added only when they directly
remove one blocker to pilot import readiness.

Before any external import attempt, add a sequence/fold-distance holdout
evaluation for the accepted countable registry and 1,000/1,025 slice context.
This should report held-out top1 accuracy, retained top3 accuracy where
applicable, retention, abstention, out-of-scope false non-abstentions, and
per-fingerprint breakdowns separately from the current in-distribution slice
metrics. Use Foldseek/MMseqs2 if available; otherwise use a deterministic local
proxy and state the limitation.

Build toward a 5-10 candidate pilot from the existing 30-row UniProtKB/Swiss-Prot
sample. Keep every external row review-only until active-site, reaction,
sequence, representation, review, and full label-factory gates pass.

Priority blockers:

- source explicit catalytic or active-site residue evidence for the 10
  active-site-feature gap rows;
- complete real near-duplicate or UniRef-style sequence searches for the 28
  rows that still require sequence search;
- replace deterministic k-mer proxy controls with a real learned or
  structure-language representation backend, or a clearly executable backend
  interface with a small computed sample;
- rank the 30 candidates and select 5-10 pilot candidates with explicit
  active-site evidence, specific reaction evidence, clean sequence holdout
  status, clean structure mapping, non-collapsed retrieval/representation
  behavior, and no broad-EC ambiguity;
- export review decisions for those pilot candidates before any countable
  import attempt.
- The active-site evidence pass now samples all 25 ready candidates from
  UniProtKB feature records. It finds active-site features for 15 candidates,
  leaves 10 candidates as active-site-feature gaps, and keeps all rows
  non-countable. A heuristic-control queue then identifies 12 candidates ready
  for structure mapping and defers 13 rows, including 3 broad-EC rows.
- The structure-mapping sample now covers all 12 heuristic-ready external
  candidates on current AlphaFold model CIFs, resolves all requested active-site
  positions, and runs the current geometry-retrieval heuristic as a control.
  The control is intentionally not a label decision: 9/12 scored candidates
  rank `metal_dependent_hydrolase` top1, 2 rank `heme_peroxidase_oxidase`, and
  1 ranks `flavin_dehydrogenase_reductase`. The failure-mode audit records
  active-site feature gaps, broad-EC disambiguation needs, top1 fingerprint
  collapse, metal-hydrolase collapse, and 9 scope/top1 mismatches as review-only
  blockers to label import.
- The external control repair plan converts the current failures into 25
  non-countable repair rows: 10 active-site feature gaps, 3 broad-EC
  disambiguation rows, and 12 heuristic-control repair rows. The representation
  control manifest exposes all 12 mapped controls for future learned or
  structure-language scoring while keeping `embedding_status` as
  `not_computed_interface_only`. The feature-proxy representation comparison
  keeps embeddings uncomputed, flags 7 metal-hydrolase collapse rows, records
  2 glycan-boundary cases, and leaves every row non-countable.
- The binding-context repair path splits the 10 active-site feature gaps into
  7 rows with binding context ready to map and 3 rows without binding context.
  The binding-context mapping sample maps 7/7 ready rows with 0 fetch failures,
  but binding positions remain repair context only and do not replace
  catalytic active-site evidence. The active-site gap source-request artifact
  turns all 10 gaps into explicit review-only sourcing tasks; 7 have mapped
  binding context and 3 need curated residue sources.
- The reaction-context pass now queries Rhea for all 30 external candidates,
  finds 64 reaction records with 0 fetch failures, and keeps every row
  `reaction_context_only` and non-countable because the Rhea rows have not been
  converted into a reviewed decision artifact or full label-factory gate. Its
  guardrail audit is clean and flags 16 broad-EC context rows across
  `1.1.1.-`, `1.11.1.-`, `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and
  `4.2.99.-`. The broad-EC disambiguation audit finds specific reaction
  context for all 3 broad-only repair rows while keeping them review-only.
- The sequence-holdout audit keeps `O15527` and `P42126` as exact M-CSA
  reference-overlap holdouts and marks the remaining 28 candidates as requiring
  near-duplicate search. The sequence-neighborhood plan converts those into
  2 exact-holdout rows and 28 near-duplicate search requests. The bounded
  sequence-neighborhood screen fetches all 30 external sequences and 733
  current countable M-CSA reference sequences, finds 0 high-similarity alerts
  under the current unaligned screen, and still requires complete
  near-duplicate or UniRef-style search before import. The bounded top-hit
  alignment verification checks 90 sequence-neighborhood pairs, confirms the
  two exact-reference holdouts by alignment, finds 88 no-signal top-hit pairs,
  and keeps complete sequence search mandatory.
- The import-readiness audit aggregates the current blockers by candidate: 10
  active-site gaps, 2 exact sequence holdouts, 28 complete near-duplicate
  search requirements, 9 heuristic scope/top1 mismatches, and 29
  representation-control issues. The active-site sourcing queue turns the 10
  active-site gaps into 7 mapped-binding-context sourcing rows and 3
  primary-source rows, and the active-site sourcing export packages 72 source
  targets without decisions. The active-site sourcing resolution re-checks all
  10 active-site-gap rows against UniProt feature evidence, finds 0 explicit
  active-site residue sources, and leaves the rows non-countable. The
  sequence-search export keeps all 30 candidates
  in no-decision sequence controls, with 28 complete near-duplicate searches and
  2 sequence holdouts. The representation-backend plan covers 12 mapped controls
  without computing embeddings, and the representation-backend sample computes a
  deterministic sequence k-mer control for those 12 rows while flagging 1
  representation near-duplicate holdout. The transfer blocker matrix joins all 30
  candidates into a review-only next-action worklist and now carries the
  resolution/sample row evidence directly: 7 rows move to primary
  literature/PDB active-site source review, 3 remain primary active-site source
  tasks, 18 require near-duplicate sequence search, and 2 stay sequence
  holdouts. Its dominant next-action fraction is 0.6000 and dominant lane
  fraction is 0.1667, so the queue has not collapsed to one action or chemistry
  lane. The external transfer gate passes 59/59 review-only checks and remains
  not ready for label import.

## Artifacts

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-source-scale-limits \
  --graph artifacts/v1_graph_1025.json \
  --prior-graph artifacts/v1_graph_1000.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --review-debt artifacts/v3_review_debt_summary_1025_preview.json \
  --label-expansion-candidates artifacts/v3_label_expansion_candidates_1025.json \
  --target-source-entries 1025 \
  --public-target-countable-labels 10000 \
  --out artifacts/v3_source_scale_limit_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-transfer-manifest \
  --source-scale-audit artifacts/v3_source_scale_limit_audit_1025.json \
  --learned-retrieval-manifest artifacts/v3_learned_retrieval_manifest_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_1025.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_1025_preview_batch.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_source_transfer_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-query-manifest \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_1025.json \
  --max-lanes 8 \
  --out artifacts/v3_external_source_query_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-ood-calibration-plan \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_ood_calibration_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-candidate-sample \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --max-records-per-lane 5 \
  --out artifacts/v3_external_source_candidate_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-candidate-sample \
  --candidate-sample artifacts/v3_external_source_candidate_sample_1025.json \
  --out artifacts/v3_external_source_candidate_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-candidate-manifest \
  --candidate-sample artifacts/v3_external_source_candidate_sample_1025.json \
  --ood-calibration-plan artifacts/v3_external_ood_calibration_plan_1025.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --out artifacts/v3_external_source_candidate_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-candidate-manifest \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --out artifacts/v3_external_source_candidate_manifest_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-lane-balance \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --min-lanes 3 \
  --max-dominant-lane-fraction 0.6 \
  --out artifacts/v3_external_source_lane_balance_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-evidence-plan \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --candidate-manifest-audit artifacts/v3_external_source_candidate_manifest_audit_1025.json \
  --out artifacts/v3_external_source_evidence_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-evidence-request-export \
  --evidence-plan artifacts/v3_external_source_evidence_plan_1025.json \
  --max-rows 50 \
  --out artifacts/v3_external_source_evidence_request_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-evidence-queue \
  --evidence-plan artifacts/v3_external_source_evidence_plan_1025.json \
  --max-rows 50 \
  --out artifacts/v3_external_source_active_site_evidence_queue_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-evidence-sample \
  --active-site-evidence-queue artifacts/v3_external_source_active_site_evidence_queue_1025.json \
  --max-candidates 25 \
  --out artifacts/v3_external_source_active_site_evidence_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-evidence-sample \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --out artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-heuristic-control-queue \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --max-rows 25 \
  --out artifacts/v3_external_source_heuristic_control_queue_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-heuristic-control-queue \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --out artifacts/v3_external_source_heuristic_control_queue_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-structure-mapping-plan \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --max-rows 25 \
  --out artifacts/v3_external_source_structure_mapping_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-structure-mapping-plan \
  --structure-mapping-plan artifacts/v3_external_source_structure_mapping_plan_1025.json \
  --out artifacts/v3_external_source_structure_mapping_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-structure-mapping-sample \
  --structure-mapping-plan artifacts/v3_external_source_structure_mapping_plan_1025.json \
  --max-candidates 12 \
  --out artifacts/v3_external_source_structure_mapping_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-structure-mapping-sample \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --out artifacts/v3_external_source_structure_mapping_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-heuristic-control-scores \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --top-k 5 \
  --out artifacts/v3_external_source_heuristic_control_scores_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-heuristic-control-scores \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --out artifacts/v3_external_source_heuristic_control_scores_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-failure-modes \
  --active-site-evidence-sample-audit artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --heuristic-control-scores-audit artifacts/v3_external_source_heuristic_control_scores_audit_1025.json \
  --structure-mapping-sample-audit artifacts/v3_external_source_structure_mapping_sample_audit_1025.json \
  --out artifacts/v3_external_source_failure_mode_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-control-repair-plan \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --heuristic-control-scores-audit artifacts/v3_external_source_heuristic_control_scores_audit_1025.json \
  --external-failure-mode-audit artifacts/v3_external_source_failure_mode_audit_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_control_repair_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-control-repair-plan \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --external-failure-mode-audit artifacts/v3_external_source_failure_mode_audit_1025.json \
  --out artifacts/v3_external_source_control_repair_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-control-manifest \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_representation_control_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-control-manifest \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --out artifacts/v3_external_source_representation_control_manifest_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-binding-context-repair-plan \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_binding_context_repair_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-binding-context-repair-plan \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --out artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-binding-context-mapping-sample \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --max-candidates 7 \
  --out artifacts/v3_external_source_binding_context_mapping_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-binding-context-mapping-sample \
  --binding-context-mapping-sample artifacts/v3_external_source_binding_context_mapping_sample_1025.json \
  --out artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-gap-source-requests \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --binding-context-mapping-sample artifacts/v3_external_source_binding_context_mapping_sample_1025.json \
  --out artifacts/v3_external_source_active_site_gap_source_requests_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-holdouts \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_sequence_holdout_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-neighborhood-plan \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --sequence-holdout-audit artifacts/v3_external_source_sequence_holdout_audit_1025.json \
  --out artifacts/v3_external_source_sequence_neighborhood_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-neighborhood-sample \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --max-external-rows 30 \
  --max-reference-sequences 1000 \
  --top-k 3 \
  --out artifacts/v3_external_source_sequence_neighborhood_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-neighborhood-sample \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --out artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-alignment-verification \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --top-k 3 \
  --max-pairs 120 \
  --out artifacts/v3_external_source_sequence_alignment_verification_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-alignment-verification \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --out artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-search-export \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --out artifacts/v3_external_source_sequence_search_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-search-export \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --out artifacts/v3_external_source_sequence_search_export_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-reaction-evidence-sample \
  --evidence-request-export artifacts/v3_external_source_evidence_request_export_1025.json \
  --max-candidates 30 \
  --max-reactions-per-ec 2 \
  --out artifacts/v3_external_source_reaction_evidence_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-reaction-evidence-sample \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-control-comparison \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_representation_control_comparison_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-control-comparison \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --out artifacts/v3_external_source_representation_control_comparison_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-plan \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --out artifacts/v3_external_source_representation_backend_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-plan \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --out artifacts/v3_external_source_representation_backend_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --out artifacts/v3_external_source_representation_backend_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --out artifacts/v3_external_source_representation_backend_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-broad-ec-disambiguation \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-import-readiness \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --out artifacts/v3_external_source_import_readiness_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-sourcing-queue \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_queue_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-sourcing-queue \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-sourcing-export \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-sourcing-export \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-sourcing-resolution \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_resolution_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-sourcing-resolution \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-transfer-blocker-matrix \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --out artifacts/v3_external_source_transfer_blocker_matrix_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-transfer-blocker-matrix \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --out artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-review-only-import-safety \
  --labels data/registries/curated_mechanism_labels.json \
  --review artifacts/v3_external_source_evidence_request_export_1025.json \
  --out artifacts/v3_external_source_review_only_import_safety_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli check-external-source-transfer-gates \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --ood-calibration-plan artifacts/v3_external_ood_calibration_plan_1025.json \
  --candidate-sample-audit artifacts/v3_external_source_candidate_sample_audit_1025.json \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --candidate-manifest-audit artifacts/v3_external_source_candidate_manifest_audit_1025.json \
  --lane-balance-audit artifacts/v3_external_source_lane_balance_audit_1025.json \
  --evidence-plan artifacts/v3_external_source_evidence_plan_1025.json \
  --evidence-request-export artifacts/v3_external_source_evidence_request_export_1025.json \
  --review-only-import-safety-audit artifacts/v3_external_source_review_only_import_safety_audit_1025.json \
  --active-site-evidence-queue artifacts/v3_external_source_active_site_evidence_queue_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --active-site-evidence-sample-audit artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --heuristic-control-queue-audit artifacts/v3_external_source_heuristic_control_queue_audit_1025.json \
  --structure-mapping-plan artifacts/v3_external_source_structure_mapping_plan_1025.json \
  --structure-mapping-plan-audit artifacts/v3_external_source_structure_mapping_plan_audit_1025.json \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --structure-mapping-sample-audit artifacts/v3_external_source_structure_mapping_sample_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --heuristic-control-scores-audit artifacts/v3_external_source_heuristic_control_scores_audit_1025.json \
  --external-failure-mode-audit artifacts/v3_external_source_failure_mode_audit_1025.json \
  --external-control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --external-control-repair-plan-audit artifacts/v3_external_source_control_repair_plan_audit_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --reaction-evidence-sample-audit artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --representation-control-manifest-audit artifacts/v3_external_source_representation_control_manifest_audit_1025.json \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --representation-control-comparison-audit artifacts/v3_external_source_representation_control_comparison_audit_1025.json \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --representation-backend-plan-audit artifacts/v3_external_source_representation_backend_plan_audit_1025.json \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --representation-backend-sample-audit artifacts/v3_external_source_representation_backend_sample_audit_1025.json \
  --broad-ec-disambiguation-audit artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-neighborhood-sample-audit artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --sequence-alignment-verification-audit artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --sequence-search-export-audit artifacts/v3_external_source_sequence_search_export_audit_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --active-site-sourcing-queue-audit artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --active-site-sourcing-export-audit artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --active-site-sourcing-resolution-audit artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --transfer-blocker-matrix-audit artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --binding-context-repair-plan-audit artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json \
  --binding-context-mapping-sample artifacts/v3_external_source_binding_context_mapping_sample_1025.json \
  --binding-context-mapping-sample-audit artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json \
  --sequence-holdout-audit artifacts/v3_external_source_sequence_holdout_audit_1025.json \
  --out artifacts/v3_external_source_transfer_gate_check_1025.json
```

## Guardrails

External-source artifacts are not label registries. They must remain
non-countable until a future run builds explicit external candidate evidence
and then passes OOD calibration, sequence-similarity failure controls, review
exports, decision artifacts, heuristic control comparison, and the full
label-factory gate. The current gate only authorizes review-only evidence
collection.

Do not import external candidates directly into
`data/registries/curated_mechanism_labels.json`. The first safe external-source
milestone is a review-only candidate manifest and evidence-request export that
can fail cleanly without changing the benchmark label count.
