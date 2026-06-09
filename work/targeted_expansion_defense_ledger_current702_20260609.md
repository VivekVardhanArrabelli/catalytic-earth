# Targeted Expansion Defense Ledger - current702 - 20260609

Created UTC: `2026-06-09T03:54:22Z`

This is a review-defense ledger, not an import artifact. It indexes current-main targeted expansion and Wave 2 materialization artifacts plus completed external scaleout/admission branches, keeping preview rows separate from countable labels.

## Expansion Thesis

- The 10k path should expand along mechanism, fold, cofactor, and near-orphan/OOS axes that previous experiments identified as brittle, not by random label accumulation.
- Predicted geometry reconstruction showed that deploy-time missing active-site context, especially cofactors, can dominate errors; therefore redox, PLP, radical-SAM/cobalamin, and metal/cofactor lanes are first-class expansion axes.
- Fold/cofactor confounding and decoder-choice artifacts require family-specific review lanes, structural duplicate checks, and source-free active-site locators before any countable import.
- Near-orphan and no-reliable-structure bins are atlas-coverage needs, but they remain review/repair queues until coordinates and locators are source-free and explicit.
- External Swiss-Prot/AFDB/PDB/Rhea ingestion is the current scalable source pattern; branch artifacts show 845 merged candidates and 333 preview-only import-ready rows, not 333 new labels.
- Current main now includes Wave 2 materialization: 333 import-ready preview rows are carried forward, 309 review-only locator sidecars are staged under a disk-floor guardrail, and 512 rows remain repair/continuation work.

## Count Ledger

| Surface | Count | Defense note |
| --- | ---: | --- |
| Current countable labels | 702 | Current benchmark surface; no new labels imported by this run. |
| Targeted factory candidates | 816 | Admission states: `acquisition_needed`=86, `blocked_coordinate`=44, `blocked_family_decision`=0, `blocked_locator`=90, `countable_candidate`=0, `reject/OOS_preserve_signal`=205, `review_only_evidence`=391. |
| Acquisition conversion rows | 86 | Terminal states: `blocked_coordinate`=0, `blocked_family_decision`=50, `blocked_locator`=7, `countable_candidate_preflight_only`=1, `reject/OOS_preserve_signal`=27, `review_only_evidence`=1. |
| Merged scaleout source rows | 4820 | Seven shards collapsed to 2463 canonical keys; 0 import preview rows. |
| Unblocker matrix target rows | 523 | Import-preview candidates: 0; repair classes: `coordinate_repair_candidate`=2, `family_default_resolved`=102, `hard_blocked_with_next_action`=273, `locator_repair_candidate`=96, `reject/OOS_preserve_signal`=14, `true_expert_only`=36. |
| External pilot preview | 16 | 16 pilot rows validated as materialization queue, not direct production imports. |
| External bulk scout | 693 | Provisional preview rows: 354. |
| External bulk pagination scaleout branch | 845 | Provisional preview rows: 442; branch `origin/ce-external-bulk-pagination-scaleout-20260609` @ `595c7ac850aa32c1fc2f6ba257bf1a370499747f`. |
| Materialization/admission branch | 370 | Import-ready preview: 333; repairable locator blockers: 37. |
| External admission QA branch | 845 | Import-ready preview: 333; repair queue: 48; exact current702 conflicts: 22. |
| Current-main Wave 2 materialization | 845 | Import-ready preview carried forward: 333; new locator sidecars: 309; repair/continuation queue: 512; coordinate downloads performed: 0 due disk floor. |

## Active Scaleout Shards

