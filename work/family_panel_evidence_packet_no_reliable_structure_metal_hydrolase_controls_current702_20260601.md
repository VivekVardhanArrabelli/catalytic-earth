# Family Panel Evidence Packet - no_reliable_structure_metal_hydrolase_controls

Run: 2026-06-01T15:21:02Z

Review-only evidence packet for the highest-value family-set expansion panel `no_reliable_structure_metal_hydrolase_controls`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_with_geometry_gaps
- Candidate rows: 6
- Predicted geometry ok rows: 1

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| mh_064 | None | None | None | None | 0.9222 | None |
| mh_065 | None | None | None | None | 0.9411 | None |
| mh_066 | metal_dependent_hydrolase | 0.3822 | None | None | 0.9445 | None |
| mh_067 | None | None | None | None | 1.004 | None |
| mh_068 | None | None | None | None | 1.002 | None |
| mh_072 | None | None | None | None | 0.5936 | None |

## Review Questions

- Do these rows share a coherent `no_reliable_structure_metal_hydrolase_controls` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
