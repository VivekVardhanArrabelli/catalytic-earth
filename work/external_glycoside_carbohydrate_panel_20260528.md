# Glycoside/Carbohydrate External Stress Panel - 2026-05-28

Review-only validation-panel design and source/evidence scouting artifact. This run did not edit labels, registries, ontologies, thresholds, production scoring, imports, or model outputs. No coordinate downloads were performed.

Outputs:

- `artifacts/v3_external_glycoside_carbohydrate_panel_20260528.json`
- `work/external_glycoside_carbohydrate_panel_20260528.md`

## Scope

Goal: test the evidence router outside the current five broad v1 families using carbohydrate-active enzymes that expose same-fold/different-mechanism and acid/base geometry issues.

This panel covers:

- retaining glycoside hydrolases with two carboxylates
- inverting glycoside hydrolases
- glycoside/polysaccharide lyases and sugar isomerases as hard boundaries
- TIM-barrel glycosidase collisions with unrelated TIM-barrel redox/metabolic enzymes
- carbohydrate esterases versus glycoside hydrolase overlap
- non-carbohydrate TIM-barrel and esterase hard negatives

## Assessment

This is a good first non-M-CSA-heavy external generalization panel for review-only validation design, not for import. The manifest has 60 rows: 39 external UniProt/PDB leads and 21 M-CSA anchors/controls. Sourcing is not too sparse for a no-decision router panel because several external rows already have reviewed active-site annotations and structures, and local artifacts already show the intended failure mode on `Q6NSJ0`.

It is still too sparse for label import or production claims. Many external leads need current-reference sequence screens, current-countable Foldseek screens, explicit substrate/analog-state inspection, and terminal review. Every row is frozen as non-countable and non-importable.

## Counts

| Lane | Rows |
| --- | ---: |
| carbohydrate_esterase_overlap | 9 |
| dna_glycosylase_boundary | 1 |
| dna_glycosylase_lyase_boundary | 1 |
| dna_lyase_boundary | 1 |
| glycosidase_lyase_boundary | 1 |
| glycoside_hydrolase_acid_base_variant | 1 |
| glycosyltransferase_and_metal_hydroxylase_boundary | 1 |
| inverting_glycoside_hydrolase | 3 |
| inverting_or_single_acid_glycoside_hydrolase | 1 |
| n_glycosidase_boundary | 1 |
| non_carbohydrate_TIM_barrel_hard_negative | 5 |
| non_carbohydrate_esterase_hard_negative | 3 |
| non_carbohydrate_isomerase_hard_negative | 2 |
| non_carbohydrate_metabolic_hard_negative | 1 |
| non_glycan_glycosidic_hydrolase_boundary | 1 |
| polysaccharide_lyase_hard_boundary | 8 |
| retaining_glycoside_hydrolase_two_carboxylates | 8 |
| substrate_assisted_glycoside_hydrolase | 3 |
| sugar_isomerase_hard_boundary | 7 |
| tim_barrel_glycosidase_collision_positive | 2 |

| Provenance tier | Rows |
| --- | ---: |
| tier_A_mcsa_curated | 21 |
| tier_B_external_curated | 19 |
| tier_C_external_incomplete | 7 |
| tier_D_control_only | 13 |

| Candidate role | Rows |
| --- | ---: |
| OOS_hard_negative | 13 |
| external_lead_incomplete | 1 |
| external_positive_lead | 8 |
| mcsa_positive_anchor | 8 |
| near_family_hard_negative | 27 |
| packet1_fold_conflict_anchor_with_TIM_caveat | 1 |
| packet1_router_abstention_anchor | 1 |
| sequence_holdout_control | 1 |

## Packet 1 Reuse

`m_csa:428` is retained as a caveated retaining-glycosidase/TIM-barrel collision control. Existing Packet 1 evidence says it has incidental primary TIM-barrel Foldseek hits but most high-TM neighbors are glycosidase-like OOS rows, so it should not be treated as a clean fold-conflict anchor.

`m_csa:440` is retained as an inverting glycosidase near-orphan abstention control. Existing Packet 1 evidence says it had zero targeted TM-pair hits and should test router abstention/no-neighbor behavior rather than fold-conflict rescue.

## Success Criteria

Foldseek success:

- Retaining/inverting glycoside hydrolases can find same-CAZy or TIM-barrel neighbors, but fold alone must not promote non-carbohydrate TIM barrels or carbohydrate esterases.
- `m_csa:428` is reported as caveated fold collision; `m_csa:440` remains near-orphan abstention diagnostic.
- Lyase/isomerase/esterase hard negatives either cluster with their own mechanism family or abstain.