| Shard | Rows | Terminal counts | Artifact |
| --- | ---: | --- | --- |
| `glycoside_nucleoside` | 835 | `blocked_coordinate`=44, `blocked_family_decision`=50, `blocked_locator`=97, `countable_candidate_preflight_only`=1, `reject/OOS_preserve_signal`=233, `review_only_evidence`=410 | `artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json` |
| `metal_hydrolase` | 411 | `blocked_coordinate`=10, `blocked_family_decision`=2, `blocked_locator`=34, `reject/OOS_preserve_signal`=117, `review_only_evidence`=248 | `artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json` |
| `near_orphan_tail` | 746 | `blocked_family_decision`=44, `blocked_locator`=74, `reject/OOS_preserve_signal`=438, `review_only_evidence`=190 | `artifacts/v3_scaleout_near_orphan_tail_shard_current702_20260608.json` |
| `phosphoryl_transfer` | 1281 | `blocked_coordinate`=16, `blocked_family_decision`=142, `blocked_locator`=33, `countable_candidate_preflight_only`=1, `reject/OOS_preserve_signal`=885, `review_only_evidence`=204 | `artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json` |
| `plp_children` | 442 | `blocked_coordinate`=2, `blocked_family_decision`=2, `blocked_locator`=90, `reject/OOS_preserve_signal`=314, `review_only_evidence`=34 | `artifacts/v3_scaleout_plp_children_shard_current702_20260608.json` |
| `radical_sam_cobalamin` | 735 | `blocked_coordinate`=23, `blocked_family_decision`=21, `reject/OOS_preserve_signal`=681, `review_only_evidence`=10 | `artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json` |
| `redox_oxygen_sulfur` | 370 | `blocked_coordinate`=79, `blocked_family_decision`=6, `blocked_locator`=47, `countable_candidate_preflight_only`=2, `reject/OOS_preserve_signal`=120, `review_only_evidence`=116 | `artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json` |

## Family And Lane Rationale

