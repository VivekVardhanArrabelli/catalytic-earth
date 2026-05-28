# Active-Site Local Tail Cache Extension Pack - 2026-05-28
This is a review-only decision pack. It does not write cache rows, fetch coordinates, train models, or change labels.
## Summary
- `recommended_extension_row_count`: 10
- `local_coordinate_present_count`: 10
- `default_coordinate_present_count`: 9
- `alternate_local_coordinate_needed_count`: 1
- `geometry_ok_count`: 10
- `current_readiness_matrix_coverage_count`: 0
- `not_in_current_readiness_matrix_count`: 10
- `extension_blocker_count`: 0
- `interpretation`: The top 10 local tail rows are locally materialized and geometry-ok, but none are in the current smoke-ready readiness matrix. The next safe action is a readiness-extension artifact or CLI extension, not direct cache writing from the existing matrix.

## Top 10 local addable rows
- `m_csa:15` / `mh_035`: beta-lactamase (Class B1) | role `positive_anchor` | state `seed_fingerprint:metal_dependent_hydrolase` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1ZNB.cif` (present) | residues 8/8 | panel `metallo_beta_lactamase_like`
- `m_csa:258` / `mh_036`: beta-lactamase (Class B1) | role `positive_anchor` | state `seed_fingerprint:metal_dependent_hydrolase` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1SML.cif` (present) | residues 7/7 | panel `metallo_beta_lactamase_like`
- `m_csa:158` / `mh_037`: cerebroside-sulfatase | role `positive_anchor` | state `seed_fingerprint:metal_dependent_hydrolase` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1AUK.cif` (present) | residues 10/11 | panel `sulfatase_fgly_metal_boundary`
- `m_csa:178` / `mh_040`: H+-transporting two-sector ATPase (F-type, mitochondrial) | role `oos_hard_negative` | state `out_of_scope` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1BMF.cif` (present) | residues 4/4 | panel `ntpase_nucleotide_hydrolase_boundary`
- `m_csa:179` / `mh_041`: chaperonin ATPase | role `oos_hard_negative` | state `out_of_scope` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1Q3S.cif` (present) | residues 4/4 | panel `ntpase_nucleotide_hydrolase_boundary`
- `m_csa:533` / `mh_042`: G-protein alpha subunit, group I (GTPase) | role `oos_hard_negative` | state `out_of_scope` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1BH2.cif` (present) | residues 5/5 | panel `ntpase_nucleotide_hydrolase_boundary`
- `m_csa:534` / `mh_043`: myosin ATPase | role `oos_hard_negative` | state `reviewed_or_candidate_control_no_current_parent_label` | coordinate `artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1VOM.cif` (present_alternate_artifact) | residues 8/8 | panel `ntpase_nucleotide_hydrolase_boundary`
- `m_csa:216` / `mh_048`: carbonate dehydratase (alpha class) | role `positive_anchor` | state `seed_fingerprint:metal_dependent_hydrolase` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1CA2.cif` (present) | residues 6/6 | panel `carbonic_anhydrase_dehydratase_boundary`
- `m_csa:516` / `mh_049`: carbonate dehydratase (gamma class) | role `positive_anchor` | state `seed_fingerprint:metal_dependent_hydrolase` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1QRG.cif` (present) | residues 7/7 | panel `carbonic_anhydrase_dehydratase_boundary`
- `m_csa:54` / `mh_051`: 3-dehydroquinate dehydratase (type I) | role `oos_hard_negative` | state `out_of_scope` | coordinate `artifacts/v3_foldseek_coordinates_1000/pdb_1QFE.cif` (present) | residues 3/3 | panel `carbonic_anhydrase_dehydratase_boundary`

## Candidate command after readiness extension
```bash
PYTHONPATH=src python -m catalytic_earth.cli build-active-site-encoder-cache --readiness-matrix artifacts/v3_active_site_encoder_readiness_matrix_local_tail_extension_20260528.json --geometry artifacts/v3_geometry_features_1025.json --include-rows m_csa:15,m_csa:258,m_csa:158,m_csa:178,m_csa:179,m_csa:533,m_csa:534,m_csa:216,m_csa:516,m_csa:54 --out artifacts/v3_active_site_encoder_cache_local_tail_extension_10_20260528.jsonl --summary-out artifacts/v3_active_site_encoder_cache_local_tail_extension_10_summary_20260528.json --report-out work/active_site_encoder_cache_local_tail_extension_10_20260528.md
```

## No-go conditions
- Do not run the cache command against the current readiness matrix because the 10 rows are not yet marked label-blind smoke-ready there.
- Do not fetch external coordinates; use only listed local coordinate paths.
- Do not train or calibrate any model from this extension pack.
- Do not promote labels or alter registries from this pack.
- Keep disk above 10 GiB before writing any future cache extension.
