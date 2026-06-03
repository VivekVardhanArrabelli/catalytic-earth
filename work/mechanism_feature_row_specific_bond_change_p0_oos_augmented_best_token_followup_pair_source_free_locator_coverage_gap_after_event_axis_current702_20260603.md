# Source-Free Locator Coverage Gap After Event Axis - current702

Run: 2026-06-03T23:35:44Z

Post event-axis-signoff coverage gap for the Lever 2 source-free application surface. This artifact only counts heldout locator coverage after approved event-axis rows are materialized; it does not evaluate heldout labels or apply thresholds.

## Status

- source_free_locator_coverage_gap_after_event_axis_blocked_review_only
- Heldout rows: 140
- Heldout rows with source-free locator sidecar: 53
- Heldout rows missing source-free locator sidecar: 87
- Approved event-axis materialized rows: 14
- Heldout rows with locator and event-axis feature: 14
- Heldout rows with locator but no event-axis feature: 39
- Blockers: source_free_current702_heldout_locator_coverage_incomplete, heldout_safe_pair_application_surface_missing

## Decision

- Heldout-safe pair application surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Create approved source-free locator sidecars for the 87 missing heldout rows or define an explicit heldout-safe partial-surface policy before any frozen threshold read.

## Interpretation

- Event-axis signoff is no longer the Lever 2 blocker: 14 heldout rows now have both locator and event-axis features, but 87 of 140 heldout rows still lack approved source-free locator sidecars.
- Do not run the frozen residual threshold. Next clear locator coverage by approving/materializing more source-free locator sidecars or by writing an explicit partial-surface policy gate.

## First Missing Locator Rows

- m_csa:10
- m_csa:12
- m_csa:14
- m_csa:20
- m_csa:30
- m_csa:31
- m_csa:34
- m_csa:67
- m_csa:71
- m_csa:73
- m_csa:79
- m_csa:80
- m_csa:86
- m_csa:116
- m_csa:118
- m_csa:125
- m_csa:129
- m_csa:144
- m_csa:155
- m_csa:185
- m_csa:191
- m_csa:192
- m_csa:193
- m_csa:197
- m_csa:198