| Family/lane | Why included | Failure mode or atlas need | Count signal | Supporting artifacts |
| --- | --- | --- | --- | --- |
| `metal_hydrolase` | Metal coordination and hydrolase-like folds are a known cofactor/fold confounding axis; the atlas needs subclass breadth and hard duplicate screens rather than one broad metal bucket. | Separates true metal-dependent hydrolase mechanisms from fold-neighbor and current702 duplicate signals; preserves locator-ready rows that still need Rhea/family review. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 9, "coordinate_ready_pending_locator": 3, "import_ready_preview": 15, "locator_ready_candidate": 91, "provisional_external_countable_preflight_candidate": 13, "repairable_locator_blocker": 1}, "factory_axis_rows": 394, "scaleout_shard_rows": 411}` | `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json`<br>`artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json`<br>`origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_merged_surface_current702_20260609.json`<br>`artifacts/v3_cofactor_presence_calibration_current702_20260604.json` |
| `redox oxygen/sulfur` | Predicted geometry failure analysis showed missing cofactor context can dominate deployment loss; oxygen/sulfur redox lanes are the clearest place to test cofactor reconstruction and electron-flow guardrails. | Prevents flavin/heme/sulfur-lipoamide rows from becoming random sequence/fold positives; expands redox boundaries with explicit source provenance and no mechanism text as features. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 5, "coordinate_ready_pending_locator": 4, "import_ready_preview": 64, "locator_ready_candidate": 29, "locator_repair_candidate": 5, "provisional_external_countable_preflight_candidate": 21, "repairable_locator_blocker": 1}, "factory_axis_rows": 173, "scaleout_shard_rows": 370}` | `artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json`<br>`artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json`<br>`artifacts/v3_lever2_source_free_electron_flow_current_split_operating_point_readout_current702_20260606.json`<br>`origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json` |
| `PLP children` | PLP mechanism children are useful only if the ledger keeps child mechanisms separate from broad PLP family evidence and locator gaps. | Defends against parent-family collapse, single-locator rows, and ambiguous residue mappings before any import-ready claim. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 2, "import_ready_preview": 72, "locator_ready_candidate": 5, "provisional_external_countable_preflight_candidate": 3, "repairable_locator_blocker": 20}, "factory_axis_rows": 56, "scaleout_shard_rows": 442}` | `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json`<br>`artifacts/v3_scaleout_plp_children_shard_current702_20260608.json`<br>`origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_admission_batch_current702_20260608.json` |
| `radical-SAM/cobalamin` | Radical-SAM and cobalamin were secondary/OOD probes and cofactor-locus sidecars; they stress active-site cofactor evidence, not just fold similarity. | Adds hard cofactor-locus diversity while preserving coordinate-repair and duplicate blockers. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 3, "coordinate_ready_pending_locator": 7, "coordinate_repair_candidate": 3, "import_ready_preview": 50, "locator_ready_candidate": 30, "provisional_external_countable_preflight_candidate": 1, "repairable_locator_blocker": 5}, "factory_axis_rows": 22, "scaleout_shard_rows": 735}` | `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json`<br>`artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json`<br>`artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json`<br>`origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_merged_surface_current702_20260609.json` |
| `glycoside/nucleoside` | This lane supplies hydrolase controls, carbohydrate/nucleoside boundary rows, and source-free locator pressure from prior external glycoside panels. | Separates hard-negative/OOS preserve signals from plausible hydrolase labels and flags active-site locator gaps before review. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 6, "coordinate_ready_pending_locator": 32, "import_ready_preview": 43, "locator_ready_candidate": 22, "provisional_external_countable_preflight_candidate": 20, "repairable_locator_blocker": 6}, "factory_axis_rows": 80, "scaleout_shard_rows": 835}` | `artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json`<br>`artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`<br>`artifacts/v3_family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.json` |
| `phosphoryl transfer` | Earlier ePK and ATP/substrate-role work showed phosphorylation-like rows are especially vulnerable to ligand/protein-substrate confounding. | Keeps kinase-like, phosphatase, and transfer boundary rows review-gated; import-ready previews remain subject to structural duplicate and label-factory review. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 3, "coordinate_ready_pending_locator": 6, "import_ready_preview": 88, "locator_ready_candidate": 4, "locator_repair_candidate": 1, "provisional_external_countable_preflight_candidate": 7, "repairable_locator_blocker": 4}, "factory_axis_rows": 25, "scaleout_shard_rows": 1281}` | `work/scope.md`<br>`artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json`<br>`origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_admission_batch_current702_20260608.json` |
| `near-orphan/no-reliable-structure` | Near-orphan and no-reliable-structure rows are the explicit atlas-growth lane for mechanisms not well represented in current702. | Creates bins for underrepresented mechanisms without treating low-evidence rows as countable labels; requires coordinate/locator repair before review. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 4, "coordinate_ready_pending_locator": 67, "hard_blocked_with_next_action": 2, "import_ready_preview": 1, "locator_ready_candidate": 39, "locator_repair_candidate": 2}, "factory_near_orphan_rows": 43, "factory_no_reliable_structure_rows": 23, "scaleout_shard_rows": 746}` | `artifacts/v3_mechanism_prediction_orphan_eval_design_702_20260525.json`<br>`artifacts/v3_near_orphan_geometry_support_review_packet_702_20260526.json`<br>`artifacts/v3_scaleout_near_orphan_tail_shard_current702_20260608.json` |
| `adjacent high-yield amidase/deaminase` | The pagination scaleout added high-yield adjacent external lanes to test whether the Swiss-Prot/AFDB/Rhea pattern can broaden without becoming random. | Useful for volume toward 10k, but remains provisional until family review and duplicate gates prove these are meaningful mechanism additions. | `{"external_scaleout_lane_counts": {"locator_ready_candidate": 1, "provisional_external_countable_preflight_candidate": 11}}` | `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json`<br>`origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_merged_surface_current702_20260609.json` |
| `adjacent high-yield lyase/isomerase` | This external-only lane tests adjacent mechanism space while keeping exact current702 conflicts and coordinate/locator blockers visible. | Candidate volume lane for 10k, not a count claim; needs family/lane review and structural duplicate screening. | `{"external_scaleout_lane_counts": {"blocked_duplicate_or_current_registry_conflict": 1, "coordinate_ready_pending_locator": 1, "provisional_external_countable_preflight_candidate": 12}}` | `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json`<br>`origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_merged_surface_current702_20260609.json` |

## Guardrails

- `m_csa_eval_only`: M-CSA/current702 is used for evaluation, current-registry overlap checks, and historical lesson artifacts; branch guardrails record m_csa_used_as_expansion_source=false for external ingestion.
- `no_heldout_leakage`: No heldout row is used for training/tuning in this ledger; prior heldout one-shot is spent and cited only as historical evidence.
- `no_mechanism_text_predictive_feature`: Mechanism text, source prose, EC/Rhea IDs, labels, source IDs, and expert notes remain forbidden predictive scoring features; they are provenance/rationale fields only.
- `source_free_coordinate_locator_requirements`: Countable import requires local coordinate provenance plus source-free/approved exact residue locators; materialized branch sidecars are preview-only and do not edit audited production locator directories.
- `no_production_edits`: This run and the cited branch outputs do not edit production registries, imports, ontologies, heldout splits, thresholds, or model weights.
- `preview_not_import`: Import-ready preview rows still need current-countable structural duplicate screening, label-factory gate, explicit review, controlled import approval, and production registry-change authorization.

## Projected Path To 10k

- Current countable labels: `702`; labels still needed for 10k: `9298`.
- If the `333` import-ready preview rows eventually pass all remaining gates and are explicitly authorized, the count would be `1035`, leaving `8965`.
- If all `442` provisional scaleout preview rows eventually clear admission and all remaining gates, the count would be `1144`, leaving `8856`.
- 333 import-ready rows are a subset of the 442 scaleout provisional preview after materialization/admission; they must not be added together.

## Review Narrative

### Honest Claims Tomorrow

- The selected expansion lanes are traceable to prior failure modes: cofactor-loss predicted geometry, fold/cofactor confounding, source-free locator gaps, near-orphan/OOS coverage, and external Swiss-Prot/AFDB/Rhea scalability.
- Current main has a non-importing targeted factory with 816 candidates, a seven-shard merged acceptance surface with 4,820 source rows / 2,463 canonical candidates, and a 523-row unblocker matrix with 0 import-preview candidates.
- Completed external branches demonstrate a larger controlled surface: 845 bulk scaleout candidates, 442 provisional preview rows, a 370-row materialization/admission batch, and a 333-row import-ready preview lane that clears exact current702 non-overlap and source-provenance checks.
- The current countable label surface remains 702; the 333 preview rows are the next controlled review queue, not registered labels.
- Current main also contains Wave 2 materialization outputs: 333 import-ready preview rows carried forward, 309 low-disk review-only locator sidecars, and a 512-row repair/continuation queue.

### Still Preview Or Provisional

- The 333 import-ready preview rows still require structural duplicate screening, label-factory gate, explicit review, controlled import lane approval, and production registry-change authorization.
- The 88 remaining provisional preflight rows in the admission surface and the 48 repair-queue rows are not ready for import review.
- The current-main scaleout/unblocker surface produced 0 import-preview candidates; it is evidence and repair-routing material.
- No 10k-label claim is available: even perfect downstream acceptance of 333 preview rows would reach only 1,035 countable labels and leave 8,965 labels to source and gate.
- Wave 2 did not download new coordinates because disk free space was below the 10 GiB floor; the 309 locator-sidecar continuation rows and 120 coordinate-ready pending-locator rows remain follow-up work.

## Branch Provenance

| Ref | Commit | Committed | Subject |
| --- | --- | --- | --- |
| `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `2026-06-08T22:49:59-05:00` | Materialize external Wave 2 preview surface |
| `origin/ce-external-bulk-pagination-scaleout-20260609` | `595c7ac850aa32c1fc2f6ba257bf1a370499747f` | `2026-06-08T20:48:48-05:00` | Scale external bulk ingestion pagination |
| `origin/ce-external-materialization-admission-batch-20260608` | `1f61a2dcf4e6268a65ee53d61e508cf878695f27` | `2026-06-08T20:43:30-05:00` | Add external materialization admission batch |
| `origin/ce-external-admission-qa-merger-20260608` | `cac2d937ebed772759a063e41e7b37e6ec403dcf` | `2026-06-08T20:32:11-05:00` | Add external admission QA merger lane |
| `origin/ce-external-admission-qa-merger-20260609` | `ec9deee9c22013659277cf0009a8a4d4eb185671` | `2026-06-08T21:35:48-05:00` | Record external admission merger handoff |

