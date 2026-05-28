# External Priority Materialization Scout - 2026-05-28

Review-only materialization scout. No fetches, imports, model outputs, or label edits were performed.

## Summary

- `priority_rows_scanned`: 40
- `blocker_counts`: {'quarantined_review_only_boundary_not_clean_canary': 1, 'none_local_current702_coordinate_available': 12, 'external_identifier_or_coordinate_mapping_needed': 27}
- `current702_rows_with_local_coordinates`: 13
- `external_rows_needing_mapping`: 27
- `quarantined_review_only_boundary_rows`: 1
- `clean_canary_allowed_count`: 12

## Top Rows

- `m_csa:497` nitric-oxide reductase (FMN) | blocker=quarantined_review_only_boundary_not_clean_canary | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:131` 4-hydroxybenzoate 3-monooxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:551` phenol 2-monooxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:973` DszC protein | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:141` 4-cresol dehydrogenase (hydroxylating) | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:128` Photinus-luciferin 4-monooxygenase (ATP-hydrolysing) | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:129` taurine dioxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:130` naphthalene 1,2-dioxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:133` camphor 5-monooxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:134` tyrosine 3-monooxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:135` peptidylglycine monooxygenase | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:699` cytochrome P450 (BM-3) | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `m_csa:795` heme oxygenase (biliverdin-producing) | blocker=none_local_current702_coordinate_available | local=True | action=use_as_review_only_boundary/current702 coordinate row; do not import or clean-canary if quarantined
- `mh_035` beta-lactamase (Class B1) | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
- `mh_036` beta-lactamase (Class B1) | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
- `mh_037` cerebroside-sulfatase | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
- `mh_040` H+-transporting two-sector ATPase (F-type, mitochondrial) | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
- `mh_041` chaperonin ATPase | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
- `mh_042` G-protein alpha subunit, group I (GTPase) | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
- `mh_043` myosin ATPase | blocker=external_identifier_or_coordinate_mapping_needed | local=False | action=resolve PDB/UniProt/AFDB identifier from source artifact, then materialize bounded coordinate if approved
