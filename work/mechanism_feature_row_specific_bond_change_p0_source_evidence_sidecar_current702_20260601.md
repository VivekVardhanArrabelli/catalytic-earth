# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Sidecar - current702

Run: 2026-06-01T23:00:43Z

Draft source-evidence sidecar for the balanced P0 row-specific bond-change pilot. It fills row-specific M-CSA mechanism spans, Rhea equations where available, active-site residue support, and draft bond-change events, but every row remains non-consumable until strict review approval.

## Status

- p0_source_evidence_sidecar_draft_review_required
- Sidecar rows: 15
- Rows with source spans: 15
- Rows with draft bond-change events: 15
- Rows with Rhea equations: 12
- Rows missing Rhea equations: 3
- Approved rows: 0
- Review status counts: {'draft': 15}
- Draft event type counts: {'bond_broken': 5, 'bond_formed': 6, 'bond_order_changed': 7, 'electron_transfer': 21, 'proton_transfer': 10}

## Row Drafts

- m_csa:5: status=draft, events=1, event_types=['bond_broken']
- m_csa:6: status=draft, events=5, event_types=['electron_transfer', 'electron_transfer', 'electron_transfer', 'electron_transfer', 'proton_transfer']
- m_csa:11: status=draft, events=4, event_types=['bond_broken', 'electron_transfer', 'bond_formed', 'electron_transfer']
- m_csa:15: status=draft, events=2, event_types=['bond_formed', 'electron_transfer']
- m_csa:16: status=draft, events=2, event_types=['proton_transfer', 'electron_transfer']
- m_csa:37: status=draft, events=2, event_types=['electron_transfer', 'electron_transfer']
- m_csa:66: status=draft, events=3, event_types=['bond_order_changed', 'bond_order_changed', 'bond_order_changed']
- m_csa:68: status=draft, events=3, event_types=['electron_transfer', 'electron_transfer', 'electron_transfer']
- m_csa:94: status=draft, events=2, event_types=['bond_formed', 'bond_formed']
- m_csa:102: status=draft, events=5, event_types=['electron_transfer', 'bond_broken', 'electron_transfer', 'electron_transfer', 'electron_transfer']
- m_csa:124: status=draft, events=5, event_types=['electron_transfer', 'proton_transfer', 'proton_transfer', 'proton_transfer', 'proton_transfer']
- m_csa:133: status=draft, events=5, event_types=['electron_transfer', 'electron_transfer', 'proton_transfer', 'bond_formed', 'electron_transfer']
- m_csa:147: status=draft, events=4, event_types=['bond_order_changed', 'proton_transfer', 'bond_order_changed', 'bond_order_changed']
- m_csa:169: status=draft, events=4, event_types=['bond_formed', 'proton_transfer', 'proton_transfer', 'bond_broken']
- m_csa:186: status=draft, events=2, event_types=['bond_broken', 'bond_order_changed']

## Interpretation

- The P0 worksheet now has a draft, source-backed evidence sidecar over all 15 rows. It closes the blank-worksheet formatting gap but not the review gate: zero rows are approved for feature-contract consumption.
- Run the strict sidecar audit, then manually review each draft event and participant mapping before any no-fit feature contract refresh.
