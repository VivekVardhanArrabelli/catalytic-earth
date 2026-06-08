# Glycoside / Nucleoside Scale-Out Shard

- Artifact: `artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json`
- Artifact ID: `v3_scaleout_glycoside_nucleoside_shard_current702_20260608`
- STARTED_AT_UTC: `2026-06-08T14:12:10Z`
- STARTED_AT_LOCAL: `2026-06-08T09:12:10-0500`
- CREATED_UTC: `2026-06-08T14:24:20Z`
- ELAPSED_MINUTES_AT_WRITE: `13.799`
- Candidate rows: `835`
- Validation passed: `True`

## Scope

Source-free candidate/evidence lane for glycoside hydrolases, nucleoside hydrolases, glycosidase boundary controls, TIM-barrel fold confounders, locator repair opportunities, and mechanistically distinct OOS rows useful for abstention. No registry edits, imports, promotions, production thresholds, splits, or model weights were changed.

## Terminal States

- `blocked_coordinate`: 44
- `blocked_family_decision`: 50
- `blocked_locator`: 97
- `countable_candidate_preflight_only`: 1
- `reject/OOS_preserve_signal`: 233
- `review_only_evidence`: 410

## Family Lanes

- `background_family_control_lane`: 384; representatives: `uniprot:H3JQW0`, `uniprot:I2DBY1`, `uniprot:K7N5M8`, `uniprot:O15229`, `uniprot:P04040`, `uniprot:P06181`, `uniprot:P06617`, `uniprot:P11295`, `uniprot:P11678`, `uniprot:P12015`, `uniprot:P13029`, `uniprot:P14532`
- `family_decision_repair_lane`: 48; representatives: `uniprot:A6NJ78`, `uniprot:O15247`, `uniprot:O43252`, `uniprot:O95050`, `uniprot:O95340`, `uniprot:O95819`, `uniprot:P00568`, `uniprot:P0A7B1`, `uniprot:P20485`, `uniprot:P27144`, `uniprot:P32189`, `uniprot:P40261`
- `glycosidase_boundary_control_lane`: 5; representatives: `uniprot:A2RU49`, `m_csa:17`, `m_csa:695`, `m_csa:91`, `m_csa:970`
- `glycoside_nucleoside_hydrolase_control_lane`: 102; representatives: `uniprot:C5G6D7`, `uniprot:O15527`, `uniprot:O34539`, `uniprot:O42807`, `uniprot:O60568`, `uniprot:O95461`, `uniprot:P04062`, `uniprot:P04843`, `uniprot:P04844`, `uniprot:P06276`, `uniprot:P06744`, `uniprot:P06746`
- `locator_coordinate_repair_lane`: 111; representatives: `uniprot:A1L0T0`, `uniprot:A2RUC4`, `uniprot:A5PLL7`, `uniprot:O43593`, `uniprot:O43708`, `uniprot:O75151`, `uniprot:O75521`, `uniprot:O95470`, `uniprot:O95571`, `uniprot:O95881`, `uniprot:P00374`, `uniprot:P04179`
- `mechanistically_distinct_oos_abstention_lane`: 178; representatives: `uniprot:C9JRZ8`, `uniprot:O14756`, `uniprot:O75828`, `uniprot:O95154`, `uniprot:O95479`, `uniprot:P00338`, `uniprot:P04406`, `uniprot:P04424`, `uniprot:P11086`, `uniprot:P14060`, `uniprot:P22830`, `uniprot:P30566`
- `tim_barrel_fold_confounder_lane`: 7; representatives: `uniprot:P0DUB6`, `uniprot:P60174`, `uniprot:Q9BV20`, `m_csa:324`, `m_csa:328`, `m_csa:397`, `m_csa:550`

## Subfamily Highlights

- `metal_hydrolase_subclasses_background_control`: 247
- `mechanistically_distinct_oos_abstention_control`: 178
- `locator_or_coordinate_repair_opportunity`: 111
- `redox_oxygen_transfer_and_sulfur_lipoamide_background_control`: 79
- `family_decision_repair_opportunity`: 48
- `plp_child_subclasses_background_control`: 33
- `glycosyltransferase_boundary_control`: 21
- `dna_glycosylase_lyase_control`: 16
- `radical_cobalamin_sam_like_probes_background_control`: 11
- `supplemental_source_free_control`: 10
- `carbohydrate_esterase_overlap`: 9
- `glycoside_or_nucleoside_hydrolase_general_control`: 9
- `polysaccharide_lyase_hard_boundary`: 8
- `retaining_glycoside_hydrolase_two_carboxylates`: 8
- `sugar_isomerase_hard_boundary`: 7
- `non_carbohydrate_TIM_barrel_hard_negative`: 5
- `near_orphan_or_unrepresented_mechanism_tail_background_control`: 4
- `inverting_glycoside_hydrolase`: 3
- `non_carbohydrate_esterase_hard_negative`: 3
- `nucleoside_hydrolase_reference_control`: 3
- `nucleoside_phosphorylase_boundary_control`: 3
- `substrate_assisted_glycoside_hydrolase`: 3
- `non_carbohydrate_isomerase_hard_negative`: 2
- `substrate_assisted_glycosidase_candidate`: 2
- `tim_barrel_glycosidase_collision_positive`: 2
- `dna_glycosylase_boundary`: 1
- `dna_glycosylase_lyase_boundary`: 1
- `dna_lyase_boundary`: 1
- `glycosidase_lyase_boundary`: 1
- `glycoside_hydrolase_acid_base_variant`: 1

## Validation

- Required row field violations: `0`
- Terminal state violations: `0`
- Source-hash violations: `0`
- Duplicate-axis violations: `0`
- Row hash violations: `0`
- Mechanism-text field violations: `0`

## Next Actions

- Review direct glycoside/nucleoside rows and the explicit nucleoside hydrolase reference controls before any merger-lane import decision.
- Use `blocked_locator`, `blocked_coordinate`, and `blocked_family_decision` rows as machine-actionable repair queues.
- Preserve `reject/OOS_preserve_signal` rows as abstention controls unless new evidence changes the terminal state.
