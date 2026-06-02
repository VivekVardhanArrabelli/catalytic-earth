# Mechanism Feature Row-Specific Bond-Change P0 Feature-Readiness Audit - current702

Run: 2026-06-02T09:19:56Z

Review-only readiness audit for converting the P0 row-specific bond-change source-evidence sidecar into future mechanism-feature contract fields. It inventories proton-transfer, electron-transfer, and bond-change draft coverage while keeping every draft row out of training and threshold selection.

## Status

- p0_feature_readiness_audit_ready_for_feature_contract_refresh
- Sidecar rows: 15
- Structurally ready draft rows: 15
- Approved consumable rows: 15
- Rows with bond-change events: 13
- Rows with proton-transfer events: 9
- Rows with electron-transfer events: 7
- Draft event type counts: {'bond_broken': 8, 'bond_formed': 8, 'bond_order_changed': 9, 'electron_transfer': 10, 'proton_transfer': 16}
- Blocker counts: {}
- Feature-contract refresh allowed: True

## Row Readiness

| row | events | event types | structurally ready | approved consumable | blockers |
| --- | ---: | --- | --- | --- | --- |
| m_csa:5 | 1 | bond_broken | True | True |  |
| m_csa:6 | 4 | bond_broken, bond_formed, electron_transfer, proton_transfer | True | True |  |
| m_csa:11 | 4 | bond_broken, bond_formed, electron_transfer | True | True |  |
| m_csa:15 | 3 | bond_broken, bond_formed, proton_transfer | True | True |  |
| m_csa:16 | 4 | bond_broken, bond_formed, proton_transfer | True | True |  |
| m_csa:37 | 2 | electron_transfer | True | True |  |
| m_csa:66 | 3 | bond_order_changed | True | True |  |
| m_csa:68 | 3 | bond_order_changed, electron_transfer, proton_transfer | True | True |  |
| m_csa:94 | 2 | bond_formed | True | True |  |
| m_csa:102 | 5 | bond_broken, bond_order_changed, electron_transfer, proton_transfer | True | True |  |
| m_csa:124 | 5 | electron_transfer, proton_transfer | True | True |  |
| m_csa:133 | 5 | bond_formed, electron_transfer, proton_transfer | True | True |  |
| m_csa:147 | 4 | bond_order_changed, proton_transfer | True | True |  |
| m_csa:169 | 4 | bond_broken, bond_formed, proton_transfer | True | True |  |
| m_csa:186 | 2 | bond_broken, bond_order_changed | True | True |  |

## Interpretation

- All P0 rows are approved and consumable for a bounded feature-contract refresh.
- Resolve the Rhea-missing rows, manually approve or reject each draft event with reviewer provenance, rerun the strict audit and this readiness audit, then refresh only train/cal feature contracts if the refresh gate passes.
