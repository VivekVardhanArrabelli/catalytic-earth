# Redox Oxygen Sulfur Scaleout Shard

- Artifact: `artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json`
- Created UTC: `2026-06-08T14:23:12Z`
- STARTED_AT_UTC: `2026-06-08T14:11:51Z`
- STARTED_AT_LOCAL: `Mon Jun  8 09:11:51 CDT 2026`
- Scope: candidate/evidence lane only; no registry, ontology, import, split, model, or threshold edits.
- Candidate rows: `370` de-duplicated candidates from `989` selected source-row contributions.
- Removed non-candidate control-group rows: `['flavin.dehydrogenase_oxidase_hydride_transfer']`.

## Terminal State Counts

- `blocked_coordinate`: `79`
- `blocked_family_decision`: `6`
- `blocked_locator`: `47`
- `countable_candidate_preflight_only`: `2`
- `reject/OOS_preserve_signal`: `120`
- `review_only_evidence`: `116`

## Subfamily Lane Counts

- `flavin_dehydrogenase_reductase_boundary`: `48`
- `flavin_fe_s_cofactor_confounded_boundary`: `18`
- `flavin_monooxygenase_oxygen_transfer_boundary`: `20`
- `heme_oxygen_peroxide_transfer_boundary`: `64`
- `iron_sulfur_or_fe_s_electron_transfer_boundary`: `100`
- `nad_p_dehydrogenase_reductase_specificity_boundary`: `4`
- `redox_oxygen_sulfur_lipoamide_unresolved_boundary`: `111`
- `sulfur_lipoamide_transfer_redox_boundary`: `2`
- `thiol_disulfide_oxidoreductase_isomerase_boundary`: `3`

## High-Value Queues

- Preflight-only candidates: `2`
  - `m_csa:281` via `flavin_fe_s_cofactor_confounded_boundary`: run human promotion review and label-factory/import gates; this shard performed no import
  - `m_csa:127` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: run human promotion review and label-factory/import gates; this shard performed no import
- Blocked locator repair opportunities: `47`
  - `m_csa:892` via `flavin_dehydrogenase_reductase_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:P0AGE6` via `flavin_dehydrogenase_reductase_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:P94424` via `flavin_dehydrogenase_reductase_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q652L6` via `flavin_dehydrogenase_reductase_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q9BRQ8` via `flavin_dehydrogenase_reductase_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:A6T923` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:B6BQB2` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:E9QYP0` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:F8G0M4` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:O94851` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:P00438` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q47PU3` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q6SSJ6` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q7RTP6` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q93L51` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q93NG3` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `uniprot:Q988D3` via `heme_oxygen_peroxide_transfer_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `m_csa:185` via `redox_oxygen_sulfur_lipoamide_unresolved_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `m_csa:230` via `redox_oxygen_sulfur_lipoamide_unresolved_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
  - `m_csa:553` via `redox_oxygen_sulfur_lipoamide_unresolved_boundary`: repair or approve a source-free active-site/residue locator, then rerun geometry and duplicate screens
- Blocked coordinate/provenance rows: `79`
  - `m_csa:102` via `flavin_fe_s_cofactor_confounded_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:277` via `flavin_fe_s_cofactor_confounded_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:319` via `flavin_fe_s_cofactor_confounded_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:320` via `flavin_fe_s_cofactor_confounded_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:879` via `flavin_fe_s_cofactor_confounded_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:809` via `flavin_monooxygenase_oxygen_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:106` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:136` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:160` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:165` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:173` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:216` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:233` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:243` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
  - `m_csa:244` via `iron_sulfur_or_fe_s_electron_transfer_boundary`: materialize or approve coordinate provenance before any scoring or countable review
- Blocked family/terminal decision rows: `6`
  - `uniprot:P30043` via `flavin_dehydrogenase_reductase_boundary`: route to expert family/terminal review; do not count or import until explicit approval and gates pass
  - `uniprot:P42898` via `flavin_dehydrogenase_reductase_boundary`: route to expert family/terminal review; do not count or import until explicit approval and gates pass
  - `uniprot:Q9NX74` via `flavin_dehydrogenase_reductase_boundary`: route to expert family/terminal review; do not count or import until explicit approval and gates pass
  - `uniprot:Q54530` via `heme_oxygen_peroxide_transfer_boundary`: route to expert family/terminal review; do not count or import until explicit approval and gates pass
  - `uniprot:Q88FY2` via `heme_oxygen_peroxide_transfer_boundary`: route to expert family/terminal review; do not count or import until explicit approval and gates pass
  - `uniprot:O15247` via `redox_oxygen_sulfur_lipoamide_unresolved_boundary`: route to expert family/terminal review; do not count or import until explicit approval and gates pass
