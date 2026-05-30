# Sequence Cofactor-Channel Probe

Run: 2026-05-29T22:54:19Z

## Answer

- Yes for one-vs-rest cofactor class-presence labels on metal/flavin/PLP/heme; not yet for a clean exact single-label multiclass probe including heme.
- Recommendation: Run the real sequence cofactor-channel probe next with local ESM-2/ProtT5 or Pfam/motif features using one-vs-rest cofactor presence labels; do not clean labels by mechanism fingerprint cofactors because that is circular with the mechanism target.

## Clean Label Balance

| Class | Presence train | Presence heldout | Exact train | Exact heldout |
| --- | ---: | ---: | ---: | ---: |
| metal_ion | 146 | 29 | 136 | 25 |
| flavin | 40 | 11 | 37 | 9 |
| plp | 24 | 6 | 21 | 6 |
| heme | 18 | 5 | 13 | 3 |
| none | - | - | 297 | 80 |

- Clean geometry label rows: 682/702.
- Runnable one-vs-rest presence classes: ['metal_ion', 'flavin', 'plp', 'heme'].
- Exact multiclass runnable now: False.
- ESM-2 vectors available: True.

## K-mer Control Probe

- Joined clean rows: 682; train 547; heldout 135.
| Class | ROC AUC | Avg precision | Balanced accuracy | TP | FP | FN | TN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| metal_ion | 0.481457 | 0.234538 | 0.518055 | 15 | 51 | 14 | 55 |
| flavin | 0.470674 | 0.082814 | 0.460044 | 4 | 55 | 7 | 69 |
| plp | 0.613695 | 0.088167 | 0.5 | 2 | 43 | 4 | 86 |
| heme | 0.807692 | 0.16128 | 0.673077 | 3 | 33 | 2 | 97 |

## Caveats

- Mechanism-fingerprint-derived cofactors have stronger support but are circular with the current mechanism labels.
- Raw M-CSA compound identities are not retained in the graph; `compound_count` is retained only as a count.
- Empty local cofactor context is selected-structure evidence, not a guaranteed biological no-cofactor label.
- The k-mer probe is a local control only; the real next probe needs local ESM-2/ProtT5 or Pfam/motif features.
