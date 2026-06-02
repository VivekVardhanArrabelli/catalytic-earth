# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Sidecar - current702

Run: 2026-06-02T08:08:19Z

Draft source-evidence sidecar for the balanced P0 row-specific bond-change pilot. It fills row-specific M-CSA mechanism spans, Rhea equations where available, active-site residue support, and draft bond-change events, but every row remains non-consumable until strict review approval.

## Status

- p0_source_evidence_sidecar_partially_approved_review_required
- Sidecar rows: 15
- Rows with source spans: 15
- Rows with draft bond-change events: 15
- Rows with Rhea equations: 12
- Rows missing Rhea equations: 3
- Approved rows: 9
- Review status counts: {'approved': 9, 'needs_more_evidence': 6}
- Draft event type counts: {'bond_broken': 1, 'bond_formed': 2, 'electron_transfer': 16, 'proton_transfer': 3}

## Row Drafts

- m_csa:5: status=approved, events=1, event_types=['bond_broken']
- m_csa:6: status=needs_more_evidence, events=5, event_types=['electron_transfer', 'electron_transfer', 'electron_transfer', 'electron_transfer', 'proton_transfer']
- m_csa:11: status=approved, events=4, event_types=['bond_broken', 'electron_transfer', 'bond_formed', 'electron_transfer']
- m_csa:15: status=needs_more_evidence, events=2, event_types=['bond_formed', 'electron_transfer']
- m_csa:16: status=needs_more_evidence, events=2, event_types=['proton_transfer', 'electron_transfer']
- m_csa:37: status=approved, events=2, event_types=['electron_transfer', 'electron_transfer']
- m_csa:66: status=approved, events=3, event_types=['bond_order_changed', 'bond_order_changed', 'bond_order_changed']
- m_csa:68: status=needs_more_evidence, events=3, event_types=['electron_transfer', 'electron_transfer', 'electron_transfer']
- m_csa:94: status=approved, events=2, event_types=['bond_formed', 'bond_formed']
- m_csa:102: status=needs_more_evidence, events=5, event_types=['electron_transfer', 'bond_broken', 'electron_transfer', 'electron_transfer', 'electron_transfer']
- m_csa:124: status=approved, events=5, event_types=['electron_transfer', 'proton_transfer', 'proton_transfer', 'proton_transfer', 'proton_transfer']
- m_csa:133: status=needs_more_evidence, events=5, event_types=['electron_transfer', 'electron_transfer', 'proton_transfer', 'bond_formed', 'electron_transfer']
- m_csa:147: status=approved, events=4, event_types=['bond_order_changed', 'proton_transfer', 'bond_order_changed', 'bond_order_changed']
- m_csa:169: status=approved, events=4, event_types=['bond_formed', 'proton_transfer', 'proton_transfer', 'bond_broken']
- m_csa:186: status=approved, events=2, event_types=['bond_broken', 'bond_order_changed']

## Interpretation

- Nine P0 rows now carry reviewer approval for split-filtered feature materialization: three M-CSA-only train rows, two Rhea-backed calibration rows, and four Rhea-backed train-depth rows. Six low-confidence electron-transfer rows stay pending rewrite.
- Rewrite or reject the six pending low-confidence electron-transfer rows, rerun strict/readiness/materialization artifacts, and only attempt no-template reruns once the approved train/cal surface reaches the intended pilot coverage.
