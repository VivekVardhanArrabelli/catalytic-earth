# Lever 2 Source-Free Electron-Flow Fe-S/Iron Projection Support Readout - current702

Run: 2026-06-05T11:02:11Z

Lever 2 train/cal-disciplined source-free Fe-S/iron projection support readout. It consumes the measured fixed 8 A relaxed non-PQQ family split and the review-only iron-sulfur locus sidecar to determine whether the Fe-S/iron current-split signal can be counted as train/cal-supported now. It does not train, tune thresholds, score heldout, edit registries, import features, or promote a primitive.

## Status

- lever2_source_free_electron_flow_iron_sulfur_projection_support_readout_research_only_iron_sulfur_current_split_signal_tiny_materialization_support_gap
- Result class: research_only_iron_sulfur_current_split_signal_tiny_materialization_support_gap
- Current Fe-S/iron primary/OOS positives: 0/1
- Current primary retain recall: 1.0
- Current retained-OOS abstain recall: 0.025
- Incremental OOS recall vs current geometry/fold OOS: 0.013333
- Existing projection positives: 0
- Review-only non-heldout proximal Fe-S/iron rows outside current split: 12
- Tiny projection materialization positives: 3
- Expanded projection materialization positives: 12

## Current Split Gate

| rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall | union OOS recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 74/74 | 0 | 1 | 1.0 | 0.025 | 0.48 |

## Existing Projection Attempt

- Complete rows: 43/43
- Positive train/cal rows: 0/0
- Positive row IDs: none
- The fixed relaxed non-PQQ distance contract has no positive train/cal projection rows.

## Review-Only Source-Free Locus Scan

- Heldout rows excluded from support scan: 140
- Non-heldout proximal rows: 13
- Non-heldout proximal rows outside current split: 12
- Predictive-use-allowed proximal rows: 0
- Smallest non-current projection tranche: m_csa:443, m_csa:127, m_csa:281

| row | split | distance | ligand codes | predictive use allowed |
| --- | --- | ---: | --- | --- |
| m_csa:443 | in_distribution | 3.458 | SF4 | False |
| m_csa:127 | in_distribution | 3.486 | FE2, SF4 | False |
| m_csa:281 | in_distribution | 3.664 | SF4 | False |
| m_csa:208 | in_distribution | 3.724 | FES | False |
| m_csa:130 | in_distribution | 3.76 | FE, FES | False |
| m_csa:398 | in_distribution | 3.858 | SF4 | False |
| m_csa:358 | in_distribution | 4.023 | SF4 | False |
| m_csa:123 | in_distribution | 4.436 | SF4 | False |

## Tiny Projection Materialization

- Available: True
- Candidate rows: 3
- Complete rows: 3
- Positive rows: 3
- Positive row IDs: m_csa:127, m_csa:281, m_csa:443
- Consumable as train/cal support now: False
- The tiny Fe-S/iron projection tranche can be materialized from source-free coordinate fields in research-only mode, but it is not an approved/imported train/cal feature sidecar and therefore does not by itself make the Fe-S/iron current-split positive deployable.

### Expanded Non-Current Tranche

- Candidate rows: 12
- Complete rows: 12
- Positive rows: 12
- Positive row IDs: m_csa:108, m_csa:123, m_csa:127, m_csa:130, m_csa:208, m_csa:212, m_csa:276, m_csa:281, m_csa:358, m_csa:398, m_csa:443, m_csa:562
- Consumable as train/cal support now: False

## Decision

- Current split adds value beyond geometry/fold: True
- Existing projection rows support Fe-S/iron contract: False
- Review-only source-free evidence exists outside current split: True
- Review-only source-free evidence consumable now: False
- Tiny projection materialization positive: True
- Tiny materialization consumable as train/cal support now: False
- Train/cal supported now: False
- Deployable now: False
- Remaining gap: The Fe-S/iron family split is measured and primary-safe on the current 74-row split, but the existing 43-row train/cal projection surface has 0 Fe-S/iron positives. Separate non-heldout source-free Fe-S/iron locus evidence exists and the tiny materialization attempt can make those rows positive in research-only mode, but the rows remain outside the approved train/cal feature sidecar and predictive_use_allowed is false.
- Smallest next experiment: Approve/import the research-only tiny Fe-S/iron materialization tranche (m_csa:443, m_csa:127, m_csa:281) into the train/cal source-free feature sidecar, then rerun the same Fe-S/iron family split gate without changing thresholds or touching heldout rows.

## Interpretation

- The Fe-S/iron family split catches the current-retained OOS row m_csa:119 at primary retain 1.0, but the existing train/cal projection surface has no Fe-S/iron positive rows. The tiny non-current Fe-S/iron projection materialization attempt is source-free positive in research-only mode, but those rows are still outside the approved train/cal feature sidecar and are not consumable as predictive features.
- Keep the projection-backed PQQ+NAD subunion as the supported measured route for now; the exact next Fe-S/iron action is approval/import of the tiny materialized projection tranche before deciding whether m_csa:119 can join it.
