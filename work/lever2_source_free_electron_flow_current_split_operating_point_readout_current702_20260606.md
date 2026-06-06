# Lever 2 Source-Free Electron-Flow Current-Split Operating-Point Readout - current702

Run: 2026-06-06T03:45:34Z

Lever 2 measured train/cal operating-point readout for direct source-free electron-flow fields. It consumes the row-gate audit matrix, compares a fixed electron-flow OR overlay against the current geometry/fold operating point, and reports smoke/full current-split value while preserving primary retention. It does not apply protected imports, edit approved sidecars, change thresholds, train models, score heldout, or touch labels, registries, ontologies, or Lever 3 surfaces.

## Status

- lever2_source_free_electron_flow_current_split_operating_point_readout_research_only_direct_source_free_operating_point_signal_pending_protected_import
- Result class: research_only_direct_source_free_operating_point_signal_pending_protected_import
- Critical violations: 0
- Protected imports executed: 0
- Approved sidecar rows written: 0

## Fixed Operating-Point Comparison

| variant | OOS abstain recall | delta vs geometry/fold | estimated OOS rows | primary retain |
| --- | ---: | ---: | ---: | ---: |
| current geometry/fold | 0.466667 | 0.0 | 35 | 1.0 |
| smoke electron-flow OR | 0.48 | 0.013333 | 36 | 1.0 |
| full electron-flow OR | 0.506667 | 0.04 | 38 | 1.0 |

## Source-Free Positive Rows

- Smoke positives: ['m_csa:104']
- Full positives: ['m_csa:104', 'm_csa:119', 'm_csa:464']
- PQQ: ['m_csa:104']
- NAD-family: ['m_csa:464']
- Fe-S/iron: ['m_csa:119']

## Component Operating-Point Decomposition

| component | OOS abstain recall | delta vs geometry/fold | primary positives | retained-OOS IDs |
| --- | ---: | ---: | ---: | --- |
| pqq | 0.48 | 0.013333 | 0 | m_csa:104 |
| nad_family | 0.48 | 0.013333 | 0 | m_csa:464 |
| iron_sulfur_or_iron | 0.48 | 0.013333 | 0 | m_csa:119 |

## Decision

- Direct electron-flow operating point measured: True
- Adds value beyond geometry/fold: True
- Primary retention preserved: True
- Component decomposition primary-safe: True
- All three components add value: True
- Done-bar evidence measured: True
- Deployable now: False
- Remaining gap: No source-free electron-flow evidence gap remains for the current train/cal split; the remaining gap is explicit protected import authorization and approved-sidecar rerun.

## Interpretation

- Direct source-free electron-flow adds measured train/cal operating-point signal beyond the current geometry/fold surface: smoke recall moves 0.466667 -> 0.48, full recall moves 0.466667 -> 0.506667, and primary retain recall stays 1.0.
- Treat the remaining gap as protected import authorization, not missing source-free electron-flow evidence; next run should only apply smoke if that authorization is explicit.
