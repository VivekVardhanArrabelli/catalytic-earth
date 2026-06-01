# Family Panel Evidence Packet - cobalamin_and_radical_rearrangement_panel

Run: 2026-06-01T15:22:47Z

Review-only evidence packet for the highest-value family-set expansion panel `cobalamin_and_radical_rearrangement_panel`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_with_geometry_gaps
- Candidate rows: 3
- Predicted geometry ok rows: 2

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| secondary_probe::cobalamin_radical_rearrangement | None | None | None | None | 0.4655 | None |
| secondary_probe::radical_sam_enzyme | metal_dependent_hydrolase | 0.2628 | None | None | 0.7039 | None |
| m_csa:750 | metal_dependent_hydrolase | 0.3664 | 0.703989 | None | 0.7357 | -1.465543 |

## Review Questions

- Do these rows share a coherent `cobalamin_and_radical_rearrangement_panel` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
