# Fold-Augmented Confounded Proxy Train/Cal Unsupported-Geometry Repair Queue - current702

Run: 2026-06-03T18:21:44Z

Train/cal-only repair queue for background rows whose only remaining source-free proxy-axis signal is unsupported or missing inorganic-locus geometry. It does not score rows, register a proxy axis, fetch coordinates, tune thresholds, read heldout rows, or count unsupported geometry as abstention evidence.

## Status

- fold_augmented_confounded_proxy_train_cal_unsupported_geometry_repair_queue_blocked
- Unsupported-geometry repair rows: 8
- Local AFDB-v6 coordinates observed: 0/8
- Ready to score now: 0
- Blockers: ['unsupported_geometry_rows_require_coordinate_or_locus_repair']

## Decision

- New proxy axis ready to score now: False
- Score repair rows now: False
- Next gate: Repair the listed coordinate/locus blockers, then rerun the background-axis scout before any new proxy-axis contract. Do not score unsupported geometry rows as abstention evidence.

## Repair Rows

| row | accession | local AFDB-v6 | active-site count | organic max | repair blocker |
| --- | --- | --- | ---: | --- | --- |
| m_csa:105 | Q46509 | False | 1 | flavin:0.024633 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:137 | P18548 | False | 1 | flavin:0.003489 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:318 | P27000 | False | 1 | heme:0.034086 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:327 | Q56310 | False | 3 | heme:0.005613 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:360 | P68175 | False | 1 | heme:0.035844 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:610 | P15807 | False | 1 | plp:0.222226 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:618 | Q9P4R4 | False | 1 | flavin:0.215006 | unsupported_or_missing_inorganic_locus_geometry |
| m_csa:649 | Q7SIE1 | False | 1 | heme:0.022674 | unsupported_or_missing_inorganic_locus_geometry |

## Interpretation

- 8 background-only rows need coordinate/locus repair before they can support another source-free proxy axis.
- Treat unsupported geometry as a data-quality repair queue, not as a scored proxy axis.