Geometry rescue:

- Retaining GH rows require role-assigned acidic residues around glycosidic C1 geometry.
- Inverting GH rows require acid plus water-activating base geometry, not a covalent glycosyl-enzyme nucleophile.
- GH18 substrate-assisted rows use N-acetyl substrate participation rather than a second enzyme nucleophile.
- Carbohydrate esterases separate by ester/acyl-enzyme geometry, not glycan wording.

Learned-representation value add:

- Helpful if it separates glycosidase leads from TIM/isomerase controls when sequence/Foldseek is ambiguous.
- Helpful if carbohydrate esterases group closer to serine/aspartate esterases than retaining glycosidases.
- Not helpful if it reproduces EC/name keywords or merges all TIM barrels.

Correct abstention:

- Abstain on tier C rows missing residue-role evidence or duplicate screens.
- Abstain or reject exact/near sequence holdouts such as `O15527`.
- Abstain on non-carbohydrate TIM barrels, glycosyltransferases, and metabolic isomerases if no supported non-v1 route exists.

## Candidate Rows

| # | Row | Lane | Role | Tier | Structure | Expected router behavior |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `uniprot:Q6NSJ0` | retaining_glycoside_hydrolase_two_carboxylates | external_positive_lead | tier_B_external_curated | pdb_or_alphafold_available | route_to_review_only_glycoside_hydrolase_candidate_not_generic_metal_hydrolase |
| 2 | `uniprot:P0DUB6` | tim_barrel_glycosidase_collision_positive | external_positive_lead | tier_B_external_curated | pdb_or_alphafold_available | route_to_review_only_retaining_glycosidase_TIM_barrel_candidate |
| 3 | `uniprot:Q9H227` | retaining_glycoside_hydrolase_two_carboxylates | external_positive_lead | tier_B_external_curated | pdb_or_alphafold_available | route_to_review_only_retaining_beta_glucosidase_candidate |
| 4 | `uniprot:Q9Y3R4` | glycoside_hydrolase_acid_base_variant | external_positive_lead | tier_B_external_curated | pdb_or_alphafold_available | route_to_review_only_sialidase_glycosidase_candidate_with_no_generic_hydrolase_import |
| 5 | `uniprot:Q9BZP6` | substrate_assisted_glycoside_hydrolase | external_positive_lead | tier_B_external_curated | pdb_or_alphafold_available | route_to_review_only_chitinase_candidate_with_substrate_assisted_geometry_check |
| 6 | `uniprot:Q13231` | substrate_assisted_glycoside_hydrolase | external_positive_lead | tier_B_external_curated | pdb_or_alphafold_available | route_to_review_only_chitinase_candidate_with_substrate_assisted_geometry_check |
| 7 | `uniprot:P38567` | inverting_or_single_acid_glycoside_hydrolase | external_positive_lead | tier_C_external_incomplete | pdb_or_alphafold_available | route_to_review_only_hyaluronidase_candidate_or_abstain_if_geometry_not_supported |
| 8 | `uniprot:P35573` | retaining_glycoside_hydrolase_two_carboxylates | external_positive_lead | tier_C_external_incomplete | pdb_or_alphafold_available | route_to_review_only_debranching_glycosidase_candidate_after_domain_disambiguation |
| 9 | `uniprot:Q86W56` | non_glycan_glycosidic_hydrolase_boundary | near_family_hard_negative | tier_C_external_incomplete | pdb_or_alphafold_available | abstain_or_route_to_ADP_ribose_glycohydrolase_review_only_not_glycan_GH |
| 10 | `uniprot:P30176` | n_glycosidase_boundary | external_lead_incomplete | tier_C_external_incomplete | pdb_or_alphafold_available | abstain_until_active_site_roles_are_sourced |
| 11 | `uniprot:P29372` | dna_glycosylase_boundary | near_family_hard_negative | tier_C_external_incomplete | pdb_or_alphafold_available | abstain_or_route_to_DNA_glycosylase_not_glycan_GH |
| 12 | `uniprot:P33025` | glycosidase_lyase_boundary | near_family_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_current_duplicate_or_abstain_as_metal_assisted_glycosidase_boundary |
| 13 | `uniprot:O15527` | dna_glycosylase_lyase_boundary | sequence_holdout_control | tier_D_control_only | pdb_or_alphafold_available | keep_as_exact_reference_holdout_or_abstain_not_external_positive |
| 14 | `uniprot:P06746` | dna_lyase_boundary | near_family_hard_negative | tier_C_external_incomplete | pdb_or_alphafold_available | route_to_DNA_lyase_review_only_or_abstain_not_glycoside_hydrolase |
| 15 | `uniprot:P39116` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_polysaccharide_lyase_beta_elimination_not_GH_hydrolysis |
| 16 | `uniprot:Q00704` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_chondroitin_lyase_not_GH_hydrolysis |
| 17 | `uniprot:Q9AQS0` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_xanthan_lyase_beta_elimination_not_GH_hydrolysis |
| 18 | `uniprot:C5G6D7` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_chondroitin_lyase_not_GH_hydrolysis |
| 19 | `uniprot:P0CZ00` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_hyaluronate_lyase_not_GH_hydrolysis |
| 20 | `uniprot:P34949` | sugar_isomerase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_or_abstain_as_isomerase_not_glycoside_hydrolase |
| 21 | `uniprot:P60174` | non_carbohydrate_TIM_barrel_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_TIM_barrel_metabolic_isomerase_not_glycosidase |
| 22 | `uniprot:P06744` | sugar_isomerase_hard_boundary | near_family_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_sugar_phosphate_isomerase_not_glycosidase |
| 23 | `uniprot:Q9BV20` | non_carbohydrate_TIM_barrel_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_isomerase_TIM_like_fold_not_glycosidase |
| 24 | `uniprot:P32140` | sugar_isomerase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_sugar_isomerase_not_glycosidase |
| 25 | `uniprot:P0A7Z0` | sugar_isomerase_hard_boundary | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_ribose_phosphate_isomerase_not_GH |
| 26 | `uniprot:P37351` | sugar_isomerase_hard_boundary | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_ribose_phosphate_isomerase_not_GH |
| 27 | `uniprot:P69922` | sugar_isomerase_hard_boundary | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | reject_as_metal_sugar_isomerase_not_GH |
| 28 | `uniprot:P14280` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | route_to_serine_or_aspartate_esterase_boundary_not_glycosidase |
| 29 | `uniprot:P0C1A9` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | route_to_carbohydrate_esterase_boundary_not_GH |
| 30 | `uniprot:Q09LX1` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | route_to_ser_his_acid_hydrolase_or_abstain_not_GH |
| 31 | `uniprot:O42807` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | route_to_ser_his_acid_hydrolase_or_abstain_not_GH |
| 32 | `uniprot:P83218` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_B_external_curated | pdb_or_alphafold_available | route_to_pectinesterase_boundary_not_GH |
| 33 | `uniprot:Q99034` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_C_external_incomplete | pdb_or_alphafold_available | abstain_until_full_ser_his_acid_triad_confirmed |
| 34 | `uniprot:O60568` | glycosyltransferase_and_metal_hydroxylase_boundary | near_family_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_or_abstain_as_transferase/hydroxylase_not_GH |
| 35 | `uniprot:P23872` | non_carbohydrate_esterase_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_generic_esterase_not_carbohydrate_GH |
| 36 | `uniprot:P06276` | non_carbohydrate_esterase_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_serine_esterase_not_carbohydrate_GH |
| 37 | `uniprot:Q9L9D7` | non_carbohydrate_esterase_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_serine_esterase_not_carbohydrate_GH |
| 38 | `uniprot:Q13907` | non_carbohydrate_isomerase_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_non_carbohydrate_isomerase |
| 39 | `uniprot:Q9BXS1` | non_carbohydrate_isomerase_hard_negative | OOS_hard_negative | tier_D_control_only | pdb_or_alphafold_available | reject_as_non_carbohydrate_isomerase |
| 40 | `m_csa:428` | retaining_glycoside_hydrolase_two_carboxylates | packet1_fold_conflict_anchor_with_TIM_caveat | tier_A_mcsa_curated | local_geometry_row_available | route_to_OOS_review_only_glycosidase_boundary_not_current_v1_hydrolase |
| 41 | `m_csa:440` | inverting_glycoside_hydrolase | packet1_router_abstention_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_OOS_review_only_inverting_glycosidase_or_correct_abstention |
| 42 | `m_csa:397` | tim_barrel_glycosidase_collision_positive | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_retaining_alpha_amylase_candidate_not_generic_TIM |
| 43 | `m_csa:422` | retaining_glycoside_hydrolase_two_carboxylates | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_retaining_beta_galactosidase_candidate |
| 44 | `m_csa:442` | retaining_glycoside_hydrolase_two_carboxylates | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_retaining_beta_glucosidase_candidate |
| 45 | `m_csa:432` | retaining_glycoside_hydrolase_two_carboxylates | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_retaining_xylanase_candidate |
| 46 | `m_csa:475` | inverting_glycoside_hydrolase | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_inverting_chitinase_candidate |
| 47 | `m_csa:478` | substrate_assisted_glycoside_hydrolase | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_substrate_assisted_chitinase_candidate |
| 48 | `m_csa:203` | retaining_glycoside_hydrolase_two_carboxylates | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_lysozyme_candidate |
| 49 | `m_csa:559` | inverting_glycoside_hydrolase | mcsa_positive_anchor | tier_A_mcsa_curated | local_geometry_row_available | route_to_review_only_inverting_cellulase_candidate |
| 50 | `m_csa:681` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | route_to_carbohydrate_esterase_boundary_not_glycoside_hydrolase |
| 51 | `m_csa:431` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | route_to_ser_his_acid_hydrolase_or_carbohydrate_esterase_boundary_not_GH |
| 52 | `m_csa:705` | carbohydrate_esterase_overlap | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | route_to_ser_his_acid_hydrolase_boundary_not_GH |
| 53 | `m_csa:184` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_polysaccharide_lyase_beta_elimination_not_GH |
| 54 | `m_csa:439` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_hyaluronate_lyase_beta_elimination_not_GH |
| 55 | `m_csa:441` | polysaccharide_lyase_hard_boundary | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_chondroitin_lyase_beta_elimination_not_GH |
| 56 | `m_csa:736` | sugar_isomerase_hard_boundary | near_family_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_mannose_phosphate_isomerase_not_GH |
| 57 | `m_csa:324` | non_carbohydrate_TIM_barrel_hard_negative | OOS_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_TIM_barrel_isomerase_not_glycosidase |
| 58 | `m_csa:328` | non_carbohydrate_TIM_barrel_hard_negative | OOS_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_TIM_barrel_metabolic_isomerase_not_glycosidase |
| 59 | `m_csa:550` | non_carbohydrate_TIM_barrel_hard_negative | OOS_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_aldolase_not_glycosidase |
| 60 | `m_csa:52` | non_carbohydrate_metabolic_hard_negative | OOS_hard_negative | tier_A_mcsa_curated | local_geometry_row_available | reject_as_metal_aldolase_not_glycosidase |

