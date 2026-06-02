# Mechanism Feature Row-Specific Bond-Change Materialization Priority - current702

Run: 2026-06-01T18:26:45Z

No-fit prioritization manifest for the row-specific bond-change evidence gap. It intersects the staged bond-change schema with the current train/cal feature contract and split manifest, but does not materialize source evidence, consume the feature, or fit a model.

## Status

- row_specific_bond_change_materialization_priority_ready_no_fit
- Rows requiring row-specific bond-change evidence: 232
- Priority tiers: {'P0_train_cal_feature_contract_gap': 171, 'P1_in_distribution_not_feature_contract_ready': 13, 'P2_heldout_final_only_evidence_gap': 48}
- Train/cal feature-contract gap rows: 171
- In-distribution not feature-contract-ready rows: 13
- Heldout final-only gap rows: 48
- Balanced P0 pilot seed rows: 15

## Fingerprints

- cobalamin_radical_rearrangement: 3
- flavin_dehydrogenase_reductase: 50
- flavin_monooxygenase: 2
- heme_peroxidase_oxidase: 20
- metal_dependent_hydrolase: 83
- plp_dependent_enzyme: 31
- radical_sam_enzyme: 1
- ser_his_acid_hydrolase: 42

## Chemical Operations

- cobalamin_radical_rearrangement: 3
- flavin_mediated_redox_transfer: 50
- flavin_peroxide_oxygen_transfer: 2
- heme_mediated_redox_catalysis: 20
- metal_activated_water_attack: 83
- nucleophilic_acyl_substitution: 42
- plp_stabilized_carbanion_chemistry: 31
- sam_derived_radical_chemistry: 1

## Balanced P0 Pilot Seed Queue

- m_csa:6 (flavin_dehydrogenase_reductase, calibration)
- m_csa:68 (flavin_dehydrogenase_reductase, train)
- m_csa:102 (flavin_dehydrogenase_reductase, train)
- m_csa:37 (heme_peroxidase_oxidase, train)
- m_csa:124 (heme_peroxidase_oxidase, train)
- m_csa:133 (heme_peroxidase_oxidase, calibration)
- m_csa:11 (metal_dependent_hydrolase, train)
- m_csa:15 (metal_dependent_hydrolase, train)
- m_csa:16 (metal_dependent_hydrolase, train)
- m_csa:66 (plp_dependent_enzyme, train)
- m_csa:147 (plp_dependent_enzyme, calibration)
- m_csa:186 (plp_dependent_enzyme, calibration)
- m_csa:5 (ser_his_acid_hydrolase, train)
- m_csa:94 (ser_his_acid_hydrolase, train)
- m_csa:169 (ser_his_acid_hydrolase, train)

## Interpretation

- The row-specific bond-change gap is now prioritized against the current no-fit train/cal feature contract: P0 rows are contract-ready except for missing source-backed bond-change evidence, while P1/P2 rows remain excluded from training or threshold use.
- Materialize the balanced P0 pilot seed queue from frozen source graphs/databases, audit the source-backed sidecar, then regenerate the train/cal feature contract only if the audit passes.
