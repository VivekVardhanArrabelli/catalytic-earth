# Fold-Augmented Confounded Proxy Train/Cal Protein-Only Fold-Topology Residual Contract

Run: 2026-06-03T19:31:45Z

Pre-registration contract for a train/cal-only protein-only fold-topology residual axis. It selects rows and feature rules only; it does not run Foldseek, parse scores, register a deployable threshold, or read heldout.

## Status

- fold_augmented_confounded_proxy_train_cal_protein_only_fold_topology_residual_contract_ready
- Contract rows: 8
- Query coordinate files observed/missing: 8/0
- Ready to build scoring-input rows: 8
- Ready-to-score-now rows: 0
- Blockers: []

## Decision

- Contract pre-registered: True
- Build scoring-input manifest next: True
- Score contract rows now: False
- Register deployable axis now: False
- Next gate: Build a scoring-input manifest for these eight train/cal rows against the train atlas, run Foldseek/TM scoring, and parse only numeric topology residual features. Do not use nearest-hit IDs, labels, target names, or heldout rows as predictive features.

## Contract Rows

| entry | accession | split | coordinate exists |
| --- | --- | --- | --- |
| m_csa:610 | P15807 | train_cal | True |
| m_csa:137 | P18548 | train_cal | True |
| m_csa:318 | P27000 | train_cal | True |
| m_csa:360 | P68175 | train_cal | True |
| m_csa:105 | Q46509 | train_cal | True |
| m_csa:327 | Q56310 | train_cal | True |
| m_csa:649 | Q7SIE1 | train_cal | True |
| m_csa:618 | Q9P4R4 | train_cal | True |

## Interpretation

- A protein-only fold-topology residual contract is pre-registered for the eight unsupported-geometry train/cal rows.
- 8 train/cal rows have local AFDB query coordinates and can be moved to a scoring-input manifest; no row was scored by this contract.
- Build the scoring-input manifest and run the numeric predicted-structure-vs-atlas scoring pass before any threshold or fixed-audit claim.
