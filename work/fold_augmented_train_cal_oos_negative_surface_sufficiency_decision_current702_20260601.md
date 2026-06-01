# Fold-Augmented Train/Cal OOS Surface Sufficiency Decision - current702

Run: 2026-06-01T07:54:42Z

Bounded decision artifact for whether the partial train/cal OOS-negative fold-augmented score surface is sufficient for the current research gate.

## Decision

- research_contract_sufficient_with_blocker_disclosure
- Research sufficient: True
- Production sufficient: False
- Reason: Coverage is above the 90% bounded research bar, the OOS-calibrated contract consumes exactly the score-complete rows, accession-compatible mapping blockers are cleared, and the primary threshold remains the same as the prior in-scope-only contract.

## Counts

- Score-complete rows: 71 / 76 (0.934211)
- Fold-only salvage rows: 4
- Blocker reason counts: {'alphafold_db_coordinate_unavailable': 1, 'experimental_geometry_not_ok:None': 1, 'experimental_geometry_not_ok:insufficient_resolved_residues': 1, 'not_m_csa_entry': 2}
- Calibration OOS used by contract: 71

## Threshold Readout

- Primary channel: combined_mean_geometry_fold
- Prior in-scope threshold: 0.44155
- OOS-calibrated threshold: 0.44155
- Heldout in-scope retention: 0.9574
- Heldout OOS abstain recall: 0.557
- Heldout confounded-OOS abstain recall: 0.8333

## Remaining Blockers

| Entry | reason | fold TM available | action |
| --- | --- | --- | --- |
| m_csa:78 | alphafold_db_coordinate_unavailable | False | verify replacement accession or alternate local coordinate source; AFDB has no v1-v6 model for this accession |
| m_csa:204 | experimental_geometry_not_ok:None | True | repair source geometry evidence or keep row excluded from geometry-calibrated OOS surface |
| m_csa:531 | experimental_geometry_not_ok:insufficient_resolved_residues | True | repair source geometry evidence or keep row excluded from geometry-calibrated OOS surface |
| uniprot:P78549 | not_m_csa_entry | True | provide an active-site residue sidecar for UniProt-only rows or score them in a fold-only negative surface |
| uniprot:Q3LXA3 | not_m_csa_entry | True | provide an active-site residue sidecar for UniProt-only rows or score them in a fold-only negative surface |

## Next Action

- Treat the 71/76 surface as sufficient for the bounded research contract and do not block downstream diagnostics on the remaining five disclosed coordinate/source-geometry/sidecar gaps. Clear those blockers before any stronger production or production-like threshold claim.
