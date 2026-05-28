# External Panel Router Queue - 2026-05-28

Review-only normalization of completed external panel scouts. No labels, registries, thresholds, scoring, imports, or model outputs were changed.

## Summary

- `unique_candidate_count`: 273
- `source_panel_input_counts`: {'flavin_redox': 48, 'metal_hydrolase_tail': 74, 'heme_redox_boundary': 46, 'plp_child_mechanism': 50, 'glycoside_carbohydrate': 60, 'mcsa_card_crossmap': 9}
- `readiness_tier_mentions`: {'unspecified': 149, 'gold': 38, 'silver': 42, 'review-only': 24, 'bronze': 20}
- `panel_role_mentions_top20`: {'near_family_hard_negative': 55, 'positive': 31, 'positive_anchor': 29, 'oos_hard_negative': 20, 'external_positive_lead': 20, 'review_only_positive_lead': 16, 'OOS_hard_negative': 13, 'out_of_scope_control': 11, 'unspecified': 9, 'mcsa_positive_anchor': 8, 'hard_negative': 7, 'positive_child_anchor': 6, 'silver_positive_lead': 6, 'boundary_hard_negative_for_peroxidase_terminal_oxidase': 5, 'external_positive_like_terminal_duplicate_control': 5, 'positive_future_child': 4, 'external_ligninolytic_peroxidase': 4, 'oos_hard_negative_for_heme_panel': 3, 'source_clean_lead': 3, 'duplicate_family_hold': 3}
- `multi_panel_candidate_count`: 14
- `hard_negative_or_control_count`: 123
- `priority_review_or_materialization_count`: 40

## Priority Review / Materialization Set

- `m_csa:497`: nitric-oxide reductase (FMN) | panels=flavin_redox,heme_redox_boundary | routes=flavodiiron_no_reductase; non_heme_diiron_redox
- `m_csa:131`: 4-hydroxybenzoate 3-monooxygenase | panels=flavin_redox,heme_redox_boundary | routes=flavin_monooxygenase; flavin_monooxygenase_c4a_peroxy_oxygen_transfer
- `m_csa:551`: phenol 2-monooxygenase | panels=flavin_redox,heme_redox_boundary | routes=flavin_monooxygenase_c4a_peroxy_oxygen_transfer; flavin_monooxygenase_future_support
- `m_csa:973`: DszC protein | panels=flavin_redox,heme_redox_boundary | routes=flavin_monooxygenase_c4a_peroxy_oxygen_transfer; two_component_fmnh2_monooxygenase
- `m_csa:141`: 4-cresol dehydrogenase (hydroxylating) | panels=flavin_redox,heme_redox_boundary | routes=flavin_heme_hydroxylating_boundary; heme_plus_flavin_electron_transfer
- `m_csa:128`: Photinus-luciferin 4-monooxygenase (ATP-hydrolysing) | panels=flavin_redox,heme_redox_boundary | routes=luciferase_atp_oxygenase; nonflavin_oxygenase_hard_negative
- `m_csa:129`: taurine dioxygenase | panels=flavin_redox,heme_redox_boundary | routes=non_heme_iron_oxygenase; nonflavin_oxygenase_hard_negative
- `m_csa:130`: naphthalene 1,2-dioxygenase | panels=flavin_redox,heme_redox_boundary | routes=nonflavin_oxygenase_hard_negative; rieske_non_heme_iron_oxygenase
- `m_csa:133`: camphor 5-monooxygenase | panels=flavin_redox,heme_redox_boundary | routes=nonflavin_oxygenase_hard_negative; p450_boundary
- `m_csa:134`: tyrosine 3-monooxygenase | panels=flavin_redox,heme_redox_boundary | routes=nonflavin_oxygenase_hard_negative; pterin_non_heme_iron_monooxygenase
- `m_csa:135`: peptidylglycine monooxygenase | panels=flavin_redox,heme_redox_boundary | routes=copper_oxygenase; nonflavin_oxygenase_hard_negative
- `m_csa:699`: cytochrome P450 (BM-3) | panels=flavin_redox,heme_redox_boundary | routes=nonflavin_oxygenase_hard_negative; p450_boundary
- `m_csa:795`: heme oxygenase (biliverdin-producing) | panels=flavin_redox,heme_redox_boundary | routes=heme_oxygenase_boundary; nonflavin_oxygenase_hard_negative
- `mh_035`: beta-lactamase (Class B1) | panels=metal_hydrolase_tail | routes=metallo_beta_lactamase_like; seed_fingerprint:metal_dependent_hydrolase
- `mh_036`: beta-lactamase (Class B1) | panels=metal_hydrolase_tail | routes=metallo_beta_lactamase_like; seed_fingerprint:metal_dependent_hydrolase
- `mh_037`: cerebroside-sulfatase | panels=metal_hydrolase_tail | routes=seed_fingerprint:metal_dependent_hydrolase; sulfatase_fgly_metal_boundary
- `mh_040`: H+-transporting two-sector ATPase (F-type, mitochondrial) | panels=metal_hydrolase_tail | routes=ntpase_nucleotide_hydrolase_boundary; out_of_scope
- `mh_041`: chaperonin ATPase | panels=metal_hydrolase_tail | routes=ntpase_nucleotide_hydrolase_boundary; out_of_scope
- `mh_042`: G-protein alpha subunit, group I (GTPase) | panels=metal_hydrolase_tail | routes=ntpase_nucleotide_hydrolase_boundary; out_of_scope
- `mh_043`: myosin ATPase | panels=metal_hydrolase_tail | routes=ntpase_nucleotide_hydrolase_boundary; reviewed_or_candidate_control_no_current_parent_label

## No-Go Conditions

- do not train on this queue as gold labels
- do not import labels from this queue
- do not use source prose as predictive evidence
- do not claim external generalization until exact coordinates/leakage checks are materialized
