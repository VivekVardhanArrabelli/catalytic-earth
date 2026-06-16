# Mechanism Representation Loop (leakage-safe self-feeding supply)

Run: 2026-06-16T18:06:46Z

First iteration of the self-feeding loop. A representation learned ONLY from review-only cofactor/ligand chemistry + active-site residue roles organises the bronze labels, triages bronze->silver promotion, and proposes candidates for the governor's holes. EC / protein-name / prose / lane / the fingerprint label / the frozen benchmark are never read.

- Feature space: ['flavin', 'plp', 'heme', 'iron_sulfur', 'sam', 'cobalamin', 'zinc', 'divalent_metal_other', 'calcium', 'cos_nad', 'cos_coa', 'cos_nucleotide_sugar', 'cos_2_oxoglutarate', 'cos_prenyl_diphosphate', 'bc_phosphomonoester', 'bc_phosphodiester', 'bc_peptide_cn', 'bc_amide_cn', 'bc_ester_hydrolysis', 'bc_glycoside_hydrolysis', 'bc_n_glycosidic_hydrolysis', 'bc_beta_lactam_hydrolysis', 'bc_redox_hydride', 'bc_phosphoryl_transfer', 'bc_atp_dependent_ligation', 'bc_glycosyl_transfer', 'bc_acyl_transfer', 'bc_methyl_transfer', 'bc_oxygenation', 'bc_decarboxylation', 'bc_carboxylation', 'bc_diphosphate_lyase', 'bc_isomerization', 'bc_carbon_carbon_lyase', 'bc_aldehyde_oxidation', 'acc_protein', 'acc_nucleoside', 'acc_sugar', 'catalytic_fraction', 'binding_fraction', 'active_site_size'].
- Excluded from representation: ['ec_numbers', 'fingerprint_id', 'label_type', 'protein_name', 'uniprot_prose', 'target_family_lane', 'rationale'].
- Seed labels: 6802; out_of_scope: 1224; centroids: ['aldehyde_dehydrogenase', 'alpha_beta_hydrolase_esterase_lipase', 'aminoglycoside_phosphotransferase', 'askha_sugar_acetate_kinase', 'atp_amide_ligase', 'biotin_dependent_carboxylase', 'class_ii_metal_aldolase', 'coa_acyltransferase', 'cobalamin_radical_rearrangement', 'cofactor_independent_isomerase', 'copper_oxidoreductase', 'cytochrome_p450_monooxygenase', 'deoxynucleoside_kinase', 'flavin_dehydrogenase_reductase', 'flavin_monooxygenase', 'ghmp_small_molecule_kinase', 'glycoside_hydrolase', 'glycosyltransferase', 'had_like_phosphatase', 'heme_peroxidase_oxidase', 'manganese_iron_superoxide_dismutase', 'metal_dependent_hydrolase', 'metal_independent_phosphodiesterase', 'metal_racemase_epimerase_non_plp', 'metallo_amidohydrolase_deaminase', 'metallopeptidase', 'metallophosphoesterase_nuclease', 'metallophosphomonoesterase', 'molybdopterin_oxidoreductase', 'n_ribosyl_hydrolase', 'nad_p_dehydrogenase', 'non_heme_iron_2og_dioxygenase', 'nucleoside_diphosphate_kinase', 'pfka_phosphofructokinase', 'pfkb_ribokinase_family', 'plp_dependent_enzyme', 'protein_kinase_ser_thr_tyr', 'radical_sam_enzyme', 'sam_methyltransferase', 'ser_his_acid_hydrolase', 'ser_thr_protein_phosphatase', 'serine_beta_lactamase', 'short_chain_dehydrogenase_reductase', 'terpene_cyclase_synthase', 'thiamine_diphosphate_enzyme', 'zinc_lyase_hydratase'].

## Promotion triage

- Leave-one-out self-consistency (chemistry alone recovers the fingerprint): 0.7523.
- Promotion candidates (cohesion >= 0.92): 3211.
- Review outliers (chemistry points at a different fingerprint): 1685.
- Coherent but below threshold: 1906.

## Hole proposals (model-ranked from out_of_scope)

- radical_sam_enzyme: centroid available; 0 proposed candidates.
- cobalamin_radical_rearrangement: centroid available; 4 proposed candidates.
- ser_his_acid_hydrolase: centroid available; 0 proposed candidates.

## Leakage guardrails

- Frozen benchmark read: False.
- EC/name/prose/lane used: False.
- Fingerprint label used as feature: False.
- Used only for candidate ranking + promotion triage, NEVER as a benchmark scorer.
- Registry written: False.
