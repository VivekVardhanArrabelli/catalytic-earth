# Mechanism Feature Row-Specific Bond-Change P0 OOS Calibration Gap - current702

Run: 2026-06-02T09:49:45Z

Review-only packet of split-safe none_of_above train/cal rows that could supply OOS/novel row-specific bond/proton/electron evidence for the P0 no-template operating point.

## Status

- p0_oos_calibration_gap_ready_review_packet
- Candidate rows: 353
- Candidate calibration rows: 71
- Candidate train rows: 282
- Packet rows: 30
- Packet calibration rows: 30

## Decision

- Feature consumption allowed now: False
- Fills no-template OOS operating point if approved: True
- Next gate: Create source-evidence extraction rows for calibration candidates first; approve only source-spanned row-specific events, then rerun the P0 no-template artifact.

## Packet Rows

| entry | assigned split | active-site residues | role graph | reaction template |
| --- | --- | ---: | --- | --- |
| m_csa:2 | calibration | 7 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:17 | calibration | 11 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:23 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:25 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:40 | calibration | 4 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:49 | calibration | 7 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:59 | calibration | 10 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:70 | calibration | 3 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:76 | calibration | 3 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:78 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:85 | calibration | 7 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:101 | calibration | 4 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:149 | calibration | 6 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:154 | calibration | 3 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:194 | calibration | 9 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:202 | calibration | 3 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:221 | calibration | 4 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:222 | calibration | 7 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:224 | calibration | 2 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:241 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:246 | calibration | 4 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:253 | calibration | 10 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:256 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:263 | calibration | 4 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:273 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:287 | calibration | 5 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:292 | calibration | 6 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:312 | calibration | 4 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:317 | calibration | 3 | ok | no_mechanism_fingerprint_oos_or_unlabeled |
| m_csa:318 | calibration | 1 | ok | no_mechanism_fingerprint_oos_or_unlabeled |

## Interpretation

- Found 71 calibration and 282 train none_of_above candidates outside the approved P0 sidecar; the first 30 are staged for manual source-evidence extraction.
- Start with the calibration rows in this packet because the current P0 no-template rerun lacks any OOS/novel calibration rows.
