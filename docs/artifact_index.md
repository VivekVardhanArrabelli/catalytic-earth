# Artifact Index

This index maps important artifacts to the question they answer. It also marks
artifacts that are historical, superseded, or confounded for current decisions.

Status terms:

- Current gate: use for the next decision unless a newer decision log entry says
  otherwise.
- Trusted contract: source-of-truth constraints or benchmark definitions.
- Diagnostic: useful for analysis, but not enough alone for a gate decision.
- Historical/superseded/confounded: read only through the caveat stated here.

## Start Here

| Artifact | Answers | Status |
| --- | --- | --- |
| `docs/project_state.md` | What is the current north star, benchmark state, trusted result set, and next gate? | Current orientation |
| `docs/decision_log.md` | Which dated decisions override older artifact wording? | Current orientation |
| `docs/agent_runbook.md` | How should an agent run bounded work safely? | Current orientation |
| `README.md` | What is this repo and how do I get started? | Front door |

## Current Benchmark Contracts

| Artifact | Answers | Status |
| --- | --- | --- |
| `data/registries/curated_mechanism_labels.json` | What labels are canonical now? | Source of truth; read-only unless explicitly asked |
| `data/registries/mechanism_fingerprints.json` | What fingerprints exist? | Source of truth; do not edit in routine runs |
| `data/registries/mechanism_ontology.json` | What ontology/family structure exists? | Source of truth; do not edit in routine runs |
| `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json` | Which 702 labels, sequences, and split assignments formed the current sequence benchmark? | Trusted with readthrough caveat for `m_csa:497` and `m_csa:750` |
| `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json` | What repaired split assignment supports current702? | Trusted |
| `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json` | Which v1 fingerprints are primary versus secondary? | Trusted contract |
| `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json` | How must OOS, diversity, pooling, and win conditions be reported? | Trusted contract |

## Wave 1 And Representation Diagnostics

| Artifact | Answers | Status |
| --- | --- | --- |
| `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json` | Did geometry join policy or decoder choice confound Wave 1, and what is the current representation x decoder comparison? | Current gate |
| `work/wave1_2_decoder_join_confound_audit_702_20260528.md` | Human-readable Wave 1.2 audit report and recommendation | Current gate |
| `artifacts/v3_wave1_1_model_by_cell_report_702_20260528.json` | Which diagnostic cells showed model value or failure patterns before the Wave 1.2 correction? | Diagnostic; read with Wave 1.2 |
| `artifacts/v3_wave1_representation_shootout_result_card_20260526.json` | What was the original broad Wave 1 result card? | Historical; superseded for gate decisions |
| `docs/wave1_representation_shootout.md` | Human summary of the original Wave 1 representation shootout | Historical; contains pre-audit caveats |
| `artifacts/v3_sequence_nn_metrics_current702_20260525.json` | What did the deterministic 3-mer sequence-NN smoke baseline show? | Trusted smoke baseline, not PLM evidence |

## D11 Novelty And Northstar Levers

| Artifact | Answers | Status |
| --- | --- | --- |
| `artifacts/v3_mechanism_abstention_gate_eval_predicted_atlas_current702_20260601.json` | Does the predicted-geometry atlas-percentile two-channel gate run after adding in-distribution atlas rows? | Current deployment-regime rerun |
| `artifacts/v3_fold_level_novelty_signal_current702_20260601.json` | Does the frozen selected-PDB Foldseek proxy add a fold-level novelty signal for OOS and cofactor-confounded rows? | Diagnostic; selected-PDB fold proxy, not predicted-Foldseek deployment signal |
| `artifacts/v3_learned_mechanism_feature_embedding_plan_current702_20260601.json` | What leakage-safe scaffold and feature gaps exist for a learned mechanism-feature embedding? | Current scaffold/plan |
| `artifacts/v3_family_set_expansion_targets_current702_20260601.json` | Which targeted family expansions de-risk the 8-fingerprint bound without imports? | Proposal-only; no label/import mutation |

## Geometry And Active-Site Evidence

| Artifact | Answers | Status |
| --- | --- | --- |
| `artifacts/v3_geometry_features_1025.json` | What active-site geometry descriptors exist for the 1,025 preview surface? | Trusted existing feature source |
| `artifacts/v3_geometry_retrieval_1025.json` | What did geometry retrieval produce on the 1,025 surface? | Trusted existing retrieval source |
| `artifacts/v3_geometry_label_eval_1025_preview_batch.json` | What is the existing geometry abstention threshold source? | Trusted for threshold source; not current702-native heldout join |
| `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json` | Does the clean experimental-geometry 45/45 hand-router result survive AlphaFoldDB-predicted geometry? | Current diagnostic; shows predicted-geometry degradation |
| `artifacts/v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601.json` | What predicted-geometry retrieval rows are available for current702 in-distribution atlas percentile/novelty methods? | Current deployment-regime atlas retrieval |
| `artifacts/v3_predicted_geometry_robustness_audit_current702_esmfold_20260529.json` | Was ESMFold available locally for the same predicted-geometry audit? | Blocked; no local runtime/weights and no large download attempted |
| `artifacts/v3_selected_pdb_override_plan_700.json` | Which selected-PDB override path was planned? | Repair evidence |
| `docs/geometry_features.md` | What does the geometry feature layer mean? | Design/reference doc |

