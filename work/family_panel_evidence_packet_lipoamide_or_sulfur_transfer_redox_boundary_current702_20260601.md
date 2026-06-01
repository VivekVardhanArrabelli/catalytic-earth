# Family Panel Evidence Packet - lipoamide_or_sulfur_transfer_redox_boundary

Run: 2026-06-01T05:04:22Z

Review-only evidence packet for the highest-value family-set expansion panel `lipoamide_or_sulfur_transfer_redox_boundary`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_review_only
- Candidate rows: 2
- Predicted geometry ok rows: 2

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:267 | heme_peroxidase_oxidase | 0.3969 | 0.834847 | 0.0 | 0.7389 | -1.475892 |
| m_csa:448 | metal_dependent_hydrolase | 0.3576 | 0.904927 | 0.0 | 0.5106 | -1.350762 |

## Review Questions

- Do these rows share a coherent `lipoamide_or_sulfur_transfer_redox_boundary` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
