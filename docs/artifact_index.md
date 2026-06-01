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
| `artifacts/v3_predicted_structure_fold_channel_current702_20260601.json` | What exact AlphaFoldDB/Foldseek scores exist for the real predicted-structure fold channel against the in-distribution atlas? | Current all-heldout scored artifact; persistent coordinate bundle still pending |
| `artifacts/v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json` | Does the scored predicted-structure fold channel match frozen current702 inputs, parsed TSVs, source hashes, and guardrails? | Current validation contract; passes with zero critical violations |
| `artifacts/v3_fold_augmented_abstention_gate_current702_20260601.json` | Does the real predicted-structure Foldseek/TM channel improve the deployment-regime abstention diagnostic when combined with predicted geometry? | Current no-fit diagnostic; no production threshold selected |
| `artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json` | Which geometry-plus-predicted-fold novelty combinations work best without recomputing Foldseek/TM? | Current review-only companion diagnostic; existing channels only, no threshold selected |
| `artifacts/v3_predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.json` | What high-retention operating-point diagnostics do the geometry-plus-predicted-fold novelty variants expose? | Current review-only operating grid; existing variant rows only, no threshold selected |
| `artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json` | What train/cal-selected threshold contract exists for the fold-augmented gate, and how does it read out on heldout once? | Current research threshold contract; train/cal in-scope retention only, not production |
| `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_manifest_current702_20260601.json` | Which non-heldout OOS rows could calibrate OOS abstention for the fold-augmented threshold contract? | Manifest/blocker packet; predicted geometry and fold scores missing for candidates |
| `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.json` | Which hash-selected train/cal OOS negatives now have predicted geometry, cofactor, and nearest-train Foldseek/TM scores? | Current partial calibration surface; 71/76 score-complete rows |
| `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601.json` | Why are 5 selected train/cal OOS negatives not score-complete, and what repair path applies per row? | Current blocker-resolution packet; accession-compatible mapping blockers cleared |
| `artifacts/v3_fold_only_train_cal_oos_negative_surface_current702_20260601.json` | Which selected train/cal OOS negatives have Foldseek/TM evidence but cannot enter the combined geometry+fold channel yet? | Current fold-only salvage surface; diagnostic only |
| `artifacts/v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json` | What OOS-calibrated research threshold contract results after adding train/cal OOS negatives? | Current research contract; partial OOS calibration surface, no production threshold |
| `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json` | Is the partial 71/76 train/cal OOS-negative surface sufficient for the current fold-augmented research contract? | Current decision; sufficient for research with blocker disclosure, not production |
| `artifacts/v3_fold_augmented_train_cal_oos_remaining_blocker_clearance_attempts_current702_20260601.json` | What attempts were made to clear the five remaining train/cal OOS score-surface blockers? | Current blocker-attempt packet; no safe repair without new source evidence/coordinate policy |
| `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json` | Do predicted-atlas geometry percentile and robust-distance variants improve novelty separation after atlas retrieval was unblocked? | Current diagnostic; atlas-only normalization, no deployment threshold selected |
| `artifacts/v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json` | What post-hoc operating-point tradeoff do the geometry-only predicted-atlas novelty variants expose? | Current operating-grid readout; geometry-only signal remains diagnostic, no deployment threshold selected |
| `artifacts/v3_selected_organic_cofactor_sidecar_schema_audit_current702_20260601.json` | Does the selected organic cofactor sidecar satisfy a strict row-class schema and lineage contract for D11/embedding use? | Current schema audit; organic flavin/heme/PLP sidecar contract passed |
| `artifacts/v3_learned_mechanism_feature_embedding_plan_current702_20260601.json` | What leakage-safe scaffold and feature gaps exist for a learned mechanism-feature embedding? | Current scaffold/plan |
| `artifacts/v3_mechanism_feature_active_site_role_graph_sidecar_current702_20260601.json` | Which current702 rows have normalized active-site residue-role graph features for a future mechanism-feature embedding pilot? | Current feature sidecar; no model fit or threshold change |
| `artifacts/v3_mechanism_feature_reaction_center_template_sidecar_current702_20260601.json` | Which current702 rows can inherit fingerprint-template reaction-center descriptors, and what row-specific bond-change gap remains? | Current template sidecar; not row-specific reaction evidence |
| `artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json` | Do the mechanism-feature role-graph and reaction-center sidecars satisfy strict current702 schema and row alignment? | Current schema validation; passes with zero critical violations |
| `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json` | What schema should close the metal/cobalamin/radical-SAM/Fe-S cofactor locus gap? | Current review-only schema/materialization queue; sidecar values tracked in class-specific artifacts |
| `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json` | Which current702 rows have proximal, structure-wide-only, absent, or unsupported metal-ion context? | Current review-only row sidecar from existing geometry ligand context |
| `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.json` | Does the metal-ion locus sidecar pass row alignment, required-key, status, split, range, and guardrail checks? | Current schema audit; passes with zero critical violations |
| `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json` | Which current702 rows have proximal, structure-wide-only, absent, or unsupported cobalamin context? | Current review-only row sidecar from existing geometry ligand context |
| `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json` | Does the cobalamin locus sidecar pass row alignment, required-key, status, split, range, and guardrail checks? | Current schema audit; passes with zero critical violations |
| `artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json` | Which current702 rows have proximal, structure-wide-only, absent, or unsupported SAM context? | Current review-only row sidecar from existing geometry ligand context; includes SAM/Fe-S copresence |
| `artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.json` | Does the radical-SAM locus sidecar pass row alignment, required-key, status, split, range, and guardrail checks? | Current schema audit; passes with zero critical violations |
| `artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.json` | Which current702 rows have proximal, structure-wide-only, absent, or unsupported Fe-S context? | Current review-only row sidecar from existing geometry ligand context; includes SAM/Fe-S copresence |
| `artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.json` | Does the Fe-S locus sidecar pass row alignment, required-key, status, split, range, and guardrail checks? | Current schema audit; passes with zero critical violations |
| `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.json` | Are all schema-named metal/cobalamin/radical-SAM/Fe-S locus sidecars materialized and schema-passing? | Current completion audit; 4/4 classes materialized, zero critical violations, still review-only |
| `artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json` | Which in-distribution rows can feed a no-fit train/cal-only mechanism-feature embedding pilot? | Current input manifest; 562 candidate rows, 524 minimal feature bundles, no model fit and heldout excluded |
| `artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json` | Which ready mechanism-feature rows are assigned to train versus calibration for a future pilot? | Current deterministic split; 418 train, 106 calibration, no model fit and heldout excluded |
| `artifacts/v3_mechanism_feature_embedding_feature_contract_current702_20260601.json` | Which label-stripped feature rows and fields may a future mechanism-feature embedding pilot consume? | Current no-fit feature contract; 524 train/cal rows, labels excluded, heldout excluded |
| `artifacts/v3_mechanism_feature_embedding_feature_contract_strict_audit_current702_20260601.json` | Does the no-fit mechanism-feature feature contract pass strict train/cal and label-exclusion checks? | Current strict audit; 524/524 rows pass, zero critical violations, no model fit |
| `artifacts/v3_mechanism_feature_embedding_train_cal_guardrail_audit_current702_20260601.json` | Do the no-fit mechanism-feature train/cal manifests remain split-consistent and leakage-guarded? | Current guardrail audit; 524 feature rows match split rows, 140 heldout excluded, no model fit |
| `artifacts/v3_current_run_artifact_integrity_audit_current702_20260601.json` | Which current-run JSON artifacts and reports were produced, and did they parse? | Current run integrity audit; 10 JSON artifacts and 10 reports present, validation suite passed |
| `artifacts/v3_family_set_expansion_targets_current702_20260601.json` | Which targeted family expansions de-risk the 8-fingerprint bound without imports? | Proposal-only; no label/import mutation |
| `artifacts/v3_family_panel_evidence_packet_glycyl_radical_or_thiamine_radical_lyase_current702_20260601.json` | What frozen evidence supports the highest-value glycyl-radical/thiamine-lyase boundary panel? | Review-only evidence packet; no label/import mutation |
| `artifacts/v3_family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.json` | What frozen evidence supports the thiol/disulfide oxidoreductase redox boundary panel? | Review-only evidence packet; no label/import mutation |
| `artifacts/v3_family_panel_evidence_packet_lipoamide_or_sulfur_transfer_redox_boundary_current702_20260601.json` | What frozen evidence supports the lipoamide/sulfur-transfer redox boundary panel? | Review-only evidence packet; no label/import mutation |
| `artifacts/v3_family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.json` | What frozen evidence supports the FMO/flavin oxygen-transfer boundary panel? | Review-only evidence packet; no label/import mutation; consumes repaired `m_csa:132` scores |
| `artifacts/v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json` | What frozen evidence supports the cobalamin/radical rearrangement review panel? | Review-only evidence packet; `secondary_probe::radical_sam_enzyme` now has source-free predicted geometry, one gap remains |
| `artifacts/v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json` | What frozen evidence exists for no-reliable-structure metal hydrolase controls? | Review-only evidence packet; `mh_066` now has source-free predicted geometry, five rows remain geometry gaps |
| `artifacts/v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json` | What frozen evidence supports near-orphan glycoside/nucleoside hydrolase controls? | Review-only evidence packet; consumes repaired `m_csa:116` and source-free `mh_073` geometry scores |
| `artifacts/v3_family_panel_packet_coverage_audit_current702_20260601.json` | Across all seven family-expansion packets, which panels are evidence-ready versus geometry-gap queues? | Review-only coverage audit; 15/22 rows have predicted geometry after source-free retrieval joins |
| `artifacts/v3_fold_augmented_family_panel_research_readout_current702_20260601.json` | How do the review-only family panels read out under the fixed fold-augmented research threshold? | Current review-only downstream diagnostic; includes source-free predicted geometry for `mh_066`, `mh_073`, and `secondary_probe::radical_sam_enzyme`; no threshold, label, import, or training change |
| `artifacts/v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json` | Which non-abstained family-panel rows should be source-checked first? | Current review-only queue; nine non-abstained rows after source-free retrieval join; no new source data fetched and no label/import mutation |
| `artifacts/v3_fold_augmented_family_panel_source_check_m_csa267_current702_20260601.json` | Does the top-ranked non-abstained row `m_csa:267` support a family promotion? | Current review-only source check; keep as OOS boundary control |
| `artifacts/v3_fold_augmented_family_panel_source_check_m_csa131_current702_20260601.json` | Does `m_csa:131` support FMO promotion under the family-panel readout? | Current review-only source check; confirms secondary-probe support, no primary promotion |
| `artifacts/v3_fold_augmented_family_panel_source_check_m_csa750_current702_20260601.json` | Does `m_csa:750` support a current seed-family promotion? | Current review-only source check; keep OOS and future radical flavin/Fe-S candidate |
| `artifacts/v3_fold_augmented_family_panel_source_check_m_csa551_current702_20260601.json` | Does `m_csa:551` close the FMO family-promotion gap? | Current review-only source check; confirms future support, no registry/import change |
| `artifacts/v3_fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.json` | Can the remaining M-CSA family-panel missing-channel rows be repaired and scored? | Current review-only repair; `m_csa:132` and `m_csa:116` score-complete, no label/import mutation |
| `artifacts/v3_fold_augmented_family_panel_source_check_m_csa132_current702_20260601.json` | Does repaired `m_csa:132` support FMO promotion? | Current review-only source check; confirms secondary FMO support only, no primary promotion |
| `artifacts/v3_fold_augmented_family_panel_source_check_m_csa116_current702_20260601.json` | Does repaired `m_csa:116` support a current seed-family promotion? | Current review-only source check; keep OOS transhydrogenase control |
| `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json` | Which family-panel rows still need source-free predicted geometry for the primary channel? | Current review-only materialization queue; 7 secondary/external rows remain after the approved-locator scoring pass; no label/import mutation |
| `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json` | Do any missing-queue rows already have frozen geometry/fold scores upstream? | Current review-only diagnosis; all 7 queued rows are source-backed fold-scored and still need source-free geometry |
| `artifacts/v3_family_panel_source_backed_sidecar_materialization_plan_current702_20260601.json` | Which source-backed representatives and exact commands should materialize the 10 remaining family-panel sidecars? | Current review-only manifest; no coordinates fetched, no scoring run, no label/import mutation |
| `artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601.json` | Which source-backed family-panel rows now have coordinate hashes and predicted Foldseek/TM scores? | Current review-only materialization; 10/10 P0/P1 rows fold-scored, predicted-geometry sidecars still missing |
| `artifacts/v3_family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.json` | Why are the 10 fold-scored family-panel rows still missing source-free predicted geometry? | Current blocker manifest; all 10 have AFDB CIFs and fold scores, 3/10 have approved source-free active-site locator sidecars, and 7/10 remain blocked |
| `artifacts/v3_family_panel_source_free_predicted_geometry_retrieval_current702_20260601.json` | Which approved source-free locator rows now have predicted-geometry retrieval scores and fixed research-gate projections? | Current review-only retrieval; 3/3 approved locator rows score OK and remain non-importable; 7 rows still lack approved locators |
| `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.json` | What local source-check package gates the three newly non-abstained source-free geometry rows? | Current review-only preflight; holds all 3 rows pending source check, with 1 geometry/fold agreement and 2 disagreements |
| `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.json` | Does the first source-free geometry row `mh_066` support immediate family promotion? | Current review-only source check; keep as external metal-hydrolase expansion candidate, no import or promotion |
| `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.json` | Does source-free row `mh_073` support hydrolase-family promotion? | Current review-only source check; keep as Mg/GTPase boundary hard negative, no import or promotion |
| `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.json` | Does source-free radical-SAM row `secondary_probe::radical_sam_enzyme` support family promotion? | Current review-only source check; confirms radical-SAM/Fe-S locus evidence, no import or promotion |
| `artifacts/v3_family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.json` | Which seven family-panel rows still block source-free predicted-geometry scoring, and what clears each blocker? | Current review-only action queue; start with `mh_065`/`mh_072` UniProt position validation |
| `artifacts/v3_family_panel_source_free_locator_uniprot_position_validation_mh065_mh072_current702_20260601.json` | Can `mh_065` and `mh_072` candidate locators be sequence-position validated against the source UniProt accessions? | Current review-only validation; both rows remain blocked by selected-PDB `struct_ref` accession mismatches, no locator copy or scoring |
| `artifacts/v3_family_panel_source_free_locator_split_safe_template_check_mh067_mh068_current702_20260601.json` | Can `mh_067` and `mh_068` use same-accession template locators without heldout leakage? | Current review-only split check; both pass against in-distribution same-accession seeds, but locator copy remains manually gated |
| `artifacts/v3_family_panel_source_free_locator_ligand_specificity_review_external_glycoside_panel_current702_20260601.json` | Is the `external_glycoside_panel` acetate-derived locator biologically specific enough to copy? | Current review-only ligand review; selected acetate locator rejected, no copy or scoring |
| `artifacts/v3_family_panel_source_free_locator_policy_blockers_mh064_q59490_current702_20260601.json` | What policy decisions remain for the no-ligand locator blockers `mh_064` and Q59490? | Current review-only decision packet; `mh_064` needs alternate-coordinate fetch approval and Q59490 needs a nonlabel locator strategy or alternate source row |
| `artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json` | What is the current state of all seven unresolved source-free locator blockers after this run's reviews? | Current review-only consolidated status; automation discovery complete, 0/7 scoring-ready, all rows need human/policy decisions |
| `artifacts/v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json` | What schema must a locator sidecar satisfy before those review rows can enter predicted-geometry scoring? | Current schema contract; requires at least two source-free sequence-position locators and forbids source prose/labels/IDs as predictive features |
| `artifacts/v3_family_panel_source_free_active_site_locator_schema_audit_current702_20260601.json` | Do any source-free locator sidecars currently pass the schema? | Current schema audit; 3/10 locator sidecars present and schema-passed, with 7 still missing |
| `artifacts/v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json` | Which source-free locator sidecar files should be created next, and under which allowed policy candidates? | Current materialization plan; 10 planned sidecars, no locators created, no predicted geometry scored |
| `artifacts/v3_family_panel_source_free_active_site_locator_template_bundle_current702_20260601.json` | Which review-only locator templates are staged for the 10 source-free predicted-geometry blockers? | Current template bundle; 10 sidecar shells outside the audited locator directory, none scoring-ready |
| `artifacts/v3_family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.json` | Which coordinate-only locator candidates can be staged from the source-backed selected structures? | Current review-only candidate audit; 8/10 rows have >=2 candidate locators, 6 have UniProt-position mapping, 0 are approved for scoring |
| `artifacts/v3_family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.json` | Do the staged locator candidate sidecars match the audit and preserve review-only guardrails? | Current integrity audit; 10/10 staged sidecars pass file/payload/guardrail checks, 0 scoring-ready |
| `artifacts/v3_family_panel_source_free_active_site_locator_review_queue_current702_20260601.json` | Which candidate sidecars should be reviewed first before any audited locator copy? | Current review-only queue; 3 priority-1 rows, 0 scoring-ready |
| `artifacts/v3_family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.json` | What exact row packet should manual locator review use next? | Current review-only packet; combines candidate hashes, integrity status, priority class, and per-row checklist; 0 copy-ready |
| `artifacts/v3_family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.json` | Do the three priority-1 locator candidates pass automation preflight before human approval? | Current review-only preflight; 3/3 pass schema, guardrail, and coordinate-contact checks, but 0 are copy-authorized or scoring-ready |
| `artifacts/v3_family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.json` | What exact rescue path exists for no-ligand source-free locator blockers? | Current review-only rescue manifest; `mh_064` has five alternate PDB fetch commands pending approval, Q59490 has no frozen alternate source PDB |
| `artifacts/v3_fmo_subtype_hard_negative_packet_current702_20260601.json` | What FMO subtype and hard-negative packet is ready after the fold-panel readout? | Current review-only packet; repaired `m_csa:132` remains secondary-only; no primary FMO import/promotion authorized |

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
| `artifacts/v3_current_docs_artifact_reference_check_current702_20260601.json` | Do current durable docs point only to existing concrete repo paths? | Current maintenance check; 430 concrete references checked, zero missing after excluding templates/globs |

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