## Source Notes

Local source artifacts:

- `external_stress_panel_roadmap`: `artifacts/v3_external_stress_panel_roadmap_20260528.json`
- `glycoside_control_preregistration`: `artifacts/v3_glycoside_hydrolase_control_tranche_preregistration_20260520.json`
- `glycoside_axis_decisions`: `artifacts/v3_glycoside_hydrolase_control_tranche_axis_decisions_20260520.json`
- `glycoside_baseline_comparison`: `artifacts/v3_glycoside_hydrolase_control_tranche_baseline_comparison_20260520.json`
- `glycoside_boundary_control`: `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json`
- `pilot_active_site_evidence`: `artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json`
- `import_readiness_audit`: `artifacts/v3_external_source_import_readiness_audit_1025.json`
- `packet1_tm_disposition`: `work/packet1_tm_and_497_expert_disposition_20260527.md`
- `sequence_failure_benchmark_queue`: `work/sequence_failure_benchmark_queue_20260528.md`
- `mcsa_geometry_features`: `artifacts/v3_geometry_features_875.json`
- `foldseek_m_csa428_targeted_chunk`: `artifacts/v3_foldseek_tm_score_signal_1000_current702_wave1_target_m_csa428_query_chunk_423_20260527.json`
- `foldseek_m_csa440_targeted_chunk`: `artifacts/v3_foldseek_tm_score_signal_1000_current702_wave1_target_m_csa440_query_chunk_435_20260527.json`

External metadata source: UniProtKB REST search on 2026-05-28 plus RCSB PDB identifiers from UniProt cross-references. This was metadata-only scouting; no structure coordinate downloads were made.

## Non-Claims

This artifact is not a registry proposal, threshold change, import batch, model-output update, or performance claim. It is a frozen source/evidence candidate panel for future review-only router validation.