## Key Artifact Provenance

| Role | Path/spec | Ref | Commit | SHA256 | Exists/access |
| --- | --- | --- | --- | --- | --- |
| current-main first targeted expansion factory batch | `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `4143170e0c948d5ba60c56e090c5aae0ce0b16e6c5d60caeae9215484531cee2` | local exists |
| current-main first targeted expansion report | `work/targeted_expansion_factory_batch_current702_20260608.md` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `55d2134a0b719fbb1b636711fd6547a2604507f0339af3e11234b470b767af4b` | local exists |
| current-main acquisition conversion screens | `artifacts/v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `50f2aea5c862787a4f296ed8035ac30a2f064e5e0518a91bdc71784d7cc93066` | local exists |
| current-main acquisition conversion report | `work/targeted_expansion_acquisition_conversion_screens_current702_20260608.md` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `f304be04bd54738dba436e6cd8b367354a0c46f67e893b1cc7f44fda8e84c2e3` | local exists |
| current-main merged scaleout acceptance surface | `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `b3c6523dc74d999c80c89e64859d5917e401cda54507d192338ede2ef5f2e803` | local exists |
| current-main merged scaleout report | `work/scaleout_merged_acceptance_surface_current702_20260608.md` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `aa4a73804d8494a7790f5d0d8317fb612cf0e6191a04f3d57f900498392e7734` | local exists |
| current-main scaleout locator/coordinate repair overlay | `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `b27361f058b8f4bf2221dc4e9c9b3c9e977ee71f4585806b499da9f3054ff685` | local exists |
| current-main scaleout repair report | `work/scaleout_locator_coordinate_repair_current702_20260608.md` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `c1f18d2f5c3de658b2ecd2e0356b979b63a84ee31f5f6d2431dcc24ce2e8a5ed` | local exists |
| current-main countable label unblocker matrix | `artifacts/v3_countable_label_unblocker_matrix_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `a2a37b6908ddfe9424104332bf1c27f95eccef617c6eb264d8071e071b663231` | local exists |
| current-main countable label unblocker report | `work/countable_label_unblocker_matrix_current702_20260608.md` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `ea23a2046f20412216cf3a5cca215f0f30a51edeffb0987884afbabe9e12887d` | local exists |
| current-main external Swiss-Prot/AFDB/Rhea pilot | `artifacts/v3_external_source_ingestion_pilot_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `d224e15dca0c0f56237510ae1be70b07ab28170dbb088422c2868cb3799e269d` | local exists |
| current-main pilot import preview | `artifacts/v3_external_source_ingestion_import_preview_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `237759dda87fe16872d5db974911180796ef8d1cea085a9bd0ad888322b9bb87` | local exists |
| current-main admission validation for 16 pilot preview rows | `artifacts/v3_external_source_admission_validation_16_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `b68ea16fbcffc8cb2cd895db213ce6c74879f1d9536dad4571ac053e172c02c1` | local exists |
| current-main admission-ready preview for 16 pilot rows | `artifacts/v3_external_source_admission_ready_preview_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `09d6a3d9c9c38bfcd896f2401a504e2f5f31f83b8291f10864c8f4d2706982d4` | local exists |
| current-main external bulk ingestion scout | `artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `1d0b1637f2d17ad4a72d6f6599b4c67dee4f15267a434a146de67aca048501dc` | local exists |
| current-main external bulk provisional preview | `artifacts/v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `97b8bfbc48f6b9daeb79742a90493ce7a068ea1ce9511f0f98922bff19f04644` | local exists |
| completed branch bulk pagination scaleout | `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json` | `origin/ce-external-bulk-pagination-scaleout-20260609` | `595c7ac850aa32c1fc2f6ba257bf1a370499747f` | `3804f45dec32578ddab615abf78a8aadfc6d9591065bcd0ab19a1dbcf23e8592` | git-ref accessible |
| completed branch scaleout provisional preview | `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_provisional_import_preview_current702_20260609.json` | `origin/ce-external-bulk-pagination-scaleout-20260609` | `595c7ac850aa32c1fc2f6ba257bf1a370499747f` | `5d37f102a095ee3dfa1a1bcd7fbc62b186232b60f71938499f0db665b4a43001` | git-ref accessible |
| completed branch scaleout report | `origin/ce-external-bulk-pagination-scaleout-20260609:work/external_bulk_ingestion_scaleout_current702_20260609.md` | `origin/ce-external-bulk-pagination-scaleout-20260609` | `595c7ac850aa32c1fc2f6ba257bf1a370499747f` | `1c5a9aef31fefb6a90a2eaa0700b7ee15732e3f97a9877a3859007a31cf89da3` | git-ref accessible |
| completed branch materialization/admission batch | `origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_admission_batch_current702_20260608.json` | `origin/ce-external-materialization-admission-batch-20260608` | `1f61a2dcf4e6268a65ee53d61e508cf878695f27` | `ce0cd844c465fcd28181d087f6d807bc90f8b0f47df951572564acca9540f9a6` | git-ref accessible |
| completed branch materialization import-ready preview | `origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_import_ready_preview_current702_20260608.json` | `origin/ce-external-materialization-admission-batch-20260608` | `1f61a2dcf4e6268a65ee53d61e508cf878695f27` | `b771d847359392ccc17c472906b8497012071ebc7b5c1d284f1d8fb2313b926e` | git-ref accessible |
| completed branch materialization report | `origin/ce-external-materialization-admission-batch-20260608:work/external_materialization_admission_batch_current702_20260608.md` | `origin/ce-external-materialization-admission-batch-20260608` | `1f61a2dcf4e6268a65ee53d61e508cf878695f27` | `3ab20693e7fc5c1a4973fc352a2c2c41d6a368bc34da5fdc81e063ad7eb96c01` | git-ref accessible |
| completed branch external admission QA merged surface | `origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_merged_surface_current702_20260609.json` | `origin/ce-external-admission-qa-merger-20260609` | `ec9deee9c22013659277cf0009a8a4d4eb185671` | `ecf2103e9a95fc5ffa870de63c0faf88022c8cceeda34d4fe774b9c9380a211b` | git-ref accessible |
| completed branch external admission import-ready preview | `origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_import_ready_preview_current702_20260609.json` | `origin/ce-external-admission-qa-merger-20260609` | `ec9deee9c22013659277cf0009a8a4d4eb185671` | `07dfa19f68822ffb3fd7a78bfc3b7c5645c6694ef55dc01d6ecdf7c9747bd713` | git-ref accessible |
| completed branch external admission repair queue | `origin/ce-external-admission-qa-merger-20260609:artifacts/v3_external_admission_repair_queue_current702_20260609.json` | `origin/ce-external-admission-qa-merger-20260609` | `ec9deee9c22013659277cf0009a8a4d4eb185671` | `4e85e665f8097a01df2df35638ad22c2599d6dcf96af4efa276e9d822648c3bd` | git-ref accessible |
| completed branch admission QA report | `origin/ce-external-admission-qa-merger-20260609:work/external_admission_qa_merger_current702_20260609.md` | `origin/ce-external-admission-qa-merger-20260609` | `ec9deee9c22013659277cf0009a8a4d4eb185671` | `4e4f6f0144d9421aaec881748be1aa4c843c02d5dcb6f5b5aadec0a5085a8bf5` | git-ref accessible |
| current-main materialized copy of completed bulk pagination scaleout | `artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `3804f45dec32578ddab615abf78a8aadfc6d9591065bcd0ab19a1dbcf23e8592` | local exists |
| current-main materialized copy of scaleout provisional preview | `artifacts/v3_external_bulk_ingestion_scaleout_provisional_import_preview_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `5d37f102a095ee3dfa1a1bcd7fbc62b186232b60f71938499f0db665b4a43001` | local exists |
| current-main external admission QA merged surface | `artifacts/v3_external_admission_merged_surface_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `ecf2103e9a95fc5ffa870de63c0faf88022c8cceeda34d4fe774b9c9380a211b` | local exists |
| current-main external admission import-ready preview | `artifacts/v3_external_admission_import_ready_preview_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `07dfa19f68822ffb3fd7a78bfc3b7c5645c6694ef55dc01d6ecdf7c9747bd713` | local exists |
| current-main external admission repair queue | `artifacts/v3_external_admission_repair_queue_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `4e85e665f8097a01df2df35638ad22c2599d6dcf96af4efa276e9d822648c3bd` | local exists |
| current-main external materialization Wave 2 surface | `artifacts/v3_external_materialization_wave2_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `73686414677506c7c89922c15637c18cbb8fb4cad2eb4f29348deb91c3c3ab29` | local exists |
| current-main external materialization Wave 2 import-ready preview | `artifacts/v3_external_materialization_wave2_import_ready_preview_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `0c7d27e641ba4735076f44a5e85acadb1d64fbbf95650bf133fd9e3101b48655` | local exists |
| current-main external materialization Wave 2 repair queue | `artifacts/v3_external_materialization_wave2_repair_queue_current702_20260609.json` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `8b1b78e41a4c3bc8189418ffb8c7cded0afec85e030989c226ecc8ab5982bb1f` | local exists |
| current-main external materialization Wave 2 review-only locator sidecar directory | `artifacts/external_materialization_wave2_source_free_locators_current702_20260609` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `-` | local exists |
| current-main external materialization Wave 2 report | `work/external_materialization_wave2_current702_20260609.md` | `origin/main` | `4190c5a27c341d49efc5980041ffea270812ce01` | `eab7c848a9f4d6f24b3ac908944ccca3d824adf90e4da3ef5966cb20da88421b` | local exists |