- Preserved OOS/reject/cofactor-confounded signals: `120`
  - `m_csa:110` via `flavin_dehydrogenase_reductase_boundary`
  - `m_csa:113` via `flavin_dehydrogenase_reductase_boundary`
  - `m_csa:354` via `flavin_dehydrogenase_reductase_boundary`
  - `m_csa:822` via `flavin_dehydrogenase_reductase_boundary`
  - `m_csa:852` via `flavin_dehydrogenase_reductase_boundary`
  - `m_csa:895` via `flavin_dehydrogenase_reductase_boundary`
  - `mh_057` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P0AEN1` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P0AEZ1` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P15559` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P21375` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P32340` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P33371` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P38489` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P41407` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P42593` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:P77258` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:Q07923` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:Q8LAH7` via `flavin_dehydrogenase_reductase_boundary`
  - `uniprot:Q9FUP0` via `flavin_dehydrogenase_reductase_boundary`

## Source Contribution Counts

- `external_flavin_redox_stress_panel_20260528`: `48` selected source rows
- `external_heme_redox_boundary_panel_20260528`: `46` selected source rows
- `external_minicampaign_modern_baseline_rollup_post_flavin_dehydrogenase_20260521`: `59` selected source rows
- `external_minicampaign_modern_baseline_rollup_post_heme_20260521`: `39` selected source rows
- `external_panel_router_queue_20260528`: `84` selected source rows
- `external_redox_third_blocker_deep_terminal_decision_packet_after_source_free_geometry_and_targeted_lane_screen_20260522`: `3` selected source rows
- `family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601`: `4` selected source rows
- `family_panel_evidence_packet_lipoamide_or_sulfur_transfer_redox_boundary_current702_20260601`: `2` selected source rows
- `family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601`: `1` selected source rows
- `flavin_dehydrogenase_second_deep_terminal_decision_packet_after_targeted_fdr_screen_20260521`: `7` selected source rows
- `flavin_dehydrogenase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522`: `6` selected source rows
- `flavin_monooxygenase_deep_terminal_decision_packet_after_targeted_fmo_rescue_screen_20260521`: `7` selected source rows
- `fmo_acquisition_sprint_integrated_status_702_20260527`: `76` selected source rows
- `fmo_admission_gate_and_benchmark_impact_702_20260527`: `76` selected source rows
- `fmo_external_hard_negative_duplicate_gate_702_20260528`: `6` selected source rows
- `fmo_external_structure_geometry_materialization_702_20260528`: `6` selected source rows
- `fmo_mcsa_candidate_scout_702_20260527`: `37` selected source rows
- `heme_peroxidase_second_deep_terminal_decision_packet_after_targeted_heme_screen_20260521`: `7` selected source rows
- `heme_peroxidase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522`: `5` selected source rows
- `learned_retrieval_manifest_1025_current702_full_20260525`: `72` selected source rows
- `lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_current702_20260605`: `74` selected source rows
- `lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout_current702_20260605`: `2` selected source rows
- `lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout_current702_20260605`: `3` selected source rows
- `mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601`: `48` selected source rows
- `nadp_redox_family_source_free_cofactor_blocker_queue_post_sdr_20260522`: `2` selected source rows
- `nadp_redox_holo_or_specificity_source_request_queue_post_proxy_20260522`: `3` selected source rows
- `prospective_external_flavin_dehydrogenase_minicampaign_freeze_20260521`: `20` selected source rows
- `prospective_external_flavin_monooxygenase_minicampaign_freeze_20260521`: `20` selected source rows
- `prospective_external_heme_peroxidase_minicampaign_freeze_20260521`: `19` selected source rows
- `targeted_expansion_acquisition_conversion_screens_current702_20260608`: `11` selected source rows
- `targeted_expansion_factory_batch_current702_20260608`: `196` selected source rows

## Guardrails

- This shard is source-free/candidate-evidence only and performed no label import or promotion.
- Mechanism text, labels, source identifiers, target names, and EC-like fields are retained only as provenance/rationale in selected evidence fields.
- No heldout training/tuning, production scoring threshold changes, split changes, model weight edits, ontology edits, registry edits, or global docs edits were performed.
- Every row has a terminal state, source hashes, duplicate-screen status, coordinate/provenance status, ligand/cofactor evidence, confidence tier, and machine-actionable next step.
