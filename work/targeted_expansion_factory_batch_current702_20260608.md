# Targeted Expansion Factory Batch - current702

- Artifact: `v3_targeted_expansion_factory_batch_current702_20260608`
- Status: `targeted_expansion_factory_batch_ready`
- Target volume: target_volume_met
- Candidate rows: 703
- Family axes: 12
- Countable/import-ready rows: 0 / 0

## Admission Counts

- `countable_candidate`: 0
- `review_only_evidence`: 262
- `reject_preserve_signal`: 58
- `oos_hard_negative`: 0
- `blocked_locator`: 72
- `blocked_coordinate`: 3
- `blocked_family_decision`: 130
- `acquisition_needed`: 178

## Family Axes

- `flavin_oxygen_transfer_boundary`: 9
- `glycoside_nucleoside_hydrolase_glycan_transfer`: 69
- `metal_hydrolase_subclass_expansion`: 105
- `near_orphan_isomerase_controls`: 60
- `near_orphan_low_geometry_support`: 153
- `no_reliable_structure_or_locator_gap`: 23
- `phosphoryl_transfer_boundary_review_only`: 70
- `plp_schiff_base_or_nucleoside_lyase_controls`: 50
- `plp_subclass_expansion`: 4
- `sam_methyltransferase_transfer_axis`: 70
- `serine_or_cysteine_hydrolase_boundary_controls`: 27
- `underrepresented_redox_oxygen_transfer`: 63

## Coordinate Status

- `coordinate_missing`: 2
- `coordinate_reference_missing`: 1
- `experimental_pdb_references_present`: 248
- `experimental_pdb_selected`: 322
- `predicted_alphafold_reference_present`: 130

## Proposed Tiers

- `tier_2_external_review_evidence`: 12
- `tier_2_geometry_ready_review`: 73
- `tier_3_acquisition_needed`: 178
- `tier_3_blocked_coordinate`: 3
- `tier_3_blocked_family_decision`: 130
- `tier_3_blocked_locator`: 72
- `tier_3_review_only_low_support`: 177
- `tier_4_reject_preserve_signal`: 58

## Source Surfaces

- `m_csa`: 324
- `uniprot_swissprot`: 379

## Source Hashes

- `label_expansion_candidates`: `bea58b3e6cdd4a45905110e38d783e48a28ff25bb263795791b963985057e585` from `artifacts/v3_label_expansion_candidates_1025.json`
- `external_candidate_freeze`: `2c8aca26c479f4dd25ff09ab17349526bdec01561dc5f4f37dea107fdea59260` from `artifacts/v3_prospective_external_minicampaign_candidate_freeze_20260520.json`
- `sequence_cluster_proxy`: `2451b2256afcbb8669563744967e519abd62ce1cd55a091a5f1e4119d30386af` from `artifacts/v3_sequence_cluster_proxy_1025.json`

## Factory Audit

- Passed: True
- Accession/source-accession coverage complete: True
- Source hashes complete: True
- Family axes complete: True
- Forbidden predictive feature policy clean: True
- Prior architecture-default rows absent: True

## Action Tranches

1. `review_only_evidence` - 12 rows - run duplicate, structural, UniRef, review, and label-factory gates before import
2. `review_only_evidence` - 177 rows - preserve as non-counting evidence until a sharper family gate is available
3. `review_only_evidence` - 73 rows - run family-specific source/duplicate/import-preview gates before any countable use
4. `acquisition_needed` - 178 rows - collect explicit catalytic residue/locator evidence before admission scoring
5. `blocked_locator` - 72 rows - repair source-free residue locator mapping before family admission
6. `blocked_coordinate` - 2 rows - materialize or approve a coordinate source before locator scoring
7. `blocked_coordinate` - 1 rows - acquire AlphaFold/PDB coordinate reference before source-free scoring
8. `blocked_family_decision` - 130 rows - decide whether this source lane belongs in the next targeted axis before scoring

## First Action Preview

- Tranche 1: `review_only_evidence` / 12 rows
- Action: run duplicate, structural, UniRef, review, and label-factory gates before import
- `uniprot:P07237` / `P07237` / `near_orphan_isomerase_controls`
- `uniprot:P0A6L4` / `P0A6L4` / `plp_schiff_base_or_nucleoside_lyase_controls`
- `uniprot:P14174` / `P14174` / `near_orphan_isomerase_controls`
- `uniprot:P28240` / `P28240` / `plp_schiff_base_or_nucleoside_lyase_controls`
- `uniprot:P28330` / `P28330` / `underrepresented_redox_oxygen_transfer`
- `uniprot:P30101` / `P30101` / `near_orphan_isomerase_controls`
- `uniprot:P30838` / `P30838` / `underrepresented_redox_oxygen_transfer`
- `uniprot:P31040` / `P31040` / `underrepresented_redox_oxygen_transfer`
- `uniprot:P36959` / `P36959` / `underrepresented_redox_oxygen_transfer`
- `uniprot:P54098` / `P54098` / `plp_schiff_base_or_nucleoside_lyase_controls`
- `uniprot:Q8TAT5` / `Q8TAT5` / `plp_schiff_base_or_nucleoside_lyase_controls`
- `uniprot:Q9BZE2` / `Q9BZE2` / `near_orphan_isomerase_controls`

## Blockers And Next Batch

- Acquisition-needed rows: 178
- Blocked family-decision rows: 130
- Blocked locator rows: 72
- Blocked coordinate rows: 3

## Mechanical Next Steps

1. Run source-free duplicate and structural distance screens for the external review-only rows.
2. Collect explicit catalytic residue or locator sources for acquisition_needed external rows.
3. Materialize or repair coordinate/locator mappings for blocked M-CSA rows.
4. Decide whether uncovered external lanes become targeted axes or stay preserved OOS signal.

## Guardrails

- No labels, registries, ontologies, imports, splits, thresholds, or model weights were changed.
- Mechanism text, EC/Rhea IDs, names, labels, target names, and source IDs are preserved only as provenance/review context and are not scoring inputs.
- Human review is required only to cross a countable-promotion boundary.

