# Fold-Augmented Train/Cal OOS Remaining Blocker Clearance Attempts - current702

Run: 2026-06-01T08:00:00Z

Bounded row-level clearance attempts for the five remaining train/cal OOS-negative fold-augmented score-surface blockers after the 71/76 sufficiency decision.

## Status

- clearance_attempts_staged_no_safe_repo_mutation
- Remaining blocker rows: 5
- Safe repairs applied: 0
- Rows with fold-only evidence: 4

## Row Attempts

| Entry | blocker | fold-only evidence | result | next action |
| --- | --- | ---: | --- | --- |
| m_csa:78 | alphafold_db_coordinate_unavailable | False | blocked | Find a source-backed alternate accession with compatible catalytic residues and an AFDB model, or explicitly authorize an experimental-coordinate-only calibration diagnostic separate from the predicted fold channel. |
| m_csa:204 | experimental_geometry_not_ok:None | True | blocked | Source a row-specific active-site residue/interaction sidecar for uroporphyrinogen-III synthase, or keep this row fold-only in calibration diagnostics. |
| m_csa:531 | experimental_geometry_not_ok:insufficient_resolved_residues | True | blocked | Source additional residue or interaction evidence for L-carnitine CoA-transferase, or keep this row fold-only until a source-backed sidecar exists. |
| uniprot:P78549 | not_m_csa_entry | True | blocked | Create a source-backed active-site sidecar for P78549 if an external hard-negative geometry channel is authorized; otherwise keep fold-only evidence separate. |
| uniprot:Q3LXA3 | not_m_csa_entry | True | blocked | Create a source-backed active-site sidecar for Q3LXA3 if an external hard-negative geometry channel is authorized; otherwise keep fold-only evidence separate. |

## Interpretation

- No remaining blocker can be safely cleared from current frozen inputs without adding new source-backed active-site evidence or an alternate predicted coordinate.
- Proceed with the research-sufficient 71/76 surface for downstream diagnostics; clear blockers only when new source evidence or an explicitly authorized coordinate policy is available.
