# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Retained-OOS Feature Target - current702

Run: 2026-06-02T11:10:26Z

Review-only target analysis for richer label-stripped row-specific bond/proton/electron feature families on retained calibration OOS misses. Candidate tokens are derived from approved event types, event/residue-role links, residue-code counts, participant-role counts, and event arity; source text, source IDs, EC/Rhea IDs, accessions, names, and labels are excluded from predictive tokens.

## Status

- p0_oos_augmented_retained_oos_feature_target_ready
- Retained OOS failure rows: 14
- Priority retained OOS failure rows: 5
- Feature families scanned: 14
- Ready candidate feature families: ['event_residue_code', 'event_residue_code_count', 'event_residue_role_count', 'residue_role_count', 'event_mapped_residue_count', 'event_participant_arity', 'event_type_sequence', 'event_mapped_residue_bucket']
- Critical violations: 0

## Feature Families

| family | priority contrast rows | retained contrast rows | top tokens |
| --- | ---: | ---: | ---: |
| event_residue_code | 5 | 14 | 8 |
| event_residue_code_count | 5 | 14 | 8 |
| event_residue_role_count | 5 | 14 | 8 |
| residue_role_count | 5 | 14 | 8 |
| event_mapped_residue_count | 5 | 13 | 8 |
| event_participant_arity | 5 | 13 | 8 |
| event_type_sequence | 5 | 13 | 8 |
| event_mapped_residue_bucket | 5 | 9 | 8 |
| residue_code_count | 4 | 13 | 8 |
| participant_role_count | 4 | 12 | 8 |
| event_type_count | 4 | 9 | 4 |
| event_residue_role | 3 | 12 | 8 |

## Retained Row Coverage

| row | priority | nearest primary | contrast families |
| --- | --- | --- | --- |
| m_csa:2 | borderline_contract_miss | ser_his_acid_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count |
| m_csa:23 | near_contract_miss | ser_his_acid_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, residue_code_count, residue_role_count |
| m_csa:49 | strong_primary_alias | heme_peroxidase_oxidase | event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count, residue_role_present |
| m_csa:59 | strong_primary_alias | heme_peroxidase_oxidase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count |
| m_csa:70 | strong_primary_alias | metal_dependent_hydrolase | event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, participant_role_count, residue_code_count, residue_role_count |
| m_csa:78 | strong_primary_alias | metal_dependent_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count |
| m_csa:101 | strong_primary_alias | ser_his_acid_hydrolase | event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count, residue_role_present |
| m_csa:149 | near_contract_miss | ser_his_acid_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count |
| m_csa:246 | strong_primary_alias | flavin_dehydrogenase_reductase | event_mapped_residue_count, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_sequence, residue_code_count, residue_role_count, residue_role_present |
| m_csa:256 | near_contract_miss | heme_peroxidase_oxidase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count |
| m_csa:263 | strong_primary_alias | metal_dependent_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count, residue_role_present |
| m_csa:273 | borderline_contract_miss | metal_dependent_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_role_count |
| m_csa:312 | strong_primary_alias | heme_peroxidase_oxidase | event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count, residue_role_present |
| m_csa:318 | strong_primary_alias | ser_his_acid_hydrolase | event_mapped_residue_bucket, event_mapped_residue_count, event_participant_arity, event_residue_code, event_residue_code_count, event_residue_role, event_residue_role_count, event_type_count, event_type_sequence, participant_role_count, residue_code_count, residue_role_count, residue_role_present |

## Top Candidate Tokens

| token | priority hits | contrast rows | cal primary hits | score |
| --- | ---: | ---: | ---: | ---: |
| event_residue_role:bond_formed|electrostatic_stabiliser | 3 | 7 | 1 | 20 |
| event_residue_role_count:proton_transfer|electrostatic_stabiliser=1 | 2 | 5 | 0 | 14 |
| residue_role_present:hydrogen_bond_acceptor | 5 | 0 | 4 | 13 |
| event_residue_role:proton_transfer|electrostatic_stabiliser | 3 | 2 | 0 | 13 |
| event_residue_role_count:bond_formed|electrostatic_stabiliser=1 | 2 | 6 | 1 | 13 |
| residue_role_present:hydrogen_bond_donor | 5 | 0 | 4 | 12 |
| residue_role_present:activator | 2 | 1 | 1 | 12 |
| participant_role_count:product=2 | 1 | 4 | 1 | 12 |
| residue_role_count:hydrogen_bond_donor=2 | 3 | 3 | 2 | 11 |
| event_residue_code:proton_transfer|tyr | 2 | 4 | 0 | 11 |
| event_residue_code:proton_transfer|his | 2 | 2 | 1 | 11 |
| event_residue_role:proton_transfer|hydrogen_bond_acceptor | 4 | 0 | 3 | 10 |

## Decision

- Feature family ready for expanded sidecar: True
- Next gate: Materialize the highest-coverage ready candidate families in a strict train/cal-only expanded sidecar, then rerun the no-template centroid and residual methods without changing the frozen residual contract until the new calibration artifact explicitly replaces it.

## Interpretation

- 8 candidate feature families cover every borderline/near retained OOS miss with at least one token not seen in that row's nearest-primary train/cal contrast set.
- Promote the top ready feature families into a train/cal-only expanded feature sidecar and rerun the calibration diagnostics.
