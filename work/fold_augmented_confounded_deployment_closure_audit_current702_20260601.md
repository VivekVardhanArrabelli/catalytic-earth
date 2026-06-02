# Fold-Augmented Confounded Deployment Closure Audit - current702

Run: 2026-06-02T07:29:36Z

Validation-only Lever 3 synthesis for the predicted-structure-vs-atlas fold channel at the fixed OOS-calibrated operating point, focused on the six cofactor-confounded heldout OOS rows.

## Status

- confounded_fold_channel_research_ready_production_blocked
- Fixed threshold: combined_mean_geometry_fold >= 0.44155
- Confounded heldout OOS abstained: 5/6
- Heldout in-scope retain recall: 0.9574
- Remaining production blocker rows: 5

## Confounded Rows

| row | nearest atlas | atlas fingerprint | TM |
| --- | --- | --- | ---: |
| m_csa:30 | m_csa:11 | metal_dependent_hydrolase | 0.4988 |
| m_csa:31 | m_csa:900 | ser_his_acid_hydrolase | 0.3809 |
| m_csa:80 | m_csa:973 | flavin_dehydrogenase_reductase | 0.5109 |
| m_csa:191 | m_csa:631 | ser_his_acid_hydrolase | 0.3863 |
| m_csa:267 | m_csa:800 | flavin_dehydrogenase_reductase | 0.7389 |
| m_csa:448 | m_csa:528 | metal_dependent_hydrolase | 0.5106 |

## Production Blockers

| row | blocker | fold-only evidence | next action |
| --- | --- | ---: | --- |
| m_csa:78 | alphafold_db_coordinate_unavailable | False | Find a source-backed alternate accession with compatible catalytic residues and an AFDB model, or explicitly authorize an experimental-coordinate-only calibration diagnostic separate from the predicted fold channel. |
| m_csa:204 | experimental_geometry_not_ok:None | True | Source a row-specific active-site residue/interaction sidecar for uroporphyrinogen-III synthase, or keep this row fold-only in calibration diagnostics. |
| m_csa:531 | experimental_geometry_not_ok:insufficient_resolved_residues | True | Source additional residue or interaction evidence for L-carnitine CoA-transferase, or keep this row fold-only until a source-backed sidecar exists. |
| uniprot:P78549 | not_m_csa_entry | True | Create a source-backed active-site sidecar for P78549 if an external hard-negative geometry channel is authorized; otherwise keep fold-only evidence separate. |
| uniprot:Q3LXA3 | not_m_csa_entry | True | Create a source-backed active-site sidecar for Q3LXA3 if an external hard-negative geometry channel is authorized; otherwise keep fold-only evidence separate. |

## Interpretation

- The predicted-structure-vs-atlas fold channel is contract-passing and hits the confounded subset research target at the fixed operating point: 5/6 cofactor-confounded heldout OOS rows abstain while in-scope retention is preserved.
- For production-like closure, clear m_csa:78, m_csa:204, m_csa:531, uniprot:P78549, and uniprot:Q3LXA3, or create an explicit fold-only contract for the rows that already have Foldseek/TM evidence.
