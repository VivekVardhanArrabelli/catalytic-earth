# Mechanism Representation Loop (leakage-safe self-feeding supply)

Run: 2026-06-11T16:12:49Z

First iteration of the self-feeding loop. A representation learned ONLY from review-only cofactor/ligand chemistry + active-site residue roles organises the bronze labels, triages bronze->silver promotion, and proposes candidates for the governor's holes. EC / protein-name / prose / lane / the fingerprint label / the frozen benchmark are never read.

- Feature space: ['flavin', 'plp', 'heme', 'iron_sulfur', 'sam', 'cobalamin', 'zinc', 'divalent_metal_other', 'calcium', 'bc_phosphomonoester', 'bc_phosphodiester', 'bc_peptide_cn', 'bc_amide_cn', 'catalytic_fraction', 'binding_fraction', 'active_site_size'].
- Excluded from representation: ['ec_numbers', 'fingerprint_id', 'label_type', 'protein_name', 'uniprot_prose', 'target_family_lane', 'rationale'].
- Seed labels: 1716; out_of_scope: 1224; centroids: ['cobalamin_radical_rearrangement', 'flavin_dehydrogenase_reductase', 'flavin_monooxygenase', 'heme_peroxidase_oxidase', 'metal_dependent_hydrolase', 'metallo_amidohydrolase_deaminase', 'metallopeptidase', 'metallophosphoesterase_nuclease', 'metallophosphomonoesterase', 'plp_dependent_enzyme', 'radical_sam_enzyme', 'ser_his_acid_hydrolase'].

## Promotion triage

- Leave-one-out self-consistency (chemistry alone recovers the fingerprint): 0.7512.
- Promotion candidates (cohesion >= 0.92): 892.
- Review outliers (chemistry points at a different fingerprint): 427.
- Coherent but below threshold: 397.

## Hole proposals (model-ranked from out_of_scope)

- radical_sam_enzyme: centroid available; 14 proposed candidates.
- cobalamin_radical_rearrangement: centroid available; 25 proposed candidates.
- ser_his_acid_hydrolase: centroid available; 25 proposed candidates.

## Leakage guardrails

- Frozen benchmark read: False.
- EC/name/prose/lane used: False.
- Fingerprint label used as feature: False.
- Used only for candidate ranking + promotion triage, NEVER as a benchmark scorer.
- Registry written: False.
