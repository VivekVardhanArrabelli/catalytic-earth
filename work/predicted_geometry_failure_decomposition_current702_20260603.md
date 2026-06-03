# Predicted Geometry Failure Decomposition

Backend: `alphafold_db` | source audit: `v3_predicted_geometry_robustness_audit_current702_20260529`

## Why do predicted-geometry primary calls degrade?

- Lost primary rows: 22 (by mode: {'cofactor_apo_loss': 22})
- Wave 1 readthrough (excl. m_csa:497/750): 20 (by mode: {'cofactor_apo_loss': 20})
- OOS/secondary false positives: 10 (by mode: {'cofactor_apo_loss': 7, 'fold_or_sidechain': 3})

## Control

- Correct primaries: 23, of which 13 had an experimental cofactor (apo geometry can suffice for some rows).

## ESMFold2 ceiling

- Fold/side-chain-limited (a better apo folder could plausibly recover): 0
- Cofactor-apo-loss (ESMFold2 cannot recover, it is also apo): 22

ESMFold2 is also apo, so it cannot supply the missing cofactor. 22 of 22 lost primary rows are cofactor_apo_loss and cannot be recovered by swapping in ESMFold2 coordinates; only 0 are fold/side-chain limited (the rows a better apo folder could plausibly recover). The degradation is cofactor-loss-dominated, so the primary lever is cofactor-awareness, not a better apo folder. ESMFold2's plausible contributions are OOS false-positive reduction (better apo pocket packing) and pLDDT-gated abstention, not primary recovery.

This is a descriptive readout: it categorizes outcomes already computed by the robustness audit, selects no threshold, and fits no model.
