# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Sidecar - current702

Run: 2026-06-02T05:12:36Z

Draft source-evidence sidecar for the balanced P0 row-specific bond-change pilot. It fills row-specific M-CSA mechanism spans, Rhea equations where available, active-site residue support, and draft bond-change events, but every row remains non-consumable until strict review approval.

## Status

- p0_source_evidence_sidecar_partially_approved_review_required
- Sidecar rows: 15
- Approved rows: 3
- Feature-contract consumable rows: 3
- Review status counts: {'approved': 3, 'draft': 12}

## Approved Reviewer Decisions

- m_csa:5: approve_m_csa_only_source_evidence by Vivek Vardhan Arrabelli at 2026-06-02T05:12:36Z; accepted_events=[0]
- m_csa:11: approve_m_csa_only_source_evidence by Vivek Vardhan Arrabelli at 2026-06-02T05:12:36Z; accepted_events=[0, 1, 2, 3]
- m_csa:169: approve_m_csa_only_source_evidence by Vivek Vardhan Arrabelli at 2026-06-02T05:12:36Z; accepted_events=[0, 1, 2, 3]

## Leakage Guardrail

- Approved M-CSA-derived bond-change features are consumable only after train/cal split filtering; heldout M-CSA rows remain excluded from training and threshold tuning.

## Interpretation

- Three previously Rhea-missing P0 rows now carry reviewer-approved M-CSA-only provenance and are feature-contract-consumable only through train/cal split filtering; the remaining rows stay draft.
- Rerun strict sidecar, review queue, Rhea manifest, feature-readiness, Rhea consumption, reviewer-decision, and refresh-blocker audits before materializing any row-specific feature-contract fields.
