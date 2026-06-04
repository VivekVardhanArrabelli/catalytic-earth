# Fold-Augmented Confounded Proxy High-Cofactor Acquisition Blocker - current702

Run: 2026-06-04T12:12:44Z

Precise Lever 3 blocker packet for the high-cofactor confounded OOS calibration gap after Q43088 locator clearance. It composes the frozen high-cofactor probe contract, current train/cal candidate pool, and near-miss triage; it registers no rows, scores no candidates, and does not change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_high_cofactor_acquisition_blocker_blocked_zero_eligible_rows
- Ready train/cal OOS rows: 353
- High-cofactor-axis candidates: 0
- Minimum new abstained rows for 80%: 16
- Eligible rows missing for minimum: 16
- Affected near-miss rows: 16
- Blockers: ['current_train_cal_candidate_pool_has_zero_high_cofactor_axis_rows', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'candidate_rows_not_scored_at_fixed_threshold', 'fixed_threshold_audit_not_ready_to_rerun']

## Decision

- Current evidence can solve high-cofactor gap: False
- Candidate rows ready to score now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not relax high-cofactor membership or tune threshold 0.44155. Acquire new eligible train/cal OOS rows or pre-register a separate source-free proxy axis before any scoring tranche.

## Affected Near Miss Rows

| rank | row | organic max | missing evidence |
| ---: | --- | --- | --- |
| 1 | m_csa:288 | heme:0.407563 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 2 | m_csa:89 | heme:0.398339 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 3 | m_csa:214 | plp:0.353171 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 4 | m_csa:75 | heme:0.34378 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 5 | m_csa:60 | plp:0.337092 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 6 | m_csa:583 | heme:0.296056 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 7 | m_csa:64 | plp:0.246623 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 8 | m_csa:607 | heme:0.236789 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 9 | m_csa:610 | plp:0.222226 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 10 | m_csa:618 | flavin:0.215006 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 11 | m_csa:555 | flavin:0.213904 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 12 | m_csa:404 | heme:0.193581 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 13 | m_csa:26 | plp:0.177608 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 14 | m_csa:515 | plp:0.150245 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 15 | m_csa:232 | plp:0.147019 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |
| 16 | m_csa:351 | plp:0.144021 | source-free high-cofactor proxy membership evidence: either a frozen high organic-cofactor signature or a frozen high inorganic cofactor locus, plus deployment-valid predicted-structure inputs |

## Smallest Next Experiment

- Acquire exactly 16 new non-heldout train/cal OOS rows whose source-free cofactor/locus evidence satisfies the frozen high-cofactor axis, stage deployment-valid predicted structures, then score those rows at unchanged threshold 0.44155.

## Interpretation

- The current ready train/cal OOS surface cannot close the high-cofactor calibration gap: 0 eligible rows are available against a 16-row minimum.
- Treat the listed rows as non-countable near misses. The next experiment is new source-free high-cofactor train/cal OOS acquisition, not another threshold readout.