## Label Factory, Review, And Imports

| Artifact | Answers | Status |
| --- | --- | --- |
| `docs/label_factory.md` | What are the label schema and gate expectations? | Current reference |
| `artifacts/v3_mcsa_ai_visual_review_support_index_20260524.json` | How should the AI-visual review surface be navigated? | Review-only |
| `artifacts/v3_mcsa_ai_visual_remaining_manual_expert_holds_index_20260525.json` | Which exact manual/expert holds remain after the exact40 follow-up? | Review-only |
| `artifacts/v3_mcsa_positive_clean9_import_preview_20260523.json` | Which nine M-CSA positive rows were gated/imported in clean9? | Trusted import record |
| `artifacts/v3_mcsa_ai_visual_clean10_accept7_vivek_20260524_import_summary.json` | Which seven clean10 AI-visual accept rows were imported? | Trusted import record |
| `artifacts/v3_mcsa_positive_holo_override_import_preview_20260523.json` | Were selected-PDB override rows ready for import at that time? | Review/repair preview; not import authorization |

## Row-Level Override Decisions

| Artifact | Answers | Status |
| --- | --- | --- |
| `artifacts/v3_m_csa497_label_revision_702_20260527.json` | Why is `m_csa:497` OOS now? | Current decision |
| `artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json` | How did the `m_csa:497` relabel affect Wave 1 metrics? | Current readthrough addendum |
| `artifacts/v3_m_csa750_label_revision_702_20260527.json` | Why is `m_csa:750` OOS now? | Current decision |
| `artifacts/v3_m_csa750_wave1_metric_canary_impact_702_20260527.json` | Why must `m_csa:750` be removed from canary use? | Current readthrough addendum |
| `artifacts/v3_packet1_wave1_decision_closure_702_20260527.json` | Which Packet 1 / Wave 1 stale cells are closed? | Current closure |

## FMO Secondary Work

| Artifact | Answers | Status |
| --- | --- | --- |
| `artifacts/v3_fmo_source_evidence_scout_702_20260527.json` | Which local and source-only FMO-like rows have evidence? | Review-only source evidence |
| `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json` | What would a future FMO child/primary path require? | Proposal-only |
| `artifacts/v3_fmo_admission_gate_and_benchmark_impact_702_20260527.json` | What hard-negative controls and benchmark impacts are required before admission? | Review-only gate |
| `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json` | What is the current status of local candidates `m_csa:551` and `m_csa:973`? | Review/readiness only |
| `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json` | Is the FMO definition too narrow, or are blockers elsewhere? | Current FMO blocker analysis |
| `artifacts/v3_fmo_external_hard_negative_duplicate_gate_702_20260528.json` | Which external FMO candidates pass duplicate/hard-negative review gates? | Review-only |

## Artifact Storage And Reproducibility

| Artifact | Answers | Status |
| --- | --- | --- |
| `docs/artifact_storage.md` | What is the non-loss storage policy? | Current reference |
| `artifacts/v3_artifact_storage_inventory_1025.json` | What artifacts exist and how large are they? | Trusted inventory |
| `artifacts/v3_artifact_migration_execution_1025.json` | What migration/removal is authorized? | Fail-closed; authorizes no removal |
| `artifacts/v3_artifact_admission_guard_1025.json` | Are current large artifacts classified? | Trusted guard |

## Historical Or Confounded Artifacts

Use these only with the stated caveat:

- `artifacts/v3_wave1_representation_shootout_result_card_20260526.json` and
  `docs/wave1_representation_shootout.md`: useful historical summaries, but
  geometry joined 135/140 heldout rows and the decoder comparison was not fair.
  Read through the Wave 1.2 audit before making decisions.
- `artifacts/v3_wave1_1_model_by_cell_report_702_20260528.json`: diagnostic
  and useful for cell vocabulary, but superseded by the Wave 1.2 audit for
  representation x decoder and geometry-join conclusions.
- `artifacts/v3_geometry_label_eval_1025_preview_batch.json`: valid as a
  threshold/source artifact, but not a standardized current702 heldout export.
- Existing ProtT5 and SaProt standardized exports: useful NN/cosine diagnostics,
  but not matched logistic-head comparisons.
- The 2026-05-25 current702 label manifest: still the split/sequence source,
  but old row-level label roles for `m_csa:497` and `m_csa:750` must be read
  through the later OOS revision artifacts.
