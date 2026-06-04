# Fold-Augmented Q43088 Geometry/Locator Blocker Packet - current702

Run: 2026-06-04T08:16:37Z

Single-row Lever 3 blocker packet for m_csa:604/Q43088 after the P10746 policy blocker was reconciled. It records only local deployment-valid/fail-closed evidence and does not approve a sidecar, rescore rows, rerun thresholds, or use heldout rows for calibration.

## Status

- fold_augmented_q43088_geometry_locator_blocker_packet_blocked_missing_source_free_locator
- Local predicted coordinate available: True
- Fold channel available: True
- Approved source-free geometry/locator rows: 0
- Active-site residue count: 1/3
- Additional approved locator positions needed: 2
- Selected organic cofactor max score: 0.605709
- Blockers: ['q43088_fewer_than_three_approved_locator_positions', 'q43088_missing_approved_source_free_geometry_sidecar', 'fixed_threshold_audit_still_not_ready']

## Row Evidence

- Entry/accession: m_csa:604 / Q43088
- Blocker detail: experimental_geometry_not_ok:insufficient_resolved_residues; fold channel exists but combined channel lacks approved geometry features
- Fold nearest train atlas: {'nearest_train_atlas_entry_id': 'm_csa:528', 'nearest_train_atlas_tm_score': 0.4713, 'nearest_train_atlas_true_fingerprint_id': 'metal_dependent_hydrolase', 'raw_query_name': 'afdb_Q43088_v6', 'raw_target_name': 'afdb_Q6UV28_v6'}
- Cofactor families: ['flavin']
- Local role graph residues: [{'residue_node_id': 'm_csa:604:residue:1', 'roles': ['activator', 'proton_acceptor', 'proton_donor'], 'roles_raw': ['activator', 'proton acceptor', 'proton donor'], 'sequence_positions': [{'code': 'Tyr', 'is_reference': True, 'resid': 287, 'uniprot_id': 'Q43088'}], 'structure_positions': [{'chain_name': 'A', 'code': 'Tyr', 'is_reference': True, 'pdb_id': '1mlv', 'resid': 243}]}]

## Decision

- Ready for combined-channel rescore now: False
- Fixed-threshold audit ready to rerun now: False
- Smallest next experiment: Supply or approve at least two additional source-free locator positions, or an explicitly approved alternate source-free geometry sidecar, for Q43088; then rescore only m_csa:604 at unchanged threshold 0.44155.

## Interpretation

- Q43088 is not coordinate-missing: the local AFDB-v6 CIF and fold hit exist, and the row is a high-cofactor proxy member. The blocker is specifically the absence of approved source-free geometry/locator evidence for the combined channel.
- Do not rerun the fixed-threshold audit from Q43088 alone. Either approve/source at least two additional locator positions for this row or keep it outside combined-channel closure, then continue the 16-row high-cofactor acquisition contract.
