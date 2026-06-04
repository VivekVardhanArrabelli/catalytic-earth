# Lever 2 Event-Axis Signature-Exclusion Sensitivity Readout

- Artifact: `v3_lever2_event_axis_signature_exclusion_sensitivity_readout_current702_20260604`
- Status: `lever2_event_axis_signature_exclusion_sensitivity_readout_research_only_signature_exclusion_sensitivity_signal_with_axis_caveat`
- Created UTC: `2026-06-04T23:02:43Z`

## Sensitivity Matrix

| signature axis | best new axis | best marginal catches | best marginal rows | bond-change marginal | electron-flow marginal | same-signature rows excluded |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| source_free_projected_proton_role_subset | bond_change | 2 | m_csa:256, m_csa:312 | 2 | 1 | 60 |
| bond_change | electron_flow | 1 | m_csa:256 | 0 | 1 | 66 |
| electron_flow | bond_change | 2 | m_csa:256, m_csa:312 | 2 | 1 | 302 |
| event_topology | bond_change | 2 | m_csa:256, m_csa:312 | 2 | 1 | 118 |

## Key Counts

- Signature axes evaluated: 4
- Signature axes with any marginal signal: 4
- Projected-signature bond-change marginal catches: 2
- Bond-signature bond-change marginal catches: 0
- Bond-signature electron-flow marginal catches: 1

## Decision

- Any signature-excluded axis signal beyond current surface: True
- Bond-change survives projected-signature exclusion: True
- Bond-change survives bond-signature exclusion: False
- Bond-change collapses under own-signature exclusion: True
- Electron-flow survives bond-signature exclusion: True
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Next gate: Treat the bond-change rescue as research-only and axis-fragile until source-free current-split event-axis evidence can be measured. Prioritize m_csa:256 because it remains marginal under the bond-signature exclusion through electron-flow.

## Interpretation

- Projected-signature exclusion preserves two bond-change marginal catches, but bond-signature exclusion removes the bond-change marginal signal and leaves one electron-flow catch.
- Research-only mixed signal: mechanism event axes add local current-retained OOS value under signature exclusion, but the bond-change marginal effect is not robust to excluding same-bond-signature calibration OOS neighbors.
- Materialize source-free current-split event-axis rows for m_csa:256 first, then m_csa:312 only if the projected-signature bond-change path remains primary-controlled.
