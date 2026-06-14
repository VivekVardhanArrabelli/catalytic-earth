# Mechanism Representation Loop (leakage-safe self-feeding supply)

Run: 2026-06-14T07:54:41Z

First iteration of the self-feeding loop. A representation learned ONLY from review-only cofactor/ligand chemistry + active-site residue roles organises the bronze labels, triages bronze->silver promotion, and proposes candidates for the governor's holes. EC / protein-name / prose / lane / the fingerprint label / the frozen benchmark are never read.

- Feature space: ['flavin', 'plp', 'heme', 'iron_sulfur', 'sam', 'cobalamin', 'zinc', 'divalent_metal_other', 'calcium', 'cos_nad', 'cos_coa', 'cos_nucleotide_sugar', 'cos_2_oxoglutarate', 'cos_prenyl_diphosphate', 'bc_phosphomonoester', 'bc_phosphodiester', 'bc_peptide_cn', 'bc_amide_cn', 'bc_redox_hydride', 'bc_phosphoryl_transfer', 'bc_glycosyl_transfer', 'bc_acyl_transfer', 'bc_methyl_transfer', 'bc_oxygenation', 'bc_decarboxylation', 'bc_carboxylation', 'bc_diphosphate_lyase', 'bc_isomerization', 'catalytic_fraction', 'binding_fraction', 'active_site_size'].
- Excluded from representation: ['ec_numbers', 'fingerprint_id', 'label_type', 'protein_name', 'uniprot_prose', 'target_family_lane', 'rationale'].
- Seed labels: 5638; out_of_scope: 1224; centroids: ['askha_sugar_acetate_kinase', 'atp_amide_ligase', 'biotin_dependent_carboxylase', 'class_ii_metal_aldolase', 'coa_acyltransferase', 'cobalamin_radical_rearrangement', 'cofactor_independent_isomerase', 'copper_oxidoreductase', 'cytochrome_p450_monooxygenase', 'deoxynucleoside_kinase', 'flavin_dehydrogenase_reductase', 'flavin_monooxygenase', 'ghmp_small_molecule_kinase', 'glycoside_hydrolase', 'glycosyltransferase', 'heme_peroxidase_oxidase', 'manganese_iron_superoxide_dismutase', 'metal_dependent_hydrolase', 'metal_racemase_epimerase_non_plp', 'metallo_amidohydrolase_deaminase', 'metallopeptidase', 'metallophosphoesterase_nuclease', 'metallophosphomonoesterase', 'molybdopterin_oxidoreductase', 'nad_p_dehydrogenase', 'non_heme_iron_2og_dioxygenase', 'nucleoside_diphosphate_kinase', 'pfka_phosphofructokinase', 'pfkb_ribokinase_family', 'plp_dependent_enzyme', 'protein_kinase_ser_thr_tyr', 'radical_sam_enzyme', 'sam_methyltransferase', 'ser_his_acid_hydrolase', 'terpene_cyclase_synthase', 'thiamine_diphosphate_enzyme', 'zinc_lyase_hydratase'].

## Promotion triage

- Leave-one-out self-consistency (chemistry alone recovers the fingerprint): 0.6628.
- Promotion candidates (cohesion >= 0.92): 2324.
- Review outliers (chemistry points at a different fingerprint): 1901.
- Coherent but below threshold: 1413.

## Hole proposals (model-ranked from out_of_scope)

- radical_sam_enzyme: centroid available; 0 proposed candidates.
- cobalamin_radical_rearrangement: centroid available; 4 proposed candidates.
- ser_his_acid_hydrolase: centroid available; 22 proposed candidates.

## Leakage guardrails

- Frozen benchmark read: False.
- EC/name/prose/lane used: False.
- Fingerprint label used as feature: False.
- Used only for candidate ranking + promotion triage, NEVER as a benchmark scorer.
- Registry written: False.
