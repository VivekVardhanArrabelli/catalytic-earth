# Family Panel Evidence Packet - thiol_disulfide_oxidoreductase_isomerase_boundary

Run: 2026-06-01T07:44:28Z

Review-only evidence packet for the highest-value family-set expansion panel `thiol_disulfide_oxidoreductase_isomerase_boundary`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_review_only
- Candidate rows: 1
- Predicted geometry ok rows: 1

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:191 | metal_dependent_hydrolase | 0.3718 | 0.555321 | 0.0 | 0.3863 | -1.800092 |

## Review Questions

- Do these rows share a coherent `thiol_disulfide_oxidoreductase_isomerase_boundary` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