## Prior Lesson Artifacts

| Category | Artifact | Why it matters | Exists |
| --- | --- | --- | --- |
| `predicted_geometry_reconstruction` | `artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json` | Diagnoses the predicted apo geometry drop as cofactor-loss dominated. | True |
| `predicted_geometry_reconstruction` | `artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json` | Bounds the recoverable ceiling when missing cofactors are restored. | True |
| `predicted_geometry_reconstruction` | `artifacts/v3_cofactor_graft_fidelity_probe_current702_20260604.json` | Checks realistic cofactor graft fidelity before deployment claims. | True |
| `predicted_geometry_reconstruction` | `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json` | Fits the leakage-safe sequence-to-cofactor reconstruction channel on train/cal only. | True |
| `predicted_geometry_reconstruction` | `artifacts/v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json` | Confirms the spent heldout one-shot recovery and precision cost. | True |
| `fold_cofactor_confounding` | `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json` | Shows representation decoder/fold joins are confounded without careful readthrough. | True |
| `fold_cofactor_confounding` | `artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json` | Records deployment-readiness limits for fold-augmented predicted structure channels. | True |
| `fold_cofactor_confounding` | `artifacts/v3_fold_augmented_confounded_deployment_closure_audit_current702_20260601.json` | Closes the confounded deployment surface before threshold claims. | True |
| `fold_cofactor_confounding` | `artifacts/v3_cofactor_presence_calibration_current702_20260604.json` | Source-free sequence cofactor heads motivating cofactor-axis expansion. | True |
| `fold_cofactor_confounding` | `artifacts/v3_lever2_source_free_electron_flow_current_split_operating_point_readout_current702_20260606.json` | Electron-flow readout motivates redox precision lanes without heldout retuning. | True |
| `source_free_locator_materialization` | `artifacts/v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json` | Defines source-free locator schema expected before countable import. | True |
| `source_free_locator_materialization` | `artifacts/v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json` | Records the locator materialization plan and no-import gating. | True |
| `near_orphan_oos_bins` | `artifacts/v3_mechanism_prediction_orphan_eval_design_702_20260525.json` | Motivates explicit near-orphan/orphan evaluation bins. | True |
| `near_orphan_oos_bins` | `artifacts/v3_near_orphan_geometry_support_review_packet_702_20260526.json` | Captures near-orphan geometry-support review packet. | True |
| `near_orphan_oos_bins` | `artifacts/v3_packet2_near_orphan_geometry_support_decision_closure_702_20260527.json` | Closes near-orphan geometry-support decisions used for lane selection. | True |
| `near_orphan_oos_bins` | `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json` | Frames OOS/diversity evaluation as an atlas requirement. | True |

## Ledger Validation

- `factory_candidate_count_matches_rows`: `True`
- `factory_admission_counts_sum_to_candidates`: `True`
- `acquisition_counts_sum_to_rows`: `True`
- `merged_source_rows_reconcile`: `True`
- `merged_canonical_rows_reconcile`: `True`
- `unblocker_target_rows_reconcile`: `True`
- `bulk_scaleout_rows_reconcile`: `True`
- `bulk_scaleout_preview_rows_reconcile`: `True`
- `materialization_rows_reconcile`: `True`
- `materialization_preview_reconcile`: `True`
- `admission_rows_reconcile`: `True`
- `admission_preview_rows_reconcile`: `True`
- `admission_repair_queue_rows_reconcile`: `True`
- `all_local_source_paths_exist`: `True`
- `all_remote_source_specs_available`: `True`
- `all_lesson_paths_exist`: `True`
- `passed`: `True`
- `wave2_rows_reconcile`: `True`
- `wave2_preview_rows_reconcile`: `True`
- `wave2_repair_queue_rows_reconcile`: `True`
- `wave2_sidecar_count_reconciles`: `True`

