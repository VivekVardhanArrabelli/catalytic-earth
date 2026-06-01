# Mechanism Feature Active-Site Role Graph Sidecar - current702

Run: 2026-06-01T05:08:25Z

Row-level active-site residue-role graph sidecar for current702 mechanism-feature embedding gap closure.

## Status

- active_site_role_graph_sidecar_ready
- Manifest rows: 702
- Rows with ok role graph: 656
- Rows by status: {'missing_accession_compatible_sequence_positions': 42, 'missing_catalytic_residue_nodes': 1, 'not_m_csa_no_curated_active_site_roles': 3, 'ok': 656}
- Unique roles: 53
- Unique role co-occurrence edges: 669

## Top Roles

- electrostatic_stabiliser: 1757
- hydrogen_bond_donor: 1068
- metal_ligand: 848
- proton_acceptor: 793
- proton_donor: 790
- hydrogen_bond_acceptor: 708
- activator: 356
- steric_role: 264
- proton_shuttle_general_acid_base: 228
- nucleophile: 182
- nucleofuge: 168
- covalently_attached: 160
- proton_relay: 135
- modifies_pka: 103
- increase_basicity: 75
- increase_acidity: 67
- attractive_charge_charge_interaction: 67
- covalent_catalysis: 63
- transition_state_stabiliser: 56
- increase_nucleophilicity: 55

## Interpretation

- row_level_active_site_residue_role_graph_vocabulary_normalized
- directed proton-transfer/electron-flow edges and row-specific bond-change mapping are not inferred here
- Use this sidecar as a train/cal-only feature source in a future mechanism-feature embedding pilot; do not train on heldout rows.
