# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Sidecar - current702

Run: 2026-06-02T09:08:56Z

Draft source-evidence sidecar for the balanced P0 row-specific bond-change pilot. It fills row-specific M-CSA mechanism spans, Rhea equations where available, active-site residue support, and draft bond-change events, but every row remains non-consumable until strict review approval.

## Status

- p0_source_evidence_sidecar_all_train_cal_p0_rows_approved
- Sidecar rows: 15
- Rows with source spans: 15
- Rows with draft bond-change events: 15
- Rows with Rhea equations: 12
- Rows missing Rhea equations: 3
- Approved rows: 15
- Feature-contract consumable rows: 15
- Review status counts: {'approved': 15}
- Draft event type counts: {'bond_broken': 8, 'bond_formed': 8, 'bond_order_changed': 9, 'electron_transfer': 10, 'proton_transfer': 16}

## Row Drafts

- m_csa:5: status=approved, events=1, event_types=['bond_broken']
- m_csa:6: status=approved, events=4, event_types=['electron_transfer', 'bond_broken', 'proton_transfer', 'bond_formed']
- m_csa:11: status=approved, events=4, event_types=['bond_broken', 'electron_transfer', 'bond_formed', 'electron_transfer']
- m_csa:15: status=approved, events=3, event_types=['bond_formed', 'bond_broken', 'proton_transfer']
- m_csa:16: status=approved, events=4, event_types=['bond_formed', 'proton_transfer', 'bond_broken', 'proton_transfer']
- m_csa:37: status=approved, events=2, event_types=['electron_transfer', 'electron_transfer']
- m_csa:66: status=approved, events=3, event_types=['bond_order_changed', 'bond_order_changed', 'bond_order_changed']
- m_csa:68: status=approved, events=3, event_types=['proton_transfer', 'electron_transfer', 'bond_order_changed']
- m_csa:94: status=approved, events=2, event_types=['bond_formed', 'bond_formed']
- m_csa:102: status=approved, events=5, event_types=['proton_transfer', 'bond_broken', 'electron_transfer', 'bond_order_changed', 'proton_transfer']
- m_csa:124: status=approved, events=5, event_types=['electron_transfer', 'proton_transfer', 'proton_transfer', 'proton_transfer', 'proton_transfer']
- m_csa:133: status=approved, events=5, event_types=['electron_transfer', 'proton_transfer', 'electron_transfer', 'proton_transfer', 'bond_formed']
- m_csa:147: status=approved, events=4, event_types=['bond_order_changed', 'proton_transfer', 'bond_order_changed', 'bond_order_changed']
- m_csa:169: status=approved, events=4, event_types=['bond_formed', 'proton_transfer', 'proton_transfer', 'bond_broken']
- m_csa:186: status=approved, events=2, event_types=['bond_broken', 'bond_order_changed']

## Rewritten Pending Rows

- m_csa:6: approved after rewrite; events=['electron_transfer', 'bond_broken', 'proton_transfer', 'bond_formed']; rationale=Rewrite and approve because the Rhea-backed row now has only source-spanned, mapped hydride/electron, disulfide-exchange, proton-transfer, and bond-formation events over catalytic residue support; the low-confidence unmapped draft electron-transfer events were replaced, not consumed.
- m_csa:15: approved after rewrite; events=['bond_formed', 'bond_broken', 'proton_transfer']; rationale=Rewrite and approve because the zinc-water attack was retyped as mapped bond/proton chemistry over the Rhea-backed hydrolysis surface, removing the low-confidence unmapped electron-transfer event.
- m_csa:16: approved after rewrite; events=['bond_formed', 'proton_transfer', 'bond_broken', 'proton_transfer']; rationale=Rewrite and approve because the monometallic zinc-water sequence is represented as mapped bond-formation, proton-transfer, and bond-cleavage chemistry rather than the previous unmapped electron-transfer placeholder.
- m_csa:68: approved after rewrite; events=['proton_transfer', 'electron_transfer', 'bond_order_changed']; rationale=Rewrite and approve because the source-backed dehydrogenation sentence now yields mapped proton-transfer, hydride/electron-transfer, and bond-order-change events; downstream ETF transfer context is left out of the row-specific active-site surface.
- m_csa:102: approved after rewrite; events=['proton_transfer', 'bond_broken', 'electron_transfer', 'bond_order_changed', 'proton_transfer']; rationale=Rewrite and approve because lactate oxidation is now represented by mapped His/Tyr/Asp proton-transfer, bond-cleavage, hydride/electron-transfer, and bond-order events instead of unmapped generic electron-transfer spans.
- m_csa:133: approved after rewrite; events=['electron_transfer', 'proton_transfer', 'electron_transfer', 'proton_transfer', 'bond_formed']; rationale=Rewrite and approve because the heme/putidaredoxin row now has mapped electron-transfer, proton-relay, hydrogen-abstraction, and hydroxylation bond-formation events; the terminal product-displacement sentence is omitted rather than consumed as an unmapped event.

## Interpretation

- All 15 P0 rows now carry reviewer approval for split-filtered train/cal feature materialization: three M-CSA-only train rows, eight Rhea-backed train rows, and four Rhea-backed calibration rows. The six prior pending rewrite rows were rewritten as mapped source-spanned event surfaces before approval.
- Rerun strict/readiness/materialization and guardrail artifacts, then attempt the no-template centroid/residual rerun only from the label-stripped train/cal feature sidecar.
