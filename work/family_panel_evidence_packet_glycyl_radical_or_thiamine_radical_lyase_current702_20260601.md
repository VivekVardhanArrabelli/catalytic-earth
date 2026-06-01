# Family Panel Evidence Packet - glycyl_radical_or_thiamine_radical_lyase_boundary

Run: 2026-06-01T14:02:02Z

Review-only evidence packet for the highest-value family-set expansion panel `glycyl_radical_or_thiamine_radical_lyase_boundary`: cofactor-confounded OOS boundary rows that stress the current de novo abstention gate.

## Status

- evidence_packet_ready_review_only
- Candidate rows: 2
- Predicted geometry ok rows: 2

## Row Evidence

| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:30 | metal_dependent_hydrolase | 0.2616 | 0.589255 | 0.057 | 0.4988 | -2.309839 |
| m_csa:31 | metal_dependent_hydrolase | 0.3466 | 0.808565 | 0.014 | 0.3809 | -1.399238 |

## Review Questions

- Do these rows share a coherent `glycyl_radical_or_thiamine_radical_lyase_boundary` mechanism locus, or should they stay OOS controls?
- Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?
- Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?

## Next Actions

- use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic
- source-check mechanism locus and bond-change evidence before any panel promotion discussion
- keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized
