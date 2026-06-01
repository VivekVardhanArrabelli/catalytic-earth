# Family Panel Evidence Packet - near_orphan_glycoside_or_nucleoside_hydrolase_controls

Run: 2026-06-01T11:03:57Z

Review-only evidence packet for the highest-value family-set expansion panel `near_orphan_glycoside_or_nucleoside_hydrolase_controls`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_with_geometry_gaps
- Candidate rows: 4
- Predicted geometry ok rows: 2

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:10 | heme_peroxidase_oxidase | 0.356 | 0.017518 | None | 0.4733 | -1.534108 |
| m_csa:116 | metal_dependent_hydrolase | 0.3734 | 0.050535 | None | 0.5417 | None |
| mh_073 | None | None | None | None | 0.8022 | None |
| external_glycoside_panel | None | None | None | None | 0.6259 | None |

## Review Questions

- Do these rows share a coherent `near_orphan_glycoside_or_nucleoside_hydrolase_controls` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
