# Mechanism Representation Loop (leakage-safe self-feeding supply)

Run: 2026-06-10T05:27:24Z

First iteration of the self-feeding loop. A representation learned ONLY from review-only cofactor/ligand chemistry + active-site residue roles organises the bronze labels, triages bronze->silver promotion, and proposes candidates for the governor's holes. EC / protein-name / prose / lane / the fingerprint label / the frozen benchmark are never read.

- Feature space: ['flavin', 'plp', 'heme', 'iron_sulfur', 'sam', 'cobalamin', 'zinc', 'divalent_metal_other', 'calcium', 'catalytic_fraction', 'binding_fraction', 'active_site_size'].
- Excluded from representation: ['ec_numbers', 'fingerprint_id', 'label_type', 'protein_name', 'uniprot_prose', 'target_family_lane', 'rationale'].
- Seed labels: 486; out_of_scope: 1224; centroids: ['cobalamin_radical_rearrangement', 'flavin_dehydrogenase_reductase', 'flavin_monooxygenase', 'heme_peroxidase_oxidase', 'metal_dependent_hydrolase', 'plp_dependent_enzyme', 'radical_sam_enzyme'].

## Promotion triage

- Leave-one-out self-consistency (chemistry alone recovers the fingerprint): 0.8951.
- Promotion candidates (cohesion >= 0.92): 368.
- Review outliers (chemistry points at a different fingerprint): 51.
- Coherent but below threshold: 67.

## Hole proposals (model-ranked from out_of_scope)

- radical_sam_enzyme: centroid available; 14 proposed candidates.
- cobalamin_radical_rearrangement: centroid available; 0 proposed candidates.
- ser_his_acid_hydrolase: centroid MISSING; 0 proposed candidates.

## Leakage guardrails

- Frozen benchmark read: False.
- EC/name/prose/lane used: False.
- Fingerprint label used as feature: False.
- Used only for candidate ranking + promotion triage, NEVER as a benchmark scorer.
- Registry written: False.
