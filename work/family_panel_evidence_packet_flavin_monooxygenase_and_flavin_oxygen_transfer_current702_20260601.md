# Family Panel Evidence Packet - flavin_monooxygenase_and_flavin_oxygen_transfer

Run: 2026-06-01T09:47:29Z

Review-only evidence packet for the highest-value family-set expansion panel `flavin_monooxygenase_and_flavin_oxygen_transfer`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_review_only
- Candidate rows: 4
- Predicted geometry ok rows: 4

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:131 | metal_dependent_hydrolase | 0.3522 | 0.980908 | None | 0.751 | -1.376203 |
| m_csa:132 | ser_his_acid_hydrolase | 0.3894 | 0.010805 | None | 0.6879 | None |
| m_csa:551 | metal_dependent_hydrolase | 0.3583 | 0.922628 | None | 0.7309 | -1.385598 |
| m_csa:973 | metal_dependent_hydrolase | 0.3625 | 0.993434 | None | None | None |

## Review Questions

- Do these rows share a coherent `flavin_monooxygenase_and_flavin_oxygen_transfer` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
