# Lever 2 Source-Free Electron-Flow Fe-S/Iron Tiny-Tranche Approval Readiness Readout - current702

Run: 2026-06-05T13:15:38Z

Lever 2 source-free Fe-S/iron tiny-tranche approval-readiness readout. It consumes the measured Fe-S/iron projection-support artifact, the approval-qualified union artifact, the review-only iron-sulfur locus sidecar, and the train/cal input manifest to measure whether the smallest source-free support tranche can make the Fe-S/iron current-split OOS catch consumable. It does not approve, import, tune, train, score heldout, edit registries, or promote any feature.

## Status

- lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout_research_only_tiny_tranche_source_free_positive_partial_bundle_ready_pending_predictive_gate
- Result class: research_only_tiny_tranche_source_free_positive_partial_bundle_ready_pending_predictive_gate
- Tiny tranche source-free positives: 3/3
- Bundle-ready source-free positive rows: 2/3
- Accession-compatible role-graph rows: 2/3
- Expanded bundle-ready source-free positive rows: 8/12
- Predictive-use-allowed rows now: 0
- Rows already present in current train/cal feature sidecar: 0
- Fe-S incremental current-retained OOS rows beyond PQQ+NAD: 1
- Forbidden row-feature key hits: 0

## Tiny Tranche

| row | source-free positive | split | bundle ready | role graph | accession | accession position counts | accession-compatible | predictive use now | in current sidecar | missing import requirements |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m_csa:443 | True | in_distribution | False | missing_accession_compatible_sequence_positions | P13063 | P13063:12, P13065:7 | False | False | False | minimal_train_cal_feature_bundle_ready, accession_compatible_sequence_positions_true, predictive_use_allowed_true, approved_train_cal_feature_sidecar_row |
| m_csa:127 | True | in_distribution | True | ok | P07598 | P07598:8 | True | False | False | predictive_use_allowed_true, approved_train_cal_feature_sidecar_row |
| m_csa:281 | True | in_distribution | True | ok | P55931 | P55931:8 | True | False | False | predictive_use_allowed_true, approved_train_cal_feature_sidecar_row |

## Expanded Non-Current Tranche

| rows | source-free positives | bundle-ready positives | blocked by bundle | blocked only by predictive gate/import |
| ---: | ---: | ---: | --- | --- |
| 12 | 12 | 8 | m_csa:443, m_csa:208, m_csa:123, m_csa:212 | m_csa:127, m_csa:281, m_csa:130, m_csa:398, m_csa:358, m_csa:108, m_csa:562, m_csa:276 |

- Expanded bundle-ready entry IDs: m_csa:127, m_csa:281, m_csa:130, m_csa:398, m_csa:358, m_csa:108, m_csa:562, m_csa:276
- Expanded tranche row order: m_csa:443, m_csa:127, m_csa:281, m_csa:208, m_csa:130, m_csa:398, m_csa:358, m_csa:123, m_csa:212, m_csa:108, m_csa:562, m_csa:276

## Approval-Qualified Union Context

- Supported-now current-retained OOS positives: 2
- Approval-qualified current-retained OOS positives: 3
- Approval-qualified current primary positives: 0
- Approval-qualified current primary retain recall: 1.0
- Fe-S incremental OOS recall beyond PQQ+NAD: 0.013333
- Approval-qualified union adds value if Fe-S approved: True

## Decision

- Tiny tranche source-free evidence complete and positive: True
- All rows minimal bundle ready: False
- Bundle-ready subset available: True
- Expanded bundle-ready subset available: True
- m_csa:119 can join after bundle-ready subset approval: True
- Predictive use allowed now: False
- Present in current train/cal sidecar now: False
- Train/cal supported now: False
- Deployable now: False
- Remaining gap: The tiny Fe-S/iron support tranche is source-free positive, but it is not consumable now: no tiny support rows have predictive_use_allowed=true or an approved train/cal feature sidecar row, and the full three-row tranche has a minimal train/cal feature-bundle readiness gap for m_csa:443. The expanded non-current tranche provides a larger bundle-ready source-free positive pool of 8 rows, but those rows also remain unapproved and absent from the train/cal feature sidecar.
- Smallest next experiment: Approve/import the bundle-ready source-free Fe-S/iron support subset (m_csa:127, m_csa:281) with predictive_use_allowed=true and explicit train/cal split assignment, or first repair the minimal feature-bundle gap for m_csa:443 to import the original three-row tiny tranche. If a broader support pool is required, use the expanded bundle-ready subset (m_csa:127, m_csa:281, m_csa:130, m_csa:398, m_csa:358, m_csa:108, m_csa:562, m_csa:276). Then rerun the fixed approval-qualified union without threshold changes or heldout use.

## Interpretation

- The tiny Fe-S/iron support tranche is source-free complete and positive on 3/3 rows, and the approval-qualified union would add m_csa:119 beyond the supported PQQ+NAD route while preserving current primary retention. It still cannot be counted as train/cal support now because predictive-use and feature-sidecar approval are absent, with a full-tranche bundle-readiness gap for m_csa:443. The expanded non-current tranche offers an 8-row bundle-ready source-free positive support pool.
- Use the bundle-ready source-free subset as the smallest approval/import experiment, or repair m_csa:443 before importing all three tiny-tranche rows; use the expanded bundle-ready subset only if the approval contract requires more support rows.
